---
name: pipefy-ipaas
description: >
  Use when the user wants to build, test, publish, or manage iPaaS
  (Advanced Automations) flows: multi-step integrations with external apps
  (Slack, Gmail, Google Sheets), incoming webhooks, schedules, routers, code
  steps, or iPaaS data tables. MCP-only, driven through 4 meta-tools over a
  per-pipe catalog discovered at runtime. For native if/then rules or
  prompt-driven AI automations, use skills/automations/ instead.
tags: [pipefy, ipaas, advanced-automations, flows, integrations]
---

# iPaaS (Advanced Automations)

Pipefy's embedded workflow-automation platform. A **flow** is a trigger plus a sequence of steps that call **pieces** (integration connectors). The MCP server exposes it through **4 meta-tools**: the flow-builder verbs are catalog entries you discover per pipe and invoke through `call_ipaas_tool`, never a fixed tool list.

## When to use

- "Integrate with Slack / Gmail / Google Sheets / an external app."
- User asks to integrate Pipefy with an external app (Slack, Gmail, Sheets, etc.) — use iPaaS tools here, not traditional automations or AI agents by default.
- "When a webhook comes in, do X." "On a schedule, do Y."
- "Build a multi-step flow with a router / loop / code step."
- Managing iPaaS data tables (separate from Pipefy database tables).

**When not to use:** native if/then rules on card events, or prompt-driven AI automations, both live in [skills/automations/pipefy-automations/SKILL.md](../../automations/pipefy-automations/SKILL.md). Simple HTTP callbacks on card events are `create_webhook` in [skills/members-email-webhooks/pipefy-members-email-webhooks/SKILL.md](../../members-email-webhooks/pipefy-members-email-webhooks/SKILL.md).

## Prerequisites

- **iPaaS enabled on the organization.** If not, the backend typically returns a permission error (often coded `PERMISSION_DENIED` with text like "iPaaS is disabled for your organization" — exact code/string is backend-dependent).
- **iPaaS OAuth client configured on this MCP server.** If `PIPEFY_IPAAS_OAUTH_CLIENT_ID` is blank, every tool returns a "disabled on this server" message (server-config disable, distinct from the org-level one).
- **Permission to create automations on the pipe** (pipe-admin ability).
- **Service account must be a pipe member.** When a flow runs under a service account, that account must be a member of the target pipe, or pipe-scoped calls under its identity fail with a permission error even after the flow is built. Adding the account elsewhere (org-level) is not enough. Provision one with `create_service_account` if needed, then attach it with `add_service_account_to_pipe(pipe_id, email, role_name)` immediately — see [skills/members-email-webhooks/pipefy-members-email-webhooks/SKILL.md](../../members-email-webhooks/pipefy-members-email-webhooks/SKILL.md) and [docs/mcp/tools/service-accounts.md](../../../docs/mcp/tools/service-accounts.md). The 4 meta-tools themselves act as the calling session's identity, so this applies to the service account your flow runs under, not to these tools.
- **MCP-only.** The 4 meta-tools have no CLI twin (deferred in [docs/parity.md](../../../docs/parity.md)); `add_service_account_to_pipe` is available on both MCP and CLI.
- The iPaaS workspace is **per-pipe**: the catalog and any existing flows, connections, and tables belong to one `pipe_id`, so the same call against two pipes can differ.
- Under `profile=remote`, `$env` secret references in arguments are rejected.

## Tools needed (MCP)

| Tool (MCP) | Read-only | Purpose |
|------------|-----------|---------|
| `get_ipaas_tools` | Yes | Discover the per-pipe catalog (compact), or with `tool_name` expand one entry's full input schema. |
| `call_ipaas_tool` | No | Invoke one catalog entry by name with `arguments` matching its schema. |
| `get_ipaas_connection_auth_url` | No | Start an OAuth connection: returns a consent URL to hand the user, plus a completion bundle. |
| `create_ipaas_connection` | No | Finish an OAuth connection, or create a token / API-key one directly. |

## The meta-tool pattern

The catalog is large (flow building, testing, tables, runs), some entries carrying very large input schemas. Do not load them all. Work in three steps:

