---
name: bmob-database-restful
description: "Use when interacting with Bmob backend cloud over plain HTTP / curl from ANY language that lacks a Bmob SDK — Python (requests/httpx), Go (net/http), PHP (Guzzle), C# (HttpClient), Rust (reqwest), Ruby, Java backend, Bash, Deno, server-side scripting, data migration. Also use when the user explicitly wants curl or the raw REST API URL pattern. API base domain: https://api.codenow.cn (e.g. /1/classes/Token). Triggers: /1/classes/, /1/users, /1/batch, /1/cloudQuery, /1/timestamp, /1/requestSmsCode, X-Bmob-Application-Id, X-Bmob-REST-API-Key, X-Bmob-Safe-Sign, simple auth, encrypted auth, MD5 signature, curl bmob, Bmob REST API, Bmob HTTP. NOT for JavaScript / Node / Web / Mini Program (use bmob-database-javascript), Android (use bmob-database-android), iOS (use bmob-database-ios), or Flutter / Dart (use bmob-database-flutter). If Bmob MCP is configured, generate_code MCP tool can emit ready-to-use curl for 13 operation types — prefer it over hand-writing curl."
metadata:
  author: bmob
  version: "0.1.0"
  docs: "https://github.com/bmob/BmobDocs/blob/master/mds/data/restful/develop_doc.md"
  docs_raw: "https://raw.githubusercontent.com/bmob/BmobDocs/master/mds/data/restful/develop_doc.md"
---

# Bmob Database — REST API

Bmob REST API 是 **跨语言、跨平台** 的通用接入方式：任何能发 HTTP 请求的环境都能用，不依赖任何 SDK。典型用法包括 Python/Go/PHP/C#/Rust/Ruby/Java 后端、数据迁移脚本、Bash one-liner、Deno Edge Functions、Serverless 函数等。

## 核心原则

**1. URL 形态固定：** 所有接口在 `https://api.codenow.cn/1/`（Bmob 控制台 → 应用 → 设置 → 配置 中显示的 API 域名，一般为 `api.codenow.cn`）。版本号 `/1/` 必须保留。

示例：`https://api.codenow.cn/1/classes/Token` — 对 `Token` 表做 CRUD 时路径即 `/1/classes/Token`。

```
POST   /1/classes/<TableName>              # 新增
GET    /1/classes/<TableName>/<objectId>   # 查单条
GET    /1/classes/<TableName>              # 查列表 / 条件查询
PUT    /1/classes/<TableName>/<objectId>   # 更新
DELETE /1/classes/<TableName>/<objectId>   # 删除
POST   /1/batch                            # 批量（≤ 50 条）
GET    /1/cloudQuery                       # BQL 查询
POST   /1/users                            # 注册
POST   /1/login                            # 登录
POST   /2/files/<fileName>                 # 上传文件
GET    /1/timestamp                        # 服务器时间
```

完整快速参考见 [`references/url-cheatsheet.md`](references/url-cheatsheet.md)。

**2. 两种鉴权方式，均可用**（与 hydrogen-js-sdk **3.0+** 的两种 `Bmob.initialize` 对应）：

- **简易授权 — Application ID + REST API Key**（REST 原生方式；JS SDK **方式 B** 即走此通道）：Header `X-Bmob-Application-Id` + `X-Bmob-REST-API-Key`。适合服务端、内网脚本、与 SDK 方式 B 共用同一套 Key 的项目。详见 [shared/auth-headers.md](../../shared/auth-headers.md)。
- **加密授权 — Secret Key + API 安全码签名**（JS SDK **方式 A** 走此通道；也可手写 REST）：6 个头部 + MD5 签名。适合浏览器 / 小程序直接调 REST、且不想在 Header 里暴露 REST API Key 的场景。详见 [shared/md5-sign-algo.md](../../shared/md5-sign-algo.md)。

> 2.x 文档曾暗示前端「禁止」Application ID + REST API Key；**当前两种鉴权在全端均可正常使用**。公开 bundle 中 REST API Key 仍可被抓包，故公开端仍**推荐**优先 SDK 方式 A 或加密授权，而非硬性禁止方式 B。

**3. POST/PUT 必须 `Content-Type: application/json`**，body 用 JSON。Bmob REST 不支持 form-urlencoded。

**4. GET 的 query 必须 URL encode**：`where` / `order` / `limit` / `skip` / `include` / `keys` / `count` 都通过 query string 传，含 `{` / `:` 等字符必须 encode。

**5. 默认查询返回 10 条**，最大 1000。需要更多用 `skip` + `limit` 分页或 `count=1`。

## 安全清单

