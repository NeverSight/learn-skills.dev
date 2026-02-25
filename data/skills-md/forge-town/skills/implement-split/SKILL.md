---
name: implement-split
description: 基于预览文档和 Best Practice，实际拆分组件代码，生成符合规范的子组件。优先从 store 获取数据，避免 props 透传。
---

# implementSplit

此技能基于 generate-preview 生成的预览文档，结合 [use-store-not-props-best-practice](../../skills/use-store-not-props-best-practice/SKILL.md) 技能，智能拆分 React 组件为更小、可复用的子组件。

## 工作原理

1. 读取 generate-preview 生成的预览文档（.temp.json 和 .temp.md）
2. 分析组件结构和数据流，识别拆分机会
3. 应用 [use-store-not-props-best-practice](../../skills/use-store-not-props-best-practice/SKILL.md) 技能规则：
   - 检查每个子组件是否可直接从 store 获取数据
   - 移除不必要的 props 透传
   - 确保数据获取符合最佳实践
4. 生成拆分后的子组件代码，每个子组件独立且职责单一
5. 创建新的组件文件和目录结构
6. 更新主组件以使用新的子组件

## 使用方法

应用此指南进行组件拆分：

1. 确保有 generate-preview 生成的预览文档（.temp.json 和 .temp.md）
2. 应用 [use-store-not-props-best-practice](../../skills/use-store-not-props-best-practice/SKILL.md) 技能：
   - 分析预览文档中的数据流
   - 识别可从 store 获取的数据
   - 规划子组件的数据获取策略
3. 创建子组件文件，确保每个子组件直接从 store 获取所需数据
4. 更新主组件，移除透传的 props
5. 生成 index.ts 导出文件

## 输出

在组件目录下创建新的子组件文件：

- 子组件文件（.tsx）
- 更新的主组件文件
- index.ts 导出文件

## 呈现结果

拆分后的组件结构遵循：

- 数据优先从 Zustand store 获取
- 避免不必要的 props 透传
- 每个子组件职责单一

## 参考文档

- [use-store-not-props-best-practice](../../skills/use-store-not-props-best-practice/SKILL.md) - 数据获取优化技能

## 故障排除

- 确保预览文档存在且格式正确
- 检查 Best Practice 文档是否可访问
- 验证 store 配置正确
- 如果拆分失败，检查组件复杂度是否过高
