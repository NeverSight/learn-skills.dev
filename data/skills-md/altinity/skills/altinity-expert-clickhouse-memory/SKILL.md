---
name: altinity-expert-clickhouse-memory
description: Diagnose ClickHouse RAM usage, OOM errors, memory pressure, and allocation patterns. Use for memory-related issues and out-of-memory errors.
---

# Memory Usage and OOM Diagnostics

Diagnose RAM usage, memory pressure, OOM risks, and memory allocation patterns.

---

## Diagnostics

Run all queries from the file checks.sql and analyze the results.

---

## Problem Investigation

### High Memory from Aggregations

**Solutions:**
- Add `max_bytes_before_external_group_by`
- Use `max_threads` pragma to limit parallelism
- Restructure query to reduce group by cardinality

### High Memory from JOINs

**Solutions:**
- Use `max_bytes_in_join`
- Consider `join_algorithm = 'partial_merge'` or `'auto'`
- Ensure smaller table on right side

---

## Ad-Hoc Query Guidelines

### Required Safeguards
```sql
-- Always time-bound log queries
where event_date >= today() - 1

-- Limit results
limit 100
```

### Memory-Related Metrics
- `MemoryTracking` - current tracked memory
- `MemoryResident` - RSS
- `OSMemoryTotal`, `OSMemoryFreeWithoutCached` - system memory

---

## Cross-Module Triggers

| Finding | Load Module | Reason |
|---------|-------------|--------|
| High merge memory | `altinity-expert-clickhouse-merges` | Analyze merge patterns |
| Large dictionaries | `altinity-expert-clickhouse-dictionaries` | Dictionary optimization |
| Cache too large | `altinity-expert-clickhouse-caches` | Cache sizing |
| PK memory high | `altinity-expert-clickhouse-schema` | ORDER BY optimization |
| Query OOMs | `altinity-expert-clickhouse-reporting` | Query optimization |

---

## Settings Reference

| Setting | Scope | Notes |
|---------|-------|-------|
| `max_memory_usage` | Query | Per-query limit |
| `max_memory_usage_for_user` | User | Per-user aggregate |
| `max_server_memory_usage` | Server | Global limit |
| `max_server_memory_usage_to_ram_ratio` | Server | Auto-limit as % of RAM |
| `max_bytes_before_external_group_by` | Query | Spill aggregation to disk |
| `max_bytes_in_join` | Query | Spill join to disk |
