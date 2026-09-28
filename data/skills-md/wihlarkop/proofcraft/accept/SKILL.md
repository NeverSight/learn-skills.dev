---
name: accept
description: >-
  Verify software behavior against observable acceptance criteria using risk-appropriate evidence.
  Use for manual acceptance, integration/contract/E2E checks, regression strategy, exploratory
  checks, or an explicit test-focused request. Render PASS/FAIL/BLOCKED/NOT RUN from direct
  evidence, compose material domain specialists when they affect what the evidence proves, and
  keep acceptance read-only unless fixes are explicitly requested. TDD is available as an optional
  technique, not the default acceptance workflow.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.1"
---


# Accept

Prove product behavior rather than merely running a test command.

## Workflow

1. Start from project-local product/spec/ADR/plan/acceptance artifacts and the implemented behavior being claimed.
2. Convert each material criterion into an observable pass/fail condition.
3. Identify material verification concerns and load the relevant domain skill contracts before choosing evidence. For example, mobile runtime claims may need mobile-engineering, rendered interaction claims may need ui-engineering, and persistence/restart claims may need database-engineering. Do not load incidental specialists.
4. Choose evidence by risk: unit, integration, contract, E2E, rendered UI, manual/device interaction, exploratory testing, or a combination.
5. Collect evidence directly when the environment exposes it. Distinguish what host tests prove from what requires a real device, browser, external system, or other runtime surface.
6. Report each required criterion as PASS, FAIL, BLOCKED, or NOT RUN. Missing evidence is not PASS.
7. Keep acceptance read-only by default. If a criterion fails, record the exact observed mismatch and the smallest affected scope before changing code. Only fix during the same workflow when the user explicitly asks for repair; after an authorized fix, rerun the failed scenario and affected regression subset.
8. Give an aggregate status without hiding incomplete evidence. If any required criterion is BLOCKED or NOT RUN, do not describe the whole acceptance as fully passed; summarize the counts and name the remaining gate.

## Test strategy

Tests should protect behavior and failure modes at the level that can actually falsify the claim. Do not require every behavior to have every test level.

TDD may be used when explicitly requested, required by repository convention, or deliberately selected because test-first discovery helps the task. It is not implied by this skill.

## Stop

Stop when every required criterion has an evidence-backed verdict, the boundary of each evidence source is explicit, and any remaining gate is clearly identified.
## Reference Guide

Load only the references needed for the current task:

- [tdd](references/tdd.md)
- [principles](references/_shared/constitution/principles.md)
- [reality check](references/_shared/orchestration/reality-check.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [acceptance](references/_shared/artifacts/acceptance.md)
- [evidence](references/_shared/verification/evidence.md)
- [verdicts](references/_shared/verification/verdicts.md)
- [risk depth](references/_shared/verification/risk-depth.md)
- [regression scope](references/_shared/verification/regression-scope.md)
