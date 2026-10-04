# Ghi chú P4 — ATPG cho mạch tuần tự

## Kiến thức cốt lõi

- FF loại D giữ trạng thái: tại cạnh clock, `Q(t+1)=D(t)`. Logic giữa các FF vẫn là tổ hợp.
- Không scan, trạng thái đầu `Q0` có thể là `X`; vì vậy vector ATPG trên logic tổ hợp có thể yêu cầu một `Q` mà chip không đặt trực tiếp được. Cần khởi tạo bằng PI, rồi kích hoạt lỗi và đưa sai khác qua các FF/PO.
- Time-frame expansion tạo `k` bản sao của logic tổ hợp. PI tại mỗi khung độc lập; `D@t` nối tới `Q@(t+1)`. Một stuck-at vật lý hiện diện ở mọi khung tương ứng.
- `Q@0` trong `unroll()` chỉ là PI hình thức. Mẫu PODEM gán nó không mặc nhiên hợp lệ trên chip. Kiểm bằng mọi trạng thái đầu hoặc chứng minh chuỗi khởi tạo.
- Full scan cho phép shift trạng thái vào Q và shift trạng thái chụp từ D ra ngoài. Khi cắt FF, Q là pseudo-PI, D là pseudo-PO. Chi phí là MUX/đường scan và chu kỳ dịch.
- Partial scan chỉ thay một phần FF, giảm chi phí phần cứng nhưng còn trạng thái khó điều khiển/quan sát.

## Mạch ví dụ và điểm cần nhớ

`seq_example.bench` có `N1=A&Q`, `N2=!B`, `N3=N1|N2`, `D=!(N3&A)`, `Q=DFF(D)`, `N4=Q xor B`, `Y=N4&A`.

Với `N3/SA0`, chuỗi `(1,0),(1,0)` phát hiện lỗi trong 2 khung bất kể Q0. Ở khung đầu, `B=0` làm `N2=1`, nên N3 tốt=1; lỗi ép N3=0 và làm D tốt/lỗi=0/1. Sau clock, Q=0/1; khung sau `Y=Q`.

## Giao diện và phụ thuộc nhóm

- Module P4 chỉ dùng các trường `Circuit.name, inputs, outputs, gates, fanout, topo_order, level`; `Gate.output,type,inputs`; `Fault.net,stuck_at,branch_to`.
- `full_scan(c)`, `unroll(c,k)` trả `Circuit` tổ hợp; `fault_in_frames(fault,k)` trả `list[Fault]`. PODEM của P5 phải nhận danh sách lỗi cùng xuất hiện trên mạch trải khung.
- `fault_in_frames(fault,k)` chỉ ánh xạ lỗi stem; lỗi nhánh đi vào cổng tổ hợp hoặc DFF đều bị từ chối bằng `ValueError`. Hàm không nhận `Circuit` nên không thể xác minh cạnh đích; đặc biệt cạnh vào DFF phải đi từ `D@t` sang `Q@(t+1)` và không tồn tại sau khung cuối. Khi P5/P6 bàn giao, cần thống nhất giao diện tích hợp có thông tin mạch trước khi hỗ trợ lỗi nhánh.
- P6 chưa có parser/fault simulator/CLI trên `main` lúc viết. `tests/test_unroll.py` dùng mô hình khớp hợp đồng, và script P4 vét cạn độc lập; cần chạy lại tích hợp khi P5/P6 đưa code lên.

## Nguồn đã kiểm tra

- NPTEL, “ATPG for Synchronous Sequential Circuits”: https://archive.nptel.ac.in/content/storage2/courses/106103016/module10/lec1/1.html
- NPTEL, “Scan Chain Based Sequential Circuit Testing”: https://archive.nptel.ac.in/content/storage2/courses/106103016/module10/lec2/5.html
- Eichelberger & Williams, “A Logic Design Structure for LSI Testability”, DAC 1977, pp. 462–468: https://ieee-ceda.org/media/logic-design-structure-lsi-testability
