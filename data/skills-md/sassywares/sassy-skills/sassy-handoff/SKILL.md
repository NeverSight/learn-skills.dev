---
name: sassy-handoff
description: >-
  Hand work between sessions in any harness. mode:write (default) writes a
  self-contained handoff file under /tmp/sassywares and gives the user a
  command to continue in a fresh session; mode:read takes a handoff file,
  explains what was done, why, and where things stand, then asks what to do
  next. Use at a phase boundary, when context is getting long, when the user
  asks to hand off, or to pick up a handoff file.
argument-hint: "[mode:write|read] [goal for the next session | handoff file path]"
disable-model-invocation: true
---

# Sassy Handoff

**Outcome:** in `write`, a handoff file a fresh session can act on with no access to this one, plus the command that continues from it. In `read`, a grounded summary of that file — what was done, why, and the current state — and the user's choice of what happens next. This skill never starts or replaces a session; the user does.

**Harness.** Commands you hand the user, and the temp-file rules, follow the `sassy-setup` skill's `references/harness.md`.

## Modes

| Mode | Load | It ends with |
|---|---|---|
| `write` (default) | `references/write.md` | a handoff file on disk and the continue command |
| `read` | `references/read.md` | a summary and a question to the user — nothing changed |

Resolve the mode: an explicit `mode:write` or `mode:read` wins. With no mode, an argument that is a path to an existing handoff file is `read`; anything else is `write`. Read the one reference for that mode **and only that one**.

## The handoff file

Written by `write`, parsed by `read`. Files live in `/tmp/sassywares/<harness>/handoffs/`, named `<UTC timestamp>-<kebab-goal>.md`:

```md
# Handoff: <goal in one line>

- **Repo / cwd:** <absolute path> · **Branch:** <branch> @ <short sha> · **Written:** <ISO time>
- **Plan:** <plan path + next phase, or "none — brief below">

## Goal
What the next session must achieve, and its done-when.

## Done
What this session did, and why — the reasoning a reader cannot recover from the diff.

## State
What is finished, in progress, and untouched. Uncommitted work, if any, named by path.

## Decisions
Settled choices (`D1: …`) with the reason, so the next session does not reopen them.

## Key files
`path:line` — why it matters. Pointers, not contents.

## Next steps
1. The first concrete action, including the exact skill invocation when one applies.

## Open questions and risks
Anything unresolved, and anything the next session must not do.
```

## Rules

- **Pointer-first.** Plan paths, phases, files, and decisions are named, not reproduced. The plan is the source of truth; the file points at it.
- **Outside the repo.** Handoff files live under `/tmp/sassywares/` only — never committed, never inside the working tree.
- **No secrets.** A handoff file never carries credentials, tokens, or unrelated personal data, and `read` never echoes one.
- **The skill does not switch sessions.** Never claim it did.
