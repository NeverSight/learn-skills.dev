---
name: softprobe-agent-qa
description: Diagnose Softprobe Agent QA sessions and traces in Explorer. Use when investigating failed agent runs, tool errors, generations, sessions, or Explorer telemetry for Softprobe Agent QA. Prefer MCP tools from the softprobe server when available.
when_to_use: Softprobe Agent QA, Explorer sessions, traces, generations, tool errors, softprobe-agent-qa, softprobe skills investigate, softprobe MCP
---

# Softprobe Agent QA (investigate)

Read-only investigation of Softprobe Agent QA Sessions and traces via the Explorer gateway.

Humans bootstrap access; coding agents must **not** run browser login.

## Prefer MCP tools

When the `softprobe` MCP server is registered, call its tools directly (`whoami`, `get_session`, `search_sessions`, `get_trace`, …). Same auth and paths as the CLI scripts.

If MCP is missing, tell the human to run once:

```bash
bash ~/.agents/skills/softprobe-agent-qa/scripts/install-mcp.sh
```

Or the native one-liner:

```bash
cursor --add-mcp "{\"name\":\"softprobe\",\"command\":\"python3\",\"args\":[\"$HOME/.agents/skills/softprobe-agent-qa/scripts/mcp_server.py\"]}"
```

## Bootstrap

1. If credentials are missing or expired, tell the human to run:

```bash
python3 ~/.agents/skills/softprobe-agent-qa/scripts/login.py
```

2. Verify with MCP `whoami`, or:

```bash
python3 ~/.agents/skills/softprobe-agent-qa/scripts/softprobe_api.py whoami
```

3. If the API returns **409** / `workspace_picker_required`: MCP `list_workspaces` then `select_workspace`, or:

```bash
python3 ~/.agents/skills/softprobe-agent-qa/scripts/softprobe_api.py list-workspaces
python3 ~/.agents/skills/softprobe-agent-qa/scripts/softprobe_api.py select-workspace <workspace_id>
```

Or ask the human to pick a workspace in [Explorer](https://explorer.softprobe.ai).

Read [references/auth-and-routing.md](references/auth-and-routing.md) and [references/api-cheat-sheet.md](references/api-cheat-sheet.md).

## Investigate (narrowest first)

| Known | MCP tool / CLI |
|---|---|
| `session_id` | `get_session` then `get_session_observations` |
| `trace_id` | `get_trace` |
| `span_id` | `get_observation` |
| Time window only | `search_sessions` or `search_observations` with `from_time` / `to_time` (UTC) |
| Need log context | `logs_by_session` or `logs_by_trace` (fixed templates only) |

Prefer narrow time windows. Follow `next_cursor` when paging.

Cite `session_id` / `trace_id` / `span_id` in conclusions. Link:

`https://explorer.softprobe.ai?session=<session_id>`

## Guardrails

- **Read-only.** Do not ingest OTLP, create scores, or run arbitrary SQL.
- Do not ask the human to paste JWTs into chat.
- Do not call `https://thelake.softprobe.ai` directly with a user token.
- Do not send `X-Softprobe-Assertion` (the gateway mints it).
- This skill is **not** the OpenCode capture plugin (`@softprobe/opencode-plugin`).
