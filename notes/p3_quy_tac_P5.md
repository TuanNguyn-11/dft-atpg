# Hợp đồng trace P3 → P5 — phiên bản P3-v1.1, 06/10/2026

Bổ sung cho lỗi số 1: [quy tắc XOR/XNOR](p3_xor_xnor.md), gồm parity,
imply, objective lan truyền, backtrace và bốn ví dụ kỳ vọng. P3-v1.1
kế thừa toàn bộ quy tắc P3-v1 dưới đây; hai golden trace cũ không đổi.

Đây là đặc tả do P3 bàn giao để P5 triển khai, chưa phải xác nhận P5 đã áp dụng. Không thay chữ ký API của prompt.md. Phạm vi golden trace: một lỗi stem trên mạch tổ hợp AND/NAND/OR/NOR/NOT/BUFF. Phần XOR/XNOR, branch fault và danh sách lỗi trải khung thuộc phạm vi lõi chung nhưng chưa được hai golden trace này kiểm chứng.

## 1. Thứ tự xác định
- PI, PO và ngõ vào mỗi cổng giữ đúng thứ tự trong .bench.
- Topological order ổn định: trong các cổng đã sẵn sàng, chọn cổng xuất hiện trước trong .bench. Không dựa vào set hoặc thứ tự chuỗi tên net.
- D-frontier liệt kê theo topological order đó.
- Chọn cổng D-frontier đầu tiên còn X-path tới ít nhất một PO; chọn ngõ vào X đầu tiên theo Gate.inputs.
- Backtrace chọn ngõ vào X đầu tiên theo Gate.inputs. Không dùng level/SCOAP trong P3-v1. Đây là heuristic đơn giản, xác định được, không phải tuyên bố đây là lựa chọn tốt nhất của PODEM.
- Dừng ngay khi bất kỳ PO có D hoặc D'. Không tiếp tục chỉ vì D-frontier chưa rỗng.

## 2. Objective, backtrace và imply
Nếu lỗi chưa kích hoạt và giá trị tại vị trí lỗi còn X, objective = (fault.net, 1-stuck_at). Nếu net đã bằng stuck_at (0/1 xác định), nhánh hiện tại thất bại. Sau kích hoạt, objective đặt một ngõ vào X của cổng D-frontier về giá trị không điều khiển: AND/NAND là 1; OR/NOR là 0.

Backtrace đi từ objective về một PI chưa gán. Mỗi khi đi qua NAND/NOR/NOT, đảo giá trị mục tiêu đúng một lần; AND/OR/BUFF không đảo. Không ghi trực tiếp objective vào net nội bộ. Với AND cần 1 hoặc OR cần 0, gán một ngõ vào mới chưa chắc đủ đạt objective: imply rồi chọn objective tiếp. Quy tắc đảo này không áp dụng nguyên xi cho XOR/XNOR.

