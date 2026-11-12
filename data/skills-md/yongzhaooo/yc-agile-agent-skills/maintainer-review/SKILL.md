---
name: maintainer-review
description: Review a design, patch series, or named subsystem as a long-term maintainer. Use for rigorous architecture review of APIs, state, concurrency, compatibility and migrations, including Linux kernel design. Read-only, grounded in subsystem evidence. For a ranked list of module-deepening candidates, use codebase-design; for an ordinary diff, code-review; for an unimplemented approach's decision readiness, proposal-review.
---

# Maintainer Review

Determine which mechanisms earn their lifetime cost and whether a smaller contract meets
the same requirements. Review a proposal, patch series, or named subsystem directly;
no preliminary review skill is required. Return findings without implementing changes.

## Establish context

Identify the problem, constraints, intended behavior, consumers, and decision to enable.
For proposals, separate facts, choices, and assumptions. For patches, fix the requested
revision/range and inspect the series, including intermediate states. For an existing
subsystem, honor the named maintenance question and distinguish old debt from regressions.

Identify the intended destination branch/tree and base revision, not just the checked-out
branch. For each affected subsystem and requested backport destination, attempt to read
its contribution rules, maintainer profile, release policy and relevant API documentation.
Start with the target revision's repository instructions and linked official guides;
check current submission policy separately from version-specific implementation contracts.
Report material requirements with a source and applicable branch/version. Do not scan
unrelated branches. If the destination is unknown, continue technical review and keep
branch-specific readiness conditional; ask only when the answer changes the decision.
When sources conflict, compare dates, scope and revisions instead of silently choosing
one. An individual review exception is not a general rule. If a guide is inaccessible,
name the attempted source and unresolved requirement; do not invent its contents.

Read affected implementations and callers, existing helpers, and comparable in-tree
solutions. Consult focused history/blame when intent is unclear;
historical code is evidence, not a requirement to preserve it. Resolve discoverable
facts before asking the user; name decisive evidence that remains unavailable.

When responding to review, read the original comments and their target revision.
Separate questions, suggested designs, demonstrated defects, and style preferences.
Check each consequential premise against the code or evidence; reviewer authority
alone does not establish a race, hardware constraint, or need for a new mechanism.
Treat comments as starting evidence, not the review boundary. If a revision changes
state ownership, commit/error semantics or asynchronous recovery, reconstruct the affected
operation from its real caller through the final consumer-visible state. Establish the
call sequence and recovery obligations independently of the previous explanation and
fixtures. Revisit earlier conclusions whose assumptions changed, including paths that
the last comment did not mention; retain evidence for unaffected behavior. A local fix
can close a comment while leaving the operation incorrect.

For a disputed cause or workaround, establish when required state became valid and when
it was first consumed, not just its final sampled value. Read later corrections before
reusing a historical conclusion.

Trace a representative path across each consequential boundary and its relevant failure
or teardown path, including asynchronous consumers. Follow a state change through its
notification, scheduling, and consumer action: a correct field value does not prove that
the consumer sees it or reconfigures. For proposals, define the observable behavior and
error/recovery semantics before choosing a mechanism; distinguish analysis from tested code.
For a consequential correctness claim, apply the relevant proof in
[Evidence at review boundaries](references/review-evidence.md). Support it with concrete
paths and contracts, or mark the guarantee unresolved; a checklist label is not evidence.
Finish the requested path's proof before expanding to neighboring issues. In particular,
follow potentially final releases through the remaining expressions and return/unlock
paths. Additional findings do not substitute for answering the named review question.

## Challenge consequential mechanisms

Account for new or changed interfaces, independently owned state, abstraction boundaries,
configuration, dependencies, and distinct behavior paths. Group elements sharing one
rationale. Apply relevant questions without printing a defense for every local helper.

- **Need and reuse:** what requirement fails without this mechanism? Name applicable
  existing facilities and compare semantics, errors, ownership, execution context, and
  relevant performance. Check encodings, reserved values, early returns and side effects
  when reusing a helper across devices or modes. Reuse that increases cross-owner coupling
  may be worse.
- **Cause and repair location:** identify the earliest violated contract on the observed
  path and its owner. The repair may belong elsewhere when ownership, reach or risk favor
  it. A working disable flag does not prove the disabled feature is defective. Before
  adding a persistent knob or board quirk, compare correcting setup/order with a bounded
  workaround; neither requires an unrelated redesign.
- **Layer and interface:** why does responsibility live here? What must callers learn or
  coordinate? When a wrapper or boundary is contested, apply the deletion and interface
  tests in [codebase-design](../codebase-design/SKILL.md). One caller or implementation
  can justify a useful invariant or meaningful test seam.
