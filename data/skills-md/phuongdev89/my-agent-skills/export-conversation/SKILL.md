---
name: export-conversation
description: Xuất cuộc hội thoại Antigravity hoặc Codex ra Markdown và JSON. Tự chọn adapter theo agent hiện tại; dùng khi cần lưu vết hoặc sao lưu phiên làm việc.
---

# Export-Conversation Skill

## Chọn nguồn

CLI tự chọn Codex khi môi trường có `CODEX_THREAD_ID`/`CODEX_SESSION_ID`, còn lại dùng Antigravity như trước. Dùng `--agent codex` hoặc `--agent antigravity` để chọn thủ công. Codex đọc rollout JSONL trong `$CODEX_HOME/sessions` (hoặc `~/.codex/sessions`); dùng `-c THREAD_ID` hay `--source FILE` để chọn phiên cụ thể. Không tự nhận Claude Desktop. Chỉ xuất dữ liệu thật có trong transcript; Codex không cung cấp nội dung suy nghĩ nội bộ để xuất.

Kỹ năng xuất toàn diện phiên làm việc của AI Coding Agent. Khác với việc chỉ copy lại text chat thông thường, `export-conversation` trích xuất đầy đủ tầng dữ liệu sâu của phiên làm việc:
1. **Lời thoại 2 chiều**: Nội dung yêu cầu của User và phản hồi của Assistant.
2. **Suy nghĩ của Model (Chain of Thought / Thinking)**: Toàn bộ quá trình lập luận ngầm của model trước mỗi hành động.
3. **Lịch sử thực thi lệnh Terminal (`run_command`)**: Câu lệnh đầy đủ, thư mục thực thi (`cwd`), trạng thái, mã thoát (`exit_code`) và output stdout/stderr thực tế.
4. **Quản lý Tác vụ nền & Lịch trình (`manage_task`, `schedule`)**: Trạng thái tác vụ ngầm, timer, cron, kèm nội dung log chi tiết từ hệ thống.
5. **Cây hoạt động của Subagents (`invoke_subagent`, `send_message`)**: Tự động duyệt đệ quy vào từng Subagent để bóc tách mục tiêu giao việc (prompt), lời thoại nội bộ, câu lệnh terminal và kết quả mà subagent đã hoàn thành.
6. **Đa định dạng đầu ra**: Xuất đồng thời hoặc tùy chọn Markdown (`.md`) đẹp mắt hoặc JSON (`.json`) chuẩn hóa.

---

## Quy định Session Directory (Bắt buộc)

Mọi tệp xuất, dữ liệu backup hội thoại hoặc log tạm phải tuân thủ nghiêm ngặt quy định tổ chức session của dự án:
- **Thư mục session**: `./.scratch/yyyy-mm-dd_export-conversation_<mô-tả-phiên-viết-không-dấu>/`
  - *Ví dụ*: `./.scratch/2026-09-25_export-conversation_fix-auth-bug/`
- **Tên tệp xuất chuẩn**:
  - Markdown: `<session_dir>/conversation_<conv_id[:8]>_<timestamp>.md`
  - JSON: `<session_dir>/conversation_<conv_id[:8]>_<timestamp>.json`
- **Quy tắc cấm xả rác**: Tuyệt đối không xuất file log hay file export bừa bãi ra thư mục gốc (`cwd` / repo root), trừ khi người dùng chỉ định đích danh một đường dẫn cụ thể (ví dụ: `--output ./exports/session.md`).

---

## Quy trình Thực thi của AI Agent (Agent Workflow)

Khi nhận được yêu cầu xuất cuộc hội thoại từ người dùng (ví dụ: *"hãy xuất cuộc hội thoại này ra file md/json"*, *"lưu lại lịch sử chạy lệnh và subagent"*), Agent thực hiện 4 bước sau:

### Bước 1: Xác định Conversation ID & Định dạng mong muốn
1. **Conversation ID**:
   - Nếu người dùng muốn xuất **phiên hiện tại**: Sử dụng Conversation ID của phiên làm việc hiện tại (được cung cấp trong system context), hoặc không cần truyền cờ `-c` để script tự động phát hiện phiên hoạt động mới nhất trong thư mục `brain/`.
   - Nếu người dùng cung cấp một ID cụ thể: Sử dụng ID đó qua tham số `-c <conversation_id>`.
2. **Định dạng (`format`)**:
   - Nếu người dùng yêu cầu Markdown: `-f md`
   - Nếu người dùng yêu cầu JSON: `-f json`
   - Nếu người dùng muốn cả hai hoặc không nói rõ: `-f all` (mặc định)

### Bước 2: Khởi tạo Session Directory
Khởi tạo thư mục scratch nếu người dùng không chỉ định đường dẫn output riêng:
```bash
SESSION_DIR="./.scratch/$(date +%Y-%m-%d)_export-conversation_session"
mkdir -p "$SESSION_DIR"
```
*(Trên Windows PowerShell có thể để script tự động tạo thư mục khi chạy).*

### Bước 3: Chạy Script Trích xuất (`export_conversation.py`)
Thực thi script thuần Python nằm ngay trong thư mục skill:

