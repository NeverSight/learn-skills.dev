---
name: init
description: Use when the user asks to set up, bootstrap, or resume setting up a context-routing workspace in a repository, for example "turn this repo into a context-routing workspace". Runs a phased, resumable bootstrap. Not for adding one module to an existing workspace (use add-module) and not for routine work in a finished workspace.
---

# Init

Turns the current repository into a workspace where every task starts from
a small, predictable set of files: rules in `AGENTS.md`, a module registry
in `modules.md`, curated knowledge pages per module, and a newest-first
session log that lets the next session resume.

## Ground rules

- The repository's code and documents are read-only inputs. Never move,
  rename, or edit them.
- Never overwrite an existing file. Keep the existing one and list it as
  skipped in the phase report.
- Lines marked **ASK** need the user's answer. Never answer them yourself.
  If the user already answered in this conversation, use that answer and
  say so.
- Finish a phase, record it, then start the next. Any recorded phase is a
  safe place to stop.

## Find the current phase

1. If root `session_state.md` exists, read it only down to the first line
   that equals `<!-- AGENT-SESSION-STOP -->`.
2. If that latest entry is titled `init phase 0 started`, repeat phase 0
   (it skips files that exist, so repeating is safe). If it is titled
   `init phase N complete` and N is below 5, continue with phase N+1.
3. Otherwise, if `AGENTS.md` and `modules.md` both exist, the workspace
   is already set up: read `references/upgrade.md` and bring it up to
   date. It ends early when nothing needs to change.
4. Otherwise start at phase 0.

## Phases

Read only the reference file for the phase you are in.

| Phase | Read | Produces |
|---|---|---|
| 0 | `references/phase-0-copy.md` | skeleton copied |
| 1 | `references/phase-1-spine.md` | rules file, capability profile, entry point |
| 2 | `references/phase-2-idea.md` | confirmed `idea.md` |
| 3 | `references/phase-3-modules.md` | modules registered |
| 4 | `references/phase-4-intake.md` | raw material indexed, inventories written |
| 5 | `references/phase-5-verify.md` | verification report |
| upgrade | `references/upgrade.md` | existing workspace brought up to date |

## Record each phase

Insert a new entry at the top of root `session_state.md`:

```
## YYYY-MM-DD - init phase N complete
- Last active module: `<module, or none>`.
- Workspace docs: <what this phase produced; skipped files>.
- Verification: <what you checked>.
- Next useful action: init phase N+1 (<phase name>).
<!-- AGENT-SESSION-STOP -->
```

If you can see your context usage and it is above half, record the current
phase and suggest a fresh session; the next session resumes from the log.
