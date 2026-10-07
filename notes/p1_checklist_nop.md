# Checklist gói nộp P1 — chuẩn bị 06/10/2026

Hạn chính thức **08/10/2026**. Giờ đóng cổng, kênh và định dạng nộp **chưa xác minh**. Agent chỉ chuẩn bị gói và bằng chứng; các mục “Người thực hiện” chỉ được đánh dấu khi người đó tự xác nhận.

## A. Gói nộp (agent đã chuẩn bị, chờ P1 duyệt)

| Thành phần | Đường dẫn | Trạng thái 06/10/2026 |
|---|---|---|
| PDF báo cáo | `report/bao_cao_DFT_ATPG.pdf` | Build PASS; 14 trang (2 bìa + mục lục i + danh mục viết tắt ii + 10 trang đánh số từ Chương 1, ~9 trang nội dung); không bị Git ignore |
| PDF slide | `slides/slides_DFT_ATPG.pdf` | Build PASS; 19 trang (bìa + 3 frame × 6 người); không bị Git ignore |
| Source báo cáo/slide | `report/`, `slides/` | 8 chương; bản chi tiết Ch.5–7 trước rút gọn ở `notes/p1_chi_tiet/` |
| Code + test | `src/atpg/`, `tests/` | pytest 350 passed (Python 3.12.15), sau PR #14, #15, nhánh P5 và vá đầu vào lõi PODEM |
| README/demo | `README.md`, `demo.md` | Lệnh tái lập: `python scripts/p1_verify_release.py` |
| Bằng chứng kết quả | `results/p1_*.md` | c17, full scan, trải khung k=1..3, log kiểm chứng |
| Lời giải/kịch bản video Hình 4.5 | `notes/p1_video_loi_giai.md` | Có lời giải, lời thoại; P1 đã quay video (07/10/2026), file `notes/Fig4.5.mp4` được Git bỏ qua, nộp riêng |

Lưu ý: PDF phải được build lại trên đúng commit phát hành (sau khi merge P6 và P1), không dùng `main.pdf` trung gian.

## B. Việc con người phải làm (agent không tự xác nhận)

