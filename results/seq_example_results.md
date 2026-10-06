# Kết quả mạch tuần tự P4 (`seq_example.bench`)

## Phạm vi và cách kiểm tra

- Mạch: 2 PI (`A,B`), 1 PO (`Y`), 6 cổng tổ hợp, 1 DFF (`Q=DFF(D)`).
- Fault universe: 9 stem × {SA0, SA1} = **18 lỗi**; chưa fault collapsing, chưa gồm lỗi nhánh và lỗi bên trong FF/clock.
- `python scripts/p4_seq_experiment.py` vét cạn vector full scan và chuỗi PI dài 1–4 khung bằng mô phỏng nhị phân độc lập. Với chuỗi không scan, hai tập vết PO của mạch tốt/lỗi phải rời nhau cho **cả hai** trạng thái ban đầu `Q0=0` và `Q0=1`.
- Bảng vét cạn bên dưới là **tham chiếu độc lập**, không phải output PODEM. Kết quả tích hợp hiện tại được lưu riêng ở `seq_integrated_full_scan.md` và `seq_integrated_k1.md`–`seq_integrated_k3.md`.

## Ví dụ chạy tay

**Không scan, lỗi `N3/SA0`, k=2:** `[(A,B)=(1,0), (1,0)]`.

| Khung | Q tốt/lỗi | N3 tốt/lỗi | D tốt/lỗi | Y tốt/lỗi |
|---|---|---|---|---|
| 0 | `Q0/Q0` | `1/0` | `0/1` | `Q0/Q0` |
| 1 | `0/1` | `1/0` | `0/1` | `0/1` |

Lỗi được kích hoạt ở khung 0, lưu qua DFF và quan sát tại `Y@1`, độc lập `Q0`. Chuỗi ba khung `[(0,0),(1,1),(1,0)]` minh họa riêng pha khởi tạo `Q1=1`, rồi kích hoạt và quan sát.

**Full scan:** nạp `Q=0`, đặt `A=1,B=0`. `D` tốt/lỗi = `0/1`; sau capture và shift out có thể phân biệt. Một vector logic không tính thời gian shift vật lý.

## Kết quả vét cạn

Mỗi hàng là mẫu đầu tiên theo thứ tự vét cạn, không khẳng định số bước/backtrack của PODEM. Với cột chuỗi, mỗi cặp là `(A,B)` theo thời gian; mọi chuỗi đều không phụ thuộc `Q0`.

| Lỗi | Full scan `(A,B,Q)` | Chuỗi không scan |
|---|---|---|
| A/SA0 | `(1,0,0)` | `[(0,0),(1,0)]` |
| A/SA1 | `(0,0,0)` | `[(0,0),(0,1)]` |
| B/SA0 | `(1,1,0)` | `[(0,0),(1,1)]` |
| B/SA1 | `(1,0,0)` | `[(0,0),(1,0)]` |
| N1/SA0 | `(1,1,1)` | `[(0,0),(1,1),(1,0)]` |
| N1/SA1 | `(1,1,0)` | `[(1,0),(1,1),(1,0)]` |
| N2/SA0 | `(1,0,0)` | `[(1,0),(1,0),(1,0)]` |
| N2/SA1 | `(1,1,0)` | `[(1,0),(1,1),(1,0)]` |
| N3/SA0 | `(1,0,0)` | `[(1,0),(1,0)]` |
| N3/SA1 | `(1,1,0)` | `[(1,0),(1,1),(1,0)]` |
| D/SA0 | `(0,0,0)` | `[(0,0),(1,0)]` |
| D/SA1 | `(1,0,0)` | `[(1,0),(1,0)]` |
| Q/SA0 | `(1,0,1)` | `[(0,0),(1,0)]` |
| Q/SA1 | `(1,0,0)` | `[(1,0),(1,0)]` |
| N4/SA0 | `(1,0,1)` | `[(0,0),(1,0)]` |
| N4/SA1 | `(1,0,0)` | `[(0,0),(1,1)]` |
| Y/SA0 | `(1,0,1)` | `[(0,0),(1,0)]` |
| Y/SA1 | `(0,0,0)` | `[(0,0)]` |

**Tổng:** full scan `18/18 = 100%`; không scan `18/18 = 100%` với chuỗi tối đa **3 khung** trong giới hạn tìm 4 khung. Coverage chỉ áp dụng cho fault universe 18 stem nói trên.

