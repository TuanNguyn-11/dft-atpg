# Kiểm chứng P1 — 06/10/2026

Python 3.12.15; base `cb2be0e3b4fade5f597cd5039f7feea89efa730f` + thay đổi P1 trong working tree.

## `python -m pytest -q`

Exit 0

```text
........................................................................ [ 21%]
........................................................................ [ 43%]
........................................................................ [ 64%]
........................................................................ [ 86%]
..............................................                           [100%]
334 passed in 2.56s
```

## `python scripts/check_p1_examples.py`

Exit 0

```text
PASS: collapsing (32 vectors); c17 cube (8 completions); SCOAP (11 nets)
PASS: Figure 4.5 (8 vectors), detects y/SA0: 011, 110
SCOAP: net CC0 CC1 CO
1 1 1 5
2 1 1 6
3 1 1 5
6 1 1 7
7 1 1 6
10 3 2 3
11 3 2 5
16 4 2 3
19 4 2 3
22 5 4 0
23 5 5 0
```

## `python notes/p2_kiem_chung.py`

Exit 0

```text
PASS: 160 cells vs independent binary-completion oracle
PASS: four trace stages, D-frontier and J-frontier
PASS: c17 cube, 4 completions
PASS: c17 cube, 8 completions
PASS: four documented binary PO pairs
```

## `python notes/p3_kiem_tra_ban_giao.py`

Exit 0

```text
PASS: c17.bench agrees with specification
PASS: golden_trace_c17_11sa0.md: 2 rows, pattern=X10XX, backtracks=0
PASS: golden_trace_backtrack.md: 3 rows, pattern=01, backtracks=1
PASS: auxiliary netlist, P3 labels/citations/chapter and 3 slide frames
```

## `python scripts/p4_seq_experiment.py`

Exit 0

```text
PI=2, PO=1, cong to hop=6, DFF=1
Stem stuck-at faults=18; khong fault collapsing
fault | scan A,B,Q | sequence A,B (Q0 bat ky)
--- | --- | ---
A/SA0 | (1, 0, 0) | ((0, 0), (1, 0))
A/SA1 | (0, 0, 0) | ((0, 0), (0, 1))
B/SA0 | (1, 1, 0) | ((0, 0), (1, 1))
B/SA1 | (1, 0, 0) | ((0, 0), (1, 0))
N1/SA0 | (1, 1, 1) | ((0, 0), (1, 1), (1, 0))
N1/SA1 | (1, 1, 0) | ((1, 0), (1, 1), (1, 0))
N2/SA0 | (1, 0, 0) | ((1, 0), (1, 0), (1, 0))
N2/SA1 | (1, 1, 0) | ((1, 0), (1, 1), (1, 0))
N3/SA0 | (1, 0, 0) | ((1, 0), (1, 0))
N3/SA1 | (1, 1, 0) | ((1, 0), (1, 1), (1, 0))
D/SA0 | (0, 0, 0) | ((0, 0), (1, 0))
D/SA1 | (1, 0, 0) | ((1, 0), (1, 0))
Q/SA0 | (1, 0, 1) | ((0, 0), (1, 0))
Q/SA1 | (1, 0, 0) | ((1, 0), (1, 0))
N4/SA0 | (1, 0, 1) | ((0, 0), (1, 0))
N4/SA1 | (1, 0, 0) | ((0, 0), (1, 1))
Y/SA0 | (1, 0, 1) | ((0, 0), (1, 0))
Y/SA1 | (0, 0, 0) | ((0, 0),)
Full scan: 18/18
Unroll <=4 khung, test doc lap Q0: 18/18
Gioi han 1 khung: 1/18
Gioi han 2 khung: 13/18
Gioi han 3 khung: 18/18
Gioi han 4 khung: 18/18
```

## `python -m atpg.run circuits/c17.bench --fault 11 0 --trace`

Exit 0

