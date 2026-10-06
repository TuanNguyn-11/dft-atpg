# Ket qua mach tuan tu - seq_example, trai 1 khung

Che do: trang thai dau Q@0 CHUA BIET (khong scan/reset). `DETECTED` nghia la phat hien BAO DAM voi moi trang thai dau cua mach tot va mach loi (cung dinh nghia voi scripts/p4_seq_experiment.py); pattern chi con cac PI dieu khien duoc, Q@0 khong nam trong pattern.

## Moi truong va tai lap

- Lenh tai tao (tu goc repo, PYTHONPATH=src): `python -m atpg.run circuits/seq_example.bench --unroll 1 --all --md results/p1_seq_k1.md`
- Python 3.12.15 (CPython), Windows 11
- Commit ma nguon: b107d79
- Thoi diem chay: 2026-10-06T22:06:29
- Thu tu PI trong cot pattern: A, B
- Pham vi loi: 18 loi stem vat ly, moi loi cay vao ca 1 khung
- Nguon pattern theo hang (cot Thuat toan): PODEM, vet can chuoi (tham chieu)
- Tong thoi gian (sinh + kiem chung bao dam): 0.0031 s (time.perf_counter). So do phu thuoc may chay.

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
