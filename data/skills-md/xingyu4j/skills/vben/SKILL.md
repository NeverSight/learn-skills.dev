---
name: vben
description: Vue Vben Admin monorepo 项目专家。适用于 Vben Admin 项目中的页面开发、组件使用、路由配置、API 定义、状态管理、适配器模式、国际化、权限控制等任务。支持所有应用变体（web-antd、web-ele、web-naive）和共享包。
metadata:
  version: "1.0.0"
---

# Vue Vben Admin

基于 **pnpm workspaces + Turborepo** 的 monorepo 项目，使用 Vue 3 + TypeScript + Vite 构建。提供多套 UI 库变体（Ant Design Vue、Element Plus、Naive UI），共享同一套基于 TailwindCSS + shadcn-vue 的核心框架。

## 项目结构

→ 详见 [vben-dir](references/vben-dir.md)

## 开发指南

| 主题 | 说明 | 参考 |
|------|------|------|
| 新增页面 | 创建视图组件、路由模块和国际化配置 | [vben-add-page](references/vben-add-page.md) |
| 新增 API | 添加带类型的 API 端点定义和可选的 Mock 路由 | [vben-add-api](references/vben-add-api.md) |
| 新增 Store | 使用 Composition API 创建 Pinia Store | [vben-add-store](references/vben-add-store.md) |
| 新增 Mock | 在 Nitro 后端 Mock 服务中添加模拟路由 | [vben-add-mock](references/vben-add-mock.md) |
| CRUD 模块 | 完整 CRUD：表格 + 搜索表单 + 新建/编辑弹窗 + API + 路由 + 国际化 | [vben-crud](references/vben-crud.md) |

## 组件参考

| 组件 | 说明 | 参考 |
|------|------|------|
| Form 表单 | 适配多 UI 框架的表单组件，底层基于 vee-validate | [vben-form](references/vben-form.md) |
| Modal 模态框 | 支持拖拽、全屏、自动高度、loading 的弹窗组件 | [vben-modal](references/vben-modal.md) |
| Drawer 抽屉 | 支持自动高度、loading 的侧边抽屉组件 | [vben-drawer](references/vben-drawer.md) |
| Alert 轻量提示框 | 纯 JS 调用的 alert/confirm/prompt 提示框 | [vben-alert](references/vben-alert.md) |
| Vxe Table 表格 | 基于 vxe-table 的列表组件，集成搜索表单 | [vben-vxe-table](references/vben-vxe-table.md) |
| ApiComponent 包装器 | 为组件提供自动获取远程数据的能力 | [vben-api-component](references/vben-api-component.md) |
| CountToAnimator 数字动画 | 数字滚动动画效果组件 | [vben-count-to-animator](references/vben-count-to-animator.md) |
| EllipsisText 省略文本 | 超长文本省略、tooltip 提示、展开收起 | [vben-ellipsis-text](references/vben-ellipsis-text.md) |

## 关键约定

### 路径别名

- `#/*` 映射到各应用的 `./src/*`（在 `package.json#imports` 中定义）
- 应用内部导入始终使用 `#/` 前缀：`import { $t } from '#/locales'`
- 共享包使用 `@vben/` 前缀：`import { preferences } from '@vben/preferences'`

### 依赖管理

- 内部包：`"workspace:*"`
- 第三方包：`"catalog:"`（版本在 `pnpm-workspace.yaml#catalog` 中集中管理）

### 代码风格

- 所有 Vue SFC 使用 `<script lang="ts" setup>`
- 仅使用 Composition API，禁止 Options API
- 使用 TailwindCSS 工具类进行样式开发
- 所有用户可见文本使用 `$t('key')` 国际化
- 遵循 Conventional Commits 规范：`feat`、`fix`、`chore`、`docs`、`refactor`、`perf`、`test`

### 组件适配器模式

每个应用在 `src/adapter/` 中桥接通用组件到具体 UI 库：

- `component/index.ts` — 通过 `globalShareState.setComponents()` 注册 UI 库组件映射
- `form.ts` — 通过 `setupVbenForm()` 配置表单系统（model 属性名等）
- `vxe-table.ts` — VXE Table 适配器

添加新的表单组件类型时：
1. 在 `component/index.ts` 中添加异步导入
2. 需要占位符的组件用 `withDefaultPlaceholder()` 包装
3. 添加到 `ComponentType` 联合类型
4. 在 `initComponentAdapter()` 的组件映射中注册

### 权限控制

三种访问模式，通过 `preferences.app.accessMode` 配置：
- **frontend**：按用户角色过滤静态路由
- **backend**：从 `getAllMenusApi()` 获取菜单并动态注册路由
- **mixed**：两者结合

