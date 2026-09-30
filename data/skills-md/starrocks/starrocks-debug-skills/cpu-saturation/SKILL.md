---
name: cpu-saturation
description: "Use as the first stop when a BE or FE host shows high CPU (elevated load average or top near 100%). Attributes CPU to the right workload — query pipeline, import flush/compression, compaction threads, background tasks, FE GC, or non-StarRocks processes — then hands off to the appropriate deep-dive skill (query/import/compaction/node). Does not resolve root causes directly; acts as a triage and attribution layer."
version: 2.0.0
category: cpu-saturation
keywords:
- CPU high
- CPU full
- CPU saturation
- high load
- load average
- perf top
- thread pool
- hot function
- system load
- process cpu
tools:
- top
- htop
- perf
- pidstat
- ps
- pstack
- curl
- grep
- python3
related_cases:
- case-014-scan-skew
- case-008-be-oom
---

# CPU Saturation Triage

Investigation guide for BE or machine CPU saturation. This skill focuses on **attribution**:
which process, which module, and which workload is consuming CPU.
After attribution, follow the referenced deep-dive skill for root-cause analysis.

---

## Metric Taxonomy — Read This First

Before using the decision tree, establish what the CPU is doing and which process owns it.

### OS-level CPU indicators

| Metric | Meaning |
|---|---|
| `us` (user) in `top` | User-space CPU — StarRocks computation, compression |
| `sy` (system) in `top` | Kernel CPU — system calls, IO, interrupts; high `sy` with `us` suggests thread overhead |
| `wa` (iowait) in `top` | CPU waiting for disk IO — not CPU saturation, disk bottleneck |
| `st` (steal) in `top` | CPU stolen by hypervisor (VM environments only) — noisy neighbor |
| Load average | Running + runnable threads; >vCPU count indicates oversubscription |

**How to retrieve**:

```bash
# Snapshot CPU breakdown
top -b -n 1 | head -5
# Output: %Cpu(s): 85.2 us,  8.3 sy,  0.0 ni,  3.1 id,  2.1 wa,  0.0 hi,  1.3 si,  0.0 st

# Per-process CPU (10-second sample)
pidstat -u 2 5

# Load average vs CPU count
uptime
# Load average: 64.2, 58.1, 52.3 → compare to: nproc (e.g., 32 CPUs → overloaded)
nproc
```

### BE-level CPU classification metrics (v3.4+)

| Metric | Meaning |
|---|---|
| `starrocks_be_cpu_task_query` | CPU time consumed by query pipeline threads |
| `starrocks_be_cpu_task_load` | CPU time consumed by import/flush threads |
| `starrocks_be_cpu_task_compaction` | CPU time consumed by compaction threads |
| `starrocks_be_cpu_task_clone` | CPU time consumed by tablet clone (rebalance) |

**How to retrieve**:

```bash
# Pull all BE CPU task metrics
curl -s "http://<be_host>:<be_http_port>/metrics" | grep "starrocks_be_cpu"

# Loop across all BEs to find the hotspot node
for be in <be1> <be2> <be3>; do
    echo "=== $be ==="
    curl -s "http://$be:8040/metrics" | grep "starrocks_be_cpu_task"
done
```

### FE-level CPU indicators

| Metric / Observable | Meaning |
|---|---|
| `java` process CPU in `top` | FE planning storm or GC pressure |
| GC CPU ratio from `fe.gc.log` | High GC CPU (>30% of elapsed) indicates heap pressure |
| `jstack` — many RUNNABLE threads in optimizer code | Query planning CPU storm |

**How to retrieve**:

```bash
# FE Java process CPU
top -b -n 1 | grep java

# Per-thread breakdown for FE JVM
top -Hp $(pgrep -f 'StarRocksFE\|fe.pid') | head -20
# Convert thread ID (decimal) to hex → cross-reference with jstack

# FE thread dump
jstack $(cat fe/bin/fe.pid) > /tmp/fe_jstack.log
grep -c "RUNNABLE" /tmp/fe_jstack.log
# High RUNNABLE count relative to vCPUs → planning storm or GC

# GC pressure
grep "GC" fe/log/fe.gc.log | tail -20
```

### Function-level CPU attribution

