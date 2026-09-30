---
name: high-concurrency
description: "Use when optimizing for high-QPS (thousands of queries/sec) workloads or diagnosing throughput plateaus and latency spikes under load. Covers pipeline_dop=1 tuning, connection pooling (HikariCP/Druid), PreparedStatement plan caching, query cache hit-rate analysis, PK model point-query optimization (short-circuit scan, persistent index), and detecting session-level timeout overrides that cause memory volatility."
version: 2.0.0
category: high-concurrency
keywords:
- high QPS
- connection pool
- PreparedStatement
- query cache
- pipeline_dop
- primary key
- short circuit
tools:
- find
related_cases:
- case-015-memory-volatility
---

# High-Concurrency Best Practices

Investigation and tuning guide for high-QPS workloads: data modeling, primary-key
optimization, query cache, pipeline parallelism, connection pooling, and emergency
load disabling.

Five root causes account for most high-concurrency performance problems:

- **Cause A** — Connection pool exhausted (too many connections, no client pool)
- **Cause B** — FE planning CPU saturation (complex queries, no plan cache)
- **Cause C** — `pipeline_dop` too high for short queries (scheduling overhead)
- **Cause D** — Session-level timeout override causing memory volatility
- **Cause E** — Query cache not effective (low hit ratio, wrong workload type)

---

## Metric Taxonomy — Read This First

Before tuning, establish a baseline measurement of the current state.

### FE connection metrics

| Metric / Observable | Meaning |
|---|---|
| Connection count approaching `qe_max_connection` | Connection layer bottleneck |
| `SHOW PROC '/current_queries'` count | Active concurrent queries right now |
| FE log `Reach limit of connections` | Connection limit hit — new clients rejected |

**How to retrieve**:

```bash
# Check qe_max_connection setting
grep "qe_max_connection" fe/conf/fe.conf
# Default: 1024

# Count active connections via SQL
# (run on FE that is not itself overloaded)
SELECT COUNT(*) FROM information_schema.processlist;

# Or check current queries
# SHOW PROC '/current_queries';
```

### Query cache metrics

| Metric | Meaning |
|---|---|
| `starrocks_be_query_cache_hit_ratio` | Cache hit ratio (0–1); <0.1 = cache not effective |
| `query_cache_capacity` (BE config) | Total cache size allocated per BE |

**How to retrieve**:

```bash
# Per-BE cache hit ratio (Prometheus metric)
curl -s "http://<be_host>:<be_http_port>/metrics" | grep query_cache_hit_ratio

# Detailed cache stats per BE
curl -s "http://<be_host>:<be_http_port>/api/query_cache/stat"
```

### Pipeline parallelism metrics

| Metric / Observable | Meaning |
|---|---|
| `pipeline_dop` current session value | Degree of parallelism per query fragment |
| `SHOW PROC '/current_queries'` → many queries in `RUNNING` | Queries competing for pipeline threads |

**How to retrieve**:

```bash
# Check current global pipeline_dop
mysql -e "SHOW VARIABLES LIKE 'pipeline_dop';"

# Check per-session overrides in audit log
grep "pipeline_dop" fe/log/fe.audit.log | tail -20
```

### Audit log metrics

| Metric | Meaning |
|---|---|
| `QueryTime` distribution | Latency profile — P50/P99 separation indicates outliers |
| `MemCostBytes` per query | Memory per query; outliers indicate unbounded queries |
| `ScanRows` per query | Data volume per query; large values indicate full scans |

**How to retrieve**:

```bash
# QueryTime distribution (last hour)
grep "$(date +'%Y-%m-%d %H')" fe/log/fe.audit.log \
  | awk -F'QueryTime=' '{print $2}' | cut -d'|' -f1 \
  | sort -n | awk 'BEGIN{c=0} {a[c++]=$1} END{
      print "P50:", a[int(c*0.50)], "P99:", a[int(c*0.99)], "Max:", a[c-1]
    }'

# MemCostBytes outliers
grep "$(date +'%Y-%m-%d')" fe/log/fe.audit.log \
  | awk -F'MemCostBytes=' '{if(NF>1) print $2}' | cut -d'|' -f1 \
  | sort -rn | head -10

# Find queries with session-level query_timeout override
grep "query_timeout" fe/log/fe.log | grep "set.*session" | tail -20
```

