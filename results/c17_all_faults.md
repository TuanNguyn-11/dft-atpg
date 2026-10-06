# Ket qua toan bo loi - c17

Thuat toan sinh pattern: vet can (tham chieu). Tong thoi gian: 0.006 s. Pattern co X duoc dien 0 khi mo phong loi.

| PI | PO | cong | DFF |
|---|---|---|---|
| 5 | 2 | 6 | 0 |

So loi truoc gop: 34; sau gop (equivalence): 22.

| Loi | Trang thai | Pattern | Backtrack | Kiem chung | Moi cach dien X |
|---|---|---|---|---|---|
| 1/SA1 | DETECTED | 001XX | - | OK | co |
| 2/SA1 | DETECTED | X0X00 | - | OK | co |
| 3/SA0 | DETECTED | XX111 | - | OK | co |
| 3/SA1 | DETECTED | XX011 | - | OK | co |
| 3->10/SA1 | DETECTED | 100XX | - | OK | co |
| 3->11/SA1 | DETECTED | XX011 | - | OK | co |
| 6/SA1 | DETECTED | XX101 | - | OK | co |
| 7/SA1 | DETECTED | X0X00 | - | OK | co |
| 10/SA1 | DETECTED | 101XX | - | OK | co |
| 11/SA0 | DETECTED | XXX01 | - | OK | co |
| 11/SA1 | DETECTED | XX111 | - | OK | co |
| 11->16/SA1 | DETECTED | X111X | - | OK | co |
| 11->19/SA1 | DETECTED | XX111 | - | OK | co |
| 16/SA0 | DETECTED | X0XX0 | - | OK | co |
| 16/SA1 | DETECTED | X1X00 | - | OK | co |
| 16->22/SA1 | DETECTED | X10XX | - | OK | co |
| 16->23/SA1 | DETECTED | X1X00 | - | OK | co |
| 19/SA1 | DETECTED | X0X01 | - | OK | co |
| 22/SA0 | DETECTED | X1X0X | - | OK | co |
| 22/SA1 | DETECTED | X00XX | - | OK | co |
| 23/SA0 | DETECTED | XXX01 | - | OK | co |
| 23/SA1 | DETECTED | X0XX0 | - | OK | co |

| Chi so | Gia tri |
|---|---|
| Fault coverage (DETECTED / tong) | 22/22 = 100.0% |
| Test coverage (DETECTED / (tong - UNTESTABLE)) | 22/22 = 100.0% |
| Fault efficiency ((DETECTED + UNTESTABLE) / tong) | 22/22 = 100.0% |
| ABORTED | 0 |
| Backtrack trung binh | - |
| Pattern truoc nen | 22 |
| Pattern sau nen | 7 (phu 22/22 loi) |
| Pattern bi kiem chung SAI | 0 |
| Pattern co X ma co cach dien X khong phat hien | 0 |
| Pattern chua kiem chung het moi cach dien X (>16 bit X) | 0 |
