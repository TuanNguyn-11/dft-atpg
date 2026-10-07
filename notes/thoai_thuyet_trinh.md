# Lời thoại thuyết trình — Nhóm 4 (20 phút)

Bám theo slide bản `v1.0.12` (22 trang). Chữ trong [ngoặc vuông] là thao tác, không đọc. Mỗi người nên tập để nói tự nhiên, không đọc nguyên văn.

| Người | Slide | Thời gian |
|---|---|---|
| Phan Ngọc Tuấn Nguyên | 1–5 | ~3 phút |
| Hà Quang Huy | 6–9 | ~3,5 phút |
| Võ Trung Nguyên | 10–12 | ~3 phút |
| Phạm Trọng An Nam | 13–15 | ~3 phút |
| Nguyễn Thị Thúy Hằng | 16–18 | ~3 phút |
| Nguyễn Thị Thanh Tuyền | 19–22 (gồm demo và kết thúc) | ~4 phút |
| Dự phòng chuyển người/demo | | ~1–2 phút |

---

## 1. Phan Ngọc Tuấn Nguyên — Mở đầu và nguyên lý (slide 1–5, ~3 phút)

**Slide 1 — Bìa (≈ 20 giây).** Em chào thầy và các bạn. Nhóm 4 xin trình bày đề tài *Sinh mẫu kiểm tra tự động cho mạch tổ hợp và mạch tuần tự*, gọi tắt là ATPG. Nhóm gồm sáu thành viên như trên slide. Em là Phan Ngọc Tuấn Nguyên, xin mở đầu bằng phần nguyên lý chung, sau đó các bạn sẽ đi vào từng thuật toán và phần cài đặt.

**Slide 2 — Vì sao cần testing và ATPG? (≈ 50 giây).** Trước hết cần phân biệt hai việc. Verification là kiểm tra bản thiết kế có làm đúng yêu cầu không. Còn testing là kiểm tra con chip sau khi sản xuất có bị hỏng không. Thiết kế đúng vẫn có thể ra chip lỗi, nên chip nào cũng cần được test. Nhưng không thể thử hết mọi tổ hợp đầu vào, nên người ta dùng mô hình lỗi, phổ biến nhất là **stuck-at**: một dây bị kẹt ở 0 (SA0) hoặc kẹt ở 1 (SA1). ATPG là tìm đầu vào sao cho mạch tốt và mạch lỗi cho ra kết quả khác nhau. [Chỉ khung xanh] Muốn vậy luôn phải đủ hai điều kiện: **kích hoạt** lỗi, tức đặt dây lỗi về giá trị ngược với giá trị bị kẹt; và **lan truyền** sự khác biệt ra ngõ ra, vì máy test chỉ đo được ở ngõ ra.

**Slide 3 — Mạch c17 (≈ 25 giây).** [Chỉ toàn mạch] Để cả nhóm dễ so sánh, chúng em dùng chung một ví dụ: mạch chuẩn c17. Mạch có 6 cổng NAND, 5 ngõ vào là 1, 2, 3, 6, 7 và 2 ngõ ra là 22, 23. [Chỉ dấu X đỏ] Lỗi cần tìm là net 11, ngõ ra của cổng N11, bị kẹt ở 0. Câu hỏi là: đặt các ngõ vào thế nào để thấy được lỗi này ở ngõ ra?

