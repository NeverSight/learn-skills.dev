---
name: frontier-scan
disable-model-invocation: true
description: "Quét biên giới agent-framework 30 ngày qua và đối chiếu overstack theo 8 trục (frontier-gap-scan runbook) — gọi INSTANT, không phải cron. Chạy 5 WebSearch, chấm Ngang/Chớm/Thua, diff kỳ trước, raise-issue cho gap mới / cập nhật gap đã có, cập nhật report. Trigger: 'frontier scan', 'quét đối thủ', 'scout tuần', 'chúng ta thua gì', '/frontier-scan'."
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
---

# Skill: frontier-scan

Bản gọi-INSTANT của runbook trong `fdk/wiki/concepts/frontier-gap-scan.md`. Mục tiêu: overstack là frontier TOÀN DIỆN, không ngủ trên chiến thắng. Thay cho routine cloud (bị chặn vì cần kết nối GitHub) — chạy thủ công bất cứ lúc nào, người-trong-vòng-lặp.

## WHAT

### Purpose và context
- **Purpose:** trinh sát biên giới agent-framework 30 ngày qua, chấm overstack theo 8 trục (Ngang/Chớm/Thua), diff với kỳ trước, raise/cập nhật issue cho gap và cập nhật report.
- **Trigger (when to use):**
  - "frontier scan", "quét đối thủ", "chạy scout", "scout tuần", "chúng ta thua gì so với thế giới", "/frontier-scan".
  - Định kỳ (ý định hàng tuần) hoặc khi nghe tin một framework/kỹ thuật mới đáng đối chiếu.
- **Non-goals:** nghiên cứu chủ đề chung (đó là `/last30days`); raise một issue lẻ đã biết (đó là `/raise-issue`); code fix gap (việc phiên nhận, mở bằng `/fdk`).

### Mental model
`runbook + baseline kỳ trước → 5 WebSearch (4 cố định + 1 tự do) → verdict 8 trục so với CAPABILITIES → diff kỳ trước (tụt hạng / trục mới) → issue (raise mới hoặc comment cập nhật) → report + log`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | runbook `fdk/wiki/concepts/frontier-gap-scan.md` | có | 8 trục + cách chấm |
| In | report kỳ trước `llmwiki/html/overstack-vs-world-30d.html` | có | baseline để diff |
| In | `llmwiki/wiki/sources/ISSUES.md` + `fdk/CAPABILITIES.md` | có | issue đang mở + năng lực hiện có |
| Out | verdict 8 trục + diff kỳ trước | có | nêu rõ trục tụt hạng / trục mới |
| Out | issue mới (ledger + GH) hoặc `gh issue comment` | theo gap | không trùng issue đã có |
| Out | report cập nhật + 1 dòng `llmwiki/wiki/log.md` | có | giữ baseline cũ, thêm phần diff kỳ mới |

### Rules và capabilities
- RULE-01 (MUST): CHỈ quét + raise/cập nhật + report. Không code, không tự-merge, không tự nâng status issue quá `open`.
- RULE-02 (MUST): Giữ 4 truy vấn quét cố định qua các kỳ để diff có nghĩa; truy vấn thứ 5 tự do.
- RULE-03 (MUST): Query wiki + ISSUES.md trước khi raise (R7-f) — không raise trùng gap đã có issue.
- RULE-04 (MUST): Định nghĩa "thắng": không trục nào ở **Thua** quá 2 kỳ liên tiếp mà không có issue đang chạy.
- RULE-05 (MUST): Repo cấm AI-attribution trong commit (R15) — nếu có commit, không thêm Co-Authored-By.
- RULE-06 (MUST): Touch only what the task requires — no opportunistic changes.
- Capabilities: tìm kiếm web; đọc report kỳ trước + ledger; ghi report + log + ledger; ghi issue lên tracker remote.

