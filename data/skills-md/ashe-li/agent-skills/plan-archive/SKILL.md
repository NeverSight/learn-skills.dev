---
name: plan-archive
description: 將已完成的 plan 從 plans/active/ 歸檔至 plans/completed/，補上驗證結果與完成時間。適合在實作結束後呼叫。
allowed-tools: Bash, Read, Glob, Write, Edit
argument-hint: [plan 檔名或留空自動偵測]
---

# /plan-archive — 歸檔已完成的 Plan

將 `plans/active/` 中已完成的 plan 移至 `plans/completed/`，並補上驗證結果。

> **ECC 資源感知：** 若有可用的 code-reviewer agent，可輔助驗證 plan 中的實作結果。

---

## Step 1：找出要歸檔的 Plan

如果有傳入引數（檔名或路徑），直接使用。
否則，列出 `plans/active/` 下的所有 `.md`：

```bash
ls plans/active/*.md 2>/dev/null
```

若有多個，依 mtime 排序，問使用者選哪一個。
若只有一個，直接用。
若目錄不存在或空，輸出「找不到待歸檔的 plan」並結束。

---

## Step 2：讀取 Plan 內容

讀取目標 plan 檔案，確認：
- 是否有 `## Phase` 或 `## Step` 段落（實作步驟）
- 是否有 `## 驗證` 或 `## Verification` 段落
- 是否有 `## Industry & Standards Reference` 段落

---

## Step 3：補充驗證結果

在 plan 檔案頂部（緊接 `---` frontmatter 後）加上：

```markdown
**狀態：✅ 完成（YYYY-MM-DD）**

```

再追加或更新 `## 驗證結果` 段落，填入：
- 測試通過數（若有）
- 實際執行結果（對照 plan 中的「預期」）
- 業界/學術參照落實情況 — 對照 plan 的 Industry & Standards Reference，確認各項參照是否已實際應用
- 任何偏差或補充說明

---

## Step 4：移動檔案

```bash
mkdir -p plans/completed
mv plans/active/<filename>.md plans/completed/<filename>.md
```

確認移動成功後輸出：`✅ 已歸檔：plans/completed/<filename>.md`

---

## 自動化（Hook 設定）

若希望每次 `ExitPlanMode` 後**自動**將 plan 存至 `plans/active/`，
可設定 PostToolUse hook：

### 1. 建立 hook script

`~/.claude/hooks/save-plan-on-exit.sh`：

```bash
#!/bin/bash
# PostToolUse hook for ExitPlanMode
# Reads JSON from stdin, copies plan file to project's plans/active/

INPUT=$(cat)

# Extract plan_file path from tool response
PLAN_FILE=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    # ExitPlanMode tool_response may contain the plan file path
    resp = d.get('tool_response', d)
    print(resp.get('plan_file', resp.get('planFile', '')))
except Exception:
    print('')
" 2>/dev/null)

if [ -z "$PLAN_FILE" ] || [ ! -f "$PLAN_FILE" ]; then
  exit 0
fi

# Only act if we're inside a git repo with a plans/ directory pattern
if [ ! -f "$(pwd)/.git/HEAD" ] && [ ! -d "$(pwd)/.git" ]; then
  exit 0
fi

DEST_DIR="$(pwd)/plans/active"
mkdir -p "$DEST_DIR"

SLUG=$(basename "$PLAN_FILE")
cp "$PLAN_FILE" "$DEST_DIR/$SLUG"
echo "[plan-archive] Plan saved to plans/active/$SLUG" >&2
```

```bash
chmod +x ~/.claude/hooks/save-plan-on-exit.sh
```

### 2. 設定 `~/.claude/settings.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/save-plan-on-exit.sh"
          }
        ]
      }
    ]
  }
}
```

### 3. Rule（搭配使用）

在專案 `CLAUDE.md` 加入，確保 Claude 在實作完成後主動呼叫 `/plan-archive`：

```markdown
### Commit 前知識沉澱清單

5. **歸檔 plan** — 若本次工作有對應的 plan，實作完成後執行 `/plan-archive`
   將 `plans/active/<name>.md` 移至 `plans/completed/`，補上驗證結果
```

---

## 目錄規範

```
plans/
├── active/       # 進行中（Hook 自動存入 / /plan 手動建立）
├── completed/    # 已實作完成（/plan-archive 歸檔）
└── archived/     # 長期封存（不再參考的舊 plan）
```
