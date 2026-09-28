---
name: dsh-plugin-client
description: 开发 DSH 插件的 client 半端（浏览器 UI）时使用：按已验证的 slot 与标准-kit 契约注册界面、双目标构建并包装客户端 bundle。
whenToUse: 给 DSH 插件加 UI（设置页、输入条按钮、工具调用视图）、排查 client 插件未加载时。
---

# DSH 插件 client 半端（依据官方包实现与 dsh-voice-input 实战验证）

## 包结构

- `package.json`：`exports` 加 `"./client": "./lib/client/index.js"`；`dsh.client` 声明 `{ "platform": "web", "inject": [...] }`
- `inject` 按需列出依赖的 client 插件：`@deepseek-ai/dsh-client-runtime`（slots）、`@deepseek-ai/dsh-client-locale`（i18n）、以及插槽声明方（如 `@deepseek-ai/dsh-client-ui-conversation`、`@deepseek-ai/dsh-client-ui-settings`）
- client 源码放 `src/client/index.ts`，导出 `export const inject = ['slots']` 与 `export function apply(ctx)`

## 注册 UI（slots 契约）

```ts
ctx.slots.inject('conversation.input.right', () => ctx.slots.register({
  name: 'conversation.input.right',  // 插槽名（single/list/chain 由声明方定）
  id: 'my-button',
  order: 10,
  locale: 'my.ns',                    // 可选：声明后组件收到 t()
}, MyComponent))
```

- 组件自动收到「标准 kit」：全局 `useSessions/useWorkspaces`；会话级 `useSession`、`useInput`（draft 快照）、`inputActions`（setDraft/submit/…）；以及 `sessionId`、`useProjection`、`renderSlot`、`t`
- 常用插槽：`settings.plugins.tab`（设置页标签）、`conversation.input.left/right`（输入条按钮区）、`tool.call.toolview`（工具调用视图，keyed 注册）、`conversation.composer.dock`

## 构建（tsup 双目标）

```ts
// tsup.config.ts：host 半端
{ entry: { 'host/index': 'src/host/index.ts' }, format: ['esm'], platform: 'node' }
// client 半端
{ entry: { 'client/index': 'src/client/index.ts' }, format: ['cjs'], platform: 'browser',
  external: ['react', 'react-dom'] }
```

- 构建后必须按官方 client-modules 协议包装：`window.__ModuleLoader__.load({ id: '<包名>', factory: (require) => { ...CJS... } })`（react 由宿主加载器提供，不打进 bundle）
- 自测：Node 里 mock `window.__ModuleLoader__` 执行 bundle，断言 `apply`/`inject` 导出与注册发生

## 安装与调试

- `file:` 协议是复制安装，改代码必须重装；`link:` 协议建 Junction 指向本地目录，改源码即时生效（开发推荐）
- 验证 client 已加载：刷新页面看 UI 是否出现；host 加健康路由 `GET /<prefix>/health` 排查；页面 HTML 的 client 清单里应出现 `"id":"<包名>"` 与 `rev`
- 页面清单不更新 = 服务端未重启（rev 是启动时计算的）；改 lib 后重启 dsh
