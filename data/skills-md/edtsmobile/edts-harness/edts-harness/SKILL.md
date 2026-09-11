---
name: edts-harness
description: >-
  Generate, run, and audit a reliability harness for AI coding agents in any repo — frontend,
  backend, or mobile. Use when setting up a new or existing project for agent work, when
  running a work session with the harness loop (session start, verify, handoff, feature
  tracking), or when auditing harness health. Triggers: "edts-harness", "setup harness",
  "create harness", "start session", "end session", "audit harness", or any work on
  AGENTS.md / CONSTITUTION.md / FEATURES.md / state files.
license: MIT
---

# edts-harness

Scaffold and maintain the files that make a coding agent reliable across sessions: consistent
startup, enforced scope, evidence before "done", and clean handoff.

Agent-agnostic: generates `AGENTS.md` with `CLAUDE.md` as a pointer; all attribution comes
from `git config user.name`, never from the agent.

## Modes

| Mode | When | Reference |
|---|---|---|
| **create** | Repo has no harness, or is missing files | [references/create.md](references/create.md) |
| **migrate** | Repo already has a harness (any flavour) | [references/migrate.md](references/migrate.md) |
| **loop** | Any working session in a harnessed repo | [references/loop.md](references/loop.md) |
| **audit** | Explicit request only — never run on your own initiative | [references/audit.md](references/audit.md) |

Pick the mode from intent, then load only that reference.

## Profiles

| Profile | Files | For |
|---|---|---|
| `lite` | AGENTS (rules inline), one state file, verify.sh | Small / solo / short-lived |
| `standard` | + CONSTITUTION, FEATURES, archive/ | Default |
| `full` | + JOURNAL, evaluator-rubric | Long-running, multi-person |

Default to `standard`. Offer `lite` when the repo is small and has no test tooling.

## Invariants (all modes)

- **Never overwrite blindly.** Existing `AGENTS.md` / `CONSTITUTION.md` / `FEATURES.md` are
  modified in place, preserving user content. Report what changed.
- **Never generate alongside an existing harness.** `create` refuses and prints a migration
  plan. Two competing instruction files means the agent follows the old one and never sees the
  new harness — a silent, total failure. Migrate instead; nothing gets deleted.
- **Never auto-commit.** Update files, report, let the user decide.
- **Never invent verification.** Only list checks the project actually has — detect them from
  manifests and probes. A check that can't run is worse than no check.
- **Never leave a `{{PLACEHOLDER}}`** in generated output.
- **Attribution comes from `git config user.name`.** If unset, ask once and suggest setting it.
- **One feature active at a time, per person.** Out-of-scope ideas become new `FEATURES.md`
  rows, never drive-by edits.
- **Evidence before done.** No feature reaches ✅ without a recorded, runnable proof.

## File ownership (do not blur these)

| File | Owns | Never contains |
|---|---|---|
| `AGENTS.md` | How to work — startup, verification, done criteria | Rules (points to CONSTITUTION) |
| `CONSTITUTION.md` | Every rule + dated decisions | Session state |
| `FEATURES.md` | Team scope: epics, dependencies, `By`, evidence | Personal working notes |
| `state/<name>.md` | One person's current task | Anyone else's work |
| `archive/` | Closed features & sessions | Anything still active |

## Hot vs cold

Hot files are read every session and must stay small — `state/<name>.md` capped ~100 lines,
`AGENTS.md` ~80. When work closes, rotate its detail into `archive/` and leave a link.
`archive/` and `JOURNAL.md` are grepped on demand, never loaded whole; their size is free.

## Templates and profiles

- Templates: [templates/](templates/) — one per generated file.
- Stack profiles: [profiles/](profiles/) — detection, probe commands, verify commands, and
  known pitfalls per stack. Adding a stack means adding one file, not editing code.
- Rotation procedure: [references/rotation.md](references/rotation.md) — how closed features,
  sessions and epics move into `archive/`. This is what keeps the hot files flat.
