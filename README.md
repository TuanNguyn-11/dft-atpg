# DFT — Automatic Test Pattern Generation

Đồ án: **Automatic Test Pattern Generation Algorithms for Combinational and Sequential Circuits**.

Repo chung của nhóm gồm báo cáo LaTeX, slide và chương trình minh họa PODEM bằng Python.

## Trạng thái

**Trạng thái hiện tại (P1, 06/10/2026):** PR P6 #11 và P1 #12 đã merge; đã phát hành [release `v1.0`](https://github.com/TuanNguyn-11/dft-atpg/releases/tag/v1.0) tại `99bd39a`. Sau đó merge PR P2 #14 và P4 #15 (bằng chứng tích hợp, cập nhật Chương 5/slide P4); PDF build lại, phát hành `v1.0.1`; sau đó sửa bìa (Bộ môn Kỹ thuật Máy tính) và thụt lề đoạn, phát hành `v1.0.2`; sau đó dàn lại Hình 3.1, phát hành `v1.0.3`; sau đó tách danh mục viết tắt ra trang riêng (số La Mã), Chương 1 bắt đầu trang 1, phát hành `v1.0.4`; sau đó merge nhánh P5 (exporter trace, cập nhật Chương 6/slide P5, P1 biên tập cho vừa trang), phát hành `v1.0.5`; sau đó vá kiểm tra đầu vào lõi PODEM, phát hành `v1.0.6`; sau đó PR P3 #23 (đối chiếu trace P5/P6, cập nhật Chương 4/slide P3) được merge, P1 build lại PDF, phát hành `v1.0.7`; sau đó bỏ phân công Px và đường dẫn file trong báo cáo/slide, chỉnh cỡ chữ mục, thêm thành viên vào slide, phát hành `v1.0.8`; sau đó sửa tên thành viên trên bìa, tiêu đề mục, tài liệu tham khảo trang riêng, slide bìa theo mẫu video, bỏ dòng nguồn và hỏi đáp, phát hành `v1.0.9` (báo cáo nộp); `v1.0.10` chỉnh trang bìa slide và thêm lời thoại thuyết trình (`notes/thoai_thuyet_trinh.md`); `v1.0.11` thêm slide sơ đồ c17; `v1.0.12` thêm slide bảng logic năm giá trị 8 cổng (22 slide); `v1.0.13` bỏ câu trỏ “slide sau”; `v1.0.14` slide 11 thêm mạch c17 nhỏ cạnh bảng; `v1.0.15` thêm D-algorithm và so sánh với PODEM (`python -m atpg.compare`, PR #33); `v1.0.16` thêm slide bảng so sánh D-algorithm/PODEM trước slide cảm ơn (23 slide) — bản dùng để nộp.

