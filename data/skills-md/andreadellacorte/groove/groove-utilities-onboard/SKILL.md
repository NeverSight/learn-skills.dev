---
name: groove-utilities-onboard
description: "Generate a GROOVE.md onboarding guide for contributors to a groove-enabled project. Explains the compound loop, commands, and conventions."
license: MIT
allowed-tools: Read Write Edit Glob AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-utilities-onboard

Generate a `GROOVE.md` file at the project root — a concise onboarding guide for contributors joining a project that uses groove. Also optionally appends a groove section to `CONTRIBUTING.md` if it exists.

## Outcome

New contributors understand how groove works in this project: which commands to run, where logs live, and what the compound loop expects of them.

## Acceptance Criteria

- `GROOVE.md` exists at the project root with project-specific config values substituted
- If `CONTRIBUTING.md` exists, it contains a "## Using groove" section linking to `GROOVE.md`
- Content reflects actual configured values (task backend, git strategy)

## Steps

1. Read `tasks.backend`, `memory.review_days`, `git.*` from `.groove/index.md`; memory is always `.groove/memory/`, specs is always `.groove/memory/specs/`
2. Ask: "Any project-specific context to include? (e.g. which tasks to pick up, team conventions) — enter to skip"
3. Write `GROOVE.md` from the template below, substituting live config values
4. If `CONTRIBUTING.md` exists and does not already contain `<!-- groove:onboard -->`:
   - Append the following section:
     ```markdown
     <!-- groove:onboard -->
     ## Using groove
     This project uses [groove](https://github.com/andreadellacorte/groove) for AI-assisted engineering workflow. See [GROOVE.md](./GROOVE.md) for setup and commands.
     <!-- groove:onboard:end -->
     ```
5. Report: "GROOVE.md written" and whether CONTRIBUTING.md was updated

## GROOVE.md template

```markdown
# Groove Workflow

This project uses [groove](https://github.com/andreadellacorte/groove) — an AI-assisted engineering workflow companion.

## Quick start

```bash
npx skills add andreadellacorte/groove
/groove-admin-install
```

Then start every session with:
```
/groove-utilities-prime
```

## Daily workflow

```
/groove-daily-start     — review yesterday, load tasks, set agenda
/groove-daily-end       — write memory, commit logs
```

## Compound loop (for any feature or fix)

```
/groove-work-brainstorm — clarify scope
/groove-work-plan       — research and plan
/groove-work-exec       — implement
/groove-work-review     — evaluate output
/groove-work-compound   — capture lessons
```

## Config

| Key | Value |
|---|---|
| Task backend | `<tasks.backend>` |
| Memory path | `.groove/memory/` |
| Specs path | `.groove/memory/specs/` |
| Git strategy (memory) | `<git.memory>` |

## Conventions

- Stage tasks are named `YYYY-MM-DD, <Stage>` — no numbers
- Task completion requires a "Summary of Changes" in the task body before marking done
- Archive is always user-triggered — never automatic

## Where things live

- **Config**: `.groove/index.md`
- **Daily logs**: `.groove/memory/daily/`
- **Learned insights**: `.groove/memory/learned/`
- **Specs**: `.groove/memory/specs/`
- **Hooks**: `.groove/hooks/` (start.md, end.md)

<custom-context>
</custom-context>
```

## Constraints

- Read `.groove/index.md` and substitute all placeholder values before writing
- If `GROOVE.md` already exists: ask "GROOVE.md exists — overwrite, update, or skip?" before touching it
- The `<custom-context>` block is replaced with user-provided context or removed if none
- Do not create `CONTRIBUTING.md` if it doesn't exist — only append to existing files
- `GROOVE.md` should be short enough to read in 2 minutes
