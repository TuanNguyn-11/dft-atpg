# podem.py
# Cài đặt các thành phần cốt lõi của thuật toán PODEM.

from __future__ import annotations

from dataclasses import dataclass

from typing import TYPE_CHECKING

from .logic import PAIR_TO_VALUE, VALUE_TO_PAIR, eval_gate

@dataclass
class Decision:
    # PI đã được chọn trong một nhánh tìm kiếm.
    pi: str

    # Giá trị đã thử đầu tiên: 0 hoặc 1.
    value: int

    # False: chưa thử giá trị còn lại.
    # True: đã thử cả hai giá trị.
    tried_other: bool = False

@dataclass
class PodemResult:
    # Fault mà PODEM đang xử lý.
    fault: "Fault"

    # Trạng thái cuối cùng:
    # DETECTED / UNTESTABLE / ABORTED
    status: str

    # Test pattern tại các Primary Input.
    pattern: dict[str, str]

    # Số lần backtrack.
    backtracks: int

    # Trace từng bước của PODEM.
    steps: list[dict]

if TYPE_CHECKING:
    from .circuit import Circuit
    from .faults import Fault


def _inject_stuck_at(
    value: str,
    stuck_at: int,
) -> str:
    """
    Cấy stuck-at vào một giá trị logic 5 giá trị.

    Giữ nguyên rail của mạch tốt và ép rail của mạch lỗi
    về giá trị stuck-at.
    """

    stuck_value = str(stuck_at)

    if value == "X":
        return "X"

    if value == "0":
        if stuck_value == "0":
            return "0"
        return "D'"

    if value == "1":
        if stuck_value == "1":
            return "1"
        return "D"

    if value == "D":
        if stuck_value == "0":
            return "D"
        return "1"

    if value == "D'":
        if stuck_value == "0":
            return "0"
        return "D'"

    raise ValueError(
        f"Giá trị logic 5 giá trị không hợp lệ: {value}"
    )


def imply(
    c: "Circuit",
    pattern: dict[str, str],
    fault: "Fault | list[Fault]",
) -> dict[str, str]:
    """
    Mô phỏng tiến toàn mạch theo logic 5 giá trị.

    Giá trị trong mạch được duy trì trực tiếp dưới dạng:
    "0", "1", "X", "D", "D'".

    Fault được cấy tại đúng vị trí trước khi giá trị đó
    được truyền sang các gate tiếp theo.
    """

    # Chuẩn hóa fault thành danh sách.
    faults = fault if isinstance(fault, list) else [fault]

    # Kiểm tra pattern.
    for net, value in pattern.items():
        if value not in {"0", "1", "X"}:
            raise ValueError(
                f"Pattern của PI {net} không hợp lệ: {value}"
            )

    # Trạng thái logic 5 giá trị của toàn mạch.
    values: dict[str, str] = {}

    # ---------------------------------------------------------
    # 1. Khởi tạo Primary Inputs
    # ---------------------------------------------------------

    for pi in c.inputs:
        values[pi] = pattern.get(pi, "X")

    # ---------------------------------------------------------
    # 2. Cấy stem fault nếu fault nằm trên Primary Input
    # ---------------------------------------------------------

    for f in faults:
        if f.branch_to is None and f.net in c.inputs:
            values[f.net] = _inject_stuck_at(
                values[f.net],
                f.stuck_at,
            )

    # ---------------------------------------------------------
    # 3. Mô phỏng theo topo_order
    # ---------------------------------------------------------

    for output_net in c.topo_order:
        gate = c.gates[output_net]

        # Lấy input hiện tại theo logic 5 giá trị.
        gate_inputs = [
            values.get(input_net, "X")
            for input_net in gate.inputs
        ]

        # -----------------------------------------------------
        # 3a. Cấy branch fault
        # -----------------------------------------------------

        for f in faults:
            if f.branch_to == gate.output:

                for index, input_net in enumerate(gate.inputs):
                    if input_net != f.net:
                        continue

                    gate_inputs[index] = _inject_stuck_at(
                        gate_inputs[index],
                        f.stuck_at,
                    )

        # -----------------------------------------------------
        # 3b. Tính gate bằng logic 5 giá trị
        # -----------------------------------------------------

        output_value = eval_gate(
            gate.type,
            gate_inputs,
        )

        # -----------------------------------------------------
        # 3c. Cấy stem fault tại output của gate
        # -----------------------------------------------------

        for f in faults:
            if f.branch_to is None and f.net == gate.output:
                output_value = _inject_stuck_at(
                    output_value,
                    f.stuck_at,
                )

        values[gate.output] = output_value

    return values

