# Bàn giao P3 — cập nhật sau tích hợp 06/10/2026

**Bổ sung 06/10/2026:** bàn giao [quy tắc XOR/XNOR P3-v1.1](p3_xor_xnor.md)
để xử lý thiếu sót lý thuyết ở lỗi số 1. Đọc kèm hợp đồng đã cập nhật;
hai golden trace vẫn dùng các lựa chọn P3-v1. P5 đã áp dụng và đã kiểm thử
trên base `8564678`; xem [phiếu đối chiếu](p3_doi_chieu_P5.md).

P3 cung cấp lý thuyết PODEM, hợp đồng lựa chọn P3-v1, hai golden trace,
mạch backtrack, chương báo cáo ngắn, ba slide, hình TikZ và kiểm chứng
độc lập. Đã hoàn tất P3-01/02/03 theo feedback: đối chiếu API/exporter P5,
xác nhận simulator P6 và giới hạn dừng, cập nhật nội dung và ba slide.
Không nhận đã hoàn tất các việc con người như diễn tập hoặc nộp bài.

## P5 đọc theo thứ tự

1. [Quy tắc P3-v1](p3_quy_tac_P5.md): thứ tự netlist, objective,
   backtrace, imply, frontier, cách đếm backtrack và ABORTED.
2. [Golden trace c17](../results/golden_trace_c17_11sa0.md): PI (1,2,3,6,7),
   objective (11,1) → 3=0, rồi (2,1) → 2=1; X10XX, 2 gán, 0 backtrack,
   22=D, frontier cuối {19,23}.
3. [Mạch phụ](../circuits/backtrack_example.bench) và
   [trace backtrack](../results/golden_trace_backtrack.md): a=1 thất bại,
   đảo a=0, rồi b=1; 01, 3 hàng, 1 backtrack. Giới hạn 0: ABORTED;
   giới hạn 1: DETECTED đã chạy trên code P5.
4. [Phiếu đối chiếu](p3_doi_chieu_P5.md): nguồn P2, đủ bảy cột API/exporter,
   mọi net, simulator P6 và khác biệt ngữ nghĩa nhãn hành động.
5. [Bộ kiểm chứng độc lập](p3_kiem_chung.py) và
   [kiểm tra file bàn giao](p3_kiem_tra_ban_giao.py),
   [kiểm code thật](p3_doi_chieu_code.py) và [35 ô bằng chứng](../results/p3_doi_chieu_code.md).

P5 đã bàn giao exporter theo quy ước golden trong repo. Nếu dùng heuristic khác,
phải công bố heuristic và giải thích từng khác biệt; không sửa trace để che lỗi.

## Tái lập từ gốc repo

```text
python -B notes/p3_kiem_chung.py
python -B notes/p3_kiem_tra_ban_giao.py
python -B notes/p3_doi_chieu_code.py
python -m pytest -q
```

Script đầu cập nhật `results/p3_kiem_chung.md`. Script sau chỉ đọc file,
đối chiếu bảy cột trace với tham chiếu; kiểm tra netlist phụ và quy ước LaTeX.
Netlist c17 P6 đã có và kiểm tra khớp đặc tả. Script thứ ba gọi parser P6,
lõi P5 và simulator P6 thật, đồng thời kiểm file exporter; không dùng
implementation tham chiếu. Ba script chỉ dùng thư viện chuẩn và code repo.

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
bib P3 và slide P3; không cần thay wrapper. Hình TikZ P2 đã có trên main;
Chương 4 dùng hình chung, hình dự phòng P3 chỉ dùng nếu thiếu file.
Các đề xuất ngoài phạm vi P3 và ngân sách trang được ghi ở `p3_review.md`.

## Checklist nghiệm thu và việc con người

- [x] P3-01: 35 ô đối chiếu golden/API/exporter, giải thích hai nhãn API khác;
  file trace backtrack P5 đã có. Giữ golden không đổi.
- [x] P3-02: cube c17 8/8, PO cụ thể, mẫu phụ 01, ABORTED/DETECTED 0/1.
- [x] P3-03: lý thuyết, Chương 4, ba slide và ghi chú cập nhật; số liệu P2
  4 cube/3 PI/0 backtrack, PODEM 2 PI/0 backtrack; không suy ra tốc độ.
- [x] Bộ kiểm thử tích hợp 342 passed; các script P2/P3 PASS.
- [ ] P1 review và tích hợp bản P3 này, build lại PDF bản nộp/phát hành nếu cần.
- [ ] P3 tập trình bày phần mình, cùng nhóm diễn tập thuyết trình/demo 20 phút.
- [ ] P1 quay video 2–3 phút; xác nhận giờ/kênh/định dạng nộp ngày 08/10/2026.
- [ ] P1 duyệt và nộp sản phẩm cuối; ngân sách báo cáo 5–10 trang nội dung.

Không còn phụ thuộc code P5/P6 để hoàn tất phần kỹ thuật P3. Các dấu chưa
chọn là công việc con người, không phải kết quả agent có thể tự xác nhận.
