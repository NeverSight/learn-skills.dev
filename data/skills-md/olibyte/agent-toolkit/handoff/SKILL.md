---
name: handoff
description: Reconstructs or writes a coding-agent handoff from git and `.agents/handoff.md`. Use when the user is about to switch coding agents (Claude Code, Cursor, Codex, Antigravity), a usage limit expired, or a new agent is picking up in-progress work.
license: MIT
---

Chat history does not follow across tools. Reconstruct from files.

Codex invokes this skill as `$handoff`. Claude Code, Cursor, and Antigravity invoke it as `/handoff`.

## Sources

Read these before you ask the user anything:

- `git status`
- `git diff`
- `git log -5`
- `AGENTS.md`
- `.agents/handoff.md` if it exists

If git is unavailable, say so and use the files that exist.

## Leaving

The user is switching away, or a usage limit is about to expire.

1. Create `.agents/` if needed.
2. Write `.agents/handoff.md` with branch, what is in progress, what is done, what is blocked, and the next command.
3. Tell the user to commit before they switch. Do not commit unless they ask.

Do not put secrets, tokens, or credentials in the file.

```markdown
# Handoff

- Branch:
- In progress:
- Done:
- Blocked:
- Next command:
```

## Arriving

A new agent is picking up in-progress work.

Read the sources above. State the current position from those files. Do not ask the user to recap what they already say.
