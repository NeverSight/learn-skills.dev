---
name: spec-requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# 请求代码审查

派发 code-reviewer 子智能体，在问题蔓延前发现问题。

**核心原则：** 尽早审查、频繁审查。

**开始时宣布：**「我正在使用 spec-requesting-code-review 技能请求代码审查并派发审查子智能体。」

## 何时请求审查

**必须：**
- subagent-driven development 中每个任务之后
- 完成主要功能后
- 合并到 main 之前

**可选但有价值：**
- 卡住时（新视角）
- 重构前（基线检查）
- 修好复杂 bug 后

## 如何请求

**1. 获取 git SHAs：**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # 或 origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. 派发 code-reviewer 子智能体：**

使用 Task 工具，类型为 code-reviewer，填写 `references/code-reviewer.md` 中的模板

**占位符：**
- `{WHAT_WAS_IMPLEMENTED}` - 你刚实现的内容
- `{PLAN_OR_REQUIREMENTS}` - 应实现的内容
- `{BASE_SHA}` - 起始提交
- `{HEAD_SHA}` - 结束提交
- `{DESCRIPTION}` - 简要摘要

**3. 按反馈行动：**
- 立即修复 Critical 问题
- 继续前修复 Important 问题
- 将 Minor 问题记录待后处理
- 若审查者错误则反对（附理由）

## 示例

```
[刚完成 Task 2：添加验证函数]

你：先请求代码审查再继续。

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[派发 code-reviewer 子智能体]
  WHAT_WAS_IMPLEMENTED: 会话索引的验证和修复函数
  PLAN_OR_REQUIREMENTS: docs/plans/deployment-plan.md 的 Task 2
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: 添加 verifyIndex() 和 repairIndex()，含 4 种问题类型

[子智能体返回]：
  优点：架构清晰、有真实测试
  问题：
    Important：缺少进度指示
    Minor：报告间隔的魔法数字 (100)
  评估：可以继续

你：[修复进度指示]
[继续 Task 3]
```

## 与工作流集成

**Subagent-Driven Development：**
- 每个任务后审查
- 在问题累积前发现
- 在进入下一任务前修复

**Executing Plans：**
- 每批（3 个任务）后审查
- 获取反馈、应用、继续

**临时开发：**
- 合并前审查
- 卡住时审查

## 红旗

**绝不：**
- 因「太简单」跳过审查
- 忽视 Critical 问题
- 带着未修复的 Important 问题继续
- 与有效技术反馈争论

**若审查者错误：**
- 用技术推理反对
- 展示证明其有效的代码/测试
- 请求澄清

模板见：`skills/requesting-code-review/references/code-reviewer.md`
