# Demo P6 — chạy từng lệnh

Chạy từ thư mục gốc repo. Python ≥ 3.10; chỉ cần `pytest` cài thêm.

## 0. Chuẩn bị (một lần)
```
python -m venv .venv
# Windows (PowerShell):
.\.venv\Scripts\python.exe -m pip install pytest
$env:PYTHONPATH = (Join-Path (Get-Location) 'src')
# Linux/macOS:
source .venv/bin/activate && python -m pip install pytest && export PYTHONPATH="$PWD/src"
```

## 1. Kiểm thử
```
python -m pytest -q
```
Mong đợi: toàn bộ test pass (dòng cuối dạng `N passed`).

## 2. Một lỗi có trace: 11/SA0 trên c17
```
python -m atpg.run circuits/c17.bench --fault 11 0 --trace
```
Mong đợi: dòng `11/SA0: DETECTED ...`, `Kiem chung bang fault simulation: OK`, bảng trace trong đó net 11 có giá trị D và ít nhất một PO (22 hoặc 23) có D hoặc D'.

## 3. Kiểm tra một vector cho trước (vector chạy tay của P2/P3)
```
python -m atpg.run circuits/c17.bench --fault 11 0 --pattern X10XX --trace
```
Mong đợi: `Pattern X10XX PHAT HIEN 11/SA0`; trace: 11 = D, 16 = D', 22 = D, 23 = D (khi X điền 0).

## 4. Toàn bộ lỗi c17 + coverage
```
python -m atpg.run circuits/c17.bench --all --md results/c17_all_faults.md
```
Mong đợi: 34 lỗi trước gộp, 22 sau gộp; mọi lỗi DETECTED; coverage 100%; cột "Kiem chung" toàn OK; "Pattern bi kiem chung SAI = 0".

## 5. Mạch tuần tự (cần unroll.py của P4)
```
python -m atpg.run circuits/seq_example.bench --unroll 2 --all
```
Mong đợi: bảng lỗi tương tự, các lỗi được cấy vào cả 2 khung thời gian.

> Khi `src/atpg/podem.py` của P5 có mặt, cột thuật toán đổi từ "vet can (tham chieu)" thành "PODEM" và cột Backtrack có số thật.
