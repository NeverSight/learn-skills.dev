---
name: pica-mastra
description: Integrate PICA into an application using Mastra. Use when adding PICA tools to a Mastra agent via @mastra/core and @mastra/mcp, setting up PICA MCP with Mastra, or when the user mentions PICA with Mastra.
---

# PICA MCP Integration with Mastra

PICA provides a unified API platform that connects AI agents to third-party services (CRMs, email, calendars, databases, etc.) through MCP tool calling.

## PICA MCP Server

PICA exposes its capabilities through an MCP server distributed as `@picahq/mcp`. It uses **stdio transport** — it runs as a local subprocess via `npx`.

### MCP Configuration

```json
{
  "mcpServers": {
    "pica": {
      "command": "npx",
      "args": ["@picahq/mcp"],
      "env": {
        "PICA_SECRET": "your-pica-secret-key"
      }
    }
  }
}
```

- **Package**: `@picahq/mcp` (run via `npx`, no install needed)
- **Auth**: `PICA_SECRET` environment variable (obtain from the PICA dashboard https://app.picaos.com/settings/api-keys)
- **Transport**: stdio (standard input/output)

### Environment Variable

Always store secrets in environment variables, never hardcode them:

```
PICA_SECRET=sk_test_...
OPENAI_API_KEY=sk-...
```

Add them to `.env.local` (or equivalent) and document in `.env.example`. Mastra auto-reads provider API keys from environment (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.).

## Using PICA with Mastra

Mastra has **first-class MCP support** via the `@mastra/mcp` package. The `MCPClient` auto-detects transport type from your config — provide `command`/`args` for stdio, or `url` for HTTP/SSE.

### Required packages

```bash
pnpm add @mastra/core @mastra/mcp
```

### Before implementing: look up the latest docs

The Mastra API may change between versions. **Always check the latest docs first:**

- Docs: https://mastra.ai/docs
- MCP guide: https://mastra.ai/docs/mcp/overview
- MCPClient reference: https://mastra.ai/reference/tools/mcp-client
- GitHub: https://github.com/mastra-ai/mastra

### Integration pattern

1. **Create an MCPClient** with `command: "npx"`, `args: ["@picahq/mcp"]` — transport is auto-detected as stdio
2. **List tools** via `await mcp.listTools()` — returns tools in Mastra's format
3. **Create an Agent** with the tools and a model string (`"provider/model-name"`)
4. **Stream** via `agent.stream(messages, { maxSteps: 5 })` — the agent loop handles tool calls automatically
5. **Iterate `fullStream`** for typed chunks (`text-delta`, `tool-call`, `tool-result`) — all data lives on `chunk.payload`
6. **Disconnect** the MCP client when done via `await mcp.disconnect()`

When passing environment variables, spread `process.env` so the subprocess inherits PATH and other system vars:

```typescript
env: {
  ...(process.env as Record<string, string>),
  PICA_SECRET: process.env.PICA_SECRET!,
}
```

### Minimal example

```typescript
import { Agent } from "@mastra/core/agent";
import { MCPClient } from "@mastra/mcp";

const mcp = new MCPClient({
  id: "pica-mcp",
  servers: {
    pica: {
      command: "npx",
      args: ["@picahq/mcp"],
      env: {
        ...(process.env as Record<string, string>),
        PICA_SECRET: process.env.PICA_SECRET!,
      },
    },
  },
});

const tools = await mcp.listTools();

const agent = new Agent({
  id: "pica-assistant",
  name: "PICA Assistant",
  model: "openai/gpt-4o-mini",
  instructions: "You are a helpful assistant.",
  tools,
});

// Non-streaming
const result = await agent.generate("List my connected integrations");
console.log(result.text);

// Streaming
const stream = await agent.stream("List my connected integrations", {
  maxSteps: 5,
});

for await (const chunk of stream.fullStream) {
  if (chunk.type === "text-delta") {
    process.stdout.write(chunk.payload.text);
  } else if (chunk.type === "tool-call") {
    console.log("Tool called:", chunk.payload.toolName, chunk.payload.args);
  } else if (chunk.type === "tool-result") {
    console.log("Tool result:", chunk.payload.toolName, chunk.payload.result);
  }
}

await mcp.disconnect();
```

### Streaming SSE events for a chat UI

When building a Next.js API route, stream responses as SSE events using a `ReadableStream`. Emit events in this format for compatibility with the `PythonChat` frontend component:

- `{ type: "text", content: "..." }` — streamed text chunks
- `{ type: "tool_start", name: "tool_name", input: "..." }` — tool execution starting
- `{ type: "tool_end", name: "tool_name", output: "..." }` — tool execution result
- `{ type: "error", content: "..." }` — error messages
- `data: [DONE]` — stream finished

### Key stream chunk types

Mastra's `fullStream` yields typed chunks where all data lives on `chunk.payload`:

| Chunk Type | Payload Fields | Description |
|:---|:---|:---|
| `text-delta` | `payload.text` | Streamed text content |
| `tool-call` | `payload.toolName`, `payload.toolCallId`, `payload.args` | Tool invocation |
| `tool-result` | `payload.toolName`, `payload.toolCallId`, `payload.result`, `payload.isError` | Tool output |
| `step-finish` | `payload.stepResult`, `payload.output` | Agent step completed |
| `finish` | `payload.stepResult`, `payload.output`, `payload.messages` | Stream finished |
| `error` | `payload.error` | Error occurred |

**Important:** Chunk data is always on `chunk.payload`, not directly on the chunk. For example, use `chunk.payload.text` (not `chunk.textDelta`).

### Model string format

Mastra uses `"provider/model-name"` strings — no separate provider packages needed:

```typescript
model: "openai/gpt-4o-mini"
model: "anthropic/claude-4-5-sonnet"
model: "google/gemini-2.5-flash"
```

### Static vs dynamic tools

**Static** (at agent creation): Merge MCP tools into the agent's `tools`:

```typescript
const agent = new Agent({
  tools: await mcp.listTools(),
});
```

**Dynamic** (per request): Inject via `toolsets` at call time:

```typescript
const result = await agent.generate("...", {
  toolsets: await mcp.listToolsets(),
});
```

Use dynamic toolsets when the MCP client is created per-request (e.g., with user-specific credentials).

## Checklist

When setting up PICA MCP with Mastra:

- [ ] `@mastra/core` is installed
- [ ] `@mastra/mcp` is installed
- [ ] `PICA_SECRET` is set in `.env.local`
- [ ] Provider API key (e.g., `OPENAI_API_KEY`) is set in `.env.local`
- [ ] `.env.example` documents all required env vars
- [ ] `MCPClient` uses `command: "npx"`, `args: ["@picahq/mcp"]` (stdio auto-detected)
- [ ] Full `process.env` is spread into the MCP server's `env` option
- [ ] `MCPClient` has a unique `id` to prevent memory leaks with multiple instances
- [ ] Tools from `mcp.listTools()` are passed to the Agent's `tools`
- [ ] `agent.stream()` is called with `maxSteps` to limit tool call iterations
- [ ] Stream chunks are read from `chunk.payload` (not directly from chunk)
- [ ] `mcp.disconnect()` is called in a `finally` block to clean up connections
