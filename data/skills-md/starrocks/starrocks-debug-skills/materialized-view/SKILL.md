---
name: materialized-view
description: "Use when async materialized views are failing to refresh, timing out, becoming inactive, or query rewrite is not triggering. Covers refresh OOM (spill-to-disk), timeout tuning, MV reactivation, staleness tolerance for query rewrite, sync MV hit verification via EXPLAIN, FE restart impact on refresh schedules, and S3 rate limiting during refresh."
version: 2.0.0
category: materialized-view
keywords:
- MV refresh
- MV timeout
- MV inactive
- query rewrite
- sync MV
- async MV
tools:
- sort
related_cases:
- case-012-mv-refresh-failures
---

# Materialized View Troubleshooting

Investigation guide for async MV refresh failures, refresh timeouts, MV inactivation,
query rewrite failures, and sync MV optimization.

Five root causes account for the vast majority of cases:

- **Cause A** — refresh OOM (memory exhaustion during materialization)
- **Cause B** — refresh timeout (SQL takes longer than configured limit)
- **Cause C** — MV inactive (base table schema change or manual deactivation)
- **Cause D** — query rewrite not used (structural mismatch, staleness, or disabled)
- **Cause E** — schedule persistence issue (FE restart breaks scheduler timing)

---

## Metric Taxonomy — Read This First

Before using any metrics, understand the three observability layers:

### MV state observability

**`SHOW MATERIALIZED VIEWS`** — primary MV health check:

| Field | Meaning |
|---|---|
| `is_active` | Whether the MV is active (true = can refresh and rewrite) |
| `last_refresh_state` | State of the last refresh: SUCCESS, FAILED, RUNNING |
| `last_refresh_error_message` | Error detail when `last_refresh_state = FAILED` |
| `last_refresh_time` | Timestamp of the last completed refresh |
| `last_refresh_duration_ms` | Duration of the last refresh in milliseconds |
| `inactive_reason` | Why the MV was deactivated (schema change, explicit call) |
| `refresh_type` | ASYNC / MANUAL / SCHEDULED |
| `next_refresh_time` | Next scheduled refresh (for scheduled MVs) |

### Refresh task observability

```sql
-- Refresh history with error details
SELECT task_name, state, error_message, start_time, finish_time,
       TIMESTAMPDIFF(SECOND, start_time, finish_time) AS duration_sec
FROM information_schema.task_runs
WHERE task_name LIKE 'mv-%'
ORDER BY start_time DESC LIMIT 20;

-- Running refresh tasks right now
SELECT * FROM information_schema.task_runs
WHERE state = 'RUNNING';
```

### Resource consumption observability

```sql
-- Queries running during refresh (to identify resource contention)
SHOW PROC '/current_queries' \G

-- Analyze a specific refresh profile (get profile_id from task_runs)
ANALYZE PROFILE FROM '<profile_id>';
```

### Rewrite verification

```sql
-- Check if a query uses MV rewrite
EXPLAIN LOGICAL SELECT ...;
-- Look for "SCAN [mv_name]" in output — if the base table name appears instead, rewrite did not fire

-- Trace why rewrite was not used (v3.2+)
TRACE LOGS MV SELECT ...;
TRACE REASON MV SELECT ...;

-- Sync MV: check via EXPLAIN
EXPLAIN SELECT ... FROM <table>;
-- Look for "Rollup: <mv_name>" and "PREAGGREGATION: ON"
```

### How to retrieve metrics

**Option 1 — SQL (primary method)**

```sql
-- Overall MV health
SHOW MATERIALIZED VIEWS;

-- Refresh history
SELECT * FROM information_schema.task_runs
WHERE task_name = 'mv-<mv_id>' \G

-- Resource usage during refresh
SHOW PROC '/current_queries' \G
```

**Option 2 — FE log grep**

```bash
# Refresh start/end events
grep "Start refresh materialized view\|End refresh materialized view" fe.log | tail -30

# Refresh failures
grep "refresh.*failed\|MV.*inactive\|refresh.*timeout" fe.log | tail -30

# Scheduler timing issues
grep "initialDelay\|scheduleRefresh\|task_runs" fe.log | tail -30
```

