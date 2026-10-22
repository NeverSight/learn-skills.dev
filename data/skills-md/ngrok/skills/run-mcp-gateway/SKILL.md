---
name: run-mcp-gateway
description: Expose an in-development MCP (Model Context Protocol) server for remote testing against AI model providers like Claude and OpenAI, with per-provider authentication and traffic inspection. Puts a cloud endpoint in front of your local MCP server, authenticates each provider with its own bearer token via Vaults, and forwards to your server kept off the public internet. Use when the user is building or testing an MCP server and needs a remote AI client to reach it. Use when the user says "test my MCP server", "expose my MCP server to Claude", "connect my MCP server to OpenAI", or "front door for my MCP server".
license: MIT
metadata:
  author: ngrok
  version: "1.0"
  category: connectivity
  surface: job
compatibility: Requires a locally running MCP server, the ngrok CLI authenticated with an agent authtoken, and an ngrok API key (the cloud endpoint and Vault secrets are created via `ngrok api`).
---

# Run an MCP gateway

Expose an in-development MCP (Model Context Protocol) server for remote testing against multiple AI model providers at once, with per-provider authentication and traffic inspection.

## Before you start

Auth is required (`ngrok-setup`). This job uses a cloud endpoint + internal endpoint and a Traffic Policy with per-provider auth + `forward-internal` - both from `ngrok-engine`. A working reference implementation ships in `references/`: `http-transport.ts` and `traffic-policy.yaml`.

## Architecture

```
MCP client (Claude/OpenAI) --Bearer token--> Cloud Endpoint (public, runs the policy)
  --forward-internal--> Agent Endpoint (bound internal, e.g. https://mcp.internal)
    --HTTP--> your MCP server (streamable HTTP transport)
```

Cloud endpoint (not agent) is required here: providers connect on their own schedule, so the public URL must persist independently of your dev process.

## Steps

1. **Give your MCP server an HTTP transport.** MCP dev servers are usually stdio; providers need streamable HTTP. Drop in `references/http-transport.ts` and call it alongside your existing stdio path:

   ```ts
   await runHttp(buildServer, port); // POST /mcp, bound to 127.0.0.1
   ```

   It needs `express` and `@modelcontextprotocol/sdk`. It binds loopback by default, so the process is reachable only through the local ngrok agent - pass `{ host }` to change that. stdio keeps working for local clients.

2. **Run the server as an internal endpoint.** The `.internal` URL is what makes it internal - no extra binding flag:
   `ngrok http <port> --url https://mcp.internal --host-header=rewrite`
   The `--host-header=rewrite` matters: traffic arriving via `forward-internal` carries `Host: mcp.internal`, which the MCP SDK's DNS-rebinding protection rejects by default.

3. **Create a vault + one secret per provider.** These are tokens you generate (not the provider's API key), so you can tell providers apart:

   ```bash
   ngrok api vaults create --name "mcp-callers"
   ngrok api secrets create --name "claude-key" --value "$(openssl rand -hex 32)" --vault-id "$VAULT_ID"
   ```

4. **Create a cloud endpoint with the policy** (`references/traffic-policy.yaml`). Its shape is security-critical, so use it as-is rather than re-deriving it: one rule per provider that matches that provider's bearer token, tags the caller, and `forward-internal`s - which is terminating - followed by an unconditional catch-all that returns 401. Anything without a valid token matches no provider rule and falls through to the 401.

   Do **not** restructure it so the rejection tests the `x-mcp-caller` tag instead. That header is added by the policy but is also a request header, so a client can send it and skip the check entirely.

   Attach via whichever surface fits (see `ngrok-surfaces`: Terraform or the operator for a durable setup, `ngrok api` from the CLI for a quick one).

5. **Point each provider at `https://<your-cloud-endpoint>/mcp`** with its bearer token as a custom header. Add a provider later by adding a secret and copying its policy rule.

## Gotchas

- **New server instance per request.** MCP's stateless HTTP pattern needs a fresh server object per request so concurrent providers don't share session state. `references/http-transport.ts` follows this.
- **Caller attribution is advisory.** `x-mcp-caller` tells your server which provider called, but a client holding any valid token can also send that header itself. Trust it for logging, not for authorization.
- **The `/mcp` path.** Providers expect the MCP endpoint at a path (commonly `/mcp`); make sure the transport and the URL you hand out agree.
- **host-header rewrite** (step 2) - the single most common reason a forwarded MCP request 400s.

## Notes for agents

- This is distinct from `expose-localhost`: it needs per-provider auth and a persistent cloud endpoint, not a plain tunnel.
- Don't invent the transport - use the bundled `http-transport.ts` and adapt the user's `buildServer`.
