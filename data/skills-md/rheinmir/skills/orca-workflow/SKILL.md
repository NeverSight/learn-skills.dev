---
name: orca-workflow
description: Daily propose → gate → dispatch workflow with Orca
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: orchestrate
  requires:
    harness: ">=1.3.127"
    bin: [agy, curl, docker, gh, opencode, orca, python3]
    scripts: [harness/poc-vendor-neutral/bin/pull-gate-sweep.sh, harness/scripts/archetype.py, harness/scripts/code-logger.py, harness/scripts/orca-reconcile.py]
---

# Skill: orca-workflow

> 🧭 Dispatch backend — chọn agent/model rẻ, chạy nhiều worker song song, cú pháp opencode/orchestration → xem **orca-dispatch-reference** (nguồn chân lý duy nhất, đừng nhân bản syntax ở đây).

## WHAT

### Purpose và context
- **Purpose:** Propose → gate → dispatch → verify qua Orca. Agent pool 1:1 per engine (claude, agy, opencode, kiro, copilot). Claude: analyze. Others: execute. Kill opencode nếu chờ quá lâu.
- **Trigger (when to use):**
- "propose <feature>", "feature request", "implement <name>"
- "chạy lint", "verify wiki"
- "sync template", "upstream"
- **Non-goals:** không xử lý SỰ CỐ (bug, lỗi runtime, regression → `orca-issue`); không nhân bản cú pháp dispatch backend (→ `orca-dispatch-reference`); không mô tả lại hành vi `/propose`, `/plan`, `/query` (single source of truth ở skill con).

### Mental model
`yêu cầu tính năng → R12 sweep → /query (wiki) → /propose (SPEC .md + .html render rẻ) → gate người duyệt → /plan (PLAN máy đọc) → task-create có dấu dự án → cổng HITL/AFK + kiểu việc → dispatch --inject nguyên văn → worker_done → [/qc-code] → verify-before-commit → output report`. Claude phân tích; agent khác thi hành; T-id (ledger bền) tách khỏi `task_xxxx` (Orca ephemeral, runtime-global).

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | mô tả tính năng ("propose <feature>", "implement <name>") | có | sự cố → rẽ sang `orca-issue` |
| In | `llmwiki/wiki/` | không | thiếu/rỗng → ghi "chưa có tiền lệ" |
| In | duyệt của user ở gate | có | trước khi `/plan` + dispatch |
| In | agent CLI sẵn có (`opencode`/`agy`/`kiro`/`gh copilot`/`orca`) | không | cạn → Claude tự làm |
| Out | SPEC draft `.md` + `.html` (qua `/propose`) | có | thứ người duyệt |
| Out | `llmwiki/wiki/sources/draft/DDMMYY-<tên>-PLAN.md` (qua `/plan`) | có sau duyệt | thứ máy thi hành |
| Out | task Orca có dấu dự án + trạng thái T-id | có | `approved`/`rejected`/`dispatched` qua code-logger (fail-open) |
| Out | output report `llmwiki/wiki/draft/orca/DDMMYY-<ten>.md` + index + log | có (trừ khi 0 artifact) | "xong" = worker_done + verify-before-commit xanh + report cập nhật Status |

