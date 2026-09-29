---
name: review-and-simplify-changes
description: "Use when implementation is ready for handoff or commit, or when reviewing commits, PRs, branches, WIP diffs, or subsequent fixes. Excludes unscoped architecture audits and standalone feedback triage."
---

# Review and simplify changes

Run the required review/fix loop through independent subagents after implementation and for standalone change reviews. Delegate correctness, simplification, and Standards/Intent inspection on every pass, including small changes and follow-up fixes. The main agent coordinates coverage, judges findings, applies authorized fixes, and owns integration and completion; its own inspection cannot satisfy review coverage.

## When to Use

- Reviewing the full intended change before implementation handoff or an intended commit, then reviewing subsequent fixes
- Reviewing or simplifying an explicitly scoped commit, PR, branch, or work-in-progress diff
- Checking changed code against repo Standards and change Intent from the prompt, explicit spec, plan, task notes, issue, or commit message
- Finding duplication, weak types, dead code, cycles, fallbacks, comments, or code quality issues introduced or exposed by the change

## When Not to Use

- Use `debugging` first when behavior is broken and cause is unknown
- Use `improve-codebase-architecture` for architecture plans without implementation
- Use `test-design` when the main question is test strategy

## Minimal Workflow

1. Coordinate independent review and simplification within the implementation loop or as the primary skill for a standalone review. Load domain guidance and the pressure references below only when the diff supplies evidence for them.
2. Pin the review to a commit, PR, branch, fixed point, or WIP diff.
   - For WIP, inspect `git status --short` before choosing the diff.
   - For a branch comparison, resolve the comparison ref and its upstream, use the upstream when it is ahead, and pin the merge base. Compare that base with the intended head or WIP state. For one commit or explicit snapshots, use those exact endpoints.
   - On follow-up passes, use the progressive review loop below.
   - If the requested comparison cannot be produced locally and no exact remote base and head are available, stop without a review rather than substituting unrelated branches, PRs, or GitHub comparisons.
   - If a fixed-point diff is empty but unstaged changes exist, report the mismatch and include the unstaged diff only when user intent clearly points at WIP; otherwise ask one narrow scope question.
3. Read repo-local `AGENTS.md`, docs, package scripts, conventions, and change Intent sources: prompt, explicit spec, plan, task notes, issue, or commit message. Use the diff as evidence of touched behavior, not as proof of intent.
4. State the scope, permitted side effects, and validation target. Map correctness, Standards/Intent, and material Eight-Topic Coverage Checklist checks to bounded review tracks, then apply Adaptive Reviewer Selection below. Use one independent subagent for a small or tightly coupled diff; dispatch separable tracks in parallel.
5. Require assigned subagents to inspect every changed path and its affected callers, tests, config, and contracts for correctness, security, performance, and maintainability. Require every actionable finding, continuing after the first defect. Have them judge **Standards** (repo rules and conventions) and **Intent** (requested behavior) separately and account for each material requirement as implemented, partial, missing, contradicted, incorrect, or unrequested scope. Keep these findings separate from cleanup taste.
6. Collect the assigned reviewers' results and account for each requirement and checklist topic as covered or not material. Delegate any uncovered material topic before completing review, including coverage lost when a reviewer fails or drops out; a quick main-agent check cannot close it.
7. Apply fixes supported by clear evidence within the user's existing authorization. A standalone review is read-only; a branch or PR scope does not cancel an authorized fix request. Keep cleanup behavior-preserving; verify intentional behavior changes against the requested outcome. Report pre-existing or out-of-scope findings without changing them. Routine dependencies may be added within the authorized outcome; ask about material scope, architecture, cost, or external effects. Do not stage, commit, or push unless authorized.
8. Follow the progressive review loop. A standalone read-only review ends with findings, coverage, and proof gaps; an implementation handoff must satisfy the loop's completion condition.

## Progressive review loop

