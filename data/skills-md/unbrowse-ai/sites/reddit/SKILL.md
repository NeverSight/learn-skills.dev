---
name: reddit
description: "Reddit (reddit.com) for agents: Search Reddit posts by query; Read a old.reddit.com page by name — through Unbrowse's scoped MCP for reddit.com (unofficial), which replays reddit.com's own first-party API (no browser, verified results). Use when the user wants anything from reddit.com, e.g. search reddit posts by query."
---

# Unbrowse for Reddit (reddit.com)

Reddit as tools for your agent. Unofficial: not affiliated with or endorsed by reddit.com. Unbrowse compiled these from reddit.com's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no reddit.com API key.

## Connect the reddit.com MCP

This server is a tool scope holding only reddit.com: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on reddit.com.

```sh
claude mcp add --transport http reddit https://unbrowse.ai/mcp/reddit.com
codex mcp add reddit --url https://unbrowse.ai/mcp/reddit.com && codex mcp login reddit
```

```json
{"mcpServers":{"reddit":{"url":"https://unbrowse.ai/mcp/reddit.com"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch reddit.com some other way and present it as this skill's result.

## Tools

### `reddit_com__render_page` — Search Reddit posts by query

Search Reddit posts by query. Inputs: query. Returns the page's title, readable text and links. Read-only on reddit.com.

- `query` (string, required) — query — what to search for on reddit.com
- `cId` (string) — optional, e.g. "39fc2229-d05d-4c3e-8e8d-4c2bfbc71ee7"
- `iId` (string) — optional, e.g. "b01e7f1f-dce7-41a9-bec5-e7a09ad29673"
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"query":"<query>"}
```

### `old_reddit_com__read_page` — Read a old.reddit.com page by name

Read a old.reddit.com page by name. Inputs: name. Returns the page's title, readable text and links. Read-only on old.reddit.com.

- `name` (string, required)
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"name":"<name>"}
```

Always there too: `unbrowse.run` (a task on reddit.com in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on reddit.com), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on reddit.com → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off reddit.com is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills reddit.com's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/reddit.com/call/reddit_com__render_page \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"query":"<query>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/reddit.com/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
