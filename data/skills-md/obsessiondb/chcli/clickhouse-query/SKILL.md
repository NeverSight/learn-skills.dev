---
name: clickhouse-query
description: Query ClickHouse databases using the chcli CLI tool. Use when the user wants to run SQL queries against ClickHouse, explore database schemas, inspect tables, or extract data from ClickHouse.
metadata:
  author: obsessiondb
  version: "1.1"
compatibility: Requires bun or node (for bunx/npx). Needs network access to a ClickHouse instance.
allowed-tools: Bash(bunx @obsessiondb/chcli:*) Bash(npx @obsessiondb/chcli:*) Bash(chcli:*) Bash(doppler run:*) Read Write
---

# chcli — ClickHouse CLI

chcli is a lightweight ClickHouse command-line client. Use it to run SQL queries, explore schemas, and extract data from ClickHouse databases.

## Running chcli

Prefer `bunx` if Bun is available, otherwise use `npx`:

```bash
bunx @obsessiondb/chcli -q "SELECT 1"
npx @obsessiondb/chcli -q "SELECT 1"
```

Or install globally:

```bash
bun install -g chcli
chcli -q "SELECT 1"
```

## Connection

Set connection details via environment variables (preferred for agent use) or CLI flags.

| Flag | Env Var | Alt Env Var | Default |
|------|---------|-------------|---------|
| `--host` | `CLICKHOUSE_HOST` | | `localhost` |
| `--port` | `CLICKHOUSE_PORT` | | `8123` |
| `-u, --user` | `CLICKHOUSE_USER` | `CLICKHOUSE_USERNAME` | `default` |
| `--password` | `CLICKHOUSE_PASSWORD` | | *(empty)* |
| `-d, --database` | `CLICKHOUSE_DATABASE` | `CLICKHOUSE_DB` | `default` |
| `-s, --secure` | `CLICKHOUSE_SECURE` | | `false` |
| *(none)* | `CLICKHOUSE_URL` | | *(none)* |

`CLICKHOUSE_URL` accepts a full URL (e.g. `https://host:8443`) and is parsed into host, port, secure, and password as a fallback when the individual env vars are not set.

### Resolution Order

```
CLI flag > Individual env var > CLICKHOUSE_URL (parsed) > Default value
```

For agent workflows, prefer setting env vars in a `.env` file (Bun loads `.env` automatically) or using a secrets manager like Doppler so every invocation uses the same connection without repeating flags.

See `references/connection.md` for detailed connection examples.

## Query Patterns

**Inline query** (most common for agents):

```bash
bunx @obsessiondb/chcli -q "SELECT count() FROM events"
```

**From a SQL file:**

```bash
bunx @obsessiondb/chcli -f query.sql
```

**Via stdin pipe:**

```bash
echo "SELECT 1" | bunx @obsessiondb/chcli
```

## Output Formats

**Always use `-F json` or `-F csv` when the output will be parsed by an agent.** The default format (`pretty`) is for human display and is difficult to parse programmatically.

```bash
# JSON — best for structured parsing
bunx @obsessiondb/chcli -q "SELECT * FROM events LIMIT 5" -F json

# CSV — good for tabular data
bunx @obsessiondb/chcli -q "SELECT * FROM events LIMIT 5" -F csv

# JSONL (one JSON object per line) — good for streaming/large results
bunx @obsessiondb/chcli -q "SELECT * FROM events LIMIT 100" -F jsonl
```

Available format aliases: `json`, `jsonl`/`ndjson`, `jsoncompact`, `csv`, `tsv`, `pretty`, `vertical`, `markdown`, `sql`. Any native ClickHouse format name also works.

See `references/formats.md` for the full format reference.

## Common Workflows

### Schema Discovery

```bash
# List all databases
bunx @obsessiondb/chcli -q "SHOW DATABASES" -F json

# List tables in current database
bunx @obsessiondb/chcli -q "SHOW TABLES" -F json

# List tables in a specific database
bunx @obsessiondb/chcli -q "SHOW TABLES FROM analytics" -F json

# Describe table schema
bunx @obsessiondb/chcli -q "DESCRIBE TABLE events" -F json

# Show CREATE TABLE statement
bunx @obsessiondb/chcli -q "SHOW CREATE TABLE events"
```

### Data Exploration

```bash
# Row count
bunx @obsessiondb/chcli -q "SELECT count() FROM events" -F json

# Sample rows
bunx @obsessiondb/chcli -q "SELECT * FROM events LIMIT 10" -F json

# Column statistics
bunx @obsessiondb/chcli -q "SELECT uniq(user_id), min(created_at), max(created_at) FROM events" -F json
```

### Data Extraction

```bash
# Extract to CSV file
bunx @obsessiondb/chcli -q "SELECT * FROM events WHERE date = '2024-01-01'" -F csv > export.csv

# Extract as JSON
bunx @obsessiondb/chcli -q "SELECT * FROM events LIMIT 1000" -F json > export.json
```

## Additional Flags

| Flag | Description |
|------|-------------|
| `-t, --time` | Print execution time to stderr |
| `-v, --verbose` | Print query metadata (format, elapsed time) to stderr |
| `--help` | Show help text |
| `--version` | Print version |

## Best Practices for Agents

1. **Always specify `-F json` or `-F csv`** — never rely on the default format, which varies by TTY context.
2. **Always use `LIMIT`** on SELECT queries unless you know the table is small. ClickHouse tables can contain billions of rows.
3. **Start with schema discovery** — run `SHOW TABLES` and `DESCRIBE TABLE` before querying unfamiliar databases.
4. **Use `-t` for timing** — helps gauge whether queries are efficient.
5. **Prefer env vars for connection** — set them once in `.env` or via a secrets manager like Doppler rather than repeating flags on every command.
6. **Use `count()` first** — before extracting data, check how many rows match to avoid overwhelming output.