**Slide 4 — Kích hoạt và lan truyền (≈ 55 giây).** [Chỉ ngõ vào 3 và net 11] Bước một, kích hoạt. Net 11 là NAND của 3 và 6. Đặt 3 bằng 0 thì mạch tốt có net 11 bằng 1, còn mạch lỗi vẫn bằng 0. Cặp "tốt 1, lỗi 0" này ta gọi là **D**. [Chỉ ngõ vào 2 và net 16] Bước hai, lan truyền. Net 16 là NAND của 2 và 11. Đặt 2 bằng 1 thì D đi qua được, nhưng bị đảo thành **D ngang**. Đồng thời, vì 3 bằng 0 nên net 10 bằng 1. [Chỉ ngõ ra 22] Bước ba, ngõ ra 22 là NAND của 10 và 16: net 10 bằng 1 nên sai khác lại đi qua, 22 bằng D. Lỗi đã quan sát được, đúng theo đường màu đỏ. [Chỉ khung dưới] Theo thứ tự ngõ vào 1, 2, 3, 6, 7, mẫu là X, 1, 0, X, X; X là giá trị nào cũng được, điền 0 ta có vector 01000.

**Slide 5 — Lộ trình (≈ 30 giây).** Ví dụ vừa rồi em giải bằng suy luận tay; các phần sau trình bày cách máy tính tự làm việc đó. Bạn Huy và bạn Trung Nguyên trình bày **D-algorithm** và **PODEM** trên cùng lỗi này, bạn An Nam trình bày **mạch tuần tự**, bạn Hằng và bạn Tuyền trình bày **cài đặt và kết quả**. Nguyên tắc chung: nếu tìm hết giới hạn mà chưa ra kết quả thì báo ABORTED, không kết luận lỗi không thể kiểm tra. Bài tập ví dụ Hình 4.5 trong giáo trình em đã giải trong video nộp kèm. Sau đây em xin mời bạn Huy.

---

## 2. Hà Quang Huy — D-algorithm (slide 6–9)

**Slide 6 — D-calculus.** Để theo dõi lỗi, mình ghép mạch tốt và mạch lỗi thành một giá trị. D nghĩa là tốt bằng 1, lỗi bằng 0; D ngang là ngược lại. Tính cổng thì tính riêng từng phần rồi ghép lại, ví dụ D AND 1 vẫn là D, còn D AND D ngang thì bằng 0. Qua cổng NAND với đầu vào kia bằng 1, D đổi thành D ngang.

**Slide 7 — Bảng logic năm giá trị.** [Chỉ bảng NAND] Đây là bảng đầy đủ cho tám loại cổng. Hàng là ngõ vào a, cột là ngõ vào b. Ví dụ ở bảng NAND, dòng 1: nếu một ngõ vào bằng 1 thì D đi qua thành D ngang, còn nếu có một ngõ vào bằng 0 thì ngõ ra luôn bằng 1, sai khác bị chặn. [Chỉ bảng XOR] Riêng XOR, D gặp D lại cho 0, tức hai sai khác có thể triệt tiêu nhau. Nhóm dùng bảng này làm đáp án chuẩn để kiểm tra chương trình, và chương trình tính khớp cả 160 ô.

**Slide 8 — Thuật toán.** D-algorithm làm ba việc. Một là chọn **PDCF** để kích hoạt lỗi, ví dụ lỗi z/SA0 ở cổng NAND cần một đầu vào bằng 0. Hai là dùng **PDC** để đẩy D đi tiếp: đầu vào phụ phải bằng 1. Ba là **justify**, tức tìm giá trị đầu vào cho các yêu cầu bên trong mạch. D-frontier là các cổng có D ở đầu vào nhưng đầu ra chưa biết; J-frontier là các cổng đã gán đầu ra nhưng chưa justify. Nếu hai yêu cầu mâu thuẫn thì quay lui và thử cách khác.

**Slide 9 — Ví dụ c17.** [Chỉ hình] Bước 1 chọn PDCF: 6 bằng 0 nên 11 bằng D. Bước 2: 2 bằng 1, D qua 16 thành D ngang. Bước 3: 10 bằng 1, sai khác tới 22 thành D. Bước 4 justify net 10 bằng cách đặt 3 bằng 0. Tổng cộng 4 lần chọn cube, không cần quay lui. Điền X bằng 0 thì mạch tốt ra (1,1), mạch lỗi ra (0,0). Em xin mời bạn Trung Nguyên trình bày PODEM.

