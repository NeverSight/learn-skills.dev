---
name: sota-performance
description: >-
  State-of-the-art performance engineering for building fast systems and
  auditing existing code for bottlenecks. Use when the task involves
  performance, optimization, latency, profiling, slow code, memory usage,
  caching, or throughput — designing latency budgets, fixing N+1 and
  accidental-quadratic patterns, tuning allocation/GC pressure, network and
  I/O efficiency, cache architecture, Core Web Vitals, or setting up
  benchmarks and regression gates. Not for concurrency correctness (races,
  deadlocks, cancellation) — use sota-async-concurrency. Trigger keywords: performance,
  optimization, latency, profiling, slow, memory usage, caching, throughput,
  bottleneck, p99, flamegraph, Core Web Vitals.
---

# SOTA Performance Engineering

## Purpose

Make systems fast by default and find why they are slow by evidence. This skill
encodes two disciplines that share one rule set:

1. **BUILD** — write code whose performance characteristics are known, budgeted,
   and protected by regression tests before it ships.
2. **AUDIT** — read existing code and telemetry to locate bottlenecks, rank them
   by user-facing impact, and prescribe fixes with expected gains.

Core doctrine: **measure first, but fix known pathologies on sight.** Profiling
is mandatory before micro-optimization; it is NOT required to remove an O(n²)
loop, an N+1 query, or an unbounded cache. "Premature optimization" never
excuses shipping a known pathology.

## BUILD mode

When writing new code or features:

1. **Set a budget before writing.** Define the latency budget (p99, not average)
   and decompose it across hops. An endpoint with a 200 ms p99 budget that calls
   auth (10 ms) + 2 DB queries (2×15 ms) + serialization (5 ms) has 155 ms of
   headroom — spend it consciously. See [`rules/01-methodology.md`](rules/01-methodology.md).
2. **Choose data structures by access pattern, not habit.** Know the n. n < 100:
   anything works. n unbounded: complexity class is the design.
   See [`rules/02-algorithms-data-structures.md`](rules/02-algorithms-data-structures.md).
3. **Batch and stream at every boundary.** One round trip per collection, not
   per item. Stream large results; never materialize unbounded data.
4. **Control allocation in hot paths.** Pre-size collections, reuse buffers,
   avoid per-iteration allocation in loops that run > 10⁴ times per second.
   See [`rules/03-memory.md`](rules/03-memory.md).
5. **Make I/O cheap by construction.** Pooled connections, keep-alive, buffered
   writes, compression chosen per payload type. See [`rules/04-io-network.md`](rules/04-io-network.md).
6. **Cache deliberately or not at all.** Every cache ships with: key schema,
   TTL + jitter, eviction policy, invalidation path, stampede protection, and a
   hit-ratio metric. A cache missing any of these is a future incident.
   See [`rules/05-caching.md`](rules/05-caching.md).
7. **Protect the win.** Add a benchmark or perf test in CI for any code with a
   budget. A perf improvement without a regression gate is a loan, not an asset.
8. **Frontend ships against Core Web Vitals budgets** (LCP ≤ 2.5 s, INP ≤ 200 ms,
   CLS ≤ 0.1 at p75). See [`rules/06-frontend-web.md`](rules/06-frontend-web.md).

## AUDIT mode

**Coverage:** every `rules/` file's Audit checklist applies in AUDIT mode. Mark one *not applicable* only with its reason in the report — never skip a file because the thing it checks for is absent, since that absence may be the finding.

### How to find performance issues by reading code

Work outside-in, hottest path first:

1. **Identify the hot paths.** Entry points with highest traffic or strictest
   SLO: request handlers, queue consumers, render loops, cron jobs over large
   datasets. Audit those first; ignore cold admin paths until the end.
