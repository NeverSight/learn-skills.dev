---
name: bmob-database-javascript
description: "Use when implementing Bmob NoSQL database CRUD with the cross-platform hydrogen-js-sdk (3.0+ supports both Secret Key + API 安全码 and Application ID + REST API Key init) — ONE SDK file (Bmob-x.x.x.min.js) covers ALL of: browser, Node.js, WeChat Mini Program, Alipay / ByteDance / QQ / Baidu Mini Programs, Quick App 快应用, Cocos Creator JS, Electron, Tauri, hybrid apps, and any ES6 framework (Vue2 / Vue3 / React / Next.js / Vite / Nuxt). Triggers: Bmob.initialize, Bmob.Query, Bmob.User, Bmob.Pointer, Bmob.GeoPoint, Bmob.Relation, hydrogen-js-sdk, npm install hydrogen-js-sdk, import Bmob from 'hydrogen-js-sdk', 微信小程序 Bmob, Cocos Creator Bmob, query.find, query.set, query.save, query.destroy, query.equalTo. NOT for Android native (use bmob-database-android), iOS native (use bmob-database-ios), Flutter / Dart (use bmob-database-flutter), curl / Python / Go / PHP / C# (use bmob-database-restful), or C++ Cocos2d-x (separate skill). If Bmob MCP is configured in the project, call get_project_tables first via bmob-mcp before writing code."
metadata:
  author: bmob
  version: "0.1.0"
  sdk: "hydrogen-js-sdk"
  sdk_repo: "https://github.com/bmob/hydrogen-js-sdk"
  docs: "https://github.com/bmob/BmobDocs/blob/master/mds/data/wechat_app_new/index.md"
  docs_raw: "https://raw.githubusercontent.com/bmob/BmobDocs/master/mds/data/wechat_app_new/index.md"
  docs_api_ref: "https://raw.githubusercontent.com/bmob/BmobDocs/master/mds/data/javascript/develop_doc.md"
---

# Bmob Database — JavaScript / 跨端 SDK

