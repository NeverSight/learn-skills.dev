---
name: codex-review
description: |
  跨模型對抗式審查：用 Codex 審查 Claude 的計畫或程式碼產出。
  異質模型產生真正的對抗張力，抓住同模型自審遺漏的問題。
  自動 VERDICT 迴圈（最多 3 輪），產出結構化 issues 清單。
  支援 --model 參數切換模型（預設 gpt-5.4）。

  觸發詞：/codex-review、cross-review、對抗審查
user_invocable: true
argument_hint: "[plan file path, code file path, PR#, or 'diff'] [--model <model-id>] (optional, auto-detects)"
---

# Codex Review

跨模型對抗式審查。Claude 產出 → Codex read-only 審查 → VERDICT 迴圈 → 結構化 issues 清單。

**定位**：用 Codex 審查 Claude 的產出（自動迴圈，異源對抗，預設 gpt-5.4，可 `--model` 切換）。與 plan-review / code-review 互補——那兩個是 Claude 同模型互動審查，這個是跨模型自動審查。

---

## Step 0: 偵測輸入 + 確認

### 解析參數

從 ARGUMENTS 擷取 `--model <model-id>`（如有），剩餘部分作為審查對象路徑。

- `CODEX_MODEL` = 使用者指定的 model-id，預設 `gpt-5.4`
- 範例：`/codex-review diff --model o4-mini` → 審查 diff，使用 o4-mini

### 偵測審查模式

按 ARGUMENTS（去除 `--model` 後的部分）和檔案特徵判斷：

**Plan mode**（計畫審查）：
1. ARGUMENTS 指定 `.md` 且內容含 `# Plan:` 或 `## Overview` → plan
2. `codex-plan.md`（當前目錄）存在 → plan
3. `.claude/plans/` 最新 `.md` → plan

**Code mode**（程式碼審查）：
1. ARGUMENTS 是檔案路徑（非 `.md` 計畫）→ code
2. ARGUMENTS 是 PR 編號（如 `#123`）→ `gh pr diff 123`
3. ARGUMENTS 是 `diff` 或空白 → `git diff` + `git diff --staged`

偵測後摘要審查對象（1-2 句），用 AskUserQuestion 確認模式和聚焦範圍：

- **全面審查**（預設）：所有維度
- **聚焦審查**：security / concurrency / schema / performance（選一）

### 讀取上下文

- Plan mode：讀計畫 + 計畫中提到的 Target Files（全部讀取）
- Code mode：讀變更檔案完整內容 + 被 import 的關鍵依賴

---

## Step 1: 準備 Codex Prompt

1. 產生 UUID（`uuidgen` 或 `date +%s`）供檔名用
2. 從 `references/prompt-templates.md` 載入對應 template（plan / code）
3. 將審查對象內容 + 相關原始碼 + template 組裝成完整 prompt
4. 寫入 `/tmp/codex-review-input-${ID}.md`

**Prompt 組裝結構**：
```
[Template header — 角色 + 對抗立場 + 維度]
## 審查對象
[計畫全文 or diff/code 全文]
## 相關原始碼
[Target files 內容]
## 聚焦範圍
[全面 or 指定維度]
[Template footer — VERDICT 規則 + 輸出格式]
```

---

## Step 2: VERDICT 迴圈（核心）

```
ROUND = 1
SESSION_ID = ""

while ROUND <= 3:
    if ROUND == 1:
        # 首輪：fresh exec，擷取 session ID
        codex exec --full-auto --skip-git-repo-check \
          -s read-only \
          -c model=${CODEX_MODEL} \
          -c model_reasoning_effort=high \
          -c model_reasoning_summary=concise \
          --output-last-message /tmp/codex-review-${ID}-r${ROUND}.md \
          "$(cat /tmp/codex-review-input-${ID}.md)" \
          2>&1 | tee /tmp/codex-review-${ID}-stdout.txt

        從 stdout 擷取 session ID（格式：session ID 或類似標識）
        SESSION_ID = 擷取到的 ID

    else:
        # 後續輪：嘗試 resume 保持上下文
        # 注意：resume 不支援 -o flag，需從 stdout 擷取輸出
        嘗試:
            codex exec resume ${SESSION_ID} --full-auto \
              "$(cat /tmp/codex-review-input-${ID}.md)" \
              2>&1 | tee /tmp/codex-review-${ID}-r${ROUND}.md

        如果 resume 失敗（exit code != 0 或 session 不存在）:
            # Fallback：fresh exec + Continuation template 注入上輪 context
            codex exec --full-auto --skip-git-repo-check \
              -s read-only \
              -c model=${CODEX_MODEL} \
              -c model_reasoning_effort=high \
              -c model_reasoning_summary=concise \
              --output-last-message /tmp/codex-review-${ID}-r${ROUND}.md \
              "$(cat /tmp/codex-review-input-${ID}.md)"

    讀取輸出，解析 VERDICT:
        APPROVED → break，進 Step 3
        REVISE → 見下方處理

    如果 REVISE 且 ROUND < 3:
        1. 擷取 Codex 發現的 issues
        2. Claude 撰寫修訂回應（描述如何修改，不實際改 code）
        3. 從 references/prompt-templates.md 載入 Continuation template
        4. 組裝下輪 prompt：上輪 issues + Claude 修訂回應 + 要求驗證
        5. 寫入 /tmp/codex-review-input-${ID}.md（覆蓋）

    ROUND++

如果 3 輪後仍 REVISE → 標記為「未收斂」，列出所有未解決 issues
```

