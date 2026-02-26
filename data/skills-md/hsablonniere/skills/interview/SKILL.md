---
name: interview
description: Interview the user to deeply explore an idea, feature, or problem through Q&A. Use when the user asks to be interviewed, wants to think through something, or needs help clarifying a concept.
argument-hint: [what you want to explore]
model: opus
allowed-tools: AskUserQuestion, Read
---

<!-- Inspired by https://github.com/PierreZ/claude-personal-skills/blob/main/skills/spec-interview/SKILL.md -->

# Interview

Read what the user wants to explore: <topic>$ARGUMENTS</topic>

Interview the user in depth using AskUserQuestion. Adapt the questions to the topic — this could be a feature, an architecture decision, a process, a problem to solve, or any idea worth exploring.

Dig into:
- Goals and constraints
- Tradeoffs and alternatives considered
- Edge cases and unknowns
- Non-obvious decisions
- Anything that seems underspecified

Don't ask surface-level questions — challenge assumptions and explore the hard parts.

Keep interviewing until the user says "done" or signals they're ready to move on. Do not stop early.

When the interview is over, provide a concise summary of what was clarified, then let the user decide the next step (plan mode, implementation, write a doc, etc.).
