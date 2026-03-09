---
name: dingtalk-document
description: 钉钉知识库和文档管理操作。当用户提到"钉钉文档"、"知识库"、"新建文档"、"查看文档目录"、"读取文档内容"、"写入文档"、"更新文档"、"文档成员"、"dingtalk doc"、"knowledge base"时使用此技能。支持：创建知识库、查询知识库列表、新建文档/文件夹、读取/写入文档正文内容、管理成员权限等全部文档类操作。
---

# 钉钉文档技能

负责钉钉知识库和文档的所有操作，通过钉钉开放平台 API 实现。

API 详情见 `references/api.md`。

---

## 配置管理（每次开始前必读）

### 配置文件路径

`~/.dingtalk-skills/config`（跨会话保留，所有 dingtalk-skills 共用同一文件）

### 本技能需要的配置

| 键 | 说明 | 来源 |
|---|---|---|
| `DINGTALK_APP_KEY` | 钉钉应用 appKey | 开放平台 → 应用管理 → 凭证信息 |
| `DINGTALK_APP_SECRET` | 钉钉应用 appSecret | 同上 |
| `DINGTALK_OPERATOR_ID` | 操作人 unionId | 见下方"为什么需要 operatorId"章节 |

### 启动流程（每次执行任务前）

1. **读取配置**：检查 `~/.dingtalk-skills/config` 是否存在，解析已有键值
2. **识别缺失项**：找出上表中尚未配置的键
3. **一次性收集**：将所有缺失项合并为一条提问，**不要逐条询问**，例如：
   > 需要以下信息才能继续（已有的无需再填）：
   > - 钉钉应用 appKey（钉钉开放平台 → 应用管理 → 凭证信息）
   > - 钉钉应用 appSecret
   > - 你的钉钉 userId 或 unionId（以便以你的身份操作文档）
4. **持久化**：将用户提供的值追加写入 config，后续直接读取，无需再问
5. **执行任务**：配置完整后开始操作

> **注意**：`APP_KEY`/`APP_SECRET`/`OPERATOR_ID` 属于凭证，禁止在输出中完整打印，确认时仅显示前 4 位 + `****`。

---

## 认证

每次调用 API 前，用 appKey/appSecret 获取当次的 accessToken（有效期 2 小时）：

```
POST https://api.dingtalk.com/v1.0/oauth2/accessToken
Content-Type: application/json

{
  "appKey": "<应用 appKey>",
  "appSecret": "<应用 appSecret>"
}
```

返回：`{ "accessToken": "xxx", "expireIn": 7200 }`

所有后续请求均需携带请求头：
```
x-acs-dingtalk-access-token: <accessToken>
```

---

## 为什么需要 operatorId（unionId）

钉钉开放平台要求所有**写操作**（创建文档、写入内容、管理成员等）必须代表一个真实用户身份执行，而不是以匿名应用身份操作。`operatorId` 就是声明"这个操作是谁做的"——它会被记录到文档的变更历史，并用于权限校验。

- 值为操作人的 **`unionId`**（钉钉跨组织唯一 ID），**不是** `userId`（仅组织内唯一）
- 错误传入 userId 会导致权限报错或文档归属错误

### 如何获取 unionId

**方法一：已知 userId → 换取 unionId（最常用）**

`userId` 通常可从通讯录、免登、消息回调等场景直接获得。

第一步：获取旧式 `access_token`（与新版 accessToken 不同，此处单独获取）：
```
GET https://oapi.dingtalk.com/gettoken?appkey=<appKey>&appsecret=<appSecret>
```
返回：`{ "access_token": "xxx", "expires_in": 7200 }`

第二步：用 userId 查询用户详情，取出 unionId：
```
POST https://oapi.dingtalk.com/topapi/v2/user/get?access_token=<旧式token>
Content-Type: application/json

{ "userid": "<钉钉 userId>" }
```
返回字段 `result.unionid`（无下划线）即为 unionId。

> 注意：`result.union_id`（有下划线）在专属钉钉组织中可能为空，请使用 `result.unionid`。

**方法二：机器人/消息场景**

用户通过钉钉机器人或消息触发时，消息体中直接包含 `senderUnionId` 字段，可直接作为 `operatorId` 使用，无需额外查询。

**方法三：直接询问用户**

