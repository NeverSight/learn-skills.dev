---
name: component-scaffolder
description: 前端组件脚手架生成器。根据组件描述自动生成符合项目规范的组件代码，自动识别技术栈（React+MUI 或 Vue3+AntDesign）并生成对应模板。适用于：(1) 新建业务组件，(2) 新建共通组件，(3) 新建页面级组件。触发条件：当用户需要创建新组件时。
---

# 组件脚手架生成器

根据组件描述自动生成符合项目规范的组件代码。

## 工作流程

### 1. 技术栈识别

读取 `package.json` 自动判断，然后按对应技术栈生成代码。

### 2. 项目规范探测

在生成代码前，先探测项目的现有规范：

1. **目录结构**：扫描 `src/components/` 或 `src/pages/` 的目录组织方式
2. **命名规范**：检查现有组件是 PascalCase 目录还是 kebab-case
3. **文件组织**：单文件组件 vs 目录组件（index.tsx + styles + types）
4. **导入风格**：绝对路径（`@/components`）vs 相对路径
5. **状态管理**：Redux/Zustand/Pinia/Vuex
6. **样式方案**：CSS Modules / styled-components / Tailwind / sx prop

### 3. 信息收集

向用户确认：
- **组件名称**：英文，如 `UserTable`、`LoginForm`
- **组件类型**：
  - 页面组件（Page）
  - 业务组件（Business）
  - 共通/原子组件（Common/Atom）
- **主要功能描述**：一句话说明组件做什么
- **Props 概述**（可选）：主要输入参数

### 4. 生成代码

按技术栈选择对应模板，参见：
- React 模板：[references/react-patterns.md](references/react-patterns.md)
- Vue 3 模板：[references/vue-patterns.md](references/vue-patterns.md)

### 5. 生成内容清单

根据组件类型，生成以下文件：

| 文件 | 页面组件 | 业务组件 | 共通组件 |
|------|---------|---------|---------|
| 组件主文件 | ✅ | ✅ | ✅ |
| 类型定义 | ✅ | ✅ | ✅ |
| 样式文件（如需） | ✅ | 可选 | 可选 |
| index 导出 | ✅ | ✅ | ✅ |

## 重要原则

- **遵循项目现有规范**：探测到的规范优先于默认模板
- **最小生成**：只生成必要的文件，不过度设计
- **类型优先**：所有 props 和 state 必须有 TypeScript 类型定义
- **无业务假设**：生成骨架代码，不预设业务逻辑