### Rules và capabilities
- RULE-01 (MUST): **Caveman Mode**: Chọn độ chi tiết theo người đọc file. File markdown mà MÁY hoặc AGENT đọc và thực thi (SKILL.md, policy.yaml, AGENT.md, bảng tham chiếu thuần) thì viết ngắn gọn được — caveman ở đây tiết kiệm token mà không hại gì. Nhưng **tài liệu CON NGƯỜI đọc hoặc review thì BẮT BUỘC tắt caveman và viết đầy đủ** — proposal, output-report, wiki content (concept/ADR/registry), README, CONTRIBUTING và runbook, cùng mọi trang HTML. Những file này phải là văn xuôi với câu hoàn chỉnh, dễ đọc; không bỏ liên từ, không viết tắt cụt, không nhồi bảng thay cho câu giải thích. Bài học 2026-06-27: user phản hồi "caveman đã nén quá mức khi viết tài liệu", rồi làm rõ — file máy đọc thì gọn được, file người đọc thì cần đầy đủ.
- RULE-02 (MUST): Claude: analyze. Others: execute. Kill opencode nếu chờ quá lâu.
- RULE-03 (MUST): Sổ vấn đề quy trình (problem-tree) — Dự án có `llmwiki/` thì sổ cây vấn đề nằm ở `llmwiki/html/problem-tree.html` (repo framework: `fdk-problem-tree.html`). Phiên nào **phát hiện hoặc giải một vấn đề quy trình/framework** → cập nhật node vào block JSON `#tree-data` (append-only; solved phải ghi `solvedBy`; scope theo 3 trụ harness/skills/llmwiki — xanh lá chỉ khi 3/3). Quên cũng không mất: hook SessionEnd (R17) tự ghi thẻ pending bằng code, lần sau distill.
- RULE-04 (MUST): spec task PHẢI đóng dấu dự án: `orca orchestration task-create --spec "$(python3 harness/scripts/orca-reconcile.py --stamp '<spec>')"` (sổ task Orca là runtime-global).
- RULE-05 (MUST): *một agent được giao việc HITL chỉ còn cách đoán thay người dùng rồi im lặng — đó là con số 1/5, không phải model dốt* — HITL không dispatch cho CLI headless.
- RULE-06 (MUST): `--inject` bơm NGUYÊN VĂN brief của task từ PLAN kèm `## Global constraints`; KHÔNG tóm tắt lại.
- RULE-07 (MUST): An toàn container / DB — chạy `docker inspect <container_name> --format '{{json .Mounts}}' | python3 -m json.tool` trước bất kỳ `--force-recreate`, `down`, recreate nào; khác volume → DỪNG, hỏi user (chi tiết ở Reference).
- Capabilities: đọc wiki; tạo gate/task/dispatch qua orchestration runtime; chạy agent CLI headless hoặc terminal tương tác; ghi draft wiki + ledger T-id; (tuỳ chọn) bộ nhớ xuyên phiên qua HTTP; push đồng bộ skill lên repo nguồn.

### Failure boundaries
- Đầu vào là sự cố → **rẽ** sang `orca-issue`, không propose.
- R12 sweep: subrepo TARGET sau remote → **blocked** tới khi `git pull --rebase`; offline → fail-open.
- User từ chối ở gate → **cancelled**, T-id `state=rejected`.
- Task HITL → **không dispatch**, nhãn `ready-for-human` (chờ người).
- CLI headless im lặng quá ~60–90s / không tạo file / thiếu `diagram-box` → **kill**, Claude tiếp quản (fallback).
- Container volume khác compose → **blocked**, hỏi user.
- `task-update --status done` → `ok:false` lặng lẽ (status hợp lệ: `ready` | `in_progress` | `completed` | `failed`).

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | deterministic | workspace | Bước 0 — R12 (B) pre-work sweep `pull-gate-sweep.sh` một lần | base tươi | TARGET sau remote → pull --rebase rồi lặp |
| W02 | judgment | tính năng | Bước 1 — GỌI `/query` tổng hợp context wiki | điều đã biết + lỗ hổng | rỗng → "chưa có tiền lệ" |
| W03 | judgment | context | Bước 2 — GỌI `/propose` (SPEC `.md`); `.html` render dispatch sang CLI rẻ có watchdog | SPEC `.md` + `.html` | CLI im lặng → B03 |
| W04 | effect | SPEC | Bước 3 — `orca orchestration gate-create`, chờ user; ghi T-id approved/rejected | duyệt | từ chối → cancelled |
| W05 | judgment | SPEC đã duyệt | Bước 4 — GỌI `/plan` → PLAN; `task-create` mỗi `### Task` với spec đóng dấu | task `task_xxxx` | R7 PLAN chặn → sửa PLAN |
| W06 | judgment | task | Bước 4b — Cổng 1 HITL/AFK, Cổng 2 kiểu việc → archetype, rồi mới bảng chi phí | task AFK có kiểu + CLI | HITL → B02 |
| W07 | effect | task AFK | Bước 5 — `orca orchestration dispatch --task <id> --to <agent> --inject` (brief nguyên văn, dòng đầu khai kiểu việc); T-id dispatched | worker chạy | — |
| W08 | deterministic | dispatch | Bước 6 — `orca orchestration check --wait --types worker_done --timeout-ms 300000` | worker_done | timeout/im lặng → B03 |
| W09 | deterministic | diff | Bước 7 — `verify-before-commit` (gồm `qc-regression.py --run`) | commit sạch | đỏ → sửa |
| W10 | effect | kết quả | Output report + cập nhật Status agent + sync push skill (mục Delivery) | draft + index + log | 0 artifact → skip |

