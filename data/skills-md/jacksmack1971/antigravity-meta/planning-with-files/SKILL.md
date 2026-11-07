---
name: planning-with-files
description: >
  Provides Manus-style persistent planning memory across sessions using three
  filesystem files: task_plan.md (phased execution plan), findings.md
  (research and decisions log), progress.md (session timeline and error log).
  Use when activating /plan, starting a GSD task requiring 5+ tool calls, or
  resuming after context loss. Hooks fire automatically — no manual invocation
  needed during normal GSD execution. Trigger words: /plan, task_plan, persistent
  planning, session recovery, plan resume, goal drift, context loss.
version: "1.0.0"
source: integrated
---

# planning-with-files

## The Three Files

| File | Purpose | Written by |
|------|---------|------------|
| `task_plan.md` | Phased execution plan with step status | Agent at PLAN phase |
| `findings.md` | Research, decisions, external content ONLY | Agent (2-Action Rule) |
| `progress.md` | Session log, errors, test results | Agent (AfterTool hook) |

## Critical Constraint (Rule G-9)
`task_plan.md` is injected into context before EVERY tool call (BeforeTool hook).
Never write external fetched content here. External content → `findings.md` only.

## Scripts

| Script | Purpose | Runtime |
|--------|---------|---------|
| [init-session.sh](file:///agents/skills/planning-with-files/scripts/init-session.sh) | Bootstrap task_plan.md from SPEC.md (idempotent) | Bash |
| [init-session.ps1](file:///agents/skills/planning-with-files/scripts/init-session.ps1) | Same — Windows runtime | PowerShell |
| [session-catchup.py](file:///agents/skills/planning-with-files/scripts/session-catchup.py) | Emit structured session status on startup | Python 3 |
| [session-catchup.ps1](file:///agents/skills/planning-with-files/scripts/session-catchup.ps1) | Same — Windows fallback | PowerShell |
| [check-complete.sh](file:///agents/skills/planning-with-files/scripts/check-complete.sh) | Validate all phases complete before commit | Bash |
| [check-complete.ps1](file:///agents/skills/planning-with-files/scripts/check-complete.ps1) | Same — Windows runtime | PowerShell |

## Extended GSD Workflow
See [gsd-with-persistent-planning.md](file:///agents/workflows/gsd-with-persistent-planning.md)
