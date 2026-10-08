# So sánh D-algorithm và PODEM — c17, toàn bộ lỗi

## Môi trường và tái lập

- Lệnh tái tạo (từ gốc repo, PYTHONPATH=src): `python -m atpg.compare circuits/c17.bench --all --md results/so_sanh_c17_all.md --csv results/so_sanh_c17_all.csv`
- Python 3.14.8, Windows 10
- Commit mã nguồn: 212cea3
- Thời điểm chạy: 2026-10-08T11:55:20
- Thứ tự PI: 1, 2, 3, 6, 7; D-algorithm thử cube theo thứ tự `last`, D-frontier ưu tiên cổng gần PO nhất
- Thời gian: trung vị 20 lần chạy (time.perf_counter), phụ thuộc máy
- Phạm vi: 22 lỗi đại diện sau gộp tương đương (từ 34 lỗi gốc)
- Tổng thời gian chạy cả hai thuật toán và kiểm chứng: 0.357 s

## Tổng hợp

| Tiêu chí | D-algorithm | PODEM |
|---|---|---|
| Phát hiện (DETECTED / tổng) | 22/22 | 22/22 |
| Tổng số quyết định | 67 | 64 |
| Quyết định trung bình mỗi lỗi | 3.05 | 2.91 |
| Tổng số lần quay lui | 2 | 0 |
| Tổng net nội bộ gán trực tiếp | 72 | 0 |
| Số bit X trung bình mỗi cube | 2.27 | 2.09 |
| Pattern đúng (X=0 và mọi cách điền X) | 22/22 | 22/22 |
| Pattern trước → sau nén | 22 → 7 (phủ 34/34 lỗi gốc) | 22 → 6 (phủ 34/34 lỗi gốc) |
| Tổng số lần implication | 67 | 128 |

Số lỗi hai thuật toán cho cube khác nhau: 15/22 (khác cube vẫn có thể cùng đúng; cột kiểm chứng cho biết đúng hay sai).

## Từng lỗi

| Lỗi | D-alg: trạng thái | D-alg: cube | D-alg: quyết định | D-alg: quay lui | D-alg: kiểm chứng | PODEM: trạng thái | PODEM: cube | PODEM: quyết định | PODEM: quay lui | PODEM: kiểm chứng |
|---|---|---|---|---|---|---|---|---|---|---|
| 1/SA1 | DETECTED | 0X11X | 4 | 0 | OK | DETECTED | 001XX | 3 | 0 | OK |
| 2/SA1 | DETECTED | X00XX | 4 | 0 | OK | DETECTED | X00XX | 2 | 0 | OK |
| 3/SA0 | DETECTED | 101XX | 5 | 1 | OK | DETECTED | 11111 | 5 | 0 | OK |
| 3/SA1 | DETECTED | 100XX | 5 | 1 | OK | DETECTED | 11011 | 5 | 0 | OK |
| 3->10/SA1 | DETECTED | 100XX | 3 | 0 | OK | DETECTED | 100XX | 3 | 0 | OK |
| 3->11/SA1 | DETECTED | X101X | 3 | 0 | OK | DETECTED | X101X | 3 | 0 | OK |
| 6/SA1 | DETECTED | 0110X | 4 | 0 | OK | DETECTED | X1101 | 4 | 0 | OK |
| 7/SA1 | DETECTED | X0X00 | 4 | 0 | OK | DETECTED | X00X0 | 3 | 0 | OK |
| 10/SA1 | DETECTED | 1X11X | 3 | 0 | OK | DETECTED | 101XX | 3 | 0 | OK |
| 11/SA0 | DETECTED | X100X | 4 | 0 | OK | DETECTED | X10XX | 2 | 0 | OK |
| 11/SA1 | DETECTED | 0111X | 3 | 0 | OK | DETECTED | X1111 | 4 | 0 | OK |
| 11->16/SA1 | DETECTED | X111X | 2 | 0 | OK | DETECTED | X111X | 3 | 0 | OK |
| 11->19/SA1 | DETECTED | XX111 | 2 | 0 | OK | DETECTED | XX111 | 3 | 0 | OK |
| 16/SA0 | DETECTED | XX11X | 1 | 0 | OK | DETECTED | 00XXX | 2 | 0 | OK |
| 16/SA1 | DETECTED | X10XX | 3 | 0 | OK | DETECTED | X10XX | 2 | 0 | OK |
| 16->22/SA1 | DETECTED | X10XX | 3 | 0 | OK | DETECTED | X10XX | 2 | 0 | OK |
| 16->23/SA1 | DETECTED | X1X00 | 3 | 0 | OK | DETECTED | X10X0 | 3 | 0 | OK |
| 19/SA1 | DETECTED | X0X01 | 3 | 0 | OK | DETECTED | X00X1 | 3 | 0 | OK |
| 22/SA0 | DETECTED | X1X0X | 2 | 0 | OK | DETECTED | 1X1XX | 2 | 0 | OK |
| 22/SA1 | DETECTED | X00XX | 2 | 0 | OK | DETECTED | 00XXX | 2 | 0 | OK |
| 23/SA0 | DETECTED | XXX01 | 2 | 0 | OK | DETECTED | X10XX | 2 | 0 | OK |
| 23/SA1 | DETECTED | XX11X | 2 | 0 | OK | DETECTED | X011X | 3 | 0 | OK |