- [x] Merge PR P6 #11 vào `main` (agent, theo ủy quyền của P1, 06/10/2026; `4abf964`).
- [ ] P6 đọc lại phần P1 rút gọn Chương 7/slide P6 (bản gốc ở `notes/p1_chi_tiet/07_ket_qua.tex`).
- [ ] P4, P5 xem lại bản rút gọn Chương 5, 6 (bản gốc ở `notes/p1_chi_tiet/`).
- [x] Merge PR P1 #12 (agent, theo ủy quyền; `99bd39a`). Cây nguồn `main` trùng commit đã kiểm chứng `b8f9639`; chạy lại pytest 332 passed và checker P1/P2/P3 trên `main`.
- [ ] P1 xác nhận bìa, tên/MSSV thành viên, GVHD, tháng/năm.
- [ ] P1 xác nhận giờ đóng cổng, kênh nộp, định dạng file/video ngày 08/10/2026; có chiếu video trong 20 phút hay chỉ nộp kèm.
- [x] P1 quay video Hình 4.5 (P1 xác nhận 07/10/2026; file ngoài Git).
- [ ] P1 xem lại tiếng/hình và đổi định dạng nếu kênh nộp yêu cầu.
- [ ] Cả nhóm diễn tập 20 phút (không gồm hỏi đáp), thử demo CLI trên máy trình chiếu, chuẩn bị bản dự phòng (ảnh/kết quả `results/`).
- [x] Tạo tag `v1.0` (`99bd39a`) và [release](https://github.com/TuanNguyn-11/dft-atpg/releases/tag/v1.0) kèm hai PDF (agent, theo ủy quyền, 06/10/2026). Nếu bìa/nội dung phải sửa: phát hành `v1.0.1`.
- [x] Merge PR P2 #14 và P4 #15 (agent, theo ủy quyền); sửa dàn trang Chương 5, build lại PDF, phát hành `v1.0.1`.
- [x] Sửa bìa thành “Bộ môn Kỹ thuật Máy tính” theo yêu cầu P1; thụt lề dòng đầu mọi đoạn; phát hành `v1.0.2`.
- [x] Dàn lại Hình 3.1 (lưu đồ D-algorithm) cho các khối không chồng nhau; phát hành `v1.0.3`.
- [x] Tách danh mục viết tắt ra trang riêng (trang ii), nội dung đánh số từ Chương 1; phát hành `v1.0.4`.
- [x] Merge nhánh P5 `5b461af` (exporter trace, test); P1 biên tập Chương 6 cho vừa 10 trang, gộp cite trùng, sửa frame slide P5 tràn; bản gốc ở `notes/p1_chi_tiet/06_cai_dat_podem_p5_5b461af.tex`; phát hành `v1.0.5`.
- [x] Vá lõi `podem.podem`: từ chối net/nhánh không thuộc mạch và `max_backtracks` âm bằng `ValueError` (feedback P6-01), thêm 8 test hồi quy; sửa chữ cũ ở `demo.md`, `notes/p6_ghi_chu.md`; phát hành `v1.0.6`.
- [x] PR P3 #23 được P3 tự merge (06/10/2026); P1 kiểm lại trên `d958a69`: pytest 350 passed, checker P1/P2/P3 (kể cả `notes/p3_doi_chieu_code.py`)/P4 PASS, giới hạn 0/1 → ABORTED/DETECTED đúng; build lại PDF, phát hành `v1.0.7`.
- [x] Theo yêu cầu P1 (07/10/2026): bỏ đoạn phân công và mọi nhãn P1–P6, đường dẫn file khỏi báo cáo/slide, viết lại câu cho tự nhiên; mục `\section` nhỏ hơn tiêu đề chương; slide bìa có tên/MSSV 6 thành viên, trường, bộ môn, GVHD; slide demo mô tả kịch bản thay vì câu lệnh. Phát hành `v1.0.8`.
- [x] Theo yêu cầu P1 (07/10/2026): sửa “Thúy Hằng” trên bìa; PODEM trong danh mục viết tắt là “Thuật toán sinh mẫu kiểm tra tự động định hướng theo đường đi”; tiêu đề “Xử lý cổng XOR/XNOR trong PODEM”; bỏ xuống dòng sau các tiêu đề đậm; mục 7.4 “Mạch tuần tự”; tài liệu tham khảo trang riêng; slide bìa theo mẫu video, bỏ dòng nguồn, bỏ hỏi đáp, slide cuối là lời cảm ơn. Phát hành `v1.0.9` — **bản dùng để nộp**.
- [ ] Người trình bày demo dùng câu lệnh trong `demo.md` (slide không còn ghi lệnh).
- [ ] Báo P5 về thay đổi kiểm tra đầu vào trong `src/atpg/podem.py`.
- [ ] P5 đọc lại bản biên tập Chương 6.
- [ ] Nộp bài theo kênh giảng viên và lưu bằng chứng (ảnh xác nhận nộp, link release).

## C. Nội dung PR đề xuất (`p1-nguyen-ly` → `main`)

**Tiêu đề:** `[P1] chốt nội dung báo cáo, sửa build, thống nhất tên PDF và cập nhật trạng thái`

**Vấn đề**
- README/kế hoạch/kết luận còn ghi P2–P6 là khung, CLI chưa chạy; mâu thuẫn về video.
- Build FAIL: font mono đậm chưa định nghĩa, 3 overfull hbox (Ch.5 và bibliography).
- `.gitignore` mở ngoại lệ `slide_DFT_ATPG.pdf` trong khi P6 dùng `slides_DFT_ATPG.pdf`.
- Báo cáo vượt ngân sách 5–10 trang nội dung; mục tài liệu Wang 2006/Goel 1981 trùng.

**Thay đổi**
- Viết lại Chương 8 bằng số liệu thực đo; rút gọn Ch.5–7 (bản chi tiết lưu `notes/p1_chi_tiet/`); thống nhất ký hiệu `D'`; ghi rõ nguồn PODEM + vét cạn chuỗi bổ sung và pseudo-PO D của full scan.
- Font TeX Gyre Cursor đủ kiểu; ngắt dòng API Ch.5; `emergencystretch` cho bibliography; build script xuất PDF tên cuối.
- `.gitignore`, README, notes dùng `slides/slides_DFT_ATPG.pdf`.
- Cập nhật README, `notes/p1_ke_hoach.md`, `notes/p1_review.md` (ghi chú cũ gắn nhãn lịch sử); thêm checklist này và `scripts/p1_verify_release.py`.
- Slide P5: số test tích hợp 332; slide P4/P6: nêu đúng nguồn kết quả. Checker P3 chấp nhận khóa cite chung `p1_wang2006`.

**Kiểm chứng**
- `python scripts/p1_verify_release.py`: tất cả PASS, pytest 332 passed, full scan 18/18 qua API thật.
- `scripts/build_documents.ps1`: PASS; report 13 trang, slide 19 trang.
- `git check-ignore report/bao_cao_DFT_ATPG.pdf slides/slides_DFT_ATPG.pdf`: exit 1.

**Giới hạn**
- Base `main` `4abf964` (sau PR P6 #11).
- Chưa build trên TeXPage; tại thời điểm mở PR, video, xác nhận kênh nộp, diễn tập và tag `v1.0` chưa thực hiện (tag đã tạo sau khi merge).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
