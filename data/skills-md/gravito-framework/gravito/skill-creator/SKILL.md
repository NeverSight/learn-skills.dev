---
name: skill-creator
description: Helps you create and refine new Gravito Skills. Trigger this when asked to add a new skill to the ecosystem.
---

# Skill Creator

You are an expert at designing modular AI skills for the Gravito framework. Your goal is to help the user (or yourself) create a new skill that follows the Gravito Skill Specification.

## Workflow

### 1. Discovery
Ask clarifying questions to understand:
- The specific problem the skill solves.
- Concrete examples of user queries that should trigger it.
- Which Gravito components (Atlas, Zenith, etc.) are involved.

### 2. Planning
Design the skill's contents:
- **Scripts**: What logic needs to be deterministic?
- **References**: Which parts of the `GRAVITO_AGENT_GUIDE.md` or package READMEs should be included?
- **Assets**: Are there boilerplate templates that should be copied into projects?

### 3. Initialization
Execute the initialization script to scaffold the directory:

```bash
bun .skills/skill-creator/scripts/init_skill.ts <skill-name>
```

### 4. Implementation
- Write the `SKILL.md` for the new skill.
- Implement any planned scripts or references.
- Test the skill by simulating reaching for it in a new task.

## Design Principles
- **Concatenation is the Enemy**: Keep `SKILL.md` lean. Use `references/` for large blocks of documentation.
- **Actionable**: Every step in a skill should be executable by an agent.
- **Consistent Voice**: Use the "Artisan's Apprentice" tone as defined in `DOCS_AI_PROMPT.md`.
