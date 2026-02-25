---
name: use-store-not-props-best-practice
description: 查看给出的组件并进行修改，尽可能的不要使用props，尽可能直接从store中获取数据。
---

# 使用 Store 而非 Props 最佳实践

此最佳实践的核心原则是：

1. **查看给出的组件并进行修改**：分析现有组件的代码结构
2. **尽可能的不要使用props**：减少或避免通过 props 传递数据
3. **尽可能直接从store中获取数据**：优先使用全局状态管理库直接访问数据

## 工作原理

- 检查组件是否通过 props 接收数据
- 确认所需数据是否在全局 store 中可用
- 重构组件以直接从 store 获取数据，移除不必要的 props

## 使用方法

在重构组件时应用此原则：优先检查 store 数据可用性，然后修改组件代码以直接访问 store 而非依赖 props 传递。
