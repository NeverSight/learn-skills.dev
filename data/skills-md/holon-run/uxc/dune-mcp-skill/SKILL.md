---
name: dune-mcp-skill
description: Use Dune MCP through UXC for blockchain table discovery, SQL query creation/execution, execution result retrieval, and visualization with help-first schema inspection, explicit auth binding, and guarded credit-consuming operations.
---

# Dune MCP Skill

Use this skill to run Dune MCP operations through `uxc`.

Reuse the `uxc` skill for shared protocol discovery, output parsing, and generic auth/binding flows.

## Prerequisites

- `uxc` is installed and available in `PATH`.
- Network access to `https://api.dune.com/mcp/v1`.
- Dune API key is available for authenticated calls.

## Core Workflow

1. Confirm endpoint and protocol with help-first probing:
   - `uxc https://api.dune.com/mcp/v1 -h`
2. Configure credential/binding for repeatable auth:
   - `uxc auth credential set dune-mcp --auth-type api_key --header "x-dune-api-key={{secret}}" --secret-env DUNE_API_KEY`
   - `uxc auth credential set dune-mcp --auth-type api_key --header "x-dune-api-key={{secret}}" --secret-op op://Engineering/dune/api-key`
   - `uxc auth binding add --id dune-mcp --host api.dune.com --path-prefix /mcp/v1 --scheme https --credential dune-mcp --priority 100`
3. Use fixed link command by default:
   - `command -v dune-mcp-cli`
   - If missing, create it: `uxc link dune-mcp-cli https://api.dune.com/mcp/v1`
   - `dune-mcp-cli -h`
4. Inspect operation schema before execution:
   - `dune-mcp-cli searchTables -h`
   - `dune-mcp-cli searchTablesByContractAddress -h`
   - `dune-mcp-cli createDuneQuery -h`
   - `dune-mcp-cli executeQueryById -h`
   - `dune-mcp-cli getExecutionResults -h`
5. Prefer read/discovery operations first, then query creation or credit-consuming execution.

## Capability Map

- Discovery:
  - `searchDocs`
  - `searchTables`
  - `listBlockchains`
  - `searchTablesByContractAddress`
- Query lifecycle:
  - `createDuneQuery`
  - `getDuneQuery`
  - `updateDuneQuery`
  - `executeQueryById`
  - `getExecutionResults`
- Analysis helpers:
  - `generateVisualization`
  - `getTableSize`
  - `getUsage`

## Recommended Usage Pattern

1. Find the right table first:
   - `dune-mcp-cli searchTables query='uniswap swaps'`
   - `dune-mcp-cli searchTablesByContractAddress contractAddress=0x...`
2. Prefer higher-level `spell` tables when they already expose the metrics you need.
3. Keep SQL partition-aware:
   - use `block_date`, `evt_block_date`, or another partition/date column in `WHERE`
4. Create a temporary query only after confirming table choice and date range.
5. Execute and fetch results by execution ID.

## Guardrails

- Keep automation on JSON output envelope; do not rely on `--text`.
- Parse stable fields first: `ok`, `kind`, `protocol`, `data`, `error`.
- Use `dune-mcp-cli` as default command path.
- `dune-mcp-cli <operation> ...` is equivalent to `uxc https://api.dune.com/mcp/v1 <operation> ...`.
- Discovery operations are read-only:
  - `searchDocs`
  - `searchTables`
  - `listBlockchains`
  - `searchTablesByContractAddress`
  - `getDuneQuery`
  - `getExecutionResults`
  - `getTableSize`
  - `getUsage`
- Require explicit user confirmation before credit-consuming or state-changing operations:
  - `createDuneQuery`
  - `updateDuneQuery`
  - `executeQueryById`
  - `generateVisualization`
- Be careful with privacy:
  - confirm before switching a query from private to public
  - temporary queries can still be visible; inspect `is_private` and `is_temp`
- `key=value` input now supports automatic type conversion for numeric MCP arguments.
- Numeric IDs can be passed directly with `key=value`, for example:
  - `query_id=6794106`
  - `queryId=6794106`
- Positional JSON is still useful for nested objects or when mixing string and numeric fields precisely:
  - `{"executionId":"01...","timeout":90,"limit":20}`
- For SQL passed via `key=value`, wrap the whole SQL string in double quotes so inner SQL single quotes survive shell parsing.
- If `listBlockchains` returns a Dune-side schema/facet error, fall back to `searchTables` with `blockchains` filters.

## Tested Real Scenario

The following flow was exercised successfully through `uxc`:

- discover table: `uniswap.uniswapx_trades`
- create temporary query for Base daily volume
- execute query
- fetch results

The successful SQL shape was:

```sql
SELECT block_date,
       ROUND(SUM(amount_usd), 2) AS daily_volume_usd,
       COUNT(*) AS trades
FROM uniswap.uniswapx_trades
WHERE blockchain = 'base'
  AND block_date >= date_add('day', -7, CURRENT_DATE)
GROUP BY 1
ORDER BY 1 DESC
LIMIT 7
```

## References

- Invocation patterns:
  - `references/usage-patterns.md`
