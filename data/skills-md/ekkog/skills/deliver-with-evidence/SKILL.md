---
name: deliver-with-evidence
description: Execute an explicitly approved multi-step engineering plan with proportional evidence, role-based review, Delivery tracking, and local commits. Use for approved broad refactors, migrations, and end-to-end programs; do not use for planning, status questions, ordinary review, or a single bounded fix.
---

# Deliver With Evidence

Execute one reviewable part of an approved plan at a time and keep local
progress distinct from Whole Goal completion.

## Start From Approval

Before production work, verify that the approved contract contains the final
outcome, scope and exclusions, Work Packages and dependency graph, acceptance
labels, compatibility promises, intentional removals, risks, exceptions, and
required evidence. If it is missing or materially changed, stop and hand the
work to `$design-delivery-plan`.

Every approved plan executed through this skill requires a private persistent
Delivery document before the first production edit. Read the relevant parts of
[references/delivery-document.md](references/delivery-document.md) for path,
permissions, fields, repository state, and atomic updates. The coordinating
agent is its only writer. Keep the document after completion.

Before costly work, resolve material unknowns about toolchains, required gates
or evidence access with the cheapest useful preflight. This establishes
feasibility, not acceptance, and does not itself require a reviewer. Keep
routine preflight and its in-scope fixes within the current Slice.

## Keep Implementation Minimal

Implement only the current approved outcome. Prefer the simplest, most direct,
verifiable and maintainable option with the smallest necessary change. Add
complexity only when a simpler option cannot meet an explicit requirement,
and explain that requirement. Keep scope within the approved contract.

Before adding a module, abstraction, state, workflow, dependency, or resilience
mechanism, identify its concrete value for the current goal; omit additions
without one. For known, stable inputs, environments, and usage, rely on explicit
contracts and focused tests rather than compatibility for hypothetical changes.
Preserve the contract's required security, reliability, and compatibility.

The coordinator asks the user to resolve material requirement tradeoffs before
implementing the affected choice. Delegated roles return such decisions to the
coordinator; routine in-scope implementation choices remain local.

## Route Execution Roles

- Use `explorer` only before Slice selection when a bounded unknown can change
  Slice scope, authority, dependencies, or acceptance. The `executor` owns
  ordinary Slice-local discovery.
- Delegate every non-trivial approved production Slice to `executor`, including
  resumed and corrective Slices. The main agent may implement a simple low-risk
  Slice directly. Treat a Slice as non-trivial when it crosses files or
  modules, changes a shared authority, needs isolated write context, or has
  acceptance evidence that the main thread cannot safely own. Reuse an executor
  for continuing work and corrections within one domain, authority and
  acceptance context. Start a fresh executor for an independent domain with a
  minimal complete packet; stop the prior writer before transferring ownership.
- Use `implementation_reviewer` only at a stable risk boundary where later
  work depends on the boundary's authority, behavior, or evidence, or where a
  high-impact security, permission, data-integrity, or migration failure would
  be materially more costly to discover at Final. State the behavior or
  authority at risk and the concrete dependency or delayed-discovery cost;
  a file's location or a declaration-only edit is not enough. Other changes
  receive focused verification and Final coverage. Reuse the reviewer for
  original-blocker and direct-regression closure; start fresh for a new boundary.
- Before Whole Goal completion, use a fresh `final_reviewer` for independent
  acceptance. Do not substitute a Slice or implementation review. Reviewers
  use only non-mutating reads; checks requiring writes return to the
  coordinator. A writable sandbox does not block review; disclose the lack of
  sandbox isolation in the result. If a required reviewer is unavailable, use
  the clean-room fallback in
  [references/acceptance-review.md](references/acceptance-review.md).
- Start delegated execution and review work with `fork_turns="none"` and a
  self-contained packet; reference exact paths rather than copying long
  documents.

Before falling back for a required role, establish an explicit tool or policy
restriction, or an actual start/resume failure that remains after one applicable
recovery attempt. Judge availability separately for each role; task listings
describe existing tasks, not which roles can be started. Recover invocation
conflicts by reusing an eligible agent or choosing a unique task name. Disclose
the restriction or error and recovery outcome, and record them in Delivery.
If `executor` remains unavailable, the coordinator may take over the authorized
Slice only after the previous writer has stopped, retaining the same
verification and review gates.

