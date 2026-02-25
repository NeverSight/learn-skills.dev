---
name: building-cloudflare-mcp
description: Create MCP servers on Cloudflare Workers using the MCP Connector pattern. Use when user mentions "cloudflare mcp", "worker mcp", "mcp connector", or wants to deploy MCP tools on Cloudflare.
---

# Cloudflare MCP Connector

Build and deploy MCP (Model Context Protocol) servers on Cloudflare Workers using the MCP Connector pattern.

## Why Cloudflare Workers for MCP?

- **Global edge deployment** - Low latency worldwide
- **MCP Connector compatible** - Works with Claude API MCP integration
- **No cold starts** - Always-on serverless
- **Free tier** - 100K requests/day free
- **Easy authentication** - Headers-based auth

## Official Documentation References

When you need deeper context, fetch these with WebFetch:

| Topic | URL |
|-------|-----|
| **Code Mode Pattern** | https://www.anthropic.com/engineering/code-execution-with-mcp |
| Remote MCP Servers | https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers.md |
| MCP Connector API | https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md |
| Agent SDK MCP | https://platform.claude.com/docs/en/agent-sdk/mcp.md |
| Claude Code MCP | https://code.claude.com/docs/en/mcp.md |
| Cloudflare Code Mode | https://blog.cloudflare.com/code-mode/ |

### Code Mode (Advanced Pattern)

For high-scale deployments with many tools, consider the **Code Mode** pattern:
- Present MCP tools as code APIs (filesystem structure)
- Agent writes code to call tools instead of direct tool calls
- **98.7% token savings** for large tool sets
- Filter/transform data in execution environment before returning

**Why it works**: LLMs have seen millions of real TypeScript examples in training, but only contrived synthetic tool-call examples.

**Cloudflare Agents SDK** (built-in Code Mode):
```typescript
import { codemode } from "agents/codemode/ai";

const {system, tools} = codemode({
  system: "You are a helpful assistant",
  tools: { /* tool definitions */ },
});

const stream = streamText({
  model: openai("gpt-5"),
  system,
  tools,
  messages: [{ role: "user", content: "..." }]
});
```

Docs: https://github.com/cloudflare/agents/blob/main/docs/codemode.md

## MCP Server Structure

### Minimal Worker Template

```typescript
// src/index.ts
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
      });
    }

    // Auth check
    const authHeader = request.headers.get('Authorization');
    if (authHeader !== `Bearer ${env.MCP_API_KEY}`) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Parse MCP request
    const body = await request.json() as MCPRequest;

    // Handle MCP methods
    switch (body.method) {
      case 'tools/list':
        return Response.json({
          jsonrpc: '2.0',
          id: body.id,
          result: { tools: getToolsList() }
        });

      case 'tools/call':
        const result = await handleToolCall(body.params, env);
        return Response.json({
          jsonrpc: '2.0',
          id: body.id,
          result
        });

      default:
        return Response.json({
          jsonrpc: '2.0',
          id: body.id,
          error: { code: -32601, message: 'Method not found' }
        });
    }
  },
};

interface MCPRequest {
  jsonrpc: '2.0';
  id: string | number;
  method: string;
  params?: Record<string, unknown>;
}

interface Env {
  MCP_API_KEY: string;
  // Add other bindings (KV, D1, R2, etc.)
}

function getToolsList() {
  return [
    {
      name: 'example_tool',
      description: 'Description of what this tool does',
      inputSchema: {
        type: 'object',
        properties: {
          param1: { type: 'string', description: 'First parameter' },
        },
        required: ['param1'],
      },
    },
  ];
}

async function handleToolCall(params: { name: string; arguments: Record<string, unknown> }, env: Env) {
  switch (params.name) {
    case 'example_tool':
      return { content: [{ type: 'text', text: `Result: ${params.arguments.param1}` }] };
    default:
      throw new Error(`Unknown tool: ${params.name}`);
  }
}
```

### wrangler.toml

