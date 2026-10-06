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
```

## Cập nhật trạng thái P5 — 06/10/2026

### Cơ sở và phạm vi

- Branch làm việc: `p5-podem-code`, commit nền `797949070355ae160d9204c0382b6c3e9f2fdfef`.
- Đã fetch để đối chiếu; `origin/main` tại `586218e1eb244fa5374b7bc856e0ffd979447f4a`. Không merge main vào branch P5.
- `origin/main` bổ sung `Circuit`, `Fault`, fault simulator, CLI, netlist c17/mạch phụ và test tích hợp mà checkout P5 hiện chưa có. Exporter dùng đúng giao diện đó; các lần kiểm thử CLI bên dưới chạy trên snapshot kết hợp tạm thời, không chép các module P6/P4 vào branch P5.
- `src/atpg/podem.py` và `logic.py` ở hai snapshot trùng nhau. API `podem(c, fault, max_backtracks=1000, trace=False)` và các trường `PodemResult` được giữ nguyên.

### Trace và P3

- `scripts/export_podem_trace.py` đọc bench bằng `Circuit.from_bench`, kiểm tra `Fault`, gọi `podem(trace=True)` và ghi Markdown UTF-8 với đúng bảy cột.
- C17, 11/SA0: `DETECTED`, pattern `X10XX`, 0 backtrack; PI theo thứ tự `(1,2,3,6,7)`; net và D-frontier được ghi theo thứ tự ổn định.
- `backtrack_example`, t/SA0: `DETECTED`, pattern `01`, 1 backtrack. Hàng a=1 mang hành động `backtrack`; hàng đảo a=0 ghi Objective/Backtrace `—`, trạng thái `t=X,n=1,out=X`, hành động `tiếp tục`.
- Với `--max-backtracks 0`, trace ghi `ABORTED`, pattern `1X`, 0 backtrack và giải thích giới hạn; không đổi thành `UNTESTABLE`.
- Hai lần xuất c17 trong cùng môi trường cho nội dung/hash SHA-256 giống nhau. Golden của P3 trong `results/golden_trace_*.md` không bị ghi đè.
- Hợp đồng đối chiếu: `notes/p3_quy_tac_P5.md`; kết quả review P6 ghi c17, mạch phụ và ABORTED khớp. P3 định nghĩa thứ tự PI/topology, X-path, frontier và hành động; exporter chuẩn hóa nhãn hành động theo hợp đồng mà không đổi lõi PODEM.

### Review tích hợp và bằng chứng

- P2: `origin/main:notes/p2_review.md` ghi bảng logic **160/160 ô PASS** và xác nhận các mẫu/trace được đối chiếu trực tiếp. Đây là bằng chứng từ review đã lưu trong repo; không tự nhận đã liên hệ P2 trong lượt này.
- P4: đã kiểm tra phạm vi `unroll`, `fault_in_frames` và `full_scan` trong `src/atpg/unroll.py` cùng `tests/test_unroll.py`. Kiểm thử tuần tự thực gọi PODEM có trong `origin/main:tests/test_integration.py::test_sequential_with_real_podem_and_unroll`; fixture `reference_only` ở `test_sequential.py` đúng là tắt PODEM, nên không dùng riêng fixture đó làm bằng chứng tích hợp.
- P6: đã rà `fault_sim.py`, `run.py`, `faults.py` và `tests/test_input_validation.py`. Snapshot mới có test từ chối SV=2, net sai và branch không tồn tại/không nối với net; đây là validation thuộc P6. Exporter cũng tự kiểm SV và fault trước khi ghi file.
- Trên checkout P5: `tests/test_logic.py tests/test_podem.py` đạt **255 passed**; toàn bộ test có trong branch đạt **265 passed**, thêm **5 skipped** vì checkout chưa có Circuit/netlist thật, Python 3.14.8/pytest 9.1.1.
- Trên snapshot kiểm thử kết hợp tạm thời từ `origin/main` với script/test P5 hiện tại: exporter c17, backtrack, ABORTED và lỗi ghi file được kiểm tra; toàn bộ test tích hợp đạt **340 passed** trên Python 3.14.8/pytest 9.1.1. Module và netlist của phần khác chỉ được dùng làm dependency kiểm thử, không được thêm vào branch.
- Mốc **302 passed** là snapshot review trước; **220 logic / 32 PODEM** là số lịch sử của P5. Không dùng chúng làm số đo hiện tại.

### Việc còn phụ thuộc

- P5 branch hiện chưa chứa `Circuit`/`Fault`/`run` và hai bench thật. Vì vậy lệnh CLI exporter cần checkout tích hợp có các module P4–P6; trong khi branch đứng riêng, các unit test định dạng vẫn chạy và test CLI thật được skip rõ lý do.
- Chưa có xác nhận cá nhân trực tiếp của P1 về biên tập cuối, P2 ngoài review đã lưu, hoặc người phụ trách P3/P4/P6 trong lượt này. Không ghi nhận đã gửi tin hay đã trình bày/demo/nộp bài.

### Nội dung PR đề xuất

- **Vấn đề:** chưa có lệnh tái sinh trace PODEM; trace backtrack cũ chưa phản ánh quy ước hành động P3; Chương 6/slide thiếu kiến trúc, ví dụ chạy thật và giới hạn.
- **Thay đổi:** thêm exporter và kiểm thử; tái sinh hai trace P5; cập nhật Chương 6, ba frame P5 và hướng dẫn/bằng chứng hiện tại.
- **Kiểm chứng:** ghi rõ lệnh và kết quả tại `notes/p5_huong_dan_chay.md`; tách test P5 trên checkout khỏi test tích hợp snapshot.
- **Giới hạn:** exporter cần các module Circuit/Fault/CLI của snapshot tích hợp; P1 quyết định rút gọn/dàn trang cuối; phần demo/trình bày/nộp do người trong nhóm thực hiện.

### Checklist P5

- [x] P5-01 exporter, trace c17/backtrack, tính lặp lại, 7 cột và trạng thái ABORTED: đạt trên snapshot tích hợp; test CLI trên branch riêng được skip do thiếu module P6.
- [x] P5-02 Chương 6 và ba frame P5: đã thêm kiến trúc, mã giả, quy tắc XOR/XNOR, bảng trace, giới hạn, citation và số test đúng phạm vi.
- [ ] P5-02 biên dịch XeLaTeX/Biber: chưa chạy vì `xelatex`/`biber` không có trong PATH hiện tại.
- [x] P5-03 ghi chú chạy, môi trường, evidence; P4/P6 review và tuần tự PODEM thật: đã kiểm tra qua review artifacts/tests trên snapshot tích hợp.
- [x] P5-03 160 ô logic P2: review P2 đã lưu ghi 160/160 PASS; không có xác nhận cá nhân mới ngoài artifact đó.
- [ ] Người thực hiện: P1 biên tập/dàn trang cuối; thành viên phụ trách demo, luyện thuyết trình và nộp bài.
