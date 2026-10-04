"""Kiểm thử P4 độc lập trong khi Circuit/Fault của P6 chưa được ghép.

MiniCircuit chỉ hiện thực đúng các thuộc tính trong hợp đồng chung. Khi P6
đưa parser vào, cùng các hàm biến đổi này nhận trực tiếp Circuit của P6.
"""

from dataclasses import dataclass, field
from pathlib import Path
from itertools import product
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from atpg.unroll import fault_in_frames, full_scan, unroll
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import p4_seq_experiment as reference


@dataclass
class Gate:
    output: str
    type: str
    inputs: list[str]


@dataclass
class Circuit:
    name: str
    inputs: list[str]
    outputs: list[str]
    gates: dict[str, Gate]
    fanout: dict[str, list[str]] = field(default_factory=dict)
    topo_order: list[str] = field(default_factory=list)
    level: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class Fault:
    net: str
    stuck_at: int
    branch_to: str | None = None


def read_example() -> Circuit:
    path = Path(__file__).resolve().parents[1] / "circuits" / "seq_example.bench"
    inputs, outputs, gates = [], [], {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if m := re.fullmatch(r"INPUT\((\w+)\)", line):
            inputs.append(m.group(1))
        elif m := re.fullmatch(r"OUTPUT\((\w+)\)", line):
            outputs.append(m.group(1))
        elif m := re.fullmatch(r"(\w+)\s*=\s*(\w+)\(([^)]*)\)", line):
            output, kind, args = m.groups()
            gates[output] = Gate(output, kind, [s.strip() for s in args.split(",")])
        else:
            raise AssertionError(f"Dòng .bench không hợp lệ: {line}")
    return Circuit(path.stem, inputs, outputs, gates)


def evaluate(c: Circuit, inputs: dict[str, int], faults: list[Fault] = ()) -> dict[str, int]:
    """Mô phỏng nhị phân độc lập để kiểm tra mẫu và liên kết khung."""
    values = dict(inputs)
    stuck = {f.net: f.stuck_at for f in faults if f.branch_to is None}
    for net in c.inputs:
        if net in stuck:
            values[net] = stuck[net]
    for net in c.topo_order:
        gate = c.gates[net]
        args = [values[parent] for parent in gate.inputs]
        if gate.type == "AND":
            value = int(all(args))
        elif gate.type == "OR":
            value = int(any(args))
        elif gate.type == "NAND":
            value = int(not all(args))
        elif gate.type == "NOT":
            value = 1 - args[0]
        elif gate.type == "XOR":
            value = sum(args) % 2
        elif gate.type == "BUFF":
            value = args[0]
        else:
            raise AssertionError(f"Cổng không được hỗ trợ trong test: {gate.type}")
        values[net] = stuck.get(net, value)
    return {net: values[net] for net in c.outputs}


def test_full_scan_turns_q_into_controllable_pi_and_d_into_po():
    original = read_example()
    scan = full_scan(original)
    assert scan.inputs == ["A", "B", "Q"]
    assert scan.outputs == ["Y", "D"]
    assert "Q" not in scan.gates
    assert len(scan.gates) == 6
    assert len(scan.topo_order) == 6
    assert scan.level["Q"] == 0
    assert scan.fanout["Q"] == ["N1", "N4"]
    assert "Q" in original.gates  # không sửa mạch nguồn
    good = evaluate(scan, {"A": 1, "B": 1, "Q": 1})
    bad = evaluate(scan, {"A": 1, "B": 1, "Q": 1}, [Fault("N3", 0)])
    assert (good["D"], bad["D"]) == (0, 1)


def test_unroll_two_frames_wires_state_and_detects_n4_fault():
    expanded = unroll(read_example(), 2)
    assert expanded.inputs == ["A@0", "B@0", "A@1", "B@1", "Q@0"]
    assert expanded.outputs == ["Y@0", "Y@1"]
    assert len(expanded.gates) == 13  # 6 cổng x 2 + 1 BUFF thay FF
    assert expanded.gates["Q@1"].inputs == ["D@0"]
    assert expanded.gates["Q@1"].type == "BUFF"
    assert expanded.level["Q@1"] > expanded.level["D@0"]
    fault = Fault("N4", 0)
    assert fault_in_frames(fault, 2) == [Fault("N4@0", 0), Fault("N4@1", 0)]
    for initial in (0, 1):
        pattern = {"Q@0": initial, "A@0": 0, "B@0": 0, "A@1": 1, "B@1": 0}
        good = evaluate(expanded, pattern)
        bad = evaluate(expanded, pattern, fault_in_frames(fault, 2))
        assert good == {"Y@0": 0, "Y@1": 1}
        assert bad == {"Y@0": 0, "Y@1": 0}


def test_three_frame_n3_fault_initializes_then_propagates_independent_of_initial_state():
    expanded = unroll(read_example(), 3)
    assert expanded.gates["Q@2"].inputs == ["D@1"]
    assert len(expanded.gates) == 20
    faults = fault_in_frames(Fault("N3", 0), 3)
    for initial in (0, 1):
        pattern = {
            "Q@0": initial,
            "A@0": 0, "B@0": 0,
            "A@1": 1, "B@1": 1,
            "A@2": 1, "B@2": 0,
        }
        good = evaluate(expanded, pattern)
        bad = evaluate(expanded, pattern, faults)
        assert good == {"Y@0": 0, "Y@1": 0, "Y@2": 0}
        assert bad == {"Y@0": 0, "Y@1": 0, "Y@2": 1}


def test_all_stem_faults_match_independent_sequential_simulation():
    original = read_example()
    faults = [None] + [Fault(net, stuck) for net in [*original.inputs, *original.gates] for stuck in (0, 1)]
    comparisons = 0
    for k in (1, 2, 3):
        expanded = unroll(original, k)
        for sequence in product(tuple(product((0, 1), repeat=2)), repeat=k):
            for initial in (0, 1):
                pattern = {f"{net}@{t}": value for t, pair in enumerate(sequence) for net, value in zip(("A", "B"), pair)}
                pattern["Q@0"] = initial
                for fault in faults:
                    reference_fault = (fault.net, fault.stuck_at) if fault else None
                    expected = reference.output_trace(sequence, initial, reference_fault)
                    outputs = evaluate(expanded, pattern, fault_in_frames(fault, k) if fault else [])
                    actual = tuple(outputs[f"Y@{t}"] for t in range(k))
                    assert actual == expected, (k, sequence, initial, fault, actual, expected)
                    comparisons += 1
    assert comparisons == 3192


def test_all_scan_patterns_and_faults_match_reference():
    original = read_example()
    scan = full_scan(original)
    faults = [None] + [Fault(net, stuck) for net in [*original.inputs, *original.gates] for stuck in (0, 1)]
    for a, b, q in product((0, 1), repeat=3):
        for fault in faults:
            expected = reference.one_cycle(a, b, q, (fault.net, fault.stuck_at) if fault else None)
            actual = evaluate(scan, {"A": a, "B": b, "Q": q}, [fault] if fault else [])
            assert (actual["Y"], actual["D"]) == expected


def test_two_dffs_transfer_simultaneously_without_changing_source():
    original = Circuit("swap", [], ["Q1", "Q2"], {
        "Q1": Gate("Q1", "DFF", ["Q2"]),
        "Q2": Gate("Q2", "DFF", ["Q1"]),
    })
    expanded = unroll(original, 3)
    assert evaluate(expanded, {"Q1@0": 0, "Q2@0": 1}) == {
        "Q1@0": 0, "Q2@0": 1, "Q1@1": 1, "Q2@1": 0, "Q1@2": 0, "Q2@2": 1,
    }
    expanded.gates["Q1@1"].inputs.append("unused")
    assert original.gates["Q1"].inputs == ["Q2"]
    assert full_scan(original).gates == {}


def test_assuming_initial_state_can_produce_an_invalid_physical_test():
    expanded = unroll(read_example(), 1)
    fault = Fault("N4", 0)
    pattern = {"A@0": 1, "B@0": 0, "Q@0": 1}
    assert evaluate(expanded, pattern) != evaluate(expanded, pattern, fault_in_frames(fault, 1))
    # Q0 không phải PI vật lý: cùng mẫu này không phân biệt được hai tập vết.
    assert not reference.detects_without_scan(((1, 0),), ("N4", 0))


def test_branch_fault_names_and_invalid_frame_count():
    assert fault_in_frames(Fault("N3", 1, "D"), 2) == [
        Fault("N3@0", 1, "D@0"), Fault("N3@1", 1, "D@1")
    ]
    for operation in (lambda: unroll(read_example(), 0), lambda: fault_in_frames(Fault("N3", 0), 0)):
        try:
            operation()
        except ValueError as error:
            assert "k" in str(error)
        else:
            raise AssertionError("k=0 phải bị từ chối")


if __name__ == "__main__":
    # Cho phép kiểm tra nhanh bằng Python chuẩn khi máy chưa cài pytest.
    for name, test in sorted(globals().items()):
        if name.startswith("test_") and callable(test):
            test()
            print(f"PASS {name}")
