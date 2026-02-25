---
name: feishu-im
description: 飞书消息与群管理 Skill。发送消息、建群、置顶、加急、撤回、群菜单/Tab/公告等 25+ 项 IM 能力。当需要通过飞书发送消息、管理群聊、操作群成员或配置群功能时使用此 Skill。
required_permissions:
  - im:message
  - im:message:recall
  - im:message.pins:write_only
  - im:message.reactions:write_only
  - im:message.urgent
  - im:message.group_msg
  - im:message:send_sys_msg
  - im:chat:create
  - im:chat.members:read
  - im:chat.members:write_only
  - im:chat.announcement:read
  - im:chat.announcement:write_only
  - im:chat.top_notice:write_only
  - im:chat.menu_tree:write_only
  - im:chat.tabs:write_only
  - im:chat.widgets:write_only
  - im:chat.collab_plugins:write_only
  - im:chat.access_event.bot_p2p_chat:read
  - im:url_preview.update
  - im:app_feed_card:write
  - im:tag:write
  - im:datasync.feed_card.time_sensitive:write
---

# 飞书消息与群管理

你是飞书 IM 自动化专家，负责通过 API 实现消息发送、群聊管理和群功能配置。

---

## 一、API 基础信息

| 项目 | 值 |
|------|---|
| Base URL | `https://open.feishu.cn/open-apis/im/v1` |
| 认证方式 | `Authorization: Bearer {tenant_access_token}` |
| Content-Type | `application/json` |

---

## 二、消息操作

### 1. 发送文本消息

```
POST /open-apis/im/v1/messages?receive_id_type=open_id
```

```json
{
  "receive_id": "ou_xxx",
  "msg_type": "text",
  "content": "{\"text\":\"Hello\"}"
}
```

**实测心法**：`content` 必须是字符串化的 JSON，不能直接传对象。

**receive_id_type 可选值**：`open_id` / `user_id` / `union_id` / `email` / `chat_id`

### 2. 发送交互卡片

```
POST /open-apis/im/v1/messages?receive_id_type=open_id
```

```json
{
  "receive_id": "<open_id>",
  "msg_type": "interactive",
  "content": "<card_json_string>"
}
```

**实测心法**：
1. `content` 必须是字符串化的 JSON（JSON string），不能是原始 JSON 对象。
2. 内部嵌套的双引号需进行转义（如 `{\"config\":...}`）。
3. 如果发送失败，请检查 API 调用参数或直接调用 API。

**卡片结构**：

```json
{
  "config": { "wide_screen_mode": true },
  "header": {
    "title": { "tag": "plain_text", "content": "卡片标题" },
    "template": "blue"
  },
  "elements": [
    { "tag": "div", "text": { "tag": "lark_md", "content": "**加粗** 和 `代码` 支持" } },
    { "tag": "hr" },
    { "tag": "action", "actions": [
      { "tag": "button", "text": { "tag": "plain_text", "content": "确认" }, "type": "primary", "value": { "action": "confirm" } }
    ]}
  ]
}
```

**Header 颜色模板**：

| template | 颜色 | 适用场景 |
|----------|------|---------|
| `blue` | 蓝色 | 日常通知、信息 |
| `green` | 绿色 | 成功、完成 |
| `red` | 红色 | 告警、失败 |
| `orange` | 橙色 | 警告、降级 |
| `purple` | 紫色 | 特殊、创意 |
| `turquoise` | 青色 | 技术结果 |
| `grey` | 灰色 | 低优先级 |

**lark_md 语法**：`**加粗**`、`*斜体*`、`~~删除线~~`、`[链接](url)`、`<at id=ou_xxx>名字</at>`

### 3. 消息置顶

```
POST /open-apis/im/v1/pins
```

```json
{ "message_id": "om_xxx" }
```

**实测心法**：必须使用 `/pins` 集合端点，不能使用 `messages/:id/pin` 路径。

### 4. 消息回应（Reaction）

```
POST /open-apis/im/v1/messages/:message_id/reactions
```

```json
{ "reaction_type": { "emoji_type": "OK" } }
```

**实测心法**：emoji_type 必须使用大写标准 ID（如 `OK`、`THUMBSUP`、`HEART`）。

### 5. 撤回消息

```
DELETE /open-apis/im/v1/messages/:message_id
```

**实测心法**：仅能撤回机器人自己在有效期内发送的消息。

### 6. 消息加急

```
PATCH /open-apis/im/v1/messages/:message_id/urgent_app
```

```json
{ "user_id_list": ["ou_xxx"] }
```

**实测心法**：消耗加急额度，请谨慎调用，仅用于 P0 级事件。

### 7. 设置置顶公告

```
POST /open-apis/im/v1/chats/:chat_id/top_notice
```

