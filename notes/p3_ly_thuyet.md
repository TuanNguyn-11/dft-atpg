# PODEM — lý thuyết và lời dẫn thuyết trình

Chương tích hợp được rút gọn theo README và `notes/p1_ke_hoach.md`:
báo cáo toàn nhóm 5–10 trang, P3 dự kiến 1,25 trang. Gói ZIP gốc vẫn giữ
bản dài; tài liệu này, hợp đồng P3-v1 và hai golden trace giữ phần giải thích.

## Objective → backtrace → imply

PODEM tổ chức cây quyết định trên PI. Objective (net, giá trị) là yêu cầu
muốn đạt, không phải phép ghi vào net nội bộ. Với lỗi l/SA0 cần l tốt=1;
với l/SA1 cần l tốt=0. Sau kích hoạt, chọn một cổng D-frontier còn X-path,
đặt đầu vào bên cạnh về giá trị không điều khiển để truyền sai khác.

Backtrace đi ngược từ objective qua đầu vào chưa biết về một PI chưa gán.
Qua NAND/NOR/NOT thì đảo bit mong muốn; AND/OR/BUFF không đảo. Với NAND11,
objective (11,1) chọn đầu vào 3 trước 6; qua một NAND nên gán 3=0.
Imply mô phỏng lại từ PI theo topo, cấy lỗi stem trước khi phân nhánh.
NAND(0,X)=1 nên 10=1 và 11=D. Objective lan truyền (2,1) chính là PI2.
NAND(1,D)=D', NAND(1,D')=D: sai khác tới PO22 sau hai phép gán.

Một lần backtrace không nhất thiết đạt objective ngay. AND cần ra 1 phải
đưa mọi đầu vào về 1; sau một quyết định PI, imply rồi tiếp tục chọn mục tiêu.
Các cổng XOR/XNOR dùng `y = XOR(các đầu vào) ⊕ q`, với q=0/1 tương ứng.
Backtrace mục tiêu y=v khi chỉ còn một X dùng `v ⊕ q ⊕ p`, với p là
parity các bit tốt đã biết. Khi còn nhiều X, ưu tiên X đầu tiên bằng 0,
imply rồi tính lại. Objective lan truyền cũng thử X đầu tiên bằng 0;
không gọi đó là giá trị không điều khiển. Bảng logic, trường hợp triệt
tiêu D/D' và bốn ví dụ nằm trong [bổ sung P3-v1.1](p3_xor_xnor.md).

## Controllability và heuristic

SCOAP CC0/CC1 càng nhỏ thì giá trị tương ứng càng dễ đạt. Nếu chỉ cần một
đầu vào mang giá trị điều khiển, có thể thử đầu vào dễ trước. Nếu cần mọi
đầu vào mang giá trị không điều khiển, có thể chọn mục tiêu khó trước để
phát hiện bế tắc sớm. Đây là heuristic, không phải duy nhất.
P3-v1 chỉ dùng thứ tự netlist/topo ổn định và đầu vào X đầu tiên, không dùng
SCOAP hoặc level. Code P5 tích hợp đã áp dụng; đối chiếu API và exporter
ngày 06/10/2026 ở `p3_doi_chieu_P5.md` ghi rõ khác biệt nhãn hành động.

## D-frontier, X-path và năm giá trị

0=(0,0), 1=(1,1), D=(1,0), D'=(0,1) theo thứ tự tốt/lỗi. Cặp chỉ biết một
thành phần được rút về X bảo thủ. PI trong pattern chỉ chứa 0/1/X; PI có lỗi
có thể mang D/D' trong trạng thái mô phỏng sau cấy lỗi.
D-frontier là tập cổng có đầu ra X và đầu vào D/D', ghi bằng tên net đầu ra.
Tính lại sau mỗi imply, kể cả khi thành công. Trên c17, frontier cuối là
{19,23}; net 16 đã là D' nên không còn ở frontier, PO23 còn X nên được thêm.

