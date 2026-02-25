---
name: aptx-api-core
description: "使用 @aptx/api-core 进行 HTTP 请求的指导。用于：创建和配置 RequestClient、实现 middleware/plugin、替换核心组件（Transport/Decoder 等）、处理错误、监听事件、使用 Context Bag、测试扩展。当代码需要理解或修改 @aptx/api-core 的架构、扩展机制、最佳实践时触发。"
---

# aptx-api-core

在需要接入或调整请求内核时，按以下顺序执行：

1. 创建 `RequestClient`，先确定全局配置：`baseURL`、`headers`、`timeoutMs`、`querySerializer`、`defaultResponseType`、`strictDecode`。详见 [实例化配置](#实例化配置)
2. 只在 `@aptx/api-core` 层处理通用行为，不引入业务认证、缓存、重试逻辑。业务逻辑应通过 [Middleware](references/middleware-patterns.md) 和 [Plugin](references/plugin-patterns.md) 实现。
3. 通过 `use(middleware)` 或 `apply(plugin)` 扩展能力，确保核心逻辑保持纯净。详见 [扩展能力](#扩展能力)
4. 使用 `request:start/end/error/abort` 事件做观测，不在事件回调里修改 payload。详见 [事件系统](#事件系统)
5. 发生错误时按错误类型分流：`HttpError`、`NetworkError`、`TimeoutError`、`CanceledError`、`ConfigError`、`SerializeError`、`DecodeError`。详见 [defaults.md - ErrorMapper](references/defaults.md#defaulterrormapper)

最小接入模板：

```ts
import { RequestClient } from "@aptx/api-core";

const client = new RequestClient({
  baseURL: "/api",
  timeoutMs: 10_000,
  headers: { "X-App": "web" },
  defaultResponseType: "json",
});

const res = await client.fetch("/user", {
  method: "GET",
  query: { include: ["profile", "roles"] },
});
```

## 快速参考

| 操作 | API | 示例 |
|------|-----|------|
| 创建客户端 | `new RequestClient()` | 见上方模板 |
| 创建客户端（函数式） | `createClient()` | 见[创建客户端工厂函数](#创建客户端工厂函数) |
| 发送请求 | `client.fetch()` | `await client.fetch("/user", { method: "GET" })` |
| 发送请求（高级） | `client.request()` | 见[request() - 高级入口](#request---高级入口) |
| 添加 middleware | `client.use()` | `client.use(loggingMiddleware)` |
| 应用 plugin | `client.apply()` | `client.apply(authPlugin)` |
| 监听事件 | `client.events.on()` | 见[事件系统](#事件系统) |

### 核心 API 映射

| 需求 | 方法 | 文档位置 |
|------|------|----------|
| 请求/响应修改 | Middleware | [middleware-patterns.md](references/middleware-patterns.md) |
| 替换核心组件 | Plugin | [plugin-patterns.md](references/plugin-patterns.md) |
| 中间件间共享状态 | Context Bag | [context-bag.md](references/context-bag.md) |
| 自定义传输/解码器等 | Extension Points | [extension-points.md](references/extension-points.md) |
| 测试扩展 | Testing | [testing-guide.md](references/testing-guide.md) |
| 查看默认实现 | Defaults | [defaults.md](references/defaults.md) |

## 请求元数据

`RequestMeta` 用于传递扩展元数据：

```ts
interface RequestMeta {
  /** 响应类型（覆盖默认值） */
  responseType?: "json" | "text" | "blob" | "arrayBuffer" | "raw";
  /** 自定义标签（用于追踪、日志等） */
  tags?: string[];
  /** 上传进度回调（best-effort） */
  onUploadProgress?: (info: ProgressInfo) => void;
  /** 下载进度回调（best-effort） */
  onDownloadProgress?: (info: ProgressInfo) => void;
  /** 其他扩展字段 */
  [key: string]: unknown;
}
```

### 进度回调（best-effort）

```ts
await client.fetch("/upload", {
  method: "POST",
  body: largeFile,
  meta: {
    onUploadProgress: ({ loaded, total, progress }) => {
      console.log(`Upload: ${(progress! * 100).toFixed(1)}%`);
    },
  },
});
```

**约束**：
- 进度回调仅在 FetchTransport 中生效
- 需要服务端返回 `Content-Length` 头
- 仅作为 best-effort 功能，不保证精确性

### 显式响应类型

```ts
// 文本响应
const res = await client.fetch("/data", {
  meta: { responseType: "text" },
});

// Blob 响应（文件下载）
const blobRes = await client.fetch("/file.pdf", {
  meta: { responseType: "blob" },
});
```

## 实例化配置

RequestClient 构造函数支持以下配置选项：

```ts
import {
  RequestClient,
  Transport,
  UrlResolver,
  BodySerializer,
  ResponseDecoder,
  ErrorMapper,
  Middleware,
  EventBus,
} from "@aptx/api-core";

const client = new RequestClient({
  // 基础配置
  baseURL: "https://api.example.com",
  headers: { "X-App": "web" },
  timeoutMs: 10_000,
  querySerializer: (query, url) => `${url}?${new URLSearchParams(query).toString()}`,
  meta: { tags: ["api"] }, // 默认 meta

  // 响应配置
  defaultResponseType: "json",
  strictDecode: true, // 严格 JSON 解码

  // 核心组件（可自定义）
  transport?: Transport,        // 底层传输层
  urlResolver?: UrlResolver,    // URL 解析
  bodySerializer?: BodySerializer, // 请求体序列化
  decoder?: ResponseDecoder,    // 响应解码
  errorMapper?: ErrorMapper,    // 错误映射
  events?: EventBus,            // 事件总线

  // 扩展
  middlewares?: Middleware[],   // 初始 middleware 列表
});
```

> 详见 [defaults.md](references/defaults.md) 了解所有默认实现的详细说明和最佳实践。

## fetch() vs request()

### fetch() - fetch-like 入口

适用于大多数场景，自动处理 URL 解析和请求构建。

```ts
const res = await client.fetch("/user", {
  method: "GET",
  headers: { "X-Custom": "value" },
  query: { id: 123 },
  body: { name: "test" },
  timeoutMs: 5000,
});
```

### request() - 高级入口

适用于需要手动构建 `Request` 对象的场景：

```ts
import { Request } from "@aptx/api-core";

const req = new Request({
  method: "POST",
  url: "/api/data",
  headers: { "Content-Type": "application/json" },
  body: { key: "value" },
  timeoutMs: 5000,
  meta: { tags: ["important"] },
});

const res = await client.request(req);
```

### 选择指南

| 需求 | 选择 | 原因 |
|------|------|------|
| 简单请求 | fetch() | API 简洁，自动处理 URL 解析 |
| 需要复用 Request 对象 | request() | 更灵活，Request 对象可传递 |
| 需要在 middleware 间传递状态 | request() | Request 对象可携带更多信息，详见 [context-bag.md](references/context-bag.md) |
| 需要显式控制请求构建 | request() | 完全控制 Request 创建过程 |

约束：

- 不把重试、认证、CSRF 写进 core；统一放插件层。
- `headers: { key: null }` 表示删除 header。
- `onUploadProgress` 和 `onDownloadProgress` 仅在支持的 transport 中生效。

## 响应元数据

`ResponseMeta` 用于在 middleware/plugin 间传递响应扩展信息：

```ts
interface ResponseMeta {
  /** 例如：{ fromCache: true } 由缓存 middleware 设置 */
  [key: string]: unknown;
}
```

### 使用示例（缓存 middleware）

```ts
const cacheMiddleware: Middleware = {
  async handle(req, ctx, next) {
    const cached = cache.get(req.url);
    if (cached) {
      return new Response({
        status: 200,
        headers: new Headers(),
        url: req.url,
        data: cached.data,
        raw: {},
        meta: { fromCache: true, cachedAt: cached.at },
      });
    }

    const res = await next(req, ctx);
    cache.set(req.url, res);
    return res;
  }
};
```

> 详见 [middleware-patterns.md](references/middleware-patterns.md#4-缓存-middleware简化版) 了解更多缓存实现模式。

## 扩展能力

### Middleware - 请求/响应修改

Middleware 用于处理横切关注点，如日志、认证、重试等。详见 [middleware-patterns.md](references/middleware-patterns.md)。

创建自定义 middleware：
```ts
import { Middleware, Request, Context, Response } from "@aptx/api-core";

const loggingMiddleware: Middleware = {
  async handle(req, ctx, next) {
    console.log(`[${req.method}] ${req.url}`);
    const res = await next(req, ctx);
    console.log(`[${res.status}] ${req.url}`);
    return res;
  }
};
client.use(loggingMiddleware);
```

常见 Middleware 模式：
- [日志 Middleware](references/middleware-patterns.md#1-日志-middleware)
- [缓存 Middleware](references/middleware-patterns.md#4-缓存-middleware简化版)
- [请求签名 Middleware](references/middleware-patterns.md#5-请求签名-middleware)

### Plugin - 核心组件替换

Plugin 用于替换核心组件或监听事件。详见 [plugin-patterns.md](references/plugin-patterns.md)。

使用场景：
- 替换 HTTP 客户端 → [Transport](references/extension-points.md#1-transport---底层传输层)
- 自定义序列化 → [BodySerializer](references/extension-points.md#3-bodyserializer---请求体序列化)
- 自定义解码 → [ResponseDecoder](references/extension-points.md#4-responsedecoder---响应解码)
- 错误映射 → [ErrorMapper](references/extension-points.md#5-errormapper---错误映射)

### Context Bag - 中间件间共享状态

使用 `ctx.bag` 在 middleware 间安全地共享状态。详见 [context-bag.md](references/context-bag.md)。

关键用法：
- [创建 Bag Key](references/context-bag.md#创建-bag-key)
- [防止无限循环](references/context-bag.md#2-防止无限循环参考-auth-middleware)
- [跨 Middleware 数据传递](references/context-bag.md#6-跨-middleware-数据传递)

### 测试扩展

详见 [testing-guide.md](references/testing-guide.md) 学习如何测试 middleware 和 plugin。

## 事件系统

支持以下事件：

| 事件名 | Payload | 触发时机 |
|--------|---------|----------|
| `request:start` | `{ req, ctx }` | 请求开始 |
| `request:end` | `{ req, res, ctx, durationMs, attempt }` | 请求成功 |
| `request:error` | `{ req, error, ctx, durationMs, attempt }` | 请求失败（不包括 abort） |
| `request:abort` | `{ req, ctx, durationMs }` | 请求被中止 |

### 使用示例

```ts
client.events.on("request:start", ({ req, ctx }) => {
  console.log(`[${ctx.id}] START ${req.method} ${req.url}`);
});

client.events.on("request:end", ({ req, res, ctx, durationMs, attempt }) => {
  console.log(`[${ctx.id}] END ${res.status} ${req.url} (${durationMs}ms, attempt ${attempt})`);
});

client.events.on("request:error", ({ req, error, ctx, durationMs, attempt }) => {
  console.error(`[${ctx.id}] ERROR ${req.url} (${durationMs}ms)`, error);
});

client.events.on("request:abort", ({ req, ctx, durationMs }) => {
  console.warn(`[${ctx.id}] ABORT ${req.url} (${durationMs}ms)`);
});
```

> 详见 [defaults.md](references/defaults.md#simpleeventbus) 了解事件总线的完整实现。

## 创建客户端工厂函数

`createClient()` 是 `new RequestClient()` 的别名：

```ts
import { createClient } from "@aptx/api-core";

const client = createClient({
  baseURL: "/api",
  timeoutMs: 10_000,
});
```

  适用于偏好函数式编程的场景。

## 常见问题

详见 [faq.md](references/faq.md) 查看完整 FAQ，包括：
- Request headers 没有被修改？
- Progress 回调没有触发？
- 如何区分超时和用户取消？
- 如何防止 auth middleware 无限重试？
- 何时使用 Middleware vs Plugin？
- 如何在 middleware 间共享数据？
- 如何测试自定义 middleware？
- Response 数据类型不对怎么办？
- 如何自定义 JSON 序列化？