- [ ] **前端接入优先级**：浏览器 / 小程序优先 [`bmob-database-javascript`](../bmob-database-javascript/SKILL.md) SDK（3.0+ 支持 Secret Key **或** Application ID 两种初始化）；若必须手写 REST，公开端优先加密授权或自建 BFF。
- [ ] **Application ID + REST API Key 可用**：不再禁止在前端或 SDK 中使用此组合（对应 SDK 方式 B / REST 简易授权）；注意 REST API Key 会出现在请求头中，抓包后可复用。
- [ ] **服务端代码里 Key 用环境变量**：不要硬编码到源码、不 commit 到公开仓库。
- [ ] **Master Key 仅用于服务端**：通过 `X-Bmob-Master-Key` 头部使用，**不要**给前端。
- [ ] **写操作的表必须配 ACL**：见 `bmob-acl-and-roles`（P1）；REST 创建对象时 body 里加 `"ACL": {...}` 即可。
- [ ] **生产用 HTTPS**：你的 API domain 必须是 https，否则 Header 里的 Key 会明文传输。
- [ ] **批量上限 50 条 / 请求**：`/1/batch` 单次最多 50 个子请求。

## 常见问题

跨平台 Q&A：[`shared/faq.md`](../../shared/faq.md)。

## 反模式

见 [`shared/anti-patterns.md`](../../shared/anti-patterns.md)。本端重点：Master Key 仅服务端；公开端优先加密授权或 SDK，勿裸奔 REST Key。

## 五大基础操作（简易授权 + curl）

公共头部（所有请求都要带，下方示例不再重复）：

```
X-Bmob-Application-Id: <your-application-id>
X-Bmob-REST-API-Key:   <your-rest-api-key>
Content-Type:          application/json
```

### 添加数据

```bash
curl -X POST 'https://api.codenow.cn/1/classes/GameScore' \
  -H "X-Bmob-Application-Id: <id>" \
  -H "X-Bmob-REST-API-Key:   <key>" \
  -H "Content-Type: application/json" \
  -d '{"score":1337,"playerName":"Sean Plott","cheatMode":false}'
```

成功 `201 Created` + body：

```json
{ "createdAt": "2011-08-20 02:06:57", "objectId": "e1kXT22L" }
```

### 查询单条

```bash
curl -X GET 'https://api.codenow.cn/1/classes/GameScore/e1kXT22L' \
  -H "X-Bmob-Application-Id: <id>" \
  -H "X-Bmob-REST-API-Key:   <key>"
```

### 查询列表（条件 + 分页 + 排序）

```bash
curl -X GET 'https://api.codenow.cn/1/classes/GameScore' \
  -H "X-Bmob-Application-Id: <id>" \
  -H "X-Bmob-REST-API-Key:   <key>" \
  -G \
  --data-urlencode 'where={"score":{"$gt":100}}' \
  --data-urlencode 'limit=20' \
  --data-urlencode 'skip=0' \
  --data-urlencode 'order=-createdAt' \
  --data-urlencode 'count=1'
```

返回：

```json
{
  "results": [ /* ... */ ],
  "count":   123
}
```

完整 `where` 运算符列表（`$gt` / `$lt` / `$in` / `$nin` / `$exists` / `$regex` / `$inQuery` / `$or` …）见 [`references/query-where-syntax.md`](references/query-where-syntax.md)。

### 更新

```bash
curl -X PUT 'https://api.codenow.cn/1/classes/GameScore/e1kXT22L' \
  -H "X-Bmob-Application-Id: <id>" \
  -H "X-Bmob-REST-API-Key:   <key>" \
  -H "Content-Type: application/json" \
  -d '{"score":73453}'
```

### 删除

```bash
curl -X DELETE 'https://api.codenow.cn/1/classes/GameScore/e1kXT22L' \
  -H "X-Bmob-Application-Id: <id>" \
  -H "X-Bmob-REST-API-Key:   <key>"
```

## 原子计数器

```bash
curl -X PUT 'https://api.codenow.cn/1/classes/Post/abc' \
  -H "Content-Type: application/json" \
  ...
  -d '{"likes":{"__op":"Increment","amount":1}}'
```

`amount` 支持负数。

## 批量操作（≤ 50）

```bash
curl -X POST 'https://api.codenow.cn/1/batch' \
  -H "Content-Type: application/json" \
  ...
  -d '{
    "requests": [
      { "method": "POST",   "path": "/1/classes/GameScore",     "body": { "score": 1 } },
      { "method": "PUT",    "path": "/1/classes/GameScore/aaa", "body": { "score": 9 } },
      { "method": "DELETE", "path": "/1/classes/GameScore/bbb" }
    ]
  }'
```

每个子请求独立成功/失败，**不会回滚**。

## 数据类型：Pointer / Relation / Date / File / GeoPoint

REST 通过 `__type` 字段标识特殊类型：

```jsonc
{
  // Pointer：一对多
  "author":   { "__type": "Pointer",   "className": "_User",   "objectId": "abc" },

  // Date：日期（注意服务器存的格式）
  "publishedAt": { "__type": "Date",   "iso": "2024-08-21 18:02:52" },

  // File：上传后返回的结构原样存
  "cover":    { "__type": "File",      "group": "group1", "filename": "1.jpg", "url": "M00/01/14/x.jpg" },

  // GeoPoint：地理位置
  "location": { "__type": "GeoPoint",  "latitude": 23.05, "longitude": 113.40 },

  // Relation：多对多（实际操作通过 __op AddRelation / RemoveRelation）
  "likedBy":  { "__type": "Relation",  "className": "_User" }
}
```

