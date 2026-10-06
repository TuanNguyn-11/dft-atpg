"""Xuất trace PODEM ra Markdown theo hợp đồng bảy cột dùng chung."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

if TYPE_CHECKING:
    from atpg.circuit import Circuit
    from atpg.podem import PodemResult


COLUMNS = (
    "Bước",
    "Objective (net, giá trị)",
    "Backtrace → PI",
    "Gán PI",
    "Giá trị các net sau imply",
    "D-frontier",
    "Hành động",
)


def _cell(value: object) -> str:
    """Đổi giá trị của trace thành một ô Markdown ổn định, dễ đọc."""
    if value is None:
        return "—"
    if isinstance(value, tuple) and len(value) == 2:
        return f"({value[0]},{value[1]})"
    if isinstance(value, list):
        return "{" + ",".join(str(item) for item in value) + "}" if value else "∅"
    return str(value).replace("|", "\\|").replace("\n", " ")


def _values_cell(circuit: Circuit, values: dict[str, str]) -> str:
    """Ghi PI và các net theo thứ tự Circuit, không phụ thuộc thứ tự dict."""
    pi_values = ",".join(values.get(pi, "X") for pi in circuit.inputs)
    net_order = getattr(circuit, "nets", [*circuit.inputs, *circuit.topo_order])
    other_nets = [net for net in net_order if net not in circuit.inputs]
    net_values = ", ".join(f"{net}={values.get(net, 'X')}" for net in other_nets)
    return f"PI=({pi_values}); {net_values}"


def _trace_rows(circuit: Circuit, result: PodemResult) -> list[list[str]]:
    """Chuẩn hóa steps thành mỗi hàng gán/đảo PI đúng một dòng trace.

    PODEM lưu thao tác phát hiện bế tắc thành một bước backtrack riêng.
    Theo hợp đồng P3, hành động đó thuộc hàng gán PI dẫn tới bế tắc; hàng
    đảo PI tiếp theo mang hành động tiếp tục. Các hàng kết thúc không gán PI
    được gộp vào kết luận thay vì lặp lại cùng trạng thái trong bảng.
    """
    steps = result.steps
    assignment_indexes = [
        index for index, step in enumerate(steps)
        if step.get("Gán PI") is not None
    ]
    rows: list[list[str]] = []

    for row_number, step_index in enumerate(assignment_indexes, 1):
        step = steps[step_index]
        action = step.get("Hành động", "tiếp tục")

        next_index = step_index + 1
        if next_index < len(steps) and steps[next_index].get("Hành động") == "backtrack":
            action = "backtrack"
        elif step.get("Hành động") == "backtrack":
            action = "tiếp tục"
        elif result.status == "ABORTED" and row_number == len(assignment_indexes):
            # Hành động backtrack đã đến hạn nhưng bị chặn bởi giới hạn.
            action = "backtrack"
        elif result.status == "UNTESTABLE" and row_number == len(assignment_indexes):
            action = "thất bại"

        values = step.get("Giá trị các net sau imply", {})
        row = [
            str(row_number),
            _cell(step.get("Objective (net, giá trị)")),
            _cell(step.get("Backtrace → PI")),
            _cell(step.get("Gán PI")),
            _values_cell(circuit, values),
            _cell(step.get("D-frontier", [])),
            action,
        ]
        rows.append(row)

    return rows


def render_trace(circuit: Circuit, result: PodemResult) -> str:
    """Tạo tài liệu Markdown tái lập được từ kết quả PODEM thật."""
    fault = result.fault
    pattern = "".join(result.pattern.get(pi, "X") for pi in circuit.inputs)
    circuit_name = getattr(circuit, "name", "circuit")
    lines = [
        f"# Trace PODEM — {circuit_name}, {fault.net}/SA{fault.stuck_at}",
        "",
        f"- PI theo thứ tự .bench: ({','.join(circuit.inputs)})",
        f"- PO theo thứ tự .bench: ({','.join(circuit.outputs)})",
        f"- Topological order: ({','.join(circuit.topo_order)})",
        f"- Fault: `{fault.net}/SA{fault.stuck_at}`" + (f" trên nhánh vào `{fault.branch_to}`" if fault.branch_to else " (stem)"),
        f"- Status: `{result.status}`",
        f"- Pattern: `{pattern}`",
        f"- Backtracks: `{result.backtracks}`",
        "- Quy ước: mỗi hàng là một lần gán/đảo PI sau imply; Objective và Backtrace dùng `—` khi đảo quyết định; hành động ở hàng trước ghi nhận nhánh dẫn tới backtrack.",
        "",
        "| " + " | ".join(COLUMNS) + " |",
        "|" + "|".join("---" for _ in COLUMNS) + "|",
    ]
    for row in _trace_rows(circuit, result):
        lines.append("| " + " | ".join(row) + " |")

    lines.extend([
        "",
        "## Kết luận",
        "",
        f"- Status: `{result.status}`",
        f"- Pattern: `{pattern}`",
        f"- Backtracks: `{result.backtracks}`",
    ])
    if result.status == "ABORTED":
        lines.append("- Lý do dừng: đạt giới hạn `max_backtracks`; đây không phải kết luận `UNTESTABLE`.")
    elif result.status == "UNTESTABLE":
        lines.append("- Lý do dừng: đã duyệt hết cây quyết định trong giới hạn đã cho.")
    return "\n".join(lines) + "\n"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Tái sinh trace PODEM từ mạch .bench thật.")
    parser.add_argument("--bench", required=True, type=Path, help="đường dẫn mạch .bench")
    parser.add_argument("--fault", required=True, nargs=2, metavar=("NET", "SV"), help="net và stuck-at value 0 hoặc 1")
    parser.add_argument("--output", required=True, type=Path, help="đường dẫn file Markdown đầu ra")
    parser.add_argument("--max-backtracks", type=int, default=1000, help="giới hạn backtrack (mặc định: 1000)")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    net, sv_text = args.fault
    if sv_text not in {"0", "1"}:
        parser.error(f"SV phải là 0 hoặc 1, nhận {sv_text!r}")
    if args.max_backtracks < 0:
        parser.error("--max-backtracks phải >= 0")

    bench = args.bench if args.bench.is_absolute() else Path.cwd() / args.bench
    output = args.output if args.output.is_absolute() else Path.cwd() / args.output
    try:
        # Import ở thời điểm chạy để các hàm định dạng vẫn kiểm thử được
        # độc lập trên branch P5 trước khi tích hợp module Circuit của P6.
        from atpg.circuit import Circuit
        from atpg.faults import Fault, validate_fault
        from atpg.podem import podem

        circuit = Circuit.from_bench(str(bench))
        fault = Fault(net, int(sv_text))
        validate_fault(circuit, fault)
        result = podem(circuit, fault, max_backtracks=args.max_backtracks, trace=True)
        content = render_trace(circuit, result)
        output.write_text(content, encoding="utf-8", newline="\n")
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f"Lỗi xuất trace PODEM: {exc}\n")

    print(f"Đã ghi trace `{output}`: {result.status}, pattern {''.join(result.pattern.get(pi, 'X') for pi in circuit.inputs)}, backtracks {result.backtracks}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
