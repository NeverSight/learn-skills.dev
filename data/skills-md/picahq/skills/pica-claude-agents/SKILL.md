---
name: pica-claude-agents
description: Integrate PICA into an application using the Anthropic SDK (Claude Agents). Use when adding PICA tools to a Claude agent via @anthropic-ai/sdk, setting up PICA MCP with the Anthropic TypeScript SDK, or when the user mentions PICA with Claude Agents SDK.
---

# PICA MCP Integration with the Anthropic SDK (Claude Agents)

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
```

Add it to `.env.local` (or equivalent) and document it in `.env.example`.

## Using PICA with the Anthropic SDK

The Anthropic TypeScript SDK (`@anthropic-ai/sdk`) connects to MCP servers via the `@modelcontextprotocol/sdk` package.

### Required packages

```bash
pnpm add @anthropic-ai/sdk @modelcontextprotocol/sdk
```

### Before implementing: look up the latest docs

The Anthropic SDK and MCP SDK APIs may change between versions. **Always search the official docs first** to get the current API before writing any code:

- Anthropic SDK: https://github.com/anthropics/anthropic-sdk-typescript
- MCP SDK: https://github.com/modelcontextprotocol/typescript-sdk

### Integration pattern

1. **Create an MCP client** using `Client` from `@modelcontextprotocol/sdk` with `StdioClientTransport` pointed at `npx @picahq/mcp`
2. **List tools** from the MCP client via `client.listTools()`
3. **Convert tools** to Anthropic's `Tool[]` format (map `name`, `description`, `inputSchema`)
4. **Stream responses** using `anthropic.messages.create({ stream: true })` with the converted tools
5. **Handle the agent loop** — when the model returns `tool_use` blocks, execute them via `mcpClient.callTool()`, append results, and loop back
6. **Close the MCP client** when the conversation turn is finished

When passing environment variables to the stdio transport, spread `process.env` so the subprocess inherits the full environment (PATH, etc.):

```typescript
env: {
  ...process.env as Record<string, string>,
  PICA_SECRET: process.env.PICA_SECRET!,
}
```

### Minimal example

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const anthropic = new Anthropic();

// Connect to PICA MCP server
const transport = new StdioClientTransport({
  command: "npx",
  args: ["@picahq/mcp"],
  env: {
    ...process.env as Record<string, string>,
    PICA_SECRET: process.env.PICA_SECRET!,
  },
});

const mcpClient = new Client({ name: "my-agent", version: "1.0.0" });
await mcpClient.connect(transport);

// Get tools in Anthropic format
const { tools: mcpToolsList } = await mcpClient.listTools();
const tools: Anthropic.Tool[] = mcpToolsList.map((t) => ({
  name: t.name,
  description: t.description || "",
  input_schema: t.inputSchema as Anthropic.Tool.InputSchema,
}));

// Agent loop with streaming
let messages: Anthropic.MessageParam[] = [
  { role: "user", content: "List my connected integrations" },
];

let stepsRemaining = 5;
while (stepsRemaining-- > 0) {
  const response = await anthropic.messages.create({
    model: "claude-haiku-4-5-20251001",
    max_tokens: 4096,
    messages,
    tools,
    stream: true,
  });

  const assistantContent: Anthropic.ContentBlock[] = [];
  const toolUseBlocks: { id: string; name: string; input: Record<string, unknown> }[] = [];
  let currentText = "";
  let currentToolId = "";
  let currentToolName = "";
  let currentToolInputJson = "";
  let currentBlockType: "text" | "tool_use" | null = null;

  for await (const event of response) {
    switch (event.type) {
      case "content_block_start":
        if (event.content_block.type === "text") {
          currentBlockType = "text";
          currentText = "";
        } else if (event.content_block.type === "tool_use") {
          currentBlockType = "tool_use";
          currentToolId = event.content_block.id;
          currentToolName = event.content_block.name;
          currentToolInputJson = "";
        }
        break;
      case "content_block_delta":
        if (event.delta.type === "text_delta") {
          currentText += event.delta.text;
          // Stream text chunk to client here
        } else if (event.delta.type === "input_json_delta") {
          currentToolInputJson += event.delta.partial_json;
        }
        break;
      case "content_block_stop":
        if (currentBlockType === "text") {
          assistantContent.push({ type: "text", text: currentText } as Anthropic.TextBlock);
        } else if (currentBlockType === "tool_use") {
          const input = JSON.parse(currentToolInputJson || "{}");
          assistantContent.push({
            type: "tool_use", id: currentToolId, name: currentToolName, input,
          } as Anthropic.ToolUseBlock);
          toolUseBlocks.push({ id: currentToolId, name: currentToolName, input });
        }
        currentBlockType = null;
        break;
    }
  }

  // No tool calls — done
  if (toolUseBlocks.length === 0) break;

  // Append assistant message
  messages.push({ role: "assistant", content: assistantContent });

  // Execute tools via MCP and collect results
  const toolResults: Anthropic.ToolResultBlockParam[] = [];
  for (const tool of toolUseBlocks) {
    const result = await mcpClient.callTool({ name: tool.name, arguments: tool.input });
    const output = (result.content as { type: string; text?: string }[])
      .map((c) => (c.type === "text" ? c.text : JSON.stringify(c)))
      .join("\n");
    toolResults.push({ type: "tool_result", tool_use_id: tool.id, content: output });
  }

  // Append tool results
  messages.push({ role: "user", content: toolResults });
}

await mcpClient.close();
```

### Streaming SSE events for a chat UI

When building a Next.js API route, stream responses as SSE events using a `ReadableStream`. Emit events in this format for compatibility with the `PythonChat` frontend component:

- `{ type: "text", content: "..." }` — streamed text chunks
- `{ type: "tool_start", name: "tool_name", input: "..." }` — tool execution starting
- `{ type: "tool_end", name: "tool_name", output: "..." }` — tool execution result
- `{ type: "error", content: "..." }` — error messages
- `data: [DONE]` — stream finished

### Key types

```typescript
// Tool conversion: MCP tool → Anthropic tool
const tools: Anthropic.Tool[] = mcpToolsList.map((t) => ({
  name: t.name,
  description: t.description || "",
  input_schema: t.inputSchema as Anthropic.Tool.InputSchema,
}));

// Tool results sent back as user messages
const toolResult: Anthropic.ToolResultBlockParam = {
  type: "tool_result",
  tool_use_id: toolUseBlock.id,
  content: "result text",
  is_error: false, // set true for errors
};
```

## Checklist

When setting up PICA MCP with the Anthropic SDK:

- [ ] `@anthropic-ai/sdk` is installed
- [ ] `@modelcontextprotocol/sdk` is installed
- [ ] `ANTHROPIC_API_KEY` is set in `.env.local`
- [ ] `PICA_SECRET` is set in `.env.local`
- [ ] `.env.example` documents both `ANTHROPIC_API_KEY` and `PICA_SECRET`
- [ ] MCP client uses stdio transport with `npx @picahq/mcp`
- [ ] Full `process.env` is spread into the transport's `env` option
- [ ] MCP tools are converted to `Anthropic.Tool[]` format
- [ ] Agent loop handles `tool_use` blocks and calls `mcpClient.callTool()`
- [ ] Tool results are sent back as `tool_result` blocks in a `user` message
- [ ] Loop has a step limit to prevent runaway execution
- [ ] MCP client is closed after use (`finally` block)
- [ ] Streaming handles `content_block_start`, `content_block_delta`, `content_block_stop` events
