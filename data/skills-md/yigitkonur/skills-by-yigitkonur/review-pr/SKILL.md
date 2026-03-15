---
name: review-pr
description: Use skill if you are reviewing a GitHub pull request or branch diff for merge readiness and need high-signal findings grounded in PR goals, changed-file clusters, and existing review threads.
---

# Review PR

High-signal pull request review for GitHub. Read the PR as a change proposal, not a pile of files. Prioritize goal achievement, correctness, security, data safety, contract compatibility, and merge risk. Avoid style policing, speculative architecture feedback, and shallow summaries with no evidence.

## Trigger

Use this skill when the task is to:
- review a PR, pull request, or branch diff
- decide whether a PR is safe to merge
- check whether code changes match the stated goal
- review a PR that already has human or bot comments
- triage a large diff by grouping files into review clusters

Prefer other skills when:
- generating review configuration or rules for a platform → `init-*`
- writing or refactoring code rather than reviewing it → `build-*` or `develop-*`
- debugging runtime behavior with tools or logs → `debug-*`
- running test suites as the main job → `test-*`
- commenting only on formatting, lint, or style nits → skip or rely on automation

## Review stance

1. **Goal first** — a PR that misses its stated outcome fails even if the code looks clean.
2. **Context before diff** — read why the change exists before judging how it is implemented.
3. **Conversation-aware** — existing threads and bot reviews are part of the evidence set.
4. **Cluster before depth** — review related files together and prioritize highest-risk clusters first.
5. **Evidence before opinion** — every reported finding needs `file:line`, observed behavior, impact, and a suggested fix or question.
6. **Questions before speculation** — if you cannot point to specific evidence for a concern, ask instead of asserting.
7. **Signal over volume** — fewer high-confidence findings beat long nit lists.

## Default workflow

Follow these phases in order. Load `references/review-workflow.md` for detailed procedures and command variants.

> **Tool access:** Examples below use `gh` CLI syntax. If you have GitHub MCP server tools available (e.g. `pull_request_read`, `get_file_contents`, `issue_read`), prefer those — they return the same data without shell access. See `references/gh-cli-reference.md` for the MCP equivalents table.

### Phase 1 — Triage the review request

First identify:
- PR number, URL, branch, and repo
- whether the user wants a full review or a targeted pass
- whether the PR is draft or ready
- whether the task is merge-readiness, security-only, performance-only, or general review

If no review type is specified, default to **general merge-readiness review**.

**Decision rules**
- Draft PR with no explicit request for deep review → stop after a readiness note or limit feedback to high-level concerns.
- Targeted review request such as security on PR 42 → still do Phases 2 through 4, then go deep only on the requested dimension.
- No clear repo or PR target → do not begin code review until the target is known.
- PR is a refactor, deprecation, or behavioral change → in Phase 6, weight call-site impact, backwards compatibility, and migration path over net-new bug patterns. In Phase 7, check that all callers of deprecated APIs have been updated or warned.

### Phase 2 — Gather context before reading code

Read:
- PR title, body, and metadata
- linked issues or acceptance criteria
- CI or check status
- commit history and fixup signals

Create one sentence internally:
`This PR should accomplish X by changing Y in Z.`

Do not start code review before you can explain the goal in plain language.

**Recovery**
- PR body or linked issue is thin → record a context gap and keep that uncertainty visible in later findings.
- CI is failing → note which checks fail, then focus on merge-risk issues the failing checks do not already cover.
- Lint or format checks are already red → do not repeat machine-catchable style feedback.
- Security scan failed → escalate its findings and read the scan output before concluding the review.
- No linked issue → rely on the PR description and commit history, but lower confidence on scope judgments.

Load if needed:
- `references/review-workflow.md` for full phase procedure and goal validation
- `references/gh-cli-reference.md` for exact `gh` syntax
- `references/automation.md` for CI, static analysis, and bot review signals

### Phase 3 — Scope the diff and cluster files

Group changed files by concern before reviewing:
- Data or migration
- Security or auth
- API or routes
- Core logic
- Types, interfaces, or schemas
- Frontend
- Infrastructure, config, or docs

Pair tests with the source files they validate. Pair type definition files (*.d.ts, types.ts, schemas) with the cluster that consumes those types. Review clusters in risk order, not file-list order.

