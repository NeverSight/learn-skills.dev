---
name: product-workflow
description: "Dùng khi cần phân tích yêu cầu, xác định Epic/actors, viết User Stories, lập Product Backlog (Rank, Priority, Story Point) hoặc chia sprint và task. Điều phối 3 cổng duyệt: nghiệp vụ, stories và backlog, sprint và tasks; kết quả lưu Markdown trong docs/workflow/, có thể xuất CSV import Jira."
---

# Product workflow

Điểm vào duy nhất của quy trình: **từ mô tả yêu cầu đến Product Backlog và kế hoạch sprint có chia task**. Ngôn ngữ làm việc mặc định là tiếng Việt, trừ khi có yêu cầu khác.

Bộ skills chỉ phục vụ lập kế hoạch sản phẩm. Không viết code, thiết kế kiến trúc, review hay nghiệm thu. Yêu cầu thuộc các mảng này được nêu rõ là ngoài phạm vi; hướng xử lý tiếp theo do người phê duyệt quyết định.

Thuật ngữ vai trò dùng thống nhất trong bộ skills được định nghĩa tại `contract.md`, mục 3.

## Khởi động

1. Đọc `skill://product-workflow/references/contract.md` và `skill://product-workflow/references/harness.md`. Nếu harness không hỗ trợ `skill://` (như Claude Code), đọc cùng file dưới `<skills-dir>/product-workflow/references/`; `<skills-dir>` là thư mục cha của skill này (`.claude/skills/`, `.agents/skills/` hoặc bản toàn cục). Skills con dùng cùng quy tắc fallback. Tên công cụ viết theo Oh My Pi; harness khác quy đổi theo `harness.md`.
2. Rà soát `docs/workflow/` và tài liệu đầu vào được cung cấp (mô tả, PDF, Excel, backlog cũ) trước khi đặt câu hỏi. Không giả định dự án rỗng.
3. Xác định kiểu tiếp nhận (mục dưới) và cổng hiện tại. Báo cáo ngắn gọn: cổng hiện tại, nội dung đã có, nội dung còn thiếu, bước tiếp theo.

## Quy trình 3 cổng

```text
Mô tả yêu cầu
  → G1 Nghiệp vụ & Epic      (product-discovery) → [Duyệt]
  → G2 Stories & Backlog     (product-backlog)   → [Duyệt]
  → G3 Sprint & Tasks        (sprint-planning)   → [Duyệt] → Kết thúc
```

| Cổng | Skill phải đọc | Đầu ra | Điều kiện duyệt |
|---|---|---|---|
| G1 Nghiệp vụ & Epic | `skill://product-discovery` | `docs/workflow/specs/<du-an>-brief.md` | Vấn đề As-Is/To-Be, actors, danh mục Epic, rules chính, phạm vi và R1–R8 theo quy mô đã rõ |
| G2 Stories & Backlog | `skill://product-backlog` | `docs/workflow/specs/<du-an>-stories.md`, `docs/workflow/product-backlog.md` | Mọi story có actor, AC, Priority, Story Point, Rank; ma trận Actor–Story đầy đủ |
| G3 Sprint & Tasks | `skill://sprint-planning` | `docs/workflow/sprints/roadmap.md`, `docs/workflow/sprints/sprint-<X>-<slug>/sprint-plan.md`, tùy chọn `docs/workflow/jira-import.csv` | Có team/capacity đã xác nhận, Sprint Goal, story theo sprint trong capacity, bảng task cho từng story |

Đọc skill bằng công cụ đọc file (`read`; Claude Code: `Read`) trước khi thực hiện. Không dùng tool `Skill` để nạp skill ẩn. Chỉ đọc skill của cổng đang thực hiện, không đọc cả bộ.

Chỉ đọc `skill://diagram-design` khi có yêu cầu vẽ sơ đồ (story map, chuỗi dependency, roadmap). Bảng Markdown là định dạng mặc định. Không dùng Mermaid.

## Kiểu tiếp nhận

1. **Bắt đầu mới:** bắt đầu từ G1.
2. **Tiếp tục:** đọc file trong `docs/workflow/`, kiểm tra trạng thái cổng ở đầu mỗi file, rồi tiếp tục từ cổng chưa duyệt. Không hỏi lại nội dung đã chốt.
3. **Đã có đề bài hoặc backlog:** đưa dữ kiện vào đúng mẫu. Khi mô tả đã đủ rõ, G1 vẫn được thực hiện nhưng chỉ hỏi phần còn thiếu. Danh sách story có sẵn được chuẩn hóa ở G2. Backlog có sẵn Rank/SP được xác nhận lại trước khi chuyển sang G3.
4. **Thay đổi yêu cầu:** sửa brief hoặc story liên quan, cập nhật backlog, rồi lập lại kế hoạch cho các sprint bị ảnh hưởng. Giữ nguyên ID cũ. Cổng đã duyệt có nội dung thay đổi thì chuyển sang `needs-revalidation` và xin duyệt lại phần thay đổi.

## Quy tắc cổng

- **Mỗi lượt một cổng.** Hoàn thành một cổng thì lưu file, tóm tắt trong chat, gọi `ask` và dừng. Không thực hiện cổng tiếp theo trong cùng lượt.
- **Lưu file trước khi xin duyệt.** Mọi đầu ra của cổng phải nằm trong `docs/workflow/`, không chỉ hiển thị trong chat.
- `ask` duyệt cổng có ba lựa chọn: `Duyệt và tiếp tục` (recommended), `Cần điều chỉnh`, `Hỏi thêm chi tiết`.
- "OK" chỉ duyệt đúng cổng vừa trình bày.
- AI đề xuất, người phê duyệt quyết định. Priority, Story Point, Rank và phân bổ sprint do AI đưa ra đều là đề xuất cho đến khi được duyệt.
- Khi có yêu cầu rút ngắn quy trình (ví dụ "làm hết luôn"), vẫn dừng ở từng cổng, nhưng gom câu hỏi và giảm độ sâu phỏng vấn theo quy mô đã chọn.

## Kích hoạt

Ví dụ yêu cầu kích hoạt quy trình: "Phân tích yêu cầu hệ thống này", "Tạo product backlog từ mô tả sau", "Chia sprint cho backlog này", "Thêm chức năng X vào backlog", "Tiếp tục từ chỗ đang làm".

Oh My Pi: `/skill:product-workflow`. Claude Code: `/product-workflow`. Ba skill cổng có `hide: true` (Claude Code: `disable-model-invocation: true`): model không tự gọi, router đọc bằng đường dẫn file. Sau khi cài mới, cần mở phiên mới để harness nhận skill.
