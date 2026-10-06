"""Kiem thu mo phong loi, coverage, nen tap test, CLI - P6."""
import os
from itertools import product

from atpg import run
from atpg.circuit import Circuit
from atpg.fault_sim import (compact, coverage, coverage_parallel, detects, detects_cube,
                            exhaustive_test, simulate, simulate_parallel)
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
