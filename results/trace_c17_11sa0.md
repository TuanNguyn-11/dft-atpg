# Trace PODEM — c17, 11/SA0

- PI theo thứ tự .bench: (1,2,3,6,7)
- PO theo thứ tự .bench: (22,23)
- Topological order: (10,11,16,19,22,23)
- Fault: `11/SA0` (stem)
- Status: `DETECTED`
- Pattern: `X10XX`
- Backtracks: `0`
- Quy ước: mỗi hàng là một lần gán/đảo PI sau imply; Objective và Backtrace dùng `—` khi đảo quyết định; hành động ở hàng trước ghi nhận nhánh dẫn tới backtrack.

| Bước | Objective (net, giá trị) | Backtrace → PI | Gán PI | Giá trị các net sau imply | D-frontier | Hành động |
|---|---|---|---|---|---|---|
| 1 | (11,1) | (3,0) | 3=0 | PI=(X,X,0,X,X); 10=1, 11=D, 16=X, 19=X, 22=X, 23=X | {16,19} | tiếp tục |
| 2 | (2,1) | (2,1) | 2=1 | PI=(X,1,0,X,X); 10=1, 11=D, 16=D', 19=X, 22=D, 23=X | {19,23} | thành công |

## Kết luận

- Status: `DETECTED`
- Pattern: `X10XX`
- Backtracks: `0`