Chi tiết từng bước (nguồn chân lý cho W01–W09):

0. **R12 (B) — pre-work sweep cả workspace (MỘT LẦN, trước khi làm / fan-out đa-agent)**: orchestrator chạy `harness/poc-vendor-neutral/bin/pull-gate-sweep.sh` — quét MỌI subrepo (từ `.harness-workspace.yaml`, thiếu → auto-discover harnessed), fetch song song; subrepo **TARGET** sau remote → DỪNG, `git pull --rebase` trong repo đó rồi mới dispatch (cả đàn agent chung base tươi); subrepo `watch` chỉ cảnh báo. 1 repo → sweep tự rút về `pull-gate.sh`. Offline → fail-open. **KHÔNG chặn từng-edit** (cố tình bỏ per-edit PreToolUse). **R12 (C)** gate2 per-repo: cài mọi subrepo bằng `install-harness.sh --all-subrepos`; check tay `pull-gate.sh gate2`.
1. **query**: GỌI skill `query` (Skill tool → `query`, hoặc `/query`) để synthesis context từ `wiki/` về tính năng — KHÔNG đọc tay rời rạc, dùng đúng wiki-loop `query` (tổng hợp `[[wikilinks]]`, trả về điều đã biết + lỗ hổng). Project chưa có `wiki/` (hoặc query trả rỗng) → ghi nhận "chưa có tiền lệ" rồi sang bước 2.
2. **propose** — KHÔNG mô tả lại; **GỌI skill `propose`** (Skill tool → `/propose`, đúng pattern bước 1 gọi `query`). Mọi yêu cầu R7 (cặp `.md`+`.html`, `## Plan`, `## Agent Task Assignment`, glass-style `docs-site-macos`, prose chi tiết) sống trong skill con — sửa hành vi propose chỉ sửa `llmwiki/skills/dev-loop/propose.md`, KHÔNG sửa ở đây (single source of truth, xem [[ADR-003-skill-as-single-source-of-truth]]).
   - **Tách Claude-nghĩ / CLI-rẻ-render:** Claude (qua `/propose`) chỉ sản xuất SUBSTANCE = `.md` render-complete (Plan + prose + `## Render brief` = bước diagram dạng data + đoạn prose mỗi task). Phần `.html` là RENDER **cơ học** của `## Render brief` → **dispatch sang một CLI rẻ** theo bảng chi phí (OpenCode `big-pickle` → `agy` → `kiro`, $0). Render free nên dùng **Full** `docs-site-macos` richness, KHÔNG cắt bớt — token Claude chỉ tốn cho substance, không phình theo độ giàu HTML.
   - **Watchdog + R7 gate (bài học 250626 — headless giao ~1/5):** chờ ~60–90s; im lặng / không tạo file / thiếu `diagram-box` → **kill, Claude render fallback**. Thử CLI rẻ theo thứ tự sẵn-có (probe `--version`); cạn → Claude. R7 vẫn chặn lúc write+commit nên chất lượng được gác bất kể ai render.
3. **gate**: `orca orchestration gate-create --question "Duyệt proposal này?"` → chờ user (gửi kèm preview URL của html)
   - **Trụ 3 lifecycle (best-effort, fail-open):** user DUYỆT → `python3 harness/scripts/code-logger.py --task set <T-id> state=approved note="gate"` (`<T-id>` = field `task:` trong frontmatter draft do `/propose` mint; trống thì bỏ qua). User TỪ CHỐI → `--task set <T-id> state=rejected`. Lệnh fail-open, không chặn flow.
