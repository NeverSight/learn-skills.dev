---
name: agentcore-mcp-oauth-facade
description: Build an OAuth + MCP protocol facade in front of Bedrock AgentCore Gateway or Runtime so strict MCP clients (Claude Code, Cursor, Amazon Quick, mcp-remote) can connect. Use when an MCP client fails OAuth discovery ("Fix highlighted fields", DCR errors), when tools beyond 30 silently disappear (Gateway tools/list pagination), when tool calls return 404 or "Unknown tool" (dual session-id, tool name prefix), or when adapting Cognito to RFC 9728/8414 metadata, redirect_uri rewriting, or Gateway schema limits.
license: MIT
metadata:
  author: sample-skills-for-builders
  version: "1.0.0"
---

# AgentCore MCP OAuth Facade

Bedrock AgentCore Gateway and Runtime expose MCP endpoints, but real-world MCP
clients expect a *complete* OAuth 2.0 + MCP implementation: RFC 9728 protected
resource metadata, RFC 8414 authorization server metadata, Dynamic Client
Registration, arbitrary loopback redirect URIs, `Mcp-Session-Id` continuity,
SSE responses, and un-paginated tool lists. Neither Cognito nor AgentCore
Gateway provides all of that out of the box.

This skill captures a production-tested pattern: a small stateless Lambda
facade (CloudFront → HTTP API → Lambda) that bridges every gap while **never
issuing tokens itself** — Cognito remains the issuer, and the Gateway's JWT
authorizer validates tokens unchanged.

```
MCP client (Claude Code / Cursor / Quick / mcp-remote)
    │  OAuth discovery, /oauth/authorize, /oauth/token, /register, /mcp
    ▼
OAuth Facade  (CloudFront → HTTP API $default stage → Lambda)
    │  injects routing session-id, rewrites tool names, aggregates pages,
    │  re-wraps JSON as SSE, synthesizes Mcp-Session-Id
    ▼
AgentCore Gateway (CUSTOM_JWT authorizer) ──► Lambda target ──► tools
```

## When to Apply

Reference this skill when:

- Putting Bedrock AgentCore Gateway or Runtime behind OAuth for third-party
  MCP clients (Claude Code, Cursor, Amazon Quick, anything built on
  `mcp-remote`).
- An MCP client's connect wizard fails with a manual-credentials form (e.g.
  Quick's "Fix highlighted fields") — almost always a broken discovery chain.
- Tools past the first 30 are missing from `tools/list` — Gateway pagination
  that the client never follows.
- Tool calls intermittently return 404 "no valid session" or `-32602 Unknown
  tool` after migrating from an MCP Runtime to AgentCore Gateway.
- Cognito must serve clients that expect DCR (RFC 7591) or arbitrary
  `redirect_uri` values.

**Not for:** general AgentCore service setup (Gateway targets, Runtime
deployment, IAM) — see the `aws-agentic-ai` skill for that.

## How It Works

The facade solves three groups of problems. Each has a deep-dive reference:

### 1. OAuth discovery and Cognito gap-filling

Cognito supports OAuth flows but is an *incomplete* OIDC provider for MCP
purposes: no DCR API, metadata only under Cognito's own domain, registered
redirect URIs only. The facade:

1. Serves three metadata documents at the **root domain** (CloudFront exists
   purely to give a clean root — some clients do not support path-prefixed
   discovery): RFC 9728 protected-resource, RFC 8414 authorization-server,
   and OIDC `openid-configuration`. Interactive endpoints point at the
   facade; `issuer` and `jwks_uri` stay on the real Cognito issuer so token
   validation is untouched.
2. Serves each document at both the bare path **and** the path-insertion
   variant (`/.well-known/openid-configuration/mcp`) — clients probe both.
3. Implements **fake DCR**: `POST /register` echoes the request and returns a
   pre-provisioned public client ID (201). No Cognito API call needed.
4. Rewrites `redirect_uri`: the client's original `{redirect_uri, state}` is
   packed into an HMAC-SHA256-signed `state` (10-min max age), Cognito always
   sees the facade's single registered callback, and the callback handler
   verifies the signature and bounces the code back to the client's real
   redirect URI. The facade stays fully stateless — no session store.
5. Injects the resource-server scope during `/oauth/authorize` (union with
   what the client asked for) — Gateway enforces scopes per `tools/call`,
   and generic clients only request `openid email`.

See [references/oauth-discovery-and-dcr.md](references/oauth-discovery-and-dcr.md).

### 2. MCP session and protocol bridging

