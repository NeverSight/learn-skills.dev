---
name: performance-engineering
description: >-
  Diagnose and improve software performance through user/system baselines, measurement, profiling,
  representative benchmarks, controlled changes, and before/after verification. Use for latency,
  throughput, startup time, memory/CPU/IO efficiency, hot paths, scaling headroom, or capacity/cost
  tradeoffs. Do not optimize speculatively; measure the real symptom before choosing a technique.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.0"
---


# Performance Engineering

Measure first, change one meaningful bottleneck, then measure again.

## Workflow

1. Define the user/system symptom and target metric: latency percentile, throughput, startup time, memory, CPU, IO, battery, or unit cost as appropriate.
2. Establish a representative baseline and workload. Avoid synthetic microbenchmarks that do not exercise the reported bottleneck.
3. Profile or instrument enough to localize the dominant cost before proposing optimization.
4. Form a hypothesis and change the smallest meaningful factor.
5. Re-measure under comparable conditions and check counter-metrics/correctness.
6. If the problem is load/headroom rather than code-path efficiency, model demand, capacity units, scaling trigger, and cost without assuming a provider.
7. Preserve readability/reliability unless the measured gain justifies the complexity.

## Stop

Stop when the target symptom has before/after evidence, the bottleneck/result is understood, and remaining tradeoffs are explicit.
## Reference Guide

Load only the references needed for the current task:

- [capacity cost](references/capacity-cost.md)
- [measurement profiling](references/measurement-profiling.md)
- [optimization experiment](references/optimization-experiment.md)
- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [provider neutrality](references/_shared/engineering/provider-neutrality.md)
- [evidence](references/_shared/verification/evidence.md)
- [risk depth](references/_shared/verification/risk-depth.md)