**Decision rules**
- Under 100 changed lines → deep review the full diff.
- 100 to 500 changed lines → deep review top clusters, lighter scan on low-risk clusters.
- 500 to 1000 changed lines → deep review only the highest-risk clusters and explicitly note skimmed areas.
- More than 1000 changed lines or incoherent mixed concerns → flag PR size or scope as a review concern and recommend splitting.

**Recovery**
- Monorepo or unusual layout → cluster first by package or service, then by concern.
- Generated code dominates the diff → review the source definitions and note generated files lightly.
- Hunk context is insufficient → load full-file and before-vs-after analysis instead of guessing from the patch.

Load if needed:
- `references/file-clustering.md` for clustering rules, test pairing, and size strategy
- `references/large-pr-strategy.md` for very large PRs
- `references/diff-analysis.md` for deep diff-reading tactics

### Phase 4 — Read existing review state before adding new findings

Fetch:
- formal reviews
- inline comment threads
- general PR conversation comments
- bot or AI review comments

Build an already-reviewed map and classify threads as:
- **resolved** → skip unless the bug is still present or reintroduced
- **active** → acknowledge or extend; do not duplicate
- **outdated** → recheck the current code before re-raising

**Decision rules**
- Same issue on the same lines as an active thread → reference it; do not create a new independent finding.
- Same issue on a resolved thread → only re-raise if the current code still has the problem.
- Author pushback or rationale in comments → treat it as context, not noise.
- Bot comments count as prior review state when they already identify the same issue.

**Recovery**
- Thread state is unclear → state the uncertainty and avoid confident duplication.
- Only bots reviewed so far → continue with a full review, but still deduplicate against bot findings.
- All review feedback is conversation-level (general PR comments, not inline threads) → classify it as strategic discussion; do not try to map it to code lines. Summarize team positions in your output.
- Team disagreement on approach → note both sides neutrally; do not take a side unless you have specific technical evidence that favors one. If you do have evidence, state it and let the team decide.
- Mixed human-and-bot reviews → humans take priority; deduplicate bot findings against human conclusions.

Load if needed:
- `references/comment-correlation.md` for the full thread-state decision flow
- `references/communication.md` for agreement, extension, and non-duplicative phrasing
- `references/automation.md` for interpreting bot and static-analysis comments

### Phase 5 — Validate goals before judging quality

Before hunting bugs, confirm that the PR actually does what it claims.

Check in order:
1. happy path is implemented end to end
2. failure and error paths are handled
3. described behavior exists in the diff
4. risky extra scope is explained
5. supporting changes exist where needed, such as tests, docs, config, consumers, type definitions, or migrations

**Immediate escalation**
- Described-but-not-implemented behavior → likely 🔴 blocker
- Implemented-but-not-described risky scope → at least 🟡 important
- Cannot explain what success looks like → raise the context or goal gap before deeper review

Load if needed:
- `references/review-workflow.md` for goal-validation steps
- `references/cross-cutting.md` when the goal spans multiple layers

### Phase 6 — Review by cluster, then trace blast radius

Within each cluster, check the highest-signal dimensions first:
1. security and auth
2. correctness and edge cases
3. data integrity and backward compatibility
4. API contract and validation
5. performance with realistic scale impact
6. tests for changed behavior
7. maintainability only when it materially affects safety or comprehension

Trace blast radius when the diff changes:
- shared types or schemas
- public interfaces, routes, or events
- auth boundaries
- env vars or deployment assumptions
- dependency or configuration contracts

**Actionability gate — report a finding only if all are true**
- It is in scope for this PR.
- It has concrete user, system, or merge impact.
- It is not just style, lint, or formatter output.
- It is not already adequately covered by an existing thread.
- It matches repo conventions rather than importing your own taste.
- You can point to evidence in the code — a specific line, a missing guard, or a concrete failing input. If you cannot, phrase it as a 💡 question instead.

Load if needed:
- `references/review-dimensions.md` for the full checklist
- `references/security-review.md` for security depth
- `references/performance-review.md` for performance depth
- `references/bug-patterns.md` for correctness traps
- `references/language-specific.md` for language-specific pitfalls
- `references/diff-analysis.md` for patch-vs-file interpretation

### Phase 7 — Run a cross-cutting sweep

Look for coordination failures between clusters:
- schema changed but API or consumer did not
- API changed but tests or docs did not
- new endpoint or page without auth
- new env var or dependency without deploy or config updates
- changed source with no meaningful coverage for the risky path
- deprecated accessor or method with call sites still using the old API — check for cascading deprecation warnings at runtime
- new abstraction layer without migration path for existing consumers

