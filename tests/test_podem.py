# test_podem.py
# Kiểm thử các hàm imply và objective trên mạch tạm của nhóm.

from dataclasses import dataclass

from atpg.podem import (
    imply,
    objective,
    backtrace,
    Decision,
    backtrack,
    PodemResult,
    _is_detected,
    podem,
)


@dataclass
class Gate_for_Test:
    output: str
    type: str
    inputs: list[str]


@dataclass
class Circuit_for_Test:
    inputs: list[str]
    outputs: list[str]
    gates: dict[str, Gate_for_Test]
    fanout: dict[str, list[str]]
    topo_order: list[str]


@dataclass(frozen=True)
class Fault_for_Test:
    net: str
    stuck_at: int
    branch_to: str | None = None


def make_c17() -> Circuit_for_Test:
    # C17 theo netlist chuẩn của project.
    gates = {
        "10": Gate_for_Test("10", "NAND", ["1", "3"]),
        "11": Gate_for_Test("11", "NAND", ["3", "6"]),
        "16": Gate_for_Test("16", "NAND", ["2", "11"]),
        "19": Gate_for_Test("19", "NAND", ["11", "7"]),
        "22": Gate_for_Test("22", "NAND", ["10", "16"]),
        "23": Gate_for_Test("23", "NAND", ["16", "19"]),
    }

    return Circuit_for_Test(
        inputs=["1", "2", "3", "6", "7"],
        outputs=["22", "23"],
        gates=gates,
        fanout={
            "1": ["10"],
            "2": ["16"],
            "3": ["10", "11"],
            "6": ["11"],
            "7": ["19"],
            "10": ["22"],
            "11": ["16", "19"],
            "16": ["22", "23"],
            "19": ["23"],
        },
        topo_order=["10", "11", "16", "19", "22", "23"],
    )


# ---------------------------------------------------------
# Kiểm thử imply
# ---------------------------------------------------------

def test_imply_activates_c17_11_sa0():
    c = make_c17()
    fault = Fault_for_Test("11", 0)

    pattern = {
        "1": "X",
        "2": "X",
        "3": "0",
        "6": "X",
        "7": "X",
    }

    values = imply(c, pattern, fault)

    assert values["10"] == "1"
    assert values["11"] == "D"


def test_imply_propagates_c17_11_sa0():
    c = make_c17()
    fault = Fault_for_Test("11", 0)

    pattern = {
        "1": "X",
        "2": "1",
        "3": "0",
        "6": "X",
        "7": "X",
    }

    values = imply(c, pattern, fault)

    assert values["11"] == "D"
    assert values["16"] == "D'"
    assert values["22"] == "D"


def test_imply_branch_fault():
    # Fault chỉ nằm trên nhánh a -> t.
    gates = {
        "t": Gate_for_Test("t", "NAND", ["a", "b"]),
    }

    c = Circuit_for_Test(
        inputs=["a", "b"],
        outputs=["t"],
        gates=gates,
        fanout={
            "a": ["t"],
            "b": ["t"],
        },
        topo_order=["t"],
    )

    fault = Fault_for_Test("a", 0, "t")

    pattern = {
        "a": "1",
        "b": "1",
    }

    values = imply(c, pattern, fault)

    # Good: NAND(1,1) = 0
    # Faulty branch: NAND(0,1) = 1
    # => D' = (0,1)
    assert values["t"] == "D'"


# ---------------------------------------------------------
# Kiểm thử objective
# ---------------------------------------------------------

def test_objective_activates_c17_11_sa0():
    c = make_c17()
    fault = Fault_for_Test("11", 0)

    pattern = {
        "1": "X",
        "2": "X",
        "3": "X",
        "6": "X",
        "7": "X",
    }

    values = imply(c, pattern, fault)

    result = objective(c, values, fault)

    # SA0 -> muốn mạch tốt có giá trị 1 tại net lỗi.
    assert result == ("11", 1)


def test_objective_propagates_c17_11_sa0():
    c = make_c17()
    fault = Fault_for_Test("11", 0)

    pattern = {
        "1": "X",
        "2": "X",
        "3": "0",
        "6": "X",
        "7": "X",
    }

    values = imply(c, pattern, fault)

    # Sau khi 3=0, fault được kích hoạt:
    # 11 tốt = 1, 11 lỗi = 0 -> 11 = D.
    assert values["11"] == "D"

    result = objective(c, values, fault)

    # D-frontier = {16, 19}
    # Chọn 16 trước theo topo_order.
    # 16 = NAND(2, 11)
    # Input X đầu tiên là 2.
    # NAND cần non-controlling value = 1.
    assert result == ("2", 1)


