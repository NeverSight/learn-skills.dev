---
name: nx-cloud-api
description: Query the read-only Nx Cloud API for workspace data. Use this skill when a user asks to inspect or retrieve CIPEs, run groups, runs, tasks, workflows, agents, task statistics, flaky tasks, cache data, or API endpoint details. Use this skill before direct API calls. It provides safe authentication recovery steps. Do not use it for live CI monitoring.
---

# Nx Cloud API

This skill requires Node.js 18+, network access, and read access to the target Nx Cloud workspace. Its client is at `<skill_dir>/scripts/nx-cloud-api.mjs`. Use the workspace root only for the `--workspace` option.

Answer a defined workspace-data question with the bundled read-only client. This
is an API access skill, not a report generator or configuration editor.

## Non-negotiable rules

- Run `describe` before an unfamiliar named request. Use `catalog` only when you
  need to discover or disambiguate a route. The client reads the live OpenAPI
  document. Do not use remembered routes, fields, or parameters.
- Use only `request`. It permits documented `GET` operations only.
- Start with one filtered page. Ask for a workspace, scope, or time range when
  they are missing. Do not collect history by default.
- Read the operation description. A dry run validates only formal OpenAPI
  schema. It does not read credentials, contact the data endpoint, prove access,
  or enforce prose-only server limits.
- Do not put a token in a command, variable, chat message, or verbose log.

## Cache boundary

The API returns recorded task and run fields. It does not query the local Nx
target. `cacheEnabled` describes the recorded run. `cacheable` describes the
recorded task. Neither value identifies `targetDefaults`, an inferred target,
or Vite, ESLint, or another tool-native cache.

Do not infer `cache: false` from an absent project property. For cache causes,
target settings, inputs, outputs, or a configuration change, use
`nx-cloud-cache-investigator`. API data alone cannot justify a cache or inputs
pull request.

## Quick workflow

Run these commands from the workspace root. Add `--workspace <directory>` when
needed.

```sh
# Use catalog only when the endpoint is unknown or ambiguous.
node <skill_dir>/scripts/nx-cloud-api.mjs catalog --workspace .
node <skill_dir>/scripts/nx-cloud-api.mjs describe cipes --workspace .

# Save one bounded response. Do not print raw API data.
node <skill_dir>/scripts/nx-cloud-api.mjs request cipes \
  --workspace . \
  --query createdAfter=2026-08-01T00:00:00Z \
  --query statuses=FAILED \
  --pages 1 \
  --out /tmp/nx-cloud-cipes.json

# Fill a path parameter. Repeat an array filter.
node <skill_dir>/scripts/nx-cloud-api.mjs request 'runs/{runId}/tasks' \
  --workspace . \
  --path runId=<run-id> \
  --query statuses=FAILED \
  --query statuses=CANCELED \
  --pages 1
```

Use `describe` output for every selector, filter, status, and response field.
Follow a returned `links.*` URL directly. Do not reconstruct child URLs or use
an internal workflow ID as a route parameter. A relative link keeps the selected
server and filters. Check `source.cloudUrl` when a local `nx.json` and supplied
link can name different servers.

## Keep API output compact

For every live data request, use `--out <private-file>`. Do not let raw JSON or
NDJSON print to the terminal unless the user explicitly requests it. Read only a
question-specific projection with `jq`:

```sh
jq '{pageCount, fetchedItemCount, pageLimitReached,
  items: [.items[] | {id, status, createdAt}]}' /tmp/nx-cloud-cipes.json
```

Choose fields from `describe`. For one row, select it first, then project only
needed fields. For a single-resource response, project `.response` fields. Do
not read or paste the complete saved response into the model context.

Use `describe --json | jq '<small projection>'` when the normal description is
larger than the question needs. The default human-readable `catalog` output is
small; do not request catalog JSON unless you need to filter it.

## Authentication and failures

The client resolves the cloud URL and one credential set. It does not print a
token. Use `--token-file` for a workspace access token file. For PAT access, run
`nx login --status` from the workspace root. Run `nx login` there only when the
status check has no usable PAT.

Read [references/authentication.md](references/authentication.md) only when you
need credential precedence, a custom config file, or recovery from an
authentication, access, rate-limit, or network error.

## Same-session retry

Arrange one same-session wake only for a known request that the server cannot yet
complete: HTTP 409 while a named parent is non-terminal, or HTTP 429 with a retry
delay. Preserve the endpoint, IDs, filters, and page limit. Retry once after the
known delay. Stop at a terminal response or the retry limit. Do not use this skill
to poll or monitor live CI.

## Pagination and saved data

The default is one page. Set `--pages` only after the first response. Stop when
`pageLimitReached: true` unless the user accepts incomplete data. Do not fetch
all `flaky-tasks` or `task-stats` pages without a narrow filter.

For large or multi-range extraction, NDJSON, binary assets, or a calculation,
read [references/extraction-and-calculation.md](references/extraction-and-calculation.md)
before the request. That reference defines safe pagination, data-file metadata,
redirect downloads, and reproducible calculations.

## Interpret responses

`catalog` and `describe` return their server in `cloudUrl`. Collection rows are
in top-level `items`. A single-resource API object is in `response`; request
metadata is in `source`. Do not infer a field meaning from its name. Inspect its
live schema and a live record first.

Label cache statements by evidence source:

- **API response field:** a recorded `cacheEnabled`, `cacheable`, cache-status,
  or hash value.
- **Nx target query:** a value from `nx show project ... --json` in a matching
  checkout.
- **Tool-native cache:** `Unknown` until its executor options are inspected.

## Empty task assets

A valid task asset can have zero-byte terminal output and no output files;
`nx:noop` commonly does. Check the matching workspace task before reporting a
log-capture or archive defect.

## Report

State the APIs queried, filters, page count, and only material limits. State
whether a result is recorded API data, a local target query, or a hypothesis.
Never claim that an API-only read proved configuration provenance or tool-native
cache state.
