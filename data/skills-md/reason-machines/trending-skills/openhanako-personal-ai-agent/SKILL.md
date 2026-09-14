---
name: openhanako-personal-ai-agent
description: Build and configure personal AI agents with memory, personality, and autonomy using OpenHanako on Electron.
triggers:
  - set up OpenHanako agent
  - add a skill to Hanako
  - configure multi-agent in OpenHanako
  - how do I use OpenHanako memory system
  - create a new Hanako agent personality
  - connect Telegram to OpenHanako
  - write a custom skill for OpenHanako
  - schedule a task with Hanako cron
---

# OpenHanako Personal AI Agent

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

OpenHanako is a desktop AI agent platform built on Electron that gives each agent persistent memory, a distinct personality, and the ability to autonomously operate your computer — read/write files, run terminal commands, browse the web, execute JavaScript, and manage schedules. Multiple agents can collaborate via channel group chats or task delegation.

---

## Installation

### Download & Run

```bash
# macOS Apple Silicon — download from releases page
# https://github.com/liliMozi/openhanako/releases
# Mount the .dmg and drag to Applications

# First launch — bypass Gatekeeper (one-time):
# Right-click app → Open → Open
```

```powershell
# Windows — run the .exe installer from releases
# SmartScreen warning: click "More info" → "Run anyway"
```

### Build from Source

```bash
git clone https://github.com/liliMozi/openhanako.git
cd openhanako
npm install

# Development mode
npm run dev

# Build for production
npm run build

# Run tests
npm test
```

---

## First-Run Onboarding

On first launch, the wizard asks for:

1. **Language** — UI language preference
2. **Your name** — used by agents when addressing you
3. **Model provider** — any OpenAI-compatible endpoint
4. **Three models:**
   - `chat model` — main conversation (e.g. `gpt-4o`, `deepseek-chat`)
   - `utility model` — lightweight tasks, summarization (e.g. `gpt-4o-mini`)
   - `utility large model` — memory compilation, deep analysis (e.g. `gpt-4o`)

### Provider Configuration Examples

```json
// OpenAI
{
  "baseURL": "https://api.openai.com/v1",
  "apiKey": "process.env.OPENAI_API_KEY"
}

// DeepSeek
{
  "baseURL": "https://api.deepseek.com/v1",
  "apiKey": "process.env.DEEPSEEK_API_KEY"
}

// Local Ollama
{
  "baseURL": "http://localhost:11434/v1",
  "apiKey": "ollama"
}

// Qwen (Alibaba Cloud)
{
  "baseURL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
  "apiKey": "process.env.DASHSCOPE_API_KEY"
}
```

---

## Project Architecture

```
openhanako/
├── core/           # Engine orchestration + Managers (Agent, Session, Model, Preferences, Skill)
├── lib/            # Core libraries
│   ├── memory/     # Custom memory system (recency decay)
│   ├── tools/      # Built-in tools (files, terminal, browser, screenshot, canvas)
│   ├── sandbox/    # PathGuard + OS-level isolation (Seatbelt/Bubblewrap)
│   └── bridge/     # Multi-platform adapters (Telegram, Feishu, QQ)
├── server/         # Fastify 5 HTTP + WebSocket server
├── hub/            # Scheduler, ChannelRouter, EventBus
├── desktop/        # Electron 38 main process + React 19 frontend
├── tests/          # Vitest test suite
└── skills2set/     # Built-in skill definitions
```

### Key Managers (via unified engine facade)

| Manager | Responsibility |
|---------|---------------|
| `AgentManager` | Create, load, delete agents |
| `SessionManager` | Conversation sessions per agent |
| `ModelManager` | Route requests to configured providers |
| `PreferencesManager` | User/global settings |
| `SkillManager` | Install, enable, disable, sandbox skills |

---

## Agent Configuration

Each agent is a self-contained folder you can back up:

```
~/.openhanako/agents/<agent-id>/
├── personality.md      # Personality template (free-form prose or structured)
├── memory/
│   ├── working.db      # Recent events (SQLite WAL)
│   └── compiled.md     # Long-term compiled memory
├── desk/               # Agent's file workspace
│   └── notes/          # Jian notes
└── skills/             # Agent-local installed skills
```

### Personality Template Example

```markdown
# Hanako

You are Hanako, a calm and thoughtful assistant who prefers directness over verbosity.
You remember past conversations and refer to them naturally.
You ask clarifying questions before starting large tasks.
When writing code, you always add brief inline comments.

## Tone
- Warm but professional
- Uses occasional dry humor
- Never uses hollow affirmations ("Great question!")

## Constraints
- Always confirm before deleting files
- Summarize long terminal output rather than dumping it raw
```

