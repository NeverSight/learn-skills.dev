---
name: product-discovery
description: "Cổng G1: phân tích yêu cầu từ mô tả và phỏng vấn case study theo quy mô, chuyển As-Is sang To-Be, xác định actors, quy tắc nghiệp vụ và danh mục Epic trước khi viết User Stories."
hide: true
disable-model-invocation: true
---

# Product discovery (G1 Nghiệp vụ & Epic)

Đọc `skill://product-workflow/references/contract.md` và `skill://product-workflow/references/records.md` trước. Nếu harness không hỗ trợ `skill://` (như Claude Code), đọc `<skills-dir>/product-workflow/references/`; `<skills-dir>` là thư mục cha của skill này (`.claude/skills/`, `.agents/skills/` hoặc bản toàn cục). Tên công cụ quy đổi theo `<skills-dir>/product-workflow/references/harness.md`.

Mục tiêu: một business brief đủ rõ để viết User Stories. Không viết story, không ước lượng, không chia sprint ở bước này.

## 1. Thu thập nguồn

Đọc toàn bộ tài liệu đầu vào trước khi đặt câu hỏi. Phân loại nguồn theo 7 hình thức thu thập yêu cầu:

1. Phỏng vấn khách hàng.
2. Họp với khách hàng.
3. Quan sát quy trình nghiệp vụ.
4. Phiếu khảo sát.
5. Email / tài liệu yêu cầu (mô tả, đề bài, hợp đồng).
6. Feedback từ hệ thống đang sử dụng.
7. Yêu cầu thay đổi / bổ sung chức năng.

Trong đợt hỏi đầu tiên, đề nghị cung cấp tài liệu thực tế nếu có: file Excel/sổ theo dõi, mẫu phiếu, hóa đơn, báo cáo hiện có, quy định nội bộ. Một tài liệu thực tế thường trả lời được nhiều câu hỏi. Không có tài liệu thì tiếp tục, không chặn discovery.

## 2. Xác định quy mô

Nếu quy mô chưa được xác định, câu hỏi `ask` đầu tiên là:

```text
ask(questions=[{
  "id": "project_scale",
  "question": "Dự án thuộc quy mô nào? Quy mô quyết định độ sâu phỏng vấn.",
  "options": [
    {"label": "MVP / Đồ án môn học", "description": "Một luồng giá trị chính, phỏng vấn ngắn, thường khoảng 5–15 câu tình huống."},
    {"label": "Hệ thống vừa (cửa hàng, SME)", "description": "Đủ các phân hệ vận hành; phỏng vấn sâu về tiền, trạng thái, phân quyền, báo cáo."},
    {"label": "Nền tảng lớn / nhiều phân hệ", "description": "Chốt danh mục phân hệ trước, sau đó phỏng vấn từng phân hệ."}
  ],
  "recommended": 0
}])
```

Quy mô quyết định độ sâu:
- **MVP:** chỉ làm rõ các điểm xung đột trên luồng chính (ai thực hiện, xử lý khi sai, ai được sửa/xóa). Không mở rộng sang bài toán cấp doanh nghiệp.
- **Vừa:** bổ sung các chủ đề gợi ý ở mục 4.
- **Lớn:** đề xuất danh mục phân hệ (`Quản lý + …`), dùng `ask` để duyệt danh mục và xác định phân hệ ưu tiên, rồi phỏng vấn lần lượt từng phân hệ.

## 3. Phân tích từ mô tả

AI soạn bản nháp từ các nguồn hiện có, sau đó chỉ hỏi phần còn thiếu:

0. **Tên và slug dự án:** lấy từ mô tả (ví dụ `HLPHONE` → `hlphone`). Dùng slug này cho tên file `<du-an>` ở mọi cổng. Tên chưa rõ thì đưa vào đợt hỏi đầu.
1. **As-Is → To-Be:** nêu vấn đề thực tế (quản lý bằng Excel, sai lệch tồn kho, khó tra cứu…) và giải pháp chuẩn hóa bằng hệ thống.
2. **Actors:** các nhóm người dùng tương tác trực tiếp với hệ thống, kèm quyền được thực hiện và không được thực hiện.
3. **Danh mục Epic:** gom yêu cầu cùng miền trách nhiệm thành Epic `EP01`, `EP02`…, tên dạng `Quản lý + …`. Mỗi Epic liệt kê "các yêu cầu xác định được", là đầu vào để tách story ở G2.
4. **Quy tắc nghiệp vụ:** mỗi rule có ID `BRxx`, ví dụ và nguồn xác nhận (`bên yêu cầu xác nhận`, `tài liệu <tên>`, `AI suy luận – cần xác nhận`). Rule do AI suy luận là giả định mở, chưa được tính là đã rõ.
5. **Yêu cầu phi chức năng:** các yêu cầu như "giao diện đơn giản", "tìm kiếm nhanh", "chạy trên máy tính quầy". Diễn đạt thành câu kiểm tra được khi có thể (ví dụ: tìm sản phẩm theo tên hoặc mã trong một ô tìm kiếm). Các yêu cầu này đi vào AC của story liên quan ở G2, không thành story riêng.

