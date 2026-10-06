# Ket qua toan bo loi - c17

## Moi truong va tai lap

- Lenh tai tao (tu goc repo, PYTHONPATH=src): `python -m atpg.run circuits/c17.bench --all --no-collapse --md results/p1_c17_all.md`
- Python 3.12.15 (CPython), Windows 11
- Commit ma nguon: cb2be0e
- Thoi diem chay: 2026-10-06T20:36:38
- Thu tu PI trong cot pattern: 1, 2, 3, 6, 7
- Pham vi loi goc: 34 loi = 22 stem + 12 nhanh
- Dang chay 34 loi goc, khong gop.
- Pattern co X duoc dien 0 khi mo phong loi; cot "Moi cach dien X" la vet can moi cach dien (toi da 16 bit X).
- Thoi gian sinh pattern: 0.0020 s (time.perf_counter, chi tinh bo sinh pattern); ca kiem chung va nen: 0.0089 s. So do phu thuoc may chay.

| PI | PO | cong | DFF |
|---|---|---|---|
| 5 | 2 | 6 | 0 |

So loi truoc gop: 34; sau gop (equivalence): 22.

## Ket qua tung loi

| Loi | Trang thai | Pattern | Thuat toan | Backtrack | Kiem chung | Moi cach dien X |
|---|---|---|---|---|---|---|
| 1/SA0 | DETECTED | 101XX | PODEM | 0 | OK | co |
| 1/SA1 | DETECTED | 001XX | PODEM | 0 | OK | co |
| 2/SA0 | DETECTED | X10XX | PODEM | 0 | OK | co |
| 2/SA1 | DETECTED | X00XX | PODEM | 0 | OK | co |
| 3/SA0 | DETECTED | 11111 | PODEM | 0 | OK | co |
| 3/SA1 | DETECTED | 11011 | PODEM | 0 | OK | co |
| 3->10/SA0 | DETECTED | 101XX | PODEM | 0 | OK | co |
| 3->10/SA1 | DETECTED | 100XX | PODEM | 0 | OK | co |
| 3->11/SA0 | DETECTED | X1111 | PODEM | 0 | OK | co |
| 3->11/SA1 | DETECTED | X101X | PODEM | 0 | OK | co |
| 6/SA0 | DETECTED | X1111 | PODEM | 0 | OK | co |
| 6/SA1 | DETECTED | X1101 | PODEM | 0 | OK | co |
| 7/SA0 | DETECTED | X00X1 | PODEM | 0 | OK | co |
| 7/SA1 | DETECTED | X00X0 | PODEM | 0 | OK | co |
| 10/SA0 | DETECTED | 00XXX | PODEM | 0 | OK | co |
| 10/SA1 | DETECTED | 101XX | PODEM | 0 | OK | co |
| 11/SA0 | DETECTED | X10XX | PODEM | 0 | OK | co |
| 11/SA1 | DETECTED | X1111 | PODEM | 0 | OK | co |
| 11->16/SA0 | DETECTED | X10XX | PODEM | 0 | OK | co |
| 11->16/SA1 | DETECTED | X111X | PODEM | 0 | OK | co |
| 11->19/SA0 | DETECTED | X00X1 | PODEM | 0 | OK | co |
| 11->19/SA1 | DETECTED | XX111 | PODEM | 0 | OK | co |
| 16/SA0 | DETECTED | 00XXX | PODEM | 0 | OK | co |
| 16/SA1 | DETECTED | X10XX | PODEM | 0 | OK | co |
| 16->22/SA0 | DETECTED | 00XXX | PODEM | 0 | OK | co |
| 16->22/SA1 | DETECTED | X10XX | PODEM | 0 | OK | co |
| 16->23/SA0 | DETECTED | X011X | PODEM | 0 | OK | co |
| 16->23/SA1 | DETECTED | X10X0 | PODEM | 0 | OK | co |
| 19/SA0 | DETECTED | XX11X | PODEM | 0 | OK | co |
| 19/SA1 | DETECTED | X00X1 | PODEM | 0 | OK | co |
| 22/SA0 | DETECTED | 1X1XX | PODEM | 0 | OK | co |
| 22/SA1 | DETECTED | 00XXX | PODEM | 0 | OK | co |
| 23/SA0 | DETECTED | X10XX | PODEM | 0 | OK | co |
| 23/SA1 | DETECTED | X011X | PODEM | 0 | OK | co |

## Tong hop

| Chi so | Gia tri |
|---|---|
| Fault coverage (DETECTED / tong) | 34/34 = 100.0% |
| Test coverage (DETECTED / (tong - UNTESTABLE)) | 34/34 = 100.0% |
| Fault efficiency ((DETECTED + UNTESTABLE) / tong) | 34/34 = 100.0% |
| ABORTED | 0 |
| Backtrack trung binh | 0.00 |
| Pattern truoc nen | 34 |
| Pattern sau nen | 7 (phu 34/34 loi dang chay) |
| Tap sau nen phu toan bo loi goc (34 loi) | 34/34 = 100.0% |
| Pattern bi kiem chung SAI | 0 |
| Pattern co X ma co cach dien X khong phat hien | 0 |
| Pattern chua kiem chung het moi cach dien X (>16 bit X) | 0 |

## Tap test sau nen (X da dien 0; thu tu PI: 1, 2, 3, 6, 7)

| # | Pattern |
|---|---|
| 1 | 00100 |
| 2 | 01000 |
| 3 | 11111 |
| 4 | 11011 |
| 5 | 10000 |
| 6 | 01101 |
| 7 | 00001 |