---

**Key rules for interpretation**:

1. If `pipeline_dop` is auto (0) on a system with many vCPUs, short queries spawn too many threads per query — the scheduling overhead exceeds query execution time. Always set `pipeline_dop = 1` for high-QPS OLTP workloads.
2. Query cache hit ratio below 10% means the workload is not cache-friendly — common with high-cardinality `GROUP BY` or pre-shuffle aggregation. Do not allocate more cache capacity; fix the workload pattern.
3. Connection exhaustion (`qe_max_connection`) is a hard limit — new clients receive immediate rejection. This is different from query queue (which waits). Check both.
4. `MemCostBytes` outliers in audit log that do not appear in the query latency P99 are likely queries with session-level timeout overrides that run for hours without being killed.

---

## High-Concurrency Tuning Reference

| Scenario | Key signal | Recommended action |
|---|---|---|
| QPS plateau below expected throughput | `pipeline_dop` > 1; short query profile shows scheduler overhead | `SET GLOBAL pipeline_dop = 1` |
| Connection exhausted; clients rejected | `qe_max_connection` reached; FE log `Reach limit of connections` | Increase `qe_max_connection`; enforce client-side connection pooling |
| Cache hit ratio < 10% | `starrocks_be_query_cache_hit_ratio` < 0.1 | Analyze workload — fix high-cardinality GROUP BY; consider PreparedStatement for plan reuse |
| Memory volatility; BEs OOM | `MemCostBytes` outliers in audit; long-running queries; session-level overrides | Kill offending queries; add resource group timeout governance |
| FE CPU near 100%; queries stuck in Planning | `SHOW PROC '/current_queries'` shows large count in Planning state | Enable PreparedStatement (`useServerPrepStmts=true`); scale FE; stagger dashboard refreshes |
| Connection storm on cold start | No connection pool configured | Deploy HikariCP or Druid; set pool min/max to expected concurrency |

---

## Phase 1 — Identify Bottleneck Type

### Step 1.1 — Determine where queries are stuck

```sql
-- Check query states
SHOW PROC '/current_queries';
-- Key columns: QueryState (Planning/Running/etc.), ElapsedTime, MemUsageBytes

-- If many in Planning state → Cause B (FE planning CPU)
-- If many in Running state with short QueryTime expected → Cause C (pipeline_dop)
-- If connection errors before reaching query state → Cause A (connection pool)
```

```bash
# Check FE CPU
top -b -n 1 | grep java
# If FE java process near 100% CPU → Cause B

# Check connection limit
grep "qe_max_connection" fe/conf/fe.conf
mysql -e "SELECT COUNT(*) FROM information_schema.processlist;"
# If count near qe_max_connection → Cause A
```

**Bottleneck signal → root cause**:

| Pattern | Points toward |
|---|---|
| Clients get `too many connections` error | **Cause A** — connection pool exhausted |
| `SHOW PROC '/current_queries'` shows many in Planning; FE CPU high | **Cause B** — FE planning CPU saturation |
| QPS plateaus; short queries slow; `pipeline_dop` > 1 | **Cause C** — pipeline_dop overhead |
| BE memory drops sharply; OOM restarts; outlier queries in audit | **Cause D** — session-level timeout override |
| Cache hit ratio < 10% despite high QPS | **Cause E** — query cache not effective |

---

## Phase 2 — Measure Current State

### Step 2.1 — Baseline connection utilization

```sql
-- Active query count
SELECT COUNT(*) FROM information_schema.processlist;

-- Query state distribution
SELECT STATE, COUNT(*) FROM information_schema.processlist GROUP BY STATE;
```

### Step 2.2 — Baseline cache effectiveness

```bash
# Check cache hit ratio on each BE
for be in <be1> <be2> <be3>; do
    echo "=== $be ==="
    curl -s "http://$be:8040/api/query_cache/stat" | python3 -m json.tool 2>/dev/null | grep -E "hit|miss|ratio"
done
```

### Step 2.3 — Baseline audit log latency