4. **Sau duyệt — GỌI skill `plan` (Skill tool → `/plan`) TRƯỚC KHI phân rã.** `/propose` sinh **SPEC** (thứ NGƯỜI đọc để duyệt); `/plan` mở rộng nó thành `llmwiki/wiki/sources/draft/DDMMYY-<tên>-PLAN.md` — thứ **MÁY** đọc để thi hành: mỗi `### Task` có `**Files:**` (đường dẫn chính xác), `**Interfaces:**` (Consumes/Produces — chữ ký cho task hàng xóm), và các bước 2–5 phút kiểu TDD có code thật + lệnh + output mong đợi. R7 nhánh PLAN chặn nếu thiếu. Rồi mới `orca orchestration task-create` cho mỗi `### Task` — **spec phải ĐÓNG DẤU dự án**:
     `orca orchestration task-create --spec "$(python3 harness/scripts/orca-reconcile.py --stamp '<spec>')"`.
     Sổ task của Orca là **runtime-global** (guide Orca nói thẳng); đo 2026-07-20: 18 terminal của NHIỀU dự án cùng ghi một sổ, nên `task-list` ở repo A trả về cả việc của repo B — và một orchestrator sẽ **claim nhầm task của dự án khác**, phá đúng mục tiêu tách-bias-tầng-vật-lý. Orca không có trường dự án (`task-create` không có tag, `task-list` không có bộ lọc), nên dấu này là cách duy nhất để quy thuộc chính xác — và nó còn đúng cả sau khi terminal tạo task đã chết (thực đo: 0/17 terminal cũ còn sống). Đối soát: `orca-reconcile.py [--scope current|all]`.
   - **Vì sao bắt buộc, không phải "nên":** agent CLI rẻ chạy headless **không thừa hưởng context nào** của phiên này và **không hỏi lại được** — nó chỉ có đúng thứ ta bơm vào; gặp chỗ mơ hồ nó **đoán rồi im lặng**. Brief mỏng chính là nguyên nhân của thực đo "giao hàng ~1/5" (bài học 250626), không phải do model dốt.
   - PLAN **không cần `.html`** — HTML gắn với SPEC (thứ người xem lúc duyệt), do `/propose` sinh. Vẽ diagram cho agent đọc là đốt token vô ích.
4b. **GIAO ĐÚNG LOẠI VIỆC — cổng chạy TRƯỚC khi chọn CLI.** Bảng chi phí bên dưới chỉ trả lời *"model nào rẻ nhất"*. Nó chưa bao giờ hỏi *"việc này làm được không cần người không"* — và đó là mảnh còn thiếu của con số ~1/5. Hai cổng, đúng thứ tự:
   - **Cổng 1 — HITL/AFK.** Task cần một người sống trả lời (quyết định thiết kế, đánh đổi, thứ chỉ user biết, truy cập ngoài, kiểm thủ công) là **HITL** → nhãn `ready-for-human` trong ledger, **KHÔNG dispatch cho CLI headless**. Chỉ task **AFK** (`ready-for-agent`) mới đi tiếp. Luật cứng: *một agent được giao việc HITL chỉ còn cách đoán thay người dùng rồi im lặng — đó là con số 1/5, không phải model dốt*.
   - **Cổng 2 — kiểu việc → archetype.** Gắn kiểu cho task: `research` (lôi ra fact) · `prototype` (bản thô để phản ứng) · `grilling` (hỏi từng câu) · `build` (thi hành theo brief) · `sweep` (dọn cơ học). Map sang archetype (ADR-015) → persona preamble. **Rồi mới** tới bảng chi phí chọn CLI — nó tụt xuống bước cuối, không phải bước đầu.
5. **dispatch**: `orca orchestration dispatch --task <id> --to <agent> --inject`
   - **`--inject` bơm NGUYÊN VĂN brief của task đó từ PLAN** (Files + Interfaces + Steps) **kèm `## Global constraints`** của PLAN. KHÔNG tóm tắt lại — tóm tắt chính là chỗ context rụng, và cái rụng luôn là cái agent cần.
   - **Dòng ĐẦU của brief khai kiểu việc:** một câu nói thẳng phiên này là phiên gì — "anh đang giải một QUYẾT ĐỊNH, không phải đi build" / "anh đang dọn cơ học, KHÔNG thêm feature". Kiểu việc quyết định *hình dạng của phiên*, không chỉ chọn model; một agent biết mình đang làm gì hành xử khác hẳn agent nhận một cục mô tả.
   - **Trụ 3 lifecycle (best-effort):** khi giao việc → `python3 harness/scripts/code-logger.py --task set <T-id> state=dispatched note="<agent>"`. Đây là `T-id` bền (audit trail bất biến), độc lập với `task_xxxx` ephemeral của orca orchestration. Fail-open.
   - **Persona theo archetype (Boris Cherny — 5 vai vòng đời):** muốn dispatch theo một *posture* cụ
     thể thì gọi bằng **từ khoá** — `/proto` `/build` `/sweep` `/grow` `/maintain`. Cơ chế:
     `python3 harness/scripts/archetype.py --get /<kw>` → in (a) **CLI gợi ý** cho archetype đó
     (Prototyper→opencode rẻ · Builder/Grower/Maintainer→Claude · Sweeper→opencode), và (b)
     **PREAMBLE persona** (`llmwiki/personas/<archetype>.md`) — **inject preamble đó vào `<task>`**
     trước khi dispatch để agy/opencode/kiro vào đúng vai (vd Sweeper bị cấm thêm feature). CLI nào
     hợp archetype nào là adapter `verified:false` (`harness/archetypes.config.yaml`). Xem ADR-015.