AgentCore uses **two unrelated session identifiers**:

| Header | Owner | Purpose |
|---|---|---|
| `X-Amzn-Bedrock-AgentCore-Runtime-Session-Id` | AgentCore platform | Container routing key, **must be ≥ 33 chars** |
| `Mcp-Session-Id` | MCP protocol | Protocol session continuity |

The facade mints a fresh routing key per request (`facade-<uuid4hex>`, 39
chars) and passes the protocol header through untouched — with one surgical
exception: if the upstream echoes the injected routing key back as an
`mcp-session-id` response header (AgentCore does this on session-less
responses), the facade suppresses that echo. Spec-compliant clients adopt any
new `Mcp-Session-Id` they see, so the un-suppressed echo poisons the client's
session and every later call 404s.

Gateway itself is stateless and never returns an `Mcp-Session-Id`, but strict
clients require one from `initialize` — so the facade synthesizes a stable
one. It also re-wraps Gateway's `application/json` responses as single-event
SSE when the client sent `Accept: text/event-stream`, answers `GET /mcp` with
an empty SSE stream (Gateway 405s it, and `mcp-remote` retries forever), and
converts scope-403s into 401 + `WWW-Authenticate` so clients re-authenticate
instead of retry-looping.

See [references/mcp-session-and-protocol-bridging.md](references/mcp-session-and-protocol-bridging.md).

### 3. Gateway pagination and schema limits

- **tools/list pagination (the big one):** Gateway returns at most 30 tools
  per page plus `nextCursor`. Many MCP clients never follow the cursor, so
  tool #31 onward silently vanishes. The facade intercepts `tools/list` and
  walks the cursor chain server-side (bounded loop), returning one merged
  page with no `nextCursor`.
- **Tool name prefix:** Gateway exposes every tool as
  `{targetName}___{toolName}`. The facade strips the prefix on the way in
  (`tools/list`) and re-adds it on the way out (`tools/call`), so clients and
  internal callers keep using bare names. Every code path that talks to the
  Gateway directly (not through the proxy) must add the prefix itself.
- **Input schema whitelist:** Gateway's `create_gateway_target` accepts only
  `type/properties/required/items/description` in tool schemas. Pydantic
  output (`title`, `default`, `additionalProperties`, `anyOf` from
  `Optional[...]`) must be stripped and `anyOf` flattened to the first
  non-null branch.
- **No null arguments:** Gateway validates `tools/call` arguments against the
  schema and rejects `null` for typed optionals (FastMCP tolerated them).
  Drop `None` values before calling.

See [references/gateway-pagination-and-limits.md](references/gateway-pagination-and-limits.md)
— includes the Lambda-target pattern (reusing live FastMCP tool registrations,
generating the Gateway payload from them) and Custom Resource lifecycle
gotchas.

## Usage

Adoption checklist when fronting a Gateway with a facade:

1. **Discovery first.** Implement all three well-known documents (plus `/mcp`
   path-insertion variants) before debugging anything else. A single 404 in
   the chain silently downgrades clients to manual-credential forms.
2. **Never break the token chain.** Facade endpoints for interaction only;
   `issuer`/`jwks_uri` must remain the real IdP so the Gateway authorizer
   works unchanged.
3. **Handle both session-ids.** Mint a ≥33-char routing key per request;
   never let it leak into `Mcp-Session-Id`.
4. **Aggregate `tools/list`.** Assume clients do not paginate.
5. **Test with a real strict MCP client, not curl.** curl doesn't demand
   session-ids, doesn't request SSE, brings its own scopes, and never
   paginates — it passes while every real client fails. All six
   Gateway-vs-FastMCP differences in this skill were invisible to curl.
6. **Regenerate the tool payload on every tool-surface change**, or the
   Gateway keeps broadcasting the stale tool list.

## References

- [OAuth discovery, fake DCR, redirect rewriting](references/oauth-discovery-and-dcr.md)
- [MCP session handling and protocol bridging](references/mcp-session-and-protocol-bridging.md)
- [Gateway pagination, tool prefix, schema limits, Lambda target](references/gateway-pagination-and-limits.md)
- [MCP Authorization spec](https://modelcontextprotocol.io/specification/draft/basic/authorization)
- [RFC 9728 — OAuth 2.0 Protected Resource Metadata](https://www.rfc-editor.org/rfc/rfc9728)
- [RFC 8414 — OAuth 2.0 Authorization Server Metadata](https://www.rfc-editor.org/rfc/rfc8414)
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
