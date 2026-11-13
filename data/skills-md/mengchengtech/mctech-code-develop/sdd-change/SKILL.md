---
name: sdd-change
description: Safely handle requirement, behavioral, specification, design, or architecture changes after an OpenSpec change has already been planned or partially implemented. Analyze impact before updating the approved specification and tasks.
argument-hint: "[change-request]"
disable-model-invocation: true
---

# MCTech SDD Change

你现在处于 SDD 的变更管理阶段。

新的变化：

$ARGUMENTS

## 目标

在不破坏已经完成工作的情况下，安全处理需求或 Spec 变化。

## 重要原则

需求变化 ≠ 实现 Bug。

如果只是代码没有按照 Spec 实现：

/sdd-fix

只有以下情况进入本 Skill：

- 新业务需求
- 业务规则变化
- Spec 变化
- API 行为变化
- Design 变化
- Architecture 变化

## Phase 1：Impact Analysis

必须分析：

### Proposal

变化是否改变原始目标？

### Design

是否改变：

- 架构
- 模块职责
- 数据流
- 调用关系

### Spec

哪些 Spec 需要修改？

### Tasks

分别判断：

- 已完成 Task
- 正在执行 Task
- 未执行 Task

### Code

检查已经产生的代码变化。

### Tests

检查已有测试是否仍然有效。

### Data

检查：

- Schema
- Migration
- 数据兼容性

### API

检查：

- Request
- Response
- Status
- Backward Compatibility

### Cache

检查缓存行为。

### Migration / Rollback

检查迁移和回滚影响。

## Phase 2：Change Classification

将变化分类：

- IMPLEMENTATION_CHANGE
- SPEC_CHANGE
- DESIGN_CHANGE
- ARCHITECTURE_CHANGE
- NEW_REQUIREMENT
- TASK_CHANGE
- OUT_OF_SCOPE

## Phase 3：更新 OpenSpec

根据影响分析更新：

1. Proposal
2. Design
3. Spec
4. Tasks
5. Dependencies

不得直接修改业务代码。

## 已完成 Task

如果需求变化影响已经完成的 Task，必须明确：

Task
→ 旧行为
→ 新行为
→ 影响
→ 补偿 Task

不得简单删除历史 Task。

可以新增补偿任务，例如：

Task X.1
Task X.2

作为补偿任务。

## 正在执行 Task

如果当前 Task 已经无法按照新 Spec 继续：

停止继续实现。

重新调整 Task 后再执行。

## 未执行 Task

可以：

- 修改
- 合并
- 拆分
- 删除
- 增加

但必须说明原因。

## 架构变化

如果变化涉及重大架构调整：

不要自行确定最终方案。

先进入：

/sdd-decide

## 输出格式

使用下面yaml代码片断内的格式输出，输出时不含包表示yaml代码块的前后标记，禁止以代码片段方式输出

```yaml
# Change Impact Report

## 1. Change Request

## 2. Classification

## 3. Proposal Impact

## 4. Design Impact

## 5. Spec Impact

## 6. Completed Task Impact

## 7. Current Task Impact

## 8. Pending Task Impact

## 9. Code Impact

## 10. Test Impact

## 11. Data / Migration Impact

## 12. API Impact

## 13. Cache Impact

## 14. Rollback Impact

## 15. Updated OpenSpec

## 16. New Tasks

## 17. Modified Tasks

## 18. Obsolete Tasks

## 19. Decision Required
```

## 强制要求

1. 避免输出结果中包含有岐异的描述
2. 重要信息不要使用精简话语，避免省略太多有效信息导致理解错误
3. 如果是新生成的 ADR 或 OpenSpec 变更，不要立即生成 OpenSpec 文件
4. 需要人工决策的内容详细展开说明

### 严格禁止

不得：

- 直接修改业务代码
- 偷偷修改 Spec
- 删除旧决策
- 把需求变化伪装成 Bug Fix
- 为了方便或减少工作量而降低需求
- 自动重新执行整个 Change
- 修改业务代码
- 执行实现 Task
- 自行改变架构决策
- 将推测写成 MUST

## Next Action

### 通常情况

可能的下一步：

/sdd-decide
/sdd-plan
/sdd-implement
/sdd-verify

### 特殊情况

#### 1. 如果是新生成的 ADR 或 OpenSpec 变更

可能的一下步：

/sdd-spec
