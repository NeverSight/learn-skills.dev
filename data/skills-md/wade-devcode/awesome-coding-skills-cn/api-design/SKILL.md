---
name: api-design
description: 设计 HTTP/REST 接口时使用。资源命名、状态码、版本、错误响应的规范。
category: backend
tags: [api, rest, 接口]
---

# 接口设计

## 何时用

- 新增 HTTP/REST 接口，需要确定 URL 路径、请求体与响应结构时。
- 修改已有接口，要评估是否属于破坏性变更、是否需要新版本时。
- 联调阶段前端反馈"不知道错误含义"或"状态码对不上"时。
- code review 发现接口风格混乱，需要统一约定时。

## 核心规则

### 1. 资源用名词复数，HTTP 方法表达动作

**规则：** URL 只描述资源，增删改查全靠 HTTP 方法（GET/POST/PUT/PATCH/DELETE）区分，禁止在路径里塞动词。

**为什么：** AI 生成代码时极容易把动作写进路径——`POST /createUser`、`GET /getUserById`、`POST /deleteOrder`。这样做破坏了 REST 的统一接口约束：客户端无法通过方法推断语义，反向代理的缓存/日志规则也按 HTTP 方法设计，动词 URL 会绕开这些设施。积累下来接口命名五花八门，新人一眼看不懂哪个是幂等的、哪个有副作用。

**怎么做：**
- 集合资源用复数：`/users`、`/orders`、`/products/{id}/reviews`。
- 子资源层级不超过三级：`/users/{uid}/addresses/{aid}` 可接受，再深就拍平。
- 真正的「动作」（非 CRUD）用子资源或 `action` 后缀：`POST /orders/{id}/cancel` 或 `POST /payments/{id}/refund`，不要 `POST /cancelOrder`。

---

### 2. 状态码严格对应语义

**规则：** 按 HTTP 语义选状态码：2xx 成功、4xx 客户端的错、5xx 服务端的错；不用"一律 200 + `{ "code": 500 }` "的私有协议。

**为什么：** AI 生成的服务端代码极常见"全部返回 200，用 body 里的 code 表示真实状态"——看起来简单，实则让所有上层基础设施失效：Nginx 的 5xx 告警触发不了，监控平台抓不到真实错误率，HTTP 客户端的重试/熔断逻辑按 2xx 判定成功而放行所有故障流量。出了事故查日志，全是绿的。

**怎么做：**
- `200` 成功返回资源，`201` 创建成功（带 `Location` 头），`204` 成功但无响应体（DELETE）。
- `400` 请求格式/参数错误，`401` 未认证，`403` 无权限（已认证但拒绝），`404` 资源不存在，`409` 冲突（重复创建），`422` 业务校验失败。
- `500` 服务内部错误，`502`/`503` 上游/服务不可用，`504` 超时。
- 不要用 `200` 返回错误信息，也不要用 `500` 返回校验失败。

---

### 3. 错误响应结构统一，前端可程序化处理

**规则：** 所有错误响应用相同结构：`code`（机器可读的错误标识）、`message`（人类可读说明）、`details`（可选，字段级明细），不能每个接口各自为政。

**为什么：** AI 最容易犯的错是：有的接口报错返回 `{"error": "invalid email"}`，有的返回 `{"msg": "用户不存在"}`，有的直接丢出框架的原始异常 JSON。前端被迫为每个接口写专属错误解析逻辑，错误提示文案散落各处。哪天要做统一的错误埋点或国际化，根本没有抓手。

**怎么做：**
```json
{
  "code": "VALIDATION_ERROR",
  "message": "请求参数不合法",
  "details": [
    { "field": "email", "message": "邮箱格式不正确" },
    { "field": "age",   "message": "年龄必须大于 0" }
  ]
}
```
- `code` 用 `SCREAMING_SNAKE_CASE` 枚举值，前端可 `switch/map` 处理。
- `message` 面向开发者，不直接作为用户提示（i18n 由前端按 `code` 查表）。
- `details` 仅在有字段级信息时出现，表单校验必带。

---

### 4. 破坏性变更走版本号

**规则：** 接口路径加 `/v1`、`/v2` 前缀；不兼容的改动新开版本，旧版本保留至少一个过渡期，不在原路径上直接覆盖。

**为什么：** AI 修改接口时惯于"直接改字段名"或"删除旧字段"——测试环境跑通了，但已上线的移动端 App、第三方集成、还没发版的前端全部一起炸。破坏性变更无声地推出去，只有故障告警才会被发现，而此时回滚服务端又会打烂已经发版的新客户端。