**XOR/XNOR (P3-v1.1):** objective lan truyền chọn đầu vào X đầu tiên,
ưu tiên 0. Backtrace mục tiêu đầu ra v: đặt q=0 cho XOR, q=1 cho XNOR,
p là XOR các bit mạch tốt đã biết (D→1, D'→0). Nếu còn đúng một X,
đưa đầu vào đó về v ⊕ q ⊕ p; nếu còn nhiều X, chọn X đầu tiên và thử 0.
Imply rồi tính lại; không coi X còn lại là 0. Nếu không còn X, kiểm tra
mục tiêu đã đạt/mâu thuẫn, không sinh thêm quyết định từ cổng đó.
Không có giá trị điều khiển; sai khác có thể triệt tiêu khi nhiều D/D'
gặp nhau. Chi tiết, điều kiện áp dụng và ví dụ ở tài liệu bổ sung.

PI trong pattern chỉ là 0/1/X. Sau mỗi lần gán, đảo hoặc khôi phục PI, mô phỏng lại từ PI theo topo và cấy lỗi. Stem fault tác động đến tất cả nhánh fanout. 0=(0,0), 1=(1,1), D=(1,0), D'=(0,1), X=(X,X). Một cặp chỉ xác định được một thành phần, như (X,0), được trừu tượng hóa bảo thủ thành X trong logic 5 giá trị; không tự biến nó thành 0. Cần giữ giá trị mạch tốt trước cấy lỗi khi kiểm tra kích hoạt nếu dùng mô phỏng hai rail.

## 3. D-frontier và X-path
D-frontier gồm cổng có đầu ra X và ít nhất một đầu vào D/D'. D-frontier là tập cổng (ghi tên net đầu ra), không phải tập mọi dây X. Tính lại toàn bộ sau mỗi imply, kể cả hàng thành công.

X-path cho hợp đồng này: bắt đầu tại đầu ra X của cổng D-frontier, duyệt theo fanout qua các net đầu ra X, tìm một PO có giá trị X; nếu điểm bắt đầu là PO thì đạt. Đây là kiểm tra cấu trúc bảo thủ: tồn tại đường X không đảm bảo mọi ràng buộc tái hội tụ đều thỏa. Chỉ dùng việc không có X-path để cắt nhánh sau khi đã kích hoạt lỗi và chưa có D/D' ở PO. D-frontier rỗng khi lỗi chưa kích hoạt không đủ để tuyên bố thất bại.

## 4. Quay lui và giới hạn
DFS hai nhánh: thử giá trị backtrace trước, rồi giá trị ngược lại. Nếu cả hai thất bại, trả PI về X và trở lại mức cha. Xóa mọi quyết định con trước khi đảo quyết định cha; mô phỏng lại để không giữ các net suy ra từ nhánh cũ.

backtracks = số lần thực sự đảo PI sang nhánh thứ hai. Không đếm lần đầu gán PI; không đếm reset PI về X. max_backtracks=0 vẫn cho thử đường đầu tiên. Trước mỗi phép đảo, nếu backtracks >= max_backtracks thì trả ABORTED và lan truyền trạng thái này, không chuyển thành UNTESTABLE. Kết luận UNTESTABLE chỉ khi toàn bộ cây đã được duyệt/cắt nhánh hợp lệ và không bị giới hạn. Không dùng bộ đếm số hàng trace thay cho số backtrack.

## 5. Định dạng trace
Giữ nguyên 7 cột của prompt. Một hàng cho mỗi gán/đảo PI sau imply; không tính trạng thái khởi tạo là bước 1. Với thao tác reset, nếu có, thêm hàng Gán PI = pi=X, Objective và Backtrace là “—”, Hành động = backtrack, nhưng không tăng bộ đếm. Hàng đảo PI không gọi objective/backtrace mới: ghi “— (đảo quyết định trước)” và “—”.

Hành động mô tả bước xử lý sau trạng thái của hàng: thành công được ưu tiên nếu PO có D/D'; nếu nhánh bế tắc và còn lựa chọn thì backtrack; nếu còn tìm tiếp thì tiếp tục; nếu đã hết toàn cây thì thất bại. Với ABORTED giữ status riêng trong phần kết luận, không thêm một từ mới vào cột Hành động. Hàng cuối trước khi dừng giới hạn có thể vẫn ghi backtrack (hành động cần làm nhưng bị chặn); thêm lý do giới hạn ở dưới bảng.

steps là list[dict] nhưng prompt chưa chốt key. Đề xuất P5 dùng: step, objective (list [net,int] hoặc null), backtrace (list [PI,int] hoặc null), assignment (dict PI→string), values (dict net→string), d_frontier (list[str]), action (4 từ đúng quy định). Đây là đề xuất bổ sung, không đổi PodemResult hay podem().

## 6. Kết quả P5 cần tái hiện
| Mạch/lỗi | PI theo thứ tự | Pattern | Hàng gán/đảo | Backtracks | PO quan sát |
|---|---|---|---:|---:|---|
| c17, 11/SA0 stem | 1,2,3,6,7 | X10XX | 2 | 0 | 22=D |
| backtrack_example, t/SA0 stem | a,b | 01 | 3 | 1 | out=D |

Cả hai status=DETECTED khi giới hạn đủ. Với mạch phụ và max_backtracks=0: ABORTED sau a=1, backtracks=0. Với giới hạn 1: DETECTED, backtracks=1. Ví dụ phụ không phải mạch Hình 4.5.

## 7. Những chỗ dễ sai
1. D-frontier hàng thành công của c17 là {19,23}, không phải rỗng.
2. Vector X10XX có X tại 1,6,7; không được đổi thành một vector chỉ có 4 bit.
3. Gán X=0 chỉ khi chuyển sang mô phỏng nhị phân: X10XX → 01000.
4. Backtrack a=1→a=0 không có objective mới; t từ D trở lại X là đúng.
5. UNTESTABLE khác ABORTED. Một nhánh thất bại chưa chứng minh lỗi không thể phát hiện.
6. Chưa được tuyên bố logic XOR/branch/multiple faults đã đúng chỉ nhờ vượt qua hai ví dụ này.
