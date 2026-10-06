# Demo P6 — chạy từng lệnh

Chạy từ **thư mục gốc repo**. Cần Python **≥ 3.10** và `pytest`. Mọi lệnh dưới đây dùng **cùng một interpreter** trong `.venv`.

## 0. Chuẩn bị (một lần, PowerShell)
```
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install pytest
```
Chỉ tiếp tục nếu `python --version` ≥ 3.10; nếu không, gọi đúng file python.exe ≥ 3.10 khi tạo `.venv`.

**Mỗi cửa sổ PowerShell mới** phải đặt lại hai biến:
```
$env:PYTHONPATH = (Join-Path (Get-Location) 'src')
$env:PYTHONIOENCODING = 'utf-8'
```
Bash (Linux/macOS): `source .venv/bin/activate`, `export PYTHONPATH="$PWD/src"`, rồi thay `.\.venv\Scripts\python.exe` bằng `python`.

Muốn lưu kết quả thì dùng `--md FILE` (ghi UTF-8), **không** chuyển hướng `>` stdout vì trace PODEM có tiếng Việt và console cũ có thể không ghi được.

## 1. Kiểm thử
```
.\.venv\Scripts\python.exe -m pytest -q
```
Mong đợi: dòng cuối `... passed` (không có `failed`). Nhóm test tích hợp `tests/test_integration.py` chạy PODEM thật của P5 (đã có trong repo) và đếm số lần gọi PODEM; nếu thiếu `podem.py` các test đó bị skip thay vì pass giả. Mốc 06/10/2026: `350 passed`.

## 2. Trace lỗi mẫu 11/SA0 trên c17
```
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --fault 11 0 --trace
```
Các dòng mong đợi:
```
Mach c17: 5 PI, 2 PO, 6 cong, 0 DFF
11/SA0: DETECTED, pattern X10XX, backtrack 0 (PODEM)
Kiem chung bang fault simulation: OK; moi cach dien X deu phat hien: co
Phat hien tai PO: 22, 23
```
Kèm bảng mô phỏng (net 11 = D, 16 = D', 22 = D, 23 = D) và bảng trace PODEM 7 cột, 2 bước: `(11,1)` → `3=0`, rồi `(2,1)` → `2=1`, hành động cuối `thành công`.

## 3. Kiểm tra vector chạy tay của P2/P3
```
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --fault 11 0 --pattern X10XX
```
Dòng mong đợi: `Pattern X10XX 11/SA0: PHAT HIEN voi moi cach dien X`

## 4. Ví dụ có backtrack (mạch phụ của P3)
```
.\.venv\Scripts\python.exe -m atpg.run circuits/backtrack_example.bench --fault t 0 --trace
```
Dòng mong đợi: `t/SA0: DETECTED, pattern 01, backtrack 1 (PODEM)`; bảng trace có 3 hàng với hành động `tiếp tục`, `backtrack`, `thành công`.

## 5. Toàn bộ lỗi c17 + coverage
```
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --all --md results/c17_all_faults.md
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --all --no-collapse --md results/c17_all_faults_uncollapsed.md
```
Dòng mong đợi (lệnh đầu, 22 lỗi đại diện sau gộp):
```
| Fault coverage (DETECTED / tong) | 22/22 = 100.0% |
| Backtrack trung binh | 0.00 |
| Pattern sau nen | 6 (phu 22/22 loi dang chay) |
| Tap sau nen phu toan bo loi goc (34 loi) | 34/34 = 100.0% |
| Pattern bi kiem chung SAI | 0 |
```
Lệnh thứ hai (34 lỗi gốc): `34/34 = 100.0%`, `Pattern sau nen | 7`. Cột `Thuat toan` ghi `PODEM` ở mọi hàng. File `.md` có phần "Moi truong va tai lap" (lệnh, Python, commit, thứ tự PI) và danh sách pattern sau nén.

## 6. Mạch tuần tự (trạng thái đầu chưa biết)
```
.\.venv\Scripts\python.exe -m atpg.run circuits/seq_example.bench --unroll 2 --all
```
Dòng mong đợi:
```
Mach seq_example_unroll_2: 5 PI, 2 PO, 13 cong, 0 DFF
| Phat hien BAO DAM (DETECTED / tong) | 13/18 = 72.2% |
| Chi phat hien CO DIEU KIEN Q@0 | 5 |
| Coverage neu Q@0 dieu khien duoc (scan/reset): (DETECTED + co dieu kien) / tong | 18/18 = 100.0% |
```
- Phạm vi: 18 lỗi stem vật lý, cấy vào mọi khung; không gộp, không lỗi nhánh.
- `DETECTED` chỉ khi phát hiện **bảo đảm** với mọi trạng thái đầu. Cột `Thuat toan` theo từng hàng: `PODEM`, hoặc `vet can chuoi (tham chieu)` khi pattern PODEM phụ thuộc `Q@0` (k = 2: 3 chuỗi từ PODEM, 10 từ vét cạn).
- `--unroll 1` cho 1/18, `--unroll 3` cho 18/18 (khớp P4). Lưu kết quả: thêm `--md results/seq_example_p6_k2.md`.
- `--init controllable` cho 18/18 ở k = 2 nhưng là kết quả có điều kiện `Q@0`, **không** tương đương full scan (full scan của P4: 18/18).

## 7. Đầu vào sai bị từ chối
```
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --fault 11 2
```
Dòng mong đợi (mã thoát 2, không in coverage): `atpg.run: error: SV phai la 0 hoac 1 (stuck-at-0/stuck-at-1), nhan '2'`
