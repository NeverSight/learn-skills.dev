---
name: feishu-calendar
description: 飞书日历日程管理 Skill。创建日历/日程、查询空闲忙状态、订阅日历变更。当需要自动安排会议、查询时间冲突或监控日程变动时使用此 Skill。
required_permissions:
  - calendar:calendar
  - calendar:calendar.free_busy:read
  - calendar:calendar:subscribe
---

# 飞书日历日程管理

你是飞书日历自动化专家，负责通过 Calendar v4 API 实现日程创建、空闲查询和日历订阅。

---

## 一、API 基础信息

| 项目 | 值 |
|------|---|
| Base URL | `https://open.feishu.cn/open-apis/calendar/v4` |
| 认证方式 | `Authorization: Bearer {tenant_access_token}` |
| Content-Type | `application/json` |

---

## 二、日历操作

### 1. 创建日历

```
POST /open-apis/calendar/v4/calendars
```

```json
{ "summary": "项目日历" }
```

**实测心法**：创建后可添加协作者，适合为特定项目创建共享日历。

---

## 三、日程操作

### 2. 创建日程

创建日程分为两步：

**第一步：创建日程基本信息**

```
POST /open-apis/calendar/v4/calendars/:calendar_id/events
```

```json
{
  "summary": "需求对齐会",
  "description": "讨论 Q2 产品规划",
  "start_time": { "timestamp": "1770641576" },
  "end_time": { "timestamp": "1770645176" }
}
```

**第二步：添加参与人 (关键)**

创建成功获取 `event_id` 后，必须调用此接口才能邀请他人：

```
POST /open-apis/calendar/v4/calendars/:calendar_id/events/:event_id/attendees?user_id_type=open_id
```

```json
{
  "attendees": [
    { "type": "user", "user_id": "ou_xxx" }
  ]
}
```

**实测心法**：
- **创建日程接口不支持直接传参会人**，必须分两步走。
- **时间戳必须为秒级字符串**（不是毫秒，不是数字）。
- 必须带上 `user_id_type=open_id` 参数，否则无法识别 `ou_` 开头的 ID。
- 添加 `reminders` 确保参会人收到提醒。

### 3. 更新日程

```
PATCH /open-apis/calendar/v4/calendars/:calendar_id/events/:event_id
```

### 4. 删除日程

```
DELETE /open-apis/calendar/v4/calendars/:calendar_id/events/:event_id
```

---

## 四、智能排期

### 5. 批量查询空闲忙状态

```
POST /open-apis/calendar/v4/freebusy/list
```

```json
{
  "time_min": "2026-02-10T09:00:00+08:00",
  "time_max": "2026-02-10T18:00:00+08:00",
  "user_id": "ou_xxx"
}
```

**实测心法**：安排跨部门会议的利器。先查空闲再创建日程，避免时间冲突。

---

## 五、日历订阅

### 6. 订阅日历变更

```
POST /open-apis/calendar/v4/calendars/:calendar_id/subscribe
```

**实测心法**：实时感知关键人员的日程变动并调整后续任务。需要配置事件回调（Webhook）。

---

## 六、最佳实践

1. **先查后建**：创建日程前先用 freebusy 查询空闲时段
2. **秒级字符串**：时间戳格式是最常踩的坑，必须是秒级字符串
3. **提醒设置**：始终添加 reminders，否则参会人容易错过
4. **订阅监控**：对关键日历开启订阅，实现日程变更的实时感知