| Hot function prefix | Likely module |
|---|---|
| `starrocks::pipeline::` | Query pipeline executor |
| `starrocks::vectorized::` | Vectorized evaluation (scan / aggregate / join) |
| `starrocks::MemTable::` | Import memtable flush |
| `starrocks::Compaction::` | Compaction |
| `starrocks::SegmentWriter::` | Import segment write |
| `starrocks::lake::` | Shared-data operations |
| `snappy::` / `lz4::` / `zstd::` | Compression (flush or compaction) |
| `tcmalloc::` / `malloc` | Memory allocator contention |
| `starrocks::SchemaChange` | Schema change task |
| `starrocks::clone` | Tablet clone (rebalance) |

**How to retrieve**:

```bash
# Live hot functions (needs root or perf permission)
perf top -p $(pidof starrocks_be) -d 5
# Format: [overhead%]  [symbol_name]  [DSO]
# Focus on the top 5 functions; the prefix identifies the module

# Quick thread snapshot without perf
pstack $(pidof starrocks_be) > /tmp/be_pstack_$(date +%s).log
grep -oE "starrocks::[A-Za-z:]+" /tmp/be_pstack_$(date +%s).log | sort | uniq -c | sort -rn | head -20
```

---

**Key rules for interpretation**:

1. High `wa` (iowait) is NOT CPU saturation — it means CPU is idle waiting for disk. Diagnose with `iostat -x 1`, then follow compaction/SKILL.md or import/SKILL.md.
2. `starrocks_be_cpu_task_*` metrics are available only in v3.4+. On older versions, use `perf top` or `pidstat` for function-level attribution.
3. If ALL metrics degrade simultaneously (query + import + compaction), suspect a non-StarRocks process or hypervisor steal (`st` > 0) rather than a StarRocks-internal cause.
4. BE CPU metrics are per-BE — always identify the hotspot node first before applying cluster-wide changes.
5. FE GC CPU exceeding 30% of elapsed wall time is a separate problem from BE CPU saturation and requires heap/GC tuning, not thread reduction.

---

## CPU Saturation Signal Reference

| Observation combination | Most likely root cause | First checkpoint |
|---|---|---|
| `us` high; query latency up; import and compaction normal | Query-caused (Section 3a) | `SHOW PROC '/current_queries'`; `perf top` shows `vectorized::` |
| `us` high; import latency up; `perf top` shows `MemTable::` / `snappy::` | Import compression CPU (Section 3b) | `starrocks_be_cpu_task_load` metric |
| `us` high; compaction score dropping; query slow; `perf top` shows `Compaction::` | Compaction over-provisioned (Section 3c) | `starrocks_be_cpu_task_compaction`; reduce threads |
| ALL metrics degrade simultaneously; `st` > 0 in VM or non-StarRocks process in top | Non-StarRocks process or hypervisor steal (Section 5) | `ps aux --sort=-%cpu`; top `%st` |
| `java` process CPU high; FE queries stuck in Planning | FE planning storm or GC (Section 4) | `jstack` + `top -Hp`; `fe.gc.log` |
| `wa` (iowait) high; `us` normal | IO bottleneck, not CPU | `iostat -x 1`; see compaction/SKILL.md |
| `sy` high; many threads in `top -Hp` | Thread scheduling overhead | Reduce `pipeline_dop` or compaction thread count |
| `starrocks_be_cpu_task_clone` elevated | Tablet rebalance consuming CPU | `SHOW PROC '/cluster_balance'`; throttle clone |

---

## Triage Decision Tree

```
CPU saturation observed (load average high or top shows 100% on a node)
  │
  ├─ Step 1: Which process owns the CPU?
  │     → see Section 1
  │
  ├─ Process = starrocks_be
  │     └─ Step 2: Which BE module?
  │           → see Section 2
  │           ├─ Queries  → Section 3a + query/SKILL.md
  │           ├─ Import   → Section 3b + import/SKILL.md
  │           ├─ Compaction → Section 3c + compaction/SKILL.md
  │           └─ Background task / unknown → Section 3d
  │
  ├─ Process = java (FE)
  │     → FE Full GC or planning storm → Section 4 + node/SKILL.md
  │
  └─ Process = non-StarRocks (backup agent, kernel, etc.)
        → Section 5: OS-level attribution
```

---

## 1. Which Process Owns the CPU?