若上述方式不可用，在初始配置阶段询问用户提供 userId 或 unionId（均可在钉钉个人信息页查看）。获取后写入 config，后续操作无需重复获取。

---

## 核心操作

### 1. 查询用户知识库列表

用户想查看有哪些知识库时：

```
GET https://api.dingtalk.com/v2.0/wiki/workspaces?operatorId=<unionId>&maxResults=20&nextToken=<分页令牌>
x-acs-dingtalk-access-token: <accessToken>
```

如有 `nextToken` 则继续翻页，直到无 `nextToken` 为止。返回字段中 `workspaceId` 和 `rootNodeId` 供后续操作使用。

---

### 2. 查询知识库信息

```
GET https://api.dingtalk.com/v2.0/wiki/workspaces/{workspaceId}?operatorId=<unionId>
x-acs-dingtalk-access-token: <accessToken>
```

---

### 3. 查询目录结构（节点列表）

用户想看知识库里有哪些文档/文件夹时：

```
GET https://api.dingtalk.com/v2.0/wiki/nodes?parentNodeId=<nodeId>&operatorId=<unionId>&maxResults=50
x-acs-dingtalk-access-token: <accessToken>
```

`parentNodeId` 传知识库的 `rootNodeId` 可列出顶层内容，传子文件夹 `nodeId` 可深入查看。

每个节点包含：`nodeId`、`name`、`type`（`FILE`/`FOLDER`）、`category`、`workspaceId`、`url`。

---

### 4. 查询单个节点信息（通过 nodeId）

```
GET https://api.dingtalk.com/v2.0/wiki/nodes/{nodeId}?operatorId=<unionId>
x-acs-dingtalk-access-token: <accessToken>
```

---

### 5. 通过文档链接查询节点信息

用户提供了文档 URL（如 `https://alidocs.dingtalk.com/i/nodes/Xxx...`）时：

```
POST https://api.dingtalk.com/v2.0/wiki/nodes/queryByUrl?operatorId=<unionId>
x-acs-dingtalk-access-token: <accessToken>
Content-Type: application/json

{
  "url": "https://alidocs.dingtalk.com/i/nodes/<nodeId>",
  "operatorId": "<unionId>"
}
```

返回节点信息，其中 `nodeId` 可作为后续内容读取的 `docKey`。

---

### 6. 创建文档

在指定知识库下新建文档：

```
POST https://api.dingtalk.com/v1.0/doc/workspaces/{workspaceId}/docs
x-acs-dingtalk-access-token: <accessToken>
Content-Type: application/json

{
  "operatorId": "<unionId>",
  "docType": "DOC",
  "name": "<文档标题>"
}
```

返回字段：

| 字段 | 说明 |
|---|---|
| `nodeId` | 知识库节点 ID（用于删除） |
| `docKey` | 文档内容 Key（用于内容读写，≠ nodeId） |
| `workspaceId` | 实际所在知识库 ID（可能与请求的不同，删除时须使用此值） |
| `url` | 文档访问链接 |

> `docType` 固定填 `"DOC"`（ALIDOC 富文本格式）。

---

### 10. 删除文档

```
DELETE https://api.dingtalk.com/v1.0/doc/workspaces/{workspaceId}/docs/{nodeId}?operatorId=<unionId>
x-acs-dingtalk-access-token: <accessToken>
```

`workspaceId` 和 `nodeId` 均从创建文档的响应中获取。成功返回 `200 {}`。

---

### 7. 读取文档正文内容（Block 结构）

用户想看文档里写了什么内容时，使用 `docKey` 读取文档 Block：

```
GET https://api.dingtalk.com/v1.0/doc/suites/documents/{docKey}/blocks?operatorId=<unionId>
x-acs-dingtalk-access-token: <accessToken>
```

`docKey` 的来源：
- 通过 wiki nodes 接口查到的节点：`docKey = nodeId`（同一个值）
- 通过创建文档接口新建的文档：使用响应中的 `docKey` 字段（**不是** `nodeId`）

所需权限：`Storage.File.Read`

返回示例：
```json
{
  "result": {
    "data": [
      { "blockType": "heading", "heading": { "level": "heading-2", "text": "快速开始" }, "index": 0, "id": "xxx" },
      { "blockType": "paragraph", "paragraph": { "text": "正文内容..." }, "index": 1, "id": "yyy" },
      { "blockType": "unknown", "index": 2, "id": "zzz" }
    ]
  },
  "success": true
}
```

