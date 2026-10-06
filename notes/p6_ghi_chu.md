# Ghi chú P6 — những gì đã tìm hiểu

> Bản nháp để P6 đọc, sửa lại bằng lời của mình và bổ sung. Số liệu c17 đã được kiểm bằng code (`pytest`).

## 1. Định dạng .bench
- Mỗi dòng: `INPUT(x)`, `OUTPUT(y)` hoặc `y = LOẠI(a, b, ...)`; `#` là chú thích; `DFF` là flip-flop.
- c17: 5 PI (1, 2, 3, 6, 7), 2 PO (22, 23), 6 cổng NAND, tổng 11 net.

## 2. Đồ thị mạch, topo, levelization, fanout
- Mỗi net là một đỉnh; cổng nối các net vào với net ra. Sắp xếp topo: tính cổng sau khi mọi ngõ vào đã có giá trị.
- Level: PI = 0; level(cổng) = 1 + max level ngõ vào. c17: 10, 11 ở level 1; 16, 19 ở level 2; 22, 23 ở level 3.
- Bảng fanout c17: 3 → {10, 11}; 11 → {16, 19}; 16 → {22, 23}; các net còn lại có một đích (hoặc là PO).
- Quy ước DFF trong code: ngõ ra Q coi là nguồn (level 0), cổng DFF không nằm trong `topo_order`.

## 3. Fault universe của c17
- Lỗi trên stem: 11 net × 2 (SA0, SA1) = 22.
- Lỗi trên nhánh: chỉ net rẽ nhánh (3, 11, 16), mỗi net 2 nhánh × 2 = 12.
- Tổng ban đầu: **34 lỗi**.

## 4. Fault collapsing theo equivalence
- Hai lỗi tương đương nếu tập vector phát hiện chúng giống hệt nhau.
- Quy tắc theo cổng (lỗi ở ngõ vào ≡ lỗi ở ngõ ra): AND: SA0 ≡ SA0; NAND: SA0 ≡ SA1; OR: SA1 ≡ SA1; NOR: SA1 ≡ SA0; NOT: SA0 ≡ SA1 và SA1 ≡ SA0; XOR/XNOR: không gộp được.
- c17 (toàn NAND): 34 → **22 lỗi**. Ví dụ lớp {3→11/SA0, 6/SA0, 11/SA1} giữ lại đại diện 11/SA1. Lỗi 11/SA0 đứng một mình.
- Chú ý: 22 sau gộp là phép gộp trên 34 lỗi; trùng với "11 net × 2 = 22" chỉ là ngẫu nhiên.

## 5. Mô phỏng lỗi
- Nối tiếp (serial): mô phỏng mạch tốt và mạch lỗi, so các PO; phát hiện nếu có PO khác nhau.
- Lỗi stem ép giá trị cả net; lỗi nhánh chỉ ép giá trị tại ngõ vào của cổng `branch_to`.
- Song song theo pattern: mỗi net là một số nguyên, bit k là giá trị ở pattern k; cổng NAND = `~(a & b) & mask`.
- Pattern có X: điền 0 rồi mô phỏng (quy ước nhóm); thêm kiểm "mọi cách điền X" để chắc chắn.

## 6. Chỉ số
- Fault coverage = DETECTED / tổng.
- Test coverage = DETECTED / (tổng − UNTESTABLE).
- Fault efficiency = (DETECTED + UNTESTABLE) / tổng.
- Fault dropping: lỗi đã phát hiện thì bỏ khỏi các lần mô phỏng sau.
- Trạng thái: DETECTED (có pattern), UNTESTABLE (chứng minh không có pattern), ABORTED (hết giới hạn backtrack).

## 7. Nén tập test
- Duyệt pattern, giữ pattern phát hiện thêm lỗi mới; duyệt thêm lượt ngược để loại pattern thừa.
- c17 (22 lỗi sau gộp, bản tham chiếu vét cạn): 22 pattern → 7 pattern, vẫn coverage 100%.

## 8. Lệnh/CLI và công cụ
- `argparse`: `--fault NET SV [--branch GATE]`, `--all`, `--trace`, `--unroll K`, `--md FILE`.
- Beamer: `slides/main.tex` dùng `\input{parts/pX}`.

## 9. Việc còn mở
- [ ] Đối chiếu `Circuit`/`Fault` với P4, P5 (mục 8 prompt.md).
- [ ] Đối chiếu vector của P2, P3 cho 11/SA0 bằng `--pattern`.
- [ ] Chạy lại `--all` khi `podem.py` của P5 có mặt.
