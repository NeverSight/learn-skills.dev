---
name: code-review
description: "Review one implementation change against its Phat task, feature spec, acceptance criteria, repository engineering standards, and any accepted prototype evidence. In standalone or final mode record supported task evidence/status; in delegated mode return a read-only report to the parent. Use after implement-task or when reviewing a working tree, staged change, commit, or branch."
---

# Code Review

Review completed implementation against its documented contract and the repository's engineering standards.

Determine whether the change:

* satisfies the selected task;
* satisfies the acceptance criteria it claims to cover;
* stays within scope;
* is technically safe enough to maintain;
* has credible verification evidence.

Do not fix implementation code by default.

Do not expand scope.

Do not rewrite the requirement, spec, ADR, or task merely to make the implementation pass review.

The review mode controls the write boundary:

* **Standalone:** the user explicitly invokes `$code-review`; the reviewer may
  update the selected task's review evidence and status when the result is
  sufficiently supported, but it must not fix implementation code.
* **Final:** `implement-task` dispatches the reviewer as the single final
  review sub-agent after the task is already `in_review`, with `Mode: final`.
  The reviewer may update only the selected task's review evidence and status;
  approval may move the task to `done`, but the reviewer must not fix
  implementation code or modify any other repository state.
* **Delegated:** `implement-task` dispatches the reviewer as a dedicated
  sub-agent with `Mode: delegated`; the reviewer is strictly read-only and
  returns findings, evidence, and a status recommendation to the parent. This
  mode is for other read-only parent handoffs, not the final `implement-task`
  review stage. It must not modify task metadata or task status, and it must not
  dispatch another capability.

## Contents

