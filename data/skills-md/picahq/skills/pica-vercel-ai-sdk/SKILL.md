---
name: pica-vercel-ai-sdk
description: Integrate PICA into an application via MCP. Use when adding PICA tools, connecting PICA to an AI agent, setting up PICA MCP with Vercel AI SDK, or when the user mentions PICA.
---

# PICA MCP Integration

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

## Using PICA with Vercel AI SDK

The Vercel AI SDK provides MCP client support via the `@ai-sdk/mcp` package. Install it:

```bash
npm add @ai-sdk/mcp
```

### CRITICAL: Version alignment

`@ai-sdk/mcp`, `ai`, `@ai-sdk/react`, `@ai-sdk/openai`, `@ai-sdk/anthropic`, and all other `@ai-sdk/*` packages **must resolve to the same `@ai-sdk/provider-utils` major version**. If they don't, tool schemas created by the MCP client use different internal symbols than those expected by `streamText`, causing validation errors like:

```
Invalid input for tool ...: Type validation failed: Value: {}.
Error message: Cannot read properties of undefined (reading 'validate')
```

**How to diagnose:** look for multiple copies of `@ai-sdk/provider-utils`:

```bash
find node_modules -path "*/provider-utils/package.json" \
  -exec sh -c 'echo "$(dirname "{}"): $(node -e "console.log(require(\"{}\").version)")"' \;
```

If you see two different versions (e.g. `3.x` at root and `4.x` nested inside `@ai-sdk/mcp/node_modules/`), **upgrade all `@ai-sdk/*` and `ai` packages together** so they share a single version:

```bash
npm install ai@latest @ai-sdk/react@latest @ai-sdk/openai@latest @ai-sdk/anthropic@latest @ai-sdk/mcp@latest
```

You may also need to upgrade `react`/`react-dom` if peer dependency constraints require it.

### Before implementing: look up the latest docs

The Vercel AI SDK MCP API may change between versions. **Always search the bundled docs first** to get the current API before writing any code. For detailed instructions on where to find the docs and what to look for, see [vercel-ai-sdk-mcp-reference.md](vercel-ai-sdk-mcp-reference.md).

### Integration pattern

1. **Create an MCP client** using stdio transport pointed at `npx @picahq/mcp`
2. **Get tools** from the client — they are automatically converted to AI SDK tool format
3. **Pass tools** to `streamText()` or `generateText()`
4. **Enable multi-step execution** with `stopWhen: stepCountIs(N)` so the model can call tools and process results
5. **Close the MCP client** when the response is finished

When passing environment variables to the stdio transport, spread `process.env` so the subprocess inherits the full environment (PATH, etc.):

```typescript
env: {
  ...process.env as Record<string, string>,
  PICA_SECRET: process.env.PICA_SECRET!,
}
```

### Working example (API route)

```typescript
import {
  streamText,
  UIMessage,
  convertToModelMessages,
  stepCountIs,
} from 'ai';
import { createMCPClient } from '@ai-sdk/mcp';
import { Experimental_StdioMCPTransport as StdioMCPTransport } from '@ai-sdk/mcp/mcp-stdio';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const mcpClient = await createMCPClient({
    transport: new StdioMCPTransport({
      command: 'npx',
      args: ['@picahq/mcp'],
      env: {
        ...process.env as Record<string, string>,
        PICA_SECRET: process.env.PICA_SECRET!,
      },
    }),
  });

  const tools = await mcpClient.tools();

  const result = streamText({
    model: yourModel,
    // convertToModelMessages is async as of ai@6.x
    messages: await convertToModelMessages(messages),
    tools,
    stopWhen: stepCountIs(5),
    onFinish: async () => {
      await mcpClient.close();
    },
  });

  return result.toUIMessageStreamResponse({
    sendSources: true,
    sendReasoning: true,
  });
}
```

### UI rendering of PICA tool calls

PICA tools appear as **dynamic tool parts** in the AI SDK's `UIMessage` system (`type: "dynamic-tool"` with a `toolName` field). Standard AI SDK tools appear as `tool-invocation` (prefix `tool-`). Handle both in the message parts renderer:

```tsx
// In the message parts switch/map:
if (part.type.startsWith('tool-') || part.type === 'dynamic-tool') {
  const toolPart = part as any;
  // toolPart.toolName — the MCP tool name (e.g. "list_pica_integrations")
  // toolPart.state — "input-streaming" | "input-available" | "output-available" | "output-error"
  // toolPart.input — tool input parameters
  // toolPart.output — tool result (when state is "output-available")
}
```

Pass `toolPart.toolName` as the display title so Pica tools show their actual name rather than the generic part type.

## Checklist

When setting up PICA MCP in a project:

- [ ] `@ai-sdk/mcp` is installed
- [ ] **All `@ai-sdk/*` and `ai` packages share the same `@ai-sdk/provider-utils` version** (see Version alignment above)
- [ ] `PICA_SECRET` is set in `.env.local` (or equivalent)
- [ ] `.env.example` documents the `PICA_SECRET` variable
- [ ] MCP client uses stdio transport with `npx @picahq/mcp`
- [ ] Full `process.env` is spread into the transport's `env` option
- [ ] `convertToModelMessages` is awaited (async as of `ai@6.x`)
- [ ] Multi-step execution is configured with `stopWhen: stepCountIs(N)`
- [ ] MCP client is closed after use (`onFinish` for streaming, `try/finally` for non-streaming)
- [ ] UI handles both `"tool-invocation"` and `"dynamic-tool"` parts for rendering tool calls

## Additional resources

- For Vercel AI SDK MCP specifics and where to find the latest docs, see [vercel-ai-sdk-mcp-reference.md](vercel-ai-sdk-mcp-reference.md)
