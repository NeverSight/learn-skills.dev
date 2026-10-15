---
name: yss-ui-business-page-generation
description: 指导生成或改造 Vue3 YSS UI CRUD、列表、表单、详情、左树右表和弹窗抽屉页面，覆盖组件选型、模块拆分、Orval API、响应式高度、主题和原型验收；当用户要求生成 YSS UI 业务页或 CRUD 模块时使用。
---

# YSS UI 业务页面生成 Skill

## 触发条件

- 用户要求生成或改造业务页面、CRUD 模块、列表页、表单页、详情页、左树右表、树表联动页面。
- 页面涉及 `YTable`、`YTree`、`YFormily`、`YButton`、`YCard`、`YSplitPane`、`YConditionBuilder` 等 YSS UI 组件。
- 需要让 AI 优先复用 YSS UI 组件、hooks、utils，而不是直接使用 Ant Design Vue 或重复造工具函数。
- 用户提供旧项目路径、原型截图、目标截图或要求“照旧项目/照原型还原”。

## 不适用场景

- 只修改组件库内部组件实现：使用 `../component-development/SKILL.md`。
- 只写文档、提交信息或发版流程，不生成业务页面代码。
- 用户明确要求不用 YSS UI 组件库。

## 必读参考

- 组件来源速查：`./references/component-map.md`
- Hooks 速查：`./references/hooks-map.md`
- Utils 速查：`./references/utils-map.md`
- 表格细节：`../ytable-usage/SKILL.md`
- 编辑表格细节：`../yedit-table-usage/SKILL.md`
- 树形细节：`../ytree-usage/SKILL.md`
- 表单细节：`../yss-formily/SKILL.md`
- 原型还原验收：`../prototype-page-acceptance/SKILL.md`
- 主题 Token 与换肤：`../theme-token-usage/SKILL.md`
- 文件导出下载：`../file-export-download/SKILL.md`
- Orval 接口与错误处理：`../api-integration/SKILL.md`

## 文档检索顺序

1. 当前会话可用 yss-ui MCP 时，生成业务代码前先调用一次 `get_codegen_rules`；不确定导出时用 `list_components`，配置组件/Hook/Utils 前用 `get_component_docs`，复杂场景用 `get_demo`，不确定归属时用 `search_docs`。
2. MCP 查询未命中时，先用 `list_components` 或 `search_docs` 校正名称；只有 MCP 工具不可用、调用失败或校正后仍无结果时，才读取最新 `llms-full.txt`。
3. MCP/`llms-full.txt` 与当前项目的依赖版本或导出不一致时，使用当前项目源码、CodeGraph 和可编译导出交叉核验，明确记录差异，不猜测 API。
4. 当前 Skill 已被本地加载时不得再用 `get_skill` 查询自身；仅在所需子 Skill 未同步到本地时才用 `list_skills/get_skill` 兜底。

## 硬约束（禁止/必须）

