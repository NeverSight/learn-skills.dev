---
name: cc-refactoring-guidance
description: "Guides safe refactoring using Code Complete's fix-first-then-refactor discipline: decides between refactor, rewrite, and fix-first; enforces separate commits; applies small-change rigor to high-error-rate one-liners. Not for diagnosing the bug itself (use cc-debugging), transforming working code's complexity (use aposd-simplifying-complexity), or untested legacy code (it routes to welc-legacy-code)."
user-invocable: false
---

# cc-refactoring-guidance

Refactoring is behavior-preserving change to *working* code. Three rules govern it:

- **Fix first, then refactor** — never in the same change; separate commits with a boundary between them.
- **Small changes need MORE rigor, not less** — 1–5-line changes have the highest error rate.
- **Over half of changes fail the first attempt** — review and test even "trivial" ones; the error rate is per change, not cumulative.

| Rule | Value | Source |
|---|---|---|
| Small-change error rate | Peaks at 1–5 lines | Weinberg 1983 |
| First-attempt success | <50% for any change | Yourdon 1986b |
| Review effect on 1-line changes | 55% → 2% error rate | Freedman and Weinberg 1982 |

Shared thresholds (routine length, parameters, cohesion): `Read(${CLAUDE_PLUGIN_ROOT}/references/cc-foundations.md)`. The full 40-item refactoring checklist: `Read(${CLAUDE_SKILL_DIR}/checklists.md)`.

**Definitions:**
- **small** = ONE structural change (one rename, one extract, one inline). If you describe it with "and", it's not small.
- **review** = a distinct person (or AI) examines the diff. Self-review does not satisfy this.
- **working code** = all tests pass AND no known behavior bugs. Compiles-but-fails-tests is not working.
- **then** (fix first, *then* refactor) = with a commit boundary between the activities, not the same commit.

## Before refactoring: identify the target pattern

Refactor *toward* something, not just away from bad code. Find the best examples of the target pattern in this codebase, the module's conventions, and how similar refactorings were structured; match the existing pattern exactly, or — if none exists — be deliberate about the precedent you're setting. Full gate: `Read(${CLAUDE_PLUGIN_ROOT}/references/pattern-reuse-gate.md)`.

## Core patterns

- **Mixing fix and refactor → separate commits.** Fix the bug, verify, commit; then refactor, commit. "I'm just cleaning while I fix" is the anti-pattern.
- **Casual small change → rigorous small change.** Desk-check, review (55% → 2%), and run regression tests even on one line.
- **Documenting bad code → rewriting it.** A comment explaining confusing code is a signal to make the code self-explanatory instead.

## Modes

### APPLIER

Guide the refactoring decision and the safe process.

When production is down: fix only — no refactoring or cleanup — deploy, then refactor as a separate activity when stable. Combining the two raises complexity and error likelihood.

**Refactor vs rewrite:**
1. Does the code currently work? NO → this is fixing, not refactoring; fix first.
2. Is the design fundamentally sound? NO → consider rewriting.
3. Would changes touch >30% of the module? YES → "big refactoring"; consider a rewrite.

**Safe process (priority order):**
1. Save the starting code (version-control checkpoint).
2. Keep each refactoring small — one change at a time.
3. List the planned steps before executing.
4. Do one at a time; recompile and retest after each — state "tests pass after [change]".
5. Use frequent checkpoints (commit working states).
6. Enable the pickiest compiler warnings.
7. Retest after each change and report results, not just "tests pass".
8. Review changes — required even for 1-line changes.
9. Adjust for risk — extra caution for high-risk changes.

If tests fail after a refactoring: don't debug extensively — back out the change, take a smaller step, and reconsider whether you understood the code.

**When prerequisites are missing:**
- No automated tests → `Skill(code-foundations:welc-legacy-code)` and write characterization tests first; if impossible, document expected behavior, write a manual test script, and increase review rigor.
- No version control → back up files before starting; set up VCS first if at all possible.
- No reviewer → systematic checklist-based self-review, smaller changes, more commits and tests to compensate.

### TRANSFORMER

Transform code smells into clean code while preserving all observable behavior (same tests pass before and after): setup/takedown smell → encapsulated interface; tramp data → direct access or restructure; duplicated code → extracted routine; speculative "design ahead" code → remove it. Behavior changes are fixing, not refactoring — fix first.

## Recovering from a violation

If you mixed fix and refactor in one commit:
- Before push: `git reset --soft HEAD~1`, separate the changes, re-commit properly.
- After push: document it and split in a follow-up PR; don't force-push shared branches.

If you skipped review on a small change:
- Before merge: get the review now.
- After merge: note it and move on.

Fixing a violation post-commit still costs less than the bugs it would otherwise cause.

## Chain

| After | Next |
|---|---|
| Refactoring complete | `Skill(code-foundations:cc-control-flow-quality)` |
| Structure changed | `Skill(code-foundations:cc-routine-and-class-design)` |
| Reviewing a refactoring | `Skill(code-foundations:aposd-reviewing-module-design)` |
