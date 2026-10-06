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
- Pattern có X: điền 0 rồi mô phỏng (quy ước nhóm). Kiểm "mọi cách điền X" có ba kết quả: có (đã vét cạn), không (có phản ví dụ), chưa kiểm chứng hết (quá giới hạn bit X). Không được coi "thử X=0 và X=1 đều đạt" là bằng chứng cho mọi cách điền.

## 6. Chỉ số
- Fault coverage = DETECTED / tổng.
- Test coverage = DETECTED / (tổng − UNTESTABLE).
- Fault efficiency = (DETECTED + UNTESTABLE) / tổng.
- Fault dropping: lỗi đã phát hiện thì bỏ khỏi các lần mô phỏng sau.
- Trạng thái: DETECTED (có pattern), UNTESTABLE (chứng minh không có pattern), ABORTED (hết giới hạn backtrack).

## 7. Nén tập test
- Duyệt pattern, giữ pattern phát hiện thêm lỗi mới; duyệt thêm lượt ngược để loại pattern thừa.
- c17 bằng PODEM: 22 lỗi sau gộp, 22 pattern → 6 pattern; 34 lỗi không gộp → 7 pattern; vẫn coverage 100%, backtrack trung bình 0.

## 8. Lệnh/CLI và công cụ
- `argparse`: `--fault NET SV [--branch GATE]`, `--all`, `--trace`, `--unroll K`, `--init`, `--no-collapse`, `--pattern`, `--max-x`, `--max-backtracks`, `--md FILE`.
- Đầu vào sai (SV khác 0/1, net hoặc nhánh không tồn tại, K < 1, giới hạn âm, mạch có DFF mà thiếu `--unroll`) bị từ chối với mã thoát 2; API ném `ValueError`. `generate_test` chỉ dùng vét cạn khi PODEM báo chưa hỗ trợ, và ghi nguồn theo từng hàng. Từ 06/10/2026, lõi `podem.podem` gọi trực tiếp cũng ném `ValueError` khi net/nhánh không thuộc mạch hoặc `max_backtracks` âm (trước đó nhánh 11→999 trả `UNTESTABLE`); test ở `tests/test_input_validation.py`.
- Beamer: `slides/main.tex` dùng `\input{parts/pX}`.

## 9. Việc còn mở
- [x] Đối chiếu `Circuit`/`Fault` với P4, P5 (mục 8 prompt.md): ghép P4, P5 chạy đúng, 302 test pass (mốc trước tích hợp; ngày 06/10/2026 sau khi merge P2/P4/P5 và vá kiểm tra đầu vào lõi PODEM: 350 passed).
- [x] Đối chiếu vector của P2, P3 cho 11/SA0 bằng `--pattern`: `X10XX` phát hiện với mọi cách điền X.
- [x] Chạy lại `--all` bằng PODEM của P5: `results/c17_all_faults.md`.

## 10. Mạch tuần tự: trạng thái đầu chưa biết
- Sau `unroll`, `Q@0` chỉ là đầu vào hình thức. Trên chip không scan/reset không tự đặt được `Q@0`.
- Mạch tốt và mạch lỗi là hai chip riêng nên mỗi chip có thể bắt đầu ở trạng thái bất kỳ. Pattern chỉ **phát hiện bảo đảm** khi mọi vết PO của mạch tốt khác mọi vết PO của mạch lỗi, với mọi cặp trạng thái đầu và mọi cách điền X (cùng định nghĩa với `scripts/p4_seq_experiment.py`).
- Pattern phụ thuộc `Q@0` chỉ là kết quả **có điều kiện** (nhãn `CO DIEU KIEN Q@0`), tách khỏi coverage bảo đảm. Ví dụ `Q = DFF(A)`, `Y = AND(Q, A)`, lỗi `Y/SA0`: 1 khung chỉ phát hiện nếu `Q@0 = 1`; 2 khung với `A = 1, 1` thì bảo đảm.
- seq_example, 18 lỗi stem, bảo đảm: k = 1: 1/18; k = 2: 13/18; k = 3: 18/18 (khớp kết quả của P4).
- Chế độ trải khung chỉ dùng lỗi stem vật lý, sao sang mọi khung, không gộp lỗi, không có lỗi nhánh (`fault_in_frames` của P4 chỉ nhận stem; lỗi nhánh vào DFF phải ánh xạ `D@t` sang `Q@(t+1)`).

## 11. Kết quả chính thức (PODEM, 06/10/2026)
- c17: 22/22 (22 đại diện, nén 22 → 6) và 34/34 (34 lỗi gốc, nén 34 → 7); backtrack trung bình 0; tập 6 pattern phủ cả 34 lỗi gốc; 0 pattern sai. File: `results/c17_all_faults.md`, `results/c17_all_faults_uncollapsed.md`.
- seq_example (Q@0 chưa biết): k = 1, 2, 3 → bảo đảm 1/18, 13/18, 18/18; nguồn chuỗi bảo đảm PODEM/vét cạn 0/1, 3/10, 3/15. File: `results/seq_example_p6_k1.md` … `k3.md`.
- Review chéo P5 và xác nhận P2/P3: xem `notes/p6_review_p5.md`.

