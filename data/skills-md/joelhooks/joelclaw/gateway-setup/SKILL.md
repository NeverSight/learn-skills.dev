---
name: gateway-setup
displayName: Gateway Setup
description: "Set up a persistent AI agent gateway on macOS with Redis event bridge, heartbeat monitoring, and multi-session routing. Interactive Q&A to match your intent — from minimal (Redis + extension) to full (embedded daemon + Telegram + watchdog). Use when: 'set up a gateway', 'I want my agent always on', 'event bridge', 'heartbeat monitoring', 'agent notifications', or any request to make an AI agent persistent and reachable."
version: 1.0.0
author: Joel Hooks
tags: [joelclaw, gateway, setup, redis, telegram]
---

# Gateway Setup for AI Agents on macOS

This skill builds a persistent gateway for an AI coding agent on a Mac. It bridges background workflows (Inngest, cron, pipelines) into your agent's session and optionally routes responses to external channels (Telegram, WebSocket).

## Before You Start

**Required:**
- macOS (Apple Silicon preferred)
- pi coding agent installed and working
- Redis running (locally, Docker, or k8s — see `inngest-local` skill if you need this)

**Optional (unlocks more features):**
- Inngest self-hosted (for durable event-driven workflows)
- Tailscale (for secure remote access from phone/laptop)
- Telegram bot token (for mobile notifications/chat)

## Critical Setup Notes

**`GATEWAY_ROLE=central` is required for the always-on session.** Without it, the session runs as a satellite and misses heartbeats, system alerts, and any events not targeted at it specifically. Set it when launching:
```bash
GATEWAY_ROLE=central pi
```

**`serveHost` is mandatory when Inngest runs in Docker and the worker runs on the host.** The SDK advertises `localhost:3100` as its callback URL, but Docker can't reach the host's loopback. Set it in your Hono serve handler:
```typescript
inngestServe({
  client: inngest,
  functions,
  serveHost: "http://host.docker.internal:3100",
})
```
Then force re-sync: `curl -X PUT http://localhost:3100/api/inngest`

**ioredis resolution in Bun is flaky.** If you get `Cannot find module '@ioredis/commands'`, install it explicitly:
```bash
bun add @ioredis/commands
# or: rm -rf node_modules && bun install
```

**Two ioredis clients required for pub/sub.** A subscribed client can't run LRANGE, DEL, or other commands. The extension creates separate `sub` and `cmd` clients.

## Intent Alignment

Before building anything, ask the user these questions to determine scope. Adapt based on their answers.

### Question 1: What's your goal?

Present these options:
1. **Notifications only** — background jobs finish, I want to know about it without watching the terminal
2. **Always-on agent** — I want a persistent session that survives terminal closes, handles heartbeats, routes events
3. **Full gateway** — always-on + talk to my agent from Telegram/phone + multi-session routing

Each level builds on the previous. Start with what they need now.

### Question 2: What's your event source?

1. **Just cron/timers** — I want a heartbeat that checks system health periodically
2. **Inngest functions** — I have durable workflows that emit completion events
3. **Mixed** — Inngest + cron + maybe webhooks

### Question 3: How many concurrent agent sessions?

1. **One** — I run one pi session at a time
2. **Multiple** — I often have 2-5 sessions in different terminals working on different things

If multiple: enable central/satellite routing. If one: simpler single-session mode.

## Architecture Tiers

### Tier 1: Notification Bridge (simplest)

**What you get:** Background events show up in your pi session as messages.

**Components:**
- Redis (already running)
- Gateway pi extension (~100 lines)
- `pushGatewayEvent()` utility function

**How it works:**
```
Background process → Redis LPUSH → pi extension drains on notify → injected as user message
```

**Build steps:**

1. Create the extension directory:
```bash
mkdir -p ~/.pi/agent/extensions/gateway
```

2. Create `~/.pi/agent/extensions/gateway/package.json`:
```json
{
  "name": "gateway-extension",
  "private": true,
  "dependencies": {
    "ioredis": "^5.4.2"
  }
}
```

3. Install dependencies:
```bash
cd ~/.pi/agent/extensions/gateway && npm install
```

4. Create `~/.pi/agent/extensions/gateway/index.ts` with the minimal bridge:

