# logic.py
# Biểu diễn và tính toán logic 5 giá trị cho ATPG/PODEM.

from __future__ import annotations


# Quy ước:
# 0  = (0, 0)
# 1  = (1, 1)
# D  = (1, 0)
# D' = (0, 1)
# X  = unknown


VALUE_TO_PAIR: dict[str, tuple[int | None, int | None]] = {
    "0": (0, 0),
    "1": (1, 1),
    "D": (1, 0),
    "D'": (0, 1),
    "X": (None, None),
}

PAIR_TO_VALUE: dict[tuple[int, int], str] = {
    (0, 0): "0",
    (1, 1): "1",
    (1, 0): "D",
    (0, 1): "D'",
}


def _and_bit(a: int | None, b: int | None) -> int | None:
    """AND 3-valued cho từng thành phần."""
    if a == 0 or b == 0:
        return 0
    if a == 1 and b == 1:
        return 1
    return None


def _or_bit(a: int | None, b: int | None) -> int | None:
    """OR 3-valued cho từng thành phần."""
    if a == 1 or b == 1:
        return 1
    if a == 0 and b == 0:
        return 0
    return None


def _xor_bit(a: int | None, b: int | None) -> int | None:
    """XOR 3-valued cho từng thành phần."""
    if a is None or b is None:
        return None
    return a ^ b


def _not_bit(a: int | None) -> int | None:
    """NOT cho từng thành phần."""
    if a is None:
        return None
    return 1 - a


def _apply_binary(
    operation,
    input_values: list[str],
) -> str:
    """Tính cổng nhiều ngõ vào theo từng thành phần."""
    if not input_values:
        raise ValueError("Cổng phải có ít nhất một ngõ vào.")

    pairs = [VALUE_TO_PAIR[value] for value in input_values]

    result = pairs[0]

    for pair in pairs[1:]:
        result = (
            operation(result[0], pair[0]),
            operation(result[1], pair[1]),
        )

    return PAIR_TO_VALUE.get(result, "X")


def _invert(value: str) -> str:
    """Đảo cả hai thành phần để thực hiện NOT/NAND/NOR."""
    pair = VALUE_TO_PAIR[value]
    result = (_not_bit(pair[0]), _not_bit(pair[1]))

    return PAIR_TO_VALUE.get(result, "X")


def eval_gate(gate_type: str, input_values: list[str]) -> str:
    """
    Đánh giá một cổng logic theo logic 5 giá trị.

    gate_type:
        AND, NAND, OR, NOR, NOT, BUFF, XOR, XNOR

    input_values:
        Danh sách các giá trị "0", "1", "X", "D", "D'".

    Trả về:
        Một trong "0", "1", "X", "D", "D'".
    """
    gate_type = gate_type.upper()

    for value in input_values:
        if value not in VALUE_TO_PAIR:
            raise ValueError(f"Giá trị logic không hợp lệ: {value}")

    if gate_type == "AND":
        return _apply_binary(_and_bit, input_values)

    if gate_type == "NAND":
        return _invert(_apply_binary(_and_bit, input_values))

    if gate_type == "OR":
        return _apply_binary(_or_bit, input_values)

    if gate_type == "NOR":
        return _invert(_apply_binary(_or_bit, input_values))

    if gate_type == "XOR":
        return _apply_binary(_xor_bit, input_values)

    if gate_type == "XNOR":
        return _invert(_apply_binary(_xor_bit, input_values))

    if gate_type == "NOT":
        if len(input_values) != 1:
            raise ValueError("NOT phải có đúng một ngõ vào.")
        return _invert(input_values[0])

    if gate_type == "BUFF":
        if len(input_values) != 1:
            raise ValueError("BUFF phải có đúng một ngõ vào.")
        return input_values[0]

    raise ValueError(f"Loại cổng không được hỗ trợ: {gate_type}")