---
name: generate-preview
description: 输入一个 React 组件，输出结构化描述的 .json 和可视化目录树的 .md 预览文档。用于组件拆分前的预览分析。
---

# generatePreview

此技能基于 skeleton 工具，分析 React 组件的结构，生成结构化描述的 JSON 文件和可视化目录树的 Markdown 文档，作为组件智能拆分的预览阶段。

**重要**：此技能仅做结构提取，不涉及业务逻辑判断或拆分决策。

## 工作原理

1. 使用 skeleton 工具解析输入的 .tsx 文件
2. 提取组件的 AST（抽象语法树）结构信息
3. 分析组件的子组件、props、状态、hooks 调用
4. 生成结构化 JSON 描述（遵循 FORMAT.md 规范）
5. 生成可视化 Markdown 目录树
6. 输出临时文件（强制使用 .temp. 中缀）

## 使用方法

输入 React 组件文件路径，技能将自动分析组件结构并生成预览文档。

**输入参数：**

- `component-path` - React 组件文件路径（.tsx）

**处理流程：**

1. 解析组件的 AST 结构
2. 提取子组件、props、状态等信息
3. 生成结构化 JSON 和可视化 Markdown
4. 保存为 .temp. 中缀文件

**示例输出：**
对于 `src/components/UserProfile.tsx`，生成：

- `src/components/UserProfile.temp.json`
- `src/components/UserProfile.temp.md`

## 输出

生成两个临时文件在组件所在目录：

- `{ComponentName}.temp.json`：结构化描述（供 AI 解析）
- `{ComponentName}.temp.md`：可视化目录树（供人阅读）

**文件命名规范**：

- 必须使用 `.temp.` 中缀，例如 `UserProfile.temp.json`
- 目的：明确标识为 AI 中间产物，避免与源码混淆
- 禁止使用其他命名方式

## 呈现结果

### JSON 文件包含：

- 组件名称和路径
- 子组件列表及其依赖关系
- Props 结构和类型
- 状态信息和 hooks 调用
- 复杂度评估
- 初步拆分建议（基于结构分析）

### Markdown 文件包含：

- 目录树结构可视化
- 组件关系图（文本形式）
- 结构复杂度指标
- 拆分建议提示

## 故障排除

- 确保输入文件是有效的 .tsx 文件
- 检查 skeleton 工具是否正确安装
- 验证输出目录有写入权限
- 如果解析失败，检查组件语法是否正确

## 参考文档

- [REQUIREMENTS.md](references/REQUIREMENTS.md) - 拆分要求和原则
- [FORMAT.md](references/FORMAT.md) - JSON 格式规范
- [EXAMPLES.md](references/EXAMPLES.md) - 实际拆分示例
