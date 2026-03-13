---
name: spec-test
description: >
  测试计划撰写与测试执行。由角色 spec-tester 调用。
  触发条件：(1) Spec 创建阶段，spec-tester 需要撰写 test-plan.md，
  (2) 实现阶段完成后，spec-tester 需要执行测试并产出 test-report.md，
  (3) spec-debugger 修复 bug 后，spec-tester 需要重新验证。
---

# Spec Test

## 核心原则

1. **两个阶段，两个产出**：Spec 创建阶段 → test-plan.md；测试执行阶段 → test-report.md
2. **不直接修复 bug**：发现 bug 时通知 spec-debugger，等修复后重新验证
3. **与 spec-writer 协作**：Spec 阶段需讨论接口边界和异常情况，确保测试覆盖完整

## 阶段一：撰写测试计划（Spec 创建阶段）

### 步骤 1：读取探索报告

读取同目录下的 `exploration-report.md`，了解：
- 现有代码结构和接口
- 历史经验和已知的边界情况
- 外部依赖和限制条件

### 步骤 2：与 spec-writer 协作讨论

通过 SendMessage 与 spec-writer 讨论：
- 接口设计（参数类型、返回值、异常情况）
- 验收边界（何时算通过、何时算失败）
- 边界条件（空值、极端输入、并发场景）

### 步骤 3：撰写 test-plan.md

在 plan.md 同目录下创建 `test-plan.md`：

```yaml
---
title: 测试计划
type: test-plan
status: 未确认
created: YYYY-MM-DD
plan: "[[plan]]"
tags:
  - spec
  - test-plan
---
```

**必须包含的章节**：

```markdown
# 测试计划

## 验收标准
[通过/不通过的判定标准，要具体可衡量]

## 测试用例

| 用例编号 | 描述 | 输入 | 预期输出 | 边界条件 |
|---------|------|------|---------|---------|
| TC-001 | [描述] | [输入] | [预期] | [边界] |

## 覆盖率要求
- 代码覆盖率：> 80%
- 功能覆盖率：[具体要求]

## 测试环境要求
[依赖、配置、数据准备]
```

### 步骤 4：通知 TeamLead 完成

```python
SendMessage(recipient="TeamLead", content="test-plan.md 已完成，等待用户确认")
```

---

## 阶段二：执行测试（测试执行阶段）

### 步骤 1：读取必要文档

- `plan.md`：了解设计方案
- `test-plan.md`：测试用例和验收标准
- `summary.md`：了解实现细节

### 步骤 2：执行测试用例

按 test-plan.md 的用例逐一执行，记录结果。

### 步骤 3：发现 Bug 时的处理

> [!important] 不直接修复，通知 spec-debugger

```python
SendMessage(
    recipient="spec-debugger",
    content="""发现 bug：
    现象：[错误描述]
    复现步骤：[步骤]
    预期：[期望行为]
    实际：[实际行为]
    相关测试用例：TC-XXX
    """
)
```

等待 spec-debugger 修复完成后，重新执行相关测试用例。

### 步骤 4：记录微小修改

测试过程中如有微小调整（非 bug，如参数调优、配置修正）：
- 直接记录到 test-report.md 的「修改记录」表
- 不创建 debug 文档

### 步骤 5：产出 test-report.md

在同目录下创建 `test-report.md`：

```yaml
---
title: 测试报告
type: test-report
status: 未确认
created: YYYY-MM-DD
plan: "[[plan]]"
test-plan: "[[test-plan]]"
tags:
  - spec
  - test-report
---
```

**必须包含的章节**：

```markdown
# 测试报告

## 测试概况
- 测试用例总数：X
- 通过：X
- 失败：X（已修复：X）
- 代码覆盖率：X%

## 测试过程中的修改记录

| 修改类型 | 描述 | 关联文档 |
|---------|------|---------|
| 微小调整 | [直接描述] | — |
| Bug 修复 | [问题现象简述] | [[debug-001\|debug-001]] |

## 发现的 Bug（如有）
- [[debug-001|Bug 标题]] - 已修复 ✅

## 最终测试结果
[通过/不通过，结论]

## 文档关联
- 设计文档: [[plan|设计方案]]
- 测试计划: [[test-plan|测试计划]]
```

### 步骤 6：通知 TeamLead 完成

```python
SendMessage(recipient="TeamLead", content="test-report.md 已完成，等待用户确认")
```

## 与其他角色的协作

```
阶段二：spec-explorer → (exploration-report.md) → spec-tester
        spec-writer ↔ spec-tester（接口讨论）

阶段四：spec-executor → (summary.md) → spec-tester 执行测试
        spec-tester ↔ spec-debugger（bug 修复闭环）
           发现 bug → SendMessage → spec-debugger 修复
           修复完成 → SendMessage → spec-tester 重新验证
```

## 后续动作

阶段一完成后确认：
1. test-plan.md 已在 plan.md 同目录下创建
2. 已与 spec-writer 讨论并对齐接口边界
3. 已通知 TeamLead

阶段二完成后确认：
1. test-report.md 已创建，包含所有测试结果
2. 所有发现的 bug 都已由 spec-debugger 修复并重新验证
3. 已通知 TeamLead

### 常见陷阱
- 直接修复 bug 而不通知 spec-debugger（破坏协作闭环）
- test-plan.md 验收标准不够具体（无法判断通过/失败）
- 忘记在 test-report.md 中引用 debug 文档