If individual files look fine in isolation but the layers do not line up, treat that as a real review finding.

Load if needed:
- `references/cross-cutting.md`
- `references/file-clustering.md` for cross-cluster checks

### Phase 8 — Calibrate, synthesize, and output

Before finalizing:
- re-check severity
- remove duplicates
- batch repeated issues into one finding where helpful
- cut anything speculative, stylistic, or low-value
- include at least one specific positive observation
- summarize existing review state
- state which clusters were deep-reviewed versus skimmed
- note whether tests cover the risky paths you reviewed

Choose the verdict from the findings, not from vibes:
- **✅ Approve** — no blockers, goal achieved, and only minor issues or questions remain
- **💬 Comment** — non-blocking issues or open questions remain
- **🔄 Request Changes** — blocker, goal failure, or risky unaddressed gap

If you only have suggestions, do not escalate to request changes.
- When a team disagreement on approach exists, note both sides and state your technical evidence if you have it, but do not override team consensus.
- When PR scope judgment depends on context you do not have (product goals, team conventions), ask rather than assert.

**Present the review to the user. Do not submit it to GitHub unless explicitly asked.** Use the compact template from `references/output-templates.md` for PRs under 500 changed lines with 5 or fewer findings; use the full template for larger PRs or reviews with 6+ findings.

Load if needed:
- `references/severity-guide.md`
- `references/output-templates.md`
- `references/communication.md`

## Severity calibration

Use this default ladder:
- **🔴 Blocker** — security flaw, data loss, crash or common-path failure, or goal-validation miss that makes the PR unsafe to merge
- **🟡 Important** — likely bug, contract gap, missing validation or error handling, meaningful performance issue, or missing coverage for risky behavior
- **🟢 Suggestion** — worthwhile improvement that does not change merge safety
- **💡 Question** — intent or behavior is unclear, or you cannot point to specific evidence for the concern
- **🎯 Praise** — specific thing done well; always include at least one

Calibration checks:
- More than 3 blockers → reassess; blockers are rare.
- More than 10 total findings → likely too noisy; re-apply the actionability gate.
- Same concern across several files → batch into one finding.
- Existing unresolved blocking thread on the same issue → surface it in the summary rather than duplicating it.

## Evidence contract for every finding

Every finding must contain:
1. severity
2. concise title
3. exact `file:line` or line range
4. what the code does now
5. why that matters in this PR
6. suggested fix or clarifying question

Prefer:
- `This could cause...`
- `I noticed...`
- `Is it intentional that...`
- a concrete failing input, missing guard, or contract mismatch
- one batched finding for repeated identical issues

Avoid:
- `You should...`
- `Why did you not...`
- vague reactions such as `this looks wrong`
- style-only feedback, architecture redesigns, and hypothetical disaster chains
- approval or merge-readiness claims without saying what you actually reviewed

## Do this, not that

| Do this | Not that |
|---|---|
| Form the goal hypothesis before reading diffs | Start line-by-line review with no model of intent |
| Cluster related files and pair tests with source | Review changed files in alphabetical order |
| Read existing threads first and reference them | Post duplicate findings already covered by reviewers or bots |
| Convert low-confidence concerns into 💡 questions | State speculative bugs as facts |
| Batch repeated issues across files | Leave four near-identical comments |
| Note which clusters were deep-reviewed versus skimmed | Pretend a large PR received uniform coverage |
| Flag correctness, security, data, contract, and test gaps | Spend review budget on lint, formatting, or taste |
| Use repo conventions as the baseline | Import outside style preferences |
| Recommend a separate discussion for architecture drift | Demand a redesign inside the PR |
| Include specific praise with evidence | End with generic approval language |
| Acknowledge team disagreements neutrally | Take sides without technical evidence |
| Present the review to the user first | Auto-submit reviews to GitHub without being asked |

## Guardrails and recovery paths

