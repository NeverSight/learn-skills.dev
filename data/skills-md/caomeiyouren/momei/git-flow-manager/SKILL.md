---
name: git-flow-manager
description: 专注于 Git 暂存、规范化提交与变更记录管理。
version: 1.0.0
author: GitHub Copilot
applyTo: "**/*"
---

# Git Flow Manager Skill (Git 工作流管理技能)

## 能力 (Capabilities)

-   **多分支并行管理**: 熟练操作 `master` (发布/管理开发), `dev` (并行开发/Fix/Docs) 和 `test` (测试/质量检查) 分支。
-   **工作空间维护**: 深度集成 `git worktree` 管理多个物理工作目录；使用 `git stash` 暂存未完成的代码。
-   **同步协作**: 拉取、推送与变基 (`git pull`, `git push`, `git rebase`, `git fetch`)。
-   **合并与冲突**: 处理代码合并 (`git merge`) 并辅助解决冲突。
-   **历史审查**: 使用 `git log`, `git show`, `git diff` 审查变更历史。

## 指令 (Instructions)

1.  **Worktree 优先**: 处理不同维度的任务（如开发 vs 测试）时，应优先检查并使用对应的 Git Worktree（如 `../momei-dev`, `../momei-test`）。
2.  **原子操作**: 在执行推送 (`push`) 前，必须确保本地代码已与远程分支同步 (`pull --rebase`)。
3.  **环境清理**: 任务完成后，及时使用 `git worktree remove` 移除临时工作树，并执行 `git worktree prune` 清理残留元数据。
4.  **上下文保护**: 当需要处理紧急任务、修复 Bug 或检查 PR 时，若对应 Worktree 不可用，优先使用 `git worktree add` 创建新现场。

## 规范 (Conventions)
-   **分支角色**: 遵循 [Git 工作流规范](../../../docs/standards/git.md) 定义的分支职责：
    -   `master`: 发布、合并。项目管理员可直接进行功能开发。
    -   `dev`: 并行开发、PR 合并审查、新需求探索、问题修复（Fix）及文档维护。
    -   `test`: 自动化测试编写、集成测试、代码质量检查与修复。
-   **工作树路径**: 统一使用 `../momei-[branch]` 格式的同级目录。
-   **清理规范**: 定期清理不再需要的工作树，保持开发环境整洁。
-   **暂存管理**: 切换分支或工作树前，确保当前改动已提交或 `stash`。
-   **安全性**: 严禁在 `master` 分支执行可能会破坏稳定性的非原子化修改。禁止在未授权时执行 `force push`。
-   **格式规范**: 提交信息应遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范，确保清晰的变更记录。
-   **提交语言**：提交信息应该使用用户的语言习惯，并参考 `git log` 输出的历史记录格式，保持一致性。
-   **协作流程**: 在进行 PR 合并前，确保所有相关工作树已同步最新代码，并通过必要的测试验证。


## 使用示例 (Usage Example)

输入: "我需要去 dev 分支开发新功能。"
动作: 检查 `../momei-dev` 目录，若不存在则执行 `git worktree add ../momei-dev dev`，随后在对应目录工作。

输入: "清理所有没用的工作树。"
动作: 执行 `git worktree prune` 随后根据需要 `rm` 或 `git worktree remove` 对应目录。