```bash
# Snapshot: top CPU consumers by process
top -b -n 1 | head -20

# More detail: per-thread breakdown for a single process
top -Hp $(pidof starrocks_be) | head -30

# Or use pidstat for sustained view
pidstat -u 2 10
```

| Observation | Next Step |
|---|---|
| `starrocks_be` is top consumer | Section 2 |
| `java` (FE) is top consumer | Section 4 |
| Other process (mysqld, rsync, python...) | Section 5 |
| `kworker` / `ksoftirqd` / kernel threads | Network interrupt or disk IRQ — check `sar -I ALL`, `iostat` |
| CPU `wa` (iowait) is high, not `us` | IO bottleneck, not CPU — see compaction/SKILL.md or import/SKILL.md |

---

## 2. Which BE Module?

### Step 2a: Quick workload inventory

```sql
-- Any active long-running queries?
SHOW PROC '/current_queries';
-- Look for QueryTime > 30s or MemUsageBytes > 1GB

-- Any active imports?
SELECT LABEL, STATE, PROGRESS, TYPE, LOAD_START_TIME
FROM information_schema.loads
WHERE STATE IN ('LOADING', 'PREPARED', 'PREPARED')
ORDER BY LOAD_START_TIME ASC;
```

### Step 2b: v3.4+ per-task-type CPU metrics

```bash
# CPU breakdown by task type (query / load / compaction / clone / schema change)
curl -s http://<BE_IP>:<BE_HTTP_PORT>/metrics | grep "starrocks_be_cpu"
```

Key metrics:
- `starrocks_be_cpu_task_query` — query pipeline CPU
- `starrocks_be_cpu_task_load` — import write CPU
- `starrocks_be_cpu_task_compaction` — compaction CPU
- `starrocks_be_cpu_task_clone` — tablet clone CPU

### Step 2c: perf top (function-level attribution)

```bash
# Live hot functions (needs root or perf permission)
perf top -p $(pidof starrocks_be) -d 5

# Or: pstack for a quick thread snapshot without perf
pstack $(pidof starrocks_be) > /tmp/be_pstack_$(date +%s).log
```

---

## 3a. Query-Caused CPU Saturation

**Confirm signals**:
- `starrocks_be_cpu_task_query` is the dominant rising metric
- `perf top` shows `starrocks::pipeline::` or `starrocks::vectorized::` as hot functions
- `SHOW PROC '/current_queries'` shows active queries with high `ScanRows` or `MemUsageBytes`

**Mechanism**: Query pipeline threads consume CPU proportional to data volume and operator complexity. Full-table scans (no predicate pushdown), large hash joins (hash table exceeds CPU cache), and high-cardinality aggregations all create sustained CPU pressure. Without resource group limits, a single large query can saturate all cores.

### Identify the Culprit SQL

```bash
# Find queries with highest scan rows in audit log (last 1 hour)
python3 scripts/analyze_logs.py "$(date -d '1 hour ago' '+%Y-%m-%d %H:%M:%S')" "$(date '+%Y-%m-%d %H:%M:%S')" "ScanRows" 5 fe.audit.log

# Or find by query execution time
grep 'QueryTime' fe.audit.log | awk -F'QueryTime=' '{print $2}' | cut -d'|' -f1 | sort -rn | head -10
```

### Profile the Query

```sql
SET is_report_success = true;
-- Re-run the query, then check profile:
-- http://<fe_ip>:8030 -> Queries -> Profile
```

**Common query CPU causes:**

| Symptom in Profile | Cause | Fix |
|---|---|---|
| `HASH_JOIN_NODE` dominates CPU | Large hash table probe | Force `[SHUFFLE]`; collect statistics |
| `AGGREGATE_NODE` dominates | High-cardinality aggregation | Check streaming pre-agg; add pre-filter |
| `OLAP_SCAN_NODE` CPU high, `BytesRead` huge | Full scan, no pushdown | Fix predicate type mismatch; add index |
| Many pipeline threads near 100% | Too many concurrent heavy queries | Add resource group; set `query_mem_limit` |

**→ Deep-dive: [query/SKILL.md](../query/SKILL.md)**

---

## 3b. Import-Caused CPU Saturation

**Confirm signals**:
- `starrocks_be_cpu_task_load` is the dominant elevated metric
- `perf top` shows `starrocks::MemTable::`, `starrocks::SegmentWriter::`, `snappy::`, or `zstd::` as hot functions
- Active imports visible via `information_schema.loads`

