---
name: greenhouse
description: "Greenhouse (greenhouse.io) for agents: Greenhouse job board: open jobs — through Unbrowse's scoped MCP for greenhouse.io (unofficial), which replays greenhouse.io's own first-party API (no browser, verified results). Use when the user wants anything from greenhouse.io, e.g. greenhouse job board: open jobs."
---

# Unbrowse for Greenhouse (greenhouse.io)

Greenhouse as tools for your agent. Unofficial: not affiliated with or endorsed by greenhouse.io. Unbrowse compiled these from greenhouse.io's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no greenhouse.io API key.

## Connect the greenhouse.io MCP

This server is a tool scope holding only greenhouse.io: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on greenhouse.io.

```sh
claude mcp add --transport http greenhouse https://unbrowse.ai/mcp/greenhouse.io
codex mcp add greenhouse --url https://unbrowse.ai/mcp/greenhouse.io && codex mcp login greenhouse
```

```json
{"mcpServers":{"greenhouse":{"url":"https://unbrowse.ai/mcp/greenhouse.io"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch greenhouse.io some other way and present it as this skill's result.

## Tools

### `boards_api_greenhouse_io__get_anthropic_jobs` — Greenhouse job board: open jobs

Greenhouse job board: open jobs. Inputs: board. Returns jobs, meta. Read-only on boards-api.greenhouse.io.

- `board` (string, required) — board (typed during “search”)
- `content` (string) — optional, e.g. "true"
- `pay_transparency` (string) — optional, e.g. "true"
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"board":"<board>"}
```

Always there too: `unbrowse.run` (a task on greenhouse.io in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on greenhouse.io), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on greenhouse.io → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off greenhouse.io is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills greenhouse.io's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/boards-api.greenhouse.io/call/boards_api_greenhouse_io__get_anthropic_jobs \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"board":"<board>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/boards-api.greenhouse.io/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
