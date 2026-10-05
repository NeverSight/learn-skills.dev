---
name: ticket
description: 'Use whenever the user wants to create, track, query, or manage tickets: claim, release, complete, handoff, resume, migrate IDs, plan-to-ticket, split, evaluate granularity. Triggers: /ticket, task tracking, ticket lifecycle.'
argument-hint: '<subcommand> [args]'
allowed-tools: Bash(ticket *), Read, Write, Edit, Grep, Glob
metadata:
  version: 2.44.37
---

# Ticket System

統一 Ticket 系統，整合 create/track/handoff/resume/migrate/generate 等頂層子命令；`lease`／`registry`／`票面`／`落票`／`派發骨架`／`鑑識三查`／`隔離索引`／`接手`等術語定義見 `references/architecture.md`〈術語〉，本檔各詞首次出現處皆指向該節。

---

## Ticket 狀態與程式碼提交的 root 分離（worktree 場景）

linked worktree 內執行 `ticket track` 系列命令時，ticket 狀態（md 讀寫）與程式碼提交走**兩條不同的 root 解析路徑**：狀態一律反向回推寫入主倉庫，提交依 cwd 或 --worktree 旗標解析——此為刻意設計，非 cwd 解析漏洞，誤判並「修復」會重新引入票面分裂風險。

> 完整設計理由（Why/Consequence/Action）與查證方式：Read `references/track-command.md` 同名章節

---

## 執行方式

> 安裝 shim（`python3 .claude/scripts/install-skill-clis.py`）後任何目錄可執行 `ticket track summary` 等命令；不要直接執行 `ticket_system/` 內的 `.py`（該 Python 套件僅透過 `pyproject.toml` 入口點執行）。完整安裝機制（shim 原理、`--check`、本地不安裝執行）見 `references/architecture.md`「安裝與執行方式」章節。

### subagent 派發時 claim 推薦用法

被派發的 subagent 認領自身 ticket 時，推薦使用 `ticket track claim <id> --as <self-agent-name>` 申報自身身份（不加 `--verify`）。Why/Consequence/Action 與命令對照表見 `references/track-command.md`「claim 推薦用法（subagent 派發時的身份申報）」章節。

**覆核測試指令**（skill 自身測試套件）：唯一標準指令為裸 `pytest`（不帶路徑參數）。完整規則見 `references/architecture.md`「覆核測試指令（skill 自身測試套件）」章節。

### PM 先 claim 再派發時的身份死結（已修復）

PM 依 pm-role 流程先 `claim`（無 `--as` 或 `--as rosemary-project-manager`）
再派發時，`who.current` 停在 PM。派發的代理人執行 `complete --as <self>` 曾
兩條路徑皆被擋：帶 `--as` 被 identity-guard 以身份不符拒絕，不帶 `--as`
則被要求必須提供——且 who 是權責歸屬欄位，不該由執行者自行 `set-who` 繞過。
三個代理人各自獨立撞上同一狀態後，補上兩道防線：

| 防線 | 機制 | 生效時機 |
|------|------|---------|
| 派發時自動重新綁定 | `dispatch-identity-bind-hook.py` 的 `UNBOUND_WHO_VALUES` 併入 PM 身份字面值，派發 Agent 工具呼叫成功後（PostToolUse）自動將 `who.current` 由 PM 改綁為實際派發的 subagent_type | 每次派發（常態路徑，事前預防） |
| complete 前置自動讓出 | `complete`/`finish` 執行 identity 對照前，若 `who.current` 仍是 PM 且 `--as` 申報為具名非 PM 執行者，自動重新指派 `who.current` 為該執行者後再走既有比對 | 每次 complete/finish（worktree 隔離派發等前者未觸發的場景之保底） |

兩道防線皆不需執行者自行 `set-who`，也不需 PM 代跑 `complete`。若仍出現
`who.current` 與具名執行者不符的 deny，訊息本身已含具體指令（`ticket track
set-who <id> --current <agent>`）——回報 PM 執行該指令重新指派，而非執行者
自行執行。

