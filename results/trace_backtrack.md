# Trace PODEM — backtrack_example, t/SA0

- PI theo thứ tự .bench: (a,b)
- PO theo thứ tự .bench: (out)
- Topological order: (t,n,out)
- Fault: `t/SA0` (stem)
- Status: `DETECTED`
- Pattern: `01`
- Backtracks: `1`
- Quy ước: mỗi hàng là một lần gán/đảo PI sau imply; Objective và Backtrace dùng `—` khi đảo quyết định; hành động ở hàng trước ghi nhận nhánh dẫn tới backtrack.

| Bước | Objective (net, giá trị) | Backtrace → PI | Gán PI | Giá trị các net sau imply | D-frontier | Hành động |
|---|---|---|---|---|---|---|
| 1 | (t,1) | (a,1) | a=1 | PI=(1,X); t=D, n=0, out=0 | ∅ | backtrack |
| 2 | — | — | a=0 | PI=(0,X); t=X, n=1, out=X | ∅ | tiếp tục |
| 3 | (t,1) | (b,1) | b=1 | PI=(0,1); t=D, n=1, out=D | ∅ | thành công |

## Kết luận

- Status: `DETECTED`
- Pattern: `01`
- Backtracks: `1`
