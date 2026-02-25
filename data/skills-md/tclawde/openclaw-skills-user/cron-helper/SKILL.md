---
name: cron-helper
description: 使用 openclaw cron CLI 管理定时任务。当用户需要周期提醒、定时任务、后台检查、定时执行 agent 任务时触发。关键词：定时、每天/每周/每小时/每分钟/每秒、提醒、schedule、remind、every、cron、定时任务、稍后执行、延迟执行、预定、计划、闹钟、倒计时、X分钟后、X秒后、几点几分。
---

# Cron Helper Skill

**Purpose:** Guides me to use `openclaw cron` CLI for time-based tasks and send logs on create/remove.

**When to use:**
- User asks for periodic/reminder tasks
- User mentions "remind me every X"
- User needs scheduled background checks
- User wants agent to perform a task at a specific time

---

## Core Principle

**Always prefer cron over manual timing.**

Reason: I lack an internal clock. Manual "track time yourself" fails because I can get absorbed in reading/thinking and lose track of time. Cron is an external clock that works reliably.

---

## Main vs Isolated Session

### Isolated Session (RECOMMENDED for tasks) ✅ Best Practice

Use `--session isolated` when you want the agent to **actually perform a task**:
- Agent receives the message and executes it
- Can use tools (exec, read, message, etc.)
- Can deliver output to a channel
- Does not pollute main conversation history

**Format:**
```bash
openclaw cron add \
  --name "job_name" \
  --cron "0 9 * * *" \
  --session isolated \
  --message "Task instructions for the agent" \
  --deliver \
  --channel feishu
```

### Main Session (simple notifications only)

Use `--session main` with `--system-event` for **simple notifications only**:
- Just displays a message in main chat
- Agent does NOT execute any tasks
- No tool calls, no delivery

**Format:**
```bash
openclaw cron add \
  --name "reminder" \
  --at "+30m" \
  --session main \
  --system-event "Reminder: check email"
```

---

## How I Should Respond

### Step 1: Detect the request
Keywords: "every", "remind", "schedule", "定时", "每小时/每天/每周", "在X分钟后执行"

### Step 2: Ask for details
Get from user:
- **What** - task description or notification message
- **When** - schedule (e.g., "every 2 hours", "at 9am daily", "in 10 minutes")
- **Delivery** - does output need to be sent to a chat? (default: no)
- **Name** - job name (optional, auto-generated if not provided)

### Step 3: Create cron job

**For agent tasks (RECOMMENDED):**
```bash
openclaw cron add \
  --name "task_name" \
  --at "+10m" \
  --session isolated \
  --message "Your task instructions here" \
  --deliver \
  --channel feishu
```

**For simple reminders:**
```bash
openclaw cron add \
  --name "reminder" \
  --at "+10m" \
  --session main \
  --system-event "Your reminder message"
```

**Remove a cron job:**
```bash
openclaw cron rm <job_id>
```

**List all cron jobs:**
```bash
openclaw cron list
```

**Other useful commands:**
```bash
openclaw cron status          # 查看调度器状态
openclaw cron run <job_id>    # 立即触发任务
openclaw cron enable <job_id> # 启用任务
openclaw cron disable <job_id> # 禁用任务
openclaw cron runs <job_id>   # 查看执行历史
```

---

## Delivery Options

When using `--session isolated`, you can deliver output to a chat:

| Option | Description |
|--------|-------------|
| `--deliver` | Enable delivery (required for channel output) |
| `--channel <name>` | Channel: feishu, telegram, slack, whatsapp, etc. |
| `--to <dest>` | Channel-specific target (chat ID, phone, etc.) |
| `--post-mode full` | Post full output instead of summary |

**Examples:**
```bash
# Deliver to Feishu
--deliver --channel feishu

# Deliver to Telegram
--deliver --channel telegram --to "-1001234567890"

# Deliver with full output
--deliver --channel feishu --post-mode full
```

---

## Common Options

| Option | Description |
|--------|-------------|
| `--cron <expr>` | Cron expression (5-field or 6-field with seconds) |
| `--every <duration>` | Run every duration (e.g., 10m, 1h) |
| `--at <when>` | Run once at time (ISO or +duration, supports m/s) |
| `--tz <iana>` | Timezone (default: local) |
| `--session main\|isolated` | Target session (default: main) |
| `--system-event <text>` | System event payload (main session only) |
| `--message <text>` | Agent message payload (isolated session only) |
| `--delete-after-run` | Delete one-shot job after success |
| `--disabled` | Create job in disabled state |

