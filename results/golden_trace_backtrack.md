# Golden trace — backtrack_example, t/SA0 (stem)

Mạch do P3 thiết kế để minh họa quay lui, không gán cho ISCAS hoặc giáo trình. PI=(a,b); PO=(out); topo=(t,n,out). Áp dụng cùng P3-v1, chọn ngõ vào X đầu tiên. Khởi tạo mọi net X.

Hàm mạch tốt: out=(a+b)·NOT(a)=NOT(a)·b. Với t/SA0, out lỗi=0. Do đó vector phát hiện duy nhất là (a,b)=01.

| Bước | Objective (net, giá trị) | Backtrace → PI | Gán PI | Giá trị các net sau imply | D-frontier | Hành động |
|---|---|---|---|---|---|---|
| 1 | (t,1) | OR(a,b), chọn a ⇒ a=1 | a=1 | a=1, b=X; t=D, n=0, out=0 | ∅ | backtrack |
| 2 | — (đảo quyết định trước) | — | a=0 | a=0, b=X; t=X, n=1, out=X | ∅ | tiếp tục |
| 3 | (t,1) | a đã biết 0, chọn b đang X ⇒ b=1 | b=1 | a=0, b=1; t=D, n=1, out=D | ∅ | thành công |

Bước 1 kích hoạt lỗi nhưng n=0 chặn AND cuối. Mọi cách điền b đều cho out tốt=out lỗi=0. Không thể sửa nhánh này bằng gán thêm b.

Bước 2 đảo a=1 thành a=0; tăng backtracks từ 0 lên 1. Mô phỏng lại khiến t trở lại X: đây chưa phải thất bại vì lỗi còn có thể kích hoạt bằng b. Không được giữ t=D từ bước 1 hoặc kết luận thất bại chỉ vì D-frontier rỗng.

Bước 3 gán b=1, kích hoạt t=D và lan truyền ngay qua AND với n=1. Thành công không cần objective lan truyền riêng.

Kết quả: status=DETECTED; pattern={"a":"0","b":"1"}; backtracks=1; 3 hàng gán/đảo PI, 2 lần gọi objective/backtrace. Cây quyết định ở report/figures/p3/decision_tree.tex.

## Kiểm chứng tất cả 4 vector
| a | b | out tốt | out lỗi | Phát hiện |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | Không |
| 0 | 1 | 1 | 0 | Có |
| 1 | 0 | 0 | 0 | Không |
| 1 | 1 | 0 | 0 | Không |

Giới hạn backtrack: 0 ⇒ ABORTED trước bước 2; 1 ⇒ DETECTED. Không dùng ví dụ này để tuyên bố t/SA0 untestable.

## Lý do dùng mạch phụ
Kiểm tra tham chiếu với P3-v1 trên 22 lỗi stem của c17 không gặp backtrack. Kết luận này giới hạn ở 22 lỗi stem, không bao gồm branch fault hoặc mọi heuristic có thể có. Mạch phụ nằm trong phương án được P3.md cho phép.
