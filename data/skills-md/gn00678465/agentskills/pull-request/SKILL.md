---
name: pull-request
description: 協助建立、修改、查看或管理 GitHub Pull Request (PR)。自動分析分支 commits 與變更內容，產生符合規範的繁體中文 PR 標題與描述。使用時機包括：(1) 從當前分支建立新 PR、(2) 修改現有 PR 的標題、描述、審核者或標籤、(3) 檢查分支的 PR 狀態（開啟、已合併、已關閉）、(4) 需要自動彙整多個變更以產生摘要。適用於包含「建立 PR」、「create pull request」、「幫我開 PR」、「修改 PR 內容」等請求的情境。透過 GitHub CLI (gh) 執行操作。
metadata:
   version: 0.1.0
---

# GitHub Pull Request 助手

協助使用者建立或修改 GitHub Pull Request，自動分析分支 commits 並產生繁體中文 PR 標題與描述。

## 功能

- **建立 PR**：從當前分支建立 Pull Request 到目標分支
- **修改 PR**：更新現有 PR 的標題或描述
- **分析 commits**：自動彙整分支變更產生 PR 內容

## 決策流程

```
使用者請求 PR 相關操作
│
├─ 步驟 1：檢查當前分支是否有對應的 PR
│  │
│  │  gh pr view --json number,title,state 2>&1
│  │
│  ├─ 【有輸出且 state="OPEN"】→ PR 已存在
│  │  │
│  │  └─ 進入【修改 PR 流程】
│  │     - 顯示現有 PR 資訊
│  │     - 詢問使用者要修改的內容
│  │     - 執行 gh pr edit 指令
│  │
│  └─ 【無輸出或錯誤】→ PR 不存在
│     │
│     └─ 進入【建立 PR 流程】
│        - 執行前置檢查
│        - 分析 commits
│        - 產生標題與描述
│        - 執行 gh pr create 指令
│
└─ 步驟 2：執行對應流程並回報結果
```

### 檢查 PR 是否存在

```bash
# 檢查當前分支是否已有 PR
gh pr view --json number,title,state,url
```

**判斷邏輯：**

| 輸出結果 | 判斷 | 後續動作 |
|---------|------|---------|
| 返回 JSON 且 `state: "OPEN"` | PR 已存在且開啟中 | 進入修改流程 |
| 返回 JSON 且 `state: "MERGED"` | PR 已合併 | 詢問是否建立新 PR |
| 返回 JSON 且 `state: "CLOSED"` | PR 已關閉 | 詢問是否重開或建立新 PR |
| 錯誤訊息 `no pull requests found` | PR 不存在 | 進入建立流程 |

## 建立 PR 流程

### 步驟 0：前置檢查

確認當前分支已推送至遠端：

```bash
# 取得當前分支名稱
git rev-parse --abbrev-ref HEAD

# 檢查分支是否存在於遠端
git ls-remote --heads origin $(git rev-parse --abbrev-ref HEAD)
```

**若無輸出**：分支尚未推上遠端，需先執行：
```bash
git push -u origin <當前分支>
```

### 步驟 1：取得 commits 清單

取得當前分支相對於目標分支（預設 `main`）的 commits：

```bash
git --no-pager log --oneline <目標分支>..<當前分支>
```

### 步驟 2：取得 commit 詳細資訊

針對每個 commit 取得變更統計：

```bash
git --no-pager show <commit-hash> --stat
```

### 步驟 3：產生 PR 標題

根據 commit 數量決定標題策略：

| 情況 | 標題策略 |
|------|---------|
| 單一 commit | 直接使用該 commit 訊息 |
| 多個 commits | 總結所有變更的描述性標題 |

### 步驟 4：產生 PR 描述

> 完整範本請參考 `references/pr-template.md`

PR 內容應包含以下區塊：

```markdown
### 摘要
[一句話總結此 PR 的主要目的]

### 修改內容
- 變更項目 1：描述具體的修改內容
- 變更項目 2：描述具體的修改內容
- 變更項目 3：描述具體的修改內容

### ⚠️ 風險評估
[評估此 PR 是否有破壞性變更、需要特別注意的地方]

常見風險類型：
- 資料庫變更（migration、schema 修改）
- API 變更（endpoint 修改、參數變更）
- 設定檔變更（環境變數、設定參數）
- 相依性更新（套件版本升級）

若無風險，可註明：「無破壞性變更」

### 備註
[其他需要審查者注意的地方，如測試方式、部署注意事項、相關 Issue 連結等]
```

### 步驟 5：建立 Pull Request

使用 GitHub CLI 建立 PR。

**⚠️ 重要：使用 `--body-file` 避免轉義問題**

直接在命令列使用 `--body` 會導致換行符 `\n` 和其他特殊字符出現轉義問題。**建議使用檔案方式**：

