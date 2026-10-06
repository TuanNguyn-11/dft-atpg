# Bổ sung P3-v1.1: quy tắc XOR/XNOR cho P5 — 06/10/2026

## 1. Phạm vi và lý do bổ sung

P3-v1 mới đặc tả AND/NAND/OR/NOR/NOT/BUFF. Câu “XOR/XNOR cần xử lý
parity riêng” chưa đủ để P5 cài objective và backtrace. P3-v1.1 bổ sung
quy tắc dưới đây, giữ nguyên thứ tự topo, thứ tự Gate.inputs, DFS và
cách đếm backtrack của [hợp đồng P3](p3_quy_tac_P5.md).
Hai golden trace c17 và mạch phụ không chứa XOR/XNOR nên không đổi.
Đây là đặc tả bàn giao, chưa phải xác nhận code P5 đã hỗ trợ hai cổng.

## 2. Parity và bảng chân trị

Ký hiệu ⊕ là XOR (cộng modulo 2), q=0 với XOR và q=1 với XNOR:

`y = x1 ⊕ x2 ⊕ ... ⊕ xn ⊕ q`.

XOR bằng 1 khi số bit 1 là lẻ. XNOR là đảo của XOR trên **toàn bộ**
đầu vào, bằng 1 khi số bit 1 là chẵn. Với nhiều đầu vào, tính XOR tất cả
rồi đảo đúng một lần cho XNOR; không gấp lần lượt bằng XNOR hai ngõ vào.

| a | b | XOR(a,b) | XNOR(a,b) |
|---|---|---|---|
| 0 | 0 | 0 | 1 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |

XOR/XNOR không có giá trị điều khiển: khi giữ một đầu vào ở 0 hay 1,
đầu ra vẫn phụ thuộc đầu vào kia. Vì vậy không áp dụng nguyên xi quy tắc
“non-controlling = 1/0” của AND/OR, hay chỉ đếm cổng đảo khi backtrace.

## 3. Imply: tính trên hai mạch

Biểu diễn 0=(0,0), 1=(1,1), D=(1,0), D'=(0,1), theo thứ tự tốt/lỗi.
Áp dụng công thức parity độc lập trên mỗi thành phần; XNOR đảo cả hai.
Nếu có X, phép đánh giá cổng theo logic năm giá trị bảo thủ trả X.
Không coi X là 0 khi imply hoặc tính parity đã biết.

| a | b | XOR(a,b) | XNOR(a,b) |
|---|---|---|---|
| D | 0 | D | D' |
| D | 1 | D' | D |
| D' | 0 | D' | D |
| D' | 1 | D | D' |
| D | D | 0 | 1 |
| D | D' | 1 | 0 |
| D' | D' | 0 | 1 |
| D | X | X | X |
| 0 | X | X | X |
| 1 | X | X | X |
| X | X | X | X |

Hai đầu vào hoán đổi được. Với XOR(a,a), hai bản sao thực tế có tương
quan nên kết quả Boolean luôn 0; bộ đánh giá cổng cục bộ nhận (X,X) vẫn
trả X vì không lưu tương quan. Đây là xấp xỉ, không phải chứng minh có nghiệm.

Khi mọi đầu vào đã xác định, `y_good ⊕ y_faulty` bằng XOR của các
`xi_good ⊕ xi_faulty`. Do đó số đầu vào D/D' lẻ tạo D hoặc D' ở đầu ra;
số chẵn làm sai khác triệt tiêu. q không thay đổi điều kiện này.

## 4. Objective lan truyền qua D-frontier

Giữ cách kích hoạt lỗi: tại net lỗi cần giá trị mạch tốt `1-stuck_at`.
Khi lỗi đã kích hoạt, duyệt frontier và X-path theo hợp đồng cũ.
Nếu cổng được chọn là XOR/XNOR, chọn đầu vào X đầu tiên theo Gate.inputs
và objective **(đầu vào đó, 0)**. Đây là ưu tiên thử nhánh, không phải
giá trị bắt buộc để lan truyền; 1 cũng truyền sai khác khi chỉ có một
đầu vào mang D/D' và các đầu vào khác là nhị phân xác định.

Ví dụ XOR(D,X): thử đầu vào bên cạnh bằng 0 được D; nếu nó bằng 1 thì
được D'. XNOR(D,0)=D', XNOR(D,1)=D. PODEM chấp nhận cả D và D' tại PO.
Với nhiều X, đặt từng objective rồi backtrace về PI, imply lại sau mỗi
quyết định; không gán tất cả net nội bộ cùng lúc.

Không suy ra “frontier có D nên chắc chắn truyền được”: XOR(D,D,X)
còn đầu ra X, nhưng khi đầu vào cuối thành 0/1 thì đầu ra không có D/D'.
Mỗi lần imply phải tính lại frontier; nếu đường này tắt thì xét đường
khác hoặc quay lui theo điều kiện thất bại chung. Không cắt nhánh chỉ
dựa trên parity hiện tại nếu còn X và chưa chứng minh tính bất khả thi.

## 5. Backtrace mục tiêu (y,v)