**Mechanism**: Import flush compresses memtable data before writing to disk segments. Compression (especially `zstd`) is CPU-intensive. With many concurrent stream loads, flush threads saturate available cores. Query pipeline threads then compete for CPU time slices, causing query latency to rise even without any change in query patterns.

### Identify the Import Load

```bash
# Check import thread CPU contribution
curl -s http://<BE_IP>:<BE_HTTP_PORT>/metrics | grep "starrocks_be_cpu_task_load"

# Check active imports
curl -s http://<BE_IP>:<BE_HTTP_PORT>/api/running_load | python3 -m json.tool 2>/dev/null
```

**Common import CPU causes:**

| Observation | Cause | Fix |
|---|---|---|
| Many concurrent stream loads | Memtable flush compression saturating cores | Reduce concurrency; use `lz4` instead of `zstd` for memtable |
| `flush_thread_num_per_store` threads all busy | Flush threads competing with query | Balance `flush_thread_num_per_store` vs query concurrency |
| `perf top` shows `snappy::` or `zstd::` hot | Compression CPU during flush | Tune `compression_type` for the table |
| Import CPU high, query CPU also high | Both competing for CPU | Use resource groups to cap import CPU |

**→ Deep-dive: [import/SKILL.md](../import/SKILL.md)**

---

## 3c. Compaction-Caused CPU Saturation

**Confirm signals**:
- `starrocks_be_cpu_task_compaction` is the dominant elevated metric
- `perf top` shows `starrocks::Compaction::` or `starrocks::SegmentWriter::` as hot functions
- Compaction score was recently high or threads were recently increased to clear a backlog

**Mechanism**: Compaction threads merge rowsets into larger segments, which involves decompressing source segments, merging sorted data, and recompressing the output. With `cumulative_compaction_num_threads_per_disk` set too high (e.g., to clear a historical backlog), compaction monopolizes CPU cores, reducing the time slices available to query pipeline threads.

### Confirm Compaction Is the Source

```bash
# Check compaction CPU contribution
curl -s http://<BE_IP>:<BE_HTTP_PORT>/metrics | grep "starrocks_be_cpu_task_compaction"

# Check compaction activity
curl -s http://<BE_IP>:<BE_HTTP_PORT>/api/compaction/show | python3 -m json.tool 2>/dev/null

# Check compaction score
SELECT tablet_id, num_rowset, num_segment, data_size
FROM information_schema.be_tablets
ORDER BY num_rowset DESC LIMIT 10;
```

**Common compaction CPU causes:**

| Observation | Cause | Fix |
|---|---|---|
| Compaction CPU consistently >30% of BE | Too many compaction threads | Reduce `cumulative_compaction_num_threads_per_disk` |
| CPU spike during compaction of large tablets | Base compaction of multi-GB rowset | Schedule off-peak; throttle base compaction IO |
| Compaction CPU high + query slow | CPU contention | Use resource groups or cgroup to cap compaction CPU |

```bash
# Temporarily reduce compaction threads (dynamic — no restart)
curl -XPOST "http://<BE_IP>:<BE_HTTP_PORT>/api/update_config?cumulative_compaction_num_threads_per_disk=1"

# Or via SQL (v3.2+, applies to all BEs)
# UPDATE information_schema.be_configs SET value = 1
# WHERE name = 'cumulative_compaction_num_threads_per_disk';
```

**→ Deep-dive: [compaction/SKILL.md](../compaction/SKILL.md)**

---

## 3d. Unknown Background Task

**Confirm signals**:
- `perf top` shows hot functions that don't match query/import/compaction prefixes
- `SHOW PROC '/current_queries'` shows no long-running queries
- `information_schema.loads` shows no active imports

**Mechanism**: Schema changes, tablet clone (rebalance), and memory allocator contention (`tcmalloc`) can cause sustained CPU usage without appearing in the query or import workload metrics. Clone operations copy tablet data between BEs during rebalancing; schema changes rebuild column segments. Both generate significant IO and CPU workload.

If `perf top` shows hot functions that don't match query/import/compaction prefixes:

```bash
# Check schema change tasks
SHOW ALTER TABLE COLUMN;

# Check clone tasks
SHOW PROC '/cluster_balance';

# Check routine load tasks
SHOW ROUTINE LOAD;

# Memory allocator contention (tcmalloc)
curl -s http://<BE_IP>:<BE_HTTP_PORT>/memz | head -30
```