1. `get_ipaas_tools(pipe_id)` — compact catalog: each entry's `name` and one-line description.
2. `get_ipaas_tools(pipe_id, tool_name="...")` — one entry's full description and `inputSchema`, fetched right before you use it.
3. `call_ipaas_tool(pipe_id, tool_name="...", arguments={...})` — invoke it. Arguments are forwarded verbatim; the iPaaS host validates them and its error messages relay back.

Never expand more than the entry you are about to call, and read the entry's own schema for exact argument names (they are not uniform across the catalog). What the catalog offers, by capability group:

- **Author a flow** — create a flow (trigger plus steps) in one call; add or update individual steps; set or update the trigger; add conditional router branches; rename or duplicate a flow. Steps can be an integration piece, a code step, a loop, or a router (prefer a piece over code).
- **Inspect a flow** — list flows; read a flow's step tree and per-step validity; validate a flow before publishing.
- **Discover pieces** — search the piece catalog (exact or fuzzy); read a piece action/trigger's input properties; resolve dropdown option values; validate a step config before applying it.
- **Connections** — list existing connections (each exposes an `externalId` used as a step's `auth`); get setup guidance.
- **Publish / lifecycle** — lock and publish a draft (enables it); enable or disable a published flow; delete a flow.
- **Test and runs** — test a flow end to end; test a single step; list runs; read one run's detail; retry a failed run; run one piece action once without saving a flow.
- **iPaaS data tables** — list tables, query records, create tables and fields, insert/update/delete records, delete a table.
- **AI** — list configured AI providers and models for agent-style steps.

Destructive catalog **calls** need the MCP confirmation token when the call is judged destructive, in this order: catalog `annotations.destructiveHint` true, then `arguments.operation` needle-equality after strip and casefold against `delete` / `remove` / `destroy` / `drop` / `uninstall` / `revoke`, then annotation false stops (do not fall through to name needles), else the catalog name is matched as a substring against those needles. A catalog miss (the name was not on the page this server read) is unclassifiable and takes the two-step as well. Mixed manage with `operation=DELETE` is two-step; `ADD` / `UPDATE` stay one-shot unless a `confirmation_token` is supplied, which routes any call through the guard. Show the preview to the user and get their approval, then call again with `confirm=true`, the preview's `confirmation_token`, and the same `arguments` as step 1 (`operation` may differ in case or surrounding whitespace; any other change returns a fresh preview). Do not invent extra needles.

## Steps — build and test a flow

The proven lifecycle: **discover, build, validate, test, then publish.** A self-contained webhook-to-code flow (no external connection) validated this end to end live.

1. **Discover** the catalog, then expand the flow-builder entry to read its schema:

   ```
   get_ipaas_tools pipe_id=<pipe_id>
   get_ipaas_tools pipe_id=<pipe_id> tool_name=<flow-builder entry>
   ```

2. **Research the pieces** you will use and read the exact trigger/action props before building. A trigger often has required config: a webhook trigger, for example, requires an authentication-type property (set it to none for an open URL). Use the piece-research and piece-props entries from the catalog.

3. **Build the flow** in one call via the flow-builder entry: a trigger plus an ordered list of steps. Reference the trigger output and earlier steps with the host's templating in each step's input. The call returns a `flowId` and a per-step validity summary.

4. **Validate** before testing (the validate entry) — reports structural issues without publishing.

5. **Test-run** end to end via the test entry. It runs in the TESTING environment; every `call_ipaas_tool` has a ~120s network budget (most relevant here for long runs). Pass mock trigger data when the trigger has no saved sample. A success returns each step's output — treat that payload as the source of truth for the test. **Test-run has real side effects** for external-app pieces (the action actually fires), so keep test data disposable; self-contained pieces (webhook, schedule, code, tables) are safe.

6. **(Optional) Inspect the run** with the run-detail entry for full step-by-step output. Read its schema for the exact argument name. Prefer the id returned by the test; if the run is not found, fall back to the run-listing entry or stop, since the test payload already holds the outputs.

7. **Publish** only on explicit user intent: the lock-and-publish entry locks the draft, publishes it, and enables it (yielding a live webhook URL for webhook triggers). A separate entry enables or disables an already-published flow.

## Steps — connect an external app

Any piece that touches an external app (Slack, Gmail, Google Sheets) needs a **connection** first; pass its `externalId` as the step's (or trigger's) `auth`. Self-contained pieces (webhook, schedule, HTTP, code, iPaaS tables) need none.

