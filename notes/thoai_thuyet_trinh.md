# Lời thoại thuyết trình — Nhóm 4 (20 phút)

Bám theo slide bản `v1.0.10` (20 trang). Chữ trong [ngoặc vuông] là thao tác, không đọc. Mỗi người nên tập để nói tự nhiên, không đọc nguyên văn.

| Người | Slide | Thời gian |
|---|---|---|
| Phan Ngọc Tuấn Nguyên | 1–4 và 20 | ~3 phút |
| Hà Quang Huy | 5–7 | ~3 phút |
| Võ Trung Nguyên | 8–10 | ~3 phút |
| Phạm Trọng An Nam | 11–13 | ~3 phút |
| Nguyễn Thị Thúy Hằng | 14–16 | ~3 phút |
| Nguyễn Thị Thanh Tuyền | 17–19 (gồm demo) | ~3–4 phút |
| Dự phòng chuyển người/demo | | ~1–2 phút |

---

## 1. Phan Ngọc Tuấn Nguyên — Mở đầu và nguyên lý (slide 1–4)

**Slide 1 — Bìa.** Em chào thầy và các bạn. Nhóm 4 xin trình bày đề tài *Sinh mẫu kiểm tra tự động cho mạch tổ hợp và tuần tự*, tức ATPG. Nhóm gồm sáu thành viên trên slide; em là Tuấn Nguyên, phụ trách phần mở đầu.

**Slide 2 — Vì sao cần testing và ATPG?** Verification kiểm tra thiết kế có đúng đặc tả không, còn testing kiểm tra con chip sau khi sản xuất có bị hỏng không. Thiết kế đúng vẫn có thể ra chip lỗi. Nhóm dùng mô hình lỗi *stuck-at*: một dây bị kẹt ở 0 hoặc ở 1. ATPG là đi tìm đầu vào sao cho mạch tốt và mạch lỗi cho ra kết quả khác nhau. Muốn vậy phải làm đủ hai việc [chỉ khung xanh]: **kích hoạt** lỗi tại chỗ hỏng và **lan truyền** sự khác biệt ra ngõ ra.

**Slide 3 — c17, lỗi 11/SA0.** Cả nhóm dùng chung một ví dụ: mạch chuẩn c17, lỗi net 11 kẹt ở 0. Đặt 3 bằng 0 thì net 11 mạch tốt bằng 1, mạch lỗi bằng 0, ta gọi là D. Đặt 2 bằng 1 để D đi qua cổng 16, rồi tới ngõ ra 22. Vậy mẫu là X10XX, điền X bằng 0 được 01000.

**Slide 4 — Lộ trình.** Tiếp theo, các bạn sẽ trình bày D-algorithm, PODEM, ATPG cho mạch tuần tự, rồi phần cài đặt và kiểm chứng. Một nguyên tắc chung: nếu tìm kiếm hết giới hạn thì kết quả là ABORTED, không được kết luận là không thể kiểm tra. Bài tập Hình 4.5 trong giáo trình em đã giải trong video nộp kèm. Em xin mời bạn Huy.

**Slide 20 — Kết thúc (sau phần demo).** Tóm lại, nhóm đã cài đặt PODEM, kiểm chứng bằng mô phỏng lỗi độc lập: c17 đạt 100% coverage, nén còn 6 mẫu; mạch tuần tự đạt 18 trên 18 lỗi khi dùng full scan hoặc trải 3 khung. Em xin cảm ơn thầy và các bạn đã lắng nghe.

---

## 2. Hà Quang Huy — D-algorithm (slide 5–7)

**Slide 5 — D-calculus.** Để theo dõi lỗi, mình ghép mạch tốt và mạch lỗi thành một giá trị. D nghĩa là tốt bằng 1, lỗi bằng 0; D ngang là ngược lại. Tính cổng thì tính riêng từng phần rồi ghép lại, ví dụ D AND 1 vẫn là D, còn D AND D ngang thì bằng 0. Qua cổng NAND với đầu vào kia bằng 1, D đổi thành D ngang.

