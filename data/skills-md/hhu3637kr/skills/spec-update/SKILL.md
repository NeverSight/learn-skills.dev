---
name: spec-update
description: 执行已有功能的更新迭代（单 Agent 模式）。触发条件：已完成功能的需求或设计发生变化（目录下已有 plan.md + summary.md）。负责从创建 update-xxx.md 到实现、审查的完整流程。若更新规模较大需要多角色协作，应新建 Spec 走 spec-start 流程。
---

# Spec Update

## 核心原则

1. **同目录原则**：update 文档必须放在原 plan.md 的同一目录下，禁止创建新目录
2. **不归档原则**：更新完成后不归档，保留在原目录以便后续更新
3. **编号递增**：update-001.md → update-002.md → update-003.md（三位数，不跳号）
4. **严格遵循方案**：只实现 update-xxx.md 定义的修改，不添加方案之外的内容
5. **回归测试必须通过**：新增测试 + 修改测试 + 原有功能回归测试全部通过

## 用户确认（必须执行）

在以下两个节点**必须**使用 `AskUserQuestion` 工具：

**节点 1 — 更新方案确认**（创建 update-xxx.md 后）：
```python
AskUserQuestion(
    questions=[{
        "question": "update-xxx.md 已创建完成，更新方案是否可以开始执行？",
        "header": "确认方案",
        "multiSelect": false,
        "options": [
            {
                "label": "确认，开始执行",
                "description": "更新方案正确，可以开始实现"
            },
            {
                "label": "需要修改",
                "description": "更新方案需要调整，请说明修改要求"
            }
        ]
    }]
)
```

**节点 2 — 审查报告确认**（生成 update-xxx-review.md 后）：
```python
AskUserQuestion(
    questions=[{
        "question": "update-xxx-review.md 已创建完成，审查结果是否通过？",
        "header": "确认审查",
        "multiSelect": false,
        "options": [
            {
                "label": "审查通过",
                "description": "更新实现符合要求，审查通过"
            },
            {
                "label": "需要修复",
                "description": "存在问题需要修复，请说明问题"
            }
        ]
    }]
)
```

响应处理：选择确认选项 → 继续；选择修改/修复或"Other" → 根据用户反馈调整后重新确认。

## 文档模板

- **update-xxx.md 模板**：见 [references/update-template.md](references/update-template.md)（含 frontmatter 字段说明）
- **update-xxx-summary.md 模板**：见 [references/summary-template.md](references/summary-template.md)（含 frontmatter 字段说明）

## 工作流程

1. **确认原 Spec 目录**：找到目录，确认 `plan.md` 和 `summary.md` 都存在。若缺少 summary.md，先用 spec-execute 完成原功能
2. **确定更新编号**：检查目录下已有的 `update-*.md`，确定下一个编号
3. **创建 update-xxx.md**：参照 [references/update-template.md](references/update-template.md)，在同一目录创建
4. **等待用户确认**：使用 `AskUserQuestion` 工具（节点 1）
5. **检索历史经验**：调用 `/exp-search <关键词>`
6. **创建任务清单**：根据 update-xxx.md 的"实现步骤"章节创建
7. **按方案实现更新**：严格遵循方案，不修改方案之外的代码
8. **编写/更新测试**：新增测试 + 修改测试 + 回归测试
9. **运行测试验证**：全部通过才能继续
10. **创建 update-xxx-summary.md**：参照 [references/summary-template.md](references/summary-template.md)，应用 Obsidian 格式：`[[plan|设计方案]]` 双链、`> [!success]` / `> [!warning]` Callout、`#spec/更新` 标签
11. **使用 spec-review 审查**：生成 update-xxx-review.md
12. **等待用户确认审查报告**：使用 `AskUserQuestion` 工具（节点 2），完成后不归档

## 错误处理

| 场景 | 解决方案 |
|------|----------|
| 原 Spec 目录不存在 | 确认路径；若为新功能，用 spec-write + spec-execute |
| 缺少 summary.md | 先用 spec-execute 完成原功能 |
| 回归测试失败 | 分析原因 → 修复回归代码 → 重新测试 → 全部通过后才能继续 |

## 后续动作

完成更新后：
1. 调用 `/exp-reflect` 进行经验反思
2. 如有经验沉淀，更新 summary 添加经验引用
3. **不归档**，保留在原目录
