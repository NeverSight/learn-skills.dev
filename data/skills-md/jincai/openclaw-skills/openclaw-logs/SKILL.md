---
name: openclaw-logs
description: 查询和分析 OpenClaw gateway 日志。当用户提到「查日志」「openclaw 发生了什么」「openclaw 日志」「gateway 日志」「查看最近的错误」「openclaw 最近怎么了」「openclaw 报错」或询问 OpenClaw 在某个时间段内的运行情况时，使用此技能。支持时间范围查询、按类别过滤（error/restart/telegram/plugin/acp/config 等）、自动去噪、时区转换，输出结构化的事件时间线。
---

# OpenClaw Log Query

查询 OpenClaw gateway 日志，生成结构化的事件时间线。

## Quick Start

运行脚本获取日志数据，然后基于输出为用户分析：

```bash
# 查询指定时间段（北京时间）
python3 ~/.claude/skills/openclaw-logs/scripts/query_logs.py --from "19:20" --to "20:00"

# 查询最近 N 分钟/小时
python3 ~/.claude/skills/openclaw-logs/scripts/query_logs.py --last 30m
python3 ~/.claude/skills/openclaw-logs/scripts/query_logs.py --last 2h

# 只看错误
python3 ~/.claude/skills/openclaw-logs/scripts/query_logs.py --from "19:00" --to "20:00" --category error

# 只看重启事件
python3 ~/.claude/skills/openclaw-logs/scripts/query_logs.py --last 1h --category restart

# 指定日期
python3 ~/.claude/skills/openclaw-logs/scripts/query_logs.py --from "2026-03-03 22:00" --to "2026-03-04 02:00"

# 详细模式（含 cron 心跳等噪声）
python3 ~/.claude/skills/openclaw-logs/scripts/query_logs.py --last 1h --verbose
```

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--from` | Start time (HH:MM or YYYY-MM-DD HH:MM), Beijing time | `"19:20"`, `"2026-03-04 19:20"` |
| `--to` | End time, Beijing time | `"20:00"` |
| `--last` | Relative time window from now | `30m`, `2h` |
| `--date` | Override date for HH:MM times (default: today) | `2026-03-03` |
| `--category` / `-c` | Filter by event category | `error`, `restart`, `plugin`, `telegram`, `acp`, `config`, `agent`, `gateway` |
| `--verbose` / `-v` | Include normally-filtered noise (cron heartbeats etc) | |

## Categories

The script auto-categorizes each log entry:

- **ERROR** - Failures, rate limits, authentication errors
- **RESTART** - SIGTERM/SIGUSR1, draining, shutdown/startup
- **PLUGIN** - Plugin install, load, acpx backend
- **TELEGRAM** - Message sends, bot command issues
- **ACP** - ACP identity reconcile, agent dispatch
- **CONFIG** - Config changes, reload, provider updates
- **WS** - WebSocket connections (webchat UI)
- **HEALTH** - Health monitor checks and restarts
- **AGENT** - Agent model info, embedded run results
- **GATEWAY** - Listener, canvas, heartbeat, browser control
- **CRON** - Cron job triggers

## Log Sources

The script reads from multiple sources and deduplicates:

1. `~/.openclaw/logs/gateway.log` - Plain text, mixed UTC/+08:00 timestamps
2. `~/.openclaw/logs/gateway.err.log` - Plain text, errors and warnings
3. `/tmp/openclaw/openclaw-YYYY-MM-DD.log` - Structured JSON (one file per day)

All timestamps are normalized to Beijing time (UTC+8) in the output.

## Workflow

1. Run the script with the user's time range
2. Read the output - it includes a **Summary** (category counts), **Errors** (highlighted), and **Timeline** (chronological)
3. Provide analysis to the user: what happened, what's concerning, and any suggested actions
4. If the user asks about a specific issue, use `--category` to drill down

When the user's question is vague (like "openclaw 怎么了"), start with `--last 30m` to see recent activity, then narrow down based on what you find.
