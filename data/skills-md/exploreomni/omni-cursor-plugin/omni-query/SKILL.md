---
name: omni-query
description: Run queries against Omni Analytics' semantic layer using the REST API, interpret results, and chain queries for multi-step analysis. Use this skill whenever someone wants to query data through Omni, run a report, get metrics, pull numbers, analyze data, ask "how many", "what's the trend", "show me the data", retrieve dashboard query results, or perform any data retrieval through Omni's query engine. Also use when someone wants to programmatically extract data from an existing Omni dashboard or workbook.
---

# Omni Query

Run queries against Omni's semantic layer via the REST API. Omni translates field selections into optimized SQL — you specify what you want (dimensions, measures, filters), not how to get it.

> **Tip**: Use `omni-model-explorer` first if you don't know the available topics and fields.

## Prerequisites

```bash
export OMNI_BASE_URL="https://yourorg.omniapp.co"
export OMNI_API_KEY="your-api-key"
```

You also need a **model ID** and knowledge of available **topics and fields**.

## API Discovery

When unsure whether an endpoint or parameter exists, fetch the OpenAPI spec:

```bash
curl -L "$OMNI_BASE_URL/openapi.json" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

Use this to verify endpoints, available parameters, and request/response schemas before making calls.

## Running a Query

### Basic Query

```bash
curl -L -X POST "$OMNI_BASE_URL/api/v1/query/run" \
  -H "Authorization: Bearer $OMNI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "modelId": "your-model-id",
      "table": "order_items",
      "fields": [
        "order_items.created_at[month]",
        "order_items.total_revenue"
      ],
      "limit": 100,
      "join_paths_from_topic_name": "order_items"
    }
  }'
```

### Query Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `modelId` | Yes | UUID of the Omni model |
| `table` | Yes | Base view name (the `FROM` clause) |
| `fields` | Yes | Array of `view.field_name` references |
| `join_paths_from_topic_name` | Recommended | Topic for join resolution |
| `limit` | No | Row limit (default 1000, max 50000, `null` for unlimited) |
| `sorts` | No | Array of sort objects |
| `filters` | No | Filter object |
| `pivots` | No | Array of field names to pivot on |

### Field Naming

Fields use `view_name.field_name`. Date fields support timeframe brackets:

```
users.created_at[date]      — Daily
users.created_at[week]      — Weekly
users.created_at[month]     — Monthly
users.created_at[quarter]   — Quarterly
users.created_at[year]      — Yearly
```

### Sorts

```json
"sorts": [
  { "column_name": "order_items.total_revenue", "sort_descending": true }
]
```

### Filters

```json
"filters": {
  "order_items.created_at": "last 90 days",
  "order_items.status": "complete",
  "users.state": "California,New York"
}
```

Expressions: `"last 90 days"`, `"this quarter"`, `"2024-01-01 to 2024-12-31"`, `"not California"`, `"null"`, `"not null"`, `">100"`, `"between 10 and 100"`, `"contains sales"`, `"starts with A"`. See [references/filter-expressions.md](references/filter-expressions.md) for the complete expression syntax reference.

### Pivots

```json
{
  "query": {
    "fields": ["order_items.created_at[month]", "order_items.status", "order_items.count"],
    "pivots": ["order_items.status"],
    "join_paths_from_topic_name": "order_items"
  }
}
```

## Handling Results

Default response: base64-encoded Apache Arrow table. Arrow results are binary — you cannot parse individual row data from the raw response. To verify a query returned data, check `summary.row_count` in the response.

For human-readable results, request CSV instead:

```json
{ "query": { ... }, "resultType": "csv" }
```

### Decoding Arrow Results

```python
import base64, pyarrow as pa
arrow_bytes = base64.b64decode(response["data"])
reader = pa.ipc.open_stream(arrow_bytes)
df = reader.read_all().to_pandas()
```

### Long-Running Queries

If the response includes `remaining_job_ids`, poll until complete:

```bash
curl -L -X POST "$OMNI_BASE_URL/api/v1/query/wait" \
  -H "Authorization: Bearer $OMNI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "jobIds": ["job-id-1", "job-id-2"] }'
```

## Running Queries from Dashboards

Extract and re-run queries powering existing dashboards:

```bash
# Get all queries from a dashboard
curl -L "$OMNI_BASE_URL/api/v1/documents/{dashboardId}/queries" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Run as a specific user
{ "query": { ... }, "userId": "user-uuid-here" }

# Skip cache (valid values: disabled, normal, refresh, refresh_all)
{ "query": { ... }, "cache": "refresh" }
```

## Multi-Step Analysis Pattern

For complex analysis, chain queries:

1. **Broad query** — understand the shape of the data
2. **Inspect results** — identify interesting segments or patterns
3. **Focused follow-ups** — filter based on findings
4. **Synthesize** — combine results into a narrative

## Common Query Patterns

**Time Series**: fields + date dimension + ascending sort + date filter

**Top N**: fields + metric + descending sort + limit

**Aggregation with Breakdown**: multiple dimensions + multiple measures + descending sort by key metric

## Known Bugs

- **`IS_NOT_NULL` filter generates `IS NULL`** (reported Omni bug) — workaround: invert the filter logic or use the base view to apply the filter differently.
- **Boolean filters may be silently dropped** when a `pivots` array is present — if boolean filters aren't applying, remove the pivot and test again.

## Linking to Results

Queries are ephemeral — there is no persistent URL for a query result. To give the user a shareable link:

- **For existing dashboards**: `{OMNI_BASE_URL}/dashboards/{identifier}` (the `identifier` comes from the document API response)
- **For new analysis**: Create a document via `omni-content-builder` with the query as a `queryPresentation`, then share `{OMNI_BASE_URL}/dashboards/{identifier}`

## Docs Reference

- [Query API](https://docs.omni.co/api/queries.md) · [Running Document Queries](https://docs.omni.co/guides/run-document-queries.md) · [Querying Documentation](https://docs.omni.co/analyze-explore/querying.md) · [Filter Syntax](https://docs.omni.co/modeling/filters.md)

## Related Skills

- **omni-model-explorer** — discover fields and topics before querying
- **omni-content-explorer** — find dashboards whose queries you can extract
- **omni-content-builder** — turn query results into dashboards
