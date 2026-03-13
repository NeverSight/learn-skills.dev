---
name: openclaw
description: OpenClaw documentation reference. OpenClaw is a self-hosted, open-source (MIT) gateway that connects chat apps (WhatsApp, Telegram, Discord, iMessage, Slack, etc.) to AI agents. Use when the user asks about OpenClaw setup, configuration, channels, automation, deployment, or any OpenClaw feature.
---

# OpenClaw Documentation

OpenClaw is a **self-hosted gateway** that connects chat apps — WhatsApp, Telegram, Discord, iMessage, Slack, and more — to AI coding agents. A single Gateway process runs on your hardware and bridges messaging apps to an always-available AI assistant.

**Requirements:** Node 22+, an API key (Anthropic recommended), 5 minutes.
**Config:** `~/.openclaw/openclaw.json`
**Default dashboard:** `http://127.0.0.1:18789/`

## Quick start

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
openclaw channels login
openclaw gateway --port 18789
```

## Quick Reference

| I want to... | Read |
|---|---|
| Install OpenClaw | [references/installation.md](references/installation.md) |
| Connect a chat platform | [references/channels-overview.md](references/channels-overview.md) |
| Set up WhatsApp, Signal, iMessage, LINE, Telegram, Nostr | [references/channels-messaging-apps.md](references/channels-messaging-apps.md) |
| Set up Discord, Slack, Teams, Mattermost, Google Chat, IRC, Matrix, Feishu | [references/channels-team-platforms.md](references/channels-team-platforms.md) |
| Understand core architecture (runtime, workspace, sessions, compaction) | [references/core-concepts.md](references/core-concepts.md) |
| Use the CLI | [references/cli-reference.md](references/cli-reference.md) |
| Set up cron jobs, hooks, webhooks, Gmail PubSub | [references/automation.md](references/automation.md) |
| Configure agent tools and slash commands | [references/tools.md](references/tools.md) |
| Run multiple agents | [references/multi-agent.md](references/multi-agent.md) |
| Deploy to cloud (exe.dev, Northflank, Fly.io, GCP, DigitalOcean) | [references/deployment.md](references/deployment.md) |
| Manage secrets and gateway operations | [references/gateway-operations.md](references/gateway-operations.md) |
| Use the web dashboard or TUI | [references/web-ui.md](references/web-ui.md) |
| Extend with plugins or configure model providers | [references/plugins-providers.md](references/plugins-providers.md) |
| Use macOS app, Voice Wake, or Android | [references/platforms.md](references/platforms.md) |
| Build, test, or contribute | [references/development-reference.md](references/development-reference.md) |

## Reference files

### [references/overview.md](references/overview.md)
Home page: what OpenClaw is, how it works (Gateway as central hub), quick-start install, dashboard access, basic config.

### [references/core-concepts.md](references/core-concepts.md)
Agent Runtime (pi-mono embedded runtime, bootstrap files), Agent Workspace (SOUL.md, USER.md, TOOLS.md, HEARTBEAT.md, memory/), System Prompt assembly, Compaction (context window management), Retry Policy (exponential backoff), Memory v2 Research (offline-first architecture).

### [references/channels-overview.md](references/channels-overview.md)
Channel index (20+ platforms), Channel Routing (session key formats, routing priority), Groups (group policy, mention gating), Group Messages (WhatsApp-specific), Broadcast Groups (parallel/sequential multi-agent), Channel Location Parsing, Pairing (DM/device pairing, 8-char codes).

### [references/channels-messaging-apps.md](references/channels-messaging-apps.md)
BlueBubbles/iMessage (tapbacks, effects, voice memos), Signal (signal-cli, QR pairing), LINE (Flex messages, quick replies), grammY/Telegram (webhook + long-poll), Nostr (NIP-04 encrypted DMs).

### [references/channels-team-platforms.md](references/channels-team-platforms.md)
Discord (guilds, forums, Components v2, voice, PluralKit), Slack (Socket Mode, Events API, threading, streaming), MS Teams (Azure Bot, Adaptive Cards, SharePoint), Mattermost (chat modes, reactions), Google Chat (HTTP webhooks), Feishu/Lark (WebSocket), Matrix (E2EE, Beeper), IRC (NickServ, per-channel tools), Nextcloud Talk, Synology Chat.

### [references/automation.md](references/automation.md)
Cron Jobs (one-shot `at`, recurring `cron`/`every`, isolated sessions), Cron vs Heartbeat decision guide, Hooks (event-driven TypeScript handlers, HOOK.md metadata), Webhooks (`/hooks/wake` and `/hooks/agent`), Gmail PubSub, Polls (cross-channel), Auth Monitoring (OAuth expiry, ntfy alerts), Troubleshooting.

### [references/cli-reference.md](references/cli-reference.md)
All `openclaw <command>` subcommands: browser (tab/snapshot/screenshot management), completion (shell completions), dashboard (open Control UI), logs (tail Gateway logs), memory (semantic indexing/search), models (discovery, defaults, auth profiles), nodes (paired devices), status (channel/session diagnostics), system (enqueue events, heartbeat controls, presence).

### [references/tools.md](references/tools.md)
Tools Index (all first-class tools: apply_patch, exec, web_search, browser, canvas, nodes, cron, gateway, etc.), Slash Commands (/help, /status, /model, /think, /exec, /tts, /config, /debug, /reset, /stop, etc.), Reactions (cross-channel emoji semantics), Browser Login (Chrome profile auth), ClawHub (public skill registry), LLM Task (JSON-only tasks with schema validation).

### [references/gateway-operations.md](references/gateway-operations.md)
Heartbeat (periodic agent turns, intervals, HEARTBEAT_OK contract, active hours, visibility), Secrets Management (env/file/exec sources, 1Password/Vault/sops integration).

### [references/multi-agent.md](references/multi-agent.md)
Multi-Agent Routing: running multiple isolated agents in one Gateway, routing rules (most-specific-wins bindings), DM splits, per-agent accounts, per-agent sandbox/tool policies.

### [references/installation.md](references/installation.md)
Install Overview (Node 22+, npm, curl one-liner, Docker/Podman/Nix/Ansible), Docker (Compose, ClawDock, persistent volumes, agent sandbox), Node.js (nvm/fnm/mise, PATH troubleshooting).

### [references/deployment.md](references/deployment.md)
exe.dev (VM deploy, nginx proxy, device pairing), Northflank (one-click template, persistent storage).

### [references/platforms.md](references/platforms.md)
macOS app (Skills via gateway, API key management, remote mode), Voice Wake (wake-word detection, push-to-talk).

### [references/plugins-providers.md](references/plugins-providers.md)
Plugin Agent Tools (`registerTool` API, allowlist/denylist), OpenAI Provider (API key, Codex, WebSocket/SSE transport).

### [references/web-ui.md](references/web-ui.md)
Control UI (Vite + Lit SPA: chat, channel status, sessions, cron, skills, nodes, exec approvals, config editing, logs, updates, Tailscale Serve for remote access).

### [references/development-reference.md](references/development-reference.md)
CI Pipeline (push + PR gates, smart scoping), RPC Adapters (JSON-RPC integration), TOOLS.md Template (environment notes), Tests (pnpm test, coverage, E2E, Docker smoke tests), OpenClaw Lore (community history), Onboarding Overview, Scripts.

## Key Config Files & Paths

| Path | Purpose |
|---|---|
| `~/.openclaw/openclaw.json` | Main Gateway configuration |
| `~/.openclaw/credentials/` | Stored credentials and pairing state |
| `~/.openclaw/agents/<id>/` | Per-agent workspace, sessions, state |
| `~/.openclaw/hooks/` | User-managed hook directory |
| `~/.openclaw/cron/` | Cron job storage (`jobs.json`) |
| Workspace: `SOUL.md` | Agent personality/identity |
| Workspace: `USER.md` | User preferences for the agent |
| Workspace: `TOOLS.md` | Local environment notes (cameras, SSH hosts, etc.) |
| Workspace: `HEARTBEAT.md` | Checklist for periodic heartbeat runs |
| Workspace: `BOOT.md` / `BOOTSTRAP.md` | Extra context injected at boot |
| Workspace: `AGENTS.md` | Multi-agent configuration |
| Workspace: `memory/` | Agent memory files |
| Workspace: `skills/` | Installed skills |
