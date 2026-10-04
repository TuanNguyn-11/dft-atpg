# Kết quả mạch tuần tự P4 (`seq_example.bench`)

## Phạm vi và cách kiểm tra

- Mạch: 2 PI (`A,B`), 1 PO (`Y`), 6 cổng tổ hợp, 1 DFF (`Q=DFF(D)`).
- Fault universe: 9 stem × {SA0, SA1} = **18 lỗi**; chưa fault collapsing, chưa gồm lỗi nhánh và lỗi bên trong FF/clock.
- `python scripts/p4_seq_experiment.py` vét cạn vector full scan và chuỗi PI dài 1–4 khung bằng mô phỏng nhị phân độc lập. Với chuỗi không scan, hai tập vết PO của mạch tốt/lỗi phải rời nhau cho **cả hai** trạng thái ban đầu `Q0=0` và `Q0=1`.
- Đây là số liệu tham chiếu của P4, **chưa phải output PODEM**. Khi P5/P6 ghép code, cần đối chiếu pattern và coverage qua `podem()` và `fault_sim.detects()`.

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

Theo giới hạn độ dài chuỗi: `k=1`: **1/18**; `k=2`: **13/18**; `k=3`: **18/18**; `k=4`: **18/18**. Vì vậy không được gán con số 100% cho riêng lần chạy `--unroll 2`. Các lỗi chưa phát hiện ở k nhỏ không đồng nghĩa untestable.

## Kiểm thử code P4

`python tests/test_unroll.py`: **8/8 phép thử qua**. Bao gồm 3192 trường hợp đối chiếu mạch do `unroll()` sinh với mô phỏng tuần tự độc lập (toàn bộ chuỗi dài 1–3 khung, hai giá trị Q0, 18 lỗi và trường hợp không lỗi), 152 trường hợp full scan, cập nhật đồng thời hai DFF, ví dụ phản chứng khi tùy ý gán Q0, cấu trúc đồ thị và đầu vào k không hợp lệ. Cũng có thể chạy bằng `pytest tests/test_unroll.py` khi đã cài pytest; lần rà soát này chạy trực tiếp bằng Python, chưa chạy qua pytest.

## Tích hợp cần chạy khi P5/P6 bàn giao

1. Đọc `seq_example.bench` bằng `Circuit.from_bench` của P6 và chạy lại 4 phép thử trên đối tượng thực.
2. Dùng `podem(full_scan(c), Fault("N3",0))`; xác nhận `DETECTED` rồi kiểm bằng `fault_sim.detects()`.
3. Dùng `podem(unroll(c,2), fault_in_frames(Fault("N3",0),2))`; kiểm pattern không dựa vào giá trị `Q@0` không thể điều khiển. So với chuỗi hai khung ở trên.
4. Chạy CLI nhóm `python -m atpg.run circuits/seq_example.bench --unroll 2 --all` và ghi lại coverage/thời gian thực tế. CLI chưa có trên `main` tại thời điểm viết kết quả này.
