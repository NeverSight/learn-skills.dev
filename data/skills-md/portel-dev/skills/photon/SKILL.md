---
name: photon
description: "Build Photon MCPs — single-file TypeScript MCP servers. Use for creating photons with @format annotations (table, chart:bar), stateful photons using this.memory for persistent storage, photons with @readOnly/@destructive annotations, custom UI using @ui tags/HTML templates, photons wrapping APIs (Stripe, payments), task scheduler photons with cron, mermaid diagrams for photon architecture, editing .photon.ts files. DO NOT trigger for general TypeScript or non-photon MCP."
---

# Photon Development Guide

Photons are single-file TypeScript MCP servers. No compilation — runs directly with `tsx`.

## Quick Start

```bash
npm install -g @portel/photon    # Install runtime
photon maker new my-weather      # Create photon
photon beam                      # Launch Beam UI
photon mcp my-weather            # Run as MCP server
photon cli my-weather current --city London  # CLI
```

Files go in `~/.photon/`. Connect to Claude Desktop:

```json
{ "mcpServers": { "my-weather": { "command": "photon", "args": ["mcp", "my-weather"] } } }
```

## Minimal Photon

```typescript
import { PhotonMCP } from '@portel/photon-core';

/**
 * Weather API
 * @version 1.0.0
 * @dependencies axios@^1.0.0
 * @icon 🌤️
 */
export default class Weather extends PhotonMCP {
  constructor(private apiKey: string) { super(); }

  /**
   * Get current weather for a city
   * @param city City name {@example London}
   * @readOnly
   * @title Current Weather
   * @format markdown
   */
  async current({ city }: { city: string }): Promise<string> {
    const res = await fetch(`https://api.weather.com/v1/current?q=${city}&key=${this.apiKey}`);
    if (!res.ok) throw new Error(`API error: ${res.statusText}`);
    const data = await res.json();
    return `**${data.name}** — ${data.temp}°C, ${data.description}`;
  }
}
```

## Core Principles

1. **Return values directly** — no `{ success: true, data }` wrappers. If it returns, it succeeded.
2. **Throw on errors** — let the runtime handle them. Don't catch and wrap.
3. **Single-word method names** — they read as CLI commands: `weather current`, not `weather getCurrentWeather`.
4. **Constructor = config** — constructor params auto-map to env vars: `PHOTON_WEATHER_APIKEY`.

## Class Structure

```typescript
/**
 * Brief description (becomes photon description)
 *
 * @version 1.0.0
 * @runtime ^1.5.0
 * @dependencies package1, package2@^2.0.0
 * @icon 🔧
 * @tags api, utility
 */
export default class MyTool extends PhotonMCP {
  constructor(private apiKey: string) { super(); }

  /**
   * Method description (becomes tool description)
   * @param query Search query {@example "typescript"} {@min 1}
   * @readOnly
   * @title Search Items
   * @format table
   */
  async search({ query }: { query: string }) { ... }
}
```

## MCP Annotations

JSDoc tags map to MCP protocol annotations (spec 2025-11-25):

```typescript
/**
 * @readOnly        — no side effects, safe to auto-approve
 * @destructive     — requires confirmation
 * @idempotent      — safe to retry
 * @openWorld       — calls external systems
 * @closedWorld     — local data only
 * @title My Tool   — human-readable display name
 * @audience user   — who sees results: user, assistant, or both
 * @priority 0.9    — content importance (0.0–1.0)
 */
```

## Structured Output

Auto-generated from TypeScript return types — no tags needed:

```typescript
async create(params: { title: string }): Promise<{ id: string; done: boolean }> { ... }
```

For field descriptions, use an interface with JSDoc:

```typescript
interface Task {
  /** Unique identifier */
  id: string;
  /** Whether complete */
  done: boolean;
}
async create(params: { title: string }): Promise<Task> { ... }
```

## Output Formats

Use `@format` to control rendering. Common values:

| Format | Use For |
|--------|---------|
| `table` | Array of objects |
| `list` | Styled list with `{@title name, @subtitle email}` |
| `markdown` | Rich text, diagrams |
| `chart:bar` / `chart:line` / `chart:pie` | Data visualization |
| `json` | Raw JSON |
| `dashboard` | Composite panels (auto-detected) |

For complete format reference with layout hints, containers, and auto-detection rules, see [references/output-formats.md](references/output-formats.md).

## Lifecycle & Workflows

```typescript
// Lifecycle hooks
async onInitialize() { /* called once on load */ }
async onShutdown() { /* called before unload */ }