路由 meta 选项：
- `meta.ignoreAccess: true` — 跳过权限检查
- `meta.authority: ['admin']` — 限制特定角色（frontend 模式）
- `meta.menuVisibleWithForbidden: true` — 菜单中显示但跳转 403
- `meta.affixTab: true` — 固定标签页
- `meta.hideInMenu: true` — 从侧边菜单隐藏

UI 级别的权限控制：
```vue
<!-- 指令方式 -->
<button v-access:code="['permission-code']">操作</button>

<!-- 组件方式 -->
<AccessControl :codes="['permission-code']">
  <button>操作</button>
</AccessControl>
```

### 偏好设置系统

`@vben/preferences` 导出单例 `preferences`（响应式，自动持久化到 localStorage）。

各应用在 `apps/<app>/src/preferences.ts` 中覆盖默认配置：
```ts
import { defineOverridesPreferences } from '@vben/preferences';

export const overridesPreferences = defineOverridesPreferences({
  app: { name: 'My App' },
  theme: { mode: 'light' },
});
```

### 请求客户端拦截器

各应用的 `src/api/request.ts` 创建 `RequestClient`，包含以下拦截器：
1. **请求拦截**：附加 `Bearer Token` + `Accept-Language` 请求头
2. **defaultResponseInterceptor**：解包 `{ code, data, message }` 格式
3. **authenticateResponseInterceptor**：处理 401，刷新 token 或跳转登录
4. **errorMessageResponseInterceptor**：显示错误提示

### 国际化

- 框架级翻译：`packages/locales/src/langs/`
- 应用级翻译：`apps/<app>/src/locales/langs/<locale>/*.json`
- 模板中使用 `$t('key')`，脚本中从 `#/locales` 导入 `$t('key')`
- 第三方组件库的 locale 加载在 `apps/<app>/src/locales/index.ts` 中处理

### Mock 后端

`apps/backend-mock/` 是基于 Nitro 的服务端，使用 h3 路由 + faker.js 生成数据。
- API 路由位于 `apps/backend-mock/api/`
- 独立启动：`pnpm -F @vben/backend-mock start`
- Vite 开发服务器将 API 请求代理到此服务

## 核心包参考

| 包名 | 路径 | 用途 |
|------|------|------|
| `@vben/access` | `packages/effects/access` | 路由/菜单生成，权限指令 |
| `@vben/common-ui` | `packages/effects/common-ui` | 共享 UI（ApiComponent、IconPicker 等） |
| `@vben/hooks` | `packages/effects/hooks` | `useAppConfig` 等 |
| `@vben/layouts` | `packages/effects/layouts` | BasicLayout、登录页、小部件 |
| `@vben/request` | `packages/effects/request` | 基于 Axios 的 RequestClient |
| `@vben/preferences` | `packages/preferences` | 响应式偏好管理器 |
| `@vben/stores` | `packages/stores` | 全局 Pinia Store |
| `@vben/locales` | `packages/locales` | vue-i18n 工具 |
| `@vben/styles` | `packages/styles` | 全局 CSS / TailwindCSS 基础样式 |
| `@vben/utils` | `packages/utils` | 共享工具函数 |
| `@vben/types` | `packages/types` | 共享 TypeScript 类型 |
| `@vben/icons` | `packages/icons` | Iconify 图标封装 |
| `@vben/constants` | `packages/constants` | 全局常量（LOGIN_PATH 等） |

## 应用引导流程

`main.ts` → `initApplication()`：
1. `initPreferences({ namespace, overrides })` — 加载/持久化偏好设置
2. `bootstrap(namespace)`：
   - `initComponentAdapter()` — 注册 UI 组件映射
   - `initSetupVbenForm()` — 配置表单系统
   - `setupI18n(app)` — 初始化国际化
   - `initStores(app, { namespace })` — 初始化 Pinia Store
   - `registerAccessDirective(app)` — 注册 `v-access` 指令
   - `initTippy(app)` — 初始化 tooltip
   - `app.use(router)` — 安装路由（含导航守卫）
   - `app.use(MotionPlugin)` — 安装动画插件
   - 挂载到 `#app`

## 常用命令

```bash
pnpm dev              # 启动所有应用（开发模式）
pnpm build            # 构建所有应用
pnpm lint             # ESLint 检查
pnpm format           # Prettier 格式化
pnpm test:unit        # 运行单元测试（vitest）
pnpm check:circular   # 检查循环依赖
pnpm check:dep        # 检查未使用/缺失依赖
pnpm check:cspell     # 拼写检查
pnpm commit           # 交互式 Conventional Commit（czg）
pnpm typecheck        # vue-tsc 类型检查

# 启动特定应用
pnpm -F @vben/web-antd dev
pnpm -F @vben/backend-mock start
```
