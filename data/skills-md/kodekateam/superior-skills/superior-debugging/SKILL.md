---
name: superior-debugging
description: Diagnose and repair reproducible, intermittent, environment-specific, or production-observed software failures by tracing evidence to a root cause. Use when a symptom exists but its cause is uncertain or when a proposed fix needs causal validation. Do not use for feature implementation, speculative cleanup, or a general review without a concrete failure.
---

# Superior Debugging

Turn an observed failure into a supported causal explanation, then make the smallest complete repair. Preserve the user's scope and the repository's existing architecture while distinguishing evidence from assumptions.

## Define the failure precisely

Before changing code, establish:

- the observed result, expected result, and source of that expectation;
- the smallest known reproduction and whether it is deterministic;
- the affected versions, environments, inputs, users, or data states;
- the last known good state when evidence exists;
- impact, urgency, and any unsafe reproduction boundary.

Do not silently redefine expected behavior to match the implementation. If the contract is ambiguous, identify the ambiguity and use repository evidence or user direction before treating either behavior as a defect.

## Follow evidence to cause

Read [references/evidence-driven-diagnosis.md](references/evidence-driven-diagnosis.md) when the cause is uncertain, multiple hypotheses are plausible, or a regression must be narrowed through history or controlled experiments.

Trace the failing path across the boundaries that can own the symptom. Inspect actual values, state transitions, configuration, persistence, external responses, and timing rather than inferring them from nearby code. Maintain a small set of falsifiable hypotheses and run the cheapest discriminating check first.

Separate:

- **trigger:** the input or condition that exposes the failure;
- **root cause:** the violated invariant or incorrect behavior that makes failure possible;
- **amplifier:** retries, caching, concurrency, stale state, or error handling that increases impact;
- **symptom:** the user-visible or operational result.

Do not stop at the first suspicious line, exception site, or correlated event. A stack frame shows where a failure surfaced, not necessarily where it originated.

## Diagnose runtime boundaries safely

Read [references/runtime-and-distributed-failures.md](references/runtime-and-distributed-failures.md) for environment-only failures, asynchronous or concurrent behavior, queues, caches, databases, external services, resource exhaustion, or production telemetry.

- Prefer existing logs, traces, metrics, error reports, and safe local reproduction before adding instrumentation.
- Redact secrets, tokens, personal data, and sensitive payloads from diagnostics.
- Do not experiment on production traffic, mutate shared data, disable safeguards, or increase broad logging without explicit authorization and a rollback plan.
- Do not treat a timeout increase, retry, cache clear, process restart, or swallowed exception as a root-cause repair unless the contract proves it is the correct behavior.

## Repair at the owning boundary

Once evidence identifies the cause:

1. state the causal chain in one concise explanation;
2. change the boundary that owns the violated contract;
3. preserve compatibility and unrelated behavior;
4. remove temporary diagnostics that are noisy, sensitive, or no longer useful;
5. add or update a regression test when practical and credible;
6. verify the original reproduction and relevant neighboring behavior.

If evidence disproves the suspected code defect, report the actual cause instead of forcing a code change. If the cause remains uncertain, label the result as partial and preserve the next discriminating observation or experiment.

## Report confidence honestly

Report:

- symptom and confirmed scope;
- evidence inspected and reproduction status;
- root cause, with trigger and amplifier separated when relevant;
- repair and why it addresses the causal mechanism;
- verification performed and its result;
- remaining uncertainty, untested environments, and operational follow-up.

Do not claim a production-only incident is resolved solely because a local test passes. State whether the result is reproduced, mitigated, repaired, or still under investigation.

## Combine skills narrowly

- Use `superior-code-review` when the primary task is to assess a change set rather than diagnose an observed failure.
- Use `superior-logic` when the confirmed repair changes domain rules, persistence, state transitions, or API behavior.
- Use `superior-database` when the confirmed cause requires schema, query, transaction, migration, or data-repair work.
- Use `superior-performance` when the confirmed cause leads to measured optimization, capacity analysis, or a performance budget.
- Use `superior-reliability` when the confirmed cause requires resilience, degradation, recovery, alerting, or runbook changes.
- Use `superior-delivery` when the failure belongs to a pipeline, artifact, rollout, or environment-promotion path.
- Use `superior-testing` when regression design, test isolation, or flaky-test diagnosis becomes a primary concern.
- Use `superior-api-security` when the failure reveals an authorization, validation, abuse, token, SSRF, or information-disclosure weakness.
- Use `superior-docs` after a verified material repair or when a durable diagnostic or recovery procedure changes.

Do not broaden diagnosis into unrelated refactoring, observability-platform adoption, performance optimization, or architecture redesign.
