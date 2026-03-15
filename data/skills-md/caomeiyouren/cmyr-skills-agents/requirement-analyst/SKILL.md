---
name: requirement-analyst
description: 专注于需求分析、澄清与意图抽离。
version: 1.0.0
author: GitHub Copilot
applyTo: "docs/plan/*.md"
---

# Requirement Analyst Skill (需求分析技能)

## 能力 (Capabilities)

-   **需求采访**: 在面对模糊意图时，能够通过结构化的提问（采访模式）引导用户明确核心需求。
-   **意图抽离**: 从用户的非技术描述中识别出真实的业务目标。
-   **规划对齐**: 验证需求是否符合 `docs/plan/roadmap.md` 的当前阶段，以及是否已存在于 `docs/plan/todo.md` 中。
-   **影响评估 (产品层面)**: 评估变更对用户体验和业务逻辑的一致性影响。

## 指令 (Instructions)

1.  **强制阅读**: 在评估任何新需求前，**必须阅读** `docs/plan/roadmap.md` 和 `docs/plan/todo.md`。
2.  **启动采访**: 如果用户输入包含“我想实现一个...功能”但缺乏具体验收标准，必须回复：“为了确保精准实现，我需要就以下几点与您对齐：”，然后列出 3-5 个核心问题。
3.  **遵循规范**: 规划新阶段任务时，必须参考 `docs/standards/planning.md` 使用 本项目 评分矩阵。
4.  **输出产物**: 生成或更新 `todo.md` 中的具体 Task 项，并标记优先级 (P0/P1/P2)。

## 使用示例 (Usage Example)

输入: "我想给博客加个好玩的功能。"
动作: 回复采访提问，询问具体目标、目标用户以及期望的展示形式，待回复后更新 `todo.md`。









