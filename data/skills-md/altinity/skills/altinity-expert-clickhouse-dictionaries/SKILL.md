---
name: altinity-expert-clickhouse-dictionaries
description: Analyze ClickHouse external dictionaries including configuration, memory usage, reload status, and performance. Use for dictionary issues and load failures.
---

# Dictionary Diagnostics

Analyze external dictionaries: configuration, memory usage, reload status, and performance.

---

## Diagnostics

Run all queries from the file checks.sql and analyze the results.

---

## Dictionary Reload Operations

### Force Reload (syntax reference)

```sql
-- SYSTEM RELOAD DICTIONARY {database}.{name}
-- SYSTEM RELOAD DICTIONARIES
```

### Check Reload Result for Specific Dictionary

```sql
-- Check reload result
select
    name,
    status,
    loading_start_time,
    loading_duration,
    last_exception
from system.dictionaries
where name = '{dictionary_name}'
```

---

## Best Practices

### Dictionary Sizing Guidelines

| Elements | Recommended Type |
|----------|-----------------|
| < 100K | Flat (if sequential keys) |
| 100K - 10M | Hashed |
| > 10M | Consider partitioning or cache |
| Complex keys | ComplexKeyHashed |
| Sparse access | Cache with SSD |

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| High memory | Too many elements | Use cache type, filter data |
| Slow reload | Large source table | Add filters, use delta updates |
| Stale data | Source unreachable | Check connectivity, add retry |
| Failed status | Source query fails | Check source table/query |

---

## Cross-Module Triggers

| Finding | Load Module | Reason |
|---------|-------------|--------|
| High memory usage | `altinity-expert-clickhouse-memory` | Overall memory analysis |
| Load failures | `altinity-expert-clickhouse-overview` | Error summary + routing |
| Source connectivity | `altinity-expert-clickhouse-logs` | Log investigation |
| Slow lookups | `altinity-expert-clickhouse-reporting` | Query optimization |

---

## Settings Reference

| Setting | Notes |
|---------|-------|
| `dictionaries_lazy_load` | Load on first access vs startup |
| `dictionary_load_wait_timeout_ms` | Wait time for lazy load |
| `max_dictionary_num_to_warn` | Warning threshold |