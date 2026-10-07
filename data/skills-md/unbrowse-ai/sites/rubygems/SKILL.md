---
name: rubygems
description: "Rubygems (rubygems.org) for agents: Search rubygems — through Unbrowse's scoped MCP for rubygems.org (unofficial), which replays rubygems.org's own first-party API (no browser, verified results). Use when the user wants anything from rubygems.org, e.g. search rubygems."
---

# Unbrowse for Rubygems (rubygems.org)

Rubygems as tools for your agent. Unofficial: not affiliated with or endorsed by rubygems.org. Unbrowse compiled these from rubygems.org's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no rubygems.org API key.

## Connect the rubygems.org MCP

This server is a tool scope holding only rubygems.org: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on rubygems.org.

```sh
claude mcp add --transport http rubygems https://unbrowse.ai/mcp/rubygems.org
codex mcp add rubygems --url https://unbrowse.ai/mcp/rubygems.org && codex mcp login rubygems
```

```json
{"mcpServers":{"rubygems":{"url":"https://unbrowse.ai/mcp/rubygems.org"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch rubygems.org some other way and present it as this skill's result.

## Tools

### `rubygems_org__get_search` — Search rubygems

Search rubygems. Inputs: query. Returns the page's title, readable text and links. Read-only on rubygems.org.

- `query` (string, required) — query (typed during “fill Search Gems…”)
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"query":"<query>"}
```

Always there too: `unbrowse.run` (a task on rubygems.org in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on rubygems.org), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on rubygems.org → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off rubygems.org is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills rubygems.org's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/rubygems.org/call/rubygems_org__get_search \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"query":"<query>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/rubygems.org/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