### Failure boundaries
- Thiếu report kỳ trước → không diff được: báo rõ đây là baseline đầu (**partial**), không bịa verdict kỳ trước.
- Tracker remote không truy cập được (chưa auth `gh`) → chỉ ghi ledger + ISSUES.md (**partial**), báo user.
- Gap không chắc đã có issue hay chưa → **clarify**/query thêm, không raise trùng (RULE-03).

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | deterministic | runbook, report, ISSUES.md | Đọc runbook + baseline | 8 trục + verdict kỳ trước + issue mở | thiếu report → partial (baseline đầu) |
| W02 | effect | 5 truy vấn | Quét 5 WebSearch (4 cố định + 1 tự do) | kết quả tìm kiếm | — |
| W03 | judgment | kết quả + `fdk/CAPABILITIES.md` | Chấm 8 trục Ngang/Chớm/Thua | verdict | — |
| W04 | judgment | verdict mới + cũ | Diff kỳ trước: tụt hạng / trục mới | danh sách thay đổi | — |
| W05 | effect | gap | Raise (B01) hoặc comment cập nhật (B02) | issue | trùng → B02 |
| W06 | effect | verdict + diff | Cập nhật report + log | report + log | — |
| W07 | deterministic | — | Dừng, không code fix | báo cáo | — |

Chi tiết từng bước (nguồn chân lý cho W01–W07):

1. **Đọc runbook + baseline**: `fdk/wiki/concepts/frontier-gap-scan.md` và report kỳ gần nhất `llmwiki/html/overstack-vs-world-30d.html`. Nạp danh sách 8 trục + verdict kỳ trước + issue đang mở (`llmwiki/wiki/sources/ISSUES.md`, GH#9-13 + Ralph #15).
2. **Quét (5 WebSearch)**: (a) Claude Code / agent framework updates tháng này; (b) AI agent memory + context engineering; (c) self-improving agents + harness eval; (d) agent skills marketplace + supply-chain security; (e) 1 truy vấn theo tin nóng tự chọn. Giữ 4 truy vấn đầu cố định để so-sánh-được qua kỳ.
3. **Đối chiếu**: chấm 8 trục (Harness, Orchestration, Memory, Self-evolving skills, Knowledge/context, Eval/observability, Skill security, Quy mô) so với `fdk/CAPABILITIES.md` → verdict Ngang/Chớm/Thua.
4. **Diff kỳ trước**: trục nào tụt hạng? trục MỚI nào xuất hiện? Đây là tín hiệu quan trọng nhất — nêu rõ.
5. **Raise / cập nhật** (R7-f query trước để không trùng):
   - Gap MỚI hoặc XẤU ĐI chưa có issue → `/raise-issue` (ledger draft + dòng ISSUES.md + `gh issue create --assignee Rheinmir`, body link ngược ledger, thêm mục "Repo/paper tham khảo").
   - Gap đã có issue → CHỈ `gh issue comment` cập nhật bằng chứng, KHÔNG raise trùng.
6. **Report + log**: cập nhật `llmwiki/html/overstack-vs-world-30d.html` (giữ baseline cũ, thêm phần diff kỳ mới) + append 1 dòng `llmwiki/wiki/log.md`.
7. **Dừng, KHÔNG code fix**: skill này chỉ trinh sát + raise. Thực thi gap là việc phiên nhận (mở bằng `/fdk`).

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | conditional_required | gap MỚI hoặc XẤU ĐI, chưa có issue | `/raise-issue` (ledger + ISSUES.md + `gh issue create`) | — | W06 |
| B02 | conditional_required | gap đã có issue | chỉ `gh issue comment` cập nhật bằng chứng | — | W06 |

### Validation và stopping
Mỗi issue mới phải qua query R7-f (không trùng); report giữ baseline cũ. Verdict 8 trục là judgment — cần người đọc duyệt. Dừng sau W07, không sang code.

### Examples
- **Positive:** "/frontier-scan" tuần này → trục Memory tụt Ngang → Chớm, chưa có issue → `/raise-issue` + dòng ISSUES.md; report thêm phần diff kỳ mới + 1 dòng log.
- **Boundary/failure:** trục Skill security vẫn Thua nhưng đã có issue đang mở trong ISSUES.md → chỉ `gh issue comment` bằng chứng mới, KHÔNG raise issue thứ hai.