| Hot function | Likely task | Action |
|---|---|---|
| `starrocks::SchemaChange` | Concurrent schema change | Pause or serialize schema changes |
| `starrocks::clone` | Tablet clone (rebalance) | Throttle clone tasks |
| `tcmalloc` / `malloc` | Memory allocator contention (many threads) | Check `brpc_num_threads`; reduce thread count |
| `starrocks::DictColumn` / `GlobalDictCache` | Low-cardinality dict build | Usually self-resolving; monitor |

---

## 4. FE (Java) CPU Saturation

**Confirm signals**:
- `top` shows `java` process (FE) in top CPU consumers
- `jstack` shows many RUNNABLE threads in CBO optimizer or statistics code
- `fe.gc.log` shows frequent Full GC events

**Mechanism**: FE Java process CPU saturation has two distinct causes: (1) query planning storm where many concurrent complex queries overwhelm CBO planner threads, and (2) Full GC where Java's garbage collector consumes CPU cleaning heap. Both appear as high `java` process CPU but have different jstack signatures.

```bash
# Identify hot Java threads
top -Hp $(pgrep -f 'StarRocksFE\|fe.pid') | head -20
# Convert thread ID to hex, then cross-reference jstack

jstack $(cat fe/bin/fe.pid) > /tmp/fe_jstack.log
# Look for threads in RUNNABLE state consuming CPU

# Check if GC is the cause
grep "GC" fe/log/fe.gc.log | tail -20
```

| Observation | Cause | Fix |
|---|---|---|
| Many `RUNNABLE` threads in CBO/optimizer code | Query plan storm (high QPS of complex queries) | Add plan cache; reduce concurrent complex queries |
| GC CPU > 30% (`%cpu` in GC log) | Heap pressure / Full GC | Increase FE `-Xmx`; check for memory leaks |
| `StatisticsCollectJob` threads hot | Statistics collection concurrent with traffic | Reduce `statistic_collect_concurrency`; schedule off-peak |

**→ Deep-dive: [node/SKILL.md](../node/SKILL.md) — Section 3 (FE GC) / Section 4 (thread pool)**

---

## 5. Non-StarRocks Process CPU

**Confirm signals**:
- `ps aux --sort=-%cpu` shows a non-StarRocks process in the top CPU consumers
- `st` (steal) > 0 in `top` (VM environments)
- All StarRocks metrics (query + import + compaction) degrade simultaneously

**Mechanism**: Co-located processes (backup agents, Spark jobs, monitoring scanners) compete for CPU with StarRocks. In VM environments, hypervisor steal (`st`) directly reduces the CPU available to StarRocks without appearing as a StarRocks-internal issue. The distinguishing signal is simultaneous degradation of ALL metrics — if only one metric category is affected, the cause is StarRocks-internal.

```bash
# Identify the process
ps aux --sort=-%cpu | head -20

# Check if it's a StarRocks-adjacent tool
ls /proc/$(pgrep <process_name>)/exe -l  # What binary is it?

# Check cgroup CPU usage if StarRocks is in a cgroup
cat /sys/fs/cgroup/cpu/starrocks/cpu.stat 2>/dev/null
```

**Common non-StarRocks culprits:**

| Process | Cause | Fix |
|---|---|---|
| `rsync` / `tar` / backup agent | Scheduled backup competing with queries | Schedule backups during off-peak; add `ionice` / `cpulimit` |
| `python3` / `spark` / other analytics | Co-located workload on same host | Isolate StarRocks nodes; use dedicated hosts |
| `kcompactd` / `kswapd` | Memory pressure causing kernel to reclaim pages | Reduce memory overcommit; add more RAM |
| `irqbalance` / high `si` (soft IRQ) | Network interrupt handling at high packet rate | Enable RSS; tune NIC queues; spread IRQ affinity |
| `dockerd` / container overhead | Container overhead or overlay fs writes | Use dedicated bare-metal or tune cgroup limits |

**Mitigation**: Use `cgroup` or `systemd` resource limits to cap non-StarRocks CPU:

```bash
# Cap a process to 50% of 2 cores
systemctl set-property <service> CPUQuota=100%

# Or use cpulimit for an ad-hoc process
cpulimit -p $(pgrep rsync) -l 20
```

