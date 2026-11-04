---
name: wot-ui-v2
description: '回答、生成、重构、排查 wot-ui v2 相关代码时使用。关键词：wot-ui、uni-app、Vue3、wd-、ConfigProvider、useToast、useDialog、Form、Popup、theme、llms-full。适用于组件选型、API 查询、示例页面生成、主题定制、常见坑排查。'
argument-hint: '组件名、页面场景、问题描述或主题定制需求'
---

# Wot UI V2 Skill

这个 skill 用于让 Agent 在处理 wot-ui v2 相关任务时，优先采用组件库既有能力、遵守 uni-app 场景限制，并结合本仓库提供的 `wot` CLI 查询离线知识。

## 适用场景

- 用户询问某个 `wd-*` 组件的基础用法、属性、事件、插槽或样式变量。
- 需要生成或重构 `uni-app + Vue 3 + TypeScript` 的 wot-ui 页面或组件代码。
- 需要在 `ConfigProvider`、主题变量、暗黑模式、国际化、反馈类 hooks、表单等场景下给出正确做法。
- 需要排查文档中常见的 `Toast`、`Dialog`、`Popup`、`Tabs`、`Slider`、样式覆盖问题。
- 用户只是泛化地提到主题定制，但还没有明确要求按“单文件主题 SCSS + App.vue 只 `@use`”的结构生成时。

## 推荐流程

1. 先用本仓库 CLI 或 MCP 工具查组件知识。
2. 再根据项目实际安装方式决定导入路径与集成方式。
3. 优先复用现成的 `wd-*` 组件、hooks、主题变量与组合模式，不要退化成原生标签堆砌。
4. 如果问题涉及约束或坑位，再查阅 [参考知识](./references/overview.md)。
5. 如果用户明确要求生成 `src/themes/styles/{主题名}.scss` 单文件主题，并把挂载逻辑收进主题文件，优先切换到 `create-wot-ui-theme` skill。

## 查询顺序

1. `wot list` 找组件名。
2. `wot info <Component>` 看 props、events、slots、CSS 变量。
3. `wot demo <Component>` 看 demo 名称或具体 demo 代码。
4. `wot doc <Component>` 看完整 markdown 文档。
5. `wot token <Component>` 看主题变量。

## 工作规则

- 默认把 wot-ui 视为 `uni-app + Vue 3 + TypeScript` 组件库。
- 写页面时优先输出 `script setup` 风格。
- 反馈类能力如 `useToast`、`useDialog`、`useNotify`、`useImagePreview`、`useVideoPreview`，除了 hook 调用外，通常还需要页面内显式声明对应组件实例。
- 文档里经常出现 `@/uni_modules/wot-ui` 导入路径；如果用户项目采用 npm 安装，应切换成 `@wot-ui/ui`。
- 主题定制优先走 `ConfigProvider` 和 CSS 变量，不优先建议深度覆盖内部类名。
- 生成代码时尽量沿用组件库文档里的命名和交互模式，例如 `v-model:visible`、`before-confirm`、`confirm`、`change`、`custom-class`、`custom-style`。

## 参考资料

- [Wot UI V2 概览](./references/overview.md)
