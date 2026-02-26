---
name: finishing-a-development-branch
description: 當實現完成時，所有測試都通過並且您需要決定如何整合工作時使用 - 透過提供合併、PR 或清理的打包選項來指導開發工作的完成
---

# 完成開發分支

## 概述

通過提供清晰的選項和處理選定的工作流程來指導開發工作的完成。

**核心原則：** 驗證測試→呈現選項→執行選擇→清理。

**開始時宣佈：**“我正在使用完成開發分支技能來完成這項工作。”

## 流程

### 第 1 步：驗證測試

**在提供選項之前，請先驗證測試是否通過：**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**如果測試失敗：**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

停止。不要繼續執行步驟 2。

**如果測試通過：** 繼續執行步驟 2。

### 步驟2：確定基礎分支

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

或者問：“這個分支從主分支中分離出來 - 這是正確的嗎？”

### 第 3 步：提出選項

準確呈現這 4 個選項：

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**不要加入解釋** - 保持選項簡潔。

### 第四步：執行選擇

#### 選項 1：本地合併

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify tests on merged result
<test command>

# If tests pass
git branch -d <feature-branch>
```

然後：清理工作樹（步驟 5）

#### 選項2：全民並建立PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

然後：清理工作樹（步驟 5）

#### 選項 3：保持原樣

報告：“保留分支 <名稱>。工作樹保留在 <路徑>。”

**不要清理工作樹。 **

#### 選項 4：丟棄

**先確認：**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

等待具體確認。

如果確認：
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

然後：清理工作樹（步驟 5）

### 第 5 步：清理工作樹

**對於選項 1、2、4：**

檢查是否在工作樹中：
```bash
git worktree list | grep $(git branch --show-current)
```

如果是：
```bash
git worktree remove <worktree-path>
```

**對於選項 3：** 保留工作樹。

## 快速參考

|選項 |合併 |推|保留工作樹 |清理分行|
|--------|-------|------|---------------|----------------|
| 1.本地合併| ✓ | - | - | ✓ |
| 2.建立公關| - | ✓ | ✓ | - |
| 3. 保持原樣| - | - | ✓ | - |
| 4. 丟棄| - | - | - | ✓（力）|

## 常見錯誤

**跳過測試驗證**
- **問題：**合併損壞的碼，建立失敗的PR
- **修復：** 在提供選項之前始終驗證測試

**開放式問題**
- **問題：**“接下來我應該做什麼？” → 模棱兩可
- **修復：** 準確呈現 4 個結構化選項

**自動工作樹清理**
- **問題：** 在可能需要時刪除工作樹（選項 2、3）
- **修復：** 僅清理選項 1 和 4

**沒有確認丟棄**
- **問題：** 意外刪除工作
- **修復：** 需要輸入「丟棄」確認

## 危險信號

**絕不：**
- 繼續失敗的測試
- 合併而不驗證結果測試
- 刪除作品而不確認
- 沒有明確請求的強制推送

**總是：**
- 在提供選項之前驗證測試
- 正好給出 4 個選項
- 取得選項 4 的鍵入確認訊息
- 僅清理選項 1 和 4 的工作樹

## 一體化

**調用者：**
- **子代理驅動開發**（第 7 步）- 所有任務完成後
- **執行計劃**（步驟 5）- 所有批次完成後

**搭配：**
- **using-git-worktrees** - 透過此技能創建工作樹進行清理
