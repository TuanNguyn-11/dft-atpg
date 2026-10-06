# Hướng dẫn chạy P5 — PODEM

## Trạng thái hiện tại sau merge — 06/10/2026

Đang ở branch `p5-podem-code`, merge commit
`6a5d0153c6e961b1de0a5d1ed379699829aa87d3` (P5 `94ee04a` + main
`53374fb`). Checkout này đã có Circuit/Fault, `run`, fault simulator,
`unroll` và hai bench thật; các lệnh dưới đây chạy trực tiếp tại repo root.

### Môi trường đã kiểm tra

- Python 3.14.8; pytest 9.1.1.
- PowerShell:

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) 'src')
$env:PYTHONIOENCODING = 'utf-8'
```

### Kiểm chứng đã chạy trên checkout hiện tại

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_logic.py tests/test_podem.py -q
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --fault 11 0 --trace
.\.venv\Scripts\python.exe -m atpg.run circuits/backtrack_example.bench --fault t 0 --trace
.\.venv\Scripts\python.exe -m pytest -q
```

- Logic/PODEM: **255 passed**.
- Toàn repo: **342 passed, 0 skipped**.
- c17 `11/SA0`: `DETECTED`, `X10XX`, 0 backtrack; fault simulation xác nhận.
- `backtrack_example` `t/SA0`: `DETECTED`, `01`, 1 backtrack; fault simulation xác nhận.

Kiểm tra tích hợp/review chéo:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_integration.py tests/test_p4_integration.py tests/test_input_validation.py -q
.\.venv\Scripts\python.exe notes/p2_kiem_chung.py --integrated
```

- Tích hợp PODEM/P4/P6/input validation: **32 passed**.
- P2: Markdown đối chiếu `atpg.logic.eval_gate` **160/160**; `X100X` **4/4** và `X10XX` **8/8** cách điền được phát hiện; vector `01000` cho PO tốt `(1,1)` và PO lỗi `(0,0)`.
- `test_sequential.py` có fixture tham chiếu tắt PODEM. Bằng chứng gọi PODEM thật qua unroll là `test_sequential_with_real_podem_and_unroll` trong `tests/test_integration.py`; P4 kiểm thêm trong `tests/test_p4_integration.py`.
- P6 validation: test từ chối SV=2, net sai, branch không tồn tại hoặc không nối với net. Đây là xác nhận trên code P6 đã merge, không phải thay đổi P5.

### Tái sinh trace P5

```powershell
.\.venv\Scripts\python.exe scripts/export_podem_trace.py --bench circuits/c17.bench --fault 11 0 --output results/trace_c17_11sa0.md
.\.venv\Scripts\python.exe scripts/export_podem_trace.py --bench circuits/backtrack_example.bench --fault t 0 --output results/trace_backtrack.md
```

Hai lệnh đã chạy thành công trên checkout này. Exporter gọi `podem(trace=True)`;
các hàng được dựng từ `PodemResult.steps`, có đúng 7 cột, ổn định theo thứ tự
PI/net. Test xác nhận xuất lặp lại, trạng thái backtrack/ABORTED và lỗi đầu vào/
ghi file. Trace mạch phụ ghi hàng `a=1` là `backtrack`; hàng đảo `a=0` có
Objective/Backtrace `—`, net `t=X,n=1,out=X`, hành động `tiếp tục`.
Golden trace P3 trong `results/golden_trace_*.md` được giữ nguyên.

### Bàn giao còn mở

- Chưa build XeLaTeX/Biber (`xelatex`, `biber` không có trong PATH).
- Cần P2 xác nhận trực tiếp khi phối hợp; kiểm tra độc lập 160/160 đã chạy,
  nhưng không được xem là lời xác nhận của thành viên.
- P1 biên tập/dàn trang cuối; nhóm tập demo/thuyết trình 20 phút và P1 làm
  video 2–3 phút; xác nhận giờ/kênh nộp trước hạn 08/10/2026.
- Merge commit đang local; push chưa hoàn tất do thao tác push cần quyền đã
  bị từ chối.

## Hướng dẫn lịch sử trước merge

Phần dưới được giữ làm hướng dẫn/ghi nhận của snapshot cũ. Các nhận định rằng
checkout P5 thiếu Circuit/bench hoặc chưa merge main và các con số 265/5
skipped, 340 thuộc về những snapshot lịch sử, không mô tả checkout hiện tại.

## Môi trường

- Python **3.10 trở lên** và `pytest`.
- Đã kiểm tra trên Python 3.14.8, pytest 9.1.1.
- Trên Windows dùng PowerShell; lệnh dưới đây tính từ gốc checkout.

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install pytest
$env:PYTHONPATH = (Join-Path (Get-Location) 'src')
$env:PYTHONIOENCODING = 'utf-8'
```