```text
Mach c17: 5 PI, 2 PO, 6 cong, 0 DFF
11/SA0: DETECTED, pattern X10XX, backtrack 0 (PODEM)
Kiem chung bang fault simulation: OK; moi cach dien X deu phat hien: co

Trace mo phong (X dien 0 -> 01000)
| net | mach tot | mach loi | gia tri 5 |
|---|---|---|---|
| 1 | 0 | 0 | 0 |
| 2 | 1 | 1 | 1 |
| 3 | 0 | 0 | 0 |
| 6 | 0 | 0 | 0 |
| 7 | 0 | 0 | 0 |
| 10 | 1 | 1 | 1 |
| 11 | 1 | 0 | D |
| 16 | 0 | 1 | D' |
| 19 | 1 | 1 | 1 |
| 22 | 1 | 0 | D |
| 23 | 1 | 0 | D |

Phat hien tai PO: 22, 23

Trace PODEM (P5):
| Bước | Objective (net, giá trị) | Backtrace → PI | Gán PI | Giá trị các net sau imply | D-frontier | Hành động |
|---|---|---|---|---|---|---|
| 1 | ('11', 1) | ('3', 0) | 3=0 | {'1': 'X', '2': 'X', '3': '0', '6': 'X', '7': 'X', '10': '1', '11': 'D', '16': 'X', '19': 'X', '22': 'X', '23': 'X'} | ['16', '19'] | tiếp tục |
| 2 | ('2', 1) | ('2', 1) | 2=1 | {'1': 'X', '2': '1', '3': '0', '6': 'X', '7': 'X', '10': '1', '11': 'D', '16': "D'", '19': 'X', '22': 'D', '23': 'X'} | ['19', '23'] | thành công |
```

## `python -m atpg.run circuits/backtrack_example.bench --fault t 0 --trace`

Exit 0

```text
Mach backtrack_example: 2 PI, 1 PO, 3 cong, 0 DFF
t/SA0: DETECTED, pattern 01, backtrack 1 (PODEM)
Kiem chung bang fault simulation: OK; moi cach dien X deu phat hien: co

Trace mo phong (X dien 0 -> 01)
| net | mach tot | mach loi | gia tri 5 |
|---|---|---|---|
| a | 0 | 0 | 0 |
| b | 1 | 1 | 1 |
| t | 1 | 0 | D |
| n | 1 | 1 | 1 |
| out | 1 | 0 | D |

Phat hien tai PO: out

Trace PODEM (P5):
| Bước | Objective (net, giá trị) | Backtrace → PI | Gán PI | Giá trị các net sau imply | D-frontier | Hành động |
|---|---|---|---|---|---|---|
| 1 | ('t', 1) | ('a', 1) | a=1 | {'a': '1', 'b': 'X', 't': 'D', 'n': '0', 'out': '0'} | [] | tiếp tục |
| 2 | None | None | a=0 | {'a': '0', 'b': 'X', 't': 'X', 'n': '1', 'out': 'X'} | [] | backtrack |
| 3 | ('t', 1) | ('b', 1) | b=1 | {'a': '0', 'b': '1', 't': 'D', 'n': '1', 'out': 'D'} | [] | thành công |
```

## `python -m atpg.run circuits/c17.bench --all --md results/p1_c17_collapsed.md`

Exit 0

