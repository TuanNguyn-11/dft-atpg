# Bằng chứng P3 đối chiếu code thật — 06/10/2026

- Checkout HEAD khi chạy: `8564678cd360594cbd540389d49c99021525ac08`.
- Python: `3.12.10`; lệnh: `python -B notes/p3_doi_chieu_code.py`.
- Dùng Circuit.from_bench, podem(trace=True), simulate/detects và exporter thật.
- PASS chỉ được ghi sau khi tất cả assertion đạt; không sửa golden hoặc trace P5.

## c17, 11/SA0

PASS: DETECTED, pattern `X10XX`, backtracks=0; file P5 tái sinh trùng nội dung.

| Hàng | Cột | Golden sau chuẩn hóa | API thực tế | File P5 sau chuẩn hóa | Đánh giá |
|---|---|---|---|---|---|
| 1 | Bước | 1 | 1 | 1 | Khớp giá trị |
| 1 | Objective (net, giá trị) | ["11", 1] | ["11", 1] | ["11", 1] | Khớp giá trị |
| 1 | Backtrace → PI | ["3", 0] | ["3", 0] | ["3", 0] | Khớp giá trị |
| 1 | Gán PI | "3=0" | "3=0" | "3=0" | Khớp giá trị |
| 1 | Giá trị các net sau imply | {"1": "X", "10": "1", "11": "D", "16": "X", "19": "X", "2": "X", "22": "X", "23": "X", "3": "0", "6": "X", "7": "X"} | {"1": "X", "10": "1", "11": "D", "16": "X", "19": "X", "2": "X", "22": "X", "23": "X", "3": "0", "6": "X", "7": "X"} | {"1": "X", "10": "1", "11": "D", "16": "X", "19": "X", "2": "X", "22": "X", "23": "X", "3": "0", "6": "X", "7": "X"} | Khớp giá trị |
| 1 | D-frontier | ["16", "19"] | ["16", "19"] | ["16", "19"] | Khớp giá trị |
| 1 | Hành động | "tiếp tục" | "tiếp tục" | "tiếp tục" | Khớp giá trị |
| 2 | Bước | 2 | 2 | 2 | Khớp giá trị |
| 2 | Objective (net, giá trị) | ["2", 1] | ["2", 1] | ["2", 1] | Khớp giá trị |
| 2 | Backtrace → PI | ["2", 1] | ["2", 1] | ["2", 1] | Khớp giá trị |
| 2 | Gán PI | "2=1" | "2=1" | "2=1" | Khớp giá trị |
| 2 | Giá trị các net sau imply | {"1": "X", "10": "1", "11": "D", "16": "D'", "19": "X", "2": "1", "22": "D", "23": "X", "3": "0", "6": "X", "7": "X"} | {"1": "X", "10": "1", "11": "D", "16": "D'", "19": "X", "2": "1", "22": "D", "23": "X", "3": "0", "6": "X", "7": "X"} | {"1": "X", "10": "1", "11": "D", "16": "D'", "19": "X", "2": "1", "22": "D", "23": "X", "3": "0", "6": "X", "7": "X"} | Khớp giá trị |
| 2 | D-frontier | ["19", "23"] | ["19", "23"] | ["19", "23"] | Khớp giá trị |
| 2 | Hành động | "thành công" | "thành công" | "thành công" | Khớp giá trị |

Simulator P6: 8/8 cách điền X phát hiện; điền X=0: PO tốt (1, 1), lỗi (0, 0).

## backtrack_example, t/SA0

PASS: DETECTED, pattern `01`, backtracks=1; file P5 tái sinh trùng nội dung.

| Hàng | Cột | Golden sau chuẩn hóa | API thực tế | File P5 sau chuẩn hóa | Đánh giá |
|---|---|---|---|---|---|
| 1 | Bước | 1 | 1 | 1 | Khớp giá trị |
| 1 | Objective (net, giá trị) | ["t", 1] | ["t", 1] | ["t", 1] | Khớp giá trị |
| 1 | Backtrace → PI | ["a", 1] | ["a", 1] | ["a", 1] | Khớp giá trị |
| 1 | Gán PI | "a=1" | "a=1" | "a=1" | Khớp giá trị |
| 1 | Giá trị các net sau imply | {"a": "1", "b": "X", "n": "0", "out": "0", "t": "D"} | {"a": "1", "b": "X", "n": "0", "out": "0", "t": "D"} | {"a": "1", "b": "X", "n": "0", "out": "0", "t": "D"} | Khớp giá trị |
| 1 | D-frontier | [] | [] | [] | Khớp giá trị |
| 1 | Hành động | "backtrack" | "tiếp tục" | "backtrack" | Khác ngữ nghĩa API; exporter khớp |
| 2 | Bước | 2 | 2 | 2 | Khớp giá trị |
| 2 | Objective (net, giá trị) | null | null | null | Khớp giá trị |
| 2 | Backtrace → PI | null | null | null | Khớp giá trị |
| 2 | Gán PI | "a=0" | "a=0" | "a=0" | Khớp giá trị |
| 2 | Giá trị các net sau imply | {"a": "0", "b": "X", "n": "1", "out": "X", "t": "X"} | {"a": "0", "b": "X", "n": "1", "out": "X", "t": "X"} | {"a": "0", "b": "X", "n": "1", "out": "X", "t": "X"} | Khớp giá trị |
| 2 | D-frontier | [] | [] | [] | Khớp giá trị |
| 2 | Hành động | "tiếp tục" | "backtrack" | "tiếp tục" | Khác ngữ nghĩa API; exporter khớp |
| 3 | Bước | 3 | 3 | 3 | Khớp giá trị |
| 3 | Objective (net, giá trị) | ["t", 1] | ["t", 1] | ["t", 1] | Khớp giá trị |
| 3 | Backtrace → PI | ["b", 1] | ["b", 1] | ["b", 1] | Khớp giá trị |
| 3 | Gán PI | "b=1" | "b=1" | "b=1" | Khớp giá trị |
| 3 | Giá trị các net sau imply | {"a": "0", "b": "1", "n": "1", "out": "D", "t": "D"} | {"a": "0", "b": "1", "n": "1", "out": "D", "t": "D"} | {"a": "0", "b": "1", "n": "1", "out": "D", "t": "D"} | Khớp giá trị |
| 3 | D-frontier | [] | [] | [] | Khớp giá trị |
| 3 | Hành động | "thành công" | "thành công" | "thành công" | Khớp giá trị |

Simulator P6: 1/1 cách điền X phát hiện; điền X=0: PO tốt (1,), lỗi (0,).

Giới hạn 0: ABORTED, pattern 1X, backtracks=0; API có hàng kết thúc không gán PI,
exporter gộp vào kết luận và giữ một hàng gán với hành động backtrack (bị chặn).
Giới hạn 1: DETECTED, pattern 01, backtracks=1. Không coi nhãn thất bại của hàng cuối API là UNTESTABLE.

## Phạm vi

35 ô (5 hàng × 7 cột) được so giữa golden/API/file P5, bao gồm đầy đủ PI/net và thứ tự frontier.
Chuẩn hóa cách viết tuple/đường backtrace và PI nhóm; hai khác biệt hành động API được kiểm tra tường minh.
Không chứng minh mọi mạch/lỗi hoặc mọi heuristic bằng hai ví dụ này.