**怎么做：**
- 路由注册时统一加版本前缀：`/api/v1/users`，不要把版本号藏在 Header 里（难调试）。
- 以下属于破坏性变更，必须升版本：删除字段、重命名字段、改变字段类型、改变 URL 路径、改变 HTTP 方法。
- 新增可选字段、新增可选查询参数、新增响应字段（客户端应忽略未知字段）属于向后兼容，不需要升版本。
- 旧版本下线前通过响应头 `Deprecation: true` + `Sunset: <date>` 提前通知。

---

### 5. 分页、过滤、排序与字段命名全局一致

**规则：** 分页统一用 `page`/`page_size`（或 `cursor`/`limit`），排序用 `sort`，过滤用字段名直接作为参数名；入参出参字段命名统一 `snake_case` 或 `camelCase`，全项目只选一种。

**为什么：** AI 生成多个接口时，分页参数会出现 `pageNum`、`page_index`、`currentPage` 三种写法混用；排序有的叫 `orderBy`、有的叫 `sort_field`；有的接口字段用 `camelCase`，有的用 `snake_case`。前端对接时需要为每个接口单独记参数名，SDK 封装无法复用，文档维护代价翻倍。

**怎么做：**
- 分页（偏移式）：`?page=1&page_size=20`；分页（游标式）：`?cursor=<token>&limit=20`，响应带 `next_cursor`。
- 排序：`?sort=-created_at,name`（`-` 前缀表示降序，多字段逗号分隔）。
- 过滤：`?status=active&user_id=123`，复杂过滤走请求体（POST + filter 对象）。
- 字段命名：与项目已有约定保持一致；JSON 普遍用 `camelCase`，数据库导出型接口常用 `snake_case`，选定后全局统一，在 OpenAPI schema 中声明。

---

## 正例 / 反例

### 反例：动词 URL + 全 200 + 结构不统一

```http
# 反例 — 动词路径，全部 200，错误结构各自为政
POST /api/createUser          HTTP/1.1
POST /api/getUserList         HTTP/1.1
POST /api/deleteUserById      HTTP/1.1

# 响应（无论成功失败都是 200）
HTTP/1.1 200 OK
{ "status": "fail", "msg": "邮箱已存在" }

# 另一个接口的错误格式完全不同
HTTP/1.1 200 OK
{ "error": true, "errorMessage": "参数缺失", "errorCode": 1001 }
```

```http
# 正例 — 名词资源 + 正确状态码 + 统一错误结构
GET    /api/v1/users           # 列表
POST   /api/v1/users           # 创建
DELETE /api/v1/users/{id}      # 删除

# 创建时邮箱冲突
HTTP/1.1 409 Conflict
{
  "code": "EMAIL_ALREADY_EXISTS",
  "message": "该邮箱已被注册",
  "details": [{ "field": "email", "message": "邮箱已存在" }]
}

# 参数缺失
HTTP/1.1 400 Bad Request
{
  "code": "MISSING_REQUIRED_FIELD",
  "message": "缺少必填参数",
  "details": [{ "field": "email", "message": "不能为空" }]
}
```

---

### 反例：破坏性改动原地覆盖

```python
# 反例 — 直接把 full_name 改成 display_name，所有老客户端即刻崩溃
@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    user = db.get_user(user_id)
    return {
        "id": user.id,
        "display_name": user.display_name,   # ❌ 原字段是 full_name，直接改名
        "email": user.email,
    }
```

```python
# 正例 — 旧版本保留兼容字段，新版本走新路径
@app.get("/api/v1/users/{user_id}")
def get_user_v1(user_id: int):
    user = db.get_user(user_id)
    return {
        "id": user.id,
        "full_name": user.display_name,   # ✅ v1 维持旧字段名，兼容老客户端
        "email": user.email,
    }

@app.get("/api/v2/users/{user_id}")
def get_user_v2(user_id: int):
    user = db.get_user(user_id)
    return {
        "id": user.id,
        "display_name": user.display_name,  # ✅ v2 使用新字段名
        "email": user.email,
    }
```

---

## 自查清单

- [ ] URL 中没有出现动词（`create`/`get`/`delete`/`update` 等）。
- [ ] 每个接口的 HTTP 状态码与实际语义一致，没有用 200 返回错误。
- [ ] 所有错误响应都包含 `code`/`message` 字段，结构与项目约定一致。
- [ ] 本次新增/修改是否涉及破坏性变更？若是，已新开版本号而非覆盖原路径。
- [ ] 分页/排序/过滤参数名与现有接口保持一致，无私自发明新参数名。
- [ ] 字段命名风格（camelCase / snake_case）与项目已有约定相同。
- [ ] OpenAPI / Swagger 文档（若有）已同步更新。