**VERDICT 判定規則**（由 Codex 在 template 中執行）：
- **APPROVED** = 0 個 HIGH + 至多 1 個 MEDIUM
- **REVISE** = 任何 HIGH 或 2+ MEDIUM

**Codex exec 參數說明**：
- `-s read-only`：只讀 sandbox，Codex 不會改檔案
- `model_reasoning_effort=high`：審查不需 xhigh，省 token
- `${CODEX_MODEL}`：使用 Step 0 解析的模型（預設 `gpt-5.4`）
- Round 1 fresh exec → 擷取 session ID
- Round 2+ 嘗試 `codex exec resume` 保持跨輪上下文，失敗時 fallback 回 fresh exec + Continuation template

---

## Step 3: 整理結果

### APPROVED（第一輪即通過）

簡化輸出：

```markdown
## Codex Review: LGTM

**跨模型確認** — Codex (${CODEX_MODEL}) 未發現重大問題。

| 輪次 | VERDICT | HIGH | MEDIUM | LOW |
|------|---------|------|--------|-----|
| 1    | APPROVED | 0   | 0      | 2   |

### 低風險備註
- LOW: [描述]
```

### APPROVED（多輪後通過）或 REVISE（未收斂）

完整輸出：

```markdown
## Codex Review 摘要

| 輪次 | VERDICT | HIGH | MEDIUM | LOW |
|------|---------|------|--------|-----|
| 1    | REVISE  | 2    | 1      | 3   |
| 2    | REVISE  | 0    | 2      | 1   |
| 3    | APPROVED | 0   | 1      | 0   |

### Issues（按嚴重度排序）

#### HIGH
- **[H1] Auth bypass in /api/users** — `src/auth.ts:42`
  Round 1 發現，Round 2 已解決

#### MEDIUM
- **[M1] Missing input validation** — `src/handlers/create.ts:15`
  Round 1 發現，Round 3 降級為 LOW

#### LOW
- **[L1] Inconsistent error format** — `src/errors.ts:8`

### 建議行動
- [ ] `src/auth.ts:42` — 加入 token 驗證（H1）
- [ ] `src/handlers/create.ts:15` — 加入 zod schema 驗證（M1）
```

### 未收斂處理

如果 3 輪後仍 REVISE，在摘要表標注「未收斂」，並列出所有仍為 HIGH/MEDIUM 的 issues，建議使用者手動處理。

### 清理暫存檔

審查結束後（無論結果），清理所有暫存檔：

```bash
rm -f /tmp/codex-review-input-${ID}.md /tmp/codex-review-${ID}-r*.md /tmp/codex-review-${ID}-stdout.txt
```

---

## 與現有 skill 的關係

| Skill | 審查者 | 模式 | 用途 |
|-------|--------|------|------|
| plan-review | Claude | 互動式 | Claude 審計畫，人在迴圈 |
| code-review | Claude | 互動式 | Claude 審程式碼，人在迴圈 |
| **codex-review** | **Codex** | **自動迴圈** | **異源對抗審查** |

**建議使用順序**：
1. `/codex-plan` 生成計畫
2. `/codex-review` 跨模型審查計畫
3. 實作程式碼
4. `/codex-review diff` 跨模型審查程式碼
5. `/code-review` Claude 互動式細部審查

---

## Now Execute

使用者的審查請求見下方 `ARGUMENTS:`。從 Step 0 開始。
