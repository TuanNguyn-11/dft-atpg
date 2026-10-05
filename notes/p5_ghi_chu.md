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

## 2. Logic năm giá trị

Sử dụng năm giá trị:
- 0
- 1
- X
- D
- D'

Trong đó D biểu diễn good=1, faulty=0 và D' biểu diễn good=0, faulty=1.

Pattern của Primary Input sử dụng các giá trị 0, 1 và X.

## 3. Objective

Khi fault chưa được kích hoạt, Objective đặt net lỗi về giá trị đối lập với stuck-at value.

Sau khi fault được kích hoạt, Objective được chọn trên D-frontier để lan truyền D hoặc D' về Primary Output.

## 4. Backtrace

Backtrace đưa Objective từ một net trung gian về Primary Input.

Thứ tự lựa chọn được giữ xác định theo thứ tự ngõ vào của gate.

NAND, NOR và NOT đảo giá trị Objective.

AND, OR và BUFF giữ nguyên giá trị Objective.

## 5. Backtrack

Các quyết định của Primary Input được lưu trong decision stack.

Nếu nhánh hiện tại thất bại, giá trị quyết định được đảo và thuật toán tiếp tục thử nhánh còn lại.

Số lần backtrack chỉ tăng khi thực sự chuyển sang nhánh mới.

## 6. D-frontier

D-frontier được cập nhật sau mỗi lần implication.

Thuật toán kết thúc thành công khi một Primary Output có giá trị D hoặc D'.

## 7. Fault branch

Stem fault tác động đến các fanout của net.

Branch fault chỉ tác động đến branch được chỉ định.

## 8. Fault-frame

PODEM nhận được Fault hoặc danh sách Fault tương ứng với các fault-frame sau khi mạch tuần tự được unroll.

## 9. Kết quả kiểm thử

Toàn bộ test hiện tại của project:

194 passed

Các trường hợp chính:
- c17, 11/SA0: DETECTED, pattern X10XX, 0 backtrack.
- backtrack example, t/SA0: DETECTED, pattern 01, 1 backtrack.
- max_backtracks = 0: ABORTED.
- branch fault: PASS.
- sequential fault-frame: PASS.