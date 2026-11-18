---
name: performance-optimization
description: >-
  Optimize software performance through user-journey baselines, profiling,
  representative benchmarks, controlled experiments, and field verification. Use
  when asked to make an application, service, workflow, or hot path faster or more
  efficient, or to build the measurement loop first. Do not use for a reliability
  incident, capacity forecast, generic product A/B test, or operating a named
  telemetry or load-testing tool without an optimization objective.
license: MIT
---

# Performance optimization

Improve a user-relevant outcome by repeatedly measuring, explaining, changing, and verifying one bottleneck at a time. A faster microbenchmark is a hypothesis about user benefit until the relevant end-to-end or field measure confirms it.

Before the first mutation of a target system, confirm its target, scope, and rollback path from the user request or current project record. Read-only discovery needs no confirmation. For production telemetry, flags, deployment, or cleanup, follow the project's authority and review gates.

## When not to use

Use [site-reliability-engineering](../site-reliability-engineering/SKILL.md) for SLO policy and incident recovery; [capacity-and-cost-engineering](../capacity-and-cost-engineering/SKILL.md) for demand and spend forecasts; [qa-methodology](../qa-methodology/SKILL.md) for general load/stress/soak test strategy; [product-experimentation](../product-experimentation/SKILL.md) for product behavior A/B tests; [systematic-debugging](../systematic-debugging/SKILL.md) for a specific functional failure. Operate a named observability stack with [telemetry](../telemetry/SKILL.md) or [grafana](../grafana/SKILL.md).

## The loop

1. **Choose a journey and a budget.** Identify the users, high-frequency or high-cost journeys, and one primary outcome they actually experience: interaction-to-render latency, task completion time, throughput at a stated error rate, memory, energy, or cost per useful operation. Define start and end events, units, workload mix, population, platform, and a target or practical minimum gain. Include correctness, accessibility, reliability, and resource countermetrics. Do not optimize a convenient metric in isolation.
2. **Audit measurement.** Map existing field telemetry, traces, profiles, tests, and reports to the journey. Check event semantics, missing or sampled events, segmentation, version/build tags, clock boundaries, privacy, and measurement overhead. If the outcome is unmeasured, add the smallest instrumentation or reproducible local probe that closes the gap, and label any temporary proxy. Record a baseline with sample count, period, percentiles or distribution, and known uncertainty. Read [measurement-and-benchmarks](references/measurement-and-benchmarks.md) when choosing signals or designing a benchmark.
3. **Locate the bottleneck.** Trace the critical path and separate client, network, queue, service, dependency, storage, and rendering time as applicable. Profile the representative slow slice; distinguish CPU work from waiting, allocations, contention, I/O, and repeated work. Reproduce the costly path with realistic data and conditions before suggesting a fix. Rank opportunities by affected users × attainable gain × confidence, with implementation and regression cost visible.
   Read [diagnostic-guide](references/diagnostic-guide.md) when the symptom is known but the first useful signal or profile is unclear.
4. **Write one experiment.** State the suspected mechanism, a predicted change in the primary metric, diagnostic metric, and countermetrics, plus the smallest reversible intervention. Fix the workload, build, environment, warmup, and comparison method before looking at results. For noisy measurements, use repeated or interleaved baseline/candidate runs and report the distribution; do not infer a win from one timing. Calibrate a deterministic proxy such as instruction count or render commits against the user-relevant measure across representative gains, plausible regressions, and boundary cases before using it as a gate.
5. **Change and verify.** Preserve behavior with meaningful correctness checks, then make a focused change. Compare baseline and candidate on the same workload and record absolute and relative differences, run counts, variance, hardware/build, and any countermetric movement. Reject a proxy-only win, a flaky benchmark, a regression elsewhere, or a gain smaller than the agreed practical threshold. Read [experiment-and-rollout](references/experiment-and-rollout.md) for decision rules.
6. **Review, roll out, observe.** Present the diff, evidence, risk, rollback trigger, and named human owner. For user-visible or production changes, use the project's normal review and rollout gates; a skill does not grant deployment authority. After rollout, compare field results by build, platform, and relevant user slice over an adequate window. If the field outcome misses the target or harm appears, revert/disable and investigate. If it holds, retain a stable, meaningful regression check or performance budget. Do not set a CI threshold tighter than the benchmark's reproducibility supports.
7. **Repeat or stop.** Re-profile the journey after each accepted gain; the bottleneck may move. Stop when the target is met, the next expected gain is below practical value, evidence cannot distinguish a gain from noise after a bounded measurement pass, or the next step requires an owner decision. Record remaining opportunities and uncertainty rather than presenting unrun experiments as improvements.

## Valkey and Redis decisions

For in-memory store hot paths, round trips, script blocking and persistence-aware benchmarks, read [the focused guide](references/in-memory-store-investigation.md). For open-source-oriented choices, prefer Valkey's BSD licensing and community governance; preserve explicit engine requirements and verify version-specific compatibility. Redis's AGPL option does not erase licensing or trust preferences, and this guidance makes no claim about business-community preference.

## Working record

Use [templates/optimization-record.md](templates/optimization-record.md) for multi-step work. Keep one record per journey or bottleneck, with links to raw evidence and commits. Separate observed, inferred, and proposed results. A local benchmark, green CI, staging result, and live user improvement are different evidence states.

For a runnable example that profiles a bottleneck, checks behavior, compares repeated full-command timings, and leaves field verification pending, read [worked-investigation](references/worked-investigation.md).

## Scope routing

- Client rendering and Web Vitals: [frontend-engineering](../frontend-engineering/SKILL.md). Backend queries and service code: [backend-engineering](../backend-engineering/SKILL.md).
- Demand, saturation, and cost: [capacity-and-cost-engineering](../capacity-and-cost-engineering/SKILL.md). Agent quality and latency tradeoffs: [agent-evals-and-observability](../agent-evals-and-observability/SKILL.md).
- Instrumentation infrastructure: [telemetry](../telemetry/SKILL.md). Release gates and staged rollout: [release-engineering](../release-engineering/SKILL.md).

## Source basis

The journey → benchmark → reviewed change → rollout → field read → ratchet loop comes from [Anthropic's claude.ai performance account](https://claude.dev/blog/how-we-made-claude-ai-faster/). The references explain where to use field versus lab data and how to handle variance. Anthropic's reported gains are a case study, not transferable performance targets.