```bash
# Xuất cả Markdown và JSON (mặc định)
python skills/export-conversation/scripts/export_conversation.py -c <conversation_id> -f all -o "$SESSION_DIR"

# Chỉ xuất Markdown
python skills/export-conversation/scripts/export_conversation.py -c <conversation_id> -f md -o "$SESSION_DIR/chat-history.md"

# Chỉ xuất JSON
python skills/export-conversation/scripts/export_conversation.py -c <conversation_id> -f json -o "$SESSION_DIR/chat-history.json"
```

> [!TIP]
> Nếu muốn ẩn các đoạn suy nghĩ dài (thinking) trong file Markdown để tài liệu ngắn gọn hơn, thêm cờ `--no-thinking`.  
> Nếu không muốn đệ quy vào subagents, thêm cờ `--no-subagents`.

### Bước 4: Báo cáo Kết quả & Cung cấp Đường dẫn
Sau khi script hoàn thành, Agent:
1. Thông báo tóm tắt số liệu: Số lượt thoại (Turns), số lệnh chạy (Commands), số tác vụ (Tasks), số Subagents bóc tách được.
2. Dẫn link markdown file clickable (`file:///...`) tới tệp vừa xuất để người dùng có thể bấm mở trực tiếp.

---

## Chi tiết Định dạng Đầu ra

### 1. Định dạng Markdown (`.md`)
Bản xuất Markdown được cấu trúc theo tiêu chuẩn tài liệu kỹ thuật cao cấp:
- **Header & Stats Badges**: ID phiên, thời gian xuất, thời lượng, bảng tổng quan số liệu.
- **1. Full Dialogue & Turn History**: Lời thoại người dùng và phản hồi của trợ lý. Phần Thinking và Tool Call Arguments được gói trong thẻ `<details>` có thể thu gọn/mở rộng.
- **2. Terminal Command Execution History**: Bảng tổng hợp toàn bộ lệnh terminal đã chạy kèm exit code. Phía dưới là log chi tiết từng lệnh và stdout/stderr.
- **3. Background Tasks & Schedules**: Bảng thống kê các tác vụ nền, timer, cron và nội dung file log (`task-*.log`).
- **4. Subagent Operations & Tree**: Cây phân cấp subagent. Mỗi subagent hiển thị role, type, prompt được giao, số turn nội bộ, các lệnh terminal subagent đã chạy và hội thoại con.
- **5. Chronological Event Timeline**: Dòng thời gian chi tiết theo thứ tự diễn ra từng sự kiện.

### 2. Định dạng JSON (`.json`)
Cấu trúc JSON chuẩn hóa (RFC 8259) phục vụ phân tích tự động hoặc nạp vào hệ thống RAG/eval:
```json
{
  "conversation_id": "string",
  "metadata": {
    "start_time": "ISO-8601",
    "end_time": "ISO-8601",
    "total_steps": 120,
    "total_dialogue_turns": 40,
    "total_commands_run": 15,
    "total_tasks": 3,
    "total_subagents": 2
  },
  "dialogue": [
    {
      "turn": 1,
      "step_index": 0,
      "speaker": "user",
      "timestamp": "ISO-8601",
      "content": "cleaned user prompt",
      "raw_content": "raw content with system tags",
      "metadata": {}
    },
    {
      "turn": 2,
      "step_index": 1,
      "speaker": "assistant",
      "timestamp": "ISO-8601",
      "thinking": "chain of thought",
      "response": "assistant text response",
      "tool_calls": [
        {
          "name": "run_command",
          "args": {},
          "status": "DONE",
          "output": "command output"
        }
      ]
    }
  ],
  "command_history": [
    {
      "step_index": 12,
      "timestamp": "ISO-8601",
      "command": "python test.py",
      "cwd": "d:/project",
      "exit_code": 0,
      "output": "..."
    }
  ],
  "task_history": [
    {
      "task_id": "...",
      "type": "schedule",
      "log_content": "..."
    }
  ],
  "subagents": [
    {
      "subagent_meta": {
        "conversation_id": "...",
        "role": "Business Analyst",
        "type_name": "ba",
        "prompt": "..."
      },
      "subagent_data": {
        "metadata": {},
        "dialogue": [],
        "command_history": []
      }
    }
  ],
  "timeline": []
}
```

---

## Bảng Tham số Script `export_conversation.py`

| Tham số | Kiểu | Mặc định | Ý nghĩa |
| :--- | :--- | :--- | :--- |
| `-c`, `--conversation-id` | string | Tự nhận diện | ID phiên hội thoại cần xuất (mặc định lấy phiên mới nhất trong `brain/`). |
| `-b`, `--brain-dir` | string | Tự nhận diện | Đường dẫn thư mục transcript. Mặc định tự tìm thư mục Antigravity cục bộ; có thể ghi đè bằng `EXPORT_CONVERSATION_BRAIN_DIR`. |
| `-f`, `--format` | choice | `all` | Định dạng xuất: `md` (Markdown), `json` (JSON), hoặc `all` (cả hai). |
| `-o`, `--output` | string | `./.scratch/...` | Đường dẫn tệp hoặc thư mục lưu file xuất. |
| `--no-thinking` | flag | `false` | Loại bỏ phần Thinking trong file Markdown để giảm dung lượng file. |
| `--no-subagents` | flag | `false` | Không quét đệ quy vào transcript của các subagent. |
