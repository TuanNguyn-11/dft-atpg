# Hướng dẫn chạy P5 — PODEM

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
