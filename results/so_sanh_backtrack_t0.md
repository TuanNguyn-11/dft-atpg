# So sánh D-algorithm và PODEM — backtrack_example, lỗi t/SA0

## Môi trường và tái lập

- Lệnh tái tạo (từ gốc repo, PYTHONPATH=src): `python -m atpg.compare circuits/backtrack_example.bench --fault t 0 --trace --md results/so_sanh_backtrack_t0.md --csv results/so_sanh_backtrack_t0.csv`
- Python 3.14.8, Windows 10
- Commit mã nguồn: 212cea3
- Thời điểm chạy: 2026-10-08T11:52:19
- Thứ tự PI: a, b; D-algorithm thử cube theo thứ tự `last`, D-frontier ưu tiên cổng gần PO nhất
- Thời gian: trung vị 200 lần chạy (time.perf_counter), phụ thuộc máy

## Bảng tiêu chí

| Nhóm | Tiêu chí | D-algorithm | PODEM | Ý nghĩa |
|---|---|---|---|---|
| A. Kết quả | Trạng thái | DETECTED | DETECTED | DETECTED = tìm được pattern |
| A. Kết quả | Test cube (thứ tự PI a, b) | 01 | 01 | X = đầu vào tùy ý |
| A. Kết quả | Số bit X trong cube | 0 | 0 | nhiều X hơn thì cube linh hoạt hơn, dễ nén tập test |
| A. Kết quả | Kiểm chứng bằng fault simulation (X điền 0) | OK | OK | mô phỏng độc lập mạch tốt và mạch lỗi |
| A. Kết quả | Đúng với mọi cách điền X | có | có | vét cạn mọi cách điền X |
| A. Kết quả | PO quan sát được lỗi (X điền 0) | out | out | đầu ra có D/D' |
| B. Quá trình tìm kiếm | Nơi ra quyết định | net nội bộ (cube của từng cổng) | chỉ ở PI | khác biệt cốt lõi giữa hai thuật toán |
| B. Quá trình tìm kiếm | Số quyết định (kể cả lần chọn thất bại) | 2 | 2 | D-alg: chọn PDCF/PDC/cover; PODEM: gán PI qua backtrace |
| B. Quá trình tìm kiếm | Net nội bộ được gán trực tiếp | 3 (t, n, out) | 0 | PODEM chỉ gán PI, net nội bộ suy ra bằng mô phỏng |
| B. Quá trình tìm kiếm | PI được chọn trực tiếp | - | a, b |  |
| B. Quá trình tìm kiếm | Số lần justify (J-frontier) | 0 | 0 (không cần) | PODEM không có bước justify riêng |
| B. Quá trình tìm kiếm | Số lần quay lui (backtrack) | 0 | 1 | phụ thuộc thứ tự thử, không phải thước đo tuyệt đối |
| B. Quá trình tìm kiếm | Nếu đổi thứ tự thử cube của D-algorithm | order=first: DETECTED, 01, 3 quyết định, 1 quay lui | - | cùng thuật toán, chỉ đổi thứ tự thử |
| C. Chi phí tính toán | Số lần gọi implication | 2 | 6 | D-alg: implication tiến + lùi; PODEM: mô phỏng tiến |
| C. Chi phí tính toán | Số lần đánh giá cổng | 9 | 18 | đếm trong code của từng thuật toán; chỉ so sánh tương đối |
| C. Chi phí tính toán | Thời gian (trung vị, ms) | 0.288 | 0.131 | phụ thuộc máy chạy |
| D. Đối chiếu | Khớp chạy tay | không có chạy tay để đối chiếu | khớp (results/golden_trace_backtrack.md (P3): 01, 2 quyết định, 1 quay lui) |  |

## Trace D-algorithm

| Bước | Loại | Cổng | Cube | Net đã biết sau implication | D-frontier | J-frontier | Hành động |
|---|---|---|---|---|---|---|---|
| 1 | PDCF | t | (a=X, b=1) -> t=D | b=1, t=D | {out} | {} | kích hoạt |
| 2 | PDC | out | PDC qua out: n=1 | a=0, b=1, t=D, n=1, out=D | {} | {} | thành công |

## Trace PODEM (P5)

| Bước | Objective (net, giá trị) | Backtrace → PI | Gán PI | Giá trị các net sau imply | D-frontier | Hành động |
|---|---|---|---|---|---|---|
| 1 | ('t', 1) | ('a', 1) | a=1 | {'a': '1', 'b': 'X', 't': 'D', 'n': '0', 'out': '0'} | [] | tiếp tục |
| 2 | None | None | a=0 | {'a': '0', 'b': 'X', 't': 'X', 'n': '1', 'out': 'X'} | [] | backtrack |
| 3 | ('t', 1) | ('b', 1) | b=1 | {'a': '0', 'b': '1', 't': 'D', 'n': '1', 'out': 'D'} | [] | thành công |

