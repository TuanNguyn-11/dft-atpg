# test_logic.py
# Kiểm thử logic 5 giá trị theo bảng chuẩn do P2 cung cấp.

import pytest

from atpg.logic import eval_gate


VALUES = ["0", "1", "X", "D", "D'"]


# Bảng 5x5 theo đúng thứ tự:
# hàng = a, cột = b
BINARY_TABLES = {
    "AND": [
        ["0", "0", "0", "0", "0"],
        ["0", "1", "X", "D", "D'"],
        ["0", "X", "X", "X", "X"],
        ["0", "D", "X", "D", "0"],
        ["0", "D'", "X", "0", "D'"],
    ],
    "NAND": [
        ["1", "1", "1", "1", "1"],
        ["1", "0", "X", "D'", "D"],
        ["1", "X", "X", "X", "X"],
        ["1", "D'", "X", "D'", "1"],
        ["1", "D", "X", "1", "D"],
    ],
    "OR": [
        ["0", "1", "X", "D", "D'"],
        ["1", "1", "1", "1", "1"],
        ["X", "1", "X", "X", "X"],
        ["D", "1", "X", "D", "1"],
        ["D'", "1", "X", "1", "D'"],
    ],
    "NOR": [
        ["1", "0", "X", "D'", "D"],
        ["0", "0", "0", "0", "0"],
        ["X", "0", "X", "X", "X"],
        ["D'", "0", "X", "D'", "0"],
        ["D", "0", "X", "0", "D"],
    ],
    "XOR": [
        ["0", "1", "X", "D", "D'"],
        ["1", "0", "X", "D'", "D"],
        ["X", "X", "X", "X", "X"],
        ["D", "D'", "X", "0", "1"],
        ["D'", "D", "X", "1", "0"],
    ],
    "XNOR": [
        ["1", "0", "X", "D'", "D"],
        ["0", "1", "X", "D", "D'"],
        ["X", "X", "X", "X", "X"],
        ["D'", "D", "X", "1", "0"],
        ["D", "D'", "X", "0", "1"],
    ],
}


UNARY_TABLES = {
    "NOT": ["1", "0", "X", "D'", "D"],
    "BUFF": ["0", "1", "X", "D", "D'"],
}


@pytest.mark.parametrize("gate_type", BINARY_TABLES.keys())
@pytest.mark.parametrize("a_index", range(len(VALUES)))
@pytest.mark.parametrize("b_index", range(len(VALUES)))
def test_binary_gates_against_p2_table(gate_type, a_index, b_index):
    # Kiểm tra từng ô trong bảng 5x5 của P2.
    a = VALUES[a_index]
    b = VALUES[b_index]

    expected = BINARY_TABLES[gate_type][a_index][b_index]
    actual = eval_gate(gate_type, [a, b])

    assert actual == expected, (
        f"{gate_type}({a}, {b}): "
        f"expected {expected}, got {actual}"
    )


@pytest.mark.parametrize("gate_type", UNARY_TABLES.keys())
@pytest.mark.parametrize("value_index", range(len(VALUES)))
def test_unary_gates_against_p2_table(gate_type, value_index):
    # Kiểm tra từng ô trong bảng 1x5 của P2.
    value = VALUES[value_index]

    expected = UNARY_TABLES[gate_type][value_index]
    actual = eval_gate(gate_type, [value])

    assert actual == expected, (
        f"{gate_type}({value}): "
        f"expected {expected}, got {actual}"
    )


def test_invalid_logic_value():
    # Giá trị ngoài năm ký hiệu chuẩn phải bị từ chối.
    with pytest.raises(ValueError):
        eval_gate("AND", ["0", "2"])


def test_invalid_gate_type():
    # Loại cổng không được hỗ trợ phải bị từ chối.
    with pytest.raises(ValueError):
        eval_gate("INVALID", ["0", "1"])


# =========================================================
# TEST XOR / XNOR THEO P3-v1.1
# =========================================================

import pytest


# ---------------------------------------------------------
# Toàn bộ 25 tổ hợp của 5 giá trị:
# 0, 1, X, D, D'
# ---------------------------------------------------------

LOGIC_VALUES = [
    "0",
    "1",
    "X",
    "D",
    "D'",
]


# Bảng XOR kỳ vọng độc lập với implementation.
XOR_EXPECTED = {
    ("0", "0"): "0",
    ("0", "1"): "1",
    ("0", "X"): "X",
    ("0", "D"): "D",
    ("0", "D'"): "D'",

    ("1", "0"): "1",
    ("1", "1"): "0",
    ("1", "X"): "X",
    ("1", "D"): "D'",
    ("1", "D'"): "D",

    ("X", "0"): "X",
    ("X", "1"): "X",
    ("X", "X"): "X",
    ("X", "D"): "X",
    ("X", "D'"): "X",

    ("D", "0"): "D",
    ("D", "1"): "D'",
    ("D", "X"): "X",
    ("D", "D"): "0",
    ("D", "D'"): "1",

    ("D'", "0"): "D'",
    ("D'", "1"): "D",
    ("D'", "X"): "X",
    ("D'", "D"): "1",
    ("D'", "D'"): "0",
}


