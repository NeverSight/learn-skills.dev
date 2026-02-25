---
name: xsql
description: Use when you need to safely inspect MySQL/PostgreSQL data or schema via the xsql CLI.
license: MIT
compatibility: Designed for Claude Code and compatible AI agents that can run CLI commands.
metadata:
  repository: https://github.com/zx06/xsql
  docs: https://github.com/zx06/xsql#readme
  category: database-cli
allowed-tools: Bash(xsql:*)
---

# xsql - AI-first Cross-Database CLI Tool

xsql is a command-line tool designed for AI agents to execute read-only SQL queries on MySQL and PostgreSQL databases, with optional SSH tunnel support.

## Installation

```bash
go install github.com/zx06/xsql/cmd/xsql@latest
```

## Prerequisites

- Ensure a valid `xsql.yaml` exists (`./xsql.yaml` or `~/.config/xsql/xsql.yaml`) or pass `--config`.
- Confirm the target profile exists before running queries.

## Quick Reference

```bash
# Query with profile
xsql query "SELECT * FROM users LIMIT 10" -p <profile> -f json

# List all profiles
xsql profile list -f json

# Show profile details
xsql profile show <profile> -f json

# Get tool spec
xsql spec --format json

# Check version
xsql version
```

## Common Query Workflows

### 0. Identify the target database

```bash
# List profiles
xsql profile list -f json

# Inspect a profile to confirm database/host
xsql profile show <profile> -f json
```

### 1. Explore schema

SQL syntax varies by database (MySQL vs PostgreSQL). Adjust statements as needed.

```bash
# List tables
xsql query "SHOW TABLES" -p <profile> -f json

# Describe a table
xsql query "DESCRIBE table_name" -p <profile> -f json
```

### 2. Understand data distribution

```bash
# Count rows
xsql query "SELECT COUNT(*) AS total FROM table_name" -p <profile> -f json

# Sample rows
xsql query "SELECT * FROM table_name LIMIT 10" -p <profile> -f json
```

### 3. Investigate problematic records

```bash
# Time window
xsql query "SELECT * FROM table_name WHERE created_at >= NOW() - INTERVAL 7 DAY" -p <profile> -f json

# Key field filter
xsql query "SELECT * FROM table_name WHERE status = 'failed' LIMIT 50" -p <profile> -f json
```

## Commands

| Command | Purpose |
| --- | --- |
| `xsql query <SQL>` | Run a query (read-only by default) |
| `xsql profile list` | List profiles |
| `xsql profile show` | Show profile details |
| `xsql spec` | Export tool spec |
| `xsql version` | Version info |
| `xsql mcp server` | MCP integration |

### Query Flags

- `-p, --profile`: Select profile
- `-f, --format`: `json|yaml|table|csv|auto`
- `--unsafe-allow-write`: Allow writes (dangerous, disabled by default)
- `--allow-plaintext`: Allow plaintext passwords (only when explicitly enabled in config)
- `--ssh-skip-known-hosts-check`: Skip known_hosts check (risky)

## Output & Errors

- Non-TTY defaults to JSON, TTY defaults to table
- Use `-f json` to force JSON output
- stdout is data; stderr is logs
- Success: `{"ok":true,...}`; failure: `{"ok":false,"error":{...}}`
- Exit codes are stable; use `error.code` for programmatic handling

## Config & Env

- Priority: CLI > ENV > Config
- Paths: `--config` > `./xsql.yaml` > `~/.config/xsql/xsql.yaml`
- Store secrets in keyring when possible; allow plaintext only when explicitly enabled

## Best Practices

- Use `-f json` for machine consumption
- Use `ok` and `error.code` to decide success
- Read-only by default; writes require `--unsafe-allow-write`
