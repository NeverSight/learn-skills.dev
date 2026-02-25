---
name: aptx-api-plugin-csrf
description: "使用 @aptx/api-plugin-csrf 添加 CSRF 保护。触发条件：当代码需要在请求中添加 CSRF token、配置 cookie/header 名称、处理 SSR/Node 环境的 cookie 读取、或使用 createCsrfMiddleware 时使用。"
---

# aptx-api-plugin-csrf

在接入 CSRF 插件时，执行以下流程：

1. 使用 `createCsrfMiddleware({ cookieName, headerName, sameOriginOnly, getCookie })` 创建中间件
2. 根据环境选择配置：
   - 浏览器环境：使用默认 `getCookie`（自动使用 `document.cookie`）
   - SSR/Node 环境：必须提供自定义 `getCookie` 函数
3. 保持 `sameOriginOnly: true`（默认），避免跨域请求误注入 CSRF 头
4. 确认前后端约定的 cookie/header 名称一致
5. 将中间件挂载到 `RequestClient.use()` 或构造函数

**注意:** 需要同时安装 `@aptx/api-core` 作为 peer dependency。

---

## 快速参考

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `cookieName` | `string` | `"XSRF-TOKEN"` | CSRF cookie 名称 |
| `headerName` | `string` | `"X-XSRF-TOKEN"` | 写入 CSRF token 的 header 名称 |
| `sameOriginOnly` | `boolean` | `true` | 仅在同源请求中附加 token |
| `getCookie` | `(name) => string \| undefined` | 浏览器默认使用 `document.cookie` | 自定义 cookie 读取函数（SSR 必须提供） |

**何时添加 CSRF token:**

| 场景 | 添加 token |
|------|-----------|
| Cookie 存在 + `sameOriginOnly: false` | ✅ |
| Cookie 存在 + `sameOriginOnly: true` + 同源请求 | ✅ |
| Cookie 存在 + `sameOriginOnly: true` + 跨域请求 | ❌ |
| Cookie 不存在 | ❌ |

---

## 最小模板

### 浏览器环境

```ts
import { RequestClient } from "@aptx/api-core";
import { createCsrfMiddleware } from "@aptx/api-plugin-csrf";

const client = new RequestClient({
  middlewares: [
    createCsrfMiddleware({
      cookieName: "XSRF-TOKEN",
      headerName: "X-XSRF-TOKEN",
      sameOriginOnly: true,
      // 浏览器环境下不需要 getCookie，自动使用 document.cookie
    })
  ]
});
```

### 渐进式增强

```ts
import { createCsrfMiddleware } from "@aptx/api-plugin-csrf";

const client = new RequestClient();
client.use(createCsrfMiddleware({
  cookieName: "XSRF-TOKEN",
  headerName: "X-XSRF-TOKEN",
  sameOriginOnly: true,
}));
```

### SSR/Next.js 环境

```ts
import { createCsrfMiddleware } from "@aptx/api-plugin-csrf";
import { cookies } from 'next/headers';

const csrf = createCsrfMiddleware({
  cookieName: "XSRF-TOKEN",
  headerName: "X-XSRF-TOKEN",
  sameOriginOnly: true,
  getCookie: (name) => {
    const cookieStore = cookies();
    return cookieStore.get(name)?.value;  // SSR 必须提供 getCookie
  }
});
```

### Node.js/Express 环境

```ts
import { createCsrfMiddleware } from "@aptx/api-plugin-csrf";

const csrf = createCsrfMiddleware({
  cookieName: "XSRF-TOKEN",
  headerName: "X-XSRF-TOKEN",
  sameOriginOnly: true,
  getCookie: (name) => {
    const cookies = req.cookies;  // 从 cookie-parser 或 req.headers.cookie 读取
    const value = cookies?.[name];
    return value ? decodeURIComponent(value) : undefined;
  }
});
```

---

## 环境适配要点

### 环境差异

| 环境 | `document.cookie` | `window.location` | 默认 `getCookie` | 默认 `isSameOrigin` |
|------|-------------------|-------------------|-------------------|---------------------|
| 浏览器 | ✓ 可用 | ✓ 可用 | ✓ 使用 document.cookie | ✓ 检查 origin |
| SSR (Next.js) | ✗ undefined | ✗ undefined | ✗ 需要自定义 getCookie | ✓ 返回 true（始终同源） |
| Node.js | ✗ undefined | ✗ undefined | ✗ 需要自定义 getCookie | ✓ 返回 true（始终同源） |

### 关键约束

- **SSR/Node 环境**必须提供 `getCookie` 函数，否则会报错 `document is not defined`
- `getCookie` 返回原始 cookie 值，中间件会自动 `decodeURIComponent`，不要手动解码
- 默认 `sameOriginOnly: true` 对大多数用例是安全的
- Cookie 值会 URL 解码后再添加到 header

---

## 详细文档

| 文档 | 内容 |
|------|------|
| [API Details](references/api-details.md) | 完整 API 文档、配置选项详解、默认实现 |
| [Environment Adaptation](references/environments.md) | 浏览器/SSR/Node 环境详细适配指南 |
| [Testing Guide](references/testing-guide.md) | 测试策略、测试示例代码 |
| [Troubleshooting](references/troubleshooting.md) | 常见问题、故障排查、调试技巧 |
