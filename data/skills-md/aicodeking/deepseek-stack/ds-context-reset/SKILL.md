---
name: ds-context-reset
description: "Keep a PROGRESS.md for long tasks and move to a fresh session or subagent that reads only that file when the context gets long or stale. Use when a task spans many steps or sessions, when the model starts repeating itself, forgets earlier facts, or re-tries old fixes, or when the context window is past about half full. Invoke as /ds-context-reset."
---

# ds-context-reset

Store the state of the work in a file, not in the chat, so a fresh context can continue without drift.

## Steps

1. At the start of a long task, create PROGRESS.md at the repo root with these sections:
   - **Goal**: one or two sentences, plus the acceptance check for the whole task.
   - **Done**: the verified steps, each with the command and result that proved it.
   - **Next**: the ordered steps that remain. The first item is the exact next action.
   - **Open questions**: unknowns and decisions that wait for the user.
   - **Key facts**: paths, commands, versions, gotchas, and approaches that failed (with the reason).
2. Update PROGRESS.md after every verified step. Do not update it for unverified ones. Commit the code and PROGRESS.md together with a descriptive message.
3. Watch for reset signals: you repeat an earlier answer, you forget a fact that is in Key facts, you retry a fix that failed, the same file gets reread many times, or the context is more than about half full.
4. When a signal appears, finish or revert the current step so the tree is in a known state.
5. Rewrite PROGRESS.md as a complete handoff. A reader who has only this file and the repo must be able to continue. Remove chatter and keep the facts.
6. Start a fresh session or subagent. Give it one instruction: "Read PROGRESS.md and `git log -5`, run the acceptance check for the last Done item, then do the first item in Next."
7. In the new context, confirm that the baseline check passes before you make new edits. If it fails, fix that first.

## Stop when

- The goal's acceptance check passes and PROGRESS.md shows every item as Done.
- You have done 3 resets on one Next item without progress. Stop and ask the user, with the file as your report.

## Rules

- PROGRESS.md holds facts and evidence, not plans that nobody has checked.
- Keep it under about 150 lines. Move old Done items into a short summary line.
- Never put secrets or tokens in it.
- The fresh context reads the file, not the old transcript.
- Pair with ds-plan-loop for the Next list and with ds-unstick for the failed-approach notes.
