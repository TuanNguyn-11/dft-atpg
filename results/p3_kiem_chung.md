# Kết quả kiểm chứng P3

Đã chạy `python3 notes/p3_kiem_chung.py`; mọi assertion PASS.

- c17 11/SA0: duyệt toàn bộ 32 vector; có 18 vector phát hiện lỗi.
- Pattern X10XX là một tập con gồm 8 vector: tất cả đều phát hiện lỗi.
- Golden trace chính: objective, PI, net và frontier khớp kết quả tham chiếu; 2 bước, 0 backtrack.
- Golden trace phụ: 3 bước, 1 backtrack; vector phát hiện duy nhất 01 trong 4 vector.
- 113 phép so sánh cặp tốt/lỗi cho giá trị net xác định của hai golden trace trên mọi cách điền X đều đúng.
- Kiểm tra bổ sung 22 lỗi stem c17: mọi pattern tham chiếu khớp oracle nhị phân, mọi hàng trace có giá trị xác định hợp lệ. Không phát sinh backtrack theo P3-v1.
- Phạm vi không bao gồm branch fault. Không phải kết quả thực thi code P5/P6.
- Script tham chiếu này không kiểm giới hạn; kết quả code P5 thật và ABORTED 0/1 ở results/p3_doi_chieu_code.md (chạy notes/p3_doi_chieu_code.py).

| Lỗi stem c17 | Pattern tham chiếu | Backtracks | Số vector phát hiện /32 |
|---|---|---:|---:|
| 1/SA0 | 101XX | 0 | 6 |
| 1/SA1 | 001XX | 0 | 6 |
| 2/SA0 | X10XX | 0 | 11 |
| 2/SA1 | X00XX | 0 | 11 |
| 3/SA0 | 11111 | 0 | 9 |
| 3/SA1 | 11011 | 0 | 9 |
| 6/SA0 | X1111 | 0 | 6 |
| 6/SA1 | X1101 | 0 | 6 |
| 7/SA0 | X00X1 | 0 | 6 |
| 7/SA1 | X00X0 | 0 | 6 |
| 10/SA0 | 00XXX | 0 | 14 |
| 10/SA1 | 101XX | 0 | 6 |
| 11/SA0 | X10XX | 0 | 18 |
| 11/SA1 | X1111 | 0 | 6 |
| 16/SA0 | 00XXX | 0 | 19 |
| 16/SA1 | X10XX | 0 | 11 |
| 19/SA0 | XX11X | 0 | 14 |
| 19/SA1 | X00X1 | 0 | 6 |
| 22/SA0 | 1X1XX | 0 | 18 |
| 22/SA1 | 00XXX | 0 | 14 |
| 23/SA0 | X10XX | 0 | 18 |
| 23/SA1 | X011X | 0 | 14 |
