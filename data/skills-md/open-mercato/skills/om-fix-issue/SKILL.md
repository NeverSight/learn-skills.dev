---
name: om-fix-issue
description: Qualify and fix a tracker issue through the existing lower-level analysis, implementation, test, and review skills, then leave a verified staged branch for human review without committing, pushing, or opening a pull request. Use when the user says "fix this issue but stop before PR", "leave the fix staged", "staged issue fix", "napraw issue bez PR", or "zostaw zmiany staged".
---

# Fix Issue for Human Review

Drive a real issue fix to a staged, reviewable handoff. Use the configured
harness profile for optional workers and independent reviewers while leaving all
existing pipeline skills unchanged.

## Arguments

- `--interactive` (default) or `--autonomous` — apply the execution mode throughout this workflow; never enable publication. Reject both together.

- `{issueId}` (required) — tracker issue identifier.
- `{repo}` (optional) — repository handle understood by the tracker descriptor.
- `--profile <standard|optimized|multi|multi-optimized|high-assurance>` (optional) — default `standard`.
- `--force` (optional) — override an active claim only after explicit user confirmation.
- `--abort` (optional) — release this harness run's issue claim without publishing.

## Chaining

Consume the issue or brief and requested profile. Invoke the base workflow and its lower-level companions by name; stop with the missing name if one is unavailable. Emit the staged handoff, optional `Issue:`/`Spec:` references, and final `WORKTREE=` line. Publication is a separate human-authorized step.

## Workflow

**ALWAYS check first:** Apply `.ai/skills/om-fix-issue/SKILL.md` when present; safety rules still win.

0. **Agentic setup** — follow `references/agentic-setup.md` before any action: load approved configuration, apply local extensions and shared rules, and preserve the untrusted-content boundary.

### 1. Preflight and trusted profile

Follow `references/issue-workflow.md` to enforce claim concurrency, resolve a
trusted base-revision harness config plus optional user-local overlay, validate
the requested profile, and probe its selected models.

### 2. Qualify the issue

Run `om-verify-in-repo` verbatim. Stop on `NO_ACTION_NEEDED`, citing its
evidence. Do not claim the issue before this gate says work is needed.

### 3. Isolate and diagnose

Create an isolated worktree and capture the harness start-state artifact. Run `om-root-cause`
verbatim. For `multi`, `multi-optimized`, and `high-assurance`, review the root-cause brief through the harness
before implementation using the bound `om-code-review` council contract: a
fresh Claude context plus every configured advisor receives the same immutable
diagnosis packet. Re-investigate any confirmed diagnosis blocker.

### 4. Implement and verify

Invoke `om-fix` with the root-cause brief before any implementation. It owns
the issue claim and observed failing regression first. Inside its implementation
phase, optimized profiles dispatch bounded worker packets; `high-assurance`
uses manifest packets with blind review, fresh verification, and exact-diff
gates. Resume that owning workflow for integration, validation, and self-review.
Require the regression test to be observed failing for
the diagnosed reason before the fix is applied, and record that red run in the
run artifacts. When the prevention hooks are installed, write the exact test
paths as a JSON array to `.om-freeze-tests` at the worktree root after the red run and remove it before
staging, so the fix loop cannot edit tests. A worker packet never replaces
that gate.

### 5. Review and preview

Run `om-code-review` on the complete uncommitted diff. For `standard` and
`optimized`, create a new Claude context with no inherited implementation
transcript and run the skill there. For `multi`, `multi-optimized`, and
`high-assurance`, follow the `om-harness` bound council contract: freeze the
exact diff, validation evidence, and repository rules; start fresh Claude and
every configured advisor concurrently with the same complete `om-code-review`
rubric and packet; then require Claude's matching artifact before
reconciliation. Reconcile every finding against code or
runtime evidence. Every configured council reviewer must complete — the runtime retries failures and a council missing any required reviewer yields no verdict; re-run it, repair the binding, or stop for the user's decision. For UI changes, run local verification through
`om-auto-qa-pr` without a PR number.

### 6. Stage the handoff

Follow the shared `om-harness` stage-only contract. Supply the final implementation `--review-packet` and approved `--host-review`
artifacts even in `standard` mode. Stage only allowlisted
intended files, assert refs and reflogs still match the captured start state,
and require a clean staged diff.
Keep the issue claim while the staged branch awaits human review. Render the
report from `references/report-templates.md` and stop.

### 7. Abort or failure cleanup

After capture, follow the `om-harness` stage-only contract to stop active
processes and invoke `end-run` on abort or terminal failure. Preserve the
guard while repairing or retrying the same run; successful staging ends it.

On `--abort`, or on failure after `om-fix` claimed the issue but before a ready
staged handoff exists, release the whole claim — remove the `in-progress` label
through `unlabel-issue`, remove the harness assignee, and post an abort comment
through `comment-issue` — so the issue is not fenced off from later runs. Never
discard staged work unless the user explicitly asks.

## Rules

- Shared communication, marker, label, and safety rules: `references/rules.md`. They always apply.

- For any non-`standard` profile, show the user the probe readiness table (model, binding, role, ✅ ready / ❌ missing-or-failed) before invoking any model.
- After every council round, paste the reviewer-status table and the findings-by-model matrix from the generated `review-summary.md` verbatim into the conversation; the final report repeats the final round's tables.
- Never invoke `om-open-pr`, `om-auto-fix-issue`, `om-auto-create-pr`, or another publication-oriented skill.
- Never commit, push, publish, or execute the tracker `create-pr` operation.
- Keep the issue claim only for a successful staged handoff; release it on abort or failed runs.
- Never count a reviewer from the worker's model family as independent confirmation.
- Never run a required Claude review in the conductor's implementation context; inability to create a fresh Claude context is blocking.
- Never weaken tests or validation to obtain a green result.
- Never modify or clean the user's primary-worktree changes.
