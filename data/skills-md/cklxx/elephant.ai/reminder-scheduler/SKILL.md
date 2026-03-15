---
name: reminder-scheduler
description: 统一提醒调度：单次提醒与周期提醒计划的创建、查询、取消和到期扫描。
triggers:
  intent_patterns:
    - "提醒|remind|timer|定时|倒计时|schedule|cron|周期任务|闹钟|alarm"
  context_signals:
    keywords: ["提醒", "timer", "schedule", "cron", "周期"]
  confidence_threshold: 0.55
priority: 7
requires_tools: [bash]
max_tokens: 240
cooldown: 30
---

# reminder-scheduler

一个 skill 同时覆盖两类能力：

- 单次提醒：延迟触发（如 30 分钟后提醒）
- 周期计划：维护长期提醒计划（如每周复盘）

## 调用

```bash
# 单次提醒：设置、查看、取消
python3 skills/reminder-scheduler/run.py set_once --delay 30m --task "喝水提醒"
python3 skills/reminder-scheduler/run.py list_once
python3 skills/reminder-scheduler/run.py cancel_once --id timer-12345

# 周期计划：创建/更新、查看、删除、到期扫描、执行后推进
python3 skills/reminder-scheduler/run.py upsert_plan --name weekly-retro --schedule "0 18 * * 5" --task "发送复盘提醒" --next-run-at 2026-03-06T10:00:00Z
python3 skills/reminder-scheduler/run.py list_plans
python3 skills/reminder-scheduler/run.py due_plans --now 2026-03-06T10:00:00Z
python3 skills/reminder-scheduler/run.py delete_plan --name weekly-retro
python3 skills/reminder-scheduler/run.py touch_plan --name weekly-retro --next-run-at 2026-03-13T10:00:00Z
```

## 参数

### `set_once`
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| delay | string | 是 | 延迟时间（`30s` / `5m` / `2h`） |
| task | string | 是 | 提醒内容 |

### `cancel_once`
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 单次提醒 ID |

### `upsert_plan`
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 计划名（唯一键） |
| schedule | string | 是 | 周期表达式（cron 字符串） |
| task | string | 是 | 提醒内容 |
| next_run_at | string | 否 | 下一次执行时间（ISO8601） |
| channel | string | 否 | 渠道，默认 `lark` |
| enabled | bool | 否 | 是否启用，默认 `true` |
| metadata | object | 否 | 扩展元数据 |

### `list_plans`
无参数，返回当前所有周期计划。

### `delete_plan`
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 否 | 计划名；与 `id` 至少提供一个 |
| id | string | 否 | 计划 ID；与 `name` 至少提供一个 |

当同时提供 `name` 和 `id` 时，必须命中同一条记录才会删除。

### `due_plans`
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| now | string | 否 | 当前时间（ISO8601）；未提供时取系统 UTC 时间 |

### `touch_plan`
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 否 | 计划名；与 `id` 至少提供一个 |
| id | string | 否 | 计划 ID；与 `name` 至少提供一个 |
| next_run_at | string | 否 | 更新下一次执行时间（ISO8601） |

当同时提供 `name` 和 `id` 时，必须命中同一条记录才会更新。
