---
name: check-benchmark
description: Evaluate performance claims or benchmark comparisons by checking real work, correct outputs, comparable conditions, measurement scope, and variation.
---

# Check Benchmark

Assess whether the evidence supports the stated performance claim. Use the existing measurement harness and valid runs before adding work; an existing Developer or Reviewer can perform this check.

## Identify the Claim and Inputs

State the user-relevant operation, baseline/candidate, workload, metric, units, measurement boundary, and acceptance criterion. Identify source/build, dependencies, non-sensitive configuration, environment, and actual run outputs. A local kernel result supports a kernel claim; a user-journey claim needs evidence for the relevant path.

## Inspect the Measurement

- **Real work:** verify that requests/tasks execute, asynchronous work is awaited, and collected samples cover the intended operation. Check actual counts and outputs rather than a harness's success label. Elided work, zero samples, or a cached substitute for an uncached workload changes the claim.
- **Correctness:** inspect errors, rejected/dropped work, timeouts, and output semantics. Throughput cannot count failed work as successful work. Preserve acceptance, order, gaps, and budgets; derive expected results from the contract rather than the returned value.
- **Comparability:** compare equivalent useful work and data under relevant runtime, build, configuration, concurrency, retention, and cache conditions. Record intentional differences, warm-up/setup/cleanup, background contention, and other limitations.
- **Instrument:** check clock/units, start and finish boundaries, accumulation/aggregation, and whether instrumentation includes the asserted operation. Readiness predicates and assertions should represent the same contract; dynamic tolerances must admit legal behavior and catch the target defect.
- **Variation:** inspect repeatability and distribution at the metric's relevant scale. Choose additional runs only to answer uncertainty, proportionate to cost and noise; there is no universal run count. Distinguish a real effect from noise, saturation, or a changing workload.
- **Practical effect:** connect the measured change to the end-to-end path, bottleneck, and any cost or correctness trade-off. State the limited scope when an end-to-end effect is unmeasured.

Example: “12,000 requests/minute” is insufficient if the harness counts rejected requests or compares a warm cache with a cold cache. Check accepted work, errors, equal data, and the contract's permitted tolerance before interpreting the rate.

## Result and Next Action

Report whether the evidence supports the claim, supports a narrower claim, or leaves it unproved. Include the observed comparison and variation, correctness evidence, valid inputs, measurement boundary, and residual uncertainty. Link raw receipts rather than copying complete logs.

If a defect is in the instrument, propose a bounded instrument repair and the check that distinguishes its error. Preserve product acceptance and budgets. Repeated identical green runs cannot prove a faulty oracle; a meaningful red/green or counterexample can. Use a new run only when it will resolve a stated question, and refresh only affected evidence after changes.

Method adapted from [pstack benchmark-checklist at df581122](https://github.com/cursor/plugins/blob/df581122cde17e6e27686b5a448bde23e4ad4318/pstack/skills/benchmark-checklist/SKILL.md).
