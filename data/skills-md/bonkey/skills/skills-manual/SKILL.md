---
name: skills-manual
description: "Guidelines for creating well-structured AI agent skills. Use when building a new skill, reviewing skill quality, or unsure how to organize a skill."
---

# Skills Manual

How to build effective skills for AI coding agents. For the full Anthropic guide, see `references/skill-builder-guide.md`.

## Skill Structure

```
your-skill-name/              # kebab-case, no spaces, no capitals, no underscores
  SKILL.md                    # Required — must be exactly this name (case-sensitive)
  references/                 # Optional — supporting docs loaded on demand
  scripts/                    # Optional — executable code
  assets/                     # Optional — templates, icons
```

- The main file MUST be named `SKILL.md` — not `skill.md`, `SKILL.MD`, or anything else
- Do NOT include `README.md` inside the skill folder
- Folder name must be kebab-case (e.g., `notion-project-setup`)

## YAML Frontmatter

```yaml
---
name: your-skill-name                     # Required — kebab-case, must match folder name
description: "What and when."             # Required — max 1024 chars, no < > brackets
license: MIT                              # Optional
allowed-tools: "Bash(python:*) WebFetch"  # Optional — restrict tool access
metadata:                                 # Optional
  author: Name
  version: 1.0.0
---
```

### Security Restrictions

- No XML angle brackets (`<` `>`) in frontmatter — it appears in system prompt
- No "claude" or "anthropic" in skill names (reserved)

## Writing the Description

The description is the most important field. It controls when the skill gets loaded via progressive disclosure:

1. **Frontmatter** (always loaded) — Claude reads the description to decide relevance
2. **SKILL.md body** (loaded when relevant) — full instructions
3. **Linked files** (loaded on demand) — references, scripts, assets

The description MUST include both:
- **What** the skill does
- **When** to use it — specific trigger phrases users would actually say

Good:
```yaml
description: "Manages Linear project workflows including sprint planning,
  task creation, and status tracking. Use when user mentions 'sprint',
  'Linear tasks', 'project planning', or asks to 'create tickets'."
```

Bad:
```yaml
description: "Helps with projects."
```

To debug: ask Claude "When would you use the [skill name] skill?" — it will quote the description back, revealing what's missing.

## Writing Instructions

### Structure

```markdown
---
name: your-skill
description: [...]
---

# Skill Name

## Instructions
Step-by-step workflow with clear actions.

## Examples
Common scenarios with expected inputs/outputs.

## Troubleshooting
Common errors, causes, and fixes.
```

### Rules

- Lead with the most important rules
- Be specific — include commands, file paths, expected outputs
- Use numbered steps for sequential workflows, bullet points for guidelines
- Show examples of correct and incorrect usage
- Include error handling for common failures
- Reference bundled files explicitly (e.g., "see `references/api-guide.md`")
- Keep SKILL.md under 5,000 words — move detailed docs to `references/`
- Composability — assume other skills may be loaded simultaneously

## Iteration Signals

| Signal | Meaning | Fix |
|--------|---------|-----|
| Skill doesn't load when it should | Undertriggering | Add more trigger phrases and keywords to description |
| Skill loads for unrelated queries | Overtriggering | Add negative triggers, narrow scope |
| Claude doesn't follow instructions | Too verbose or ambiguous | Use bullet points, be explicit, move detail to references |
| Inconsistent results | Missing examples or validation | Add examples, error handling, quality checks |
