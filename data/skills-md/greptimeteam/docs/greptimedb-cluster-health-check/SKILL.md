---
name: greptimedb-cluster-health-check
description: Guide for verifying a GreptimeDB deployment is healthy after deploying or restarting — checks pod/deployment readiness, object-store access via a functional write/read smoke test, error logs, key metrics, and that ingestion recovered to the expected rate. Use right after a fresh deploy, upgrade, restart, or scale event when the user wants confirmation the cluster is healthy. Triggers on phrases like "is my cluster healthy", "集群健康检查", "after deploy/restart", "部署/重启后检查", "verify cluster", "health check", "smoke test", "fresh cluster", "新部署的集群", "check pods", "object store permission". If a check fails, hand off to greptimedb-performance-diagnosis.
---

# GreptimeDB Cluster Health Check

Verify a GreptimeDB deployment is healthy after a deploy, upgrade, restart, or scale event.
This is a **positive verification checklist** — confirm things work — not a root-cause hunt.
If a check fails or a metric looks off, hand off to `greptimedb-performance-diagnosis`.

Ask up front: **GreptimeDB version**, **deployment mode** (standalone or cluster), and
**how it's deployed** (Kubernetes/operator, Docker, binary). Older versions may lack some
metrics, and older Grafana dashboards may lack some panels — supplement from the
[grafana dashboards directory](https://github.com/GreptimeTeam/greptimedb/tree/main/grafana/dashboards),
where each panel's PromQL is the canonical source for the metric names used below.

**Running SQL and viewing metrics/logs.** To run the SQL in this guide, use any of: the
`greptimedb-mcp-server` `execute_sql` tool if available; a **MySQL** or **PostgreSQL** client;
or the built-in
[GreptimeDB Dashboard](https://docs.greptime.com/getting-started/installation/greptimedb-dashboard/).
For metrics and logs, use Grafana/self-monitoring (below). **GreptimeDB Enterprise** users can
use the [Management Console](https://docs.greptime.com/enterprise/console-ui/), which provides
SQL, metrics, and logs in one place.

## The workflow

### Phase 1. Deployment & infra readiness (especially a fresh cluster)

**On Kubernetes**, confirm the cluster actually came up:

```bash
kubectl get pods -n <namespace>
kubectl describe pod <pod> -n <namespace>   # for any pod not Running/Ready
```

Every enabled/deployed GreptimeDB role should be `Running`/`Ready` with no `CrashLoopBackOff`
and no unexpected restarts. Core cluster roles are metasrv, datanode, and frontend; also check
flownode when it is enabled/deployed. Check the GreptimeDBCluster CR / operator status too. For
Docker or binary deployments, confirm each configured process is up and its HTTP endpoint
responds.

**Object store permission (fresh cluster)** — a common first-deploy failure. A process can
start fine yet be unable to read/write the configured object store (wrong credentials, bucket,
region, or endpoint). Don't assume it works because the pod is `Running`; verify it with the
smoke test below.

### Phase 2. Functional smoke test (first-time deployment)

Only needed when the cluster is deployed for the **first time** — to prove the configured
object store is actually reachable and writable. On a restart, upgrade, or scale of a cluster
that was already serving writes, object-store access is already proven, so skip this and rely
on Phase 4 (confirm ingestion recovered). Run it anyway if you have any doubt the write path
works.

Run an end-to-end write/read to exercise the real write path (object store + WAL), not just
process liveness (see access methods above). Use a unique table name for each run, replace it
consistently in every statement, and only drop the table created by this smoke test. For
example, append the current timestamp: `_health_check_YYYYMMDD_HHMMSS`.

```sql
CREATE TABLE _health_check_20260706_123000 (
  host STRING,
  val  DOUBLE,
  ts   TIMESTAMP TIME INDEX,
  PRIMARY KEY (host)
);

INSERT INTO _health_check_20260706_123000 (host, val, ts)
VALUES ('node-1', 1.0, now()), ('node-2', 2.0, now());

SELECT * FROM _health_check_20260706_123000;

-- Force a flush so the object-store write path is exercised, then confirm:
ADMIN flush_table("_health_check_20260706_123000");
SELECT count(*) FROM _health_check_20260706_123000;

DROP TABLE _health_check_20260706_123000;
```

If the insert or flush fails (e.g. object-store auth/permission error), stop here and treat it
as a deployment problem — check Phase 3 logs for the exact error.

### Phase 3. Check logs for errors

Inspect datanode, frontend, and metasrv logs for `ERROR` (and notable `WARN`) lines that
indicate an unhealthy state:

- Object store authentication/permission failures
- Region open failures
- Flush or compaction failures
- Repeated restarts / panics

On Kubernetes: `kubectl logs <pod> -n <namespace>` (add `--previous` for a crashed container).
For self-monitoring deployments, use the **`self-monitoring-export`** skill to pull logs from
the self-monitoring instance. GreptimeDB Enterprise users can also browse logs in the
[Management Console](https://docs.greptime.com/enterprise/console-ui/).

### Phase 4. Metrics checklist

Check these against the Grafana dashboard groups (or run the PromQL directly if no dashboard).
Standalone and cluster dashboards share these panels (cluster panels filter by instance).

**Overview**

- Uptime, and **Recent Restarts**: `changes(process_start_time_seconds[$__range])` — should be
  flat after the restart settles.
- Query rate and HTTP/gRPC P99 latency (`greptime_servers_http_requests_elapsed_bucket`,
  `greptime_servers_grpc_requests_elapsed_bucket`).
- User-facing error rate: `sum(rate(greptime_servers_error[$__rate_interval]))`.

**Ingestion**

- `sum(rate(greptime_table_operator_ingest_rows[$__rate_interval]))` — **compare against the
  rate before the restart/deploy** and confirm it recovered to the expected level (not merely
  that it is non-zero). Break down by protocol if needed.

**Health / errors**

- `greptime_servers_error`, `greptime_datanode_region_request_fail_count`
- `greptime_mito_write_reject_total`, `greptime_mito_write_stall_total`,
  `greptime_mito_flush_failure_total`, `greptime_mito_compaction_failure_total`
- `greptime_pending_rows_flush_dropped_rows` (buffered ingestion loss)

**Resources**

- CPU: `rate(process_cpu_seconds_total[$__rate_interval]) * 1000` vs
  `greptime_cpu_limit_in_millicores` (both in millicores)
- Memory: `process_resident_memory_bytes` vs `greptime_memory_limit_in_bytes`

### Phase 5. Interpret

- All green (pods ready, smoke test passes on a first deploy, no error logs, ingestion
  recovered, errors/stalls flat, resources within limits) → the cluster is healthy.
- Anything off → hand off to `greptimedb-performance-diagnosis` with the specific signal.

If a needed panel is missing because the dashboard is old, give the user the PromQL above so
they can add it, or upgrade the dashboard from the grafana directory.

## Escalation

If a check fails and the cause is unclear, collect context (failing `kubectl describe`/logs,
the smoke-test error, relevant metrics, version and deployment mode) and open an issue or
discussion at https://github.com/GreptimeTeam/greptimedb. For self-monitoring users, use the
**`self-monitoring-export`** skill to export the incident logs/metrics.

## Reference

1. Self-monitoring deployment:
   https://docs.greptime.com/user-guide/deployments-administration/monitoring/cluster-monitoring-deployment/
2. Grafana dashboards (canonical source for metric names / PromQL):
   https://github.com/GreptimeTeam/greptimedb/tree/main/grafana/dashboards
3. Performance tuning tips (ingestion/health metric meanings):
   https://docs.greptime.com/user-guide/deployments-administration/performance-tuning/performance-tuning-tips/
4. REGION_STATISTICS:
   https://docs.greptime.com/reference/sql/information-schema/region-statistics/
5. CREATE TABLE:
   https://docs.greptime.com/reference/sql/create/
6. ADMIN functions (flush_table, compact_table):
   https://docs.greptime.com/reference/sql/admin/
7. GreptimeDB Dashboard (run SQL from a web UI):
   https://docs.greptime.com/getting-started/installation/greptimedb-dashboard/
8. GreptimeDB Enterprise Management Console (SQL, metrics, logs):
   https://docs.greptime.com/enterprise/console-ui/
