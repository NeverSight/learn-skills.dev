---
name: aile-delivery-report
description: 面向团队工作流的交付报告技能（阶段4）。生成 PR Description（引用计划/设计/验证项），并（可选）同步 Jira Story 。
---

# Aile：交付报告（aile-delivery-report）

## 概述

本技能在提交 PR 时使用，目标是让 CR/QA/PM 在一个入口完成验收：

- PR 必须引用计划与设计产物
- PR 必须声明验证项（测试/构建等）
-（可选）自动把 PR 链接回写 Jira，并流转状态


## 输出契约

PR Description 必须使用模板：`docs-templates/stage3-pr-description-template.md`。

至少包含：

- Jira Story Key + 链接
- Plan Reference：`docs/plans/{Story-Key}/analysis.md`（及可选 `design.pencil`）
- Change Summary（2-3 句）
- Verification（勾选项）

## 执行流程

1. 从 `analysis.md` 提取 Story-Key 与计划引用
2. 按模板生成 PR Description（可直接粘贴到 PR 平台）
3.（可选）若启用 Jira MCP：
   - 在 Story Comment 贴 PR 链接并 @mention 开发负责人
4. Jira状态变更时调用 `jira_update_issue` 更新对应 Story 的状态字段为 developed
