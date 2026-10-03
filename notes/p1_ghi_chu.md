# Ghi chú P1

## Tiến độ học
- Đã học và trả lời đúng: verification và testing; kích hoạt và lan truyền lỗi stuck-at.
- Đã giới thiệu: logic 5 giá trị và ý tưởng ATPG; chưa hoàn tất câu hỏi kiểm tra.
- Đã giới thiệu fault list, fault simulation, coverage; chưa nhận câu trả lời tự kiểm tra.
- Cần học tiếp và kiểm tra hiểu: fault collapsing, SCOAP và các nội dung chuyên sâu ở mục 2 của P1.md.

## Ví dụ đã học
Mạch c17, lỗi stem `11/SA0`.
Theo thứ tự PI `(1,2,3,6,7)`, mẫu `(X,1,0,X,X)` phát hiện lỗi qua ngõ ra 22.
Net 11 mang D, net 16 mang D', net 22 mang D.
Đặt PI 2 bằng 0 sẽ chặn đường truyền lỗi qua net 16.

## Mốc M0
- Khởi tạo repo và khung báo cáo, slide.
- Chưa có nội dung hoàn chỉnh của các chương hoặc code ATPG.
- Đã bổ sung thông tin trường, giảng viên và sáu thành viên theo xác nhận của P1.
- Đã đọc rubric: báo cáo 5–10 trang; bắt buộc có bài tập từ tài liệu môn học và video giải thích.
- Cần mời năm thành viên, tổ chức họp khởi động, xác nhận giao diện P5/P6.
- Cần biên dịch bằng XeLaTeX + Biber trên TeXPage hoặc máy có TeX Live.

## Điều chỉnh ngày 01/10/2026
- Hạn nộp chính thức 08/10; mục tiêu hoàn thành hết 05/10.
- Thuyết trình và demo: 20 phút, không bao gồm hỏi đáp. Video giải thích: khoảng 2–3 phút.
- Dàn ý nhiều trang trong P1.md được thay bằng ngân sách trang ở [kế hoạch P1](p1_ke_hoach.md).
- Chưa xác nhận thành công khi biên dịch trên TeXPage.
- Giáo trình chính đã nhận: Wang/Wu/Wen (biên tập), 2006. Đề xuất ví dụ video tại mục 4.3, Hình 4.5, trang 166–167; chưa dạy/kiểm tra phần Boolean difference.
- P2–P6 chưa triển khai theo thông tin P1 cung cấp.

## Tiến độ ngày 03/10/2026
- Đã tạo bản nháp Chương 1 từ kiến thức nền đã học; chưa biên dịch PDF để đo số trang.
- Kiểm tra GitHub: main còn là khung, chưa có code/kết quả/chương hoàn chỉnh được đưa lên; không suy ra tiến độ làm riêng của từng thành viên.
- PR số 4 còn mở; P1 kiểm tra trước khi merge.
- Đáp án bài trước: 11 net nhân 2 lỗi = 22 lỗi (chỉ xét net/stem); 8 + 7 - 3 = 12 lỗi khác nhau; hết giới hạn backtrack là ABORTED, không kết luận UNTESTABLE.

## Bài học tiếp: fault equivalence
- Hai lỗi tương đương về phát hiện có cùng tập vector phát hiện; có thể giữ một đại diện khi sinh mẫu.
- Cổng NAND hai đầu vào: a/SA0, b/SA0, z/SA1 cùng được phát hiện bởi ab=11 khi xét cổng riêng.
- Ví dụ c17: net 1 chỉ đi vào cổng 10, nên lỗi stem 1/SA0 tương đương 10/SA1. Đã kiểm tra hai đáp ứng PO bằng nhau trên toàn bộ 32 vector nhị phân.
- Với net có fanout, không áp dụng máy móc tương đương tại một cổng cho lỗi stem toàn mạch; phải phân biệt stem và branch.
- Nguồn khái niệm: bài giảng chap2_Fundamentals of Fault Modeling and Structural Testing.pdf, trang PDF 14. Ví dụ NAND/c17 do trợ giảng diễn giải và kiểm tra, không nhận là ví dụ nguyên văn từ bài giảng.
- Chưa xác nhận người học đã hiểu phần này; chưa chuyển thành nội dung Chương 2.