**`who.current` 的值因票而異，派發者無法預知**：上述兩道防線只處理
「PM 先 claim 再派發」這一種情況。若 ticket 從建立時就由另一代理人指定
具名執行者（`who.current` 從一開始就不是 PM），派發 prompt 若沿用經驗
寫死 `--as rosemary-project-manager`，反而會撞上情境 4（身份不符）——
因為真正該用的值其實是 `who.current` 目前的具體值，而這個值因票而異，
連派發者都無法預先猜對。故 deny 訊息本身直接把當前值印出來，不留占位符：

| 情境 | 訊息內容 |
|------|---------|
| 1a：缺 `--as`，`who.current` 已有具體值 | 直接給出可複製的 `--as <who.current 值>` 建議指令 |
| 1a：缺 `--as`，`who.current` 真無主 | 維持 `--as <agent-name>` 占位符提示 |
| 4：身份不符，`who.current` 已有具體值 | 並列兩條出口：(a) 若你就是該值，改用 `--as <值>` 自行重試；(b) 若指派本身錯誤，回報 PM 執行 `set-who` |
| 4：身份不符，`who.current` 真無主 | 僅出口 (b)（回報 PM `set-who`），不印出無法執行的 `--as (未指派)` |

執行者收到 deny 訊息時應直接依訊息內容判斷下一步，不需另外查
`ticket track who <id>` 才知道該填什麼。

---

## 無子命令時的預設行為（dashboard-first）

> `track onboard`／`track runqueue` 為輔助／除錯入口，非首選；裸 `/ticket` 一律先走本節 dashboard-first 流程（版本沿革見 CHANGELOG.md v2.7.0 條目）。

當用戶輸入 `/ticket`（無子命令或參數）時，依序執行以下流程：

1. **取得接手聚合視圖** — 執行 `ticket track dashboard --top 5`

   dashboard 一次回傳 `[In Progress]` + `[Handoff Target]`（待接手，`ticket resume <id>`）+ `[Ready Top N]` + `[Stale Warning]` 四區塊，Ready 區塊含可直接 claim 的編號 `[1] [2] [N]` 與 priority 標籤。設計目的：見 `references/track-command.md`〈track dashboard 子命令〉### 設計目的。

   [In Progress] 條目帶 lease 狀態標記（術語見 `references/architecture.md`〈術語〉）：`[LIVE]`＝FRESH session 處理中；`[RECLAIMABLE]`＝無 FRESH session 佐證持有（含 STALE／registry 未追蹤，須 reclaim）；無標記＝registry 不可用。

   - **dashboard 有 in_progress 或 ready 任務** → 使用 AskUserQuestion 依 dashboard 順序列出選項：
     - `[LIVE]` 的 in_progress 票**不列入選項**（issue tarrragon/claude#78），僅在 AUQ 前的回覆文字中資訊性提及（「N 張由其他 session 處理中」）
     - 非 `[LIVE]` 的 in_progress 任務優先列出（label: `[ip] {ticket_id} - {title}`；`[RECLAIMABLE]` 者 description: `無 FRESH session 佐證持有（走 reclaim 鑑識，非直接 resume）`；無標記者 description: `registry 無法判定（resume 接手）`）
     - Ready 任務依 dashboard `[1] [2] [N]` 編號順序列出（label: `[{N}] {ticket_id} - {title}`, description: `[{priority}]`）
     - 額外選項：「建立新 Ticket」（description: `執行 /ticket create`）
     - 用戶選擇：
       - 無標記 in_progress 任務 → `resume --list` 有列才 `ticket resume <selected_id>`；未列則 `ticket track full <selected_id>` 接手（票已 in_progress 無需 claim；收尾身份見 `track-command.md`「接手者收尾身份」）
       - `[RECLAIMABLE]` 任務 → `ticket track reclaim <selected_id>`（dry-run 通過再 `--confirm`，見 `track-command.md`〈track reclaim 子命令〉）。拒絕：即停手回報 PM；持續拒絕非 bug
       - Ready 任務 → `ticket track claim <selected_id>`
       - 建立新 Ticket → 引導進入 `/ticket create` 流程
     - 流程結束
   - **dashboard 只有 `[LIVE]` in_progress、無其他任務** → 回覆文字告知處理中清單後進入步驟 2 fallback（fallback 清單同樣不把 `[LIVE]` 票列為選項）
   - **dashboard 無 in_progress 也無 ready** → 進入步驟 2 fallback