```typescript
import type { ExtensionAPI, ExtensionContext } from "@mariozechner/pi-coding-agent";

const SESSION_ID = "main";
const EVENT_LIST = `agent:events:${SESSION_ID}`;
const NOTIFY_CHANNEL = `agent:notify:${SESSION_ID}`;

type RedisLike = {
  on(event: string, listener: (...args: unknown[]) => void): void;
  connect(): Promise<void>;
  subscribe(channel: string): Promise<unknown>;
  lrange(key: string, start: number, stop: number): Promise<string[]>;
  del(key: string): Promise<number>;
  llen(key: string): Promise<number>;
  unsubscribe(): void;
  disconnect(): void;
};

type RedisCtor = new (options: { host: string; port: number; lazyConnect: boolean }) => RedisLike;

let Redis: RedisCtor | null = null;
let sub: RedisLike | null = null;
let cmd: RedisLike | null = null;
let ctx: ExtensionContext | null = null;
let piRef: ExtensionAPI | null = null;

interface SystemEvent {
  id: string;
  type: string;
  source: string;
  payload: Record<string, unknown>;
  ts: number;
}

function formatEvents(events: SystemEvent[]): string {
  return events.map((e) => {
    const time = new Date(e.ts).toLocaleTimeString("en-US", { hour12: false });
    return `- **[${time}] ${e.type}** (${e.source})`;
  }).join("\n");
}

async function drain(): Promise<void> {
  if (!cmd || !piRef) return;
  const raw = await cmd.lrange(EVENT_LIST, 0, -1);
  if (raw.length === 0) return;

  const events = raw.reverse().map(r => {
    try { return JSON.parse(r) as SystemEvent; } catch { return null; }
  }).filter(Boolean) as SystemEvent[];

  if (events.length === 0) { await cmd.del(EVENT_LIST); return; }

  const prompt = [
    `## 🔔 ${events.length} event(s) — ${new Date().toISOString()}`,
    "", formatEvents(events), "",
    "Take action if needed, otherwise acknowledge briefly.",
  ].join("\n");

  if (ctx?.isIdle()) {
    piRef.sendUserMessage(prompt);
  } else {
    piRef.sendUserMessage(prompt, { deliverAs: "followUp" });
  }
  await cmd.del(EVENT_LIST);
}

export default function (pi: ExtensionAPI) {
  piRef = pi;

  pi.on("session_start", async (_event, _ctx) => {
    ctx = _ctx;
    if (!Redis) {
      try {
        Redis = (await import("ioredis")).default as RedisCtor;
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        _ctx.ui.notify(`Gateway extension running without Redis: ${message}`, "warning");
        return;
      }
    }

    sub = new Redis({ host: "localhost", port: 6379, lazyConnect: true });
    cmd = new Redis({ host: "localhost", port: 6379, lazyConnect: true });
    await sub.connect();
    await cmd.connect();

    await sub.subscribe(NOTIFY_CHANNEL);
    sub.on("message", () => { if (ctx?.isIdle()) drain(); });

    // Drain anything that accumulated while session was down
    const pending = await cmd.llen(EVENT_LIST);
    if (pending > 0) await drain();

    ctx.ui.setStatus("gateway", "🔗 connected");
  });

  pi.on("agent_end", async () => { drain(); });

  pi.on("session_shutdown", async () => {
    if (sub) { sub.unsubscribe(); sub.disconnect(); }
    if (cmd) { cmd.disconnect(); }
  });
}
```

5. Push events from any script:
```typescript
import Redis from "ioredis";
const redis = new Redis();

async function pushEvent(type: string, source: string, payload = {}) {
  const event = { id: crypto.randomUUID(), type, source, payload, ts: Date.now() };
  await redis.lpush("agent:events:main", JSON.stringify(event));
  await redis.publish("agent:notify:main", JSON.stringify({ type }));
}

// Example: notify when a download finishes
await pushEvent("download.complete", "my-script", { file: "video.mp4" });
```

6. Restart pi — the extension loads automatically.

### Tier 2: Always-On with Heartbeat

**Adds:** Cron heartbeat, watchdog failure detection, boot sequence.

**Additional components:**
- HEARTBEAT.md checklist (read by the agent on each heartbeat)
- Watchdog timer in the extension
- tmux or launchd for persistence

**Build steps (on top of Tier 1):**

1. Create `~/HEARTBEAT.md` (or wherever your agent's home is):
```markdown
# Heartbeat Checklist

## System Health
- [ ] Redis is reachable
- [ ] Background worker is responding
- [ ] No stuck jobs

## Pending Work
- [ ] Check inbox for unprocessed items