详见 [`references/data-types.md`](references/data-types.md)。

## 用户系统

```bash
# 注册
curl -X POST 'https://api.codenow.cn/1/users' \
  -H "Content-Type: application/json" \
  ... \
  -d '{"username":"hello","password":"pwd123","email":"x@y.com"}'

# 登录（必须用 GET，参数走 query）
curl -X GET 'https://api.codenow.cn/1/login' \
  -H "Content-Type: application/json" \
  ... \
  -G \
  --data-urlencode 'username=hello' \
  --data-urlencode 'password=pwd123'

# 拿当前用户（带上 X-Bmob-Session-Token）
curl -X GET 'https://api.codenow.cn/1/users/<objectId>' \
  -H "X-Bmob-Session-Token: <session-token>" \
  ...
```

完整用户系统接口见 [`references/users.md`](references/users.md)。

## 文件上传

走独立的 `/2/files/` 端点，body 是文件二进制：

```bash
curl -X POST 'https://api.codenow.cn/2/files/cover.jpg' \
  -H "X-Bmob-Application-Id: <id>" \
  -H "X-Bmob-REST-API-Key:   <key>" \
  -H "Content-Type: image/jpeg" \
  --data-binary @/path/to/cover.jpg
```

详见 [`references/files.md`](references/files.md)。

## 加密授权

浏览器 / 小程序**直接调用 REST**（不经 SDK）时，**推荐**加密授权；Application ID + REST API Key 简易授权同样可用（与 SDK 3.0 方式 B 一致），但 REST API Key 更易被抓包。签名规则：

```
sign = md5(url + timeStamp + SecurityCode + noncestr + body + SDKVersion)
```

完整 6 个头部、签名拼接顺序、Node 参考实现见 [shared/md5-sign-algo.md](../../shared/md5-sign-algo.md)。

## 多语言客户端示例

| 语言 | 示例 |
|---|---|
| Python（requests） | [`references/lang-snippets/python.md`](references/lang-snippets/python.md) |
| Go（net/http） | [`references/lang-snippets/go.md`](references/lang-snippets/go.md) |
| PHP（Guzzle） | [`references/lang-snippets/php.md`](references/lang-snippets/php.md) |
| C#（HttpClient） | [`references/lang-snippets/csharp.md`](references/lang-snippets/csharp.md) |

## 与 MCP 联动

如果用户配置了 [Bmob MCP](../bmob-mcp/SKILL.md)，**`generate_code` 工具能直接生成 curl**，覆盖 13 种 type（添加 / 删除 / 更新 / 条件查询 / 注册 / 登录 / SMS / 云函数 / 文件上传等）。优先调用它而不是手写 curl——这样能确保 URL pattern / Header / where 语法都是当前服务器最新版本。

## 进阶参考

| 主题 | 路径 |
|---|---|
| 端到端场景（迁移、文件、ACL 等） | [`shared/recipes/`](../../shared/recipes/) |
| BmobDocs 同步代码片段 | [`references/snippets/`](references/snippets/) |
| where 语法 | [`references/query-where-syntax.md`](references/query-where-syntax.md) |
| 用户 / 文件 | [`references/users.md`](references/users.md)、[`references/files.md`](references/files.md) |

## 排错速查

跨平台现象先查 [`shared/faq.md`](../../shared/faq.md)。

| HTTP | code | 含义 |
|---|---|---|
| 401 | — | App ID 或 REST API Key 错；或加密授权签名错 |
| 400 | 101 | 对象不存在 / 用户名密码不正确 |
| 400 | 105 | 字段名非法或是保留字段（`objectId`/`createdAt`/`updatedAt`/`ACL`） |
| 400 | 106 | Pointer 格式不对 |
| 400 | 107 | JSON 格式错 / Content-Type 不是 application/json |
| 400 | 117 | 纬度 / 经度越界 |
| 400 | 122 | 用户权限验证失败（ACL） |
| 400 | 202 | username 已被使用 |
| 400 | 209 | mobilePhoneNumber 已被使用 |
| 400 | 211 | 用户未登录 / 登录已过期 |
| 400 | 401 | 唯一索引重复值 |
| 400 | 402 | where 超字节限制 |
| 400 | 10076 | QPS 超限 |
| 500 | — | 服务端临时故障，稍后重试 |

完整错误码见 [`bmob-error-codes`](../bmob-error-codes/SKILL.md)。

## 参考

- 完整 REST 文档：[BmobDocs/mds/data/restful/develop_doc.md](https://github.com/bmob/BmobDocs/blob/master/mds/data/restful/develop_doc.md)
- 鉴权约定：[shared/auth-headers.md](../../shared/auth-headers.md)
- MD5 签名：[shared/md5-sign-algo.md](../../shared/md5-sign-algo.md)
- BQL 语法：`bmob-bql`（P1）
- MCP `generate_code` 工具：[`bmob-mcp`](../bmob-mcp/SKILL.md)
- 错误码：[`bmob-error-codes`](../bmob-error-codes/SKILL.md)
