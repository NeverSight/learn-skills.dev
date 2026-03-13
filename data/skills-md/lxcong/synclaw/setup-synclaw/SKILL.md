---
name: setup-synclaw
description: Install and run SyncClaw from scratch. Use when the user says "setup synclaw", "install synclaw", "deploy synclaw", "init synclaw", or needs to get SyncClaw running on a new machine. SyncClaw is an intelligent task console that bridges human task management with autonomous AI agent execution — a kanban board where tasks are dispatched to AI agents with real-time thought streaming.
---

# Setup SyncClaw

## Prerequisites

- Node.js 20+
- Git
- An [OpenClaw Gateway](https://github.com/nicepkg/openclaw) instance (optional, for agent execution)

## Quick Setup

Run the bundled setup script:

```bash
bash scripts/setup.sh --gateway-url ws://localhost:18789 --gateway-token YOUR_TOKEN
```

Options:
- `--dir <path>` — parent directory for the clone (default: current directory)
- `--gateway-url <url>` — OpenClaw Gateway WebSocket endpoint (default: `ws://localhost:18789`)
- `--gateway-token <token>` — Gateway auth token

The script clones the repo, installs deps, configures `.env`, initializes the SQLite database, builds for production, and installs the `synclaw` CLI globally.

## Manual Setup

```bash
git clone https://github.com/lxcong/synclaw.git && cd synclaw
npm install
cp .env.example .env   # edit with your Gateway URL and token
npm run db:generate
npm run db:push
npm run db:seed         # optional: sample data
npm run build
npm install -g synclaw  # install CLI globally
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQLite path | `file:./dev.db` |
| `OPENCLAW_GATEWAY_URL` | Gateway WebSocket endpoint | `ws://localhost:18789` |
| `OPENCLAW_GATEWAY_TOKEN` | Gateway auth token | — |

## CLI Usage

After setup, manage the server with the `synclaw` CLI (run from the project directory):

```
synclaw start [-p port] [-H host] [-d dev]   Start server
synclaw stop [-t timeout]                     Stop server
synclaw restart                               Restart server
synclaw status                                Show PID, uptime, Gateway status
synclaw logs [-f] [-n lines]                  View/follow logs
```

## Verification

After setup, verify everything works:

```bash
cd synclaw
synclaw start
synclaw status        # should show Running with PID and port
curl localhost:3000   # should return HTML
synclaw stop
```
