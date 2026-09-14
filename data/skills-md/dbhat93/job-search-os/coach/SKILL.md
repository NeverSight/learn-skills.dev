---
name: coach
description: >
  Interview coaching system. Activates for any coaching command: prep, round, sync, strategy, stories, mock, outreach, thankyou, analyze, progress, practice, research, decode, fit, apply, feedback, reflect, salary, negotiate, hype, pitch, resume, linkedin, present.
metadata:
  author: dbhat93
  version: "4.3"
  license: MIT
---

The interview coaching system is now active.

**Base directory**: ${CLAUDE_SKILL_DIR}
**Coaching state**: ${CLAUDE_SKILL_DIR}/coaching_state.md
**Storybank**: ${CLAUDE_SKILL_DIR}/storybank.md (story index; read it only when a command needs story evidence)

When loading any reference file (e.g. `references/commands/prep.md`), resolve it as an absolute path under `${CLAUDE_SKILL_DIR}/`.

!`cat ${CLAUDE_SKILL_DIR}/COACH.md`
