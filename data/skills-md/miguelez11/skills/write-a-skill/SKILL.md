---
name: write-a-skill
description: Add a new agent skill to the MIGUELez11/skills personal GitHub repo. Use when the user wants to create a new workflow, process, or reusable capability and publish it to their skills collection.
---

# Add Skill

Creates a new skill in `/Users/miguel.florido/Projects/skills` following skills.sh conventions.

## Repo structure

```
skills/
└── <skill-name>/
    ├── SKILL.md        # Agent instructions (required)
    ├── REFERENCE.md    # Detailed docs (if needed)
    └── scripts/        # Optional helper scripts
```

## Process

1. **Gather requirements** — ask the user:
   - What workflow or task does this skill cover?
   - What specific use cases should it handle?
   - Are helper scripts needed for deterministic operations?
   - Any reference materials to include?

2. **Draft the skill** — create:
   - `skills/<skill-name>/SKILL.md`
   - Additional files if content exceeds 100 lines
   - Utility scripts if deterministic operations needed

3. **Review with user** — present draft and ask:
   - Does this cover your use cases?
   - Anything missing or unclear?
   - Should any section be more/less detailed?

4. **Update README** — add a row to the Available Skills table in `README.md`

5. **Commit** with message: `Add <skill-name> skill`

## SKILL.md Template

```md
---
name: skill-name
description: [What it does]. Use when [specific triggers].
---

# Skill Name

## Quick start
[Minimal working example]

## Workflows
[Step-by-step processes for complex tasks]

## Advanced features
[See REFERENCE.md if needed]
```

## Description rules

- Max 1024 chars, written in third person
- First sentence: what the skill does
- Second sentence: `Use when [triggers]` — be explicit about keywords/contexts
- Bad: `Helps with documents.`
- Good: `Extract markdown documents. Use when user asks to convert or restructure markdown files.`

## When to add scripts

- Operation is deterministic (validation, formatting)
- Same code would be generated repeatedly
- Errors need explicit handling

## When to split files

- SKILL.md exceeds 100 lines
- Content has distinct domains
- Advanced features are rarely needed

## Checklist

- [ ] Description includes "Use when..." with explicit triggers
- [ ] SKILL.md under 100 lines (split to REFERENCE.md if longer)
- [ ] No time-sensitive information
- [ ] Consistent terminology
- [ ] Concrete examples included
- [ ] README Available Skills table updated
- [ ] Committed with `Add <skill-name> skill`
