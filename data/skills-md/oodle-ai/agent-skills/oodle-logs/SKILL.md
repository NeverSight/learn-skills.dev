---
name: oodle-logs
description: Search and query log data using OpenSearch Query DSL, and discover available log index patterns.
metadata:
  version: "1.0.0"
  author: oodle-ai
  repository: https://github.com/oodle-ai/agent-skills
  tags: oodle,logs,search,opensearch,index-patterns
  globs: "**/*log*,**/*opensearch*,**/*.ndjson"
  alwaysApply: "false"
---

# Oodle Logs — Search and Index Pattern Discovery

This skill teaches the agent to search log data using the OpenSearch-compatible query DSL and to discover available log index patterns.

## Prerequisites

```bash
brew install oodle-ai/oodle/oodle
oodle configure
```

Confirm the logs endpoint works:

```bash
oodle logs index-patterns -o json | jq 'length'
```

## Command Execution Order

Before running any log query:
1. Run `oodle logs index-patterns -o json` to discover available log index patterns.
2. Pick the appropriate index pattern `title` for your query.
3. Build the NDJSON query file using the discovered index pattern and OpenSearch Query DSL.
4. Set `--start` and `--end` to cover the time range you need. They default to `-1h` and `now`. 
5. Do not guess index names — always confirm with `index-patterns` first.

## Quick Reference

| Task | Command |
|------|---------|
| List log index patterns | `oodle logs index-patterns -o json` |
| Search logs | `oodle logs query -f query.ndjson --start <start> --end <end> -o json` |

## Common Operations

### List log index patterns

Discover available log index patterns before building log queries. The returned `title` field is used as the `index` value in NDJSON query files.

```bash
# CORRECT — list all available index patterns
oodle logs index-patterns -o json

# CORRECT — extract just the pattern titles
oodle logs index-patterns -o json | jq '.[].title'

# CORRECT — use a discovered pattern in a log query
oodle logs index-patterns -o json | jq '.[].title'
# Then use the title in your NDJSON file:
# {"index": "oodle_internal_dev_logs"}
# {"query": {"match_all": {}}, "size": 10}
```

### Log query

Search log data using the OpenSearch-compatible multi-search API. The request body uses NDJSON format with exactly two JSON lines: the first selects the index, the second contains the search query using OpenSearch Query DSL. Pass the body via `-f <file>`.

**Important constraints:**
- The CLI only supports a **single search body** (exactly 2 NDJSON lines: one header + one search). Multiple search pairs are not supported.
- Use `--start` and `--end` flags for time range filtering. Values can be epoch milliseconds (e.g., `1716825600000`), `now`, or relative expressions (e.g., `-1h`, `-24h`, `-7d`).
- **`--start` defaults to `-1h` and `--end` defaults to `now`**. If you are searching for data older than 1 hour, you **must** pass an explicit `--start` or the query will silently return 0 results.
- Do **not** put range filters on `timestamp` in the query body — the CLI auto-injects a `timestamp` range filter from `--start`/`--end`.

```bash
# CORRECT — basic query (searches last 1 hour by default)
cat > query.ndjson <<'EOF'
{"index": "logs-*"}
{"query": {"match_all": {}}, "size": 10}
EOF
oodle logs query -f query.ndjson -o json

# CORRECT — search for specific log messages with explicit time range
cat > query.ndjson <<'EOF'
{"index": "logs-*"}
{"query": {"bool": {"must": [{"match_phrase": {"message": "error"}}]}}, "size": 50, "sort": [{"timestamp": {"order": "desc"}}]}
EOF
oodle logs query -f query.ndjson --start -6h --end now -o json

# CORRECT — search older data using relative time
cat > query.ndjson <<'EOF'
{"index": "logs-*"}
{"query": {"bool": {"must": [{"match_phrase": {"message": "OOMKilled"}}]}}, "size": 100}
EOF
oodle logs query -f query.ndjson --start -7d --end -6d -o json

# CORRECT — search older data using epoch milliseconds
cat > query.ndjson <<'EOF'
{"index": "logs-*"}
{"query": {"match_phrase": {"message": "connection refused"}}, "size": 50}
EOF
oodle logs query -f query.ndjson --start 1716825600000 --end 1716912000000 -o json

# WRONG — omitting --start when searching for data older than 1 hour
cat > query.ndjson <<'EOF'
{"index": "logs-*"}
{"query": {"match_phrase": {"message": "yesterday's deploy error"}}, "size": 50}
EOF
oodle logs query -f query.ndjson -o json
# ^^^ Returns 0 results! --start defaults to -1h, so older data is excluded.
# FIX: add --start -24h (or whatever range covers the target timeframe)

# WRONG — putting a range filter on timestamp in the query body
cat > query.ndjson <<'EOF'
{"index": "logs-*"}
{"query": {"bool": {"must": [{"range": {"timestamp": {"gte": "now-1h", "lte": "now"}}}]}}, "size": 100}
EOF
# The CLI already injects a timestamp range from --start/--end. In-query range filters conflict.
# FIX: use --start and --end flags instead.

# WRONG — passing the query inline without -f
oodle logs query --body '{"index":"logs-*"}'

# WRONG — using JSON instead of NDJSON format
oodle logs query -f query.json   # file must be valid NDJSON (exactly two lines)
```

