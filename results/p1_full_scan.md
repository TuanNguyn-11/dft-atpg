# Full scan qua API thật — 06/10/2026
Python 3.12.15; base `8564678cd360594cbd540389d49c99021525ac08` + P1.
Tái lập: `python scripts/p1_verify_release.py`.
PI: ['A', 'B', 'Q']; PO: ['Y', 'D']. Q là pseudo-PI, D là pseudo-PO.
| Lỗi stem | Pattern (thứ tự PI trên) | Trạng thái | Mọi cách điền X |
|---|---|---|---|
| A/SA0 | 111 | DETECTED | Đạt |
| A/SA1 | 011 | DETECTED | Đạt |
| B/SA0 | 110 | DETECTED | Đạt |
| B/SA1 | 100 | DETECTED | Đạt |
| Q/SA0 | 101 | DETECTED | Đạt |
| Q/SA1 | 100 | DETECTED | Đạt |
| N1/SA0 | 111 | DETECTED | Đạt |
| N1/SA1 | 110 | DETECTED | Đạt |
| N2/SA0 | 100 | DETECTED | Đạt |
| N2/SA1 | 110 | DETECTED | Đạt |
| N4/SA0 | 110 | DETECTED | Đạt |
| N4/SA1 | 100 | DETECTED | Đạt |
| N3/SA0 | 1X1 | DETECTED | Đạt |
| N3/SA1 | 110 | DETECTED | Đạt |
| Y/SA0 | 110 | DETECTED | Đạt |
| Y/SA1 | X00 | DETECTED | Đạt |
| D/SA0 | 0XX | DETECTED | Đạt |
| D/SA1 | 1X1 | DETECTED | Đạt |

Kết quả: 18/18 lỗi stem, PODEM thật + simulator P6 + oracle P4.
