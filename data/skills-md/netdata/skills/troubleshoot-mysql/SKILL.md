---
name: troubleshoot-mysql
description: "Use when diagnosing issues with MySQL: redo log stall, connection exhaustion, purge lag explosion, metadata lock cascade, or replication lag spiral. Queries Netdata via MCP for mysql server availability, connection utilization, query throughput (questions), slow query rate, active execution queue (threads_running), applies the diagnostic tree from the Netdata operator playbook, and recommends remediation."
version: 0.1.0
author: Netdata
license: Apache-2.0
tags:
  - netdata
  - troubleshoot
  - mcp
  - mysql
---

# Troubleshoot MySQL

## When to use this skill

- **Redo log stall**: Write rate exceeds checkpoint capacity then synchronous flush then all writes
                      freeze.
- **Connection exhaustion**: max_connections reached then new connections rejected then cascading
                             application failures.
- **Purge lag explosion**: Long-running transaction blocks purge then history list grows then all
                           MVCC reads degrade.
- **Metadata lock cascade**: DDL blocks behind long transaction then all DML on that table queues
                             then connection pool fills.
- **Replication lag spiral**: Single-threaded apply or large transactions then lag grows without
                              bound then data staleness.
- **Buffer pool cliff**: Working set exceeds buffer pool then hit ratio collapses then disk I/O
                         saturates then latency explosion.
- Any time the user reports a MySQL service behaving outside its expected envelope (elevated errors,
  latency, saturation, resource exhaustion, or unexpected restarts).
- An on-call engineer is paging on a Netdata alert tied to a MySQL instance and wants a structured
  triage path.

## Key facts

- This skill wraps the Netdata operator playbook for MySQL. It does not replace the playbook; it
  routes a coding agent through MCP queries against the same signals the playbook relies on.
- MySQL is a connection-oriented request processor with a pluggable storage engine. Production
  deployments overwhelmingly use InnoDB. Understanding these internal subsystems is required to
  reason about failures:
- The playbook decomposes MySQL health into 9 signal domains: Availability, Throughput, Latency,
  Errors, Saturation, Resource Utilization. Each domain maps to one rule file in this skill.
- Dominant failure archetypes the playbook calls out: Redo log stall; Connection exhaustion; Purge
  lag explosion; Metadata lock cascade; Replication lag spiral.
- Netdata observes the signals listed in the rule files via its native collectors, plus any
  OpenTelemetry-shipped metrics that your MySQL instrumentation adds. Both paths end at the same MCP
  query surface.
- Netdata's mysql collector emits 225 context(s) under `mysql.*`. The rule files enumerate which
  contexts surface which domain; the Verification section below names the load-bearing ones
  explicitly.

## Step-by-step

1. Confirm the MySQL service is up. Query Netdata via MCP with `list_nodes` and filter by the host
   running the target. A missing node means the symptom is at the network or orchestrator layer, not
   inside the service.
2. Pull the last 15 minutes of signals for the target. Use `query_metrics` against the contexts
   listed in the domain rule files. Run `find_anomalous_metrics` in parallel over the same window;
   anomalies frame which rule file to read first.
3. Check for **Redo log stall**. Write rate exceeds checkpoint capacity then synchronous flush then
   all writes freeze. Inspect the rule file whose signals move first for this mode.
4. Check for **Connection exhaustion**. max_connections reached then new connections rejected then
   cascading application failures. Inspect the rule file whose signals move first for this mode.
5. Check for **Purge lag explosion**. Long-running transaction blocks purge then history list grows
   then all MVCC reads degrade. Inspect the rule file whose signals move first for this mode.
6. Check for **Metadata lock cascade**. DDL blocks behind long transaction then all DML on that
   table queues then connection pool fills. Inspect the rule file whose signals move first for this
   mode.
7. Check for **Replication lag spiral**. Single-threaded apply or large transactions then lag grows
   without bound then data staleness. Inspect the rule file whose signals move first for this mode.
8. Correlate with host-level signals (`system.cpu.utilization`, `system.memory.usage`,
   `system.disk.io_time`). Many service-level failures have a host-resource precursor.