## 4. Phỏng vấn case study

- Hỏi theo đợt, mỗi đợt 2–4 câu qua `ask`. Mỗi câu nêu một tình huống cụ thể kèm các phương án xử lý; tránh câu hỏi chung chung như "Quy tắc nghiệp vụ là gì?".
  - Ví dụ: "Khách mua 2 máy nhưng kho chỉ còn 1: hệ thống chặn tạo đơn, cho tạo đơn chờ hàng, hay cho bán và báo kho sau?"
- Sau mỗi đợt, cập nhật bản nháp brief và chỉ hỏi tiếp phần còn thiếu. Dừng khi đạt điều kiện ở mục 6. Không đặt số câu tối thiểu hay tối đa.
- Không hỏi chi tiết giao diện, màu sắc, công nghệ, hạ tầng; các nội dung này không ảnh hưởng tới backlog ở mức story.
- Làm rõ thuật ngữ mơ hồ (ví dụ: "hủy đơn" và "trả hàng" khác nhau thế nào; "khách hàng" có phải người đăng nhập hệ thống không).

**Chủ đề gợi ý cho quy mô Vừa/Lớn** (chỉ hỏi phần áp dụng):
- Vòng đời và trạng thái của thực thể chính (đơn hàng, phiếu, hợp đồng…).
- Tính tiền, giảm giá, hoàn tiền, các ràng buộc số liệu (tồn kho không âm…).
- Hai người cùng thao tác trên một dữ liệu.
- Phân quyền chi tiết theo actor.
- Sự cố và ngoại lệ (thanh toán lỗi, hủy giữa chừng).
- Tích hợp với hệ thống khác.

## 5. Danh sách phủ R1–R8

Hỏi bằng tình huống cụ thể, ví dụ: "Cuối tháng quản lý cần xem những số liệu nào, lọc theo tiêu chí gì, có xuất Excel không?", thay vì "Hệ thống có cần báo cáo không?".

- **R1. Mục tiêu:** vấn đề cần giải quyết, đối tượng hưởng lợi, kết quả đo được.
- **R2. Ưu tiên phạm vi:** nhóm chức năng nào Bắt buộc / Nên có / Để sau. Đây là đầu vào cho Priority ở G2.
- **R3. Báo cáo:** ai xem gì, kỳ báo cáo, bộ lọc, định dạng xuất.
- **R4. Pháp lý:** chứng từ bắt buộc, dữ liệu cá nhân, thời hạn lưu.
- **R5. Lịch sử thay đổi:** thao tác nào cần ghi vết người thực hiện và thời điểm.
- **R6. Dữ liệu cũ:** vị trí lưu trữ hiện tại, có chuyển đổi sang hệ thống mới không.
- **R7. Thông báo:** sự kiện nào thông báo cho ai, qua kênh nào.
- **R8. Ràng buộc dự án:** hạn chót, số người, thời gian khả dụng. Đây là đầu vào cho số sprint ở G3.

Theo quy mô:
- **MVP:** bắt buộc R1, R2, R8. Với R3–R7 chỉ xác nhận nhanh có cần hay không; không cần thì ghi `N/A` kèm lý do.
- **Vừa/Lớn:** cả R1–R8 phải có câu trả lời, hoặc `N/A` có lý do được bên yêu cầu xác nhận.

## 6. Điều kiện chốt brief

Brief được chốt khi:
1. Mỗi Epic có danh sách yêu cầu đủ để tách story.
2. Mỗi actor có phạm vi quyền rõ ràng.
3. Luồng chính không còn câu hỏi chặn.
4. R1–R8 đạt mức của quy mô đã chọn.

Trường hợp dừng sớm khi còn câu hỏi mở: ghi các câu hỏi vào mục `Câu hỏi mở`. Nếu vẫn duyệt, chuyển chúng vào mục `Rủi ro đã chấp nhận` trước khi duyệt.

## 7. Lưu và xin duyệt G1

1. Lưu `docs/workflow/specs/<du-an>-brief.md` theo mẫu `G1 — Business brief` trong `records.md`. Phân hệ đã có brief thì cập nhật tại chỗ.
2. Tóm tắt trong chat: số actors, danh mục Epic (ID, tên, số yêu cầu), rules chính, câu hỏi mở.
3. Gọi `ask` duyệt G1 với ba lựa chọn `Duyệt và tiếp tục` / `Cần điều chỉnh` / `Hỏi thêm chi tiết`, rồi dừng lượt.

Sau khi được duyệt, ghi trạng thái `approved` vào brief. Bước tiếp theo duy nhất là `product-backlog` (G2).

Khi yêu cầu thay đổi về sau: sửa brief tại chỗ, ghi ngày và nội dung thay đổi, liệt kê các story bị ảnh hưởng để G2 cập nhật.
