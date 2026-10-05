---
name: ddd.xreview
description: >
  Cross review：派多個獨立 AI 模型平行審查文件、規格一致性、實作與安全性，交叉比對 findings 降低單一模型盲點，
  驗證高嚴重度問題後直接回報對話並提出解決方法提案。
  開發完成後、commit 或 push 前使用；findings 的後續修正也在本流程內，不走 /ddd.fixbug。
  Trigger: "review code", "cross review", "let's review", "check my changes",
  "審查程式碼", "code review", "review 一下", /ddd.xreview。
---

# ddd.xreview — Cross Review

派多個獨立模型平行審查文件、規格一致性、實作與安全性，交叉比對 findings，**由 coordinator 驗證 Critical/Important 後直接回報對話**。主流程聚焦在「蒐集各方觀點 → 驗證 → 提出修法」，執行細節交給 orchestrator script。

## 嚴格禁令

- **禁止自動修改程式碼**：review 產出建議，不直接改 code。修改必須由使用者確認後才執行
- **禁止省略任一 reviewer 的意見**：即使結論相似，仍須完整呈現各方觀點
- **禁止以 main agent self-review 取代 cross review**：所有 reviewer 都失敗時直接告知使用者，不自己頂上

## 執行步驟

### 1. 確認 Review 範圍

- **Sprint 文件**：當前 sprint 的 `spec.md` 路徑。
- **Review Lens**：依變更範圍判斷本次啟用哪些 lens。
  1. 只有文件變更 → `Docs Lens`
  2. 文件 + 實作變更 → `Docs Lens`、`Spec Lens`、`Code Lens`、`Security Lens`
  3. 只有實作變更且有 spec 或已確認 task source → `Spec Lens`、`Code Lens`、`Security Lens`
  4. 只有實作變更但無 spec 或已確認 task source → `Code Lens`、`Security Lens`，並標記無法驗證規格一致性
- **Lens 摘要**（詳細 checklist 由 `ddd-reviewer` agent definition 自帶）：
  - **Docs**：規格自洽、可測性、edge case、scope、決策紀錄
  - **Spec**：規格符合度、任務完成度、scope drift、測試對應、SSOT 同步
  - **Code**：correctness、資料安全、failure mode、相容性、DRY 風險、可觀測性
  - **Security**：auth、trust boundary、injection、secrets、data exposure、abuse、supply chain
- **變更範圍**——依優先順序判斷，**勿硬套 `main`**：
  1. **使用者明確指定** → 直接採用（如「review changes from dev」→ `git diff dev...HEAD`）
  2. **使用者未指定** → 自動偵測上游：先查 tracking branch（`git rev-parse --abbrev-ref @{upstream}`），無則依序找 `dev`、`main`、`master`。偵測後用 Question Tool 確認：
     - 有未提交變更 → 確認要 review uncommitted 還是整個 branch diff
     - 在 feature branch 且無未提交變更 → 確認 `git diff <upstream>...HEAD`
     - 在 main/dev 上且無未提交變更 → 詢問要 review 什麼

各 reviewer 會自己讀檔案與跑 git，不需把完整內容塞進 prompt。

### 2. 組 Prompt 暫存檔

Reviewer prompt 只傳遞本次啟用的 lens 名稱；詳細 checklist 由 `ddd-reviewer` agent definition 自帶。

```bash
review_prompt_file=$(mktemp /tmp/xreview-XXXXXX.md) && cat > "$review_prompt_file" << 'XREVIEW_EOF'
請依照 ddd-reviewer 角色定義執行獨立 DDD review。

審查範圍：
- Sprint 規格：<spec.md 路徑>
- 任務來源：<spec.md 路徑>（Milestones）
- 變更：請執行 `<git diff 指令>` 取得
- 本次啟用 lens：<Docs Lens / Spec Lens / Code Lens / Security Lens>

請依啟用的 lens 與 ddd-reviewer 角色定義審查。先讀取 sprint 文件理解目標、驗收條件與任務來源（spec.md Milestones），再檢視文件與程式碼變更。
XREVIEW_EOF
echo "$review_prompt_file"
```

審查方法論由各 reviewer 的 `ddd-reviewer` agent definition 自帶。

### 3. 派 Orchestrator

公開入口維持 skill-local script：`scripts/xreview-orchestrator.sh`。此檔案是 shared `agent-runner.sh` 的 symlink entrypoint；runner 會依 invocation basename 進入 `xreview` mode。Coordinator 不需也不應直接呼叫 shared runner 實體路徑。

**Claude Code**（Monitor 可用）：

```
Monitor({
  command: "bash ~/.claude/skills/ddd.xreview/scripts/xreview-orchestrator.sh $review_prompt_file; rc=$?; rm -f $review_prompt_file; exit $rc",
  timeout_ms: 3600000,
  persistent: false,
  description: "xreview 平行派 N 個 reviewer"
})
```

**其他 host**（Gemini / Codex / OpenCode，走 blocking mode）：

