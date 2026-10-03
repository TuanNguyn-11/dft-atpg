# DFT — Automatic Test Pattern Generation

Đồ án: **Automatic Test Pattern Generation Algorithms for Combinational and Sequential Circuits**.

Repo chung của nhóm gồm báo cáo LaTeX, slide và chương trình minh họa PODEM bằng Python.

## Trạng thái

**Cập nhật P1 ngày 03/10/2026:** đã viết Chương 1, 2, kết luận theo trạng thái hiện tại, ba slide P1, bảng SCOAP và ví dụ collapsing c17. Có lời giải/lời dẫn Hình 4.5; **P1 tự quay video 2–3 phút**. P2–P6 trong repo vẫn là khung, chưa có lõi ATPG, netlist hoặc kết quả thực nghiệm được tích hợp. Các lệnh CLI ATPG bên dưới là giao diện dự kiến, chưa chạy được. Chưa phát hành PDF cuối hoặc tag `v1.0`.

Kiểm chứng độc lập phần P1 (chỉ dùng thư viện chuẩn, chạy từ gốc repo):

```text
python scripts/check_p1_examples.py
```

Lệnh này kiểm tra collapsing trên 32 vector c17, tám cách điền mẫu X, bảng SCOAP 11 net và toàn bộ tám vector bài Hình 4.5. Đây không phải phép chạy PODEM hoặc kết quả coverage của nhóm. Xem [kiến thức và thuật ngữ P1](notes/p1_kien_thuc.md), [lời giải video](notes/p1_video_loi_giai.md) và [biên bản kiểm tra tích hợp](notes/p1_review.md).

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
| P5 | Nguyễn Thị Thúy Hàng — 23119142 | Chương 6; logic 5 giá trị và lõi PODEM | `p5-podem-code` |
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

Các thư mục trống có `.gitkeep` để Git lưu được cấu trúc. Những file code, netlist và kết quả sẽ được chủ sở hữu thêm khi triển khai.

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

Kết quả là `slides/main.pdf`. Hiện có trang tiêu đề và ba frame P1; P6 tiếp tục ghép khi P2–P6 gửi slide.

PDF trung gian được bỏ qua bởi Git. Khi đã rà soát bản cuối, sao chép thành `report/bao_cao_DFT_ATPG.pdf` và `slides/slide_DFT_ATPG.pdf`; hai tên này được phép commit.

## Chạy code và kiểm thử — sau khi P4/P5/P6 triển khai

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
- **Bắt buộc chọn 01 ví dụ/bài tập từ sách hoặc tài liệu môn học, trình bày đề bài, cách giải và kết luận; quay video giải thích để nộp kèm.** Đã chốt Hình 4.5, mục 4.3, trang in 166–167, tìm vector phát hiện y/SA0; **P1 thực hiện video 2–3 phút**. Xem [lời giải và lời dẫn](notes/p1_video_loi_giai.md). Video còn chờ P1 quay.
- Giáo trình chính: *VLSI Test Principles and Architectures: Design for Testability*, Laung-Terng Wang, Cheng-Wen Wu, Xiaoqing Wen (biên tập), Morgan Kaufmann, 2006. Thông tin được kiểm tra trực tiếp từ PDF do P1 cung cấp; mục BibLaTeX ở `report/bib/p1.bib`.
- Chưa xác nhận tiến độ làm riêng của P2–P6 ngoài repo. Bản ZIP TeXPage do P1 cung cấp trùng nội dung nguồn báo cáo trước đợt cập nhật này; chưa có bằng chứng build trên TeXPage. Kiểm tra build cục bộ được ghi trong biên bản review.
- Hạn nộp chính thức: **08/10/2026**. Mục tiêu nội bộ: hoàn thiện hết ngày **05/10/2026**, tức trước 06/10.
- Kế hoạch này thay thế mốc 10/10 và dự kiến số trang dài trong bộ hướng dẫn ban đầu. Chi tiết phân bổ trang, rubric và thời gian: [kế hoạch P1](notes/p1_ke_hoach.md).

## Các mốc chung mới — kế hoạch đề xuất

| Ngày | Đầu ra cần đạt |
|---|---|
| 01/10/2026 | Repo và khung; kiểm tra TeXPage; xác nhận giao diện P5/P6, tài liệu môn học và bài tập video |
| 02/10/2026 | Netlist c17 đọc được, bảng logic, golden trace, mạch tuần tự; học và viết ghi chú song song |
| 03/10/2026 | PR bản nháp các phần; PODEM chạy lỗi mẫu, kiểm chứng bằng fault simulation |
| 04/10/2026 | Ghép báo cáo/slide; coverage c17, demo tuần tự, đối chiếu trace; hoàn thiện lời giải và quay video |
| 05/10/2026 | Sửa lỗi, chốt 5–10 trang, diễn tập trong 20 phút; xuất PDF cuối, kiểm tra video và gói nộp |
| 06–07/10/2026 | Dự phòng sửa lỗi hoặc phản hồi, không bố trí nội dung bắt buộc mới |
| 08/10/2026 | Hạn nộp chính thức; thời điểm đóng cổng và cách nộp cần xác nhận |

## Việc P1 cần hoàn tất

- Mời năm thành viên vào repo; xác nhận mỗi người đã tạo branch từ `main` mới nhất.
- Kiểm tra biên dịch trên TeXPage bằng XeLaTeX + Biber; khi có nội dung, rà soát tràn trang, tham chiếu và trích dẫn.
- Thống nhất kế hoạch rút ngắn với cả nhóm, xác nhận tiến độ thực tế của P2–P6.
- Quay video Hình 4.5 theo lời giải đã kiểm tra (P1 phụ trách).
- Xác nhận hình thức nộp, định dạng video và có cần chiếu video trong 20 phút hay chỉ nộp kèm.
- Tự kiểm tra hiểu phần học trong `notes/p1_kien_thuc.md`; cập nhật kết luận khi có kết quả thực nghiệm thật từ P2–P6.
