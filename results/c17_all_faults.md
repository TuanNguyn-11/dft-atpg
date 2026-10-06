# Ket qua toan bo loi - c17

Thuat toan sinh pattern: PODEM. Tong thoi gian: 0.004 s. Pattern co X duoc dien 0 khi mo phong loi.

| PI | PO | cong | DFF |
|---|---|---|---|
| 5 | 2 | 6 | 0 |

So loi truoc gop: 34; sau gop (equivalence): 22.

| Loi | Trang thai | Pattern | Backtrack | Kiem chung | Moi cach dien X |
|---|---|---|---|---|---|
| 1/SA1 | DETECTED | 001XX | 0 | OK | co |
| 2/SA1 | DETECTED | X00XX | 0 | OK | co |
| 3/SA0 | DETECTED | 11111 | 0 | OK | co |
| 3/SA1 | DETECTED | 11011 | 0 | OK | co |
| 3->10/SA1 | DETECTED | 100XX | 0 | OK | co |
| 3->11/SA1 | DETECTED | X101X | 0 | OK | co |
| 6/SA1 | DETECTED | X1101 | 0 | OK | co |
| 7/SA1 | DETECTED | X00X0 | 0 | OK | co |
| 10/SA1 | DETECTED | 101XX | 0 | OK | co |
| 11/SA0 | DETECTED | X10XX | 0 | OK | co |
| 11/SA1 | DETECTED | X1111 | 0 | OK | co |
| 11->16/SA1 | DETECTED | X111X | 0 | OK | co |
| 11->19/SA1 | DETECTED | XX111 | 0 | OK | co |
| 16/SA0 | DETECTED | 00XXX | 0 | OK | co |
| 16/SA1 | DETECTED | X10XX | 0 | OK | co |
| 16->22/SA1 | DETECTED | X10XX | 0 | OK | co |
| 16->23/SA1 | DETECTED | X10X0 | 0 | OK | co |
| 19/SA1 | DETECTED | X00X1 | 0 | OK | co |
| 22/SA0 | DETECTED | 1X1XX | 0 | OK | co |
| 22/SA1 | DETECTED | 00XXX | 0 | OK | co |
| 23/SA0 | DETECTED | X10XX | 0 | OK | co |
| 23/SA1 | DETECTED | X011X | 0 | OK | co |

| Chi so | Gia tri |
|---|---|
| Fault coverage (DETECTED / tong) | 22/22 = 100.0% |
| Test coverage (DETECTED / (tong - UNTESTABLE)) | 22/22 = 100.0% |
| Fault efficiency ((DETECTED + UNTESTABLE) / tong) | 22/22 = 100.0% |
| ABORTED | 0 |
| Backtrack trung binh | 0.00 |
| Pattern truoc nen | 22 |
| Pattern sau nen | 6 (phu 22/22 loi) |
| Pattern bi kiem chung SAI | 0 |
| Pattern co X ma co cach dien X khong phat hien | 0 |
| Pattern chua kiem chung het moi cach dien X (>16 bit X) | 0 |
