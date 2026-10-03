# Biên bản kiểm tra P2 — 03/10/2026

## Sản phẩm

- Chương 3: D-calculus, singular cover, PDCF/PDC, giao cube, frontier,
  implication, justification, backtrack, ví dụ và nhận xét.
- Bảng chuẩn tám cổng, 160 ô tại `tests/data/five_valued_tables.md`.
- Trace đầy đủ và mã giả ở `notes/p2_ghi_chu.md`.
- Lưu đồ TikZ, bảng trạng thái cuối và ba frame P2.
- Hình `C:\DFT\mach_c17.jpg` dùng lại qua `report/figures/common/c17.tex`.
  Wrapper chèn JPG thay vì tạo lại hình TikZ theo yêu cầu dùng hình sẵn có.
  Hình đúng kết nối và thể hiện cube sau tổng quát hóa, không phải cube bước 4.
- Bibliography: bài gốc Roth 1966; metadata bản đầu Bushnell--Agrawal 2000.
  Chưa có toàn văn sách Bushnell--Agrawal để nhận đã đối chiếu trang.

## Tái lập

Từ gốc repo:

```powershell
python -B notes/p2_kiem_chung.py
python -B scripts/check_p1_examples.py
# Locale C tránh cảnh báo Perl/Biber về C.UTF-8 trên Windows.
$env:LC_ALL = 'C'
$env:LC_CTYPE = 'C'
$env:LANG = 'C'
& .\scripts\build_documents.ps1
git diff --check
```

## Kết quả thực hiện

| Kiểm tra | Kết quả |
|---|---|
| Bảng logic | 160/160 ô khớp oracle độc lập duyệt các cách điền nhị phân |
| Trace | Bốn trạng thái trung gian, D-frontier và J-frontier khớp |
| Cube chạy tay | 4/4 cách điền `(X,1,0,0,X)` phát hiện 11/SA0 tại 22 |
| Cube tổng quát | 8/8 cách điền `(X,1,0,X,X)` phát hiện lỗi tại 22 |
| Đáp ứng PO ghi trong tài liệu | Cả bốn mẫu cube chạy tay có PO tốt (1,1), lỗi (0,0) |
| Ví dụ P1 | Script hiện có vẫn PASS toàn bộ |
| Build | XeLaTeX → Biber → XeLaTeX hai lượt; script trả mã 0 |
| Tham chiếu/bố cục | Không undefined reference/citation, missing character hoặc overfull box trong log cuối |
| Diff | `git diff --check` đạt; chỉ cảnh báo chuyển LF/CRLF |
| Xem PDF | Kiểm tra hình, bảng, lưu đồ, tiếng Việt và ba frame P2 |

Báo cáo tích hợp xem trước có **8 trang PDF: 2 bìa, 1 mục lục, 5 trang nội dung**;
slide có **7 trang: tiêu đề, 3 P1, 3 P2**. Chương 3 hiện chiếm khoảng
1,5 trang kể cả hình và lưu đồ; cần P1 cân đối ngân sách đề xuất một trang
khi nhận P3–P6. Không kết luận gói nhóm đã hoàn thành hoặc đạt giới hạn trang
sau khi bổ sung tất cả chương. Bản dựng dùng TeX Live cục bộ, chưa thử TeXPage.
Còn cảnh báo Babel thiếu mẫu ngắt từ tiếng Việt và underfull ở bảng thuật ngữ
P1; không sửa cấu hình hoặc nội dung P1 để xử lý chúng.

## Phạm vi và bàn giao

Không thay đổi chương, code, slide riêng của P1/P3/P4/P5/P6 hoặc hai main.tex.
Không thay branch, commit, push, merge hoặc phát hành PDF cuối của nhóm.
Script kiểm chứng nằm trong notes P2, không thay test_logic/test_podem của P5.
PDF xem trước là `report/main.pdf` và `slides/main.pdf`, được Git bỏ qua.

Còn bước review/tích hợp của nhóm: P1 review chương/slide và việc dùng JPG;
P3 dùng số liệu **4 lần chọn cube, 0 backtrack** theo đơn vị đã công bố;
P5 đối chiếu bảng chuẩn; P6 xác nhận lại pattern bằng simulator chung khi có.
Không nhận đã trao đổi hoặc gửi thông báo cho các thành viên.
