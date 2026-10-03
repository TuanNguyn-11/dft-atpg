# P2 — D-algorithm, bảng chuẩn và ví dụ c17

## Phạm vi và trạng thái

Thực hiện sản phẩm trước theo yêu cầu P2; chưa xác nhận sinh viên đã học hoặc
trả lời câu hỏi tự kiểm tra. Branch: `p2-d-algorithm`.
P2 sở hữu lý thuyết D-algorithm, bảng chuẩn, Chương 3 và slide riêng.
P5 sở hữu implementation logic/PODEM; P3 sở hữu golden trace PODEM;
P6 sở hữu netlist và fault simulator. Không có implementation D-algorithm ở đây.

Nội dung chi tiết được lưu tại ghi chú này để Chương 3 giữ ngắn theo README:
báo cáo nhóm 5–10 trang, hạn 08/10/2026; ngân sách Chương 3 khoảng một trang
là đề xuất P1. Không áp dụng dàn ý bảy trang hay lịch nộp 10/10 của bản cũ.

## 1. D-calculus và singular cover

Theo thứ tự (tốt,lỗi): 0=(0,0), 1=(1,1), D=(1,0), D'=(0,1).
X là chưa biết. Tính cổng riêng trên mỗi thành phần; cặp chỉ biết một thành
phần được rút về X trong API năm giá trị. X trong cube là chưa ràng buộc;
X trong mô phỏng là chưa biết. Không coi mọi X là don't-care an toàn.