```json
{ "action_type": "message", "message_id": "om_xxx" }
```

**实测心法**：置顶条目有限，建议仅置顶核心卡片。

### 8. 批量发送群消息

```
POST /open-apis/im/v1/messages/batch_send
```

**实测心法**：注意限频策略，单次建议控制在 200 个群。

### 9. 发送系统消息

```
POST /open-apis/im/v1/messages/send_sys
```

**实测心法**：视觉干扰度低，适合非业务强提醒（如入群须知）。

---

## 三、群聊管理

### 10. 创建群聊

```
POST /open-apis/im/v1/chats
```

```json
{ "name": "群名称", "user_ids": ["ou_xxx"] }
```

**实测心法 (重要)**：
1. 建群后机器人自动成为群成员。
2. **可见性保障**：虽然建群时可以传 `user_ids`，但由于飞书缓存或权限延迟，建议紧接着调用 **12. 拉人入群** API 显式将用户再次加入，以确保群聊在用户端立即弹出。

### 11. 获取群成员列表

```
GET /open-apis/im/v1/chats/:chat_id/members
```

**实测心法**：分页拉取大群成员时注意 Token 翻页。

### 12. 拉人入群

```
POST /open-apis/im/v1/chats/:chat_id/members?member_id_type=open_id
```

```json
{ "id_list": ["ou_xxx"] }
```

**实测心法**：被拉取人必须在机器人可见范围内。这是确保群聊对用户可见的最稳健方式。

### 13. 更新群公告

```
PATCH /open-apis/im/v1/chats/:chat_id/announcement
```

```json
{ "content": "最新进度..." }
```

**实测心法**：内容支持富文本格式。

### 14. 获取群公告

```
GET /open-apis/im/v1/chats/:chat_id/announcement
```

**实测心法**：解析内容后可结合 LLM 生成执行周报。

---

## 四、群功能增强

### 15. 管理群菜单

```
POST /open-apis/im/v1/chats/:chat_id/menu_tree
```

**实测心法**：在群聊右上角添加自定义菜单（如"项目概览"、"一键周报"），极大增强群聊的功能入口属性。

### 16. 管理群选项卡（Tab）

```
POST /open-apis/im/v1/chats/:chat_id/tabs
```

**实测心法**：群内集成多维表格看板、Wiki SOP 为独立 Tab，让群聊变身为"项目工作台"。

### 17. 管理群组件（Widget）

```
POST /open-apis/im/v1/chats/:chat_id/widgets
```

**实测心法**：在群聊右侧挂载动态汇率表、实时监控大屏，将群聊 UI 能力扩展到极限。

### 18. 管理群内协同插件

```
POST /open-apis/im/v1/chats/:chat_id/collab_plugins
```

**实测心法**：在对话框上方常驻"项目文档"入口，减少翻找时间。

---

## 五、高级功能

### 19. 更新 URL 预览

```
POST /open-apis/im/v1/url_preview
```

**实测心法**：机器人发送的项目链接，自动附带最新的进度摘要，增强信息传达的视觉丰富度。

### 20. 管理应用快捷卡片（Feed Card）

```
POST /open-apis/im/v1/feed_cards
```

**实测心法**：在飞书左侧导航栏推送即时状态，比消息更轻量，适合展示"当前正在运行"的任务。

### 21. 管理标签

```
POST /open-apis/im/v1/tags
```

**实测心法**：为群聊或成员打上业务标签（如"核心项目"、"高优先级"），便于后续分类筛选。

### 22. 数据同步 Feed 流

权限：`im:datasync.feed_card.time_sensitive:write`

**实测心法**：将外部 CRM 或代码仓库动态实时推送到飞书 Feed，对时间敏感型信息（如紧急 Bug）效果极佳。

### 23. 设置机器人 P2P 权限

权限：`im:chat.access_event.bot_p2p_chat:read`

**实测心法**：确保机器人能主动给特定用户发送私聊，用户需在机器人可见范围内。

---

## 六、错误处理

| 错误码 | 含义 | 解决方案 |
|--------|------|---------|
| 0 | 成功 | — |
| 230001 | 无发送权限 | 检查机器人是否在群内或用户可见范围 |
| 230002 | 消息不存在 | 检查 message_id 是否正确 |
| 230014 | 频率限制 | 等待后重试，注意限频策略 |
| 99991663 | token 过期 | 重新获取 tenant_access_token |

---

## 七、最佳实践

1. **卡片优先**：结构化信息用交互卡片，不要用纯文本
2. **加急慎用**：消耗额度，仅用于 P0 级事件
3. **批量限频**：批量发送控制在 200 个群/次
4. **置顶精简**：置顶条目有限，只放核心信息
5. **群功能组合**：菜单 + Tab + Widget 组合使用，把群聊变成工作台
