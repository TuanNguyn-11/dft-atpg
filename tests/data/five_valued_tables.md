# Bảng chuẩn logic năm giá trị — P2

Dữ liệu cho P5 đối chiếu `eval_gate` và `tests/test_logic.py`.
Ký hiệu giao tiếp chính xác: `"0"`, `"1"`, `"X"`, `"D"`, `"D'"`.
Thứ tự hàng/cột: `0, 1, X, D, D'`; hàng là ngõ vào a, cột là b.

## Quy tắc tính và giới hạn

| Giá trị | Mạch tốt | Mạch lỗi |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 1 | 1 |
| X | Chưa biết | Chưa biết |
| D | 1 | 0 |
| D' | 0 | 1 |

Tính riêng từng thành phần bằng logic ba giá trị: AND có 0 thì ra 0,
OR có 1 thì ra 1; nếu chưa đủ thông tin thì ra chưa biết. XOR có ngõ vào
chưa biết thì ra chưa biết. NAND/NOR/XNOR đảo kết quả tương ứng.
Cặp có ít nhất một thành phần chưa biết được quy về X vì API chỉ có năm giá trị.
Việc này có thể mất thông tin, nhưng không tạo sai khác chắc chắn khi chưa biết.

X trong bảng mô phỏng là chưa biết. X trong test cube là ràng buộc để trống;
chỉ gọi là don't-care khi các cách điền đã được kiểm chứng. Bảng cổng không
lưu tương quan giữa các net: không suy ra XOR(X,X)=0 chỉ từ hai ký hiệu X.
Nếu hai chân nối cùng một net, việc khai thác tương quan phải được xử lý riêng.


## AND

| a \ b | 0 | 1 | X | D | D' |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | X | D | D' |
| X | 0 | X | X | X | X |
| D | 0 | D | X | D | 0 |
| D' | 0 | D' | X | 0 | D' |

## NAND

| a \ b | 0 | 1 | X | D | D' |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 0 | X | D' | D |
| X | 1 | X | X | X | X |
| D | 1 | D' | X | D' | 1 |
| D' | 1 | D | X | 1 | D |

## OR

| a \ b | 0 | 1 | X | D | D' |
|---|---|---|---|---|---|
| 0 | 0 | 1 | X | D | D' |
| 1 | 1 | 1 | 1 | 1 | 1 |
| X | X | 1 | X | X | X |
| D | D | 1 | X | D | 1 |
| D' | D' | 1 | X | 1 | D' |

## NOR

| a \ b | 0 | 1 | X | D | D' |
|---|---|---|---|---|---|
| 0 | 1 | 0 | X | D' | D |
| 1 | 0 | 0 | 0 | 0 | 0 |
| X | X | 0 | X | X | X |
| D | D' | 0 | X | D' | 0 |
| D' | D | 0 | X | 0 | D |

## XOR

| a \ b | 0 | 1 | X | D | D' |
|---|---|---|---|---|---|
| 0 | 0 | 1 | X | D | D' |
| 1 | 1 | 0 | X | D' | D |
| X | X | X | X | X | X |
| D | D | D' | X | 0 | 1 |
| D' | D' | D | X | 1 | 0 |

## XNOR

| a \ b | 0 | 1 | X | D | D' |
|---|---|---|---|---|---|
| 0 | 1 | 0 | X | D' | D |
| 1 | 0 | 1 | X | D | D' |
| X | X | X | X | X | X |
| D | D' | D | X | 1 | 0 |
| D' | D | D' | X | 0 | 1 |

## NOT

| Input | 0 | 1 | X | D | D' |
|---|---|---|---|---|---|
| Output | 1 | 0 | X | D' | D |

## BUFF

| Input | 0 | 1 | X | D | D' |
|---|---|---|---|---|---|
| Output | 0 | 1 | X | D | D' |

## Kiểm tra nhanh và lan truyền

- AND(D,1)=D; AND(D,D')=0; AND(D,0)=0; AND(D,X)=X.
- OR(D,0)=D; OR(D,D')=1; OR(D,1)=1; OR(D,X)=X.
- XOR(D,D)=0; XOR(D,D')=1; XOR(D,1)=D'; XOR(D,0)=D.
- NOT(D)=D'; NOT(D')=D; NOT(X)=X; BUFF giữ nguyên.
- AND/NAND: ngõ vào phụ bằng 1 cho sai khác đi qua; 0 chặn.
- OR/NOR: ngõ vào phụ bằng 0 cho sai khác đi qua; 1 chặn.
- XOR/XNOR: ngõ vào phụ phải biết; 0/1 quyết định cực sai khác.
- Cổng nhiều ngõ vào: tính từng thành phần trên toàn bộ danh sách rồi ghép; các bảng trên chỉ dành cho hai ngõ vào.

## Phạm vi và nguồn

160 ô: sáu bảng hai ngõ vào × 25, hai bảng một ngõ vào × 5.
Các ô được tính từ quy tắc tốt/lỗi, không sao chép bảng từ tài liệu.
Bối cảnh D-calculus: Roth (1966), DOI https://doi.org/10.1147/rd.104.0278.
Xem trace và bằng chứng kiểm tra trong `notes/p2_ghi_chu.md`.
DFF thuộc phần tuần tự, không thuộc tám bảng này.
