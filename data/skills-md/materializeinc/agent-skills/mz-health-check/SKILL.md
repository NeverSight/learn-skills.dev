---
name: mz-health-check
description: 'Analyze a Materialize environment via the MCP Developer endpoint, and/or configure an MCP client (Claude Code, Cursor, VS Code, Zed, Continue, Windsurf, Claude Desktop) to connect to the materialize-developer server. For analysis: check environment health, investigate performance, troubleshoot stale materialized views, diagnose memory pressure, find paused clusters holding back compaction, audit resource utilization, run EXPLAIN ANALYZE on user objects, get optimization recommendations. For client connection: configure/connect/set-up an MCP client to materialize-developer (Emulator, Cloud, or self-managed), control which user/role is used, switch between identities. Trigger even if user just says "check my environment", "why is my MV stale", "why is my cluster slow", "what can I optimize", "explain analyze my materialized view", "how do I connect Claude Code to materialize-developer", or "configure Cursor for the Materialize MCP".'
---

# Materialize Developer Analysis

Analyze a Materialize environment via the MCP Developer endpoint and produce a
structured report with health status, performance findings, and optimization
recommendations. Assumes Materialize v26.24 or later.

The developer endpoint exposes two read-only tools:

- **`query_system_catalog`** — `SELECT`/`SHOW`/`EXPLAIN` restricted to system
  catalog tables (`mz_*`, `pg_catalog`, `information_schema`). Takes no cluster
  argument, and one passed anyway is silently ignored rather than rejected.
  Catalog reads are auto-routed to the catalog server cluster
  (`mz_catalog_server`) while `auto_route_catalog_queries` is on (the
  default); anything the router cannot serve there — notably every
  `mz_introspection` relation — runs on the session's default cluster (the
  role's `cluster` default if set, else the system default, `quickstart`
  unless the operator changed it). Use for most catalog lookups.