```bash
# 方法 1（推薦）：將內容寫入暫存檔案
# 1. 建立暫存檔案 pr-body.md，寫入 PR 描述內容
# 2. 使用 --body-file 讀取檔案
gh pr create --base <目標分支> --head <當前分支> --title "<標題>" --body-file pr-body.md

# 3. 建立完成後刪除暫存檔案
```

**PowerShell 範例：**

```powershell
# 將 PR 描述寫入檔案
@"
### 摘要
實作使用者登入功能

### 修改內容
- 新增登入 API 端點
- 實作 JWT 驗證機制

### ⚠️ 風險評估
無破壞性變更
"@ | Out-File -FilePath pr-body.md -Encoding UTF8

# 建立 PR
gh pr create --base main --title "feat: 實作登入功能" --body-file pr-body.md

# 清理暫存檔案
Remove-Item pr-body.md
```

**Bash 範例：**

```bash
# 將 PR 描述寫入檔案
cat << 'EOF' > pr-body.md
### 摘要
實作使用者登入功能

### 修改內容
- 新增登入 API 端點
- 實作 JWT 驗證機制

### ⚠️ 風險評估
無破壞性變更
EOF

# 建立 PR
gh pr create --base main --title "feat: 實作登入功能" --body-file pr-body.md

# 清理暫存檔案
rm pr-body.md
```

**常用選項：**

| 選項 | 說明 |
|------|------|
| `--body-file <file>` | 從檔案讀取 PR 描述（推薦） |
| `--draft` | 建立草稿 PR |
| `--reviewer <users>` | 指定審核者（逗號分隔） |
| `--assignee <users>` | 指定負責人 |
| `--label <labels>` | 新增標籤 |

## 修改 PR 流程

當 PR 已存在時，進入此流程。

### 步驟 1：取得現有 PR 資訊

```bash
gh pr view --json number,title,body,state,url,headRefName,baseRefName
```

### 步驟 2：顯示 PR 摘要

向使用者顯示：
- PR 編號與標題
- 目前狀態（OPEN/DRAFT）
- 來源分支 → 目標分支
- PR 連結

### 步驟 3：確認修改內容

根據使用者需求執行對應操作：

### 修改標題

```bash
gh pr edit <PR編號或URL> --title "<新標題>"
```

### 修改描述

```bash
gh pr edit <PR編號或URL> --body "<新描述>"
```

### 新增審核者/標籤

```bash
gh pr edit <PR編號或URL> --add-reviewer <users>
gh pr edit <PR編號或URL> --add-label <labels>
```

### 查看現有 PR

```bash
# 列出當前 repo 的 PR
gh pr list

# 查看特定 PR 詳情
gh pr view <PR編號>
```

## 注意事項

- **僅處理已提交的變更**：忽略未 staged 的變更
- **語言要求**：PR 標題與描述使用**繁體中文 (zh-TW)**
- **目標分支預設**：若使用者未指定，預設為 `main`
- **需要 GitHub CLI**：確保已安裝並登入 `gh` 工具

## 範例

### 範例 1：PR 不存在 - 建立新 PR

**使用者請求：** 「幫我建立 PR 到 develop」

**執行流程：**

1. 檢查 PR：`gh pr view` → 錯誤「no pull requests found」
2. 判斷：PR 不存在，進入建立流程
3. 前置檢查：確認分支已在遠端
4. 取得 commits：`git --no-pager log --oneline develop..HEAD`
5. 分析變更產生標題與描述
6. 執行：`gh pr create --base develop --head feature/login --title "feat: 實作使用者登入功能" --body "..."`

### 範例 2：PR 已存在 - 自動進入修改模式

**使用者請求：** 「幫我開 PR」

**執行流程：**

1. 檢查 PR：`gh pr view --json number,title,state`
   ```json
   {"number": 42, "title": "feat: 新增登入功能", "state": "OPEN"}
   ```
2. 判斷：PR 已存在，進入修改流程
3. 回報：「此分支已有 PR #42『feat: 新增登入功能』，請問要進行什麼修改？」
4. 等待使用者指示

### 範例 3：明確修改 PR

**使用者請求：** 「修改 PR #42 的標題為『修正購物車計算錯誤』」

**執行：**
```bash
gh pr edit 42 --title "修正購物車計算錯誤"
```

### 範例 4：PR 已合併

**使用者請求：** 「幫我建 PR」

**執行流程：**

1. 檢查 PR：`gh pr view --json number,title,state`
   ```json
   {"number": 38, "title": "feat: 舊功能", "state": "MERGED"}
   ```
2. 判斷：PR 已合併
3. 回報：「此分支的 PR #38 已合併。若有新的變更需要建立 PR，請確認已有新的 commits。」

## 參考資料

- `references/pr-template.md` - PR 描述範本與編寫指南
- `references/gh-pr-commands.md` - GitHub CLI PR 相關指令完整參考