**Default HTTP ports**: FE = 8030. Profile UI at `http://<fe_ip>:8030`.

---

**Key rules for interpretation**:

1. `is_active = false` blocks both refresh and query rewrite — restoring active state is always the first step when queries are not rewriting.
2. `last_refresh_state = FAILED` with `last_refresh_error_message` containing `OOM` → Cause A. Containing `timeout` → Cause B. Containing schema change → Cause C.
3. If `last_refresh_time` diverges from `now()` by more than `mv_rewrite_staleness_second`, the MV will not be used for rewrite unless `query_rewrite_consistency = LOOSE`.
4. `TRACE LOGS MV` output contains `MV_REWRITE_FAIL_REASON` — read this before assuming structural incompatibility.

---

## MV Issue Reference

| Phenomenon | Root cause | Quick confirmation |
|---|---|---|
| Refresh ends quickly with FAILED state | OOM (Cause A) | `last_refresh_error_message` contains OOM or heap detail; `fe.gc.log` shows Full GC |
| Refresh hangs then fails | Timeout (Cause B) | `last_refresh_error_message` contains timeout; `task_runs.duration_sec` > `insert_timeout` value |
| MV not refreshing at all | Inactive (Cause C) | `is_active = false` in `SHOW MATERIALIZED VIEWS`; check `inactive_reason` |
| EXPLAIN shows base table scan despite MV existing | Rewrite not used (Cause D) | `TRACE LOGS MV` shows `MV_REWRITE_FAIL_REASON`; or MV is stale / inactive |
| Scheduled refresh stops firing after FE restart | Schedule persistence (Cause E) | Compare `next_refresh_time` vs current time; FE log shows wrong `initialDelay` |

---

## Phase 1 — Confirm MV Issue Type

### Step 1.1 — Check overall MV state

```sql
-- Run on FE (any node, but Leader gives authoritative state)
SHOW MATERIALIZED VIEWS;
```

Classify based on output:

| `is_active` | `last_refresh_state` | Classification |
|---|---|---|
| false | any | Cause C — MV inactive (fix active state first) |
| true | FAILED | Cause A or B (read error message to distinguish) |
| true | SUCCESS | Cause D — check query rewrite |
| true | SUCCESS | Cause E — check schedule timing |
| true | RUNNING for > expected time | Cause B — refresh running too long |

### Step 1.2 — Check refresh history

```sql
SELECT task_name, state, error_message,
       start_time, finish_time,
       TIMESTAMPDIFF(SECOND, start_time, finish_time) AS duration_sec
FROM information_schema.task_runs
WHERE task_name LIKE 'mv-%'
ORDER BY start_time DESC LIMIT 10;
```

- `error_message` contains `Out of memory` or `java.lang.OutOfMemoryError` → **Cause A**
- `error_message` contains `timeout` or `insert_timeout` → **Cause B**
- `state = FAILED`, `error_message` contains `schema` → **Cause C**
- All states SUCCESS but query plan shows base table → **Cause D**
- No task runs scheduled despite past refresh interval → **Cause E**

---

## Phase 2 — Investigate Root Cause

### Step 2.1 — For FAILED refreshes (Cause A or B)

```bash
# Check FE GC log for OOM evidence
grep "Full GC\|OutOfMemory" fe.gc.log | tail -20

# Check FE heap usage around refresh time
grep "heap" fe.log | grep -A2 "Start refresh" | tail -20
```

```sql
-- Profile the last failed refresh (if profile_id is available)
ANALYZE PROFILE FROM '<profile_id>';
-- Look for: which operator consumed the most memory
-- Look for: which stage timed out
```

### Step 2.2 — For inactive MV (Cause C)

```sql
SHOW MATERIALIZED VIEWS;
-- Check: inactive_reason column
-- Common values: "base table schema changed", "manually set inactive"
```

### Step 2.3 — For rewrite miss (Cause D)

```sql
-- Confirm MV is active and fresh
SHOW MATERIALIZED VIEWS;
-- is_active = true AND last_refresh_time is recent

-- Trace the rewrite decision
TRACE LOGS MV SELECT ...;
-- Look for MV_REWRITE_FAIL_REASON in output
```

