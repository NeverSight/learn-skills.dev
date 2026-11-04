---
name: review-diff
description: >-
  Reviews a git diff through reviewer subagents on each lens (big picture, detail), then checks and triages
  the findings and fixes clear problems.
  Use when the user asks for a code review, PR review, sanity check on changes,
  or reviews with specific or multiple models.
disable-model-invocation: false
---

# Review diff

Reviews always run in subagents: a fresh context, on a different model from the implementer (which is probably you).
Each subagent reviews through one **lens**: a file saying what to look for and how much code to read.
You coordinate: scope, lenses, launch, check, triage, fix, report.

Other skills reuse this flow with their own lens set (for example, `/deep-review`).

## 1. Scope

The default change set is the working tree against the current branch's `HEAD`:
`git diff HEAD` plus untracked files (`git status --short`), which the diff doesn't show.
If that's empty (for example, a clean tree on a feature branch),
ask the user for the range, such as the merge-base with `main`.
Don't launch reviewers on an empty change set.

Find the originating ticket, task, or plan, if there is one, so lenses that judge against it can.

## 2. Lenses

Use the lens set the calling skill gives. Otherwise, the standard set:

- [`lenses/big-picture.md`](lenses/big-picture.md), on the `strong` tier:
  approach, fit, boundaries, consistency, and the originating work.
- [`lenses/detail.md`](lenses/detail.md), on the `standard` tier:
  logic, edge cases, data flow, small-scale consistency.

Brief reviewers with absolute paths: `reviewer.md` and the standard lenses live in this skill's directory
(`review-diff`'s), whichever skill supplies the lens set.

## 3. Choose models

For each lens:

- User names models → one reviewer per model.
- User gives a count → that many reviewers.
- Otherwise → one reviewer.

Resolve models with the `/model-tiers` skill: named models as the user named them, the rest from the lens's tier.
Models should be different from the implementer when possible.

## 4. Launch

Launch all reviewers in parallel, in one message, as `/model-tiers` describes, and wait for their results.
Brief each with:

```text
Read and follow <absolute path to review-diff's directory>/reviewer.md.
Lens: <absolute path to the lens file>
Review: <diff command, e.g. git diff HEAD, plus any untracked files by path>
Originating work: <ticket/task/plan pointer, or "none">
```

Point at the files; don't summarise them into the brief.

If a reviewer fails, retry once. If it fails again, continue with the other reviewers' findings and report the failure.
If every reviewer fails, report the blocker and stop.

## 5. Check and triage

Merge findings from all reviewers. Merge findings that share a root cause, across lenses.
Note where reviewers disagree, especially on design questions.

Check each finding against the code before acting on or reporting it.
Drop findings that don't hold, and say why in the report.
A fix-now or fix-trivial you can't confirm either way is a design question.
Drop other findings you can't confirm.

| Category | Action |
|----------|--------|
| **fix-now** | Fix directly. |
| **fix-trivial** | Fix directly when the fix is local and uncontroversial. |
| **design-question** | Don't fix. Present to the user with enough context to decide. |
| **informational** | Mention briefly; no change unless the user asks. |

Treat a fix-now as a design question when:

- another reviewer calls it a design question,
- it has more than one reasonable remediation, or
- it changes user-visible behaviour.

Skip fixes that expand scope beyond the reviewed diff, unless the diff introduced the bug.

## 6. Fix

Apply fix-now and fix-trivial items. Match existing codebase style. Run the project's lint, if known.

Don't re-run the review unless the user asks.

## 7. Report

1. **Reviewers**: lens and model per reviewer, with its finding counts.
   Group reviewers on the `cheap` tier into one line: their lenses, models, and total findings.
   Note any fallback: another tier, or a reviewer on the implementer's model.
2. **Fixed**: what changed and why; group trivial fixes briefly.
3. **Dropped**: findings the check rejected, one line each with the reason.
4. **Design questions**: numbered, with the trade-off and each reviewer's view where they disagreed.
5. **Informational**: one line, if anything noteworthy remains.

Name the lens each finding came from.
If nothing needed fixing and there are no design questions, say so in one sentence.