6. **Chờ**: `orca orchestration check --wait --types worker_done --timeout-ms 300000`
6b. **(Tùy chọn) QC senior trước commit** — muốn một cặp mắt senior soi diff trước khi chốt thì gọi `/qc-code` (Skill tool → `qc-code`): review 4 mục (security/performance/naming/logic) chấm điểm + verdict, và sinh test tái hiện `qc-*` cho mỗi bug logic. Verdict CẦN SỬA → sửa trước khi commit. **Tùy chọn, không bắt buộc** — verdict LLM là advisory (người quyết), thứ gác cứng là test `qc-*` chạy ở bước 7.
7. **Kiểm tra**: `verify-before-commit` tự động chạy trước mỗi commit (gồm bước 3b: `qc-regression.py --run` chạy test `qc-*` tất định — bug đã tái hiện không âm thầm quay lại).

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | conditional_required | đầu vào là SỰ CỐ (bug, lỗi runtime, regression, "hôm qua còn chạy") | GỌI skill `orca-issue` thay vì propose | sự cố nặng cần fan-out → orca-issue escalate về W07, giữ 2 chốt cứng của nó | kết thúc (hoặc W07 khi escalate) |
| B02 | conditional_required | task cần người sống trả lời (HITL) | nhãn `ready-for-human` trong ledger, KHÔNG dispatch CLI headless | — | chờ người, rồi W06 |
| B03 | recovery | CLI headless im lặng ~60–90s / không tạo file / thiếu `diagram-box` | kill + Claude tự tiếp quản theo spec; thử CLI rẻ kế tiếp theo thứ tự sẵn-có (probe `--version`) | cạn CLI → Claude | bước đang chạy (W03/W08) |
| B04 | user_optional | muốn soi diff trước khi chốt | Bước 6b — `/qc-code` (verdict advisory + test `qc-*`) | verdict CẦN SỬA → sửa trước commit | W09 |
| B05 | user_optional | muốn dispatch theo posture (`/proto` `/build` `/sweep` `/grow` `/maintain`) | `python3 harness/scripts/archetype.py --get /<kw>` → CLI gợi ý + inject PREAMBLE persona vào `<task>` | — | W07 |
| B06 | conditional_required | sắp đụng docker (`--force-recreate`, `down`, recreate) | `docker inspect` mounts, so với compose; khác → DỪNG hỏi user | không backup + xác nhận → không đổi volume | bước đang chạy |
| B07 | capability_optional | có `AGENTMEMORY_TOKEN` | search đầu session / remember sau decision + cuối session (Reference — AgentMemory) | không có → bỏ qua | W02 / W10 |

Chi tiết nhánh sự cố (nguyên văn):

#### Rẽ nhánh: SỰ CỐ ≠ tính năng
Đầu vào là **sự cố** (bug, lỗi runtime, regression, "hôm qua còn chạy") → **GỌI skill `orca-issue`** thay vì propose: vòng riêng triage → repro-first gate (chưa tái hiện chưa được sửa) → fix red→green → distill kép. Sự cố nặng cần fan-out thì orca-issue escalate ngược về đây để dispatch, nhưng 2 chốt cứng của nó vẫn giữ.

### Validation và stopping
Cổng người: gate W04 (duyệt SPEC) và Cổng 1 HITL ở W06. Cổng máy: R7 chặn SPEC/PLAN thiếu mục lúc write+commit; `verify-before-commit` + `qc-regression.py --run` trước mỗi commit. Watchdog CLI ~60–90s (B03); `check --wait` timeout 300000 ms. Đối soát task theo dự án: `orca-reconcile.py [--scope current|all]`.

