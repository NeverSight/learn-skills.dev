---
name: verification-before-completion
description: Run verification commands before claiming work is complete or fixed. Use before asserting any task is done, bug is fixed, tests pass, or feature works.
---

# Verification Before Completion

**Core Principle:** No completion claims without fresh verification evidence.

Unverified claims break trust and ship broken code: undefined functions that crash production, incomplete features missing requirements, lost time on rework after false completion. The cost of running one command is trivial compared to the cost of a wrong claim.

## The Verification Gate

Before any claim of success, completion, or satisfaction:

1. **IDENTIFY** - What command proves this claim?
2. **RUN** - Execute the full verification command (fresh, complete)
3. **READ** - Check full output, exit code, failure counts
4. **VERIFY** - Does output confirm the claim?
   - NO - State actual status with evidence
   - YES - State claim WITH evidence from step 2-3

## When This Applies

Before:

- Claiming "tests pass", "build succeeds", "linter clean", "bug fixed"
- Expressing satisfaction ("Great!", "Done!", "Perfect!")
- Using qualifiers ("should work", "probably fixed", "seems to")
- Committing, creating PRs, marking tasks complete
- Marking a multi-file implementation as complete (dispatch `ce:code-reviewer` agent)
- Moving to next task or delegating work

## Common Verification Requirements

| Claim                 | Required Evidence                | Not Sufficient                |
| --------------------- | -------------------------------- | ----------------------------- |
| Tests pass            | `yarn test` output: 0 failures   | Previous run, "looks correct" |
| Build succeeds        | Build command: exit 0            | Linter clean, "should work"   |
| Bug fixed             | Test reproducing bug: now passes | Code changed, assumed fix     |
| Linter clean          | Linter output: 0 errors          | Partial check, spot test      |
| Regression test works | Red→Green cycle verified         | Test passes once              |
| Agent task complete   | VCS diff shows expected changes  | Agent reports "success"       |
| Work is complete      | Code review via `ce:code-reviewer` with no unresolved Critical issues | Self-review, "looks good to me" |

## Red Flags

Stop and verify if you're about to:

- Use hedging language ("should", "probably", "seems to")
- Express satisfaction before running verification
- Trust agent/tool success reports without independent verification
- Rely on partial checks or previous runs

## Key Examples

**Regression test (TDD Red-Green):**

```
Write test → Run (fail) → Fix code → Run (pass) → Revert fix → Run (fail) → Restore → Run (pass)
vs. "I've written a regression test" (without verifying red-green cycle)
```

**Build vs Linter:**

```
Run `npm run build` → See "exit 0" → Claim "build passes"
vs. Run linter → Claim "build will pass" (linter ≠ compiler)
```

**Agent delegation:**

```
Agent reports success → Check `git diff` → Verify changes → Report actual state
vs. Trust agent's success message without verification
```
