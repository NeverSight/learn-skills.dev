---
name: altinity-expert-clickhouse-index-analysis
description: Analyze whether ClickHouse indexes (PRIMARY KEY, ORDER BY, skipping indexes, projections) are being used effectively for actual query patterns. Use when investigating index effectiveness, ORDER BY key design, query-to-index alignment, or when queries scan more data than expected.
---


## Diagnostics

Run all queries from the file checks.sql and analyze the results.

---

## Deep Dive Queries (Placeholder-Based)

### EXPLAIN Index Usage for Specific Query

```sql
EXPLAIN indexes = 1
{query_without_format}
```

**Look for:**
- `PrimaryKey` condition should not be `true` (means no filtering)
- `Granules: X/Y` ratio shows selectivity (low X/Y = good)
- `Skip` indexes should reduce parts/granules further

### Column Cardinality Analysis

```sql
SELECT 
    {columns} APPLY uniq
FROM {database}.{table}
WHERE {time_column} > now() - INTERVAL {days} DAY
```

**Optimal ORDER BY ordering:** Low cardinality columns first, high cardinality last.

### Query Pattern WHERE Columns Extraction

```sql
WITH
    any(query) AS q,
    arrayJoin(extractAll(query, '\\b(?:PRE)?WHERE\\s+(.*?)\\s+(?:GROUP BY|ORDER BY|UNION|SETTINGS|FORMAT|$)')) AS w,
    arrayFilter(x -> (position(w, extract(x, '\\.(`[^`]+`|[^\\.]+)$')) > 0), columns) AS c,
    arrayJoin(c) AS c2
SELECT
    c2,
    count() AS usage_count
FROM system.query_log
WHERE event_time >= now() - toIntervalDay({days})
  AND arrayExists(x -> x LIKE '%{table}%', tables)
  AND query ILIKE 'SELECT%'
  AND type = 'QueryFinish'
GROUP BY c2
ORDER BY usage_count DESC
FORMAT PrettyCompactMonoBlock
```

### Normalized WHERE Clause Patterns

```sql
WITH
    arrayJoin(extractAll(normalizeQuery(query), '\\b(?:PRE)?WHERE\\s+(.*?)\\s+(?:GROUP BY|ORDER BY|UNION|SETTINGS|FORMAT|$)')) AS w
SELECT
    w AS where_pattern,
    count() AS frequency
FROM system.query_log
WHERE event_time >= now() - toIntervalDay({days})
  AND arrayExists(x -> x LIKE '%{table}%', tables)
  AND query ILIKE 'SELECT%'
  AND type = 'QueryFinish'
GROUP BY w
ORDER BY frequency DESC
LIMIT 20
```

### Granule Selectivity from Query Log

```sql
SELECT
    query_id,
    normalized_query_hash,
    selected_parts,
    selected_marks,
    read_rows,
    round(read_rows / nullIf(selected_marks, 0)) AS rows_per_mark,
    query_duration_ms,
    formatReadableSize(read_bytes) AS read_bytes
FROM system.query_log
WHERE event_time >= now() - toIntervalDay({days})
  AND arrayExists(x -> x LIKE '%{table}%', tables)
  AND query ILIKE 'SELECT%'
  AND type = 'QueryFinish'
ORDER BY selected_marks DESC
LIMIT 20
```

**High `selected_marks` / total marks = poor index utilization.**

---

## Analysis Workflow

### Step 1: Check Current Indexes

```sql
-- Table structure with ORDER BY, PRIMARY KEY, indexes
SHOW CREATE TABLE {database}.{table}
```

```sql
-- Skipping indexes
SELECT name, type, expr, granularity
FROM system.data_skipping_indices
WHERE database = '{database}' AND table = '{table}'
```

### Step 2: Extract Query Patterns

Run the WHERE column extraction and normalized pattern queries to understand:
- Which columns appear most frequently in WHERE clauses
- What condition combinations are common

### Step 3: Check Column Cardinalities

Compare cardinalities of columns in:
- Current ORDER BY key
- Frequently filtered columns from Step 2

### Step 4: Evaluate Index Alignment

| Query Pattern | Index Support | Action |
|---------------|---------------|--------|
| Filters on ORDER BY prefix | ✅ Good | None |
| Filters on non-ORDER BY cols | ⚠️ Skip index? | Add bloom_filter or projection |
| Time range + entity | ⚠️ Check order | Time in ORDER BY or partition? |
| High-cardinality first in ORDER BY | ❌ Bad | Reorder (low→high cardinality) |

---

## ORDER BY Design Guidelines

### Column Order Principles

1. **Lowest cardinality first** - maximizes granule skipping
2. **Most frequently filtered** - columns in WHERE should be in ORDER BY
3. **Time column considerations:**
   - If most queries filter on time ranges → include in ORDER BY (possibly with lower resolution like `toDate(ts)`)
   - If partition key handles time filtering → may not need in ORDER BY

### Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| High-cardinality UUID first | No granule skipping | Move after low-cardinality columns |
| DateTime64 microseconds first | Too granular | Use `toDate()` or `toStartOfHour()` |
| Column in WHERE not in ORDER BY | Full scan | Add to ORDER BY or create projection |
| Bloom filter on ORDER BY column | Redundant | Remove skip index |
| Time not in ORDER BY or partition | Range queries scan all | Add `toDate(ts)` to ORDER BY prefix |

### Cardinality Ordering Example

Given cardinalities:
- `entity_type`: 6
- `entity`: 18,588
- `cast_hash`: 335,620

**Recommended ORDER BY:** `(entity_type, entity, cast_hash, ...)`

---

## Skipping Index Guidelines

### When Skip Indexes Help

- Column NOT in ORDER BY
- Column values correlate with physical data order
- Low false-positive rate for the index type

### When Skip Indexes Don't Help

- Column already in ORDER BY prefix (use PRIMARY KEY instead)
- Column values randomly distributed (no correlation with ORDER BY)
- Very high cardinality with set/bloom_filter

