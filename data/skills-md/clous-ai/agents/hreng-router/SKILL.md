---
name: hreng-router
description: Command and skill mapping for the clous-hreng plugin; use when deciding which /clous command or skill to use for hiring, performance, onboarding, burnout, skills, ladder, 1:1, or offboard.
version: 1.0.0
license: MIT
---

# When to Use What (clous-hreng)

Single reference for command ↔ skill mapping. Prefer the command when the user intent matches; invoke the skill from the command or when the user asks for the capability without naming the command.

**Source of truth:** This table should be updated when commands (under `commands/`) or agents change. Each command should have a corresponding file in `commands/`; skills are invoked by name. This skill produces no artifacts (templates folder is placeholder).

## Hiring

| Intent | Command | Skill / agent |
|--------|---------|----------------|
| Define role, requirements, intake | `/clous:intake` | hreng-hire-intake |
| Evaluate candidate packet / rubric / assessment | `/clous:eval` | hreng-hire-eval |
| Full hiring flow (intake → interviews → eval) | — | hreng-hiring agent |

## Performance & health

| Intent | Command | Skill / agent |
|--------|---------|----------------|
| Diagnose performance (person/team) | `/clous:perf-diagnose` | hreng-perf-diagnose |
| Assess burnout risk | `/clous:burnout` | hreng-burnout |
| Full team health (burnout + perf + skills) | `/clous:health-check` | hreng-burnout, hreng-perf-diagnose, hreng-skills |
| PIP or feedback round | `/clous:pip`, `/clous:feedback-round` | hreng-perf-diagnose (context) |
| Promotion / review packet | `/clous:review-packet` | hreng-ladder |

## Skills & ladder

| Intent | Command | Skill |
|--------|---------|--------|
| Skills matrix or gap analysis | `/clous:skills-gap` | hreng-skills |
| Define/update ladder, level definitions | `/clous:ladder` | hreng-ladder |

## Lifecycle

| Intent | Command | Skill |
|--------|---------|--------|
| 30/60/90 onboarding | `/clous:onboard` | hreng-onboard-306090 |
| 1:1 prep (agenda, talking points) | `/clous:1-1-prep` | hreng-1-1-prep |
| Exit checklist, handoff, offboard | `/clous:offboard` | hreng-offboard |

## Quick rule

- **Single-purpose** (eval, burnout, skills-gap, perf-diagnose, ladder) → use the matching command; it invokes the skill.
- **Multi-step or agent-led** (full hiring, full health-check) → use the agent or health-check command.
- **Lifecycle** (onboard, 1:1-prep, offboard) → use the command; it invokes the skill.
