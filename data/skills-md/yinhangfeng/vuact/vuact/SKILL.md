---
name: vuact
description: Vuact 最佳实践与集成指南，Vuact 是 Vue3 环境下的 React 运行时兼容层，核心支持在 Vue3 项目中无缝接入 React 组件生态，实现 Vue 与 React 双框架组件、事件、响应式、Context、Ref 等核心能力的双向互通。
---

# Vuact

Vuact 是 Vue3 环境下的 React 运行时兼容层，核心支持在 Vue3 项目中无缝接入 React 组件生态，实现 Vue 与 React 双框架组件、事件、响应式、Context、Ref 等核心能力的双向互通。

**核心价值**：
- 在 Vue 应用中无缝调用 React 组件
- 支持 Vue ↔ React 双向迁移
- 允许在一个应用中同时使用 Vue 和 React
- 可以用类 React 方式开发跨技术栈的组件库

## 快速开始

完整的配置与初始化流程请查看 [setup-config.md](references/setup-config.md)

## 核心能力

### 1. 组件互转

Vuact 提供两个核心函数来实现 Vue 和 React 组件的互相转换：

- **r2v (react-to-vue)**：将 React 组件转换为 Vue 组件
- **v2r (vue-to-react)**：将 Vue 组件转换为 React 组件

详细示例请参考：
- [r2v 基础](references/r2v-basic.md)
- [v2r 基础](references/v2r-basic.md)

### 2. Slots 与渲染属性

Vuact 提供了灵活的插槽与渲染属性转换机制：

- Vue 侧可以通过 slots 给 React 组件传递 children, element props 或 render props
- React 侧可以通过 slot: 前缀的属性给 Vue 组件传递 slots

详细示例请参考：
- [r2v 渲染属性与 slots](references/r2v-render-props.md)
- [v2r Slots](references/v2r-slots.md)

### 3. 事件与属性互通

Vuact 自动处理 Vue 和 React 之间的属性和事件转换：

- Vue 的 class → React 的 className
- Vue 的 style（字符串或对象）→ React 的 style（对象）
- React 的 className → Vue 的 class
- React 的 style（对象，单位less自动加px）→ Vue 的 style
- Vue 的 v-model 更新事件 → React 的 onUpdate:xxx

详细示例请参考：
- [r2v 事件回调](references/r2v-event.md)
- [v2r 事件回调](references/v2r-event.md)

### 4. Context 互通

Vuact 支持 Vue 和 React 之间的 Context 双向传递：

- Vue 侧可以通过 provideContext 给 React 组件提供 React Context
- React 侧可以通过 VueContextProvider 给 Vue 组件提供 Vue Context
- 两种框架的 Context 可以互相穿透

详细示例请参考：
- [r2v React Context](references/r2v-react-context.md)
- [r2v Vue Context](references/r2v-vue-context.md)
- [v2r React Context](references/v2r-react-context.md)
- [v2r Vue Context](references/v2r-vue-context.md)

### 5. Ref 互通

Vuact 支持 Vue 和 React 组件之间的 ref 传递：

- Vue 侧通过 ref 属性获取 React 组件的实例
- React 侧通过 ref 属性获取 Vue 组件的实例
- 函数组件通过 useImperativeHandle 暴露方法

详细示例请参考：
- [r2v 获取组件 ref](references/r2v-ref.md)
- [v2r 获取组件 ref](references/v2r-ref.md)

### 6. 在 React 组件中使用 Vue Hooks

Vuact 允许在 React 组件中直接使用 Vue 的响应式能力：

- 通过 useVueEffectScope 创建 Vue 响应式作用域
- 在该作用域内可以使用 ref、watch、computed 等 Vue Hooks
- 可以实现两种框架响应式系统的结合

详细示例请参考：
- [r2v Vue Hooks](references/r2v-vue-hooks.md)
- [r2v 混合组件](references/r2v-hybrid.md)

## 兼容性与限制

### 版本兼容性

- **React 兼容**：主要兼容 React 16-18，React 19 支持开发中
- **Vue 要求**：Vue 版本需要 >= 3.5
- **构建工具**：仅提供 ESM 版本，需使用现代构建工具

### 已知限制

由于 Vuact 本质是基于 Vue 的，存在一些局限性无法完全模拟 React：

1. **并发渲染**：Vue 采用递归渲染，无法实现 React 的并发渲染特性
2. **Commit 机制**：Vue 采用边递归渲染边修改 DOM，没有 React 的 commit 机制
   - useInsertionEffect 的调用时机与 React 不同
   - getSnapshotBeforeUpdate 的调用时机与 React 不同
3. **事件系统**：@vue/runtime-dom 无法与 react-dom 完全对齐
   - react-dom 的 SyntheticEvent 系统实现了一套与标准 web 不同的事件系统
   - react-dom 对一些原生 DOM 做了特殊处理（如 input、form 等）

## 完整示例参考

按需加载对应参考文档获取完整示例代码与详细说明。

### Vue 调用 React (r2v)

- [r2v 基础](references/r2v-basic.md) - 最基本的 Vue 调用 React 组件用法
- [r2v 事件回调](references/r2v-event.md) - Vue 与 React 组件之间的事件传递
- [r2v 混合组件](references/r2v-hybrid.md) - Vue React 混合使用，同时使用两种框架的能力
- [r2v React Context](references/r2v-react-context.md) - Vue 为 React 组件提供 React Context
- [r2v 获取组件 ref](references/r2v-ref.md) - Vue 获取 React 组件的 ref
- [r2v 渲染属性与 slots](references/r2v-render-props.md) - React 组件的 render prop 和 element prop 用法
- [r2v Vue Context](references/r2v-vue-context.md) - Vue 为 React 组件提供 Vue Context
- [r2v Vue Hooks](references/r2v-vue-hooks.md) - 在 React 组件中使用 Vue Hooks

### React 调用 Vue (v2r)

- [v2r 基础](references/v2r-basic.md) - 最基本的 React 调用 Vue 组件用法
- [v2r 事件回调](references/v2r-event.md) - React 与 Vue 组件之间的事件传递
- [v2r React Context](references/v2r-react-context.md) - React 为 Vue 组件提供 React Context
- [v2r 获取组件 ref](references/v2r-ref.md) - React 获取 Vue 组件的 ref
- [v2r Slots](references/v2r-slots.md) - React 为 Vue 组件传递 slots
- [v2r Vue Context](references/v2r-vue-context.md) - React 为 Vue 组件提供 Vue Context

### 配置与初始化

- [setup-config.md](references/setup-config.md) - 完整的配置与初始化指南，比 README 更全面
