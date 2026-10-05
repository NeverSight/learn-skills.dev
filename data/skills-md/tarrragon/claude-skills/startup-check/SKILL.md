---
name: startup-check
description: "Session startup check tool that recovers pending handoff tasks, verifies Git environment, and confirms development state. Use for: (1) environment verification at session start, (2) detecting pending handoff tasks to resume, (3) confirming Git and development environment status."
disable-model-invocation: true
metadata:
  version: 1.0.0
---

# Claude 指令：Startup-Check

此命令在 Claude Code session 開始時執行環境檢查，並偵測待恢復的 handoff 任務。

## 使用方法

```
/startup-check
```

## 系統指令

你是 Claude Code Session 啟動檢查專家。執行以下檢查流程，按順序完成每個步驟。

---

### Step 1: Handoff 待恢復任務偵測

**最高優先級**：先檢查是否有待恢復的 handoff 任務。

執行以下步驟：

1. 掃描 `.claude/handoff/pending/` 目錄中的所有 `.json` 檔案
2. 過濾條件：`resumed_at` 欄位為 `null`（表示尚未接手）
3. 如果找到待恢復任務：

**有待恢復任務時**：

對每個待恢復任務：

a. 讀取 handoff JSON 檔案，取得 `ticket_id`、`title`、`direction`
b. 從 `ticket_id` 解析版本號（例如 `{version}-W{wave}-{seq}` -> `v{version}`）
c. 讀取對應的 Ticket 檔案：`docs/work-logs/v{version}/tickets/{ticket_id}.md`
d. 輸出完整的 Ticket 內容到對話中

輸出格式：

```
============================================================
[Handoff 任務恢復] 偵測到 N 個待恢復任務
============================================================

任務: {ticket_id} - {title}
方向: {direction}

--- Ticket 完整內容 ---
{Ticket 檔案完整內容}
--- End ---

建議動作：
1. 執行 /ticket track claim {ticket_id} 認領任務
2. 根據 Ticket 內容繼續執行

============================================================
```

然後**直接開始恢復任務**：
- 讀取 Ticket 的 frontmatter 了解任務狀態和 TDD 階段
- 根據 Ticket 內容判斷下一步動作
- 主動開始執行（無需等待用戶額外指令）

**無待恢復任務時**：跳過此步驟，繼續 Step 2。

---

### Step 2: Git 環境檢查

執行以下指令並分析結果：

```bash
git status --porcelain
git branch --show-current
git log --oneline -3
```

預期結果：
- 工作目錄狀態（乾淨或有未提交變更）
- 當前分支名稱
- 最近 3 次提交

---

### Step 3: 開發狀態檢查

確認以下項目：
- 關鍵檔案存在性（CLAUDE.md、FLUTTER.md、pubspec.yaml）
- 最後測試執行時間（如可取得）

---

### Step 4: 輸出報告

彙整所有檢查結果，輸出簡潔的環境狀態報告。

```
=== Session 啟動檢查報告 ===

Handoff: {有/無} 待恢復任務
Git: {分支名} | {狀態}
環境: {正常/異常}

{如有 handoff 任務，已在 Step 1 輸出完整內容}
```

---

## 與 Hook 的協作邊界

| 元件 | 職責 | 觸發方式 |
|------|------|---------|
| startup-check SKILL | 主動恢復：讀取 Ticket 完整內容到主對話流 | 用戶執行 /startup-check |
| handoff-reminder-hook | 提醒：SessionStart 時顯示簡短提醒 | 自動（SessionStart） |
| handoff-prompt-reminder-hook | 備用注入：UserPromptSubmit 時注入 context | 自動（UserPromptSubmit） |

**設計原則**：
- SKILL 輸出在主對話流中，Claude 會自然處理並主動執行
- Hook 輸出在 system-reminder 中，作為備用提醒
- 兩者可共存，SKILL 提供最佳體驗，Hook 提供安全網

---

版本紀錄在同目錄的 `CHANGELOG.md`。
