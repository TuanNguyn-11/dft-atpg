# Biên bản kiểm tra P3 — 05/10/2026

## Đầu vào và phạm vi

- Đọc đầy đủ `DFT_ATPG/prompt.md` (không tìm thấy file tên `prompt(1).md`),
  `DFT_ATPG/P3.md`, README_P3, hướng dẫn bàn giao và các nguồn trong ZIP.
  Thư mục giải nén sẵn thiếu nhiều sản phẩm; dùng ZIP làm nguồn đầy đủ.
  Các file nguồn giải nén sẵn trùng ZIP; riêng PDF preview sẵn có khác byte.
  Không sửa ZIP, bản giải nén hoặc tài liệu gốc đang mở trong IDE.
- Clone mới `TuanNguyn-11/dft-atpg`; cây ban đầu sạch, không có AGENTS.md,
  không có branch/PR P3. Branch tạo từ main `f95d60949b35b20833b168c7f618b03367db71c5`.
  Đã fetch lại trước bàn giao; main vẫn ở commit đó.
- Đọc README và kế hoạch P1: báo cáo toàn nhóm 5–10 trang, hạn 08/10,
  mục tiêu nội bộ 05/10; rút Chương 4 từ gói dài sang bản tích hợp ngắn.
  Giữ lý thuyết chi tiết, quy tắc, mã giả và trace trong notes/results.
- Chỉ sửa các file P3, netlist phụ và bộ kiểm chứng P3. Không sửa src/atpg,
  file P2/P4, main báo cáo, main slide hoặc README của P1.
- Đối chiếu P2 tại `bb3756de9b434f2aaf91f194f3c05cdc61b9b58e` bằng
  bản sao tạm. Chưa có dữ liệu P5/P6; chi tiết trong `p3_doi_chieu_P5.md`.

## Các kiểm tra thực sự đã chạy

| Kiểm tra | Kết quả |
|---|---|
| `python -B notes/p3_kiem_chung.py` | PASS; c17: 18/32 vector phát hiện 11/SA0; X10XX: 8/8 completions; 22 lỗi stem; hai trace và 113 so sánh net xác định |
| Mạch phụ | PASS: 01 duy nhất trong 4 vector; 3 hàng gán/đảo, 1 backtrack |
| `python -B notes/p3_kiem_tra_ban_giao.py` | PASS bảy cột của hai bảng, netlist phụ, chapter/nhãn/cite/key và 3 frame; báo PENDING netlist c17 P6 |
| `python -B scripts/check_p1_examples.py` | PASS collapsing 32 vector, cube 8 completions, SCOAP 11 net, Hình 4.5 8 vector |
| Kiểm chứng P2 tại snapshot | PASS 160 ô logic, 4 trạng thái và D/J-frontier, 4/4 và 8/8 completions, đáp ứng PO |
| LaTeX | XeLaTeX → Biber → XeLaTeX → XeLaTeX, tất cả exit 0 trong các bản sao khung thật |
| Slide | XeLaTeX nhiều lượt exit 0; ba frame P3 hiển thị đầy đủ |
| Hình | Build hình dự phòng, cây, lưu đồ riêng trong khung thật; build lại với wrapper JPG P2 |
| Tham chiếu/ký tự | Không undefined reference/citation, không Missing character, không dấu ?? trong PDF |
| Git | `git diff --check` đạt; chỉ cảnh báo chuẩn hóa LF/CRLF của Git trên Windows |

Kiểm tra tham chiếu P3 không cài giới hạn backtrack. Kỳ vọng ABORTED với
giới hạn 0 và DETECTED với giới hạn 1 còn chờ chạy trên P5, không tính là test
đã chạy. Cũng chưa kiểm chứng code P5/P6, branch fault, XOR/XNOR hoặc multiple faults.

## Build và xem PDF

Môi trường: Python 3.12; TeX Live 2026 (TinyTeX v2026.10), XeLaTeX,
Biber 2.22, biblatex, babel-vietnamese, TeX Gyre/Latin Modern; TikZ có
positioning, arrows.meta, shapes.geometric và calc theo main hiện tại.
Các main.tex trong bản sao giống byte với repo; không dùng wrapper của ZIP.

