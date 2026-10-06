# P6 — Review chéo P5 và xác nhận P2/P3 (06/10/2026)

Phạm vi: `src/atpg/podem.py`, `src/atpg/logic.py` của P5 tại commit `7979490` (đã merge vào `main` qua PR #10, `c864406`), chạy cùng `circuit.py`, `faults.py`, `fault_sim.py`, `run.py` (P6) và `unroll.py` (P4). Bằng chứng tự động: `tests/test_integration.py` (PODEM thật, không fixture ép vét cạn).

## Review P5 (kiểm bằng kết quả chạy, chưa rà từng dòng thuật toán)

| Hạng mục | Kết quả |
|---|---|
| Giao diện mục 8 | `podem(c, fault \| list[Fault], max_backtracks, trace)` trả `PodemResult` có `status`, `pattern` ("0"/"1"/"X"), `backtracks`, `steps`: khớp |
| Trace mục 9 | `steps` có đúng 7 cột; c17 `11/SA0`: (11,1) → 3=0, (2,1) → 2=1, `X10XX`, 0 backtrack: khớp golden trace P3 |
| c17 toàn bộ lỗi | 22/22 lỗi đại diện và 34/34 lỗi gốc `DETECTED`, 0 backtrack, mọi pattern được fault simulator xác nhận với mọi cách điền X |
| Mạch phụ P3 (`t/SA0`) | `01`, 1 backtrack, 3 hàng `tiếp tục`/`backtrack`/`thành công`; giới hạn 0 → `ABORTED` (không phải `UNTESTABLE`) |
| Mạch trải khung | Nhận `list[Fault]`; k = 1, 2, 3 không có kết luận `UNTESTABLE` sai; 8 kết luận `UNTESTABLE` ở k = 1 được vét cạn xác nhận |

Lịch sử: tại commit `92845c3` (trước khi merge), backtrace chưa hỗ trợ XOR và có 4 kết luận `UNTESTABLE` sai (`N1`, `N2` SA0/SA1) ở `seq_example --unroll 2`; cả hai đã hết ở `7979490`.

Góp ý (không chặn merge): PODEM coi `Q@0` là PI hình thức nên thường gán nó; với trạng thái đầu chưa biết, phần lớn chuỗi bảo đảm hiện phải lấy từ vét cạn (k = 2: 3 từ PODEM, 10 từ vét cạn). Có thể thêm tùy chọn giữ các PI trạng thái ở X.

## Xác nhận P2/P3 bằng fault simulator P6

| Nội dung | Kết quả |
|---|---|
| Cube P2 `(X,1,0,0,X)` | 4/4 cách điền phát hiện `11/SA0` tại PO 22 |
| Cube `(X,1,0,X,X)` | 8/8 cách điền phát hiện `11/SA0` tại PO 22 |
| Vector `01000` | mạch tốt (22,23) = (1,1), mạch lỗi = (0,0) |
| Mạch phụ P3 | chỉ vector `01` trong 4 vector phát hiện `t/SA0` |
