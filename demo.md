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

Các lệnh bên dưới viết cho Windows và gọi thẳng `.\.venv\Scripts\python.exe` (pytest chỉ cài trong `.venv`, nên python hệ thống không có pytest). Trên Linux/macOS thay `.\.venv\Scripts\python.exe` bằng `python` sau khi `source .venv/bin/activate`. Mỗi cửa sổ PowerShell mới phải đặt lại `$env:PYTHONPATH` (riêng `pytest` đã có `tests/conftest.py` nên không cần).

## 1. Kiểm thử
```
.\.venv\Scripts\python.exe -m pytest -q
```
Mong đợi: toàn bộ test pass (dòng cuối dạng `N passed`).

## 2. Một lỗi có trace: 11/SA0 trên c17
```
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --fault 11 0 --trace
```
Mong đợi: dòng `11/SA0: DETECTED, pattern X10XX, backtrack 0 (PODEM)`, `Kiem chung bang fault simulation: OK`, trace PODEM 2 bước (P5), bảng trace trong đó net 11 có giá trị D và ít nhất một PO (22 hoặc 23) có D hoặc D'.

## 3. Kiểm tra một vector cho trước (vector chạy tay của P2/P3)
```
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --fault 11 0 --pattern X10XX --trace
```
Mong đợi: `Pattern X10XX PHAT HIEN 11/SA0`; trace: 11 = D, 16 = D', 22 = D, 23 = D (khi X điền 0).

## 4. Toàn bộ lỗi c17 + coverage
```
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --all --md results/c17_all_faults.md
```
Mong đợi: thuật toán `PODEM`; 34 lỗi trước gộp, 22 sau gộp; mọi lỗi DETECTED; coverage 100%; backtrack trung bình 0; nén 22 → 6 pattern; cột "Kiem chung" toàn OK; "Pattern bi kiem chung SAI = 0". Thêm `--no-collapse` để chạy cả 34 lỗi (34/34, nén còn 7 pattern).

## 5. Mạch tuần tự (cần `src/atpg/unroll.py` của P4)
```
.\.venv\Scripts\python.exe -m atpg.run circuits/seq_example.bench --unroll 2 --all
```
Mong đợi:
- Phạm vi: **18 lỗi stem vật lý** (9 net × 2), mỗi lỗi được sao sang cả 2 khung; **không gộp lỗi, không có lỗi nhánh**; mẫu số coverage = 18.
- Trạng thái đầu `Q@0` được coi là **chưa biết** (không scan/reset). `DETECTED` chỉ khi phát hiện **bảo đảm** với mọi trạng thái đầu: **13/18 = 72,2%** (khớp `results/seq_example_results.md` của P4 ở k = 2).
- 5 lỗi chỉ phát hiện **có điều kiện** `Q@0` (nhãn `CO DIEU KIEN Q@0`); nếu `Q@0` điều khiển được nhờ scan/reset thì coverage là 18/18.
- Số khung đổi kết quả: `--unroll 1` cho 1/18, `--unroll 3` cho 18/18 (bảo đảm).

Chế độ điều khiển được `Q@0`:
```
.\.venv\Scripts\python.exe -m atpg.run circuits/seq_example.bench --unroll 2 --init controllable --all
```
Kết quả có điều kiện, pattern gồm cả `Q@0`; không gọi là phát hiện bảo đảm từ trạng thái đầu chưa biết.

Chưa hỗ trợ: `--branch` kết hợp `--unroll` (`fault_in_frames` của P4 chỉ nhận lỗi stem).

> Nguồn pattern: PODEM của P5. Với mạch tuần tự, PODEM coi `Q@0` là PI hình thức nên có thể gán nó; pattern chỉ được tính `DETECTED` khi đã kiểm bảo đảm độc lập với `Q@0`. Nếu pattern PODEM phụ thuộc `Q@0`, công cụ tìm chuỗi bảo đảm bằng vét cạn trên các PI điều khiển được và ghi `vet can chuoi (tham chieu)` trong dòng thuật toán (ở k = 2: 3 chuỗi từ PODEM, 10 chuỗi từ vét cạn).
