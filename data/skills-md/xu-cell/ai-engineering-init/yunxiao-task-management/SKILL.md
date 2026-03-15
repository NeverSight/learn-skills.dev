---
name: yunxiao-task-management
description: |
  阿里云云效（Yunxiao）项目协作任务管理技能。通过云效 Open API 直接操作工作项：查询任务、修改状态、编辑描述、添加评论、记录工时、创建子任务、搜索项目等。
  支持完整开发工作流：读取任务 → 查找父需求 → 读取需求详情 → 创建提测单 → 编辑提测单 → 转给测试。
  支持智能提测单完善：自动从 git 获取分支/提交信息，从 pom.xml 读取版本号，查找用户任务并填充提测单模板。

  触发场景：
  - 查询/修改云效任务状态
  - 完善提测单内容（自动收集 git 信息）
  - 创建提测单子任务
  - 查看个人待处理任务
  - 读取需求详情

  触发词：云效、任务管理、工作项、修改状态、提测、提测单、完善提测单、SARW、EZML、IXXP、云效任务
---

# 云效任务管理 Skill

通过阿里云云效 Open API 管理项目工作项。所有操作使用 Node.js fetch 直接调用 API。

## 前置配置

从 `.claude/settings.json` 的 `mcpServers.yunxiao.env` 中读取 Token：
```
YUNXIAO_ACCESS_TOKEN: 个人访问令牌
```

**已知用户信息**：
- 组织 ID: `61dbcd725356b19beeb1dc03`
- 用户: 徐嘉骏（ID: `66286d4b06679a65daed4d28`）

**已知项目缓存**（避免全量扫描）：

| customCode | 项目名称 | 项目 ID |
|------------|---------|---------|
| SARW | - | `4574cb1c653fe873335b6c4716` |
| EZML | - | `6f99a4e627fa88d6f8cb541e6c` |
| IXXP | 广州小鹏汽车 | `d93e6ddf18c83254d0b8f27e7d` |

> 新发现的项目应追加到此表。搜索项目时**优先查缓存**，命中则跳过 API 搜索。

## API 基础信息

| 项目 | 值 |
|------|-----|
| Base URL | `https://openapi-rdc.aliyuncs.com` |
| 认证方式 | 请求头 `x-yunxiao-token: {token}` |
| 内容类型 | `application/json` |
| 成功响应 | 200（有 body）或 204（无 body） |

## 通用请求模板

```javascript
async function yunxiaoReq(path, opts = {}) {
  const TOKEN = "从settings.json读取";
  const BASE = "https://openapi-rdc.aliyuncs.com";
  const r = await fetch(BASE + path, {
    method: opts.method || "GET",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "x-yunxiao-token": TOKEN
    },
    body: opts.body ? JSON.stringify(opts.body) : undefined
  });
  if (r.status === 204) return { success: true };
  const text = await r.text();
  try { return JSON.parse(text); } catch { return text; }
}
```

## API 操作清单

### 1. 搜索项目

```
POST /oapi/v1/projex/organizations/{orgId}/projects:search?page={page}&perPage={perPage}
Body: {} 或 { keyword: "关键词" }
```

返回数组，每个项目包含 `id`、`name`、`customCode`（如 SARW、IXXP）。

**重要**：`keyword` 搜索按项目名称模糊匹配，**不支持按 customCode 搜索**。要找 customCode，需全量分页扫描匹配。

**优先使用缓存**：先查"已知项目缓存"表，命中则直接用 ID，无需调 API。

**按项目名称查找**（用户说"小鹏汽车"时）：
1. 先查缓存表的项目名称列
2. 未命中则用 `keyword` 搜索：`{ keyword: "小鹏汽车" }`
3. 仍未找到则全量分页扫描（perPage=100，逐页匹配 name）

### 2. 搜索工作项

```
POST /oapi/v1/projex/organizations/{orgId}/workitems:search
Body: {
  spaceIdentifier: "项目ID",
  spaceId: "项目ID",
  category: "Task",     // Task | Req | Bug | Risk
  page: 1,
  perPage: 200
}
```

**⚠️ 必须指定 spaceId/spaceIdentifier**，不支持跨项目搜索。

返回数组。每个工作项关键字段：
- `serialNumber`: 编号（如 SARW-87）
- `id`: 工作项 ID
- `subject`: 标题
- `status`: `{ name, id }` — 状态名和状态 ID
- `assignedTo`: `{ name, id }` — 负责人
- `parentId`: 父工作项 ID

#### conditions 高级过滤

`conditions` 是 **JSON 字符串**，格式：

```json
{
  "conditionGroups": [[
    { "className": "类型", "fieldIdentifier": "字段", "format": "格式", "operator": "操作符", "toValue": null, "value": ["值"] }
  ]]
}
```

