---
name: nodejs-performance
description: Identify, validate, and ship production-safe Node.js optimizations with execution time as the primary objective. Use when users ask to reduce latency (p50/p95/p99), improve throughput, and then reduce CPU/memory/event-loop lag/FD pressure or retry amplification, using one-PR-per-improvement workflows with benchmarks.
---

# Node.js Performance

Use this workflow to turn Node.js performance/resource investigations into safe, reviewable PRs.

## Goals

- Improve execution time first: reduce p50/p95/p99 latency and increase throughput without changing intended behavior.
- Reduce CPU, memory, event-loop lag, I/O pressure, or lock contention when it supports execution-time gains.
- Ship small, isolated changes with measurable impact.

## Operating Rules

- Work on one optimization per PR.
- Always choose the highest expected-impact task first.
- Confirm and respect intentional behaviors before changing them.
- Prefer low-risk changes in high-frequency paths.
- Prioritize request/job execution-path work over bootstrap/startup micro-optimizations unless startup is on the critical path at scale.
- Include evidence: targeted tests + before/after benchmark.

## Impact-First Selection

Before coding, rank candidates using this score:

`priority = (frequency x blast_radius x expected_gain) / (risk x effort)`

Use 1-5 for each factor:

- `frequency`: how often the path runs in production.
- `blast_radius`: how many requests/jobs/users are affected.
- `expected_gain`: estimated latency/resource improvement.
- `risk`: probability of behavior regression.
- `effort`: engineering time and change surface area.

Pick the top-ranked candidate, then validate with a baseline measurement.

If two candidates have similar score, pick the one with clearer end-to-end execution-time impact.

## Prioritization Targets

Start with code that runs on every request/job/task:

- Request/job wrappers and middleware.
- Retry/timeout/circuit-breaker code.
- Connection pools (DB/Redis/HTTP) and socket reuse.
- Stream/pipeline transformations and buffering.
- Serialization/deserialization hot paths (JSON, parsers, schema validation).
- Queue consumers, schedulers, and worker dispatch.
- Event listener attach/detach lifecycle and cleanup logic.

Deprioritize unless justified by production profile:

- One-time startup/bootstrap code.
- Rare admin/debug-only flows.
- Teardown paths that are not on the steady-state critical path.

## Common Hot-Path Smells

- Recomputing invariant values per invocation.
- Re-parsing code/AST repeatedly.
- Duplicate async lookups returning the same value.
- Per-call heavy object allocation in common-case parsing.
- Unnecessary awaits in teardown/close/dispose paths.
- Missing fast paths for dominant input shapes.
- Unbounded retries or retry storms under degraded dependencies.
- Excessive concurrency causing memory spikes or downstream saturation.
- Work done for logging/telemetry/metrics formatting even when disabled.

## Execution Workflow

1. **Pick one candidate**
- Rank candidates and pick the highest priority score.
- Explain the issue in one sentence.
- State expected impact (CPU, latency, memory, event-loop lag, I/O, contention).

2. **Prove it is hot**
- Add a focused micro-benchmark or scenario benchmark.
- Capture baseline numbers before editing.
- Prefer scenario benchmarks that include real request/job flow when the goal is execution-time improvement.
- For resource issues, capture process metrics (`rss`, heap, FD count, event-loop delay).

3. **Design minimal fix**
- Keep behavior-compatible defaults.
- Add fallback path for edge cases.
- Avoid broad refactors in the same PR.

4. **Implement**
- Make the smallest patch that removes repeated work.
- Keep interfaces stable unless change is necessary.

5. **Test**
- Add/adjust targeted tests for new behavior and regressions.
- Run relevant package tests (not only whole-monorepo by default).
- Add concurrency/degradation tests when the bug appears only under load.

6. **Benchmark again**
- Re-run the same benchmark with same parameters.
- Report absolute and relative deltas.
- Include latency deltas first (p50/p95/p99, throughput), then resource deltas when applicable.

7. **Package PR**
- Branch naming: `codex/perf-<area>-<change>`.
- Commit message: `perf(<package>): <what changed>`.
- Include risk notes and rollback simplicity.

8. **Iterate**
- Wait for review, then move to next isolated improvement.

## Benchmarking Guidance

- Keep benchmark scope narrow to isolate one change.
- Use warmup iterations.
- Measure both:
- `micro`: operation-level overhead.
- `scenario`: request/job flow, concurrency, and degraded dependency condition.
- For execution-time work, scenario numbers are the decision-maker; micro numbers are supporting evidence.
- Always print:
- total time
- per-op time
- p50/p95/p99 latency when applicable
- speedup ratio
- iterations and workload shape
- resource counters (`rss`, heap, handles, event-loop delay) when relevant

## Resource Exhaustion Checklist

- Cap concurrency at each boundary (ingress, queue, downstream clients).
- Ensure timeout + cancellation are wired end-to-end.
- Ensure retries are bounded and jittered.
- Confirm listeners/timers/intervals are always cleaned up.
- Confirm streams are closed/destroyed on success and error paths.
- Confirm object caches have size/TTL controls.

## CI / Flake Handling

- If CI-only failures appear, add temporary diagnostic payloads in tests.
- Serialize only affected flaky tests when resource contention is the cause.
- Keep determinism improvements in test code, not production code, unless required.

## Output Template

For each PR, report:

1. Issue being fixed.
2. Why it matters under load.
3. Code locations changed.
4. Tests run and results.
5. Benchmark before/after numbers (execution first: p50/p95/p99 and throughput).
6. Risk assessment.
7. Next candidate optimization.
