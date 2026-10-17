---
name: review
description: Review a local branch diff or an open GitHub pull request against the pack standards and the spec, with evidence-backed findings. Use when the user asks to review, check, or audit a branch, a diff, or a PR.
category: Code
---

# Review

Review a shipped diff (local branch or open GitHub PR) on the Standards and Spec axes with evidence-backed findings.

For either target, use [selective navigation](../rules/main-context.md#selective-navigation)
to locate touched paths, public signatures, responsibilities, and relevant
callers, then read the implementations needed to judge the change. A small
named-file or PR review needs no repository map; widen only for material
dependencies. Signatures locate behavior, not prove it.

## Read when

- Reviewing a touched user flow? Open [user-experience.md](../rules/user-experience.md), the ticket's interaction requirements, and `docs/design.md` when present. Judge interactions within Standards and Spec using [interaction review](doctrine.md#interaction-review).
- About to read a large diff, search the codebase, or wade through long output? Open [main-context.md](../rules/main-context.md). Skip it and noise crowds out your judgment of the findings.
- About to judge Standards on any `initial` or `full-rescan`, or on new PR follow-up surface, however small the diff? Open [code-quality.md](../rules/code-quality.md) and [code-structure.md](../rules/code-structure.md). Skip them and you pass code the rules reject.
- Reviewing a Feature diff? Open [strong-foundation.md](../rules/strong-foundation.md). Skip it and you pass a Feature that hardcodes what the plan said would vary.
- Every run: open [doctrine.md](doctrine.md) and the [review contract](contract.md). Skip them and the output fence and axes come out wrong.
- At a combined-result gate: use the [fresh review context](contract.md#fresh-combined-review-context). Keep the selected route's gate order and worker self-review intact.
- Reviewing tests or using their results to support an important claim: apply [test claim review](doctrine.md#test-claim-review), including the canonical testing rules.
- Unsure how to check Knip or the cyclomatic cap? Open [static-checks.md](static-checks.md). Skip it and you guess at a number.
- A parent supplied the handoff? Open the [execution context](../rules/planning.md#execution-context). Skip it and you re-ask settled decisions.
- Unsure whether a finding meets the evidence bar or how to word it? Open [examples.md](examples.md). Skip it and you ship a finding with no evidence.
- About to write a user-facing finding? Open [Plain language](../rules/writing-style.md#plain-language). Skip it and the author gets a rule slug instead of a fix.
- Reviewing a GitHub PR? Open [reference.md](reference.md) and [Asking the user](../rules/writing-style.md#asking-the-user). Skip them and you post comments nobody approved.
- About to recommend a behavior-lock test? Open [no-unrequested-tests.md](../rules/no-unrequested-tests.md) and [testing.md](../rules/testing.md). Skip them and you treat your recommendation as acceptance.

Use the review contract's scope-aware output: concise evidence for focused low-risk
work; the full review output fence for substantial/high-risk or requested full reviews.

## Pick the target

- **Local branch diff** (default): the user or a parent names a branch, ref, or
  the current work. Results stay in chat. `/task` selects local or independent
  review according to risk and the requested workflow under
  [verification scope](../rules/execution.md#verification-scope).
- **GitHub PR**: the user gives a PR number or link. Drafts comments and asks
  one publish question. User start only.

## Modes

Select the shared review mode deliberately:

- `initial` reviews the complete shipped diff with a Standards pass and a
  Spec pass.
- `remediation` receives named finding IDs, the fix diff, touched direct paths,
  and direct callers only. Verify those findings and regressions in that
  surface only.
- `full-rescan` requires an explicit request (or material scope expansion) to
  re-open full-review depth after a meaningful change.

Apply `review:axes`, `review:blocker-vs-follow-up`, `review:naming-alignment`,
`review:folder-placement`, `review:env-reuse`, and the review contract evidence
bar. On a GitHub PR, also apply the `review:*` PR extras.

## Local branch diff

1. Pin the requested fixed point and inspect its shipped diff.
2. If a parent already supplied outcome, done-when, non-goals, ticket or PR,
   fixed point, area, phase, rules that must stay true, current slices, and fix backlog,
   treat that chat context as the binding handoff. Otherwise derive the Spec axis from, in order:
   1. The user's stated outcome and Done when
   2. A named PR, ticket, and their available discussion
   3. Relevant repository code, rules, and committed documentation

   If no specification is available, say so and run Standards without
   inventing requirements. Cite a rule that must stay true only when it is actually
   violated; otherwise cite the relevant Done when item or state that no
   rule applies.
3. Run the Standards pass, then the Spec pass, over the whole diff. Keep them
   as separate passes so each axis gets its own evidence.
4. Report stable finding IDs and the Fix now / Follow-up / Optional nit
   disposition in chat. Keep all findings, decisions, and remediation memos in
   chat.

The parent (this chat, or `/task` when nested) owns fixed-point setup,
acceptance evidence, and review gates. A remediation review stays inside its
named findings.

### If a parent already owns the next step

Return stable findings and evidence to the active orchestrator under
[remediation](../rules/execution.md#remediation). It adjudicates, requests
bounded analysis only as needed, and dispatches fixes once. Review does not
invoke analysis, promote, or launch a second fix lifecycle.

### If this is a user one-off

Report the disposition in chat and stop. If the user requested fixes, hand
the findings and that authorization to an explicitly selected execution
orchestrator using [AGENTS routing](../../AGENTS.md#skills); it owns the
[remediation flow](../rules/execution.md#remediation).

## GitHub PR

1. Pin the PR fixed point (`headSha`) and load its body, commits, diff, all
   inline review comments, and all review threads, including resolved threads
   and every prior review page. Record `previousReviewedHead` from the last
   review this skill completed on this PR when available (from chat or the
   latest review commit association).
2. Run the Standards and Spec passes against the PR, its plan, and the bars,
   including the PR extras. This chat owns the publish question.
3. With no prior finding thread, run the shared contract's `initial` review.
4. On every follow-up, complete **Pass A** first, then **Pass B**
   ([reference.md](reference.md#follow-up-passes)). Use `full-rescan` only
   under the condition in Modes.
5. Show drafts, ask one publish question, apply the stale-head guard, then post
   only after approval ([reference.md](reference.md)).