#Thêm helper _branch_value()
def _branch_value(
    c: "Circuit",
    values: dict[str, str],
    fault: "Fault",
    gate_output: str,
    input_net: str,
) -> str:
    """
    Xác định giá trị thực tế trên một input của gate,
    có xét branch fault nếu fault nằm đúng trên nhánh đó.
    """
    value = values.get(input_net, "X")

    # Nếu là stem fault thì giá trị của net được dùng trực tiếp.
    if fault.branch_to is None:
        return value

    # Không phải gate đích của branch fault.
    if gate_output != fault.branch_to:
        return value

    # Không phải đúng nhánh xuất phát từ fault.net.
    if input_net != fault.net:
        return value

    # Chưa kích hoạt fault nên nhánh vẫn chưa tạo sai biệt.
    if value == "X":
        return "X"

    # Nếu stem đang bằng giá trị stuck-at thì không có sai biệt.
    if value == str(fault.stuck_at):
        return value

    # Stem đang ở giá trị đối lập stuck-at,
    # nên riêng branch này xuất hiện D hoặc D'.
    if fault.stuck_at == 0:
        return "D"

    return "D'"

def _get_d_frontier(
    c: "Circuit",
    values: dict[str, str],
    fault: "Fault | None" = None,
) -> list[str]:
    """
    Tìm D-frontier theo đúng thứ tự topo.

    D-frontier gồm các gate:
    - output đang là X
    - có ít nhất một input là D hoặc D'
    """
    frontier: list[str] = []

    for net in c.topo_order:
        if values.get(net, "X") != "X":
            continue

        gate = c.gates[net]

        # Kiểm tra từng input của gate.
        for input_net in gate.inputs:
            # Lấy giá trị thực tế trên nhánh,
            # có xét branch fault nếu fault là branch fault.
            effective_value = _branch_value(
                c,
                values,
                fault,
                gate.output,
                input_net,
            )

            # Nếu input có sai biệt D/D' thì gate thuộc D-frontier.
            if effective_value in {"D", "D'"}:
                frontier.append(net)
                break

    return frontier

def _has_x_path(
    c: "Circuit",
    start_net: str,
    values: dict[str, str],
) -> bool:
    """
    Kiểm tra từ một net có đường X tới ít nhất một PO hay không.

    Chỉ đi qua các net có giá trị X.
    """
    if start_net in c.outputs:
        return values.get(start_net, "X") == "X"

    queue = [start_net]
    visited: set[str] = {start_net}

    while queue:
        current = queue.pop(0)

        for next_net in c.fanout.get(current, []):
            if next_net in visited:
                continue

            if values.get(next_net, "X") != "X":
                continue

            if next_net in c.outputs:
                return True

            visited.add(next_net)
            queue.append(next_net)

    return False

def _is_detected(
    c: "Circuit",
    values: dict[str, str],
) -> bool:
    """
    Kiểm tra fault đã được phát hiện chưa.

    Fault được phát hiện nếu bất kỳ Primary Output nào
    có giá trị D hoặc D'.
    """
    return any(
        values.get(po, "X") in {"D", "D'"}
        for po in c.outputs
    )

