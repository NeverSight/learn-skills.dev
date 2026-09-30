---
name: art-design-pro
description: 基于 Art Design Pro 的 Vue3 + TS 中后台开发规范与组件使用规则。
version: 1.0.0
---

# Art Design Pro 开发 Skill

你正在开发基于 Art Design Pro 的 Vue 3 + TypeScript 中后台项目。默认遵循 Art Design Pro 官方架构、组件和工程规范，不要把页面当成普通 Element Plus 项目从零拼装。

## 技术基线

- Vue 3 + TypeScript + Vite
- Element Plus
- Tailwind CSS + Sass
- ECharts（通过项目封装使用）
- VueUse / Pinia / vue-i18n 等项目既有能力
- 当前源码主线为 Art Design Pro v3.x；v3.0 已从 Sass/iconfont 等旧方案迁移到 Tailwind CSS + Iconify，新增项目优先按当前主线实现。

## 核心开发原则

1. 先阅读项目现有页面、hooks、api、types，再写代码。
2. 优先复用 `src/components/core` 和 `src/hooks`，不要重复实现已有能力。
3. 业务专用组件留在 `src/views/<domain>/modules`；只有稳定跨业务复用的组件才提升到 `src/components/business` 或 `core`。
4. 页面负责编排，API 负责请求，hooks 负责可复用状态/流程，core 组件负责通用 UI。
5. 列表页优先 `useTable + ArtSearchBar + ArtTableHeader + ArtTable`。
6. 表单优先 `ArtForm`；查询表单优先 `ArtSearchBar`。
7. 表格操作优先复用 `ArtTableHeader`、`ArtButtonTable` 等现有组件。
8. 图表优先 `Art*Chart`，不要直接在业务页面重复初始化 ECharts。
9. 统计/趋势/进度等 Dashboard 卡片优先 `Art*Card`。
10. 尽量使用项目已有 Tailwind class、主题变量和 Iconify 图标，不随意引入新的 CSS 体系。
11. 不要为了“更灵活”把简单页面全部配置化；组件的目标是复用稳定能力，不是把业务代码变成低可读性的 JSON。
12. 保持响应式，尤其关注 `<768px`、`<1024px` 等项目已有断点行为。
13. 搜索参数、表单提交数据应避免把无效空值发送到后端；ArtSearchBar/ArtForm 已提供数据清洗能力。
14. 组件 API 以源码为准；不确定时先查 `src/components/core` 对应实现。

## 项目定位

Art Design Pro 是企业级中后台模板，核心价值是视觉、交互、组件库和开发效率。官方技术栈为 Vue 3、TypeScript、Vite、Element Plus、Tailwind CSS、Sass，并提供 useTable、ArtForm、ArtSearchBar 等开发能力。

## 目录定位

常用目录：

- `src/api`：按业务域封装 API
- `src/components/core`：系统级通用组件
- `src/components/business`：稳定的业务通用组件
- `src/views`：业务页面
- `src/views/<domain>/<page>/modules`：页面私有 search/dialog 等子组件
- `src/hooks`：组合式复用逻辑
- `src/config`：系统配置
- `src/directives`：指令
- `src/enums`：枚举
- `src/types`：类型
- `src/utils`：工具函数
- `src/store`：Pinia 状态

## Core 组件目录

`src/components/core` 当前包含：

- `banners`
- `base`
- `cards`
- `charts`
- `forms`
- `layouts`
- `media`
- `others`
- `tables`
- `text-effect`
- `theme`
- `views`
- `widget`

详细组件清单和用法见 `references/components.md`。

## 标准 CRUD 页面

对于“列表 + 搜索 + 新增/编辑 + 删除”的需求，默认结构：

```text
src/views/<domain>/<page>/
├── index.vue
└── modules/
    ├── <page>-search.vue       # 页面需要复杂查询时
    └── <page>-dialog.vue       # 新增/编辑/详情
```

