---
name: debug-plan-cache-misses
description: Find and debug Chalk query plan cache misses from engine logs. Use when a query is replanning on every request, an "ad-hoc query request missed the plan cache" warning shows up, latency spikes from repeated planning, or someone asks why two seemingly identical queries don't share a cached plan. Drives the `chalk logs` CLI search.
---

# Debug Chalk query plan cache misses

Chalk caches a compiled query plan the first time it plans a query, keyed by a
normalized `BatchQuery`. A **cache miss** forces the engine to replan on the
hot path, which is slow. Misses are expected the first time a query shape is
seen; they are a *problem* when a query that "looks identical" to a previous
one keeps missing — that means some field in the request is varying between
calls.

This skill: (1) finds misses in the logs, and (2) diffs the planned queries to
identify exactly which field differs and forces the miss.

## What the cache key actually is

The plan cache key wraps the **entire normalized `BatchQuery`**. The only
normalization applied is that `planner_options` are resolved to their
effective values — so leaving an option unset and setting it explicitly to its
default produce the **same** key and will not cause a spurious miss.

Everything else in the request is part of the key, including:

- `given_features` — the exact set of input features the caller provides
- target features (`optional_target_features` / `required_target_features`)
- `tags`, `required_resolver_tags`
- `max_staleness_overrides` and staleness/recompute flags
- `query_name_and_version`
- and the remaining `BatchQuery` fields

So **any** difference in these forces a new plan. The single most common
real-world cause is a **varying `given_features` set** — the caller sometimes
supplies more or fewer input features (e.g. raw `*_original` inputs, or derived
inputs like `email_username`) than a previous call. A query that provides a
different set of inputs genuinely needs a different plan (different resolvers
must run), so it cannot reuse the cached one.

## The two log lines that signal a miss

The engine emits these on the planning path:

1. **Ad-hoc miss warning** (`batch_online_query_service.py`):
   `Ad-hoc query request with query name/version '(<name>, <version>)' missed the plan cache. The query was: <BatchQuery ...>`

2. **Plan computation** — emitted on *every* miss (ad-hoc or named), and the
   most useful line for debugging (`local_plan_factory.py`):
   `Computed plan for [<target features>] given [<given features>] with planner options <NonNullPlannerOptions(...)>; query.query_name_and_version=(<name>, <version>)`

There are also statsd counters if you want to trend rather than read lines:
`chalk.engine.planner.python_plan_cache_miss` vs
`chalk.engine.planner.python_plan_cache_hit`.

## Finding misses with `chalk logs`

`chalk logs` searches the environment's engine logs. Point it at the right
environment/context first (`chalk config` / the usual project or `--environment`
selection), then query by log fields.

Search for the miss warnings over the last day:

```sh
chalk logs --query 'message:"missed the plan cache"' \
  --start-time "24h ago" --end-time "now"
```

Search for plan computations for one query name (best for diffing):

```sh
chalk logs --query 'message:"Computed plan for" message:sv5_idplus_features_parallel' \
  --start-time "24h ago" --end-time "now"
```

Trend miss volume over time in 10-minute buckets:

```sh
chalk logs --aggregate --window-period 10m \
  --query 'message:"missed the plan cache"' --start-time "6h ago"
```

Tail misses live while reproducing:

```sh
chalk logs --follow --query 'message:"missed the plan cache"'
```

### Query syntax

`field:value` pairs, space-separated (implicit AND). Quote any value that
contains a space or a `.` — e.g. `message:"missed the plan cache"`,
`query_name:"my.query"`. Useful fields:

- `message` — substring match on the log message (use this for the two lines above)
- `component` — Chalk component, e.g. `component:engine`
- `query_name` — filter to a specific named query
- `operation_id` — internal query id; `correlation_id` — caller-supplied query id
- `trace_id`, `pod_name`, `resource_group`, `deployment`, `app`
- `all_filter` — match across multiple fields at once

Time flags: `--start-time` / `--end-time` accept `'1h ago'`, `'now'`, or
ISO-8601 (`'2024-01-01T00:00:00Z'`). Add `--tui` for an interactive viewer.

## Debugging workflow

1. Confirm misses are happening and how often:

   ```sh
   chalk logs --query 'message:"missed the plan cache"' --start-time "24h ago"
   ```

   If this is empty, plan caching is working — look elsewhere for the latency.

2. Pull the `Computed plan for` lines for the affected query name:

   ```sh
   chalk logs --query 'message:"Computed plan for" message:<query_name>' \
     --start-time "24h ago"
   ```

3. Take the two most recent computations and **diff them field by field**:
   compare the `given [...]` lists first (most common culprit), then the
   target-feature lists, then the `planner options` block. Whatever differs is
   the cause of the miss. Because planner options are normalized before keying,
   a difference there is a real difference — not a set-vs-default artifact.

4. Attribute the difference to the caller. A varying `given` set almost always
   means an upstream service is sending an inconsistent input schema (sometimes
   including raw/derived inputs, sometimes not). The fix is to make the caller
   send a **stable** `given_features` set on every request so the key is
   stable and subsequent identical queries hit the cache.

## Notes

- Two byte-identical requests should hit the cache on the second call. If they
  don't, that's a distinct issue from a field mismatch (e.g. cache not being
  populated/shared) — call it out separately rather than blaming the request.
- Fixing a miss only helps if **all** callers converge on one request shape. If
  some callers still send a different `given` set, those keep missing.
- This skill reads logs and reasons about the request; it does not mutate any
  environment. Any remediation (changing what a caller sends) happens in the
  caller's code, not here.
