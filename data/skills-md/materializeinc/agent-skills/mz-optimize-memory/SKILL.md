---
name: mz-optimize-memory
description: >
  Reduce the memory footprint and cost of Materialize compute clusters:
  find where arrangement memory sits, pick and size the right optimization
  lever (index strategy, GROUP SIZE hint tuning, view slimming, subquery
  decorrelation), adjudicate
  proposed index or view changes, run measured experiments safely, and
  package verified changes. Use when a Materialize cluster or replica uses
  too much memory or is OOMing or crash-looping, when the user wants to
  downsize a replica or cut Materialize spend, when deciding which indexes
  to add or drop, or when tuning GROUP SIZE hints.
---

# Optimize Cluster Memory

Reduce what a Materialize compute cluster spends on memory, with every
claim backed by a measurement. The deliverable of an engagement is a set
of per-item verdicts with measured evidence, validated changes expressed
in the user's own deployment tooling, and a right-sized replica at the
end. Freed memory is not saved money until the replica is resized down.

For freshness problems (an object lagging behind wall-clock time) use
the mz-debug-freshness skill instead. Memory work and freshness
work share instruments but have different workflows.

## Ground rules

- Ask before changing anything, and before reading the user's data. Catalog,
  introspection and EXPLAIN reads need no permission; a SELECT over the user's
  relations (a cardinality probe, the match-rate query, an exactness proof)
  reads their data and is asked for first. Anything that creates, alters,
  drops, or writes rows, in the user's environment or on their machine
  (including a local Docker container), is proposed first and run only after a
  yes. Approval covers a class of change, not each statement: an approved
  experiment cluster covers building and dropping candidate objects on it, and
  anything beyond it needs a fresh ask.
- Never change objects on production clusters, even with permission to
  experiment. Object definitions usually have a source of truth
  outside Materialize (mz-deploy, dbt, or deploy scripts), and a
  catalog-only change is silently reverted, or half-reverted, by the
  next deploy. Accepted changes are delivered as edits to that source
  of truth, or as DDL for the user to run where the catalog is the
  source.
- Experiments run on a dedicated experiment cluster that the user
  creates (you supply the commands). Never build or rebuild candidate
  objects on a production cluster: an object built there hydrates on
  the production replica and spends production memory and CPU on an
  experiment. Read-only `EXPLAIN ANALYZE` and introspection reads against
  production are diagnosis and are fine; anything that hydrates goes
  to the experiment cluster.
- Do not recommend `REFRESH EVERY` materialized views as an optimization
  lever in any situation.
- Every verdict rests on a measurement: both sides sized, the join key read
  from the plan, the consumer count counted. A graph-shape or plan-text
  argument alone is not a verdict, and an estimate gates an experiment but
  never settles one: shared arrangements restructure join plans in ways static
  bytes-per-row arithmetic (the width math of step 5) cannot see, so an
  estimate can err either way, and any non-trivial index or boundary verdict (a
  boundary: an indexed view placed at a (collection, key) point several
  consumers share) gets a measured build before it ships.
- Leave-alone is the default outcome of a check, and it stays in your
  notes. Check many things (a hint that measures correct, an exact
  min/max or TopK whose arrangement is just the input it must retain
  to answer retractions, a single-copy arrangement no signature applies
  to), change only what a measured signature calls for, and report
  only the opportunities. A change without such a signature is churn:
  a rebuild for no measured saving. State a leave-alone only for an
  item the user asked about (a proposal item, a named object) or when
  the residual footprint needs explaining, such as why the replica
  cannot go lower.
