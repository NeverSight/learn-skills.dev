---
name: node-best-practices
description: 写 Node.js 后端时使用。异步、错误、依赖与安全的实战规范。
category: language
tags: [node, javascript, 后端]
---

# Node.js 最佳实践

## 何时用

- 写新的 Node.js HTTP 服务、CLI 工具或后台任务时。
- 处理异步流程、设计中间件错误处理时。
- 引入新依赖或做安全加固时。
- Review 代码，发现有混用回调、漏 `await`、阻塞事件循环或配置硬编码时。
- 上线前做安全自查时。

## 核心规则

### 1. 全程 `async`/`await` + `try/catch`；不混用回调，不漏 `await` 导致竞态

**规则：** 所有异步操作统一用 `async`/`await`；禁止在 async 函数中混写 callback 风格；每个 `await` 表达式都必须被 `try/catch` 覆盖或由调用链上的统一错误处理捕获；`await` 不能遗漏——没有 `await` 的 Promise 是悬空的。

**为什么：** AI 生成 Node.js 代码时最常见的错误：`router.get('/user', async (req, res) => { const user = getUser(req.params.id); res.json(user); })`——忘记 `await`，`user` 是一个 Promise 对象而非数据，`res.json` 把 Promise 序列化成 `{}`，请求返回空对象。这类 bug 在简单场景下测试不出来，到了有延迟的生产环境才暴露，且错误信息毫无指向性。

**怎么做：**
- 接收到 callback 风格 API（如旧版 `fs`）→ 用 `util.promisify` 包一层，再 `await`。
- 并行等多个无依赖的 Promise → `await Promise.all([...])` 而非串行多个 `await`。
- `async` 函数内若有 `setTimeout`/`setInterval` 回调，注意内部异常不会自动冒泡，需显式 `try/catch`。

---

### 2. 不阻塞事件循环；CPU 密集任务用 Worker/队列

**规则：** 事件循环线程禁止执行耗时超过几毫秒的 CPU 密集操作（JSON 解析大文件、加密运算、图像处理、复杂正则）；此类任务交给 `worker_threads`、独立进程或异步任务队列（BullMQ、Celery 等）处理。

**为什么：** Node.js 是单线程事件循环，一个同步计算如果耗时 200ms，这 200ms 内所有其他请求都被冻结。AI 常把 `JSON.parse(fs.readFileSync('huge.json'))` 或同步加密写在请求处理函数里——在压测前完全看不出问题，一旦数据量上去，P99 延迟暴涨，整个服务响应停滞。这是 Node.js 最致命的性能陷阱之一。

**怎么做：**
- 大文件解析 → 用流式读取（`fs.createReadStream` + `JSONStream`）或 `Worker`。
- CPU 密集计算（哈希、压缩、图像缩放）→ `worker_threads` 或独立微服务。
- 怀疑阻塞 → 用 `clinic.js` 或 `--prof` 火焰图定位，不凭感觉优化。

---

### 3. 错误统一处理（中间件）；未捕获 rejection 要监听并优雅处理

**规则：** Express/Koa 等框架中必须注册全局错误处理中间件（四参数 `(err, req, res, next)`），所有路由的异步错误通过 `next(err)` 或框架的 async wrapper 汇聚到这里；必须监听 `process.on('unhandledRejection')` 和 `process.on('uncaughtException')`，记录日志后优雅退出（不静默吞掉，也不忽视）。

**为什么：** AI 写 Express 时的典型遗漏：每个路由自己 `catch` 然后 `res.status(500).json({error: e.message})`——错误格式散落各处，有些路由根本没 `catch`，未处理的 rejection 让进程悄悄进入不一致状态继续服务请求。`unhandledRejection` 在 Node.js 15+ 默认会终止进程，但在旧版本只打印警告，AI 生成的代码常假设旧版行为。

**怎么做：**
- Express：async 路由用 `asyncHandler` 包装（自动把 rejection 转成 `next(err)`）；最后注册 `app.use((err, req, res, next) => { ... })` 统一响应。
- `unhandledRejection` → 记录错误、触发优雅关闭（不 `process.exit(1)` 立即硬停，先排空连接池）。
- 区分操作错误（用户输入错误、资源不存在，HTTP 4xx）与程序错误（bug，HTTP 5xx），中间件里按类型返回合适的状态码。

---

### 4. 依赖最小化、锁版本、定期审计；不引入巨型依赖

**规则：** 引入新依赖前评估：标准库或已有依赖能否满足需求？依赖须锁定精确版本（`package-lock.json` 或 `yarn.lock` 提交入库）；定期运行 `npm audit`，高危漏洞须在 CI 中阻断；禁止为一个小功能引入体积巨大或维护不活跃的包。

**为什么：** AI 最容易犯的依赖滥用：为了格式化日期引入 `moment`（343KB，已停止维护），为了生成 UUID 引入一个包（原生 `crypto.randomUUID()` 已够用）。更危险的是引入被投毒或有供应链风险的包——`npm audit` 能发现已知 CVE，但不运行就是零防护。`package-lock.json` 不提交 → 不同环境安装不同版本 → "在我机器上好好的"。

