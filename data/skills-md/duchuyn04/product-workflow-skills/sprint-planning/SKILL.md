---
name: sprint-planning
description: "Cổng G3: từ Product Backlog đã duyệt, khảo sát team và capacity, xét dependency, chọn User Stories vào từng sprint theo 5 tiêu chí, viết Sprint Goal, chia story thành task và xuất CSV import Jira."
hide: true
disable-model-invocation: true
---

# Sprint planning (G3 Sprint & Tasks)

Đọc `skill://product-workflow/references/contract.md` và `skill://product-workflow/references/records.md` trước. Nếu harness không hỗ trợ `skill://` (như Claude Code), đọc `<skills-dir>/product-workflow/references/`; `<skills-dir>` là thư mục cha của skill này (`.claude/skills/`, `.agents/skills/` hoặc bản toàn cục). Tên công cụ quy đổi theo `<skills-dir>/product-workflow/references/harness.md`.

Quy trình: Product Backlog → Sprint Planning → Sprint Backlog → Task/Sub-task.

## Đầu vào

- `docs/workflow/product-backlog.md` đã duyệt G2 (Rank, Priority, SP) và file stories (dependency, AC).
- R8 trong brief: hạn chót, số người, thời gian.

Backlog chưa duyệt, hoặc có story thiếu SP, thì quay về G2.

## 1. Khảo sát nhóm

Dùng `ask` cho các thông tin chưa có, tối đa 4 câu trong một lần gọi:

```text
ask(questions=[
  {"id": "team_size", "question": "Nhóm thực hiện có bao nhiêu người?",
   "options": [
     {"label": "1 người", "description": "Thực hiện tuần tự, không cần phân vai."},
     {"label": "2–3 người", "description": "Phân vai Frontend / Backend / QA."},
     {"label": "4–6 người", "description": "Nhiều đầu việc song song trong một sprint."}
   ]},
  {"id": "sprint_length", "question": "Độ dài mỗi sprint?",
   "options": [
     {"label": "2 tuần", "description": "Phổ biến nhất."},
     {"label": "1 tuần", "description": "Phản hồi nhanh, sprint nhỏ."},
     {"label": "3–4 tuần", "description": "Ít sprint hơn, mỗi sprint nhiều story hơn."}
   ], "recommended": 0},
  {"id": "velocity", "question": "Velocity của nhóm (Story Point mỗi sprint) đã được xác định chưa?",
   "options": [
     {"label": "Chưa, cần đề xuất", "description": "AI ước lượng từ số người và độ dài sprint, nhóm xác nhận."},
     {"label": "Đã xác định", "description": "Nhập con số ở ô Other."}
   ], "recommended": 0}
])
```

- Không đánh dấu lựa chọn khuyến nghị cho câu hỏi số người; đây là dữ kiện, không phải đề xuất.
- Velocity chưa xác định: đề xuất một con số ban đầu và trình bày cách tính, ví dụ: `số người × số ngày làm việc thực tế trong sprint × SP một người hoàn thành mỗi ngày`. Nhóm mới hoặc sinh viên làm bán thời gian thì dùng hệ số thấp và nêu rõ giả định. Số liệu tham khảo, không phải mặc định: nhóm 4–5 sinh viên, sprint 2 tuần, khoảng 18–20 SP. Chỉ áp dụng sau khi được xác nhận.
- Nhóm từ 2 người trở lên: đề xuất phân vai (ví dụ 2 Backend, 1 Frontend, 1 QA) kèm nhãn `(đề xuất)`, hoặc đưa vào cùng lần gọi `ask` nếu còn chỗ. Cột `Vai trò` của task dựa trên phương án phân vai này.
- Có hạn chót (R8): tính số sprint khả dụng. Nếu tổng SP vượt `số sprint × velocity`, nêu rõ chênh lệch và đưa ra ba phương án để quyết định: cắt story Priority thấp, thêm sprint, hoặc giữ nguyên phạm vi và chấp nhận rủi ro.
- Không phỏng đoán số người hay tên thành viên.

## 2. Chuỗi dependency

Lập bảng dependency giữa các story từ trường `Phụ thuộc` của story, bổ sung các quan hệ còn thiếu. Ví dụ chuỗi: Đăng nhập → Quản lý sản phẩm → Tìm kiếm → Kiểm tra tồn kho → Tạo đơn → Thêm sản phẩm vào đơn → Tính tiền → Thanh toán → Trừ tồn kho → Hóa đơn.

Kiểm tra phụ thuộc vòng (A cần B, B cần A). Có phụ thuộc vòng thì tách story hoặc đưa vào câu hỏi mở.

Chỉ vẽ sơ đồ khi có yêu cầu, bằng `skill://diagram-design` (`type-dependency`).

## 3. Chọn story vào sprint

Không lấy máy móc N dòng đầu của backlog. Xét 5 tiêu chí:

1. **Priority:** ưu tiên story quan trọng.
2. **Story Point:** tổng SP của sprint không vượt capacity.
3. **Dependency:** story chỉ vào sprint khi các story nó phụ thuộc đã nằm ở sprint trước, hoặc cùng sprint và được xếp trước. Do đó Thanh toán dù `Highest` vẫn chưa vào Sprint 1 nếu chưa có Tạo đơn.
4. **Sprint Goal:** các story trong sprint cùng hướng tới một kết quả demo được.
5. **Capacity:** năng lực nhóm đã xác nhận ở bước 1. Ưu tiên chức năng cơ bản trước, chức năng phức tạp sau.