def objective(
    c: "Circuit",
    values: dict[str, str],
    fault: "Fault",
) -> tuple[str, int] | None:
    """
    Chọn Objective tiếp theo cho PODEM.

    Trả về:
        (net, value)

    hoặc:
        None nếu nhánh hiện tại không thể tiếp tục.
    """

    current_value = values.get(fault.net, "X")

    # ---------------------------------------------------------
    # Giai đoạn 1: kích hoạt fault
    # ---------------------------------------------------------

    if current_value == "X":
        # Muốn kích hoạt SA0 -> good = 1.
        # Muốn kích hoạt SA1 -> good = 0.
        return fault.net, 1 - fault.stuck_at

    # Giá trị D/D' tương ứng với stem fault đã được kích hoạt.
    fault_effect = "D" if fault.stuck_at == 0 else "D'"

    # ---------------------------------------------------------
    # Giai đoạn 2: fault đã được kích hoạt -> lan truyền
    # ---------------------------------------------------------

    # Stem fault:
    #   stem mang D/D'.
    #
    # Branch fault:
    #   stem vẫn mang giá trị logic bình thường,
    #   nhưng nhánh được chỉ định bởi branch_to mang sai biệt.
    if (
        (
            fault.branch_to is None
            and current_value == fault_effect
        )
        or
        (
            fault.branch_to is not None
            and current_value == str(1 - fault.stuck_at)
        )
    ):
        # D-frontier phải xét cả stem fault và branch fault.
        d_frontier = _get_d_frontier(
            c,
            values,
            fault,
        )

        for gate_net in d_frontier:
            # Chỉ chọn D-frontier còn đường X tới PO.
            if not _has_x_path(
                c,
                gate_net,
                values,
            ):
                continue

            gate = c.gates[gate_net]
            gate_type = gate.type.upper()

            # -------------------------------------------------
            # Giá trị objective khi truyền fault
            # -------------------------------------------------
            #
            # AND/NAND -> 1
            # OR/NOR   -> 0
            # XOR/XNOR -> 0 theo P3-v1.1
            #
            if gate_type in {"AND", "NAND"}:
                propagation_value = 1

            elif gate_type in {"OR", "NOR"}:
                propagation_value = 0

            elif gate_type in {"XOR", "XNOR"}:
                propagation_value = 0

            else:
                # NOT/BUFF không cần objective propagation
                # trong bước này.
                continue

            # Chọn input X đầu tiên theo đúng thứ tự Gate.inputs.
            for input_net in gate.inputs:
                if values.get(input_net, "X") == "X":
                    return input_net, propagation_value

        # Không còn D-frontier có X-path.
        return None

    # ---------------------------------------------------------
    # Fault chưa thể kích hoạt / trạng thái không hợp lệ
    # ---------------------------------------------------------

    if current_value == str(fault.stuck_at):
        return None

    return None

