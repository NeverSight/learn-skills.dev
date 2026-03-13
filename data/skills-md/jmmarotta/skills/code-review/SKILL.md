---
name: code-review
description: Review diffs, commits, or pull requests for correctness, regressions, integration risk, and design quality. Load `software-design` for design judgment, `software-implementation` for code shape or verification depth, and `software-planning` only when planning artifacts matter.
---

# Code Review

Use this skill to review diffs, commits, and pull requests.
Load `software-design` when review quality depends on abstraction quality, ownership boundaries, interface fit, or long-term complexity judgment.
Load `software-implementation` when review quality depends on code shape, local validation loops, comment judgment, or refactor heuristics.
Consult `software-planning` only when original requirements, rollout assumptions, interface intent, or planned verification materially affect the review.
This skill focuses on review mechanics: scope, evidence, prioritization, and actionable findings.

## Review Focus

- Unless specified otherwise, review only the change set unless surrounding code directly affects
  correctness, design, or operational risk.
- Check correctness and security: logic errors, edge conditions, race
  conditions, broken error handling, and data exposure.
- Check integration and design fit: abstraction mismatches, leaked invariants,
  ownership boundary violations, and unnecessary coupling.
- Check performance and operations: obvious complexity risks for expected load,
  N+1 and repeated-scan patterns, blocking hot-path work, and missing
  observability or rollback safety.

## Review Loop

1. **Understand intent and context**: identify what changed and where it fits.
2. **Inspect boundaries first**: review interfaces and call sites before internals.
3. **Verify with evidence**: confirm issues from code paths, callers, types,
   tests, or observable behavior.
4. **Check failure handling**: validate invariants, error paths, blast radius,
   and rollback path for risky changes.
5. **Check verification depth**: confirm test and manual validation coverage is
   appropriate for change risk.
6. **Prioritize findings**: classify by impact and confidence.

## Obtain the Diff

- **No args (default)**: `git diff` and `git diff --cached`.
- **Commit hash**: `git show <commit-hash>`.
- **Branch name**: `git diff <branch-name>...HEAD`.
- **PR URL/number**: `gh pr view <pr-identifier>` then `gh pr diff <pr-identifier>`.
- **Unknown base branch**: `git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'`, then `git diff <default-branch>...HEAD`.

After obtaining the diff, gather surrounding context from related callers,
callees, types, and tests.

## Reporting Findings

Use a structured format so findings are easy to reference in follow-up discussion:

1. **Review Header**: scan-friendly metadata for the review.
2. **Findings Index**: numbered one-line entries sorted by priority.
3. **Detailed Findings**: one subsection per finding with full context.
4. **Open Questions**: separate numbered list for unresolved questions.

`Review Header` fields:

- Base
- Head
- Scope
- Verdict (`approve`, `approve-with-notes`, or `changes-requested`)
- Severity counts (`P0:<n> P1:<n> P2:<n> P3:<n>`)

Assign a stable ID to every finding (`F01`, `F02`, ...) and every question
(`Q01`, `Q02`, ...). Reuse the same ID in all follow-up references.

`Findings Index` entry format:

`<number>. [<priority>][<confidence>] <id> - <short title> - <file:line> (<impact>)`

`Detailed Findings` heading format:

`### <id> - <short title>`

Within each detailed finding, use this exact field order:

- Severity (`P0`, `P1`, `P2`, or `P3`)
- Confidence (`High`, `Medium`, or `Low`)
- Location (`file:line` and symbol when possible)
- Impact (`correctness`, `complexity`, `performance`, `security`, or `operations`)
- Risk (concrete failure scenario or design risk)
- Evidence (code path, caller, type, test, or behavior proof)
- Fix direction (when straightforward)

Additional rules:

- Use one issue per root cause; do not duplicate findings for the same cause.
- If one finding affects multiple locations, keep one ID and add `Also affects`.
- Use one issue per finding; split mixed concerns into separate IDs.
- Prefer `file:line` plus symbol for stable references.
- Use numbered lists, not Markdown tables, for terminal readability.
- Order by priority: blocking issues, non-blocking improvements, then open questions.
- Keep open questions in a separate `Open Questions` section using `Qxx` IDs,
  and include `Blocking: yes` or `Blocking: no` for each question.
- If there are no findings, write `Findings Index: None` and
  `Detailed Findings: None`.
- If there are no open questions, write `Open Questions: None`.

## Applying Judgment

- Do not report speculative issues without a realistic scenario.
- Respect project conventions and match rigor to change impact.
- Accept tactical fixes when appropriate, but note debt and follow-up work.

Goal: surface the highest-impact issues that improve correctness and make the
system easier to understand, change, and operate safely over time.