```text
Mach c17: 5 PI, 2 PO, 6 cong, 0 DFF
# Ket qua toan bo loi - c17

## Moi truong va tai lap

- Lenh tai tao (tu goc repo, PYTHONPATH=src): `python -m atpg.run circuits/c17.bench --all --md results/p1_c17_collapsed.md`
- Python 3.12.15 (CPython), Windows 11
- Commit ma nguon: cb2be0e
- Thoi diem chay: 2026-10-06T20:36:38
- Thu tu PI trong cot pattern: 1, 2, 3, 6, 7
- Pham vi loi goc: 34 loi = 22 stem + 12 nhanh
- Dang chay 22 loi dai dien sau gop tuong duong (tu 34 loi goc). Tap 22 loi dai dien nay KHAC tap 22 loi stem, du hai so co the trung nhau.
- Pattern co X duoc dien 0 khi mo phong loi; cot "Moi cach dien X" la vet can moi cach dien (toi da 16 bit X).
- Thoi gian sinh pattern: 0.0015 s (time.perf_counter, chi tinh bo sinh pattern); ca kiem chung va nen: 0.0057 s. So do phu thuoc may chay.

| PI | PO | cong | DFF |
|---|---|---|---|
| 5 | 2 | 6 | 0 |

So loi truoc gop: 34; sau gop (equivalence): 22.

## Ket qua tung loi

| Loi | Trang thai | Pattern | Thuat toan | Backtrack | Kiem chung | Moi cach dien X |
|---|---|---|---|---|---|---|
| 1/SA1 | DETECTED | 001XX | PODEM | 0 | OK | co |
| 2/SA1 | DETECTED | X00XX | PODEM | 0 | OK | co |
| 3/SA0 | DETECTED | 11111 | PODEM | 0 | OK | co |
| 3/SA1 | DETECTED | 11011 | PODEM | 0 | OK | co |
| 3->10/SA1 | DETECTED | 100XX | PODEM | 0 | OK | co |
| 3->11/SA1 | DETECTED | X101X | PODEM | 0 | OK | co |
| 6/SA1 | DETECTED | X1101 | PODEM | 0 | OK | co |
| 7/SA1 | DETECTED | X00X0 | PODEM | 0 | OK | co |
| 10/SA1 | DETECTED | 101XX | PODEM | 0 | OK | co |
| 11/SA0 | DETECTED | X10XX | PODEM | 0 | OK | co |
| 11/SA1 | DETECTED | X1111 | PODEM | 0 | OK | co |
| 11->16/SA1 | DETECTED | X111X | PODEM | 0 | OK | co |
| 11->19/SA1 | DETECTED | XX111 | PODEM | 0 | OK | co |
| 16/SA0 | DETECTED | 00XXX | PODEM | 0 | OK | co |
| 16/SA1 | DETECTED | X10XX | PODEM | 0 | OK | co |
| 16->22/SA1 | DETECTED | X10XX | PODEM | 0 | OK | co |
| 16->23/SA1 | DETECTED | X10X0 | PODEM | 0 | OK | co |
| 19/SA1 | DETECTED | X00X1 | PODEM | 0 | OK | co |
| 22/SA0 | DETECTED | 1X1XX | PODEM | 0 | OK | co |
| 22/SA1 | DETECTED | 00XXX | PODEM | 0 | OK | co |
| 23/SA0 | DETECTED | X10XX | PODEM | 0 | OK | co |
| 23/SA1 | DETECTED | X011X | PODEM | 0 | OK | co |

## Tong hop

| Chi so | Gia tri |
|---|---|
| Fault coverage (DETECTED / tong) | 22/22 = 100.0% |
| Test coverage (DETECTED / (tong - UNTESTABLE)) | 22/22 = 100.0% |
| Fault efficiency ((DETECTED + UNTESTABLE) / tong) | 22/22 = 100.0% |
| ABORTED | 0 |
| Backtrack trung binh | 0.00 |
| Pattern truoc nen | 22 |
| Pattern sau nen | 6 (phu 22/22 loi dang chay) |
| Tap sau nen phu toan bo loi goc (34 loi) | 34/34 = 100.0% |
| Pattern bi kiem chung SAI | 0 |
| Pattern co X ma co cach dien X khong phat hien | 0 |
| Pattern chua kiem chung het moi cach dien X (>16 bit X) | 0 |

## Tap test sau nen (X da dien 0; thu tu PI: 1, 2, 3, 6, 7)

| # | Pattern |
|---|---|
| 1 | 00100 |
| 2 | 11111 |
| 3 | 10000 |
| 4 | 01010 |
| 5 | 01101 |
| 6 | 00001 |

Da ghi results/p1_c17_collapsed.md
```

## `python -m atpg.run circuits/c17.bench --all --no-collapse --md results/p1_c17_all.md`

Exit 0

```text
Mach c17: 5 PI, 2 PO, 6 cong, 0 DFF
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

Da ghi results/p1_c17_all.md
```

## `python -m atpg.run circuits/seq_example.bench --unroll 1 --all --md results/p1_seq_k1.md`

Exit 0

