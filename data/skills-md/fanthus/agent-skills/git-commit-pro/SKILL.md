---
name: git-commit-pro
description: Generate professional git commit messages following Conventional Commits specification. Use when user asks to commit changes or write a commit message.
---

# Git Commit Pro Instructions

当用户要求生成 commit message 或提交代码时，请严格遵守以下步骤：

## 1. 分析变更
运行 `git diff --cached` 查看暂存区的变更。如果没有暂存更改，运行 `git diff` 查看未暂存的更改。

## 2. 格式规范
生成的 Commit Message 必须符合 **Conventional Commits** 格式：
`<type>(<scope>): <subject>`

- **type** 只能是: feat, fix, docs, style, refactor, test, chore
- **scope** (可选): 指明修改的模块（例如: auth, api, ui）
- **subject**: 简短描述（50字符以内），用祈使句（例如 "Add login button" 而不是 "Added login button"）

## 3. 输出要求
- 不要解释，直接给出代码块格式的 Commit Message。
- 如果变更很复杂，请在 subject 下方空一行，添加详细的 body。

## 示例
```text
feat(auth): implement google oauth2 login

- add passport strategy
- update user schema