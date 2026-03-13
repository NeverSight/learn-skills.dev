---
name: git-workflow-sop
description: Git 工作流标准操作规程，包括提交信息生成和远程仓库同步
---

# Git 工作流 SOP

## 概述

本 Skill 提供标准化的 Git 操作工作流，包括：
1. 检查 git 状态并审查变更
2. 生成合适的提交信息
3. 使用规范的信息提交变更
4. 与远程仓库同步
5. 创建可复用的 SOP 文档

## 使用场景

当需要执行 Git 操作或记录标准工作流程时，调用此 Skill 以遵循最佳实践。

## 操作步骤

### 1. 检查 Git 状态

首先，检查仓库的当前状态：
```bash
git status
```

### 2. 审查变更

查看工作目录与上次提交之间的差异：
```bash
git diff
```

### 3. 暂存变更

将所有变更添加到暂存区：
```bash
git add .
```

### 4. 生成提交信息

创建描述性的提交信息，说明做了什么变更以及为什么：
```bash
git commit -m "<描述性提交信息>"
```

**提交信息最佳实践**：
- 使用祈使句（"添加功能" 而不是 "添加了功能"）
- 第一行限制在 72 个字符以内
- 如需要，在正文中提供详细说明
- 如适用，引用相关的 issue 编号

**提交信息类型前缀**：
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

### 5. 推送到远程仓库

将本地变更同步到远程仓库：
```bash
git push origin <分支名>
```

### 6. 记录 SOP

创建文档，为后续参考和团队成员记录操作流程。

## 示例

### 示例 1：标准提交工作流

常规变更：
```bash
git status
git diff
git add .
git commit -m "docs: 更新文档并修复小问题"
git push origin main
```

### 示例 2：功能开发

带详细提交信息的功能开发：
```bash
git status
git diff
git add .
git commit -m "feat: 实现用户认证功能

- 添加登录和注册接口
- 集成数据库进行用户存储
- 包含密码哈希以确保安全
- 添加 JWT 令牌生成用于会话管理"
git push origin feature/user-auth
```

### 示例 3：Bug 修复

```bash
git status
git diff
git add .
git commit -m "fix: 修复 WebSocket 连接断开问题

- 添加心跳机制保持连接
- 增加重连逻辑
- 优化错误处理"
git push origin main
```

## 最佳实践

1. **频繁提交**：进行小而专注的提交，而不是大范围的变更
2. **描述性信息**：编写清晰的提交信息，说明"做了什么"和"为什么"
3. **一致的工作流**：每次提交都遵循相同的步骤以保持一致性
4. **远程同步**：定期推送变更以避免丢失工作
5. **文档记录**：保持 SOP 文档与当前实践同步更新

## 故障排除

### 问题：合并冲突

如果遇到合并冲突：
1. 拉取最新变更：`git pull origin main`
2. 在受影响的文件中手动解决冲突
3. 暂存已解决的文件：`git add <已解决的文件>`
4. 完成合并：`git commit`

### 问题：大文件

如果 git 因大文件而变慢：
1. 检查文件大小：`git ls-files | xargs ls -l | sort -k5 -n -r | head`
2. 考虑将大文件添加到 `.gitignore`
3. 如需要，使用 Git LFS 处理大型二进制文件

### 问题：撤销操作

- 撤销未暂存的修改：`git checkout -- <文件>`
- 撤销已暂存的文件：`git reset HEAD <文件>`
- 撤销最近一次提交（保留修改）：`git reset --soft HEAD~1`

## 常用命令参考

| 命令 | 说明 |
|------|------|
| `git log --oneline -10` | 查看最近 10 条提交历史 |
| `git diff --staged` | 查看已暂存的变更 |
| `git reset HEAD <文件>` | 取消暂存文件 |
| `git checkout -- <文件>` | 丢弃工作目录中的变更 |
| `git stash` | 临时保存当前修改 |
| `git stash pop` | 恢复临时保存的修改 |
| `git branch -a` | 查看所有分支 |
| `git remote -v` | 查看远程仓库信息 |
