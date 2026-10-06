"""Kiểm chứng dữ liệu P2 độc lập; không cài đặt ATPG hoặc thay test của P5/P6."""

import argparse
from itertools import product
from pathlib import Path
import runpy
import sys


ROOT = Path(__file__).resolve().parents[1]
VALUES = ("0", "1", "X", "D", "D'")
PAIRS = {"0": [(0, 0)], "1": [(1, 1)],
         "X": list(product((0, 1), repeat=2)),
         "D": [(1, 0)], "D'": [(0, 1)]}
ENCODE = {(0, 0): "0", (1, 1): "1", (1, 0): "D", (0, 1): "D'"}


def binary(gate, a, b=0):
    # Oracle nhị phân, không dùng lại logic ba giá trị để sinh bảng.
    return {"AND": a & b, "NAND": 1 - (a & b), "OR": a | b,
            "NOR": 1 - (a | b), "XOR": a ^ b, "XNOR": 1 - (a ^ b),
            "NOT": 1 - a, "BUFF": a}[gate]


def oracle(gate, a, b=None):
    candidates = PAIRS[b] if b is not None else [(0, 0)]
    outputs = {(binary(gate, x[0], y[0]), binary(gate, x[1], y[1]))
               for x in PAIRS[a] for y in candidates}
    return ENCODE[next(iter(outputs))] if len(outputs) == 1 else "X"


def check_integrated(table_cells):
    # Nạp code đã tích hợp, không thay oracle độc lập hoặc bảng chuẩn.
    sys.path.insert(0, str(ROOT / "src"))
    from atpg.circuit import Circuit
    from atpg.faults import Fault
    from atpg.fault_sim import detects, detects_cube, simulate
    from atpg.logic import eval_gate

    for gate, inputs, expected in table_cells:
        actual = eval_gate(gate, inputs)
        assert actual == expected, (
            f"Markdown/P5 mismatch: gate={gate}, inputs={inputs}, "
            f"expected={expected}, actual={actual}"
        )
    assert len(table_cells) == 160
    print("PASS integrated: Markdown vs atpg.logic.eval_gate: 160/160 cells")

    circuit = Circuit.from_bench(str(ROOT / "circuits/c17.bench"))
    assert circuit.inputs == ["1", "2", "3", "6", "7"], circuit.inputs
    assert circuit.outputs == ["22", "23"], circuit.outputs
    fault = Fault("11", 0)
    print("PI order: (1,2,3,6,7); PO order: (22,23); fault: stem 11/SA0")
    for pattern, expected_count in (("X100X", 4), ("X10XX", 8)):
        cube = dict(zip(circuit.inputs, pattern))
        vectors = [dict(zip(circuit.inputs, bits))
                   for bits in product((0, 1), repeat=5)
                   if all(value == "X" or int(value) == bits[i]
                          for i, value in enumerate(pattern))]
        assert len(vectors) == expected_count
        for vector in vectors:
            good = simulate(circuit, vector)
            bad = simulate(circuit, vector, fault)
            good_po = tuple(good[o] for o in circuit.outputs)
            bad_po = tuple(bad[o] for o in circuit.outputs)
            assert detects(circuit, vector, fault) and good["22"] != bad["22"], (
                f"P6 counterexample: cube={pattern}, vector={vector}, "
                f"good_PO={good_po}, faulty_PO={bad_po}"
            )
        assert detects_cube(circuit, cube, fault) is True, pattern
        print(f"PASS integrated: {pattern}: {len(vectors)}/{expected_count} "
              "completions detected at PO22; detects_cube=True")
    vector = dict(zip(circuit.inputs, (0, 1, 0, 0, 0)))
    good = simulate(circuit, vector)
    bad = simulate(circuit, vector, fault)
    good_po = tuple(good[o] for o in circuit.outputs)
    bad_po = tuple(bad[o] for o in circuit.outputs)
    assert (good_po, bad_po) == ((1, 1), (0, 0)), (good_po, bad_po)
    print(f"PASS integrated: 01000: good_PO={good_po}, faulty_PO={bad_po}")