# Bảng XNOR kỳ vọng độc lập với implementation.
XNOR_EXPECTED = {
    ("0", "0"): "1",
    ("0", "1"): "0",
    ("0", "X"): "X",
    ("0", "D"): "D'",
    ("0", "D'"): "D",

    ("1", "0"): "0",
    ("1", "1"): "1",
    ("1", "X"): "X",
    ("1", "D"): "D",
    ("1", "D'"): "D'",

    ("X", "0"): "X",
    ("X", "1"): "X",
    ("X", "X"): "X",
    ("X", "D"): "X",
    ("X", "D'"): "X",

    ("D", "0"): "D'",
    ("D", "1"): "D",
    ("D", "X"): "X",
    ("D", "D"): "1",
    ("D", "D'"): "0",

    ("D'", "0"): "D",
    ("D'", "1"): "D'",
    ("D'", "X"): "X",
    ("D'", "D"): "0",
    ("D'", "D'"): "1",
}


@pytest.mark.parametrize(
    "left",
    LOGIC_VALUES,
)
@pytest.mark.parametrize(
    "right",
    LOGIC_VALUES,
)
def test_xor_all_25_combinations(left, right):
    expected = XOR_EXPECTED[(left, right)]

    result = eval_gate(
        "XOR",
        [left, right],
    )

    assert result == expected


@pytest.mark.parametrize(
    "left",
    LOGIC_VALUES,
)
@pytest.mark.parametrize(
    "right",
    LOGIC_VALUES,
)
def test_xnor_all_25_combinations(left, right):
    expected = XNOR_EXPECTED[(left, right)]

    result = eval_gate(
        "XNOR",
        [left, right],
    )

    assert result == expected


# ---------------------------------------------------------
# Multi-input XOR
# ---------------------------------------------------------

def test_xor_multi_input():
    assert eval_gate(
        "XOR",
        ["1", "0", "1"],
    ) == "0"

    assert eval_gate(
        "XOR",
        ["D", "0", "1"],
    ) == "D'"

    assert eval_gate(
        "XOR",
        ["D", "D", "0"],
    ) == "0"

    assert eval_gate(
        "XOR",
        ["D", "D'", "0"],
    ) == "1"

    assert eval_gate(
        "XOR",
        ["D", "X", "0"],
    ) == "X"


# ---------------------------------------------------------
# Multi-input XNOR
# ---------------------------------------------------------

def test_xnor_multi_input():
    assert eval_gate(
        "XNOR",
        ["1", "0", "1"],
    ) == "1"

    assert eval_gate(
        "XNOR",
        ["D", "0", "1"],
    ) == "D"

    assert eval_gate(
        "XNOR",
        ["D", "D", "0"],
    ) == "1"

    assert eval_gate(
        "XNOR",
        ["D", "D'", "0"],
    ) == "0"

    assert eval_gate(
        "XNOR",
        ["D", "X", "0"],
    ) == "X"


# ---------------------------------------------------------
# D / D' lan truyền và triệt tiêu
# ---------------------------------------------------------

def test_xor_d_propagation():
    assert eval_gate(
        "XOR",
        ["D", "0"],
    ) == "D"

    assert eval_gate(
        "XOR",
        ["D", "1"],
    ) == "D'"

    assert eval_gate(
        "XOR",
        ["D'", "0"],
    ) == "D'"

    assert eval_gate(
        "XOR",
        ["D'", "1"],
    ) == "D"


def test_xnor_d_propagation():
    assert eval_gate(
        "XNOR",
        ["D", "0"],
    ) == "D'"

    assert eval_gate(
        "XNOR",
        ["D", "1"],
    ) == "D"

    assert eval_gate(
        "XNOR",
        ["D'", "0"],
    ) == "D"

    assert eval_gate(
        "XNOR",
        ["D'", "1"],
    ) == "D'"


def test_xor_d_cancellation():
    assert eval_gate(
        "XOR",
        ["D", "D"],
    ) == "0"

    assert eval_gate(
        "XOR",
        ["D'", "D'"],
    ) == "0"


def test_xor_d_and_d_prime():
    assert eval_gate(
        "XOR",
        ["D", "D'"],
    ) == "1"

    assert eval_gate(
        "XOR",
        ["D'", "D"],
    ) == "1"


def test_xnor_d_cancellation():
    assert eval_gate(
        "XNOR",
        ["D", "D"],
    ) == "1"

    assert eval_gate(
        "XNOR",
        ["D'", "D'"],
    ) == "1"


def test_xnor_d_and_d_prime():
    assert eval_gate(
        "XNOR",
        ["D", "D'"],
    ) == "0"

    assert eval_gate(
        "XNOR",
        ["D'", "D"],
    ) == "0"