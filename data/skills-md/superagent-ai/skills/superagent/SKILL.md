---
name: superagent
description: Set up Superagent Context Guardrails at coding-agent tool boundaries, configure and safely use the remote MCP server, and manage signed webhooks for findings, security reports, Contributor Trust, and Runtime Guardrails. Use when the user asks to enable context scanning before an agent consumes URLs, files, email, skills, or MCP repositories; integrate coding-agent hooks; or install, connect, configure, troubleshoot, or operate Superagent from Cursor, Claude Code, Codex CLI, or another MCP client.
---

# Superagent

Set up Context Guardrails so external context is checked before a coding agent
consumes it, connect the agent to Superagent over MCP, or configure signed
webhooks. Keep credentials protected and avoid surprising the user with remote,
billable, destructive, or policy-changing actions.

Superagent MCP is an authenticated remote service. Do not connect to it, send
it data, or change an MCP client configuration unless the user explicitly asks.

Route setup requests by intent:

- **Context Guardrails setup or coding-agent hooks**: follow
  [Context Guardrails integration](#context-guardrails-integration). Connecting
  MCP alone does not enforce pre-consumption checks.
- **Connect or troubleshoot Superagent MCP**: follow
  [MCP setup workflow](#mcp-setup-workflow).
- **Signed event delivery**: follow [Webhook setup](#webhook-setup).

## MCP setup workflow

1. Identify the MCP client and whether the user wants a new connection,
   troubleshooting, or an operation on an existing connection.
2. For setup, direct the user to create an organization API key at
   [Superagent Settings](https://www.superagent.sh/app/settings#api-keys).
   Never ask them to paste the key into chat.
3. Store the key as `SUPERAGENT_API_KEY` in the user's shell or system
   environment. Never put it in a repository, tracked `.env` file, command
   output, or response.
4. Use the exact endpoint `https://www.superagent.sh/mcp`. The bare domain
   redirects, and some MCP clients fail on redirected POST requests.
5. Show the proposed configuration and obtain approval before editing client
   configuration or running a setup command.
6. Verify that the client connects and exposes Superagent tools before
   attempting a product operation.

An organization API key can access the entire organization. Prefer a dedicated,
revocable key for agent use and revoke it immediately if it is exposed.

## Client configuration

### Cursor

Add this server to `mcp.json`. Remote servers cannot read `envFile`, so
`SUPERAGENT_API_KEY` must exist in the environment that launches Cursor.

```json
{
  "mcpServers": {
    "superagent": {
      "url": "https://www.superagent.sh/mcp",
      "headers": {
        "Authorization": "Bearer ${env:SUPERAGENT_API_KEY}"
      }
    }
  }
}
```

### Claude Code

After confirming that `SUPERAGENT_API_KEY` is exported, propose:

```bash
claude mcp add --transport http --scope user superagent https://www.superagent.sh/mcp \
  --header "Authorization: Bearer $SUPERAGENT_API_KEY"
```

Run `/mcp` in Claude Code to confirm the connection.

### Codex CLI

Add the following to `~/.codex/config.toml`. The feature flag must appear above
every `[mcp_servers.*]` block. The token setting is the environment variable's
name, not the token itself.

```toml
experimental_use_rmcp_client = true

[mcp_servers.superagent]
url = "https://www.superagent.sh/mcp"
bearer_token_env_var = "SUPERAGENT_API_KEY"
```

Export the variable before launching Codex, then use `/mcp` to verify.

### Other MCP clients

Configure Streamable HTTP with:

- URL: `https://www.superagent.sh/mcp`
- Header: `Authorization: Bearer $SUPERAGENT_API_KEY`

Keep the token in the client's supported secret or environment-variable store,
not in a tracked configuration file.

## Operating Superagent

Inspect the connected server's available tools rather than assuming a fixed
tool list. Match the user's request to these capability groups:

- **Findings**: list and inspect findings, update manual triage, or request
  automated triage.
- **Reports**: list or inspect repository, Web app, agent, and package reports;
  create a new report only after confirmation.
- **Contributor Trust**: retrieve a cached result or start and check a scan.
- **Context Guardrails**: score Web pages, email, files, skills, and public MCP
  repositories before an agent consumes them.
- **Runtime Guardrails**: manage endpoint clients, groups, rules, built-in rule
  modes, and alerts.

Prefer the smallest read-only call that answers the question. Summarize the
result and preserve identifiers the user needs for a follow-up. For
asynchronous operations, report the returned status or identifier and avoid
tight polling.

## Context Guardrails integration

Distinguish a one-off scan from enforcement:

- For "scan/check this URL, file, email, skill, or MCP repository," use the
  corresponding MCP tool.
- For "add/enable/integrate Context Guardrails," install a check at the tool
  boundary before the agent consumes the context. A `SKILL.md`, `AGENTS.md`,
  rule, or system prompt is guidance, not enforcement.

Use this setup workflow:

1. Ask which context origins to protect, whether the setup is project-local or
   global, and whether an unavailable scanner should block the action. Recommend
   fail-closed for security-sensitive workflows and user-level or managed hooks
   for controls that use an organization API key. Use project hooks only in a
   trusted repository.
2. Inspect the client's current hook configuration and supported events. Merge
   with existing configuration; never replace it wholesale.
3. Gate the action that introduces context, before consumption: web-fetch and
   `curl`/`wget` actions for pages, download actions for public files, skill
   installation for skills, MCP add/install configuration for MCP repositories,
   and the inbound-message wrapper for email. Do not treat every later MCP tool
   call as a repository scan.
4. Map each selected origin to the narrowest client pre-execution boundary:
   - Cursor: `preToolUse`, `beforeShellExecution`, or `beforeMCPExecution`.
   - Claude Code: `PreToolUse` matched to `WebFetch`, `Bash`, `Skill`, or the
     relevant MCP tool.
   - Codex CLI: `PreToolUse` for supported local and MCP tools. Hosted
     `WebSearch` is not hookable, so disclose that gap instead of claiming full
     coverage.
   - Other clients: their equivalent before-tool hook, wrapper, middleware, or
     enforced rule plus an approved wrapper.
5. Show the exact hook, helper, paths, scope, verdict policy, outage behavior,
   and known coverage gaps. Obtain approval before writing files, changing
   client configuration, or sending a test target to Superagent.
6. For enforced hooks, install a small local helper that calls the Context
   Guardrails REST API with `SUPERAGENT_API_KEY`. Some clients support MCP-backed
   hook handlers, but a scan tool's result is not automatically a client-specific
   allow or deny decision, and MCP errors may fail open. Use MCP directly for
   interactive scans, not as the cross-client enforcement adapter. Keep the key
   in the environment, never in the helper or hook configuration. Prefer a
   user-controlled helper outside the repository and reference it by absolute
   path so repository code cannot silently replace it.
7. Test one allowed target and one blocked or unresolved target, then restart
   or reload the client if its hook system requires it. Use the client's hook
   inspector when available and verify the action itself was blocked, not merely
   that the helper printed a warning.

The helper must call the matching `/api/v1/context/*` endpoint:

- Web page URL -> `GET /context/web_page/{identifier}`
- Public text or PDF URL -> `POST /context/file`
- Raw RFC 822 email -> `POST /context/email`
- skills.sh or public GitHub skill -> `POST /context/skill`
- Public GitHub MCP repository -> `POST /context/mcp`

Skill and MCP scans support public GitHub targets only and require an active
Superagent Security GitHub App installation. Verify that prerequisite before
claiming those hook paths are enforced. Keep agent lifecycle hooks distinct
from package, Git, or other install hooks found inside scanned content; the
latter are threat signals.

Do not upload local private files through the public-URL file scanner, and get
explicit authorization before sending raw email or other user content. Package
and general repository scanning are not Context Guardrails origins: use
Superagent supply-chain scanning for packages and repository reports for source
repositories. Do not port an old package-install hook and claim that Context
Guardrails scanned the package.

For an enforcement decision, parse the JSON response rather than relying only
on score headers. Apply the selected tolerance consistently:

- `safe`: allow.
- `caution`: require user review unless the user explicitly chose a different
  policy.
- `suspicious` or `dangerous`: deny.
- `pending_deep_scan: true`, unscannable results, malformed responses, and
  scanner timeouts: treat as unresolved and follow the approved outage policy.

Do not let a preliminary identity score silently allow consumption while the
deep scan is pending. Either request `mode=full` with a hook timeout long enough
for completion, or block/ask and tell the agent to retry after the asynchronous
scan finishes. Exempt the Superagent scanner calls themselves from generic MCP
gates to avoid recursive checks.

### Hook safety requirements

Follow the installed client's current hook schema rather than copying one
client's JSON response into another:

- Use narrow, anchored tool matchers and command predicates. Broad hooks add
  latency and create bypasses or accidental blocks.
- Parse stdin as structured JSON. Never use `eval`, shell interpolation, or
  string-built commands with untrusted tool input. URL-encode identifiers and
  pass values as quoted arguments or request bodies.
- Emit only the client's documented decision JSON on stdout; send diagnostics
  to stderr. Treat malformed input and output as a security failure under the
  chosen outage policy.
- Use one bounded HTTPS request with explicit connection and total timeouts.
  Do not log authorization headers, raw email, or response bodies containing
  user content.
- Do not let hook configuration auto-approve an action that the client's normal
  permission system denies. Context Guardrails should only add restrictions.

Apply platform failure behavior explicitly:

- **Cursor:** security hooks fail open on crashes, timeouts, and invalid JSON
  unless the hook sets `failClosed: true`. Set it for enforced boundaries.
  `permission: "ask"` is not enforced for `preToolUse`; when review is required,
  use a boundary that supports asking or deny with a clear review instruction.
- **Claude Code:** use a `PreToolUse` denial response or exit code `2` for a hard
  block. A timed-out command, HTTP, or MCP-tool hook continues through normal
  permission flow, so timeout alone is not fail-closed. Keep normal permission
  rules in place as defense in depth.
- **Codex CLI:** use the documented `PreToolUse` denial JSON or exit code `2`
  with the reason on stderr. Invalid fields and hook failures can continue the
  tool call. Hosted tools such as `WebSearch` remain outside hook coverage.

## Webhook setup

Use webhooks when the user wants Superagent events delivered to an agent,
ticketing system, or remediation workflow. Webhook targets are configured at
the organization level in
[Superagent Settings](https://www.superagent.sh/app/settings), not through the
current MCP tool surface. Do not claim that an MCP call created or changed a
webhook.

Before setup:

1. Ask which public HTTPS endpoint should receive events and which event types
   the user needs.
2. Confirm that the endpoint can preserve the raw request body, return a quick
   `2xx` response, and move longer work to an asynchronous queue.
3. Show the proposed target name, URL, and subscriptions. Obtain approval
   before using browser tools or another authenticated interface to create or
   modify the organization-wide target.

Guide the user through **Settings** → **Webhooks** → **Add webhook**. Enter the
approved target name and HTTPS URL, select subscriptions, save, and copy the
signing secret. The secret is shown only once. Never ask the user to paste it
into chat, and never place it in source control, command output, logs, or a
response. Store it in the receiver's secret manager or environment.

Supported subscriptions include:

- `report.started` and `report.finished`
- `finding.created`, `finding.triage_completed`, and `finding.accepted`
- `contributor_trust.finished`
- `agent.finding_created` and `agent.action_blocked`

The receiver must:

- verify `X-Superagent-Signature` with HMAC-SHA256 over
  `<X-Superagent-Timestamp>.<raw-json-body>` using the signing secret;
- compare signatures with a timing-safe operation;
- deduplicate deliveries by `X-Superagent-Event-Id` or the payload `id`;
- return a `2xx` quickly, because network errors, `408`, `429`, and `5xx`
  responses are retried.

After saving, send a test event from Settings and verify the signature,
deduplication, and response path before enabling downstream automation. If the
secret is exposed, regenerate it immediately and update the receiver.

## Confirmation gates

Get explicit confirmation immediately before:

- creating any report or running automated finding triage, because these
  consume organization credits;
- permanently deleting a finding;
- creating, updating, assigning, or deleting Runtime Guardrails clients,
  groups, or rules;
- changing or restoring a built-in rule mode, because endpoint policy changes
  immediately;
- creating, changing, disabling, rotating, or deleting an organization webhook
  target or its event subscriptions;
- sending a target or content the user has not already authorized for remote
  analysis.

State the exact action, target, and consequence in the confirmation request.
Tool annotations are hints, not a substitute for this gate.

## Troubleshooting

- `401 invalid_token`: verify the key is present, active, and sent as
  `Authorization: Bearer ...`.
- `404` or failed connection on `superagent.sh/mcp`: switch to
  `https://www.superagent.sh/mcp`.
- Connected server with no tools: verify a proxy is not stripping the
  authorization header.
- Codex server unavailable: put `experimental_use_rmcp_client = true` above
  all MCP server blocks and ensure `bearer_token_env_var` contains the variable
  name.
- `429`: wait for the server's `Retry-After` interval. Do not retry
  aggressively.

## Documentation

- [MCP server](https://www.superagent.sh/docs/mcp)
- [API overview](https://www.superagent.sh/docs/api)
- [Settings and API keys](https://www.superagent.sh/docs/reference/settings)
- [Webhooks](https://www.superagent.sh/docs/webhooks)
- [Findings](https://www.superagent.sh/docs/findings)
- [Red Team reports](https://www.superagent.sh/docs/red-team)
- [Context Guardrails](https://www.superagent.sh/docs/context-guardrails)
- [Context Guardrails API](https://www.superagent.sh/docs/api/context-guardrails)
- [Cursor hooks](https://cursor.com/docs/hooks)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Codex CLI hooks](https://developers.openai.com/codex/hooks)
