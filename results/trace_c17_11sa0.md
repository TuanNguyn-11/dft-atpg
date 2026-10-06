# Trace P5 — c17, 11/SA0

PI = (1,2,3,6,7)

PO = (22,23)

Topo order = (10,11,16,19,22,23)

| Bước | Objective (net, giá trị) | Backtrace → PI | Gán PI | Giá trị các net sau imply | D-frontier | Hành động |
|---|--------|-----|-----|-------------------------------------|---------|------------|
| 1 | (11,1) | 3=0 | 3=0 | 10=1, 11=D, 16=X, 19=X, 22=X, 23=X  | {16,19} | tiếp tục   |
| 2 | (2,1)  | 2=1 | 2=1 | 10=1, 11=D, 16=D', 19=X, 22=D, 23=X | {19,23} | thành công |

## Kết quả

- Status: `DETECTED`
- Pattern: `X10XX`
- Backtracks: `0`
- PO chứa D: `22`