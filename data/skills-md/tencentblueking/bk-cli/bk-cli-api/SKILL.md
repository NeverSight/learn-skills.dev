---
name: bk-cli-api
description: 当需要通过 `bk-cli api` 对任意 BlueKing API Gateway 发起原始 HTTP 调用时使用，尤其适合现有系统子命令还没覆盖、需要精确复现某个 URL/query/path/body/header、先做 dry-run 验证请求构造，或直接调试请求输入与响应包络时。只要用户明确在做“原始 API 请求”而不是现成业务子命令，都应优先使用这个 skill。
---

# bk-cli api — 原始 API 调用

直接对任意 BlueKing API Gateway 网关发起 HTTP 请求。

CRITICAL — 开始前 MUST 先用 Read 工具读取 `../bk-cli-shared/SKILL.md`。那里定义了认证、context、stage、timeout、header、body、tenant、dry-run 和 verbose 的共享规则；本 skill 只补充 `bk-cli api` 独有的原始请求构造细节。

## 何时优先使用本 Skill

- 用户已经知道要访问哪个 `gateway_name`、HTTP 方法和路径，希望直接发请求。
- 现有系统子命令还没覆盖目标接口，但用户仍想通过 `bk-cli` 调试或调用。
- 用户想确认 URL、query、path placeholder、body 或自定义 header 最终会怎样落到请求里。
- 用户在排查“为什么这个请求打不通”，需要先看 dry-run、再看 verbose 输出、最后看 JSON envelope。

## 何时先看别的 Skill

- 如果用户还不知道有哪些网关、资源或 API 名称，先看 `bk-cli-apigateway` 做发现和 Schema 浏览。
- 如果问题是认证、context、tenant、超时、header 覆盖优先级或其他共享请求规则，先看 `bk-cli-shared`。
- 如果已经有现成系统子命令能直接完成目标，而且用户并不关心底层 URL 细节，优先使用系统专属 skill，而不是默认退回原始 API。

## 推荐工作流

1. 先用 `bk-cli-shared` 确认 context、认证和 stage 这些全局前提。
2. 能直接把值写进 `api_path` 时，优先直接写值；只有在模板路径更清晰时才使用 `--path`。
3. 首次尝试或排障时优先加 `--dry-run`，确认 URL、headers、body 都正确后再实际发送。
4. 需要看请求/响应细节时再加 `--verbose`；脚本消费 stdout 时只解析 JSON envelope。

## 命令形态

```
bk-cli api <gateway_name> <method> <api_path> [flags]
```

| 位置参数 | 说明 |
|----------|------|
| `gateway_name` | 网关名，例如 `bk-apigateway`、`bk-iam`；必须匹配 `^[a-z][a-z0-9-]{2,29}$` |
| `method` | HTTP 方法：GET、POST、PUT、PATCH、DELETE |
| `api_path` | API 路径，推荐直接写入值；也支持使用 `{placeholder}` 模板 |

## Flags

| Flag | 类型 | 说明 |
|------|------|------|
| `--query` | JSON 字符串 | 追加到 URL 的查询参数 |
| `--path` | JSON 字符串 | 用于替换 `api_path` 中 `{placeholder}` 的值 |
| `--body` | JSON 字符串 | JSON 请求体，会自动设置 `Content-Type: application/json` |
| `--header` | 可重复 | 自定义请求头，格式为 `Key:Value`，可重复传入 |
| `--stage` | string | 网关 stage：`prod`（默认）或 `testing` |
| `--timeout` | duration | 覆盖当前请求超时，例如 `180s`；默认使用 context 中的 `timeout`（默认 60s） |
| `--dry-run` | bool | 仅预览请求，不实际执行 |
| `--context` | string | 覆盖当前激活的 context |
| `--verbose` | bool | 将请求/响应详情打印到 stderr |
| `--insecure` | bool | 跳过 HTTPS 证书校验，仅用于临时调试 |

## 快速参考

