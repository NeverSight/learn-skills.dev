---
name: build-copilot-sdk-app
description: Use skill if you are building TypeScript applications with the GitHub Copilot SDK (@github/copilot-sdk), including sessions, tools, streaming, hooks, custom agents, or BYOK.
---

# Build Copilot SDK App

Build applications powered by GitHub Copilot using the `@github/copilot-sdk` TypeScript/Node.js package (v0.1.32+, protocol v3). The SDK communicates with the Copilot CLI over JSON-RPC (stdio or TCP) and exposes a session-based API for sending prompts, receiving streamed responses, registering custom tools, handling permissions, and managing agent workflows.

## Decision tree

```
What do you need?
│
├── New app from scratch
│   ├── Install & basic example ──────────► Quick start (below) — npm init, ESM setup, first prompt
│   ├── Client options & transport ───────► references/client-and-transport.md — stdio vs TCP, CopilotClient config
│   └── Authentication ──────────────────► references/auth-and-byok.md — OAuth, tokens, BYOK with 5 providers
│
├── Sessions
│   ├── Create / resume / disconnect ────► references/sessions.md — lifecycle, create-or-resume pattern
│   ├── Infinite sessions & compaction ──► references/sessions.md — long conversations, context window mgmt
│   └── Persistence & resumption ────────► references/sessions.md — disk persistence, resumeSession semantics
│
├── Messages & streaming
│   ├── send / sendAndWait ──────────────► Quick start (below) — blocking vs fire-and-forget
│   ├── Streaming deltas ────────────────► references/events-and-streaming.md — incremental content delivery
│   └── All 47 event types ─────────────► references/events-and-streaming.md — full event catalog
│
├── Custom tools
│   ├── defineTool with Zod ─────────────► references/tools-and-schemas.md — Zod schema, handler, auto-JSON-Schema
│   ├── JSON Schema tools ──────────────► references/tools-and-schemas.md — raw schema without Zod
│   └── Override built-in tools ────────► references/tools-and-schemas.md — replace default Copilot tools
│
├── Permissions & user input
│   ├── Permission handler ─────────────► references/permissions-and-user-input.md — approveAll or custom logic
│   ├── askUser / onUserInputRequest ───► references/permissions-and-user-input.md — programmatic user prompts
│   └── Elicitation (MCP forms) ────────► references/permissions-and-user-input.md — structured input via MCP
│
├── Hooks (lifecycle interceptors)
│   ├── Pre/post tool use ──────────────► references/hooks.md — intercept tool calls, modify args/results
│   ├── Prompt modification ────────────► references/hooks.md — rewrite prompts before send
│   └── Session lifecycle & errors ─────► references/hooks.md — onError, onSessionStart, void return OK
│
├── Agents, MCP & skills
│   ├── Custom agents ──────────────────► references/agents-mcp-skills.md — agent registration & routing
│   ├── MCP server config ─────────────► references/agents-mcp-skills.md — connect external MCP servers
│   ├── Skills system ─────────────────► references/agents-mcp-skills.md — skill discovery & invocation
│   └── CLI extensions (.mjs) ─────────► references/agents-mcp-skills.md — extend Copilot CLI via scripts
│
├── Advanced patterns
│   ├── Plan / autopilot / interactive ─► references/advanced-patterns.md — mode switching workflow
│   ├── Fleet mode ─────────────────────► references/advanced-patterns.md — parallel session orchestration
│   ├── Multi-client architecture ──────► references/advanced-patterns.md — multiple CopilotClient instances
│   ├── Ralph loop (autonomous dev) ───► references/advanced-patterns.md — autonomous code generation loop
│   ├── Steering & queueing ───────────► references/advanced-patterns.md — prompt queueing, backpressure
│   └── System message modes ──────────► references/advanced-patterns.md — system prompt configuration
│
├── Auth & BYOK
│   ├── GitHub OAuth / tokens ──────────► references/auth-and-byok.md — token acquisition flow
│   └── Bring Your Own Key ────────────► references/auth-and-byok.md — OpenAI/Anthropic/Azure/Gemini/Ollama
│
└── Type reference
    └── All interfaces & RPC methods ──► references/types-reference.md — TypeScript interfaces, RPC API
```

