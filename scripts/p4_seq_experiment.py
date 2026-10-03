"""Kiểm chứng độc lập mạch tuần tự P4 bằng vét cạn nhị phân.

Chạy: python scripts/p4_seq_experiment.py
Không thay thế PODEM/fault_sim của P5/P6; kết quả là mốc tham chiếu nhỏ.
"""

from itertools import product
from pathlib import Path
import re


BENCH = Path(__file__).resolve().parents[1] / "circuits" / "seq_example.bench"


def read_bench():
    inputs, outputs, gates = [], [], {}
    for raw in BENCH.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if m := re.fullmatch(r"INPUT\((\w+)\)", line):
            inputs.append(m.group(1))
        elif m := re.fullmatch(r"OUTPUT\((\w+)\)", line):
            outputs.append(m.group(1))
        elif m := re.fullmatch(r"(\w+)\s*=\s*(\w+)\(([^)]*)\)", line):
            net, kind, args = m.groups()
            gates[net] = (kind, [s.strip() for s in args.split(",")])
        else:
            raise ValueError(f"Dòng .bench sai: {line}")
    return inputs, outputs, gates


def one_cycle(a: int, b: int, q: int, fault=None):
    """Trả (Y,D), cấy một stuck-at trên stem ở mỗi chu kỳ."""
    _, _, gates = read_bench()
    values = {"A": a, "B": b, "Q": q}
    if fault and fault[0] in values:
        values[fault[0]] = fault[1]
    # Thứ tự này là topo của phần tổ hợp trong seq_example.bench.
    for net in ("N1", "N2", "N3", "D", "N4", "Y"):
        kind, parents = gates[net]
        args = [values[parent] for parent in parents]
        if kind == "AND":
            value = int(all(args))
        elif kind == "OR":
            value = int(any(args))
        elif kind == "NAND":
            value = int(not all(args))
        elif kind == "NOT":
            value = 1 - args[0]
        elif kind == "XOR":
            value = sum(args) % 2
        else:
            raise ValueError(kind)
        values[net] = fault[1] if fault and fault[0] == net else value
    return values["Y"], values["D"]


def output_trace(sequence, initial_q: int, fault=None):
    q = initial_q
    trace = []
    for a, b in sequence:
        y, q = one_cycle(a, b, q, fault)
        trace.append(y)
    return tuple(trace)


def detects_without_scan(sequence, fault):
    # Hai tập vết phải rời nhau dù trạng thái ban đầu là 0 hay 1.
    good = {output_trace(sequence, q) for q in (0, 1)}
    bad = {output_trace(sequence, q, fault) for q in (0, 1)}
    return good.isdisjoint(bad)


def first_sequence(fault, max_frames=4):
    for frames in range(1, max_frames + 1):
        for sequence in product(product((0, 1), repeat=2), repeat=frames):
            if detects_without_scan(sequence, fault):
                return sequence
    return None


def first_scan_pattern(fault):
    # Full scan: Q điều khiển được; D quan sát được sau capture.
    for a, b, q in product((0, 1), repeat=3):
        if one_cycle(a, b, q) != one_cycle(a, b, q, fault):
            return (a, b, q)
    return None


def main():
    inputs, outputs, gates = read_bench()
    assert inputs == ["A", "B"] and outputs == ["Y"]
    assert gates["Q"] == ("DFF", ["D"])
    nets = [*inputs, *gates]
    faults = [(net, stuck) for net in nets for stuck in (0, 1)]
    print(f"PI={len(inputs)}, PO={len(outputs)}, cong to hop={len(gates)-1}, DFF=1")
    print(f"Stem stuck-at faults={len(faults)}; khong fault collapsing")
    print("fault | scan A,B,Q | sequence A,B (Q0 bat ky)")
    print("--- | --- | ---")
    scan_detected = seq_detected = 0
    for fault in faults:
        scan = first_scan_pattern(fault)
        seq = first_sequence(fault)
        scan_detected += scan is not None
        seq_detected += seq is not None
        print(f"{fault[0]}/SA{fault[1]} | {scan} | {seq}")
    print(f"Full scan: {scan_detected}/{len(faults)}")
    print(f"Unroll <=4 khung, test doc lap Q0: {seq_detected}/{len(faults)}")


if __name__ == "__main__":
    main()