2. **Fallback：完整 pending/in_progress 清單**（步驟 1 無可列入選項的任務時觸發，含「只有 `[LIVE]`」與「全空」） — 執行 `ticket track list --status pending in_progress`

   - **有待辦任務** → 使用 AskUserQuestion 列出選項：
     - 各待辦任務作為選項（label: `{ticket_id} - {title}`, description: `狀態: {status}`）
     - 額外選項：「建立新 Ticket」（description: `執行 /ticket create`）
     - 用戶選擇既有任務 → 依狀態處理：pending → claim；in_progress `[RECLAIMABLE]` → reclaim（同步驟 1 流程）；in_progress 無標記 → resume
     - 用戶選擇「建立新 Ticket」→ 引導進入 `/ticket create` 流程
     - 流程結束

3. **無任何待辦** → 顯示本檔〈子命令路由表〉

> **除錯查詢**：完整待恢復清單 `ticket resume --list`；scheduler 接手建議 `ticket track runqueue --context=resume --top 3`（SessionStart hook 會在用戶輸入前先印出此類提示作為歷史入口，PM 實際接手流程仍以 dashboard-first 為主）。

---

## 統一命令格式

```bash
/ticket <subcommand> [options]
```

> **命令層級慣例**：`create` / `batch-create` / `show` / `handoff` / `resume` / `migrate` / `generate` 為**頂層命令**；`claim` / `complete` / `append-log` / `query` / `list` / `set-acceptance` 等狀態操作在 **`track` 之下**（`ticket track <op> ...`）。常見誤打：`ticket track create`、`ticket claim`。本標註僅說明既有慣例，零 CLI 行為變更。

## 子命令路由表

> 下表以子命令為鍵，合併原三節（子命令總覽／子命令詳細說明／參考資料，WRAP 裁決見 issue tarrragon/claude#94）；跨子命令通用檔案（architecture／field-semantics／ticket-lifecycle-details）殿於相關群組或表尾。涵蓋章節欄與各 `references/*.md` 的 `##` 標題逐字雙向齊全（判準見 `skill-design-guide`〈按需讀取〉前言），僅計 fenced block 外的 `##`（`awk '/^```/{f=!f;next} !f && /^## /'`）；`batch-create`／`show` 無獨立 reference，見表後小節。`track` 子族僅具獨立 exit code 語意或需要 PM 額外理解流程分支者才獨立成列（如 `dashboard`／`reclaim`／`dispatch-readiness` 等，見下表列）；其餘子命令於 `track-command.md` 以 `##` 子節呈現，不獨立成列。