## Quick start

### Prerequisites

Verify your environment:
```bash
node --version   # must be >= 20
copilot --version # Copilot CLI must be installed
```

### Project setup

```bash
npm init -y
npm pkg set type=module   # SDK is ESM-only
npm install @github/copilot-sdk tsx zod
```

> **ESM required.** The SDK only ships ESM exports. Your `package.json` must have `"type": "module"`.

### Common imports

```typescript
// Core
import { CopilotClient, approveAll } from "@github/copilot-sdk";

// Tools
import { defineTool } from "@github/copilot-sdk";
import { z } from "zod";

// Advanced — hooks, resume, types
import type { SessionConfig, ToolInvocation } from "@github/copilot-sdk";
```

### Minimal example

```typescript
import { CopilotClient, approveAll } from "@github/copilot-sdk";

const client = new CopilotClient();

const session = await client.createSession({
  model: "gpt-4.1",
  onPermissionRequest: approveAll,
});

const response = await session.sendAndWait({ prompt: "What is 2 + 2?" });
console.log(response?.data.content);

await session.disconnect();
await client.stop();
```

### With streaming

```typescript
const session = await client.createSession({
  model: "gpt-4.1",
  streaming: true,
  onPermissionRequest: approveAll,
});

session.on("assistant.message_delta", (event) => {
  process.stdout.write(event.data.deltaContent);
});

session.on("session.idle", async () => {
  console.log("\n--- done ---");
  await session.disconnect();
  await client.stop();
});

await session.send({ prompt: "Explain TypeScript generics" });
```

### With a custom tool

```typescript
import { CopilotClient, defineTool, approveAll } from "@github/copilot-sdk";
import { z } from "zod";

const getWeather = defineTool("get_weather", {
  description: "Get current weather for a city",
  parameters: z.object({
    city: z.string().describe("City name"),
  }),
  handler: async ({ city }) => ({
    city,
    temperature: "62°F",
    condition: "cloudy",
  }),
});

const client = new CopilotClient();
const session = await client.createSession({
  model: "gpt-4.1",
  tools: [getWeather],
  onPermissionRequest: approveAll,
});

const response = await session.sendAndWait({
  prompt: "What's the weather in San Francisco?",
});
console.log(response?.data.content);

await session.disconnect();
await client.stop();
```

## Key patterns

### Send-and-wait vs fire-and-forget

```typescript
// Blocking — waits for session.idle, returns last assistant.message
const response = await session.sendAndWait(
  { prompt: "Hello" },
  30_000, // optional timeout in ms
);

// Non-blocking — returns immediately, events arrive via session.on()
await session.send({ prompt: "Start a long task..." });
```

### Event subscription (typed + wildcard)

```typescript
// Typed — only fires for the specific event type
const unsub = session.on("tool.execution_complete", (event) => {
  console.log(`${event.data.toolName}: ${event.data.success}`);
});

// Wildcard — fires for every event
session.on((event) => {
  if (event.type === "session.error") {
    console.error(event.data.message);
  }
});

unsub(); // unsubscribe
```

### Session persistence

```typescript
// Create with a stable ID
const session = await client.createSession({
  sessionId: "user-123-conversation",
  model: "gpt-4.1",
  onPermissionRequest: approveAll,
});
await session.sendAndWait({ prompt: "Let's discuss TypeScript" });
await session.disconnect(); // preserves state on disk

// Resume later (same or different client)
const resumed = await client.resumeSession("user-123-conversation", {
  onPermissionRequest: approveAll,
});
```

### Create-or-resume pattern

