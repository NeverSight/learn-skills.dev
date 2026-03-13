---
name: new-relic-nerdgraph
description: "Query New Relic via NerdGraph GraphQL API — run NRQL queries, search entities, and execute cross-account queries. Use when the user needs to fetch, search, or analyze data from New Relic."
license: MIT
compatibility: "Node.js 18+, run_in_terminal"
metadata:
  author: Maxim Yushin
  version: "1.0.0"
---

# New Relic NerdGraph Query Tool

## Purpose

Execute queries against the New Relic NerdGraph GraphQL API and return structured JSON results. This skill is a **data retrieval tool only** — it does not interpret or analyze the results.

Supports three operation types:

- **NRQL queries** — run any NRQL query (defaults to `Log` collection)
- **Entity search** — discover monitored services, hosts, and apps
- **Account listing** — discover accessible New Relic accounts and their IDs

## Prerequisites

### NR_API_KEY (required)

The `NR_API_KEY` environment variable must be set (New Relic User API key, starts with `NRAK-`).

**Check if it's set:**
```bash
echo "${NR_API_KEY:+SET}"
```

**If NOT set**, suggest one of these approaches to the user:

The key can be generated at: https://one.newrelic.com/admin-portal/api-keys/home (create a **User** key).

1. **Shell profile (recommended)** — add to `~/.zshrc` or `~/.bashrc`:
   ```bash
   export NR_API_KEY="NRAK-XXXXXXXXXXXXXXXXXXXX"
   ```
2. **direnv** — add to a `.envrc` file:
   ```bash
   export NR_API_KEY="NRAK-XXXXXXXXXXXXXXXXXXXX"
   ```
3. **macOS Keychain + shell** — store securely and load on shell init:
   ```bash
   security add-generic-password -a "$USER" -s NR_API_KEY -w "NRAK-XXXXXXXXXXXXXXXXXXXX"
   # Then in ~/.zshrc:
   export NR_API_KEY=$(security find-generic-password -a "$USER" -s NR_API_KEY -w)
   ```

Do NOT proceed with queries until the key is available. Do NOT hardcode the key in commands.

### NR_ACCOUNT_ID (required for `query` subcommand)

Required for NRQL queries. Set via:
- `--account <ID>` flag
- `NR_ACCOUNT_ID` environment variable

**If the user doesn't know their account ID**, run the `accounts` subcommand first to discover it.

### Node.js 18+

Required for the query script (uses native `fetch`).

## Script Location

The script location depends on how the skill was installed:

- **Global install (GitHub Copilot):** `~/.copilot/skills/new-relic-nerdgraph/scripts/nerdgraph.mjs`
- **Global install (Claude Code):** `~/.claude/skills/new-relic-nerdgraph/scripts/nerdgraph.mjs`
- **Project install:** `./.agents/skills/new-relic-nerdgraph/scripts/nerdgraph.mjs`

Detect the correct path by checking which exists. The script is always at `scripts/nerdgraph.mjs` relative to this SKILL.md.

## Subcommands

### `query` — Run NRQL Queries

```bash
node <script> query "<NRQL_QUERY>" --account <ID> [--limit <N>]
```

- Requires `--account <ID>` or `NR_ACCOUNT_ID` env var
- Outputs JSON array to stdout; errors go to stderr
- Retries up to 3 times on transient failures
- `--limit <N>` appends `LIMIT N` if the query doesn't already have one
- If the query has no `FROM` clause, `FROM Log` is appended automatically

**Cross-account queries:**

```bash
node <script> query "<NRQL_QUERY>" --accounts 12345,67890,11111
```

Use `--accounts` (plural, comma-separated) to run NRQL across multiple accounts simultaneously. This is useful when data spans dev/staging/prod or separate team accounts.

### `entities` — Search Entities

```bash
node <script> entities ["<search-query>"] [--type <TYPE>] [--domain <DOMAIN>]
```

- Search query uses NR entity search syntax (e.g., `name LIKE 'my-app'`)
- `--type`: filter by entity type (`APPLICATION`, `HOST`, `MONITOR`, etc.)
- `--domain`: filter by domain (`APM`, `INFRA`, `BROWSER`, `SYNTH`, etc.)
- If no arguments given, lists all reporting entities
- Returns: name, entityType, guid, alertSeverity, reporting status, and tags

### `accounts` — List Accounts

```bash
node <script> accounts
```

- No account ID required — uses the API key to discover all accessible accounts
- Returns: account ID and name for each account
- Use this when the user doesn't know their `NR_ACCOUNT_ID`

## NRQL Reference

### Common query patterns

The default collection is `Log`. These examples use it, but you can query any event type (`Transaction`, `SystemSample`, `Metric`, `PageView`, `SyntheticCheck`, etc.).

```sql
-- Fetch logs by time range
SELECT * FROM Log
WHERE `level` = 'error'
SINCE 1 hour ago
LIMIT 100

-- Filter by application or host
SELECT * FROM Log
WHERE `application` = '<APP_NAME>'
  AND `level` = 'error'
SINCE 1 hour ago
LIMIT 100

-- Search by message content
SELECT * FROM Log
WHERE `message` LIKE '%timeout%'
SINCE 1 hour ago
LIMIT 100

-- Count errors by facet
SELECT count(*) FROM Log
WHERE `level` = 'error'
SINCE 1 day ago
FACET `application`

-- Query transactions (non-Log example)
SELECT average(duration), count(*)
FROM Transaction
WHERE `appName` = '<APP_NAME>'
SINCE 1 hour ago
FACET `name`

-- Infrastructure metrics (non-Log example)
SELECT average(cpuPercent), average(memoryUsedPercent)
FROM SystemSample
SINCE 30 minutes ago
FACET `hostname`
```

### Syntax tips

- `SINCE` / `UNTIL` accept ISO strings (`'2026-02-25 07:15:59+01:00'`) or relative (`1 hour ago`)
- Backtick-wrap field names with dots/hyphens: `` `labels.app` ``
- `LIMIT MAX` returns up to 5000 events; default is 100
- `FACET` groups results by field
- `TIMESERIES` returns time-bucketed data
- Expand time windows progressively if queries return no results

### Entity search examples

```
name LIKE 'my-service'
type IN ('APPLICATION')
domain = 'APM' AND reporting = 'true'
tags.environment = 'production'
alertSeverity = 'CRITICAL'
```