Full scan dùng **bộ mẫu vét cạn**, chọn mẫu riêng cho từng lỗi. Tám vector `(A,B,Q)` theo thứ tự nhị phân phát hiện lần lượt `3, 3, 3, 3, 8, 7, 9, 8` lỗi; một vector phát hiện nhiều nhất `9/18`, còn hợp của bộ mẫu phát hiện `18/18`.

Theo giới hạn độ dài chuỗi: `k=1`: **1/18**; `k=2`: **13/18**; `k=3`: **18/18**; `k=4`: **18/18**. Vì vậy không được gán con số 100% cho riêng lần chạy `--unroll 2`. Các lỗi chưa phát hiện ở k nhỏ không đồng nghĩa untestable.

## Kiểm thử code P4 trước tích hợp (04/10/2026)

Ngày 04/10, `python tests/test_unroll.py`: **10/10 phép thử qua**. Bao gồm 3192 trường hợp đối chiếu mạch do `unroll()` sinh với mô phỏng tuần tự độc lập (toàn bộ chuỗi dài 1–3 khung, hai giá trị Q0, 18 lỗi và mạch không lỗi), 152 trường hợp full scan, cập nhật đồng thời hai DFF, ví dụ phản chứng khi tùy ý gán Q0, cấu trúc đồ thị, đầu vào k không hợp lệ và kiểm tra k=1,2 cho lỗi stem/nhánh. Lỗi nhánh bị từ chối rõ; `evaluate()` không mô phỏng lỗi nhánh. Lần rà soát **trước tích hợp** chạy trực tiếp bằng Python chuẩn vì khi đó môi trường thiếu `pytest`; kết quả pytest hiện tại ở phần dưới.

## Kết quả tích hợp trên `main` mới — 06/10/2026

Chạy bằng Python 3.12.0 trên mã nguồn commit `553dfb6` (cha `586218e`). Thí nghiệm full scan dùng **Circuit/PODEM/simulator thật**, lấy đúng 18 lỗi stem vật lý từ `base.nets`, không dùng danh sách có lỗi nhánh của mạch sau scan. Mọi cube `DETECTED` được xác nhận qua `detects_cube()` cho tất cả cách điền X và qua oracle nhị phân P4. Sau điền X=0, hợp 6 vector khác nhau phủ 18/18 lỗi; một vector riêng lẻ tối đa 9/18. Bảng 18 hàng, backtracks, pattern và lệnh tái lập nằm tại [seq_integrated_full_scan.md](seq_integrated_full_scan.md).

| Chế độ | Phát hiện bảo đảm / 18 stem | Nguồn chuỗi bảo đảm |
|---|---:|---|
| Full scan | 18/18 | PODEM 18; simulator và oracle xác nhận |
| Không scan, k=1 | 1/18 | PODEM 0; vét cạn bổ sung 1 |
| Không scan, k=2 | 13/18 | PODEM 3; vét cạn bổ sung 10 |
| Không scan, k=3 | 18/18 | PODEM 3; vét cạn bổ sung 15 |

CLI thật ghi từng hàng tại [k=1](seq_integrated_k1.md), [k=2](seq_integrated_k2.md), [k=3](seq_integrated_k3.md), gồm cột `Thuat toan` từ `GenResult.algo`. Mỗi stem được cấy ở **mọi khung**; không gộp lỗi tuần tự. `Q@0` chưa biết nên chỉ tính `DETECTED` khi hai tập vết PO tốt/lỗi rời nhau với mọi cặp trạng thái đầu. Ở k=1 có 9 lỗi chỉ phát hiện **có điều kiện** và 8 lỗi `UNTESTABLE` **trong giới hạn một khung**, không phải untestable với mọi độ dài. k=2 có 5 lỗi chỉ có điều kiện; không có `ABORTED` hay hàng chưa kiểm chứng hết ở các lần chạy này. `--init controllable` chỉ cho đặt `Q@0`, không tương đương full scan vì không thêm pseudo-PO `D`.

Kiểm thử hồi quy trên Python 3.12.0/pytest 9.1.1: `tests/test_unroll.py`, `tests/test_sequential.py`, `tests/test_p4_integration.py` **24 passed**; toàn repo **334 passed**. Test P4 tích hợp nằm ngoài fixture `reference_only` của P6 và thật sự gọi PODEM, simulator cùng oracle độc lập. Script vét cạn cũ vẫn giữ nguyên để đối chiếu.
