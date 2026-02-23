---
name: altinity-expert-clickhouse-merges
description: Diagnose ClickHouse merge performance, part backlog, and 'too many parts' errors. Use for merge issues and part management problems.
---


## Diagnostics

Run all queries from `checks.sql` (cluster-wide) one by one and produce a decision-ready report.

## Triage Order (Mandatory)

1. Check **current active merges** from `system.merges`.
2. Check **merge success/failure trend** from `system.part_log`.
3. Check **table-level status** (`merge_ok`, `merge_failed`, last success/failure).
4. Check **merge reason + algorithm** (`merge_reason`, `merge_algorithm`).
5. Check **merge RAM now + historical peak RAM** (`system.merges.memory_usage`, `system.part_log.peak_memory_usage`).
6. Check **part-count offenders** with split:
   - `database = 'system'`
   - `database != 'system'`
7. Check **relevant settings**, including TTL merge concurrency.


## Decision Rules

Use one of these final verdicts explicitly:

- `PROVED`: cluster-wide merge stop (no successful merges in the selected window).
- `DECLINED`: cluster-wide stop is false.
- `PARTIAL`: merges are blocked for specific table(s) while others still merge.

Additional rules:
- If some tables still have successful merges in same timeframe, do **not** report global merge stop.
- If a target table has `merge_ok = 0` with repeated `MEMORY_LIMIT_EXCEEDED`, report table-level block.
- If merges are 100% `Horizontal`, state that planner selected horizontal merges (do not say vertical is disabled unless settings prove it).
- If max part count is driven by `system.*` tables, call out alert-source mismatch to avoid misattribution to business tables.

---

## Problem-Specific Investigation

### "Too Many Parts" Investigation

For a specific table, run ad-hoc checks (time-bound and limited):

```sql
select
    toStartOfMinute(event_time) as minute,
    countIf(event_type = 'NewPart') as new_parts,
    countIf(event_type = 'MergeParts') as merges,
    countIf(event_type = 'MergeParts') - countIf(event_type = 'NewPart') as net_reduction
from system.part_log
where database = '{database}'
  and table = '{table}'
  and event_time > now() - interval 1 hour
group by minute
order by minute desc
limit 60
```

If `net_reduction` is negative consistently, inserts outpace merges.

## TTL merge pressure and merge-size settings snapshot

Check system.merge_tree_settings if modified
Suggest changing (reducing or increasing) in case of a problem as remediation.

- max_parts_to_merge_at_once
- max_bytes_to_merge_at_max_space_in_pool 
- max_bytes_to_merge_at_min_space_in_pool 
- enable_vertical_merge_algorithm 
- vertical_merge_algorithm_min_rows_to_activate 
- vertical_merge_algorithm_min_columns_to_activate 
- max_number_of_merges_with_ttl_in_pool 
- max_replicated_merges_with_ttl_in_queue 
- parts_to_delay_insert 
- parts_to_throw_insert 


## Structural Fix Guidance (When Settings Are Not Enough)

Call out anti-patterns explicitly:
- Single hot partition (`partition_id='all'`)
- Heavy `TTL ... GROUP BY ... SET ...` on a hot ingestion table
- Persistent large horizontal merge attempts with OOM failures

Recommended long-term direction:
- Add time-based partitioning
- Move heavy rollup logic from TTL path to MV/batch table
- Keep base-table TTL simple (delete-oriented)


## Ad-Hoc Query Guidelines

### Required Safeguards

```sql
-- Always include LIMIT
limit 100

-- Always time-bound historical queries
where event_time >= now() - interval 24 hour

-- For part_log, always filter event_type
where event_type in ('NewPart', 'MergeParts', 'MutatePart')
```

### Avoid
- `select * from system.part_log`
- Unbounded scans on `*_log` tables
- Large joins in-context (aggregate in SQL)

---

## Cross-Module Triggers

| Finding | Load Module | Reason |
|---------|-------------|--------|
| High memory during merges / OOM | `altinity-expert-clickhouse-memory` | Memory limits and pressure |
| Slow merges + normal disk | `altinity-expert-clickhouse-schema` | ORDER BY/partitioning anti-patterns |
| Slow merges + high disk IO | `altinity-expert-clickhouse-storage` | Storage bottleneck |
| Merges blocked by mutations | `altinity-expert-clickhouse-mutations` | Mutation backlog |
| Replication lag + merge issues | `altinity-expert-clickhouse-replication` | Queue/replica bottlenecks |

---

## Final Report Sections (Mandatory)

1. Environment header
2. Global vs table-specific merge status
3. Current and peak merge RAM
4. Merge reason and merge algorithm findings
5. Max-part offenders (`system` vs non-`system`)
6. Current settings and recommended deltas
7. Immediate mitigation and structural remediation
