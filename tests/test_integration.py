"""P6-03: tich hop THAT PODEM (P5) + unroll (P4) + fault simulator (P6).
Khong dung fixture ep _load_podem=None; neu thieu podem.py thi cac test PODEM bi skip (khong pass gia)."""
import os
from argparse import Namespace
from itertools import product

import pytest

from atpg import run
from atpg.circuit import Circuit
from atpg.fault_sim import compact, coverage, detects, detects_cube, simulate
from atpg.faults import Fault, all_faults, collapse

ROOT = os.path.dirname(os.path.dirname(__file__))
C17 = os.path.join(ROOT, "circuits", "c17.bench")
SEQ = os.path.join(ROOT, "circuits", "seq_example.bench")
AUX = os.path.join(ROOT, "circuits", "backtrack_example.bench")
ARGS = Namespace(max_backtracks=1000, trace=False, max_x=16)


@pytest.fixture
def podem_spy():
    """PODEM that cua P5, boc them bo dem de chung minh duong PODEM thuc su duoc goi."""
    podem = pytest.importorskip("atpg.podem").podem
    calls = []

    def spy(c, fault, max_backtracks=1000, trace=False):
        calls.append(fault)
        return podem(c, fault, max_backtracks=max_backtracks, trace=trace)

    spy.calls = calls
    run.PODEM_ERRORS.clear()
    yield spy
    assert not run.PODEM_ERRORS, f"PODEM bao loi, da phai fallback: {run.PODEM_ERRORS}"


def test_cli_loads_real_podem():
    pytest.importorskip("atpg.podem")
    assert run._load_podem() is not None


# ---------------- c17 ----------------
@pytest.mark.parametrize("collapsed, n_faults, n_kept", [(True, 22, 6), (False, 34, 7)])
def test_c17_all_faults_by_podem(podem_spy, collapsed, n_faults, n_kept):
    c = Circuit.from_bench(C17)
    universe = all_faults(c)
    faults = collapse(c, universe) if collapsed else universe
    assert len(faults) == n_faults
    pats = []
    for f in faults:
        r = run.generate_test(c, f, podem_spy)
        assert r.algo == "PODEM" and r.status == "DETECTED" and r.backtracks == 0, str(f)
        cube = {i: r.pattern.get(i, "X") for i in c.inputs}
        assert detects_cube(c, cube, f) is True, str(f)        # moi cach dien X
        pats.append(run.fill0(c, r.pattern))
    assert len(podem_spy.calls) == n_faults                    # khong pass nho fallback
    kept = compact(c, pats, faults)
    assert len(kept) == n_kept
    assert coverage(c, kept, universe)["detected"] == 34        # tap nen phu ca 34 loi goc


def test_c17_11sa0_matches_golden_trace(podem_spy):
    """Golden trace P3: (11,1) -> 3=0, (2,1) -> 2=1; X10XX; 0 backtrack; 7 cot trace."""
    c = Circuit.from_bench(C17)
    r = podem_spy(c, Fault("11", 0), trace=True)
    assert r.status == "DETECTED" and r.backtracks == 0
    assert "".join(r.pattern[i] for i in c.inputs) == "X10XX"
    assert len(r.steps) == 2 and len(r.steps[0]) == 7
    first, second = r.steps
    assert first["Objective (net, giá trị)"] == ("11", 1) and first["Backtrace → PI"] == ("3", 0)
    assert second["Objective (net, giá trị)"] == ("2", 1) and second["Hành động"] == "thành công"


