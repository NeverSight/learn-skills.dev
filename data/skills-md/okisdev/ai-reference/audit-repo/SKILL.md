---
name: audit-repo
description: Run a multi-round parallel verification sweep over recent work or a whole repository, tracking findings in a fix ledger and looping fix and re-verify rounds until a round comes back clean.
argument-hint: "[scope] [--rounds <n>] [--agents <n>]"
---

## Context

Current branch and status: !`git branch --show-current; git status --short | head`

Commits ahead of the default base: !`git log $(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main)..HEAD --oneline 2>/dev/null || echo "(none or base not found)"`

Existing ledger: !`test -f fix.md && echo "yes, resume it" || echo "(none)"`

## Instructions

Sweep the scope with parallel verification agents covering distinct angles, track every finding in a fix ledger, fix and re-verify until a full round finds nothing new, and never let the ledger or a weakened check ship.

### Process

1. Parse `$ARGUMENTS` (scope is a path, a feature, or `all`, defaulting to the work since the default base when on a feature branch and the whole repository otherwise; `--rounds` caps the loop, default 5; `--agents` sets verifiers per round, default 5). Resume an existing `fix.md` ledger instead of starting over.
2. Write the ledger `fix.md` at the repository root: numbered findings, each with status open, fixed, or rejected, its evidence, and the round it surfaced in. Follow [references/rounds.md](references/rounds.md) for the exact ledger format.
3. Run a round: dispatch the round's verification agents in one parallel batch, each covering a distinct angle (functional correctness, convention conformance, rendered UI when the scope has UI, tests and types, docs and dead surface); every agent returns concrete findings with file and line evidence. A non-trivial claim needs two independent verifiers, because a single verifier's confirmation is unreliable. See [references/rounds.md](references/rounds.md) for the full angle menu and dispatch mechanics.
4. Triage into the ledger: confirmed findings open, refuted findings rejected with the stated reason, duplicates merged into the earliest entry, and a finding whose check itself failed (repro would not run, environment blocked it) recorded as inconclusive with the blocker named, never dropped or rounded to rejected.
5. Fix every open finding, independent fixes in parallel, then re-verify each fix with a fresh check before flipping it to fixed; a fix that has not been re-verified stays open.
6. Loop to step 3 with fresh angles and fresh eyes until a full round yields zero new confirmed findings, or the round cap hits; hitting the cap is a reported outcome, not a silent stop.
7. Close out: report rounds run, findings found, fixed, and rejected, and any remaining risk. Delete `fix.md` once the report carries its content; the ledger is working state.

### Rules

- Never weaken, skip, or delete a failing check to make a round converge.
- A UI finding needs render evidence, not code reading alone; compose `verify-ui` when it is installed.
- Never commit `fix.md`; remove the ledger first if a commit is later requested.