```text
Mach seq_example_unroll_1: 3 PI, 1 PO, 6 cong, 0 DFF
# Ket qua mach tuan tu - seq_example, trai 1 khung

Che do: trang thai dau Q@0 CHUA BIET (khong scan/reset). `DETECTED` nghia la phat hien BAO DAM voi moi trang thai dau cua mach tot va mach loi (cung dinh nghia voi scripts/p4_seq_experiment.py); pattern chi con cac PI dieu khien duoc, Q@0 khong nam trong pattern.

## Moi truong va tai lap

- Lenh tai tao (tu goc repo, PYTHONPATH=src): `python -m atpg.run circuits/seq_example.bench --unroll 1 --all --md results/p1_seq_k1.md`
- Python 3.12.15 (CPython), Windows 11
- Commit ma nguon: cb2be0e
- Thoi diem chay: 2026-10-06T20:36:39
- Thu tu PI trong cot pattern: A, B
- Pham vi loi: 18 loi stem vat ly, moi loi cay vao ca 1 khung
- Nguon pattern theo hang (cot Thuat toan): PODEM, vet can chuoi (tham chieu)
- Tong thoi gian (sinh + kiem chung bao dam): 0.0035 s (time.perf_counter). So do phu thuoc may chay.

Pham vi: 18 loi stem vat ly cua seq_example (moi net 2 loi), moi loi duoc sao sang ca 1 khung; khong gop loi (equivalence cua mach to hop khong mac nhien dung cho mach tuan tu), khong co loi nhanh, mau so = 18.

| PI moi khung | PO moi khung | cong moi khung | DFF |
|---|---|---|---|
| 2 | 1 | 6 | 1 |

Pattern: moi nhom ky tu la cac PI (A, B) cua mot khung, theo thoi gian.

| Loi | Trang thai | Chuoi (PI moi khung) | Thuat toan | Backtrack | Pham vi dam bao |
|---|---|---|---|---|---|
| A/SA0 | CO DIEU KIEN Q@0 | 11 ; Q@0=0 | PODEM | 0 | chi khi Q@0 nhu ghi |
| A/SA1 | CO DIEU KIEN Q@0 | 01 ; Q@0=0 | PODEM | 0 | chi khi Q@0 nhu ghi |
| B/SA0 | CO DIEU KIEN Q@0 | 11 ; Q@0=0 | PODEM | 0 | chi khi Q@0 nhu ghi |
| B/SA1 | CO DIEU KIEN Q@0 | 10 ; Q@0=0 | PODEM | 0 | chi khi Q@0 nhu ghi |
| Q/SA0 | CO DIEU KIEN Q@0 | 10 ; Q@0=1 | PODEM | 0 | chi khi Q@0 nhu ghi |
| Q/SA1 | CO DIEU KIEN Q@0 | 10 ; Q@0=0 | PODEM | 0 | chi khi Q@0 nhu ghi |
| N1/SA0 | UNTESTABLE | 0X | PODEM | 2 | - |
| N1/SA1 | UNTESTABLE | 1X | PODEM | 2 | - |
| N2/SA0 | UNTESTABLE | X1 | PODEM | 1 | - |
| N2/SA1 | UNTESTABLE | X0 | PODEM | 1 | - |
| N4/SA0 | CO DIEU KIEN Q@0 | 11 ; Q@0=0 | PODEM | 0 | chi khi Q@0 nhu ghi |
| N4/SA1 | CO DIEU KIEN Q@0 | 10 ; Q@0=0 | PODEM | 0 | chi khi Q@0 nhu ghi |
| N3/SA0 | UNTESTABLE | 01 | PODEM | 4 | - |
| N3/SA1 | UNTESTABLE | 1X | PODEM | 4 | - |
| Y/SA0 | CO DIEU KIEN Q@0 | 11 ; Q@0=0 | PODEM | 0 | chi khi Q@0 nhu ghi |
| Y/SA1 | DETECTED | 0X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| D/SA0 | UNTESTABLE | 1X | PODEM | 3 | - |
| D/SA1 | UNTESTABLE | 0X | PODEM | 3 | - |

| Chi so | Gia tri |
|---|---|
| Phat hien BAO DAM (DETECTED / tong) | 1/18 = 5.6% |
| Chi phat hien CO DIEU KIEN Q@0 | 9 |
| Coverage neu Q@0 dieu khien duoc (scan/reset): (DETECTED + co dieu kien) / tong | 10/18 = 55.6% |
| UNTESTABLE (ke ca khi Q@0 dieu khien duoc, trong gioi han khung) | 8 |
| ABORTED | 0 |
| Chua kiem chung het | 0 |
| Ket luan UNTESTABLE bi kiem chung SAI (vet can tim ra pattern) | 0 |
| Nen tap test | khong ap dung o che do tran khung |

Da ghi results/p1_seq_k1.md
```

## `python -m atpg.run circuits/seq_example.bench --unroll 2 --all --md results/p1_seq_k2.md`