```bash
# P99 QueryTime for the last hour
grep "$(date +'%Y-%m-%d %H')" fe/log/fe.audit.log \
  | awk -F'QueryTime=' 'NF>1{print $2}' | cut -d'|' -f1 \
  | sort -n > /tmp/qtimes.txt
wc -l /tmp/qtimes.txt
# P99 line number = 0.99 * total_count
```

---

## Phase 3 — Take Action by Cause

### Cause A — Connection Pool Exhausted

**Confirm all match**:
- FE log shows `Reach limit of connections` or clients receive `too many connections`
- `SELECT COUNT(*) FROM information_schema.processlist` is near or at `qe_max_connection`
- Client applications do not use connection pooling (verified by connection creation patterns in audit)

**Mechanism**: FE enforces `qe_max_connection` as a hard limit on simultaneous MySQL protocol connections. Without client-side connection pooling, each request opens and closes a TCP connection, which both exhausts the FE limit and adds round-trip overhead. Under bursty load (dashboard refreshes, batch job starts), the FE connection queue fills instantly.

**Actions**:

```sql
-- Step A-1: Increase connection limit (FE config, requires restart)
-- Edit fe/conf/fe.conf: qe_max_connection = 4096

-- Step A-2: Increase per-user connection limit
ALTER USER 'bi_user' SET PROPERTIES ('max_user_connections' = '500');

-- Step A-3: Enable query queue to absorb bursts
ADMIN SET FRONTEND CONFIG ("enable_query_queue" = "true");
ADMIN SET FRONTEND CONFIG ("query_queue_max_queued_queries" = "1000");
```

```
# Step A-4: Client-side — mandatory connection pooling
# HikariCP example:
# hikari.minimumIdle=10
# hikari.maximumPoolSize=50
# hikari.connectionTimeout=30000

# Step A-5: JDBC URL for PreparedStatement plan caching
# jdbc:mysql://<fe_ip>:9030/<db>?useServerPrepStmts=true
```

```sql
-- Step A-6: FE load balancing — deploy 3+ FEs behind TCP load balancer
-- Nginx: stream proxy to port 9030 across all FE hosts
```

→ **Go to Phase 4: Verify Recovery**

---

### Cause B — FE Planning CPU Saturation

**Confirm all match**:
- `SHOW PROC '/current_queries'` shows large number in `Planning` state
- `top` on FE host shows `java` process consuming near 100% CPU
- Queries are complex (many joins, views, or large partition counts)

**Mechanism**: FE planner runs CBO (cost-based optimizer), partition pruning, and statistics lookups for every query. With high concurrent QPS of non-trivial queries, planner threads compete for CPU. PreparedStatement plan caching avoids re-planning identical query shapes, which is the primary mitigation.

**Actions**:

```bash
# Step B-1: Enable PreparedStatement plan caching via JDBC
# Add to JDBC URL:
# useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=256
```

```sql
-- Step B-2: Reduce planning cost for complex views
-- Replace complex views with materialized views for frequent query patterns

-- Step B-3: Reduce statistics collection concurrency during peak hours
ADMIN SET FRONTEND CONFIG ("statistic_collect_concurrency" = "1");
-- Or disable temporarily:
ADMIN SET FRONTEND CONFIG ("enable_statistic_collect" = "false");
```

```bash
# Step B-4: Scale FE horizontally
# Add another FE behind the load balancer for additional planner capacity
# Add 3+ FEs; use Nginx/HAProxy TCP load balancer on port 9030
```

→ **Go to Phase 4: Verify Recovery**

---

### Cause C — High pipeline_dop for Short Queries

**Confirm all match**:
- `SHOW VARIABLES LIKE 'pipeline_dop'` shows 0 (auto) or >1
- Queries are short (sub-second expected) but actual latency is much higher
- System QPS is lower than expected given available CPU headroom

**Mechanism**: When `pipeline_dop = 0` (auto), StarRocks sets parallelism to `vCPUs/2`. For a 32-vCPU BE, each query spawns 16 pipeline threads. With 100 concurrent short queries, the OS scheduler must context-switch among 1600 threads — the overhead exceeds actual computation time. Setting `pipeline_dop = 1` reduces each query to one thread, allowing the OS to schedule them efficiently.

**Actions**:

