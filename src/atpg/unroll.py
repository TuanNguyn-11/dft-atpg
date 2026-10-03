"""Biến mạch có DFF thành mạch tổ hợp cho ATPG.

Chỉ dùng giao diện Circuit/Gate/Fault đã thống nhất trong prompt chung. Q@0
trong mạch trải khung là trạng thái ban đầu *không biết*, không phải một PI
điều khiển được trên chip; mẫu do ATPG sinh phải được kiểm tra tính khả đạt.
"""

from __future__ import annotations

from copy import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .circuit import Circuit, Gate
    from .faults import Fault


def _split_gates(c: Circuit) -> tuple[dict[str, Gate], dict[str, Gate]]:
    combinational = {}
    dffs = {}
    for net, gate in c.gates.items():
        if gate.output != net:
            raise ValueError(f"Gate key {net!r} khac output {gate.output!r}")
        if gate.type.upper() == "DFF":
            if len(gate.inputs) != 1:
                raise ValueError(f"DFF {net!r} phai co dung mot ngo vao D")
            dffs[net] = gate
        else:
            combinational[net] = gate
    return combinational, dffs


def _clone_gate(gate: Gate, output: str, inputs: list[str], gate_type: str | None = None) -> Gate:
    return type(gate)(output=output, type=gate_type or gate.type, inputs=inputs)


def _finish(c: Circuit, name: str, inputs: list[str], outputs: list[str], gates: dict[str, Gate]) -> Circuit:
    """Tái tạo metadata đồ thị sau khi bỏ/thêm DFF.

copy(c) giữ tương thích với Circuit của P6 dù constructor có thêm trường.
Không sửa đối tượng đầu vào hoặc các danh sách/dict của nó.
    """
    if len(inputs) != len(set(inputs)) or len(outputs) != len(set(outputs)):
        raise ValueError("PI/PO trung lap")
    if set(inputs) & set(gates):
        raise ValueError("Mot net vua la PI vua la ngo ra cong")

    known = set(inputs) | set(gates)
    fanout: dict[str, list[str]] = {net: [] for net in known}
    indegree: dict[str, int] = {}
    for output, gate in gates.items():
        if gate.type.upper() == "DFF":
            raise ValueError("Mach sau bien doi khong duoc con DFF")
        indegree[output] = 0
        for net in gate.inputs:
            if net not in known:
                raise ValueError(f"Ngo vao cong {output!r} tham chieu net {net!r} khong ton tai")
            fanout[net].append(output)
            if net in gates:
                indegree[output] += 1
    for output in outputs:
        if output not in known:
            raise ValueError(f"PO {output!r} khong ton tai")

    # Kahn theo thứ tự xuất hiện để trace lặp lại được giữa các lần chạy.
    ready = [net for net in gates if indegree[net] == 0]
    topo_order: list[str] = []
    level: dict[str, int] = {net: 0 for net in inputs}
    cursor = 0
    while cursor < len(ready):
        net = ready[cursor]
        cursor += 1
        topo_order.append(net)
        level[net] = 1 + max((level[parent] for parent in gates[net].inputs), default=0)
        for child in fanout[net]:
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
    if len(topo_order) != len(gates):
        raise ValueError("Mach to hop sau bien doi co chu trinh")

    result = copy(c)
    result.name = name
    result.inputs = inputs
    result.outputs = outputs
    result.gates = gates
    result.fanout = fanout
    result.topo_order = topo_order
    result.level = level
    return result


def full_scan(c: Circuit) -> Circuit:
    """Cắt mỗi DFF: Q thành pseudo-PI, D thành pseudo-PO.

Đầu ra D có thể trùng PO thật; giữ mỗi tên đúng một lần.
    """
    combinational, dffs = _split_gates(c)
    inputs = list(dict.fromkeys([*c.inputs, *dffs]))
    outputs = list(dict.fromkeys([*c.outputs, *(gate.inputs[0] for gate in dffs.values())]))
    gates = {
        net: _clone_gate(gate, net, list(gate.inputs))
        for net, gate in combinational.items()
    }
    return _finish(c, f"{c.name}_full_scan", inputs, outputs, gates)


def unroll(c: Circuit, k: int) -> Circuit:
    """Trải k chu kỳ; Q@t = D@(t-1) với t từ 1 tới k-1.

Quan sát PO thật tại mỗi khung. Q@0 là PI hình thức biểu diễn trạng thái
ban đầu chưa biết; người dùng phải chứng minh mẫu độc lập với Q@0 hoặc có
chuỗi khởi tạo đưa FF tới trạng thái mà mẫu cần.
    """
    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        raise ValueError("k phai la so nguyen duong")
    combinational, dffs = _split_gates(c)
    inputs = [f"{net}@{t}" for t in range(k) for net in c.inputs]
    inputs.extend(f"{net}@0" for net in dffs)
    outputs = [f"{net}@{t}" for t in range(k) for net in c.outputs]
    gates: dict[str, Gate] = {}

    for t in range(k):
        if t:
            for q, dff in dffs.items():
                gates[f"{q}@{t}"] = _clone_gate(
                    dff, f"{q}@{t}", [f"{dff.inputs[0]}@{t - 1}"], "BUFF"
                )
        for net, gate in combinational.items():
            gates[f"{net}@{t}"] = _clone_gate(
                gate, f"{net}@{t}", [f"{parent}@{t}" for parent in gate.inputs]
            )

    return _finish(c, f"{c.name}_unroll_{k}", inputs, outputs, gates)


def fault_in_frames(fault: Fault, k: int) -> list[Fault]:
    """Sao lỗi vật lý ở một net/nhánh sang từng khung thời gian.

Với lỗi nhánh đi vào DFF, nhánh khung cuối không có FF kế tiếp trong
unroll(k), nên danh sách trả về chỉ dùng trực tiếp cho nhánh cổng tổ hợp.
    """
    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        raise ValueError("k phai la so nguyen duong")
    return [
        type(fault)(
            net=f"{fault.net}@{t}",
            stuck_at=fault.stuck_at,
            branch_to=f"{fault.branch_to}@{t}" if fault.branch_to is not None else None,
        )
        for t in range(k)
    ]
