---
name: sdd-implement
description: Implement exactly one approved OpenSpec task by modifying production code, tests, and necessary configuration while staying within the task scope and latest specification.
argument-hint: "[task-id-or-task-description]"
disable-model-invocation: true
---

# MCTech SDD Implement

你现在处于 SDD 的任务实施阶段。

当前 Task：

$ARGUMENTS

## 开始前必须读取

1. 当前 OpenSpec Change
2. Proposal
3. Design
4. 最新 Spec
5. Architecture Decisions
6. 当前 Task
7. 已完成 Task
8. 当前代码状态

## 核心原则

一次只实施当前 Task。

必须：

- 遵守最新 Spec
- 遵守 Architecture Decision
- 遵守 Task Scope
- 保持已有兼容性
- 增加必要测试

## 实施步骤

### 1. Understand

确认：

- Task 要解决什么
- 对应哪些 Spec
- 修改哪些模块
- 前置 Task 是否完成

### 2. Inspect

阅读实际代码。

不要假设代码结构。

### 3. Implement

按照 Design 和 Spec 实现。

### 4. Test

增加或修改：

- Unit Test
- Integration Test
- API Test
- E2E Test

具体测试范围根据项目实际情况决定。

### 5. Validate

执行适当的：

- Unit Test
- Integration Test
- Typecheck
- Lint
- Build

不要为了通过测试而修改业务需求。
完成Task后一定要设置Task的完成状态标识

## 修改边界

允许：

- 当前 Task 涉及的业务代码
- 当前 Task 涉及的测试
- 当前 Task 明确要求的配置

禁止：

- 自行修改 Spec
- 自行修改 Architecture Decision
- 扩大 Task 范围
- 顺便重构无关代码
- 顺便实现其他 Task
- 修改 Out-of-Scope 模块

## 遇到问题

### Spec 不完整

停止并报告。

### Spec 与实际业务冲突

停止并报告。

### 需要改变架构

停止并建议：

/sdd-decide

### 需求发生变化

停止并建议：

/sdd-change

### 只是当前实现错误

可以在当前 Task 内解决。

### 需要修改其他 Task

停止并报告，不要自行扩大范围。

## 完成后输出

# Implementation Report

## Task

## Changed Files

## Implementation Summary

## Tests Added / Changed

## Tests Executed

## Build / Lint / Typecheck

## Spec Compliance

## Out-of-Scope Findings

## Remaining Issues

如果项目使用 ADR 或 OpenSpec Design 文件，设置任务完成标记

## Recommended Next Step

通常：

/sdd-verify
