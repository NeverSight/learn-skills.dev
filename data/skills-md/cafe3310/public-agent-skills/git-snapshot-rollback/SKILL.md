---
name: git-snapshot-rollback
description: 在 Git 开发中，当需要放弃当前尝试并回退到某个历史提交时使用。它会自动将当前状态存档至 archive/ 分支，并在 ARCHIVE.md 中建立双向链接（来源与目标），确保开发决策流的可追溯性。适用于需要安全回退且保留失败尝试上下文的场景。
author: github/cafe3310
license: Apache-2.0
---

# Git Snapshot & Rollback

此技能通过自动化脚本确保在回退 Git 提交时，不仅保留了当前的尝试（Snapshot），还通过 `ARCHIVE.md` 构建了一个可追溯的决策链表。

## 核心工作流

### 1. 确认回退目标
- 获取用户想要回退到的目标 Commit Hash。
- 询问或总结回退的具体原因（Reason）。

### 2. 执行自动化回退脚本
- **在执行前，必须询问用户是否需要将存档分支推送到远端仓库。**
- 使用 `run_shell_command` 调用技能内置脚本：
  - 如果用户同意推送：`python3 <path_to_skill>/scripts/rollback.py <Target_Commit> "<Reason>" --push`
  - 如果用户不同意推送（默认）：`python3 <path_to_skill>/scripts/rollback.py <Target_Commit> "<Reason>"`
- **脚本将自动完成**：
    1. Commit 当前所有未提交的变更。
    2. 创建 `archive/{current_branch}/YYYY-MM-DD-HH-mm` 分支。
    3. 更新存档分支的 `ARCHIVE.md` 记录。
    4. (可选) 将存档分支推送到远端。
    5. 回到原分支并执行 `git reset --hard`。
    6. 在原分支更新 `ARCHIVE.md` 并提交回退记录。
    7. 列出当前所有领先于远程（未推送）的分支。

### 3. 结果验证
- 检查 `ARCHIVE.md` 是否已正确记录了本次回退的双向链接。
- 确认当前分支已处于目标 Commit 状态。

## 记录规范
- 关于 `ARCHIVE.md` 的具体格式，请参考 [references/log-format.md](references/log-format.md)。
- 每次回退的 Commit Message 必须包含来源存档分支的信息。

## 使用禁令
- 严禁在没有使用此技能的情况下直接执行 `git reset --hard` 来放弃大量工作。
- 不得修改或删除 `ARCHIVE.md` 中的历史记录。