| 子命令 | 用途 | 範例 | 檔案 | 涵蓋章節 |
| --- | --- | --- | --- | --- |
| `create` | 建立 Atomic Ticket，支援 5W1H 引導式建立、子 Ticket 建立；版本目錄不存在時自動建立（無獨立 init 子命令） | `/ticket create --version 0.31.0 --wave 1 --action "實作" --target "XXX"` | `references/workflow-create.md` | 〈建立流程決策樹〉 |
| `create` | 需要參數/歸屬引導/重複偵測細節時讀本檔 |  | `references/create-command.md` | 〈基本用法〉〈版本歸屬引導〉〈主題歸屬（自動推導）〉〈多值參數格式〉〈類型說明〉〈決策樹路由參數〉〈重複偵測（兩層防護）〉〈可攜問題分流硬閘門〉〈--source-ticket 參數（衍生關係）〉 |
| `track` | 追蹤和更新 Ticket 狀態：READ 操作（summary/query/dashboard/list/runqueue/board/5W1H/validate 等）與 UPDATE 操作（claim/complete/release/set-*/append-log/dispatch 等）；`list` 支援 `--wave`、`--status`、`--format`、`--top`、`--all` | `/ticket track summary` | `references/workflow-execute.md` | 〈執行流程決策樹〉〈更新操作決策樹〉〈批量操作決策樹〉〈完成判斷決策樹〉〈完成後同步提醒〉 |
| `track` | 只需查詢決策路徑時讀本檔 | `ticket track query <id>` | `references/workflow-query.md` | 〈查詢流程決策樹〉 |
| `track` | 需要 UPDATE/READ 完整旗標細節時讀本檔 | `ticket track claim <id>` / `ticket track complete <id> --as <agent>` / `ticket track complete <id> --no-stage` / `ticket track complete <id> --force` | `references/track-command.md` | 〈子命令總覽（全量對照 --help）〉〈READ 操作〉〈track runqueue 子命令（Scheduler）〉〈UPDATE 操作〉〈UPDATE 操作補充：commit 副作用與欄位語意〉〈track commit 子命令〉〈track set-exit-status 子命令〉〈Ticket 狀態與程式碼提交的 root 分離（worktree 場景）〉〈驗收條件操作詳解〉〈CLI 可修改欄位 vs 手動編輯欄位〉〈track deps / depth 子命令〉〈track parallel-check 子命令〉〈track board 子命令〉〈track audit 子命令〉〈track stale-list 子命令〉〈track stuck-anas 子命令〉〈track dashboard 子命令〉〈track list 子命令〉〈track dispatch 子命令〉〈track dispatch-validate 子命令〉〈track dispatch-readiness 子命令〉〈track dispatch-check 子命令〉〈track sessions 子命令〉〈track reclaim 子命令〉〈track activity 子命令〉〈track conflicts 子命令〉〈track onboard 子命令〉〈track hook-liveness 子命令〉〈track register-artifact / resolve-artifact / list-artifacts 子命令〉〈共用旗標語意（track 系列命令通用）〉〈空狀態字面規範（track 系列命令通用）〉<!-- rule8-exempt: relocation:自 references/track-command.md 逐字搬移 --> |
| `track dashboard` | PM 接手聚合視圖，見 track-command.md〈track dashboard 子命令〉 | `ticket track dashboard --top 5` | — | — |
| `track list` | 預設 top 10 priority 排序，見 track-command.md〈track list 子命令〉 | `ticket track list --status pending --top 20` | — | — |
| `track td-status` | TD 清單校準，見 track-command.md〈td-status — 校準 TD 清單（PC-094）〉 | `ticket track td-status <id>` | — | — |
| `track reclaim` | 已鎖 ticket 受控釋放（ghost 鑑識三查，multi-PM Phase 3），見 track-command.md〈track reclaim 子命令〉 | `ticket track reclaim <id> --confirm` | — | — |
| `track stuck-anas` | 列出卡住的 ANA（spawned_tickets／children 全完成卻未收尾），見 track-command.md〈track stuck-anas 子命令〉 | `ticket track stuck-anas --wave 3` | — | — |
| `track depth` | 查詢嵌套深度與 can_descend（沿 parent_id 鏈），見 track-command.md〈track deps / depth 子命令〉 | `ticket track depth <id>.5` | — | — |
| `track parallel-check` | 偵測子任務/兄弟 ticket 檔案衝突（對齊 askuserquestion-rules 規則 7），見 track-command.md〈track parallel-check 子命令〉 | `ticket track parallel-check <id>` | — | — |
| `track dispatch-validate` | Context Bundle 自動填料合理性檢查（C 方案安全網；exit code 語意見 `references/track-command.md`〈track dispatch-validate 子命令〉，與 `dispatch-check` 不共享） | `ticket track dispatch-validate <id>` | — | — |
| `track dispatch-readiness` | 派發前綜合就緒度檢查（六項檢查：功能職責數／修改檔案數／Context Bundle tokens／acceptance 一致性／where.files 存在性／acceptance 路徑涵蓋；exit code 與閾值語意見 `references/track-command.md`〈track dispatch-readiness 子命令〉，與 `dispatch-check`／`dispatch-validate` 不共享） | `ticket track dispatch-readiness <id>` | — | — |
| `track dispatch` | 派發並落票，輸出代理人 prompt 骨架，見 track-command.md〈track dispatch 子命令〉 | `ticket track dispatch <id> --as <agent> --dry-run` | — | — |
| `track commit` | 隔離索引精確提交（files 為 `where.files` 子集），見 track-command.md〈track commit 子命令〉 | `ticket track commit <id> -m "..." -- {exact files}` | — | — |
| `track dispatch-check` | 列出目前活躍派發，見 track-command.md〈track dispatch-check 子命令〉 | `ticket track dispatch-check` | — | — |
| `track` | 設定或釐清 Ticket 血緣/依賴/關聯欄位與 where.files 語意、阻擋情境判斷 | — | `references/field-semantics.md` | 〈適用範圍〉〈六欄位定義〉〈阻擋語意對照表〉〈用戶情境對照表〉〈欄位選擇決策樹〉〈反模式速查〉〈設計沿革〉〈相關文件〉 |
| `track` | 查詢 Ticket 生命週期詳細規則（建立格式、驗收條件、決策樹路徑等） | — | `references/ticket-lifecycle-details.md` | 〈任務鏈後續步驟建議〉〈任務鏈 ID 格式〉〈Ticket 建立格式範本〉〈驗收條件 4V 格式要求〉〈Ticket 有效性驗證〉〈驗收前置條件檢查流程〉〈acceptance-gate-hook 技術細節〉〈驗收提示訊息模板〉〈P0 緊急任務處理〉〈簡化驗收檢查清單〉〈與其他流程的整合〉 |
| `handoff` | 任務鏈管理與 Context 交接：支援自動判斷方向、指定交接到父/子/兄弟任務，含絕對指向（`--next`）與從 worklog 批次補建（`--from-worklog`）。五種交接情境 | `/ticket handoff <id> --to-sibling <id2>` | `references/workflow-handoff.md` | 〈交接流程決策樹〉〈狀態-命令映射規則〉〈任務鏈結束決策樹〉〈恢復流程決策樹〉 |
| `handoff` | 需要旗標對照/指向語意/情境細節時讀本檔 |  | `references/handoff-command.md` | 〈移動方向與旗標對照〉〈指向語意：source vs target〉〈用法〉〈自動偵測行為〉〈Session 結束時的使用方式〉〈按 Ticket 狀態選擇命令〉〈任務鏈結束時的替代流程〉〈五種情境〉<!-- rule8-exempt: relocation:自 references/handoff-command.md 逐字搬移 --> |
| `resume` | 恢復任務：從 handoff 檔案載入 context；SessionStart hook 僅被動提醒，實際觸發見〈無子命令時的預設行為（dashboard-first）〉；`/ticket resume <id>` 可明確恢復指定任務（交接/恢復決策樹與 `handoff` 共用 `references/workflow-handoff.md`，見上列） | `/ticket resume <id>` | `references/resume-command.md` | 〈用法〉〈恢復機制（顯式觸發）〉〈Flag 說明〉〈handoff JSON 格式〉〈相關 Hook〉 |
| `migrate` | Ticket ID 遷移：支援單一和批量遷移；改名、引用改寫（含 discovered_during／closed_by／子孫 chain）與 topic-assignments 追加新 ID 行以單一隔離 commit 入庫（提交最終失敗 exit 75）；被遷移票的 `previous_ids` 欄位依序記錄曾用 ID（長度即遷移次數，與撞號改號的 `migrated_from` 不同），body 與 Context Bundle 中的舊 ID 不改寫 | `/ticket migrate <old-id> <new-id>` | `references/workflow-migrate.md` | 〈ID 遷移決策樹〉 |
| `migrate` | 需要前置檢查/批量配置/collision detection 細節時讀本檔 |  | `references/migrate-command.md` | 〈基本用法〉〈前置檢查（強制）〉〈單一遷移範例〉〈批量遷移配置檔案格式〉〈整版改號流程〉〈遷移邏輯〉〈Collision Detection〉〈備份機制〉〈Flag 說明〉<!-- rule8-exempt: relocation:自 references/migrate-command.md 逐字搬移 --> |
| `generate` | Plan 轉換為 Tickets：從 Plan 檔案自動生成 Atomic Tickets | `/ticket generate plan.md --version 0.31.0 --wave 5` | `references/generate-command.md` | 〈用法〉〈Flag 說明〉〈範例〉〈流程〉 |
| `batch-create` | 批次建立 Tickets：從模板 + 目標清單快速建立多個 Tickets，適用大量同質任務場景（如 30 個實作子任務）。詳見表後「batch-create 補充」 | `ticket batch-create --template impl-parsley --targets "a,b,c" --wave 28` | — | — |
| `show` | 顯示 Ticket（含 Markdown 渲染）。終端閱讀專用，詳見表後「show 補充」 | `ticket show <id>` / `ticket show <id> -r` | — | — |
| （跨子命令） | 查詢目錄結構、共用模組設計、自動化分析功能、系統模型完整版、multi-PM 協調層與票務術語、CLI 安裝與執行方式，或覆核 skill 測試套件；並行協調入口見 `pm-rules/parallel-dispatch.md`、`.claude/references/cross-session-coordination-details.md` | — | `references/architecture.md` | 〈系統模型（設計自我描述，完整版）〉〈術語〉〈目錄結構〉〈共用模組設計〉〈自動化分析功能〉〈安裝與執行方式〉〈覆核測試指令（skill 自身測試套件）〉 |

