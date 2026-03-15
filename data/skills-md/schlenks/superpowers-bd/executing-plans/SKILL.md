---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

Load beads epic, review critically, execute tasks in dependency-aware batches, report for review between batches.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."
**REQUIRED BACKGROUND:** Read `superpowers-bd:beads` SKILL.md first (bd CLI usage, permission avoidance, dependency management).
**Prerequisites:** Beads epic exists (via plan2beads), dependencies set (`bd blocked` shows expected blockers).

## The Process

### Step 1: Load and Review Epic

`bd show <epic-id>`, check `bd ready` and `bd blocked`. Review critically -- raise concerns before starting.

### Step 2: Execute Batch

Batch = all currently ready issues (no blockers). For each:
1. `bd update <id> --status=in_progress` then `bd show <id>`
2. Follow each step exactly; run verifications as specified
3. **REQUIRED:** `git diff --cached --stat` -- any file >50 lines changed -> apply the appropriate rule-of-five variant: `Skill(superpowers-bd:rule-of-five-code)` for code, `Skill(superpowers-bd:rule-of-five-tests)` for test files. Complete all 5 passes before proceeding
4. Commit the work
5. `bd close <id>` -- unblocks dependent issues

File conflicts: serialize issues touching same file. See `references/batch-execution-detail.md`.

### Step 3: Report (Task-Tracked)

Create checkpoint task after each batch. Show: implemented work, verification output, rule-of-five variant passes, newly unblocked issues (`bd ready`). Say: "Ready for feedback." See `references/report-and-feedback.md`.

### Step 4: Continue (Task-Tracked)

Create blocked feedback + execution tasks to enforce checkpoint. Do NOT proceed until human feedback received. See `references/report-and-feedback.md`.

### Step 5: Complete Development

All epic issues closed -> verify with `bd show <epic-id>` -> hand off to `superpowers-bd:finishing-a-development-branch`. See `references/completion-protocol.md`.

## Dependency-Aware Batching

```
Batch 1: All tasks with no blockers (bd ready)
         Close completed -> check bd ready again
Batch 2: Newly unblocked tasks
         Close completed -> check bd ready again
```

See `references/batching-example.md` for full walkthrough.

## Epic Scoping

`bd ready` shows ALL epics. Filter to current epic: `bd show <epic-id>` for child IDs, only work on issues that are both ready AND children of your epic.

## When to Stop

STOP when: blocker mid-batch, no ready issues but open issues remain, unclear instructions, repeated verification failures. Check `bd blocked` for deadlocks. See `references/epic-scoping-and-deadlock.md`.

**Ask for clarification rather than guessing.**

## Remember

- Check `bd ready` before each batch, close issues promptly to unblock dependents
- Follow issue steps exactly, don't skip verifications
- Reference skills when issue says to
- Between batches: report and wait for feedback
- Stop when blocked, don't guess
- **REQUIRED: Apply appropriate rule-of-five variant before committing any file >50 lines changed** (`rule-of-five-code` for code, `rule-of-five-tests` for tests)

## Integration

- **plan2beads** -- creates the epic (must run first)
- **superpowers-bd:finishing-a-development-branch** -- after all issues
- **superpowers-bd:subagent-driven-development** -- alternative: same session, parallel execution

## Reference Files

- `references/batch-execution-detail.md`: Full Step 2 procedure with file conflict handling and rule-of-five-code trigger
- `references/report-and-feedback.md`: Steps 3+4 TaskCreate blocks and feedback enforcement flow
- `references/batching-example.md`: Dependency-aware batching walkthrough with bd ready/blocked at each stage
- `references/epic-scoping-and-deadlock.md`: Epic scoping, deadlock detection, bd failures, when to revisit
- `references/completion-protocol.md`: Step 5 completion handoff to finishing-a-development-branch

<!-- compressed: 2026-02-11, original: 652 words, compressed: 434 words -->