def backtrace(
    c: "Circuit",
    values: dict[str, str],
    objective_net: str,
    objective_value: int,
) -> tuple[str, int]:
    """
    Backtrace từ Objective về một Primary Input.

    Quy tắc:
    - Chọn input X đầu tiên theo Gate.inputs.
    - AND, OR, BUFF: giữ nguyên objective value.
    - NAND, NOR, NOT: đảo objective value.
    - XOR/XNOR: xử lý theo parity của rail tốt.

    Trả về:
        (PI, value)
    """

    current_net = objective_net
    current_value = objective_value

    while current_net not in c.inputs:

        gate = c.gates[current_net]
        gate_type = gate.type.upper()

        # -----------------------------------------------------
        # XOR/XNOR
        # -----------------------------------------------------

        if gate_type in {"XOR", "XNOR"}:

            # Các input đang còn X, giữ nguyên thứ tự Gate.inputs.
            unknown_inputs = [
                input_net
                for input_net in gate.inputs
                if values.get(input_net, "X") == "X"
            ]

            if not unknown_inputs:
                raise ValueError(
                    f"Không còn input X để backtrace từ net {current_net}."
                )

            # q = 0 với XOR, q = 1 với XNOR.
            q = 0 if gate_type == "XOR" else 1

            # p = XOR các bit tốt của các input đã biết.
            # good:
            #   0  -> 0
            #   1  -> 1
            #   D  -> 1
            #   D' -> 0
            p = 0

            for input_net in gate.inputs:
                value = values.get(input_net, "X")

                if value == "0":
                    good_bit = 0

                elif value == "1":
                    good_bit = 1

                elif value == "D":
                    good_bit = 1

                elif value == "D'":
                    good_bit = 0

                else:
                    # X không tham gia vào p.
                    continue

                p ^= good_bit

            # -------------------------------------------------
            # Chỉ còn đúng một X:
            #
            # u = v XOR q XOR p
            # -------------------------------------------------
            if len(unknown_inputs) == 1:

                selected_input = unknown_inputs[0]

                current_value = (
                    current_value
                    ^ q
                    ^ p
                )

            # -------------------------------------------------
            # Còn từ hai X trở lên:
            #
            # Chọn X đầu tiên và ưu tiên thử 0.
            # -------------------------------------------------
            else:

                selected_input = unknown_inputs[0]
                current_value = 0

            current_net = selected_input

            continue

        # -----------------------------------------------------
        # Các loại gate thông thường
        # -----------------------------------------------------

        # Tìm input X đầu tiên theo đúng thứ tự Gate.inputs.
        selected_input = None

        for input_net in gate.inputs:
            if values.get(input_net, "X") == "X":
                selected_input = input_net
                break

        if selected_input is None:
            raise ValueError(
                f"Không tìm thấy input X để backtrace "
                f"từ net {current_net}."
            )

        # Cập nhật objective value theo loại gate.
        if gate_type in {"NAND", "NOR", "NOT"}:
            current_value = 1 - current_value

        elif gate_type in {"AND", "OR", "BUFF"}:
            pass

        else:
            raise ValueError(
                f"Backtrace chưa hỗ trợ loại cổng: {gate_type}"
            )

        current_net = selected_input

    return current_net, current_value

def backtrack(
    decisions: list[Decision],
) -> tuple[str, int] | None:
    """
    Quay lui tới quyết định gần nhất còn một giá trị chưa thử.

    Trả về:
        (PI, giá trị mới)

    Trả về None nếu không còn nhánh nào để thử.
    """

    while decisions:
        decision = decisions[-1]

        # Giá trị còn lại chưa được thử.
        if not decision.tried_other:
            decision.tried_other = True

            # Đảo giá trị hiện tại: 0 <-> 1.
            decision.value = 1 - decision.value

            return decision.pi, decision.value

        # Cả hai giá trị đã được thử.
        # Bỏ quyết định này và quay lên mức trước.
        decisions.pop()

    # Toàn bộ cây quyết định đã được duyệt.
    return None

def _pattern_from_decisions(
    c: "Circuit",
    decisions: list[Decision],
) -> dict[str, str]:
    """
    Tạo pattern đầy đủ cho tất cả Primary Input.

    PI chưa được PODEM quyết định sẽ giữ giá trị X.
    """
    pattern = {
        pi: "X"
        for pi in c.inputs
    }

    for decision in decisions:
        pattern[decision.pi] = str(decision.value)

    return pattern

