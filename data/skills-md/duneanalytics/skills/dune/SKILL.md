---
name: dune
description: "Dune CLI for querying blockchain and on-chain data via DuneSQL, searching decoded contract tables, managing saved queries, and monitoring credit usage on Dune Analytics. Use when user asks about blockchain data, on-chain analytics, token transfers, DEX trades, smart contract events, wallet balances, Ethereum/EVM chain queries, DuneSQL, or says \"query Dune\", \"search Dune datasets\", or \"run a Dune query\"."
compatibility: Requires network access and the Dune CLI (auto-installed on first use). Works on macOS, Linux, and Windows.
allowed-tools: Bash(dune:*) Bash(curl:*) Read
metadata:
  author: duneanalytics
  version: "1.0.0"
  cli_version: "0.1"
---

## Prerequisites

Assume the Dune CLI is already installed and authenticated. **Do not** run upfront install or auth checks. Just execute the requested `dune` command directly.

If a `dune` command fails, inspect the error to determine the cause and follow the recovery steps in [install-and-recovery.md](references/install-and-recovery.md):

- **"command not found"** → CLI not installed. See [CLI Not Found Recovery](references/install-and-recovery.md#cli-not-found-recovery).
- **401 / "unauthorized" / "missing API key"** → Auth failure. See [Authentication Failure Recovery](references/install-and-recovery.md#authentication-failure-recovery).
- **Unknown subcommand or flag / unexpected output** → Possible version mismatch. See [Version Compatibility](references/install-and-recovery.md#version-compatibility).

# Dune CLI

A command-line interface for [Dune](https://dune.com) -- the leading blockchain data platform. Use it to write and execute DuneSQL queries against on-chain data, discover datasets, search documentation, and monitor credit usage.

## Authentication

All commands except `docs search` require authentication via a Dune API key. The key is resolved in this priority order:

```bash
# 1. Flag (highest priority -- overrides everything)
dune query run 12345 --api-key <key>

# 2. Environment variable
export DUNE_API_KEY=<key>
dune query run 12345

# 3. Saved config file (lowest priority)
dune auth --api-key <key>        # saves to ~/.config/dune/config.yaml
dune query run 12345              # uses saved key
```

To save your key interactively (prompted from stdin):

```bash
dune auth
```

Config file location: `~/.config/dune/config.yaml`

## Global Flags

| Flag | Description |
|------|-------------|
| `--api-key <KEY>` | Dune API key (overrides `DUNE_API_KEY` env var and saved config) |

### Output Format (per-command flag)

Most commands support `-o, --output <FORMAT>` with values `text` (default, human-readable tables) or `json` (machine-readable).

> **Always use `-o json`** on every command that supports it. JSON output contains more detail than `text` (full API response objects vs. summarized tables) and is unambiguous to parse. The `text` format is for human terminal use and drops fields.

## DuneSQL

Dune uses **DuneSQL**, a Trino-based SQL dialect, as its query engine. Key points:

- All SQL passed to `--sql` flags or saved queries must be valid DuneSQL
- DuneSQL supports standard SQL with extensions for blockchain data types (addresses, hashes, etc.)
- See [dunesql-cheatsheet.md](references/dunesql-cheatsheet.md) for common types, functions, patterns, and pitfalls
- Use `dune docs search --query "DuneSQL functions"` to look up syntax and functions
- Reference docs: [Writing Efficient Queries](https://docs.dune.com/query-engine/writing-efficient-queries), [Functions and Operators](https://docs.dune.com/query-engine/Functions-and-operators)

## Key Concepts

### Performance Tiers

Query execution supports two tiers:

| Tier | Flag Value | Description |
|------|-----------|-------------|
| Medium | `medium` (default) | Standard compute resources. Suitable for most queries. |
| Large | `large` | Higher compute resources. Use for complex queries, large joins, or heavy aggregations. Costs more credits. |

### Execution States

After submitting a query, the execution progresses through these states:

| State | Meaning | Action |
|-------|---------|--------|
| `QUERY_STATE_PENDING` | Queued for execution | Wait |
| `QUERY_STATE_EXECUTING` | Currently running | Wait |
| `QUERY_STATE_COMPLETED` | Results available | Fetch results |
| `QUERY_STATE_FAILED` | Execution failed | Check error message; fix SQL and retry |
| `QUERY_STATE_CANCELLED` | Cancelled by user or system | Re-execute if needed |

### Dataset Categories

| Category | Description |
|----------|-------------|
| `canonical` | Core blockchain data (blocks, transactions, traces, logs) |
| `decoded` | ABI-decoded contract data (events and function calls) |
| `spell` | Dune Spellbook transformations (curated, higher-level tables like `dex.trades`) |
| `community` | Community-contributed datasets |

### Dataset Types

| Type | Description |
|------|-------------|
| `dune_table` | Core Dune-maintained tables |
| `decoded_table` | Contract ABI-decoded tables |
| `spell` | Spellbook transformation tables |
| `uploaded_table` | User-uploaded CSV/data tables |
| `transformation_table` | Materialized transformation tables |
| `transformation_view` | Virtual transformation views |

### Query Parameters

Parameters let you create reusable queries with variable inputs. Pass them as `--param key=value` (repeatable). The API auto-detects the type, but parameters support these types: `text`, `number`, `datetime`, `enum`.

```bash
dune query run 12345 --param wallet=0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --param days=30 -o json
```

## Command Overview

| Command | Description | Auth |
|---------|-------------|------|
| `dune auth` | Save API key to config file | No |
| `dune query create` | Create a new saved query | Yes |
| `dune query get <id>` | Fetch a saved query's SQL and metadata | Yes |
| `dune query update <id>` | Update an existing query | Yes |
| `dune query archive <id>` | Archive a saved query | Yes |
| `dune query run <id>` | Execute a saved query and wait for results | Yes |
| `dune query run-sql` | Execute raw DuneSQL directly (no saved query needed) | Yes |
| `dune execution results <id>` | Fetch results of a previous execution | Yes |
| `dune dataset search` | Search the Dune dataset catalog | Yes |
| `dune dataset search-by-contract` | Find decoded tables for a contract address | Yes |
| `dune docs search` | Search Dune documentation | No |
| `dune usage` | Show credit and resource usage | Yes |

## Common Workflows

### Ad-hoc SQL Analysis

```bash
# Run a one-off query directly
dune query run-sql --sql "SELECT block_number, block_time FROM ethereum.blocks ORDER BY block_number DESC LIMIT 5" -o json
```

### Discover Tables, Then Query

```bash
# 1. Find relevant tables with column schemas
dune dataset search --query "uniswap swaps" --categories decoded --include-schema -o json

# 2. Write and execute SQL using discovered table/column names
dune query run-sql --sql "SELECT * FROM uniswap_v3_ethereum.evt_Swap LIMIT 10" -o json
```

### Find Contract Tables, Then Query

```bash
# 1. Find decoded tables for a specific contract
dune dataset search-by-contract --contract-address 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984 --include-schema -o json

# 2. Query the discovered tables
dune query run-sql --sql "SELECT * FROM uniswap_v3_ethereum.evt_Transfer LIMIT 10" -o json
```

### Save and Execute a Reusable Query

```bash
# 1. Create a saved query with parameters
dune query create --name "Top Wallets" --sql "SELECT address, balance FROM ethereum.balances WHERE balance > {{min_balance}} LIMIT {{row_limit}}" -o json

# 2. Run it with parameter values
dune query run <returned-id> --param min_balance=1000 --param row_limit=50 -o json
```

### Long-Running Query (Submit and Poll)

```bash
# 1. Submit without waiting
dune query run 12345 --no-wait --performance large -o json
# Output: {"execution_id": "01ABC...", "state": "QUERY_STATE_PENDING"}

# 2. Check results later
dune execution results 01ABC... -o json
```

## Limitations

The following capabilities are available via the Dune MCP server or web UI but **not** via the CLI:

- **Visualization creation** (charts, counters, tables)
- **Blockchain listing** (list all indexed blockchains with table counts)
- **Table size analysis** (storage size of specific tables)

## Security

- **Never** output API keys or tokens in responses. Before presenting CLI output to the user, scan for strings that look like API keys (e.g. long alphanumeric tokens, strings prefixed with `dune_`, or values from `DUNE_API_KEY`). Redact them with `[REDACTED]`.
- **Always** confirm with the user before running write commands (`query create`, `query update`, `query archive`)
- **Always** use `-o json` on every command -- JSON output is more detailed and reliably parseable
- Use `--temp` when creating throwaway queries to avoid cluttering the user's saved queries
- **Never** pass `--api-key` on the command line when other users might see the terminal history. Prefer `dune auth` or the `DUNE_API_KEY` environment variable.

## Reference Documents

Load the relevant reference when you need detailed command syntax and flags:

| Task | Reference |
|------|-----------|
| Create, get, update, or archive saved queries | [query-management.md](references/query-management.md) |
| Execute queries (run, run-sql) or fetch execution results | [query-execution.md](references/query-execution.md) |
| Search datasets or find tables for a contract address | [dataset-discovery.md](references/dataset-discovery.md) |
| Search documentation or check account usage | [docs-and-usage.md](references/docs-and-usage.md) |
| DuneSQL types, functions, common patterns, and pitfalls | [dunesql-cheatsheet.md](references/dunesql-cheatsheet.md) |
| CLI install, authentication, and version recovery | [install-and-recovery.md](references/install-and-recovery.md) |
