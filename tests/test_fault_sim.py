"""Kiem thu mo phong loi, coverage, nen tap test, CLI - P6."""
import os
from itertools import product

from atpg import run
from atpg.circuit import Circuit
from atpg.fault_sim import (compact, coverage, coverage_parallel, detects, detects_cube,
                            detects_unknown_state, exhaustive_test, simulate, simulate_parallel)
from atpg.faults import Fault, all_faults, collapse

ROOT = os.path.dirname(os.path.dirname(__file__))
C17 = os.path.join(ROOT, "circuits", "c17.bench")
F11 = Fault("11", 0)


def c17():
    return Circuit.from_bench(C17)


def vec(c, s):
    return dict(zip(c.inputs, s))


def test_good_simulation():
    c = c17()
    v = simulate(c, vec(c, "11111"))
    assert (v["10"], v["11"], v["16"], v["19"], v["22"], v["23"]) == (0, 0, 1, 1, 1, 0)


def test_x_filled_with_zero():
    c = c17()
    assert simulate(c, vec(c, "X10XX")) == simulate(c, vec(c, "01000"))


def test_11sa0_hand_vectors():
    c = c17()
    assert detects(c, vec(c, "01000"), F11)           # trace tay: 11=D, 16=D', 22=D
    assert detects(c, vec(c, "00001"), F11)           # lan truyen qua 19 -> 23
    assert not detects(c, vec(c, "00110"), F11)       # 3.6 = 1 nen khong kich hoat duoc loi
    v = simulate(c, vec(c, "01000"), F11)
    assert v["11"] == 0 and v["16"] == 1 and v["22"] == 0 and v["23"] == 0


def test_eighteen_vectors_detect_11sa0():
    c = c17()
    n = sum(detects(c, vec(c, bits), F11) for bits in product((0, 1), repeat=5))
    assert n == 18


def test_cube_all_fills():
    c = c17()
    assert detects_cube(c, vec(c, "X10XX"), F11)
    assert not detects_cube(c, vec(c, "XXXXX"), F11)


def test_branch_fault_differs_from_stem():
    c = c17()
    p = vec(c, "01001")
    good = simulate(c, p)
    stem = simulate(c, p, Fault("11", 0))
    branch = simulate(c, p, Fault("11", 0, "16"))      # chi nhanh di vao cong 16 bi ket
    assert good["19"] == 0 and stem["19"] == 1         # stem loi lam doi ca nhanh 19
    assert branch["19"] == 0 and branch["16"] == 1     # nhanh loi chi anh huong cong 16


def test_multi_site_fault_list():
    c = c17()
    both = simulate(c, vec(c, "01001"), [Fault("10", 0), Fault("19", 1)])
    assert both["10"] == 0 and both["19"] == 1


def test_coverage_full_and_dropping():
    c = c17()
    pats = [dict(zip(c.inputs, b)) for b in product((0, 1), repeat=5)]
    faults = all_faults(c)
    r = coverage(c, pats, faults)
    assert r["total"] == 34 and r["detected"] == 34 and r["coverage"] == 100.0
    assert coverage(c, pats[:1], faults)["coverage"] < 100.0
    assert coverage(c, [], faults)["detected"] == 0


def test_parallel_matches_serial():
    c = c17()
    pats = [dict(zip(c.inputs, b)) for b in product((0, 1), repeat=5)]
    faults = all_faults(c)
    a, b = coverage(c, pats, faults), coverage_parallel(c, pats, faults)
    assert a["detected_by"] == b["detected_by"]
    sp = simulate_parallel(c, pats)
    for k, p in enumerate(pats):
        s = simulate(c, p)
        assert all(((sp[n] >> k) & 1) == s[n] for n in c.nets)


def test_compact_keeps_coverage_and_shrinks():
    c = c17()
    pats = [dict(zip(c.inputs, b)) for b in product((0, 1), repeat=5)]
    faults = collapse(c, all_faults(c))
    kept = compact(c, pats, faults)
    assert len(kept) < len(pats)
    assert coverage(c, kept, faults)["coverage"] == 100.0


def test_exhaustive_reference_valid_for_every_fault():
    c = c17()
    for f in all_faults(c):
        cube, exhausted = exhaustive_test(c, f)
        assert exhausted and cube is not None and detects_cube(c, cube, f)


def test_cli_single_fault(capsys):
    assert run.main([C17, "--fault", "11", "0", "--trace"]) == 0
    out = capsys.readouterr().out
    assert "11/SA0" in out and "DETECTED" in out and "| 11 |" in out


def test_cli_all(tmp_path, capsys):
    md = tmp_path / "r.md"
    assert run.main([C17, "--all", "--md", str(md)]) == 0
    text = md.read_text(encoding="utf-8")
    assert "34" in text and "22" in text and "100.0%" in text