### Examples
- **Positive:** "propose export CSV cho báo cáo" → sweep sạch → `/query` ra 2 trang liên quan → `/propose` sinh SPEC, `.html` render bằng `opencode run -m opencode/big-pickle` → user duyệt gate → `/plan` sinh `DDMMYY-export-csv-PLAN.md` 3 task → task-create có stamp → 2 task AFK `build` dispatch `--inject`, 1 task HITL ("chọn định dạng ngày") gắn `ready-for-human` → worker_done → verify-before-commit xanh → output report.
- **Boundary/failure:** "hôm qua login còn chạy, nay 500" → B01: không propose, gọi `orca-issue` (repro-first).
- **Boundary:** `opencode run` render `.html` im lặng 90s, không tạo file → B03: kill, Claude render fallback; R7 vẫn gác chất lượng lúc write.

### Reference — Gotchas orchestration CLI (bài học 230626)

- **2 id từ `task-create --json`**: response có envelope `id` (uuid) VÀ `result.task.id` (`task_xxxx`). Mọi lệnh sau (`gate-create --task`, `dispatch --task`, `task-update --id`) PHẢI dùng `result.task.id`, KHÔNG dùng envelope id. Dùng nhầm: gate vẫn tạo/resolve được nhưng trỏ task ma → task thật kẹt ở `ready`.
- **Status hợp lệ của `task-update --status`**: `ready` | `in_progress` | `completed` | `failed`. KHÔNG có `done` — truyền `done` trả `ok:false` lặng lẽ (không báo lỗi rõ).
- Lấy id thật chắc ăn: `orca orchestration task-list --json` rồi match theo `spec`.

### Reference — An toàn container / DB (BẮT BUỘC trước khi đụng docker)

#### Trước khi đụng container (docker compose / docker run)

```bash
# BẮT BUỘC chạy trước bất kỳ --force-recreate, down, recreate nào:
docker inspect <container_name> --format '{{json .Mounts}}' | python3 -m json.tool
```

So sánh `Source` path với volume trong compose file sắp dùng. Nếu khác → DỪNG, hỏi user.

**Production DB của Cozyroom:** `/mnt/c/Users/olive/orca/workspaces/home-spotify/m/data/metadata.db`
Không bao giờ đổi volume mount mà không backup + xác nhận user.

> Bài học 2026-05-29: recreate container với compose sai path → mất toàn bộ DB người dùng.

### Reference — Dispatch nhanh

> ⚠️ **CLI agent headless KHÔNG đáng tin (bài học 250626 — orca-eval):** `opencode run` / `agy -p` / `kiro run` chạy nền từ Claude Code thường **không giao hàng** (process thoát/treo, không tạo file — thực đo 1/5 task thành công). Quy tắc: đặt **watchdog** (~60–90s), nếu im lặng/không có file → **kill + Claude tự tiếp quản theo spec** (đừng chờ vô ích). Dùng OpenCode cho task boilerplate ĐỘC LẬP, đã verify được; task có dependency/nuance → Claude làm. Muốn dispatch THẬT cho agent → ưu tiên `orca terminal` interactive thay vì `-p`/`run`.

```bash
# OpenCode non-interactive (DEFAULT — dùng big-pickle miễn phí):
# ⚠ KHÔNG dùng --dangerously-skip-permissions khi dispatch từ Claude Code — auto-mode classifier sẽ DENY (bài học 120626)
opencode run -m opencode/big-pickle --dir "<project>" "<task>"

# Antigravity non-interactive:
agy -p "<task>"

# Kiro non-interactive:
kiro run --dir "<project>" "<task>"

# GitHub Copilot Coding Agent (async — via GitHub issue):
gh issue create --title "<task>" --body "<task details>" --assignee "@me"
# Then: gh copilot suggest "<task>" or trigger via VS Code Copilot Chat

# Nếu dùng Orca terminal (interactive):
orca terminal list
orca terminal create --worktree active --title "OpenCode" --command "opencode"
orca terminal send --title "OpenCode" --text "<task>"
orca terminal wait --for tui-idle && orca terminal read --title "OpenCode"
```

### Reference — Phân công task theo chi phí