Common rewrite blockers:
- Nested aggregation in query not supported by MV structure
- Join + aggregation combination not covered by MV
- Query filter column not included in MV SELECT
- MV data is stale beyond staleness tolerance
- `query_rewrite_consistency = DISABLE` set at session level

### Step 2.4 — For schedule persistence (Cause E)

```bash
# Check if FE was recently restarted
grep "FE started\|system start" fe.log | tail -5

# Check initialDelay calculation in scheduler
grep "initialDelay\|scheduleRefresh" fe.log | tail -20
```

```sql
-- Check next_refresh_time vs now
SELECT mv_name, last_refresh_time, next_refresh_time,
       TIMESTAMPDIFF(MINUTE, now(), next_refresh_time) AS minutes_until_refresh
FROM information_schema.materialized_views;
-- If minutes_until_refresh is very large (e.g., > 1440 min for a daily MV) → schedule broken
```

---

## Phase 3 — Take Action by Cause

### Cause A — Refresh OOM

**Step A-1: Enable spill to disk (immediate, no restart)**

```sql
ALTER MATERIALIZED VIEW <mv_name> SET ('session.enable_spill' = 'true');
```

**Step A-2: Increase FE heap (requires FE restart)**

```bash
# In fe.conf or JVM args
-Xmx16g   # increase from default (e.g., 8g)
```

**Step A-3: Reduce per-refresh data volume**

```sql
-- Partition-by-partition refresh (incremental)
ALTER MATERIALIZED VIEW <mv_name>
REFRESH ASYNC START('2024-01-01 00:00:00') EVERY (INTERVAL 1 HOUR);

-- Or set partition batch size
ALTER MATERIALIZED VIEW <mv_name>
SET ('mv_refresh_partition_batch_num' = '1');
```

**Step A-4: Emergency stop if OOM is cascading**

```sql
CANCEL REFRESH MATERIALIZED VIEW <mv_name>;
-- Or deactivate until fixed:
ALTER MATERIALIZED VIEW <mv_name> INACTIVE;
```

---

### Cause B — Refresh timeout

**Step B-1: Extend timeout (dynamic)**

```sql
-- v3.2+: default 1 hour; pre-v3.2: default 5 min
ALTER MATERIALIZED VIEW <mv_name>
SET ('session.insert_timeout' = '7200');   -- seconds
```

**Step B-2: Profile the refresh SQL**

```sql
-- Get the refresh SQL from MV definition
SHOW CREATE MATERIALIZED VIEW <mv_name>;

-- Run the SQL manually with profiling to find the bottleneck
SET enable_profile = true;
-- Execute the refresh SQL
-- Then: SHOW PROC '/current_queries' for profile_id
ANALYZE PROFILE FROM '<profile_id>';
```

**Step B-3: Add a resource group for heavy refreshes**

```sql
-- Create a dedicated resource group
CREATE RESOURCE GROUP rg_mv
TO (role='root')
WITH (
  'cpu_core_limit' = '4',
  'mem_limit' = '0.3',
  'big_query_cpu_second_limit' = '0',
  'big_query_scan_rows_limit' = '0',
  'big_query_mem_limit' = '0',
  'type' = 'normal'
);

-- Assign to MV
ALTER MATERIALIZED VIEW <mv_name>
SET ('resource_group' = 'rg_mv');
```

Note: default resource group `default_mv_wg` has `cpu_core_limit=1` which throttles large refreshes.

---

### Cause C — MV inactive

**Step C-1: Restore active state**

```sql
ALTER MATERIALIZED VIEW <mv_name> ACTIVE;
```

**Step C-2: If `ACTIVE` fails (schema incompatibility)**

```sql
-- Check what changed in the base table
SHOW CREATE TABLE <base_table>;
SHOW CREATE MATERIALIZED VIEW <mv_name>;

-- Drop and recreate the MV with updated definition
DROP MATERIALIZED VIEW <mv_name>;
CREATE MATERIALIZED VIEW <mv_name>
REFRESH ASYNC
AS <updated_select>;
```

**Step C-3: Prevent future deactivation from schema changes**

