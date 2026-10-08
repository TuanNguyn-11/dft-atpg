"""So sanh D-algorithm va PODEM (P6): D-algorithm dung, khop chay tay P2, CLI so sanh."""
import csv
import os
import random

import pytest

from atpg import compare
from atpg.circuit import Circuit, Gate
from atpg.dalg import d_algorithm
from atpg.fault_sim import detects_cube, exhaustive_test
from atpg.faults import Fault, all_faults

ROOT = os.path.dirname(os.path.dirname(__file__))
C17 = os.path.join(ROOT, "circuits", "c17.bench")
AUX = os.path.join(ROOT, "circuits", "backtrack_example.bench")
SEQ = os.path.join(ROOT, "circuits", "seq_example.bench")


def c17():
    return Circuit.from_bench(C17)


# ---------------- D-algorithm ----------------
def test_dalg_c17_11sa0_matches_p2_hand_trace():
    """Chuong 3 (P2): PDCF (3,6,11)=(X,0,D); PDC qua 16 (2=1); PDC qua 22 (10=1), J={10};
    cover (1,3,10)=(X,0,1); cube (X,1,0,0,X); 4 lan chon cube, 0 backtrack."""
    c = c17()
    r = d_algorithm(c, Fault("11", 0), trace=True)
    assert r.status == "DETECTED" and r.decisions == 4 and r.backtracks == 0
    assert "".join(r.pattern[i] for i in c.inputs) == "X100X"
    assert [(s["Loại"], s["Cổng"]) for s in r.steps] == [("PDCF", "11"), ("PDC", "16"), ("PDC", "22"),
                                                          ("Cover", "10")]
    assert r.steps[0]["Giá trị các net"]["6"] == "0" and r.steps[0]["Giá trị các net"]["11"] == "D"
    assert r.steps[1]["Giá trị các net"]["16"] == "D'"
    assert r.steps[2]["J-frontier"] == ["10"] and r.steps[3]["J-frontier"] == []
    assert r.steps[3]["Giá trị các net"]["3"] == "0" and r.steps[-1]["Hành động"] == "thành công"
    assert sorted(r.internal_assigned) == ["10", "11", "16", "22"]
    assert detects_cube(c, r.pattern, Fault("11", 0)) is True


def test_dalg_backtrack_depends_on_order():
    c = Circuit.from_bench(AUX)
    last = d_algorithm(c, Fault("t", 0), order="last")
    first = d_algorithm(c, Fault("t", 0), order="first", trace=True)
    assert last.pattern == first.pattern == {"a": "0", "b": "1"}
    assert last.backtracks == 0 and first.backtracks == 1
    assert [s["Hành động"] for s in first.steps] == ["kích hoạt", "backtrack", "kích hoạt", "thành công"]
    assert d_algorithm(c, Fault("t", 0), order="first", max_backtracks=0).status == "ABORTED"


@pytest.mark.parametrize("order", ["last", "first"])
def test_dalg_all_c17_faults_verified(order):
    c = c17()
    for f in all_faults(c):
        r = d_algorithm(c, f, order=order)
        assert r.status == "DETECTED", str(f)
        assert detects_cube(c, r.pattern, f) is True, str(f)


def test_dalg_untestable_and_aborted():
    """y = a OR (a AND b): loi m/SA0 du thua (khong the phat hien)."""
    c = Circuit.from_gates("red", ["a", "b"], ["y"], [Gate("m", "AND", ["a", "b"]), Gate("y", "OR", ["a", "m"])])
    assert exhaustive_test(c, Fault("m", 0)) == (None, True)
    assert d_algorithm(c, Fault("m", 0)).status == "UNTESTABLE"
    assert d_algorithm(c, Fault("m", 0), max_backtracks=0).status == "ABORTED"