If nothing needs attention, reply HEARTBEAT_OK.
```

2. Add heartbeat cron — if using Inngest:
```typescript
export const heartbeatCron = inngest.createFunction(
  { id: "system-heartbeat" },
  [{ cron: "*/15 * * * *" }],
  async ({ step }) => {
    await step.run("push-heartbeat", async () => {
      await pushEvent("cron.heartbeat", "inngest", {});
    });
  }
);
```

Or without Inngest, use a simple cron/setInterval:
```bash
# crontab -e
*/15 * * * * redis-cli LPUSH agent:events:main '{"id":"'$(uuidgen)'","type":"cron.heartbeat","source":"cron","payload":{},"ts":'$(date +%s000)'}' && redis-cli PUBLISH agent:notify:main '{"type":"cron.heartbeat"}'
```

3. Add watchdog to the extension (insert after session_start):
```typescript
const WATCHDOG_THRESHOLD_MS = 30 * 60 * 1000; // 2x the 15-min interval
let lastHeartbeatTs = Date.now();
let watchdogAlarmFired = false;

setInterval(() => {
  if (!piRef || !ctx) return;
  if (watchdogAlarmFired) return;
  const elapsed = Date.now() - lastHeartbeatTs;
  if (elapsed > WATCHDOG_THRESHOLD_MS) {
    watchdogAlarmFired = true;
    piRef.sendUserMessage(`## ⚠️ MISSED HEARTBEAT\n\nNo heartbeat in ${Math.round(elapsed / 60000)} minutes. Check your worker/cron.`);
  }
}, 5 * 60 * 1000);

// Reset on heartbeat receipt (inside drain function):
// if (events.some(e => e.type === "cron.heartbeat")) {
//   lastHeartbeatTs = Date.now();
//   watchdogAlarmFired = false;
// }
```

4. Make it survive terminal close — tmux:
```bash
tmux new-session -d -s agent -x 120 -y 40 "pi"
# Attach: tmux attach -t agent
# Detach: Ctrl-B, D
```

Or launchd for full always-on:
```xml
<!-- ~/Library/LaunchAgents/com.you.agent-gateway.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.you.agent-gateway</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-c</string>
    <string>tmux new-session -d -s agent -x 120 -y 40 "GATEWAY_ROLE=central pi" && while tmux has-session -t agent 2>/dev/null; do sleep 5; done</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>/tmp/agent-gateway.log</string>
  <key>StandardErrorPath</key><string>/tmp/agent-gateway.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.you.agent-gateway.plist