def test_objective_fails_when_fault_stuck_value_is_already_present():
    c = make_c17()
    fault = Fault_for_Test("11", 0)

    values = {
        "1": "X",
        "2": "X",
        "3": "1",
        "6": "1",
        "7": "X",
        "10": "X",
        "11": "0",
        "16": "X",
        "19": "X",
        "22": "X",
        "23": "X",
    }

    result = objective(c, values, fault)

    # 11 đã đúng bằng stuck value 0,
    # nên trạng thái hiện tại không tạo được fault effect.
    assert result is None

def test_backtrace_activates_c17_11_sa0():
    c = make_c17()

    values = {
        "1": "X",
        "2": "X",
        "3": "X",
        "6": "X",
        "7": "X",
        "10": "X",
        "11": "X",
        "16": "X",
        "19": "X",
        "22": "X",
        "23": "X",
    }

    result = backtrace(
        c,
        values,
        "11",
        1,
    )

    # 11 = NAND(3,6)
    # Input X đầu tiên: 3
    # NAND đảo 1 -> 0
    assert result == ("3", 0)


def test_backtrace_propagates_c17_11_sa0():
    c = make_c17()

    values = {
        "1": "X",
        "2": "X",
        "3": "0",
        "6": "X",
        "7": "X",
        "10": "1",
        "11": "D",
        "16": "X",
        "19": "X",
        "22": "X",
        "23": "X",
    }

    result = backtrace(
        c,
        values,
        "2",
        1,
    )

    # 2 đã là PI nên trả về ngay.
    assert result == ("2", 1)

def test_backtrack_tries_other_value():
    decisions = [
        Decision("a", 1),
    ]

    result = backtrack(decisions)

    assert result == ("a", 0)
    assert decisions[-1].tried_other is True
    assert decisions[-1].value == 0


def test_backtrack_removes_exhausted_decision():
    decisions = [
        Decision("a", 1, True),
    ]

    result = backtrack(decisions)

    assert result is None
    assert decisions == []


def test_backtrack_skips_exhausted_decision():
    decisions = [
        Decision("a", 1, True),
        Decision("b", 0, False),
    ]

    result = backtrack(decisions)

    assert result == ("b", 1)
    assert decisions[-1].tried_other is True

def test_is_detected_when_po_has_d():
    c = make_c17()

    values = {
        "22": "D",
        "23": "X",
    }

    from atpg.podem import _is_detected

    assert _is_detected(c, values) is True


def test_is_not_detected_when_no_po_has_d():
    c = make_c17()

    values = {
        "22": "X",
        "23": "X",
    }

    from atpg.podem import _is_detected

    assert _is_detected(c, values) is False

def test_podem_detects_c17_11_sa0():
    c = make_c17()
    fault = Fault_for_Test("11", 0)

    result = podem(
        c,
        fault,
    )

    assert result.status == "DETECTED"

    assert result.pattern == {
        "1": "X",
        "2": "1",
        "3": "0",
        "6": "X",
        "7": "X",
    }

    assert result.backtracks == 0

def test_podem_trace_c17_11_sa0():
    c = make_c17()
    fault = Fault_for_Test("11", 0)

    result = podem(
        c,
        fault,
        trace=True,
    )

    assert result.status == "DETECTED"
    assert len(result.steps) > 0

    assert result.steps[-1]["Hành động"] == "thành công"

#Test với mạch phụ P3
def make_backtrack_circuit() -> Circuit_for_Test:
    gates = {
        "t": Gate_for_Test("t", "OR", ["a", "b"]),
        "n": Gate_for_Test("n", "NOT", ["a"]),
        "out": Gate_for_Test("out", "AND", ["t", "n"]),
    }

    return Circuit_for_Test(
        inputs=["a", "b"],
        outputs=["out"],
        gates=gates,
        fanout={
            "a": ["t", "n"],
            "b": ["t"],
            "t": ["out"],
            "n": ["out"],
        },
        topo_order=["t", "n", "out"],
    )

def test_podem_backtracks_and_detects():
    c = make_backtrack_circuit()
    fault = Fault_for_Test("t", 0)

    result = podem(
        c,
        fault,
    )

    assert result.status == "DETECTED"

    assert result.pattern == {
        "a": "0",
        "b": "1",
    }

    assert result.backtracks == 1

#In trace
def test_print_podem_trace_c17_11_sa0():
    c = make_c17()
    fault = Fault_for_Test("11", 0)

    result = podem(
        c,
        fault,
        trace=True,
    )

    print("\n===== PODEM TRACE: c17 / 11-SA0 =====")

    for step in result.steps:
        print(f"\nBước {step['Bước']}")
        print(f"Objective: {step['Objective (net, giá trị)']}")
        print(f"Backtrace: {step['Backtrace → PI']}")
        print(f"Gán PI: {step['Gán PI']}")
        print(f"Giá trị các net: {step['Giá trị các net sau imply']}")
        print(f"D-frontier: {step['D-frontier']}")
        print(f"Hành động: {step['Hành động']}")

    print("\nPattern:", result.pattern)
    print("Status:", result.status)
    print("Backtracks:", result.backtracks)

    assert result.status == "DETECTED"

