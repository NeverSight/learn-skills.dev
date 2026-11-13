---
name: sdd-plan
description: Convert an approved OpenSpec change into an executable implementation plan with dependency-aware tasks, clear scope, acceptance criteria, and test requirements.
argument-hint: "[change-name]"
disable-model-invocation: true
---

# MCTech SDD Plan

你现在处于 SDD 的实施规划阶段。

## 目标

将已经确定的 Spec 拆分为安全、可执行、可验证的 Tasks。

Change：

$ARGUMENTS

## 前置条件

开始前必须读取：

1. Proposal
2. Design
3. Spec
4. Architecture Decisions
5. 当前代码结构

如果发现 Spec 未确定：

不要自行补 Spec。

## Task 拆分原则

优先考虑依赖关系，而不是简单按照目录或文件拆分。

大型功能可以按照：

Foundation
→ Infrastructure
→ Data Model
→ Core Logic
→ API
→ Business Migration
→ Compatibility
→ Cleanup
→ Verification

进行拆分。

## 每个 Task 必须包含

### Objective

任务目标。

### Scope

允许修改的范围。

### Dependencies

前置 Task。

### Related Spec

对应哪些 Spec。

### Implementation Notes

必要的实现约束。

### Acceptance Criteria

完成条件。

### Tests

需要增加或修改的测试。

## Task 设计原则

一个 Task 应该：

- 有明确目标
- 有明确边界
- 可以独立验证
- 不依赖未定义的隐式行为

避免：

- 一个 Task 覆盖整个 Change
- 一个 Task 只修改一个无意义的小文件
- 两个 Task 同时修改同一个核心逻辑而没有依赖关系
- Task 包含 Spec 没有要求的功能

## Spec Coverage

最终必须执行：

Spec → Task

映射检查。

每个 Spec 必须至少有一个对应 Task。

如果没有：

报告 Spec Coverage Gap。

## 输出

更新 OpenSpec Change 中的 Tasks。

同时输出：

# Implementation Plan

## Task List

## Dependencies

## Spec Coverage

## Parallelizable Tasks

## Sequential Tasks

## Risks

## Verification Plan

不要修改业务代码。

## Recommended Next Step

通常：

/sdd-implement
/sdd-change 