**按负责人过滤**（最常用）：
```json
{ "className": "user", "fieldIdentifier": "assignedTo", "format": "list", "operator": "CONTAINS", "toValue": null, "value": ["用户ID"] }
```

**排除已完成/已取消状态**：
```json
{ "className": "status", "fieldIdentifier": "status", "format": "list", "operator": "NOT_CONTAINS", "toValue": null, "value": ["100014", "141230"] }
```

> `conditions` 传给 API 时必须是 **JSON 字符串**（`JSON.stringify(obj)`），不是对象。

### 3. 获取工作项详情

```
GET /oapi/v1/projex/organizations/{orgId}/workitems/{workitemId}
```

### 4. 编辑工作项（标题/描述/状态/负责人）

```
PUT /oapi/v1/projex/organizations/{orgId}/workitems/{workitemId}
```

可组合多个字段一次更新：`{ "description": "...", "status": "100011", "subject": "..." }`。成功返回 **HTTP 204**。

常见状态 ID（参考值，不同项目可能不同）：

| 状态名 | 状态 ID |
|--------|---------|
| 待处理 | 100005 |
| 处理中 | 100010 |
| 开发完成 | 100011 |
| 已完成 | 100014 |
| 已取消 | 141230 |

### 5. 添加评论

```
POST /oapi/v1/projex/organizations/{orgId}/workitems/{workitemId}/comments
Body: { "content": "评论内容" }
```

### 6. 创建子任务

```
POST /oapi/v1/projex/organizations/{orgId}/workitems
Body: {
  "spaceId": "项目ID",
  "subject": "子任务标题",
  "workitemTypeId": "任务类型ID",
  "assignedTo": "用户ID",          // 必需！
  "parentId": "父工作项ID",
  "description": "描述（可选）"
}
```

**获取任务类型 ID**：
```
GET /oapi/v1/projex/organizations/{orgId}/projects/{projectId}/workitemTypes?category=Task
```

### 7. 工时管理

**预估工时**：`POST .../workitems/{id}/estimatedEfforts` Body: `{ "spentTime": 480, "owner": "用户ID" }`
**实际工时**：`POST .../workitems/{id}/effortRecords` Body: `{ "actualTime": 240, "gmtStart": ts, "gmtEnd": ts }`

## 不支持的操作

| 操作 | 原因 |
|------|------|
| 添加附件 | API 不支持（504 超时/415 错误） |
| 获取用户信息 | 需要「用户信息（读取）」权限，Token 不支持 |

---

## 提测单完善流程（核心场景）

当用户说"完善提测单"、"填写提测单"、"帮我提测"时触发。用户可能**不提供任务 ID**，只说项目名或需求描述。

### 流程概览

```
1. 定位任务 → 2. 收集 git 信息 → 3. 读取版本号 → 4. 加载模板 → 5. 填充并更新描述
```

### Step 1: 定位任务

**场景 A：用户提供了任务编号**（如 IXXP-122）
- 从编号前缀提取 customCode（IXXP）
- 查缓存表 → 命中则直接用项目 ID
- 未命中则全量分页扫描匹配 customCode
- 搜索项目 Task，找到 serialNumber 匹配的工作项

**场景 B：用户只说项目名称**（如"小鹏汽车"）
- 用项目名称匹配缓存或 keyword 搜索
- 找到项目后，用 `assignedTo` conditions 过滤当前用户的任务
- 展示任务列表，让用户选择或自动匹配标题含"提测"的任务

**场景 C：用户只说"我的提测单"**
- 用已知项目缓存逐个搜索当前用户的任务
- 筛选标题含"提测"的任务

```javascript
// 查找用户在指定项目中的任务
const conditions = JSON.stringify({
  conditionGroups: [[
    { className: "user", fieldIdentifier: "assignedTo", format: "list", operator: "CONTAINS", toValue: null, value: [USER_ID] },
    { className: "status", fieldIdentifier: "status", format: "list", operator: "NOT_CONTAINS", toValue: null, value: ["100014", "141230"] }
  ]]
});
// POST workitems:search with { spaceId, category: "Task", conditions, page: 1, perPage: 200 }
```

### Step 2: 收集 git 信息

从当前工作目录的 git 仓库自动收集：

```bash
# 当前分支名（后端分支）
git branch --show-current

# 最近的相关提交（用户可能指定 commit hash）
git log {commitHash} -1 --stat

# 提交所在分支
git branch --contains {commitHash}
```

**信息映射**：
- 后端分支 = `git branch --show-current` 或 `git branch --contains {hash}`
- 需求描述 = 用户提供 或 commit message
- 前端分支 / h5分支 = 用户提供，默认留空或 "无"

### Step 3: 读取版本号

从定制仓库的 pom.xml 读取 `parent.version`：

