---
name: design-verifiable-slices
description: "Turn implementation work into bounded, independently verifiable slices with success criteria that reject plausible wrong outputs. Use when planning agent work, strengthening weak acceptance criteria, choosing among unit, property, contract, integration, Gherkin, end-to-end, QA, build, coverage, mutation, or quality gates, or when a task risks context decay."
---

# Design Verifiable Slices

Treat verification as the boundary around generated work, not as ceremony after
implementation. Shape the current slice so a capable agent can complete it from
authoritative context and its result can be distinguished from credible wrong
results by direct evidence.

## Preserve authority

Consume approved behavior, non-goals, ownership, and interfaces as fixed inputs.
Return missing product or design decisions to their owner. Decide task boundaries
and proof here without inventing behavior or prescribing implementation choices
that the sources leave open.

## Bound the work by cognition and proof

Prefer one coherent behavioral change that an agent can understand from named
sources in a fresh working context and verify before beginning unrelated work.
Use judgment rather than file, line, step, or token quotas.

Split when the work combines independent outcomes, still contains an unresolved
authority decision, crosses competing writable ownership, requires broad
rediscovery, or cannot be verified until later work exists. Keep coupled changes
together when separation would create a meaningless or unverifiable intermediate
state. The useful boundary is the smallest independently provable outcome, not
the smallest edit.

## Make success discriminating

Reason from the credible ways the result could be wrong while still looking
finished. A strong check observes the approved outcome directly and would fail
for the material wrong results. A passing command, high coverage number, or
agent report is weak when it does not make that distinction.

Choose the form that best exposes the proof in the current repository. Do not
force a taxonomy, table, or fixed set of fields. The plan only needs enough
information for an executor or reviewer to understand what observation decides
success and why a superficially plausible implementation would not pass.

## Choose checks from the failure, not from a checklist

Use the narrowest evidence that can detect the relevant failure, then add a
broader check only when it contributes a different signal.

- Static, compile, type, schema, and lint checks suit structural properties they
  actually analyze.
- Unit and property tests suit deterministic rules, boundaries, and input
  classes; contract and integration tests suit protocols, persistence, adapters,
  and cross-module behavior.
- Executable Gherkin can carry authoritative business examples. End-to-end
  automation or precise QA can observe user-visible behavior and runtime wiring.
- Quality metrics need a meaningful baseline, workload, threshold, and
  measurement method. Coverage locates unexercised code but does not prove the
  assertions; mutation testing is useful only when its extra signal justifies
  its cost.

These are options, not required layers. Prefer repository-native checks and
exact commands already supported by the project. Leave an unknown invocation
open instead of inventing a plausible CLI.

## Challenge the proof

Before accepting the slice, ask whether unchanged, stubbed, hard-coded,
partially wired, or mock-satisfied work could pass. Strengthen the observation
when it could. Demonstrate that a focused new check detects the absent or known
wrong behavior when practical. Add negative, boundary, regression, performance,
security, accessibility, or manual checks only when the actual failure model
gives them information value.

Reject flaky or proxy evidence when it cannot support an execution decision.
Ordinary test failure sends implementation back to correction; only evidence
that invalidates the plan's assumptions, authority, or task boundary sends work
back to planning.

## Completion bar

Finish when the slice is taskable without reconstructing broad design history,
the selected evidence directly constrains its approved outcome, and the proof is
strong against the material failures without adding low-signal ceremony. Present
that reasoning in the clearest task-specific form rather than filling a template.
