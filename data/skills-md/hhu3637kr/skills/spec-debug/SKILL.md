---
name: spec-debug
description: >
  诊断并修复 Spec 执行过程中发现的问题。由角色 spec-debugger 调用。
  触发条件：(1) 角色 spec-debugger 接收到 spec-tester 的 bug 通知，
  (2) spec-executor 执行后出现 bug 或 plan.md 中未考虑到的情况，
  (3) 运行时出现问题、依赖环境或配置问题。
  不修改已确认的 plan.md，而是创建独立的诊断文档（debug-xxx.md）和修复总结（debug-xxx-fix.md）。
  修复完成后通知 spec-tester 重新验证，形成闭环。
---

# Spec Debug

## 核心原则

1. **不修改已确认的 plan.md**：通过创建 debug 文档记录问题，保持设计的可追溯性
2. **闭环协作**：接收 spec-tester 通知 → 修复 → 通知 spec-tester 重新验证
3. **用户确认诊断**：创建 debug-xxx.md 后，由 TeamLead 向用户确认诊断结果

## 协作闭环

```
spec-tester 发现 bug
    → SendMessage 通知 spec-debugger（含复现步骤）
    → spec-debugger 调用 spec-debug
    → 诊断 → debug-xxx.md
    → TeamLead 向用户确认诊断
    → 修复 → debug-xxx-fix.md
    → SendMessage 通知 spec-tester 重新验证
    → spec-tester 验证通过 → 记录到 test-report.md
```

## 工作流程

### 步骤 1：收集问题信息

从 spec-tester 的 SendMessage 中获取：
- 问题现象和复现步骤
- 预期行为 vs 实际行为
- 相关测试用例编号

读取相关文档：plan.md、summary.md、test-report.md（草稿）。

### 步骤 2：检索历史经验

```bash
/exp-search <关键词>
```

以问题关键词检索，参考历史解决方案。

### 步骤 3：复现并定位问题

尝试复现问题，使用日志、调试工具定位问题代码，确认边界条件。

### 步骤 4：分析根因

| 类型 | 说明 |
|------|------|
| 设计遗漏 | plan.md 未考虑的边界情况 |
| 实现偏差 | 实现与 plan.md 不一致 |
| 环境问题 | 依赖、配置、版本问题 |
| 集成问题 | 模块间交互问题 |

### 步骤 5：创建 debug-xxx.md 诊断文档

**命名规范**：`debug-001.md`（按发现顺序编号）

**Frontmatter**：
```yaml
---
title: 问题诊断-简述
type: debug
category: 与 plan.md 相同
status: 未确认
severity: 高/中/低
created: YYYY-MM-DD
plan: "[[plan]]"
tags:
  - spec
  - debug
---
```

**必须包含**：问题现象、复现步骤、根因分析、修复方案、与 plan.md 的关系。

详细格式见 [references/debug-template.md](references/debug-template.md)。

### 步骤 6：通知 TeamLead 等待用户确认诊断

```python
SendMessage(
    recipient="TeamLead",
    content="debug-001.md 已创建，请向用户确认诊断结果。路径：{路径}"
)
```

TeamLead 使用 AskUserQuestion 向用户确认。等待确认通过后继续修复。

### 步骤 7：执行修复

按照确认的修复方案修改代码：
- 最小化修改范围
- 不借机添加新功能
- 在代码注释中引用 debug 文档：`# 修复: debug-001.md`

### 步骤 8：创建 debug-xxx-fix.md 修复总结

**Frontmatter**：
```yaml
---
title: 修复总结-简述
type: debug-fix
category: 与 plan.md 相同
status: 未确认
created: YYYY-MM-DD
plan: "[[plan]]"
debug: "[[debug-001]]"
tags:
  - spec
  - debug-fix
---
```

**必须包含**：修改的文件、关键修改前后对比、验证结果。

### 步骤 9：通知 spec-tester 重新验证

```python
SendMessage(
    recipient="spec-tester",
    content="bug 已修复，请重新验证测试用例 TC-XXX。修复详情见 debug-001-fix.md"
)
```

## 与其他角色的协作

```
spec-tester → SendMessage → spec-debugger（本角色）
spec-debugger → 诊断 → 通知 TeamLead（用户确认）→ 修复
spec-debugger → SendMessage → spec-tester（重新验证）
```

- 不直接修改 plan.md
- 不在修复中添加新功能（使用 spec-update）
- 修复完成后必须通知 spec-tester 验证，不自行判断修复是否成功

## 后续动作

完成修复后确认：
1. debug-xxx.md 已创建且用户已确认诊断
2. debug-xxx-fix.md 已创建
3. 已通知 spec-tester 重新验证
4. 未修改 plan.md

### 常见陷阱
- 直接修改 plan.md 而不是创建 debug 文档
- 修复后未通知 spec-tester 重新验证（破坏闭环）
- 修复时引入了新功能（应使用 spec-update）
