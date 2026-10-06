"""P6-01: dau vao sai phai bi tu choi, khong duoc thanh DETECTED/UNTESTABLE hay fallback vet can."""
import os

import pytest

from atpg import run
from atpg.circuit import Circuit
from atpg.fault_sim import detects, simulate, simulate_parallel
from atpg.faults import Fault, validate_fault

ROOT = os.path.dirname(os.path.dirname(__file__))
C17 = os.path.join(ROOT, "circuits", "c17.bench")
SEQ = os.path.join(ROOT, "circuits", "seq_example.bench")


def c17():
    return Circuit.from_bench(C17)


def cli_error(capsys, argv):
    """Chay CLI, ky vong thoat ma khac 0, co thong bao, khong in coverage."""
    with pytest.raises(SystemExit) as e:
        run.main(argv)
    out, err = capsys.readouterr()
    assert e.value.code not in (0, None)
    assert "coverage" not in out.lower() and "DETECTED" not in out and "UNTESTABLE" not in out
    return err


# ---------------- API ----------------
@pytest.mark.parametrize("sv", [2, -1, "0", None, True])
def test_fault_rejects_invalid_stuck_value(sv):
    with pytest.raises(ValueError, match="stuck_at"):
        Fault("11", sv)


def test_validate_fault_rejects_missing_net_and_branch():
    c = c17()
    with pytest.raises(ValueError, match="khong co trong mach"):
        validate_fault(c, Fault("99", 0))
    with pytest.raises(ValueError, match="khong co cong"):
        validate_fault(c, Fault("11", 0, "999"))
    with pytest.raises(ValueError, match="khong nhan net"):
        validate_fault(c, Fault("11", 0, "10"))          # cong 10 = NAND(1,3) khong nhan 11
    with pytest.raises(ValueError, match="rong"):
        validate_fault(c, [])
    assert validate_fault(c, Fault("11", 0, "16"))         # nhanh that: 11 vao cong 16


def test_simulator_does_not_silently_ignore_unknown_fault():
    c = c17()
    p = dict(zip(c.inputs, "01000"))
    for bad in (Fault("99", 0), Fault("11", 0, "999"), Fault("11", 0, "10")):
        with pytest.raises(ValueError):
            simulate(c, p, bad)
        with pytest.raises(ValueError):
            detects(c, p, bad)
        with pytest.raises(ValueError):
            simulate_parallel(c, [p], bad)


def test_generate_test_rejects_bad_input_before_any_algorithm():
    c = c17()
    called = []

    def spy(*a, **k):
        called.append(1)
        raise AssertionError("khong duoc goi PODEM voi dau vao sai")

    with pytest.raises(ValueError):
        run.generate_test(c, Fault("11", 0, "999"), spy)
    with pytest.raises(ValueError):
        run.generate_test(c, Fault("99", 1), None)          # ca duong vet can tham chieu
    with pytest.raises(ValueError):
        run.generate_test(c, Fault("11", 0), None, max_backtracks=-1)
    assert not called


# ---------------- CLI ----------------
def test_cli_rejects_stuck_value_2(capsys):
    assert "SV phai la 0 hoac 1" in cli_error(capsys, [C17, "--fault", "11", "2"])


def test_cli_rejects_nonexistent_branch(capsys):
    assert "khong ton tai" in cli_error(capsys, [C17, "--fault", "11", "0", "--branch", "999"])
    assert "khong nhan net 11" in cli_error(capsys, [C17, "--fault", "11", "0", "--branch", "10"])


def test_cli_rejects_unknown_net(capsys):
    assert "Khong co net" in cli_error(capsys, [C17, "--fault", "99", "0"])


@pytest.mark.parametrize("argv, msg", [
    ([SEQ, "--unroll", "0", "--all"], "So khung K phai >= 1"),
    ([SEQ, "--unroll", "-2", "--all"], "So khung K phai >= 1"),
    ([C17, "--all", "--max-backtracks", "-1"], "--max-backtracks phai >= 0"),
    ([C17, "--all", "--max-x", "-1"], "--max-x phai >= 0"),
    ([SEQ, "--all"], "can --unroll"),                       # mach co DFF ma khong trai khung
    ([C17, "--branch", "16", "--all"], "--branch can di kem --fault"),
])
def test_cli_rejects_bad_limits(capsys, argv, msg):
    assert msg in cli_error(capsys, argv)


def test_valid_demo_commands_still_work(capsys):
    assert run.main([C17, "--fault", "11", "0", "--trace"]) == 0
    assert run.main([C17, "--fault", "11", "0", "--branch", "16"]) == 0
    assert run.main([C17, "--all"]) == 0
    assert run.main([SEQ, "--unroll", "2", "--all"]) == 0
    capsys.readouterr()

# ---------------- loi PODEM (P5) goi truc tiep ----------------
@pytest.mark.parametrize("bad, msg", [
    (Fault("11", 0, "999"), "999"),       # nhanh toi cong khong ton tai
    (Fault("11", 0, "22"), "22"),         # cong 22 khong nhan net 11
    (Fault("99", 0), "99"),               # net khong ton tai (truoc day KeyError)
])
def test_podem_core_rejects_fault_not_in_circuit(bad, msg):
    from atpg.podem import podem
    with pytest.raises(ValueError, match=msg):
        podem(c17(), bad)


def test_podem_core_rejects_bad_fault_frame_in_list():
    from atpg.podem import podem
    with pytest.raises(ValueError):
        podem(c17(), [Fault("11", 0), Fault("11", 0, "999")])


@pytest.mark.parametrize("limit", [-1, 1.5, True])
def test_podem_core_rejects_bad_backtrack_limit(limit):
    from atpg.podem import podem
    with pytest.raises(ValueError, match="max_backtracks"):
        podem(c17(), Fault("11", 0), max_backtracks=limit)


def test_podem_core_valid_input_unchanged():
    from atpg.podem import podem
    r = podem(c17(), Fault("11", 0))
    assert (r.status, "".join(r.pattern[i] for i in c17().inputs), r.backtracks) == ("DETECTED", "X10XX", 0)
    assert podem(c17(), Fault("11", 0, "16")).status == "DETECTED"
