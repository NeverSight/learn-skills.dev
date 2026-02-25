---
name: cook-fast
description: '[Implementation] ⚡ Fast implementation - skip research, minimal planning'
argument-hint: [tasks]
---

Start working on these tasks immediately with minimal planning:
<tasks>$ARGUMENTS</tasks>

**Mode:** FAST - Skip research, minimal planning, trust your knowledge.

## ⚠️ Anti-Hallucination Reminder

**Before modifying ANY code:** Verify assumptions with actual code evidence. Search for usages, read implementations, trace dependencies. If confidence < 90% on any change, investigate first or ask user. See `.claude/skills/shared/anti-hallucination-protocol.md` for full protocol.

## Workflow

1. **Quick Planning** (skip research phase)
    - Analyze task requirements directly
    - Create minimal todo list with `TodoWrite`
    - NO researcher subagents, NO scout commands

2. **Rapid Implementation**
    - Use `/code` directly on tasks
    - Skip multi-step planning documents
    - Focus on working code over documentation

3. **Quick Validation**
    - Run type-check and compile
    - Manual spot-check over full test suite
    - Skip code-reviewer subagent

4. **Commit** (optional)
    - Ask user if ready to commit via `AskUserQuestion`
    - If yes, use `/commit`

## When to Use

- Simple features with clear requirements
- Bug fixes with known solutions
- Refactoring tasks
- When user says "just do it"

## Trade-offs

| Aspect   | Fast Mode   | Full Mode       |
| -------- | ----------- | --------------- |
| Research | Skipped     | Multiple agents |
| Planning | Minimal     | Full plan docs  |
| Testing  | Quick check | Full test suite |
| Review   | Skipped     | Code-reviewer   |
| Speed    | ~2x faster  | Thorough        |

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
