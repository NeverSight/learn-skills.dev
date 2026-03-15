---
name: kwc-vue-development
description: 本项目的前端开发专家。负责处理所有代码编写、组件修改、页面构建及咨询任务。在处理相关任务前，**请先检查本 Skill 是否已加载**；若尚未加载，则**必须**优先调用。本 Skill 内置了项目特定的环境检测逻辑，会自动识别 KWC Vue 架构（检查 .kd 目录等）并应用强制性的开发规范（即本 Skill 目录下的 rule.md）。无论用户问题是否包含特定关键词，只要涉及代码开发，都应确保此 Skill 处于激活状态以保证合规。
---

# KWC Vue 开发专家

本 Skill 是 KWC Vue 项目开发的**入口与总指挥**。基于 **Vue 3** (Composition API + `<script setup>`) 进行开发。

## 核心职责
你负责指导用户进行 KWC Vue 组件的开发、修改和维护。
**重要**：你必须严格遵守**本 Skill 目录下的** `rule.md` 文件中定义的硬性约束。在开始任何代码编写前，请务必阅读并理解这些规则。

## 1. 环境上下文确认
- **项目根目录**：包含 `.kd` 文件夹和 `app/kwc` 目录。
- **配置环境**：`.kd/config.json` 中 `framework` 为 `vue`。
- **重要**：若当前环境**不满足**上述条件，**必须立即停止**使用本 Skill 的所有约束，转而按**通用 Vue Web 项目**标准协助用户。

## 2. Vue 3 开发基础

本项目基于 **Vue 3**，必须遵循以下基本原则：

- **Composition API**：统一使用 `<script setup>` 语法，**禁止**使用 Options API（`export default { data(), methods, computed, watch }`）
- **响应式**：使用 `ref()` / `reactive()` 声明响应式状态，**禁止**使用 `this`。向 Web Components 传递复杂数据（对象/数组）时，由于底层需检测引用变化，**绝对禁止** `push` 或 `splice` 原地修改，必须通过重新赋值（如 `data.value = [...data.value, new]`）产生新引用来触发渲染。
- **生命周期**：使用 `onMounted()` / `onUnmounted()` 等 Composition API 钩子
- **模板语法**：
  - 属性绑定：`:prop="value"`
  - 事件绑定：`@sl-change="handler"`（Shoelace 组件使用 `@sl-*` 前缀）
  - **向 Web Component 传递对象/数组属性：必须用 camelCase + `.prop` 修饰符**：
    ```html
    【✅ 正确】 <sl-table :dataSource.prop="rows" :columns.prop="cols" :rowSelection.prop="sel"></sl-table>
    【❌ 错误】 <sl-table :data-source="rows" :row-selection="sel"></sl-table>
    ```
  - 数字类型属性使用 camelCase 不需 `.prop`（如 `:pageSize="20"`）；**字符串/布尔属性必须用 camelCase**（如 `rowKey="id"`、`showHeader`、`simpleMode`），**禁止** kebab-case（如 `row-key`、`show-header`）
- **TypeScript**：推荐使用 `<script setup lang="ts">`

## 3. 标准工作流 (Workflow)

1. **新建组件**：
   - **必须**使用 CLI 工具，严禁手工创建文件：
     ```bash
     kd project create [组件名] --type kwc
     ```
   - 组件命名遵循 `PascalCase`。

2. **代码实现与修改**：
   - **学习**：优先参考 `app/kwc/exampleComponent`。
   - **严格合规**：代码必须符合**本 Skill 目录下的** `rule.md` 中的所有约束（导入规范、事件绑定等）。
   - **Shoelace 集成**：涉及 Shoelace 组件时，确保从 correct path 导入。

3. **验证与交付**：
   - 按项目入口更新 `app/kwc/main*` 引用。
   - 运行 `npm run dev` 进行验证。

## 4. 关键约束摘要 (详细请见本 Skill 目录下的 rule.md)
- **导入**：`import '@kdcloudjs/shoelace/dist/components/input/input.js';`
- **模板**：使用 `<sl-input>` (kebab-case)。
- **事件**：使用 `@sl-change` 绑定。
- **CSS**：样式必须使用 Shoelace Design Token（`var(--sl-color-*)`、`var(--sl-spacing-*)`、`var(--sl-font-size-*)`、`var(--sl-border-radius-*)`），禁止硬编码 hex 色值和 px 数值。详见 `./reference/css-design-tokens.md`。

## 5. 常用资源
- **扩展组件文档**（位于本 Skill 的 `reference/` 目录下）：
  - Table: `reference/table/index.md`
  - DatePicker: `reference/datepicker/index.md`
  - TimePicker: `reference/sl-timepicker.md`
  - Pagination: `reference/sl-pagination.md`
  - **使用前必须阅读相应文档**。
- **标准组件文档**：[https://shoelace.style/](https://shoelace.style/)

## 6. 输出检查清单
提交代码前，请自查：
- [ ] 使用 Vue 3 Composition API (`<script setup>`)，未使用 Options API
- [ ] 新建组件使用了 `kd project create [组件名] --type kwc`
- [ ] 已阅读并遵守**本 Skill 目录下的** `rule.md` 中的所有约束
- [ ] 导入了所有使用的 Web Components
- [ ] 模板标签为 kebab-case
- [ ] 事件使用 `@sl-*`
- [ ] **未运行**任何 ESLint/Prettier 修复命令，并**忽略**了所有 ESLint 格式报错
