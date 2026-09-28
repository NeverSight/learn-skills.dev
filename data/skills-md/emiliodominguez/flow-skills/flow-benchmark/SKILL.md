---
name: flow-benchmark
description: "Performance measurement with a reproducible baseline and stated uncertainty. Use before optimizing, or to compare alternatives on speed, memory or size. Feeds `flow-work` or `flow-refactor` with evidence."
metadata:
  stage: verify
---

# Benchmark

Define what "better" means before measuring. Keep raw results and compare like with like;
never report a single attractive timing.

## Process

1. State metric, workload, target and the decision it informs. Define the timing boundary and
   cache/process state: cold startup includes initialization; steady-state throughput may warm
   up. Keep cold and warm experiments separate.
2. Record baseline revision, runtime/build settings, hardware/environment, fixtures,
   concurrency, sample unit and tool/version. Time setup only when it is part of the metric;
   never warm away the behavior under investigation.
3. Run baseline and candidate under controlled conditions, changing one variable per
   experiment. Interleave A/B samples when drift matters; isolate data/state between samples.
4. Collect enough observations for the claim. Report median, tails such as p95/p99 only when
   sample size supports them, variance, outliers and known noise. No false precision, no
   unexplained outlier removal.
5. Check tradeoffs in memory, CPU, responsiveness, bundle size and complexity. Profile when the
   result needs an explanation. A lower score is not automatically a better user experience.
6. Save the harness or command, raw results and comparison so others can rerun it. State
   whether the effect is large relative to noise.

## Anti-patterns

- Warming a cold-start benchmark or excluding the initialization under investigation.
- Comparing development and production builds as if only the implementation changed.
- Reporting a best run or p99 from a handful of samples.
- Claiming causation from timing alone.

## Done when

- Baseline and candidate share a relevant reproducible workload and timing boundary.
- Raw results, uncertainty and meaningful regressions are visible.
- The evidence supports an optimization decision or names what better measurement is needed.

Use `flow-work` or `flow-refactor` only for an optimization the evidence justifies.