**整版改號**（`version-shift` 已於 2.44.21 移除）：`ticket migrate --config` 搬票，再手動完成 todolist 版本條目、worklog 主檔、舊目錄三步，每步驗證方式見 `references/migrate-command.md`〈整版改號流程〉。

不知該進哪一棵 workflow 決策樹時先看此列：新任務 → `workflow-create.md`；已認領待執行 → `workflow-execute.md`；只想查現況 → `workflow-query.md`；交接／恢復 → `workflow-handoff.md`；ID 需要更動 → `workflow-migrate.md`。

拆分邊界判讀（測試變綠驗收點）見 `/tdd` skill 的 task-granularity-rules；本 skill 負責建立/拆分 ticket 本身。

其餘 Ticket 生命週期規範散於框架文件（僅指名身分，不納入上表雙向驗證）：body 各 type 章節要求見 `ticket-body-schema`；拆分原則見 `atomic-ticket-methodology`；生命週期管理見 `ticket-lifecycle-management`；PM 端流程見 `ticket-lifecycle`。

### batch-create 補充

`batch-create` 只建立 tickets，不派發 agents。多任務派發前先寫 dispatch-plan（欄位定義見 `agent-dispatch-template`），保留每張 ticket 的獨立 prompt、commit policy 與 Exit Status；禁止把 batch-create 誤用為 batch dispatch CLI。

