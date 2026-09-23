---
name: frontend-universal-standards-skill
description: >-
  现代前端工程化开发与交付全栈规范。适用于 Vue 3 (Composition API/Vite/Pinia)、React 18/19 (Hooks/Zustand/RTK/Tailwind CSS)、Uni-app/微信小程序跨端及 Vue 2 遗留工程的项目架构、页面与组件逻辑开发、网络请求 (Axios/uni.request) 工业级封装、RBAC 动态权限路由、状态管理与跨端持久化；涵盖大文件切片秒传、TS 契约、五重代码质量卡点 (ESLint/Prettier/Husky) 等任务。专注工程架构、网络通信与状态流转（纯视觉审美参考 frontend-design，设计系统推导参考 ui-ux-pro-max，A11y走查参考 web-design-guidelines）。
---

# /frontend-universal-standards-skill — 前端全栈工程化与通用开发规范

本 Skill 是面向现代前端全栈工程的通用标准与交付规范，基于对数十个真实企业级中后台、B2C 商城、车联网大屏、移动端 H5、跨端小程序以及云存储网盘项目的深度实战抽象提炼而成。覆盖从脚手架选型、目录分层、强类型契约、网络请求拦截、RBAC 动态路由鉴权、多端状态持久化，到五重代码质量卡点体系的完整工程闭环。

---

## 1. 按需适配与反过度设计铁律 (Zero Over-Engineering)

**【核心纪律】严禁凭空给不需要的项目堆砌无关技术栈！**

Agent 在为工程生成前端代码、组件或脚手架时，必须严格基于**当前项目的 `package.json`、技术栈版本与用户实际业务意图**进行按需匹配：
1. **纯 Vue 3 Web 工程**：
   * 遵循 Vue 3 `<script setup lang="ts">` + Vite + Pinia + Vue Router 4 标准规范。
   * **绝对禁止**引入 React、Redux、Uni-app 特有 API（如 `uni.*`）或无关移动端适配插件。
2. **纯 React 18/19 工程**：
   * 遵循 React 18/19 全函数组件 + Hooks + Zustand / RTK + Tailwind CSS / SCSS 规范。
   * **绝对禁止**引入 Vue 相关语法、Pinia 或 Vuex。
3. **Uni-app / 微信小程序工程**：
   * 遵循分包加载（`subPackages` 严守 2MB 红线）、`uni.addInterceptor` 统一双轨拦截器、`rpx` 响应式单位与跨端 Storage 桥接规范。
   * **绝对禁止**使用浏览器特有的 `window` / `document` DOM 操作，严禁直接依赖未桥接的 `localStorage`。
4. **Vue 2 / Webpack 历史工程维护**：
   * 遵循最小化稳妥改动原则，保持 Options API 与 Vuex / Vue Router 3 现有规范，不盲目进行全盘重构；在必须扩充功能时提供平滑过渡方案。

---

## 2. 触发场景 (Trigger)

当用户或 Agent 处理以下任何前端开发场景时，必须主动激活本 Skill：
* **日常页面与组件开发**：编写或重构 Vue 3、React、Uni-app 页面与业务组件、实现表单与表格交互、数据绑定与单向数据流。
* **前端脚手架与目录规划**：新建或重构 Vue 3、React、Uni-app 项目架构，规划 `api/`, `views/`, `components/`, `stores/`, `router/`, `utils/` 等分层结构。
* **网络请求与 API 治理**：封装 Axios 或 `uni.request` 工业级拦截器链，配置 BaseURL 动态环境变量、Token 自动注入、401 统一重定向、业务错误码集中映射、请求取消与防重。
* **路由设计与鉴权守卫**：配置 Vue Router 或 React Router，设计常量路由（白名单）、动态 RBAC 权限路由过滤注入、通配 404 兜底、NProgress 进度条与页面 Title 同步。
* **状态管理与跨端持久化**：使用 Pinia、Zustand 或 Redux Toolkit 组织领域状态，实现 State 最小化与衍生计算，配置多端兼容的持久化驱动（LocalStorage / UniStorage）。
* **组件设计与组合式逻辑**：编写高内聚可复用组件，抽象 Vue Composables / React Hooks（倒计时、无限触底加载、表格分页），实现自定义全局指令（如 `v-img-lazy`）。
* **样式与多端自适应**：配置 Tailwind CSS v4、SCSS 样式系统、移动端 `rem` 适配（`postcss-pxtorem`）、小程序 `rpx` 适配与 `:deep()` 样式穿透。
* **工程质量与 CI/CD 提交卡点**：配置 ESLint 9 Flat、Prettier、Stylelint、Husky 与 Commitlint 五重质量防线。
* **复杂业务场景实现**：大文件分片断点续传、SparkMD5 秒传、购物车双轨状态合并、WebSocket/STOMP 车辆/告警长连接。
* **前端代码审查与反模式消除**：排查 API 侵入 UI/Storage、GET 明文传递密码、路由守卫未做登录鉴权、死代码残留、依赖数组缺失等坏味道。

