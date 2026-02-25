---
name: feishu-task
description: 飞书任务管理 Skill。创建/完成任务、添加评论和附件。当需要通过飞书自动化派发和管理任务时使用此 Skill。
required_permissions:
  - task:task:write
  - task:comment:write
  - task:attachment:write
---

# 飞书任务管理

你是飞书任务自动化专家，负责通过 Task v2 API 实现任务的创建、完成、评论和附件管理。

---

## 一、API 基础信息

| 项目 | 值 |
|------|---|
| Base URL | `https://open.feishu.cn/open-apis/task/v2` |
| 认证方式 | `Authorization: Bearer {tenant_access_token}` |
| Content-Type | `application/json` |

---

## 二、任务操作

### 1. 创建任务

```
POST /open-apis/task/v2/tasks
```

```json
{
  "summary": "任务标题",
  "description": "任务详细描述",
  "due": {
    "timestamp": "1770508800",
    "is_all_day": false
  },
  "members": [
    { "id": "ou_xxx", "role": "assignee" }
  ],
  "origin": {
    "platform_i18n_name": "{\"zh_cn\": \"AI Agent\"}"
  }
}
```

**实测心法**：
- **必须指派执行人（assignee）**，否则移动端无提醒，用户看不见任务
- `due.timestamp` 是 **13 位毫秒级字符串** (例如 "1770508800000")。注意：如果传成 10 位秒级，任务截止日期会变成 1970 年。
- `origin` 标注任务来源，便于追溯

### 2. 完成任务

```
POST /open-apis/task/v2/tasks/:task_id/complete
```

**实测心法**：支持批量完成，提升效率。自动化流程跑完后同步闭环。

### 3. 更新任务

```
PATCH /open-apis/task/v2/tasks/:task_id
```

```json
{
  "task": {
    "summary": "更新后的标题"
  },
  "update_fields": ["summary"]
}
```

**实测心法**：必须在 `update_fields` 中指定要更新的字段名。

---

## 三、任务评论

### 4. 添加任务评论

```
POST /open-apis/task/v2/tasks/:task_id/comments
```

```json
{ "content": "已完成审计，结果正常" }
```

**实测心法**：支持富文本，可插入链接。用于同步执行过程中的关键日志。

---

## 四、任务附件

### 5. 挂载任务附件

```
POST /open-apis/task/v2/tasks/:task_id/attachments
```

```json
{ "file_token": "..." }
```

**实测心法**：需先通过 Drive 上传接口（`feishu-drive` Skill）获取 `file_token`，再关联至任务。

---

## 五、最佳实践

1. **必须指派**：创建任务一定要指定 assignee，否则等于没创建
2. **来源标注**：通过 `origin` 字段标注任务由 AI Agent 创建，便于区分人工和自动化任务
3. **闭环管理**：自动化流程完成后，调用 complete 接口关闭任务
4. **评论留痕**：关键执行节点通过评论记录，形成审计链
5. **附件关联**：报告、设计稿等产出物通过附件挂载到任务上