- [Workflow](#workflow)
- [Review modes](#review-modes)
- [Read before reviewing](#read-before-reviewing)
- [Establish the review target](#establish-the-review-target)
- [Preserve unrelated work](#preserve-unrelated-work)
- [Review task evidence](#review-task-evidence)
- [Review criteria](#review-criteria)
- [Findings and status](#findings-and-status)
- [Re-review](#re-review)
- [Source-of-truth conflicts](#source-of-truth-conflicts)
- [Write boundary](#write-boundary)
- [Quality gate](#quality-gate)
- [Finish](#finish)

## Workflow

Follow this sequence:

```text
Read project context
        ↓
Identify exact review target
        ↓
Establish comparison base
        ↓
Inspect implementation evidence
        ↓
Review against spec
        ↓
Review engineering quality
        ↓
Run/inspect relevant checks
        ↓
Produce actionable findings
        ↓
Decide task status
        ↓
done OR $implement-task
```

## Read before reviewing

Read `AGENTS.md` first if it exists.

Then inspect:

* the selected task;
* the complete linked spec;
* acceptance criteria covered by the task;
* relevant requirement/context;
* relevant ADRs;
* implementation evidence recorded by `$implement-task`;
* prototype references in the spec and the exact accepted revisions when UI
  behavior or states are part of the task;
* the exact diff under review;
* relevant nearby code;
* relevant tests;
* repository-supported verification commands when needed.

Read the linked spec and selected task evidence in full. Do not use
`$compact-context` as a substitute for the canonical review target or its
acceptance criteria; temporary review notes may be compacted only after those
sources remain available.

Read only enough surrounding code to evaluate the change responsibly.

Do not turn a focused task review into an unrelated repository audit.

## Review modes

For a final review, the parent prompt must include `Mode: final` and the
complete review input contract. The task must already be `in_review`; record
only supported review evidence and status in that task, and do not edit
implementation or other repository files.

For a delegated review, the parent prompt must include `Mode: delegated` and
the complete review input contract. Return the review report without editing
any repository file; the parent owns recording the result, applying fixes, and
changing task status.

For a standalone review, use the normal task-document boundary below and record
supported review findings/status in the selected task. Do not infer delegated
mode merely because the task was previously implemented.

## Establish the review target

Identify exactly what is being reviewed.

Supported targets include:

### Working tree

Review both:

* unstaged changes;
* staged changes.

Do not assume "uncommitted changes" means only unstaged files.

### Staged change

Compare the index against `HEAD` unless another base is explicitly specified.

### Commit

Compare the selected commit against its parent unless another base is specified.

### Branch

Compare against:

* the explicitly named base; or
* the repository's appropriate merge base when the base is otherwise clear.

### Explicit files or diff

Review only the user-specified target while still reading enough linked context to evaluate correctness.

State the selected target and comparison base in the review result.

If there is no diff, say so.

Do not manufacture findings from unchanged code unless the user explicitly requested a broader audit.

## Preserve unrelated work

A working tree may contain changes outside the selected task.

Distinguish:

* changes owned by the selected task;
* unrelated pre-existing changes;
* ambiguous overlapping changes.

Do not attribute an unrelated modification to the task without evidence.

Do not review unrelated work as a defect in the selected task unless it directly affects the task's behavior or safety.

## Review task evidence

Before independently judging the implementation, inspect the task's recorded evidence.

For the checklist task contract, read the task's `Goal`, `Blocked by`, and
`Todo` items. Review results belong in the existing `Todo` checklist rather
than in a new task section.

Check whether evidence claims such as:

```text
test passed
typecheck passed
manual flow verified
```

are supported by actual recorded commands, results, or observable evidence.

Do not treat an evidence claim as automatically true merely because it appears in the task document.

Distinguish:

* verified during this review;
* previously recorded and credible;
* recorded but not independently verified;
* missing;
* contradicted by current evidence.

## Review criteria

Read [the review criteria reference](references/review-criteria.md) when
mapping acceptance criteria, judging engineering risk, evaluating verification,
or deciding whether an observation meets the finding threshold.

## Findings and status

When classifying findings, writing the review record, separating questions from defects, or deciding whether the task is approved, read [the findings and status reference](references/findings-and-status.md). It contains the P0–P3 definitions, finding format, no-findings record, and status-transition rules.

## Re-review

When reviewing a task after fixes:

* read previous findings;
* inspect the new diff;
* verify whether each previous required finding is resolved;
* check for regressions caused by the fix;
* do not repeat resolved findings;
* preserve previous review history when practical.

Do not require the implementer to re-prove unrelated areas unless the new changes affect them.

## Source-of-truth conflicts

If the implementation conflicts with the spec, do not modify the spec merely to approve the code.

If the implementation conflicts only with a prototype while the spec is
correct, review against the spec. If the prototype represents accepted
behavior missing from the spec, route to `$spec-with-prototype` before deciding
whether implementation changes are required.

Route based on the problem:

```text
implementation defect
    → $implement-task

task decomposition wrong
    → $to-tasks

behavioral contract incomplete or incorrect
    → $write-spec

new product/domain/architecture decision
    → $grill-workflow
```

Do not decide a new product or architecture direction inside review.

## Changed agreements and optional assessments

When the user intends to change an existing agreed behavior across its spec and
task plan, hand that change to `$change-scope`; do not rewrite the contract as
an implementation fix or review waiver. Unsettled product decisions still
belong to `$grill-workflow`. Resume only after the affected contract and task
readiness are reconciled. Existing batch authorization does not include new
follow-up tasks automatically.

`$verify-feature` can assess a requested cross-task acceptance question and
`$release-check` can assess a requested release candidate. Neither replaces
this skill's task verification/review contract or changes its status authority.
Do not invoke them as extra mandatory completion gates.

A selected task demonstrably retired by an accepted scope change has no pending
implementation approval. Report the withdrawal evidence and preserve its
historical status; do not mark it done or review withdrawn criteria as failures.

## Write boundary

Do not edit implementation code by default.

Do not silently fix findings during review.

Do not modify requirements, specs, ADRs, or acceptance criteria to obtain approval.

In standalone mode, you may modify the selected task document only to record:

* the `Status` transition;
* a blocker in `Blocked by` when review is blocked;
* review findings and the result as `Todo` checklist items.

In final mode, modify only the selected task document to record supported
review evidence and the `in_review`/`done` status transition. In delegated
mode, do not modify the selected task document or any other file; return the
same evidence and recommended status to the parent instead.

If the user explicitly asks for review and fixes in one operation, finish the review findings first, then hand the task back to `$implement-task` rather than mixing reviewer and implementer responsibilities silently.

## Quality gate

Before finishing, confirm:

* the review target and base are explicit;
* unrelated changes were not incorrectly attributed to the task;
* each claimed acceptance criterion was considered;
* findings are evidence-backed;
* severity reflects actual impact;
* style preferences were not reported as defects;
* passed and not-run checks are distinguished;
* prior implementation evidence was not blindly trusted;
* the checklist review record reflects what was actually inspected;
* status matches the review result;
* no source document was rewritten merely to make the code pass.

## Finish

Report:

1. review target and base;
2. task ID when applicable;
3. review result;
4. resulting task status;
5. findings ordered by severity;
6. acceptance-criteria verification summary;
7. checks run and results;
8. checks not run or remaining uncertainty;
9. next skill.

Use this routing:

```text
approved
    → task done

implementation findings remain
    → $implement-task

task decomposition problem
    → $to-tasks

specification problem
    → $write-spec

product/domain/architecture decision required
    → $grill-workflow
```

Do not begin implementing fixes automatically.

Do not commit or push unless explicitly authorized.