```

### Tier 3: Multi-Session + Central/Satellite

**Adds:** Multiple pi sessions, smart event routing.

**When you need this:** You run 2+ pi sessions simultaneously — one for oversight, others for coding tasks. Heartbeats should only go to the oversight session.

**Key changes from Tier 1:**

1. Session ID becomes role-based:
```typescript
const ROLE = process.env.GATEWAY_ROLE ?? "satellite";
const SESSION_ID = ROLE === "central" ? "gateway" : `pid-${process.pid}`;
```

2. Sessions register in a Redis set:
```typescript
await cmd.sadd("agent:gateway:sessions", SESSION_ID);
// On shutdown:
await cmd.srem("agent:gateway:sessions", SESSION_ID);
```

3. `pushEvent` fans out to targets:
```typescript
async function pushEvent(type, source, payload, originSession?) {
  const event = { id: crypto.randomUUID(), type, source, payload, ts: Date.now() };
  const json = JSON.stringify(event);
  const sessions = await redis.smembers("agent:gateway:sessions");
  
  const targets = new Set<string>();
  if (sessions.includes("gateway")) targets.add("gateway"); // central always
  if (originSession && sessions.includes(originSession)) targets.add(originSession);
  
  for (const sid of targets) {
    await redis.lpush(`agent:events:${sid}`, json);
    await redis.publish(`agent:notify:${sid}`, JSON.stringify({ type }));
  }
}
```

4. Start your central session:
```bash
GATEWAY_ROLE=central pi  # This one gets ALL events
```

5. Other sessions start normally (satellites):
```bash
pi  # Gets only events it initiated
```

### Tier 4: External Channels (Telegram, WebSocket)

**Adds:** Talk to your agent from your phone.

This tier requires the embedded daemon approach — pi runs as a library inside a Node.js process, not as a TUI. See the joelclaw.com article "Building a Gateway for Your AI Agent" for the full architecture.

**Key components:**
- `createAgentSession()` from pi SDK — headless agent session
- grammY for Telegram bot
- Command queue that serializes all inputs (TUI, heartbeat, Telegram)
- Outbound router that sends responses back to the asking channel

This is the most complex tier. Only build it if you actually need mobile access.

## Verification Checklist

After setup, verify:
- [ ] Pi session starts and extension loads (check status bar for 🔗)
- [ ] Push a test event: `redis-cli LPUSH agent:events:main '{"id":"test","type":"test","source":"manual","payload":{},"ts":0}'` + `redis-cli PUBLISH agent:notify:main test`
- [ ] Event appears in pi session within seconds
- [ ] (Tier 2+) Heartbeat fires on schedule
- [ ] (Tier 2+) Kill the heartbeat source — watchdog alarm fires after 30 min
- [ ] (Tier 3+) Central session receives heartbeats, satellite sessions don't

## Setup Script (curl-first)

For automated setup, the user can run:
```bash
curl -sL joelclaw.com/scripts/gateway-setup.sh | bash
```

Or with a specific tier:
```bash
curl -sL joelclaw.com/scripts/gateway-setup.sh | bash -s -- 2
```

The script is idempotent, detects Redis, installs the extension, and configures persistence for Tier 2+.

## Decision Chain (compressed ADRs)

Sequential architecture decisions that led to the current gateway design. Each solved a real problem discovered in the previous iteration.

| # | ADR | Decision | Problem Solved | Key Tradeoff |
|---|-----|----------|---------------|-------------|
| 1 | [0010](/adrs/0010-system-loop-gateway) | Hybrid cron + event gateway | Manual triage bottleneck | Always-on LLM session = expensive. Cron = latency. Hybrid balances both. |
| 2 | [0018](/adrs/0018-pi-native-gateway-redis-event-bridge) | Redis event bridge (pi extension) | No Inngest→pi bridge existed | Extension-only, no separate process. Redis as the clean interface boundary. |
| 3 | [0035](/adrs/0035-gateway-session-routing-central-satellite) | Central + satellite routing | Heartbeats interrupting coding sessions | Fan-out by role. Central gets all, satellites get only origin-targeted. |
| 4 | [0036](/adrs/0036-launchd-central-gateway-session) | launchd + tmux (superseded) | Gateway session dies on terminal close | Pi needs PTY. tmux provides it. launchd restarts on crash. |
| 5 | [0037](/adrs/0037-gateway-watchdog-layered-failure-detection) | 3-layer watchdog | "Who watches the watchmen" | Extension watchdog (Inngest down), launchd tripwire (pi down), heartbeat (everything healthy). |
| 6 | [0038](/adrs/0038-embedded-pi-gateway-daemon) | Embedded pi daemon (supersedes 0036) | No mobile access, no multi-channel | Embeds pi as library. grammY for Telegram. Command queue serializes all inputs. Most complex tier. |

**Read order for full context:** 0010 → 0018 → 0035 → 0037 → 0038 (skip 0036, superseded)

## Known Limitations

1. **Drain race condition.** The extension does `LRANGE` then `DEL` — not atomic. Events pushed between those calls are deleted without processing. The in-memory `seenIds` dedup prevents double-delivery but doesn't prevent lost events. Fix: use `LRANGE` + `LTRIM` or a Redis transaction. Low-impact on single-user systems but real.

2. **Redis connection recovery is notify-only.** If Redis goes down, the extension catches the error and logs it, but doesn't retry or reconnect automatically. ioredis `retryStrategy` handles reconnection at the client level, but accumulated events during the outage may be lost.

3. **Watchdog intervals are hardcoded.** Check interval (5 min) and threshold (30 min) are constants in the extension. Should be configurable via env vars or Redis config.

4. **No persistent dedup across restarts.** The `seenIds` Set lives in memory and caps at 500. Process restart = dedup resets. For the heartbeat-every-15-min use case this is fine. For high-frequency events it could cause duplicates.

## Credits

- [OpenClaw](https://github.com/openclaw/openclaw) — gateway-daemon pattern, command queue serialization, channel plugin architecture
- [pi coding agent](https://github.com/mariozechner/pi-coding-agent) — extension API, sendUserMessage(), session lifecycle
- [Inngest](https://www.inngest.com/) — durable event-driven workflows
- [joelclaw.com/building-a-gateway-for-your-ai-agent](/building-a-gateway-for-your-ai-agent) — human summary
