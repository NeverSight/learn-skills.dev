---
name: clawd-control
description: Monitor and manage your Clawdbot agent fleet from within an agent. Query health, sessions, usage, and trigger actions via the Clawd Control dashboard API.
version: 1.0.0
author: temaki
tags: [dashboard, monitoring, fleet, management, multi-agent]
requires: [web_fetch]
---

# Clawd Control — Agent Skill

Monitor and manage your Clawdbot agent fleet through the Clawd Control dashboard API. This skill lets agents check fleet health, inspect sessions, trigger heartbeats, and manage other agents — all programmatically.

## Prerequisites

- **Clawd Control server** running and accessible (default: `http://<host>:3100`)
- **Auth credentials**: password from `auth.json` in the Clawd Control directory
- Full server: [github.com/temaki-ai/clawd-control](https://github.com/temaki-ai/clawd-control)

## Authentication

All API calls require a session cookie. Obtain one first:

```bash
curl -s -c cookies.txt http://<HOST>:3100/api/login \
  -H "Content-Type: application/json" \
  -d '{"password": "<PASSWORD>"}'
```

Or use the `Authorization: Bearer <session_token>` header.

For agents with `web_fetch`, you can use the session cookie approach or pass the token as a header.

## API Reference

### Fleet Overview

**GET /api/snapshot**
Returns the full fleet state: all agents + host metrics in a single call.

Response shape:
```json
{
  "ts": 1706000000000,
  "agents": {
    "gandalf": {
      "id": "gandalf",
      "name": "Gandalf",
      "emoji": "🧙",
      "online": true,
      "lastSeen": 1706000000000,
      "health": { "agents": [...], "uptime": 3600 },
      "sessions": { "sessions": [...] },
      "usage": { "totalCost": 12.50, "shared": true },
      "heartbeat": { "ts": 1706000000000 },
      "channels": { "channels": { "telegram": { "running": true } } },
      "cron": { "jobs": [...] }
    }
  },
  "host": {
    "hostname": "darth-maul",
    "loadAvg": [0.5, 0.3, 0.2],
    "memory": { "total": 16000000000, "used": 8000000000, "available": 8000000000 },
    "disk": { "total": 219000000000, "used": 24000000000 },
    "uptime": 86400
  }
}
```

### Individual Agent State

**GET /api/agents/:id**
Returns live state for a specific agent.

### Agent Detail (workspace files + live state)

**GET /api/agents/:id/detail**
Returns everything about an agent: config, workspace files (SOUL.md, MEMORY.md, TASKS.md, etc.), skills list, memory files, recent daily notes, and live state.

### Agent Actions

**POST /api/agents/:id/action**

Body: `{ "action": "<action_name>" }`

Available actions:
| Action | Description |
|---|---|
| `heartbeat-enable` | Enable heartbeat polling |
| `heartbeat-disable` | Disable heartbeat polling |
| `heartbeat-trigger` | Trigger an immediate heartbeat |
| `session-new` | Archive current main session, start fresh |
| `session-reset` | Delete ALL sessions (nuclear — creates backup) |

### Create Agent

**POST /api/create-agent**

Body:
```json
{
  "name": "Merry",
  "emoji": "🌿",
  "soul": "Loyal, practical, action-oriented.",
  "model": "anthropic/claude-sonnet-4-5",
  "telegramToken": "123456:ABC-DEF..."
}
```

Returns step-by-step creation log and result.

### Host Metrics

**GET /api/host**
Returns current host machine metrics (CPU load, RAM, disk, uptime).

### SSE Live Stream

**GET /api/stream**
Server-Sent Events stream. Emits:
- `snapshot` — full state on connect
- `agent` — individual agent updates (includes `removed: true` when agent is deleted)
- `host` — host metrics updates

### Security Audit

**GET /api/security-audit**
Runs security checks: secrets management, credential exposure, network/ports, system security, gateway config, account inventory.

## Usage Patterns

### Check if all agents are healthy
```
Fetch /api/snapshot, iterate agents, check each has online: true.
Flag any with online: false or stale lastSeen (> 5 min).
```

### Monitor costs
```
Fetch /api/snapshot, sum usage.totalCost across agents.
Note: usage is shared per gateway, so avoid double-counting agents on the same gateway.
```

### Trigger a heartbeat for a specific agent
```
POST /api/agents/gandalf/action with body {"action": "heartbeat-trigger"}
```

### Reset a stuck agent
```
POST /api/agents/pippin/action with body {"action": "session-new"}
This archives the current session and starts fresh.
```

## Notes

- The server binds to a specific IP by default (not 0.0.0.0) for security. Ensure your agent can reach it.
- Session tokens are in-memory and expire after `sessionTtlHours` (default: 24h).
- The SSE stream reconnects automatically on disconnect (client-side).
- Agent state is polled every 15s by default (configurable in `agents.json`).
