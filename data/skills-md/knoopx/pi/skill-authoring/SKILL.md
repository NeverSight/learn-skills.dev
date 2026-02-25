---
name: skill-authoring
description: Writes effective pi skills with proper structure, concise content, and progressive disclosure. Use when creating new skills, improving existing skills, or reviewing skill quality.
---

# Skill Authoring Best Practices

Use this skill when you need to create or refactor a pi skill. Keep it short and defer to the canonical reference for full rules and examples.

## Canonical Reference

Follow the full specification and patterns here:

- `agent/skills/pi/references/skills.md`

Only repeat details in this file when they are essential to the current task.

## Authoring Workflow (Condensed)

1. **Clarify scope**: Identify what the skill should do and the trigger phrases that should load it.
2. **Plan resources**: Decide which logic belongs in scripts, references, or assets instead of SKILL.md.
3. **Write the skill**: Add frontmatter, concise instructions, and links to references (one level deep).
4. **Validate and iterate**: Use the skill on real tasks, note friction, and tighten wording.

## Content Placement Heuristics

- **SKILL.md**: Overview, decision points, and minimal instructions.
- **references/**: Deep guides, specs, or domain docs the agent should read on demand.
- **scripts/**: Deterministic code you don’t want rewritten every time.
- **assets/**: Files used in outputs (templates, logos, etc.).

## Red Flags

- Duplicate information between SKILL.md and references.
- Long explanations of obvious concepts.
- Extra docs (README, changelog) that won’t be used by the agent.