# Test xác nhận không bị lỗi net 23
def test_imply_keeps_p23_as_x_on_c17():
    c = make_c17()
    fault = Fault_for_Test("11", 0)

    pattern = {
        "1": "X",
        "2": "1",
        "3": "0",
        "6": "X",
        "7": "X",
    }

    values = imply(c, pattern, fault)

    assert values["16"] == "D'"
    assert values["19"] == "X"
    assert values["22"] == "D"
    assert values["23"] == "X"

#Test UNTESTABLE
def make_untestable_circuit():
    gates = {
        "n": Gate_for_Test(
            output="n",
            type="NOT",
            inputs=["a"],
        ),
        "out": Gate_for_Test(
            output="out",
            type="AND",
            inputs=["a", "n"],
        ),
    }

    fanout = {
        "a": ["n", "out"],
        "n": ["out"],
    }

    return Circuit_for_Test(
        inputs=["a"],
        outputs=["out"],
        gates=gates,
        fanout=fanout,
        topo_order=["n", "out"],
    )

def test_podem_untestable():
    c = make_untestable_circuit()
    fault = Fault_for_Test("a", 0)

    result = podem(c, fault)

    assert result.status == "UNTESTABLE"

#Test ABORTED
def test_podem_aborts_when_backtrack_limit_is_zero():
    c = make_backtrack_circuit()
    fault = Fault_for_Test("t", 0)

    result = podem(
        c,
        fault,
        max_backtracks=0,
    )

    assert result.status == "ABORTED"
    assert result.backtracks == 0

#Test branch fault
def test_podem_branch_fault_c17():
    c = make_c17()
    fault = Fault_for_Test(
        net="11",
        stuck_at=0,
        branch_to="16",
    )

    result = podem(c, fault)

    assert result.status == "DETECTED"

#Test P4
def test_podem_sequential_fault_frames():
    """
    Kiểm tra PODEM nhận danh sách fault-frame
    trên mạch tuần tự đã được trải thành 2 khung.
    """

    from atpg.unroll import unroll, fault_in_frames

    # ---------------------------------------------------------
    # 1. Tạo mạch tuần tự của P4
    # ---------------------------------------------------------

    gates = {
        "N1": Gate_for_Test(
            output="N1",
            type="AND",
            inputs=["A", "Q"],
        ),
        "N2": Gate_for_Test(
            output="N2",
            type="NOT",
            inputs=["B"],
        ),
        "N3": Gate_for_Test(
            output="N3",
            type="OR",
            inputs=["N1", "N2"],
        ),
        "D": Gate_for_Test(
            output="D",
            type="NAND",
            inputs=["N3", "A"],
        ),
        "Q": Gate_for_Test(
            output="Q",
            type="DFF",
            inputs=["D"],
        ),
        "N4": Gate_for_Test(
            output="N4",
            type="XOR",
            inputs=["Q", "B"],
        ),
        "Y": Gate_for_Test(
            output="Y",
            type="AND",
            inputs=["N4", "A"],
        ),
    }

    fanout = {
        "A": ["N1", "D", "Y"],
        "B": ["N2", "N4"],
        "Q": ["N1", "N4"],
        "N1": ["N3"],
        "N2": ["N3"],
        "N3": ["D"],
        "D": ["Q"],
        "N4": ["Y"],
    }

    c = Circuit_for_Test(
        inputs=["A", "B"],
        outputs=["Y"],
        gates=gates,
        fanout=fanout,
        topo_order=[
            "N1",
            "N2",
            "N3",
            "D",
            "Q",
            "N4",
            "Y",
        ],
    )

    # Gán tên mạch để tương thích với unroll().
    c.name = "seq_example"

    # ---------------------------------------------------------
    # 2. Trải mạch thành 2 time frames
    # ---------------------------------------------------------

    unrolled = unroll(
        c,
        2,
    )

    # ---------------------------------------------------------
    # 3. Tạo fault-frame
    # ---------------------------------------------------------

    fault = Fault_for_Test(
        net="N3",
        stuck_at=0,
    )

    faults = fault_in_frames(
        fault,
        2,
    )

    # ---------------------------------------------------------
    # 4. Kiểm tra fault-frame được tạo đúng
    # ---------------------------------------------------------

    assert [f.net for f in faults] == [
        "N3@0",
        "N3@1",
    ]

    assert [f.stuck_at for f in faults] == [
        0,
        0,
    ]

    # ---------------------------------------------------------
    # 5. Chạy PODEM
    # ---------------------------------------------------------

    result = podem(
        unrolled,
        faults,
    )

    # PODEM phải tìm được test pattern.
    assert result.status == "DETECTED"

    # Pattern phải chứa toàn bộ Primary Input của mạch trải khung.
    assert set(result.pattern.keys()) == set(
        unrolled.inputs
    )