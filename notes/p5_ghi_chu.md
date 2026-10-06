# P5 — Ghi chú triển khai PODEM

## 1. Phạm vi

P5 triển khai thuật toán PODEM cho mạch logic tổ hợp sử dụng logic năm giá trị.

Các bước chính gồm:

- Imply

- Objective

- Backtrace

- Gán Primary Input

- Backtrack

- Kiểm tra phát hiện fault

PODEM cũng hỗ trợ danh sách Fault tương ứng với các fault-frame
của mạch tuần tự sau khi unroll.

## 2. Logic năm giá trị

Sử dụng năm giá trị:

- 0

- 1

- X

- D

- D'

Trong đó:

- D biểu diễn good=1, faulty=0.
- D' biểu diễn good=0, faulty=1.

Pattern của Primary Input chỉ sử dụng các giá trị:

- 0
- 1
- X

Giá trị D và D' được sử dụng trong quá trình implication
và biểu diễn sự khác nhau giữa mạch tốt và mạch lỗi.

## 3. Objective

Khi fault chưa được kích hoạt, Objective đặt net lỗi về giá trị
đối lập với stuck-at value.

Sau khi fault được kích hoạt, Objective được chọn trên D-frontier
để lan truyền D hoặc D' về Primary Output.

Với cổng XOR/XNOR trong D-frontier:

- Chọn đầu vào X đầu tiên theo thứ tự Gate.inputs.
- Đặt Objective cho đầu vào đó bằng 0.
- Sau khi gán Primary Input và implication lại, Objective được
  tính lại từ trạng thái mới.

D và D' đều được xem là fault effect có thể phát hiện khi xuất hiện
tại Primary Output.

## 4. Backtrace

Backtrace đưa Objective từ một net trung gian về Primary Input.

Thứ tự lựa chọn được giữ xác định theo thứ tự ngõ vào của gate.

Với NAND, NOR và NOT, giá trị Objective được đảo.

Với AND, OR và BUFF, giá trị Objective được giữ nguyên.

Với XOR/XNOR:

- XOR tương ứng với q=0.
- XNOR tương ứng với q=1.
- Tính giá trị trên rail tốt của các đầu vào đã biết.
- Nếu còn đúng một đầu vào X, giá trị Objective của đầu vào đó
  được tính theo tính chẵn lẻ của các đầu vào đã biết.
- Nếu còn nhiều đầu vào X, chọn đầu vào X đầu tiên theo thứ tự
  Gate.inputs và ưu tiên giá trị 0.
- Không coi các đầu vào X còn lại là đã bằng 0.
- Tiếp tục backtrace cho đến Primary Input chưa được gán.

## 5. Backtrack

Các quyết định của Primary Input được lưu trong decision stack.

Nếu nhánh hiện tại thất bại, giá trị quyết định được đảo và thuật toán
tiếp tục thử nhánh còn lại.

Số lần backtrack chỉ tăng khi thực sự chuyển sang nhánh mới.

Sau khi backtrack, pattern được tạo lại từ decision stack và
imply được thực hiện lại trước khi tiếp tục.

Trong trace, thao tác backtrack không được ghi như một lần
Backtrace mới; trạng thái net và D-frontier phải phản ánh trạng thái
sau implication mới.

## 6. D-frontier

D-frontier được cập nhật sau mỗi lần implication.

Thuật toán kết thúc thành công khi một Primary Output có giá trị
D hoặc D'.

## 7. Fault injection

Stem fault tác động đến các fanout của net.

Branch fault chỉ tác động đến branch được chỉ định.

Khi cấy stuck-at vào một giá trị logic 5 giá trị:

- Giữ nguyên rail của mạch tốt.
- Ép rail của mạch lỗi về stuck-at value.

Do đó:

- D + SA0 -> D
- D + SA1 -> 1
- D' + SA0 -> 0
- D' + SA1 -> D'

Cách xử lý này tránh tạo ra fault effect D/D' giả khi fault được
cấy lặp lại trên các frame.

## 8. Fault-frame

PODEM nhận được Fault hoặc danh sách Fault tương ứng với các
fault-frame sau khi mạch tuần tự được unroll.

Với danh sách Fault, imply() sử dụng toàn bộ danh sách fault-instance,
trong khi từng fault-frame lần lượt được chọn làm target cho
Objective -> Backtrace.

## 9. Kết quả kiểm thử

Lệnh kiểm thử:

```text
$env:PYTHONPATH = "src"
python -m pytest -q