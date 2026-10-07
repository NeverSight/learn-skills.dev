---
name: gutenberg
description: "Gutenberg (gutenberg.org) for agents: Search gutenberg — through Unbrowse's scoped MCP for gutenberg.org (unofficial), which replays gutenberg.org's own first-party API (no browser, verified results). Use when the user wants anything from gutenberg.org, e.g. search gutenberg."
---

# Unbrowse for Gutenberg (gutenberg.org)

Gutenberg as tools for your agent. Unofficial: not affiliated with or endorsed by gutenberg.org. Unbrowse compiled these from gutenberg.org's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no gutenberg.org API key.

## Connect the gutenberg.org MCP

This server is a tool scope holding only gutenberg.org: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on gutenberg.org.

```sh
claude mcp add --transport http gutenberg https://unbrowse.ai/mcp/gutenberg.org
codex mcp add gutenberg --url https://unbrowse.ai/mcp/gutenberg.org && codex mcp login gutenberg
```

```json
{"mcpServers":{"gutenberg":{"url":"https://unbrowse.ai/mcp/gutenberg.org"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch gutenberg.org some other way and present it as this skill's result.

## Tools

### `gutenberg_org__get_ebooks_search` — Search gutenberg

Search gutenberg. Inputs: query. Returns the page's title, readable text and links. Read-only on gutenberg.org.

- `query` (string, required) — query (typed during “fill Search books”)
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"query":"<query>"}
```

Always there too: `unbrowse.run` (a task on gutenberg.org in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on gutenberg.org), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on gutenberg.org → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off gutenberg.org is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills gutenberg.org's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/gutenberg.org/call/gutenberg_org__get_ebooks_search \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"query":"<query>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/gutenberg.org/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