2. **Grep for pathology signatures** (high hit rate, low effort):
   - Loops containing `await`/network/DB calls → N+1 ([`rules/02`](rules/02-algorithms-data-structures.md))
   - String/array concatenation inside loops → accidental quadratic ([`rules/02`](rules/02-algorithms-data-structures.md))
   - `.includes`/`in list`/linear `find` inside a loop → O(n·m) ([`rules/02`](rules/02-algorithms-data-structures.md))
   - `SELECT *`, queries without LIMIT, missing pagination ([`rules/02`](rules/02-algorithms-data-structures.md), [`rules/04`](rules/04-io-network.md))
   - Caches/maps with insert but no eviction or TTL → leak ([`rules/03`](rules/03-memory.md), [`rules/05`](rules/05-caching.md))
   - `addEventListener`/subscribe without matching removal ([`rules/03`](rules/03-memory.md))
   - Sequential awaits on independent operations → serialized latency ([`rules/04`](rules/04-io-network.md))
   - New client/connection per request instead of pooled ([`rules/04`](rules/04-io-network.md))
   - Sync file/crypto/compression calls on async event loops ([`rules/04`](rules/04-io-network.md))
   - `JSON.parse`/serialize of large payloads in hot loops ([`rules/03`](rules/03-memory.md))
3. **Check the boundaries.** Most production latency lives at boundaries:
   process↔kernel (syscalls), service↔DB, service↔service, server↔browser.
   Count round trips per user action; > 3 sequential round trips is a finding.
4. **Check resource lifecycle.** Anything created per-request that is expensive
   to create (connections, TLS sessions, regexes, compiled templates, clients)
   should be created once and reused.
5. **Check what's missing**: no timeouts, no pagination, no backpressure, no
   pool bounds, no cache eviction — absent code is the most common perf bug.

### What to measure (when you can run the system)

- **Latency distribution**: p50/p95/p99 per endpoint — never averages
  ([`rules/01`](rules/01-methodology.md)). Compare p99 to p50; ratio > 10× means contention, GC, or
  stampedes, not slow code.
- **USE per resource** (Utilization, Saturation, Errors): CPU, memory, disk,
  network, pools, queues. **RED per service** (Rate, Errors, Duration).
- **Where time goes**: CPU flamegraph for compute, off-CPU/wall profile for
  waiting. A request that is slow with idle CPU is blocked on I/O or locks.
- **Allocation rate and GC pause time** for managed runtimes.
- **Cache hit ratios** and **DB round trips per request**.
- **Frontend**: field CWV (CrUX/RUM) at p75, not lab-only Lighthouse.

### Severity conventions (by user-facing impact)

| Severity | Criteria |
|---|---|
| **Critical** | Active or imminent user-facing failure: unbounded growth (memory leak, unpaginated scan) that will OOM/timeout at production scale; O(n²)+ on user-controlled input; stampede-capable cache in front of a fragile origin; p99 SLO breached now. |
| **High** | Measurable user-facing degradation: N+1 on a hot path; missing pool/keep-alive adding RTTs per request; blocking call on event loop; CWV in "poor" band; hot-path complexity that degrades super-linearly with organic growth. |
| **Medium** | Wasteful but currently within budget: avoidable allocations in warm paths; missing compression; suboptimal cache TTLs; sequential awaits worth ~10–50 ms; bundle over budget but CWV still "needs improvement". |
| **Low** | Hygiene: micro-inefficiencies in cold paths, style-level fixes, missing benchmarks for non-critical code. |

Escalate one level if the code path is on the critical user journey (checkout,
login, search) or if growth is super-linear with data/users.

### Finding format

```
[SEVERITY] <one-line title>
Location: <file:line(s)>
Pattern: <pathology name, e.g. "N+1 query", "unbounded cache">
Evidence: <code excerpt or metric>
Impact: <quantified or estimated user-facing effect, with the math>
Fix: <specific change, with expected gain>
Verify: <how to confirm the fix: benchmark, profile, metric to watch>
```

Estimate impact with arithmetic, not adjectives: "200 items × 1 query × ~1 ms
RTT = ~200 ms added per page view" beats "this is slow".

## Rules index

