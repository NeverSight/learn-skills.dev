---
name: single-responsibility
description: 单一职责原则，确保代码文件、函数、模块职责清晰单一。适用于所有代码文件。
metadata:
  type: declarative
  category: architecture-principle
  scope: generic
  role: secondary-principle
  parent_skill: architecture-governance
---

# 单一职责原则

> 每个文件、函数、模块应该只负责一个明确的功能或职责。

---

## ⚠️ 核心强制要求

### 1. 文件级别

- 文件的主要功能可以用一句话描述
- 所有函数/类都与主要功能相关

### 2. 函数级别

- 函数名清晰表达单一职责
- 内部逻辑围绕一个明确目标

### 3. 模块级别

- 按业务领域或技术层次划分
- 不存在循环依赖

---

## AI Agent 行为要求

### 创建代码时

1. 在编码前规划好职责边界
2. 如果不确定如何划分，主动与用户讨论

### 修改代码时

1. 检查当前职责划分是否合理
2. 发现问题时提供重构建议
3. 拆分前与用户确认方案

### 发现职责不清时

提供建议模板：
```
⚠️ 职责划分建议
当前问题：[描述]
建议拆分方案：[具体文件/职责]
是否执行拆分？
```

### 与 `architecture-governance` 的组合使用

- 当改动涉及分层边界、依赖方向、接口契约时，先触发 `architecture-governance`。
- 当改动核心是职责拆分、边界澄清、文件/类瘦身时，触发本 skill。
- 若两者同时出现，顺序为：
  1. `architecture-governance`（定架构边界）
  2. `single-responsibility`（做职责拆分）
  3. `architecture-governance`（复核依赖与分层）

---

## 分类标注

- 本 skill 是可独立复用的通用原则 skill。
- 在架构治理场景中，作为 `architecture-governance` 的联动子原则使用。

---

## 参考资料

- `references/file-level.md` - 文件级别职责划分详细说明
- `references/function-level.md` - 函数级别职责划分详细说明
- `references/module-level.md` - 模块级别职责划分详细说明