```bash
# 基本用法
ticket batch-create --template impl-parsley --targets "目標1,目標2,目標3" --wave 28

# 指定版本
ticket batch-create --template impl-parsley --targets "a,b,c" --version 0.31.0 --wave 28

# 預演模式（只顯示摘要，不建立檔案）
ticket batch-create --template impl-parsley --targets "a,b,c" --dry-run

# 建立子任務
ticket batch-create --template impl-parsley --targets "a,b" --parent <id>
```

**參數說明**：`--template`（必填，模板名稱如 `impl-parsley`）／`--targets`（必填，逗號分隔目標清單）／`--version`（建議明示；本專案自動偵測失效，缺此參數會回「無法偵測版本，請使用 --version 指定」，版本偵測與 `create` 不同源，屬已知限制）／`--wave`（必填；缺或 < 1 會回「Wave 編號無效」）／`--parent`（可選，建立子任務）／`--dry-run`（預演模式）。

**預定義模板**：`impl-parsley`（parsley-flutter-developer 實作 Ticket 模板，type: IMP, who: parsley-flutter-developer）；更多模板可在 `ticket_system/templates/` 目錄中定義。

### show 補充

TTY 下自動以 `glow`/`mdcat`/`bat` 渲染；pipe 時自動降純文字，避免汙染下游消費者。

```bash
ticket show <full-id>          # 完整 ID（含版本號）
ticket show <short-id>         # 短 ID（自動補當前版本）
ticket show <short-id> -r      # 純文字（同 track full）
ticket show <short-id> -R bat  # 指定渲染器
ticket show <short-id> -P      # 停用分頁
```

短 flag：`-r` raw / `-R` renderer / `-p` pager / `-P` no-pager。完整說明 `ticket show --help`。

與 `ticket track full <id>` 差異：`track full` 永遠純文字（腳本友善，向後相容）；`show` 預設渲染（閱讀友善）。

---

版本紀錄在同目錄的 `CHANGELOG.md`。
