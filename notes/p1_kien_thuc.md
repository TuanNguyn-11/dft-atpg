# Tài liệu tự học và thuật ngữ P1

Nội dung phục vụ phần P1 theo prompt.md/P1.md; không xác nhận người học đã trả lời đúng các câu tự kiểm tra. Báo cáo dùng bản ngắn theo kế hoạch 5–10 trang, còn diễn giải chi tiết để tại đây.

## 1. Testing, mô hình lỗi và logic

Verification kiểm tra thiết kế theo đặc tả; testing tìm chip lỗi sau chế tạo. Chuỗi khái quát là thiết kế → chế tạo wafer → kiểm thử wafer → đóng gói → kiểm thử thành phẩm. Yield là tỷ lệ sản phẩm đạt yêu cầu trong một tập sản phẩm xác định; defect là khuyết tật vật lý, fault là mô hình trừu tượng của ảnh hưởng khuyết tật. Test escape là sản phẩm lỗi không bị phép kiểm thử loại ra. Coverage của mô hình không đồng nhất với yield hoặc tỷ lệ phát hiện tất cả khuyết tật vật lý.

SA0/SA1 buộc tín hiệu bằng 0/1; bridging mô tả nối ngoài ý muốn giữa dây, delay mô tả tín hiệu đến muộn. Stuck-at được dùng vì đơn giản, phù hợp logic mức cổng và nhiều phương pháp ATPG đã phát triển, nhưng không thay mọi mô hình lỗi khác.

Trong logic năm giá trị, `0=(0,0)`, `1=(1,1)`, `D=(1,0)`, `D'=(0,1)` theo thứ tự tốt/lỗi; X là chưa xác định. Kích hoạt lỗi 11/SA0 trên c17 cần net 11 tốt bằng 1; chọn PI 3=0. Đặt PI 2=1 để lỗi đi qua cổng 16 và tới 22. Mẫu `(X,1,0,X,X)` được kiểm tra với đủ 8 cách điền X, không suy rộng rằng mọi X trong một kết quả thuật toán bất kỳ đều hợp lệ.

Tự kiểm tra: (1) Vì sao thiết kế đúng vẫn cần testing? (2) Net mang D' có giá trị tốt/lỗi nào? (3) Vì sao chỉ kích hoạt lỗi chưa đủ?

## 2. Collapsing, mô phỏng và coverage

Fault list phải ghi phạm vi: 11 net c17 × 2 = 22 lỗi chỉ khi xét net/stem, không gồm các lỗi nhánh riêng. Fault equivalence về phát hiện là cùng tập mẫu phát hiện. Tương đương đáp ứng yêu cầu mọi mẫu cho cùng đáp ứng mạch lỗi, mạnh hơn tương đương phát hiện.

NAND độc lập: input SA0 và output SA1 đều làm output=1. Trên c17 chỉ có thể áp dụng trực tiếp với đường không phân nhánh như net 1 → 10: 1/SA0 và 10/SA1 cho cùng hai PO trên cả 32 mẫu. Stem 3 có hai nhánh nên không áp dụng máy móc quy tắc này.

Dominance nên diễn đạt bằng tập để tránh nhầm quy ước tên: nếu `T(a) ⊆ T(b)`, giữ lỗi a làm mục tiêu khó hơn; mẫu cho a bảo đảm phát hiện b. Với NAND độc lập, `T(input a/SA1)={01}` và `T(output/SA0)={00,01,10}`. Không tự xem đây là quan hệ toàn mạch có fanout.

Serial fault simulation chạy từng mạch lỗi. Parallel fault simulation có thể dùng các bit trong từ máy để đánh giá đồng thời nhiều lỗi. Fault dropping ngừng xét lại lỗi đã được phát hiện. Coverage phải đếm hợp của tập lỗi, ví dụ hai mẫu phát hiện 8 và 7 lỗi, giao nhau 3 thì tổng là 12, không phải 15. Nếu dùng fault list rút gọn, cần ánh xạ về lỗi gốc trước khi tuyên bố coverage gốc; trọng số lớp và dominance không được bỏ qua.

`DETECTED`: có mẫu được kiểm chứng. `UNTESTABLE`: đã chứng minh không có mẫu trong mô hình/phạm vi đang xét. `ABORTED`: hết giới hạn, chưa đủ kết luận. Mạch tuần tự trải hữu hạn khung không có mẫu không chứng minh mạch gốc không bao giờ kiểm thử được.

Tự kiểm tra: (1) Vì sao 22 không phải số lỗi của mọi quy ước c17? (2) Nếu T(a) nằm trong T(b), nên giữ lỗi nào? (3) Hết giới hạn backtrack thuộc trạng thái nào?