`index.vue` 负责：
- 页面布局
- useTable
- API 调用
- columns
- 刷新/删除/批量操作
- 权限按钮
- 打开 dialog

不要把复杂表单、查询配置全部堆在 index.vue。

## 标准列表组件组合

推荐：

```vue
<ArtSearchBar v-model="searchForm" :items="searchItems" @search="handleSearch" @reset="handleReset" />

<ArtTableHeader
  v-model:columns="columns"
  :loading="loading"
  @refresh="refresh"
>
  <template #left>
    <ElButton type="primary" @click="openCreate">新增</ElButton>
  </template>
</ArtTableHeader>

<ArtTable
  :data="data"
  :columns="columns"
  :loading="loading"
  :pagination="pagination"
/>
```

实际项目必须根据已有页面的 useTable API 和 types 调整，不能机械复制上述片段。

## 表单原则

- 简单表单：`ArtForm`
- 查询表单：`ArtSearchBar`
- 复杂业务表单：可以组合 Element Plus 原生组件，但优先复用 ArtForm 的响应式布局、render、slots、校验模式。
- 自定义控件优先使用 `render` 或 slot，而不是修改 core 组件。
- 表单项支持常用 Element Plus 控件；具体 `type` 和 props 见 `references/forms.md`。

## 表格原则

`ArtTable` 在 Element Plus `ElTable` 上提供分页、loading、列配置、自定义列、全局序号、展开行、空状态和响应式分页等能力。它支持大部分 ElTable 属性、事件、插槽。

列需要自定义内容时优先使用项目 ColumnOption 对应的 `useSlot / slotName`；表头自定义可使用 `useHeaderSlot / headerSlotName`。

`ArtTableHeader` 负责搜索切换、刷新、表格尺寸、全屏、列显示/排序、斑马纹、边框、表头背景等表格工具。

## 图表原则

使用 `src/components/core/charts` 下的 Art 图表组件。图表组件内部已经处理 ECharts 初始化、主题、动画、loading、resize 等通用逻辑。

常见：
- `ArtLineChart`
- `ArtBarChart`
- `ArtHBarChart`
- `ArtDualBarCompareChart`
- `ArtKLineChart`
- `ArtMapChart`
- `ArtRadarChart`
- `ArtRingChart`
- `ArtScatterChart`

先确认 props/type，再传数据，不要在业务页面直接复制 ECharts option 初始化代码。

## Dashboard 卡片

优先使用：
- `ArtStatsCard`
- `ArtProgressCard`
- `ArtImageCard`
- `ArtDataListCard`
- `ArtTimelineListCard`
- `ArtBarChartCard`
- `ArtLineChartCard`
- `ArtDonutChartCard`

卡片应负责展示，业务页面负责提供数据。

## Banner

优先使用：
- `ArtBasicBanner`
- `ArtCardBanner`

不要为了普通欢迎区/顶部宣传区自己重新写一套卡片 Banner。

## 输出代码前检查

- 是否已经存在对应 core 组件？
- 是否存在类似页面可以复制结构而不是重新设计？
- 是否应该使用 useTable？
- 查询是否应该用 ArtSearchBar？
- 表单是否应该用 ArtForm？
- 表格是否应该用 ArtTable + ArtTableHeader？
- Dashboard 是否可以用现成 Card/Chart？
- 是否使用现有权限、i18n、主题和 icon 方案？
- 是否把页面专用代码错误提升成全局组件？
- 是否把空字符串、空数组等无效参数发送给 API？
- 是否破坏移动端布局？

## 参考资料

- `references/architecture.md`：官方架构、目录和页面组织
- `references/components.md`：core 组件分类和组件清单
- `references/forms.md`：ArtForm / ArtSearchBar
- `references/tables.md`：ArtTable / ArtTableHeader
- `references/charts.md`：图表组件
- `references/cards-banners.md`：卡片和 Banner
- `references/others.md`：others/base/media 等组件使用原则