```bash
# 简单 GET
bk-cli api bk-apigateway GET /api/v2/open/gateways/

# 带查询参数的 GET
bk-cli api bk-apigateway GET /api/v2/open/gateways/ \
  --query '{"name":"bk-iam","fuzzy":true}'

# 直接在路径中渲染值的 GET（推荐给 agent）
bk-cli api bk-apigateway GET /api/v2/open/gateways/bk-iam/resources/

# 通过 --path 做路径模板替换
bk-cli api bk-apigateway GET /api/v2/open/gateways/{gateway_name}/resources/ \
  --path '{"gateway_name":"bk-iam"}'

# 带请求体的 POST
bk-cli api bk-demo POST /api/v2/foo/ --body '{"name":"bar"}'

# 自定义请求头
bk-cli api bk-demo GET /api/v2/foo/ --header "X-Custom:value"

# 特殊场景下显式覆盖 auth / tenant header
bk-cli api bk-demo GET /api/v2/foo/ \
  --header 'X-Bkapi-Authorization:{"access_token":"custom-token"}' \
  --header 'X-Bk-Tenant-Id:tenant-b'

# 仅预览，不执行
bk-cli api bk-demo GET /api/v2/foo/ --dry-run

# 使用 testing stage
bk-cli api bk-demo GET /api/v2/foo/ --stage testing

# 单次请求覆盖超时
bk-cli api bk-demo GET /api/v2/foo/ --timeout 180s
```

## 超时

`bk-cli api` 支持 `--timeout <duration>` 单次覆盖 context timeout；完整优先级见 `../bk-cli-shared/SKILL.md`。

## URL 构造

最终 URL 按四步构造：

1. 用 `gateway_name` 渲染 `bk_api_url_tmpl`，得到基础 URL
2. 追加 `/{stage}`，默认是 `prod`
3. 如有需要，用 `--path` 替换 `api_path` 中的占位符
4. 追加解析后的 `api_path`

```
bk_api_url_tmpl = "https://bkapi.example.com/api/{gateway_name}/"
gateway_name    = bk-iam
stage           = prod
api_path        = /api/v2/systems/
→ https://bkapi.example.com/api/bk-iam/prod/api/v2/systems/
```

## 路径替换

**推荐做法：** 如果可以，直接把值写进 `api_path`，不要额外依赖 `--path`。

```bash
# ✅ 推荐：直接在路径里写值
bk-cli api bk-apigateway GET /api/v2/open/gateways/bk-iam/resources/

# 也支持：通过 --path 做模板替换
bk-cli api bk-apigateway GET /api/v2/open/gateways/{gateway_name}/resources/ \
  --path '{"gateway_name":"bk-iam"}'
```

校验规则：
- `api_path` 中有未解析的 `{placeholder}` 且未提供 `--path`，会在本地报错
- `--path` JSON 缺少某个占位符对应的 key，会在本地报错
- `--path` 包含多余 key，且不匹配任何占位符，会在本地报错
- `--path` 不是合法 JSON，会在本地报错
- 当占位符名是 `gateway_name` 时，其值必须匹配 `^[a-z][a-z0-9-]{2,29}$`
- 路径转义、header 覆盖、tenant、`Content-Type` 与脱敏规则见 `../bk-cli-shared/SKILL.md`

## 输出格式

### 成功（HTTP 2xx）

```json
{"ok": true, "status": 200, "headers": {"X-Request-Id": "..."}, "data": {...}}
```

### API 错误（HTTP 非 2xx）

```json
{"ok": false, "status": 400, "headers": {...}, "data": {...}}
```

### CLI 错误（stderr）

```json
{"ok": false, "error": {"code": "auth_required", "message": "...", "hint": "Run: bk-cli auth login"}}
```

### Dry Run

```json
{"ok": true, "dry_run": true, "request": {"method": "GET", "url": "...", "headers": {...}, "params": {...}, "body": null}}
```

## 解析输出

```bash
# 提取 data
bk-cli api bk-apigateway GET /api/v2/open/gateways/ | jq '.data'

# 检查是否成功
bk-cli api bk-apigateway GET /api/v2/open/gateways/ | jq '.ok'

# 获取 HTTP 状态码
bk-cli api bk-apigateway GET /api/v2/open/gateways/ | jq '.status'
```

脚本默认读 stdout 中的 JSON envelope；排障时如果还要看请求细节，再结合 stderr 中的 verbose 输出一起看。

## 常见错误

| 错误码 | 原因 | 修复方式 |
|--------|------|----------|
| `config_error` | 尚未配置 context | `bk-cli context init --bk_api_url_tmpl=...` |
| `auth_required` | 当前 context 没有凭据 | `bk-cli auth login` |
| `invalid_gateway_name` | `gateway_name` 输入不合法 | 使用匹配 `^[a-z][a-z0-9-]{2,29}$` 的网关名 |
| `path_error` | 占位符未解析，或 `--path` JSON 非法 | 检查 `api_path` 占位符和 `--path` 的值 |
| `request_error` | `--query`、`--body` 或 `--header` 输入非法 | 检查 JSON 或 header 格式 |
| `network_error` | 请求发送失败 | 检查网络连通性和 VPN |