```toml
name = "my-mcp-server"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[vars]
# Non-secret config here

# Secrets added via: wrangler secret put MCP_API_KEY
```

## Claude Code Configuration

### Add Remote MCP Server

```bash
# Using CLI (user scope for global access)
claude mcp add --scope user my-mcp-server \
  --transport http \
  --url "https://my-mcp-server.username.workers.dev" \
  --header "Authorization: Bearer YOUR_API_KEY"
```

### Manual Configuration (~/.claude.json)

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "type": "http",
      "url": "https://my-mcp-server.username.workers.dev",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

### Auto-Approve Tools (~/.claude/settings.json)

```json
{
  "autoApproveTools": [
    "mcp__my-mcp-server__*"
  ]
}
```

## Tool Naming Convention

Tools from MCP servers follow this pattern:
```
mcp__<server-name>__<tool-name>
```

Examples:
- `mcp__my-mcp-server__example_tool`
- `mcp__supabase__execute_sql`
- `mcp__context7__query-docs`

## Authentication Patterns

### Bearer Token (Recommended)
```typescript
const authHeader = request.headers.get('Authorization');
if (authHeader !== `Bearer ${env.MCP_API_KEY}`) {
  return Response.json({ error: 'Unauthorized' }, { status: 401 });
}
```

### API Key Header
```typescript
const apiKey = request.headers.get('X-API-Key');
if (apiKey !== env.API_KEY) {
  return Response.json({ error: 'Unauthorized' }, { status: 401 });
}
```

### IP Allowlist (Additional Layer)
```typescript
const clientIP = request.headers.get('CF-Connecting-IP');
const allowedIPs = env.ALLOWED_IPS?.split(',') || [];
if (allowedIPs.length && !allowedIPs.includes(clientIP)) {
  return Response.json({ error: 'Forbidden' }, { status: 403 });
}
```

## Deployment Workflow

```bash
# 1. Create project
npm create cloudflare@latest my-mcp-server -- --template worker-typescript

# 2. Install dependencies
cd my-mcp-server
npm install

# 3. Add secrets
wrangler secret put MCP_API_KEY
# Enter your secure API key

# 4. Deploy
wrangler deploy

# 5. Add to Claude Code
claude mcp add --scope user my-mcp-server \
  --transport http \
  --url "https://my-mcp-server.username.workers.dev" \
  --header "Authorization: Bearer YOUR_API_KEY"

# 6. Restart Claude Code
# Exit and run: claude --resume
```

## Advanced: Cloudflare Bindings

### KV Storage
```typescript
// wrangler.toml
[[kv_namespaces]]
binding = "MY_KV"
id = "abc123"

// Usage
const value = await env.MY_KV.get('key');
await env.MY_KV.put('key', 'value');
```

### D1 Database
```typescript
// wrangler.toml
[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "abc123"

// Usage
const result = await env.DB.prepare('SELECT * FROM users WHERE id = ?')
  .bind(userId)
  .first();
```

### R2 Storage
```typescript
// wrangler.toml
[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket"

// Usage
const object = await env.BUCKET.get('file.txt');
await env.BUCKET.put('file.txt', content);
```

## Troubleshooting

### MCP Not Loading
1. Check worker is deployed: `curl https://your-worker.workers.dev`
2. Verify auth header matches secret
3. Restart Claude Code after config changes

### Tools Not Appearing
1. Check `tools/list` response format
2. Verify tool schema is valid JSON Schema
3. Check Claude Code logs: `/mcp` command

### Permission Errors
1. Add to autoApproveTools in settings.json
2. Use wildcard: `mcp__my-mcp-server__*`

## Security Checklist

- [ ] Use strong, unique API keys (32+ chars)
- [ ] Store secrets via `wrangler secret put`
- [ ] Never commit secrets to git
- [ ] Consider IP allowlisting for sensitive MCPs
- [ ] Use HTTPS only (Cloudflare provides this)
- [ ] Implement rate limiting if needed
- [ ] Log access attempts for auditing