---

## Step 4: Send log

### On CREATE/REMOVE only:
After creating or removing cron jobs, send ONE log with the exact command:

**Log format:**
```bash
# 新增任务
[HH:MM] CRON ✅
$ openclaw cron add \
  --name "job_name" \
  --at "+10m" \
  --session isolated \
  --message "task description" \
  --deliver \
  --channel feishu

# 删除任务
[HH:MM] CRON ❌
$ openclaw cron rm <job_id>
```

**Examples:**
```bash
# 新增
[21:30] CRON ✅
$ openclaw cron add \
  --name "daily-summary" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "总结今天的工作" \
  --deliver \
  --channel feishu

# 删除
[21:41] CRON ❌
$ openclaw cron rm 983a0f0e-0976-414a-b3d0-fd09c533e301
```

**Key points:**
- Send log ONLY on create/remove, NOT on execution
- Keep it minimal: One command block, no extra text

**Cron → Human mapping (五位 - 分时日月周):**
- `*/5 * * * *` → 每5分钟
- `*/30 * * * *` → 每30分钟
- `0 * * * *` → 每1小时
- `0 */2 * * *` → 每2小时
- `0 9 * * *` → 每天1次(09:00)
- `0 10,22 * * *` → 每天2次(10:00,22:00)
- `0 9 * * 1` → 每周1次(周一09:00)

**Cron → Human mapping (六位 - 秒分时日月周):**
- `*/1 * * * * *` → 每1秒
- `*/5 * * * * *` → 每5秒
- `*/30 * * * * *` → 每30秒

---

## Best Practice Summary

| Use Case | Session | Payload | Delivery |
|----------|---------|---------|----------|
| Agent performs task | `isolated` | `--message` | `--deliver` ✅ |
| Simple notification | `main` | `--system-event` | ❌ |

**Rule of thumb:** If you want the agent to **do something** (use tools, send messages), use `--session isolated` + `--message`.

---

## What NOT To Do

❌ Don't say "I'll set a reminder myself"
❌ Don't try to track time manually
❌ Don't use `--system-event` when you need the agent to execute tasks
❌ Don't forget `--deliver` when you need output sent to chat
❌ Don't send execution logs (only log on create/remove)

✅ Always use the `openclaw cron` CLI
✅ Use `--session isolated` for agent tasks
✅ Use `--session main` for simple notifications only
✅ Send log on create/remove only
✅ Keep log simple and clean

---

## Common Schedule Patterns

### 五位 Cron（分 时 日 月 周）
| Frequency | Cron Expression | CLI Flag |
|-----------|-----------------|----------|
| Every 5 min | `*/5 * * * *` | `--cron "*/5 * * * *"` |
| Every 30 min | `*/30 * * * *` | `--cron "*/30 * * * *"` |
| Every hour | `0 * * * *` | `--cron "0 * * * *"` |
| Every 2 hours | `0 */2 * * *` | `--cron "0 */2 * * *"` |
| Daily at 9am | `0 9 * * *` | `--cron "0 9 * * *"` |
| Twice daily (10am, 10pm) | `0 10,22 * * *` | `--cron "0 10,22 * * *"` |
| Weekly (Monday 9am) | `0 9 * * 1` | `--cron "0 9 * * 1"` |

### 六位 Cron（秒 分 时 日 月 周）
| Frequency | Cron Expression | CLI Flag |
|-----------|-----------------|----------|
| Every 1 second | `*/1 * * * * *` | `--cron "*/1 * * * * *"` |
| Every 5 seconds | `*/5 * * * * *` | `--cron "*/5 * * * * *"` |
| Every 30 seconds | `*/30 * * * * *` | `--cron "*/30 * * * * *"` |

Duration flags:
| Frequency | CLI Flag |
|-----------|----------|
| Every 10 minutes | `--every "10m"` |
| Every 2 hours | `--every "2h"` |
| Once in 20 minutes | `--at "+20m"` |
| Once in 20 seconds | `--at "+20s"` |

---

**Loaded automatically** when skill is installed.