When altering base tables that have MVs, test the MV definition against the new schema before applying the DDL. After any base table `ALTER TABLE`, immediately run:

```sql
SHOW MATERIALIZED VIEWS;
-- Check is_active; reactivate if needed
```

---

### Cause D — Query rewrite not used

**Step D-1: Check staleness tolerance**

```sql
-- Allow rewrite even when MV is slightly stale
ALTER MATERIALIZED VIEW <mv_name>
SET ('query_rewrite_consistency' = 'LOOSE');

-- Or set allowed staleness window in seconds
ALTER MATERIALIZED VIEW <mv_name>
SET ('mv_rewrite_staleness_second' = '300');
```

**Step D-2: Check session-level rewrite settings**

```sql
-- Ensure rewrite is enabled at session level
SET enable_materialized_view_rewrite = true;
SET materialized_view_rewrite_mode = 'default';  -- or 'force'
```

**Step D-3: Trace and fix structural mismatches**

```sql
TRACE LOGS MV SELECT ...;
-- Read MV_REWRITE_FAIL_REASON in output
```

Common structural fixes:
- `Nested aggregation unsupported`: flatten the MV definition; avoid `SELECT SUM(SUM(x))` patterns
- `Join + aggregation unsupported`: separate the join and aggregation, or use a flat MV
- `Filter column not in MV SELECT`: add the filter column to MV SELECT

**Step D-4: Verify sync MV hit**

```sql
EXPLAIN SELECT ... FROM <table>;
-- Must see: "Rollup: <mv_name>" and "PREAGGREGATION: ON"
-- If see base table name → sync MV not hitting
```

For sync MVs, supported aggregations: `sum`, `min`, `max`, `count`, `bitmap_union`, `hll_union`.
Sync MVs on Duplicate/Aggregate models only — not Primary Key model.

---

### Cause E — Schedule persistence issue

**Step E-1: Confirm the broken schedule**

```sql
SELECT mv_name, last_refresh_time, next_refresh_time
FROM information_schema.materialized_views;
-- next_refresh_time far in the future despite short refresh interval → broken
```

**Step E-2: Fix by re-triggering schedule**

```sql
-- Manual refresh to unblock immediately
REFRESH MATERIALIZED VIEW <mv_name>;

-- Reset the schedule definition
ALTER MATERIALIZED VIEW <mv_name>
REFRESH ASYNC START(NOW()) EVERY (INTERVAL 1 HOUR);
```

**Step E-3: Increase task runs concurrency if queue is backed up**

```sql
ADMIN SET FRONTEND CONFIG ("task_runs_concurrency" = "8");
```

**Step E-4: Mitigation for FE restart impact**

- Ensure FE uptime covers at least one full scheduling cycle before the next restart
- Stagger refresh schedules across MVs to reduce post-restart thundering herd
- Monitor `next_refresh_time` after each FE restart

---

## Phase 4 — Verify Recovery

```sql
-- Primary signal: MV active and refreshing successfully
SHOW MATERIALIZED VIEWS;
-- is_active = true
-- last_refresh_state = SUCCESS
-- last_refresh_time is recent (within expected refresh interval)

-- Confirm query rewrite is working
EXPLAIN LOGICAL SELECT ...;
-- Must show "SCAN [mv_name]", not the base table name

-- Confirm refresh completing within timeout
SELECT task_name, state, TIMESTAMPDIFF(SECOND, start_time, finish_time) AS duration_sec
FROM information_schema.task_runs
WHERE task_name LIKE 'mv-%'
ORDER BY start_time DESC LIMIT 5;
-- state = SUCCESS and duration_sec within expected range

-- Confirm no OOM or timeout errors in recent runs
SELECT task_name, state, error_message
FROM information_schema.task_runs
WHERE task_name LIKE 'mv-%'
  AND state = 'FAILED'
ORDER BY start_time DESC LIMIT 5;
-- Should return 0 rows
```

Target state:
- `is_active = true` for all operational MVs
- `last_refresh_state = SUCCESS`
- Query plans show MV scan nodes, not base table scan nodes
- Refresh duration trending stable or decreasing

---

