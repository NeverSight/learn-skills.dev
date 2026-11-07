---
name: add-mcp-server
description: Expose a Buildpad app's own data and actions as an MCP server, so Claude, Copilot, Kiro or Antigravity can call them as tools. Adds one Next.js route (`/api/mcp`, Streamable HTTP, stateless) built on the official MCP TypeScript SDK, where every tool forwards the caller's own access token to the data API, so the caller's permissions apply and no elevated key is used. Covers tool design, input validation, the response shape, client configuration, and testing with the MCP Inspector. Use when the user says add an MCP server, expose my app to AI agents, make tools for an agent, or build an MCP endpoint in the app. Not for connecting an agent to the Buildpad Platform's own MCP.
argument-hint: "[tool, e.g. list_orders]"
---

# Add an MCP Server to a Buildpad App

An MCP server lets an AI agent call your app's operations as typed tools. In a Buildpad app the
server is one API route. Each tool calls the data API on behalf of the person who connected, with
that person's own token, so the agent can do exactly what that person may do and nothing more.

This skill builds a server **inside the app**. It is not the Buildpad Platform's MCP, which
manages the project itself (environment variables, workers, connectors); to use that one, follow
the Platform's own instructions.

## Rules

1. **Forward the caller's token; never use an elevated key.** A tool reads the token from the
   request's `Authorization: Bearer <access token>` header and sends the same header to the data
   API. Do not read a service key, an administrator token or a stored credential in a tool. If the
   data API refuses the call, return its refusal as the tool's error; do not retry with more power.
2. **No token, no tools.** The route answers `401` with a `WWW-Authenticate: Bearer` header before
   it creates the server. Never list tools to an anonymous caller.
3. **Stateless.** Create a server and a transport per request (`sessionIdGenerator: undefined`).
   Amplify and other serverless hosts do not keep memory between requests, so a session map
   breaks.
4. **Validate every input with zod** and bound it: a `limit` has a maximum, a string has a maximum
   length, an enum lists its values. The agent writes these inputs, so treat them as untrusted.
5. **Small, named tools.** One tool is one operation with a verb name (`list_orders`,
   `create_order`). Do not add a tool that takes a raw path or a raw query and passes it through.
6. **Mark what changes data.** Give a read tool `annotations: { readOnlyHint: true }` and a delete
   tool `destructiveHint: true`, so the client can ask the person before it runs one.
7. **Return a short, structured answer.** Return only the fields the agent needs, as text of
   JSON. Never return tokens, headers or the raw upstream error body; return its message.
8. **Do not log the token** or the `Authorization` header.

## Steps

### 1. Install

```bash
pnpm add @modelcontextprotocol/sdk zod
```

Use the SDK's current documentation for the installed version if an import path below differs:
the Streamable HTTP transport for Web Standard `Request`/`Response` is the one to use in a
Next.js route.

### 2. Find how the app calls the data API

Read the app's existing server code for the helper that gives the data API's address and the
headers for a call (the one its API routes use; see [create-api-route](../create-api-route/SKILL.md)).
Reuse it. If the app has none, build the address from `NEXT_PUBLIC_BUILDPAD_DAAS_URL`. The MCP
route is a server route, so it needs no new environment variable.

### 3. Write the route

```ts
// app/api/mcp/route.ts
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { WebStandardStreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/webStandardStreamableHttp.js';
import { z } from 'zod';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

const DATA_URL = process.env.NEXT_PUBLIC_BUILDPAD_DAAS_URL!;

function unauthorized() {
  return new Response(JSON.stringify({ error: 'Send Authorization: Bearer <access token>' }), {
    status: 401,
    headers: { 'Content-Type': 'application/json', 'WWW-Authenticate': 'Bearer' },
  });
}

// One call to the data API, as the caller. A refusal comes back as the tool's error.
async function callData(authorization: string, path: string, init?: RequestInit) {
  const res = await fetch(`${DATA_URL}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...init?.headers, Authorization: authorization },
  });
  const body = await res.json().catch(() => null);
  if (!res.ok) {
    const message = body?.errors?.[0]?.message ?? `The data API answered ${res.status}`;
    return { isError: true as const, content: [{ type: 'text' as const, text: message }] };
  }
  return { content: [{ type: 'text' as const, text: JSON.stringify(body?.data ?? body) }] };
}

function buildServer(authorization: string) {
  const server = new McpServer({ name: 'my-app', version: '1.0.0' });

  server.registerTool(
    'list_orders',
    {
      title: 'List orders',
      description: 'List the most recent orders the signed-in user may see.',
      inputSchema: { limit: z.number().int().min(1).max(50).default(10) },
      annotations: { readOnlyHint: true },
    },
    ({ limit }) => callData(authorization, `/api/items/orders?limit=${limit}&sort=-date_created`)
  );

  return server;
}

export async function POST(request: Request) {
  const authorization = request.headers.get('authorization');
  if (!authorization?.toLowerCase().startsWith('bearer ')) return unauthorized();

  const server = buildServer(authorization);
  const transport = new WebStandardStreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  await server.connect(transport);
  return transport.handleRequest(request);
}

// A stateless server has no stream to resume or session to end.
const notAllowed = () => new Response('Method not allowed', { status: 405, headers: { Allow: 'POST' } });
export { notAllowed as GET, notAllowed as DELETE };
```

Replace `orders` with the app's own collection and add one `registerTool` per operation. Keep
the collection name and the allowed fields in the tool, not in the input.

### 4. Keep the route reachable and safe

- If the app's middleware redirects signed-out requests to a login page, exclude `/api/mcp` from
  that redirect: an agent cannot follow it, and the route does its own `401`.
- Do not add the route to a CORS allow-list for browsers. Agents call it server to server or from
  a desktop client, not from a page.
- Add the route to the app's rate limiting if it has any.

### 5. Connect a client

The agent needs the route's address and a token to send. Give the person this block and
fill in the address:

```json
{
  "mcpServers": {
    "my-app": {
      "type": "http",
      "url": "https://<the app's address>/api/mcp",
      "headers": { "Authorization": "Bearer ${MY_APP_TOKEN}" }
    }
  }
}
```

The file name and exact keys differ by tool (for example `.mcp.json` for Claude Code,
`.vscode/mcp.json` for VS Code, a user-level file for Kiro). Check the tool's own documentation
rather than guessing. Never commit a real token: the client reads it from an environment
variable. A token is the person's own access token, so it expires; say so, and do not put it in a
file in the repository.

### 6. Test

1. `curl -i -X POST <url>` with no header: expect `401`.
2. Run `npx @modelcontextprotocol/inspector`, choose Streamable HTTP, set the URL and the
   `Authorization` header, list the tools and call one.
3. Call a tool as a user whose role may not read that collection: expect the data API's refusal
   as the tool's error, not data.
4. Call a tool with an out-of-range input (`limit: 5000`): expect a validation error.

Add a Vitest test for the route that covers the `401`, one allowed call with `fetch` mocked, and
one refusal. See [create-tests](../create-tests/SKILL.md).

## Checklist before you finish

- [ ] No tool reads a service key or an administrator token.
- [ ] A call with no token gets `401` and lists nothing.
- [ ] Every input has a bound; every tool has a verb name; changing tools carry the hints.
- [ ] No tool returns a token, a header or a raw upstream body.
- [ ] The token is not logged and not committed.
- [ ] The route has a test for the `401`, an allowed call and a refusal.
