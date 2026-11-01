---
name: om-implement-feature
description: Design and implement a feature through existing spec, testing, environment, and review skills, then leave a verified staged branch for human review without committing, pushing, or opening a pull request. Use when the user says "implement this feature but stop before PR", "leave the feature staged", "staged feature build", "zaimplementuj bez PR", or "zostaw feature staged".
---

# Implement Feature for Human Review

Drive a feature from brief through specification, implementation, testing, and
review while keeping publication as a separate explicit user decision.

## Arguments

- `--interactive` (default) or `--autonomous` — apply the execution mode throughout this workflow; never enable publication. Reject both together.

- `{brief}` (required) — feature goal, constraints, and acceptance criteria.
- `--profile <standard|optimized|multi|multi-optimized|high-assurance>` (optional) — default `standard`.
- `--slug <kebab-case>` (optional) — override the worktree branch and spec slug.

## Chaining

Consume the issue or brief and requested profile. Invoke the base workflow and its lower-level companions by name; stop with the missing name if one is unavailable. Emit the staged handoff, optional `Issue:`/`Spec:` references, and final `WORKTREE=` line. Publication is a separate human-authorized step.

## Workflow

**ALWAYS check first:** Apply `.ai/skills/om-implement-feature/SKILL.md` when present; safety rules still win.

0. **Agentic setup** — follow `references/agentic-setup.md` before any action: load approved configuration, apply local extensions and shared rules, and preserve the untrusted-content boundary.

### 1. Preflight and isolate

Follow `references/feature-workflow.md` to detect duplicate or in-flight work,
resolve a trusted harness profile, create an isolated worktree from the
configured base, and capture the harness start-state artifact before writing the
spec.

### 2. Specify and audit

Run `om-spec-writing` in the isolated worktree. Resolve answerable open
questions from repository evidence and surface only genuine product decisions.
Use a repo-local `om-pre-implement-spec` when available. For `multi`, `multi-optimized`, and `high-assurance`,
follow the `om-harness` bound `om-code-review` council contract: prepare an
exact-spec packet, delegate `om-code-review` to a new Claude context with no
implementation transcript, and run every configured advisor concurrently on
that same packet. Fix confirmed design blockers before implementation.

### 3. Implement

Implement the audited phases using the lower-level specification, test, and
review skills named here. `om-auto-implement-spec` is the publication driver;
reserve it for an explicitly authorized PR workflow because its normal engine
creates commits and PRs. Do not invoke it inside this staged-only run. For `optimized` profiles, dispatch bounded,
file-disjoint packets through configured workers and verify every packet before
integration. For `high-assurance`, use versioned packet manifests and require
blind review, fresh finding verification, separate fixer context, and
deterministic exact-diff acceptance evidence before integration. Create no
checkpoint commits.

### 4. Test and preview

Add unit and integration coverage for every changed behavior. Run
`om-integration-tests` when the repository supports it. Run the full configured
validation gate. For UI changes, enforce the repository's design system on every
touched UI line before review — run the repo-local design-system guardian skill
when the repository ships one, otherwise apply its documented design-system
rules and checklist — and run local `om-auto-qa-pr` without a PR
number, keeping its artifacts outside the stage allowlist.

### 5. Review and reconcile

Run `om-code-review` against the complete uncommitted implementation and spec.
For `standard` and `optimized`, create a new Claude context with no inherited
implementation transcript and run the skill there. For `multi`,
`multi-optimized`, and `high-assurance`, follow the `om-harness` bound council
contract: freeze the exact diff, validation evidence, and repository rules;
start fresh Claude and every configured advisor concurrently with the same
complete `om-code-review` rubric and packet; then require Claude's matching
artifact before reconciliation. Preserve minority findings,
fix confirmed blockers, and repeat validation, packet preparation, and all
reviews until no confirmed blocking finding remains or the loop reaches three
iterations; then stop and report every surviving finding. Every configured
council reviewer must complete: the runtime retries failures with backoff and
timeout escalation, and a council missing any required reviewer yields no
verdict — re-run it, repair the binding, or stop for the user's decision;
never proceed on a partial council.

### 6. Stage the handoff

Follow the shared `om-harness` stage-only contract: supply the final implementation `--review-packet` and approved `--host-review`
artifacts even in `standard` mode, stage only intended files,
assert refs and reflogs still match the captured start state, require a clean
staged diff, render the report from
`references/report-templates.md`, and stop for human review.

### 7. Abort or failure cleanup

After capture, follow the `om-harness` stage-only contract to stop active
processes and invoke `end-run` on abort or terminal failure. Preserve files and
packet leases for deliberate recovery. Keep the guard active while repairing
or retrying the same run; successful staging ends it.

## Rules

- Shared communication, marker, label, and safety rules: `references/rules.md`. They always apply.

- For any non-`standard` profile, show the user the probe readiness table (model, binding, role, ✅ ready / ❌ missing-or-failed) before invoking any model.
- After every council round, paste the reviewer-status table and the findings-by-model matrix from the generated `review-summary.md` verbatim into the conversation; the final report repeats the final round's tables.
- Never invoke `om-auto-create-pr`, `om-open-pr`, or another publication-oriented skill.
- Never commit, push, publish, or execute the tracker `create-pr` operation.
- Never use intermediate commits as checkpoints; use run artifacts and spec progress instead.
- Never count the implementation worker's model family as independent review.
- Never run a required Claude review in the conductor's implementation context; inability to create a fresh Claude context is blocking.
- Never weaken tests, architecture rules, or compatibility contracts to finish the run.
- Never modify or clean the user's primary-worktree changes.