[hydrogen-js-sdk](https://github.com/bmob/hydrogen-js-sdk) 是 **同一个 SDK 文件 `Bmob-<version>.min.js`** 支持以下所有宿主环境，无平台分支代码：

- 浏览器 / 任何 Web 前端（React、Vue 2、Vue 3、Next.js、Nuxt、Vite、Astro、SvelteKit、Solid 等）
- Node.js 服务端（必须源码引入）
- 微信小程序 / 支付宝 / 字节跳动 / QQ / 百度 小程序
- 快应用
- Cocos Creator JS
- Electron / Tauri
- 任意混合 App（WebView 内嵌 H5）

> **本 skill 只覆盖新版 hydrogen-js-sdk**（`Bmob.Query('X')` Promise 风格，3.0+）。基于 Backbone.js 的旧 `bmob-min.js`（`Bmob.Object.extend("X")` callback 风格）**不要用，也不要回退**。

## 核心原则

**1. 初始化支持两种方式**（hydrogen-js-sdk **3.0+** 均兼容；按场景二选一，**不要混用**）：

**方式 A — Secret Key + API 安全码**（**推荐**：浏览器 / 小程序 / 公开客户端，SDK 内部走加密授权）：

```js
Bmob.initialize("你的Secret Key", "你的API 安全码");
```

- **Secret Key**：控制台 → 应用 → 设置 → 应用密钥 → **Secret Key**。
- **API 安全码**：控制台 → 应用 → 应用功能设置 → 安全验证 → **API 安全码** 自行设置。

**方式 B — Application ID + REST API Key**（3.0 起正式兼容；适合已有 1.x/2.x 项目迁移、或与服务端 REST 共用同一套 Key）：

```js
Bmob.initialize("你的Application ID", "你的REST API Key");
```

- **Application ID** / **REST API Key**：控制台 → 应用 → 设置 → 应用密钥 同一页。
- REST API 请求域名一般为 `https://api.codenow.cn`（见 [`bmob-database-restful`](../bmob-database-restful/SKILL.md)）。

> 2.x 时代方式 B 功能受限；**3.0+ 两种初始化等价可用**。公开 bundle 仍优先方式 A（REST API Key 可被抓包）。

**2. 不要 commit 真实密钥进 git；CDN / dist 不要写死 SDK 版本号。** 密钥用环境变量（Vite `import.meta.env.VITE_BMOB_*`、Next.js `process.env.NEXT_PUBLIC_BMOB_*`、小程序构建期注入等）。dist 文件名为 `Bmob-<version>.min.js`，有打包工具时用 `npm install hydrogen-js-sdk`；纯 CDN 浏览器场景用 jsDelivr API 动态取 `tags.latest` 再拼 URL（见 [`references/platform-init.md`](references/platform-init.md)）。**禁止**在示例里写 `@2.7.3` 这类会过期的具体版本。

**3. 默认查询返回 100 条**，最大 1000。需要更多用 `skip + limit` 分页或走 BQL（`bmob-bql` skill）。

**4. 三个保留字段不能手动写入**：`objectId`、`createdAt`、`updatedAt`。读 objectId 时用 `res.objectId`（不是 `id`）。

**5. 时间字段比较的精度**：`createdAt` / `updatedAt` 在服务器是微秒精度，应用层做时间比较时要 +1 秒。

## 安全清单

- [ ] **密钥分级**：浏览器 / 小程序 / 移动端优先 **Secret Key + API 安全码**（方式 A），**永不用 Master Key**。若用 Application ID + REST API Key（方式 B），REST API Key 会暴露在 bundle 中。
- [ ] **生产环境关闭调试模式**：`Bmob.debug(true)` 仅在小程序开发时使用，上线前删掉。
- [ ] **小程序必须配置服务器域名白名单**：微信后台 `request` 合法域名至少添加 `https://api.bmobcloud.com`（见 [`references/platform-init.md`](references/platform-init.md) 微信小程序段）。
- [ ] **微信小程序若使用 npm 引入 SDK，需先在开发者工具执行“工具 --> 构建 npm”**：未构建时 `import Bmob from "hydrogen-js-sdk"` 不会生效。
- [ ] **写入的表必须配 ACL**：否则任意用户可改任意行。参见 `bmob-acl-and-roles`（P1）。
- [ ] **批量操作上限 50 条**（含批量更新、批量删除）。超出需循环。
- [ ] **批量查询上限 100 条 / 单次 1000 条**：避免一次拉全表。
- [ ] **`Bmob.User.login` 在小程序里要先调用 `wx.login()`** 获取 code，否则会话拿不到 sessionToken。

## 常见问题

跨平台 Q&A：[`shared/faq.md`](../../shared/faq.md)（路由、密钥、MCP、Pointer 格式等）。

## 反模式

见 [`shared/anti-patterns.md`](../../shared/anti-patterns.md)。本端重点：勿混用旧版 `Bmob.Object.extend`；勿混用两种 `initialize`；Node 勿用压缩版入口。

## 快速开始（80% 场景就这么写）

### 初始化

默认推荐 **方式 A**（Secret Key + API 安全码）；3.0+ 亦可用 **方式 B**（Application ID + REST API Key），见上方核心原则。

```js
import Bmob from "hydrogen-js-sdk";
Bmob.initialize("你的Secret Key", "你的API 安全码");
// 或：Bmob.initialize("你的Application ID", "你的REST API Key");
```

详细的 8 种宿主环境引入方式见 [`references/platform-init.md`](references/platform-init.md)。

### 新增一行

```js
const query = Bmob.Query("GameScore");
query.set("score", 1337);
query.set("playerName", "bmob");
query.set("cheatMode", false);
query.save().then((res) => {
  console.log(res.objectId, res.createdAt);
});
```

### 通过 objectId 取一行

```js
const query = Bmob.Query("GameScore");
query.get("7ecd253a25").then((res) => {
  console.log(res);
});
```

### 修改一行

```js
const query = Bmob.Query("GameScore");
query.set("id", "7ecd253a25");          // 注意 set("id", objectId)
query.set("score", 9999);
query.save().then((res) => {
  console.log(res.updatedAt);
});
```

### 删除一行

```js
const query = Bmob.Query("GameScore");
query.destroy("7ecd253a25").then((res) => {
  console.log(res);                      // { msg: "ok" }
});
```

### 删除某个字段的值

```js
const query = Bmob.Query("GameScore");
query.get("7ecd253a25").then((res) => {
  res.unset("cover");
  res.save();
});
```

### 查询全部（默认 100 条）

```js
const query = Bmob.Query("GameScore");
query.find().then((res) => {
  console.log(res);
});
```

### 条件查询

`equalTo(field, op, value)`，`op` 可以是 `"=="` / `"!="` / `">"` / `">="` / `"<"` / `"<="`。

```js
const query = Bmob.Query("GameScore");
query.equalTo("score", ">", 100);
query.equalTo("cheatMode", "==", false);   // 多个条件 = AND
query.limit(20);
query.skip(0);
query.order("-score");                      // 降序
query.find().then(console.log);
```

### 或查询（OR）

```js
const query = Bmob.Query("GameScore");
const q1 = query.equalTo("score", ">", 150);
const q2 = query.equalTo("score", "<", 5);
query.or(q1, q2);
query.find().then(console.log);
```

### 只取部分字段

```js
const query = Bmob.Query("Post");
query.select("title");
query.find().then(console.log);
```

### 集合查询

```js
query.containedIn("playerName", ["Bmob", "Codenow", "JS"]);
query.notContainedIn("playerName", ["spam"]);
query.exists("score");           // 含此字段
query.doesNotExist("score");     // 不含此字段
```

### 统计

```js
const query = Bmob.Query("diary");
query.count().then((n) => console.log(`共 ${n} 条`));
query.count(100).then((arr) => console.log("最多返回 100 条记录数据 + count"));
```

### 原子计数器

```js
const query = Bmob.Query("Post");
query.get("objectId").then((res) => {
  res.increment("likes");        // +1
  res.increment("likes", 5);     // +5（支持负数）
  res.save();
});
```

### 数组字段

```js
const query = Bmob.Query("Diary");
query.add("DiaryType", ["public"]);          // 末尾追加
query.addUnique("DiaryType", ["secret"]);    // 去重追加
query.save();

query.get("objectId").then((res) => {
  res.remove("DiaryType", ["secret"]);       // 删除元素
  res.save();
});
```

## 进阶能力（按需读 references/）

| 主题 | 路径 |
|---|---|
| 端到端场景（博客、小程序登录、Todo ACL 等） | [`shared/recipes/`](../../shared/recipes/) |
| 8 种宿主环境的初始化差异（浏览器 / Node / 微信/支付宝/字节/QQ/百度小程序 / 快应用 / Cocos Creator / Electron） | [`references/platform-init.md`](references/platform-init.md) |
| BmobDocs 同步代码片段 | [`references/snippets/`](references/snippets/) |
| Pointer / Relation 一对多 / 多对多 | [`references/pointer-and-relation.md`](references/pointer-and-relation.md) |
| 复杂子查询（`$inQuery` / `$notInQuery`）、模糊查询、地理位置查询 | [`references/query.md`](references/query.md) |
| 实时数据订阅（仅小程序 / Web）+ WebSocket | [`references/realtime.md`](references/realtime.md) |
| 批量操作（≤ 50） | [`references/batch.md`](references/batch.md) |

## 与 MCP 联动

如果用户在 IDE 里配置了 [Bmob MCP](../bmob-mcp/SKILL.md)，**写代码前先调用 `get_project_tables`** 拿到真实 schema，避免：

- 字段名拼错（schemaless 不报错，数据进库后再排查很慢）
- Pointer 字段类型用错（必须是 `{"__type":"Pointer","className":"X","objectId":"..."}`）
- 把保留字段当业务字段写

```mermaid
sequenceDiagram
    autonumber
    participant Dev as Developer
    participant Agent as Agent
    participant MCP as bmob-mcp
    participant Code as bmob-database-javascript
    Dev->>Agent: "Next.js 项目里加 Bmob 文章列表"
    Agent->>MCP: get_project_tables()
    MCP-->>Agent: {Article: {title:String, content:String, author:Pointer(_User)}}
    Agent->>Code: 按真实 schema 生成 Bmob.Query("Article") 代码
    Code-->>Dev: 完整可运行代码（含 ACL 提示）
```

## 排错速查

跨平台现象先查 [`shared/faq.md`](../../shared/faq.md)。

| 现象 | 排查 |
|---|---|
| `Bmob is undefined` | 没引入 SDK；或 Node.js 用了压缩版（必须用源码 `require('hydrogen-js-sdk/src/lib/app.js')`） |
| 初始化报 401 | 方式 A：Secret Key 或 API 安全码与控制台不一致；方式 B：Application ID 或 REST API Key 错；或两种方式的参数混用（例如用 Application ID 当 Secret Key 传） |
| 写入成功但字段值不见 | 字段名拼错（schemaless 不报错）；先 `get_project_tables` 比对 |
| 查询返回数据少 | 默认 100 条上限；用 `query.limit(1000)` 或分页 |
| `set("id", ...)` 没生效 | 更新时必须用 `set("id", objectId)`（不是 `set("objectId", ...)`） |
| 时间范围查询少一条 | 服务端时间是微秒精度，区间右端 +1 秒 |
| 小程序请求失败 | 先检查微信后台 `request` 合法域名是否已添加 `https://api.bmobcloud.com`；若 SDK 是 npm 引入，还要在微信开发者工具执行“工具 --> 构建 npm”后再编译运行 |
| Promise 一直 pending | 调用了不存在的方法名（hydrogen 不抛错只挂起）；对照 [完整 API](https://github.com/bmob/BmobDocs/blob/master/mds/data/wechat_app_new/index.md) |
| 9015 报错 | 见 [`bmob-error-codes`](../bmob-error-codes/SKILL.md) 的 9015 专题 |

## 参考

- 完整 API：[BmobDocs/mds/data/wechat_app_new/index.md](https://github.com/bmob/BmobDocs/blob/master/mds/data/wechat_app_new/index.md) — 跨端 hydrogen-js-sdk 主文档
- 旧版 API 参考（仍在线）：[BmobDocs/mds/data/javascript/develop_doc.md](https://github.com/bmob/BmobDocs/blob/master/mds/data/javascript/develop_doc.md)
- SDK 源码：<https://github.com/bmob/hydrogen-js-sdk>
- 错误码：[`bmob-error-codes`](../bmob-error-codes/SKILL.md)
- MCP 联动：[`bmob-mcp`](../bmob-mcp/SKILL.md)
