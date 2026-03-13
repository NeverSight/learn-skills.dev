---
name: thegraph-mcp-skill
description: Use The Graph Subgraph MCP through UXC via native SSE with a fixed linked command for subgraph discovery, schema retrieval, deployment selection, and GraphQL query execution with help-first inspection and explicit auth handling.
---

# The Graph MCP Skill

Use this skill to run The Graph Subgraph MCP operations through `uxc` using the native SSE MCP endpoint.

Reuse the `uxc` skill for generic protocol discovery, envelope parsing, and error handling rules.

## Prerequisites

- `uxc` is installed and available in `PATH`.
- Network access to `https://subgraphs.mcp.thegraph.com/sse`.
- The Graph Gateway API key is available for authenticated calls.

## Core Workflow (The Graph-Specific)

Endpoint candidate inputs before finalizing:
- Official remote MCP endpoint:
  - `https://subgraphs.mcp.thegraph.com/sse`

1. Verify protocol/path from official source and probe:
   - Official source: `https://thegraph.com/docs/en/ai-suite/subgraph-mcp/introduction/`
   - probe candidate endpoint with:
     - `uxc https://subgraphs.mcp.thegraph.com/sse -h`
   - Confirm protocol is MCP (`protocol == "mcp"` in envelope).
2. Detect auth requirement explicitly:
   - Run host help or a minimal read call and inspect envelope.
   - This endpoint requires a The Graph Gateway API key sent as `Authorization: Bearer <key>`.
3. Register credential and use fixed link command by default:
   - `uxc auth credential set thegraph --secret-env THEGRAPH_API_KEY`
   - `uxc auth binding add --id thegraph-sse --host subgraphs.mcp.thegraph.com --path-prefix /sse --scheme https --credential thegraph --priority 100`
   - `command -v thegraph-mcp-cli`
   - If missing, create it:
     - `uxc link thegraph-mcp-cli https://subgraphs.mcp.thegraph.com/sse`
   - `thegraph-mcp-cli -h`
   - If command conflict is detected and cannot be safely reused, stop and ask skill maintainers to pick another fixed command name.
4. Inspect operation schema before execution:
   - `thegraph-mcp-cli -h`
   - `thegraph-mcp-cli <operation> -h`
5. Prefer discovery/schema operations first:
   - find candidate subgraphs or deployments
   - inspect schema
   - execute query only after identifier and schema are understood

## Capability Map

- Discovery:
  - search subgraphs by keyword
  - find top deployments for a contract
  - inspect deployment popularity / 30-day query volume
- Schema:
  - get schema by deployment ID
  - get schema by subgraph ID
  - get schema by IPFS hash
- Query execution:
  - execute GraphQL query by deployment ID
  - execute GraphQL query by subgraph ID
  - execute GraphQL query by IPFS hash

## Guardrails

- Keep automation on JSON output envelope; do not rely on `--text`.
- Parse stable fields first: `ok`, `kind`, `protocol`, `data`, `error`.
- Use `thegraph-mcp-cli` as default command path.
- `thegraph-mcp-cli <operation> ...` is equivalent to `uxc https://subgraphs.mcp.thegraph.com/sse <operation> ...` when the same auth binding is configured.
- Use direct `uxc "<endpoint>" ...` only as temporary fallback when link setup is unavailable.
- Prefer discovery and schema inspection before query execution.
- For production/stable workflows, prefer deployment-oriented selection over loosely changing latest-version references.
- Keep GraphQL query scope small on first pass:
  - add filters
  - add limits
  - fetch only required fields
- If auth fails:
  - confirm `uxc auth credential info thegraph` succeeds
  - confirm `uxc auth binding match https://subgraphs.mcp.thegraph.com/sse` resolves to `thegraph`
  - rerun `thegraph-mcp-cli -h`

## Tested Real Scenario

The following flow was exercised successfully through `uxc` against the live endpoint:

- search `uniswap` subgraphs
- compare candidates with `get_deployment_30day_query_counts`
- select the highest-volume candidate
- fetch schema for the chosen subgraph
- execute a minimal `_meta` GraphQL query

The selected candidate in that run was:

- subgraph ID: `5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV`
- deployment IPFS hash: `QmTZ8ejXJxRo7vDBS4uwqBeGoxLSWbhaA7oXa1RvxunLy7`

The minimal verified query shape was:

```graphql
{
  _meta {
    deployment
    hasIndexingErrors
  }
}
```

## References

- Invocation patterns:
  - `references/usage-patterns.md`
