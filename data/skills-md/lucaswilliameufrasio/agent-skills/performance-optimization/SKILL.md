---
name: performance-optimization
description: >-
  Diagnose and improve application performance or resource efficiency using
  measured evidence. Always use when the user says an app/API is slow, reports a
  performance regression or bottleneck, asks to optimize/tune code, or wants
  higher throughput or lower latency, CPU, memory, or cost—even if they request
  a specific code change before providing a profile. Reproduce the workload,
  locate the bottleneck, change one cause at a time, and verify comparable runs.
---

# Evidence-driven performance optimization

Optimize the system's actual objective, not an isolated benchmark score. Keep
correctness, reliability, tail latency, resource use, and cost in view. A queue
that rejects overload correctly or a slow external dependency may be a design
boundary rather than an application-code defect.

## Establish the target and baseline

1. Ask what outcome matters: latency percentile, sustainable throughput, CPU or
   memory per request, queue age, startup time, cost, or a specific regression.
   Define a success threshold and unacceptable trade-offs.
2. Inspect the project, existing dashboards, performance scripts, prior
   baselines, release/runtime settings, and environment. Preserve existing
   workflows and unrelated changes.
3. Reproduce the symptom with a representative, repeatable workload. Record
   commit/build, runtime and flags, machine/architecture, resource limits,
   dependencies/topology, input size, offered load, duration, warmup, and
   repetitions. Do not compare numbers from materially different environments
   as if they were directly comparable.
4. Measure useful outputs together: offered and delivered throughput, p50/p95/
   p99 latency, errors/timeouts, CPU, RSS/allocations, queue depth/age, and
   dependency calls or cost as relevant. Check that the load generator is not
   the bottleneck.

Use `performance-benchmarking-and-load-testing` to create or run the harness;
use `performance-profiling-ebpf` when sampling can narrow a measured bottleneck.

## Diagnose before editing

Form a falsifiable hypothesis tied to evidence: profile samples, traces,
allocation/lock data, query plans, queue growth, runtime metrics, or an isolated
microbenchmark. Rank candidates by expected user impact, confidence, effort, and
risk. Distinguish CPU-bound work, allocation/GC pressure, lock contention, I/O,
queueing, downstream capacity, and load-generator/infrastructure limits.

Do not optimize a synthetic endpoint or microbenchmark and present it as a
production capacity improvement. Do not treat a flamegraph as proof of a fix;
it helps explain where time was spent under one workload. If the bottleneck is
external or the evidence is inconclusive, report that and gather the smallest
useful next measurement rather than making speculative changes.

## Make and prove one change at a time

1. State the hypothesis and predicted metric change before editing.
2. Make the smallest change that tests it; preserve API, data, security, and
   backpressure semantics. Add or update correctness/regression tests, then run
   the repository's full relevant quality gate so a speedup does not hide a
   correctness or reliability regression.
3. Repeat the same workload, tool version, environment, and resource settings.
   Use enough independent runs to distinguish noise; report distributions or
   medians, not a cherry-picked fastest run.
4. Compare the target and guardrails: a throughput gain is not a win if p99,
   errors, memory, queue growth, downstream load, or cost worsens beyond the
   agreed bounds.
5. Keep, revise, or revert only the change under evaluation based on evidence.
   Do not discard unrelated user changes.

The final report should include the bottleneck evidence, hypothesis, change,
before/after results and run conditions, correctness checks, trade-offs,
limitations, and remaining bottlenecks. Separate observed facts from estimates
and recommendations. Never generalize a local ceiling into a production SLO.

## Review checklist

- Was the original behavior reproduced and the objective defined?
- Is the claimed bottleneck supported by evidence under representative load?
- Are baseline and candidate runs comparable and repeated?
- Did correctness and reliability remain intact?
- Were focused regression tests and the repository's required quality checks run?
- Were tail latency, errors, resource use, queues, dependencies, and cost checked?
- Are conclusions appropriately limited to the tested environment/workload?