def _validate_fault_in_circuit(c: "Circuit", fault: "Fault") -> None:
    """
    Kiểm tra fault thuộc đúng mạch c; sai thì raise ValueError.

    Chỉ dùng thuộc tính chung (net, stuck_at, branch_to; gates, inputs)
    để chạy được với Circuit/Fault thật lẫn bản giả trong test.
    Input sai không được trả về UNTESTABLE/ABORTED như kết luận thuật toán.
    """
    stuck_at = getattr(fault, "stuck_at", None)
    if isinstance(stuck_at, bool) or stuck_at not in (0, 1):
        raise ValueError(
            f"stuck_at phải là 0 hoặc 1, nhận {stuck_at!r}."
        )

    net = getattr(fault, "net", None)
    if net not in c.gates and net not in c.inputs:
        raise ValueError(
            f"Fault {net}/SA{stuck_at}: net {net!r} không tồn tại trong mạch."
        )

    branch_to = getattr(fault, "branch_to", None)
    if branch_to is not None:
        gate = c.gates.get(branch_to)
        if gate is None:
            raise ValueError(
                f"Fault {net}->{branch_to}/SA{stuck_at}: "
                f"cổng {branch_to!r} không tồn tại trong mạch."
            )
        if net not in gate.inputs:
            raise ValueError(
                f"Fault {net}->{branch_to}/SA{stuck_at}: "
                f"cổng {branch_to!r} không nhận net {net!r} làm ngõ vào."
            )