```sql
-- Step C-1: Set pipeline_dop = 1 globally (critical for high-QPS OLTP)
SET GLOBAL pipeline_dop = 1;

-- Step C-2: For mixed workloads (some OLAP, some OLTP)
-- Use resource groups with per-group pipeline_dop override
-- Or use query hints for OLAP queries:
SELECT /*+ SET_VAR(pipeline_dop=4) */ * FROM large_table ...;
```

```sql
-- Step C-3: Enable short-circuit read for PK point queries
SET GLOBAL enable_short_circuit = true;
-- Verify: EXPLAIN shows "Short Circuit Scan: true" for PK lookup queries

-- Step C-4: Confirm version compatibility
-- pipeline_dop = 1 effective from v2.3+
-- v2.4+: parallel_fragment_exec_instance_num forced to 1; pipeline_dop = 0 auto-sets to vCPUs/2
```

→ **Go to Phase 4: Verify Recovery**

---

### Cause D — Session-Level Timeout Override Causing Memory Volatility

**Confirm all match**:
- BE memory drops sharply or BEs OOM-restart
- `MemCostBytes` outliers in audit log — queries using GB of memory
- FE log shows `query_timeout` set at session level by specific clients
- Global `query_timeout` policy appears correct but individual queries run for hours

**Mechanism**: A client sets `query_timeout = 30000` (30000 seconds = 8+ hours) at session level, overriding the global `query_timeout`. Queries from this client run unbounded, accumulating memory across BEs. When multiple such queries coexist, cumulative memory exceeds BE capacity, triggering OOM kills. The global policy appears correct in `SHOW VARIABLES` but session-level overrides are invisible unless explicitly searched.

**Actions**:

```bash
# Step D-1: Find session-level timeout overrides in FE log
grep "query_timeout" fe/log/fe.log | grep -v "global" | tail -20

# Step D-2: Find long-running queries in audit log
awk -F'QueryTime=' 'NF>1{qt=$2+0; if(qt>300000) print}' fe/log/fe.audit.log | tail -20
# QueryTime > 300000ms = >5 min
```

```sql
-- Step D-3: Identify and kill the offending queries
SHOW PROC '/current_queries';
-- Filter: ElapsedTime > expected threshold
KILL QUERY <query_id>;

-- Step D-4: Enforce timeout governance via resource groups
CREATE RESOURCE GROUP rg_governed
TO (user='offending_user')
PROPERTIES (
    "cpu_core_limit" = "4",
    "mem_limit" = "20%",
    "big_query_cpu_second_limit" = "300",
    "big_query_mem_limit" = "5368709120"  -- 5GB
);

-- Step D-5: Add SQL blacklist for queries without WHERE (optional)
ADMIN SET FRONTEND CONFIG ("enable_sql_blacklist" = "true");
ADD SQLBLACKLIST "select .* from [^w]*;";
```

→ **Go to Phase 4: Verify Recovery**

---

### Cause E — Query Cache Not Effective

**Confirm all match**:
- `starrocks_be_query_cache_hit_ratio` < 0.1 (less than 10% hit rate)
- `enable_query_cache = true` is set but QPS / latency have not improved
- Workload uses high-cardinality `GROUP BY` or involves Shuffle before aggregation

**Mechanism**: Query cache stores intermediate aggregation results per tablet. It only works when the aggregation can be partitioned by tablet without a prior shuffle. High-cardinality `GROUP BY` (e.g., GROUP BY user_id with 100M distinct users) produces too many unique cache keys to achieve meaningful reuse. Similarly, if a query requires data from multiple tablets for the same aggregation result, results cannot be cached per-tablet.

**Actions**:

```sql
-- Step E-1: Verify cache is enabled and configured
SHOW VARIABLES LIKE 'enable_query_cache';
-- Check BE config:
-- query_cache_capacity (default 512MB per BE)
-- query_cache_entry_max_bytes
-- query_cache_entry_max_rows

-- Step E-2: Analyze EXPLAIN for cache eligibility
EXPLAIN SELECT ... FROM tbl GROUP BY low_cardinality_col;
-- Look for: QueryCache: Enabled in EXPLAIN output
-- If not present → workload is not cache-eligible

-- Step E-3: For cache-ineligible workloads — use PreparedStatement instead
-- PreparedStatement caches execution plans, reducing FE planning overhead
-- jdbc:mysql://<fe_ip>:9030/<db>?useServerPrepStmts=true

-- Step E-4: Optimize data model for cache eligibility
-- Use low-cardinality GROUP BY columns (e.g., date, region, category)
-- Move high-cardinality filters to WHERE clause rather than GROUP BY
-- Use materialized views for frequently repeated aggregation patterns
```

