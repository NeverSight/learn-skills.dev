---
name: altinity-expert-clickhouse-storage
description: Diagnose ClickHouse disk usage, compression efficiency, part sizes, and storage bottlenecks. Use for disk space issues and slow IO.
---

# Storage and Disk Usage Analysis

Diagnose disk usage, compression efficiency, part sizes, and storage bottlenecks.

---

## Diagnostics

Run all queries from the file checks.sql and analyze the results.

---

## Ad-Hoc Query Guidelines

### Required Safeguards
```sql
-- Always limit results
limit 100

-- For part_log
where event_date >= today() - 1
```

### Key Tables
- `system.disks` - Disk configuration
- `system.parts` - Part storage details
- `system.columns` - Column compression
- `system.storage_policies` - Tiered storage
- `system.detached_parts` - Orphaned parts

---

## Cross-Module Triggers

| Finding | Load Module | Reason |
|---------|-------------|--------|
| Poor compression | `altinity-expert-clickhouse-schema` | Codec recommendations |
| Many small parts | `altinity-expert-clickhouse-merges` | Merge backlog |
| High write IO | `altinity-expert-clickhouse-ingestion` | Batch sizing |
| System logs large | `altinity-expert-clickhouse-logs` | TTL configuration |
| Slow disk + merges | `altinity-expert-clickhouse-merges` | Merge optimization |

---

## Settings Reference

| Setting | Notes |
|---------|-------|
| `min_bytes_for_wide_part` | Threshold for Wide vs Compact parts |
| `min_rows_for_wide_part` | Row threshold for Wide parts |
| `max_bytes_to_merge_at_max_space_in_pool` | Max merge size |
| `prefer_not_to_merge` | Disable merges (emergency) |