| Task | Agent | Model |
|------|-------|-------|
| Search, grep, list, read | OpenCode | `opencode/big-pickle` ($0) |
| Viết boilerplate, CRUD | OpenCode | `opencode/big-pickle` ($0) |
| Wiki ingest/lint | OpenCode | `opencode/big-pickle` ($0) |
| Review diff, explain | agy | default |
| Architectural decisions | Claude Code | Opus 5 (`claude-opus-5`) — xem chain Claude ở `/orca-dispatch-reference` |
| Debug lỗi khó | Claude Code | Sonnet 5 (`claude-sonnet-5`) mặc định, nâng Opus 5 nếu đứng yên |
| Frontend UI boilerplate | Kiro | default |
| Cross-file refactor | Kiro | default |
| PR review + suggest fixes | Copilot | gpt-4o (GitHub) |

### Reference — Agent binaries

| Agent | Binary | CHECK |
|-------|--------|-------|
| Antigravity | `agy` | `agy --version` |
| OpenCode | `opencode run -m opencode/big-pickle` | `opencode --version` |
| Kiro | `kiro run` | `kiro --version` |
| GitHub Copilot | `gh copilot suggest` | `gh copilot --version` |
| Orca | GUI only — dùng qua `orca terminal *` commands | `orca terminal list` |

### Reference — Antigravity Dispatch Reality (tested 2026-05-21, updated 2026-05-23)

**Binary**: `agy` — `%LOCALAPPDATA%\agy\bin\agy.exe`. NOT `antigravity`, NOT `~/.local/bin/agy` (Linux).

**Tạo terminal**:
```bash
orca terminal create --worktree active --title "Antigravity" --command "agy"
```

**Hook**: Orca v1.4.21 fix Windows hook quoting — `antigravity-hook.cmd` no manual edit needed.

**OpenCode**: `opencode` — npm global at `%APPDATA%\npm\opencode.cmd`.

Dispatch status:

| Bước | Trạng thái |
|------|-----------|
| `dispatch --inject` | Thử sau v1.4.21 — nếu fail, dùng `terminal send` |
| `terminal send` thủ công | **OK** |
| Antigravity đọc file/chạy lệnh | **OK** |
| `worker_done` về inbox | Cần retest |

### Reference — Slash Skill Installation per Agent CLI

Agent nhận dispatch: **tự cài skill** từ `llmwiki/skills/` trước khi bắt đầu.

#### Claude Code CLI
```bash
mkdir -p .claude/commands/
cp llmwiki/skills/<loop>/<name>.md .claude/commands/<name>.md
# User-level:
mkdir -p ~/.claude/commands/
cp llmwiki/skills/<loop>/<name>.md ~/.claude/commands/<name>.md
```

#### OpenCode CLI
```bash
mkdir -p ~/.agents/skills/<name>/
cp llmwiki/skills/<loop>/<name>.md ~/.agents/skills/<name>/SKILL.md
# Restart OpenCode để discover skill mới.
```

#### Antigravity CLI
```bash
mkdir -p ~/.agents/skills/<name>/
cp llmwiki/skills/<loop>/<name>.md ~/.agents/skills/<name>/SKILL.md
```

#### Kiro CLI
```bash
mkdir -p ~/.kiro/skills/<name>/
cp llmwiki/skills/<loop>/<name>.md ~/.kiro/skills/<name>/SKILL.md
```

#### GitHub Copilot
```bash
# Workspace-level steering via .github/copilot-instructions.md
# Skills injected as context file:
mkdir -p .github/
cat llmwiki/skills/<loop>/<name>.md >> .github/copilot-instructions.md
# Or per-skill steering file (Copilot Workspace):
mkdir -p .github/skills/
cp llmwiki/skills/<loop>/<name>.md .github/skills/<name>.md
```

#### Rules cho tất cả agent
- Copy skill files only — skip `README.md`, `index.md`, `log.md`.
- File by file — no `cp -R`.
- Scope: `.claude/commands/` (Claude Code); `~/.agents/skills/` (OpenCode/agy); `~/.kiro/skills/` (Kiro); `.github/` (Copilot).
- Sau khi cài, report:
  ```
  | Agent       | Skill   | Installed at                            |
  |-------------|---------|------------------------------------------|
  | claude-cli  | propose | .claude/commands/propose.md              |
  | opencode    | propose | ~/.agents/skills/propose/SKILL.md        |
  | antigravity | propose | ~/.agents/skills/propose/SKILL.md        |
  | kiro        | propose | ~/.kiro/skills/propose/SKILL.md          |
  | copilot     | propose | .github/skills/propose.md                |
  ```

