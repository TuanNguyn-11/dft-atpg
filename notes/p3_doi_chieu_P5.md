# Phiếu đối chiếu P3 ↔ code P5/P6 — 06/10/2026

## Trạng thái và nguồn thực thi

Đã đối chiếu hai golden trace với API P5 và file exporter; simulator P6
xác nhận các vector. Không còn phụ thuộc “chưa nhận P5/P6”.

- Base: `8564678cd360594cbd540389d49c99021525ac08` (origin/main sau fetch),
  mới hơn mốc feedback `eb6694d`; đã có exporter và trace backtrack.
- P5 remote `5b461af`; exporter đưa vào tại `94ee04a`. Đọc thêm
  [bàn giao P5](p5_ghi_chu.md); đây là bằng chứng trong repo, không phải
  xác nhận cá nhân qua tin nhắn.
- Python 3.12.10, pytest 9.1.1 trên Windows: `342 passed`.
- [Bằng chứng 35 ô chi tiết](../results/p3_doi_chieu_code.md) sinh bằng
  [script P3](p3_doi_chieu_code.py), gọi trực tiếp `Circuit.from_bench`
  P6, `podem(..., trace=True)` P5, `simulate/detects` P6. Không dùng
  implementation tham chiếu P3 làm kết quả lõi P5.
- File P5: [c17](../results/trace_c17_11sa0.md),
  [backtrack](../results/trace_backtrack.md). Tái sinh bằng exporter trong
  bộ nhớ và so toàn nội dung với file đã commit: khớp (chuẩn hóa newline).

## Đối chiếu đủ bảy cột

| Cột | Golden mong đợi | API P5 thực tế | File exporter P5 | Kết luận |
|---|---|---|---|---|
| Bước | c17: 1,2; phụ: 1,2,3 | Cùng thứ tự và số hàng | Cùng thứ tự | Khớp |
| Objective | c17: (11,1),(2,1); phụ: (t,1),—,(t,1) | Tuple tương ứng; None tại hàng đảo | Tuple và — | Khớp ngữ nghĩa; golden thêm chú thích đảo |
| Backtrace → PI | c17: 3=0,2=1; phụ: a=1,—,b=1, có diễn giải đường đi | Tuple (3,0),(2,1); (a,1),None,(b,1) | Tuple và — | Khớp PI/bit, không giống nguyên văn |
| Gán PI | 3=0,2=1; a=1,a=0,b=1 | Đúng từng phép gán | Đúng từng phép gán | Khớp |
| Mọi net sau imply | Các trạng thái dưới đây | So toàn bộ dict PI/net, không chỉ PO | PI viết gộp thành tuple | Khớp sau chuẩn hóa cách viết PI |
| D-frontier | c17: [16,19],[19,23]; phụ: rỗng cả 3 hàng | Đúng cả nội dung lẫn thứ tự | Cùng nội dung | Khớp |
| Hành động | c17: tiếp tục/thành công; phụ: backtrack/tiếp tục/thành công | c17 khớp; phụ: tiếp tục/backtrack/thành công | Đã chuẩn hóa đúng golden | Hai khác biệt API có giải thích |

### Mọi net theo từng hàng

Các giá trị sau đều đã so bằng assertion giữa golden, API và exporter:

| Mạch/hàng | PI theo .bench | Toàn bộ net cổng (mong đợi = thực tế) |
|---|---|---|
| c17/1 | (X,X,0,X,X) | 10=1,11=D,16=X,19=X,22=X,23=X |
| c17/2 | (X,1,0,X,X) | 10=1,11=D,16=D',19=X,22=D,23=X |
| phụ/1 | (1,X) | t=D,n=0,out=0 |
| phụ/2 | (0,X) | t=X,n=1,out=X |
| phụ/3 | (0,1) | t=D,n=1,out=D |

Kết quả c17: DETECTED, X10XX, 0 backtrack; mạch phụ: DETECTED, 01,
1 backtrack. Không giữ t=D từ nhánh cũ sau khi đảo a.

### Chốt cách đọc hành động cùng bản bàn giao P5

