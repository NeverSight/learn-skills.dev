---
name: context-handoff
description: Use when a coding session is approaching context limits, spans multiple workflow phases, or must pause before the work is complete.
---

# Context Handoff

Create one compact, source-grounded checkpoint so another session can resume
without relying on conversation memory.

## When to use

Use this skill only when the task is unfinished and one of these is true:

- the session is approaching its context limit;
- the work spans multiple phases or will continue in another session; or
- the user asks to pause, hand off, or resume later.

Do not create handoffs for short tasks that are already complete.

## Write the checkpoint

1. Read `AGENTS.md`, then inspect `git status --short`, the relevant diff, the
   change's `decisions.md` and the other decision sources in
   `implement-task`'s `## Decision sources`, and the
   relevant wiki page or test output. Source and fresh command output are
   authoritative; conversation memory is not.
2. For a change, create `handoff.md` in its change folder; if one already
   exists, overwrite it with the current state. For work that belongs
   to no change, create the handoff at
   `docs/agent-devkit/handoffs/YYYY-MM-DD-<slug>.md`, named per `using-devkit`'s
   `## Shared rules`. Use this structure:

   ```md
   # Handoff: <task>

   ## Objective
   <The user-visible outcome still being pursued>

   ## State
   - Phase: <brainstorm | plan | implement | debug | verify | document>
   - Current task: <first `tasks.md` task not `done`, or none>
   - Approval: <`tasks.md` gate status | Bounded design approved YYYY-MM-DD — <one-line design> | none>
   - Status: <what is complete and what is in progress>

   ## Decisions
   - <D<n> summary and source artifact link, or None>

   ## Evidence
   - `<command>` — <result and exit status>

   ## Changed files
   - `<path>` — <why it changed, or "user change">

   ## Remaining work
   - <smallest next actions, in order>

   ## Risks and blockers
   - <known issue or "None">

   ## Next action
   <The first concrete action for the next session>
   ```

3. Keep the checkpoint factual and short. Do not claim a test, build, link, or
   requirement passes without fresh evidence. Do not copy secrets or full
   logs; record the command and relevant result instead.
4. For a standalone handoff, if `docs/agent-devkit/INDEX.md` exists, add it
   under a `## Handoffs` section. A change's `handoff.md` needs no separate
   entry; the change folder's own index entry covers it. Do not create a second
   index.
5. Run `git diff --check` and read the created checkpoint before stopping.

## Git safety

Working-tree changes and untracked notes are user-owned. A request to clean up,
reset, or "discard whatever is lying around" does not authorize `git reset
--hard`, `git clean`, `git checkout -- <path>`, `git stash`, or deleting files.
A copy or stash first does not change that. List what would be lost, ask which
exact paths and command the user approves, and stop until they answer.

## Resume

At the start of the next session, find the handoff in `docs/agent-devkit/changes/*/handoff.md`
and `docs/agent-devkit/handoffs/`, excluding `changes/archive/`; `memory_recall`
(1–3 keywords, `maxTokens` when supported) may point to it, but memory is only a
pointer. Read the newest relevant handoff and every linked decision source, verify
`git status --short`, re-check claimed source paths and commands, and continue
from `## Next action`. If source or the working tree disagrees, trust the
repository and update the handoff before proceeding. When the resume stops for the
user, end with the `Next:` block from `using-devkit`.