---

## Skills System

Skills extend agent capabilities. They live in `skills2set/` (built-in) or are installed per-agent.

### Install a Skill from GitHub

```javascript
// Via the Skills UI in the app, or programmatically:
const { skillManager } = engine;

await skillManager.installFromGitHub({
  repo: 'some-user/hanako-skill-weather',
  agentId: 'agent-abc123',
  safetyReview: true   // strict review enabled by default
});
```

### Skill Definition Format (SKILL.md → skills2set)

```markdown
---
name: web-scraper
version: 1.0.0
description: Scrape structured data from web pages
tools:
  - browser
  - javascript
permissions:
  - network
---

## Instructions for Agent

When asked to scrape a page:
1. Use the `browser` tool to navigate to the URL
2. Use `executeJavaScript` to extract structured data
3. Save results to the desk as JSON
```

### Writing a Custom Skill (JavaScript)

```javascript
// skills/my-skill/index.js
export default {
  name: 'my-skill',
  version: '1.0.0',
  description: 'Does something useful',

  // Tools this skill adds to the agent
  tools: [
    {
      name: 'fetch_weather',
      description: 'Fetch current weather for a city',
      parameters: {
        type: 'object',
        properties: {
          city: { type: 'string', description: 'City name' }
        },
        required: ['city']
      },
      async execute({ city }) {
        const res = await fetch(
          `https://wttr.in/${encodeURIComponent(city)}?format=j1`
        );
        const data = await res.json();
        return {
          temp_c: data.current_condition[0].temp_C,
          description: data.current_condition[0].weatherDesc[0].value
        };
      }
    }
  ]
};
```

---

## Memory System

OpenHanako uses a recency-decay memory model: recent events stay sharp, older ones fade.

```javascript
// Accessing memory programmatically (core/lib/memory)
import { MemoryManager } from './lib/memory/index.js';

const memory = new MemoryManager({ agentId: 'agent-abc123' });

// Store a memory event
await memory.store({
  type: 'conversation',
  content: 'User prefers dark mode and terse responses',
  importance: 0.8   // 0.0–1.0; higher = decays slower
});

// Retrieve relevant memories
const relevant = await memory.query({
  query: 'user preferences',
  limit: 10,
  minRelevance: 0.5
});

// Trigger manual compilation (normally runs automatically)
await memory.compile();
```

### Memory Tiers

| Tier | Storage | Decay |
|------|---------|-------|
| Working memory | `working.db` (SQLite) | Fast — recent N turns |
| Compiled memory | `compiled.md` | Slow — summarized by utility-large model |
| Desk notes (Jian) | Files on desk | Manual / no decay |

---

## Built-in Tools

Tools available to agents out of the box:

```javascript
// File operations
{ tool: 'read_file',   args: { path: '/Users/me/notes.txt' } }
{ tool: 'write_file',  args: { path: '/Users/me/out.txt', content: '...' } }

// Terminal
{ tool: 'run_command', args: { command: 'ls -la', cwd: '/Users/me' } }

// Browser & web
{ tool: 'browse',      args: { url: 'https://example.com' } }
{ tool: 'web_search',  args: { query: 'OpenHanako latest release' } }

// Screen
{ tool: 'screenshot',  args: {} }

// Canvas
{ tool: 'draw',        args: { instructions: '...' } }

// Code execution
{ tool: 'execute_js',  args: { code: 'return 2 + 2' } }
```

### Sandbox Access Tiers (PathGuard)

```
Tier 0 — Denied:     System paths (/System, /usr, registry hives)
Tier 1 — Read-only:  Home directory files outside agent desk
Tier 2 — Read-write: Agent desk folder only
Tier 3 — Full:       Explicitly granted paths (user confirms)
```

OS-level sandbox: **macOS Seatbelt** / **Linux Bubblewrap** wraps the skill process.

---

## Multi-Agent Setup

```javascript
// core/AgentManager usage example
import { createEngine } from './core/engine.js';

const engine = await createEngine();

// Create a second agent
const researchAgent = await engine.agentManager.create({
  name: 'Researcher',
  personalityTemplate: 'researcher.md',
  models: {
    chat: 'deepseek-chat',
    utility: 'gpt-4o-mini',
    utilityLarge: 'gpt-4o'
  }
});

// Delegate a task from one agent to another via channel
await engine.hub.channelRouter.delegate({
  fromAgent: 'agent-abc123',
  toAgent: researchAgent.id,
  task: 'Find the top 5 papers on mixture-of-experts published in 2025',
  returnTo: 'agent-abc123'   // result routed back automatically
});
```

---

## Scheduled Tasks (Cron & Heartbeat)

```javascript
// hub/scheduler usage
import { Scheduler } from './hub/scheduler.js';

