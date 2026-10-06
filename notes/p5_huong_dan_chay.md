# Hướng dẫn cài đặt và chạy P5 — PODEM

## 1. Mục đích

File này hướng dẫn các thành viên trong nhóm cài đặt môi trường và chạy phần P5 — PODEM trên máy cá nhân.

Branch sử dụng cho P5:

```text
p5-podem-code
```

---

## 2. Yêu cầu môi trường

Các công cụ cần có:

- Git
- Python 3.14+
- uv
- Windows PowerShell

Kiểm tra phiên bản:

```powershell
git --version
python --version
uv --version
```

---

## 3. Lấy source code

Clone repository của nhóm:

```powershell
git clone <URL_REPOSITORY>
cd dft-atpg
```

Chuyển sang branch P5:

```powershell
git checkout p5-podem-code
```

Cập nhật source code mới nhất:

```powershell
git pull origin p5-podem-code
```

---

## 4. Cài đặt môi trường

Tại thư mục gốc của repository, chạy:

```powershell
uv sync
```

Sau đó kích hoạt virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 5. Thiết lập PYTHONPATH

Project sử dụng source code trong thư mục `src/`, vì vậy trước khi chạy test cần thiết lập:

```powershell
$env:PYTHONPATH = "src"
```

Lệnh này áp dụng cho cửa sổ PowerShell hiện tại.

---

## 6. Chạy toàn bộ test

Để kiểm tra toàn bộ project:

```powershell
python -m pytest -q
```

Kết quả kiểm thử của branch P5 tại thời điểm hoàn thiện:

```text
262 passed
```

---

## 7. Chạy riêng test của P5

### 7.1. Test PODEM

```powershell
python -m pytest tests/test_podem.py -q
```

Kết quả hiện tại:

```text
32 passed
```

### 7.2. Test logic 5 giá trị

```powershell
python -m pytest tests/test_logic.py -q
```

Kết quả hiện tại:

```text
220 passed
```

### 7.3. Test riêng XOR/XNOR

```powershell
python -m pytest tests/test_logic.py -q -k "xor or xnor"
```

Lệnh này dùng để kiểm tra riêng các trường hợp XOR/XNOR được bổ sung theo P3-v1.1.

---

## 8. Các nội dung P5 đã được kiểm thử

Branch P5 hiện đã kiểm thử các nội dung chính:

- Logic 5 giá trị: `0`, `1`, `X`, `D`, `D'`
- Objective và Backtrace cho các cổng logic
- Objective và Backtrace cho XOR/XNOR
- D-frontier
- Backtracking
- Fault-frame
- Fault injection
- Stem fault và branch fault
- Sequential/unroll
- Các ví dụ PODEM từ P3
- Trace sau backtrack được cập nhật lại theo trạng thái mới

---

## 9. Quy trình chạy nhanh

Sau khi đã clone repository và cài môi trường, có thể chạy theo thứ tự:

```powershell
cd dft-atpg
git checkout p5-podem-code
git pull origin p5-podem-code
.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "src"
python -m pytest -q
```

Nếu kết quả là:

```text
262 passed
```

thì toàn bộ test hiện tại của branch P5 đã chạy thành công.

---

## 10. Kiểm tra thay đổi trước khi commit

Kiểm tra trạng thái repository:

```powershell
git status --short
```

Kiểm tra tổng quan thay đổi:

```powershell
git diff --stat
```

Kiểm tra lỗi whitespace:

```powershell
git diff --check
```

Xem toàn bộ nội dung thay đổi:

```powershell
git diff
```

---

## 11. Lưu ý

- Không tự ý sửa các file ngoài phạm vi công việc đang được giao.
- Khi phát hiện test fail, cần kiểm tra nguyên nhân trước khi sửa code.
- Không sử dụng kết quả test của máy khác để thay thế cho việc kiểm tra trên máy hiện tại.
- P5 hiện tập trung vào phần cài đặt PODEM và các test liên quan.
- Việc xác nhận pattern bằng fault simulator P6 sẽ được thực hiện khi phần P6 hoàn thiện.

---