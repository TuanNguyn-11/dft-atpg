# Biên bản kiểm tra P1

## Kiểm tra tích hợp — 06/10/2026 (hiện tại)

Base `1b3730008b3505af62dcca619a2dd2b528d87099` (head PR P6 #11; sau merge là `main` `4abf964`, cùng cây nguồn) + thay đổi P1. Python 3.12.15, pytest 9.1.1, TinyTeX (TeX Live 2026).

| Hạng mục | Lệnh | Kết quả |
|---|---|---|
| Test + kiểm chứng P2/P3/P4 + demo CLI | `python scripts/p1_verify_release.py` | Tất cả PASS; pytest 332 passed (`results/p1_verification.md`) |
| c17 | `--all`, `--all --no-collapse` | 22/22 đại diện, 34/34 gốc; nén 22→6, 34→7; tập nén phủ 34/34 |
| Full scan qua API thật | trong script trên | 18/18 lỗi stem, khớp oracle P4 (`results/p1_full_scan.md`) |
| Trải khung, trạng thái đầu chưa biết | `--unroll k --all` | Bảo đảm 1/18, 13/18, 18/18 tại k=1,2,3; nguồn PODEM/vét cạn chuỗi: 17/1, 8/10, 3/15 |
| Build | `scripts/build_documents.ps1 -TexBin ...` | PASS; report 13 trang, slide 19 trang; không overfull/undefined/missing character |
| Ignore | `git check-ignore report/bao_cao_DFT_ATPG.pdf slides/slides_DFT_ATPG.pdf` | Không in gì, exit 1 |

Sửa trong đợt này: font mono có đủ bold/italic (TeX Gyre Cursor); ngắt dòng API ở Chương 5; `emergencystretch` cho bibliography; gộp các mục Wang 2006/Goel 1981 trùng về `p1_wang2006`/`p3_goel1981` (checker P3 được nới để chấp nhận khóa chung P1); tên slide cuối thống nhất `slides_DFT_ATPG.pdf`. Còn cảnh báo Babel không có mẫu ngắt từ tiếng Việt và 1 underfull hbox ở bảng viết tắt; không ảnh hưởng hiển thị.

Giới hạn: chưa chạy trên TeXPage; PR P6 #11 đã merge sau khi P1 chạy pytest trên head `1b37300` (332 passed); chưa review độc lập phần rút gọn Chương 5–7 bởi P4/P5/P6.

### Bổ sung 06/10/2026 — PR P2 #14, P4 #15

- Thử merge cả hai trên `586218e`: pytest 334 passed; `notes/p2_kiem_chung.py --integrated` PASS (160/160 ô, X100X 4/4, X10XX 8/8); `scripts/p4_integrated_experiment.py` PODEM 18/18, bộ mẫu phủ 18/18; nguồn chuỗi k=1,2,3 là 0/1, 3/10, 3/15, khớp Chương 7.
- Build FAIL do đoạn mới ở Chương 5 (2 overfull hbox 14,9pt và 2,2pt, đường dẫn dài). Đã merge (`cb2be0e`) rồi sửa dàn trang, giữ nguyên nội dung; build PASS, report 13 trang, slide 19 trang. Cập nhật số test 334 ở Chương 6 và slide P5.

---

## Lịch sử — kiểm tra P1 ngày 03/10/2026 (trước tích hợp)

## Phạm vi

- Đọc prompt.md, P1.md, kế hoạch đã cập nhật và rubric do P1 cung cấp. Giữ hạn 08/10, mục tiêu nội bộ 05/10 và giới hạn báo cáo 5–10 trang; không áp dụng dự kiến Chương 2 dài 8 trang trong phân công cũ.
- Đối chiếu từng file trong `dft-atpg-report-texpage.zip`: giống nguồn `report/` tại commit `eec1163` sau khi chuẩn hóa xuống dòng; không có chỉnh sửa riêng cần nhập.
- Khi kiểm tra, GitHub chỉ có PR mở #4, từ `p1-nguyen-ly` vào `main`; chưa có PR P2–P6. Main và nhánh P1 chưa chứa lõi PODEM, netlist hay thực nghiệm hoàn chỉnh.
- Phần P1 được bổ sung: Chương 1/2, kết luận theo thực trạng, sơ đồ TikZ, ba slide, thuật ngữ/ghi chú tự học, lời giải video và script kiểm chứng. Khung slide chỉ được chỉnh font/nhóm để tích hợp; P6 vẫn phụ trách ghép phần còn lại.

## Kiểm tra kỹ thuật

Chạy từ gốc repo:

```text
python scripts/check_p1_examples.py
powershell -ExecutionPolicy Bypass -File scripts/build_documents.ps1 -TexBin <thu-muc-bin-TeX-Live>
git diff --check
```

Kết quả:

| Hạng mục | Bằng chứng |
|---|---|
| Collapsing c17 | 1/SA0 và 10/SA1 cùng đáp ứng hai PO trên 32/32 vector |
| Mẫu lỗi 11/SA0 | Cả tám cách điền `(X,1,0,X,X)` đều tạo khác biệt tại PO 22 |
| SCOAP | Tính CC thuận/CO ngược cho 11 net; trùng bảng Chương 2 và ghi chú |
| Hình 4.5 | Duyệt 8/8 vector, chỉ 011 và 110 phát hiện stem y/SA0 |
| Nguồn | Đọc trực tiếp giáo trình: trang 12–14 (stuck-at/collapsing), 41–42 (SCOAP), 166–167 và ảnh hình gốc (video); lịch sử thuật toán ở trang 27, 36, 186 |
| Báo cáo | XeLaTeX + Biber + hai lượt XeLaTeX thành công trên TeX Live 2026/Biber 2.22 |
| Slide | XeLaTeX nhiều lượt thành công; tiêu đề và ba frame P1 |
| Tham chiếu | Không còn undefined reference/citation hoặc dấu `??` trong PDF |
| Bố cục | Không có overfull box hoặc missing character; xem ảnh PDF kiểm tra bìa, mục lục, bảng, sơ đồ và slide |
| Diff | `git diff --check` đạt |

Báo cáo hiện có **6 trang PDF: hai bìa + một mục lục + ba trang nội dung** (kể cả viết tắt và tài liệu tham khảo). Slide có **4 trang**. Đây là bản xem trước phần P1, **chưa đạt đầu ra báo cáo nhóm 5–10 trang nội dung**, vì Chương 3–7 còn khung. Không dùng số trang hiện tại để khẳng định đã đạt rubric cuối.

Đã sửa lỗi font trên TeX Live portable bằng cách nạp font theo tên file và khai báo ánh xạ ngôn ngữ BibLaTeX. Còn cảnh báo Babel không có mẫu ngắt từ tiếng Việt và một underfull hbox ở ô thuật ngữ SCOAP; đã xem bố cục, không mất chữ hoặc tràn trang. Biber có cảnh báo locale hệ thống Windows nhưng trả mã 0 và tạo bibliography đúng. Chưa chạy trên tài khoản TeXPage/Overleaf của nhóm, nên không nhận đã kiểm tra môi trường đó.

## Kết luận review PR #4

Đạt yêu cầu để tích hợp **phần nội dung và hạ tầng P1 hiện có** sau khi đưa các sửa đổi đã kiểm tra lên nhánh. PR không phải bản phát hành cuối của cả nhóm. Bằng chứng kiểm tra nằm ở script tái lập và biên bản này; không có CI hoặc review độc lập của thành viên khác tại thời điểm kiểm tra. Trạng thái merge thực tế xem [PR #4](https://github.com/TuanNguyn-11/dft-atpg/pull/4).

## Việc còn phụ thuộc đầu vào

- P1 tự quay/nộp video 2–3 phút; lời giải và lời dẫn ở `p1_video_loi_giai.md`.
- Chờ PR chương, code, netlist, golden trace, bảng logic và slide P2–P6; review theo phân công và chạy kiểm thử tích hợp khi nhận được.
- Khi có thực nghiệm, thay đoạn trạng thái trong Chương 8 bằng kết quả thật, đối chiếu coverage và trace, kiểm tra lại tổng 5–10 trang và diễn tập 20 phút.
- Chỉ xuất/commit `bao_cao_DFT_ATPG.pdf`, `slide_DFT_ATPG.pdf` (nay đổi thành `slides_DFT_ATPG.pdf`) và gắn `v1.0` sau khi gói nhóm hoàn chỉnh. Chưa thực hiện nộp bài hoặc mời thành viên/gửi thông báo thay P1.
