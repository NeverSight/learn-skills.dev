---
name: yqcloud-function-calling
description: YQCloud 自定义 Function Calling 格式说明，用于 ITSM 工单场景。包含 createTicket、getCreateTicketParamJsonSchema、getAllServiceItem、requestUserSelectServiceItem 四个函数的调用规范和典型流程。
user-invocable: false
---

# YQCloud 自定义 Function Calling 格式说明

本 skill 描述了一套自定义的 function calling 格式，用于 ITSM（IT服务管理）场景下的工单操作。

## 格式结构说明

每个函数定义包含两层结构：
- 外层：标准的函数描述（name、description、parameters）
- 内层 `function` 字段：执行配置（type、url、headers 等）

### 函数类型（function.type）

| 类型 | 说明 |
|------|------|
| `manual` | 手动处理，由前端/系统自行实现逻辑，不发起 HTTP 请求 |
| `call_url` | 自动发起 HTTP 请求到指定 URL |

### 通用字段

- `stopAfterFunctionCall`：调用函数后是否停止 AI 继续生成（true=停止，false=继续）
- `intl`：国际化配置，包含 `zh_CN` 和 `en_US`
- `requestParser`：JavaScript 代码字符串，`data` 为 AI 函数调用参数的 JSON 字符串（需 `JSON.parse(data)` 解析）
- `responseParser`：JavaScript 代码字符串，`data` 为响应体对象，可使用 `_`（lodash）

### 变量占位符

- `${STATIC#yqcloud_url}`：YQCloud 服务基础地址
- `${tenantId}`：当前租户 ID
- `${yqAccessToken}`：当前用户访问令牌

---

## 函数列表

### 1. createTicket — 创建工单

- **类型**：`manual`（前端自行处理，不发 HTTP 请求）
- **stopAfterFunctionCall**：`true`
- **参数**：`additionalProperties: true`，接受任意字段
- **调用时机**：已获取表单 Schema 并从用户处收集完所有字段后调用

### 2. getCreateTicketParamJsonSchema — 获取工单参数 Schema

- **类型**：`call_url`，GET 请求
- **URL**：`${STATIC#yqcloud_url}/ai/v1/${tenantId}/itsmScene/getServiceItemSchema`
- **stopAfterFunctionCall**：`false`
- **必填参数**：`id`（string，服务项 ID）
- **调用时机**：确定服务项后立即调用，根据返回的 Schema 向用户逐一收集字段

### 3. getAllServiceItem — 获取全部服务项

- **类型**：`call_url`，GET 请求
- **URL**：`${STATIC#yqcloud_url}/itsm/v1/${tenantId}/service_items/catalog/page/all?serviceCatalogFlag=true&page=0&size=9999`
- **参数**：无必填参数
- **responseParser**：过滤 `type === 'SERVICE' || type === 'RECORD'`，只保留 `id`、`name`、`shortDescription`、`description`，返回 `{ allServiceItemList: [...] }`
- **调用时机**：用户提出任何工单相关需求后第一步调用

### 4. requestUserSelectServiceItem — 请求用户选择服务项

- **类型**：`call_url`，POST 请求，URL：`/transparent`
- **stopAfterFunctionCall**：`true`
- **必填参数**：`serviceItemList`（array，**最多传 1 个**最可能匹配的服务项）
- **responseParser**：`return data?.serviceItemList ? data : {result: 'no data'}`
- **调用时机**：AI 无法确定具体服务项时调用

---

## 典型调用流程

```
用户提出工单需求
       ↓
调用 getAllServiceItem
       ↓
AI 分析匹配服务项
       ├─ 能确定 → getCreateTicketParamJsonSchema → 收集字段 → createTicket
       └─ 无法确定 → requestUserSelectServiceItem → 用户选择后重新进入流程
```

## 注意事项

1. `getAllServiceItem` 实际无必填参数，直接调用即可
2. `requestUserSelectServiceItem` 的 `serviceItemList` 最多传 **1 个**服务项
3. `createTicket` 是 `manual` 类型，实际创建逻辑由前端实现
4. `stopAfterFunctionCall: true` 的函数调用后 AI 不会继续输出
