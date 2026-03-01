---
name: hummingbot-heartbeat
description: OpenClaw cron job that delivers hourly Hummingbot status updates to your chat — API health, Gateway container, active bots/controllers, executors, and portfolio balances.
---

# hummingbot-heartbeat

An OpenClaw cron skill that runs every hour and delivers a formatted Hummingbot status report to your connected chat channel (Telegram, Discord, etc.). Covers API health, Gateway container, active bots/controllers, executors, and portfolio balances.

## Installation

```bash
clawhub install hummingbot-heartbeat
```

Or manually clone into your skills directory.

## Quick Start

### 1. Set up the OpenClaw cron job

Ask your OpenClaw agent:

> "Set up the hummingbot-heartbeat cron job"

The agent will resolve the skill path and register it with `openclaw cron`. Or do it manually:

```bash
# Replace <SKILL_PATH> with the actual installed path
openclaw cron add \
  --name "hummingbot-heartbeat" \
  --description "Hourly Hummingbot status check" \
  --every 1h \
  --announce \
  --channel telegram \
  --message "Run this and send output verbatim: python3 <SKILL_PATH>/scripts/bot_status.py"
```

### 2. Run manually (debug)

```bash
python3 scripts/bot_status.py
python3 scripts/bot_status.py --json
```

## Configuration

Set via environment variables or a `.env` file in the skill directory:

```bash
# .env (optional — defaults shown)
HUMMINGBOT_API_URL=http://localhost:8000
API_USER=admin
API_PASS=admin
```

| Variable | Default | Description |
|----------|---------|-------------|
| `HUMMINGBOT_API_URL` | `http://localhost:8000` | Hummingbot API base URL |
| `API_USER` | `admin` | API username |
| `API_PASS` | `admin` | API password |

## Requirements

- Python 3.9+
- Hummingbot API running (see `hummingbot-deploy` skill)
- Docker (optional — Gateway status check skipped if Docker unavailable)

## Sample Output

```
🤖 Hummingbot Status — Feb 28, 2026 09:06 AM

**Infrastructure**
  API:     ✅ Up (v1.0.1)
  Gateway: ✅ Up 17 hours

**Active Bots:** none

**Active Executors:** none

**Portfolio** (total: $187.23)
  Token           Units       Price      Value
  ------------ ----------- ---------- ----------
  SOL            2.0639    $81.4996    $168.20
  USDC          19.0286     $1.0000     $19.03
```

## What It Checks

| Check | Endpoint | Notes |
|-------|----------|-------|
| API health | `GET /` | Returns version |
| Gateway | `docker ps \| grep gateway` | Skipped if Docker unavailable |
| Active bots | `GET /bot-orchestration/status` | Lists controller configs |
| Active executors | `POST /executors/search` | Filters out CLOSED/FAILED |
| Portfolio | `POST /portfolio/history` | Latest balances with prices |
