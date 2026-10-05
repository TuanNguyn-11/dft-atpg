# Golden trace — c17, 11/SA0 (stem)

Phiên bản P3-v1; áp dụng notes/p3_quy_tac_P5.md. PI=(1,2,3,6,7); PO=(22,23); topo=(10,11,16,19,22,23). Khởi tạo mọi PI và net là X. Không tính khởi tạo thành một bước. Đây là trace chạy tay đã kiểm chứng bằng mô phỏng nhị phân độc lập; chưa phải trace code của P5.

```text
10 = NAND(1,3)
11 = NAND(3,6)
16 = NAND(2,11)
19 = NAND(11,7)
22 = NAND(10,16)
23 = NAND(16,19)
```

| Bước | Objective (net, giá trị) | Backtrace → PI | Gán PI | Giá trị các net sau imply | D-frontier | Hành động |
|---|---|---|---|---|---|---|
| 1 | (11,1) | NAND(3,6), chọn 3; đảo 1→0 ⇒ 3=0 | 3=0 | PI=(X,X,0,X,X); 10=1, 11=D, 16=X, 19=X, 22=X, 23=X | {16,19} | tiếp tục |
| 2 | (2,1) | 2 đã là PI ⇒ 2=1 | 2=1 | PI=(X,1,0,X,X); 10=1, 11=D, 16=D', 19=X, 22=D, 23=X | {19,23} | thành công |

## Giải thích
Bước 1: muốn kích hoạt 11/SA0 phải làm 11 tốt bằng 1. NAND chỉ cần một đầu vào 0; ngõ vào đầu tiên là 3. Khi 3=0 thì 10=1, 11 tốt=1 và 11 lỗi=0, nên 11=D. Hai cổng 16 và 19 có đầu vào D, đầu ra X. Cả hai còn X-path; chọn cổng 16 vì xuất hiện trước.

Bước 2: để lan truyền qua NAND16, đặt ngõ vào còn lại 2=1. Khi đó NAND(1,D)=D', và NAND(1,D')=D tại PO22. Dừng thành công dù D-frontier vẫn chứa 19 và 23. PO23 còn X không làm mất điều kiện phát hiện tại PO22.

## Kết quả
- status: DETECTED
- pattern: {"1":"X","2":"1","3":"0","6":"X","7":"X"}
- backtracks: 0; số gán PI: 2.
- Thay X=0: 01000. Mạch tốt (22,23)=(1,1); mạch lỗi (22,23)=(0,0).
- Cả 8 cách điền X trong X10XX đều phát hiện lỗi qua 22: 22 tốt=1, 22 lỗi=0.

Dùng logic 5 giá trị, PO23=X là xấp xỉ bảo thủ trong trace; sau khi điền đủ bit có thể xác định thêm. Không đổi các X giữa chừng chỉ để ép trace khớp mô phỏng nhị phân đầy đủ.
