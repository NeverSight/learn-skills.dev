---
name: vue3-element-admin
description: Develop, maintain, refactor, and review the vue3-element-admin frontend, including Vue pages, API modules, stores, routes, menus, permissions, caching, i18n, and project components. Use only in the vue3-element-admin repository or when the user explicitly asks to follow its conventions; do not apply these project-specific patterns to unrelated Vue applications.
---

# vue3-element-admin 开发

为 `vue3-element-admin` 提供项目专用约定。目标：可维护、类型安全、与现有代码一致。

## 边界

仅在本仓库或用户明确要求遵循时使用。冲突时优先级：用户请求 → 仓库实际代码与检查 → 本 Skill → 通用惯例。维护既有模块沿用相邻实现，不为套示例改写架构。

## 工作流程

1. 确认范围：读相关配置、目标文件与同目录实现，保留用户未提交的修改。
2. 做最小且完整的改动，复用已有 API、类型、Composables、组件与样式变量。
3. 按风险验证：至少类型检查与修改文件的 lint；涉及构建配置、路由或依赖时再跑构建。
4. 交付时说明改动、验证结果与未验证事项，不掩盖失败或既有问题。

不自动修复或格式化整个仓库；这类操作会改动无关文件。

## 按需读取参考文档

| 场景 | 读取 |
| --- | --- |
| 新增或重构 API、列表页、表单页、简单页面 | [new-page-guide.md](references/new-page-guide.md) |
| 配置驱动 CRUD（`src/components/Crud`：`CrudSearch`/`CrudTable`/`CrudModal` + `useCrudPage`） | [crud-development.md](references/crud-development.md) |
| 静态路由、动态菜单、路由 Meta | [router-menu.md](references/router-menu.md) |
| `v-hasPerm`、`hasPerm()`、权限标识 | [permission.md](references/permission.md) |
| `keepAlive`、标签页缓存与刷新 | [page-caching.md](references/page-caching.md) |
| 菜单标题、语言包与语言切换 | [i18n.md](references/i18n.md) |
| `settings.ts`、环境变量、存储键、主题 | [project-config.md](references/project-config.md) |
| Upload、Dict、TableSelect、IconSelect | [components.md](references/components.md) |
| 注释形式（JSDoc / `//`）与文案取舍 | [comments.md](references/comments.md) |

页面模式按 new-page-guide.md 的表选择：新增默认 Composables，维护时保留原模式，不因行数迁移模式或强行拆分。页面根节点沿用 `page-container`，搜索、内容、工具栏复用 `page-search`、`page-content`、`page-toolbar` 等全局样式。

## 项目约定

### Vue 与组件

- Composition API + `<script setup lang="ts">`；SFC 块顺序 `template` → `script` → `style`（ESLint 已约束）。
- 组件文件 PascalCase，路由页面 `index.vue`；Props 用类型声明，默认值选与相邻代码一致、类型最清楚的写法。
- Composable 用 `use` + camelCase，只提取有状态、可复用的逻辑；不为简单工具函数制造 Composable。
- 不设置固定行数或原子类数量门槛；按职责边界、复用价值和变更频率决定拆分。

### 命名

| 对象 | 约定 | 示例 |
| --- | --- | --- |
| 变量、函数 | camelCase；名称与数据形态一致 | `selectedUserId` / `selectedUserIds` / `users`（复数即集合，不加 `List`） |
| 布尔 | `is` / `has` / `can` / `should` 前缀 | `isSaving`、`hasSelection` |
| 易混单位 | 单位写进名称；展示字符串用 `Text` | `durationSeconds`、`sizeText` |
| 类型 | PascalCase，按用途：`Item` / `Detail` / `Form` / `QueryParams` / `Result` | `UserItem`、`UserForm`；不用 `VO` / `DTO` 后缀 |
| UI 事件入口 | `handleXxx` | `handleQueryClick`、`handleSubmit` |
| 数据加载 | `loadXxx` / `fetchData` | `loadUsers`；`handleQuery` 回第一页，`fetchData` 保留当前页 |
| 打开、关闭、重置 | `openEditor` / `closeEditor` / `resetFilters` | |
| 纯转换与校验 | 动词开头 | `formatDate`、`buildOptions`、`validatePassword` |
| 指定值 / 反转 | `setThemeMode(mode)` / `toggleThemeMode()` | 两者不合并 |
| API 读取 | `getPage` / `getOptions` / `getFormData` | 编辑回填用 `getFormData`，不与详情混同；详情类按相邻模块命名 |
| API 写入 | `create` / `update` / `deleteByIds` | 同类方法不混用同义词 |
| 组件事件 | kebab-case | `query-click`、`confirm-click`（CRUD 组件契约） |

