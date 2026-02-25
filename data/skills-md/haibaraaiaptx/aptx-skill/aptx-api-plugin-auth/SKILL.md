---
name: aptx-api-plugin-auth
description: "使用 @aptx/api-plugin-auth 实现 token 认证中间件和控制器。支持自动添加 Authorization header、token 刷新（主动/被动401处理）、防止重复刷新、失败回调。触发条件：用户请求认证功能（配置中间件、处理401刷新、管理token）或代码涉及 createAuthMiddleware/createAuthController 时使用。"
---

# aptx-api-plugin-auth

## 目录

- [工作流程](#工作流程)
- [TokenStore 接口](#tokenstore-接口)
- [中间件模式（推荐）](#中间件模式推荐)
- [控制器模式（手动 token 管理）](#控制器模式手动-token-管理)
- [配置选项](#配置选项)
- [错误处理](#错误处理)
- [关键约束](#关键约束)
- [高级主题](#高级主题)

---

## 工作流程

在接入认证插件时，执行以下流程：

1. 强制使用 `TokenStore` 抽象，不直接在业务代码里散落 token 读写。
2. 创建 `createAuthMiddleware({ store, refreshToken, ... })` 并挂到 `RequestClient.use(...)`。
3. `refreshToken` 返回 `{ token, expiresAt }` 或 `string`，优先返回 `expiresAt` 以便存储层同步过期时间。
4. 使用 `shouldRefresh` 定义触发刷新条件；默认仅在 `HttpError(401)` 时刷新。
5. 配置 `onRefreshFailed` 处理刷新失败后的业务动作（例如清理会话或跳转登录）。

默认推荐搭配：

- `@aptx/token-store`（TokenStore 接口定义）
- `@aptx/token-store-cookie`（浏览器 cookie 实现）
- SSR：`@aptx/token-store-ssr-cookie`（Node/SSR request-scoped cookie 实现）

---

## TokenStore 接口

`store` 参数必须实现 `TokenStore` 接口（由 `@aptx/token-store` 提供）：

```typescript
interface TokenStore {
  // 获取存储的 token
  getToken(): Promise<string | null>;

  // 存储 token（可选 expiresAt 用于支持过期时间）
  setToken(token: string, expiresAt?: number): Promise<void>;

  // 清除 token
  clearToken(): Promise<void>;
}
```

推荐实现：
- `@aptx/token-store-cookie` - 浏览器 cookie 存储（自动跨标签页同步）
- 自定义实现（如 localStorage、sessionStorage、IndexedDB）

---

## 中间件模式（推荐）

最小模板：

```ts
import { createAuthMiddleware } from "@aptx/api-plugin-auth";
import { createCookieTokenStore } from "@aptx/token-store-cookie";

const store = createCookieTokenStore({
  tokenKey: "token",
  metaKey: "token_meta",
  syncExpiryFromMeta: true,
});

const auth = createAuthMiddleware({
  store,
  refreshLeewayMs: 60_000,
  refreshToken: async () => {
    return { token: "new-token", expiresAt: Date.now() + 30 * 60 * 1000 };
  },
});
```

---

## 控制器模式（手动 token 管理）

对于需要手动控制 token 的场景（如手动刷新、预加载 token）：

```ts
import { createAuthController } from "@aptx/api-plugin-auth";

const controller = createAuthController({
  store,
  refreshToken: async () => ({ token: "...", expiresAt: Date.now() + 30000 }),
});

// 手动触发刷新并返回新 token
const token = await controller.refresh();

// 确保返回有效 token（接近过期时自动刷新）
const validToken = await controller.ensureValidToken();
```

**AuthController 方法：**
- `refresh(): Promise<string>` - 强制刷新 token 并返回新 token
- `ensureValidToken(): Promise<string>` - 返回有效 token，接近过期时自动刷新

---

## 配置选项

### AuthPluginOptions

| 选项 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `store` | `TokenStore` | ✅ | - | Token 持久化抽象（必须实现 TokenStore 接口） |
| `refreshToken` | `Promise<{token, expiresAt?} \| string>` | ✅ | - | 刷新 token 的异步函数 |
| `refreshLeewayMs` | `number` | ❌ | `60_000` | 提前刷新的时间窗口（毫秒） |
| `shouldRefresh` | `(error, req, ctx) => boolean` | ❌ | 401 检查 | 判断是否需要刷新的条件。error 结构：`{ status?: number, message?: string, code?: string }` |
| `onRefreshFailed` | `(error) => void` | ❌ | - | 刷新失败回调 |
| `headerName` | `string` | ❌ | `"Authorization"` | 自定义 header 名称 |
| `tokenPrefix` | `string` | ❌ | `"Bearer "` | Token 前缀 |
| `maxRetry` | `number` | ❌ | `1` | 刷新失败后重试次数 |

### refreshToken 返回值

`refreshToken` 可以返回两种格式：

1. **推荐格式**（包含过期时间）：
```ts
return {
  token: "new-token",
  expiresAt: Date.now() + 30 * 60 * 1000, // 30 分钟后过期
};
```

2. **简单格式**（仅 token）：
```ts
return "new-token"; // 适用于不需要过期时间的场景
```

优先返回包含 `expiresAt` 的对象，便于存储层（如 `@aptx/token-store-cookie`）同步过期时间。

### 自定义 header 配置

对于非标准认证方案（如自定义 header 或无 Bearer 前缀）：

```ts
const auth = createAuthMiddleware({
  store,
  refreshToken: async () => ({ token: "custom-token" }),
  headerName: "X-Auth-Token",      // 自定义 header 名称
  tokenPrefix: "",                  // 移除 Bearer 前缀
  maxRetry: 2,                      // 增加重试次数
});
```

### 自定义 shouldRefresh 条件

默认仅在 401 状态码时触发刷新。如需自定义逻辑：

```ts
const auth = createAuthMiddleware({
  store,
  refreshToken: async () => ({ token: "..." }),
  shouldRefresh: (error, req, ctx) => {
    // error: { status?: number, message?: string, code?: string }
    return error.status === 401 || error.code === "TOKEN_EXPIRED";
  },
});
```

**参数说明：**
- `error`: 错误对象，包含 `status`（HTTP状态码）、`message`（错误消息）、`code`（业务错误码）
- `req`: 原始请求对象
- `ctx`: 上下文对象

### 重试策略

`maxRetry` 控制刷新失败后的重试次数：

- `maxRetry: 0` - 刷新失败后立即抛出错误
- `maxRetry: 1` (默认) - 刷新失败后重试一次
- `maxRetry: 2` - 刷新失败后重试两次

刷新失败时会自动调用 `store.clearToken()` 清除本地 token。

---

## 错误处理

```ts
const auth = createAuthMiddleware({
  store,
  refreshToken: async () => {
    const res = await fetch("/api/refresh");
    if (!res.ok) throw new Error("Refresh failed");
    return await res.json();
  },
  onRefreshFailed: (error) => {
    // 刷新失败后的业务动作
    console.error("Auth refresh failed:", error);
    // 例如：跳转登录页、清除用户状态、显示登录弹窗
    window.location.href = "/login";
  },
});
```

---

## 关键约束

- `store` 必填且是唯一 token 持久化入口，必须实现 `TokenStore` 接口。
- `refreshToken` 尽量返回 `expiresAt`，便于存储层处理过期时间。
- 若刷新失败，必须由 `onRefreshFailed` 统一处理业务动作。
- `shouldRefresh` 默认仅在 `HttpError(401)` 时触发刷新，其他错误不会刷新。

---

## 高级主题

### 边缘情况处理

详见 [edge-cases.md](references/edge-cases.md)，包含：

- 并发刷新防止
- Token 验证
- 网络错误重试
- 跨标签页 Token 同步
- 无限刷新保护