def podem(
    c: "Circuit",
    fault: "Fault | list[Fault]",
    max_backtracks: int = 1000,
    trace: bool = False,
) -> PodemResult:
    """
    Chạy thuật toán PODEM cho single fault hoặc danh sách fault-frame.

    Với single fault:
    - xử lý giống phiên bản PODEM hiện tại.

    Với list[Fault]:
    - danh sách được xem là các fault-instance của cùng một fault
      trên các frame của mạch tuần tự đã trải khung;
    - imply() vẫn nhận toàn bộ danh sách fault;
    - từng fault trong danh sách lần lượt được chọn làm target
      cho Objective -> Backtrace.
    """

    # ---------------------------------------------------------
    # 1. Chuẩn hóa fault
    # ---------------------------------------------------------

    # Single fault -> chuyển thành danh sách một phần tử.
    # List fault -> giữ nguyên toàn bộ danh sách.
    faults = fault if isinstance(fault, list) else [fault]

    # Không cho phép danh sách rỗng.
    if not faults:
        raise ValueError(
            "Danh sách fault không được rỗng."
        )

    # Giới hạn quay lui phải là số nguyên không âm.
    if (
        isinstance(max_backtracks, bool)
        or not isinstance(max_backtracks, int)
        or max_backtracks < 0
    ):
        raise ValueError(
            f"max_backtracks phải là số nguyên >= 0, nhận {max_backtracks!r}."
        )

    # Mọi fault (kể cả từng fault-frame) phải thuộc mạch đang chạy.
    for target in faults:
        _validate_fault_in_circuit(c, target)

    # ---------------------------------------------------------
    # 2. Hàm chạy PODEM cho một target fault
    # ---------------------------------------------------------

    def run_target_fault(
        target_fault: "Fault",
    ) -> PodemResult:
        """
        Chạy một phiên PODEM với target_fault hiện tại.

        imply() vẫn nhận toàn bộ faults để mô phỏng đầy đủ
        các fault-instance trên mạch trải khung.
        """

        # -----------------------------------------------------
        # 2.1. Khởi tạo trạng thái
        # -----------------------------------------------------

        # Ban đầu tất cả Primary Input đều chưa được quyết định.
        pattern: dict[str, str] = {
            pi: "X"
            for pi in c.inputs
        }

        # Stack lưu các quyết định PI đã chọn.
        decisions: list[Decision] = []

        # Số lần backtrack.
        backtracks = 0

        # Trace từng bước.
        steps: list[dict] = []

        step_number = 0

        # -----------------------------------------------------
        # 2.2. Vòng lặp chính của PODEM
        # -----------------------------------------------------

        while True:

            # =================================================
            # A. IMPLY
            # =================================================

            # Mô phỏng toàn bộ mạch với toàn bộ fault-frame.
            values = imply(
                c,
                pattern,
                faults,
            )

            # D-frontier được xác định theo target fault hiện tại.
            d_frontier = _get_d_frontier(
                c,
                values,
                target_fault,
            )

            # =================================================
            # B. KIỂM TRA FAULT ĐÃ ĐƯỢC PHÁT HIỆN CHƯA
            # =================================================

            if _is_detected(
                c,
                values,
            ):
                step_number += 1

                if trace:
                    steps.append(
                        {
                            "Bước": step_number,
                            "Objective (net, giá trị)": None,
                            "Backtrace → PI": None,
                            "Gán PI": None,
                            "Giá trị các net sau imply": values.copy(),
                            "D-frontier": d_frontier.copy(),
                            "Hành động": "thành công",
                        }
                    )

                return PodemResult(
                    fault=target_fault,
                    status="DETECTED",
                    pattern=pattern.copy(),
                    backtracks=backtracks,
                    steps=steps,
                )

            # =================================================
            # C. OBJECTIVE
            # =================================================

            obj = objective(
                c,
                values,
                target_fault,
            )

            # =================================================
            # D. KHÔNG CÒN OBJECTIVE
            #    -> nhánh hiện tại thất bại
            # =================================================

            if obj is None:

                # -------------------------------------------------
                # D1. Đã đạt giới hạn backtrack
                # -------------------------------------------------

                if backtracks >= max_backtracks:

                    step_number += 1

                    if trace:
                        steps.append(
                            {
                                "Bước": step_number,
                                "Objective (net, giá trị)": None,
                                "Backtrace → PI": None,
                                "Gán PI": None,
                                "Giá trị các net sau imply": values.copy(),
                                "D-frontier": d_frontier.copy(),
                                "Hành động": "thất bại",
                            }
                        )

                    return PodemResult(
                        fault=target_fault,
                        status="ABORTED",
                        pattern=pattern.copy(),
                        backtracks=backtracks,
                        steps=steps,
                    )

                # -------------------------------------------------
                # D2. Thử backtrack
                # -------------------------------------------------

                new_assignment = backtrack(
                    decisions
                )

                # -------------------------------------------------
                # D3. Không còn quyết định nào để quay lại
                # -------------------------------------------------

                if new_assignment is None:

                    step_number += 1

                    if trace:
                        steps.append(
                            {
                                "Bước": step_number,
                                "Objective (net, giá trị)": None,
                                "Backtrace → PI": None,
                                "Gán PI": None,
                                "Giá trị các net sau imply": values.copy(),
                                "D-frontier": d_frontier.copy(),
                                "Hành động": "thất bại",
                            }
                        )

                    return PodemResult(
                        fault=target_fault,
                        status="UNTESTABLE",
                        pattern=pattern.copy(),
                        backtracks=backtracks,
                        steps=steps,
                    )

                # -------------------------------------------------
                # D4. Có nhánh mới
                # -------------------------------------------------

                backtracks += 1

                # Tạo lại pattern từ decision stack.
                pattern = _pattern_from_decisions(
                    c,
                    decisions,
                )

                # Quan trọng:
                # Sau khi backtrack phải imply lại trạng thái mới.
                values = imply(
                    c,
                    pattern,
                    faults,
                )

                # Cập nhật lại D-frontier theo trạng thái mới.
                d_frontier = _get_d_frontier(
                    c,
                    values,
                    target_fault,
                )

                step_number += 1

                if trace:
                    steps.append(
                        {
                            "Bước": step_number,

                            # Backtrack không phải là một lần
                            # Backtrace Objective -> PI mới.
                            "Objective (net, giá trị)": None,
                            "Backtrace → PI": None,

                            # Đây là PI vừa được đảo giá trị.
                            "Gán PI": (
                                f"{new_assignment[0]}="
                                f"{new_assignment[1]}"
                            ),

                            # Phải ghi trạng thái MỚI sau imply.
                            "Giá trị các net sau imply": values.copy(),
                            "D-frontier": d_frontier.copy(),

                            "Hành động": "backtrack",
                        }
                    )

                # Tiếp tục vòng lặp với trạng thái mới.
                continue

            # =================================================
            # E. BACKTRACE OBJECTIVE -> PRIMARY INPUT
            # =================================================

            objective_net, objective_value = obj

            pi, pi_value = backtrace(
                c,
                values,
                objective_net,
                objective_value,
            )

            # =================================================
            # F. LƯU QUYẾT ĐỊNH
            # =================================================

            decision = Decision(
                pi=pi,
                value=pi_value,
            )

            decisions.append(decision)

            # Tạo pattern đầy đủ:
            # PI chưa quyết định -> X
            # PI đã quyết định -> 0/1
            pattern = _pattern_from_decisions(
                c,
                decisions,
            )

            # =================================================
            # G. IMPLY SAU KHI GÁN PI
            # =================================================

            # Tiếp tục mô phỏng với toàn bộ fault-frame.
            new_values = imply(
                c,
                pattern,
                faults,
            )

            # Cập nhật D-frontier theo target fault.
            new_d_frontier = _get_d_frontier(
                c,
                new_values,
                target_fault,
            )

            step_number += 1

            # =================================================
            # H. NẾU ĐÃ DETECTED -> GHI TRACE VÀ DỪNG
            # =================================================

            if _is_detected(
                c,
                new_values,
            ):

                if trace:
                    steps.append(
                        {
                            "Bước": step_number,
                            "Objective (net, giá trị)": (
                                objective_net,
                                objective_value,
                            ),
                            "Backtrace → PI": (
                                pi,
                                pi_value,
                            ),
                            "Gán PI": (
                                f"{pi}={pi_value}"
                            ),
                            "Giá trị các net sau imply": (
                                new_values.copy()
                            ),
                            "D-frontier": (
                                new_d_frontier.copy()
                            ),
                            "Hành động": "thành công",
                        }
                    )

                return PodemResult(
                    fault=target_fault,
                    status="DETECTED",
                    pattern=pattern.copy(),
                    backtracks=backtracks,
                    steps=steps,
                )

            # =================================================
            # I. CHƯA DETECTED -> TIẾP TỤC
            # =================================================

            if trace:
                steps.append(
                    {
                        "Bước": step_number,
                        "Objective (net, giá trị)": (
                            objective_net,
                            objective_value,
                        ),
                        "Backtrace → PI": (
                            pi,
                            pi_value,
                        ),
                        "Gán PI": (
                            f"{pi}={pi_value}"
                        ),
                        "Giá trị các net sau imply": (
                            new_values.copy()
                        ),
                        "D-frontier": (
                            new_d_frontier.copy()
                        ),
                        "Hành động": "tiếp tục",
                    }
                )

    # ---------------------------------------------------------
    # 3. Single fault
    # ---------------------------------------------------------

    if len(faults) == 1:
        return run_target_fault(
            faults[0]
        )

    # ---------------------------------------------------------
    # 4. Multi-frame fault
    # ---------------------------------------------------------

    # Với list[Fault], lần lượt chọn từng fault-frame làm
    # target cho Objective.
    #
    # imply() vẫn luôn nhận toàn bộ faults.
    last_untestable: PodemResult | None = None
    last_aborted: PodemResult | None = None

    for target_fault in faults:

        result = run_target_fault(
            target_fault
        )

        # Chỉ cần một frame phát hiện được fault
        # thì fault vật lý đã được phát hiện.
        if result.status == "DETECTED":
            return result

        if result.status == "ABORTED":
            last_aborted = result

        else:
            last_untestable = result

    # ---------------------------------------------------------
    # 5. Tất cả target fault đều thất bại
    # ---------------------------------------------------------

    # Nếu có một phiên bị giới hạn backtrack,
    # giữ trạng thái ABORTED.
    if last_aborted is not None:
        return last_aborted

    # Nếu tất cả đều không thể test,
    # trả về UNTESTABLE.
    if last_untestable is not None:
        return last_untestable

    # Trường hợp này chỉ có thể xảy ra khi faults không hợp lệ,
    # nhưng đã được kiểm tra ở đầu hàm.
    raise RuntimeError(
        "PODEM không tạo được kết quả."
    )