- 生成页面前必须先判定组件来源：YSS UI 已封装的组件从 `@yss-ui/components` 导入。
- 表单默认使用 `YFormily + JSON Schema`，业务代码禁止导入 `@formily/antdv` UI 组件。
- 所有 `YFormily` 横向业务表单必须显式设置固定 `labelWidth` 与 `labelAlign: 'right'`，并使用 `FormLayout -> FormGrid -> 字段` 响应式结构；禁止用 `minColumns: maxColumns` 固定列数破坏响应式。
- 标准列表/CRUD 查询区必须采用 `YCard -> search-content -> search-form(YFormily) + search-actions(YButton 查询/重置)` 的纵向布局；按钮行独占下一行并右对齐，缩放或窄屏字段换行后仍位于搜索卡片右下角。
- 查询区禁止横向放“表单 + 按钮”并用大 `gap`、`align-items: flex-start`、`padding-top` 硬调按钮位置。
- 抽屉/弹窗编辑表单默认 `labelWidth: 140`、`FormGrid { maxColumns: 2, minColumns: 1, minWidth: 320~360 }`，备注/长文本字段用 `gridSpan` 占满整行。
- 下拉选择器（`Select`/`TreeSelect`/`Radio.Group`）异步数据源必须通过 `enum` 或 `x-reactions` / `field.dataSource` 注入，严禁写入 `x-component-props.options`（会导致首次打开弹窗显示“暂无数据”、关闭再打开才展示的经典时序 Bug）；弹窗基础下拉字典优先在打开前 `await` 或页面初始化提前拉取。
- 表格默认使用 `YTable`；远程分页使用 `pageable + pagination.remote + @page-change`，事件参数固定读取 `{ current, pageSize }`，禁止使用 `currentPage`。
- 编辑表格默认使用 `YEditTable`；需求出现“编辑表格/添加行/删除行/行内下拉”时禁止直接用 `a-table` 手搓。
- 左树右表优先使用 `YSplitPane + YCard + YTree + YTable`，高度使用 `useTreeHeight/useTableHeight`。
- 标准列表必须使用 `YTable` 真实 API：`:data`、`:columns`、`:loading`、`pageable`、`v-model:pagination`、`@page-change`；禁止臆造 `request/search-params` 等 Prop。实例 `refresh()` 只刷新当前 vxe 表格数据，远程重新查询必须调用业务 Hook。
- 新增/导入/批量操作等主操作直接放入 `#toolbar-right` 插槽；**无需配置 `:toolbar-config="{ custom: true }"`**，避免无端展示列设置图标；**仅在业务明确需要列设置时才传入 `:toolbar-config="{ custom: true }"`**。
- 删除确认默认使用 `YTable actionConfig.buttons[].isConfirm` 按钮项或 AntDV `Popconfirm` 气泡确认，禁止默认使用居中 `Modal.confirm`。
- 样式抽离到 `style.less`，在 SFC 中使用 `<style scoped lang="less">@import './style.less';</style>`。
- `index.vue` 原则上不超过 150 行；状态、API、副作用和处理方法进入 `hooks/`，列定义和静态配置进入 `constant.ts`。
- 所有导出函数、hooks、类型和静态配置必须使用中文 JSDoc。
- Orval 请求必须使用真实生成导出和 DTO；禁止 `if (res?.success)` 冗余包裹，也禁止在 `else`/`catch` 重复 `message.error`。
- 页面、公共组件、内联样式、TS 渲染配置和 SVG 必须遵循 `theme-token-usage`；禁止硬编码品牌色及 hover/active/selected/focus 色阶，主色透明态必须由真实动态 Token 派生。
- 页面包含导出、报表、模板或附件下载时必须遵循 `file-export-download`，使用 `handleBlobResponse(res.data, res.headers)`，并检查生成方法是否已包含 `responseType: 'blob'`。
- **全链路国际化工厂函数规范（Critical）**：
  - 若当前项目支持或启用了多语言（存在 `locales/` 目录或依赖了 `vue-i18n`），页面开发必须全链路遵循国际化规范，**严禁在模板、`constant.ts` 或 Hook 中硬编码中文**；
  - 表格列定义统一采用 `createColumns(t)` 工厂函数，操作列采用 `createActionConfig(handlers, t)` 工厂函数；
  - 分页 `pagination` 必须绑定 `showTotal: (total: number) => t('common.total', { total })`；
  - 查询/编辑表单 Schema 采用 `createSearchSchema(t)` / `createFormSchema(t)` 工厂函数并由 `computed` 驱动；
  - 页面所有操作按钮（查询、重置、新增、批量操作等）必须使用多语言词条；
  - 业务新词条在 `locales/lang/{zh-CN,zh-TW,en-US}/` 中镜像对齐维护。
- 若用户给出旧项目路径或截图，开发前必须先提取 UI/交互验收清单；交付前逐项对照，不允许只实现字段和接口。


### 统一消费与构建契约

- 默认单包安装，从 `@yss-ui/components` 具名导入并局部注册；不全局安装 YSSUI，不拆新的功能包。
- `@yss-ui/components/table`、`@yss-ui/components/formily` 自 1.6.7 起公开，是可选入口；旧版本先核对 exports，禁止批量改写根入口。
- 子路径与插件改善加载边界，不减少默认安装依赖；VXE/Formily 仍由组件库配套安装。
- 官方 `@yss-ui/components/vite` 插件自 1.7.0 起已发布，完整验收范围为 Vite 6。旧项目先读取实际安装版本、exports 和现有插件，禁止与旧隔离插件同时运行。
- 生成代码前用 MCP `get_consumption_contract` 核对版本；未知版本不得假设新插件可用。文档站 Demo 的样式导入不能直接复制为业务全局样式策略。

## 标准代码骨架

```text
src/views/{module-name}/
├── index.vue
├── constant.ts
├── style.less
├── hooks/
│   ├── use{Module}List.ts
│   └── use{Module}Form.ts
├── type.ts              # 独立类型较多时增加
└── components/          # 多个私有视图时增加
    ├── {Module}Table.vue
    └── {Module}Modal.vue
```

## 生成流程