def test_backtrack_example_from_p3(podem_spy):
    """Mach phu P3, t/SA0: a=1 that bai, dao a=0, roi b=1; 1 backtrack; gioi han 0 -> ABORTED."""
    c = Circuit.from_bench(AUX)
    f = Fault("t", 0)
    r = podem_spy(c, f, max_backtracks=1, trace=True)
    assert r.status == "DETECTED" and r.backtracks == 1 and r.pattern == {"a": "0", "b": "1"}
    assert [s["Hành động"] for s in r.steps] == ["tiếp tục", "backtrack", "thành công"]
    assert podem_spy(c, f, max_backtracks=0).status == "ABORTED"   # ABORTED, khong phai UNTESTABLE
    found = [bits for bits in product((0, 1), repeat=2) if detects(c, dict(zip(c.inputs, bits)), f)]
    assert found == [(0, 1)]                                       # 01 duy nhat trong 4 vector


# ---------------- mach tuan tu: PODEM + unroll that ----------------
@pytest.mark.parametrize("k, guaranteed, conditional, untestable", [(1, 1, 9, 8), (2, 13, 5, 0), (3, 18, 0, 0)])
def test_sequential_with_real_podem_and_unroll(podem_spy, k, guaranteed, conditional, untestable):
    from atpg.unroll import fault_in_frames, unroll
    base = Circuit.from_bench(SEQ)
    c = unroll(base, k)
    states = [f"{g.output}@0" for g in base.dffs]
    faults = [Fault(n, sv) for n in base.nets for sv in (0, 1)]
    assert len(faults) == 18 and all(f.branch_to is None for f in faults)
    kinds, statuses, from_podem = [], [], 0
    for f in faults:
        frames = fault_in_frames(f, k)
        assert [x.net for x in frames] == [f"{f.net}@{t}" for t in range(k)]   # cay o moi khung
        assert all(x.stuck_at == f.stuck_at for x in frames)
        r, kind = run.seq_generate(c, tuple(frames), podem_spy, states, ARGS)
        kinds.append(kind)
        statuses.append(r.status)
        from_podem += kind == "bao dam" and r.algo == "PODEM"
    assert len(podem_spy.calls) == 18                              # PODEM duoc goi cho moi loi
    assert kinds.count("bao dam") == guaranteed
    assert kinds.count("co dieu kien") == conditional
    assert statuses.count("UNTESTABLE") == untestable
    assert not any(s.startswith("KIEM CHUNG SAI") for s in statuses)
    if k >= 2:
        assert from_podem >= 1                                     # co chuoi bao dam lay truc tiep tu PODEM


def test_cli_sequential_demo_uses_podem(capsys):
    pytest.importorskip("atpg.podem")
    assert run.main([SEQ, "--unroll", "2", "--all"]) == 0
    out = capsys.readouterr().out
    assert "| PODEM |" in out and "13/18 = 72.2%" in out


# ---------------- xac nhan vector cua P2/P3 (khong can PODEM) ----------------
def fills(cube):
    xs = [i for i, v in enumerate(cube) if v == "X"]
    for bits in product("01", repeat=len(xs)):
        s = list(cube)
        for i, b in zip(xs, bits):
            s[i] = b
        yield "".join(s)


@pytest.mark.parametrize("cube, n", [("X100X", 4), ("X10XX", 8)])
def test_p2_cubes_detect_11sa0_at_po22(cube, n):
    """P2: 4/4 cach dien (X,1,0,0,X) va 8/8 cach dien (X,1,0,X,X) phat hien 11/SA0 tai 22."""
    c = Circuit.from_bench(C17)
    f = Fault("11", 0)
    vecs = list(fills(cube))
    assert len(vecs) == n
    for v in vecs:
        p = dict(zip(c.inputs, v))
        assert simulate(c, p)["22"] != simulate(c, p, f)["22"], v


def test_vector_01000_outputs():
    """01000: mach tot (22,23) = (1,1), mach loi 11/SA0 = (0,0)."""
    c = Circuit.from_bench(C17)
    p = dict(zip(c.inputs, "01000"))
    good, bad = simulate(c, p), simulate(c, p, Fault("11", 0))
    assert (good["22"], good["23"]) == (1, 1) and (bad["22"], bad["23"]) == (0, 0)