## Key Configuration Parameters

### MV Properties (per-MV, set via ALTER MATERIALIZED VIEW ... SET)

| Property | Default | Description | Dynamic |
|---|---|---|---|
| `session.insert_timeout` | 3600 (v3.2+) / 300 (pre-v3.2) | Refresh SQL timeout in seconds | Yes |
| `session.enable_spill` | false | Enable spill to disk during refresh | Yes |
| `query_rewrite_consistency` | `CHECKED` | Rewrite staleness policy: DISABLE / CHECKED / LOOSE | Yes |
| `mv_rewrite_staleness_second` | 0 | Allowed staleness in seconds for rewrite (0 = no tolerance) | Yes |
| `resource_group` | `default_mv_wg` | Resource group for refresh tasks | Yes |
| `mv_refresh_partition_batch_num` | all | Partitions refreshed per batch | Yes |
| `partition_refresh_number` | -1 (all) | Number of partitions to refresh per task | Yes |

### Session Variables (affect both queries and refresh SQL)

| Variable | Default | Description | Dynamic |
|---|---|---|---|
| `enable_materialized_view_rewrite` | true | Enable/disable MV query rewrite globally | Yes |
| `materialized_view_rewrite_mode` | `default` | `default` / `force` — force mode errors if rewrite fails | Yes |
| `enable_spill` | false | Enable spill during query (including MV refresh) | Yes |

### FE System Configuration

| Parameter | Default | Description | Dynamic |
|---|---|---|---|
| `task_runs_concurrency` | 4 | Max concurrent async task runs (MV refresh tasks) | Yes |
| `mv_refresh_concurrent_num` | system-dependent | Cap parallel MV refresh workers | Yes |
| `enable_mv_refresh_query_rewrite` | true | Allow query rewrite during MV refresh | Yes |

---

## 4. Sync Materialized View Optimization

### Supported Scenarios

Sync materialized views (on Duplicate/Aggregate models only) support:

- **Pre-aggregation**: `sum`, `min`, `max`, `count`, `bitmap_union`, `hll_union`.
- **Column reorder**: change sort key prefix for different query patterns.

### Verifying MV Hit

```sql
-- Check via EXPLAIN
EXPLAIN SELECT ... FROM table;
-- Look for "Rollup: <mv_name>" (not the base table name)
-- Check PREAGGREGATION: ON = storage layer returns pre-aggregated data
```

In Profile, check `OLAP_SCAN_NODE`:

- `Rollup: <mv_name>` confirms MV was used.
- Compare `BytesRead`, `RowsRead` before/after MV creation.

### Performance Impact Example

SSB 1TB benchmark: `SELECT date, SUM(qty) FROM lineorder_flat GROUP BY date`.

- Without MV: 27.61s (scanned 6.79GB, 1.4B rows).
- With MV: 0.96s (scanned 488KB, 100K rows) — about 29x speedup.

---

## 5. Operational Pitfalls

### Non-deterministic functions in MV definitions

Functions like `current_date()` cause invalid rewrite plans. Replace with stable expressions
or recreate the MV with a constant cutoff column.

### FE restart impact on schedule persistence

A daily FE restart can break MV schedule persistence — the scheduler re-registers tasks
with the wrong `initialDelay`, skipping the next scheduled run. Mitigation:

- Ensure FE uptime covers at least one full scheduling cycle.
- Increase `task_runs_concurrency` when async task queue grows large.
- Track this as a known limitation pending persistent scheduler metadata.

### S3 rate limiting during refresh

Symptom: refresh fails with `503: Please reduce your request rate`.
See `skills/06-shared-data.md` for rate-limit mitigation (`num_partitioned_prefix`, etc.).

---

## Common Issues