---

## CPU Throttling Config Parameters

| Parameter | Default | Description | Dynamic |
|---|---|---|---|
| `cumulative_compaction_num_threads_per_disk` | 1 | Cumulative compaction threads per disk | No (restart), but curl update_config works at runtime |
| `base_compaction_num_threads_per_disk` | 1 | Base compaction threads per disk | No (restart) |
| `max_compaction_concurrency` | -1 (unlimited) | Global compaction thread cap | Yes (v2.5+ curl or SQL) |
| `update_compaction_num_threads_per_disk` | 1 | PK update compaction threads per disk | Yes (increase only) |
| `flush_thread_num_per_store` | 2 | Memtable flush threads per storage path | No (restart) |
| `brpc_num_threads` | -1 (auto) | BRPC worker thread count | No (restart) |
| `pipeline_dop` | 0 (auto=vCPUs/2) | Query pipeline parallelism; set to 1 for high-QPS OLTP | Yes (`SET GLOBAL`) |
| `statistic_collect_concurrency` | 3 | Concurrent statistics collection jobs (FE) | Yes (FE ADMIN SET) |
| `enable_statistic_collect` | true | Enable background statistics collection | Yes (FE ADMIN SET) |
| `clone_worker_count` | 3 | Tablet clone (rebalance) thread count | No (restart) |

### Applying Dynamic Parameters

```bash
# Per BE (v2.5+): update compaction threads dynamically
curl -XPOST "http://<be_ip>:<be_http_port>/api/update_config?cumulative_compaction_num_threads_per_disk=1"
curl -XPOST "http://<be_ip>:<be_http_port>/api/update_config?max_compaction_concurrency=4"

# Verify
curl "http://<be_ip>:<be_http_port>/varz" | grep compaction_num_threads
```

```sql
-- v3.2+: apply to all BEs at once
UPDATE information_schema.be_configs SET value = 4
WHERE name = 'max_compaction_concurrency';

-- Verify
SELECT * FROM information_schema.be_configs WHERE name = 'max_compaction_concurrency';
```

Static parameters (`flush_thread_num_per_store`, `clone_worker_count`, `brpc_num_threads`) require `be.conf` change and BE restart.

---

## Causal Chains

### Chain 1: Heavy Scan Query → BE CPU Saturation → Query Feedback Loop

```
Large full-table-scan or multi-join query submitted without resource group
  ↓ observable: SHOW PROC '/current_queries' shows query with ScanRows >> expected; no LIMIT
Pipeline executor threads saturate available CPU cores
  ↓ observable: top -Hp <be_pid> shows many threads at 100%; perf top shows vectorized:: hot
Other queries and imports compete for CPU; scheduling latency rises
  ↓ observable: concurrent simple queries start taking seconds; import write latency rises
New queries slow → users retry → more load submitted → CPU stays saturated (feedback loop)
  ↓ observable: SHOW PROC '/current_queries' count growing; no queries completing
```
Cluster appears frozen; all operations slow; restarting query does not help until root cause is killed.

**Trigger conditions**: No resource group limits; ad-hoc analytics on production cluster; missing WHERE filter causes full-table scan.

**Break point**: `KILL QUERY <query_id>` for the offending query; set `query_mem_limit` and resource groups to prevent recurrence.

---

### Chain 2: High-Frequency Import → Memtable Flush Compression → CPU Saturation

```
High-throughput import with zstd compression on memtable flush
  ↓ observable: perf top shows snappy:: or zstd:: hot; starrocks_be_cpu_task_load elevated
Flush thread pool saturates CPU; query pipeline gets fewer CPU slices
  ↓ observable: query latency increases; SHOW PROC '/current_queries' shows elevated QueryTime
Queries appear slow despite no change in query patterns
  ↓ observable: profile shows similar execution plan but higher wall time; CPU wa low (not IO)
```
Queries degrade without any query-side change; root cause is import workload added to the same BEs.

**Trigger conditions**: Large-batch import with high compression ratio (zstd/snappy) while serving online queries; `flush_thread_num_per_store` too high relative to available cores.

**Break point**: Reduce `flush_thread_num_per_store`; switch to `lz4` compression for memtable (`compression_type = "LZ4"` in table properties); add resource group CPU cap for import tasks.

