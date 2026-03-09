---
name: pr
description: 總結當前工作、commit、推送並建立或更新 PR。自動將對話脈絡寫入 PR description，確保 reviewer 能快速理解背景。
allowed-tools: Bash, Read, Glob, Grep, Edit, Write, Task, AskUserQuestion
argument-hint: [PR 號碼或留空建立新 PR]
---

# /pr — 總結工作並維護 PR

請依照以下步驟執行：

> **ECC 資源感知：** 若有可用的 code-reviewer 或 security-reviewer agent，Step 2 可委派更深度審查。

## Step 1: 分析當前工作

### 1a. Git 分析

1. 執行 `git status` 和 `git diff`（staged + unstaged）了解**未 commit 的變更**
2. 執行 `git log` 查看近期 commit 風格
3. **關鍵步驟 — 確認 PR 完整範圍：**
   - 執行 `git log --oneline <base-branch>..HEAD` 查看 PR 包含的**所有 commits**
   - 執行 `gh pr diff <PR-number> --name-only` 查看 PR 涉及的**所有檔案**
   - 如果已有 open PR，執行 `gh pr view <PR-number> --json body` 讀取現有 description

### 1b. 對話脈絡分析

**回顧本次對話的完整內容**，提取以下資訊：

- **動機**：使用者最初提出的問題或需求是什麼？
- **討論過程**：過程中探索了哪些方案？做了哪些比較或調查？
- **決策點**：哪些地方有多個選擇？最終為什麼選擇這個方案？
- **放棄的嘗試**：有沒有試過但放棄的做法？為什麼放棄？
- **隱含知識**：對話中出現但不會反映在 diff 裡的重要 context（例如：調查數據、外部工具比較、效能考量）
- **業界/學術依據**：技術決策是否有引用業界標準（RFC、OWASP 等）或學術研究？方案是否基於標準化解決方案？

> ⚠️ **常見錯誤**：
> - 只看 `git diff` 會遺漏 PR 中其他 commits 的內容
> - **只看 diff 不看對話**會遺漏「為什麼這樣做」的決策脈絡
> - PR description 必須同時反映 **what changed（diff）** 和 **why it changed（對話 context）**

### 1c. 總結

綜合 git 分析 + 對話脈絡，總結本次工作的**目的、做了什麼、為什麼這樣做**。

## Step 2: Quick Review

對所有變更進行快速 code review，檢查以下項目：

### 檢查清單

- **安全性**：是否有敏感資訊外洩（API keys、secrets、.env 內容）
- **正確性**：邏輯是否正確、有無明顯 bug
- **遺漏**：是否有 debug code（console.log、debugger）未清除
- **型別**：TypeScript 型別是否正確、有無 `any` 濫用
- **樣式**：是否符合專案既有 coding style

### 輸出格式

用簡潔的表格或清單呈現 review 結果：
- ✅ 沒問題的項目一句帶過
- ⚠️ 有疑慮但不阻擋的項目說明原因
- ❌ 必須修正的問題列出檔案和行號

### 互動確認

Review 完成後，使用 AskUserQuestion 詢問使用者：

- **繼續 PR 流程**：review 結果沒問題，繼續 commit → push → PR
- **先修正問題**：先處理 review 發現的問題，修完再重新執行 `/pr`

如果使用者選擇「先修正問題」，則根據 review 結果逐一修正，修正完後重新從 Step 1 開始。

## Step 3: Commit 當前變更

1. 如果有未 commit 的變更，根據變更內容撰寫 commit message
2. 使用 conventional commits 格式（feat / fix / chore / refactor / test / docs）
3. commit message 使用英文
4. 確保不要 commit 敏感檔案（.env, credentials 等）

## Step 4: 推送到遠端

1. 確認當前 branch 是否有對應的 remote tracking branch
2. 如果沒有，使用 `git push -u origin <branch>` 推送
3. 如果有，使用 `git push` 推送

## Step 5: 建立或更新 PR

### Base Branch 防護（強制執行）

**PR 的 base branch 禁止直接指向主要的 production branch（如 `master`、`main`）。**

執行以下檢查：

