---
name: aptx-token-store
description: "使用 @aptx/token-store 定义或实现 token 持久化。用于：实现 TokenStore 接口、支持同步/异步 API（getToken/setToken/clearToken）、可选的元数据方法、实现不同存储后端（cookie、localStorage、小程序、内存）、配合 @aptx/api-plugin-auth 使用。当代码需要实现自定义 TokenStore 时触发。"
---

# aptx-token-store

## 核心规范

在实现 token 存储抽象时，按以下规范执行：

1. 实现 `TokenStore` 的最小能力：`getToken`、`setToken`、`clearToken`。
2. 若需要过期控制，提供 `getMeta/setMeta` 或 `getRecord/setRecord`，并确保 `meta.expiresAt` 可读取。
3. 保持实现无业务耦合，不包含请求逻辑，不依赖 `@aptx/api-core`。
4. 把环境相关能力放到独立包中（如 cookie、小程序、内存）。
5. 以 `@aptx/api-plugin-auth` 作为主要消费方进行联调测试。
6. 所有方法必须保持同步/异步一致性，不可混用。

## 接口定义

```ts
import type { TokenStore, TokenMeta, TokenRecord } from '@aptx/token-store';

interface TokenStore {
  // 核心方法（必须实现）
  getToken(): string | undefined | Promise<string | undefined>;
  setToken(token: string, meta?: TokenMeta): void | Promise<void>;
  clearToken(): void | Promise<void>;

  // 可选方法（支持过期控制）
  getMeta?(): TokenMeta | undefined | Promise<TokenMeta | undefined>;
  setMeta?(meta: TokenMeta): void | Promise<void>;
  getRecord?(): TokenRecord | undefined | Promise<TokenRecord | undefined>;
  setRecord?(record: TokenRecord): void | Promise<void>;
}

interface TokenMeta {
  expiresAt?: number;  // 时间戳（毫秒）
  [key: string]: unknown;
}

interface TokenRecord {
  token?: string;
  meta?: TokenMeta;
}
```

## 实现检查清单

- [ ] 实现了 `getToken()`、`setToken()`、`clearToken()` 三个核心方法
- [ ] 如需过期控制，实现了 `getMeta()/setMeta()`（或 `getRecord()/setRecord()`）
- [ ] `meta.expiresAt` 支持时间戳格式（毫秒）
- [ ] 所有方法保持同步/异步一致性（不可混用）
- [ ] `clearToken()` 同时清除 token 和 meta 数据
- [ ] 不依赖 `@aptx/api-core` 或请求库
- [ ] 实现了 `TokenStoreFactory.create()`（如果需要配置）

## 同步/异步选择规则

| 场景 | 推荐 | 理由 |
|------|------|------|
| localStorage/sessionStorage | 同步 | 阻塞时间极短 |
| cookie (js-cookie) | 同步 | 内存操作 |
| IndexedDB | 异步 | I/O 操作 |
| 网络请求 | 异步 | 必须异步 |
| 内存存储 | 同步 | 无 I/O |
| 小程序存储 (wx.getStorageSync) | 同步 | 同步 API 更可靠 |

**重要原则：** 所有方法必须保持同步/异步一致性，不可混用。

## 实现指南

### 详细实现示例

完整的实现示例请参考：

- [最小实现（无过期控制）](references/implementations.md#最小实现无过期控制)
- [完整实现（带过期管理）](references/implementations.md#完整实现带过期管理)
- [Cookie 实现](references/implementations.md#cookie-实现)
- [LocalStorage 实现](references/implementations.md#localstorage-实现)
- [小程序实现](references/implementations.md#小程序实现)
- [内存实现（仅用于测试）](references/implementations.md#内存实现仅用于测试)
- [TokenStoreFactory 模式](references/implementations.md#tokenstorefactory-模式)

### TokenStoreFactory 模式

当实现需要配置时，使用 Factory 模式：

```ts
import type { TokenStoreFactory } from '@aptx/token-store';

// 定义配置接口
export interface YourStoreOptions {
  tokenKey?: string;
  metaKey?: string;
  prefix?: string;
}

// 实现类
class YourTokenStore implements TokenStore {
  constructor(private options: YourStoreOptions) {
    this.tokenKey = options.tokenKey ?? 'aptx_token';
    this.metaKey = options.metaKey ?? 'aptx_token_meta';
    this.prefix = options.prefix ?? '';
  }

  private readonly tokenKey: string;
  private readonly metaKey: string;
  private readonly prefix: string;

  // ... 实现 TokenStore 方法
}

// Factory 函数
export const createYourTokenStore: TokenStoreFactory<YourStoreOptions>["create"] = (
  options: YourStoreOptions = {}
) => {
  return new YourTokenStore(options);
};
```

## 与 @aptx/api-plugin-auth 集成

### 基本集成模式

```ts
import { createAuthMiddleware } from '@aptx/api-plugin-auth';

client.use(createAuthMiddleware({
  store,                      // 你的 TokenStore 实现
  refreshLeewayMs: 60_000,   // 提前60秒刷新
  refreshToken: async () => {
    // 返回格式1：完整对象（推荐）
    return {
      token: 'new-token',
      expiresAt: Date.now() + 30 * 60 * 1000  // 30分钟后过期
    };

    // 或返回格式2：仅 token（不自动设置 expiresAt）
    // return 'new-token';
  },
}));
```

### 集成要求

- **必须实现：** `getToken()` - 读取 token 用于请求
- **必须实现：** `setToken()` - 保存刷新后的 token
- **必须实现：** `clearToken()` - 刷新失败时清除无效 token
- **推荐实现：** `getMeta()` - 支持 `expiresAt` 读取（主动刷新）
- **推荐实现：** `setMeta()` - 支持 `expiresAt` 写入

### 更多集成详情

完整的集成指南和示例请参考 [references/integration.md](references/integration.md)，包括：

- api-plugin-auth 的关键调用逻辑
- 常见集成场景（localStorage、Cookie、小程序、测试）
- 同步/异步集成注意事项
- 调试技巧

## 测试

### 测试模式

测试相关的内容请参考 [references/test-patterns.md](references/test-patterns.md)，包括：

- Mock 存储模式
- 使用内存存储进行测试
- 完整的测试用例示例

### 实现注意事项

实现过程中的注意事项请参考 [references/test-patterns.md#实现注意事项](references/test-patterns.md#实现注意事项)，包括：

- 错误处理（localStorage 超限、cookie 禁用等）
- 类型安全（使用完整类型定义）
- 性能考虑（避免阻塞、并发控制）
- 安全性（Cookie 配置、敏感信息加密、XSS 防护）