`createSession` always starts fresh — only `resumeSession` restores conversation context. In applications that may revisit a session:

```typescript
let session;
try {
  session = await client.resumeSession(sessionId, {
    onPermissionRequest: approveAll,
  });
} catch {
  session = await client.createSession({
    sessionId,
    model: "gpt-4.1",
    onPermissionRequest: approveAll,
  });
}
```

### Handling askUser programmatically

```typescript
const session = await client.createSession({
  onPermissionRequest: approveAll,
  onUserInputRequest: async (request) => {
    if (request.choices?.length) {
      return { answer: request.choices[0], wasFreeform: false };
    }
    return { answer: "Yes, proceed", wasFreeform: true };
  },
});
```

### Plan / autopilot mode

```typescript
await session.rpc.mode.set({ mode: "plan" });

session.on("exit_plan_mode.requested", (event) => {
  console.log("Plan ready:", event.data.summary);
  session.rpc.mode.set({ mode: "autopilot" });
});
```

### Abort in-flight work

```typescript
await session.send({ prompt: "Run sleep 100" });
await session.abort(); // cancels current work; session remains usable
```

## Common pitfalls

| Pitfall | Fix |
|---------|-----|
| `onPermissionRequest` missing | Required on every `createSession`/`resumeSession`. Use `approveAll` for unattended operation. |
| `sendAndWait` timeout | Default is 60s. Pass explicit timeout: `sendAndWait(opts, 300_000)`. Timeout does NOT abort in-flight work. |
| Streaming events not arriving | Set `streaming: true` in SessionConfig. |
| `cliUrl` + `useStdio` | Mutually exclusive. `cliUrl` connects to external server; `useStdio` spawns child process. |
| `console.log` in extensions | stdout is reserved for JSON-RPC. Use `session.log()` instead. |
| Tool name collision in extensions | Tool names must be globally unique across all extensions. |
| BYOK without `model` | `model` is required when using `provider` config. Session creation succeeds silently, but `sendAndWait` will fail. |
| Race condition on event registration | Register `session.on()` before calling `session.send()`. |

## Steering notes for AI agents

> These notes are distilled from real-world testing. They address the exact points where an agent following these instructions literally will get stuck.

### Project initialization
- **Always** run `npm init -y` then `npm pkg set type=module` before installing. The SDK is ESM-only and will throw `ERR_PACKAGE_PATH_NOT_EXPORTED` without this.
- **Always** install `zod` alongside the SDK if you plan to use `defineTool`. It's not bundled.
- Verify `node --version` is >= 20 and `copilot --version` responds before writing any code.

### Session lifecycle
- `createSession` **always starts fresh** — even with the same `sessionId`. It does NOT restore previous messages.
- To resume a conversation, use `resumeSession(sessionId)`. If the session doesn't exist, it throws — catch and fall back to `createSession`.
- **Always** call `session.disconnect()` then `client.stop()` when done. Without this, streaming processes hang indefinitely because the RPC connection keeps the event loop alive.

### Streaming
- Register **all** event handlers (`session.on(...)`) **before** calling `session.send()`. Handlers registered after send may miss early events.
- In the `session.idle` handler, always include cleanup (`disconnect` + `stop`) unless you're building a multi-turn REPL.
- When the model calls multiple tools in parallel, `tool.execution_start` and `tool.execution_complete` events interleave. Use `toolCallId` to correlate them.

### Tools
- `defineTool` requires a Zod schema for parameters. The SDK auto-detects Zod and calls `toJSONSchema()`.
- Tool handler errors are caught and surfaced to the model as error results — they don't crash your process.
- Tool names must be globally unique across all extensions.

### Timeouts and errors
- `sendAndWait` timeout does **not** abort in-flight work. It only stops waiting. Call `session.abort()` explicitly if you need to cancel.
- BYOK without `model` in provider config creates a session successfully but fails silently at send time. Always pair `provider` with `model`.
