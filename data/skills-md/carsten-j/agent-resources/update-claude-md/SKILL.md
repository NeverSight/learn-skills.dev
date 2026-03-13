---
name: update-claude-md
description: You are updating this project's CLAUDE.md to reflect **meta learnings** (conventions, philosophy, gotchas) and **significant recent changes** to the codebase.
disable-model-invocation: true
---

# Update Claude.md with learnings

## What TO Add

- **Philosophy/conventions** - e.g., "No backwards compatibility unless explicitly requested"
- **Gotchas** - Non-obvious things that cause bugs repeatedly
- **Commands or scripts** - New ways to run/test things
- **Structure changes** - When directories or files move
- **Recent significant changes** - New features, refactors, or capabilities added

## What NOT to Add

- Specific technical details about a single bug fix
- Implementation details that are obvious from code
- Temporary workarounds
- One-off decisions that won't recur
- Verbose explanations of how something works

**Rule of thumb**: If it's something you'd tell a new developer joining the project, add it. If it's just details about today's work, skip it.

## Instructions

1. **Read current CLAUDE.md** - Understand what's already documented
2. **Review recent work** - Check git log/diff for significant changes; extract meta learnings
3. **Update conservatively** - Keep CLAUDE.md <300 lines. Remove outdated info if needed.

## Output

After updating, summarize:
- What was added
- What was removed (if anything)
- Current line count