---

## 3. Võ Trung Nguyên — PODEM (slide 10–12)

**Slide 10 — Ý tưởng.** Khác D-algorithm, PODEM chỉ ra quyết định ở **ngõ vào chính**. Mỗi vòng có bốn bước: objective chọn net và giá trị cần đạt; backtrace lần ngược về một ngõ vào chưa gán; imply mô phỏng lại toàn mạch; nếu thất bại thì đảo giá trị ngõ vào đó, hết cả hai cách thì quay lên mức trên. Các net bên trong tự suy ra bằng mô phỏng nên không cần justify.

**Slide 11 — c17.** Với cùng lỗi 11/SA0, PODEM chỉ cần hai quyết định. Bước 1, mục tiêu là net 11 bằng 1, backtrace về đặt 3 bằng 0, lỗi được kích hoạt. Bước 2, muốn D qua cổng 16 thì cần 2 bằng 1. Lúc này ngõ ra 22 có D, dừng. Mẫu X10XX, không quay lui, và mô phỏng xác nhận cả 8 cách điền X đều phát hiện lỗi.

**Slide 12 — Ví dụ quay lui.** Mạch phụ này có một lần quay lui. Thử a bằng 1: t thành D, nhưng n bằng 0 nên ngõ ra bị chặn, nhánh thất bại. Đảo lại a bằng 0: n bằng 1. Gán thêm b bằng 1: t bằng D, ngõ ra bằng D. Kết quả 01, một lần backtrack. Nếu giới hạn quay lui là 0 thì chương trình trả ABORTED. Lưu ý: D-algorithm đếm lần chọn cube, PODEM đếm lần gán ngõ vào, nên không so sánh nhanh chậm trực tiếp được. Em xin mời bạn An Nam.

---

## 4. Phạm Trọng An Nam — ATPG tuần tự (slide 13–15)

**Slide 13 — Vì sao khó?** Mạch tuần tự có flip-flop lưu trạng thái, và lúc bật nguồn mình không biết trạng thái đó là gì. Không có scan thì không đặt được Q, không đọc được D, nên phải dùng một chuỗi đầu vào qua nhiều chu kỳ để khởi tạo, kích hoạt rồi đưa lỗi ra. Mạch ví dụ của nhóm có 2 ngõ vào, 1 ngõ ra, 6 cổng và 1 flip-flop.

**Slide 14 — Trải khung thời gian.** Cách làm là "trải" mạch: chép phần tổ hợp thành nhiều khung, ngõ ra D của khung trước nối vào Q của khung sau, và lỗi có mặt ở mọi khung. Với lỗi N3/SA0, đặt A bằng 1, B bằng 0 ở cả hai khung. Khung 0: N3 tốt 1, lỗi 0, nên D thành 0/1. Khung 1: Q nhận 0/1 và đưa thẳng ra Y. Lỗi được phát hiện ở khung 1, bất kể trạng thái đầu là 0 hay 1.

**Slide 15 — Full scan và kết quả.** Full scan thay flip-flop bằng scan flip-flop: dịch giá trị vào Q, chạy một xung, rồi dịch D ra. Khi đó Q như một ngõ vào, D như một ngõ ra, quay về bài toán tổ hợp. [Chỉ bảng] Kết quả trên 18 lỗi: full scan phát hiện 18/18. Không scan, trạng thái đầu chưa biết: 1 khung được 1/18, 2 khung 13/18, 3 khung đủ 18/18. Scan dễ test hơn nhưng tốn thêm phần cứng và thời gian dịch. Em xin mời bạn Hằng.

---

## 5. Nguyễn Thị Thúy Hằng — Cài đặt PODEM (slide 16–18)

