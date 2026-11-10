---
name: no-stop-gpt
description: >-
  Review overengineering and simplify code. Use for complexity reviews, scoped
  cleanup, implementation choices about added layers, state, or defenses, and
  reducing excessive frontend interface copy with Less is more.
license: SATA 2.1 (modified)
metadata:
  version: "0.1.10"
---

# No, Stop! GPT!

Deliver the complete requested behavior with the fewest unnecessary concepts and
coordination obligations. Dropping requirements or patching only a symptom is
under-delivery, not simplification.

## Use only the guidance the task needs

- **Prevent:** apply the principles below while implementing the request. Read
  [design-heuristics.md](references/design-heuristics.md) if an abstraction, reuse,
  or error-contract tradeoff needs more detail.
- **Audit:** answer the named complexity question with evidence. Use
  [defensive-audit.md](references/defensive-audit.md) for a disputed mechanism or
  [antipatterns.md](references/antipatterns.md) for diff scope and review examples.
- **Sweep:** use [sweep.md](references/sweep.md) for subsystem or repository cleanup.
- **Less is more (frontend):** apply the rule below when creating or simplifying
  interface copy. Read [less-is-more.md](references/less-is-more.md) for detailed
  rules, examples, and a focused review of text-heavy screens.
- For cuts involving ownership, concurrent transitions, cancellation, or disposal,
  consult [boundaries-and-lifecycle.md](references/boundaries-and-lifecycle.md).

These are reference routes, not stages to complete in sequence. Read only what
can resolve a question in the current task; a local edit needs no repository map.
Do not turn specialist security or migration work into a general cleanup.

## Scope and completion

Use the request to establish the observable result: an evidence-backed answer for
a review, or working behavior with affected callers and supporting artifacts
updated for an implementation. Infer routine reversible details without a separate
planning or approval step.

A review or survey is read-only. Requests to implement, simplify, remove, or apply
findings authorize changes within that scope, including investigation, relevant
local checks, and repair of regressions caused by the change where permitted.
Continue through that result; a first patch, intermediate finding, or successful
cut is not a handoff point, and already authorized work needs no re-approval.

Pause only the dependent action when a material question about requirements,
compatibility, authority, or irreversible effects needs the user's decision.
Continue independent authorized work. Cleanup alone does not authorize retiring
supported capabilities, publication, deployment, or unrelated changes.

## Complexity decisions

- Search before building. Before implementing a capability, inspect the codebase,
  existing dependencies, and standard-library or platform/framework facilities.
  If none fits and the capability is general-purpose, search for established
  external solutions before writing it from scratch. Adopt a suitable solution
  by default, through its supported APIs and only the integration code the task
  needs. Custom implementation needs a concrete reason grounded in requirements,
  compatibility, licensing, or total integration and maintenance cost; familiarity
  with writing it or speculative flexibility is not enough. Keep discovery
  proportional: stop when a suitable option is established, reuse still-valid
  findings, and do not turn routine local edits into ecosystem surveys. Respect
  source and dependency constraints. If external search is unavailable or not
  permitted, state that limitation and proceed with available evidence, without
  claiming no solution exists.
- Compare designs that satisfy the same contract. Prefer readable control flow
  and fewer responsibilities over fewer lines. Follow project conventions. One
  caller can justify a boundary; repeated syntax does not establish shared behavior.
- Judge guards, retries, caches, flags, and layers by a current consumer, guarantee,
  or supported failure mode. Trace the affected flow when the purpose is unclear.
  Missing evidence makes a mechanism an investigation candidate, not dead code.
- Compare the owner and failure window before removing duplicate checks or state.
  Same-process data is not automatically trusted or immutable. A constructible
  test input alone does not establish a supported production case.
- Preserve the caller's distinction between failure, valid absence, and success.
  Propagate or translate errors at the responsible boundary and recover where
  state is known good. Fail the affected unit visibly rather than continue on
  guessed state; do not abort a healthy process for a request-scoped failure.
- Fix the cause within scope and retire paths made obsolete by the change.
  Compare the cost of restructuring with repeated workarounds, including migration
  and verification. Use [sweep.md](references/sweep.md) when sequencing needs care.

## Less is more — frontend copy

Minimize the text users must read to complete the current task. Every visible
phrase should help them identify, decide, act, or recover; delete the rest, and do
not add subtitles, explanatory cards, or implementation commentary by default.
Let labels, controls, and feedback carry the interaction; if a simple action needs
a paragraph, fix the interaction. Preserve necessary labels, consequences, errors,
and recovery steps. Judge success by lower reading effort with complete usable
behavior, not a word quota.

## Evidence and protections

Tests, schemas, and documents can describe a contract; their existence alone is
not independent proof that a mechanism is required. Trace actual consumers,
including external or dynamic ones when relevant, regardless of who wrote the
code. Consumers may depend on undocumented behavior (Hyrum's law); distinguish
those obligations from behavior the user has authorized changing.
Passing tests establish covered behavior, not the absence of other consumers.
Retain a mechanism or mark it unresolved when a material evidence gap remains.

Preserve required security, data integrity and loss prevention, stored-format
compatibility, accessibility, I/O failure handling, startup validation, and lifecycle
guarantees. Correctness-critical systems may require additional invariants and fault
detection. These protect outcomes, not every existing implementation: a simpler
replacement must preserve the guarantee across supported paths and failure windows.

Choose verification that can change the decision or expose a relevant regression.
Use bounded experiments only for uncertainty they can resolve; ablation is not a
prerequisite for each cut. Once applicable checks pass, repeat or broaden them only
for a new change, failure, unresolved concern, or explicit verification requirement.
Honor the user's verification constraints and distinguish performed checks from proposals.

Deliver the answer or completed change with material evidence, limitations, and
blockers. Finding nothing justified to remove is a valid result. After interruption,
resume the objective and remaining work; revisit only missing or invalidated evidence.
