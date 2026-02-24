---
name: system-audit
description: |
  掃描 CLAUDE.md、MEMORY.md 與所有已安裝 skills，找出冗餘指令、臃腫內容、
  重疊範圍與 token 浪費。產出清理建議並互動確認執行。

  觸發詞：/system-audit、audit skills、audit claude.md、系統審核
user_invocable: true
argument_hint: "[focus: all | claude | memory | skills] (default: all)"
---

# System Audit

掃描 Claude Code 設定生態系，找出可清理或最佳化的項目。一次涵蓋 CLAUDE.md、MEMORY.md、所有 skills。

---

## Step 0: 掃描所有來源

### 讀取 CLAUDE.md

按順序讀取（每個都算 token）：

1. **全域** `~/.claude/CLAUDE.md`
2. **專案** `CLAUDE.md`（當前目錄）
3. **專案私有** `.claude/CLAUDE.md`（如存在）

### 讀取 MEMORY.md

1. **Auto Memory** — 專案級 `.claude/projects/*/memory/MEMORY.md`
2. 該目錄下的所有 `.md` 附屬檔案

### 掃描 Skills

1. **全域 skills** — `~/.claude/skills/*/SKILL.md`（含 references/ 子目錄）
2. **專案 skills** — 當前目錄下任何含 `SKILL.md` 的子目錄

對每個 skill 記錄：
- SKILL.md 行數
- references/ 檔案數與總行數
- 預估 token 數（行數 × 4 粗估）

### ARGUMENTS 過濾

如果 ARGUMENTS 指定了 focus（`claude` / `memory` / `skills`），只執行對應段落。預設 `all`。

---

## Step 1: CLAUDE.md 審查

逐檔分析，找出以下問題：

### 1A. 冗餘指令

- 跨檔重複的指令（全域 vs 專案級說了同一件事）
- 同檔內重複表達同一規則

### 1B. 臃腫內容

- 超過 3 行的範例或解釋 → 可否壓縮？
- 歷史脈絡描述（「之前我們試過 X 但失敗」）→ 搬到 memory
- 低頻使用的指令 → 改做 skill 或 slash command

### 1C. 過時內容

- 提到已不存在的檔案、功能、或工具
- 版本號/日期看起來過時
- 與現有 codebase 矛盾的描述

### 1D. Token 估算

```
| 檔案 | 行數 | 預估 tokens | 問題數 |
|------|------|------------|--------|
| ~/.claude/CLAUDE.md | 200 | ~3,200 | 3 |
| CLAUDE.md | 50 | ~800 | 1 |
```

---

## Step 2: MEMORY.md 審查

### 2A. 過時條目

- 描述已完成/已不存在的功能
- 與現有程式碼矛盾的技術發現
- 被後續條目取代的舊記錄

### 2B. 與 CLAUDE.md 重複

- memory 和 CLAUDE.md 說同一件事 → 保留一處，刪另一處
- 判斷標準：高頻查用留 CLAUDE.md，低頻留 memory

### 2C. 組織問題

- 過長條目 → 拆到獨立 `.md` 檔
- 分類不清楚的條目 → 建議歸類
- 接近 200 行上限 → 標記需要瘦身

---

## Step 3: Skills 審查

### 3A. 總覽表

```
| Skill | SKILL.md 行 | Refs 行 | 預估 tokens | 觸發詞 |
|-------|-------------|---------|------------|--------|
| good-writing-zh | 165 | 158 | ~1,300 | /good-writing |
| humanizer-tw | 122 | 450 | ~2,300 | humanize |
| ... | | | | |
```

### 3B. 範圍重疊

掃描所有 skill 的 description + 觸發詞，找出：
- 功能重疊的 skill 對（如 good-writing-zh ↔ humanizer-tw 的邊界是否清楚？）
- 觸發詞衝突（不同 skill 回應同一關鍵字）

### 3C. Token 效率

- SKILL.md 超過 200 行 → 建議瘦身（抽到 references/）
- references/ 超過 500 行 → 是否有低頻內容可刪？
- 有沒有 skill 其實很少用，但每次載入成本很高？

### 3D. 結構問題

- 缺少 frontmatter（name / description / user_invocable）
- 缺少 argument_hint
- references/ 內有未被 SKILL.md 引用的孤立檔案

---

## Step 4: 呈現結果 + 互動執行

### 產出審查報告

```markdown
## System Audit 報告

### Token 預算概覽
| 類別 | 每次對話載入 | 按需載入 |
|------|------------|---------|
| CLAUDE.md（全域+專案） | ~4,000 | — |
| MEMORY.md | ~3,200 | — |
| Skills（平均每次觸發） | — | ~2,000 |

### 發現問題
| # | 類別 | 嚴重度 | 描述 | 建議動作 |
|---|------|--------|------|---------|
| 1 | CLAUDE.md | 高 | 重複指令 X 出現在全域和專案級 | 刪除專案級 |
| 2 | MEMORY.md | 中 | 條目 Y 已過時 | 刪除 |
| 3 | Skills | 低 | skill Z 的 refs 有孤立檔案 | 清理 |
```

### AskUserQuestion 互動

用 multiSelect 讓使用者勾選要執行哪些清理動作：

- 每個發現列為一個選項
- 標註嚴重度和預估影響（省多少 token / 行）
- 使用者確認後才動手

### 執行清理

使用者勾選的項目，逐一執行（Edit / Write）。每個動作完成後簡短回報。

---

## 審查原則

- **每次對話載入的內容越少越好** — CLAUDE.md 和 MEMORY.md 是最貴的，因為每次都載入
- **低頻內容移到 skill 或 memory** — 不是每次都用的指令不該佔 CLAUDE.md
- **Skills 之間邊界要清楚** — 重疊的 skill 浪費 token 也讓 Claude 困惑
- **過時資訊要刪** — 錯誤的記憶比沒有記憶更危險

---

## Now Execute

使用者的審查請求見下方 `ARGUMENTS:`。從 Step 0 開始。