Exit 0

```text
Mach seq_example_unroll_2: 5 PI, 2 PO, 13 cong, 0 DFF
# Ket qua mach tuan tu - seq_example, trai 2 khung

Che do: trang thai dau Q@0 CHUA BIET (khong scan/reset). `DETECTED` nghia la phat hien BAO DAM voi moi trang thai dau cua mach tot va mach loi (cung dinh nghia voi scripts/p4_seq_experiment.py); pattern chi con cac PI dieu khien duoc, Q@0 khong nam trong pattern.

## Moi truong va tai lap

- Lenh tai tao (tu goc repo, PYTHONPATH=src): `python -m atpg.run circuits/seq_example.bench --unroll 2 --all --md results/p1_seq_k2.md`
- Python 3.12.15 (CPython), Windows 11
- Commit ma nguon: cb2be0e
- Thoi diem chay: 2026-10-06T20:36:39
- Thu tu PI trong cot pattern: A, B
- Pham vi loi: 18 loi stem vat ly, moi loi cay vao ca 2 khung
- Nguon pattern theo hang (cot Thuat toan): PODEM, vet can chuoi (tham chieu)
- Tong thoi gian (sinh + kiem chung bao dam): 0.0136 s (time.perf_counter). So do phu thuoc may chay.

Pham vi: 18 loi stem vat ly cua seq_example (moi net 2 loi), moi loi duoc sao sang ca 2 khung; khong gop loi (equivalence cua mach to hop khong mac nhien dung cho mach tuan tu), khong co loi nhanh, mau so = 18.

| PI moi khung | PO moi khung | cong moi khung | DFF |
|---|---|---|---|
| 2 | 1 | 6 | 1 |

Pattern: moi nhom ky tu la cac PI (A, B) cua mot khung, theo thoi gian.

| Loi | Trang thai | Chuoi (PI moi khung) | Thuat toan | Backtrack | Pham vi dam bao |
|---|---|---|---|---|---|
| A/SA0 | DETECTED | 11,11 | PODEM | 2 | bao dam moi trang thai dau |
| A/SA1 | DETECTED | 01,10 | PODEM | 0 | bao dam moi trang thai dau |
| B/SA0 | DETECTED | X0,11 | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| B/SA1 | DETECTED | 0X,10 | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| Q/SA0 | DETECTED | 0X,1X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| Q/SA1 | DETECTED | 1X,1X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| N1/SA0 | CO DIEU KIEN Q@0 | 11,10 ; Q@0=1 | PODEM | 0 | chi khi Q@0 nhu ghi |
| N1/SA1 | CO DIEU KIEN Q@0 | 11,10 ; Q@0=0 | PODEM | 1 | chi khi Q@0 nhu ghi |
| N2/SA0 | CO DIEU KIEN Q@0 | 10,10 ; Q@0=0 | PODEM | 1 | chi khi Q@0 nhu ghi |
| N2/SA1 | CO DIEU KIEN Q@0 | 11,10 ; Q@0=0 | PODEM | 1 | chi khi Q@0 nhu ghi |
| N4/SA0 | DETECTED | 0X,10 | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| N4/SA1 | DETECTED | 0X,11 | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| N3/SA0 | DETECTED | 10,1X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| N3/SA1 | CO DIEU KIEN Q@0 | 11,10 ; Q@0=0 | PODEM | 2 | chi khi Q@0 nhu ghi |
| Y/SA0 | DETECTED | 0X,10 | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| Y/SA1 | DETECTED | XX,0X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| D/SA0 | DETECTED | 0X,10 | PODEM | 0 | bao dam moi trang thai dau |
| D/SA1 | DETECTED | 10,1X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |

| Chi so | Gia tri |
|---|---|
| Phat hien BAO DAM (DETECTED / tong) | 13/18 = 72.2% |
| Chi phat hien CO DIEU KIEN Q@0 | 5 |
| Coverage neu Q@0 dieu khien duoc (scan/reset): (DETECTED + co dieu kien) / tong | 18/18 = 100.0% |
| UNTESTABLE (ke ca khi Q@0 dieu khien duoc, trong gioi han khung) | 0 |
| ABORTED | 0 |
| Chua kiem chung het | 0 |
| Ket luan UNTESTABLE bi kiem chung SAI (vet can tim ra pattern) | 0 |
| Nen tap test | khong ap dung o che do tran khung |

Da ghi results/p1_seq_k2.md
```