const scheduler = new Scheduler({ agentId: 'agent-abc123' });

// Run a task every day at 9am
scheduler.cron('daily-briefing', '0 9 * * *', async () => {
  await agent.run('Summarize my desk notes from yesterday and post to #briefing channel');
});

// Heartbeat — check desk for new files every 5 minutes
scheduler.heartbeat('desk-watch', 300_000, async () => {
  const changed = await agent.desk.checkChanges();
  if (changed.length > 0) {
    await agent.run(`New files on desk: ${changed.join(', ')} — summarize and notify me`);
  }
});

scheduler.start();
```

---

## Multi-Platform Bridge

Connect one agent to Telegram, Feishu, and QQ simultaneously:

```javascript
// lib/bridge configuration
const bridgeConfig = {
  telegram: {
    enabled: true,
    token: process.env.TELEGRAM_BOT_TOKEN,
    allowedUsers: [process.env.TELEGRAM_ALLOWED_USER_ID]
  },
  feishu: {
    enabled: true,
    appId: process.env.FEISHU_APP_ID,
    appSecret: process.env.FEISHU_APP_SECRET
  },
  qq: {
    enabled: false
  }
};

await engine.agentManager.setBridges('agent-abc123', bridgeConfig);
```

---

## Server API (Fastify + WebSocket)

The embedded Fastify server runs locally and the Electron main process communicates via stdio bridge.

```javascript
// WebSocket — real-time chat stream
const ws = new WebSocket('ws://localhost:PORT/ws/agent-abc123');

ws.send(JSON.stringify({
  type: 'chat',
  content: 'Summarize my project folder'
}));

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  // msg.type: 'chunk' | 'tool_call' | 'tool_result' | 'done'
  console.log(msg);
};

// HTTP — one-shot task
const res = await fetch('http://localhost:PORT/api/agent/agent-abc123/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ task: 'List all .md files on my desk' })
});
const result = await res.json();
```

---

## Testing

```bash
# Run all tests
npm test

# Run a specific test file
npx vitest run tests/memory.test.js

# Watch mode
npx vitest
```

```javascript
// tests/memory.test.js example pattern
import { describe, it, expect, beforeEach } from 'vitest';
import { MemoryManager } from '../lib/memory/index.js';

describe('MemoryManager', () => {
  let memory;

  beforeEach(async () => {
    memory = new MemoryManager({ agentId: 'test-agent', inMemory: true });
    await memory.init();
  });

  it('stores and retrieves a memory', async () => {
    await memory.store({ type: 'fact', content: 'User likes dark mode', importance: 0.9 });
    const results = await memory.query({ query: 'dark mode', limit: 5 });
    expect(results[0].content).toContain('dark mode');
  });
});
```

---

## Troubleshooting

### App won't open on macOS
```bash
# Remove quarantine attribute if right-click → Open doesn't work
xattr -dr com.apple.quarantine /Applications/OpenHanako.app
```

### Agent not responding
- Check that the API key env var is set and the base URL is reachable
- Open DevTools (`Cmd+Option+I` / `Ctrl+Shift+I`) → Console for errors
- Verify the model name matches exactly what your provider supports

### Memory compilation not triggering
```javascript
// Force a manual compile
await engine.agentManager.getAgent('agent-abc123').memory.compile({ force: true });
```

### Skill installation blocked by safety review
```javascript
// Temporarily disable safety review for trusted local skills only
await skillManager.installLocal({
  path: './my-skill',
  agentId: 'agent-abc123',
  safetyReview: false   // ⚠️ only for local dev, never for untrusted sources
});
```

### Sandbox permission denied
- Check the PathGuard tier for the path being accessed
- Use the desktop UI: Agent Settings → Sandbox → Grant Path Access
- Or programmatically request elevation to Tier 3 (prompts user confirmation)

### Windows Defender false positive on built `.exe`
- The installer is unsigned; click **More info → Run anyway** in SmartScreen
- Add an exclusion in Windows Security if needed during development

---

## Key Links

- **Releases:** https://github.com/liliMozi/openhanako/releases
- **Issues:** https://github.com/liliMozi/openhanako/issues
- **Homepage:** https://openhanako.com
- **Contributing:** https://github.com/liliMozi/openhanako/blob/main/CONTRIBUTING.md
- **Security Policy:** https://github.com/liliMozi/openhanako/blob/main/SECURITY.md
- **License:** Apache 2.0
