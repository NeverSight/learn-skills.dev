---
name: altinity-expert-clickhouse-caches
description: Analyze ClickHouse cache systems including mark cache, uncompressed cache, and query cache. Use for cache hit ratio issues and cache tuning.
---

# Cache Analysis and Tuning

Analyze ClickHouse cache systems: mark cache, uncompressed cache, query cache, and compiled expression cache.

---

## Diagnostics

Run all queries from the file checks.sql and analyze the results.

---

## Cache Sizing Recommendations

| Cache | Typical Size | Notes |
|-------|-------------|-------|
| Mark Cache | 5-10% of RAM | Higher if random access patterns |
| Uncompressed | 0 (disabled) or 5-10% | Enable only for specific workloads |
| Query Cache | 1-5GB | For repeated identical queries |
| Compiled Expression | 128MB-1GB | Higher for complex expressions |

---

## Problem Investigation

### Poor Mark Cache Hit Ratio

**Possible causes:**
1. Cache too small for working set
2. Queries scan many different tables
3. Many small queries to cold data

### Cache Too Large

If mark cache > 15% RAM:

**Solutions:**
- Reduce `index_granularity` for tables with excessive marks
- Drop unused tables
- Reduce `mark_cache_size` setting

---

## Cross-Module Triggers

| Finding | Load Module | Reason |
|---------|-------------|--------|
| Cache using too much RAM | `altinity-expert-clickhouse-memory` | Overall memory analysis |
| Poor hit ratio + high disk IO | `altinity-expert-clickhouse-storage` | Disk bottleneck |
| Many marks per table | `altinity-expert-clickhouse-schema` | Consider index_granularity tuning |
| Query cache misses | `altinity-expert-clickhouse-reporting` | Query pattern analysis |

---

## Settings Reference

| Setting | Scope | Notes |
|---------|-------|-------|
| `mark_cache_size` | Server | Global mark cache limit |
| `uncompressed_cache_size` | Server | Set to 0 to disable |
| `use_uncompressed_cache` | Query | Enable per-query |
| `query_cache_max_size` | Server | Query result cache |
| `use_query_cache` | Query | Enable per-query |