---
name: query-api
description: "Use when working with Laminar's SQL Query API (/v1/sql/query): design SELECT-only ClickHouse queries, use parameters, authenticate with project API keys, and interpret response data from spans, traces, events, tags, datasets, and evaluations."
---

# Laminar Query API

## Workflow

1. Clarify the question, target tables, and time window.
2. Draft a SELECT-only ClickHouse query with a time filter on start_time.
3. If needed, use typed parameters (for example, {id:String}) and supply a parameters map.
4. Call POST /v1/sql/query with Bearer auth and parse the data array.
5. Provide results and follow-up query suggestions when helpful.

## References

- Read `references/laminar-query-api.md` for endpoint details, auth headers, request/response shape, table list, and query patterns.