**怎么做：**
- 引入依赖前检查：weekly downloads、最后发布时间、open issues 数量、安全公告。
- CI 中：`npm ci`（不是 `npm install`，严格遵守 lockfile）+ `npm audit --audit-level=high` 失败即阻断。
- 能用 Node.js 内置模块（`crypto`、`path`、`stream`、`url`）解决的，不依赖第三方。

---

### 5. 配置走环境变量；输入校验与安全头（`helmet`）默认开

**规则：** 所有环境相关配置（数据库连接串、密钥、端口、Feature Flag）通过环境变量注入，禁止硬编码在代码或 git 追踪的配置文件中；所有外部输入（HTTP body、query、header）必须通过 schema 校验（Zod/Joi）；HTTP 服务默认启用 `helmet`。

**为什么：** AI 经常在示例代码里直接写 `const DB_URL = "mongodb://admin:password@localhost"`，用户照抄提交入库，密钥泄漏到 GitHub 是 Node.js 生态里最高频的安全事故之一。输入校验缺失则是 NoSQL 注入、原型链污染等攻击的入口——`req.body` 是完全不可信的用户输入，AI 却经常直接 `spread` 进数据库查询。

**怎么做：**
- 配置管理：用 `dotenv` 加载 `.env`（`.env` 加入 `.gitignore`）；生产环境走 Secret Manager/Vault；用 Zod `z.object({DB_URL: z.string().url()})` 在启动时验证必要环境变量，缺失则启动失败而非运行时崩溃。
- 输入校验：`const body = UserSchema.parse(req.body)`，校验失败抛出错误，由全局中间件返回 400。
- `app.use(helmet())` 写在所有路由之前，默认禁止 `X-Powered-By`、开启 `Content-Security-Policy` 等。

---

## 正例 / 反例

### 反例：漏 `await` + 无全局错误处理 + 硬编码密钥

```javascript
// 反例 — 漏 await、密钥硬编码、错误处理散乱
const express = require('express');
const app = express();

const SECRET = "super_secret_key_123";  // ❌ 硬编码密钥

app.get('/user/:id', (req, res) => {    // ❌ 非 async，或 async 但没 try/catch
    const user = User.findById(req.params.id);  // ❌ 漏 await，user 是 Promise
    res.json(user);                             // ❌ 返回 {}
});
// ❌ 没有全局错误处理中间件
```

```javascript
// 正例 — async/await 正确，统一错误处理，配置走环境变量
import express from 'express';
import helmet from 'helmet';
import { z } from 'zod';
import { asyncHandler } from './middleware/asyncHandler.js';

const app = express();
app.use(helmet());          // ✅ 安全头默认开
app.use(express.json());

const ParamSchema = z.object({ id: z.string().uuid() });

app.get('/user/:id', asyncHandler(async (req, res) => {
    const { id } = ParamSchema.parse(req.params);   // ✅ 输入校验
    const user = await User.findById(id);           // ✅ 正确 await
    if (!user) return res.status(404).json({ error: '用户不存在' });
    res.json(user);
}));

// ✅ 全局错误处理中间件
app.use((err, req, res, next) => {
    if (err instanceof z.ZodError) return res.status(400).json({ error: err.issues });
    console.error(err);
    res.status(500).json({ error: '服务器内部错误' });
});
```

---

### 反例：阻塞事件循环处理大文件

```javascript
// 反例 — 同步读取大 JSON，冻结事件循环
app.post('/import', (req, res) => {
    const data = JSON.parse(
        fs.readFileSync('/uploads/huge.json', 'utf8')  // ❌ 同步 I/O，阻塞所有请求
    );
    process(data);
    res.json({ ok: true });
});
```

```javascript
// 正例 — 流式解析，不阻塞事件循环
import { createReadStream } from 'fs';
import JSONStream from 'jsonstream';
import { pipeline } from 'stream/promises';

app.post('/import', asyncHandler(async (req, res) => {
    const results = [];
    await pipeline(
        createReadStream('/uploads/huge.json'),  // ✅ 流式读取
        JSONStream.parse('*'),
        async function* (source) {
            for await (const item of source) {
                results.push(await processItem(item));  // ✅ 逐条处理，不积压内存
            }
        }
    );
    res.json({ count: results.length });
}));
```

---

## 自查清单

- [ ] 所有 `async` 函数中，每个返回 Promise 的调用前都有 `await`？
- [ ] HTTP 服务是否注册了全局错误处理中间件，所有异步路由错误都能汇聚到那里？
- [ ] 有没有在请求处理函数中执行同步 CPU 密集操作（大 JSON、加密、正则）？
- [ ] 监听了 `process.on('unhandledRejection')` 并做了日志记录 + 优雅退出？
- [ ] 所有密钥、连接串、端口配置都走环境变量，不硬编码在代码或 git 追踪文件里？
- [ ] 外部输入（body、query、params）是否经过 schema 校验才使用？
- [ ] `helmet()` 是否在所有路由之前挂载，`npm audit` 在 CI 中有没有对高危漏洞阻断？
