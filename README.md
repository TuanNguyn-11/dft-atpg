# DFT — Automatic Test Pattern Generation

Đồ án: **Automatic Test Pattern Generation Algorithms for Combinational and Sequential Circuits**.

Repo chung của nhóm gồm báo cáo LaTeX, slide và chương trình minh họa PODEM bằng Python.

## Trạng thái

**M0 — khung dự án:** đã chuẩn bị cấu trúc thư mục, tám chương báo cáo, cấu hình XeLaTeX và khung slide. Chưa có code ATPG, netlist, kết quả đo hoặc nội dung chương hoàn chỉnh. Các lệnh chạy Python bên dưới là giao diện dự kiến theo thỏa thuận nhóm, chưa chạy được ở mốc này.

## Mục tiêu và phạm vi

- Trình bày nguyên lý ATPG, D-algorithm, PODEM và ATPG cho mạch tuần tự.
- Cài đặt PODEM bằng Python, minh họa từng bước trên ISCAS'85 c17.
- Dùng lỗi chung `11/SA0` để đối chiếu trace chạy tay và trace code.
- Minh họa full scan và trải khung thời gian trên mạch tuần tự nhỏ.
- Chỉ dùng công cụ miễn phí; code dùng thư viện chuẩn Python, kiểm thử bằng pytest.

## Thành viên và phân công

Điền họ tên và MSSV trước khi nộp.

| Vai trò | Họ tên / MSSV | Công việc | Branch |
|---|---|---|---|
| P1 | Chưa điền | Chương 1, 2, 8; repo; khung LaTeX; review và tích hợp báo cáo | `p1-nguyen-ly` |
| P2 | Chưa điền | Chương 3; D-algorithm; bảng logic 5 giá trị; hình c17 dùng chung | `p2-d-algorithm` |
| P3 | Chưa điền | Chương 4; PODEM lý thuyết; golden trace | `p3-podem-ly-thuyet` |
| P4 | Chưa điền | Chương 5; mạch tuần tự; full scan và unroll | `p4-tuan-tu` |
| P5 | Chưa điền | Chương 6; logic 5 giá trị và lõi PODEM | `p5-podem-code` |
| P6 | Chưa điền | Chương 7; đọc mạch, mô phỏng lỗi, CLI, kiểm chứng; ghép slide | `p6-mo-phong-ket-qua` |

## Cấu trúc repo

```text
circuits/                 Netlist .bench (P6: c17; P4: mạch tuần tự)
src/atpg/                 Code Python của P4, P5, P6
tests/data/               Dữ liệu kiểm tra chung của P2; tests/ chứa kiểm thử
results/                  Trace, pattern và kết quả kiểm chứng
notes/                    Ghi chú học tập pX_ghi_chu.md
report/
  main.tex                File gốc báo cáo do P1 quản lý
  chapters/               Tám chương theo phân công
  figures/common/         Hình c17 dùng chung do P2 cung cấp
  figures/p1/ ... p6/      Hình riêng của từng thành viên
  bib/p1.bib ... p6.bib    Tài liệu tham khảo riêng
slides/
  main.tex                Khung Beamer; P6 phụ trách bản cuối
  parts/p1.tex ... p6.tex  Mỗi người viết 2–3 frame
```

Các thư mục trống có `.gitkeep` để Git lưu được cấu trúc. Những file code, netlist và kết quả sẽ được chủ sở hữu thêm khi triển khai.

## Biên dịch báo cáo

Cần TeX Live có XeLaTeX, Biber, hỗ trợ tiếng Việt và các font TeX Gyre, Latin Modern; hoặc dùng Overleaf. Không dùng pdfLaTeX cho khung này.

### Trên Overleaf

1. Tải ZIP của branch đang làm việc trên GitHub và tải lên thành project Overleaf.
2. Chọn **Main document** là `report/main.tex`, **Compiler** là **XeLaTeX**.
3. Bấm Recompile; Overleaf dùng Biber khi cần xử lý thư mục tham khảo của biblatex.
4. Bổ sung thông tin bìa và nội dung chương. File `.bib` ban đầu chỉ có chú thích, nên chưa có danh mục tài liệu và có thể có cảnh báo bibliography trống.
5. Muốn biên dịch slide, đổi Main document thành `slides/main.tex`.
6. Cuối mỗi đợt, tải nguồn `.tex`, `.bib` và hình về rồi commit vào đúng thư mục; không phụ thuộc tính năng đồng bộ GitHub trả phí.

### Trên máy cá nhân

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

Kết quả là `slides/main.pdf`. Bản khung slide chỉ có trang tiêu đề cho đến khi các thành viên thêm frame.

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

## Các mốc chung

| Ngày | Mốc |
|---|---|
| 01/10/2026 | M0: repo, khung LaTeX; học kiến thức chung; P5/P6 xác nhận giao diện |
| 03/10/2026 | M1: đọc c17, golden trace, bảng 5 giá trị, mạch tuần tự ví dụ |
| 06/10/2026 | M2: PODEM chạy được lỗi mẫu; PR bản nháp chương |
| 07/10/2026 | M3: tích hợp code, kiểm chứng; PR chương hoàn chỉnh |
| 08/10/2026 | M4: ghép báo cáo và slide |
| 09/10/2026 | Rà soát, tập thuyết trình và demo |
| 10/10/2026 | Nộp PDF báo cáo, PDF slide và link repo; tạo tag `v1.0` |

## Việc P1 cần hoàn tất cho M0

- Mời năm thành viên vào repo và bổ sung họ tên/MSSV.
- Merge PR khung dự án, thông báo cả nhóm tạo branch từ `main` mới nhất.
- Xác nhận biên dịch trên Overleaf và máy có XeLaTeX + Biber.
- Hỏi giảng viên mẫu trang bìa và quy định định dạng.
- Tổ chức buổi họp khởi động; nhắc P5/P6 xác nhận giao diện.