```bash
# Step E-5: Tune cache size if hit rate is >30% but eviction rate is high
# Check eviction stats:
curl -s "http://<be_host>:8040/api/query_cache/stat" | python3 -m json.tool

# Increase cache size in be.conf (requires restart):
# query_cache_capacity = 1073741824  # 1GB
```

→ **Go to Phase 4: Verify Recovery**

---

## Phase 4 — Verify Recovery

```sql
-- Verify connection utilization is below limit
SELECT COUNT(*) FROM information_schema.processlist;
-- Should be well below qe_max_connection

-- Verify query state distribution is healthy
SELECT STATE, COUNT(*) FROM information_schema.processlist GROUP BY STATE;
-- Should show no accumulation in Planning state

-- Verify pipeline_dop setting took effect
SHOW VARIABLES LIKE 'pipeline_dop';
-- Should show the configured value (e.g., 1)
```

```bash
# Verify cache hit ratio improved (Cause E)
curl -s "http://<be_host>:8040/api/query_cache/stat" | python3 -m json.tool | grep ratio

# Verify no long-running outlier queries (Cause D)
grep "$(date +'%Y-%m-%d %H')" fe/log/fe.audit.log \
  | awk -F'QueryTime=' 'NF>1{qt=$2+0; if(qt>300000) print}' | wc -l
# Should be 0 or very low

# Verify FE CPU is no longer saturated (Cause B)
top -b -n 1 | grep java
# FE java process CPU% should be well below 100%
```

**QPS validation**: Run a load test with your expected concurrency. Compare:
- P99 latency before vs. after
- Max QPS before plateau vs. after
- Connection error rate (should be 0)

---

## High-Concurrency Key Config Parameters

| Parameter | Default | Description | Dynamic |
|---|---|---|---|
| `qe_max_connection` | 1024 | Max simultaneous MySQL connections per FE | No (fe.conf restart) |
| `max_user_connections` | 100 | Per-user connection limit | Yes (`ALTER USER SET PROPERTIES`) |
| `pipeline_dop` | 0 (auto) | Pipeline parallelism per fragment; set to 1 for high-QPS OLTP | Yes (`SET GLOBAL`) |
| `enable_query_cache` | false | Enable per-tablet query result caching | Yes (`SET GLOBAL`) |
| `query_cache_capacity` | 536870912 (512MB) | Cache size per BE node | No (be.conf restart) |
| `query_cache_entry_max_bytes` | 4194304 (4MB) | Max size of a single cache entry | No (be.conf restart) |
| `query_cache_entry_max_rows` | 409600 | Max rows in a single cache entry | No (be.conf restart) |
| `enable_query_queue` | false | Enable query queuing to absorb bursts | Yes (FE ADMIN SET) |
| `query_queue_max_queued_queries` | 1024 | Max queries waiting in queue | Yes (FE ADMIN SET) |
| `enable_short_circuit` | false | Short-circuit scan for PK point queries | Yes (`SET GLOBAL`) |
| `enable_persistent_index` | false | Persistent PK index on SSD (PK tables) | No (table property at creation) |
| `statistic_collect_concurrency` | 3 | Concurrent statistics collection jobs | Yes (FE ADMIN SET) |
| `disable_load_job` | false | Emergency: stop all import jobs | Yes (FE ADMIN SET) |

---

## Data Modeling for High QPS

**Partition + Sort Key + Bucket Key synergy:**

- **Partition key**: always use a time column; ensures partition pruning via `WHERE event_time >= ...`.
- **Sort key**: put highest-frequency equality filter columns first (e.g., `user_id`).
- **Bucket key**: use the query's ID column as bucket key for bucket pruning
  (`WHERE order_id = 12345` scans only one tablet).

