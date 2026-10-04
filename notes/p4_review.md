# Rà soát P4 sau phản hồi PR #5 — 04/10/2026

## Hai sửa đổi kỹ thuật

1. `fault_in_frames(fault,k)` giữ nguyên chữ ký và chỉ ánh xạ lỗi stem. Mọi lỗi nhánh đều báo `ValueError` rõ ràng trước khi đưa sang PODEM hoặc fault simulator: hàm không có `Circuit` để xác nhận đích là cổng tổ hợp hay DFF. Với DFF, cạnh chuyển trạng thái trong `unroll(c,2)` là `D@0 -> Q@1`; `Q@0` là PI hình thức và không có cạnh `D@1 -> Q@1`. Hỗ trợ lỗi nhánh trong tương lai cần giao diện có thông tin mạch, thống nhất cùng P1/P5/P6.
2. Slide full scan ghi “bộ vector vét cạn”. Tám vector `(A,B,Q)` lần lượt phát hiện `3, 3, 3, 3, 8, 7, 9, 8` trên 18 lỗi stem; tối đa **9/18 lỗi cho một vector**. Tổng `18/18` nghĩa là **mỗi lỗi có ít nhất một vector phát hiện**, không phải cùng một vector phát hiện tất cả.

## Kiểm tra trên bản sửa

- `python tests/test_unroll.py`: **10/10 test qua**. Test mới kiểm tra k=1 và k=2, mọi stem ánh xạ đến net tồn tại, nhánh vào cổng tổ hợp và nhánh vào DFF đều bị từ chối rõ; đối chiếu unroll với mô phỏng tuần tự vẫn gồm 3192 trường hợp, full scan vẫn gồm 152 trường hợp.
- `python -m pytest tests/test_unroll.py -q`: chưa chạy được trong môi trường này vì `No module named pytest`. Các hàm test trên đã chạy trực tiếp bằng Python chuẩn.
- `python scripts/p4_seq_experiment.py`: cả 18 hàng mẫu khớp bảng kết quả. Full scan `18/18`; không scan tối đa k=1 `1/18`, k=2 `13/18`, k=3 `18/18`, k=4 `18/18`. Đây là vét cạn độc lập, chưa phải output PODEM.
- Đếm riêng tám vector full scan bằng `one_cycle()` của script: `3, 3, 3, 3, 8, 7, 9, 8`; max `9/18`.

## Phạm vi và bàn giao

- `evaluate()` trong test chỉ mô phỏng lỗi stem; các test nhánh xác minh đường từ chối và cạnh của mạch trải, **không** tuyên bố đã mô phỏng hoặc phát hiện lỗi nhánh.
- Chưa chạy tích hợp với `Circuit`, `Fault`, `podem`, `fault_sim` và CLI thật của P5/P6 vì các module đó chưa có trong `main` đối chiếu. Khi tích hợp, cần kiểm tra tính khả đạt của trạng thái `Q@0` và coverage thực tế.
- P1 đã biên dịch PDF ở commit P4 trước đó nhưng script build trả mã 1 do overfull; bản sửa này chưa được biên dịch lại ở môi trường hiện tại. P1 phụ trách tràn lề, rút gọn và biên tập báo cáo cuối.
