---
name: git-flow-manager
description: 专注于 Git 暂存、规范化提交与变更记录管理。
version: 1.0.0
author: GitHub Copilot
applyTo: "**/*"
---

# Git Flow Manager Skill (Git 工作流管理技能)

## 能力 (Capabilities)

-   **精准暂存**: 识别应当被 `git add` 的相关文件，排除临时文件。
-   **Conventional Commits**: 生成语义明确、符合规范的提交消息。
-   **Changelog 生成**: 基于提交记录更新变更日志。
-   **冲突预警**: 识别并行任务可能产生的合并冲突。

## 指令 (Instructions)

1.  **分步提交**: 严格执行 PDTFC+ 中的两阶段提交（功能提交 + 测试提交）。
2.  **提交描述**: 必须使用中文（或用户使用的语言），描述“为什么”而不仅仅是“做了什么”。
3.  **验证先验**: 在执行提交命令前，必须确信已经执行过 `quality-guardian`。

## 使用示例 (Usage Example)

输入: "提交刚才修复的 Bug。"
动作: 生成 `fix(api): 修复文章详情页 PV 统计不准的问题` 并执行提交。









