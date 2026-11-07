---
name: cx-profiling
description: >
  Query Coralogix continuous-profiling data with the `cx profiling` CLI — find
  which services use the most CPU or memory, which profile types a service has,
  what profiles can be filtered by, when usage spiked and which pod or version
  caused it, and which code paths and functions a service spends its CPU or
  memory on (flame graphs). Use when the user asks "which services use the most
  CPU", "top memory consumers", "what is service X spending CPU on", "hot
  functions", "flame graph for a service", "why is this service using so much
  CPU", "memory allocations by function", "CPU spike by pod", "which version
  increased CPU", "continuous profiling", "profiling data", or wants to explore
  profiles of a service. For how much CPU or memory a service or pod uses and
  whether it is saturated, use `cx-service-catalog` instead.
metadata:
  version: "0.1.0"
---

# Profiling Skill

Use this skill to answer **continuous-profiling** questions — which services
burn the most CPU or memory, and which functions inside a service are
responsible — via the Coralogix profiling API. Requires the
`profiles.cpu-profiles:Read` permission.

## CLI Commands

| Command | Purpose | Key flags |
|---|---|---|
| `cx profiling services` | Profiled services ranked by CPU+wall seconds (`cpu`) or allocated+heap bytes (`memory`) | `--category` (required), `--environment`, `--limit` (default 20, max 100), `--offset`, `--include-time-series` |
| `cx profiling metadata <service>` | A service's language and which profile types have data | - |
| `cx profiling filters <service>` | Label keys a service's profiles can be filtered by, with their values | `--profile-type` (required), `--filter`, `--max-values-per-key` (default 50) |
| `cx profiling metrics <service>` | One profile type's usage over time, split by `service`, `pod`, or any label; highest totals first | `--profile-type` (required), `--sum-by` (default `service`), `--max-buckets` (default 60), `--limit` (default 10), `--filter` |
| `cx profiling flame-graph <service>` | Decoded flame graph plus the top functions by self value | `--profile-type` (required), `--filter`, `--top-functions` (default 20), `--min-node-ratio` (default 0.01), `--max-depth`, `--show-kernel` |

- All commands are **read-only** and support `-o json` / `-o toon`.
- Every command takes `--start` / `--end` (default `now-1h` / `now`): `now`,
  `now-1h`-style relative expressions, or ISO-8601 timestamps.
- `--profile-type` is one of `cpu`, `wall`, `memory-allocation-bytes`,
  `memory-allocation-objects`, `memory-heap-bytes`, `memory-heap-objects`
  (case-insensitive; `MEMORY_HEAP_BYTES` also works). Check `metadata` first —
  only types with `has_data: true` return anything.
- `--filter` is repeatable and filters AND together:
  `key=v1,v2` (any of the values), `key!=v1,v2` (none of them),
  `key:exists`, `key:not-exists`. Discover keys and values with `filters`.
- `services --environment` matches `deployment.environment.name`; it is the
  only filter the services ranking honors.
- `services` pages through the ranking: when a page is full the CLI prints the
  `--offset` to use next. Time series are omitted unless `--include-time-series`
  is passed.
- `flame-graph` can take ~40 s on large services; don't set a short
  `--http-timeout`.

## Investigation Workflow

1. **Find the heavy services** (skip if the user named one):

   ```bash
   cx profiling services --category cpu --limit 10 -o json
   cx profiling services --category memory --environment <env> --limit 10 -o json
   ```

2. **Check which profile types exist** for the service:

   ```bash
   cx profiling metadata <service> -o json
   ```

3. **See what you can filter or split by** (pods, versions, environments, ...):

   ```bash
   cx profiling filters <service> --profile-type cpu -o json
   ```

4. **Find when usage changed and who caused it** — split by `pod` or a label
   key from step 3:

   ```bash
   cx profiling metrics <service> --profile-type cpu --sum-by pod --limit 5 -o json
   cx profiling metrics <service> --profile-type cpu --sum-by service.version --start now-24h -o json
   ```

5. **Find the code responsible** — start with the top functions, then the tree:

   ```bash
   cx profiling flame-graph <service> --profile-type cpu --top-functions 10 -o json | jq '.top_functions'
   cx profiling flame-graph <service> --profile-type cpu --filter k8s.pod.name=<pod> \
     --min-node-ratio 0.05 --max-depth 20 -o json
   ```

## Reading the Output

- **Services**: `cpu` rows carry `total_cpu_seconds` / `total_wall_seconds`;
  `memory` rows carry `total_memory_allocations_bytes` / `total_heap_bytes`.
  `last_active` is epoch seconds.
- **Metrics**: `series` is ranked by `total` (sum of the bucket totals) and
  trimmed to `--limit`; `total_series` is how many the server returned. `unit`
  is `seconds`, `bytes`, or `objects` depending on the profile type.
- **Flame graph**: `top_functions` sums self value per function+file across the
  **whole** tree, so it is unaffected by tree trimming. `tree` nodes carry
  `function`, `file`, `line`, `self`, `total`, `self_percent`, `total_percent`,
  and `children` (sorted by total, highest first). `omitted_subtrees` counts
  nodes dropped by `--min-node-ratio` / `--max-depth`. The server already prunes
  nodes under 0.1% of the total. Frames with no symbol show as their address or
  `unknown`. `warnings` (e.g. `maxBytes`) mean the server stopped reading
  profiles early, so the graph covers part of the range.

## Key Principles

- **Rank first, drill down second** — `services` and `metrics` are cheap;
  `flame-graph` is the expensive call, so narrow the service, profile type,
  time range, and filters before asking for one.
- **Large trees are big** — a deep stack (Java, Scala) can produce hundreds of
  KB of JSON. Raise `--min-node-ratio` or set `--max-depth` for the tree, or
  read just `.top_functions`.
- **Self vs total** — high `self` means the function itself is hot; high
  `total` with low `self` means the cost is in what it calls.
- **Empty results are not errors** — a service with no data for the chosen
  profile type or range returns empty series or a zero-total graph; re-check
  `metadata` and widen `--start`.
- **No profiling data** — if `metadata` shows no profile type with
  `has_data: true`, the service is not profiled. Do not look for other service
  names: answer from `cx-service-catalog` or `cx-telemetry-querying` (how much
  CPU or memory, when, which pod) and say that function-level detail needs
  profiling enabled for that service.
- **Multi-profile fan-out** works on every subcommand: repeat `-p <profile>`;
  results are tagged with `profile` when more than one is given.

## Related Skills

- **`cx-service-catalog`** — RED metrics (latency, errors) for the same
  services; correlate a latency regression with a CPU spike found here.
- **`cx-telemetry-querying`** — pivot to logs, spans, or PromQL metrics for a
  service or pod surfaced by profiling (`cx logs`, `cx spans`, `cx metrics`).
- **`cx-infra`** — host and container health when a hot pod points to an
  infrastructure problem.