后端字段、权限字符串等契约不机械重命名。表中无项目先例的条目（如 `loadXxx`、`openEditor`、`setXxx` / `toggleXxx`、单位入名）为通用约定，仅用于新代码；与相邻实现冲突时，以相邻实现为准。

### 类型与 API

- 新业务 API 模块通常 `index.ts` + `types.ts`，但不为形式拆分很小或已有稳定结构的模块。
- 复用 `@/api/common` 的 `BaseQueryParams`、`PageResult`、`OptionItem` 等公共类型。
- 请求拦截器已返回业务 `data`，调用端不再读取 `.data`。
- API 以现有对象字面量风格组织；HTTP 方法、URL 和参数结构以真实后端契约及相邻 API 为准。
- 不为绕过类型检查新增 `any`、非空断言或强转。

### 状态与 Store

- 新 Store 用 Setup Store，保持扁平目录结构。
- 组件外需要稳定 Pinia 实例时，复用 `useXxxStoreHook()` 或显式传入 `store`。
- 不复制服务端状态到多个 Store；先复用已有状态和 Composable。

### 样式

- 简单、一次性的排版与外观（布局、间距、尺寸、字号字重、圆角、边框等）直接用 UnoCSS 原子类，不为它们建语义类名，也不写 SCSS。
- 出现以下任一情况才建语义类（BEM + scoped SCSS）：样式承载业务语义需要可寻址（如 `order-card__price`）、含状态或嵌套选择器（`:hover`、`is-*`、父子联动）、动画、媒体查询、`:deep()`；同一串原子类在多处重复时提炼为 shortcut 或组件，不复制粘贴。
- 同一节点的同一属性只维护一处；已有 BEM 类的内部样式不再叠加控制该属性的原子类。组件外部间距与占位由使用方用原子类控制，组件内部不重复定义这些属性。
- 主题感知的界面颜色优先使用 Element Plus 或项目 CSS 变量。
- 品牌色、图表色、状态色和必要的第三方覆盖可以使用明确颜色；重复使用时集中为变量或配置。
- 沿用现有 BEM 风格时使用 `block__element--modifier`；状态类使用 `is-*`。不要为满足形式给简单结构增加无意义类名。

### 路由、权限与国际化

- 固定入口（登录、错误页等）进静态路由；业务菜单走后端菜单配置，不在前后端重复维护。
- 按钮权限用 `v-hasPerm` / `hasPerm()`，格式 `模块:资源:操作`；配置驱动 CRUD 用 `permPrefix` 复用内置按钮权限。
- 路由标题优先语言包 key；新增 key 同步维护所有受支持语言文件。
- 动 `keepAlive` 与缓存策略前先读 page-caching.md（缓存按 `fullPath` 匹配，不是组件 `name`）。

### 注释

注释形式按「是否对外暴露」选择：对外暴露的成员（`defineProps` / `defineEmits` / `defineExpose`、`export` 的函数 / 类型 / 常量）用 JSDoc，组件内部实现（`computed`、`ref`、私有函数、局部变量、页面 `<script setup>` 内部成员）用 `//`。文案解释"为什么、约束和副作用"，不复述代码，也不用 JSDoc 给 `onMounted`、`watch` 等执行逻辑开场。完整表格、示例与 API 模块等特例见 [comments.md](references/comments.md)。

## 验证清单

- [ ] 改动符合用户请求，保留既有架构与无关修改
- [ ] 命名、类型、权限、路由与真实契约一致，无新增 `any` / 断言 / 重复状态
- [ ] 权限、国际化、缓存等跨文件关系已同步
- [ ] 类型检查与修改文件 lint 通过；涉构建、路由、依赖时构建通过
