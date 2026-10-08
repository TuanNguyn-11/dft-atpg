# So sánh D-algorithm và PODEM — c17, lỗi 11/SA0

## Môi trường và tái lập

- Lệnh tái tạo (từ gốc repo, PYTHONPATH=src): `python -m atpg.compare circuits/c17.bench --fault 11 0 --trace --md results/so_sanh_c17_11sa0.md --csv results/so_sanh_c17_11sa0.csv --tex report/figures/p6/so_sanh_c17_11sa0.tex`
- Python 3.14.8, Windows 10
- Commit mã nguồn: 212cea3
- Thời điểm chạy: 2026-10-08T11:53:47
- Thứ tự PI: 1, 2, 3, 6, 7; D-algorithm thử cube theo thứ tự `last`, D-frontier ưu tiên cổng gần PO nhất
- Thời gian: trung vị 200 lần chạy (time.perf_counter), phụ thuộc máy

## Bảng tiêu chí

| Nhóm | Tiêu chí | D-algorithm | PODEM | Ý nghĩa |
|---|---|---|---|---|
| A. Kết quả | Trạng thái | DETECTED | DETECTED | DETECTED = tìm được pattern |
| A. Kết quả | Test cube (thứ tự PI 1, 2, 3, 6, 7) | X100X | X10XX | X = đầu vào tùy ý |
| A. Kết quả | Số bit X trong cube | 2 | 3 | nhiều X hơn thì cube linh hoạt hơn, dễ nén tập test |
| A. Kết quả | Kiểm chứng bằng fault simulation (X điền 0) | OK | OK | mô phỏng độc lập mạch tốt và mạch lỗi |
| A. Kết quả | Đúng với mọi cách điền X | có | có | vét cạn mọi cách điền X |
| A. Kết quả | PO quan sát được lỗi (X điền 0) | 22, 23 | 22, 23 | đầu ra có D/D' |
| B. Quá trình tìm kiếm | Nơi ra quyết định | net nội bộ (cube của từng cổng) | chỉ ở PI | khác biệt cốt lõi giữa hai thuật toán |
| B. Quá trình tìm kiếm | Số quyết định (kể cả lần chọn thất bại) | 4 | 2 | D-alg: chọn PDCF/PDC/cover; PODEM: gán PI qua backtrace |
| B. Quá trình tìm kiếm | Net nội bộ được gán trực tiếp | 4 (11, 16, 10, 22) | 0 | PODEM chỉ gán PI, net nội bộ suy ra bằng mô phỏng |
| B. Quá trình tìm kiếm | PI được chọn trực tiếp | - | 3, 2 |  |
| B. Quá trình tìm kiếm | Số lần justify (J-frontier) | 1 | 0 (không cần) | PODEM không có bước justify riêng |
| B. Quá trình tìm kiếm | Số lần quay lui (backtrack) | 0 | 0 | phụ thuộc thứ tự thử, không phải thước đo tuyệt đối |
| B. Quá trình tìm kiếm | Nếu đổi thứ tự thử cube của D-algorithm | order=first: DETECTED, X10XX, 2 quyết định, 0 quay lui | - | cùng thuật toán, chỉ đổi thứ tự thử |
| C. Chi phí tính toán | Số lần gọi implication | 4 | 4 | D-alg: implication tiến + lùi; PODEM: mô phỏng tiến |
| C. Chi phí tính toán | Số lần đánh giá cổng | 36 | 24 | đếm trong code của từng thuật toán; chỉ so sánh tương đối |
| C. Chi phí tính toán | Thời gian (trung vị, ms) | 0.759 | 0.087 | phụ thuộc máy chạy |
| D. Đối chiếu | Khớp chạy tay | khớp (Chương 3 (P2), bảng chạy tay: X100X, 4 quyết định, 0 quay lui) | khớp (results/golden_trace_c17_11sa0.md (P3): X10XX, 2 quyết định, 0 quay lui) |  |

## Trace D-algorithm

| Bước | Loại | Cổng | Cube | Net đã biết sau implication | D-frontier | J-frontier | Hành động |
|---|---|---|---|---|---|---|---|
| 1 | PDCF | 11 | (3=X, 6=0) -> 11=D | 6=0, 11=D | {16, 19} | {} | kích hoạt |
| 2 | PDC | 16 | PDC qua 16: 2=1 | 2=1, 6=0, 11=D, 16=D' | {22, 23, 19} | {} | lan truyền |
| 3 | PDC | 22 | PDC qua 22: 10=1 | 2=1, 6=0, 10=1, 11=D, 16=D', 22=D | {23, 19} | {10} | lan truyền |
| 4 | Cover | 10 | (1=X, 3=0) -> 10=1 | 2=1, 3=0, 6=0, 10=1, 11=D, 16=D', 22=D | {23, 19} | {} | thành công |

## Trace PODEM (P5)

| Bước | Objective (net, giá trị) | Backtrace → PI | Gán PI | Giá trị các net sau imply | D-frontier | Hành động |
|---|---|---|---|---|---|---|
| 1 | ('11', 1) | ('3', 0) | 3=0 | {'1': 'X', '2': 'X', '3': '0', '6': 'X', '7': 'X', '10': '1', '11': 'D', '16': 'X', '19': 'X', '22': 'X', '23': 'X'} | ['16', '19'] | tiếp tục |
| 2 | ('2', 1) | ('2', 1) | 2=1 | {'1': 'X', '2': '1', '3': '0', '6': 'X', '7': 'X', '10': '1', '11': 'D', '16': "D'", '19': 'X', '22': 'D', '23': 'X'} | ['19', '23'] | thành công |

