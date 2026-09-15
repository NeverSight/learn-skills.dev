---
name: mcp-z-client
description: Use @mcp-z/client from Node.js code. Load when writing or reviewing a script or application that connects to MCP servers through @mcp-z/client. MCP server implementation belongs to the server SDK instead.
---

# @mcp-z/client

`@mcp-z/client` manages MCP server configuration, process startup, connections, discovery, calls, and cleanup. Use the package's wrappers for ordinary tool, prompt, and resource calls. Reach for the raw MCP SDK responses only when the wrapper omits data the caller needs.

## Install

```bash
npm install @mcp-z/client
```

Read the consuming project's existing MCP configuration before inventing one. A standard `.mcp.json` stores entries under `mcpServers`.

## Use the client

HTTP entries include `type: 'http'`. Stdio entries use `command` and optional `args` and `env`.

`registry.close()` closes every managed client and spawned process. Keep it in `finally`, or use `await using registry = createServerRegistry(config)` when the consuming runtime and project conventions support explicit resource management.

Tool names and schemas belong to the connected server, not this skill. Call `client.listTools()` before composing an unfamiliar invocation and use the returned input schema. Discovery is read-only. A tool call may change external state, so the call must stay within the user's requested action.

The convenience methods accept simple arguments:

- `client.callTool(name, args)`
- `client.getPrompt(name, args)`
- `client.readResource(uri)`

Their response wrappers expose `json()`, `text()`, and `raw()`. For tools, `json()` returns `structuredContent` when present and otherwise parses the first text block. Wrapper methods throw a typed response error for MCP error results or incompatible content.

Use `callToolRaw()`, `getPromptRaw()`, or `readResourceRaw()` only when the caller needs the untouched SDK response.

## Examples

- [Connect to a public server](resources/connect-public-server.md)
- [Spawn a local server](resources/spawn-local-server.md)
- [Use multiple servers](resources/multiple-servers.md)
- [Discover capabilities](resources/discover-capabilities.md)
- [Embed a server cluster](resources/embedded-cluster.md)
- [Test an MCP server](resources/automated-testing.md)

## Connection options

`createServerRegistry(config, { cwd, env, dialects })` controls spawned processes. Supplying `env` replaces the base environment rather than merging with `process.env`.

The default `dialects: ['servers']` starts stdio `command` entries. An HTTP entry with a `start` block needs `dialects: ['start']`, or `['servers', 'start']` when both forms should start.

`registry.connect(name, { versionNegotiation: { mode: 'auto' } })` probes for the current protocol revision and falls back to the legacy sequence. Pin a revision only when the caller requires that exact protocol.
