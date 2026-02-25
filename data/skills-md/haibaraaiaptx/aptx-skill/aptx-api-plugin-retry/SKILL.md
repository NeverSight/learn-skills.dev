---
name: aptx-api-plugin-retry
description: "使用 @aptx/api-plugin-retry 实现请求重试。用于：配置重试次数、设置固定或动态延迟策略、定义 retryOn 判定函数（NetworkError/TimeoutError）、防止非幂等请求重试、跟踪重试次数、createRetryMiddleware API。当代码需要重试功能或 createRetryMiddleware 时触发。"
---

# aptx-api-plugin-retry

## 安装

```bash
pnpm add @aptx/api-plugin-retry
```

## API 接口

```ts
interface RetryOptions {
  retries: number;  // 重试次数（不含首次请求）
  delayMs?: number | ((attempt: number, error: Error, req: Request, ctx: Context) => number);
  retryOn?: (error: Error, req: Request, ctx: Context) => boolean;
}

function createRetryMiddleware(options: RetryOptions): Middleware;
```

## 单次调用覆盖（Per-call Override）

`@aptx/api-plugin-retry` 支持通过 `req.meta.__aptxRetry` 对单次调用覆盖重试行为（无需在运行时层重复实现重试逻辑）。

```ts
// 禁用本次调用重试
meta: { __aptxRetry: { retries: 0 } }

// 或显式 disable（优先级最高）
meta: { __aptxRetry: { disable: true } }
```

规则：
- override 只影响当前 `Request`。
- 若同时配置了全局 `createRetryMiddleware({ retries })`，override 以 `req.meta.__aptxRetry` 为准。
- 建议生成器封装一个 helper，例如 `retryMeta({ retries: 0 })`，避免业务直接写魔法字段。

### 参数说明

- **retries**: 重试次数，`retries: 2` 表示总尝试次数 = 首次请求 + 2次重试 = 3次
- **delayMs**: 固定延迟或动态延迟函数，函数接收 `(attempt, error, req, ctx)` 四个参数
- **retryOn**: 判断是否重试的函数，接收 `(error, req, ctx)` 三个参数

## ctx.attempt 语义

- 首次请求时 `ctx.attempt = 0`
- 每次重试前递增（第一次重试 `ctx.attempt = 1`）
- 当 `ctx.attempt === retries` 时为最后一次尝试
- 可用于实现"仅在首次失败时重试"等逻辑

## 在接入重试插件时，按以下步骤执行：

1. 使用 `createRetryMiddleware({ retries, delayMs, retryOn })` 并通过 `client.use()` 挂载到 `RequestClient`。重试中间件应位于管道前端。
2. 明确 `retryOn` 规则，利用 `req.method`、`req.url` 等上下文信息，避免对业务错误或不可重试请求无差别重试。
3. 把指数退避、抖动策略放到 `delayMs` 函数里实现，不修改 core。
4. 保持 `ctx.attempt` 可观测，便于定位重试链路。
5. 在测试中覆盖成功重试、放弃重试、延迟重试三类场景。

最小模板：

```ts
import { createRetryMiddleware } from "@aptx/api-plugin-retry";

const retry = createRetryMiddleware({
  retries: 2,  // 总共 3 次尝试（首次 + 2 次重试）
  delayMs: (attempt, error, req, ctx) => attempt * 200,  // 可使用 req 和 ctx 信息
  retryOn: (error, req, ctx) => {
    // 仅对网络错误或超时重试
    const shouldRetry = error.name === "NetworkError" || error.name === "TimeoutError";
    // 可利用请求上下文判断：GET 请求可重试，POST 不重试
    return shouldRetry && req.method === "GET";
  },
});

// 挂载到客户端（重试中间件应位于管道前端）
client.use(retry);
```

## 行为说明

- **延迟处理**: `delayMs` 为 undefined 或 0 时无延迟；负值视为 0
- **错误传播**: 所有重试耗尽后，抛出原始错误（未修改）
- **重试次数**: `retries < 0` 会自动 clamp 为 0

## 风险控制

- **禁止对所有错误无差别重试**：仅在 `retryOn` 满足条件时重试（如 NetworkError、TimeoutError、5xx 状态码）。
- **非幂等写请求默认不重试**：如支付、创建资源等 POST/PUT 请求，除非业务明确允许。
- **重试次数控制**：生产环境建议 `retries <= 3`，避免级联雪崩。
- **超时设置**：配合 `req.timeout` 使用，避免无限等待。
- **管道顺序**：重试中间件应挂载在管道前端，在请求发出前捕获失败。