```bash
XREVIEW_MODE=blocking bash <skill-dir>/scripts/xreview-orchestrator.sh "$review_prompt_file"; rc=$?; rm -f "$review_prompt_file"; exit "$rc"
```

模型覆蓋、短名、**單一 reviewer 冒煙測試**（驗證某 model／adapter 活著，不必組正式 review prompt）等用法見 `references/cli-reference.md`。

### 4. 收集並讀取結果

orchestrator 輸出 `RETURN <spec> <log> <final>` 和 `FAIL <spec> ...` 事件，以 `ALL_DONE` 收尾。Coordinator 必須先讀取各 RETURN 的 `<final-path>`，確認 reviewer report 內容後才進入整合；空檔標失敗。

事件格式與邊界案例見 `references/orchestrator-internals.md`。

### 5. 整合、驗證、回報

**5.1 閱讀 reviewer reports**

收到 `RETURN` 後，逐一讀取每份 `<final-path>`：

1. 確認 report 是否完整、可讀、且有明確 findings / 無 findings 結論
2. 標記失敗、空報告、格式不完整的 reviewer
3. 保留每位 reviewer 的原始觀點，後續整合時不得省略

**5.2 組對照表**

```markdown
# Cross Review 報告

## Reviewer 組成
| Reviewer | 模型 | 狀態 |
|----------|------|------|
| claude | claude-opus-4-7 | ✅ 完成 |
| opencode | gpt-5.x | ✅ 完成 |
| gemini | gemini-3-pro-preview | ❌ 失敗（timeout） |

## 各 Reviewer 評估
<每個有效 reviewer 一個 section，完整呈現 review 結果>

## 交叉比對
| 問題 | claude | opencode | gemini | 共識 |
|------|--------|----------|--------|------|
| <問題摘要> | Critical/Important/未提及 | ... | ... | 一致/分歧 |

## 共識問題
<最值得優先處理>

## 分歧點
<意見不同之處>

## 共識優點
<多方都認可的設計>
```

**5.3 Coordinator 驗證 Critical / Important findings**

彙整完成後、回報給使用者前，coordinator 先自行驗證中～高嚴重度的 findings：

1. 從報告篩 Critical / Important findings
2. 逐一讀 finding 引用的程式碼確認問題是否真實存在
3. 標記每個 finding：
   - ✅ **確認**：問題存在，附上修正建議與優先度
   - ⚠️ **存疑**：無法確認或情境不明，保留給使用者判斷
   - ❌ **False Positive**：問題不存在或 reviewer 誤讀，說明理由

**原則**：驗證時讀實際程式碼，不靠 reviewer 描述；共識不等於正確，共識問題仍須驗證；低嚴重度直接帶過。

**5.4 對話回報**

完整報告直接回應到對話，不另寫 `xreview-<YYYYMMDD>.md`，也不串 Question Tool。使用者要修哪些項目、採用哪個方案，改由一般對話確認；不得在同一輪自動修改程式碼。

對話報告至少包含：

1. Review 範圍、啟用 lens、reviewer 成功 / 失敗狀態
2. 每個待決策 issue 的 ID、嚴重度、提出者、驗證結果；ID 採 `Issue #N` 循序編號，與第 6 節 Question Tool 的 `header` 同一套編號
3. 證據：檔案路徑、行號、必要程式碼片段
4. 影響：不修會造成什麼風險
5. 解決方法提案：每個待處理 issue 至少列 1 個建議修法；有明顯 tradeoff 時列 2–3 個方案，標出推薦方案與理由
6. ❌ False Positive 項目：每項一行帶過（finding 與駁回理由），不列入待決策

### 6. 修正銜接

對步驟 5.3 標記為 ✅ 確認 或 ⚠️ 存疑 的每個 issue，在對話報告中附修法提案與建議優先序。使用者明確要求修正後，依 AGENTS.md「角色分工」路由；需要 `ddd-developer` 的 findings 與對應方向彙整後一次派發。

修正完成並驗收後，由 coordinator 在當前 sprint 的 `works.md` 追加紀錄，不需要獨立開檔（works.md 整體格式見 `/ddd.work`）：

```markdown
### xreview 修正

- **[finding 摘要]**：<修了什麼> → <測試結果>
- **[finding 摘要]**：<修了什麼> → <測試結果>
```

## 產出

- 對話中的 Cross Review 報告（對照表＋驗證結果＋解決方法提案）
- 使用者確認後的程式碼修正（由 `ddd-developer` 執行）
- 更新後的 `works.md`（xreview 修正紀錄）

## 結束條件

使用者確認 review 結果，修正完成（或決定不修正）。

## 進一步閱讀

- `references/cli-reference.md` — 模型覆蓋、短名、部署前提
- `references/orchestrator-internals.md` — 事件語意、timeout、content-layer 失敗、config
- `references/cli-adapters.md` — 各 CLI 的安裝、認證、JSON 抽取機制