1. 读取本 skill 的三个 reference，并按上述文档检索顺序核对真实 API 与导出，禁止根据旧示例猜测。
2. 读取 `theme-token-usage`，检查项目真实主题变量与运行时同步链路。
3. 若有截图或旧项目路径，先按 `prototype-page-acceptance` 提取布局、按钮位置、表格高度、抽屉宽度、字段控件类型等验收项。
4. 按需求类型加载细分 skill：列表读 `page-list-module` 和 `ytable-usage`；表单读 `yss-formily`；编辑表格读 `yedit-table-usage`；树读 `ytree-usage`；导出下载读 `file-export-download`。
5. 先设计 `constant.ts`、`style.less` 和 hooks；独立类型或私有视图确有需要时再增加 `type.ts`/`components/`，最后写 `index.vue` 组合视图。
6. 对 API 请求使用 Orval 真实生成类型和导出，在 hooks 内封装 loading、分页映射和失败后状态；错误 Toast 由 mutator 统一处理。
7. 交付前检查导入来源、真实组件 API、分页字段、Formily schema 层级、主题 Token、查询按钮右下角布局、表格工具栏、样式作用域、删除确认和原型对照清单。

## 最小组合示例

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { YButton, YCard, YTable } from '@yss-ui/components';
import { useTableHeight } from '@yss-ui/hooks';
import { TABLE_COLUMNS } from './constant';
import { useRuleList } from './hooks/useRuleList';

const emit = defineEmits<{ create: [] }>();
const tableAreaRef = ref<HTMLDivElement>();
const { tableHeight, isReady } = useTableHeight(tableAreaRef, { withPagination: true, withToolbar: true });
const { loading, dataList, pagination, handlePageChange } = useRuleList();

/** 打开新增表单，实际项目中由表单 Hook 实现。 */
const openCreate = (): void => {
  emit('create');
};
</script>

<template>
  <YCard class="page-card">
    <div ref="tableAreaRef" class="table-area">
      <YTable
        v-if="isReady"
        :height="tableHeight"
        :data="dataList"
        :columns="TABLE_COLUMNS"
        :loading="loading"
        pageable
        v-model:pagination="pagination"
        @page-change="handlePageChange"
      >
        <template #toolbar-right>
          <YButton type="primary" @click="openCreate">新增</YButton>
        </template>
      </YTable>
    </div>
  </YCard>
</template>

<style scoped lang="less">
@import './style.less';
</style>
```

## 交付检查清单

- [ ] 已优先复用 `@yss-ui/components`、`@yss-ui/hooks`、`@yss-ui/utils`。
- [ ] `index.vue` 不超过 150 行，业务逻辑、常量、列配置和样式已按职责拆分。
- [ ] 未出现未导出的 Y 前缀组件。
- [ ] 未导入 `@formily/antd-v3`、`@formily/antd` 或业务层 `@formily/antdv` UI 组件。
- [ ] `YTable` 分页字段为 `current/pageSize/total`。
- [ ] `YTable` 未臆造 `request/search-params` Prop，也未把实例 `refresh()` 当作远程请求。
- [ ] 主表格主操作放在 `#toolbar-right`，仅在业务需要列设置时才配置了 `toolbar-config.custom`。
- [ ] 编辑表格场景使用 `YEditTable`，下拉可输入/多选等能力通过列 `props` 配置。
- [ ] `YFormily` 未使用不存在的详情开关 prop，表单 label 固定宽度右对齐，`FormGrid` 保持响应式。
- [ ] 查询区按钮在外部 `.xxx__search-actions` 右对齐独占一行，缩窄后仍处于搜索卡片右下角。
- [ ] 主题色、状态色、中性色及交互态使用动态 Token；未依赖未同步变量的固定色 fallback。
- [ ] 导出下载使用 `handleBlobResponse`，且 Blob 配置、响应头、loading 与错误链路已验证。
- [ ] 国际化多语言规范：在支持国际化的项目中，表格列定义、操作列配置、表单 Schema 均使用工厂函数结合 `computed` 驱动，分页 `showTotal`、按钮文案、枚举标签与校验提示无硬编码中文。
- [ ] 已核对 Orval 真实导出，未使用 `if (res?.success)` 或重复错误 Toast。
- [ ] 若有截图或旧项目参考，已逐项对照布局、按钮、表格高度、抽屉响应式和字段控件类型。

## 失败兜底策略

- 组件来源不确定时，先用 MCP `list_components/get_component_docs/search_docs` 交叉确认；MCP 不可用时才查 `component-map.md` 和 `llms-full.txt`，仍无法确认时报告待确认项，不得将猜测的导入直接落地。
- 页面复杂度过高时，先落地最小列表/表单闭环，再拆分私有组件和 hooks。
- API 契约不稳定时，先在 hook 内做最小字段映射，不把兼容逻辑散落到模板。
