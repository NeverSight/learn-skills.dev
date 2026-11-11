---
name: performance-verification
description: Improve a measured performance problem through a measure, fix, re-measure, keep-or-revert loop. Use when a latency, load-time, throughput, query, bundle, or Core Web Vitals problem is reported or budgeted, or a change is suspected of a performance regression. Do not use for speculative optimization without evidence of a problem, or for a fault with no measurement yet whose cause is unknown; that is bug-diagnosis.
---

# Performance Verification

A fix is a hypothesis until re-measured. Optimize only what a measurement shows
matters, and keep only changes that beat the noise.

## 1. Measure the baseline

Record one command, its conditions, and a fixed budget (wall-clock, sample count,
or request count), repeated enough to know the run-to-run variance. Choose the
starting measurement by symptom:

- slow first load: bundle size, TTFB in the network waterfall, render-blocking
  resources;
- sluggish interaction: main-thread long tasks over 50 ms, re-renders, forced
  reflows;
- slow after navigation: request waterfalls, N+1 fetches, render time;
- one slow endpoint: its queries and their plans;
- every endpoint slow at once: connection pool, memory, CPU;
- intermittent slowness: lock contention, GC pauses, external dependencies.

Lab and field data are different measurements; label every number with its source
and never infer a metric from reading code.

## 2. Identify the bottleneck

Name the specific cause from the measurement before changing code. For a slow
query, capture `EXPLAIN ANALYZE` before the fix as the baseline and read it: a
sequential scan where an index was expected,
estimated rows off by an order of magnitude (stale statistics), or a sort node
above the scan (the index covers the filter but not the order). Index the query's
shape, equality columns before range or sort columns. An index will not help
filtering on a dominant value, a leading-wildcard `LIKE`, or a function on the
column, and every index taxes writes; an index that did not change the plan is
reverted.

When every endpoint slows together, time goes to waiting for a connection, and the
database shows idle sessions, find what holds connections. A larger pool only moves
the queue into the database; with unbounded instance counts use a connection proxy.

Cache only what is expensive to produce and read far more often than it changes.
Every input that changes the response belongs in the key (tenant, locale, viewer,
permissions). State the staleness window, pick one invalidation strategy, and guard
hot keys against stampedes by serving stale during one recompute or coalescing
concurrent misses. Values whose staleness is a correctness bug are never cached.

## 3. Fix one thing

Change one variable per measurement. Bundled changes produce one number that no
single change can claim.

## 4. Re-measure, then keep or revert

Re-run the baseline command under the same conditions and budget, and compare the
delta against the variance, not only the mean.

| Result | Action |
| --- | --- |
| Beyond the noise, tests green | Keep; put the before and after numbers in the report or commit |
| Within noise | Revert |
| Worse | Revert |
| Better but a test went red | Revert |

A neutral change is a revert: kept, it is complexity that never paid for itself.
An improvement that drops work the product needs — a validation, a required
freshness, a load-bearing `await` — is a regression.

Log every attempt, kept and reverted, as idea, baseline to result, verdict, and
reason, in the report or the repository's existing performance notes, so a dead
idea is not retried.

## 5. Guard

Protect the metric that justified the work with a repeatable budget check that
compares a median or trend, so normal variance does not make it flaky. When it
fires, start again from a fresh baseline.
