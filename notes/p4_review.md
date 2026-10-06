# Rà soát P4 hiện tại — 06/10/2026

## Checklist theo feedback mới

| Mục | Trạng thái | Bằng chứng / phụ thuộc |
|---|---|---|
| P4-01: full scan trên API thật | Đã làm | `scripts/p4_integrated_experiment.py`, `results/seq_integrated_full_scan.md`: 18/18 PODEM `DETECTED`, mọi X xác nhận bởi simulator và oracle P4, bộ 6 vector điền X=0 phủ 18/18. |
| P4-02: CLI không scan k=1/2/3 | Đã làm | `results/seq_integrated_k1.md`–`seq_integrated_k3.md`: 1/18, 13/18, 18/18 bảo đảm; từng hàng có cột `Thuat toan` từ `GenResult.algo`. Exporter chung đã có cột này ở `main` mới nên P4 không sửa module P6. |
| P4-03: test tích hợp và tài liệu | Đã làm | `tests/test_p4_integration.py` gọi PODEM thật, ngoài fixture tắt PODEM; giữ 10 test unroll và oracle độc lập. Đã cập nhật Chương 5, slide, ghi chú kết quả. |
| Bản PDF/slide phát hành | Phụ thuộc P1 | P1 phụ trách dàn trang, build và duyệt lại tài liệu cuối sau khi nhận thay đổi P4. Không coi PDF/PPT hiện có đã chứa commit này. |

## Bằng chứng chạy lại

- Nền: `origin/main` commit `586218e` (sau release `v1.0`); PR P4 cũ #5 đã merge. Script/test tích hợp được commit ở `553dfb6` trước khi sinh artifact; commit này được ghi trong các tệp output. Chỉ sửa nhánh `p4-tuan-tu`.
- Python **3.12.0**, pytest **9.1.1** trên Windows; `PYTHONPATH=src`, `PYTHONIOENCODING=utf-8`.
- `python -m pytest tests/test_unroll.py tests/test_sequential.py tests/test_p4_integration.py -q`: **24 passed**. `python -m pytest -q`: **334 passed**.
- `python scripts/p4_seq_experiment.py`: tham chiếu độc lập vẫn cho full scan 18/18, không scan k=1/2/3 là 1/18, 13/18, 18/18.
- `python scripts/p4_integrated_experiment.py --md results/seq_integrated_full_scan.md`: PODEM 18/18, cube 18/18 được simulator và oracle nhị phân xác nhận, bộ mẫu điền X=0 phủ 18/18. Tám vector nhị phân có tối đa 9/18 lỗi cho một vector.
- `python -m atpg.run circuits/seq_example.bench --unroll K --all --md results/seq_integrated_kK.md` cho K=1,2,3: bảo đảm 1/18, 13/18, 18/18; nguồn PODEM/vét cạn bổ sung lần lượt 0/1, 3/10, 3/15. Không có `ABORTED` hay kết luận kiểm chứng sai trong ba lần chạy.

## Phạm vi và bàn giao

- Mẫu số luôn là **18 lỗi stem vật lý**, cấy ở mọi khung; không dùng lỗi nhánh hoặc fault collapsing tuần tự. Full scan đặt Q qua scan-in và quan sát D qua capture/scan-out. `--init controllable` chỉ đặt `Q@0`, không thêm quan sát D.
- `Q@0` không biết trong CLI k=1/2/3: `DETECTED` chỉ khi tập vết PO tốt và lỗi rời nhau với mọi cặp trạng thái đầu và mọi cách điền X. `CO DIEU KIEN Q@0` chưa phải bảo đảm; 8 `UNTESTABLE` ở k=1 chỉ đúng trong **giới hạn một khung**, không kết luận cho mọi độ dài.
- File P4 đổi/thêm: script và test tích hợp, bốn artifact `results/seq_integrated_*.md`, `results/seq_example_results.md`, `notes/p4_review.md`, Chương 5 và slide P4. Script tham chiếu cũ cùng `tests/test_unroll.py` giữ nguyên.
- Nội dung đề xuất PR: “Bổ sung thí nghiệm P4 tái lập trên Circuit/PODEM/simulator thật và CLI k=1–3; đối chiếu mọi cube với oracle độc lập, phân biệt nguồn PODEM/vét cạn và trạng thái đầu chưa biết. Kiểm thử 334 passed; giới hạn 18 stem, không hỗ trợ nhánh DFF. P1 dàn trang lại PDF/slide cuối.”

## Việc cần con người xác nhận hoặc thực hiện

- [ ] P1 nhận và dàn trang lại Chương 5/slide trong bản phát hành, kiểm tra PDF cuối; P4 không tự xác nhận bản nộp.
- [ ] Nhóm tập demo/thuyết trình 20 phút, xác nhận giờ, kênh và định dạng nộp ngày 08/10/2026; P1 phụ trách video 2–3 phút.
- [ ] Người có quyền review PR P4 mới và quyết định merge; P4 không tự merge.

---

# Lịch sử: rà soát P4 sau phản hồi PR #5 — 04/10/2026

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
