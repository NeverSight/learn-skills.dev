---
name: troubleshoot-ceph
description: "Use when diagnosing issues with Ceph: capacity exhaustion, stuck pgs, slow requests, mon quorum loss, or osd flapping. Queries Netdata via MCP for Ceph health signals, applies the diagnostic tree from the Netdata operator playbook, and recommends remediation."
version: 0.1.0
author: Netdata
license: Apache-2.0
tags:
  - netdata
  - troubleshoot
  - mcp
  - ceph
---

# Troubleshoot Ceph

## When to use this skill

- **Capacity exhaustion**: Ceph throttles at nearfull (85%), blocks backfill at
- **Stuck PGs**: PGs unable to reach active+clean due to failed OSDs, map inconsistencies,
- **Slow requests**: OSD operations exceeding `osd_op_complaint_time` (default 30s). Causes
- **MON quorum loss**: Without majority agreement, cluster cannot accept map updates. Client
- **OSD flapping**: OSDs repeatedly marking up/down due to heartbeat timeouts, network
- **Recovery storm**: Multiple OSD failures trigger massive data movement that competes with
- Any time the user reports a Ceph service behaving outside its expected envelope (elevated errors,
  latency, saturation, resource exhaustion, or unexpected restarts).
- An on-call engineer is paging on a Netdata alert tied to a Ceph instance and wants a structured
  triage path.

## Key facts

- This skill wraps the Netdata operator playbook for Ceph. It does not replace the playbook; it
  routes a coding agent through MCP queries against the same signals the playbook relies on.
- Ceph is a distributed storage system that presents block (RBD), file (CephFS), and object
  (RGW/S3/Swift) interfaces on top of RADOS (Reliable Autonomic Distributed Object Store).
  Everything is an object stored across OSDs, placed by the CRUSH algorithm.
- Dominant failure archetypes the playbook calls out: Capacity exhaustion; Stuck PGs; Slow requests;
  MON quorum loss; OSD flapping.
- Netdata observes the signals listed in the rule files via its native collectors, plus any
  OpenTelemetry-shipped metrics that your Ceph instrumentation adds. Both paths end at the same MCP
  query surface.
- Netdata's ceph collector emits 27 context(s) under `ceph.*`. The rule files enumerate which
  contexts surface which domain; the Verification section below names the load-bearing ones
  explicitly.

## Step-by-step

1. Confirm the Ceph service is up. Query Netdata via MCP with `list_nodes` and filter by the host
   running the target. A missing node means the symptom is at the network or orchestrator layer, not
   inside the service.
2. Pull the last 15 minutes of signals for the target. Use `query_metrics` against the contexts
   listed in the domain rule files. Run `find_anomalous_metrics` in parallel over the same window;
   anomalies frame which rule file to read first.
3. Check for **Capacity exhaustion**. Ceph throttles at nearfull (85%), blocks backfill at Inspect
   the rule file whose signals move first for this mode.
4. Check for **Stuck PGs**. PGs unable to reach active+clean due to failed OSDs, map
   inconsistencies, Inspect the rule file whose signals move first for this mode.
5. Check for **Slow requests**. OSD operations exceeding `osd_op_complaint_time` (default 30s).
   Causes Inspect the rule file whose signals move first for this mode.
6. Check for **MON quorum loss**. Without majority agreement, cluster cannot accept map updates.
   Client Inspect the rule file whose signals move first for this mode.
7. Check for **OSD flapping**. OSDs repeatedly marking up/down due to heartbeat timeouts, network
   Inspect the rule file whose signals move first for this mode.
8. Correlate with host-level signals (`system.cpu.utilization`, `system.memory.usage`,
   `system.disk.io_time`). Many service-level failures have a host-resource precursor.
9. Apply the remediation hinted at in the matching rule file or the operator playbook. Re-run the
   MCP queries from the Verification section to confirm the signals returned to expected ranges. A
   fix that does not move the signal back is not a fix.