1. First pass: batch completed changes into a stable snapshot, then have independent subagents review the entire intended diff, including relevant staged, unstaged, and untracked source. Record the base and reviewed head or reproducible WIP snapshot, reviewer assignments/results, covered paths/topics, findings, and validation. A WIP checkpoint must preserve the reviewed contents or diff, including untracked files; `HEAD` alone cannot identify it. Keep this record in task context unless a durable artifact is already authorized.
2. Judge every finding against repository evidence. A reproducible defect from one reviewer outweighs unsupported agreement from others; reviewer counts do not decide correctness. Track each as open, fixed awaiting review, verified fixed, rejected with evidence, or deferred by explicit user decision. Explain rejected findings. Fix accepted in-scope findings under existing authority, then run affected checks.
3. Batch related fixes before dispatch. Send all edits since the last reviewed snapshot to independent reviewers, including fixes, cleanup, tests, and concurrent or integration edits. Require them to trace affected callers and contracts, verify accepted fixes, and look for regressions introduced by them. Carry unresolved findings forward. Keep unchanged earlier scope closed unless new evidence, changed assumptions, or affected dependencies invalidate its coverage; explain any reopening. If a fixture or assumption is disproved, reopen the related tests and review conclusions that relied on it.
4. Repeat fix, affected verification, and delta review until no actionable finding remains unresolved and required checks pass. Only Q may accept a deferral. Report a blocker or missing authority honestly; a pass limit or time budget does not make an unresolved review complete.
5. An unchanged reviewed snapshot needs a comparison, not another review. Before handoff or an intended commit, confirm the final state is covered by returned subagent reviews from the initial and subsequent passes. For parallel slices, assign review of the combined diff and cross-slice wiring; reuse valid slice evidence while reviewers inspect every previously unreviewed interaction. Any later edit needs affected verification and another delegated delta review. A mechanical delta (formatting, a lint or type fix, a rename, a comment, or a test-assertion tweak, with no behaviour change) whose affected checks pass needs only one `fast_reviewer` pass confirming it is mechanical and complete; any other delta gets the full delta review. If the previous snapshot or coverage is missing, recover it or delegate review of the full identifiable intended diff; disclose unresolved scope instead of claiming incremental coverage.

## Adaptive Reviewer Selection

Choose reviewer count from the pinned diff's material, separable review work. The eight topics below are a coverage checklist, not an assignment quota.

- Read [references/delegated-review.md](references/delegated-review.md) before assigning review tracks. Every actual review pass requires independent subagents; diff size, low risk, and prior main-agent inspection do not waive delegation.
- Select roles from the material checks. Split independent subsystems, contracts, risk areas, and mechanical checks into bounded tracks; group tightly coupled topics under one reviewer. Use as many subagents as the separable work warrants, with no fixed topic-to-agent quota.
- Discover active subagent capacity before dispatch. Start independent reviewers together when slots are available; otherwise run bounded waves. Dispatch reviewers in the background and keep working while they run: verification gates, PR description, UI evidence, the next independent slice. Collect every result before commit or handoff. If no suitable independent agent is available, report blocked review coverage. Main-agent inspection cannot replace the required subagent pass.
- On the first full pass, the main agent also runs `codex review` alongside the subagent reviewers, using the target closest to the intended diff. Pass exactly one target: `--uncommitted` (staged, unstaged, and untracked, including unrelated WIP), `--base <branch>` (tracked changes since the merge base, committed or not, including tracked WIP; omits untracked files), or `--commit <sha>` (one commit). Targets reject a prompt argument, so Intent and Standards coverage stays with the subagents. Ignore findings outside the intended diff and judge the rest with the subagent findings. It supplements subagent review and cannot replace it; if it fails or cannot cover the diff, report that. Delegated reviewers do not run it.
- Give each reviewer the same pinned scope and Standards/Intent digest plus its material focus. Keep reviewers read-only: no edits, staging, commits, pushes, or state mutation.
- Delegate substantive review to `reviewer`, with the `review-agent` skill for defect review. Use `fast_reviewer` only for bounded mechanical evidence and `verifier` for command evidence. Include the selected role and its assigned concern in each brief, and tell reviewers not to invoke this skill or any repo post-code review gate recursively.
- Require file/symbol, checklist topic, issue, recommended fix, confidence, evidence, and validation needed. A reviewer may report no finding after completing its assigned checks; retain its coverage and proof gaps.
- The main agent owns checklist accounting, synthesis, judgment, edits, validation, and completion claims.

## Scope and read-only reviews

For branch and PR reviews, pin the comparison before delegation. Determine mutation authority from the user's request and prior authorization, including any explicit read-only restriction.

- Pin base, head, dirty state, relevant untracked source, and ignored generated/artifact dirs with `git status --short`, `git log <base>..HEAD --oneline`, and the relevant diff/stat commands.
- Pass each reviewer the same pinned scope and require it to trace changed symbols through callers, tests, config, and public contracts before reporting a finding.
- Compare base vs HEAD before claiming a new dead-code path, fallback removal, cycle, contract drift, or other regression.
- During a read-only review, use validators with a no-write mode; skip those that write caches, incremental state, snapshots, or generated artifacts. After allowed checks, rerun `git status --short` and disclose skipped validators, evidence used, and unexpected worktree changes.

