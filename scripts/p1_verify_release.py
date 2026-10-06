"""Chạy lại kiểm chứng P1 và demo trên source hiện tại; lưu bằng chứng UTF-8.

Chạy từ gốc repo bằng Python >=3.10. Không sửa kết quả bàn giao gốc của P6.
"""
from pathlib import Path
import os
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))


def main():
    assert sys.version_info >= (3, 10), 'Cần Python >=3.10'
    os.chdir(ROOT)
    env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'), PYTHONIOENCODING='utf-8')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    evidence = [f'# Kiểm chứng P1 — 06/10/2026\n\nPython {platform.python_version()}; '
                f'base `{commit}` + thay đổi P1 trong working tree.\n']
    commands = [
        ['-m', 'pytest', '-q'],
        ['scripts/check_p1_examples.py'],
        ['notes/p2_kiem_chung.py'],
        ['notes/p3_kiem_tra_ban_giao.py'],
        ['scripts/p4_seq_experiment.py'],
        ['-m', 'atpg.run', 'circuits/c17.bench', '--fault', '11', '0', '--trace'],
        ['-m', 'atpg.run', 'circuits/backtrack_example.bench', '--fault', 't', '0', '--trace'],
        ['-m', 'atpg.run', 'circuits/c17.bench', '--all', '--md', 'results/p1_c17_collapsed.md'],
        ['-m', 'atpg.run', 'circuits/c17.bench', '--all', '--no-collapse', '--md', 'results/p1_c17_all.md'],
    ]
    commands += [['-m', 'atpg.run', 'circuits/seq_example.bench', '--unroll', str(k),
                  '--all', '--md', f'results/p1_seq_k{k}.md'] for k in (1, 2, 3)]
    for args in commands:
        result = subprocess.run([sys.executable, *args], env=env, capture_output=True, text=True, encoding='utf-8')
        evidence.append(f'\n## `python {" ".join(args)}`\n\nExit {result.returncode}\n\n```text\n{result.stdout}{result.stderr}```\n')
        (ROOT / 'results/p1_verification.md').write_text(''.join(evidence), encoding='utf-8')
        print(f'{"PASS" if result.returncode == 0 else "FAIL"}: {" ".join(args)}')
        if result.returncode:
            raise SystemExit(result.returncode)

    # Full scan through the real P4/P5/P6 API, compared to P4's independent oracle.
    from atpg.circuit import Circuit
    from atpg.faults import Fault
    from atpg.podem import podem
    from atpg.fault_sim import detects_cube
    from atpg.unroll import full_scan
    import p4_seq_experiment as reference
    base = Circuit.from_bench('circuits/seq_example.bench')
    scan = full_scan(base)
    rows = ['# Full scan qua API thật — 06/10/2026\n',
            f'Python {platform.python_version()}; base `{commit}` + P1.\n',
            'Tái lập: `python scripts/p1_verify_release.py`.\n',
            f'PI: {scan.inputs}; PO: {scan.outputs}. Q là pseudo-PI, D là pseudo-PO.\n',
            '| Lỗi stem | Pattern (thứ tự PI trên) | Trạng thái | Mọi cách điền X |\n|---|---|---|---|\n']
    from itertools import product
    for net in base.nets:
        for sv in (0, 1):
            fault = Fault(net, sv)
            result = podem(scan, fault)
            assert result.status == 'DETECTED', fault
            assert detects_cube(scan, result.pattern, fault) is True, fault
            # Check every completion against the separate binary model.
            for bits in product('01', repeat=len(scan.inputs)):
                pattern = dict(zip(scan.inputs, bits))
                if all(result.pattern[n] in ('X', b) for n, b in pattern.items()):
                    a, b, q = (int(pattern[n]) for n in ('A', 'B', 'Q'))
                    assert reference.one_cycle(a, b, q) != reference.one_cycle(a, b, q, (net, sv))
            rows.append(f'| {fault} | {"".join(result.pattern[n] for n in scan.inputs)} | {result.status} | Đạt |\n')
    rows.append('\nKết quả: 18/18 lỗi stem, PODEM thật + simulator P6 + oracle P4.\n')
    (ROOT / 'results/p1_full_scan.md').write_text(''.join(rows), encoding='utf-8')
    print('PASS: full scan 18/18, real API and independent oracle')


if __name__ == '__main__':
    main()
