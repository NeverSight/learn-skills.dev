---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for architect review.

**Announce at start:** "I'm using the executing-plans skill to implement this plan. **REQUIRED:** Ensure Antigravity is set to **Fast Mode** for efficient execution."

## Step 0: Prerequisites

**STOP if:**
- (a) You are on main or master branch without explicit user instruction
- (b) There are uncommitted changes not related to this plan

Resolve both conditions before proceeding. Never start implementation on main/master branch without explicit user instruction.

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create TodoWrite and proceed

### Step 2: Execute Batch

**Batch size criteria:**
- Default batch: 3 tasks
- Shrink to 1 task if: first task in a new phase, or previous batch had failures
- Expand to 5 tasks if: all tasks are mechanical (file copies, config changes) with no logic

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Report

When batch complete, use this template:

```
## Batch Report
Tasks completed: [N-M]
Files changed: [list]
Tests: [passed X / failed Y / skipped Z]
Verification output:
  [paste exact command output]
Ready for feedback.
```

**If Tests: failed > 0:**
Do NOT mark tasks completed. Report the failure with exact test output.
Load systematic-debugging skill. Do not proceed to next batch until failures are resolved.

### Step 4: Continue
Based on feedback:
- Apply changes if needed
- Execute next batch
- Repeat until complete

### Step 5: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- Before loading: verify (a) all tasks are marked completed, (b) all tests pass, (c) no BLOCKERS.md is active.
- **REQUIRED SUB-SKILL:** Load finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

**If the session ends without human response, or if 2 or more messages have passed without acknowledgment of the STOP:**
1. Document the blocking question in a `BLOCKERS.md` file
2. Mark the plan task as 'blocked'
3. Skip to the next non-dependent task if one exists
4. If no tasks are unblocked, leave a clear status note and stop

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Complete Step 0 prerequisites before anything else
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Between batches: just report and wait
- Stop when blocked, don't guess

## Integration

**Required workflow skills:**
- **writing-plans** - Creates the plan this skill executes
- **finishing-a-development-branch** - Complete development after all tasks

## Completion State

The session is complete when:
- All plan tasks are marked completed
- Final batch report shows zero test failures
- finishing-a-development-branch skill has been loaded and executed

Announce: "Plan execution complete. All [N] tasks finished. Branch ready for review."
