# Kế hoạch P1 — Nhóm 4

## Cập nhật thực hiện 03/10/2026

- Theo yêu cầu tiếp tục triển khai của P1, đã viết Chương 1/2, kết luận đúng trạng thái repo, ba frame và tài liệu tự học. Các ghi chú “học trước khi viết” bên dưới là kế hoạch ban đầu, không xác nhận P1 đã vượt qua kiểm tra kiến thức.
- P1 đã chốt và tự quay video Hình 4.5, mục 4.3, trang in 166–167; lời giải và lời dẫn ở `p1_video_loi_giai.md`. Công việc quay vẫn còn chờ thực hiện.
- Bảng SCOAP, ví dụ collapsing và vector Hình 4.5 đã có script kiểm chứng độc lập. Trạng thái kiểm tra bản dựng/PR ở `p1_review.md`.
- Chưa có phần P2–P6 hoàn chỉnh trong repo; chưa chốt báo cáo cuối, PDF nộp, hoặc tag v1.0. Chương 8 cần cập nhật khi nhận đủ thực nghiệm.

Các mục chưa phân công video bên dưới ghi lại kế hoạch trước cập nhật này.

## Cơ sở và ưu tiên
- Nguồn yêu cầu: thông tin P1 xác nhận ngày 01/10/2026 và trang 1 của `Thang_diem_DFT_public.pdf` do GV Nguyễn Văn Thành Lộc cung cấp.
- Yêu cầu mới thay thế các mốc và số trang cũ trong prompt.md/P1.md: hạn nộp 08/10, hoàn thành nội bộ hết 05/10, báo cáo 5–10 trang (không tính bìa và mục lục), trình bày và demo 20 phút.
- Đây là kế hoạch đề xuất của P1; chưa xác nhận khả năng đáp ứng của P2–P6.
- P1 xác nhận P2–P6 chưa triển khai, chưa biên dịch TeXPage. Thời gian trình bày 20 phút không gồm hỏi đáp; video khoảng 2–3 phút.
- Giữ phân công và hợp đồng code/trace. Không viết thay nội dung của thành viên khác.
- Tiếp tục học từng nhóm khái niệm trước khi viết; kết luận phải dựa trên kết quả thực tế.

## Ngân sách trang đề xuất
Tính cả hình, bảng, công thức trong từng phần. Đây là ngân sách biên tập, chưa phải số trang PDF đã đo.

| Phần | Người | Số trang mục tiêu | Nội dung ưu tiên |
|---|---|---:|---|
| 1. Giới thiệu | P1 | 0,5 | Bối cảnh, mục tiêu, phạm vi |
| 2. Nguyên lý ATPG | P1 | 1,75 | Stuck-at, activation/propagation, collapsing, coverage, SCOAP và luồng ATPG |
| 3. D-algorithm | P2 | 1 | Cơ chế, ví dụ c17, nhận xét |
| 4. PODEM | P3 | 1,25 | Objective/backtrace/imply/backtrack, trace rút gọn, so sánh |
| 5. ATPG tuần tự | P4 | 1 | Trạng thái, time-frame expansion, scan và đánh đổi |
| 6. Cài đặt | P5 | 0,75 | Kiến trúc, lựa chọn thiết kế, điều kiện dừng |
| 7. Kết quả | P6 | 1 | Kiểm chứng, coverage có mẫu số rõ, so sánh trace, giới hạn |
| 8. Kết luận | P1 | 0,25 | Kết quả thật, hạn chế và hướng phát triển |
| Viết tắt và tài liệu tham khảo | P1 tích hợp | 0,75–1,25 | Nguồn đã xác minh, ký hiệu thống nhất |

Tổng mục tiêu 8,25–8,75 trang; tối đa 10 trang. Riêng P1 khoảng 2,5 trang cho phần 1, 2, 8. Không giữ dự kiến riêng Chương 2 dài 8 trang.

Trong Chương 2 vẫn cần một ví dụ fault collapsing và bảng SCOAP c17, nhưng trình bày gọn. Trace đầy đủ, bảng logic đầy đủ và chi tiết code lưu trong repo; báo cáo phải có ví dụ đại diện và giải thích đủ để tự hiểu.

