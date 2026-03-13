---
name: finishing-a-development-branch
description: Use when ALL tasks in an epic or branch are closed and you are ready to integrate the entire body of work - never after individual task completions, never mid-epic
---

# Finishing a Development Branch

## Guard: Do NOT Use Mid-Epic

**STOP.** Before proceeding, check:

1. **Are you a subagent implementing a single task?** -> This skill does NOT apply. Report your evidence and stop.
2. **Are there still open tasks in the epic?** -> This skill does NOT apply. Only the orchestrator at COMPLETE state should invoke this.
3. **Is there an epic with a `completion:*` label?** -> Read it and execute automatically (see Step 3 Auto below). No prompting needed.

**This skill is ONLY for:** The final integration step after ALL work is done. If even one task remains open, do not invoke this skill.

## The Process

### Step 0: Check Epic Verification Tasks (If Applicable)

**Skip if** not working on a beads epic. Otherwise, run `bd list --parent <epic-id>` and check for verification tasks. Three outcomes: open verification tasks (STOP), no verification tasks/legacy (WARNING, proceed), all closed (proceed). See `references/epic-verification.md`.

### Step 1: Verify Tests (Task-Tracked)

Create a "Verify all tests pass" task. Run the project's full test suite.

**ENFORCEMENT:** Cannot mark completed unless test command was run fresh, output shows 0 failures, and exit code was 0. If tests fail, stop. See `references/test-verification.md`.

### Step 1.5: Pre-Merge Simplification (Task-Tracked, Mandatory)

Create a "Pre-merge simplification" task blocked by test verification. Get changed files: first run `git merge-base HEAD main` to get the base SHA, then `git diff --name-only <base-sha>..HEAD`. Dispatch `code-simplifier:code-simplifier` on the full changeset. If changes made, re-run tests -- revert if they fail, commit if they pass. See `references/pre-merge-simplification.md`.

### Step 2: Determine Base Branch

```bash
git merge-base HEAD main
```
If that fails, try `git merge-base HEAD master` instead.

Or ask: "This branch split from main - is that correct?"

### Step 3 Auto: Execute Pre-Chosen Strategy

If the epic has a `completion:*` label, execute automatically:

| Label | Action |
|-------|--------|
| `completion:commit-only` | Verify clean tree. Done. |
| `completion:push` | Verify clean, push. |
| `completion:push-pr` | Push, create PR. |
| `completion:merge-local` | Merge to base locally. |

Skip to Step 5 if applicable. See `references/completion-strategies.md`.

### Step 3 Manual: Present Options

If no `completion:*` label, present exactly 4 choices:

1. Merge back to \<base-branch\> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Keep options concise. See `references/completion-strategies.md`.

### Step 4: Execute Chosen Option

Execute the user's chosen option. Each option has specific bash commands and confirmation requirements. Option 4 (Discard) requires typed "discard" confirmation. See `references/option-workflows.md`.

### Step 5: Cleanup Worktree

**Options 1, 2, 4:** Check if in worktree (`git worktree list`), remove if yes.
**Option 3:** Keep worktree. See `references/worktree-cleanup.md`.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | Y | - | - | Y |
| 2. Create PR | - | Y | Y | - |
| 3. Keep as-is | - | - | Y | - |
| 4. Discard | - | - | - | Y (force) |

## Common Mistakes

- **Skip test verification** -> merge broken code. Always verify tests first.
- **Open-ended questions** -> present exactly 4 options, not "what should I do?"
- **Auto-cleanup worktree** -> only for Options 1 & 4, not 2 & 3.
- **No discard confirmation** -> require typed "discard" before Option 4.

See `references/red-flags.md` for detailed Never/Always lists.

## Integration

**Called by:** subagent-driven-development (Step 7), executing-plans (Step 5)
**Pairs with:** using-git-worktrees (cleans up worktree created by that skill)

## Reference Files

- `references/epic-verification.md`: checking beads epic verification tasks
- `references/test-verification.md`: task-tracked test verification protocol
- `references/pre-merge-simplification.md`: code simplifier dispatch protocol
- `references/completion-strategies.md`: auto/manual completion strategy details
- `references/option-workflows.md`: execution details for all 4 options
- `references/worktree-cleanup.md`: worktree cleanup procedures
- `references/red-flags.md`: detailed red flags and common mistakes

<!-- compressed: 2026-02-11, original: 797 words, compressed: 679 words -->