## Best Practices

### Discover index patterns before querying

Always run `oodle logs index-patterns` to find the correct index name. Guessing index names may return empty results or errors.

```bash
# CORRECT — discover first, then query
oodle logs index-patterns -o json | jq '.[].title'
# Use the discovered title in your NDJSON file

# WRONG — guessing index names
cat > query.ndjson <<'EOF'
{"index": "my-logs"}
{"query": {"match_all": {}}, "size": 10}
EOF
oodle logs query -f query.ndjson -o json
```

### Always use `--start` and `--end` for time range filtering

The CLI injects a `timestamp` range filter automatically from `--start`/`--end`. Do not add your own range filter on `timestamp` in the query body — it conflicts with the CLI-injected one.

```bash
# CORRECT — use CLI flags for time range
oodle logs query -f query.ndjson --start -24h --end now -o json

# CORRECT — use epoch milliseconds for precise ranges
oodle logs query -f query.ndjson --start 1716825600000 --end 1716912000000 -o json

# WRONG — relying on the default 1-hour window for older data
oodle logs query -f query.ndjson -o json
# ^^^ Only searches the last 1 hour. If the data you need is older, you get 0 results.

# WRONG — putting range filters on timestamp in the query body
{"query": {"bool": {"must": [{"range": {"timestamp": {"gte": "now-6h"}}}]}}}
# FIX: remove the range from the query body and use --start -6h instead.
```

### Use `-o json` for log query results

Log query responses contain nested JSON structures. Always use `-o json` and pipe through `jq` for extraction.

```bash
# CORRECT — extract log messages from the response
oodle logs query -f query.ndjson -o json | jq '.responses[].hits.hits[]._source.message'

# WRONG — using table output for complex nested log data
oodle logs query -f query.ndjson -o table
```

### Use index pattern fields to build precise queries

Each index pattern includes a `fields` array with field names and types. Use these to build targeted queries instead of `match_all`.

```bash
# CORRECT — check available fields first
oodle logs index-patterns -o json | jq '.[0].fields[].name'
# Then build a query using confirmed field names
```

## Failure Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API key | Run `oodle configure` or set `OODLE_API_KEY` |
| 400 Bad Request | Invalid NDJSON body or Query DSL | Validate the NDJSON file has exactly two lines; check OpenSearch Query DSL syntax |
| Empty result (not an error) | No matching logs in the index or time range | Widen the time range or check the index name with `oodle logs index-patterns` |
| 0 results for older data | `--start` defaults to `-1h`; data outside that window is excluded | Pass explicit `--start` for older data, e.g. `--start -24h` or `--start <epoch_ms>` |
| connection refused | Wrong `OODLE_DEPLOYMENT` URL | Check `OODLE_DEPLOYMENT` env var, ensure no trailing slash |
| 429 Too Many Requests | Rate limited | Add `--retries 3`, back off, reduce query frequency |
| `required flag "file"` | Missing required flag for log query | Add `-f` flag with path to NDJSON file |

## References

- [Oodle CLI repo](https://github.com/oodle-ai/oodle-cli)
- [Oodle docs](https://docs.oodle.ai)
- [OpenSearch Query DSL](https://opensearch.org/docs/latest/query-dsl/)
