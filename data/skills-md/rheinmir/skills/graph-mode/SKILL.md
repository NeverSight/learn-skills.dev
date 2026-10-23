---
name: graph-mode
description: Bật luật chứng cứ evidence-chain (R19) cho phần CHAT — bắt buộc mọi chuỗi lập luận chấm dứt ở chứng cứ xem được (observed/tool-record/graph-edge/web/parametric/absence), khác fable5 (kỷ luật suy luận chung, không ràng buộc trích dẫn). Dùng khi user nói 'graph-mode', 'bật graph mode', 'evidence mode', hoặc invoke /graph-mode. Nặng token (buộc trích dẫn/mở file nhiều hơn mỗi câu trả lời) nên KHÔNG auto-bơm mỗi phiên — chỉ bật khi gọi tay. Once invoked it stays active for the rest of the session (toggle off with 'tắt graph mode' / 'graph-mode off' / 'normal mode').
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
---

# Skill: graph-mode

Luật chứng cứ của R19 (evidence-terminal) áp cho phần CHAT, chuyển ra khỏi
`llmwiki/CLAUDE.md`/`llmwiki/AGENT.md` (trước đây auto-bơm mọi phiên — nặng token vì
buộc trích dẫn/mở file nhiều hơn mỗi câu trả lời). Validator máy (`evidence_terminal.py`)
trên tài liệu có khối ```evidence-chain KHÔNG phụ thuộc skill này — luôn chạy qua
`harness/policy.yaml` bất kể graph-mode bật hay tắt. Skill này chỉ bật/tắt kỷ luật
CHAT (không validator nào với tới), là phần không tự-gate được nên cần cân nhắc chi phí
trước khi bật.

## WHAT

### Purpose và context
- **Purpose:** bật (và giữ cho tới khi tắt) kỷ luật CHAT: mọi chuỗi lập luận trong câu trả lời phải chấm dứt ở một trong sáu loại chứng cứ mở ra xem được.
- **Trigger (when to use):**
  - User nói "graph-mode", "bật graph mode", "evidence mode", "chế độ chứng cứ", hoặc gõ `/graph-mode`.
  - Việc cần độ tin cậy cao trên kết luận sẽ dùng để QUYẾT ĐỊNH (audit, nghiệm thu, viết ADR/PLAN, chẩn đoán bug lan rộng nhiều file) — nơi một kết luận sai giá đắt hơn vài lượt tool call thêm.
- **Non-goals:** KHÔNG dùng cho việc thường ngày (sửa 1 file, trả lời câu hỏi đơn giản, việc reversible) — bật tràn lan làm mọi câu trả lời dài và tốn hơn không cần thiết. Không thay/không đè validator máy R19 (`evidence_terminal.py`) cho tài liệu; không phải kỷ luật suy luận chung (đó là `fable5`).

### Mental model
`kết luận A → vì B → … → điểm cuối ∈ {observed, tool-record, graph-edge, web, parametric, absence}`. Trạng thái: `tắt (mặc định) → bật khi gọi → giữ mọi lượt → tắt khi user nói`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | lệnh bật | có | "graph-mode" / `/graph-mode` / "evidence mode"… |
| In | lệnh tắt | không | "tắt graph mode" / "graph-mode off" / "normal mode" |
| Out | mọi câu trả lời CHAT khi bật | có | mỗi chuỗi lập luận có điểm cuối thuộc 6 loại, khai đủ thuộc tính của loại đó |

### Rules và capabilities
- RULE-01 (MUST): Đây là kỷ luật CHAT không có validator nào bắt được — nếu tắt, không ai chặn; nếu
  bật, phải tự tuân thủ nghiêm vì không có cổng nào cứu.
- RULE-02 (MUST): Không đè lên luật R19 machine-gate cho tài liệu `evidence-chain` (`applies_to: [write]`
  trong `harness/policy.yaml`) — luật đó độc lập, luôn chạy bất kể skill này.
- RULE-03 (MUST): Touch only what the task requires — no opportunistic changes.
- RULE-04 (MUST): `parametric` KHÔNG được là điểm cuối duy nhất của một kết luận dùng để quyết định.
- RULE-05 (MUST): Không kết luận bằng "rõ ràng là", "ai cũng biết", hay bằng cách trỏ ngược về một mục lập luận khác trong cùng câu trả lời.
- Capabilities: đọc file / chạy lệnh / tra log-ledger / tra wiki graph / tìm web để lấy chứng cứ; không ghi gì do chính skill.

### Failure boundaries
- Không tìm được chứng cứ cho một mắt xích → khai rõ bằng `absence` (lệnh đã chạy + output rỗng) hoặc hạ kết luận thành chưa chứng minh, không lấp bằng lập luận.
- Chỉ có `parametric` cho kết luận dùng để quyết định → **partial**: nói rõ chưa kiểm chứng, đề nghị nâng lên `web`/`observed`.
- Việc thường ngày mà user vẫn bật → vẫn tuân theo (user quyết), có thể nhắc chi phí token một lần.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | deterministic | lệnh bật | Bật chế độ, ACTIVE mọi câu trả lời | trạng thái = bật | — |
| W02 | judgment | mỗi câu hỏi | Lập chuỗi lập luận, lần tới đáy chứng cứ thuộc 6 loại | câu trả lời có điểm cuối | mắt xích chỉ là suy luận → lần tiếp |
| W03 | deterministic | lệnh tắt | Tắt, trở lại trả lời thường | trạng thái = tắt | chưa có lệnh tắt → lặp W02 |

Chi tiết từng bước (nguồn chân lý cho W01–W03):

#### Bật (persistence)
ACTIVE MỌI câu trả lời kể từ lúc gọi cho tới khi tắt. Không tự trôi lại kiểu trả lời
suông sau nhiều lượt. **Tắt bằng:** "tắt graph mode" / "graph-mode off" / "normal mode".
Mặc định: **tắt** (không tự bật đầu phiên).

Khi bật, mọi chuỗi lập luận trong CHAT phải chấm dứt ở chứng cứ mở ra xem được, không
phải một lập luận nữa. Chuỗi `A vì B vì chứng cứ C` là xong; chuỗi `A vì B vì C` mà C
lại là suy luận thì CHƯA xong — phải khai tiếp C dựa trên cái gì, cho tới khi chạm đáy.

Sáu loại được tính là điểm cuối:
- `observed` — đường dẫn `file:line` mở ra được, hoặc lệnh chạy lại được kèm output.
- `tool-record` — id một mục trong provenance-log / events.jsonl / ledger.
- `graph-edge` — eid một cạnh trong wiki graph.
- `web` — dữ liệu tìm trên mạng: phải kèm **link tới ĐÚNG CHỖ tìm được** (không phải
  trang chủ), ngày truy cập, và trích nguyên văn đoạn đã dựa vào.
- `parametric` — kiến thức từ **training của model**: phải tự khai đúng là loại này,
  **chỉ rõ nó ở đâu ra** (tên chuẩn, tài liệu, tác giả), và nói rõ là chưa kiểm chứng.
  KHÔNG được là điểm cuối duy nhất của một kết luận dùng để quyết định — phải nâng lên
  `web`/`observed` hoặc đi kèm loại khác.
- `absence` — chính lệnh/truy vấn đã chạy để tìm, kèm output rỗng của nó.

Không kết luận bằng "rõ ràng là", "ai cũng biết", hay bằng cách trỏ ngược về một mục
lập luận khác trong cùng câu trả lời. Chi tiết cơ chế: [[evidence-terminal-chain]].

### Branches
Không có nhánh phụ trong version này.

### Validation và stopping
Không validator máy nào kiểm phần CHAT (RULE-01) — tuân thủ là tự kiểm: trước khi gửi, rà mỗi kết luận có điểm cuối thuộc 6 loại. Chế độ chỉ dừng khi user nói lệnh tắt.

### Examples
- **Positive:** bật graph-mode, hỏi "hook stop có chặn commit thiếu Origin không?" → trả lời kèm `observed` `llmwiki/.claude/hooks/stop.py:<line>` hoặc lệnh chạy lại + output, không dừng ở "chắc là có".
- **Boundary/failure:** kết luận quyết định chỉ dựa trên "theo spec OWASP (parametric)" → chưa đủ; phải khai `parametric` + nguồn, nói chưa kiểm chứng và nâng lên `web` (link đúng mục + ngày truy cập + trích nguyên văn) trước khi dùng để quyết định.