- **`query`** (added in Materialize v26.30) — `SELECT`/`SHOW`/`EXPLAIN` against
  any object the role can access, on the cluster named by its required
  `cluster` argument (plus, from v26.33, an optional `cluster_replica`).
  Required for `EXPLAIN ANALYZE` (it must run on the
  MV/index's cluster) and for reading user data directly. May be hidden when
  the operator has disabled `enable_mcp_developer_query_tool`.

## Connecting an MCP client to `materialize-developer`

If the user is asking how to **configure**, **connect**, or **set up** an MCP
client (Claude Code, Cursor, VS Code, Zed, Continue, Windsurf, Claude Desktop)
to talk to the `materialize-developer` server — including how to control which
user or role the connection uses, or how to switch between identities — see
[`mcp-client-connect.md`](mcp-client-connect.md). It covers the Emulator,
Materialize Cloud, and self-managed deployments, with per-client snippets,
authentication patterns, and verification recipes.

The rest of this `SKILL.md` covers what to do *once you are connected* and want
to analyze the environment.

## Discovering Tables and Columns

**Do NOT guess column names.** System catalog relations are a mix of tables,
views, materialized views and sources, so no single `SHOW TABLES` or
`SHOW VIEWS` lists them all; use `SHOW OBJECTS FROM <schema>`. The ontology
views in `mz_internal` describe the catalog; use them to discover the correct
tables, columns, join paths, and ID types:

| Table | What it tells you |
|-------|-------------------|
| `mz_internal.mz_ontology_entity_types` | What catalog entities exist and which `mz_*` table they map to. |
| `mz_internal.mz_ontology_link_types` | Relationships between entities (foreign keys, metrics, etc.). |
| `mz_internal.mz_ontology_properties` | Column names, types, and descriptions for each entity. |
| `mz_internal.mz_ontology_semantic_types` | Typed ID domains (CatalogItemId, ReplicaId, etc.). |

Example queries:
```sql
-- Find the right table for an entity
SELECT name, relation, description
FROM mz_internal.mz_ontology_entity_types
WHERE name LIKE '%source%'

-- Find join paths between entities
SELECT name, source_entity, target_entity, properties, description
FROM mz_internal.mz_ontology_link_types
WHERE source_entity = 'source' OR target_entity = 'source'

-- Find columns for a table
SELECT column_name, semantic_type, description
FROM mz_internal.mz_ontology_properties
WHERE entity_type = 'source_status'
```

Verify column names with `SHOW COLUMNS FROM <schema>.<table>` before querying.

## Critical Rules

The server's own `initialize` instructions carry the catalog gotchas: column
names such as `last_status_change_at`, the replica-to-cluster JOIN for
`mz_cluster_replica_utilization`, the ontology views, and from v26.40 the
`mz_introspection` routing and id types. Most clients forward them; if yours
does not, `SHOW COLUMNS` is the fallback.

### `mz_introspection` relations need the `query` tool

Every `mz_introspection` relation, `mz_dataflow_arrangement_sizes` included,
is cluster-scoped, and `query_system_catalog` cannot target a cluster, so
through that tool the read lands on the session's default cluster: with
exactly one replica there you get its numbers, or an empty result, with no
error; with several replicas the read fails with `log source reads must
target a replica`, with none with `has no replicas available to service
request`. Read them through `query` with the `cluster` argument, plus
`cluster_replica` (from v26.33) on a cluster with more than one replica
(unbilled ones count), which is what the first error asks for; nothing fixes
the second.
Servers before v26.40 say in their `initialize` instructions never
to query `mz_dataflow_arrangement_sizes`; that rule predates the `query`
tool, and this supersedes it. The query, its join path to the catalog, and
its caveats are under Arrangement Sizes in `references/queries.md`. Without
the `query` tool, fall back to the relations under Memory and Resource
Consumption below.

## Workflow Overview

1. **Connect** — Verify the MCP Developer tools are available
2. **Discover** — Use the ontology + catalog queries to inventory all deployed objects
3. **Analyze** — Assess performance metrics: freshness, hydration, memory, utilization
4. **Report** — Produce a structured markdown report with findings and recommendations

## Step 1: Verify MCP Connection

Confirm you have access to the `query_system_catalog` tool. Run a quick test:

```
query_system_catalog: SELECT mz_version() FROM mz_catalog.mz_databases LIMIT 1
```

`query_system_catalog` rejects a `SELECT` that references no system catalog
table, so a bare `SELECT mz_version()` fails with `Query must reference at
least one system catalog table`, which reads like a broken connection.

Check whether a `query` tool is among the tools your client exposes. With it
you can also run `EXPLAIN ANALYZE` and queries against user objects on a named
cluster; without it (operator disabled it, or a pre-v26.30 build), fall back
to `query_system_catalog` for everything that fits.

If `query_system_catalog` fails, check:
- The MCP server is registered in your client's MCP configuration (the
  file and key differ per client, see `mcp-client-connect.md`)
- The `enable_mcp_developer` feature flag is enabled on the environment
- Your authentication credentials are valid

### Running Queries

Both tools take one read-only statement per call, no `SET`, and no trailing
semicolon (one is tolerated; two statements are rejected).