### Reference — AgentMemory — Persistent Cross-Session Memory

Service tại `https://agentmemory.giatbh.io.vn/` — lưu context giữa các session.

```bash
BASE="https://agentmemory.giatbh.io.vn"
TOKEN="${AGENTMEMORY_TOKEN}"

# Health check
curl -sk -H "Authorization: Bearer $TOKEN" "$BASE/agentmemory/health"

# Ghi memory (cuối session hoặc sau quyết định quan trọng)
curl -sk -X POST "$BASE/agentmemory/remember" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"<nội dung>","category":"fact|preference|decision|context"}'

# Tìm kiếm (đầu session hoặc trước khi propose)
curl -sk -H "Authorization: Bearer $TOKEN" \
  "$BASE/agentmemory/search?query=<từ+khóa>"
```

**Khi dùng:**
- **Đầu session**: search context trước khi bắt đầu
- **Sau decision**: lưu approach + lý do
- **Cuối session**: lưu tasks xong, commits, trạng thái

### Reference — Commands chính

```bash
orca orchestration run --spec "Propose: <tính năng>. Query wiki, tạo draft, gate chờ duyệt."
```

> Dispatch chi tiết: `llmwiki/skills/orchestrate/orca-dispatch-reference.md`

---

### Delivery — Output Report (sau khi implement xong)

> Đây là **báo cáo kết quả** sau khi implement, KHÔNG phải propose plan.
> Propose plan phải được tạo ở Bước 2 TRƯỚC khi làm bất kỳ thứ gì.

After all implementation tasks complete, write an output report to the wiki.

#### Steps

**1. Build the filename:**
- Format: `DDMMYY-<ten>.md`
- `DDMMYY` = today (e.g., `020626` for 2 June 2026)
- `<ten>` = 2–4 kebab-case words summarising what was done (e.g., `landing-page-coteccons`, `brand-kit-fintech`, `ingest-auth-spec`)

**2. Write** `llmwiki/wiki/draft/orca/DDMMYY-<ten>.md`:

```
---
type: draft
title: "DDMMYY-<ten>"
status: proposed
tags: [<skill-name>, output-report]
timestamp: YYYY-MM-DD
---

# DDMMYY-<ten>
**Type:** draft
**Status:** proposed
**Tags:** <skill-name>, output-report
**Proposed:** YYYY-MM-DD

## Agent Task Assignment
| Task | Agent | Status |
|------|-------|--------|
| <mô tả task 1> | <tên agent> | pending / in-progress / done |
| <mô tả task 2> | <tên agent> | pending / in-progress / done |

## What
<One sentence — what this skill invocation produced or decided>

## Output
<Key artefacts, files created/modified, or decisions made>

## Files
| File | Action |
|------|--------|
| `path/to/file` | created / modified |

## Notes
- Invoked via: `/<skill-name>` skill

## Origin
- **Draft:** `wiki/draft/orca/DDMMYY-<ten>.md`
- **Commit:** _(filled by verify-before-commit)_
- **Date promoted:** _(filled by verify-before-commit)_
```

**3. Update wiki index & log:**
- `llmwiki/wiki/index.md` — append one row: `| [DDMMYY-<ten>](draft/orca/DDMMYY-<ten>.md) | draft | YYYY-MM-DD |`
- `llmwiki/wiki/log.md` — append: `## YYYY-MM-DD — <skill-name> — <ten>`

**4. Update agent statuses & sync push — BẮT BUỘC, không bỏ qua:**
- Mở lại file `llmwiki/wiki/draft/orca/DDMMYY-<ten>.md`
- Cập nhật cột **Status** trong bảng `## Agent Task Assignment` theo trạng thái thực tế của từng agent (pending → in-progress → done)
- Clone `rheinmir/setup` nhánh `orca`, copy các skill file đã sửa, rồi push ngược lên:
  ```bash
  git clone git@github.com:rheinmir/setup.git /tmp/rheinmir-setup-sync -b orca --depth 1
  cp /path/to/skill.md /tmp/rheinmir-setup-sync/skills/<skill-name>/SKILL.md
  cd /tmp/rheinmir-setup-sync
  git add .
  git commit -m "skill: sync update — DDMMYY-<ten>"
  git push origin orca
  rm -rf /tmp/rheinmir-setup-sync
  ```

> Skip chỉ khi skill không tạo ra artifact hoặc quyết định nào.
