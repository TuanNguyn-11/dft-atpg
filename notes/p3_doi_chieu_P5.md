# Phiếu đối chiếu — chưa nhận trace code P5

## Nguồn kiểm tra ngày 05/10/2026

- Main: `f95d60949b35b20833b168c7f618b03367db71c5`.
- P2: `bb3756de9b434f2aaf91f194f3c05cdc61b9b58e`, nhánh
  [p2-d-algorithm](https://github.com/TuanNguyn-11/dft-atpg/tree/bb3756de9b434f2aaf91f194f3c05cdc61b9b58e).
  Đã đọc `notes/p2_ghi_chu.md`, `notes/p2_review.md`, Chương 3,
  bảng logic, bộ kiểm chứng và wrapper hình `report/figures/common/c17.tex`.
  Dữ liệu P2 chưa nằm trên main; chỉ đưa vào bản kiểm tra tạm, không chép
  các file P2 vào branch P3.
- Các nhánh remote có main, P1, P2, P4; chưa có nhánh P5/P6.
  Main không có `src/atpg/podem.py`, `logic.py`, `circuit.py`,
  `fault_sim.py`, `faults.py`, `run.py`, `circuits/c17.bench`,
  `results/trace_c17_11sa0.md` hoặc `results/c17_all_faults.md`.
  ZIP P3 và thư mục cung cấp cũng không có sản phẩm P5/P6.

## Đối chiếu với P2 đã có

P2 chọn PDCF với 6=0; PDC với 2=1; yêu cầu nội bộ 10=1; sau đó justify
bằng 3=0. Có **4 lần chọn cube, 3 PI được gán, 0 backtrack**. Không đếm
khởi tạo, implication và tổng quát hóa sau kiểm chứng vào số chọn cube.
Mẫu X100X gồm bốn vector; tổng quát hóa bỏ 6=0 thành X10XX gồm tám vector.
P3-v1 chọn 3=0 ngay đầu nên không phải gán 6 và không cần quyết định nội bộ
10=1. Đây là khác biệt lựa chọn và cơ chế tìm kiếm, không phải lỗi logic.

| Đại lượng | Trace tay P2 | Trace P3-v1 |
|---|---|---|
| Quyết định được đếm | 4 lần chọn cube | 2 phép gán PI |
| PI được gán | 6=0, 2=1, 3=0 | 3=0, 2=1 |
| Backtrack | 0 | 0 |
| Pattern trước tổng quát hóa | X100X | X10XX |
| Net cuối 10/11/16/19/22/23 | 1/D/D'/X/D/X | 1/D/D'/X/D/X |
| D-frontier cuối | {19,23} | {19,23} |
| J-frontier cuối | Rỗng | Không sử dụng |

Đã chạy bộ kiểm chứng P2 tại snapshot trên trong thư mục tạm: 160 ô logic,
bốn trạng thái trace, D/J-frontier, 4/4 và 8/8 completions, đáp ứng PO đều PASS.
Đây là chạy lại kiểm chứng dữ liệu P2, không phải xác nhận simulator P6.
Không có số đo thời gian, không tính tỷ lệ tăng tốc 4/2.

## P5: từng cột còn chờ

Không điền “khớp” trước khi nhận và kiểm tra dữ liệu thật.

| Mục | Kỳ vọng P3 | Kết quả P5 | Trạng thái |
|---|---|---|---|
| c17 bước 1 | obj(11,1), PI3=0, 11=D, frontier16/19 | Chưa nhận | Chờ |
| c17 bước 2 | obj(2,1), PI2=1, 16=D', 22=D, frontier19/23 | Chưa nhận | Chờ |
| c17 kết quả | DETECTED, X10XX, 0 backtrack | Chưa nhận | Chờ |
| phụ bước 1 | a=1, t=D, n=0, out=0 | Chưa nhận | Chờ |
| phụ bước 2 | đảo a=0, t=X, n=1, out=X | Chưa nhận | Chờ |
| phụ bước 3 | obj(t,1), b=1, out=D | Chưa nhận | Chờ |
| phụ kết quả | DETECTED, 01, 1 backtrack | Chưa nhận | Chờ |
| phụ giới hạn 0 | ABORTED, 0 backtrack | Chưa nhận | Chờ |
| phụ giới hạn 1 | DETECTED, 1 backtrack | Chưa nhận | Chờ |

Thứ tự xử lý khác biệt: kiểm tra netlist/lỗi và thứ tự PI; kiểm tra heuristic; kiểm tra thời điểm ghi trace; kiểm tra logic/cấy lỗi; cuối cùng kiểm chứng nhị phân độc lập. Một vector khác nhưng phát hiện được lỗi không tự động chứng minh trace chuẩn sai. Không dùng nhánh thiếu do ABORTED làm bằng chứng UNTESTABLE.

Khi có trace P5, đối chiếu toàn bộ bảy cột từng hàng với hai file golden:
objective, backtrace về PI, gán PI, mọi net, thứ tự D-frontier, hành động;
cuối cùng so status/pattern/backtracks. Bảng rút gọn trên không thay thế
đối chiếu từng net và không đánh dấu khớp trước khi có dữ liệu.

## P6: xác nhận còn thiếu

Cần `circuit.py`, `faults.py`, `fault_sim.py`, netlist c17 đúng quy định
và kết quả thực thi `detects` cho stem 11/SA0 với 01000 (PO tốt 11, lỗi 00),
stem t/SA0 với 01 (PO tốt 1, lỗi 0). Đề nghị kiểm tra thêm 8 completions
của X10XX. Ghi commit/code/lệnh và kết quả thật khi nhận được.
Hiện **chờ đối chiếu**; số liệu P3/P2 không thay cho xác nhận này.