# ---------- phan vi du cua nhom P1: khong xac nhan "moi cach dien X" chi bang hai lan thu ----------
def xor_circuit(tmp_path):
    """a, x0..x12 -> eq = XNOR(x0,x1); y = AND(a, eq). Loi a/SA0 can x0 == x1."""
    xs = [f"x{i}" for i in range(13)]
    lines = ["INPUT(a)"] + [f"INPUT({x})" for x in xs] + ["OUTPUT(y)", "eq = XNOR(x0, x1)", "y = AND(a, eq)"]
    f = tmp_path / "xor.bench"
    f.write_text("\n".join(lines) + "\n")
    return f, Circuit.from_bench(str(f)), Fault("a", 0)


def test_detects_cube_not_true_from_two_fills(tmp_path):
    _, c, f = xor_circuit(tmp_path)
    cube = {k: "X" for k in c.inputs}
    cube["a"] = "1"
    # tat ca X=0 va tat ca X=1 deu phat hien, nhung x0=0,x1=1 thi khong
    assert detects(c, {k: (1 if k == "a" else 0) for k in c.inputs}, f)
    assert detects(c, {k: 1 for k in c.inputs}, f)
    assert not detects(c, {**{k: 0 for k in c.inputs}, "a": 1, "x1": 1}, f)
    assert detects_cube(c, cube, f, max_x=12) is None      # qua gioi han: KHONG duoc tra True
    assert detects_cube(c, cube, f, max_x=16) is False     # vet can: tim ra phan vi du


def test_exhaustive_test_relaxes_only_proven_bits(tmp_path):
    _, c, f = xor_circuit(tmp_path)
    cube, exhausted = exhaustive_test(c, f)
    assert exhausted and cube["a"] == "1"
    assert cube["x0"] != "X" and cube["x1"] != "X"          # x0 == x1 la dieu kien bat buoc
    assert all(cube[f"x{i}"] == "X" for i in range(2, 13))
    assert detects_cube(c, cube, f, max_x=len(c.inputs)) is True


def test_cli_pattern_wording_for_x_counterexample(tmp_path, capsys):
    path, c, f = xor_circuit(tmp_path)
    pat = "1" + "X" * 13
    run.main([str(path), "--fault", "a", "0", "--pattern", pat])
    out = capsys.readouterr().out
    assert "KHONG phat hien voi moi cach dien X" in out and "PHAT HIEN voi moi cach" not in out
    run.main([str(path), "--fault", "a", "0", "--pattern", pat, "--max-x", "12"])
    out = capsys.readouterr().out
    assert "CHUA KIEM CHUNG HET" in out and "PHAT HIEN voi moi cach" not in out


def test_cli_verify_column_for_unproven_cube(tmp_path):
    _, c, f = xor_circuit(tmp_path)
    cube = {k: "X" for k in c.inputs}
    cube["a"] = "1"
    res = run.GenResult(f, "DETECTED", cube, "-", "test")
    assert run.verify(c, res, 16) == ("OK", "khong")
    assert run.verify(c, res, 12)[1].startswith("chua kiem chung het")


def test_unknown_state_vs_controllable_state(tmp_path):
    from atpg.circuit import Gate
    c = Circuit.from_gates("st", ["A", "S"], ["Y"], [Gate("Y", "AND", ["S", "A"])])
    f = Fault("Y", 0)
    p = {"A": "1", "S": "1"}
    assert detects(c, p, f)                                   # neu S dieu khien duoc va = 1
    assert detects_unknown_state(c, p, f, ["S"]) is False     # S chua biet: khong bao dam


def test_generate_test_falls_back_only_when_podem_unsupported():
    import pytest
    c = c17()

    def unsupported(circ, fault, max_backtracks=1000, trace=False):
        raise ValueError("Backtrace chưa hỗ trợ loại cổng: XOR")

    def internal_bug(circ, fault, max_backtracks=1000, trace=False):
        raise ValueError("Không còn input X để backtrace từ net 16.")

    run.PODEM_ERRORS.clear()
    r = run.generate_test(c, F11, unsupported)
    assert r.status == "DETECTED" and r.algo == "vet can (PODEM chua ho tro)"
    assert "XOR" in run.podem_error_note()
    with pytest.raises(ValueError, match="backtrace"):     # loi noi bo: khong duoc che bang vet can
        run.generate_test(c, F11, internal_bug)
    run.PODEM_ERRORS.clear()


def test_podem_agrees_with_independent_fault_sim_on_c17():
    """Chi chay khi podem.py cua P5 co mat: moi pattern PODEM phai duoc fault simulation xac nhan."""
    pytest = __import__("pytest")
    podem = pytest.importorskip("atpg.podem").podem
    c = c17()
    for fault in collapse(c, all_faults(c)):
        r = run.generate_test(c, fault, podem)
        assert r.algo == "PODEM" and r.status == "DETECTED", str(fault)
        assert run.verify(c, r, 16) == ("OK", "co"), str(fault)