- **State and lifetime:** identify the source of truth, creator, readers, mutators,
  synchronization, and destructor. What enforces the invariant through partial failure,
  cancellation, concurrency, and teardown? Cached state needs a validity rule;
  duplicated authority needs a concrete justification. Before claiming a race, trace
  actual writers and outer serialization as well as asynchronous callbacks. Specify the
  whole transaction a lock protects, not just individual accesses or its name.
- **Failure and misuse:** which ordering, ownership, input, and context preconditions
  are enforced, and which rely on caller discipline? Construct a realistic failure
  sequence through actual or proposed consumers and locate the preventing guarantee
  or missing contract. Avoid invented callers used only to demand defensive layers.
  Unobserved states are not thereby impossible: before removing a guard, establish its
  contract and define what happens if its condition occurs. Separate proven code defects
  from claims about how often or on which hardware they occur.
- **Evolution:** distinguish internal contracts from public APIs and persistent formats.
  Who migrates consumers? How do supported mixed versions, rollback, and partial
  migration preserve invariants? Stable-contract extension can justify structure before
  a second use; speculative variants alone cannot.
- **Lifetime cost:** assess resource use, contention, debugging/operational burden, and
  change propagation where relevant. Optimization claims need workload and measurement
  evidence. Compare total system cost; neither fewer lines nor 'cleaner' is sufficient.
- **Patch structure:** separate independent cleanup, behavior changes, and migrations
  where useful while preserving valid intermediate states. A coherent contract change
  may require many components; file count alone is not an objection.
- **Verification:** what observation would falsify the behavior or invariant? Check
  relevant failure, concurrency, and compatibility evidence. Tests of real internal
  invariants count; tests mirroring assignments or control flow provide little proof.
  Before relying on a passing harness, apply the model-fidelity method in
  [Evidence at review boundaries](references/review-evidence.md): real functions inside a harness
  still inherit its assumptions at replaced boundaries. A synthetic input proves
  handling of that input, not its reachability. Match evidence to the claimed revision,
  configuration, path and consumer-visible result. Ask for the smallest check that
  resolves a decision; do not require hardware reproduction for a defect established
  by code, or repeat unrelated experiments after prose edits. A successful subset on
  one fixture does not justify removing established setup for other supported modes.
  Leave experiment orchestration to the pilot or implementation plan.

For Linux work, apply [Linux kernel review](references/linux-kernel.md); otherwise use
the project's domain contracts.

## Verdict

Lead with a justified direction, changes needed, or decisive evidence still missing.
Where the current approach is misdirected, give the best supported alternative and what
would change that recommendation; criticism alone does not help choose a repair.
Distinguish a viable design from an implementation ready for the named destination.
Briefly state the reviewed revision, applicable rules and boundaries actually checked;
name material unchecked paths rather than implying whole-subsystem approval.
Report findings by consequence: location/passage, supporting evidence, concrete failure
or maintenance cost, and smallest credible correction. A relevant caller, existing
mechanism, contract, historical decision, or measurement can supply evidence.

Distinguish demonstrated defects, missing guarantees, and optional preferences. Block
only on questions whose answers change the decision; explain the required guarantee
and how to establish it. Unspecified crucial lifetime, compatibility, or failure
semantics cannot earn approval. Accept sound improvements with non-blocking concerns;
omit empty categories and explain justified complexity only when contested or at risk.
Stop once material questions and affected paths are covered, noting remaining gaps.

Return in chat unless a durable review is required. Keep findings with their reviewed
artifact; accepted actions belong to its task/plan. A favorable technical verdict is not
user acceptance, proof of deployment, or a reason to create Wayfinder entries.

When outgoing patch mail is in scope, review commit message/cover separation and
delivery with the project's patch-mail workflow. Keep the technical rationale here concise;
an investigation log is not the justification each individual patch needs.

## Lessons

- Checking the producer and its unit test missed a consumer notified only on state
  transitions. Judge the promised behavior at the consumer boundary.
- A reviewer's concurrency question and a synthetic invalid-state test were treated as
  evidence of reachability. Establish that premise separately, while retaining defects
  that can be proved without a field report.
- A successful replay of the examples used to write a rule did not establish transfer to
  unfamiliar patches. When revising this skill, follow
  [Behavioral calibration](references/review-calibration.md), rather than judging strength
  by finding count or by a trial agent's own pass label.
- A trial found neighboring lifetime bugs but missed an access after the final put in
  the requested function. Complete that function's ownership transitions and subsequent
  uses before broadening the review.
- A qca8k revision fixed the previously reported restore error but missed a second CPU
  callback rejecting an already committed MTU. The review inherited the fixture's
  single-call assumption instead of reconstructing the whole operation.
