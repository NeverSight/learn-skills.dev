---
name: ghpm-work
description: "End-to-end work session on a GitHub Project item. Setup → Clarify → Plan → Implement → PR, with decisions captured throughout. Use when starting work on an issue, picking up a task, or resuming an interrupted session."
argument-hint: "<issue-number>"
allowed-tools: Bash(gh:*), Bash(git:*), Read, Write, Edit, Grep, Glob
---

# ghpm-work

> **PREREQUISITE:** Read `../ghpm-shared/SKILL.md` for prerequisites and error handling.

End-to-end workflow for a GitHub Project item. `/ghpm-work <issue-number>` drives the full lifecycle.

If no argument, ask for the issue number.

## Flow

```
Setup → Clarify → Plan → Implementation Plan → Implement → Draft PR
                    ↕ decisions captured at every phase ↕
```

| Phase | Reference | What happens |
|-------|-----------|-------------|
| 1. Setup | `references/setup.md` | Resolve item, assign, branch, status sync, write session |
| 2. Clarify | `references/clarify.md` | Evaluate issue clarity, flesh out if needed, gather context |
| 3. Plan | `references/plan.md` | Explore codebase, draft approach, post as issue comment |
| 4. Impl Plan | `references/implementation-plan.md` | Concrete steps, files, tests — post as issue comment |
| 5. Implement | `references/implement.md` | Execute plan, write code, commit, verify |
| 6. Draft PR | `references/draft-pr.md` | Create draft PR with summary |

**Decisions**: See `references/decisions.md`. Capture at ANY phase — not just coding. Watch every interaction for choices worth recording.

**Wrap up**: See `references/wrap-up.md`. Triggered by "wrap up" or "done".

## Session Resume

Sessions track `phase` in `.ghpm/sessions/<number>.json` (schema in `../ghpm-shared/references/session.md`).

Each phase writes its `phase` value to the session file **on entry, before doing any work**. This means on resume, re-run the recorded phase (it may have been interrupted):

| `phase` | Resume from |
|---------|-------------|
| missing/`setup` | Clarify (setup completed, phase field not yet added) |
| `clarify` | Clarify |
| `plan` | Plan |
| `implementation_plan` | Implementation Plan |
| `implement` | Implement |
| `pr` | Draft PR |
| `done` | Session complete — inform user and stop |

On resume, briefly show what's already done before continuing.

## Prompt Configuration

Per `../ghpm-shared/references/prompts.md`. This skill's config lives at `prompts.ghpm-work` in `.ghpm/config.json`.

Action keys: `status_sync`, `clarify_issue`, `post_plan`, `post_impl_plan`, `draft_pr`, `record_decision`.

## Rules

- Each phase updates `"phase"` in the session file **on entry, before doing any work**. This is critical for crash recovery.
- The user can say "skip" to skip any phase.
- Multiple sessions can run in parallel on different branches.
- Restarting Claude on the same branch auto-resumes via session detection.

## See Also

- [ghpm-shared](../ghpm-shared/SKILL.md) — Prerequisites and error handling
- [ghpm-status](../ghpm-status/SKILL.md) — Project health dashboard
- [ghpm-suggest](../ghpm-suggest/SKILL.md) — Find what to work on next
- [ghpm-view](../ghpm-view/SKILL.md) — Query project items