Giữ golden nguyên vẹn. Golden mô tả việc cần làm sau trạng thái một hàng;
API ghi thao tác vừa thực hiện. Vì vậy hàng a=1 chưa đảo PI nhưng golden
ghi backtrack; hàng a=0 đã đảo nên API ghi backtrack, golden ghi tiếp tục.
Exporter P5 đã chuyển sang quy ước golden: đẩy nhãn backtrack về hàng dẫn
tới bế tắc, đổi nhãn hàng đảo thành tiếp tục. Không đổi lõi hoặc exporter
của P5, không tuyên bố raw API khớp chuỗi hoàn toàn. Script bảo vệ chính xác
hai khác biệt này; không bỏ qua toàn bộ cột hành động.

Với giới hạn 0, API có hàng kết thúc không gán PI, nhãn “thất bại”, nhưng
`status=ABORTED`. Exporter giữ một hàng gán, nhãn backtrack bị chặn và lý do
ABORTED ở kết luận. Không suy ra UNTESTABLE từ chữ “thất bại” trong một hàng.

## Xác nhận simulator P6 và điều kiện dừng

| Kiểm tra thật | Kết quả |
|---|---|
| c17 cube X10XX | 8/8 cách điền được detects xác nhận |
| c17 01000; PO (22,23) | Tốt (1,1), lỗi (0,0) |
| Mạch phụ 01; PO out | Tốt 1, lỗi 0 |
| Mạch phụ max_backtracks=0 | ABORTED, pattern 1X, 0 backtrack; đã thử nhánh đầu |
| Mạch phụ max_backtracks=1 | DETECTED, pattern 01, 1 backtrack |

## So sánh P2 và P3

P2 đã tích hợp; chạy lại `notes/p2_kiem_chung.py` đạt 160 ô logic,
bốn trạng thái trace/frontier, cube 4/4 và 8/8 completions, bốn cặp PO.
Nguồn mô tả các bước: [ghi chú P2](p2_ghi_chu.md).

| Tiêu chí | D-algorithm P2 | PODEM P3/P5 |
|---|---|---|
| Nơi quyết định | PI và net nội bộ qua cube | PI |
| Biện minh | Justification, J-frontier | Backtrace về PI, imply net nội bộ |
| Tìm kiếm | Chọn cube và giải ràng buộc nội bộ | Cây quyết định nhị phân PI |
| c17 11/SA0 | 4 lần chọn cube, 3 PI, 0 backtrack | 2 phép gán PI, 0 backtrack |
| Pattern | X100X; tổng quát hóa thành X10XX | X10XX |

Không đếm implication/tổng quát hóa là chọn cube. Không suy ra tỷ lệ tăng tốc
4/2. P3-v1 dùng input X đầu tiên và topo ổn định, không dùng SCOAP; số liệu
không đại diện mọi heuristic. Xấu nhất PODEM vẫn có tìm kiếm theo hàm mũ.

## Lệnh tái lập

Từ gốc checkout, dùng Python >=3.10; môi trường đã chạy `.venv` Python 3.12.10:

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) 'src')
$env:PYTHONIOENCODING = 'utf-8'
.\.venv\Scripts\python.exe -B notes/p3_doi_chieu_code.py
.\.venv\Scripts\python.exe -B notes/p3_kiem_chung.py
.\.venv\Scripts\python.exe -B notes/p3_kiem_tra_ban_giao.py
.\.venv\Scripts\python.exe -B notes/p2_kiem_chung.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --fault 11 0 --trace
.\.venv\Scripts\python.exe -m atpg.run circuits/backtrack_example.bench --fault t 0 --trace
.\.venv\Scripts\python.exe -m atpg.run circuits/backtrack_example.bench --fault t 0 --max-backtracks 0 --trace
.\.venv\Scripts\python.exe -m atpg.run circuits/backtrack_example.bench --fault t 0 --max-backtracks 1 --trace
```

## Lịch sử và giới hạn

Phiếu ngày 05/10 trên base `f95d609` ghi chưa nhận P5/P6 là đúng ở thời
điểm đó; bản cũ lưu trong lịch sử Git trước bản cập nhật này. Góp ý về
khác biệt nhãn API vẫn đúng; việc thiếu file exporter đã được P5 giải quyết.
XOR/XNOR đã được P5 triển khai P3-v1.1, kiểm thử trong bộ 342 test; hai
golden này không tự chứng minh XOR/branch/multiple faults đúng trên mọi mạch.
Không nhận đã có cuộc trao đổi trực tiếp hay xác nhận cá nhân của P2/P5/P6.