```bash
# 读取 pom.xml 的 parent version
grep -A1 '<artifactId>core-dependencies</artifactId>' pom.xml | grep '<version>'
```

### Step 4: 加载提测单模板

模板文件位置：`{skill目录}/templates/提测单模板.html`

读取模板文件，替换占位符：
- `{项目名称}` → 项目中文名（如"小鹏汽车总部"）
- `{版本号}` → pom.xml parent version
- `{后端分支}` → git 分支名
- `{前端分支}` → 用户提供或 "无"
- `{h5分支}` → 用户提供或 "无"
- `{需求描述}` → 需求内容
- `{开发者ID}` → 当前用户 ID
- `{开发者名}` → 当前用户名
- `{自测说明}` → "已自测通过" 或用户提供
- `{测试用例}` → 根据需求自动生成或用户提供
- `{提测人ID}` → 当前用户 ID
- `{提测人}` → 当前用户名
- `{验收人}` → 用户指定（先在项目成员中搜索 ID，未找到则纯文本）

**@提及语法**：`<span data-type="mention" data-id="{用户ID}">@{用户名}</span>`

**搜索用户 ID**：从项目工作项的 `assignedTo` 和 `creator` 字段收集所有成员，匹配姓名。

### Step 5: 更新工作项描述

```javascript
await yunxiaoReq(`/oapi/v1/projex/organizations/${ORG}/workitems/${workitemId}`, {
  method: "PUT",
  body: { description: filledTemplate }
});
// 成功返回 204
```

### 完整示例

```
用户：完善 IXXP-122 提测单，提交是 45bdb2a 装修优化，前端分支 master，验收人卢佳南
```

执行步骤：
1. IXXP → 查缓存命中 → 项目 ID `d93e6ddf18c83254d0b8f27e7d`
2. 搜索 Task 找到 IXXP-122
3. `git log 45bdb2a -1 --stat` → 获取提交详情
4. `git branch --contains 45bdb2a` → 后端分支
5. 读取 pom.xml → 版本号
6. 加载模板，替换占位符
7. 在项目成员中搜索"卢佳南"（未找到则纯文本写入）
8. PUT 更新描述 → 204 成功

```
用户：帮我完善小鹏汽车项目的提测单
```

执行步骤：
1. "小鹏汽车" → 查缓存匹配 IXXP
2. 用 assignedTo 过滤当前用户的未完成任务
3. 筛选标题含"提测"的任务 → 展示列表让用户确认
4. 从 git 自动收集分支、提交信息
5. 读取版本号，加载模板，填充更新

---

## 开发工作流（创建提测单）

当需要**新建**提测单（而非完善已有的），用户说"创建提测单"时触发。

### 流程

```
读取任务（Task） → 查找父需求（Req） → 创建提测单子任务 → 填充描述
```

### Step 1: 读取任务并找到父需求

```javascript
const task = items.find(i => i.serialNumber === "EZML-1878");
const parentDetail = await yunxiaoReq(`/oapi/v1/projex/organizations/${ORG}/workitems/${task.parentId}`);
```

### Step 2: 创建提测单子任务

```javascript
const types = await yunxiaoReq(`/oapi/v1/projex/organizations/${ORG}/projects/${projectId}/workitemTypes?category=Task`);
await yunxiaoReq(`/oapi/v1/projex/organizations/${ORG}/workitems`, {
  method: "POST",
  body: {
    spaceId: projectId,
    subject: "提测-需求标题摘要",
    workitemTypeId: types[0].id,
    assignedTo: "测试人员ID",
    parentId: parentReqId,
    description: filledTemplate  // 同提测单完善流程 Step 4-5
  }
});
```

### Step 3: 修改开发任务状态

```javascript
await yunxiaoReq(`/oapi/v1/projex/organizations/${ORG}/workitems/${taskId}`, {
  method: "PUT",
  body: { status: "100011" }  // 开发完成
});
```

---

## 跨项目搜索用户任务

云效 API 不支持全局搜索，需逐项目扫描。

```javascript
// 全量扫描所有项目（perPage=100，逐页）
// 对每个项目用 assignedTo + status NOT_CONTAINS 过滤
// 并发批处理（batchSize=20）
const batchSize = 20;
for (let i = 0; i < projects.length; i += batchSize) {
  const batch = projects.slice(i, i + batchSize);
  const results = await Promise.all(batch.map(p => searchWorkitems(p.id)));
  myTasks.push(...results.flat());
}
```

> `members` 项目过滤在实测中未生效，建议直接扫描所有项目。

## Token 权限要求

| 权限 | 读取操作 | 写入操作 |
|------|---------|---------|
| 项目协作（读取） | ✅ 查询项目、搜索工作项、获取详情 | - |
| 项目协作（读写） | ✅ 全部读取 | ✅ 修改状态、编辑、评论、创建、工时 |
