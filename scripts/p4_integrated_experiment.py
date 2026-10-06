"""Thí nghiệm full scan P4 trên Circuit, PODEM và fault simulator thật.

Chạy từ gốc repo:
    python scripts/p4_integrated_experiment.py --md results/seq_integrated_full_scan.md

Script p4_seq_experiment.py là oracle nhị phân độc lập, không bị thay thế.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from itertools import product
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from atpg.circuit import Circuit
from atpg.fault_sim import coverage, detects_cube
from atpg.faults import Fault
from atpg.podem import podem
from atpg.unroll import full_scan

import p4_seq_experiment as reference


def _commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def _filled(cube: dict[str, str], inputs: list[str]) -> dict[str, int]:
    return {net: 0 if cube.get(net, "X") == "X" else int(cube[net]) for net in inputs}


def _independent_check(cube: dict[str, str], fault: Fault) -> bool:
    """Kiểm mọi cách điền X qua oracle P4, độc lập với fault_sim."""
    for bits in product("01", repeat=3):
        values = dict(zip(("A", "B", "Q"), bits))
        if any(cube[net] not in ("X", values[net]) for net in values):
            continue
        a, b, q = (int(values[net]) for net in ("A", "B", "Q"))
        if reference.one_cycle(a, b, q) == reference.one_cycle(
            a, b, q, (fault.net, fault.stuck_at)
        ):
            return False
    return True


def run() -> tuple[str, dict]:
    if sys.version_info < (3, 10):
        raise RuntimeError("Cần Python >= 3.10")
    base = Circuit.from_bench(str(ROOT / "circuits" / "seq_example.bench"))
    scan = full_scan(base)
    if scan.inputs != ["A", "B", "Q"] or scan.outputs != ["Y", "D"]:
        raise RuntimeError("Thứ tự PI/PO của mạch full scan đã thay đổi")
    faults = [Fault(net, sv) for net in base.nets for sv in (0, 1)]
    if len(faults) != 18 or any(f.branch_to is not None for f in faults):
        raise RuntimeError("Fault universe phải có đúng 18 lỗi stem vật lý")

    rows = []
    patterns = []
    detected = 0
    for fault in faults:
        result = podem(scan, fault)
        cube = {net: result.pattern.get(net, "X") for net in scan.inputs}
        sim_ok = independent_ok = "-"
        filled = "-"
        if result.status == "DETECTED":
            detected += 1
            simulator_result = detects_cube(scan, cube, fault)
            oracle_result = _independent_check(cube, fault)
            if simulator_result is not True or oracle_result is not True:
                raise AssertionError(f"PODEM {fault}: cube chưa được xác nhận bởi hai oracle")
            sim_ok = independent_ok = "OK"
            pattern = _filled(cube, scan.inputs)
            patterns.append(pattern)
            filled = "".join(str(pattern[net]) for net in scan.inputs)
        rows.append(
            (str(fault), result.status,
             "".join(cube[net] for net in scan.inputs) if result.pattern else "-",
             result.backtracks, sim_ok, independent_ok, filled)
        )

    unique_patterns = list(dict.fromkeys(tuple(p[net] for net in scan.inputs) for p in patterns))
    pattern_set = [dict(zip(scan.inputs, bits)) for bits in unique_patterns]
    cov = coverage(scan, pattern_set, faults)
    max_single = max(
        coverage(scan, [dict(zip(scan.inputs, bits))], faults)["detected"]
        for bits in product((0, 1), repeat=len(scan.inputs))
    )
    lines = [
        "# P4 — Full scan trên API tích hợp\n",
        f"- Commit mã nguồn lúc chạy: `{_commit()}`",
        f"- Python {platform.python_version()} ({platform.python_implementation()}); "
        f"{platform.system()} {platform.release()}",
        f"- Thời điểm chạy: {datetime.now().isoformat(timespec='seconds')}",
        "- Lệnh từ gốc repo: `python scripts/p4_integrated_experiment.py "
        "--md results/seq_integrated_full_scan.md`",
        "- Nguồn: `circuits/seq_example.bench`; `Circuit.from_bench`, "
        "`full_scan`, `podem`, `detects_cube`, `coverage`; oracle độc lập "
        "`scripts/p4_seq_experiment.py`.",
        "- Mẫu số: 18 lỗi stem của `base.nets` × SA0/SA1; không dùng "
        "`all_faults(scan)` vì hàm đó còn sinh lỗi nhánh.",
        "- Full scan: PI `[A,B,Q]`, PO `[Y,D]`. Shift in đặt `Q`, "
        "capture cập nhật FF từ `D`, shift out quan sát `D` qua pseudo-PO; "
        "mỗi vector logic còn cần thời gian dịch/capture vật lý.\n",
        "| Lỗi stem | PODEM | Cube A,B,Q | Backtracks | Simulator: mọi X | "
        "Oracle P4: mọi X | Điền X=0 |",
        "|---|---|---|---:|---|---|---|",
    ]
    lines.extend("| " + " | ".join(map(str, row)) + " |" for row in rows)
    lines.extend([
        "\n## Bộ mẫu và coverage\n",
        f"- PODEM DETECTED: **{detected}/18**; status khác được giữ nguyên trong bảng.",
        f"- {len(patterns)} pattern sau điền X=0; "
        f"{len(pattern_set)} vector nhị phân khác nhau: "
        + ", ".join("".join(map(str, bits)) for bits in unique_patterns) + ".",
        f"- `coverage(scan, bộ mẫu, 18 stem)`: **{cov['detected']}/{cov['total']} "
        f"= {cov['coverage']:.1f}%**.",
        f"- Coverage là hợp của **bộ mẫu**; một vector riêng lẻ phát hiện "
        f"tối đa {max_single}/18 lỗi.",
        "- Kết quả này là PODEM thật và simulator thật; bảng vét cạn độc lập "
        "vẫn lưu tại `results/seq_example_results.md`.",
    ])
    return "\n".join(lines) + "\n", {"detected": detected, "coverage": cov}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--md", type=Path, help="đường dẫn lưu Markdown")
    args = parser.parse_args()
    report, summary = run()
    if args.md:
        args.md.parent.mkdir(parents=True, exist_ok=True)
        args.md.write_text(report, encoding="utf-8")
        print(f"Da ghi {args.md}")
    else:
        print("Dung --md de luu bang day du bang UTF-8.")
    print(f"PODEM DETECTED {summary['detected']}/18; bo mau phu "
          f"{summary['coverage']['detected']}/{summary['coverage']['total']}")
    return 0 if summary["detected"] == summary["coverage"]["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