| File | Read this when... |
|---|---|
| [`rules/01-methodology.md`](rules/01-methodology.md) | You need to profile, benchmark, set latency budgets, interpret percentiles, apply USE/RED, decide what's worth optimizing (Amdahl), or set up CI perf regression gates. |
| [`rules/02-algorithms-data-structures.md`](rules/02-algorithms-data-structures.md) | Auditing loops and data access: N+1, accidental quadratics, repeated scans, hash-vs-tree choices, batching, streaming vs materializing, and high-level DB pointers (indexes, SELECT *, chatty transactions). |
| [`rules/03-memory.md`](rules/03-memory.md) | Dealing with allocation pressure, GC pauses, object pooling, arenas, cache locality, SoA vs AoS, or hunting memory leaks (closures, listeners, unbounded caches) per runtime. |
| [`rules/04-io-network.md`](rules/04-io-network.md) | Anything crossing a syscall or the wire: buffering, zero-copy, connection pooling, HTTP/2/3, compression choice (zstd/brotli), TLS resumption, CDN, request coalescing, pagination over the wire, never blocking an async event loop. |
| [`rules/05-caching.md`](rules/05-caching.md) | Designing or auditing any cache: hierarchy placement, key design, invalidation, stampede protection (singleflight, jitter, soft TTL), negative caching, when caching is the wrong fix, and the security floor (declared global/tenant/user key scope, authorize before a cache hit, invalidate on role/tenancy change). |
| [`rules/06-frontend-web.md`](rules/06-frontend-web.md) | Web performance: Core Web Vitals thresholds, bundle budgets, code splitting, image formats (AVIF/WebP), font loading, hydration cost, edge rendering. |

## Per-language detail

This skill is language-neutral. The toolchain half — profilers, allocation and GC behaviour, runtime and build flags — lives in one file per language skill. Read it beside this one whenever the code is in that language:

| Language | File |
|---|---|
| Python | [`sota-python` rules/06](../sota-python/rules/06-performance.md) |
| Go | [`sota-golang` rules/06](../sota-golang/rules/06-performance.md) |
| Rust | [`sota-rust` rules/06](../sota-rust/rules/06-performance.md) |
| C / C++ | [`sota-c-cpp` rules/07](../sota-c-cpp/rules/07-performance.md) |
| Java / Kotlin | [`sota-jvm` rules/05](../sota-jvm/rules/05-performance.md) |
| C# / .NET | [`sota-dotnet` rules/05](../sota-dotnet/rules/05-performance.md) |
| JavaScript / TypeScript | [`sota-javascript-typescript` rules/06](../sota-javascript-typescript/rules/06-performance.md) |
| PHP | [`sota-php` rules/06](../sota-php/rules/06-performance-runtime.md) |
| Ruby | [`sota-ruby` rules/05](../sota-ruby/rules/05-concurrency-performance.md) |
| Swift | [`sota-swift` rules/07](../sota-swift/rules/07-performance.md) |

## Top-10 non-negotiables

1. **Measure before optimizing; fix pathologies on sight.** Profile before
   micro-tuning. But N+1, O(n²) on unbounded input, unbounded caches, and
   sync-blocking the event loop need no profiler — fix them when you see them.
2. **Percentiles, never averages.** Report and budget p50/p95/p99. An average
   hides the 1% of users who hit every cache miss and GC pause.
3. **No I/O inside a loop over a collection.** Batch it, join it, or
   parallelize it with a bound. One round trip per item is always a finding.
4. **Every cache has bounded size, TTL with jitter, an invalidation path, and
   stampede protection.** Otherwise it's a memory leak with a hit ratio.
5. **Pool expensive resources.** Connections, TLS sessions, threads, compiled
   regexes, HTTP clients: create once, reuse always, bound the pool.
6. **Stream unbounded data; never load "all rows" into memory.** Paginate with
   cursors, process in chunks, set LIMITs.
7. **Never block an async event loop** with sync file I/O, crypto, compression,
   or CPU-heavy work. Offload to workers or use async variants.
8. **Set timeouts and bounds on everything**: requests, queries, pools, queues,
   retries (with backoff + jitter). Missing bounds turn slowness into outage.
9. **Sequential awaits on independent work are stolen latency.** Run
   independent I/O concurrently; the latency of the batch is the max, not sum.
10. **Protect every win with a regression gate.** A benchmark in CI with
    variance-aware thresholds, or the regression returns within a quarter.