Bảng chuẩn: `tests/data/five_valued_tables.md`, đủ AND/NAND/OR/NOR/XOR/XNOR
(5×5), NOT/BUFF (1×5). AND/NAND truyền qua ngõ vào phụ bằng 1;
OR/NOR qua ngõ vào phụ bằng 0. Cổng đảo đổi D và D'. XOR qua ngõ vào phụ 1
đổi cực; qua 0 giữ cực. Khi nhiều đường sai khác gặp nhau, phải tính cổng:
AND(D,D')=0, OR(D,D')=1, XOR(D,D')=1, XOR(D,D)=0.

Cube là gán bộ phận cho các net. Singular cover là tập các cube đầu vào/đầu
ra tối giản đủ mô tả hàm cổng. NAND z=NOT(a AND b), theo thứ tự (a,b,z):

| Cube | Giải thích |
|---|---|
| (0,X,1) | a=0 buộc z=1, bất kể b |
| (X,0,1) | b=0 buộc z=1, bất kể a |
| (1,1,0) | Cả hai bằng 1 để z=0 |

## 2. PDCF, PDC và D-intersection

PDCF (primitive D-cube of failure) mô tả điều kiện tạo sai khác tại lỗi.
NAND có lỗi đầu ra SA0: (0,X,D) hoặc (X,0,D). Lỗi đầu ra SA1:
(1,1,D'). Đây là cube tại cổng có lỗi, không dùng bảng NAND không lỗi
để tính đầu ra lỗi. Stem fault được cấy trước khi tín hiệu phân nhánh.

PDC (propagation D-cube) mô tả điều kiện truyền sai khác qua cổng không lỗi.
NAND: (D,1,D'), (1,D,D'), (D',1,D), (1,D',D).
Các tổ hợp (D,D,D') và (D',D',D) cũng truyền được; (D,D',1) che sai khác.

Giao cube hiện tại với cube mới theo từng net, khi cực D/D' đã cố định:

| ∩ | 0 | 1 | X | D | D' |
|---|---|---|---|---|---|
| 0 | 0 | ⊥ | 0 | ⊥ | ⊥ |
| 1 | ⊥ | 1 | 1 | ⊥ | ⊥ |
| X | 0 | 1 | X | D | D' |
| D | ⊥ | ⊥ | D | D | ⊥ |
| D' | ⊥ | ⊥ | D' | ⊥ | D' |

⊥ là xung đột, không phải giá trị mô phỏng thứ sáu. Bảng này là phép hợp nhất
ràng buộc cố định; không lẫn với phép tạo D-cube từ hai cover có đầu ra khác
nhau. Một PDC tổng quát có thể đổi đồng thời mọi D↔D' để thử cực còn lại
trước khi giao; không tự đổi cực của net đã được cấy lỗi.

## 3. Frontier, implication và backtrack

- D-frontier: cổng có ít nhất một đầu vào D/D', đầu ra còn X.
- J-frontier: cổng có đầu ra đã yêu cầu nhưng đầu vào chưa đủ justify yêu cầu.
- Implication tiến: tính các giá trị bắt buộc từ đầu vào đã biết.
- Implication lùi: suy ra yêu cầu đầu vào bắt buộc từ đầu ra. NAND ra 0
  buộc hai đầu vào bằng 1; NAND ra 1 có nhiều cover, cần chọn thay vì ép cả hai 0.
- Khi một cover/PDC có nhiều lựa chọn, lưu trạng thái và các lựa chọn chưa thử.
  Backtrack khôi phục toàn bộ gán, frontier và suy diễn phụ thuộc rồi thử lựa chọn khác.

Đầu ra có D/D' chưa đủ nếu vẫn còn yêu cầu nội bộ chưa justify. Thành công
đòi hỏi một gán PI nhất quán thực hiện được cube. Hết các lựa chọn tìm kiếm
đầy đủ mới kết luận untestable; hết giới hạn thì aborted.

### Mã giả khái niệm (không phải API Python)

```text
for each PDCF of the target fault:
    search(initial cube intersect PDCF)

search(cube):
    apply forward/backward implication with the fault injected
    if conflicting requirements: fail this branch
    refresh D-frontier and J-frontier
    if a PO carries D or D':
        if J-frontier is empty: return a consistent PI test cube
        choose an unjustified gate
        for each compatible singular-cover alternative:
            save state; search(cube intersect cover); restore on failure
    else:
        if D-frontier is empty: fail this branch
        choose a propagation gate (with a possible route to PO)
        for each compatible PDC and each alternative gate:
            save state; search(cube intersect PDC); restore on failure
    fail after exhausting all alternatives
```

Đây là trình bày rút gọn của kích hoạt → D-drive → consistency.
Trong trường hợp tổng quát, justification có thể phải xét riêng mạch tốt/lỗi
khi đầu vào mang sai khác; không dùng cover nhị phân để ép D thành 0/1.
Ví dụ dưới đây chỉ cần justify cổng 10, có đầu vào nhị phân.

## 4. c17 và trace D-algorithm 11/SA0

Netlist chung từ mục 5 `C:\DFT\DFT_ATPG\prompt.md`:

```text
PI: 1,2,3,6,7; PO: 22,23
10=NAND(1,3); 11=NAND(3,6)
16=NAND(2,11); 19=NAND(11,7)
22=NAND(10,16); 23=NAND(16,19)
```

Lỗi single stuck-at **stem 11/SA0**, tác động cả nhánh vào 16 và 19.
Chọn PDCF có 6=0 trước, rồi đường 11→16→22; chọn cover 3=0 để justify 10.
Đây là lựa chọn minh họa có chủ đích, không nhận là heuristic tối ưu.

Trong bảng, D-frontier/J-frontier ghi **tên net đầu ra của cổng**.
Suy diễn năm giá trị bảo thủ giữ X khi chưa đủ thông tin; không khai thác
tương quan fanout để điền net 23 sớm.

| Bước | Cube được chọn | Gán mới | Net sau implication | D-frontier | J-frontier | Hành động |
|---|---|---|---|---|---|---|
| 0 | Khởi tạo | PI đều X | Mọi net X | ∅ | ∅ | Chọn lỗi |
| 1 | PDCF (3,6,11)=(X,0,D) | 6=0; 11=D do cấy SA0 | 10=X,11=D,16=X,19=X,22=X,23=X | {16,19} | ∅ | Lỗi đã kích hoạt |
| 2 | PDC (2,11,16)=(1,D,D') | 2=1 | 10=X,11=D,16=D',19=X,22=X,23=X | {19,22,23} | ∅ | Lan truyền qua 16 |
| 3 | PDC (10,16,22)=(1,D',D) | Yêu cầu net nội bộ 10=1 | 10=1,11=D,16=D',19=X,22=D,23=X | {19,23} | {10} | PO có D; chưa thành công |
| 4 | Singular cover (1,3,10)=(X,0,1) | PI 3=0 | 10=1,11=D,16=D',19=X,22=D,23=X | {19,23} | ∅ | Thành công |

Không cần làm D-frontier rỗng: đã quan sát được sai khác tại PO 22 và
mọi yêu cầu đã justify. Cube PI cuối: **(X,1,0,0,X)**.

### Trạng thái cuối và kiểm chứng nhị phân

`report/figures/p2/c17_values.tex` chứa bảng net cuối và một cách điền cụ thể.
Hình người dùng cung cấp `C:\DFT\mach_c17.jpg` được sao chép vào
`report/figures/common/mach_c17.jpg`. Wrapper `common/c17.tex` dùng lại hình
trong báo cáo và slide. Đã đối chiếu đủ sáu cổng và các nhánh với netlist.
Hình thể hiện cube **sau tổng quát hóa**, có 6=X; trace trước đó giữ 6=0.
Theo yêu cầu dùng hình đã vẽ, wrapper chèn JPG thay cho bản vẽ TikZ mới:
đây là khác biệt có chủ đích với yêu cầu TikZ của P2.md, cần P1 biết khi review.

| PI (1,2,3,6,7) | PO tốt (22,23) | PO lỗi (22,23) |
|---|---|---|
| 01000 | (1,1) | (0,0) |
| 01001 | (1,1) | (0,0) |
| 11000 | (1,1) | (0,0) |
| 11001 | (1,1) | (0,0) |

Toàn bộ bốn cách điền phát hiện lỗi tại 22. Có thể bỏ 6=0 **sau kiểm chứng**:
3=0 đã buộc 11 tốt bằng 1. Cube tổng quát hóa (X,1,0,X,X) có tám cách điền,
tất cả được script P1 kiểm tra. Không xóa 6=0 khỏi trace để làm như chưa từng chọn.

### Số liệu giao cho P3

- 4 lần chọn cube: 1 PDCF, 2 PDC, 1 singular cover.
- 0 backtrack trong đường tìm kiếm đã trình bày.
- 3 PI đã gán trong trace: 6=0, 2=1, 3=0; một yêu cầu nội bộ: 10=1.
- Khởi tạo, implication và tổng quát hóa sau kiểm chứng không tính là chọn cube.
- Không so trực tiếp 4 với số vòng objective/backtrace của PODEM. Hai thuật toán
  phải công bố đơn vị đếm, lựa chọn và phạm vi để bảng so sánh có ý nghĩa.
- Đây là trace chạy tay, không phải thời gian chạy hay số đo implementation.

## 5. Fanout hội tụ và giới hạn

Net 3 rẽ vào 10/11 rồi hội tụ tại 22 qua đường 11→16.
Net 11 rẽ vào 16/19 rồi hội tụ tại 23. Net 16 rẽ tới hai PO 22/23;
trên riêng c17, hai nhánh của 16 không hội tụ lại ở một cổng phía sau.
Vì vậy không mô tả mọi fanout đều là reconvergence.

Ưu điểm: diễn đạt trực tiếp activation/propagation/justification bằng cube,
thấy rõ yêu cầu nội bộ và xung đột. Nhược điểm: nhiều lựa chọn ở net nội bộ,
chi phí justification và quay lui; reconvergence có thể che sai khác hoặc
tạo yêu cầu trái nhau. Trường hợp xấu có tìm kiếm cấp số mũ. Ví dụ không có
backtrack không chứng minh D-algorithm nhanh hơn PODEM.

## 6. Nguồn và độ chắc chắn

- Roth, J. Paul (1966), *Diagnosis of Automata Failures: A Calculus and a
  Method*, IBM Journal of Research and Development 10(4), 278–291.
  DOI: https://doi.org/10.1147/rd.104.0278.
  Bản quét bài gốc: https://bitsavers.org/pdf/ibm/IBM_Journal_of_Research_and_Development/104/ibmrd1004B.pdf.
- Bushnell & Agrawal, *Essentials of Electronic Testing for Digital, Memory
  and Mixed-Signal VLSI Circuits*: bản bìa cứng đầu tiên xuất bản 2000,
  ISBN 978-0-7923-7991-1. Metadata:
  https://link.springer.com/book/10.1007/b117406; trang tác giả:
  https://www.eng.auburn.edu/~agrawvd/BOOK/books.html.
  Chưa có toàn văn để đối chiếu trang; không gán số trang chưa xác minh.
- Specification nhóm: bảy file tại `C:\DFT\DFT_ATPG`; cập nhật lịch/độ dài:
  README và `notes/p1_ke_hoach.md` trong repository.
- Bảng logic và trace c17 là tính toán P2 theo netlist chung, không phải ví dụ
  trích nguyên văn từ sách. Không nhận đã chạy simulator P6 khi code chưa có.

## 7. Kiểm tra và việc còn chờ

Kiểm tra bảng: duyệt 160 ô, đối chiếu một mô hình độc lập duyệt các cách điền
nhị phân của X, kiểm tra dạng bảng và các luật đảo cổng.
Kiểm tra trace: duyệt bốn cách điền cube cuối và tám cách điền cube tổng quát,
so mạch tốt/lỗi; đối chiếu các trạng thái trung gian/frontier bằng mô phỏng.
Build báo cáo và slide bằng `scripts/build_documents.ps1`, kiểm tra citation,
reference, tràn hộp và tiếng Việt. Bằng chứng thực hiện ghi tại `p2_review.md`.

Tái lập kiểm chứng P2 từ gốc repository (chỉ thư viện chuẩn, không ghi file):

```text
python -B notes/p2_kiem_chung.py
python -B scripts/check_p1_examples.py
powershell -ExecutionPolicy Bypass -File scripts/build_documents.ps1
git diff --check
```

Việc còn chờ: P6 xác nhận lại pattern bằng simulator
chung; P3 nhận số liệu theo quy tắc đếm; P1 review nội dung/ngân sách trang.
Không tự sửa code, chương hay cấu hình của các thành viên khác.