1. 讀取專案的 branch 策略（如果有 `skills/git-workflow/SKILL.md` 或類似文件）
2. 如果專案有定義預設的 base branch（如 `hotfix`、`develop`），自動使用該 branch
3. 如果使用者明確要求指向 `master` 或 `main` → **必須中斷並警告**：
   - 使用 AskUserQuestion 提醒：「依照專案規範，PR 不建議直接指向 master/main。確定要繼續嗎？」
   - 提供選項：「改為 [專案預設 base branch]（推薦）」/「我確定要指向 master/main」
   - 只有使用者明確確認後才能繼續
4. 如果專案沒有特別的 branch 策略，使用 repo 的 default branch

```bash
# 範例：專案規範 base branch 為 hotfix
gh pr create --base hotfix ...

# 禁止（除非使用者明確確認）
gh pr create --base master ...
```

### 判斷邏輯

- 如果提供了 PR 號碼（`$ARGUMENTS`），更新該 PR
- 如果沒有提供號碼，檢查當前 branch 是否已有 open PR
  - 有 → 更新該 PR description
  - 沒有 → 建立新 PR（使用專案規範的 base branch）

### PR Description 格式

PR description 必須包含以下區塊，使用繁體中文撰寫：

```markdown
## Summary

<!-- 1-3 句話說明這個 PR 的目的和背景脈絡 -->
<!-- 重點：讓 reviewer 30 秒內理解「為什麼要做這件事」 -->

## Context（對話脈絡）

<!-- 這是最重要的區塊 — 從對話中提取 reviewer 需要知道的 context -->
<!-- 來源：Step 1b 的對話脈絡分析結果 -->
<!--
必須包含：
- 使用者的原始需求（不只是最終實作，而是「為什麼要做這件事」）
- 過程中的調查/比較（例如：比較了 3 個框架，選了 X 因為 Y）
- 關鍵決策點和取捨（例如：選擇性採用而非全面導入，因為...）
- 放棄的方案和原因（例如：考慮過 Semcheck 但太早期）
- 不會出現在 diff 中的重要數據（例如：審計發現 145+ 檔案使用 Bootstrap）
- 技術方案的業界/學術依據（例如：採用 OAuth 2.0 因為 RFC 6749、選擇 bcrypt 因為 OWASP 建議）
-->
<!-- 目標：reviewer 不需要問「為什麼這樣做？」就能從這裡找到答案 -->

## Changes

<!-- 按主題分類列出變更，涵蓋 PR 的所有 commits（不只是當次對話的工作） -->
<!-- 用 git log <base-branch>..HEAD 確認完整範圍 -->
<!-- 用 git diff <base-branch>..HEAD --diff-filter=D --name-only 確認刪除的檔案 -->
<!-- 每個主題明確標示：新增了什麼、刪除了什麼、修改了什麼 -->

## Test plan

<!-- 測試計畫，checkbox 格式 -->

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### Context 區塊撰寫要點

**資訊來源（按優先順序）：**

1. **對話脈絡**（Step 1b）— 使用者的原始意圖、討論過程、決策理由
2. **Git diff** — 實際變更了什麼
3. **Commit messages** — 每個 commit 的目的

**必須包含：**

- 觸發這次工作的原因（bug report、feature request、tech debt）
- 過程中的調查和比較結果（數據、框架比較、技術評估）
- 做過但放棄的嘗試（如果有的話），以及放棄的原因
- 關鍵決策點（為什麼選 A 不選 B）
- 最終方案的設計考量
- 不會出現在 diff 中但 reviewer 需要知道的 context

**常見遺漏（從對話中提取，diff 看不到的）：**

- 「調查了 4 個框架，根據 GitHub stars 和功能比較選了 X」
- 「審計發現 145+ 個檔案受影響，所以分 4 個 phase」
- 「考慮過全面導入但太重，改為選擇性採用」
- 「這個工具只有 111 stars，太早期所以自己寫」

**目標：** reviewer 不需要問「為什麼這樣做？」就能從 PR description 找到答案

## Step 6: 確認結果

1. 輸出 PR URL
2. 確認 PR description 已更新
3. 如果有相關的其他 PR（如 feature → develop、develop → master），檢查是否需要同步更新

### 使用方式

/pr # 自動偵測是否有 open PR，沒有就建新的
/pr 7195 # 更新指定 PR 的 description