def main(integrated=False):
    text = (ROOT / "tests/data/five_valued_tables.md").read_text(encoding="utf-8")
    cells = 0
    table_cells = []
    for gate in ("AND", "NAND", "OR", "NOR", "XOR", "XNOR", "NOT", "BUFF"):
        block = text.split("## " + gate + "\n")[1].split("## ")[0]
        rows = [line for line in block.splitlines() if line.startswith("|")][2:]
        if gate in ("NOT", "BUFF"):
            assert len(rows) == 1, gate
            actual = [v.strip() for v in rows[0].split("|")[2:-1]]
            assert actual == [oracle(gate, a) for a in VALUES], gate
            table_cells.extend((gate, [a], value) for a, value in zip(VALUES, actual))
            cells += 5
        else:
            assert len(rows) == 5, gate
            for a, row in zip(VALUES, rows):
                assert row.split("|")[1].strip() == a, (gate, a)
                actual = [v.strip() for v in row.split("|")[2:-1]]
                assert actual == [oracle(gate, a, b) for b in VALUES], (gate, a)
                table_cells.extend((gate, [a, b], value) for b, value in zip(VALUES, actual))
                cells += 5
    assert cells == 160
    print("PASS: 160 cells vs independent binary-completion oracle")

    p1 = runpy.run_path(str(ROOT / "scripts/check_p1_examples.py"))
    gates = p1["GATES"]
    stages = [({"6": "0"}, {}, {"16", "19"}, set()),
              ({"6": "0", "2": "1"}, {}, {"19", "22", "23"}, set()),
              ({"6": "0", "2": "1"}, {"10": "1"}, {"19", "23"}, {"10"}),
              ({"6": "0", "2": "1", "3": "0"}, {"10": "1"}, {"19", "23"}, set())]
    for index, (pi, requested, expected_d, expected_j) in enumerate(stages, 1):
        state = {net: pi.get(net, "X") for net in p1["INPUTS"]}
        j_frontier = set()
        for net, (a, b) in gates.items():
            implied = oracle("NAND", state[a], state[b])
            if net == "11":
                # Lỗi stem: cặp tốt/lỗi cố định trước khi phân nhánh.
                assert implied == "1"
                implied = "D"
            if net in requested and implied == "X":
                j_frontier.add(net)
                implied = requested[net]
            elif net in requested:
                assert implied == requested[net]
            state[net] = implied
        d_frontier = {net for net, inputs in gates.items()
                      if state[net] == "X" and any(state[a] in ("D", "D'") for a in inputs)}
        assert d_frontier == expected_d, (index, d_frontier)
        assert j_frontier == expected_j, (index, j_frontier)
        assert state["11"] == "D"
        assert state["16"] == ("X" if index == 1 else "D'")
        assert state["22"] == ("X" if index < 3 else "D")
        assert state["19"] == state["23"] == "X"
    print("PASS: four trace stages, D-frontier and J-frontier")

    simulate = p1["simulate"]
    for cube, count in [((None, 1, 0, 0, None), 4), ((None, 1, 0, None, None), 8)]:
        vectors = [v for v in product((0, 1), repeat=5)
                   if all(bit is None or v[i] == bit for i, bit in enumerate(cube))]
        assert len(vectors) == count
        assert all(simulate(v)[0] != simulate(v, ("11", 0))[0] for v in vectors)
        print(f"PASS: c17 cube, {count} completions")
    for v in ((0, 1, 0, 0, 0), (0, 1, 0, 0, 1), (1, 1, 0, 0, 0), (1, 1, 0, 0, 1)):
        assert simulate(v) == (1, 1) and simulate(v, ("11", 0)) == (0, 0)
    print("PASS: four documented binary PO pairs")
    if integrated:
        check_integrated(table_cells)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--integrated", action="store_true",
                        help="Đối chiếu Markdown và cube với code P5/P6 thật")
    main(integrated=parser.parse_args().integrated)
