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