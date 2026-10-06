# Biên bản kiểm tra P2 — 03/10/2026

## Trạng thái hiện tại — nghiệm thu feedback_P2, 06/10/2026

Base đã fetch và cập nhật fast-forward: `586218e1eb244fa5374b7bc856e0ffd979447f4a`
(origin/main). Mốc `eb6694d` trong feedback là snapshot cũ; base hiện tại đã
có P5/P6, Chương 7, PDF phát hành và biên tập P1. Branch làm việc vẫn là
`p2-d-algorithm`. Hai file feedback người dùng cung cấp giữ nguyên, không stage.
Không thay release/tag, PDF đã phát hành hoặc nội dung của thành viên khác.

Môi trường thực chạy: **Python 3.12.1, pytest 9.1.1**, venv `.venv`.
Chỉ script kiểm chứng/ghi chú P2 thay đổi, không sửa logic P5 hay simulator P6.

### Checklist thực hiện

- [x] P2-01: giữ oracle độc lập; thêm `--integrated` đọc các ô từ Markdown
  rồi gọi `atpg.logic.eval_gate` trực tiếp, không dùng bảng Python chép lại.
- [x] 160/160 ô khớp; không có bất đồng hoặc phản ví dụ.
- [x] `Circuit.from_bench('circuits/c17.bench')`, `Fault('11',0)` lỗi stem;
  PI đúng thứ tự `(1,2,3,6,7)`, PO `(22,23)`.
- [x] Duyệt mọi cách điền X rồi gọi simulator/detects thật: X100X **4/4**,
  X10XX **8/8**, đều khác tại PO22; `detects_cube` cùng trả True.
- [x] Vector 01000: PO tốt **(1,1)**, lỗi **(0,0)**; CLI trace phát hiện
  tại cả PO22 và PO23 sau khi điền đủ bit. Không thay X bảo thủ của trace tay
  bằng D ở PO23 chỉ vì một vector nhị phân cụ thể.
- [x] P2-02: **4 lần chọn cube, 3 PI gán, 0 backtrack**; X100X → X10XX.
  Tổng quát hóa không tính là quyết định thứ năm; khác đơn vị đếm gán PI P3.
- [x] Bảng bàn giao cho P3 ở `p2_ghi_chu.md`, có cùng lỗi/đơn vị/phạm vi.
- [x] Rà chương/slide: phân biệt cube gốc/hình tổng quát, D/J-frontier và
  thành công sau justification vẫn đúng; giữ nguyên bản P1 đã biên tập.
- [x] Các đoạn chờ P5/P6, netlist và wrapper JPG ở dưới đã được xác định là
  lịch sử 03–05/10; không còn là trạng thái hay phụ thuộc hiện tại.

### Lệnh chạy lại và kết quả thật