// Generator workflows (multi-step with user interaction)
async *deploy({ env }: { env: string }) {
  yield { emit: 'status', message: 'Deploying...' };
  const ok = yield { ask: 'confirm', message: `Deploy to ${env}?` };
  if (!ok) return 'Cancelled';
  return 'Done';
}

// Waiting for external async events (WebSocket, library callbacks, etc.)
async *connect() {
  yield { emit: 'status', message: 'Connecting...' };
  let resolve: (v: any) => void;
  const promise = new Promise(r => { resolve = r; });
  this.socket.on('ready', (data) => resolve(data));
  await this.initSocket();
  const event = await promise;  // blocks until external event fires
  yield { emit: 'toast', message: 'Connected!', type: 'success' };
  return event;
}
```

## Scoped Memory

Zero-config persistent storage via `this.memory`:

```typescript
await this.memory.set('key', value);              // photon scope (default)
const val = await this.memory.get<T>('key');
await this.memory.set('shared', data, 'global');   // cross-photon
```

Three scopes: `photon` (private), `session` (per-user), `global` (shared). Full API: `get`, `set`, `delete`, `has`, `keys`, `clear`, `getAll`, `update`.

## Runtime Scheduling

Dynamic task scheduling via `this.schedule` — complements static `@scheduled`/`@cron` tags:

```typescript
// Create a scheduled task at runtime
await this.schedule.create({
  name: 'nightly-cleanup',
  schedule: '0 0 * * *',       // 5-field cron or @daily, @hourly, @weekly, @monthly
  method: 'purge',
  params: { olderThan: 30 },
});

// Manage tasks
await this.schedule.pause(id);
await this.schedule.resume(id);
await this.schedule.cancel(id);
const tasks = await this.schedule.list('active');
```

Full API: `create`, `get`, `getByName`, `list`, `update`, `pause`, `resume`, `cancel`, `cancelByName`, `cancelAll`, `has`. Tasks persist to disk; the daemon executes them.

Use `@scheduled`/`@cron` for fixed schedules known at build time. Use `this.schedule` for dynamic schedules created at runtime (user-configured intervals, conditional jobs, etc.).

## Custom UIs

Link HTML files as interactive result renderers:

```typescript
/** @ui dashboard ./ui/dashboard.html */
export default class MyApp extends PhotonMCP {
  /** @ui dashboard */
  async getData({ range }: { range: string }) { return { metrics: 42 }; }
}
```

The UI gets a photon-named global proxy: `window.myApp.getData(...)`, `window.myApp.onResult(...)`.

For full MCP Apps guide, see [references/mcp-apps.md](references/mcp-apps.md).

## References

| Topic | When to Read |
|-------|-------------|
| [Docblock Tags](references/docblock-tags.md) | Need the complete tag reference (class, method, inline, daemon, MCP) |
| [Output Formats](references/output-formats.md) | Need layout hints, chart mapping, containers, or auto-detection rules |
| [Dependency Injection](references/dependency-injection.md) | Using `@mcp`, `@photon`, or `this.call()` for cross-photon communication |
| [Daemon Features](references/daemon-features.md) | Setting up webhooks, cron jobs, or distributed locks |
| [MCP Apps](references/mcp-apps.md) | Building custom HTML UIs with the photon bridge |
| [Visualization](references/visualization.md) | Generating Mermaid diagrams from photons |
| [Mermaid Syntax](references/mermaid-syntax.md) | Flowchart shapes, arrows, subgraphs |
| [Photon Patterns](references/photon-patterns.md) | Common emit/ask/yield patterns with Mermaid equivalents |
| [Examples](references/examples.md) | Complete Photon-to-Mermaid conversion examples |