**Slide 6 — Thuật toán.** D-algorithm làm ba việc. Một là chọn **PDCF** để kích hoạt lỗi, ví dụ lỗi z/SA0 ở cổng NAND cần một đầu vào bằng 0. Hai là dùng **PDC** để đẩy D đi tiếp: đầu vào phụ phải bằng 1. Ba là **justify**, tức tìm giá trị đầu vào cho các yêu cầu bên trong mạch. D-frontier là các cổng có D ở đầu vào nhưng đầu ra chưa biết; J-frontier là các cổng đã gán đầu ra nhưng chưa justify. Nếu hai yêu cầu mâu thuẫn thì quay lui và thử cách khác.

**Slide 7 — Ví dụ c17.** [Chỉ hình] Bước 1 chọn PDCF: 6 bằng 0 nên 11 bằng D. Bước 2: 2 bằng 1, D qua 16 thành D ngang. Bước 3: 10 bằng 1, sai khác tới 22 thành D. Bước 4 justify net 10 bằng cách đặt 3 bằng 0. Tổng cộng 4 lần chọn cube, không cần quay lui. Điền X bằng 0 thì mạch tốt ra (1,1), mạch lỗi ra (0,0). Em xin mời bạn Trung Nguyên trình bày PODEM.

---

## 3. Võ Trung Nguyên — PODEM (slide 8–10)

**Slide 8 — Ý tưởng.** Khác D-algorithm, PODEM chỉ ra quyết định ở **ngõ vào chính**. Mỗi vòng có bốn bước: objective chọn net và giá trị cần đạt; backtrace lần ngược về một ngõ vào chưa gán; imply mô phỏng lại toàn mạch; nếu thất bại thì đảo giá trị ngõ vào đó, hết cả hai cách thì quay lên mức trên. Các net bên trong tự suy ra bằng mô phỏng nên không cần justify.

**Slide 9 — c17.** Với cùng lỗi 11/SA0, PODEM chỉ cần hai quyết định. Bước 1, mục tiêu là net 11 bằng 1, backtrace về đặt 3 bằng 0, lỗi được kích hoạt. Bước 2, muốn D qua cổng 16 thì cần 2 bằng 1. Lúc này ngõ ra 22 có D, dừng. Mẫu X10XX, không quay lui, và mô phỏng xác nhận cả 8 cách điền X đều phát hiện lỗi.

**Slide 10 — Ví dụ quay lui.** Mạch phụ này có một lần quay lui. Thử a bằng 1: t thành D, nhưng n bằng 0 nên ngõ ra bị chặn, nhánh thất bại. Đảo lại a bằng 0: n bằng 1. Gán thêm b bằng 1: t bằng D, ngõ ra bằng D. Kết quả 01, một lần backtrack. Nếu giới hạn quay lui là 0 thì chương trình trả ABORTED. Lưu ý: D-algorithm đếm lần chọn cube, PODEM đếm lần gán ngõ vào, nên không so sánh nhanh chậm trực tiếp được. Em xin mời bạn An Nam.

---

## 4. Phạm Trọng An Nam — ATPG tuần tự (slide 11–13)

**Slide 11 — Vì sao khó?** Mạch tuần tự có flip-flop lưu trạng thái, và lúc bật nguồn mình không biết trạng thái đó là gì. Không có scan thì không đặt được Q, không đọc được D, nên phải dùng một chuỗi đầu vào qua nhiều chu kỳ để khởi tạo, kích hoạt rồi đưa lỗi ra. Mạch ví dụ của nhóm có 2 ngõ vào, 1 ngõ ra, 6 cổng và 1 flip-flop.

**Slide 12 — Trải khung thời gian.** Cách làm là "trải" mạch: chép phần tổ hợp thành nhiều khung, ngõ ra D của khung trước nối vào Q của khung sau, và lỗi có mặt ở mọi khung. Với lỗi N3/SA0, đặt A bằng 1, B bằng 0 ở cả hai khung. Khung 0: N3 tốt 1, lỗi 0, nên D thành 0/1. Khung 1: Q nhận 0/1 và đưa thẳng ra Y. Lỗi được phát hiện ở khung 1, bất kể trạng thái đầu là 0 hay 1.

