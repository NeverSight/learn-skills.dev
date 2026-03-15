---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session
---

# Subagent-Driven Development

Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance review first, then code quality review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration

## When to Use

**Use when:**
- Have implementation plan
- Tasks mostly independent
- Want to stay in this session

**vs. Executing Plans (parallel session):**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Two-stage review after each task
- Faster iteration (no human-in-loop between tasks)

## The Process

1. Read plan, extract all tasks with full text, create TodoWrite
2. For each task:
   - Dispatch implementer subagent (./implementer-prompt.md)
   - If questions: answer, re-dispatch
   - Implementer implements, tests, commits, self-reviews
   - Dispatch spec reviewer (./spec-reviewer-prompt.md)
   - If issues: implementer fixes, re-review
   - Dispatch code quality reviewer (./code-quality-reviewer-prompt.md)
   - If issues: implementer fixes, re-review
   - Mark task complete
3. After all tasks: dispatch final code reviewer
4. Use finishing-a-development-branch skill

## Prompt Templates

- `./implementer-prompt.md` - Dispatch implementer subagent
- `./spec-reviewer-prompt.md` - Dispatch spec compliance reviewer
- `./code-quality-reviewer-prompt.md` - Dispatch code quality reviewer

## Red Flags

**Never:**
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed issues
- Dispatch multiple implementation subagents in parallel
- Make subagent read plan file (provide full text instead)
- Start code quality review before spec compliance passes

**If subagent asks questions:**
- Answer clearly and completely
- Don't rush them into implementation

**If reviewer finds issues:**
- Implementer fixes them
- Reviewer reviews again
- Repeat until approved