9. Apply the remediation hinted at in the matching rule file or the operator playbook. Re-run the
   MCP queries from the Verification section to confirm the signals returned to expected ranges. A
   fix that does not move the signal back is not a fix.

### Handy MCP call templates

```text
# Discover metrics from MySQL
list_metrics with q="mysql"

# Pull a specific context over the last window
query_metrics with context="mysql.queries_type", relative_window=-15m

# Rank anomalies for the service or host
find_anomalous_metrics with node=<host> and context_pattern="mysql.*"

# Correlate a known problem context with others
find_correlated_metrics around the incident window

# Show current alert state
list_raised_alerts scoped to the node
```

## Common mistakes

- Treating MySQL as a generic HTTP or process health check. MySQL has specific failure archetypes
  (see Key facts) that generic checks miss.
- Stopping at the first anomalous metric. Several archetypes produce correlated spikes; use
  `find_correlated_metrics` to widen the search before concluding a root cause.
- Quoting percentile latency without the sample count. Low traffic plus a single slow request moves
  p99 by seconds.
- Reading dashboards for a window shorter than the failure's fingerprint. Slow-brew failures (queue
  growth, bloat, memory fragmentation) need 30+ minutes of data to see the trend.
- Skipping the host-level correlation. A process-level fix for a noisy-neighbour problem does not
  hold.
- Assuming alert thresholds are tuned for your workload. Tune against observed MySQL traffic before
  escalating an alert configuration issue.

## Verification

Run these MCP queries against the Netdata instance that sees the MySQL service. Every context listed
below is a real Netdata chart name; the agent does not need to guess.

```text
1. list_metrics filtered by q="mysql" (returns every mysql.* context Netdata sees)
2. query_metrics with contexts=[mysql.queries_type, mysql.handlers, mysql.connections, mysql.connections_active, mysql.threads, mysql.innodb_redo_log_occupancy] and relative_window=-30m
3. find_anomalous_metrics filtered by node=<host> and context_pattern="mysql.*"
```

Load-bearing contexts for this service:

- `mysql.queries_type`: Queries By Type (queries/s). Dimensions: select, delete, update, insert,
                        replace.
- `mysql.handlers`: Handlers (handlers/s). Dimensions: commit, delete, prepare, read_first,
                    read_key, read_next.
- `mysql.connections`: Connections (connections/s). Dimensions: all, aborted.
- `mysql.connections_active`: Active Connections (connections). Dimensions: active, limit,
                              max_active.
- `mysql.threads`: Threads (threads). Dimensions: connected, cached, running.
- `mysql.innodb_redo_log_occupancy`: InnoDB Redo Log Occupancy (percentage). Dimensions: occupancy.

A clean result means every context is within its expected band and the `find_anomalous_metrics` list
is empty or contains only already-acknowledged items. If the fix was real, re-running the same
queries 10 minutes after applying it will show a clean result. If it does not, revert and look
deeper.

### When the fix does not hold

If signals drift back into the anomalous range within 30 minutes of a remediation, the cause was
deeper than the applied change. Typical misdiagnoses for MySQL:

- Host-resource pressure masquerading as application bug.
- Dependent service (DB, cache, upstream) causing a secondary symptom in the instrumented service.
- Configuration change that was never reloaded (some subsystems only pick up config on full
  restart).

Escalate by widening the query window: 2-6 hours instead of 15 minutes. Slow-moving causes are
invisible at triage window sizes.

## References

- [`rules/availability.md`](./rules/availability.md)
- [`rules/throughput.md`](./rules/throughput.md)
- [`rules/latency.md`](./rules/latency.md)
- [`rules/errors.md`](./rules/errors.md)
- [`rules/saturation.md`](./rules/saturation.md)
- [`rules/resource-utilization.md`](./rules/resource-utilization.md)
- [`rules/replicationconsistency.md`](./rules/replicationconsistency.md)
- [`rules/internal-state.md`](./rules/internal-state.md)
- [`rules/disk-space.md`](./rules/disk-space.md)
- Netdata operator playbook: the authoritative source material this skill summarizes.
- `skills/netdata-mcp-integration/` for the transport setup.
- `skills/netdata-otel-setup/` if additional application signals are needed beyond what Netdata
  collects natively.