---

### Chain 3: Compaction Thread Over-Provisioned → CPU Contention → Query Slowdown

```
Compaction thread count set high to clear a historical backlog
  ↓ observable: starrocks_be_cpu_task_compaction elevated; Grafana shows compaction bytes/sec high
Compaction threads consume a sustained fraction of CPU cores
  ↓ observable: top shows BE near 100%; perf top shows Compaction:: or SegmentWriter:: functions
Query pipeline gets fewer CPU time slices; scan and join throughput drops
  ↓ observable: query latency rises proportionally to compaction CPU share; profile shows longer operator times
Compaction-query CPU contention sustained until backlog cleared
  ↓ observable: query latency normalizes once compaction score drops below threshold
```
Queries slow for hours after a compaction tuning change; operators suspect query regression but root cause is compaction.

**Trigger conditions**: `cumulative_compaction_num_threads_per_disk` increased to catch up on a backlog without considering query workload; no CPU cap on compaction tasks.

**Break point**: `curl -XPOST http://<BE>/api/update_config?cumulative_compaction_num_threads_per_disk=1` to reduce compaction pressure dynamically without restart.

---

### Chain 4: Non-StarRocks Process Steals CPU → All Operations Slow

```
Scheduled backup / monitoring agent launches and consumes CPU (no resource limit set)
  ↓ observable: top shows non-StarRocks process in top 3 by CPU; ps aux --sort=-%cpu confirms
StarRocks BE and FE receive fewer CPU cycles from OS scheduler
  ↓ observable: CPU steal (%st in top) > 0 if in VM; or BE CPU user% drops while load average stays high
Queries slow; imports slow; compaction falls behind
  ↓ observable: ALL metrics degrade simultaneously — if only queries slow, suspect query cause
Non-StarRocks process finishes or is killed → all StarRocks metrics recover
  ↓ observable: latency returns to baseline without any StarRocks config change
```
Simultaneous degradation of all metrics (query + import + compaction) at the same time is the key signal for an OS-level cause rather than a StarRocks-level cause.

**Trigger conditions**: Co-located workloads on StarRocks nodes; no cgroup or systemd resource limits for non-StarRocks processes; scheduled jobs (backup, log rotation, monitoring scan) running during peak hours.

**Break point**: `kill` or `cpulimit` the offending process; long-term: enforce cgroup CPU quotas for non-StarRocks processes, or move StarRocks to dedicated hosts.

---

## Common Issues

| Observation | Most Likely Cause | First Check |
|---|---|---|
| CPU high + only query latency up | Query-caused | `SHOW PROC '/current_queries'`; `perf top` shows `vectorized::` |
| CPU high + import and query both slow | Import-caused (compression CPU) | `starrocks_be_cpu_task_load` metric; `perf top` shows `MemTable::` / `snappy::` |
| CPU high + query slow + compaction score dropping | Compaction over-provisioned | `starrocks_be_cpu_task_compaction`; reduce compaction threads |
| CPU high + ALL metrics degrade simultaneously | Non-StarRocks process | `ps aux --sort=-%cpu`; top `%st` or `%si` |
| CPU high on FE (java process) | Plan storm or Full GC | `jstack` + `top -Hp`; `fe.gc.log` |
| High `iowait` (`wa` in top), not `us` | IO bottleneck, not CPU | `iostat -x 1`; see compaction/SKILL.md or import/SKILL.md |

---

## Related Skills

- [query/SKILL.md](../query/SKILL.md) — query profiling and scan optimization
- [import/SKILL.md](../import/SKILL.md) — import pipeline and flush tuning
- [compaction/SKILL.md](../compaction/SKILL.md) — compaction thread and score management
- [node/SKILL.md](../node/SKILL.md) — FE GC, BE OOM, deadlock
- [resource-isolation/SKILL.md](../resource-isolation/SKILL.md) — resource groups and query governance

---

## Related Cases

- `case-014-scan-skew` — query-caused CPU spike from scan skew and MERGE-heavy tablets
- `case-008-be-oom` — BE OOM triggered by CPU-saturating compaction during large query burst

---

## Resources

- [StarRocks Performance Tuning](https://docs.starrocks.io/docs/administration/management/resource_management/)
- [Linux perf basics](https://perf.wiki.kernel.org/index.php/Tutorial)