- Main + P3: **11 trang PDF = 2 bìa + 1 mục lục + 8 trang nội dung**;
  slide **10 trang = tiêu đề + 3 P1 + 3 P3 + 3 P4**.
- Bản sao thêm dữ liệu P2: **12 trang PDF = 2 bìa + 1 mục lục + 9 trang nội dung**;
  slide **13 trang**, có thêm 3 frame P2. Đây là phép thử tích hợp, không merge P2.
- Đã render và xem các trang P3, bảng c17, cây quyết định, hình c17 dùng chung,
  bibliography và ba frame; không thấy mất chữ hoặc chồng chữ trong phần P3.
  Chương P3 trải trên hai trang cùng nội dung của các phần lân cận,
  khoảng ngân sách 1,25 trang; P1 cần cân đối lại khi nhận P5/P6.
- `report/figures/common/c17.tex` P2 chỉ chứa includegraphics, không có float.
  Chỗ bọc figure của P3 đúng với snapshot này. Nếu P2 đổi wrapper thành float,
  P1 cần điều chỉnh chỗ input tương ứng để không lồng figure.

**Không tuyên bố build sạch mọi cảnh báo.** Các log cuối vẫn có:

1. Chương P4 `05_atpg_tuan_tu.tex` dòng 132–145: overfull hbox 59,60092 pt;
   dòng 146–157: 73,97719 pt. Các đoạn tên hàm/net dài tràn lề.
2. Chương P4 dòng 19: font mono đậm chưa khai báo trong khung, dùng font mono
   thường thay thế. Không phải undefined reference hoặc mất ký tự.
3. Bibliography mục FAN: overfull 0,16591 pt (khoảng 0,06 mm) dưới cấu hình
   chung tại `main.tex` dòng printbibliography. Nội dung đọc được khi render.
4. Babel cảnh báo thiếu mẫu ngắt từ tiếng Việt và một số underfull box.

Đề xuất P1/P4 ngắt tên hàm/net dài hoặc dùng `\nolinkurl`, bổ sung font mono
đậm nếu cần, cân chỉnh ngắt dòng bibliography. Không sửa các file đó trong PR P3.
Giáo trình Wang 2006 hiện được khai báo cả p1 và p3 nên bibliography có mục
lặp; P1 có thể thống nhất nguồn chung khi tích hợp, giữ tương thích key các phần.
Tổng số trang hiện tại chưa chứng minh bản cuối sẽ đạt 5–10 khi có P5/P6.

MiKTeX ban đầu không chạy trong sandbox, rồi thiếu font TeX Gyre; đã chuyển
sang TeX Live portable trên `D:\DFT_P3_check_20261005` sau khi C: hết chỗ.
Không đổi PATH hệ thống, không thay cài đặt MiKTeX. PDF/log/ảnh render nằm
ngoài repo, không stage. Chưa kiểm tra trên TeXPage/Overleaf của nhóm.

## Nguồn và bàn giao

Đã đọc trực tiếp giáo trình đính kèm, trang in 182–187 (PODEM/FAN),
256–257 (thư mục Goel/FAN); đối chiếu metadata và thuật toán. Đã truy cập bản
FAN từ trang tác giả, xem link trong `p3_ghi_chu.md`. DOI Goel không mở được
qua web nên không nhận đã đọc toàn văn bài Goel 1981. Giữ thông tin thư mục
đã đối chiếu giáo trình, không bịa số đo của bài báo.

P1 được xác định qua README phân công và tác giả các PR nhánh P1 (#2–#4):
`TuanNguyn-11`. GitHub đã xác thực tài khoản `NguyenVo-09` và API trả quyền
push vào repo; không cần người dùng gửi mật khẩu/token. Không gửi tin nhắn
hoặc email cho thành viên. PR là yêu cầu review phần P3; còn chờ P5/P6 và
review/tích hợp P1, không phải tuyên bố toàn đồ án hoàn thành.
