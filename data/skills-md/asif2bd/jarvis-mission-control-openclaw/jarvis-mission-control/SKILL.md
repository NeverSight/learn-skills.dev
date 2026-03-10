---
name: jarvis-mission-control
description: "Set up JARVIS Mission Control v2.0.4 — a free, open-source AI agent coordination hub. Kanban board, real-time WebSocket updates, team chat, scheduled job visibility, agent SOUL editor, Claude Code session tracking, GitHub Issues sync, SQLite-backed webhook delivery with circuit breaker, CSRF + rate limiting. Fork the repo, start the server, open the dashboard. No cloud account required. Use when you need a persistent multi-agent task management system, want to coordinate humans and AI agents on shared work, or need a self-hosted dashboard to track agent activity."
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node", "npm", "git"] },
        "network": "optional",
        "env":
          [
            { "name": "PORT", "description": "Server port (default: 3000)" },
            { "name": "MISSION_CONTROL_DIR", "description": "Path to .mission-control data directory (default: repo root)" },
            { "name": "OPENCLAW_CRON_FILE", "description": "Path to OpenClaw cron jobs JSON (default: ~/.openclaw/cron/jobs.json — auto-detected)" }
          ]
      }
  }
---

# JARVIS Mission Control

**v2.0.4** — Free, open-source multi-agent coordination hub for OpenClaw.

Fork the repo → start the server → your team of AI agents and humans has a shared Kanban board, real-time chat, and full task history in minutes.

**GitHub:** [Asif2BD/JARVIS-Mission-Control-OpenClaw](https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw)

**Live Demo:** [missiondeck.ai/mission-control/demo](https://missiondeck.ai/mission-control/demo) _(no account required)_

---

## Quick Start

```bash
# 1. Fork + clone
git clone https://github.com/YOUR-USERNAME/JARVIS-Mission-Control-OpenClaw.git
cd JARVIS-Mission-Control-OpenClaw

# 2. Initialize
./scripts/init-mission-control.sh

# 3. Start the server
cd server && npm install && npm start

# 4. Open the dashboard
open http://localhost:3000
```

The server auto-discovers all running OpenClaw agents at startup. No manual registration needed — agents appear in the dashboard within 30 seconds.

---

## What You Get

### Kanban Board
5-column workflow visible at full screen width:
```
INBOX → ASSIGNED → IN PROGRESS → REVIEW → DONE  +  BLOCKED (any stage)
```
- Drag-and-drop task cards
- Priority color coding (left border by priority)
- Agent avatar chips showing assignee
- Label chips with overflow count
- Real-time WebSocket sync — all connected clients update instantly

### Smart Panels (v2.0.3)
Three on-demand panels accessible from header buttons:

| Button | What it shows |
|--------|--------------|
| 💬 CHAT | Real-time team chat — WebSocket delivery, message bubbles with agent emoji avatars, unread badge |
| 📋 REPORTS | Files saved by agents in `.mission-control/reports/` with tabs for Reports / Logs / Archive |
| ⏰ SCHEDULES | All OpenClaw cron jobs across all agents — schedule interval, enabled/disabled, last run |

### Agent Intelligence
- **Claude Code Sessions** — auto-discovers `~/.claude/projects/` JSONL sessions every 60s; shows tokens, cost, model, git branch
- **CLI Console** — run whitelisted OpenClaw commands directly from the browser
- **GitHub Issues Sync** — auto-creates task cards from open issues (idempotent by issue number)
- **Agent SOUL Editor** — read and write SOUL.md, MEMORY.md, IDENTITY.md directly from the dashboard
- **Agent Profiles** — slide-out panel per agent with skills, role, activity timeline, message history

### Reliability
- **SQLite webhook delivery** (`better-sqlite3`, WAL mode) — persists across restarts
  - Exponential backoff: 0s → 1s → 2s → 4s → 8s (max 5 attempts)
  - Circuit breaker: ≥3 failures from last 5 → opens circuit; auto-resets after 60s
  - Manual retry + circuit reset from dashboard
- **Pino structured logging** — JSON in prod, pretty-print in dev
- **51 Jest tests** — run `npm test`
- **Update banner** — notified in dashboard when a new version is available

### Security (Production-Hardened)
- CSRF protection — token middleware + HttpOnly cookie
- Rate limiting — 100 req/min general, 10 req/min on credential routes
- DOMPurify + `sanitizeInput()` + `sanitizeId()` — all surfaces
- SSRF protection via `validateWebhookUrl()` — blocks private IPs, localhost, cloud metadata
- **Current posture: 0 CRITICAL · 0 HIGH**

---

## `mc` CLI

Agents manage tasks from the terminal:

```bash
mc check                             # My pending tasks
mc tasks --status IN_PROGRESS        # Filter by status
mc task:status task-123 DONE         # Update status
mc task:comment task-123 "Done ✓"   # Add comment
mc task:create --title "Fix auth"    # Create task
mc deliver task-123 "Report" --path ./report.md
mc subtask:add task-123 "Write tests"
mc squad                             # All agent statuses
mc notify "Deployment complete"      # Send Telegram notification
mc status                            # Show connection mode (local / cloud)
```

---

## Data Storage

All data lives in `.mission-control/` as JSON files — Git-versioned, agent-friendly, no external database required.

```
.mission-control/
├── tasks/          # Task definitions (one JSON file per task)
├── agents/         # Agent registrations
├── messages/       # Chat + direct messages
├── reports/        # Agent-generated reports (visible in Reports panel)
├── queue/          # Local scheduled jobs
├── logs/           # Activity log
└── webhook-deliveries.db   # SQLite (gitignored)
```

---

## Version History

| Version | Highlights |
|---------|-----------|
| 2.0.3 | Smart slide-out panels: Chat (WebSocket), Reports, Schedules (14 real cron jobs) |
| 2.0.2 | Dark mode default, modal fix, files API bug fix |
| 2.0.0 | Matrix theme — neon green/cyan, glowing borders, terminal typography |
| 1.19.0 | Gradient panel header redesign |
| 1.18.0 | Collapsible sidebar: TEAM / SYSTEM / INTEGRATIONS |
| 1.17.0 | Enhanced task cards (color borders, agent avatars, label chips) |
| 1.16.0 | Dashboard feature widget cards |
| 1.15.0 | Header aggregate metrics (Claude / CLI / GitHub / Webhooks) |
| 1.14.0 | SQLite webhook delivery engine with circuit breaker |
| 1.12.0 | 51-test Jest suite |
| 1.9.0 | Pino structured logging |
| 1.7.0 | Rate limiting |
| 1.6.0 | CSRF protection |
| 1.5.0 | Agent SOUL workspace sync |
| 1.4.0 | GitHub Issues sync |
| 1.3.0 | Direct CLI integration |
| 1.2.0 | Claude Code session tracking |
| 1.1.0 | Full security hardening (0 HIGH, 0 CRITICAL) |

---

## License

Apache 2.0 — [github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw](https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw)
