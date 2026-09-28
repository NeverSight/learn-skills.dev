---
name: reliability-engineering
description: >-
  Design, implement, or review software reliability behavior: observability, dependency failure,
  deadlines/retries, graceful degradation, recovery, backup/restore evidence, SLO/SLI reasoning,
  and incident learning. Start from the user/operational question or failure claim; add only the
  signals and mechanisms needed to answer or survive it. Reliability is proven by evidence and
  exercises, not by architecture diagrams alone.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.0"
---


# Reliability Engineering

Make failure behavior observable and recoverable without adding operational machinery by habit.

## Workflow

1. State the reliability claim or operational question: what user-visible behavior must survive or become diagnosable?
2. Map dependencies and failure modes: timeout, outage, stale state, overload, partial failure, restart, or data loss where relevant.
3. Choose the minimum useful signal: logs, metrics, traces, health/state probes, or an alert tied to an actionable condition.
4. Define deadlines, retry classification, degradation, isolation/backpressure, and reconciliation only where failure semantics require them.
5. For recovery, identify what must survive, what can be rebuilt, source of truth, restore/replay procedure, and proof.
6. Verify at the user/system boundary; alert clearance alone is not recovery evidence.
7. Convert meaningful incidents or near misses into regression/operational learning instead of adding permanent noisy instrumentation.

## Stop

Stop when the reliability claim has enough evidence and the relevant failure/recovery path is operationally understandable.
## Reference Guide

Load only the references needed for the current task:

- [incident learning](references/incident-learning.md)
- [observability](references/observability.md)
- [resilience recovery](references/resilience-recovery.md)
- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [authority](references/_shared/state/authority.md)
- [cache](references/_shared/state/cache.md)
- [provider neutrality](references/_shared/engineering/provider-neutrality.md)
- [evidence](references/_shared/verification/evidence.md)
- [risk depth](references/_shared/verification/risk-depth.md)
