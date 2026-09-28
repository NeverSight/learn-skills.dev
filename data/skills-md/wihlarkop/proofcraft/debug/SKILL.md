---
name: debug
description: >-
  Investigate and fix software failures through evidence, reproduction, boundary tracing, root-
  cause analysis, and focused regression verification. Use for bugs, flaky behavior, CI/test
  failures, unexpected state, or production-like defects. Do not patch by guesswork when the
  failure can be investigated; preserve unrelated working-tree changes and stop once the root
  cause and fix are evidenced.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.1"
---


# Debug

Find the failure mechanism before committing to a fix.

## Workflow

1. Reality-check current code, errors, recent relevant changes, environment/config differences, accepted project artifacts, and working-tree state. Treat a reported symptom as a claim to investigate, not an established fact.
2. Classify the material concerns touched by the failure and load only the relevant domain skill contracts. Debug remains the sole core workflow owner: do not invoke `accept`, `review`, `implement`, or another sibling core workflow merely to gather evidence or close the investigation.
3. Reproduce consistently when possible. Choose the smallest experiment that can falsify the report or current hypothesis. Do not run broad or expensive verification merely because it exists; bound retries/waits, and record hung or incomplete commands as missing evidence rather than pass/fail evidence.
4. Distinguish observed facts, reproducible failure, plausible but unproven hypotheses, and states that cannot occur in the current implementation. If the report depends on a future/unimplemented schema, feature, deployment state, or configuration, say so explicitly rather than inventing a current root cause.
5. Trace data/state across the smallest relevant boundaries. In multi-component systems, instrument boundary inputs/outputs only when needed to isolate where reality diverges.
6. Form a concrete root-cause hypothesis only when current evidence supports one, then seek evidence that could disprove it. A plausible mechanism without a reproducer or repository evidence remains a hypothesis, not a root cause.
7. Respect the requested remediation boundary. If the user asked for investigation only or explicitly prohibited edits, stop before changing files and report the strongest evidence plus the regression evidence a future fix would need.
8. When repair is authorized and a real mechanism is evidenced, implement the smallest correct fix that addresses the mechanism rather than the symptom.
9. Add or update focused regression evidence and rerun only the affected scope needed to show the fix removed the failure without introducing relevant regressions.

Do not ask the user to copy facts that logs, source, test output, or repository state can expose directly.

## Outputs

Observed facts, reproduction status, root cause when evidenced, plausible-but-unproven hypotheses, impossible/not-yet-applicable states, fix and regression evidence when repair is authorized, and explicit remaining uncertainty.

## Stop

Stop when the reported behavior is either reproduced and explained, or falsified/not currently applicable with sufficient evidence. If evidence cannot converge after bounded investigation, report the strongest localization and blocker rather than cycling through speculative patches.
## Reference Guide

Load only the references needed for the current task:

- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [reality check](references/_shared/orchestration/reality-check.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [diff discipline](references/_shared/engineering/diff-discipline.md)
- [evidence](references/_shared/verification/evidence.md)
- [verdicts](references/_shared/verification/verdicts.md)
- [regression scope](references/_shared/verification/regression-scope.md)
- [risk depth](references/_shared/verification/risk-depth.md)