- Code P2–P6 đã tích hợp; CLI `python -m atpg.run` chạy được. `pytest` đạt **364 passed** trên Python 3.12.15/pytest 9.1.1 (mốc review trên main: 302; tăng do test tích hợp P6, P4, exporter trace P5 và test kiểm tra đầu vào lõi PODEM, công cụ so sánh D-algorithm/PODEM của P6).
- Số liệu thực đo: c17 PODEM 34/34 lỗi gốc, 22/22 đại diện sau gộp; nén 34→7 hoặc 22→6 pattern. Full scan 18/18 lỗi stem qua API thật. Trải khung từ trạng thái đầu chưa biết: 1/18, 13/18, 18/18 tại k=1,2,3 (PODEM kết hợp vét cạn chuỗi bổ sung, không phải PODEM thuần).
- Báo cáo 8 chương đã biên tập về 14 trang PDF (2 bìa + mục lục trang i + danh mục viết tắt trang ii + 10 trang đánh số từ Chương 1; nội dung ~9 trang, tài liệu tham khảo trang 9–10). Slide 19 trang: bìa + 18 frame của 6 người. `scripts/build_documents.ps1` PASS cục bộ.
- Chương 7/slide P6 đã merge vào `main` (PR #11). P1 rút gọn Chương 5–7 để vừa số trang; bản chi tiết gốc ở `notes/p1_chi_tiet/`, P4/P5/P6 nên đọc lại.
- **Còn thiếu:** P1 duyệt PDF cuối, video Hình 4.5 (P1 đã quay ngày 07/10/2026; file giữ ngoài Git vì có hình trích giáo trình), diễn tập 20 phút, nộp bài. Nếu sửa tiếp nội dung, phát hành bản vá mới (`v1.0.10`…).

Tái lập toàn bộ kiểm chứng P1 (test, kiểm chứng P2/P3/P4, demo CLI, full scan qua API thật):

```text
python scripts/p1_verify_release.py
```

Kết quả ghi vào `results/p1_verification.md`, `results/p1_full_scan.md`, `results/p1_c17_*.md`, `results/p1_seq_k*.md`. Kiểm chứng riêng ví dụ P1 (collapsing, SCOAP, Hình 4.5): `python scripts/check_p1_examples.py`. Xem [kiến thức và thuật ngữ P1](notes/p1_kien_thuc.md), [lời giải video](notes/p1_video_loi_giai.md), [biên bản review](notes/p1_review.md) và [checklist nộp](notes/p1_checklist_nop.md).

> Lịch sử (03/10/2026, trước tích hợp): README từng ghi P2–P6 là khung, CLI chưa chạy được. Nội dung đó không còn đúng.

## Mục tiêu và phạm vi

- Trình bày nguyên lý ATPG, D-algorithm, PODEM và ATPG cho mạch tuần tự.
- Cài đặt PODEM bằng Python, minh họa từng bước trên ISCAS'85 c17.
- Dùng lỗi chung `11/SA0` để đối chiếu trace chạy tay và trace code.
- Minh họa full scan và trải khung thời gian trên mạch tuần tự nhỏ.
- Chỉ dùng công cụ miễn phí; code dùng thư viện chuẩn Python, kiểm thử bằng pytest.

## Thành viên và phân công

**Nhóm 4 — Trường Đại học Công nghệ Kỹ thuật Tp.Hồ Chí Minh, Khoa Điện-Điện tử.**

Môn: Kỹ thuật DFT và kiểm thử. Giảng viên: Nguyễn Văn Thành Lộc.

| Vai trò | Họ tên / MSSV | Công việc | Branch |
|---|---|---|---|
| P1 | Phan Ngọc Tuấn Nguyên — 23119178 | Chương 1, 2, 8; repo; khung LaTeX; review và tích hợp báo cáo | `p1-nguyen-ly` |
| P2 | Hà Quang Huy — 23119147 | Chương 3; D-algorithm; bảng logic 5 giá trị; hình c17 dùng chung | `p2-d-algorithm` |
| P3 | Võ Trung Nguyên — 23119180 | Chương 4; PODEM lý thuyết; golden trace | `p3-podem-ly-thuyet` |
| P4 | Phạm Trọng An Nam — 23119174 | Chương 5; mạch tuần tự; full scan và unroll | `p4-tuan-tu` |
| P5 | Nguyễn Thị Thúy Hằng — 23119142 | Chương 6; logic 5 giá trị và lõi PODEM | `p5-podem-code` |
| P6 | Nguyễn Thị Thanh Tuyền — 23119222 | Chương 7; đọc mạch, mô phỏng lỗi, CLI, kiểm chứng; ghép slide | `p6-mo-phong-ket-qua` |

## Cấu trúc repo

```text
circuits/                 Netlist .bench (P6: c17; P4: mạch tuần tự)
src/atpg/                 Code Python của P4, P5, P6
tests/data/               Dữ liệu kiểm tra chung của P2; tests/ chứa kiểm thử
results/                  Trace, pattern và kết quả kiểm chứng
notes/                    Ghi chú học tập pX_ghi_chu.md
report/
  main.tex                File gốc báo cáo do P1 quản lý
  cover.tex               Trang bìa theo mẫu P1 cung cấp, không hiển thị vai trò
  chapters/               Tám chương theo phân công
  figures/common/         Hình c17 dùng chung do P2 cung cấp
  figures/p1/ ... p6/      Hình riêng của từng thành viên
  bib/p1.bib ... p6.bib    Tài liệu tham khảo riêng
slides/
  main.tex                Khung Beamer; P6 phụ trách bản cuối
  parts/p1.tex ... p6.tex  Mỗi người viết 2–3 frame
```

Các thư mục trống có `.gitkeep` để Git lưu được cấu trúc. Bản nháp chi tiết Chương 5–7 trước biên tập rút gọn được lưu trong `notes/p1_chi_tiet/`.

Trang bìa nằm trong `report/cover.tex`; logo `report/figures/p1/logo_truong.png` được trích từ PDF mẫu `Final_Project_Blockchain-1.pdf` do P1 cung cấp. Khi cập nhật lên TeXPage, cần đưa cả file bìa và logo cùng với `main.tex`.

## Biên dịch báo cáo

Cần TeX Live có XeLaTeX, Biber, hỗ trợ tiếng Việt và các font TeX Gyre, Latin Modern; hoặc dùng TeXPage (nền tảng nhóm đã chọn). Không dùng pdfLaTeX cho khung này.

### Trên TeXPage

1. Tải ZIP của branch cần dùng và nhập nguồn vào project TeXPage, giữ cấu trúc thư mục.
2. Cấu hình file chính là `report/main.tex`, trình biên dịch **XeLaTeX**; bibliography dùng **Biber** theo cấu hình trong nguồn.
3. Biên dịch đủ XeLaTeX → Biber → XeLaTeX → XeLaTeX và kiểm tra log; `bib/p1.bib` đã có giáo trình được trích dẫn.
4. Để biên dịch slide, chọn `slides/main.tex` làm file chính.
5. Sau mỗi đợt chỉnh sửa, tải nguồn về, đối chiếu thay đổi và commit vào branch của mình. GitHub là nơi lưu bản nguồn chung.

Tài liệu chính thức: [bibliography với biblatex và Biber trên TeXPage](https://www.texpage.com/docs/en/learning/chapter-4/). Chưa xác nhận biên dịch thành công trên project TeXPage của nhóm.

### Trên máy cá nhân

Có thể biên dịch và kiểm tra cả báo cáo/slide bằng PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_documents.ps1
# Nếu TeX Live portable chưa có trong PATH:
powershell -ExecutionPolicy Bypass -File scripts/build_documents.ps1 -TexBin 'C:\duong-dan\TinyTeX\bin\windows'
```

Bản TeX Live tối giản cần gói `babel-vietnamese`, `tex-gyre`, `lm`, `titlesec`, `pgf`, `biblatex`, `biber` và `beamer`. Font được nạp theo file đi kèm TeX Live nên không cần cài font vào Windows.

Từ thư mục gốc repo, chạy từng lệnh:

```text
cd report
xelatex -interaction=nonstopmode -halt-on-error main.tex
biber main
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Kết quả là `report/main.pdf`. Khi các file `.bib` còn trống và chưa có trích dẫn, có thể bỏ qua bước Biber; chạy lại đủ chu trình sau khi thêm nguồn và `\cite`.

Slide: mở terminal ở thư mục gốc repo và chạy:

```text
cd slides
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Kết quả là `slides/main.pdf` (bìa + 18 frame P1–P6).

PDF trung gian (`main.pdf`) được bỏ qua bởi Git. Script build tự sao chép thành `report/bao_cao_DFT_ATPG.pdf` và `slides/slides_DFT_ATPG.pdf` (tên số nhiều, thống nhất với P6); chỉ hai tên này được phép commit. Kiểm tra: `git check-ignore report/bao_cao_DFT_ATPG.pdf slides/slides_DFT_ATPG.pdf` phải không in gì (exit 1).

## Chạy code và kiểm thử

Yêu cầu **Python ≥ 3.10**. Kiểm tra bằng `python --version` và chọn đúng interpreter trước khi thực hiện. Các lệnh dưới đây chạy từ thư mục gốc repo.

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install pytest
$env:PYTHONPATH = (Join-Path (Get-Location) 'src')
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --fault 11 0 --trace
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --all
.\.venv\Scripts\python.exe -m atpg.run circuits/seq_example.bench --unroll 2 --all
.\.venv\Scripts\python.exe -m pytest
```

Linux/macOS (Bash):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest
export PYTHONPATH="$PWD/src"
python -m atpg.run circuits/c17.bench --fault 11 0 --trace
python -m atpg.run circuits/c17.bench --all
python -m atpg.run circuits/seq_example.bench --unroll 2 --all
python -m pytest
```

## Quy ước tích hợp

- Mỗi người sửa file thuộc phần mình; cần sửa phần khác thì trao đổi với chủ sở hữu hoặc P1.
- Giữ giao diện code và cột trace đúng mục 8–9 của `prompt.md` đã phát cho nhóm. Không tự ý đổi hợp đồng P4/P5/P6.
- Mỗi chương bắt đầu bằng `\chapter{...}`; không khai báo gói hoặc lệnh dùng chung trong chương. Báo P1 nếu cần bổ sung gói.
- Nhãn có tiền tố phần, ví dụ `sec:p3-backtrace`, `fig:p2-dcube`, `tab:p5-trace`.
- Tài liệu trong `report/bib/pX.bib`, khóa dạng `p3_goel1981`; chỉ ghi nguồn đã xác minh.
- Hình riêng trong `report/figures/pX/`; hình c17 dùng chung là `report/figures/common/c17.tex` do P2 tạo.
- Pattern có `X` được điền bằng 0 trước khi mô phỏng lỗi nhị phân; ghi rõ trong báo cáo.
- Nội dung tiếng Việt; tên biến code bằng tiếng Anh, comment bằng tiếng Việt.

## Quy trình GitHub

P1 khởi tạo `main` bằng README đầu tiên. Các thay đổi tiếp theo đi qua branch và PR.

Ví dụ cho P2, sau khi khung đã được merge vào `main`:

```text
git clone https://github.com/TuanNguyn-11/dft-atpg.git
cd dft-atpg
git switch main
git pull origin main
git switch -c p2-d-algorithm
```

Trước khi mở PR, commit các file của mình rồi cập nhật `main` vào branch đang làm:

```text
git add report/chapters/03_d_algorithm.tex
git commit -m "[P2] thêm bản nháp D-algorithm"
git pull origin main
git push -u origin p2-d-algorithm
```

Giải quyết xung đột nếu có trước khi push. Mở PR vào `main`, ghi nội dung và cách kiểm tra. Báo cáo/slide do P1 review; code P5 và P6 review chéo, code P4 do P5 review. Không push trực tiếp vào `main`; chỉ P1 merge PR.

## Yêu cầu nộp đã cập nhật

Theo thông tin P1 xác nhận và `Thang_diem_DFT_public.pdf` do giảng viên cung cấp:

- Báo cáo **5–10 trang nội dung**, không tính bìa và mục lục theo xác nhận của P1. Mục tiêu 8–9 trang kể cả tài liệu tham khảo và danh mục viết tắt để chừa dư địa.
- Khung vẫn giữ tám file chương và lệnh `\chapter`, nhưng dùng `\input` và tiêu đề liên tục, không ép mỗi chương sang trang mới. Bỏ danh mục hình/bảng riêng để giảm phần đầu.
- Thuyết trình và demo tổng cộng **20 phút, không bao gồm hỏi đáp**. Video giải thích dài khoảng **2–3 phút**.
- **Bắt buộc chọn 01 ví dụ/bài tập từ sách hoặc tài liệu môn học, trình bày đề bài, cách giải và kết luận; quay video giải thích để nộp kèm.** Đã chốt Hình 4.5, mục 4.3, trang in 166–167, tìm vector phát hiện y/SA0; P1 phụ trách video 2–3 phút. Đã có [lời giải và lời dẫn](notes/p1_video_loi_giai.md); P1 đã quay video (07/10/2026); file không đưa lên repo công khai vì có hình trích giáo trình.
- Giáo trình chính: *VLSI Test Principles and Architectures: Design for Testability*, Laung-Terng Wang, Cheng-Wen Wu, Xiaoqing Wen (biên tập), Morgan Kaufmann, 2006. Thông tin được kiểm tra trực tiếp từ PDF do P1 cung cấp; mục BibLaTeX ở `report/bib/p1.bib`.
- Chưa xác nhận tiến độ làm riêng của P2–P6 ngoài repo. Bản ZIP TeXPage do P1 cung cấp trùng nội dung nguồn báo cáo trước đợt cập nhật này; chưa có bằng chứng build trên TeXPage. Kiểm tra build cục bộ được ghi trong biên bản review.
- Hạn nộp chính thức: **08/10/2026**; giờ đóng cổng, kênh và định dạng nộp **chưa xác minh**. Mục tiêu nội bộ cũ 05/10/2026 đã trễ; phần còn lại dồn vào 06–07/10.
- Kế hoạch này thay thế mốc 10/10 và dự kiến số trang dài trong bộ hướng dẫn ban đầu. Chi tiết phân bổ trang, rubric và thời gian: [kế hoạch P1](notes/p1_ke_hoach.md).

## Các mốc chung (kế hoạch 01/10/2026, giữ làm lịch sử)

| Ngày | Đầu ra cần đạt |
|---|---|
| 01/10/2026 | Repo và khung; kiểm tra TeXPage; xác nhận giao diện P5/P6, tài liệu môn học và bài tập video |
| 02/10/2026 | Netlist c17 đọc được, bảng logic, golden trace, mạch tuần tự; học và viết ghi chú song song |
| 03/10/2026 | PR bản nháp các phần; PODEM chạy lỗi mẫu, kiểm chứng bằng fault simulation |
| 04/10/2026 | Ghép báo cáo/slide; coverage c17, demo tuần tự, đối chiếu trace; hoàn thiện lời giải và quay video |
| 05/10/2026 | Sửa lỗi, chốt 5–10 trang, diễn tập trong 20 phút; xuất PDF cuối, kiểm tra video và gói nộp |
| 06–07/10/2026 | Dự phòng sửa lỗi hoặc phản hồi, không bố trí nội dung bắt buộc mới |
| 08/10/2026 | Hạn nộp chính thức; thời điểm đóng cổng và cách nộp cần xác nhận |

## Việc P1 cần hoàn tất (cập nhật 06/10/2026)

- (Đã xong 06/10) Merge PR P6 #11 và PR P1; kiểm chứng và build lại trên `main` trước khi gắn tag.
- Duyệt bìa, thông tin nhóm, nội dung rút gọn Chương 5–7 cùng P4/P5/P6.
- (Đã quay 07/10) Kiểm tra lại video Hình 4.5 trước khi nộp.
- Xác nhận giờ/kênh/định dạng nộp ngày 08/10/2026 và việc có chiếu video trong 20 phút hay không.
- (Đã xong 06/10) Release/tag [`v1.0`](https://github.com/TuanNguyn-11/dft-atpg/releases/tag/v1.0).
- Diễn tập 20 phút cùng nhóm; nộp bài và lưu bằng chứng. Checklist: [notes/p1_checklist_nop.md](notes/p1_checklist_nop.md).
- (Đã xong) Mời thành viên, tạo branch, build cục bộ XeLaTeX + Biber. Build trên TeXPage vẫn chưa xác nhận.
