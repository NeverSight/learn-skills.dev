---
name: monomind-workflow
description: "Install or adopt Monomind's persistent repository factory contract, or run its end-to-end code-task workflow: isolate, build, prove, and ship. Use when making skills mandatory for a repository, starting a new feature or fix, coordinating concurrent agents, or taking an issue or specification through implementation and a pull-request handoff. Use narrower skills for policy-profile onboarding, read-only work, or an already-isolated single phase."
---

# Monomind Workflow

Coordinate Isolate → Build → Prove → Ship through the user's authorized delivery
target. Each phase has an observable result; it does not grant additional authority.

## Select the mode

- **Adopt:** encode the workflow in a repository. Read
  [references/project-profile.md](references/project-profile.md) for installation,
  scaffold, migration, and onboarding. Adoption detail is not needed in Run mode.
- **Run:** carry a new code task through the four phases below.
- Read-only reviews, evidence-only requests, and already-isolated single-phase
  work use the relevant phase skill directly.

## Establish the task once

Read the task/spec, local instructions, Git/worktree state, and relevant profile.
Identify scope, acceptance claims, checks, authoritative base, owner, resources,
and delivery target. Reuse verified facts and existing authorization; ask only
for a missing decision that materially blocks the requested action.

If a profile or managed policy exists, run the installed
`scripts/adopt.py check --gate build --repo <repository>` before implementation.
Use `--gate integration` before integrating or merging, and `--gate release`
before executing a deployment or migration. Each gate includes lower gates;
one successful check suffices for that boundary. A failed gate routes only
its missing fields to onboarding. Read-only diagnosis may continue.

Keep a compact task record of facts, checks, revision, and environment. Reuse it
across phases rather than rediscovering commands or repeating a successful gate.
Invalidate only results affected by changed policy, tool versions, code, base,
environment, or shared-resource ownership.

## Isolate

Preserve unknown changes and establish one task owner and exclusive linked
worktree. Reuse a harness-created worktree when it belongs to this task; do not
create another for each phase. Resolve the base from the approved profile;
`origin/main` is the bootstrap default only when no base has been specified.
A supplied alternative must be recorded during adoption.

Fetch the relevant remote and create a named task branch/worktree from that
base before implementation. Never edit on `main`, the configured base branch,
or another task's worktree. The project-installed
`scripts/adopt.py preflight --repo <repository>` verifies isolation **after**
the worktree exists. It reads the recorded base; initial adoption can use
`--base <remote/branch>` for an explicitly approved alternative.

Check overlaps when concurrent work is in scope. Allocate relevant shared ports,
databases, queues, accounts, and other resources; worktrees do not isolate them.
Verify that a running service serves this task's code.

**Result:** known owner, workspace, base, scope, and resource assignments.

## Build

Implement thin behavior slices through a public test seam. For changed behavior,
obtain a failing signal when feasible, implement the smallest complete change,
and run focused checks. Use the recorded repository commands. Stop feature
expansion on unexplained failures and investigate the cause.

Actions/boundaries retain domain policy, authorization, and state transitions.
Extract reusable or volatile mechanics behind explicit inputs and structured
outputs; keep one-off mechanics local. Keep changes inside task scope.

Load a narrower skill only for missing guidance: intake/spec/plan for unresolved
intent or sequencing, design for a boundary decision, build for a substantial
slice loop, debug for a failure. Do not load them just to repeat these steps.

**Result:** approved behavior implemented and focused checks pass.

## Prove

Map material acceptance claims to checks or artifacts. Capture a failing before
state before a fix when feasible; material visible changes need matched before/
after captures. Use evidence for nontrivial runtime proof and before-after for
visual comparison packaging when installed. Equivalent local evidence is valid
when those skills are absent.

Run affected final gates once after the last relevant edit. Record revision,
environment, reproducer, and passed/failed/untested claims. Reuse valid focused
test evidence. Inspect artifacts; keep them local/private unless publication
is authorized.

**Result:** trustworthy evidence or explicit gaps for each acceptance claim.

## Ship

Inspect the diff for scope, secrets, generated noise, and weakened checks. Apply
the gate for the actual destination: integration/merge and deployment are
different boundaries. Reconcile with the approved base/integration strategy
when needed, rerunning only affected proof.

Commit, push, open/update a change request, or merge only within supplied
authority. Otherwise return a local PR-ready handoff. Include outcome, checks,
evidence, remaining risks, reversibility, affected users or components, and
next state; link existing artifacts instead of duplicating them. Use review,
release, or handoff skills only when that phase needs their additional guidance.

Address blocking CI/review findings; escalate contradictions or feedback that
repeats without new evidence. Preserve isolation until completion or deliberate
handoff. Never modify, reset, stash, rebase, or delete another owner's work.

**Result:** the authorized delivery state reached, evidence attached or linked,
and remaining work explicit. Do not repeat phase summaries in separate artifacts
unless a real consumer requires them.
