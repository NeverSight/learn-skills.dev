---
name: redmine-search
description: Redmine 访问 Skill，仅查询指派给我的工单，提供通过 API Token 认证方式访问 Redmine 系统的功能。
---

# Redmine 访问 Skill（仅指派给我）

## 连接信息

| 项目 | 值 |
|---|---|
| **服务器地址** | `https://redmine-skgd3-local.housei-inc.com` |
| **认证方式** | API Token |
| **Token** | `ac72e559db69e0107b6bc973c65b75d9acf5725b` |

## 认证方法（二选一）

1. **Header 方式（推荐）**：`X-Redmine-API-Key: <token>`
2. **URL 参数方式**：`?key=<token>`

## API 端点

| 用途 | 方法 | 端点 | 说明 |
|---|---|---|---|
| 单票详情 | GET | `/issues/{id}.json` | 获取指定工单的完整信息 |
| 工单列表 | GET | `/issues.json` | 支持筛选、分页 |
| 项目工单 | GET | `/projects/{project_id}/issues.json` | 获取指定项目的工单 |

## 常用筛选参数（默认指派给我，可按提示指定指派人）

| 参数 | 示例值 | 说明 |
|---|---|---|
| `status_id` | `open`, `closed`, `*` | 工单状态筛选 |
| `assigned_to_id` | `me`, `{user_id}` | 指派人筛选（默认 me；提示词明确指定指派人时按指定值） |
| `limit` | `25`（默认）, `100`（最大） | 每页条数 |
| `offset` | `0`, `25` | 分页偏移 |
| `sort` | `updated_on:desc` | 排序 |
| `tracker_id` | `1`=Bug, `2`=Feature | 跟踪器类型 |
| `priority_id` | `1`=低, `2`=中, `3`=高, `4`=紧急 | 优先级 |

## 调用示例

```bash
# 获取所有未关闭且指派给我的工单（最多50条，按更新时间倒序）
GET /issues.json?assigned_to_id=me&status_id=open&limit=50&sort=updated_on:desc&key=TOKEN

# 获取单个工单详情（仅在该工单指派给我时使用）
GET /issues/15400.json?key=TOKEN

# 获取分配给我的工单（不限制状态）
GET /issues.json?assigned_to_id=me&status_id=*&key=TOKEN
```

## 返回数据结构要点

工单对象关键字段：
- `id` - 工单编号
- `subject` - 标题
- `status.name` - 状态名
- `priority.name` - 优先级名
- `tracker.name` - 跟踪器名（Bug/Feature/Task等）
- `assigned_to.name` - 指派人
- `description` - 描述（可能含 Textile 标记）
- `updated_on` - 最后更新时间
- `created_on` - 创建时间