**Primary Key Model Optimizations:**

- **Persistent primary key index** (v3.1+): `"enable_persistent_index" = "true"` — moves index from memory to SSD.
- **Hybrid row-column storage**: `"storage_type" = "column_with_row"` — adds row store for single-row point queries.
- **Short-circuit read**: `SET enable_short_circuit = true` — bypasses execution engine for PK point queries.
  Verify with `EXPLAIN`: look for `Short Circuit Scan: true`.

---

## Causal Chains

### Chain 1: QPS Spike → Connection Pool Exhausted → Latency P99 Collapses

```
Client-side QPS spikes (batch job start, traffic surge)
  ↓ observable: FE metric connection_total rising rapidly toward qe_max_connection threshold
FE connection pool reaches qe_max_connection limit
  ↓ observable: FE log "Reach limit of connections" or "too many connections" rejection messages
New connection requests queued or immediately rejected by FE
  ↓ observable: client-side connection errors; SHOW PROC '/current_queries' count at or near max
Queued connections accumulate; per-connection wait time rises
  ↓ observable: client P99 latency metric rises steeply; application connection timeout logs appear
```
Clients receive connection refused or timeout; throughput collapses despite FE/BE having available CPU headroom.

**Trigger conditions**: `qe_max_connection` too low; connection pooling disabled or undersized on client; sudden batch workload launch without connection ramping.

**Break point**: Increase `qe_max_connection` in `fe.conf`; enforce client-side connection pooling; use query queuing (`enable_query_queue=true`) to absorb bursts.

---

### Chain 2: Concurrent Small Queries → FE CPU Saturated → Planning Backlog

```
High volume of small queries arrives concurrently (BI dashboard refresh)
  ↓ observable: SHOW PROC '/current_queries' shows large number of queries in Planning state
FE planner threads (CBO, partition pruning, stats lookup) compete for CPU
  ↓ observable: top on FE host shows Java process consuming near 100% CPU across all cores
FE plan generation latency increases
  ↓ observable: FE log shows increased time between query receipt and "Begin to execute" line
Query throughput drops; planning backlog grows
  ↓ observable: SHOW PROC '/current_queries' count continuously growing; arrival rate exceeds completion rate
```
Overall throughput drops; latency rises even for trivially simple queries; FE becomes the bottleneck.

**Trigger conditions**: FE host under-powered relative to concurrent query load; statistics collection running concurrently with peak traffic; complex views increase per-query planning cost.

**Break point**: Scale FE to higher-core host; enable query plan caching for repeated patterns; stagger BI dashboard refresh schedules.

---

### Chain 3: Large Runtime Filter Broadcast → Network Burst → Packet Loss → Query Retry

```
Large join query triggers runtime filter (RF) generation at build side
  ↓ observable: EXPLAIN shows RUNTIME FILTER broadcast to all probe-side BEs; RF size estimate is large
All BE nodes simultaneously receive large RF payload
  ↓ observable: network monitoring shows synchronized burst of inbound traffic on all BE hosts at join build completion
Burst exceeds switch buffer capacity; packets dropped
  ↓ observable: netstat -s | grep retransmit shows spike in TCP retransmits on BE hosts during query
BE nodes detect RF delivery timeout; RF is disabled or fragment retries
  ↓ observable: BE log "runtime filter timeout" or "skip runtime filter due to delivery failure"; execution time increases
Retried fragments generate additional traffic, amplifying the burst
  ↓ observable: SHOW PROC '/current_queries' shows elevated execution time and retry count for same query
```
Query takes significantly longer; cluster-wide synchronized network bursts coincide with large join queries.

**Trigger conditions**: Many BEs (>20) with a single large RF; network switch insufficient buffer for synchronized multicast; RF size threshold not tuned.

**Break point**: Tune `runtime_filter_max_in_num` and `runtime_filter_size_limit` to cap RF payload; enable RF pipeline mode to stagger delivery.

---

## Related Cases

- `case-015-memory-volatility` — session-level timeout override case study

---

## Resources

- [Query cache documentation](https://docs.starrocks.io/docs/using_starrocks/query_cache/)
- [Primary key model documentation](https://docs.starrocks.io/docs/table_design/table_types/primary_key_table/)