## `python -m atpg.run circuits/seq_example.bench --unroll 3 --all --md results/p1_seq_k3.md`

Exit 0

```text
Mach seq_example_unroll_3: 7 PI, 3 PO, 20 cong, 0 DFF
# Ket qua mach tuan tu - seq_example, trai 3 khung

Che do: trang thai dau Q@0 CHUA BIET (khong scan/reset). `DETECTED` nghia la phat hien BAO DAM voi moi trang thai dau cua mach tot va mach loi (cung dinh nghia voi scripts/p4_seq_experiment.py); pattern chi con cac PI dieu khien duoc, Q@0 khong nam trong pattern.

## Moi truong va tai lap

- Lenh tai tao (tu goc repo, PYTHONPATH=src): `python -m atpg.run circuits/seq_example.bench --unroll 3 --all --md results/p1_seq_k3.md`
- Python 3.12.15 (CPython), Windows 11
- Commit ma nguon: cb2be0e
- Thoi diem chay: 2026-10-06T20:36:39
- Thu tu PI trong cot pattern: A, B
- Pham vi loi: 18 loi stem vat ly, moi loi cay vao ca 3 khung
- Nguon pattern theo hang (cot Thuat toan): PODEM, vet can chuoi (tham chieu)
- Tong thoi gian (sinh + kiem chung bao dam): 0.0389 s (time.perf_counter). So do phu thuoc may chay.

Pham vi: 18 loi stem vat ly cua seq_example (moi net 2 loi), moi loi duoc sao sang ca 3 khung; khong gop loi (equivalence cua mach to hop khong mac nhien dung cho mach tuan tu), khong co loi nhanh, mau so = 18.

| PI moi khung | PO moi khung | cong moi khung | DFF |
|---|---|---|---|
| 2 | 1 | 6 | 1 |

Pattern: moi nhom ky tu la cac PI (A, B) cua mot khung, theo thoi gian.

| Loi | Trang thai | Chuoi (PI moi khung) | Thuat toan | Backtrack | Pham vi dam bao |
|---|---|---|---|---|---|
| A/SA0 | DETECTED | 11,10,11 | PODEM | 2 | bao dam moi trang thai dau |
| A/SA1 | DETECTED | 01,10,XX | PODEM | 0 | bao dam moi trang thai dau |
| B/SA0 | DETECTED | XX,XX,11 | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| B/SA1 | DETECTED | XX,XX,10 | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| Q/SA0 | DETECTED | XX,0X,1X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| Q/SA1 | DETECTED | XX,1X,1X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| N1/SA0 | DETECTED | 0X,11,1X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| N1/SA1 | DETECTED | 1X,11,1X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| N2/SA0 | DETECTED | 10,10,1X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| N2/SA1 | DETECTED | 1X,11,1X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| N4/SA0 | DETECTED | XX,0X,10 | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| N4/SA1 | DETECTED | XX,0X,11 | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| N3/SA0 | DETECTED | XX,1X,1X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| N3/SA1 | DETECTED | 1X,11,1X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| Y/SA0 | DETECTED | XX,0X,10 | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| Y/SA1 | DETECTED | XX,XX,0X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |
| D/SA0 | DETECTED | 0X,10,XX | PODEM | 0 | bao dam moi trang thai dau |
| D/SA1 | DETECTED | XX,1X,1X | vet can chuoi (tham chieu) | - | bao dam moi trang thai dau |

| Chi so | Gia tri |
|---|---|
| Phat hien BAO DAM (DETECTED / tong) | 18/18 = 100.0% |
| Chi phat hien CO DIEU KIEN Q@0 | 0 |
| Coverage neu Q@0 dieu khien duoc (scan/reset): (DETECTED + co dieu kien) / tong | 18/18 = 100.0% |
| UNTESTABLE (ke ca khi Q@0 dieu khien duoc, trong gioi han khung) | 0 |
| ABORTED | 0 |
| Chua kiem chung het | 0 |
| Ket luan UNTESTABLE bi kiem chung SAI (vet can tim ra pattern) | 0 |
| Nen tap test | khong ap dung o che do tran khung |

Da ghi results/p1_seq_k3.md
```
