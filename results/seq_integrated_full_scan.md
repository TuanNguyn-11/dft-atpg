# P4 — Full scan trên API tích hợp

- Commit mã nguồn lúc chạy: `553dfb69327f4cff10d3b5549b93acc86b3a6776`
- Python 3.12.0 (CPython); Windows 11
- Thời điểm chạy: 2026-10-06T19:44:46
- Lệnh từ gốc repo: `python scripts/p4_integrated_experiment.py --md results/seq_integrated_full_scan.md`
- Nguồn: `circuits/seq_example.bench`; `Circuit.from_bench`, `full_scan`, `podem`, `detects_cube`, `coverage`; oracle độc lập `scripts/p4_seq_experiment.py`.
- Mẫu số: 18 lỗi stem của `base.nets` × SA0/SA1; không dùng `all_faults(scan)` vì hàm đó còn sinh lỗi nhánh.
- Full scan: PI `[A,B,Q]`, PO `[Y,D]`. Shift in đặt `Q`, capture cập nhật FF từ `D`, shift out quan sát `D` qua pseudo-PO; mỗi vector logic còn cần thời gian dịch/capture vật lý.

| Lỗi stem | PODEM | Cube A,B,Q | Backtracks | Simulator: mọi X | Oracle P4: mọi X | Điền X=0 |
|---|---|---|---:|---|---|---|
| A/SA0 | DETECTED | 111 | 0 | OK | OK | 111 |
| A/SA1 | DETECTED | 011 | 0 | OK | OK | 011 |
| B/SA0 | DETECTED | 110 | 0 | OK | OK | 110 |
| B/SA1 | DETECTED | 100 | 0 | OK | OK | 100 |
| Q/SA0 | DETECTED | 101 | 0 | OK | OK | 101 |
| Q/SA1 | DETECTED | 100 | 0 | OK | OK | 100 |
| N1/SA0 | DETECTED | 111 | 0 | OK | OK | 111 |
| N1/SA1 | DETECTED | 110 | 1 | OK | OK | 110 |
| N2/SA0 | DETECTED | 100 | 1 | OK | OK | 100 |
| N2/SA1 | DETECTED | 110 | 1 | OK | OK | 110 |
| N4/SA0 | DETECTED | 110 | 0 | OK | OK | 110 |
| N4/SA1 | DETECTED | 100 | 0 | OK | OK | 100 |
| N3/SA0 | DETECTED | 1X1 | 0 | OK | OK | 101 |
| N3/SA1 | DETECTED | 110 | 2 | OK | OK | 110 |
| Y/SA0 | DETECTED | 110 | 0 | OK | OK | 110 |
| Y/SA1 | DETECTED | X00 | 0 | OK | OK | 000 |
| D/SA0 | DETECTED | 0XX | 0 | OK | OK | 000 |
| D/SA1 | DETECTED | 1X1 | 0 | OK | OK | 101 |

## Bộ mẫu và coverage

- PODEM DETECTED: **18/18**; status khác được giữ nguyên trong bảng.
- 18 pattern sau điền X=0; 6 vector nhị phân khác nhau: 111, 011, 110, 100, 101, 000.
- `coverage(scan, bộ mẫu, 18 stem)`: **18/18 = 100.0%**.
- Coverage là hợp của **bộ mẫu**; một vector riêng lẻ phát hiện tối đa 9/18 lỗi.
- Kết quả này là PODEM thật và simulator thật; bảng vét cạn độc lập vẫn lưu tại `results/seq_example_results.md`.
