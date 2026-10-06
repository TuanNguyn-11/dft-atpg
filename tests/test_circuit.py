"""Kiem thu doc mach (circuit.py) va danh sach loi (faults.py) - P6."""
import os
from itertools import product

import pytest

from atpg.circuit import Circuit
from atpg.fault_sim import detects
from atpg.faults import Fault, all_faults, collapse, equivalence_classes

ROOT = os.path.dirname(os.path.dirname(__file__))
C17 = os.path.join(ROOT, "circuits", "c17.bench")


def test_parse_c17():
    c = Circuit.from_bench(C17)
    assert c.name == "c17"
    assert c.inputs == ["1", "2", "3", "6", "7"]
    assert c.outputs == ["22", "23"]
    assert len(c.gates) == 6 and all(g.type == "NAND" for g in c.gates.values())
    assert c.gates["16"].inputs == ["2", "11"]


def test_topo_level_fanout_c17():
    c = Circuit.from_bench(C17)
    assert c.topo_order == ["10", "11", "16", "19", "22", "23"]
    assert c.level == {"1": 0, "2": 0, "3": 0, "6": 0, "7": 0,
                       "10": 1, "11": 1, "16": 2, "19": 2, "22": 3, "23": 3}
    assert c.fanout["3"] == ["10", "11"]
    assert c.fanout["11"] == ["16", "19"]
    assert c.fanout["16"] == ["22", "23"]
    assert c.fanout["22"] == []


def test_parse_dff(tmp_path):
    f = tmp_path / "seq.bench"
    f.write_text("# demo\nINPUT(A)\nINPUT(B)\nOUTPUT(Z)\nQ = DFF(D)\nD = XOR(A, Q)\nZ = AND(Q, B)\n")
    c = Circuit.from_bench(str(f))
    assert [g.output for g in c.dffs] == ["Q"]
    assert c.level["Q"] == 0 and c.level["D"] == 1
    assert "Q" not in c.topo_order and c.topo_order == ["D", "Z"]
    assert c.fanout["D"] == ["Q"]            # D noi vao DFF Q
    assert c.stats()["DFF"] == 1


def test_errors(tmp_path):
    bad = tmp_path / "bad.bench"
    bad.write_text("INPUT(A)\nOUTPUT(Z)\nZ = AND(A, MISSING)\n")
    with pytest.raises(ValueError):
        Circuit.from_bench(str(bad))
    loop = tmp_path / "loop.bench"
    loop.write_text("INPUT(A)\nOUTPUT(X)\nX = AND(A, Y)\nY = OR(A, X)\n")
    with pytest.raises(ValueError):
        Circuit.from_bench(str(loop))


def test_fault_counts_c17():
    c = Circuit.from_bench(C17)
    faults = all_faults(c)
    assert len(faults) == 34                  # 11 net x 2 + 3 net re nhanh x 2 nhanh x 2
    assert sum(1 for f in faults if f.branch_to) == 12
    assert len(set(faults)) == 34
    assert len(collapse(c, faults)) == 22     # sau gop tuong duong


def test_collapse_keeps_example_fault():
    c = Circuit.from_bench(C17)
    reps = collapse(c, all_faults(c))
    assert Fault("11", 0) in reps


def test_equivalence_is_functional():
    """Moi lop tuong duong phai co cung tap vector phat hien (kiem bang vet can)."""
    c = Circuit.from_bench(C17)
    vecs = [dict(zip(c.inputs, b)) for b in product((0, 1), repeat=5)]
    for cls in equivalence_classes(c, all_faults(c)):
        sets = [frozenset(i for i, v in enumerate(vecs) if detects(c, v, f)) for f in cls]
        assert len(set(sets)) == 1, [str(f) for f in cls]


def test_fault_str():
    assert str(Fault("11", 0)) == "11/SA0"
    assert str(Fault("11", 1, "16")) == "11->16/SA1"
