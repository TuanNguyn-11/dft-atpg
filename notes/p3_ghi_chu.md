# Ghi chú học và kiểm tra của P3

## Vai trò
P3 cung cấp lý thuyết và đáp án từng bước, P5 cài lõi, P6 mô phỏng và đối chiếu. Tài liệu này đã được soạn trực tiếp theo yêu cầu hoàn thành bàn giao của người dùng, không chờ vòng hỏi đáp học từng bước.

## Các khái niệm cần nắm
- Verification kiểm tra thiết kế đúng đặc tả; testing kiểm tra mẫu chip sau sản xuất.
- Kích hoạt SA0 bằng 1, SA1 bằng 0 trên mạch tốt. Lan truyền cần ít nhất một PO khác nhau giữa hai mạch.
- PODEM chỉ quyết định ở PI. Objective nội bộ là mong muốn, không phải phép ghi net nội bộ.
- X không phải một bit thứ ba vật lý. Pattern X biểu diễn bit chưa cần quyết định trong nghiệm; khi chỉ mô phỏng từng phần, net X cũng có thể do mất thông tin tương quan.
- D-frontier và X-path cho biết nơi còn khả năng truyền lỗi; X-path chỉ là điều kiện cần trong kiểm tra bảo thủ.
- Phân biệt FAIL của một nhánh, UNTESTABLE của toàn cây và ABORTED do giới hạn.
- Một lần backtrace qua nhiều cổng đảo: đếm parity số lần đảo. XOR/XNOR có quy tắc riêng.
- Độ điều khiển dễ/khó là heuristic. Golden trace dùng thứ tự đầu vào; không gán nhãn SCOAP cho quy tắc này.

## Liên hệ bài Hình 4.5
f=xy+NOT(y)z, lỗi y/SA0. Điều kiện phát hiện y(x XOR z)=1, hai vector (x,y,z)=110 và 011. Bài này minh họa activation/propagation bằng Boolean difference, không thay c17 và không phải ví dụ backtrack của gói này.

## Tài liệu đã dùng
Giáo trình đính kèm VLSI Test Principles and Architectures (2006): mục 4.3 trang in 166–167; mục 4.4.4 trang 182–186; mục 4.4.5 từ trang 186; danh mục nguồn Ch.4 trang 256–257. Phần thuật toán được đối chiếu trực tiếp với nội dung giáo trình. Không tuyên bố đã đọc toàn văn bài Goel/FAN: truy cập bài gốc qua công cụ web chưa thành công; thông tin tác giả/tựa/tạp chí/năm/trang được đối chiếu thư mục giáo trình. DOI Goel được tra cứu bổ sung, đích DOI chưa mở được trong phiên; CẦN KIỂM TRA LẠI truy cập khi nộp. Bản ghi IEEE FAN xác nhận tên và trang bài; link DOI được cung cấp trong .bib.

## Tự kiểm tra và đáp án
1. Vì sao 3=0 kích hoạt 11/SA0? NAND(0, bất kỳ)=1, khác stuck 0.
2. Vì sao chọn 2=1? Đây là ngõ vào bên cạnh của NAND16, giá trị không điều khiển 1.
3. Vì sao frontier cuối không rỗng mà thành công? PO22 đã là D.
4. Vì sao ví dụ phụ a=1 sai? n=0 chặn AND cuối với mọi b.
5. Vì sao a=0, b=X chưa thất bại? b=1 còn có thể kích hoạt t.
6. PODEM có luôn nhanh hơn D-algorithm không? Không có bảo đảm chung; cần đo trên cùng bộ lỗi.

## Cập nhật kiểm tra 05/10/2026

Đã nhận được dữ liệu P2 qua nhánh `p2-d-algorithm` tại commit `bb3756d`:
4 lần chọn cube, 3 PI gán, 0 backtrack; mẫu X100X rồi tổng quát hóa X10XX.
Đã chạy lại bộ kiểm chứng P2 đạt; chi tiết và nguồn ở `p3_doi_chieu_P5.md`.
Hình P2 là wrapper includegraphics, không chứa figure; đã kiểm tra cấu trúc
để không lồng float khi tích hợp. Chưa merge P2 vào nhánh P3.

Đã truy cập được [bản gốc FAN tại trang tác giả](https://archives.fujiwaralab.net/hideo/en/publication/J31_e_IEEE_TC_1983_10.pdf),
đối chiếu metadata và mô tả heuristic/headline/multiple backtrace.
DOI Goel vẫn không mở được bằng công cụ web; không nhận đã đọc toàn văn
bài Goel 1981. Thông tin nguồn gốc trong đoạn trước là ghi nhận của gói cũ.

Quy định repo mới rút toàn báo cáo còn 5–10 trang, hạn 08/10/2026, mục tiêu
nội bộ 05/10. Chương P3 được rút gọn; đọc thêm `p3_ly_thuyet.md` và hợp đồng
P3-v1. Kết quả build thực tế và phần còn thiếu ghi trong `p3_review.md`.

## Trạng thái sau tích hợp — 06/10/2026, base 8564678
- P2/P5/P6 đã tích hợp; P5 áp dụng P3-v1.1 và có exporter cả hai trace.
- Đã chạy code thật đối chiếu 35 ô và P6 xác nhận cube 8/8, mẫu phụ 01;
  giới hạn 0/1 đạt ABORTED/DETECTED. Xem `p3_doi_chieu_P5.md`.
- API và golden khác cách ghi hành động; exporter đã chuẩn hóa. Không
  nói raw trace khớp nguyên văn, không dùng tham chiếu P3 thay code P5.
- Các ghi chú ngày 05/10 phía trên là lịch sử. P1 đã tích hợp chương/bib,
  hình TikZ P2 và slide; còn review bản cập nhật P3, build PDF cuối và việc
  con người trong checklist `p3_ban_giao.md`.