- Batch by confidence. Changes you are at least about 97% sure of (a hint
  retune that `mz_expected_group_size_advice` measured, an index drop that no
  plan reads, removal of columns the plan proves unread) can ship in one batch;
  anything less certain is applied alone and re-measured before the next, so
  each saving stays attributable and an interaction (a new index restructuring
  a neighbour's plan) shows up as its own number. Record the estimate per
  change and the measurement per batch either way.

## Connection and tools

Prefer the Materialize MCP developer endpoint when it is available. Its tools
describe themselves; what matters for this skill: every cluster-bound read
(`EXPLAIN ANALYZE`, `mz_introspection`, `EXPLAIN` of user objects) goes through
the `query` tool with its cluster argument, plus its `cluster_replica` argument
on a multi-replica cluster (any extra replica counts, including an unbilled
support replica on Cloud). The endpoint's other tool, `query_system_catalog`,
is a trap here: it does not refuse those statements (the `mz_introspection`
relations pass its name check) and answers them about the session's default
cluster: with exactly one replica there the answer looks valid (often an empty
result, or another cluster's numbers) and carries no error; with several it
fails with `log source reads must target a replica`, with none with `has no
replicas available to service request`. Never send a cluster-bound read there.
The tools cannot SET anything, so the cluster is always the argument, never a
session setting. On servers before v26.40 the endpoint's own instructions say
never to query `mz_introspection.mz_dataflow_arrangement_sizes`; that rule
predates the `query` tool and concerns the catalog tool only (later servers say
so themselves), so it does not apply to `query` with a cluster argument (what
that relation's `id` joins to is in "Reading introspection"). Tool responses
are bare row arrays without column names, numbers as strings, capped by default
at 1 MB per response and 60 seconds per request (both per-environment settings
an operator can move), so keep SELECT lists short and in a fixed order, and
give census queries a `LIMIT` or an aggregation rather than listing every
arrangement of a big cluster (a `LIMIT` bounds the result, not the work of a
join). A timed-out request cancels the peek but sometimes not the work: its
dataflow can run to completion on the cluster, so do not resend it unchanged.
Timestamps arrive as milliseconds since the epoch unless cast to `text`, and
object names outside the session's database need the database prefix, or the
statement fails with `unknown catalog item` when a schema of that name exists
in the session's database and with `unknown schema` when it does not.

If no MCP server is configured, or its `query` tool is absent (older
Materialize, or disabled by the operator; `query` needs v26.30 and its
`cluster_replica` argument v26.33), suggest setting one up (the
mz-health-check skill covers client configuration), or ask the user for
a SQL connection string instead. Whenever you ask for a connection string, warn
the user that it should be for a role scoped to what the current phase needs
(read-only for diagnosis; see "Making changes", below, for the experiment
role), never an admin or superuser. Check that the scoping is real before
relying on it: `SHOW enable_rbac_checks`. Cloud enforces RBAC by default, while
self-managed instances default to `enableRbac: false` and the emulator image
turns the checks off, and with the checks off the GRANTs and ownership gates on
user objects stop being enforced, so a scoped role protects nothing there (the
gates on system objects, and `restrict_to_user_objects` below, are separate and
still apply). Ask also that the role not have `restrict_to_user_objects` set,
which hides the system catalog and makes `EXPLAIN ANALYZE` fail on objects the
role does not own, even with the RBAC checks off.

All writes happen outside MCP. The "Making changes" section defines who
executes them and where.

## Reading introspection

Rules for every introspection read, over MCP or SQL alike:

- **Measure hydrated dataflows only.** Introspection state (everything `EXPLAIN
  ANALYZE` and `mz_introspection` read) fills as hydration completes: a
  still-hydrating dataflow returns empty or partial numbers, and what it does
  return measures catching up, not steady state. Gate every measurement on
  `mz_internal.mz_hydration_statuses` (maintained by the control plane, so it
  answers even when the replica is busy). This applies equally after every
  rebuild you perform mid-engagement: rebuild, wait for hydrated, then
  re-measure. Right after a replica crash the relation can briefly serve the
  previous incarnation's rows, so re-read it once the replica is back before
  trusting a `true`. For a cluster that cannot reach hydration at all, see
  "Intake: a cluster that cannot hydrate".
- Introspection is served by the target cluster and is session-scoped:
  `SET cluster = ...` first (or the cluster argument of the MCP
  `query` tool). On a cluster with several replicas, target one
  replica too (`SET cluster_replica = ...`, or the tool's
  `cluster_replica` argument): introspection reads on a multi-replica
  cluster fail outright otherwise ("log source reads must target a
  replica"), readings legitimately differ across replicas, and the
  one you measure must itself be hydrated.
- Results can lag a few seconds behind DDL; if a query returns empty
  rows right after a change, wait and re-run before concluding
  anything.
- `mz_introspection.mz_dataflow_arrangement_sizes.id` is a dataflow id
  (`uint8`), never joinable to `mz_objects.id`: reach the catalog through
  `mz_introspection.mz_compute_exports` (`dataflow_id` to `export_id`), or
  match `name` (`Dataflow: <db>.<schema>.<object>`, the name the object was
  created under, not its current name: a blue/green deploy or a dbt run creates
  objects under a staging name and swaps them in, so the dataflow keeps the
  staging name and only the export path finds it).
- The docs' dataflow troubleshooting page
  (https://materialize.com/docs/transform-data/dataflow-troubleshooting/)
  carries the census and per-operator queries this skill builds on and the
  CPU-side instruments it does not repeat (`mz_scheduling_elapsed`,
  `mz_compute_operator_durations_histogram`, the `mz_dataflow_addresses` region
  walk); the freshness page
  (https://materialize.com/docs/transform-data/freshness-troubleshooting/)
  covers lag.

## Intake: a cluster that cannot hydrate

Users often arrive with a cluster that is OOMing, not with a stable but
oversized one. Do not start the measurement workflow against an OOM-looping
replica: a replica that dies mid-hydration yields no usable measurements
("Reading introspection"). Confirm the state first from two control-plane
relations, which answer even while the replica is looping:
`mz_internal.mz_hydration_statuses` keeps reporting `hydrated = false` across
the replica's restarts (a single `false` reading only says still hydrating; a
cluster with no replica rows in `mz_cluster_replicas` also stays `false`, with
`replica_id` NULL), and `mz_internal.mz_cluster_replica_status_history`
confirms that MEMORY is the cause (`offline` rows with reason `oom-killed`,
which covers every memory-class limit, RAM, heap and spill disk alike, without
saying which; any other failure leaves the reason NULL; the current
`mz_cluster_replica_statuses` often reads `online` between two kills, so it
cannot; the emulator's process orchestrator records no reason, so there count
the `offline` rows). The second check matters because a cluster can also fail
to hydrate on a compute grind (a cross join or a skewed key grinding one worker
for hours with flat memory: the quadratic-join shape, below;
`mz_introspection.mz_scheduling_elapsed_per_worker` summed per worker shows the
one busy worker whenever the replica still answers) or on starved inputs, and a
bigger replica fixes neither. The loop is over, and measurement meaningful,
once every object on the cluster is hydrated and the latest history row per
process is `online`; kills that recur after hydration completes are the
steady-state case this skill exists for, which ends only when the cluster holds
less state (the levers below) or the replica gets bigger.

Offer two ways to reach measurable ground, both executed by the user:

- Develop against a smaller input data set until the pipeline is
  optimized, then scale the data back up.
- Temporarily size the cluster (or a clone of it) large enough to
  hydrate without OOMing, measure and optimize there, then right-size
  down. The oversized replica is a measurement platform, not the fix.

## Cost model

The high-level model:

- Indexes and materialized views are maintained INCREMENTALLY by
  persistent dataflows that update their results as inputs change. That
  is why they need memory continuously: the operators must retain
  enough state to react to any input change.
- Most of the retained state lives in ARRANGEMENTS: in-memory
  collections of rows organized by a key, maintained as inputs change.
  The kind of arrangement decides which lever can reach it. INDEX
  arrangements are shareable: `CREATE INDEX` maintains an arrangement
  of the indexed collection that other dataflows can read, but only
  WITHIN the index's cluster. Every other arrangement is
  intra-dataflow: private working state visible only to the dataflow
  that built it.
- Intra-dataflow arrangements sit on operators' inputs and outputs. An
  operator's INPUT arrangement is either an explicit plan node or built inside
  the operator with no node of its own; both show in `EXPLAIN ANALYZE MEMORY`.
  The explicit node has three spellings in EXPLAIN: `ArrangeBy` in `EXPLAIN
  OPTIMIZED PLAN`; `ArrangeBy` with one `arrangements[i]` line per key in
  `EXPLAIN PHYSICAL PLAN` (verbose text, that statement's default); and
  `Arrange (key)` in the arrow text that a bare `EXPLAIN <object>` or `EXPLAIN
  PHYSICAL PLAN AS TEXT` prints. Some operators can REUSE an arrangement that
  already exists on their input (an index, or an upstream operator's arranged
  output) instead of building one, and some leave their OUTPUT arranged so the
  next operator in the same dataflow can reuse it. Reuse is within a dataflow;
  sharing across dataflows always needs an index. Those two properties, reuse
  of an input arrangement and an arranged output, decide what an index can
  replace; the operator table below gives them per operator.
- Only operators that retain state cost memory. A join's output is a plain,
  unarranged collection, so "this join emits 500M rows" is not a memory cost by
  itself. Look at what the output feeds: hierarchical MIN/MAX reduces, TopKs,
  and explicit arrangements retain. Accumulable aggregates (sum/count/avg)
  collapse to per-group accumulators and stay cheap.
- Not all retained memory is arrangement state: the persist sink at the end of
  every materialized view holds its own buffer, largest at hydration and
  drained afterwards, so that share of the peak is observable only during a
  hydration and a replica restart is how you get another one. See "Memory
  beyond arrangements" below.
- A plain VIEW is a saved query, not a computed thing: every consuming
  dataflow INLINES the view's definition and the optimizer replans it
  in that consumer's context, pruning columns to that consumer's
  demand. Five dataflows over one view means five independent copies
  of its operators and arrangements. This is why a big view in the
  SQL is not a thing you will find in the dataflow census: its cost
  appears inlined inside each consumer, which is also why mining
  measured arrangements beats reading view SQL. Two objects stop the
  inlining and make a view computed once, with different products:
  - an INDEX on the view computes it once per cluster, and its
    product IS an arrangement, which consumers on that cluster read
    directly, joins included;
  - a MATERIALIZED VIEW computes it once globally and persists the
    results, readable from any cluster, but persisted results do NOT
    end in an arrangement: each consuming dataflow arranges what it
    reads by whatever key it needs.
  So an MV dedups the computation but not the arrangement state; indexing the
  MV on each reading cluster recovers the missing half for the consumers that
  read it on the index's key, one shared arrangement instead of one private
  copy each.
- An index's own dataflow can hold more arrangements than the one it
  exports: indexing a computed view also computes the view, with
  whatever intra-dataflow arrangements that takes. The exported
  arrangement is the shareable product, not the dataflow's whole
  footprint.

### Operator-level detail

Per physical-plan operator, with input arrangements counted whether
printed as a node or built internally:

| Operator | Input arrangement | Reuses an existing input arrangement | Output arranged, reusable | Memory |
|---|---|---|---|---|
| Get, Constant, Map/Filter/Project, FlatMap, Negate | none | reads through one without holding it | no | none of their own |
| Explicit arrangement node (`ArrangeBy` / `Arrange`, spellings above) | builds one arrangement per key it prints (default text: `Arrange (key)`, one `(key)` each; verbose: one `arrangements[i]` line each); the node printed as `Unarranged Raw Stream` (verbose: `raw=true` with no `arrangements` line) builds nothing and only hands an existing arrangement through as a plain collection | yes, silently: it lists only the arrangements it builds; keys that the input already provides pass through unlisted, and a node whose keys all exist is elided from the plan | yes, one per key built | rows times width per key built; nothing for the raw-stream form |
| Join, `type=differential` (linear) | both inputs of every stage are arranged: an input relation reuses an existing arrangement or gets a printed Arrange; the running intermediate result is one side of every stage after the first and is arranged internally (`JoinStage`) | yes | no | input relations plus every intermediate |
| Join, `type=delta` | every input relation, by each key it is probed on: reuses an existing arrangement or gets a printed Arrange; no intermediate is arranged | yes | no | input relations only, no intermediates |
| Reduce | internal, by the group key (hierarchical variants by (hash, group key)) | no | yes, by the group key | see Reduce below |
| Distinct (a `SELECT DISTINCT` or key-only `GROUP BY`; `Distinct` in the optimized plan, `Reduce::Distinct` in the verbose physical plan, `Distinct GroupAggregate` in the arrow text and EXPLAIN ANALYZE) | internal, by all its columns (`Arranged DistinctBy`) | no | yes, by the whole row | about two records per group, input plus output, multiplicity only |
| TopK | internal, per hierarchy level, by (hash, group key) | no | only `Monotonic Top1` | non-monotonic: input per level plus a reduced arrangement per level; `MonotonicTopK`: one stage, about (workers x limit) records per group while updates flow and near the limit once quiesced, plus a reduced arrangement; `Monotonic Top1`: one record per group |
| Threshold | Arrange by the whole row (all columns, in order), printed by the physical plan only | in principle, never in practice (its input is a Union) | yes, by the whole row | one whole-row arrangement plus the output |
| Consolidating Union, LetRec boundary, monotonic-input consolidation | no arrangement; a merge batcher instead | no | no | transient, see Consolidation below |
| Persist sink (MV output, absent from EXPLAIN) | no arrangement; a correction buffer instead, logged as `mv_sink(<id>)::write` | no | no | see "Memory beyond arrangements" |

**Reduce.** A Reduce arranges its own input in its own layout (group key plus
the aggregate arguments), so it never consumes an existing arrangement and no
index can replace that input arrangement: an index on the group key is read as
a full scan, and the Reduce, a bare `count(*)` included, still builds its own
(measured). What that input arrangement holds depends on the aggregate class:

- Accumulable aggregates (sum, count, avg) carry their accumulators in the diff
  with empty values, so the input consolidates to one record per group and the
  arranged output adds a second: about two records per group, however many rows
  feed it. Cheap per row, not per group: the pair costs roughly 150 bytes per
  group for one accumulator (`count`, `sum`) and 300 for an `avg` (two), so a
  very large number of very small groups is where an accumulable stops being
  cheap. Do not calibrate this on a `generate_series` rig: over groups that are
  all alike the accumulators store compactly and the figure reads ten times
  lower.
- A plain `SELECT DISTINCT` or key-only `GROUP BY` is the Distinct row
  above. An aggregate-level
  DISTINCT (`count(DISTINCT v)`) instead adds an arrangement pair sized
  by groups times distinct values. `DISTINCT ON` is not a Reduce at
  all but a TopK with `limit=1`.
- Basic aggregates (`string_agg`, `jsonb_agg`, and the other
  non-accumulable, non-hierarchical ones) keep every qualifying input
  row of the group, thinned to the aggregate's argument columns.
  Identical thinned rows consolidate into one record carrying a
  multiplicity, so the record count is the distinct (group key,
  argument) tuples per group, not the rows: a low-cardinality argument
  column makes a large group small.
- Non-monotonic min/max (the bucketed hierarchical rendering) keeps the same
  full input, thinned the same way; no exact incremental extremal aggregate can
  hold less, because a retraction of the current extremum must be answerable
  from what is retained. The hierarchy then adds two arrangements per bucket
  level (`Arranged MinsMaxesHierarchical input` and `Reduced Fallibly
  MinsMaxesHierarchical`), and every level whose bucket count exceeds the
  group's retained record count holds a near-full copy of the input, which is
  what GROUP SIZE hints trim. A monotonic min/max (append-only input) escapes
  this and keeps the winner in the diff, one record per group; an MV is never
  monotonic, whatever its definition (its sink may retract), so only a dataflow
  reading an append-only source directly gets that rendering.

A GROUP BY mixing classes is planned as separate Reduces (one for the
accumulables, one for the hierarchicals, one per basic aggregate, such as
`string_agg` or `jsonb_agg`) joined on the group key; that join reads the
Reduces' output arrangements directly and adds none of its own.
Map/filter/project work fused into a Reduce leaves the output arranged (the
`Fused with Child Map/Filter/Project` line is printed under Get and FlatMap
nodes too, so by itself it is no sign of an arrangement); the fusion does not
happen when the projection emits a mapped column, as `avg` does, and the `Mfp`
left above the Reduce costs the next consumer a new arrangement.

**TopK.** The non-monotonic rendering arranges its input per hierarchy level
(`Arranged TopK input` in `mz_arrangement_sizes`) and keeps a reduced
arrangement per level (`Reduced TopK input`), keyed by (hash, group key); the
reduced arrangements hold the retractions of the rows the hierarchy does not
emit, once in total rather than per level and concentrated in the last levels,
near-full there whenever groups exceed the limit and empty when they fit inside
it. Like Reduce, no TopK rendering consumes an existing arrangement, so no
index can replace its input arrangement, and only `Monotonic Top1` leaves its
result arranged, so a join over the other two gets a printed Arrange. An MV's
output is never monotonic (see Reduce).

**Join implementations.** A DIFFERENTIAL join over more than two inputs
runs as a series of binary joins whose intermediate results are standing
arrangements, proportional to the intermediate sizes, which can dwarf
both the inputs and the output. A DELTA join maintains no intermediates:
it streams each input's updates against the other inputs' existing
arrangements, so its memory cost is exactly its input arrangements,
which shared indexes can supply. Reading this in `EXPLAIN ANALYZE
MEMORY`: the memory printed on a `Differential Join` operator line is
exactly the eliminable intermediate state; the input arrangements are
the separate Arrange lines below it, and those are kept under either
implementation. Which implementation the plan picked
(`type=differential` vs `type=delta`) often matters more than how big
the join is, and it can be changed: supplying the input arrangements as
indexes lets the planner pick a delta join ("Flipping differential joins
to delta", references/indexes.md).

**Consolidation.** A consolidating Union (printed `Consolidating Union`; the
planner marks a Union when any of its inputs is a Negate, so EXCEPT and the
outer-join lowerings carry one), the consolidation at a LetRec loop boundary,
and the input consolidation of monotonic reduces and TopKs hold updates in a
merge batcher until each update's timestamp completes, then emit them and keep
nothing: no maintained trace. Their memory still shows in
`mz_arrangement_sizes` (batcher records and bytes are summed into the same
`records` and `size` columns under the consolidating operator's id:
`UnionConsolidation` for a Union, `LetRecConsolidation` at a LetRec boundary,
`Consolidated ReduceMonotonic input`, `Consolidated MonotonicTopK input` and
`Consolidated MonotonicTop1 input` for the monotonic operators) and the row
disappears once the batcher drains. Normally that is a hydration-time
transient. It is standing state when a temporal filter feeds the consolidation:
every future-dated retraction is parked until its time arrives, one record per
live row for as long as the row lives. The near-term ones (within the
`compute_temporal_bucketing_summary` horizon, two seconds by default) sit in
the consuming operator's batcher and the rest in a separate `Temporal delay`
operator just ahead of it (temporal bucketing), which logs them the same way
under its own operator id. Temporal bucketing is on in Materialize Cloud, and
on self-managed and the emulator from v26.47. Older self-managed versions and
emulators run without it unless `enable_compute_temporal_bucketing` is set:
there is no `Temporal delay` operator, and every parked retraction sits in the
consuming operator's batcher.

### Memory beyond arrangements

This matters most at hydration. The persist sink at the end of every
materialized view stashes updates in a correction buffer until they are
written. At hydration that buffer holds the MV's entire snapshot (nothing is
written until the snapshot is complete), and the written copy is kept until
persist reads it back, so the sink's peak is two copies of the MV's output: it
scales with what the MV emits, not with what it reads or with the dataflow's
own arrangements, which are separate lines in the same census. A rehydration of
an existing MV peaks at the same two copies by another route: the sink writes
the difference between the recomputed output and what the shard already holds,
so it buffers both, with opposite signs, until they cancel.

The sink does not appear in EXPLAIN, but its buffer IS in the arrangement
introspection: the operator `mv_sink(<id>)::write` in `mz_arrangement_sizes`,
rolled into the dataflow and object totals. When an MV's own plan applies the
`mz_now()` predicate with nothing arranging or consolidating between it and the
sink (a filter-and-project MV), the buffer also parks every future-dated
retraction until its time arrives, one record per live row. A future-dated
retraction is parked exactly once, by the first time-batching operator after
the filter, so any intervening arrangement absorbs it instead, and a consumer
that reads the filtered view through an index or another MV never parks it at
all (its plan shows `ReadIndex` or the MV read, not the `mz_now()` Filter). A
sink line that stays big after hydration is therefore either pending
future-dated retractions (the line drains the moment they fire) or a write
backlog, the sink not keeping up with persist. A consolidation batcher line
reads the same way (see the Consolidation paragraph above).

What the arrangement sum misses around the sink: its in-flight batches being
appended to persist (only the `::write` buffer is logged, never the append) and
allocator overhead beyond the logged `size`, largest right after a rebuild.

To watch the sink buffer directly, read the `mz_persist_sink_correction_*`
metrics via `mz_introspection.mz_cluster_prometheus_metrics`
(`metric_name` column; cluster-wide counters and per-worker high-water
gauges, no per-sink label).

A replica's total heap (`heap_bytes` in
`mz_internal.mz_cluster_replica_metrics`, RAM plus swap) therefore exceeds its
arrangement sum, and post-hydration arrangement totals understate the peak
twice over: they miss that gap, and the arrangements themselves peak at
hydration, when each merge batcher holds the entire snapshot until the first
seal, and trace merges (the batch merging inside an arrangement) transiently
hold both source batches and their merged output (one index export measured
4.4x its settled size twelve seconds after its build). That is why replicas are
sized from the measured whole-cluster hydration peak (see "Making changes",
below), never from arrangement totals. The lever for a peak dominated by one
MV's sink is in the lever table ("MV hydration spikes").

Read `heap_bytes`, not `memory_bytes`, for that comparison. On Cloud and with
the self-managed defaults, replicas run with swap enabled and no scratch disk,
so arrangements are ordinary swappable heap: `memory_bytes` counts resident RAM
only and can fall below the arrangement sum once cold pages are paged out,
`heap_limit` is the enforced RAM-plus-swap ceiling, and `disk_bytes` there
reports swap, not disk. Treat swap as transparent unless there is so much of it
that hydration time or freshness suffers. Under the process orchestrator (the
emulator, and a local environmentd) the orchestrator reports NULL for
`heap_bytes`, `heap_limit` and `disk_bytes`, so `memory_bytes` is all you get;
it counts resident RAM, and a container on a host with swap enabled can still
page out, so a falling `memory_bytes` there is not by itself freed memory.
`mz_internal.mz_cluster_replica_utilization` reports the same readings as
percentages of the replica's allocation (`cpu_percent`, `memory_percent`, and
`heap_percent`, which is `heap_bytes` over `heap_limit`), the quickest headroom
read.

## Workflow

Work top-down. The numbered order is the default shape of an
engagement, not a script. Skip or reorder steps when the evidence points
elsewhere, except two load-bearing orderings: hints before attribution
(step 2) and estimates before builds (step 5).

1. Census. Confirm the cluster is hydrated ("Reading introspection"), then rank
   dataflows by size: `mz_introspection.mz_dataflow_arrangement_sizes` on the
   target cluster. This tells you where the memory is; nothing else in the
   workflow makes sense before it. Rank by size to order the work, but keep the
   census complete: the duplication probe of step 3 clusters every arrangement,
   since the same small arrangement built in twenty dataflows is a large total,
   and every object a proposal names gets measured whatever its size.
2. Hints early. Query `mz_introspection.mz_expected_group_size_advice` on the
   target cluster first: one read lists every operator on the cluster with a
   hint recommendation and its reclaimable savings. Then run `EXPLAIN ANALYZE
   HINTS FOR MATERIALIZED VIEW <mv>` (also `FOR INDEX`) on the dataflows where
   the savings are substantial, to place each hint. It is cheap, needs no logic
   change, and comes first because oversized hierarchies inflate the masses
   every later step attributes. The single biggest hint win is usually an
   un-hinted min/max, which silently defaults to an 8-level hierarchy (an
   un-hinted `DISTINCT ON` or per-group `LIMIT` TopK defaults to the same
   eight). Details: [references/hint-sizing.md].
3. Attribute before choosing a lever. The same headline number can be
   hierarchical aggregates holding their full input, raw re-keyed arrangements,
   expand-then-collapse join products, or payload bytes riding through
   arrangements, and each needs a different lever. The operator table in the
   cost model says what each operator retains; the reference files refine it
   (what a hierarchy level of a min/max or TopK costs, width and
   key-amortization effects, the packed-row state of window functions,
   temporal-filter retraction copies). Per-operator attribution: `EXPLAIN
   ANALYZE MEMORY FOR MATERIALIZED VIEW <mv>` (or `FOR INDEX <idx>`; those are
   the only two explainees), or `mz_introspection.mz_arrangement_sizes` joined
   to `mz_dataflow_operator_dataflows`. Standard probes on the big masses:
   - Bytes/row sweep: size ÷ records per operator. Rows of keys and scalar
     columns cost about 15 to 50 B/row arranged (three integers 17, a uuid and
     an integer 25, an integer with a timestamp and a 32-character string 50);
     an outlier far above that fingerprints a payload column riding the
     arrangement (a 200-byte `jsonb` document reads at about 230). Skip small
     arrangements: each carries a fixed floor of a couple of hundred bytes per
     worker (about 4.5 kB on a 16-worker replica), which dominates the ratio
     below a few hundred records.
   - Cross-dataflow duplication: cluster all sized arrangements by record
     count, within a few percent. Near-identical counts are the tell for one
     collection arranged in several dataflows even when keys, names, and
     projections differ; resolve each cluster in the plans before treating it
     as one. The tolerance exists because readings of one collection are logged
     asynchronously per operator, and `records` includes un-merged batches
     whose insert/retract pairs cancel only on merge; the exact percentage is
     empirical.
   - Intra-dataflow twin census: within each big dataflow, list arrangements
     sharing a key and record count but differing in width (the key is read
     from the operator's name, `ArrangeBy[[Column(0, "k")]]`, in
     `mz_dataflow_operator_dataflows` joined on `operator_id`;
     operator-internal arrangements carry no key in their name and need the
     plan). These are usually per-consumer projection divergences that defeated
     common-subexpression sharing. Do this as its own pass; it does not fall
     out of the cross-dataflow view.
   - Cardinality probes: rows vs distinct join-key pairs vs distinct
     group keys, which size an index candidate and estimate join pair
     mass before any rebuild (the quadratic-join shape, below).
   - Stuck projection pushdown: `EXPLAIN OPTIMIZED PLAN WITH (arity)` on
     dataflows whose big arrangements are wider than their consumers
     read; the blockers and the fix are one lever (below).
   - Worker skew: `EXPLAIN ANALYZE CPU WITH SKEW FOR MATERIALIZED VIEW <mv>`
     (or `FOR INDEX`) when one worker seems to carry a dataflow. It prints one
     row per operator per worker (`worker_id`, `cpu_ratio`, `worker_elapsed`,
     `avg_elapsed`, `total_elapsed`); the operator's max `cpu_ratio` is its
     skew. The counters are cumulative from operator creation, so a reading
     during hydration measures hydration and a reading afterwards still
     contains it; steady-state skew is the difference of two readings. Mapping
     a measured row or plan operator back to its SQL clause is its own section
     below ("Mapping measurements back to SQL").
4. Classify each big mass with the lever table below. Report the masses
   a lever can help; the rest stays in your notes (ground rules).
5. Estimate before implementing. From the attribution, estimate each
   candidate's saving (what you remove minus what you add) with a stated
   confidence (the formulas per lever, and what to do with a wide interval, are
   under "Adjudicating proposals and estimating"). Width math (bytes/row on
   both sides; the model is in references/indexes.md) and plan reasoning gate
   the experiment, for every index candidate, your own proposals included, not
   only the ones you were asked to judge; the measured build settles it (ground
   rules). Adoption and plan-shape questions can be settled for free on a
   data-free rig first ([references/indexes.md]); size questions need the
   experiment cluster. Gate implementation on estimated value vs effort and
   risk, and leave complex rewrites as designed-and-estimated proposals when
   they do not clear the gate.
6. Measure on the experiment cluster (see "Making changes"): build the
   candidate, compare against the baseline, verify exactness, record the
   number and each dataflow's hydration time (Landmines: an enabling
   index can flip a join onto a hot key).
7. Hand over: the estimated-vs-measured table (see "Adjudicating proposals
   and estimating"), accepted changes expressed in the user's source of truth,
   and the realization step: the replica resize, sized to clear the measured
   full-hydration peak rather than the steady state (see "Final evaluation and
   sizing" under "Making changes"), and the cleanup checklist.

## Mapping measurements back to SQL

Mapping measurements back to SQL takes two hops. The first hop, measured row to
plan operator, is exact. Each row of `EXPLAIN ANALYZE` is one operator of the
default `EXPLAIN` (the physical/LIR plan), but not in the same order: the rows
are sorted by LIR id descending, so a multi-input operator's children come out
reversed relative to the plan text; the plan text also has lines with no row
(`Fused with Child Map/Filter/Project`), the With/Return scaffolding is folded
into labels (`With l0 = <op>`, `Returning <op>`), relations print as ids (`Read
u20`) rather than names, and some labels differ (`Differential Cross Join` in
the plan is `Differential Join` in ANALYZE). So never map rows to operators by
position: `EXPLAIN PHYSICAL PLAN WITH (node identifiers)` annotates every
operator with its `LirId`, the same ids `mz_introspection.mz_lir_mapping` keys
by (with raw operator-id ranges per node; its `global_id` is a transient id,
bridged from the object name through `mz_introspection.mz_mappable_objects`),
and a measured row joins its plan operator by that id. The second hop, plan
operator to source clause, has no id to follow, and operator labels are generic
and repeat, so map it by landmarks: the column names the plan prints (`#2{col}`
annotations in group keys, order-by lists, join equivalences, filters; derived
columns print as bare `#n`, and names can be lost across projections), the
feeding join's complete key set (a three-relation chain is a different CTE than
a two-relation one on the same column), sibling aggregates (a `min` beside a
`count(*)` is a different clause than a lone `min`), the relations the operator
reads, distinctive constants, and the current hint value (`exp_group_size=N` on
the operator in `EXPLAIN OPTIMIZED PLAN`; a value unique in the view pins its
clause). A single landmark is a hypothesis; confirm it with the full key set
and the siblings. When that leaves a mapping below about 97% certain, make it
certain with a marker: put the view's text into `EXPLAIN OPTIMIZED PLAN FOR
SELECT ...`, give the suspected clause a distinctive hint value (`OPTIONS (...
INPUT GROUP SIZE = 1234)`), and the one operator whose `exp_group_size` changed
is that clause. One EXPLAIN, no hydration, any hint-taking clause (min/max,
`DISTINCT ON`, per-group `LIMIT`); for an operator without a hint clause, mark
a hint-taking neighbour in the same CTE and read the subtree around it. Two
things to know about markers: two clauses that are byte-identical, hint
included, are ONE operator in the plan (the optimizer shares the subtree), so
HINTS reports one row for both and both clauses get the same edit, and a marker
on one of them splits them, which is diagnostic, not a problem; and a hint's
trace in the physical plan is coarser (a min/max prints only its bucket list,
the 16^n bracket, a TopK prints nothing), so read markers and current values in
the optimized plan. Anchor every edit by content, never by line number: SQL
read back from the catalog is the engine's re-rendering, so line numbers will
not match the user's source. Structurally identical clauses that want the same
value get one collective instruction. references/hint-sizing.md uses this
technique for hint clauses; it works for any operator.

## Lever table

Dispatch from measured signatures to levers. Each reference file
carries the full method, verification steps, and worked examples.

| Signature | Lever | Details |
|---|---|---|
| HINTS reports savings; un-hinted min/max (levels=8, no exp_group_size) | Re-tune or add GROUP SIZE hints | [references/hint-sizing.md] |
| Same (collection, key) arranged in 2+ dataflows | Shared index; slim projection view + index when the base is wide | [references/indexes.md] |
| Recurring composite re-key that no existing index serves | New boundary view at exactly that (collection, key, column-union) + index, repoint consumers | [references/indexes.md] |
| One dataflow, two big arrangements, same key and count, different widths | Union-width view + index (intra-dataflow twin) | [references/indexes.md] |
| Expensive computed view consumed by 2+ dataflows | Index the computed view; dedups the whole computation and pays off even when consumers read it unkeyed | [references/indexes.md] |
| Three-or-more-input `type=differential` join whose Differential Join line carries big memory (the intermediates) | Index the extra probe keys the delta paths lack so the planner flips it to a delta join | [references/indexes.md] |
| Temporal-filtered view (mz_now window) read by several consumers | Index the shared temporal-filtered view (N private copies become 1, and consumers that carried the `mz_now()` predicate themselves stop parking retractions in their sinks) | [references/indexes.md] |
| Bytes/row outlier (payload riding arrangements) | Extract-in-place payload slimming (below) | inline |
| Reduce or arrangement carrying columns no consumer reads | Dead-column narrowing (below) | inline |
| DISTINCT over more columns than its consumers read (often `DISTINCT *` in a shared view) | Stuck projection pushdown (below): drop a redundant DISTINCT, or narrow its column list | inline |
| DISTINCT ON pick plus a sibling max/min over the same relation and key | Argmax redundancy (below): delete the redundant max/min aggregate, read the value from the pick | inline |
| LEFT JOIN whose right side provably always matches and carries no key the optimizer knows | Convert to INNER via one of the two provable guarantee classes (with the key known the diamond is already gone and the conversion buys nothing); no census signature, so hunt for it on every rebuild | [references/outer-joins.md] |
| Wide Distinct over ALL columns of a join side plus a full-width self-join (general outer-join lowering) | Stuck projection pushdown (below): pre-project the preserving side, or rewrite the ON to a plain equi-join | [references/outer-joins.md], "The pushdown gaps" |
| A stack of 2+ LEFT JOINs lowered per join (`n` differential joins with a matched-key Distinct each, no `Threshold`) instead of one delta join | Restore the VOJ (variadic outer join) lowering (move inner joins out of the stack, `ON` instead of `USING`, local predicates and expressions into derived tables, decorrelate) when the match rate and the right sides' keys clear the crossover in the reference | [references/outer-joins.md] |
| Window function (OVER/PARTITION BY) with wide rows or hot partitions | Stuck projection pushdown (below): narrow the window's input relation (memory); the incremental rewrites (DISTINCT ON, min/max, the LAG/LEAD self equi-join) buy freshness and can cost memory | [references/window-functions.md], "The projection-pushdown blocker" |
| `CrossJoin`, or a `Distinct` and `ArrangeBy` keyed on the outer relation's own columns, feeding a join back to it (a decorrelated subquery), or any form in the SQL triage list of "Query shapes to recognize" | Manual decorrelation: nine rewrite patterns, each with its exactness rule | [references/subqueries.md] |
| Index or MV that nothing reads | Drop it, with the pinning procedure (below) | inline |
| Replica's hydration peak dominated by `mv_sink(<id>)::write` buffers of one or two huge MVs | Split the MV into smaller MVs ("MV hydration spikes" below; last resort) | inline |

Inline levers:

**Extract-in-place payload slimming.** Materialize pushes column projections
down aggressively, through TopK and Reduce, into a join's inputs, and into the
source read, but it never moves a scalar EXPRESSION: a `Map` stays where the
query put it (fused into the source read only when it already sits directly
above it), above TopK, Reduce and Join alike, so a jsonb/text blob joined first
and unpacked later is demanded whole by every operator between the source and
the extraction point, the join's input arrangements and TopKs included. Fix at
the point where the payload first enters the pipeline: extract exactly the
consumed fields in the first view that reads the source relation (the scan or
wrapper view, whatever the pipeline's first layer is called), so picks,
hierarchical aggregates, and joins carry only slim columns. Prefer this over a
fetch-back join (slim the pipeline, then re-join the fat relation at the end):
the fetch-back re-arranges the fat relation by the fetch key, a full-width
arrangement that costs back most of the saving when the pipeline you slimmed
held only a copy or two. Extraction expressions are deterministic per row, so
evaluating them earlier is outputs-identical as long as they cannot fault: a
cast, division, or subscript that errors on a row a later filter would have
discarded poisons the whole collection and every consumer of it. Guard such an
expression with the downstream predicate (`CASE WHEN <pred> THEN <expr> END`),
and seed the two-way `EXCEPT ALL` proof (see "Verification discipline", below)
with a row that would fault.

**Dead-column narrowing and compact types.** A reduce keyed wider than
its consumers read, or a GROUP BY carrying columns no consumer uses,
retains dead bytes in every group. Narrow the GROUP BY or the carried
columns to what is actually consumed. A column used only as `IS NOT
NULL` can be narrowed to a boolean at the scan. Relatedly, narrow the
representation: text that is really a UUID casts to `uuid`, text
booleans to `boolean`, small fixed string vocabularies to small integer
codes. (Casting between integer widths rarely saves memory: integer
storage is already value-sized.) These are outputs-changing at the
column-type level, so they apply inside pipelines, with the consumer
contract preserved at the pipeline's outputs; prove exactness at the narrowed
sites with the two-way `EXCEPT ALL` proof.

**Stuck projection pushdown (manual projection).** The optimizer pushes
projections down until it meets a construct that demands its full input width,
and everything below that point then carries every column, however few the
consumer reads. Four constructs do this: window functions (their three-operator
gadget, see references/window-functions.md, packs the window's whole input
scope), the general outer-join lowering (it equates every preserving column),
`DISTINCT` (every listed column, so `DISTINCT *` in a shared view arranges the
full width inside each consumer), and a surviving `Threshold` (the
implementation of `EXCEPT`, `EXCEPT ALL`, and `INTERSECT`, keyed by the whole
row). An indexed view is a fifth, deliberate one: the index holds the full
width of its view, whatever its readers project (its remedy is the slim
projection view of indexes.md). One diagnostic serves all of them: `EXPLAIN
OPTIMIZED PLAN WITH (arity)` annotates every operator with its column count,
and a region whose arity stays far above the columns the output reads, and
above what the region itself consumes (partition and order columns, join keys,
the distinct list), is a stuck projection. One fix shape serves the first four,
in two flavors: project manually just below the blocker (wrap the window's
input in an explicit projection; pre-project the preserving side of the outer
join; apply the DISTINCT to exactly the columns needed, at the consumer; narrow
both operands of the set operation), or remove the blocker (rewrite the window
function to an incremental form, references/window-functions.md; rewrite the ON
to a plain equi-join, references/outer-joins.md; drop a redundant DISTINCT;
move the set operation). Exactness differs: the manual projection is
outputs-identical for windows and outer joins when the dropped columns reach no
output, while narrowing a DISTINCT changes the result unless the dropped
columns are functionally determined by the kept ones, so state that delta and
let the user decide. A DISTINCT is redundant, and already elided, when the
optimizer knows a key contained in its column list (`EXPLAIN OPTIMIZED PLAN
WITH (keys)`); when the uniqueness is only semantic, make the key known (a
keyed boundary, references/outer-joins.md) or prove it with a count versus
count-distinct probe before dropping it.

**Argmax redundancy.** A `SELECT DISTINCT ON (k) ... ORDER BY k, v DESC` pick
makes a sibling `max(v) ... GROUP BY k` over the same relation provably
redundant when `v` is the first ordering term after the key and is not null, or
when the pick spells `v DESC NULLS LAST`: the pick's first row already carries
the maximum (with another column ordered before `v`, the pick is not an argmax
at all). The condition is about NULL placement, since the default for DESC is
NULLS FIRST, which returns the NULL that `max` skips. Deleting the whole max
aggregate and reading the value from the pick is exact; prove it with the
standard two-way `EXCEPT ALL`.

**Dead objects and the pinning procedure.** An MV nobody reads is a
whole-dataflow drop; confirm it is unconsumed several independent ways (no
downstream objects, no serving reads, ask the owner) before touching it. For a
dead index, establish adoption before any DDL, never by dropping it to see what
happens: `mz_internal.mz_compute_dependencies` lists every dataflow that
imports the index (rows whose `dependency_id` is the index; other indexes count
as adopters too, and the catalog-level `mz_object_dependencies` never shows
index adoption), the stored plan's `Used Indexes` footer confirms it per
consumer, and `mz_introspection.mz_arrangement_sharing` is the live refcount of
the index's trace, which counts the consumers that read it as an arrangement
and not those that full-scan it, so a count of 1 is no evidence that nothing
reads it. Dropping the index then prints a NOTICE naming dependent objects.
That NOTICE means the index dataflow stays alive and maintained until every
named dependent is rebuilt (or altered, or environmentd restarts, which replans
an object whose dependencies changed and so drops the pin). It does not mean
the index is needed, and it does not mean the drop failed. No NOTICE means
nothing had adopted the index and the drop freed the dataflow at once. Plans
adopt indexes at CREATE time, so the full procedure is: drop the index, then
rebuild every consumer the NOTICE names, then verify no zombie dataflow remains
(the query below lists every maintained dataflow whose export is no catalog
object; a pinned consumer's `EXPLAIN` footer prints the dropped index as
`[DELETED INDEX]`, the cheapest per-consumer check). Dropping alone frees
nothing once the NOTICE names a dependent.

```sql
-- zombie dataflows: still maintained, exporting no catalog object
SELECT d.name FROM mz_introspection.mz_dataflows d
WHERE d.name LIKE 'Dataflow: %.%.%' AND NOT EXISTS (
  SELECT 1 FROM mz_introspection.mz_compute_exports e
  JOIN mz_catalog.mz_objects o ON o.id = e.export_id
  WHERE e.dataflow_id = d.id);
```

**MV hydration spikes (the persist sink).** When one or two huge MVs dominate a
cluster's hydration peak (each sink buffers roughly two copies of its MV's
output at the peak; cost model), the lever is to break the MV into several
smaller MVs (by key range, or by splitting rarely-joined column groups apart),
so that no single snapshot is buffered whole and the pieces' peaks do not all
coincide. This is tedious (consumers must be repointed or reunited with a UNION
ALL, and the object graph changes) and it only lowers the peak when the pieces
hydrate at different times. Materialize hydrates up to four dataflows
concurrently by default, so splitting into fewer than about four pieces changes
little and simultaneous sink buffering stays bounded by roughly four pieces'
worth. That four is the `compute_hydration_concurrency` setting, and lowering
it is the direct alternative to splitting. Only the Cloud flag service can
target one replica with it, and Cloud users cannot set system parameters
themselves, so they ask Materialize; a self-managed operator sets it with
`ALTER SYSTEM SET` as `mz_system` or through the system-parameters ConfigMap,
and either way the new value applies to every replica in the environment.
Recommend either only when the sink spike is the biggest thing hurting the
cluster's memory, established two ways: during a hydration (a replica restart
produces one on demand), the `mv_sink(<id>)::write` lines in
`mz_arrangement_sizes` (and the `mz_persist_sink_correction_*` high-water
gauges) show the buffers; and independently of hydration, measure each MV's
output size directly:

```sql
SELECT sum(mz_row_size(mv.*)) FROM mv;   -- bytes of the MV's rows,
                                        -- per-row overhead included
```

`mz_row_size` takes the row record (`mv.*` or just `mv`; do not wrap that
whole-row reference in `row(...)`, which nests a record and adds a header per
row). A row whose packed bytes fit the 23-byte inline buffer reports a flat 24
bytes, and a longer row reports its packed length plus that 24-byte overhead.
Two copies of that total is the sink's expected hydration contribution, as an
order of magnitude (arrangements store rows in a different representation, so
it is not byte-exact); compare it against the arrangement totals and the
measured `heap_bytes` peak before choosing this lever.

## Query shapes to recognize

Three SQL shapes plan into far more state or work than they read as.
Look for them during attribution, in the plan and in the SQL, before
choosing levers.

**IS NOT DISTINCT FROM in a join condition.** On nullable columns, when it is
the join's only usable condition, it plans as a cross join with a post-filter:
both inputs arranged with an empty key, everything on one worker (on NOT NULL
columns it simplifies to `=` and stays an equi-join, and beside a real equality
it becomes a post-filter over an ordinary equi-join). The default `EXPLAIN`
shows it as `Differential Cross Join` over `Arrange (empty key)` inputs and the
optimized plan as `CrossJoin`, so grep for either label in its plan text; note
that `mz_lir_mapping` and EXPLAIN ANALYZE label the same operator a plain
`Differential Join`, where worker-elapsed skew is the tell. Rewrite to plain
equality, or, when NULL matching is intended, to `a.k = b.k OR (a.k IS NULL AND
b.k IS NULL)`, which is exact and which the planner turns back into an
equi-join (then keyed on a nullable column: run the closure audit in
"Landmines").

**Quadratic joins (cross joins and skewed keys).** A join with no usable
equality condition, or an equality on a low-cardinality or heavily skewed
non-unique column, produces pair volumes far above either input, and every pair
for one key is produced on that key's one worker. The typical presentation is
time, not memory: hydration that never finishes, or a rebuilt MV grinding for
hours on one worker while memory stays flat (a downstream filter or collapse
discards the pairs after they are produced). The defense is the pre-build
probe, because a grinding replica is hard to inspect after the fact: before
building or rebuilding any join, estimate the pair mass from distinct-key
counts and the top per-key frequencies on both sides (the sum over hot keys of
left-count times right-count); a result orders of magnitude above both inputs
is a stop sign, not a tuning problem. On a live but responsive cluster,
`EXPLAIN ANALYZE CPU WITH SKEW` exposes the per-worker elapsed per operator,
and a true cross join shows as `Arrange (empty key)` inputs in the default
`EXPLAIN`; an empty key hashes to one worker, so every cross join on a replica
runs on that same worker and several of them stack up there. During a heavy
grind, replica-served introspection may not answer at all; that
unresponsiveness combined with one busy worker is itself the signature.

**Subqueries decorrelate into joins keyed by the outer columns.** A subquery
that reads a relation, sits inside a `CASE`, or is more than Map, Filter,
Project, and table-function calls is lowered into a `Distinct` over the
correlation key, the subquery computed once as a dataflow, and a join back on
that key, or a `CrossJoin` when nothing correlates; the cost is that join's
arrangements plus the subquery's own operators, which hold one group per
distinct outer value when the outer keys are joined in below an aggregate or a
`LIMIT`, never a re-execution per outer row. The memory is every arrangement
keyed by the correlation key (the join-back pair, the `Distinct` over the key,
the subquery's own), at that key's width, so the expensive shapes are a
subquery correlated on a payload column (`jsonb`, `list`, `array`, long
`text`), a subquery inside an outer join's `ON` (the key is every preserving
column), and the nullable cases (`NOT IN`, `IN` outside a filter conjunct)
whose outer keys seed a `CrossJoin`. In the plan, look for a `CrossJoin`, or a
`Distinct` plus `ArrangeBy` keyed on the outer relation's own columns (all of
them, or a payload column), feeding a join back to it. In SQL, look for `NOT
IN` on a nullable side, `IN`/`ANY` on a nullable comparison outside a filter
conjunct (`WHERE`, an inner join's `ON`, `HAVING`), an `IN` over a subquery
that aggregates or uses `LIMIT` (even in `WHERE`), a subquery in an outer
join's `ON`, `= ANY(<collection column>)`, and a scalar or `LATERAL ... LIMIT
1` subquery correlated only on the current row. The full signature list, the
nine rewrites with their exactness obligations, what the optimizer already
handles, and what no rewrite fixes are in [references/subqueries.md].

## Landmines

Hazards of the changes this skill makes. Run these checks before
shipping any index package or rebuild, not only at sites that already
misbehaved.

**The nullable-key closure audit.** An index on a nullable key column arranges
the whole NULL population under one key, on one worker. Private arrangements
are safe: the planner puts an `IS NOT NULL` filter below them, so NULL rows
never enter the join. A shared index cannot have that filter below it (pushing
it down would forfeit adoption), so the planner hoists the guard above the
join. Any join on that key then pairs the whole NULL population of one side
against the other's (a self-join squares it), on one worker, and discards the
product afterwards. Symptoms: one worker grinding for minutes to hours while
the rest idle, flat memory (produce-discard retains nothing), replica
introspection unresponsive. The audit: for every index and MV in the package,
read `EXPLAIN PHYSICAL PLAN AS VERBOSE TEXT`; in each join stanza, flag `IS NOT
NULL` filters sitting in the closure region (between the join line and its
input operators) whose columns are that join's arrangement key. A filter below
an arrange is the safe placement, not a hit. Confirmation without plan reading:
the NULL population shows as a record-count excess on exactly one worker in
`mz_arrangement_sizes_per_worker`. Fix, in the order the pinning procedure
requires ("Dead objects" above, "Making changes" below): drop the raw
nullable-key index (so no future consumer can re-arm the landmine and so the
new index does not adopt it), create a passthrough view `WHERE key IS NOT NULL`
and index that, then rebuild every consumer the NOTICE names.

**An enabling index can flip a join onto a hot key.** New shared indexes
change join implementations, not just share state: with all inputs
pre-arranged the planner flips linear chains to delta plans, and a delta
path that streams through a high-fan-out lookup funnels that key's
traffic through one worker, at hydration and in steady state, which can
turn a minutes-long hydration into a many-hours grind. After adding
indexes, check `EXPLAIN OPTIMIZED PLAN WITH (join implementations)` on the
big consumers and inspect delta paths whose stage keys can fan out, and
compare every rebuilt dataflow's hydration time with its pre-change one
(`mz_internal.mz_compute_hydration_times`); the verification rules in
references/indexes.md carry the mitigation.

**A dropped or replaced index can leave a zombie dataflow.** Plans adopt
indexes at CREATE time, so a new index adopts the old one and DROP INDEX leaves
the old dataflow maintained until every consumer the NOTICE names is rebuilt (a
same-version restart keeps every cached plan except those of objects whose
dependencies changed, such as a dropped index's dependents, which are replanned
against the current catalog and adopt whatever indexes exist then; an upgrade
or an optimizer-flag change replans everything). The drop-create-rebuild-verify
order in "Making changes" is the guard.

## The index advisor is one input, never ground truth

`mz_internal.mz_index_advice` reasons only over the object dependency
graph. It has no notion of sizes, column widths, key correctness, or
external consumers:

- Its 'add index' rows are width-blind. On a wide view they can
  recommend an index whose full-width arrangement washes out or exceeds
  the narrow private copies it would replace. Size both sides first.
- Indexes on tables are invisible to it. It will never tell you to drop
  one, however large and dead.
- It only propagates advice along chains under sinks or indexed
  objects. Everything under a plain, un-indexed materialized view is
  silently absent from its output.
- Its MV-demotion rows ('convert to a view', with or without an index)
  see catalog dependencies only, other clusters' maintained objects
  included; they cannot see readers that are not catalog objects (ad
  hoc SELECTs, SUBSCRIBEs, dashboards, applications). Converting a
  serving MV on such advice breaks contracts the advisor knows nothing
  about.

Consequently: adjudicate every advisor row with a measurement, and
never treat its silence as evidence.

## Adjudicating proposals and estimating

When a fix list needs verdicts, whether from a colleague, the advisor,
or your own earlier pass:

- One verdict per item: adopt, modify, or reject, each with its
  measurement (ground rules). "Modify" is a first-class verdict; the
  most common cases are the right key on the wrong, too-wide object,
  and a literal filter column folded into the join key, which makes an
  index that serves neither (references/indexes.md,
  index key correctness).
- Before endorsing an index on a shared relation, run the closure audit and the
  width math. Before endorsing a drop, check adopters
  (`mz_compute_dependencies`, the stored plan's footer) and external consumers.
  Treat every unmeasured item as unproven; a typical unreviewed list contains
  correct keys, wrong keys, redundant items, and at least one actively
  dangerous one.
- Estimates come from per-operator attribution: a dedup saves the sum
  of the private copies you remove minus what you add; a hint retune
  saves the advice view's estimated savings for the operator, confirmed
  by measuring after the retune; a slimming saves delta-bytes/row times
  records times copies. State a confidence per
  number. An interval that stays wide is a method problem: narrow it by
  attributing further, not by re-asserting it. If a number cannot be
  tightened, name the unknown quantity and the experiment that would
  pin it.
- A rewrite that relies on a data property (a window bound, a
  uniqueness the optimizer cannot see, a match rate, a column that is
  never NULL) gets that property derived, never assumed: a probe
  establishes it, then state it, verify it, and record the guard rule
  that keeps it true.
- Report estimated vs measured for everything implemented, in one
  table, and retract cleanly any number that measurement refuted.

## Making changes

Who executes what, and where:

- Diagnosis: read-only, anywhere; catalog, introspection and EXPLAIN reads need
  no permission, reads of the user's data do (ground rules).
- Experiments: on a dedicated experiment cluster that the user creates.
  Propose it with an intended replica size and expected lifetime, and
  hand the user the commands, for example:

  ```sql
    CREATE CLUSTER optimize_experiments (SIZE = '<size>');
  ```

  Run these yourself only if the user explicitly asks. A standing cluster costs
  credits on Cloud and node capacity anywhere else, and one the user created
  does not get forgotten. `CREATE CLUSTER` fails with `creating cluster would
  violate max_clusters limit` on an environment already at its limit; the limit
  is raised by Materialize on Cloud and by the operator on self-managed, so
  report it to the user rather than working around it.
- Object DDL inside the experiment cluster, two options (MCP cannot
  write; offer both and let the user pick):
  1. A direct SQL connection for a restricted role whose DDL surface is exactly
     the experiment cluster and an experiment schema (`GRANT CREATE, USAGE ON
     CLUSTER optimize_experiments TO <agent_role>`, the same on the experiment
     schema, plus USAGE on the production schemas and cluster (PUBLIC has the
     cluster's by default, hardened environments revoke it) and SELECT on the
     objects being compared). `CREATE INDEX` requires OWNERSHIP of the indexed
     object, so this role cannot index a production MV directly: create a view
     over it in the experiment schema, index that view, and have the candidate
     consumers read the view. The role cannot build anywhere else (CREATE is
     granted nowhere else) and cannot alter or drop any cluster (ownership
     gates those, and the user owns the experiment cluster). All of that holds
     only while `enable_rbac_checks` is on, which is the Cloud default but not
     the self-managed or emulator default, and only while the role is neither a
     superuser nor a member of the role that owns the production objects; where
     the checks are off, option 2 below is the only real containment.
  2. You write self-contained SQL scripts that the user executes, and
     you measure read-only over MCP. No new credentials, at the cost of
     a user round-trip per build iteration.

  Either way the experiment role needs nothing beyond SELECT on production
  objects and USAGE on their schemas and cluster. Applying accepted changes is
  a separate phase with separate privileges, and it is the user's, through the
  source of truth.
- Deployment of accepted changes: ask where the source of truth for object
  definitions lives (mz-deploy, dbt, custom scripts, or the catalog itself) and
  express the changes there. The mz-dbt and mz-deploy skills cover
  those tools. Full-rebuild deployment tools recreate all objects together,
  which dissolves most of the pinning hazards below; what survives everywhere
  is index-before-MV ordering within the deploy. After an incremental deploy
  (only the changed objects rebuilt), have the user run the restart check of
  the final evaluation below on the production cluster, at a time a rehydration
  is acceptable, to confirm the headroom the resize leaves; a full-rebuild
  deploy that hydrates the new generation on its own cluster is that check
  already (read the peak from that replica's gauges and history).
- The replica resize at the end is likewise a recommendation for the
  user to execute.

**Final evaluation and sizing.** A cluster's memory peak is normally at
hydration, when everything rebuilds at once, which a restart, a redeploy or an
upgrade does in production; upgrades roll out on Cloud automatically and the
platform reschedules replicas, so the peak is a routine event, not one the user
can avoid by never restarting. Two things make the peak. Arrangement state:
plan for at least 2x its steady-state footprint even where the measured
hydration peak is smaller, since Materialize's engineering treats a 2x
hydration spike as acceptable and any release can move a cluster's spike up to
that without notice. Materialized-view sinks are outside that rule: each
buffers about two copies of its MV's output at hydration (cost model), on top
of the arrangement peak and unrelated to the steady state, and drains
afterwards, so this share exists only while a hydration runs and a replica
restart is the only way to produce another one.

Therefore the final evaluation of an accepted change set rehydrates the whole
final state at once: restart the replica of the experiment cluster that holds
it (set a managed cluster's `REPLICATION FACTOR` to 0 and back, or drop and
recreate the replica of an unmanaged one), or build the final set from scratch
on a fresh experiment cluster, and record that hydration's peak. Rebuilding
only the changed dataflows understates the spike a production rehydration will
produce, so a change aimed at the peak, or able to raise it (a new index, a new
boundary), is measured by rehydrating the whole experiment cluster as well.

Read the peak from `mz_internal.mz_cluster_replica_metrics_history` as
`heap_bytes`, RAM plus swap, since `memory_bytes` reads flat once swap absorbs
a spike (under the process orchestrator, the emulator and a local environmentd,
no `heap_bytes` exists and `memory_bytes` is the only peak available);
`mz_cluster_replica_metrics` is a point-in-time reading and misses a peak that
has passed, and the history is sampled once a minute per replica, so treat a
single high sample as a lower bound. For the sink share read also the
`mz_persist_sink_correction_max_per_sink_worker_*` high-water gauges in
`mz_cluster_prometheus_metrics`, which keep the peak after the buffer drains,
while the `mv_sink` line is often gone before a busy replica's introspection
reports it.

Two numbers set the size: the steady-state `heap_bytes`, of which the replica
needs at least 2x whatever the experiments showed, and the measured
whole-cluster hydration peak of `heap_bytes` (RAM plus swap), which must stay
at or below roughly 90% of `heap_limit`, the enforced RAM-plus-swap ceiling
(`mz_cluster_replica_metrics.heap_limit`; `heap_percent` in
`mz_cluster_replica_utilization` is that ratio); recommend the larger of the
two resulting sizes. Read the column, never a remembered ratio: how far
`heap_limit` sits above a size's RAM differs by replica family and deployment
and changes without notice; on self-managed with swap enabled the ceiling comes
from the pod's cgroup memory and swap limits; under the process orchestrator
the column is NULL and this check is unavailable. Swap is mostly transparent;
it matters only when heavy swapping slows hydration or freshness, which shows
up as hydration time and lag, not as a memory failure.

Replicating objects onto the experiment cluster: capture definitions
with `SHOW CREATE ...`, whose output is plain SQL with names resolved;
change its `IN CLUSTER` to the experiment cluster and replay. A
materialized view's `create_sql` catalog column ends in an `AS OF`
timestamp that `CREATE` rejects; strip it and the rest replays, but its
id annotations (`[u123 AS "db"."sch"."name"]`, `IN CLUSTER [u1]`) bind
by id and ignore the name, so it replays only inside the same
environment.

Mechanics that hold whenever objects are built or replaced by hand
(experiment clusters, and environments deployed by raw SQL scripts):

- Plans are fixed at CREATE time and cached across same-version restarts: an MV
  or index does not adopt an index or hint added after it was created until
  something replans it (an upgrade or an optimizer-flag change replans
  everything, a same-version restart only the objects whose dependencies
  changed), so changing a plan on demand means DROP and CREATE of the
  consumers, indexes first, then MVs.
- Every rebuild changes adoption. After any DROP or CREATE, re-read adoption
  (`mz_compute_dependencies`, the stored plan's footer) and the replica numbers
  before restating them in the report; a figure quoted from before the rebuild
  is stale, including an index's consumer count and the rehydration peak.
- A new index created while an old index on the same chain exists adopts the
  old one as its input. DROP INDEX then leaves the old dataflow alive and
  maintained (the NOTICE lists every pinned dependent) until all adopters are
  rebuilt or environmentd restarts. Therefore: drop obsolete indexes before
  creating their replacements, then rebuild every consumer the NOTICE names,
  then verify no zombie dataflows remain.
- `DROP ... CASCADE` on a view or materialized view takes every dependent with
  it, the indexes on dependent materialized views and views included; the
  NOTICE's DETAIL lists them, and a recreate script must bring every listed
  object back in dependency order (the input indexes an object should adopt
  before the object, its own indexes after it).
- After rewriting an MV, restore NOT NULL parity with `WITH (ASSERT NOT NULL
  ...)` if the rewrite loses the inference. It is an enforced assertion, not
  metadata: a NULL reaching an asserted column makes every read of the MV fail
  until the row is gone, so assert only what the rewrite guarantees. Confirm
  column names, order and types are identical (the `mz_columns` diff under
  "Verification discipline").
- `EXPLAIN ... FOR MATERIALIZED VIEW` shows the stored plan and will not
  reflect a newly added index; explain the MV's SELECT, with the session on the
  MV's cluster (`SET cluster`, or the `query` tool's cluster argument), to
  preview what a fresh build would do (the `Target cluster:` footer shows which
  cluster the preview used). On any other cluster the preview silently shows
  the un-indexed plan, since index arrangements are cluster-local.

Close every engagement with a cleanup checklist for the user: candidate objects
dropped, the experiment cluster listed with its DROP CLUSTER command (it is the
user's to drop), and the resize command for the production replica once changes
are deployed.

## Verification discipline

- Prove exactness with `EXCEPT ALL` in both directions per relation, ideally in
  one query per relation so both sides read at one timestamp.
- Declared types are part of exactness: diff the `mz_catalog.mz_columns`
  signature (name, position, type) of every changed materialized view against
  its pre-change snapshot. A rewrite can keep every row and still change a
  column's type (the partial-sum widening below is the common case), which
  `EXCEPT ALL` cannot see and typed readers can.
- Snapshots before DDL: `INSERT INTO snap SELECT * FROM mv` is rejected
  whenever the MV's definition chain contains `mz_now()` ("calls to
  mz_now in write statements"). With temporal filters, file snapshots
  also go stale as rows age out. The valid proof there is the live
  comparison: build the replacement under a temporary name and run the
  two-way EXCEPT ALL against the still-running original at a single
  timestamp.
- Rewrites whose only semantic delta is intermediate-type widening (for
  example partial sums of an int4 column carried as int8 and a total that
  arrives as numeric) may still be offered where the user asked for
  byte-identical output, but always disclosed as an option with the delta
  stated, never shipped silently. The user may know overflow cannot occur in
  their data.
- Mutation probes on shared data: insert new keys only, or keep an
  exact undo; delete exactly what you inserted; re-verify the baseline
  afterwards.
- Leave no scratch objects behind, and report honest partials rather
  than working around a blocker.

---

Developing this skill (test methodology, eval harness): see
[DEVELOPMENT.md](DEVELOPMENT.md).