## Eight-topic coverage checklist

Use these topics to select and account for material coverage. Each reviewer inspects the diff plus relevant callers, tests, Standards, and Intent context; one reviewer may cover multiple related topics, and a topic may be explicitly not material to the pinned scope.

1. **DRY/deduplication**: consolidate duplication only when it reduces complexity; reject shallow abstractions.
2. **Shared types/contracts**: find duplicate or drifting type definitions; consolidate only where ownership is genuinely shared. When runtime gates separate raw or external payload variants from domain objects, verify exported/static contracts preserve that split instead of advertising guarded variants as happy-path domain types.
3. **Unused code**: use existing tools such as `knip`, compiler/linter output, exports, imports, and repo search; remove only when references are disproven.
4. **Circular dependencies**: use `madge` or import graph checks; check file-level SCCs and coarser directory/module boundary graphs, especially new base-vs-HEAD cross-boundary edges. A zero file-SCC count does not clear a boundary-cycle finding. Untangle with the smallest boundary move.
5. **Weak types**: replace `any`, `unknown`, casts, and language equivalents only after researching real payloads, callers, and package types. For raw or external payloads, `unknown` or an untrusted boundary type may be correct until guards or schema parsing narrow it.
6. **Error handling**: remove try/catch/fallbacks that hide errors; keep boundary handling for unknown input, external systems, cleanup, retries, or user-safe errors.
7. **Legacy/fallback paths**: remove only after proving no live caller, config, migration, or rollout dependency remains.
8. **AI slop/comments/stubs**: remove stubs, stale migration notes, and filler comments; keep concise intent comments, legal text, public contracts, and functional directives. Check suppressions and negative type tests before changing comments: their removal can change compiler, linter, or test behavior. Uncertainty about purpose is not evidence for deletion.

Keep Standards and Intent findings on separate axes in synthesis. If Intent is unavailable, say that instead of inventing requirements from the diff.

## Reference routing

Load only references needed by evidence in the pinned scope. Reuse guidance already loaded:

- `engineering/references/boundary-design.md` when judging interface depth, information hiding, caller knowledge, misuse risk, or deletion of an abstraction
- `engineering/references/feature-shape.md` when a change's tracer bullet or vertical slices leave production behavior incomplete
- `engineering/references/legacy-change.md` when a proposed refactor needs characterization seams or dependency-breaking
- `improve-codebase-architecture/AGENT_FRIENDLY_REVIEW.md` when navigation, domain ownership, or verification friction needs a broader trace
- `engineering/references/compatibility-and-delivery.md`, `security.md`, or `state-and-effects.md` when those risks appear
- `engineering/references/proof.md` when proof depends on consequential fixtures, setup, external contracts, clocks, or concurrency, or the proof boundary is unclear; `test-design` guidance when judging test behavior and public interfaces
- [URL-ATTRIBUTION-REVIEW.md](URL-ATTRIBUTION-REVIEW.md) only for URL, link, campaign attribution, analytics, or CTA-helper changes

If missing guidance or a skill defect materially affected the change, name it and propose the smallest correction.

## Architecture alignment

Architecture and cleanup findings need evidence that the proposed move improves a relevant principle from the references above. Do not recommend DRY, type consolidation, or patterns on taste alone.

Correctness, contract, Standards, and Intent findings stand on their own evidence. Report a bug or missing requirement even when no architectural improvement is involved.

## Upstream prevention

Before finalizing, classify important findings as pre-existing debt, regression from current changes, preventable by `engineering`, preventable by `debugging`, preventable by `test-design`, or repo-doc candidate.
If a producer skill should have prevented a repeated or high-cost issue, propose the smallest skill/reference update instead of expanding this review skill.
Do not auto-edit repo docs or skills unless the user asked for that mutation.

## Validation

Run the smallest trustworthy validation for touched scope: focused tests, typecheck/compile, lint/format, and dead-code or cycle tool reruns when those tracks changed code.

Reuse recorded evidence across turns when the tested code and relevant state are unchanged. Rerun affected checks after fixes or changed requirements.

If validation is too broad, unavailable, or skipped by instruction, say exactly why.

## Failure modes

- Rewrite-by-cleanup; treating the checklist as an agent quota; diff impressions mistaken for requirement traceability; deleting dynamic use after one search; merging different domain types; removing boundary defense; fake precise types; overlapping edits; recs without safe fixes.