X-path trong P3-v1 đi từ đầu ra X của frontier qua các net đầu ra X tới PO.
Có đường như vậy chỉ là điều kiện cần: reconvergence còn có thể làm những
ràng buộc trên đường xung đột. Không có X-path sau kích hoạt cho phép cắt nhánh.
Frontier rỗng trước kích hoạt không đủ để cắt nhánh; PO có D/D' được ưu tiên
trước mọi kiểm tra frontier. X ở net mô phỏng không luôn là don't-care của
test cube; tính an toàn của mẫu X10XX đã được kiểm tra đủ 8 cách điền.

## DFS, backtrack và mã giả

```text
SEARCH():
    imply từ PI hiện tại
    nếu một PO có D hoặc D': trả DETECTED
    nếu nhánh bất khả thi: trả FAIL
    objective = chọn mục tiêu
    (pi, bit) = backtrace(objective)
    gán pi = bit; result = SEARCH()
    nếu result khác FAIL: trả result
    nếu backtracks >= limit: trả ABORTED
    backtracks += 1
    gán pi = 1-bit; result = SEARCH()
    nếu result khác FAIL: trả result
    trả pi về X; imply lại; trả FAIL
```

Mỗi lời gọi con trả FAIL phải xóa các quyết định do nó tạo ra. Chỉ đổi FAIL
thành UNTESTABLE ở mức gốc. ABORTED truyền nguyên lên cha, không thử nhánh
khác như thể đã chứng minh thất bại. Đếm backtrack bằng số lần thực sự đảo
PI; không đếm lần gán đầu hoặc reset. Bộ kiểm chứng P3 hiện không cài giới
hạn backtrack; script `p3_doi_chieu_code.py` riêng đã chạy code P5 thật:
giới hạn 0 trả ABORTED, giới hạn 1 trả DETECTED trên mạch phụ.

Mạch phụ có out=(a+b)NOT(a)=NOT(a)b. Với t/SA0, out lỗi luôn bằng 0.
a=1 kích hoạt t nhưng n=0 chặn AND cuối với mọi b. Đảo a=0 phục hồi n=1,
t trở lại X; b=1 mới kích hoạt lại và đưa D ra out. Có hai lần gọi
objective/backtrace, ba hàng gán/đảo, một backtrack. Vector duy nhất là 01.

## So sánh và FAN

| Tiêu chí | D-algorithm | PODEM |
|---|---|---|
| Nơi quyết định | PI và net nội bộ thông qua cube | PI |
| Biện minh | Cần justification, J-frontier | Net nội bộ suy ra bằng imply |
| Lan truyền | D-frontier/PDC | Objective từ D-frontier, backtrace |
| Không gian | Ràng buộc tại các net | Cây nhị phân trên n PI, tối đa 2^n vector |
| Cài đặt | Phối hợp implication, propagation, justification | Objective, backtrace, imply, DFS |
| c17 theo trace đã nhận | 4 lần chọn cube, 3 PI gán, 0 backtrack | 2 PI gán, 0 backtrack |

Không lấy 4/2 làm tốc độ. Hai trace là minh họa với lựa chọn đã công bố,
không phải đo thời gian implementation. P2 chọn 6=0 trước nên mẫu ban đầu
X100X; P3 chọn 3=0 trước nên không cần gán 6. Nguồn cụ thể ở phiếu đối chiếu.

FAN (Fujiwara–Shimono, 1983) dùng cấu trúc fanout, headline và multiple
backtrace để giảm quyết định không hiệu quả. Có thể dừng backtrace ở
headline phù hợp rồi justify sau. Đồ án chưa cài FAN; không nhận các cải
tiến hoặc số đo của bài báo là kết quả nhóm.

## Lời dẫn khoảng ba phút

1. Giải thích D=(tốt 1, lỗi 0), mục tiêu kích hoạt rồi quan sát tại PO.
2. Nêu PODEM quyết định tại PI; trình bày 3=0 → 11=D và 2=1 → 22=D.
3. Giải thích X10XX có năm bit theo thứ tự (1,2,3,6,7); X=0 cho 01000.
4. Minh họa a=1 tự chặn đường lỗi, đảo a=0 rồi b=1; phân biệt ba hàng với
   một backtrack, ABORTED với UNTESTABLE.
5. Nêu P2 có đơn vị đếm khác; đã đối chiếu P5/P6. API ghi thao tác vừa làm,
   golden ghi việc kế tiếp; exporter chuẩn hóa nhãn. Không suy ra tốc độ.