`blockType` 枚举：`heading`、`paragraph`、`unorderedList`、`orderedList`、`table`、`blockquote`、`unknown`（代码块/图片等富文本暂未解析）。

将各 block 的文本提取后按 index 顺序拼接，即可重建文档文字内容。

> `docKey` 即通过 wiki nodes 接口获取的 `nodeId`，是同一个值。

---

### 8. 写入/覆盖文档正文内容

用户想修改文档内容时：

```
POST https://api.dingtalk.com/v1.0/doc/suites/documents/{docKey}/overwriteContent
x-acs-dingtalk-access-token: <accessToken>
Content-Type: application/json

{
  "operatorId": "<unionId>",
  "docContent": "# 新标题\n\n新的正文内容，支持 Markdown 格式。",
  "contentType": "markdown"
}
```

⚠️ 写入操作会**覆盖**原有内容，执行前请与用户确认或先读取备份。

---

### 9. 文档成员管理

**添加文档成员：**
```
POST https://api.dingtalk.com/v1.0/doc/workspaces/{workspaceId}/docs/{nodeId}/members
x-acs-dingtalk-access-token: <accessToken>
Content-Type: application/json

{
  "operatorId": "<unionId>",
  "members": [
    { "id": "<userId>", "roleType": "editor" }
  ]
}
```

`roleType` 可选：`viewer`（只读）、`editor`（可编辑）

---

## 典型场景

### "读取文档 X 的内容"
1. 若用户提供了 URL，调用 `POST /v2.0/wiki/nodes/queryByUrl` 获取 `nodeId`
2. 否则通过 `GET /v2.0/wiki/nodes?parentNodeId=...` 遍历查找目标文档
3. 用 `nodeId` 作为 `docKey`，调用 `GET /v1.0/doc/suites/documents/{docKey}/blocks`
4. 将 block 文本按 index 顺序拼接后展示给用户

### "把文档 X 的内容改成……"
1. 先读取原内容，告知用户将被覆盖，请求确认
2. 调用 `POST /v1.0/doc/suites/documents/{docKey}/overwriteContent`，传入新内容
3. 告知写入成功

### "帮我在钉钉创建一个文档"
1. 询问放到哪个知识库（列出知识库或让用户说名称）
2. 通过 `GET /v2.0/wiki/workspaces` 找到对应 `workspaceId`
3. 调用 `POST /v1.0/doc/workspaces/{workspaceId}/docs`，`docType: ALIDOC`
4. 返回文档链接给用户

### "查看知识库 X 下有哪些文档"
1. 通过 `GET /v2.0/wiki/workspaces` 找到 `workspaceId` 和 `rootNodeId`
2. 调用 `GET /v2.0/wiki/nodes?parentNodeId={rootNodeId}&operatorId=...`
3. 整理成目录树展示

### "把用户 xxx 加到文档 Y"
1. 确认文档的 `nodeId` 和所在 `workspaceId`
2. 调用 `POST /v1.0/doc/workspaces/{workspaceId}/docs/{nodeId}/members`，指定 `roleType`

---

## 错误处理

| HTTP 状态码 | 错误码 | 含义 | 处理方式 |
|---|---|---|---|
| 400 | `MissingoperatorId` | operatorId 未传 | 补充 operatorId（unionId）|
| 400 | `paramError` | 参数类型错误 | operatorId 必须是 unionId，不是 userId |
| 401 | — | token 过期 | 重新获取 accessToken 后重试 |
| 403 | `Forbidden.AccessDenied.AccessTokenPermissionDenied` | 应用缺少权限 | 错误信息中有 `requiredScopes`，提示用户在开放平台开通对应权限 |
| 404 | `InvalidAction.NotFound` | 接口路径不存在 | 检查版本号（v1.0/v2.0）和路径是否正确 |
| 429 | — | 触发限流 | 等待 1 秒后重试 |

发生错误时，将响应体中的 `code` 和 `message` 展示给用户辅助排查。

## 所需应用权限

| 功能 | 权限 scope |
|---|---|
| 查询知识库/节点 | `Wiki.Node.Read` |
| 读取文档正文 | `Storage.File.Read` |
| 写入文档正文 | `Storage.File.Write` |
| 创建/删除文档 | `Storage.File.Write` |
| 查询用户 unionId（获取 operatorId）| `Contact.User.Read` |
