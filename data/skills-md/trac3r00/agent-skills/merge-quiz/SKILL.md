---
name: merge-quiz
description: Pre-merge comprehension gate that quizzes the USER on the riskiest parts of the branch diff. Use before merging or opening a PR, or when the user says "merge quiz", "am I ready to merge", or "quiz me on this diff".
version: 1.0.0
author: Hien Dinh
license: MIT
---

# Merge Readiness Quiz

Before shipping, verify the HUMAN understands what's being merged. The quiz
tests the user, not the agent.

## Process

1. **Resolve the base deterministically.** Prefer, in order: the base explicitly
   named by the user; the current branch's configured upstream; the remote
   default branch from `refs/remotes/origin/HEAD`; then an existing local
   `main` or `master`. Verify the candidate with `git rev-parse --verify` before
   using it. If no candidate exists, ask for a base ref and stop.
2. **Gather the material.**
   - Diff: `git diff <base>...HEAD`. If it is empty, also check
     `git diff <base>..HEAD`, tracked worktree changes, and relevant untracked
     files reported by `git status --short`. State exactly which material was
     selected. If all are empty, stop because there is nothing to quiz.
   - Exclude generated files (lockfiles, `*.pbxproj`, build outputs, vendored
     code) from quiz material — churn there is noise, not comprehension risk.
   - Deviation log: prefer files for the current branch/task slug. If task
     identity is unavailable, include only deviation files changed in the diff;
     do not sweep unrelated logs by date.
3. **Pick the 3–5 riskiest spots.** If the diff is too small for 3 real
   questions, ask fewer and say why. First name what "dangerous" means in THIS
   codebase's domain — auth/money/deletion/migrations in a backend; lifecycle,
   state loss, and accessibility regressions in a UI app; loss/duplication/
   ordering in a pipeline. Then prioritize: behavior changes on those paths,
   deviations from the plan, error handling changes, anything irreversible.
4. **Quiz one question at a time** using the harness's question tool (e.g. AskUserQuestion in Claude Code) or plain-text
   multiple choice if this agent has no such tool). If no interactive user is
   available, output the quiz and stop without answering for them. Each question:
   - Cites the exact file:line it's about
   - Asks about consequences, not trivia: "what happens if X is null here?",
     "why did we bypass Y?", "what breaks if this runs twice?"
   - Offers 3-4 plausible answers (one correct, distractors that reflect real
     misunderstandings)
   - Has one correct answer backed by the exact diff hunk or file:line; if no
     evidence exists in the diff, do not ask that question
5. **On a wrong or unsure answer:** explain the correct answer immediately,
   quoting the exact diff hunk verbatim so the user can dispute it — the quiz
   grades the user against the agent's reading of the diff, and that reading
   can be wrong. If the user disputes with evidence, concede the question,
   correct the score, and flag the spot as review-carefully either way.
6. **Produce the merge-readiness note** (paste-ready for the PR description):

```markdown
## Merge readiness
- Quiz: N/M correct
- Review carefully: <file:line — why, for each missed question; or "nothing flagged">
- Deviations from plan: <one line each, from the deviation log; or "none">
```

## Rules

- Never skip the quiz because the diff "looks simple" — simple diffs hide the
  best surprises. But never pad with fake-risk questions.
- Questions must be answerable from the diff the user supposedly reviewed; no
  gotchas about untouched code.
