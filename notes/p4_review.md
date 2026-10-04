# Rà soát P4 ngày 04/10/2026

## Kết luận

Có thể push branch `p4-tuan-tu` để nhóm review phạm vi P4. Chưa xác nhận hoàn thành tích hợp hoặc sẵn sàng nộp PDF cuối. Chưa push, chưa mở PR, chưa merge.

## Bằng chứng đã kiểm tra

- Sau fetch, `origin/main` vẫn ở `be01e43`; chưa có thay đổi mới so với nền của nhánh P4, chưa có module P5/P6 trên main.
- Chạy `python tests/test_unroll.py`: 8/8 test qua. Mạch unroll khớp mô phỏng tuần tự trong 3192 trường hợp (k=1..3, mọi chuỗi PI, hai trạng thái đầu, 18 lỗi và mạch không lỗi). Full scan khớp trong 152 trường hợp. Có kiểm tra cập nhật đồng thời hai DFF và ví dụ không được tùy ý điều khiển Q0.
- Tính lại 18 dòng mẫu trong `seq_example_results.md`: tất cả khớp kết quả chương trình.
- Full scan đạt 18/18 lỗi stem. Không scan: k=1 đạt 1/18, k=2 đạt 13/18, k=3 đạt 18/18. Đã bổ sung số liệu theo k vào báo cáo/kết quả để tránh hiểu nhầm `--unroll 2` đạt 100%.
- Các môi trường, cặp ngoặc, đường dẫn hình, nhãn tham chiếu và khóa trích dẫn LaTeX đã qua kiểm tra cấu trúc. Kiểm tra này không thay cho biên dịch và xem PDF.

## Các bước còn thiếu trước khi xác nhận bản cuối

1. Chạy với `Circuit`, `Fault`, `podem`, `fault_sim` và CLI thật của P5/P6. Các test hiện dùng đối tượng theo hợp đồng giao diện; số liệu là vét cạn độc lập, chưa phải kết quả PODEM.
2. Khi dùng PODEM trên mạch unroll, kiểm tra mẫu hợp lệ với trạng thái đầu không biết; Q@0 là PI hình thức. Lỗi nhánh đi vào DFF chưa được ánh xạ bởi giao diện fault_in_frames hiện tại; phạm vi thực nghiệm là stem.
3. Chạy pytest trong môi trường đã cài pytest. Tám hàm test đã chạy trực tiếp bằng Python chuẩn ở lần rà soát này.
4. Biên dịch báo cáo/slide với XeLaTeX và Biber, xem bố cục PDF. Trình biên dịch tích hợp hiện báo `Unable to find standard directories for platform`, nên chưa có xác nhận biên dịch thành công.