Nếu đã có virtual environment Python >=3.10, dùng lại thay vì tạo mới.

## Kiểm thử branch P5

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_logic.py tests/test_podem.py -q
.\.venv\Scripts\python.exe -m pytest -q
```

Trên branch `p5-podem-code` tại commit nền `7979490`, sau bổ sung kiểm thử
trace, kết quả thực tế là **255 passed** cho logic/PODEM và **265 passed**,
**5 skipped** cho toàn bộ test có trong checkout P5. Năm kiểm thử CLI thật
cần Circuit/netlist hiện chưa có trong checkout. Đây là số test của branch
đó, không bao gồm các test tích hợp được thêm trên main.

## Xuất trace PODEM

Exporter đọc bench bằng `Circuit.from_bench`, gọi `podem(trace=True)` và
ghi đủ bảy cột. Hai netlist c17 và backtrack cùng các module `Circuit`,
`Fault` hiện có trên snapshot tích hợp main. Checkout P5 nền ở trên chưa có
các dependency ấy; test CLI được skip rõ ràng ở checkout này và chỉ chạy
khi các module/netlist tích hợp hiện diện.

```powershell
.\.venv\Scripts\python.exe scripts/export_podem_trace.py --bench circuits/c17.bench --fault 11 0 --output results/trace_c17_11sa0.md
.\.venv\Scripts\python.exe scripts/export_podem_trace.py --bench circuits/backtrack_example.bench --fault t 0 --output results/trace_backtrack.md
```

Muốn kiểm tra giới hạn dừng riêng:

```powershell
.\.venv\Scripts\python.exe scripts/export_podem_trace.py --bench circuits/backtrack_example.bench --fault t 0 --max-backtracks 0 --output results/trace_backtrack_aborted.md
```

Kết quả thực trên snapshot tích hợp dùng kiểm tra ngày 06/10/2026:

| Mạch/lỗi | Status | Pattern | Backtracks |
|---|---|---|---:|
| c17, 11/SA0 | DETECTED | X10XX | 0 |
| backtrack, t/SA0 | DETECTED | 01 | 1 |
| backtrack, t/SA0, giới hạn 0 | ABORTED | 1X | 0 |

Hai lần chạy c17 liên tiếp tạo nội dung giống hệt nhau. Trace backtrack ghi
`a=1` là `backtrack`, hàng đảo `a=0` có Objective/Backtrace `—` và trạng
thái `t=X,n=1,out=X`. `ABORTED` luôn được giữ riêng khỏi `UNTESTABLE`.

## Kiểm tra snapshot tích hợp

Khi checkout tích hợp có `Circuit`, fault simulator, `run`, netlist và test
P4/P6, chạy thêm các lệnh nghiệm thu:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_logic.py tests/test_podem.py -q
.\.venv\Scripts\python.exe -m atpg.run circuits/c17.bench --fault 11 0 --trace
.\.venv\Scripts\python.exe -m atpg.run circuits/backtrack_example.bench --fault t 0 --trace
.\.venv\Scripts\python.exe -m pytest -q
```

Snapshot tích hợp được kiểm thử tạm từ `origin/main` tại `586218e` cùng
thay đổi P5 cho **340 passed** trên Python 3.14.8/pytest 9.1.1. Checkout
P5 không được merge/cập nhật trong lượt này; kết quả này được ghi riêng để
không nhầm dependency kiểm thử với file đã có trên branch.

## Phạm vi review chéo

- P4: `unroll`, `fault_in_frames`, `full_scan`, `tests/test_unroll.py`.
- P6: `circuit.py`, `fault_sim.py`, `faults.py`, `run.py` và
  `tests/test_input_validation.py`; snapshot main từ chối SV=2 và branch
  không tồn tại/không nối tới net.
- Tích hợp tuần tự PODEM thật: `tests/test_integration.py` gọi PODEM được
  bọc spy qua unroll. Fixture `reference_only` trong
  `tests/test_sequential.py` tắt PODEM, không dùng fixture đó làm bằng chứng.
- P2: review đã lưu ghi 160/160 ô logic PASS; P6 review chéo xác nhận các
  vector/trace P2 và P3 bằng fault simulator. Không ghi nhận đã liên hệ
  riêng thành viên trong lượt này.

## Bàn giao

Trước commit, xem `git status --short`, `git diff --stat` và chạy
`git diff --check`. Chỉ stage file P5. P1 vẫn phụ trách quyết định rút gọn
và dàn trang cuối; người trong nhóm tự tập demo, trình bày và nộp bài.