1. List existing connections (the connection-listing entry) and reuse an `externalId` if one fits. When several candidates serve the same piece, name them and ask the user rather than pick silently.
2. **Token / API-key pieces:** one `create_ipaas_connection` call with the credential (`connection_type` plus `value` matching the piece's auth props). To keep the secret out of the conversation, set it in the server environment and reference it as `{"$env": "PIPEFY_IPAAS_CONNECTION_<NAME>"}` (local servers only; rejected under `profile=remote`).
3. **OAuth pieces:** `get_ipaas_connection_auth_url` returns a consent URL and a completion bundle; the user authorizes in a browser and pastes back the redirect URL; `create_ipaas_connection` finishes it. Durable tokens are stored host-side. Creation is an upsert on `external_id` (reuse an id to rotate a credential).
4. For dropdown fields (Slack channel, sheet, label), resolve options against the connection with the option-resolving entry and use the option `value`, not the label. Large external workspaces can time out; take the ID from the user and pass it literally, since the action still works at runtime.

## Steps — one-shot action (no flow)

For a single task ("send one Slack message", "check my inbox"), the catalog has a run-one-action entry: a piece, action, `input`, and `auth`, executed once. No flow is created or saved.

## Success criteria

- The validate entry reports the flow ready to publish (all steps valid).
- The test entry returns a success with the expected step outputs.
- The list/structure entries show the flow with a configured trigger and no unconfigured steps.

## Failure modes

- **Org-level iPaaS disabled.** The backend typically returns a permission error (often `PERMISSION_DENIED` / "iPaaS is disabled for your organization"); nothing in the catalog works. Enable iPaaS on the org or use one that has it.
- **Server-config iPaaS disabled.** When `PIPEFY_IPAAS_OAUTH_CLIENT_ID` is blank, tools return "disabled on this server" — restore the default or set a client id.
- **Trigger unconfigured after build.** A trigger with required props (for example a webhook trigger's authentication type) blocks validation until set. Read its props first, then set them in the trigger input.
- **Wrong argument name.** Entry schemas are not uniform (a run-detail entry may key the run id differently from how a test entry returns it). Always expand the entry with `get_ipaas_tools(pipe_id, tool_name=…)` and build arguments from that schema.
- **Test-run has real side effects.** For external-app pieces the test performs the real action even from a draft. Keep test data disposable; self-contained pieces are safe.
- **External step fails with an auth error.** The piece needs a connection. Create one and pass its `externalId` as the step `auth`; for Slack the bot must be a member of the target channel.
- **`PERMISSION_DENIED` on pipe operations under a service account.** The service account the flow runs under is not a member of the pipe. Attach it with `add_service_account_to_pipe(pipe_id, email, role_name)` and confirm with `get_pipe_members`.
- **Dropdown resolution times out.** Large external workspaces can time out. Ask the user for the ID and pass it literally.
- **`$env` rejected under remote profile.** Secret references are local-only. Pass credentials through `create_ipaas_connection`, not inline `$env`.
- **Accidental destruction.** A destructive catalog call returns a preview with `confirmation_token`. Show the preview to the user and get their approval, then call again with `confirm=true` and the preview's `confirmation_token`. Judgement order: annotation `true`, then `arguments.operation` needle-equality, then annotation `false` stops (a false annotation does **not** fall through to name needles), else name substring needles. Mixed `operation=DELETE` is two-step; `ADD`/`UPDATE` are not. Prefer updating a step over deleting it.

## See also

- [skills/automations/pipefy-automations/SKILL.md](../../automations/pipefy-automations/SKILL.md) — native if/then rules and AI automations (not iPaaS).
- [skills/members-email-webhooks/pipefy-members-email-webhooks/SKILL.md](../../members-email-webhooks/pipefy-members-email-webhooks/SKILL.md) — `create_webhook` for HTTP callbacks on card events; `add_service_account_to_pipe` to grant a flow's service account pipe membership.
- [docs/mcp/tools/ipaas.md](../../../docs/mcp/tools/ipaas.md) and [docs/ipaas.md](../../../docs/ipaas.md) — meta-tool semantics and flow vocabulary.
