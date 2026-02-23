---
name: im-reminder
description: IM 定时提醒技能，支持一次性和周期性定时任务。通过 cron job 在指定时间唤醒 Agent，自动检测当前 IM 频道，保证消息准确送达。
metadata: { "openclaw": { "emoji": "⏰", "channels": ["feishu", "webchat"] } }
---

# IM 定时提醒

跨平台定时提醒技能，保证准确的时间触发和消息送达。通过 cron job 配置，确保消息发送到用户请求提醒的原始频道，避免 NO_REPLY 问题。

## 适用场景

- 用户请求定时提醒（如"5 分钟后提醒我开会"）
- 用户请求周期性任务（如"每小时提醒我喝水"）
- 需要在指定时间触发 Agent 执行操作并回复用户

## 固定字段

以下字段在所有任务中取值固定，不可更改：

| 字段              | 固定值        | 说明                              |
| ----------------- | ------------- | --------------------------------- |
| `enabled`         | `true`        | **必须为 true**，否则任务不会执行 |
| `sessionTarget`   | `"isolated"`  | 每次触发创建独立会话              |
| `payload.kind`    | `"agentTurn"` | 触发类型为 Agent 回合             |
| `payload.deliver` | `true`        | 确保消息发送到外部频道            |

## 动态字段

以下字段需根据当前会话上下文自动填充：

| 字段              | 说明                                                                    |
| ----------------- | ----------------------------------------------------------------------- |
| `payload.channel` | 当前频道类型，从运行时上下文获取（如 `feishu`）                         |
| `payload.to`      | **必填**，当前频道目标用户 ID，从会话上下文获取，缺失会导致消息无法送达 |

## 调度方式

### 一次性定时（at）

在指定时间点触发一次，适用于"X 分钟后提醒我"这类场景。

```json
"schedule": {
  "kind": "at",
  "atMs": 1770449700000
}
```

`atMs` 为目标触发时间的 Unix 时间戳（毫秒）。

### 周期性定时（every）

按固定间隔重复触发，适用于"每隔 X 分钟提醒我"这类场景。

```json
"schedule": {
  "kind": "every",
  "everyMs": 60000
}
```

`everyMs` 为触发间隔的毫秒数（如 60000 = 1 分钟）。

### Cron 表达式定时（cron）

使用标准 cron 表达式调度，适用于"每天早上 7 点提醒我"这类基于日历规律的场景。

```json
"schedule": {
  "kind": "cron",
  "expr": "0 7 * * *"
}
```

`expr` 为标准五位 cron 表达式，格式如下：

```
┌───────────── 分钟 (0-59)
│ ┌───────────── 小时 (0-23)
│ │ ┌───────────── 日 (1-31)
│ │ │ ┌───────────── 月 (1-12)
│ │ │ │ ┌───────────── 星期 (0-6，0=周日)
│ │ │ │ │
* * * * *
```

常用表达式：

| 场景               | 表达式        |
| ------------------ | ------------- |
| 每天早上 7 点      | `0 7 * * *`   |
| 每天中午 12 点     | `0 12 * * *`  |
| 工作日早上 9 点    | `0 9 * * 1-5` |
| 每周一早上 10 点   | `0 10 * * 1`  |
| 每月 1 号上午 9 点 | `0 9 1 * *`   |

## 完整示例

### 示例一：一次性提醒

在指定时间点触发，执行一次后结束。

```json
{
  "version": 1,
  "jobs": [
    {
      "id": "0dd466ae-d52a-448f-ad01-2fc719f1f48c",
      "name": "test2",
      "description": "test2",
      "enabled": true,
      "schedule": {
        "kind": "at",
        "atMs": 1770449700000
      },
      "sessionTarget": "isolated",
      "wakeMode": "next-heartbeat",
      "payload": {
        "kind": "agentTurn",
        "message": "回复内容是test2",
        "deliver": true,
        "channel": "feishu",
        "to": "ou_XXXXXXXXXXX"
      }
    }
  ]
}
```

### 示例二：周期性提醒

每隔固定时间触发一次，持续执行。

```json
{
  "version": 1,
  "jobs": [
    {
      "id": "50f53ed1-4ad6-4ed2-9984-fdd4eba1fdab",
      "name": "测试1",
      "description": "测试1",
      "enabled": true,
      "schedule": {
        "kind": "every",
        "everyMs": 60000
      },
      "sessionTarget": "isolated",
      "wakeMode": "next-heartbeat",
      "payload": {
        "kind": "agentTurn",
        "message": "回复这是测试1",
        "deliver": true,
        "channel": "feishu",
        "to": "ou_XXXXXXXXXXX"
      }
    }
  ]
}
```

### 示例三：Cron 表达式定时提醒

按 cron 表达式调度，适用于基于日历规律的周期性任务。

```json
{
  "version": 1,
  "jobs": [
    {
      "id": "0ec68ffa-07b2-4ca6-93ee-75edd26b4b74",
      "name": "cron",
      "description": "cron",
      "enabled": true,
      "schedule": {
        "kind": "cron",
        "expr": "0 7 * * *"
      },
      "sessionTarget": "isolated",
      "wakeMode": "next-heartbeat",
      "payload": {
        "kind": "agentTurn",
        "message": "cron",
        "deliver": true,
        "channel": "feishu",
        "to": "ou_XXXXXXXXXXX"
      }
    }
  ]
}
```

## 频道检测

1. **获取频道类型**：从运行时 `channel` 属性获取（如 `feishu`）
2. **获取用户 ID**：从当前会话或消息上下文获取（如 `ou_xxxx`）
3. **始终自动检测**：使用发起请求的原始频道，不要硬编码

## 消息内容指南

- **避免纯文本消息**，需要包含让 Agent 生成响应的指令
- **使用完整的指令句**，确保 Agent 处理后产生可见回复

## 实现步骤

1. 检测当前频道类型和用户 ID
2. 将用户的时间请求转换为时间戳（毫秒）或间隔毫秒数
3. 构建完整的 job 配置（固定字段 + 动态字段）
4. 调用 API 创建定时任务
5. 确认创建成功，告知用户

## 常见坑点

| 错误做法                     | 正确做法                       |
| ---------------------------- | ------------------------------ |
| 硬编码 channel 和 to         | 从当前上下文自动检测           |
| `sessionTarget` 设为 `main`  | 必须设为 `isolated`            |
| `deliver` 缺失或设为 `false` | 必须设为 `true`                |
| `enabled` 缺失或设为 `false` | 必须显式设为 `true`            |
| `payload.to` 缺失或为空      | **必须填写**，否则消息无法送达 |
