---
name: git-rebase-workflow
description: Git Rebase 分支同步流程，用于将当前功能分支 rebase 到最新的目标分支（如 master/main），保持提交历史整洁。适用于功能分支落后于目标分支时，需要同步最新代码的场景。
---

# Git Rebase 工作流

将当前功能分支 rebase 到最新的目标分支（通常是 master/main），保持线性提交历史。

## 使用场景

- 功能分支落后于 master，需要同步最新代码
- 提交 MR/PR 前保持提交历史整洁
- 避免使用 `git merge` 产生的合并提交

## 前置检查

1. 确认当前分支状态：
   ```bash
   git branch -v
   git status
   ```

2. 确认工作区干净（无未提交的更改）

## Rebase 流程

### 1. 获取最新代码

```bash
git fetch origin <目标分支>
```

### 2. 执行 Rebase

```bash
git rebase origin/<目标分支>
```

### 3. 解决冲突（如有）

如果出现冲突，按以下步骤处理：

1. **查看冲突文件：**
   ```bash
   git status
   ```

2. **查看冲突详情：**
   ```bash
   grep -n "<<<<<<< HEAD\|=======\|>>>>>>>" <冲突文件>
   ```

3. **解决冲突策略：**
   
   - **保留目标分支版本（ours）：**
     ```bash
     git checkout --ours <文件路径>
     ```
   
   - **保留当前分支版本（theirs）：**
     ```bash
     git checkout --theirs <文件路径>
     ```
   
   - **手动编辑：** 直接修改冲突文件，删除冲突标记

4. **标记冲突已解决：**
   ```bash
   git add <文件路径>
   ```

5. **继续 rebase：**
   ```bash
   git rebase --continue
   ```

6. **如需中止 rebase：**
   ```bash
   git rebase --abort
   ```

### 4. 推送更新

```bash
git push origin <当前分支> --force-with-lease
```

> 注意：必须使用 `--force-with-lease` 安全地强制推送

## 常见问题

### 冲突解决原则

- **版本号冲突：** 通常保留较新的版本
- **API 变更：** 根据具体情况分析，询问用户意图
- **配置变更：** 评估变更影响，选择合适的版本

### 安全建议

1. rebase 前确保有备份或已推送的分支
2. 不要对公共分支（如 master）执行 rebase
3. 使用 `--force-with-lease` 而非 `--force` 推送
4. 如有不确定，先询问用户选择

## 完整示例

```bash
# 1. 检查状态
git branch -v
git status

# 2. 获取最新代码
git fetch origin master

# 3. 执行 rebase
git rebase origin/master

# 4. 解决冲突（如需要）
# - 查看冲突: git status
# - 保留 ours/theirs 或手动编辑
# - git add <文件>
# - git rebase --continue

# 5. 推送
git push origin feature-branch --force-with-lease
```