v là bit mong muốn trên **mạch tốt**. Với đầu vào đã xác định, lấy bit
tốt: `good(0)=0`, `good(1)=1`, `good(D)=1`, `good(D')=0`.
Đặt p là XOR các bit tốt của đầu vào đã biết; XOR tập rỗng bằng 0.
Đặt U là danh sách đầu vào X theo Gate.inputs.

1. Nếu U có đúng một đầu vào u, mục tiêu con là **(u, v ⊕ q ⊕ p)**.
2. Nếu U có từ hai đầu vào trở lên, mục tiêu con là **(U[0], 0)**.
   Đây là heuristic cố định của P3-v1.1. Sau khi gán PI và imply,
   tính lại p và U; đến đầu vào X cuối cùng mới dùng công thức ở bước 1.
   Không giả vờ các X còn lại đã bằng 0. Quyết định đầu tiên có thể chưa
   đạt mục tiêu y, hoặc tái hội tụ có thể làm mục tiêu không còn đạt được.
3. Nếu U rỗng, kiểm tra parity tốt `p ⊕ q` với v: mục tiêu đã đạt hoặc
   mâu thuẫn tại trạng thái hiện tại. Không tạo quyết định PI mới từ cổng
   này, không quay lại chọn một PI đã gán. Trình điều khiển phải imply/
   chọn lại objective hoặc xử lý nhánh thất bại, tùy trạng thái toàn mạch.

Tiếp tục backtrace mục tiêu con qua các cổng cho tới PI chưa gán.
Chỉ PI được gán. DFS vẫn thử cả bit ưu tiên và bit đảo nếu cần; giá trị
ưu tiên 0 không được dùng làm lý do loại nhánh 1. Các ràng buộc từ mạch
tái hội tụ được kiểm tra bằng imply và backtrack, không bằng công thức
parity riêng lẻ. Nếu trạng thái năm giá trị làm mất bit tốt (ví dụ cặp
(1,X) bị rút thành X), có thể giữ rail tốt riêng; không tự đoán bit tốt.

Ví dụ mục tiêu y=1:

| Cổng và trạng thái | p | q | Mục tiêu con |
|---|---|---|---|
| y=XOR(a,b), a=1, b=X | 1 | 0 | b=0 |
| y=XNOR(a,b), a=1, b=X | 1 | 1 | b=1 |
| y=XOR(a,b,c), a=1, b=0, c=X | 1 | 0 | c=0 |
| y=XOR(a,b), a=D', b=X | 0 | 0 | b=1 |

## 6. Ví dụ từng bước để P5 đối chiếu

Mạch tối thiểu: PI theo thứ tự (a,b), PO y, `y=XOR(a,b)` hoặc
`y=XNOR(a,b)`. Mỗi ví dụ khởi tạo a=b=X; lỗi là stem, giới hạn đủ.

| Mạch/lỗi | Objective lần lượt | PI được gán lần lượt | y sau imply | Pattern; backtracks |
|---|---|---|---|---|
| XOR, y/SA0 | (y,1), (y,1) | a=0, b=1 | X, D | 01; 0 |
| XNOR, y/SA0 | (y,1), (y,1) | a=0, b=0 | X, D | 00; 0 |
| XOR, a/SA0 | (a,1), (b,0) | a=1, b=0 | X, D | 10; 0 |
| XNOR, a/SA0 | (a,1), (b,0) | a=1, b=0 | X, D' | 10; 0 |

Bốn ví dụ đều kỳ vọng DETECTED. Hai dòng đầu kiểm tra **backtrace** qua
cổng parity; hai dòng sau kiểm tra **objective lan truyền** qua frontier.
Đây là ví dụ bổ sung, không thay hai golden trace bảy cột của nhóm.
P5 cần kiểm tra cả XOR/XNOR nhiều đầu vào, triệt tiêu D/D', tái hội tụ,
backtrack và giới hạn trước khi kết luận lõi hỗ trợ đầy đủ.

## 7. Căn cứ và giới hạn

- [Bài giảng ATPG, University of New Mexico](https://ece-research.unm.edu/jimp/vlsi_test/slides/html/combinational_atpg2.html):
  phần PODEM có ví dụ backtrace qua XOR, gán từng PI, imply rồi tiếp tục
  biện minh mục tiêu chưa đạt; lựa chọn theo controllability có thể cần quay lui.
- [Bài giảng parity, University of New Brunswick](https://www.ece.unb.ca/tervo/ece4253/ecc.shtml):
  XOR là cộng modulo 2. Các công thức, bảng D/D' và quy tắc triệt tiêu
  ở đây được suy ra trực tiếp từ định nghĩa Boolean và cặp tốt/lỗi.
- Ưu tiên X đầu tiên và bit 0 khi còn nhiều X là **quy ước P3-v1.1**,
  không gán cho bài Goel, không gọi là SCOAP, chưa nhận xác nhận áp dụng từ P5.
- Bổ sung này không thay hợp đồng branch fault hoặc multiple faults;
  không dùng kết quả kiểm tra parity cục bộ để tuyên bố đã kiểm chứng lõi P5.