**Slide 13 — Full scan và kết quả.** Full scan thay flip-flop bằng scan flip-flop: dịch giá trị vào Q, chạy một xung, rồi dịch D ra. Khi đó Q như một ngõ vào, D như một ngõ ra, quay về bài toán tổ hợp. [Chỉ bảng] Kết quả trên 18 lỗi: full scan phát hiện 18/18. Không scan, trạng thái đầu chưa biết: 1 khung được 1/18, 2 khung 13/18, 3 khung đủ 18/18. Scan dễ test hơn nhưng tốn thêm phần cứng và thời gian dịch. Em xin mời bạn Hằng.

---

## 5. Nguyễn Thị Thúy Hằng — Cài đặt PODEM (slide 14–16)

**Slide 14 — Kiến trúc.** [Chỉ sơ đồ] Chương trình viết bằng Python. Mạch được đọc từ file .bench, đưa vào lõi PODEM gồm objective, backtrace và imply. Kết quả được một bộ mô phỏng lỗi riêng kiểm tra lại. Với mạch tuần tự, khối unroll trải khung trước rồi mới đưa vào PODEM. Imply mô phỏng năm giá trị 0, 1, X, D, D ngang theo thứ tự từ đầu vào tới đầu ra; khi quay lui thì dựng lại mẫu và mô phỏng lại toàn mạch.

**Slide 15 — Trace c17.** Đây là trace thật chương trình in ra cho lỗi 11/SA0. Bước 1 gán 3 bằng 0, net 11 thành D. Bước 2 gán 2 bằng 1, ngõ ra 22 có D, thành công. Kết quả khớp đúng với phần chạy tay của bạn Trung Nguyên. Với mạch phụ, chương trình cũng quay lui đúng một lần như lý thuyết.

**Slide 16 — Kiểm thử và giới hạn.** Chương trình phân biệt rõ ba kết quả: DETECTED khi ngõ ra có D, UNTESTABLE khi đã thử hết, ABORTED khi chạm giới hạn quay lui. Cổng XOR được xử lý riêng vì không có giá trị điều khiển. Bộ kiểm thử có 350 test đều đạt, và đầu vào sai bị từ chối thay vì cho ra kết quả sai. Giới hạn: nhóm chưa dùng các heuristic như SCOAP hay FAN. Em xin mời bạn Tuyền.

---

## 6. Nguyễn Thị Thanh Tuyền — Kiểm chứng, kết quả, demo (slide 17–19)

**Slide 17 — Kiểm chứng độc lập.** Để không tin mù quáng vào PODEM, mọi mẫu đều được mô phỏng lại riêng ở mạch tốt và mạch lỗi. Mẫu có X chỉ được tính là đúng khi thử hết mọi cách điền X. Mạch c17 có 34 lỗi; gộp các lỗi tương đương còn 22. Với mạch tuần tự, chỉ chuỗi phát hiện được với *mọi* trạng thái đầu mới được tính.

**Slide 18 — Kết quả.** [Chỉ bảng trên] Trên c17, PODEM phát hiện 22/22 lỗi đại diện và 34/34 lỗi gốc, không cần quay lui, không mẫu nào sai. Sau khi nén, chỉ còn 6 mẫu mà vẫn phủ đủ 34 lỗi. [Chỉ bảng dưới] Mạch tuần tự: 1, 13 rồi 18 trên 18 khi trải 1, 2, 3 khung, khớp với kết quả vét cạn độc lập.

**Slide 19 — Demo.** Em xin demo nhanh. [Chạy lệnh theo `demo.md`]
1. Trace lỗi 11/SA0 trên c17: chương trình in bảng từng bước, ra mẫu X10XX.
2. Mạch phụ: thấy một lần backtrack.
3. Chạy toàn bộ lỗi c17: coverage 100%, nén còn 6 mẫu.
4. Mạch tuần tự trải 2 khung: 13/18 lỗi phát hiện chắc chắn.

Em xin chuyển lại cho bạn Tuấn Nguyên để kết thúc.

---

### Mẹo chung

- Mỗi người chỉ cần nắm chắc **ý chính** của mình; số liệu đã có trên slide, cứ chỉ vào mà đọc.
- Câu chuyển người ở cuối mỗi phần giúp buổi trình bày liền mạch.
- Demo: mở sẵn terminal đúng thư mục, đã kích hoạt `.venv`, chữ to. Nếu máy lỗi, mở file trong `results/` thay thế.
