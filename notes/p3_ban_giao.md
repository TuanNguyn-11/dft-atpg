# Bàn giao P3 — 05/10/2026

**Bổ sung 06/10/2026:** bàn giao [quy tắc XOR/XNOR P3-v1.1](p3_xor_xnor.md)
để xử lý thiếu sót lý thuyết ở lỗi số 1. Đọc kèm hợp đồng đã cập nhật;
hai golden trace vẫn dùng các lựa chọn P3-v1. Chưa xác nhận P5 đã áp dụng.

P3 cung cấp lý thuyết PODEM, hợp đồng lựa chọn P3-v1, hai golden trace,
mạch backtrack, chương báo cáo ngắn, ba slide, hình TikZ và kiểm chứng
độc lập. Chưa hoàn tất toàn bộ tiêu chí vì thiếu trace/code P5 và simulator P6.

## P5 đọc theo thứ tự

1. [Quy tắc P3-v1](p3_quy_tac_P5.md): thứ tự netlist, objective,
   backtrace, imply, frontier, cách đếm backtrack và ABORTED.
2. [Golden trace c17](../results/golden_trace_c17_11sa0.md): PI (1,2,3,6,7),
   objective (11,1) → 3=0, rồi (2,1) → 2=1; X10XX, 2 gán, 0 backtrack,
   22=D, frontier cuối {19,23}.
3. [Mạch phụ](../circuits/backtrack_example.bench) và
   [trace backtrack](../results/golden_trace_backtrack.md): a=1 thất bại,
   đảo a=0, rồi b=1; 01, 3 hàng, 1 backtrack. Giới hạn 0: ABORTED;
   giới hạn 1: DETECTED là kỳ vọng cần chạy trên code P5.
4. [Phiếu đối chiếu](p3_doi_chieu_P5.md): nguồn P2, từng mục P5/P6 còn thiếu.
5. [Bộ kiểm chứng độc lập](p3_kiem_chung.py) và
   [kiểm tra file bàn giao](p3_kiem_tra_ban_giao.py).

Đây là đặc tả P3, chưa nhận P5 xác nhận áp dụng. Nếu dùng heuristic khác,
phải công bố heuristic và giải thích từng khác biệt; không sửa trace để che lỗi.

## Tái lập từ gốc repo

```text
python -B notes/p3_kiem_chung.py
python -B notes/p3_kiem_tra_ban_giao.py
```

Script đầu cập nhật `results/p3_kiem_chung.md`. Script sau chỉ đọc file,
đối chiếu bảy cột trace với tham chiếu; kiểm tra netlist phụ và quy ước LaTeX.
Nếu `circuits/c17.bench` chưa có, nó báo PENDING và dùng c17 theo đặc tả nhóm;
nếu có, kiểm tra netlist đó có khớp đặc tả. Hai script chỉ dùng thư viện chuẩn.

Biên dịch theo README: từ `report`, XeLaTeX → Biber → XeLaTeX hai lượt;
từ `slides`, XeLaTeX nhiều lượt. Cần font TeX Gyre/Latin Modern, tiếng Việt,
biblatex và thư viện TikZ của main hiện tại. Không dùng wrapper ZIP thay main.
Kết quả và giới hạn môi trường ở [biên bản kiểm tra](p3_review.md).

## Để thuyết trình

Đọc [lý thuyết và lời dẫn](p3_ly_thuyet.md), [ghi chú tự kiểm tra](p3_ghi_chu.md).
Nắm rõ: objective khác gán net; D-frontier chưa rỗng vẫn có thể thành công;
X=0 chỉ khi chuyển sang mô phỏng nhị phân; ba hàng không phải ba backtrack;
ABORTED không đồng nghĩa UNTESTABLE; số chọn cube P2 khác số gán PI P3.

## P1 review/tích hợp

Giữ branch `p3-podem-ly-thuyet`, vào main bằng PR. Chỉ P1 merge.
Không chép preview/build/log/PDF trung gian. Hai main.tex đã nạp đủ các gói,
bib P3 và slide P3; không cần thay wrapper. Hình P2 đã có trên nhánh P2;
main chưa có nên P3 dùng hình dự phòng. Không nhập file P2 vào commit P3.
Các đề xuất ngoài phạm vi P3 và ngân sách trang được ghi ở `p3_review.md`.