def test_dalg_matches_exhaustive_on_random_circuits():
    """Doi chieu doc lap voi vet can tren mach ngau nhien co du 8 loai cong."""
    rng = random.Random(7)
    types = ["AND", "NAND", "OR", "NOR", "XOR", "XNOR", "NOT", "BUFF"]
    checked = 0
    for _ in range(60):
        pis = [f"i{k}" for k in range(rng.randint(2, 4))]
        nets, gates = list(pis), []
        for k in range(rng.randint(2, 7)):
            t = rng.choice(types)
            ins = [rng.choice(nets)] if t in ("NOT", "BUFF") else rng.sample(nets, min(rng.randint(2, 3), len(nets)))
            if t not in ("NOT", "BUFF") and len(ins) < 2:
                t, ins = "BUFF", ins[:1]
            gates.append(Gate(f"g{k}", t, ins))
            nets.append(f"g{k}")
        c = Circuit.from_gates("r", pis, rng.sample([g.output for g in gates], 1), gates)
        for f in all_faults(c):
            cube, _ = exhaustive_test(c, f)
            r = d_algorithm(c, f)
            assert r.status in ("DETECTED", "UNTESTABLE"), str(f)
            if r.status == "DETECTED":
                assert detects_cube(c, r.pattern, f) is True, str(f)
            else:
                assert cube is None, str(f)
            checked += 1
    assert checked > 300


def test_dalg_rejects_bad_input():
    c = c17()
    with pytest.raises(ValueError):
        d_algorithm(c, [Fault("11", 0)])
    with pytest.raises(ValueError):
        d_algorithm(c, Fault("99", 0))
    with pytest.raises(ValueError):
        d_algorithm(c, Fault("11", 0), order="random")
    with pytest.raises(ValueError):
        d_algorithm(Circuit.from_bench(SEQ), Fault("Q", 0))


# ---------------- CLI so sanh ----------------
def test_compare_cli_c17_11sa0(tmp_path, capsys):
    md, cs, tex = tmp_path / "r.md", tmp_path / "r.csv", tmp_path / "r.tex"
    assert compare.main([C17, "--fault", "11", "0", "--trace", "--repeat", "3",
                         "--md", str(md), "--csv", str(cs), "--tex", str(tex)]) == 0
    out = capsys.readouterr().out
    assert "| A. Kết quả | Test cube (thứ tự PI 1, 2, 3, 6, 7) | X100X |" in out
    assert "## Trace D-algorithm" in out and "khớp (Chương 3 (P2)" in out
    rows = list(csv.reader(md.parent.joinpath("r.csv").open(encoding="utf-8-sig")))
    assert rows[0] == ["Nhóm", "Tiêu chí", "D-algorithm", "PODEM", "Ý nghĩa"] and len(rows) > 10
    assert r"\begin{tabular}" in tex.read_text(encoding="utf-8")
    assert md.read_text(encoding="utf-8").startswith("# So sánh D-algorithm và PODEM")


def test_compare_with_real_podem(capsys):
    pytest.importorskip("atpg.podem")
    assert compare.main([C17, "--fault", "11", "0", "--repeat", "0"]) == 0
    out = capsys.readouterr().out
    assert "| A. Kết quả | Test cube (thứ tự PI 1, 2, 3, 6, 7) | X100X | X10XX |" in out
    assert "| B. Quá trình tìm kiếm | Số quyết định (kể cả lần chọn thất bại) | 4 | 2 |" in out
    assert "khớp (results/golden_trace_c17_11sa0.md (P3)" in out


def test_compare_all_c17(capsys):
    assert compare.main([C17, "--all", "--repeat", "0"]) == 0
    out = capsys.readouterr().out
    assert "| Phát hiện (DETECTED / tổng) | 22/22 |" in out
    assert "| Pattern đúng (X=0 và mọi cách điền X) | 22/22 |" in out


@pytest.mark.parametrize("argv", [[C17, "--fault", "11", "2"], [C17, "--fault", "11", "0", "--branch", "999"],
                                  [SEQ, "--fault", "Q", "0"], [C17]])
def test_compare_cli_rejects_bad_input(argv, capsys):
    with pytest.raises(SystemExit) as e:
        compare.main(argv)
    assert e.value.code == 2