Trình tự cho từng sprint:
1. Xác định Sprint Goal trước: kết quả demo được tiếp theo trên luồng chính, dựa vào các story Rank cao nhất chưa xếp.
2. Duyệt theo Rank. Đưa vào sprint các story phục vụ Goal, đã thỏa dependency, và còn đủ chỗ trong capacity.
3. Story tiếp theo không vừa capacity thì chuyển sang sprint sau (ví dụ Sprint 2 = 21 SP, capacity 20, thì chuyển "Tạo hóa đơn" sang Sprint 3, còn 18 SP). Không lấy story Rank thấp hơn chỉ để lấp đầy capacity; sprint thấp hơn capacity vài SP là bình thường.
4. Chỉ đưa story Rank thấp hơn lên trước khi story đó phục vụ đúng Goal và story Rank cao hơn đang chờ dependency. Ghi lý do trong roadmap.
5. Đặt tên sprint `Sprint X – <Mục tiêu ngắn>`; Sprint Goal là một câu nêu kết quả người dùng cuối nhìn thấy được.
- Lập kế hoạch cho toàn bộ backlog khi cần lộ trình tổng thể. Sprint càng xa thì mức độ chắc chắn càng thấp; ghi chú điều này trong roadmap.
- Story không xếp được thì liệt kê ở mục "Story chưa xếp sprint" kèm lý do.

## 4. Chia story thành task

Với mỗi story trong sprint, chia thành task đánh số `T01`, `T02`… liên tục trên toàn dự án.

- Các phần cần xem xét: giao diện, dữ liệu/DB, API/xử lý, kiểm tra dữ liệu nhập, testing. Chỉ tạo task cho phần story thực sự cần. Không bắt buộc đủ 5 task, không tạo task hình thức để khớp mẫu.
- Mỗi task đủ nhỏ để một người hoàn thành trong 1–2 ngày.
- Mỗi story nên có ít nhất một task kiểm thử dựa trên AC của story.
- Cột `Vai trò`: Frontend / Backend / QA / Fullstack, theo số người đã khảo sát. Nhóm 1 người thì ghi `Fullstack` hoặc bỏ cột.
- Cột `Người phụ trách`: chỉ ghi tên đã được cung cấp. Chưa có thì ghi `—`.
- Cột `Phụ thuộc`: task phải hoàn thành trước. Cột này cho thấy các task có thể thực hiện song song.
- Việc nền không thuộc story nào (dựng project, tạo DB, dữ liệu mẫu) gắn vào story đầu tiên cần đến nó, thường ở Sprint 1. Không tạo story hình thức cho việc nền.
- Kiểm tra chuỗi task phụ thuộc dài nhất của mỗi vai trò có vừa độ dài sprint không. Nếu một người phải thực hiện tuần tự quá nhiều task, phân lại vai hoặc chuyển bớt story sang sprint sau, và nêu rủi ro này trong tóm tắt.

## 5. Lưu

1. `docs/workflow/sprints/roadmap.md`: thông tin nhóm, chuỗi dependency, bảng tổng thể các sprint, story chưa xếp sprint.
2. `docs/workflow/sprints/sprint-<X>-<slug>/sprint-plan.md` cho từng sprint: Sprint Goal, thời gian, capacity, bảng story, bảng task.
3. Điền cột `Sprint` ở cả hai góc nhìn trong `docs/workflow/product-backlog.md` và cập nhật velocity ở đầu file.

Tất cả theo mẫu trong `records.md`.

## 6. Xuất CSV cho Jira (tùy chọn)

Dùng `ask` xác nhận nhu cầu xuất file import Jira. Nếu cần, tạo `docs/workflow/jira-import.csv` theo mẫu `G3 — CSV import Jira` trong `records.md`: Epic, rồi Story, rồi Sub-task; kèm hướng dẫn map cột khi import. Không tự kết nối hay ghi vào Jira.

## 7. Xin duyệt G3

1. Tóm tắt trong chat: team và velocity, bảng tổng thể các sprint (Goal, story, SP), số task mỗi sprint, story chưa xếp, rủi ro (vượt hạn chót, dependency dài).
2. Gọi `ask` duyệt G3 với ba lựa chọn `Duyệt và tiếp tục` / `Cần điều chỉnh` / `Hỏi thêm chi tiết`, rồi dừng lượt.

Sau khi được duyệt, ghi `approved` và bỏ nhãn `(đề xuất)`. Quy trình kết thúc. Các bước tiếp theo đề xuất cho nhóm: import lên Jira bằng CSV, bắt đầu Sprint 1, cập nhật trạng thái To Do → In Progress → Testing → Done trên board, sau đó Sprint Review và Retrospective.

## Lập lại kế hoạch

Khi sprint trước chưa hoàn thành, có story mới, hoặc nhóm thay đổi:
- Story chưa hoàn thành quay lại backlog với Rank cũ. Không mặc định chuyển sang sprint sau như một cam kết.
- Chỉ lập lại các sprint chưa bắt đầu. Sprint đã chốt được giữ nguyên, trừ khi có yêu cầu thay đổi.
- Giữ ID story và task. Task mới dùng số tiếp theo.
- Xin duyệt lại phần thay đổi.
