---
name: feature-plan
description: Create or revise a feature specification and divide it into small stages with observable goals, dependencies, and verification. Use for a brief, an existing large specification, or updating upcoming stages after implementation. Does not start coding.
---

# Feature Plan

Define the contract needed for the current scope and small stages the user can
assess separately. Preserve earlier decisions and user instructions;
existing material does not require restarting discovery.
Carry the requested planning work through to a reviewable specification and
delivery map. After the user resolves a question, continue the remaining work
without requiring another instruction to draft contracts or divide the stages.

## Specification

1. Read the input, repository instructions, and code needed to confirm the
   boundaries of the change. Use the existing document structure.
2. Describe the goal, scope, exclusions, state ownership, shared contracts,
   and meaningful failure behavior. Include migration, deployment, and rollback
   when relevant. Match detail to the risk and complexity.
3. Separate accepted decisions from recommendations and unknowns. Present the
   main choices and their consequences. Earlier acceptance of the recommended
   set is sufficient; silence is not acceptance.
4. Distinguish design decisions from execution prerequisites, such as environment
   availability. An open issue blocks only stages whose scope or credible
   verification depends on it. Prepare the remaining design for review.

For each new persisted field, state, background process, or abstraction, identify
the current behavior or concrete safety need that requires it. Prefer existing
state, derived values, and configuration where they suffice; persist facts that
must survive and cannot be safely reconstructed. Defer machinery whose consumer
belongs to a later stage. Specify the required failure guarantee before choosing
a recovery mechanism; automatic recovery is not implied by safe failure handling.
Record deliberate limitations and their cost in the existing scope or exclusions.
If simplifying an accepted contract changes behavior, present that trade-off for
a decision instead of silently weakening the contract.

## Divide into stages

Each stage has one primary outcome that can be run or checked.
Name it as a behavior, such as "the file reaches storage", and define its finish line.

- Record actual dependencies, scope, and explicit exclusions. Choose an order
  that gives early feedback and lets the user assess one change at a time.
- Plan demonstrations of success, a meaningful failure, and preservation of
  affected behavior. Failure handling ships with its operation; final integration
  verifies that the parts work together.
- A stage must be verifiable without implementing its successors. A technical
  foundation is a useful stage when it has evidence of working, such as reading
  an object with the correct role and rejecting reads by the wrong role.
- Split a stage again if its outcome needs several independent demonstrations
  or too many changes for one review. First remove unnecessary machinery;
  dividing the same overbuilt design into more stages does not simplify it.
  Do not impose a universal limit on stages, fields, files, diff lines, or time.
- When the breakdown depends on an unknown mechanism, define an investigation
  with a question, a bounded experiment, and evidence. Its result may change the plan.
- Explain how the stage can merge without prematurely exposing an incomplete
  feature. Identify demonstration boundaries and test doubles; do not plan
  simulated success in the application in place of missing integration.

## Documents and updates

When a specification document is needed, create or update its working skeleton
after the initial repository and scope checks. Add the known contracts and stage
map, then refine this same document as the analysis progresses. Mark unresolved
decisions and experiments at the affected boundaries; finish the independent
parts without waiting for every detail to be settled.

The main specification owns shared contracts and the delivery map: stage ID,
actual dependencies, observable goal, and a link to details. Detail only the
next one to three stages; leave the rest as outlines in the map.
Use the [stage template](assets/stage.md), adapting it to existing documents.
An example layout is `docs/features/name/spec.md` and `docs/features/name/01-goal.md`;
existing `.ai/specs` or other repository conventions take precedence.

Stage documents reference shared rules instead of copying contracts. The brief
preserves decision context; the specification is the current contract. Keep
execution results in the PR, or in the conversation summary before a PR exists.
Do not add another index, state files, reports, or placeholder documents for
later stages. A small feature may have one stage described in the conversation
or PR, without a new specification.

When `feature-loop` coordinates delivery, it may keep a compact execution
checkpoint in this specification and evidence in the existing stage documents.
The coordinator owns these shared updates; delegated planning returns proposed
changes. Follow its coordination contract without duplicating the backlog.

After implementation, check whether new evidence changes the plan. Update
related contracts and stages together while preserving IDs; use P04a and P04b
when splitting a stage, for example. Bring material changes to scope or behavior
to the user for a decision.

## Readiness and handoff

Check that every part of the scope has a stage, dependencies permit the stated
order, and the proposed demonstration actually proves the goal. Identify gaps.
A stage is ready to implement when the necessary decisions are resolved,
dependencies are satisfied, and verification is feasible. A completed
specification does not imply completed implementation or a verified environment.

Present the first ready stage for review. An optional separate design review
can use `$feature-review`; implementation of a selected stage can use
`$feature-step`. These skills are not required to use the documents.
Continue already requested follow-up work without asking the user to invoke
another skill. A completed plan alone does not authorize implementation.
At the requested task boundary, summarize the result, readiness, and any
remaining decision or missing evidence naturally in the user's language.
