---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for architect review.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with user before starting
4. If no concerns: Create tasks via TaskCreate and proceed

### Step 2: Execute Batch
**Default: First 3 tasks**

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. **Record discoveries** — After each task, append any unexpected findings, decisions, or technical insights to `.planning/findings.md`
5. Mark as completed

### Step 3: Report and Update Progress
When batch complete:
- Show what was implemented
- Show verification output
- **Update `.planning/progress.md`** (if `.planning/` exists):
  - Mark completed tasks as `complete` in the Task Status Dashboard
  - Append batch summary to the session log section
- **Update `.planning/findings.md`** — Consolidate any discoveries, decisions, or surprises from this batch
- Say: "Ready for feedback."

### Step 4: Continue
Based on feedback:
- Apply changes if needed
- Execute next batch
- Repeat until complete

### Step 5: Complete Development

After all tasks complete and verified:
- **Read `.planning/progress.md`** to compile a full summary of all batches, test results, and verification evidence before presenting final status
- Announce: "I'm using the finishing-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpower-planning:finishing-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Between batches: just report and wait
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent
- After each task, record discoveries to `.planning/findings.md`
- After each batch, update both `.planning/progress.md` and `.planning/findings.md`
- Before final report, read `.planning/progress.md` for full summary

## Integration

**Required workflow skills:**
- **superpower-planning:git-worktrees** - RECOMMENDED: Set up isolated workspace unless already on a feature branch
- **superpower-planning:writing-plans** - Creates the plan this skill executes
- **superpower-planning:finishing-branch** - Complete development after all tasks
