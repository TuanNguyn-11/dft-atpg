"""Kiểm thử CLI xuất trace trên snapshot có Circuit/bench thật."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "export_podem_trace.py"
C17 = ROOT / "circuits" / "c17.bench"
AUX = ROOT / "circuits" / "backtrack_example.bench"
pytestmark = pytest.mark.skipif(
    not (C17.is_file() and AUX.is_file()),
    reason="cần netlist thật từ snapshot tích hợp Circuit của P6",
)


def _export(bench: Path, fault_net: str, stuck_at: int, output: Path, *extra: str):
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--bench", str(bench),
            "--fault", fault_net, str(stuck_at),
            "--output", str(output),
            *extra,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def test_c17_trace_export_is_repeatable_and_has_seven_columns(tmp_path: Path):
    first_path = tmp_path / "c17-first.md"
    repeat_path = tmp_path / "c17-repeat.md"
    first = _export(C17, "11", 0, first_path)
    repeat = _export(C17, "11", 0, repeat_path)

    assert first.returncode == repeat.returncode == 0
    assert first_path.read_bytes() == repeat_path.read_bytes()
    content = first_path.read_text(encoding="utf-8")
    assert "Status: `DETECTED`" in content
    assert "Pattern: `X10XX`" in content
    assert "Backtracks: `0`" in content
    assert "| 1 | (11,1) | (3,0) | 3=0 |" in content
    assert "PI=(X,1,0,X,X); 10=1, 11=D, 16=D', 19=X, 22=D, 23=X" in content
    header = next(line for line in content.splitlines() if line.startswith("| Bước |"))
    assert header.count("|") == 8


def test_backtrack_trace_matches_p3_action_convention(tmp_path: Path):
    output = tmp_path / "backtrack.md"
    completed = _export(AUX, "t", 0, output)

    assert completed.returncode == 0
    content = output.read_text(encoding="utf-8")
    assert "Status: `DETECTED`" in content
    assert "Pattern: `01`" in content
    assert "Backtracks: `1`" in content
    assert "| 1 | (t,1) | (a,1) | a=1 | PI=(1,X); t=D, n=0, out=0 | ∅ | backtrack |" in content
    assert "| 2 | — | — | a=0 | PI=(0,X); t=X, n=1, out=X | ∅ | tiếp tục |" in content
    assert "| 3 | (t,1) | (b,1) | b=1 | PI=(0,1); t=D, n=1, out=D | ∅ | thành công |" in content


def test_backtrack_limit_exports_aborted_separately(tmp_path: Path):
    output = tmp_path / "backtrack-aborted.md"
    completed = _export(AUX, "t", 0, output, "--max-backtracks", "0")

    assert completed.returncode == 0
    content = output.read_text(encoding="utf-8")
    assert "Status: `ABORTED`" in content
    assert "đạt giới hạn `max_backtracks`" in content
    assert "Status: `UNTESTABLE`" not in content
    assert content.count("| backtrack |") == 1


def test_export_rejects_invalid_stuck_value(tmp_path: Path):
    completed = _export(C17, "11", 2, tmp_path / "invalid.md")

    assert completed.returncode == 2
    assert "SV phải là 0 hoặc 1" in completed.stderr


def test_export_reports_output_write_error(tmp_path: Path):
    output = tmp_path / "missing-directory" / "trace.md"
    completed = _export(C17, "11", 0, output)

    assert completed.returncode == 2
    assert "Lỗi xuất trace PODEM" in completed.stderr
    assert "trace.md" in completed.stderr
