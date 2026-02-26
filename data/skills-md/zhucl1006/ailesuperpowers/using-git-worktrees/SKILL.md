---
name: using-git-worktrees
description: 在開始需要與當前工作空間隔離的功能工作時或在執行實施計劃之前使用 - 通過智能目錄選擇和安全驗證創建隔離的 git 工作樹
---

# 使用 Git 工作樹

## 概述

Git 工作樹建立共用相同儲存庫的獨立工作區，允許同時在多個分支上工作而無需切換。

**核心原則：**系統的目錄選擇+安全驗證=可靠隔離。

**開始時聲明：**“我正在使用 using-git-worktrees 技能來設置隔離的工作區。”

## 目錄選擇過程

請遵循以下優先順序：

### 1.檢查現有目錄

```bash
# Check in priority order
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

**如果找到：** 使用該目錄。如果兩者都存在，`.worktrees`獲勝。

### 2.檢查CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**若指定偏好：** 無需詢問即可使用。

### 3.詢問用戶

如果不存在目錄且沒有CLAUDE.md 首選項：

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which would you prefer?
```

## 安全驗證

### 對於項目本地目錄（.worktrees 或 worktrees）

**在建立工作樹之前必須驗證目錄是否被忽略：**

```bash
# Check if directory is ignored (respects local, global, and system gitignore)
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**如果不忽略：**

根據傑西的規則“立即修復損壞的東西”：
1. 將適當的行加入 .gitignore
2. 提交更改
3. 繼續創建工作樹

**為什麼重要：** 防止意外地將工作樹內容提交到儲存庫。

### 對於全域目錄（~/.config/superpowers/worktrees）

耗盡.gitignore 驗證 - 完全在專案之外。

## 創作步驟

### 1. 檢測項目名稱

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. 創建工作樹

```bash
# Determine full path
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# Create worktree with new branch
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. 運行專案設定

自動偵測並運行適當的設定：

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. 驗證乾淨的基線

執行測試以確保工作樹乾淨啟動：

```bash
# Examples - use project-appropriate command
npm test
cargo test
pytest
go test ./...
```

**如果測試失敗：** 報告失敗，詢問是否繼續或調查。

**如果測試通過：** 報告準備就緒。

### 5. 檢舉地點

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## 快速參考

|情況|行動|
|-----------|--------|
| `.worktrees/`存在 |使用它（驗證忽略） |
| `worktrees/`存在 |使用它（驗證忽略） |
|兩者都存在|使用`.worktrees/` |
|兩者都不存在|檢查CLAUDE.md→詢問使用者|
|目錄不被忽略 |新增到 .gitignore + 提交 |
|測試在基準期間失敗 |報告失敗+詢問|
|軟件包沒有.json/Cargo.toml |跳過依賴安裝 |

## 常見錯誤

### 跳過忽略驗證

- **問題：** 工作樹內容被跟蹤，污染 git 狀態
- **修復：**始終使用`git check-ignore`在建立專案本機工作樹之前

### 假設目錄位置

- **問題：** 造成不一致，違反專案約定
- **修復：**遵循優先：現有>CLAUDE.md>詢問

### 繼續失敗的測試

- **問題：** 無法區分新錯誤和先前存在的問題
- **修復：** 報告失敗，獲得明確的許可才能繼續

### 硬編碼設置命令

- **問題：** 使用不同工具的專案中斷
- **修復：**從項目文件中自動檢測（package.json等）

## 示例工作流程

```
You: I'm using the using-git-worktrees skill to set up an isolated workspace.

[Check .worktrees/ - exists]
[Verify ignored - git check-ignore confirms .worktrees/ is ignored]
[Create worktree: git worktree add .worktrees/auth -b feature/auth]
[Run npm install]
[Run npm test - 47 passing]

Worktree ready at /Users/jesse/myproject/.worktrees/auth
Tests passing (47 tests, 0 failures)
Ready to implement auth feature
```

## 危險信號

**絕不：**
- 建立工作樹而不驗證它是否被忽略（專案本地）
- 跳過基線測試驗證
- 不詢問就繼續失敗的測試
- 當目錄位置不明確時假定目錄位置
- 跳過CLAUDE.md檢查

**總是：**
- 遵循目錄優先： 現有 > CLAUDE.md > 詢問
- 驗證專案本地的目錄被忽略
- 自動偵測並運行專案設置
- 驗證乾淨的測試基線

## 一體化

**調用者：**
- **腦力激盪**（第 4 階段）- 當設計獲得批准並隨後實施時需要
- **子代理驅動開發** - 執行任何任務之前需要
- **執行計劃** - 執行任何任務之前需要
- 任何需要獨立工作空間的技能

**搭配：**
- **完成開發分支** - 工作完成後需要清理
