---
name: component-selection-imports
description: 指导 YSS UI 业务页面、CRUD、列表页、表单页和组件评审在编码前判定组件、Hook 与工具函数的真实导出来源；当需要在 @yss-ui/components、@yss-ui/hooks、@yss-ui/utils 与 ant-design-vue 之间选择，或需要排查虚构 Y 前缀组件、错误导入、Formily UI 边界时使用。
---

# 组件选择与导入

## 触发条件

- 生成 YSS UI 业务页面前需要判定组件、Hook 或工具函数来源。
- 出现错误 Y 前缀、导入冲突、Formily UI 跨层或者组件是否已封装不明确。

## 不适用场景

- 只修改与 UI 导入无关的纯数据逻辑。
- 组件库内部组件开发；该场景应按组件开发规范处理内部依赖。

## 判定流程

1. 当前会话可用 yss-ui MCP 时，先用 `list_components` 确认组件、Hook 或 Utils 是否真实存在，再用 `get_component_docs` 确认名称、导出包、Props、Events 和 Slots，不只看 demo 标签名。
2. `get_component_docs` 未命中时，先用 `search_docs` 和 `list_components` 校正别名与归属，不得立即判定为未封装。
3. MCP 工具不可用、调用失败或校正后仍无结果时，读取当前上下文或文档站的最新 `llms-full.txt`。
4. 必要时读取 `../yss-ui-business-page-generation/references/component-map.md`、`hooks-map.md`、`utils-map.md` 快速缩小范围；文档与当前项目依赖版本不一致时，最终以当前源码和可编译导出为准。
5. 已导出的 YSS 能力优先从 `@yss-ui/components`、`@yss-ui/hooks`、`@yss-ui/utils` 导入；确认未封装后才从 `ant-design-vue` 导入原组件。
6. 若文档与导出源码不一致，记录差异并按当前仓库可编译的导出处理，不猜测 API。

## 硬约束（禁止/必须）

- 业务层已封装组件默认从 `@yss-ui/components` 导入；可编辑表格必须优先使用 `YEditTable`，业务主表格必须优先使用 `YTable`。
- 当前公共导出包含 `YButton`、`YCard`、`YTable`、`YEditTable`、`YTree`、`YSplitPane`、`YFormily` 等；未导出 `YModal`、`YDrawer`、`YInput`、`YPopconfirm`，禁止臆造这些名称。
- 当前未封装的 `Modal`、`Drawer`、`Popconfirm`、`Input` 等从 `ant-design-vue` 导入。删除操作使用按钮附近的 `Popconfirm`，不默认使用居中 `Modal.confirm`。
- 业务层禁止导入 `@formily/antdv` 或 `@formily/antd*` UI 组件；使用 `YFormily` 提供的 Schema 与组件边界。
- 微前端子应用同样默认使用根入口具名导入；Vite 6 新模板继续采用官方插件，无插件消费的样式能力按下方版本契约判断。`lite` 是可选兼容入口，旧项目保留已验证的样式策略。
- 对于 `YMonaco`、`YEcharts`、`YSheet` 等重型依赖组件，微应用可继续从 `@yss-ui/components` 正常消费（已异步化），也可直接从官方子路径 `@yss-ui/components/monaco`、`@yss-ui/components/echarts`、`@yss-ui/components/sheet` 导入，避免未使用的重型依赖及其全量 CSS 被打包到业务页面中。
- 禁止因文档暂时不可达就把猜测的 `Y*` 组件改成 Ant Design Vue “先落地”。只能复用当前仓库已证明可用的导入，或明确报告待确认项。
- 接口错误提示由 `mutator.ts` 的响应拦截器统一处理。API Hook 不得在 `success === false` 分支或 `catch` 内重复调用 `message.error`；`message` 只用于非 API 错误的本地交互反馈或成功提示。


### 统一消费与构建契约

- 默认单包安装，从 `@yss-ui/components` 具名导入并局部注册；不全局安装 YSSUI，不拆新的功能包。
- `@yss-ui/components/table`、`@yss-ui/components/formily` 自 1.6.7 起公开，是可选入口；旧版本先核对 exports，禁止批量改写根入口。
- 子路径与插件改善加载边界，不减少默认安装依赖；VXE/Formily 仍由组件库配套安装。
- 官方 `@yss-ui/components/vite` 插件自 1.7.0 起已发布，完整验收范围为 Vite 6。旧项目先读取实际安装版本、exports 和现有插件，禁止与旧隔离插件同时运行。
- `@yss-ui/components` 自 1.7.3 起，在支持 tree-shaking 的 ESM 生产构建中，无插件根入口具名导入也会关联实际组件样式；根入口保留 Ant Design Vue reset。核对目标包的版本及 `consumption.json` 后，不因未接入插件就要求业务额外导入全量 CSS。
- 无插件显式导入 `@yss-ui/components/style.css` 或 `@yss-ui/components/dist/style.css` 仍保留全量样式；官方插件继续将这两个路径转换为基础 reset，再按组件加载样式。不得批量删除旧项目已有样式导入；CJS、默认全量安装、动态整包导入及开发预构建不套用上述生产裁剪结论。
- 生成代码前用 MCP `get_consumption_contract` 核对版本；未知版本不得假设新插件可用。文档站 Demo 的样式导入不能直接复制为业务全局样式策略。

## 标准代码骨架

```typescript
import {
  YButton,
  YCard,
  YEditTable,
  YTable,
  YTree,
  YFormily,
  type YEditTableColumn,
  type YTableColumn,
} from '@yss-ui/components';
import { useLoading, useTableHeight, useTreeHeight } from '@yss-ui/hooks';
import { copyToClipboard, formatDate } from '@yss-ui/utils';
import { Drawer, Input, Modal, Popconfirm } from 'ant-design-vue';
```

## 交付检查清单

- [ ] 每个关键导入都能在最新文档或包的 `src/index.ts` 中追溯。
- [ ] 未导出的 Y 前缀组件没有出现在业务代码中。
- [ ] 删除、表格、编辑表格和 Formily 导入边界符合项目约束。
- [ ] API Hook 中没有重复 `message.error`，异常仍由 `Promise.reject` 中断后续流程。

## 失败兜底策略

- MCP 与 `llms-full.txt` 都不可用时，用 CodeGraph/源码 `src/index.ts` 和当前项目已编译的相近页面交叉确认，不猜测导出。
- 文档与源码不一致时，优先保证当前仓库可编译，并在交付中明确标注文档差异。
