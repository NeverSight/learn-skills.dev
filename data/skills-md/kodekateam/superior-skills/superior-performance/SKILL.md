---
name: superior-performance
description: Investigate, optimize, or review software performance using representative measurements, profiles, budgets, and regression evidence. Use when latency, throughput, resource use, loading, rendering, bundle cost, or scalability is a primary concern. Do not use for speculative micro-optimization without a symptom, target, or demonstrated bottleneck.
---

# Superior Performance

Improve the user or system outcome that is actually constrained, not the code that merely looks expensive. Preserve correctness, security, accessibility, and maintainability while grounding every optimization in comparable evidence.

## Define the performance contract

Before optimizing, establish:

- the affected user journey, operation, workload, or resource;
- the metric and target, including percentile or distribution where relevant;
- current baseline, regression window, and measurement source;
- environment, hardware, network, data shape, concurrency, and cache state;
- correctness and quality constraints that may not be traded away;
- whether the goal is latency, throughput, responsiveness, capacity, efficiency, or cost.

Do not convert an unverified impression such as “slow” into a universal target. If no explicit budget exists, derive a provisional comparison from product expectations and repository evidence, and label it as provisional.

## Measure before changing

Read [references/measurement-profiling-and-benchmarks.md](references/measurement-profiling-and-benchmarks.md) when establishing a baseline, selecting profiling tools, constructing a benchmark, or comparing alternatives.

- Reproduce the representative workload before editing when practical.
- Warm up runtimes and caches intentionally; report cold and warm results separately when both matter.
- Prefer profiles, traces, query plans, flame graphs, allocation data, or browser timelines over intuition.
- Change one material variable at a time and compare using the same setup.
- Account for variance, background work, sampling, throttling, and measurement overhead.

A single fast run is not evidence of improvement. A synthetic benchmark is useful only for the behavior it faithfully represents.

## Optimize the owning bottleneck

Read [references/runtime-capacity-and-caching.md](references/runtime-capacity-and-caching.md) for CPU, memory, allocation, I/O, concurrency, queues, batching, caching, connection pools, or service-capacity work.

Read [references/client-delivery-and-rendering.md](references/client-delivery-and-rendering.md) for bundles, network waterfalls, images, fonts, hydration, rendering, input responsiveness, long tasks, layout, or client memory.

- Remove unnecessary work before making necessary work faster.
- Reduce work at the layer that owns the constraint rather than shifting it invisibly to another service, client, queue, or deployment phase.
- Preserve boundedness and backpressure; higher throughput that creates unstable queues is not an improvement.
- Treat caches as consistency and lifecycle systems, not free speed.
- Prefer algorithmic, query, payload, and round-trip improvements over low-value syntax micro-optimizations.

Do not add concurrency, memoization, lazy loading, preloading, compression, or a cache merely because it can improve a benchmark. Confirm the workload, invalidation, memory, latency, and operational tradeoffs.

## Protect correctness and experience

- Verify outputs, ordering, authorization, error handling, cancellation, and idempotency remain correct.
- Do not improve averages by dropping slow requests, hiding errors, reducing result quality, or excluding difficult devices and data.
- Preserve accessibility and reduced-motion behavior in client optimizations.
- Avoid production profiling, load generation, cache flushing, broad telemetry changes, or resource-limit changes without explicit authorization and safety controls.
- Treat performance changes that alter public behavior, consistency, retention, or cost as contract changes, not invisible implementation details.

## Verify the improvement

Repeat the baseline protocol after the change and report:

- before and after distributions or representative measurements;
- workload, environment, sample count or duration, and cache state;
- profile evidence showing the bottleneck moved or diminished;
- correctness and regression checks performed;
- resource or cost tradeoffs introduced;
- limits of the benchmark and conditions not exercised.

Check neighboring workloads for regressions. An optimization can improve one percentile, payload, route, or device while harming another. If the result is within measurement noise, report it as inconclusive rather than improved.

## Combine skills narrowly

- Use `superior-debugging` when the performance symptom's cause is still uncertain and causal investigation is primary.
- Use `superior-database` when query plans, indexes, locks, schema, or datastore capacity owns the bottleneck.
- Use `superior-reliability` when objectives, overload behavior, graceful degradation, or recovery owns the outcome.
- Use `superior-delivery` when performance evidence is a release gate or the optimization changes build or rollout behavior.
- Use `superior-testing` when benchmark design or performance-regression automation requires dedicated test judgment.
- Use `superior-ui`, `superior-responsive`, or `superior-accessibility` when an interface change is required to deliver the measured improvement safely.
- Use `superior-logic` when optimization changes application behavior, concurrency, state, or external calls.
- Use `superior-docs` after a verified material performance change or durable measurement/runbook update.

Do not broaden focused optimization into a framework rewrite, infrastructure migration, or observability-platform replacement without explicit scope.
