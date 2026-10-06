# Nội dung đề xuất PR P3

**Tiêu đề:** [P3] Đối chiếu trace P5/P6 thật và hoàn tất feedback bàn giao

## Vấn đề và thay đổi

Tài liệu P3 còn ghi chưa nhận code P5/P6 dù main đã tích hợp đầy đủ.
Bản cập nhật đối chiếu hai golden trace đủ bảy cột với API thật và file
exporter P5, xác nhận vector bằng simulator P6, cập nhật Chương 4/ba slide/
notes theo kết quả chạy. Base: `8564678cd360594cbd540389d49c99021525ac08`.

Giữ golden: API ghi thao tác vừa thực hiện, golden ghi hành động kế tiếp;
hai nhãn trên mạch phụ khác nhau nhưng exporter đã chuẩn hóa. Script P3 mới
kiểm từng ô, mọi PI/net/frontier và đúng hai khác biệt này, không sửa lõi P5.
Chốt P2 4 cube/3 PI/0 backtrack và PODEM 2 PI/0 backtrack; không suy ra tốc độ.

## Kiểm chứng

- Python 3.12.10 / pytest 9.1.1: 342 passed.
- `python -B notes/p3_doi_chieu_code.py`: 35 ô golden/API/exporter đạt;
  cube c17 8/8, PO 01000 tốt (1,1)/lỗi (0,0), phụ 01 tốt 1/lỗi 0;
  giới hạn 0/1 trả ABORTED/DETECTED.
- Script tham chiếu P3, kiểm bàn giao và kiểm chứng P2 đều PASS.
- Bốn CLI nghiệm thu đều exit 0, thuật toán PODEM.
- Report XeLaTeX/Biber 14 trang (10 trang đánh số nội dung/tham khảo),
  slide 19 trang; không overfull hoặc thiếu tham chiếu trong log cuối.
- `git diff --check` đạt. Chi tiết ở `notes/p3_review.md` và
  `results/p3_doi_chieu_code.md`.

## Giới hạn và tích hợp

Không dùng hai trace để chứng minh mọi mạch, branch fault hoặc multiple faults.
Không thay API, exporter, golden, PDF bản nộp hoặc file của phần khác.
P1 review/tích hợp và build lại PDF/phát hành nếu cần; checklist tập trình
bày, demo 20 phút, video và nộp ngày 08/10/2026 nằm riêng trong bàn giao.
Không nhận đã có xác nhận cá nhân của P2/P5/P6; nguồn là code/tài liệu trong repo.