Give delegated roles a self-contained packet with the workspace, stable
repository states, approved conditions, exact scope and exclusions, preserved
behavior, required evidence, and raw-evidence locations. Include the constraints
from Keep Implementation Minimal in every executor packet. Do not suggest a
desired verdict. Delegated roles return evidence and findings; they do not edit
Delivery, change the plan, select later work, create commits, or declare a
formal boundary complete. Return one compact result with changed scope,
outcome, reproducible evidence and locations, relevant state, limitations and
whether production writing has stopped. Keep one production writer; independent
work may continue during review when it cannot invalidate the reviewed state.

## Coordinate The Delivery

The coordinating agent alone interprets the contract, selects the current
Slice, accepts evidence, updates Delivery, changes formal status, approves
exceptions, and declares Work Package, Milestone, or Goal completion.
Accept results by matching the supplied raw evidence to required conditions
and checking relevance, limits and unresolved blockers. The executor owns local
diagnosis, implementation and checks; the reviewer owns independent challenge.
Main investigates code or reproduces checks when evidence conflicts, material
gaps or consequential decisions require it, rather than repeating both roles.

Resume the recorded unfinished Slice when its contract, dependencies, and code
state remain valid. Otherwise choose one dependency-ready outcome that removes
a blocker or advances a ready package. A Slice owns one complete result,
including local discovery, implementation, necessary tests, guards and
documentation. The executor continues routine diagnosis and corrections within
that contract without a new packet for each failed check. Return material
scope, permission, dependency or risk-boundary decisions to Main. Do not
pre-plan later Slices.

Assign IDs as `<WP-ID>-S<NN>`, for example `WP-01-S01`. Allocate an ID only at
selection and never rename, renumber, or reuse a recorded ID. Record why it is
current, the acceptance labels it advances, local outcome, preserved behavior,
expected scope, and focused exit evidence.

The implementation owner completes the Slice and focused evidence before
reporting a stable result. The coordinator records acceptance, repository and
commit state, evidence links and next action in one Delivery update. Existing
logs and the result packet normally suffice; create separate reports or
snapshot manifests only for a concrete recovery, reproducibility or concurrency
need.

When evidence requires a material contract change, stop before implementing it,
record the conflict, use `$design-delivery-plan`, and resume only after user
approval. For an approved revision, read
[references/goal-change-record.md](references/goal-change-record.md) and update
the current contract and affected status atomically.

## Commit Stable Checkpoints

After accepting focused Slice evidence, create a local checkpoint when the
result is coherent, recoverable, and continuing would complicate attribution,
rollback, ownership, or interruption recovery. Adjacent Slices may share one
checkpoint when they form one outcome. Continue without committing when the
next Slice directly completes the same unfinished outcome. Never commit failed,
incomplete, or inconsistent state.

Execution of an approved plan authorizes these focused local commits unless the
user or repository explicitly opts out. Use the `commit` skill for staging,
scope, message style, and reporting. Include only the stable checkpoint;
preserve unrelated changes; do not push, create branches, amend, rebase, or
rewrite history. For multiple repositories, all intended repository commits
must succeed before a logical checkpoint is complete; otherwise record the
partial state and blocker and stop dependent work.

## Review And Accept

Record a risk boundary as review-ready only when its implementation,
dependencies, fixed snapshots, and focused evidence are stable. Defer broad
evidence until the boundary that owns it. Read the applicable sections of
[references/acceptance-review.md](references/acceptance-review.md) before
closing a Work Package, Milestone, or Goal.

Close a Work Package locally when its conditions and dependencies have current
evidence. Use a Milestone for one stable boundary containing one or more Work
Packages.

Open Final only after known production changes, required documentation, and the
evidence packet are stable. Final review is an acceptance gate, not an
iterative debugging pass. Give one fresh `final_reviewer` the complete packet
and request the complete currently discoverable finding set. If blockers share
one boundary, batch them into one corrective Slice; start a new Final pass only
after that Slice is stable and its invalidated evidence is refreshed.

Run focused checks on each corrected state as needed to finish its outcome.
Reserve expensive boundary-wide checks, final builds and Whole-Goal hygiene
for their relevant stable source. Preflight is not a substitute for these
required gates. Reuse valid evidence; rerun only checks affected by changed
code, inputs, tests, rules or contract. Documentation-only, formatting-only and
unrelated changes do not invalidate production evidence.

Delivery status and commit records locate evidence but do not prove completion.
Report the achieved outcome, verification, preserved behavior, blockers,
repository state, and exact Slice, Work Package, Milestone, and Goal status.
Read [references/handoff.md](references/handoff.md) before writing an explicit
execution handoff.
