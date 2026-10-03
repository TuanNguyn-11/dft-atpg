# Đề xuất ví dụ cho video 2–3 phút

> **Cập nhật 03/10/2026:** P1 đã chốt Hình 4.5 và tự thực hiện video. Bản dưới đây giữ làm lịch sử đề xuất; trạng thái “chưa chốt/chưa phân công” không còn áp dụng. Dùng [lời giải và lời dẫn đã kiểm tra](p1_video_loi_giai.md) để chuẩn bị quay.

## Nguồn đã kiểm tra
- Sách: *VLSI Test Principles and Architectures: Design for Testability*.
- Biên tập: Laung-Terng Wang, Cheng-Wen Wu, Xiaoqing Wen; Morgan Kaufmann, 2006.
- Chương 4 (Test Generation), tác giả chương Michael S. Hsiao.
- Mục 4.3 (Theoretical Background: Boolean Difference), Hình 4.5, trang in 166–167.
- Trong bản PDF người học cung cấp: trang PDF 197–198 (đếm từ 1).
- Khóa BibLaTeX: `p1_wang2006`. Có thể dẫn `\cite[pp.~166--167]{p1_wang2006}`.
- Đã đọc văn bản và xem ảnh trang để kiểm tra dấu phủ định. Không dùng bản OCR làm nguồn duy nhất cho công thức.

## Ví dụ đề xuất
Diễn đạt lại nhiệm vụ: với mạch có hàm đầu ra
`f = x*y + NOT(y)*z`, tìm các bộ đầu vào (x,y,z) phát hiện lỗi stem y stuck-at-0.

Đây là ví dụ trong sách, không gọi là “Bài 4.5”. Hình 4.5 là số hình. Đề xuất này đáp ứng loại “ví dụ trong sách” của rubric; chưa được nhóm chốt.

Phù hợp P1 vì tập trung vào kích hoạt lỗi, quan sát khác biệt ở đầu ra và nguyên lý sinh mẫu. c17 vẫn là ví dụ chung cho báo cáo/code; không thay đổi hợp đồng của P2/P3/P5/P6.

## Trình tự học và chuẩn bị
1. Ôn lỗi stuck-at trên stem: ảnh hưởng tất cả nhánh xuất phát từ y.
2. Tính hàm khi y=1 và y=0.
3. Đặt điều kiện kích hoạt y/SA0.
4. Đặt điều kiện hai đầu ra khác nhau, liên hệ Boolean difference.
5. Tìm và kiểm tra vector; người học giải thích lại trước khi viết lời thoại hoàn chỉnh.

Chưa tạo lời thoại hoặc video cuối khi người học chưa hoàn tất phần giải thích/kiểm tra hiểu.

## Khung video dự kiến (2 phút 30 giây)
| Thời gian | Nội dung |
|---|---|
| 0:00–0:20 | Giới thiệu nguồn sách, số hình/trang và lỗi mục tiêu |
| 0:20–0:45 | Giải thích mạch/hàm và cách mô hình hóa lỗi |
| 0:45–1:15 | Kích hoạt lỗi, tìm điều kiện lan truyền/quan sát |
| 1:15–2:05 | Tìm vector, kiểm tra đầu ra mạch tốt và mạch lỗi |
| 2:05–2:30 | Kết luận và liên hệ nguyên lý ATPG |

Đề xuất P1 giải thích, P2 hoặc P3 kiểm tra nội dung; P6 hỗ trợ ghép nếu nhóm thống nhất. Đây chưa phải phân công đã được xác nhận. Không cần có code PODEM mới giải được ví dụ này.

## Phần sách P1 nên đọc
| Nội dung | Vị trí trong sách (số trang in) |
|---|---|
| Verification, testing, yield | Chương 1, mục 1.1–1.2, trang 1–7 |
| Mô hình lỗi | Mục 1.3.2, bắt đầu trang 11 |
| SCOAP | Mục 2.2.1, trang 41–44 |
| Fault simulation | Mục 3.4, trang 132–153 |
| Nguyên lý ATPG và Boolean difference | Mục 4.1–4.3, trang 161–168 |
| D-algorithm và PODEM | Mục 4.4.3–4.4.4, bắt đầu trang 177 và 182 |
| ATPG tuần tự | Mục 4.5, bắt đầu trang 194 |

Bảng là chỉ dẫn đọc từ mục lục đã kiểm tra, không phải tuyên bố mọi phần đã được học xong.

## Việc khởi động nhóm — P1 chuyển cho các thành viên
| Người | Đầu ra ưu tiên đến hết 02/10 |
|---|---|
| P1 | Biên dịch khung trên TeXPage; thống nhất kế hoạch; tiếp tục học; chốt ví dụ video |
| P2 | Hình c17 dùng chung và bảng logic 5 giá trị |
| P3 | Golden trace cho 11/SA0; thống nhất quy tắc chọn nhánh với P5 |
| P4 | Mạch tuần tự nhỏ và kế hoạch full scan/unroll theo giao diện |
| P5 | Xác nhận giao diện với P6; logic 5 giá trị và khung PODEM |
| P6 | Netlist c17, bộ đọc Circuit và mô phỏng nhị phân ban đầu |

Không cần chờ code hoặc chương của nhau mới bắt đầu học. Các mốc vẫn là mục tiêu đề xuất; P1 cần xác nhận khả năng thực hiện với nhóm. Chưa gửi thông báo hoặc giao việc qua dịch vụ bên ngoài.
