"""Hồi quy P4 trên parser, PODEM và fault simulator thật (không tắt PODEM)."""

from argparse import Namespace
from itertools import product
from pathlib import Path
import sys

from atpg.circuit import Circuit
from atpg.fault_sim import coverage, detects_cube, detects_unknown_state
from atpg.faults import Fault
from atpg.podem import podem
from atpg.run import seq_generate
from atpg.unroll import fault_in_frames, full_scan, unroll

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import p4_seq_experiment as reference


def test_full_scan_podem_detects_all_18_physical_stems():
    base = Circuit.from_bench(str(ROOT / "circuits" / "seq_example.bench"))
    scan = full_scan(base)
    assert scan.inputs == ["A", "B", "Q"] and scan.outputs == ["Y", "D"]
    faults = [Fault(net, sv) for net in base.nets for sv in (0, 1)]
    assert len(faults) == 18 and all(f.branch_to is None for f in faults)
    patterns = []
    for fault in faults:
        result = podem(scan, fault)
        assert result.status == "DETECTED", (fault, result.status)
        cube = {net: result.pattern.get(net, "X") for net in scan.inputs}
        assert detects_cube(scan, cube, fault) is True, fault
        for bits in product("01", repeat=3):
            values = dict(zip(scan.inputs, bits))
            if any(cube[net] not in ("X", values[net]) for net in scan.inputs):
                continue
            a, b, q = (int(values[net]) for net in ("A", "B", "Q"))
            assert reference.one_cycle(a, b, q) != reference.one_cycle(
                a, b, q, (fault.net, fault.stuck_at)
            )
        patterns.append({net: 0 if cube[net] == "X" else int(cube[net]) for net in scan.inputs})
    assert coverage(scan, patterns, faults)["detected"] == 18


def test_two_frames_real_podem_and_simulator_preserve_unknown_initial_q():
    base = Circuit.from_bench(str(ROOT / "circuits" / "seq_example.bench"))
    expanded = unroll(base, 2)
    fault = Fault("N3", 0)
    frames = tuple(fault_in_frames(fault, 2))
    assert [f.net for f in frames] == ["N3@0", "N3@1"]
    raw = podem(expanded, list(frames))
    assert raw.status == "DETECTED"
    assert detects_cube(expanded, raw.pattern, frames) is True

    args = Namespace(max_backtracks=1000, trace=False, max_x=16)
    result, kind = seq_generate(expanded, frames, podem, ["Q@0"], args)
    assert result.status == "DETECTED" and kind == "bao dam"
    assert detects_unknown_state(expanded, result.pattern, frames, ["Q@0"]) is True
    known_sequence = {"A@0": 1, "B@0": 0, "A@1": 1, "B@1": 0}
    assert detects_unknown_state(expanded, known_sequence, frames, ["Q@0"]) is True
    assert reference.detects_without_scan(((1, 0), (1, 0)), ("N3", 0))