| Situation | Response |
|---|---|
| Draft PR without explicit review request | Stop after a readiness note or keep feedback high-level |
| CI failing | Record failing checks, avoid piling on style noise, and focus on issues CI does not already prove |
| PR intent unclear | Flag the missing context, state your best hypothesis, and lower confidence where needed |
| Large or mixed-scope PR | Review highest-risk clusters first, state coverage limits, and recommend splitting if necessary |
| Existing active thread covers the issue | Reference or extend it instead of creating a duplicate finding |
| Resolved thread may still be wrong | Re-read current code and re-raise only with explicit evidence |
| Finding count gets noisy | Re-run the actionability gate and cut low-signal comments |
| Need exact CLI commands or deeper procedure | Load the matching reference instead of expanding SKILL.md |
| Deprecation or refactor PR | Shift focus from new bugs to call-site impact, migration paths, and backwards compatibility |
| Team disagreement in PR comments | Note both positions neutrally; provide technical evidence if available but do not override consensus |

## Reference routing

Read only the smallest set that matches the current phase.

| Need | Load |
|---|---|
| End-to-end review flow and command sequences | `references/review-workflow.md` |
| Exact GitHub CLI syntax | `references/gh-cli-reference.md` |
| CI, static analysis, and AI review tooling | `references/automation.md` |
| File grouping, test pairing, and review depth | `references/file-clustering.md` |
| Large PR chunking | `references/large-pr-strategy.md` |
| Deep diff interpretation | `references/diff-analysis.md` |
| Existing review threads and dedupe rules | `references/comment-correlation.md` |
| Security-focused review | `references/security-review.md` |
| Performance-focused review | `references/performance-review.md` |
| Common correctness bugs | `references/bug-patterns.md` |
| Full review dimensions checklist | `references/review-dimensions.md` |
| Cross-cluster coordination gaps | `references/cross-cutting.md` |
| Language-specific pitfalls | `references/language-specific.md` |
| Severity examples and boundary cases | `references/severity-guide.md` |
| Output shape and verdict templates | `references/output-templates.md` |
| Comment tone, batching, and praise patterns | `references/communication.md` |
| Anti-noise resets when the review drifts | `references/anti-patterns.md` |

## Minimal reading sets

### Standard PR review
- `references/review-workflow.md`
- `references/file-clustering.md`
- `references/comment-correlation.md`
- `references/output-templates.md`

### Large or messy PR
- `references/review-workflow.md`
- `references/file-clustering.md`
- `references/large-pr-strategy.md`
- `references/cross-cutting.md`

### Need help calibrating findings
- `references/severity-guide.md`
- `references/communication.md`
- `references/anti-patterns.md`

### Deep domain passes
- Security → `references/security-review.md`
- Performance → `references/performance-review.md`
- Correctness → `references/bug-patterns.md`
- Language nuance → `references/language-specific.md`
- CI and bot signals → `references/automation.md`

## Steering experiences

Lessons from real-world execution that prevent common review mistakes:

1. **Do not load all references upfront.** Load only the set listed under "Load if needed" for the current phase. Loading everything wastes context and causes missed instructions in later phases.
2. **Conversation-level comments are not inline threads.** When a PR has team debate in general comments (not attached to code lines), classify it as strategic discussion. Do not try to map conversation comments to specific lines — they represent positions, not code issues.
3. **Deprecation and refactor PRs need different scrutiny.** The primary risk is not a net-new bug — it is call-site impact, backwards compatibility, and migration completeness. Shift review weight from "is this new code correct?" to "are all consumers updated?"
4. **The phase numbering in SKILL.md and review-workflow.md is intentionally offset by one.** SKILL.md Phase 1 (Triage) has no counterpart in review-workflow.md. SKILL.md Phase 2 maps to review-workflow.md Phase 1, and so on. Consult the navigation table in `references/review-workflow.md` if confused.
5. **Evidence-based, not confidence-based.** Never decide actionability by estimating a confidence percentage. Instead ask: "Can I point to a specific line, a missing guard, or a concrete failing input?" If yes, report it. If no, phrase it as a question.
6. **Present the review — do not auto-submit.** Unless the user explicitly says "submit" or "post", present your review in the chat. This prevents accidental review submissions on the wrong PR or with unintended severity.
7. **MCP tools vs gh CLI — either works.** If GitHub MCP server tools are available, prefer them over shell commands. The data is identical. See `references/gh-cli-reference.md` for the equivalence table.
8. **Type definition files are not their own review silo.** Pair *.d.ts, types.ts, and schema files with the cluster that imports them. Review type changes alongside the code that consumes those types.

## Final reminder

A good PR review is not a diff paraphrase and not a style checklist. It is a merge-risk assessment grounded in the PR goal, the changed-file topology, the existing review conversation, and evidence from the code. Keep the review sharp, concrete, and useful.