## 3. SCOAP và tìm kiếm

Controllability là mức dễ đặt tín hiệu về giá trị mong muốn; observability là mức dễ đưa ảnh hưởng tới PO. SCOAP dùng chi phí, không phải xác suất. Quy tắc PI: CC0=CC1=1; PO: CO=0. Với NAND(a,b), CC0=CC1(a)+CC1(b)+1, CC1=min(CC0(a),CC0(b))+1; CO nhánh a=CO(output)+CC1(b)+1. Stem lấy min CO của các nhánh.

| Net | CC0 | CC1 | CO |
|---|---:|---:|---:|
| 1 | 1 | 1 | 5 |
| 2 | 1 | 1 | 6 |
| 3 | 1 | 1 | 5 |
| 6 | 1 | 1 | 7 |
| 7 | 1 | 1 | 6 |
| 10 | 3 | 2 | 3 |
| 11 | 3 | 2 | 5 |
| 16 | 4 | 2 | 3 |
| 19 | 4 | 2 | 3 |
| 22 | 5 | 4 | 0 |
| 23 | 5 | 5 | 0 |

Ví dụ CO nhánh `3→10` = 3+1+1=5, nhánh `3→11` = 5+1+1=7; CO stem 3 = min(5,7)=5. SCOAP bỏ qua tương quan khi fanout hội tụ, nên có thể đánh giá lạc quan. Không dùng bảng này để chứng minh testability hoặc tuyên bố code PODEM đã dùng SCOAP.

ATPG ngẫu nhiên dễ tạo mẫu nhưng có thể bỏ sót lỗi khó. ATPG tất định chọn lỗi, tạo điều kiện kích hoạt/lan truyền, justify từ PI, imply, backtrack khi xung đột và mô phỏng để fault dropping. D-algorithm (Roth, 1966) tìm kiếm trên các đường mạch; PODEM (Goel, 1981) quyết định tại PI; FAN (Fujiwara và Shimono, 1983) khai thác fanout và nhiều kỹ thuật giảm tìm kiếm. ATPG tuần tự phải xử lý trạng thái: full scan tăng khả năng điều khiển/quan sát, còn time-frame expansion chuyển một bài toán hữu hạn chu kỳ thành mạch tổ hợp.

Tự kiểm tra: (1) Tính CC0(16) và CO(11). (2) Vì sao CO(3) là 5, không phải 12? (3) SCOAP nhỏ có bảo đảm tìm được mẫu không?

## 4. Tích hợp báo cáo và review

`report/main.tex` khai báo gói, font, thư mục tài liệu và nạp tám chương. Các chương không tự khai báo documentclass; nhãn và bib key có tiền tố người viết. XeLaTeX tạo thông tin trích dẫn; Biber đọc `.bib` và sinh bibliography; chạy XeLaTeX thêm hai lượt giải quyết tham chiếu. Không sửa thiếu nguồn bằng cách gõ tay số tài liệu hoặc dấu tham chiếu.

Review PR cần đọc diff, kiểm tra phạm vi và bằng chứng, chạy kiểm thử liên quan, build báo cáo/slide, đối chiếu nguồn và kiểm tra PDF. Cập nhật từ main rồi chỉ push nhánh cá nhân; merge khi kết quả kiểm tra phù hợp, không chỉ dựa vào trạng thái “mergeable”.

| Thuật ngữ | Cách dùng thống nhất |
|---|---|
| Fault activation | Kích hoạt lỗi |
| Fault propagation | Lan truyền ảnh hưởng lỗi |
| Justification | Tìm gán PI nhất quán để thực hiện yêu cầu nội bộ |
| Fault collapsing | Rút gọn danh sách lỗi |
| Fault dropping | Loại lỗi đã phát hiện khỏi danh sách còn xét |
| Controllability / observability | Khả năng điều khiển / quan sát |
| Reconvergent fanout | Các nhánh fanout hội tụ lại |
| Test cube | Mẫu có thể chứa X; phải kiểm chứng cách điền |

Tự kiểm tra: (1) Khi nào chạy Biber? (2) Vì sao PR không xung đột vẫn cần review nội dung?

## Nguồn và tái lập

Giáo trình Wang/Wu/Wen (2006), Chương 1, mục 2.2.1 (trang 41–44), mục 3.4 và Chương 4; slide môn học về fault modeling do P1 cung cấp. Công thức SCOAP đã đối chiếu trực tiếp trang 41–42, bài video trang 166–167. Ví dụ c17 tự tính theo netlist trong prompt.md, không nhận là số liệu đo từ lõi PODEM. Chạy `python scripts/check_p1_examples.py` để tái lập kiểm tra.
