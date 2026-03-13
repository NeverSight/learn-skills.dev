---
name: beary
description: Topic-to-whitepaper research workflow with citations and configurable depth/attendance modes.
---

# BEARY skill

Before running this skill, read `.agents/skills/beary/AGENTS.md` and follow it.

Summon behavior:
- Use `.agents/skills/beary/scripts/is-beary-summon.sh "<raw user message>"` to detect whether the raw message is exactly `BEARY` (case-insensitive, surrounding spaces ignored).
- If it matches, print `.agents/skills/beary/LOGO.md` first.
- Then continue with the normal BEARY flow (ask setup questions and run `research`).
- If it does not match, continue normally without printing the logo.

Run the command workflow:
- `research`

Core files:
- `LOGO.md`
- `scripts/is-beary-summon.sh`
- `commands/research.md`
- `skills/internet-research/SKILL.md`
- `skills/references/SKILL.md`
- `skills/whitepaper-writing/SKILL.md`
- `skills/user-context-template/SKILL.md`
- `templates/*`

Configure audience/source/output preferences in the host project's `.agents/skills/beary/USER.md` (or equivalent agent profile path).