### Handy MCP call templates

```text
# Discover metrics from Ceph
list_metrics with q="ceph"

# Pull a specific context over the last window
query_metrics with context="ceph.cluster_status", relative_window=-15m

# Rank anomalies for the service or host
find_anomalous_metrics with node=<host> and context_pattern="ceph.*"

# Correlate a known problem context with others
find_correlated_metrics around the incident window

# Show current alert state
list_raised_alerts scoped to the node
```

## Common mistakes

- Treating Ceph as a generic HTTP or process health check. Ceph has specific failure archetypes (see
  Key facts) that generic checks miss.
- Stopping at the first anomalous metric. Several archetypes produce correlated spikes; use
  `find_correlated_metrics` to widen the search before concluding a root cause.
- Quoting percentile latency without the sample count. Low traffic plus a single slow request moves
  p99 by seconds.
- Reading dashboards for a window shorter than the failure's fingerprint. Slow-brew failures (queue
  growth, bloat, memory fragmentation) need 30+ minutes of data to see the trend.
- Skipping the host-level correlation. A process-level fix for a noisy-neighbour problem does not
  hold.
- Assuming alert thresholds are tuned for your workload. Tune against observed Ceph traffic before
  escalating an alert configuration issue.

## Verification

Run these MCP queries against the Netdata instance that sees the Ceph service. Every context listed
below is a real Netdata chart name; the agent does not need to guess.

```text
1. list_metrics filtered by q="ceph" (returns every ceph.* context Netdata sees)
2. query_metrics with contexts=[ceph.cluster_status, ceph.cluster_osds_by_status_count, ceph.cluster_iscsi_gateways_by_status_count, ceph.cluster_objects_by_status_distribution, ceph.cluster_pgs_count, ceph.cluster_pgs_by_status_count] and relative_window=-30m
3. find_anomalous_metrics filtered by node=<host> and context_pattern="ceph.*"
```

Load-bearing contexts for this service:

- `ceph.cluster_status`: Ceph Cluster Status (status). Dimensions: ok, err, warn.
- `ceph.cluster_osds_by_status_count`: Ceph Cluster OSDs by Status (status). Dimensions: up, down,
                                       in, out.
- `ceph.cluster_iscsi_gateways_by_status_count`: Ceph Cluster iSCSI Gateways by Status (gateways).
                                                 Dimensions: up, down.
- `ceph.cluster_objects_by_status_distribution`: Ceph Cluster Objects by Status (percent).
                                                 Dimensions: healthy, misplaced, degraded, unfound.
- `ceph.cluster_pgs_count`: Ceph Cluster Placement Groups (pgs). Dimensions: pgs.
- `ceph.cluster_pgs_by_status_count`: Ceph Cluster Placement Groups by Status (pgs). Dimensions:
                                      clean, working, warning, unknown.

A clean result means every context is within its expected band and the `find_anomalous_metrics` list
is empty or contains only already-acknowledged items. If the fix was real, re-running the same
queries 10 minutes after applying it will show a clean result. If it does not, revert and look
deeper.

### When the fix does not hold

If signals drift back into the anomalous range within 30 minutes of a remediation, the cause was
deeper than the applied change. Typical misdiagnoses for Ceph:

- Host-resource pressure masquerading as application bug.
- Dependent service (DB, cache, upstream) causing a secondary symptom in the instrumented service.
- Configuration change that was never reloaded (some subsystems only pick up config on full
  restart).

Escalate by widening the query window: 2-6 hours instead of 15 minutes. Slow-moving causes are
invisible at triage window sizes.

## References

- [`rules/overview.md`](./rules/overview.md)
- Netdata operator playbook: the authoritative source material this skill summarizes.
- `skills/netdata-mcp-integration/` for the transport setup.
- `skills/netdata-otel-setup/` if additional application signals are needed beyond what Netdata
  collects natively.