**Slide 16 — Kiến trúc.** [Chỉ sơ đồ] Chương trình viết bằng Python. Mạch được đọc từ file .bench, đưa vào lõi PODEM gồm objective, backtrace và imply. Kết quả được một bộ mô phỏng lỗi riêng kiểm tra lại. Với mạch tuần tự, khối unroll trải khung trước rồi mới đưa vào PODEM. Imply mô phỏng năm giá trị 0, 1, X, D, D ngang theo thứ tự từ đầu vào tới đầu ra; khi quay lui thì dựng lại mẫu và mô phỏng lại toàn mạch.

**Slide 17 — Trace c17.** Đây là trace thật chương trình in ra cho lỗi 11/SA0. Bước 1 gán 3 bằng 0, net 11 thành D. Bước 2 gán 2 bằng 1, ngõ ra 22 có D, thành công. Kết quả khớp đúng với phần chạy tay của bạn Trung Nguyên. Với mạch phụ, chương trình cũng quay lui đúng một lần như lý thuyết.

**Slide 18 — Kiểm thử và giới hạn.** Chương trình phân biệt rõ ba kết quả: DETECTED khi ngõ ra có D, UNTESTABLE khi đã thử hết, ABORTED khi chạm giới hạn quay lui. Cổng XOR được xử lý riêng vì không có giá trị điều khiển. Bộ kiểm thử có 350 test đều đạt, và đầu vào sai bị từ chối thay vì cho ra kết quả sai. Giới hạn: nhóm chưa dùng các heuristic như SCOAP hay FAN. Em xin mời bạn Tuyền.

---

## 6. Nguyễn Thị Thanh Tuyền — Kiểm chứng, kết quả, demo và kết thúc (slide 19–22)

**Slide 19 — Kiểm chứng độc lập.** Để không tin mù quáng vào PODEM, mọi mẫu đều được mô phỏng lại riêng ở mạch tốt và mạch lỗi. Mẫu có X chỉ được tính là đúng khi thử hết mọi cách điền X. Mạch c17 có 34 lỗi; gộp các lỗi tương đương còn 22. Với mạch tuần tự, chỉ chuỗi phát hiện được với *mọi* trạng thái đầu mới được tính.

**Slide 20 — Kết quả.** [Chỉ bảng trên] Trên c17, PODEM phát hiện 22/22 lỗi đại diện và 34/34 lỗi gốc, không cần quay lui, không mẫu nào sai. Sau khi nén, chỉ còn 6 mẫu mà vẫn phủ đủ 34 lỗi. [Chỉ bảng dưới] Mạch tuần tự: 1, 13 rồi 18 trên 18 khi trải 1, 2, 3 khung, khớp với kết quả vét cạn độc lập.

**Slide 21 — Demo.** Em xin demo nhanh. [Chạy lệnh theo `demo.md`]
1. Trace lỗi 11/SA0 trên c17: chương trình in bảng từng bước, ra mẫu X10XX.
2. Mạch phụ: thấy một lần backtrack.
3. Chạy toàn bộ lỗi c17: coverage 100%, nén còn 6 mẫu.
4. Mạch tuần tự trải 2 khung: 13/18 lỗi phát hiện chắc chắn.

**Slide 22 — Kết thúc.** Tóm lại, nhóm đã cài đặt PODEM và kiểm chứng bằng mô phỏng lỗi độc lập: c17 đạt 100% coverage, nén còn 6 mẫu; mạch tuần tự đạt 18 trên 18 lỗi khi dùng full scan hoặc trải 3 khung. Phần trình bày của Nhóm 4 đến đây là kết thúc. Em xin thay mặt nhóm cảm ơn thầy và các bạn đã lắng nghe.

---

### Mẹo chung

- Mỗi người chỉ cần nắm chắc **ý chính** của mình; số liệu đã có trên slide, cứ chỉ vào mà đọc.
- Câu chuyển người ở cuối mỗi phần giúp buổi trình bày liền mạch.
- Demo: mở sẵn terminal đúng thư mục, đã kích hoạt `.venv`, chữ to. Nếu máy lỗi, mở file trong `results/` thay thế.