---

## 3. 架构选型与形态决策树 (Architecture Decision Tree)

```text
                                [ 前端应用形态决策 ]
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
【 PC 中后台 / SaaS 】           【 现代化富交互 Web 】           【 跨端小程序 / 移动端 】
  • Vue 3 + TS + Vite              • React 18/19 + TS + Vite        • Uni-app (Vue 3 + TS)
  • Pinia (Setup Store)            • Zustand / Redux Toolkit        • Pinia (UniStorage 适配)
  • Element Plus / Antd            • Tailwind CSS v4                • uni-ui / uview-plus
  • RBAC 动态路由 + SVG 图标        • Lucide React + Playwright      • 严格分包 (subPackages)
  • NProgress 鉴权守卫              • 大文件分片 / 声明式 AuthGuard   • uni.addInterceptor
```

---

## 4. 核心工程纪律与防御铁律 (Non-negotiable Rules)

1. **【API 纯函数原则】**：API 模块严禁直接触发 UI 弹窗（`ElMessage`）或操作 Storage；必须由调用层或拦截器统一处理。
2. **【安全传输原则】**：登录与凭证提交必须使用 POST 并在 Body 中传输，严禁用 GET Query 暴露密码或 Token。
3. **【RBAC 通配路由挂载顺序】**：通配路由 `path: '/:pathMatch(.*)*'` 必须在所有动态权限路由添加完成后作为**最后一条**挂载，严禁置于静态常量路由首部。
4. **【小程序分包隔离】**：主包页面必须精简在核心 TabBar 和登录页，业务功能全部打入分包，主包严守 2MB 体积红线。
5. **【生命周期配对清理】**：任何在 Hooks / Composables / 组件中注册的定时器、事件监听、长连接，必须在销毁钩子（`onUnmounted` / cleanup）中显式注销。
6. **【工程卫生零容忍】**：严禁提交未使用的死代码、临时练习目录（如 `old/`, `practive/`）、脚手架默认模板（如 `HelloWorld.vue`）和硬编码测试 IP。

---

## 5. 模块指引与参考文档索引 (Reference Index)

在执行具体领域任务时，必须先阅读对应的专用参考文档：

* **[architecture_and_directory.md](references/architecture_and_directory.md)**：
  * Vue 3 / React / Uni-app 标准工程目录全景树
  * RBAC 常量路由、动态权限路由与通配路由挂载规范
  * 全局路由导航守卫状态机设计
  * Pinia / Zustand / RTK 架构模型与 State 最小化原则
* **[coding_and_component_standards.md](references/coding_and_component_standards.md)**：
  * TypeScript 强类型约束、RequestDTO / ResponseVO 契约
  * Vue 3 `<script setup lang="ts">`、Props/Emits 宏规范、ref 与 reactive 选型
  * React 18/19 函数组件、Hooks 依赖完整性与副作用清理
  * Smart/Dumb 组件拆分与单向数据流
* **[network_and_api_standards.md](references/network_and_api_standards.md)**：
  * 工业级 Axios 封装标准模板与拦截器链
  * 统一泛型请求门面函数（`request<TResponse, TData>`）
  * 全局 HTTP 与业务错误码字典对照表
  * Token 凭证无感刷新与 401 自定义事件解耦广播
* **[uniapp_and_miniprogram_standards.md](references/uniapp_and_miniprogram_standards.md)**：
  * 2MB 主包红线与 `subPackages` + `preloadRule` 分包预加载
  * `uni.addInterceptor` 统一双轨（request + uploadFile）拦截器
  * Pinia 跨端 Storage 持久化桥接适配器
  * Easycom 组件自动按需扫描规则与多端生命周期避坑
* **[engineering_and_quality.md](references/engineering_and_quality.md)**：
  * Vite 5/6 与 Webpack 别名（`@/`）安全配置
  * ESLint 9 Flat、Prettier、Stylelint (Recess 属性排序)、Husky、Commitlint 五重卡点
  * 多环境变量体系（`.env.development`, `.env.production`）
  * 模板清理与工程卫生准则
* **[ui_ux_and_style_standards.md](references/ui_ux_and_style_standards.md)**：
  * Tailwind CSS v4 与 SCSS 设计系统 Tokens
  * 移动端 `amfe-flexible` + `postcss-pxtorem` 与小程序 `rpx` 适配
  * 样式作用域与 `:deep()` 现代穿透
  * 基于 `IntersectionObserver` 的图片视口懒加载、路由滚动复位、骨架屏三态闭环
