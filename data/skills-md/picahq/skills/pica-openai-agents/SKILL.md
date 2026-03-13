---
name: pica-openai-agents
description: Integrate PICA into an application using the OpenAI Agents SDK. Use when adding PICA tools to an OpenAI agent via @openai/agents, setting up PICA MCP with the OpenAI Agents SDK, or when the user mentions PICA with OpenAI Agents.
---

# PICA MCP Integration with the OpenAI Agents SDK

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

Always store the PICA secret in an environment variable, never hardcode it:

```
PICA_SECRET=sk_test_...
OPENAI_API_KEY=sk-...
```

Add them to `.env.local` (or equivalent) and document in `.env.example`.

## Using PICA with the OpenAI Agents SDK

The OpenAI Agents SDK (`@openai/agents`) has **first-class MCP support** via `MCPServerStdio`. No additional MCP client package is needed — the SDK handles tool discovery, conversion, and execution automatically.

### Required packages

```bash
pnpm add @openai/agents zod
```

- **`@openai/agents`**: Main SDK (includes `MCPServerStdio`, `Agent`, `run`)
- **`zod`**: Required by the SDK (v4+)

### Before implementing: look up the latest docs

The OpenAI Agents SDK API may change between versions. **Always check the latest docs first:**

- Docs: https://openai.github.io/openai-agents-js/
- MCP guide: https://openai.github.io/openai-agents-js/guides/mcp/
- GitHub: https://github.com/openai/openai-agents-js

### Integration pattern

1. **Create an MCP server** using `MCPServerStdio` with `command: "npx"`, `args: ["@picahq/mcp"]`
2. **Connect** the server via `await mcpServer.connect()`
3. **Create an Agent** with `mcpServers: [mcpServer]` — tools are discovered automatically
4. **Run** the agent with `run(agent, input, { stream: true })` — the SDK handles the full agent loop (tool calls, execution, multi-step)
5. **Stream events** by iterating the result — handle `raw_model_stream_event` for text deltas and `run_item_stream_event` for tool calls
6. **Close** the MCP server when done via `await mcpServer.close()`

When passing environment variables, spread `process.env` so the subprocess inherits PATH and other system vars:

```typescript
env: {
  ...(process.env as Record<string, string>),
  PICA_SECRET: process.env.PICA_SECRET!,
}
```

### Minimal example

```typescript
import { Agent, run, MCPServerStdio } from "@openai/agents";

const mcpServer = new MCPServerStdio({
  name: "PICA MCP Server",
  command: "npx",
  args: ["@picahq/mcp"],
  env: {
    ...(process.env as Record<string, string>),
    PICA_SECRET: process.env.PICA_SECRET!,
  },
});

await mcpServer.connect();

try {
  const agent = new Agent({
    name: "PICA Assistant",
    model: "gpt-4o-mini",
    instructions: "You are a helpful assistant.",
    mcpServers: [mcpServer],
  });

  // Non-streaming
  const result = await run(agent, "List my connected integrations");
  console.log(result.finalOutput);

  // Streaming
  const streamResult = await run(agent, "List my connected integrations", {
    stream: true,
  });
  for await (const event of streamResult) {
    if (event.type === "raw_model_stream_event") {
      const data = event.data as Record<string, unknown>;
      if (data.type === "response.output_text.delta") {
        process.stdout.write(data.delta as string);
      }
    }
  }
  await streamResult.completed;
} finally {
  await mcpServer.close();
}
```

### Streaming SSE events for a chat UI

When building a Next.js API route, stream responses as SSE events using a `ReadableStream`. Emit events in this format for compatibility with the `PythonChat` frontend component:

- `{ type: "text", content: "..." }` — streamed text chunks
- `{ type: "tool_start", name: "tool_name", input: "..." }` — tool execution starting
- `{ type: "tool_end", name: "tool_name", output: "..." }` — tool execution result
- `{ type: "error", content: "..." }` — error messages
- `data: [DONE]` — stream finished

### Handling streaming events

The SDK emits three event types when streaming:

| Event Type | Purpose | Key Fields |
|:---|:---|:---|
| `raw_model_stream_event` | Raw model token deltas | `data.type`, `data.delta` |
| `run_item_stream_event` | Tool calls, outputs, messages | `item.rawItem.type`, `item.rawItem.*` |
| `agent_updated_stream_event` | Agent switched (handoff) | `agent.name` |

For text streaming, match `data.type === "response.output_text.delta"` and read `data.delta`.

For tool events, check `item.rawItem.type`:
- `"function_call"` — tool was invoked (has `call_id`, `name`, `arguments`)
- `"function_call_output"` — tool returned (has `call_id`, `output`, but **no `name`** — track names via a `Map<call_id, name>`)

**Important:** `run_item_stream_event` may fire multiple times for the same tool call (created, in-progress, completed). Use a `Set<call_id>` to deduplicate `tool_start` events.

**Fallback:** After the stream loop completes, check `result.finalOutput` — if no text deltas were streamed (e.g., the model returned a single non-streamed response), send `finalOutput` as a text event.

### Multi-turn input format

Pass conversation history as an array of message objects:

```typescript
const input = messages.map((m: { role: string; content: string }) => ({
  role: m.role as "user" | "assistant",
  content: m.content,
}));

const result = await run(agent, input, { stream: true });
```

## Checklist

When setting up PICA MCP with the OpenAI Agents SDK:

- [ ] `@openai/agents` is installed
- [ ] `zod` (v4+) is installed
- [ ] `OPENAI_API_KEY` is set in `.env.local`
- [ ] `PICA_SECRET` is set in `.env.local`
- [ ] `.env.example` documents both `OPENAI_API_KEY` and `PICA_SECRET`
- [ ] `MCPServerStdio` uses `command: "npx"`, `args: ["@picahq/mcp"]`
- [ ] Full `process.env` is spread into the MCP server's `env` option
- [ ] `mcpServer.connect()` is called before creating the agent
- [ ] Agent has `mcpServers: [mcpServer]` — tools are auto-discovered
- [ ] `run()` is called with `{ stream: true }` for streaming responses
- [ ] `result.completed` is awaited after iterating the stream
- [ ] Fallback to `result.finalOutput` if no text deltas were streamed
- [ ] Tool call names are tracked by `call_id` (output events lack `name`)
- [ ] Tool start events are deduplicated with a `Set<call_id>`
- [ ] `mcpServer.close()` is called in a `finally` block
