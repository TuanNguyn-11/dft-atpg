# Lời giải và lời dẫn video của P1

P1 đã xác nhận tự quay video 2–3 phút. Tài liệu này chuẩn bị nội dung; video chưa được quay hoặc nộp.

Nguồn: Wang, Wu, Wen (biên tập), *VLSI Test Principles and Architectures: Design for Testability*, Morgan Kaufmann, 2006, Chương 4 của Michael S. Hsiao, mục 4.3, Hình 4.5, trang in 166–167 (trang PDF 197–198 trong bản được cung cấp). Đã kiểm tra dấu phủ định trên ảnh trang gốc. Đây là **ví dụ Hình 4.5**, không gọi là “Bài 4.5”.

## Đề và lời giải

Với `f = x*y + NOT(y)*z`, tìm vector `(x,y,z)` phát hiện lỗi **stem y/SA0**. Dấu `+` là OR, `*` là AND. Lỗi stem tác động cả nhánh vào AND trên và nhánh vào bộ đảo.

1. Kích hoạt: đặt `y=1`, đối nghịch stuck-at-0.
2. Mạch tốt lúc này có `f_good=x`. Mạch lỗi luôn thấy `y=0`, nên `f_faulty=z`.
3. Quan sát: cần `f_good XOR f_faulty = x XOR z = 1`.
4. Điều kiện đầy đủ là `y * (x XOR z) = 1`, cho hai vector `110` và `011`.

Boolean difference `df/dy = f(y=1) XOR f(y=0) = x XOR z` là điều kiện nhạy với thay đổi của y. Phải kết hợp với kích hoạt `y=1`; chỉ có Boolean difference bằng 1 chưa đủ phát hiện y/SA0.

| x | y | z | f tốt | f lỗi y/SA0 | Phát hiện |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | Không |
| 0 | 0 | 1 | 1 | 1 | Không |
| 0 | 1 | 0 | 0 | 0 | Không |
| 0 | 1 | 1 | 0 | 1 | Có |
| 1 | 0 | 0 | 0 | 0 | Không |
| 1 | 0 | 1 | 1 | 1 | Không |
| 1 | 1 | 0 | 1 | 0 | Có |
| 1 | 1 | 1 | 1 | 1 | Không |

## Lời dẫn gợi ý — khoảng 2 phút 30 giây

**0:00–0:20 — Nguồn và đề.** “Em là Phan Ngọc Tuấn Nguyên, phụ trách nguyên lý ATPG. Em trình bày ví dụ Hình 4.5, mục 4.3, trang 166–167 của giáo trình VLSI Test Principles and Architectures. Mục tiêu là tìm đầu vào phát hiện lỗi y kẹt ở mức 0.”

**0:20–0:45 — Giải thích mạch.** Vẽ lại hai AND, một NOT và một OR; đánh dấu y trước chỗ rẽ nhánh. “Hàm đầu ra là x AND y, OR với NOT y AND z. Vì lỗi nằm trên stem nên cả hai nhánh của y đều nhận giá trị lỗi 0, chứ không chỉ một nhánh.”

**0:45–1:15 — Kích hoạt.** “Trước hết phải đặt y bằng 1. Khi đó mạch tốt có đầu ra bằng x. Ở mạch lỗi, y vẫn bằng 0 nên đầu ra bằng z. Nếu đặt y bằng 0 thì mạch tốt và mạch lỗi giống nhau, lỗi chưa được kích hoạt.”

**1:15–1:50 — Quan sát và tìm vector.** “Muốn phát hiện lỗi, hai đầu ra phải khác nhau, tức x XOR z bằng 1. Kết hợp y bằng 1, ta có hai bộ đầu vào theo thứ tự x, y, z là 110 và 011. Biểu thức x XOR z cũng chính là Boolean difference của f theo y.”

**1:50–2:15 — Kiểm tra.** “Với 110, mạch tốt ra 1 và mạch lỗi ra 0. Với 011, mạch tốt ra 0 và mạch lỗi ra 1. Ngược lại, 111 dù kích hoạt y nhưng cả hai đầu ra đều bằng 1 nên không phát hiện lỗi.”

**2:15–2:30 — Kết luận.** “Có đúng hai vector phát hiện y/SA0: 110 và 011. Ví dụ cho thấy ATPG phải đồng thời kích hoạt lỗi và đưa ảnh hưởng lỗi ra đầu ra quan sát được.”

## Kế hoạch quay theo cảnh — bản chốt 06/10/2026

Cách quay đơn giản nhất: quay màn hình (OBS hoặc Xbox Game Bar `Win+Alt+R`) kèm micro, viết tay trên giấy/bảng trắng hoặc tablet. Đọc theo lời dẫn ở trên; mỗi cảnh có thể quay riêng rồi ghép.

| Cảnh | Thời gian | Hình trên màn hình | Thao tác |
|---|---|---|---|
| 1 | 0:00–0:20 | Trang bìa giáo trình + dòng “Hình 4.5, mục 4.3, tr. 166–167” | Giới thiệu tên, vai trò, nguồn và đề |
| 2 | 0:20–0:45 | Sơ đồ tự vẽ: AND trên (x, y), NOT trên nhánh y dưới, AND dưới (¬y, z), OR ra f | Khoanh điểm y **trước** chỗ rẽ nhánh, ghi “y/SA0 (stem)” |
| 3 | 0:45–1:15 | Cùng sơ đồ, ghi giá trị tốt/lỗi | Ghi `y = 1/0`; viết `f_tốt = x`, `f_lỗi = z` |
| 4 | 1:15–1:50 | Biểu thức | Viết `x ⊕ z = 1` và `y = 1` → khoanh `110`, `011` |
| 5 | 1:50–2:15 | Bảng chân trị 8 dòng (bảng ở trên) | Tô hai dòng “Có”; chỉ dòng `111` để giải thích vì sao không phát hiện |
| 6 | 2:15–2:30 | Một dòng kết luận | “Hai vector: 110 và 011 — vừa kích hoạt vừa lan truyền” |
| 7 (tùy chọn, ≤15 s) | — | Terminal chạy `python scripts/check_p1_examples.py` | Chỉ dòng `PASS: Figure 4.5 (8 vectors), detects y/SA0: 011, 110` |

Thứ tự đầu vào luôn đọc là **x, y, z**. Tổng thời lượng mục tiêu 2:30, tối đa 3:00. Xuất MP4 (H.264), 1080p hoặc 720p; đặt tên gợi ý `Nhom4_P1_Hinh4-5_ySA0.mp4`. Không đưa video hay ảnh chụp trang sách lên repo công khai.

## Kiểm tra trước khi quay

- Hiển thị nguồn, số hình và thứ tự PI rõ ràng; sơ đồ tự vẽ cần giữ đúng dấu NOT ở nhánh y phía dưới.
- Thử giải thích vì sao 111 không phát hiện lỗi và vì sao lỗi stem khác lỗi nhánh.
- Chạy `python scripts/check_p1_examples.py` để đối chiếu đủ 8 vector.
- P1 tự diễn tập, quay và kiểm tra âm thanh/thời lượng; bổ sung đường dẫn video vào gói nộp khi có. Định dạng và kênh nộp theo yêu cầu giảng viên.
