---
name: sdd-spec
description: Create or update OpenSpec proposal, design, and behavioral specifications from requirements, exploration results, and approved architecture decisions. Use before implementation to establish the authoritative expected behavior.
argument-hint: "[change-or-feature]"
disable-model-invocation: true
---

# MCTech SDD Spec

你现在处于 SDD 的规范定义阶段。

## 目标

明确系统应该如何工作，并将其形成 OpenSpec 可验证的规范。

Change / Feature：

$ARGUMENTS

## 权威顺序

本阶段按照以下优先级理解系统目标：

1. 已确认需求
2. 架构决策
3. 最新 OpenSpec

旧文档、旧代码不能覆盖最新批准的 Spec。

如果需求、决策和 Spec 冲突：

停止并报告。

不要自行选择。

## Proposal

明确：

- 背景
- 当前问题
- 目标
- 修改范围
- 非目标
- 影响范围

## Design

描述：

- 系统架构
- 模块职责
- 调用关系
- 数据流
- API
- 数据模型
- 缓存
- 消息
- 外部依赖
- 兼容性
- 迁移
- 回滚

不要把无关的实现细节塞进 Design。

## Spec

Spec 必须描述系统的可观察行为。

优先使用：

Given
When
Then

例如：

Given 用户没有 ORDER_EDIT 权限
When 用户修改订单
Then 系统必须拒绝请求

对于权限、认证、验权等安全敏感功能，必须明确：

- 允许条件
- 拒绝条件
- 边界条件
- 身份变化
- 租户变化
- 公司切换
- 缓存失效
- 越权行为
- 旧权限模型行为

## Spec 完整性检查

检查：

1. 每个需求是否有 Spec。
2. 每个关键行为是否可验证。
3. 是否存在相互冲突的 Spec。
4. 是否遗漏异常场景。
5. 是否遗漏兼容性要求。
6. 是否遗漏迁移要求。
7. 是否遗漏回滚要求。
8. 是否存在未确认的假设。

## 严格禁止

不得：

- 修改业务代码
- 执行实现 Task
- 自行改变架构决策
- 将推测写成 MUST
- 为了方便实现而降低需求约束

## 输出

生成或更新项目已有 OpenSpec Change 中对应的：

- Proposal
- Design
- Spec

并报告：

# Spec Summary

## Requirements

## Design

## Behavioral Scenarios

## Compatibility

## Migration

## Rollback

## Open Questions

## Spec Coverage

## Recommended Next Step

通常：

/sdd-plan
