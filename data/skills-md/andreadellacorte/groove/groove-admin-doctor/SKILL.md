---
name: groove-admin-doctor
description: "Run all groove health checks: config, backends, companions, AGENTS.md."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(beans:*) Bash(gh:*) Bash(linear:*) Bash(npx:*) Bash(mkdir:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

<!-- groove:managed — do not edit; changes will be overwritten by groove update -->

# groove-admin-doctor

## Outcome

All groove sub-skill health checks are run and a consolidated summary is reported. User knows exactly what is working, what is misconfigured, and what action to take for any failure.

## Acceptance Criteria

- `/groove-utilities-task-doctor` and `/groove-utilities-memory-doctor` are run
- Companion skill presence is checked directly
- Results are shown per sub-skill with pass/fail per check
- Overall status is shown: all healthy, or N issues found
- Each failure includes a specific remediation action

## Output format

```
groove doctor
─────────────────────────────────────
groove
  ✓ git repo: detected
  ✓ groove-version: 0.1.0
  ✓ installed version: 0.1.0
  ✓ up to date

task
  ✓ .groove/index.md present
  ✓ tasks: beans
  ✓ beans installed (v0.x.x)
  ✓ .beans.yml present
  ✓ beans reachable

memory
  ✓ memory path exists (.groove/memory/)
  ✓ memory dirs exist (.groove/memory/daily/, weekly/, monthly/, git/)

companions
  ✓ find-skills installed
  ✓ agent-browser installed
  ✓ pdf-to-markdown installed

AGENTS.md
  ✓ groove:prime section present
  ✗ groove:task section missing — run: /groove-admin-install

─────────────────────────────────────
1 issue found. Run the suggested commands above to fix.
```

## Constraints

- Run git repo check first, then version check, then `/groove-utilities-task-doctor`, `/groove-utilities-memory-doctor`, companions check in sequence
- Git repo check:
  - Run `git rev-parse --is-inside-work-tree` in the current directory
  - If it succeeds: `✓ git repo: detected`
  - If it fails: `✗ git repo: not a git repository — groove requires a git repo`
- Version check:
  - Read `groove-version:` from `.groove/index.md` (if absent, treat as `0.1.0`)
  - Read `version:` from `skills/groove/SKILL.md`
  - If they differ: `✗ groove-version (<local>) behind installed (<installed>) — run: /groove-admin-update`
- Companions check:
  - Check `ls .agents/skills/find-skills/SKILL.md` — if absent: `✗ find-skills not installed — run: /groove-admin-install`
  - Check `ls .agents/skills/agent-browser/SKILL.md` — if absent: `✗ agent-browser not installed — run: /groove-admin-install`
  - Check `ls .agents/skills/pdf-to-markdown/SKILL.md` — if absent: `✗ pdf-to-markdown not installed — run: /groove-admin-install`
- Also check `AGENTS.md` for presence of `<!-- groove:prime:start -->` and `<!-- groove:task:start -->` sections
- Collect all results before printing — do not interleave output with check progress
- Each `✗` item must include a concrete remediation command on the same line
- Exit with a clear "all healthy" message if no issues found
- Do not attempt to auto-fix issues — report only