Từ gốc checkout, dùng Python >=3.10 và pytest trong venv:

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) 'src')
$env:PYTHONIOENCODING = 'utf-8'
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pytest --version
.\.venv\Scripts\python.exe notes/p2_kiem_chung.py --integrated
.\.venv\Scripts\python.exe -m pytest tests/test_logic.py tests/test_fault_sim.py -q
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --fault 11 0 --pattern X100X --trace
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --fault 11 0 --pattern X10XX --trace
.\.venv\Scripts\python.exe -m pytest -q
git diff --check
```

- Script: oracle 160 ô, bốn trạng thái/frontier, đáp ứng nhị phân độc lập
  vẫn PASS; chế độ tích hợp PASS 160/160, 4/4, 8/8 và PO 01000.
- Test logic/fault_sim: **240 passed in 1.52s**.
- Hai lệnh CLI: `PHAT HIEN voi moi cach dien X`; X=0 cho 01000, PO22/23 khác.
- Suite đầy đủ: **332 passed in 6.50s**. Mốc 302 của feedback là lịch sử;
  không đổi số test để khớp mốc cũ. Thời gian là lần chạy máy này.
- Không sửa nguồn LaTeX/hình/slide, không rebuild hoặc thay PDF phát hành.

### File thay đổi và nội dung PR đề xuất

| File | Thay đổi và lý do |
|---|---|
| `notes/p2_kiem_chung.py` | Thêm `--integrated`, đối chiếu Markdown→logic thật; simulator thật kiểm mọi cách điền; lỗi in gate/input/expected/actual hoặc vector/PO |
| `notes/p2_ghi_chu.md` | Cập nhật trạng thái 06/10, số liệu/đơn vị bàn giao P3, checklist con người |
| `notes/p2_review.md` | Lưu base, môi trường, checklist, lệnh và kết quả thật; giữ lịch sử có ngày |

Đề xuất PR: **[P2] Bổ sung bằng chứng kiểm chứng trên code đã tích hợp**.
Vấn đề: oracle độc lập/test Python chép bảng chưa bảo đảm Markdown còn đồng bộ
với P5 và ghi chú vẫn chờ simulator đã có. Thay đổi: chế độ kiểm tích hợp tái
lập cùng cập nhật bàn giao. Kiểm chứng: 160/160 ô, 4/4 và 8/8 cách điền,
240 test liên quan và 332 test toàn bộ. Giới hạn: hai cube c17, lỗi stem
11/SA0; không phải implementation hoặc đo hiệu năng D-algorithm. Không thay
API/code chung, bảng chuẩn, nguồn LaTeX hoặc số liệu mô phỏng của thành viên khác.

### Checklist cần con người thực hiện

- [ ] P2 đọc hiểu và giải thích được phần mình; chưa xác nhận đã học.
- [ ] P2 luyện trình bày ba slide, phối hợp diễn tập/demo của nhóm.
- [ ] P1/P3 review artifact bàn giao và cập nhật phần so sánh khi cần.
- [ ] Xác nhận/nộp bài theo checklist P1; agent không thực hiện thay.

Các phần có ngày 03–05/10 dưới đây là lịch sử; các câu thiếu code/hình cũ
không còn mô tả trạng thái hiện tại.

## Sửa theo feedback P1 — 05/10/2026

- Mã giả trả Result với status/pattern, truyền DETECTED và ABORTED qua mọi
  lời gọi; chỉ restore khi nhánh thất bại. Chỉ mức gốc trả UNTESTABLE khi hết
  toàn bộ PDCF/nhánh con.
- Lưu đồ ghi điều kiện xung đột, PO có sai khác, J rỗng, còn lựa chọn và
  kết thúc; cube mới quay lại implication, giới hạn dẫn tới ABORTED riêng.
- `common/c17.tex` đã là bản vẽ TikZ sáu NAND, chỉnh kích thước/giá trị bằng
  macro local. JPG giữ làm đối chiếu; nhận xét wrapper JPG bên dưới là lịch sử.
- Slide thứ ba bỏ cột hẹp, dùng hình rộng 0.86 linewidth. Đã render và xem
  ở 1600 pixel: nhãn 11=D, 16=D-bar, 22=D đọc rõ, không chồng chữ.
- Hai script P1/P2 đều PASS; bộ kiểm tra bàn giao P3 cũng PASS, riêng netlist
  c17 của P6 vẫn PENDING. Không thay đổi dữ liệu/trace đã được review đúng.
- Build trên P2 trước cập nhật main trả mã 0, không undefined/citation,
  missing character hoặc overfull. Đã cập nhật `origin/main` tại `bbf2efd`
  bằng merge không xung đột, giữ nguyên phần P3/P4.
- Build tích hợp XeLaTeX/Biber trả mã 0: báo cáo **13 trang PDF** (2 bìa,
  1 mục lục, 10 trang nội dung), slide **13 trang**. Không có undefined
  reference/citation hoặc missing character. Overfull ngoài P2 vẫn tồn tại:
  Chương P4 dòng 132–145 (59.60092 pt), 146–157 (73.97719 pt), bibliography
  nguồn FAN (0.16591 pt). Script build strict của nhóm sẽ chặn các cảnh báo
  đó; chưa nhận build tích hợp đạt mọi kiểm tra strict. Không sửa file P4/P1
  hoặc bibliography P3 ngoài phạm vi feedback. P1 cần cân đối trang khi thêm P5/P6.

Phần dưới ghi kết quả lần bàn giao 03/10, không phải trạng thái tích hợp mới.

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
