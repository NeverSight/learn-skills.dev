---
license: MIT
name: jj-plan-restack
description: >
  Review a Jujutsu stack's behavior and design adoption, then plan coherent
  commit boundaries, dependencies, fixes, and validation. Use for restack
  planning, feature extraction, or post-restack review without changing source
  files, history, refs, or configuration.
---

# Plan a Jujutsu Restack

Produce an actionable reconstruction plan. Review the whole stack before
choosing boundaries. This skill works independently of `jj-execute-restack`.
Feature recognition and user discussion below are mandatory for both planning
and result review.

For an existing rebuilt stack, follow [review the result](references/review-restack.md)
instead of assuming the execution report proves correctness. Review is read-only;
report defects and proposed owners without repairing history.

## Review and design

- Require the intended repository's `.jj` directory and verify `jj root`.
  Resolve explicit `BASE` and `SOURCE_TIP`; never infer the stack from `@` alone.
  Use `jj --no-pager --ignore-working-copy` and a fixed operation for source
  reads. Preserve files, history, refs, working-copy state, and configuration;
  write only requested planning artifacts and temporary analysis files.
- Find the requirements in the request or supplied specification. Read every
  source change's full description (subject, body, and trailers), every parent
  diff, relevant milestone tree, final implementation, callers, and tests.
  Use `jj --no-pager --ignore-working-copy --at-op <op> log --no-graph -r <source> -T description`
  for full descriptions at the fixed snapshot; read any truncated output in
  full before choosing boundaries. Subjects and shortened log views do not
  replace this reading. Preserve substantive description details in the plan
  and proposed descriptions; follow the stack-design accounting rules below.
  Trust only substantive descriptions, checked against code and consumers.
  A `refactor` may add a feature; classify actual effects and flag uncertainty.
  Review design adoption, observable behavior, errors, compatibility, lifecycle,
  and interactions. Mark unavailable requirements or evidence as unverified.
  Do not spend review time on formatting or linter checks.
- Execute `recognize-stack-features` to establish the feature map, then follow
  [stack design](references/stack-design.md) for the inventory, semantic
  timeline, redistribution map, boundaries, and order. Each source-commit summary
  must include later code fate, consumer status at introduction and tip, and
  development-line membership from recognition, with evidence or explicit gaps.
  Use the read-only
  [analysis helpers](references/dependency-analysis.md) for advisory evidence;
  textual applicability does not establish semantic dependency or ownership.
- Propose fixes with acceptance criteria and destination owners; do not implement
  or commit them. Distinguish authorized fixes from recommendations and unresolved
  behavior decisions. A same-base history-only request preserves the source tree.
- For planned features or fixes, specify the concrete affected modules, key
  function signatures and caller wiring, and important data structures with
  fields, types, variants, and invariants. Identify existing contracts reused
  unchanged; conceptual descriptions alone do not settle implementation choices.
  Do not introduce new design merely to reorganize unchanged history.
- Provide reproducible fixtures for planned features and fixes: setup, input or
  action, independently justified expected result, execution boundary and command
  or harness, and destination owner. New-feature fixtures define acceptance
  criteria the implementation must make pass. Fix fixtures must fail for the
  reported defect before the repair and pass afterward with the same expectation;
  unrelated build or harness failures do not count. Reuse source fixtures where
  sufficient; distinguish planned checks from observed evidence. Additional unit
  tests can cover behavior but cannot replace these fixtures. Avoid tautologies,
  implementation-derived expectations, and mocks that hide the checked contract.
- When rebuilding onto another branch, typically a newer trunk, follow
  [destination-base planning](references/plan-contract.md#another-destination-base).
  Pin the destination separately from the source base; account for fully or
  partially ported and superseded work before choosing retained commits.
- Conflicts already present in the original stack may result from intentional
  feature removal. Inspect the conflicting sides, removal history, and stated
  requirements before proposing a resolution. Do not plan to restore an
  intentionally removed feature to clear a conflict. If intent remains unclear,
  ask the user and leave the affected resolution undecided.
- For selective feature extraction, follow [extraction scope](references/feature-extraction.md).
  Record retained and excluded capabilities, dependency closure, and the expected
  content delta. Extraction is a content change, not a waiver of verification.
- Distinguish [partial porting from a full rebuild with a focused prefix](references/feature-extraction.md#partial-porting-or-a-focused-full-rebuild).
  Select semantic contributions across mixed commits. In a full rebuild, move
  out-of-focus work last; an explicit user request may make that suffix
  presence-only, overriding whole-stack review/validation requirements for it.
- If the mainline must preserve behavior, record the behavior baseline and route
  every feature or fix that changes it to residuals, including work already in
  the source stack. Preserve requested reference work on side branches at the
  appropriate milestones, not in the mainline. Follow the
  [behavior-preserving contract](references/feature-extraction.md#behavior-preserving-mainline).
- Cover the full design and reserve justified future extension boundaries without
  speculative implementations. Preserve meaningful migrations and removals,
  including capabilities absent from the final tree.
- Label design questions as required now, required before later dependent work,
  or deferred, with consequences and resolution triggers. Do not introduce
  immature or unsound feature implementations as fixes or early prerequisites;
  reserve optional possibilities with a brief note and minimal existing boundary.
  Essential uncertainty needs bounded investigation or redesign before dependent
  execution. If unsound behavior already exists in the source, report it and seek
  an authorized correction; a same-base history-only restack must still preserve the tree.

## Recognize features and discuss with the user

Read and execute `recognize-stack-features` against the pinned source stack
before choosing target commit boundaries or order. A commit inventory, helper
output, or a final-tree partition does not replace feature recognition. If the
skill is unavailable, report the missing prerequisite rather than silently
substituting an abbreviated analysis. For result review, also reconcile the
rebuilt stack's actual capabilities and adoption with the source feature map.

Present the evidence-backed map to the user: outcomes, production adoption,
source ownership, dependencies, meaningful intermediate or removed capabilities,
and unresolved gaps. Explain proposed splits or combinations and justified
future extension boundaries. Ask the user to confirm or correct the inferred
feature scope, boundaries, and intent, highlighting decisions that affect
retention, exclusion, or behavior. When asking the user to decide, use simple,
direct language and say what each choice would keep, remove, or change. Avoid
jargon and overly formal wording. Give a short example when it makes the
difference clearer. Wait for their response and reconcile it with
the evidence before finalizing the plan or boundary findings; do not treat
silence as agreement. Prior explicit decisions can settle individual questions,
but do not replace presenting and discussing the recognized map.

Record the resulting decisions and remaining uncertainty. Continue independent
read-only investigation while awaiting the discussion, but do not mark the plan
executable while this step or a required behavior decision remains unresolved.
If later evidence materially changes the map, discuss the affected decisions
again before finalizing the revised boundaries.

## Deliver the plan

Use the [handoff contract](references/plan-contract.md). Retain the longest
unchanged prefix compatible with the destination ancestry; a later fix
targeting it moves the affected boundary into the
rebuilt suffix. If no changes are needed, report a no-op.

Use short jj change IDs with descriptions in user-facing material; keep exact
commit and operation identities in a separate internal snapshot record. Local
plan files are deliberately untracked: do not check their tracking status or
reread them merely to confirm they were written.

For an execution request, continue with `jj-execute-restack` after the required
feature discussion and completed planning when available and authorized. Do not
ask for an additional execution approval merely because planning is complete.
If the executor is unavailable, deliver the plan and report that execution needs it.
