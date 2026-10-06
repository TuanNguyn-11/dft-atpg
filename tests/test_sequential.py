"""Kiem thu che do tran khung (--unroll): demo, pham vi loi, trang thai dau Q@0 chua biet - P6."""
import importlib.util
import os
from argparse import Namespace

import pytest

from atpg import run
from atpg.circuit import Circuit
from atpg.faults import Fault

ROOT = os.path.dirname(os.path.dirname(__file__))


@pytest.fixture(autouse=True)
def reference_only(monkeypatch):
    """Cac test o day khoa so lieu tham chieu (vet can), khong phu thuoc podem.py cua P5."""
    monkeypatch.setattr(run, "_load_podem", lambda: None)


SEQ = os.path.join(ROOT, "circuits", "seq_example.bench")


def test_demo_command_runs(capsys):
    """Dung nguyen lenh trong demo.md."""
    assert run.main([SEQ, "--unroll", "2", "--all"]) == 0
    out = capsys.readouterr().out
    assert "18 loi stem vat ly" in out and "khong co loi nhanh" in out
    assert "13/18 = 72.2%" in out                 # phat hien bao dam, khop P4 voi k = 2
    assert "18/18 = 100.0%" in out                # chi khi Q@0 dieu khien duoc


def test_demo_command_with_no_collapse(capsys):
    assert run.main([SEQ, "--unroll", "2", "--all", "--no-collapse"]) == 0
    out = capsys.readouterr().out
    assert "luon khong gop loi" in out and "13/18 = 72.2%" in out


@pytest.mark.parametrize("k, expected", [(1, "1/18 = 5.6%"), (2, "13/18 = 72.2%"), (3, "18/18 = 100.0%")])
def test_guaranteed_coverage_by_frames_matches_p4(k, expected, capsys):
    """results/seq_example_results.md cua P4: k=1: 1/18, k=2: 13/18, k=3: 18/18."""
    assert run.main([SEQ, "--unroll", str(k), "--all"]) == 0
    assert expected in capsys.readouterr().out


def test_matches_p4_script_fault_by_fault():
    path = os.path.join(ROOT, "scripts", "p4_seq_experiment.py")
    if not os.path.exists(path):
        pytest.skip("khong co scripts/p4_seq_experiment.py")
    spec = importlib.util.spec_from_file_location("p4_seq", path)
    p4 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p4)
    from atpg.unroll import fault_in_frames, unroll
    base = Circuit.from_bench(SEQ)
    c = unroll(base, 2)
    states = [f"{g.output}@0" for g in base.dffs]
    args = Namespace(max_backtracks=1000, trace=False, max_x=16)
    for net in base.nets:
        for sv in (0, 1):
            _, kind = run.seq_generate(c, tuple(fault_in_frames(Fault(net, sv), 2)), None, states, args)
            assert (kind == "bao dam") == (p4.first_sequence((net, sv), max_frames=2) is not None), (net, sv)


def test_branch_with_unroll_is_rejected():
    with pytest.raises(SystemExit) as e:
        run.main([SEQ, "--unroll", "2", "--fault", "D", "0", "--branch", "Q"])
    assert "chua ho tro" in str(e.value)


def test_init_requires_unroll():
    with pytest.raises(SystemExit):
        run.main([SEQ, "--init", "controllable", "--all"])


def test_controllable_mode_is_labelled_conditional(capsys):
    assert run.main([SEQ, "--unroll", "2", "--init", "controllable", "--all"]) == 0
    out = capsys.readouterr().out
    assert "CHE DO Q@0 DIEU KHIEN DUOC" in out and "CO DIEU KIEN" in out
    assert "18/18 = 100.0%" in out


# ---- vi du phan chung: trang thai dau khong the tu dat ----
def bench_and_dff(tmp_path):
    f = tmp_path / "andq.bench"
    f.write_text("INPUT(A)\nQ = DFF(A)\nY = AND(Q, A)\nOUTPUT(Y)\n")
    return str(f)


def test_state_dependent_pattern_is_not_reported_as_guaranteed(tmp_path, capsys):
    path = bench_and_dff(tmp_path)
    # 1 khung: Y/SA0 chi phat hien khi Q@0 = 1 -> chi co dieu kien
    assert run.main([path, "--unroll", "1", "--fault", "Y", "0"]) == 0
    out = capsys.readouterr().out
    assert "Y/SA0: CO DIEU KIEN Q@0" in out and "Q@0=1" in out
    assert "KHONG bao dam" in out and "Y/SA0: DETECTED" not in out
    # kiem tra truc tiep pattern A@0=1, Q@0=1 (thu tu INPUT: A@0 roi Q@0)
    assert run.main([path, "--unroll", "1", "--fault", "Y", "0", "--pattern", "11"]) == 0
    out = capsys.readouterr().out
    assert "(bo qua Q@0 trong pattern): khong" in out
    assert "(Q@0 dung nhu trong pattern, X dien moi cach): co" in out


def test_two_frames_make_it_guaranteed(tmp_path, capsys):
    path = bench_and_dff(tmp_path)
    assert run.main([path, "--unroll", "2", "--fault", "Y", "0"]) == 0
    out = capsys.readouterr().out
    assert "Y/SA0: DETECTED" in out and "BAO DAM voi moi trang thai dau" in out


def test_all_mode_counts_conditional_separately(tmp_path, capsys):
    path = bench_and_dff(tmp_path)
    assert run.main([path, "--unroll", "1", "--all"]) == 0
    out = capsys.readouterr().out
    assert "| Phat hien BAO DAM (DETECTED / tong) | 1/6 = 16.7% |" in out
    assert "| Chi phat hien CO DIEU KIEN Q@0 | 5 |" in out