Results come back as a bare array of rows with no column names, and every `AS`
alias is discarded, so map columns positionally and keep the `SELECT` list
short and in the order you intend to read it. Numbers arrive as strings,
booleans as JSON `true`/`false`, NULL as `null`; `timestamp` and `timestamptz`
values arrive as millisecond-since-epoch strings (`1787687415336.000`), so cast
them to `text` where you need a readable time. Qualify object names with the database when the object is not in the
session's database (`SHOW database`), or the statement fails with `unknown
schema`. A response is capped (1 MB by
default) and a request timed out (60 seconds by default), both configurable by
the operator and both surfacing as errors. A `LIMIT` keeps a catalog
enumeration under the cap, and shortens the work only for a plain read of one
indexed relation, not for a join. A timeout releases the call but sometimes
not the query, so do not retry a timed-out statement as it was.

`query_system_catalog` checks its allowlist by walking FROM-clause table
references, so statements without one are not checked at all: `SHOW TABLES`,
`SHOW COLUMNS`, the `SHOW CREATE` forms and object-level `EXPLAIN ANALYZE`
pass there and can name user objects (which is why the latter answers empty,
see Worker Skew). Treat that as a fallback for when `query` is missing; use
`query` for user objects.

When filtering out system schemas, always exclude: `mz_catalog`, `mz_internal`,
`pg_catalog`, `information_schema`, and `mz_introspection`. `SHOW SCHEMAS` also
lists `mz_catalog_unstable` and `mz_unsafe`, which hold no relations.

## Step 2: Discover — Inventory the Environment

Run the discovery queries to understand what is deployed. See
`references/queries.md` for the full query set. The discovery phase covers:

### Environment Overview
- Materialize version
- Clusters and replicas — names, `managed`, replica counts and sizes. Start
  from `mz_clusters` and LEFT JOIN the replicas, or a cluster without
  replicas disappears from the inventory. An unmanaged cluster has NULL
  `size` and `replication_factor`; unbilled support replicas are listed in
  `mz_internal.mz_internal_cluster_replicas` and count like any other.
- Schemas in use

### Deployed Objects Inventory
- **Sources**: type (Kafka, Postgres, MySQL, Webhook, etc.), cluster
  assignment, status. `mz_sources` also has a row for every subsource and
  `progress` collection, so filter `type NOT IN ('subsource', 'progress')`
  before reporting a source count.
- **Materialized Views**: cluster assignment, indexes, dependencies
- **Views**: (non-materialized) and their usage patterns
- **Sinks**: type, destination, cluster assignment
- **Indexes**: what they're on, cluster assignment
- **Connections**: external system connections configured

### Object Definitions

Retrieve SQL definitions for materialized views, views, indexes, and sources
using `references/queries.md`. This is critical for optimization analysis —
the SQL definitions tell you *how* things are computed:
- Join patterns and join order
- Filter predicates (or lack thereof — missing temporal filters are a common issue)
- Aggregation strategies
- Whether MVs duplicate logic that could be shared

## Step 3: Analyze — Performance and Resource Metrics

### Freshness (Lag Analysis)
Query `mz_internal.mz_materialization_lag` for per-object lag. Its `local_lag`
and `global_lag` columns are plain `interval`s, so they compare and sort
directly, and `slowest_global_input_id` names the input holding the object
back. Both lags are measured against the inputs' frontiers, not the wall
clock: a pipeline whose source is paused shows zero lag while growing
arbitrarily stale, so also compare `mz_frontiers.write_frontier` with `now()`
(the Write Frontiers query).

`write_frontier` is not on this relation. It lives on
`mz_internal.mz_frontiers` as an `mz_timestamp`, which casts to `timestamptz`
for a readable time and to `text` (then `bigint`) for the raw number, never
directly to `bigint`. `references/queries.md` has the queries.

### Hydration Status
Query `mz_internal.mz_hydration_statuses` to check whether all dataflows are
hydrated. Non-hydrated objects after initial startup may indicate resource
pressure or configuration issues. LEFT JOIN the replica columns: `replica_id`
is NULL with no replica to hydrate on, and an inner join hides those objects.

### Paused Clusters Holding Back Compaction
A materialized view on a user cluster with no replicas holds back compaction
of every input it reads, so their storage keeps growing, and Materialize
raises no notice about it. Check for it in every health review and put any
hit in the executive summary. Run the Materialized Views on Clusters with No
Replicas query in `references/queries.md`. To fix it, give the cluster a
replica, which releases the inputs right away, or drop the view if nobody
needs it. A managed cluster takes `ALTER CLUSTER <name> SET (REPLICATION
FACTOR = 1)`, an unmanaged one `CREATE CLUSTER REPLICA <name>.<replica> (SIZE
= '<size>')`. Indexes on a
cluster with no replicas and `SCHEDULE = ON REFRESH` clusters don't hold back
their inputs.

### Memory and Resource Consumption
- `mz_internal.mz_cluster_replica_utilization` for memory/CPU percentage per replica process
- `mz_internal.mz_cluster_replica_metrics` for raw memory metrics, also one
  row per (replica, process)
- `mz_internal.mz_index_advice` to identify which MVs/indexes can be optimized

### Worker Skew (CPU imbalance across workers)

Use `WITH SKEW` to find operators where one worker does disproportionate
CPU/memory work.

**Run these through the `query` tool**, not `query_system_catalog`:
`EXPLAIN ANALYZE` executes on the cluster you pass as the `cluster` argument,
and for the object-level commands that must be the cluster the MV/index lives
on. Getting it wrong does not reliably error: on another single-replica
cluster, or through `query_system_catalog` when the default cluster has one
replica, the object-level commands return an empty result, which reads like
"no skew"; with several replicas the read fails with `log source reads must
target a replica`, with none with `has no replicas available to service
request`. Without `query`, this section is not actionable.

**Cluster-level (run on the cluster you want to inspect):**

```sql
EXPLAIN ANALYZE CLUSTER CPU WITH SKEW
```

**Object-level (run for both the MV and its indexes):**

```sql
EXPLAIN ANALYZE CPU WITH SKEW FOR MATERIALIZED VIEW <schema>.<mv_name>
```
```sql
EXPLAIN ANALYZE CPU WITH SKEW FOR INDEX <schema>.<index_name>
```

If skew is present: identify the skewed operator (often TopK/window/agg/join/distinct), then inspect definitions (`SHOW CREATE ...`) and recommend a concrete SQL change (remove/adjust hints, refactor keys/partitioning, or rewrite the MV).

### Index Advice
Query `mz_internal.mz_index_advice`, Materialize's built-in advisor. It emits
exactly six hints: `keep`, `drop unless queried directly`, `convert to a view`,
`convert to a view with an index`, `convert to materialized view`, `add index`.
Filtering on a subset silently drops real recommendations;
`references/queries.md` says what each one means.

### Cost Analysis (optional)
Use the Cost Analysis queries in `references/queries.md` (per-replica pricing).

When writing recommendations, **always quantify the credit impact** (credits
are a Cloud billing unit; on self-managed the shipped sizes carry Cloud's
numbers and operator-defined sizes whatever the operator set, 0 by default,
so present them as relative weights at best).

### Object Dependencies
Query `mz_internal.mz_object_dependencies` to understand the dependency graph.

## Step 4: Report — Generate the Analysis

Produce a structured markdown report following
`references/report-template.md`: executive summary, cluster topology,
deployed objects, performance analysis (freshness, hydration, utilization,
worker skew, source and sink health), cost analysis, index advice, SQL-level
analysis, and numbered recommendations with specific SQL.

The Cluster Topology table comes from the `Cluster Topology` query in
`references/queries.md` plus the credit columns of `Current Compute Cost per
Cluster` there.

### Writing Recommendations

**Always include specific SQL commands.** For example:

Good:
> **Recommendation:** Dematerialize `my_schema.unused_mv` to save memory.
> ```sql
> SHOW CREATE MATERIALIZED VIEW my_schema.unused_mv
> DROP MATERIALIZED VIEW my_schema.unused_mv
> CREATE VIEW my_schema.unused_mv AS <definition>
> ```

Bad:
> **Recommendation:** Consider dematerializing `my_schema.unused_mv`.

## Troubleshooting Runbooks

**Always end with specific SQL commands to fix the issue**, and never apply
one without the user's yes: scaling up or adding replicas costs money, and
dropping or altering objects loses state. Every fix below is DDL, which both
tools reject, so hand the commands to the user.

### "Why is my materialized view stale?"

**Diagnostic steps:**
1. Check whether the MV's cluster has any replica first: `mz_clusters` LEFT
   JOIN `mz_cluster_replicas` (the Clusters and Replicas query), not
   `replication_factor`, which is NULL on unmanaged clusters and blind to
   unbilled replicas. A cluster with no replicas runs nothing, and the steps
   below don't work well.
2. Check `mz_internal.mz_hydration_statuses` — is the MV hydrated, and is
   everything else on its cluster (the Non-Hydrated Objects query, restricted
   to that cluster)?
3. Check `mz_internal.mz_cluster_replica_status_history` for recent `offline`
   events with reason `oom-killed`, which covers the cgroup OOM killer, the
   heap limiter and a full lgalloc spill disk alike (the Replica Restarts
   query; the emulator records no reason, so there judge by the `offline`
   count): an OOM loop often reads `online` in the current status and modest
   in a utilization sample. Most OOMs happen during hydration, so the loop is
   over when step 2 shows everything hydrated and the latest history row per
   process is `online`; kills that recur after hydration completes are a
   steady-state loop, which only a size change or less on the cluster ends.
4. Check `mz_internal.mz_cluster_replica_utilization`: `memory_percent` near
   100 means RAM is full and further growth lands on swap where there is
   swap, felt as slow hydration or lag; `heap_percent` (RAM plus swap against
   the limit) climbing while `memory_percent` stays put is that swap in use,
   and near 100 the next spike kills the replica. Either way: scale up, move
   the MV, or shrink what the cluster holds (the fixes below, and step 7).
5. Check `mz_internal.mz_source_statuses` — upstream source errors?
6. Check `mz_internal.mz_materialization_lag` for the MV's lag (see Freshness)
7. If the `query` tool is available, run
   `EXPLAIN ANALYZE MEMORY FOR MATERIALIZED VIEW <schema>.<mv>` on the MV's
   cluster to see per-operator memory and spot expensive shapes (large
   arrangements, joins without indexes, missing temporal filters).

**Common fixes:**

*If the MV's cluster has no replicas:*
```sql
ALTER CLUSTER <cluster_name> SET (REPLICATION FACTOR 1)
```
```sql
-- Unmanaged cluster: add a replica directly
CREATE CLUSTER REPLICA <cluster_name>.r1 (SIZE = '<size>')
```

*If the cluster is overloaded (high memory/CPU):*
```sql
-- Option A: Scale up the cluster (unmanaged: DROP and CREATE its replicas
-- at the bigger size instead)
ALTER CLUSTER <cluster_name> SET (SIZE = '<next_size_up>')
```
```sql
-- Option B: Move the MV to a different cluster
SHOW CREATE MATERIALIZED VIEW <schema>.<mv_name>
DROP MATERIALIZED VIEW <schema>.<mv_name>
CREATE MATERIALIZED VIEW <schema>.<mv_name> IN CLUSTER <new_cluster> AS <definition>
```

*If an upstream source is not running:*
```sql
SELECT name, status, error, last_status_change_at
FROM mz_internal.mz_source_statuses
WHERE status != 'running'
```
Not every non-`running` status is a fault, and only `stalled` carries an
`error`; "Are my sources healthy?" below lists what each status means.
Fix the upstream source issue first. MV freshness depends on source health.

### "Why is my cluster running out of memory?"

**Diagnostic steps:**
1. Check `mz_internal.mz_cluster_replica_utilization` for memory percentage and
   `mz_cluster_replica_status_history` for `oom-killed` events (Replica Restarts)
2. Check `mz_internal.mz_index_advice` for MVs that can be dematerialized
3. Check MV definitions for missing temporal filters
4. Check for redundant indexes
5. If the `query` tool is available, run
   `EXPLAIN ANALYZE MEMORY FOR MATERIALIZED VIEW <schema>.<mv>` (or
   `FOR INDEX <name>`) on the suspect object's cluster to see which operators
   hold the most memory — the most direct way to confirm which arrangement is
   responsible.

**Common fixes:**

*Dematerialize MVs that don't need to be materialized:*
```sql
SELECT o.name, o.type, sc.name AS schema_name, ia.hint, ia.details
FROM mz_internal.mz_index_advice ia
JOIN mz_catalog.mz_objects o ON ia.object_id = o.id
JOIN mz_catalog.mz_schemas sc ON o.schema_id = sc.id
WHERE ia.hint = 'convert to a view'
```

`convert to a view with an index` and `convert to materialized view` are memory
recommendations too, with different remediations, so read the whole advice set
(the Index Advice query in `references/queries.md`) before acting on this one.

```sql
-- For each candidate:
SHOW CREATE MATERIALIZED VIEW <schema>.<mv_name>
DROP MATERIALIZED VIEW <schema>.<mv_name>
CREATE VIEW <schema>.<mv_name> AS <definition>
```

*Drop unused indexes:*
```sql
SELECT o.name, o.type, sc.name AS schema_name, ia.hint, ia.details
FROM mz_internal.mz_index_advice ia
JOIN mz_catalog.mz_objects o ON ia.object_id = o.id
JOIN mz_catalog.mz_schemas sc ON o.schema_id = sc.id
WHERE ia.hint = 'drop unless queried directly'
```

```sql
-- Verify with the user before dropping
DROP INDEX <schema>.<index_name>
```

*Scale up the cluster (unmanaged: DROP and CREATE its replicas at the bigger
size instead):*
```sql
ALTER CLUSTER <cluster_name> SET (SIZE = '<next_size_up>')
```

### "Are my sources healthy? / Has my source finished snapshotting?"

**Diagnostic steps:**
1. Check `mz_internal.mz_source_statuses` for source errors
2. Check `mz_internal.mz_source_statistics` for ingestion progress
3. Check `mz_internal.mz_materialization_lag` for end-to-end lag

**Common fixes:**

*If a source is not running:*
```sql
SELECT name, status, error
FROM mz_internal.mz_source_statuses
WHERE status != 'running'
```

The status is one of `created` (no status recorded yet), `starting`,
`running`, `paused`, `stalled` or `dropped`; the docs also list `failed`,
which the code never produces. Only `stalled` carries an `error`. Webhook and
`progress` rows always read `running`. `created` and `starting` are transient
and normal; `paused` means the source's cluster has no replicas, which no
amount of waiting fixes:

```sql
-- paused: give the source's cluster a replica
ALTER CLUSTER <cluster_name> SET (REPLICATION FACTOR 1)
-- unmanaged cluster: CREATE CLUSTER REPLICA <cluster_name>.r1 (SIZE = '<size>')
```
```sql
-- stalled/failed on bad credentials:
ALTER SECRET <secret_name> AS '<new_value>'
```

If `snapshot_committed` is `false`, the source is still loading its initial
snapshot. This is normal for large sources — wait for it to complete; it also
reads `false` with zero counters for about two minutes after a source or
replica starts. A source with no `mz_source_statistics` row at all never ran,
so check its status and whether its cluster has any replica instead of
waiting; a paused source keeps a stale row, so read `status` first.

### "What's the health of my environment?"

Run these checks in order:
1. `mz_internal.mz_cluster_replica_statuses` — all replicas of user clusters
   ready, and no recent `oom-killed` in `mz_cluster_replica_status_history`?
2. Paused clusters — any materialized view on a user cluster with no replicas?
   It holds back compaction of its inputs (Paused Clusters Holding Back
   Compaction).
3. `mz_internal.mz_source_statuses` — all sources running?
4. `mz_internal.mz_sink_statuses` — all sinks running?
5. `mz_internal.mz_cluster_replica_utilization` — resource pressure?

### "What can I optimize to save costs?"

1. Check `mz_internal.mz_index_advice` for optimization candidates
2. Check cluster utilization — are clusters over-provisioned?
3. Check credit rates from `mz_catalog.mz_cluster_replica_sizes`

## Notes

- Access is governed by RBAC, so you only see the *data* your credentials have
  access to. The catalog is not gated the same way: a role with no object
  grants still reads the full object inventory, every view and MV `definition`,
  and all of `mz_index_advice`. Where RBAC is on, `query` and every read that
  is not auto-routed also need `USAGE` on the cluster they run on
  (`mz_catalog_server` grants it to `PUBLIC`). Whether RBAC checks are on
  depends on the deployment and its configuration; `SHOW enable_rbac_checks`
  and `SHOW enable_session_rbac_checks` tell (either `on` enables them).
- Freshness numbers are point-in-time snapshots. Re-run to check if lag is stable or growing.
