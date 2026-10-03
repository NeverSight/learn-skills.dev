---
name: product-backlog
description: "Cổng G2: tách yêu cầu đã duyệt thành User Stories có acceptance criteria, lập ma trận Actor–Story, đề xuất Priority, Story Point và Rank, xuất Product Backlog theo Epic và theo Rank."
hide: true
disable-model-invocation: true
---

# Product backlog (G2 Stories & Backlog)

Đọc `skill://product-workflow/references/contract.md` và `skill://product-workflow/references/records.md` trước. Nếu harness không hỗ trợ `skill://` (như Claude Code), đọc `<skills-dir>/product-workflow/references/`; `<skills-dir>` là thư mục cha của skill này (`.claude/skills/`, `.agents/skills/` hoặc bản toàn cục). Tên công cụ quy đổi theo `<skills-dir>/product-workflow/references/harness.md`.

## Đầu vào

- Brief G1 đã duyệt: actors, danh mục Epic, rules, R2.
- Hoặc danh sách story/backlog có sẵn từ bên yêu cầu. Khi đó chuẩn hóa theo mẫu và chỉ hỏi phần còn thiếu.

Brief chưa duyệt thì quay về G1. Thiếu rule ảnh hưởng tới story thì ghi câu hỏi mở. Không tự quyết định thay người phê duyệt.

## 1. Tách yêu cầu thành User Stories

Với từng Epic, chuyển mỗi "yêu cầu xác định được" thành một hoặc nhiều story:

```text
USxx – <Tên ngắn>: Là <actor>, tôi muốn <hành động> để <giá trị>.
```

- Mỗi story là một chức năng người dùng cuối nhìn thấy và demo được. Không tách story theo tầng kỹ thuật (UI, API, DB); việc đó thuộc task ở G3.
- Chức năng hệ thống tự thực hiện được viết `Là hệ thống, tôi muốn … để …`, ghi rõ sự kiện kích hoạt (ví dụ: tự trừ tồn kho sau khi thanh toán).
- Kiểm tra INVEST: độc lập, thương lượng được, có giá trị, ước lượng được, đủ nhỏ, kiểm thử được.
- Story quá lớn (> 13 SP hoặc gồm nhiều hành động) phải tách, ví dụ "Quản lý khách hàng" tách thành Thêm / Sửa / Tìm kiếm / Xem lịch sử mua hàng.
- Không tự thêm chức năng ngoài brief. Chức năng còn thiếu được nêu thành đề xuất kèm câu hỏi xác nhận.
- Ghi dependency giữa các story ngay trong story (ví dụ `Phụ thuộc: US04`). Đây là đầu vào cho Rank và sprint.

## 2. Acceptance Criteria

Mỗi story có 2–5 AC dạng Given / When / Then:
- Có ít nhất một luồng thành công, và luồng từ chối hoặc lỗi quan trọng nếu có.
- Dẫn chiếu rule `BRxx` liên quan.
- Kết quả phải quan sát được. Không viết AC mang tính cảm tính như "giao diện đẹp", "chạy nhanh", "không lỗi".

## 3. Ma trận Actor–Story

Lập theo mẫu trong `records.md`: cột là actors trong brief, đánh `✓` khi actor thực hiện hoặc sử dụng trực tiếp story. Căn cứ vào rule phân quyền; nhu cầu hay lợi ích gián tiếp không tự động tạo ra quyền.

Story `Là hệ thống` không có actor thực hiện: ghi `(tự động)` ở ô User Story, để trống các cột actor, và ghi actor kích hoạt ở trường `Phụ thuộc` hoặc phần mô tả (ví dụ: chạy khi NV bán hàng xác nhận thanh toán).

Rà soát ma trận: story thường không có actor nào, actor không có story nào, hoặc phân quyền bất thường (ví dụ khách hàng được sửa giá). Phát hiện bất thường thì ghi câu hỏi mở.

## 4. Priority, Story Point, Rank

AI đề xuất cả ba giá trị với nhãn `(đề xuất)`; người phê duyệt chốt.

- **Priority** (`Highest` / `High` / `Medium` / `Low`): lấy từ R2.
  - `Highest`: Bắt buộc, và thiếu nó thì luồng giá trị chính không vận hành được (đăng nhập, tạo đơn, thanh toán).
  - `High`: Bắt buộc nhưng luồng chính vẫn demo được khi chưa có.
  - `Medium`: Nên có.
  - `Low`: Để sau.
- **Story Point** (`1, 2, 3, 5, 8, 13`):
  1. Chọn một story đơn giản, dễ hiểu làm mốc 3 SP (ví dụ "Thêm sản phẩm": một form, một bảng).
  2. So sánh từng story với mốc theo độ phức tạp, số rule, số màn hình, rủi ro. Không quy đổi ra giờ.
  3. Nhóm đã có phương pháp ước lượng riêng thì dùng phương pháp đó.
- **Rank** (1…N, không trùng): thứ tự xây dựng. Xét Priority, giá trị và dependency: story nền (đăng nhập, dữ liệu gốc) đứng trước story sử dụng nó, kể cả khi story sau có Priority cao hơn. Ghi rõ trong tóm tắt rằng Rank khác Priority.

Khi đề xuất, trình bày bảng Rank ngắn kèm lý do cho các vị trí không hiển nhiên. Khi có đánh đổi thực sự giữa hai phương án xếp hạng, dùng `ask` để lấy quyết định.

## 5. Lưu

1. `docs/workflow/specs/<du-an>-stories.md`: stories theo Epic, AC, ma trận Actor–Story. Theo mẫu `G2 — Stories` trong `records.md`.
2. `docs/workflow/product-backlog.md`: góc nhìn theo Epic (kèm cột actor), góc nhìn theo Rank, tổng hợp SP theo Epic. Theo mẫu `G2 — Product Backlog`. Cột `Sprint` để `—`.

File đã tồn tại thì cập nhật tại chỗ, giữ ID cũ.

## 6. Xin duyệt G2

1. Tóm tắt trong chat: số story theo Epic, tổng SP, 10 story đầu theo Rank, story có câu hỏi mở, các vị trí Rank khác Priority.
   - Nếu R8 đã có số người và hạn chót, ước lượng sơ bộ số sprint cần (`tổng SP ÷ velocity dự kiến`). Nếu vượt hạn chót, nêu rõ ngay ở G2 để cân nhắc hạ Priority hoặc cắt story trước khi duyệt. Con số chính thức vẫn chốt ở G3.
2. Gọi `ask` duyệt G2 với ba lựa chọn `Duyệt và tiếp tục` / `Cần điều chỉnh` / `Hỏi thêm chi tiết`, rồi dừng lượt.

Khi Priority/SP/Rank được điều chỉnh, cập nhật cả hai góc nhìn trong backlog cho khớp. Sau khi được duyệt, bỏ nhãn `(đề xuất)` và ghi `approved`. Bước tiếp theo duy nhất là `sprint-planning` (G3).

Khi bổ sung story về sau: dùng ID tiếp theo, chèn vào Rank, cập nhật tổng. Nếu đã có sprint plan thì nêu các sprint có thể bị ảnh hưởng để G3 lập lại.