| Issue | Cause | Fix |
|---|---|---|
| Refresh times out at default | Pre-v3.2 default of 5 min | Set `session.insert_timeout` (Cause B) |
| MV inactivated unexpectedly | Base table schema change | `ALTER MATERIALIZED VIEW ... ACTIVE` (Cause C) |
| Query rewrite not used | Nested agg, missing filter columns, staleness | Set `LOOSE` consistency; trace with `TRACE LOGS MV` (Cause D) |
| Refresh hits OOM | Spill not enabled | Enable spill to disk (Cause A) |
| Scheduled refresh stops after FE restart | Wrong `initialDelay` calculation | Reset schedule; increase `task_runs_concurrency` (Cause E) |
| `SHOW TABLETS` fails inside MV refresh | Ephemeral role context missing | Run as a stable user/role |
| Refresh too slow | Default resource group limits CPU to 1 core | Assign custom resource group with higher CPU limit |

---

## Related Cases

- `case-012-mv-refresh-failures` — multi-cause MV refresh investigation including S3 rate limiting

---

## Causal Chains

### Chain 1: MV Refresh Write Lock Blocks Concurrent Queries

```
MV refresh task starts and acquires DB-level write lock
  ↓ observable: FE log "[MV] Start refresh materialized view <mv_name>" timestamp; jstack shows MVRefreshTask holding Database.rwLock write lock
Concurrent read queries attempt to acquire read lock on same DB
  ↓ observable: jstack shows query threads BLOCKED on Database.rwLock.readLock()
Query execution delayed until write lock released
  ↓ observable: SHOW PROC '/current_queries' shows queries in PENDING state during refresh window
Query P99 latency spikes during refresh window
```
Users report intermittent slowness correlated with MV refresh schedule.

**Trigger conditions**: MV refresh SQL is long-running; high concurrent query load on the same database; short refresh interval.

**Break point**: Reduce refresh frequency or schedule during low-traffic windows; upgrade to async refresh mode that releases write lock earlier.

---

### Chain 2: Refresh Task OOM → MV Data Staleness → Silent Wrong Results

```
MV refresh executes complex aggregation SQL; FE heap exhausted during intermediate result materialization
  ↓ observable: fe.gc.log shows consecutive Full GC events; heap near -Xmx limit
Refresh task killed by OOM; job marked failed
  ↓ observable: SHOW MATERIALIZED VIEWS shows last_refresh_state = FAILED; last_refresh_error_message contains OOM detail
MV data timestamp frozen at last successful refresh
  ↓ observable: last_refresh_time diverges from current time; MV data growing stale
Query rewrite uses stale MV data without explicit error
  ↓ observable: query results return outdated aggregates; EXPLAIN shows OlapScanNode on MV table
```
Users see stale query results without explicit error; data staleness grows until manual intervention.

**Trigger conditions**: MV refresh SQL involves multi-table joins or large window functions; FE `-Xmx` undersized.

**Break point**: Increase FE heap; set `mv_refresh_partition_batch_num` to limit per-batch data volume; switch to incremental partition refresh.

---

### Chain 3: Frequent Refresh + Metadata Ops → FE GC Cascade → Refresh Timeout Loop

```
MV refresh tasks triggered at high frequency (e.g., every few minutes) across many MVs
  ↓ observable: FE log shows rapid succession of "Start refresh" / "End refresh" log lines
Each refresh creates metadata objects accumulating in FE heap
  ↓ observable: FE memory profile shows MV-related heap objects not GC'd between cycles
FE Full GC triggered repeatedly
  ↓ observable: fe.gc.log shows Full GC pauses >5s; FE unresponsive during GC
In-flight refresh task misses heartbeat during GC pause; task fails
  ↓ observable: FE log "refresh task timeout" or "refresh job failed: heartbeat lost"
Failed refresh queues more retries; each creating more metadata objects → feedback loop
  ↓ observable: SHOW MATERIALIZED VIEWS shows multiple MVs with FAILED state accumulating
```
Cascade failure: FE GC blocks all DDL/DML; MVs stop refreshing; query rewrite degrades to base table scan.

**Trigger conditions**: Large number of MVs (>20) with short refresh intervals; FE heap not tuned for metadata-heavy workloads.

**Break point**: Stagger MV refresh schedules; increase FE heap and enable G1GC; set `mv_refresh_concurrent_num` to cap parallel workers.

---

## Resources

- [Troubleshooting Asynchronous Materialized Views](https://docs.starrocks.io/docs/using_starrocks/async_mv/troubleshooting_asynchronous_materialized_views/)