## Đối chiếu rubric
| Tiêu chí | Điểm | Bằng chứng cần chuẩn bị |
|---|---:|---|
| Thuyết trình: nội dung/kiến thức | 1,5 | Đủ nguyên lý, D-algorithm, PODEM, tuần tự; từng người giải thích được |
| Thuyết trình: phân tích kỹ thuật | 1,0 | So sánh thuật toán, ưu/nhược, điều kiện áp dụng và đánh đổi |
| Thuyết trình: slide/kỹ năng | 1,0 | Slide rõ; phân công hợp lý; diễn tập đúng giờ |
| Thuyết trình: ví dụ/kết quả | 0,75 | c17 11/SA0, trace và demo; giải thích ý nghĩa kết quả |
| Bài tập trong sách + video | 0,75 | Một bài từ sách/tài liệu môn học; đề, lời giải, kết luận; video nộp kèm |
| Báo cáo: nội dung/cấu trúc | 1,5 | 5–10 trang, đủ mở đầu–lý thuyết–nội dung chính–kết quả–kết luận |
| Báo cáo: chiều sâu | 1,5 | Có giải thích và so sánh, không chỉ mô tả |
| Báo cáo: hình thức | 1,0 | Nhất quán định dạng, caption, số hình/bảng/công thức và chính tả |
| Báo cáo: nguồn/học thuật | 0,5 | Nguồn tin cậy đã kiểm tra, trích dẫn đúng, không bịa kết quả |
| Báo cáo: kết luận/hoàn thiện | 0,5 | Kết luận đúng kết quả; báo cáo và slide thống nhất |

## Kịch bản 20 phút — đề xuất
| Người/phần | Phút |
|---|---:|
| P1: mở đầu, stuck-at, kích hoạt và lan truyền | 2 |
| P2: D-algorithm | 3 |
| P3: PODEM và so sánh | 3 |
| P4: ATPG tuần tự | 3 |
| P5: cài đặt và demo PODEM | 3 |
| P6: kết quả kiểm chứng, coverage và nhận xét | 3 |
| P1: kết luận | 1 |
| Dự phòng thao tác/chuyển người | 2 |

Tổng 20 phút, nội dung trình bày 18 phút, hỏi đáp nằm ngoài khung này. Video nộp kèm dài khoảng 2–3 phút. Nếu cần chiếu video trong buổi thuyết trình thì điều chỉnh thời lượng nội dung; chưa mặc định phải chiếu.

## Bài tập và video — đầu ra còn thiếu
- Giáo trình chính: *VLSI Test Principles and Architectures: Design for Testability*, Wang/Wu/Wen (biên tập), Morgan Kaufmann, 2006; đã đối chiếu trang tên sách và bản quyền trong PDF.
- Đề xuất ví dụ Hình 4.5, mục 4.3, trang in 166–167 (trang PDF 197–198), lỗi y/SA0. Đây là ví dụ trong nội dung sách, không phải bài tập đánh số. Rubric cho phép ví dụ hoặc bài tập. Xem [đề xuất video](p1_video_de_xuat.md).
- Chọn bài liên quan trực tiếp đến chủ đề; không mặc định demo c17 tự xây là bài trong sách.
- Lời giải phải có đề bài, bước giải/giải thích, kết luận và kiểm chứng nếu phù hợp.
- Người giải thích, quay, ghép và nộp video: chưa phân công.
- Đã xác nhận thời lượng khoảng 2–3 phút; còn thiếu định dạng, kênh nộp và yêu cầu xuất hiện của các thành viên.
- Không công bố video hoặc tài liệu môn học lên repo công khai khi chưa thống nhất cách chia sẻ.

## Lịch rút ngắn
- 01/10: hoàn thiện khung và thông tin nhóm; kiểm tra TeXPage; thống nhất giao diện, bài tập/video.
- 02/10: các dữ liệu nền sẵn sàng; học và viết ghi chú theo phần.
- 03/10: nhận bản nháp chương; PODEM chạy được lỗi mẫu; chuẩn bị lời giải bài tập.
- 04/10: ghép báo cáo/slide, kiểm chứng code và kết quả; quay video.
- 05/10: chốt nội dung, biên dịch, rà soát trang/trích dẫn, diễn tập và chuẩn bị gói nộp.
- 06–07/10: thời gian dự phòng.
- 08/10: hạn chính thức; giờ đóng cổng/cách nộp chưa được cung cấp.

## Checklist trước khi chốt
- [ ] TeXPage biên dịch báo cáo và slide; không có tham chiếu/citation chưa giải quyết.
- [ ] Báo cáo 5–10 trang nội dung; kiểm tra trên PDF thật, không suy từ số file.
- [ ] P1 hoàn tất học phần nền và nội dung chuyên sâu; viết phần 1, 2, 8.
- [ ] Có ví dụ collapsing và bảng SCOAP c17 đã kiểm tra.
- [ ] P2–P6 nộp nội dung, slide và kết quả theo phân công.
- [ ] Demo và fault simulation kiểm chứng được; không báo coverage chưa đo.
- [ ] Chọn/giải bài từ tài liệu môn học và hoàn thiện video.
- [ ] Diễn tập 20 phút, kiểm tra bản dự phòng demo.
- [ ] PDF, code, slide và video nhất quán; README đủ để tái hiện.
- [ ] Chỉ tạo tag v1.0 khi sản phẩm đã hoàn chỉnh.
