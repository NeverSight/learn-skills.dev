---
name: skill-development
description: Create and contribute skills to the communal knowledge base. Use when creating new skills, updating existing skills, or contributing learnings back to the repository.
license: MIT
---

# Skill Development

Guide for creating effective skills and contributing them to the communal knowledge base.

## When to Use This Skill

**Creating skills:**
- Building a new skill for a specific domain or workflow
- Updating an existing skill with improvements
- Packaging skills for distribution

**Contributing skills:**
- You discovered something that took significant time to figure out
- Existing skill instructions were incomplete or led you astray
- You repeatedly solve the same undocumented problem

---

## Part 1: Creating Skills

### Skill Structure

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/      - Executable code
    ├── references/   - Documentation loaded as needed
    └── assets/       - Files used in output
```

### SKILL.md Requirements

```yaml
---
name: skill-name
description: What this skill does. Use when [triggers]. 
---

# Skill Name

[Instructions in imperative form...]
```

**Metadata rules:**
- `name`: lowercase, hyphens, gerund form (e.g., `creating-skills`)
- `description`: Lead with action verbs, end with "Use when [triggers]"

### Writing Style

Write in **imperative/infinitive form** (verb-first), not second person:
- ✅ "To accomplish X, do Y"
- ❌ "You should do X"

### Progressive Disclosure

Keep SKILL.md lean (<5k words). Move detailed content to `references/`:
1. **Metadata** (~100 words) - Always in context
2. **SKILL.md body** (<5k words) - When skill triggers
3. **References** (unlimited) - Loaded as needed by agent

### Scripts

Include scripts for tasks that:
- Are repeatedly rewritten
- Require deterministic reliability
- Save significant tokens

---

## Part 2: Contributing Skills

### Core Philosophy

This repository is a **living knowledge base**. Skills must contain **general-purpose knowledge** that helps many agents - not project-specific configs or personal preferences.

### What to Contribute

| ✅ Contribute | ❌ Don't Contribute |
|--------------|-------------------|
| Patterns that appear 3+ times | One-off solutions |
| General API/tool patterns | Project-specific configs |
| Battle-tested workarounds | Personal preferences |
| Gap in existing skills | Already documented elsewhere |

### Validation Checklist

Before contributing, verify:
- [ ] Is this generalizable beyond your specific context?
- [ ] Have you seen this pattern multiple times?
- [ ] Does this address a real gap vs. personal preference?
- [ ] Would this help an agent on a completely different project?

### Contribution Process

1. **Recognize** - Notice patterns during work (time investment, repetition, corrections)
2. **Validate** - Confirm pattern is general, not specific to your context
3. **Create branch** - `add/skill-name` or `fix/skill-name`
4. **Submit PR** - Clear description with rationale and evidence

See `references/pr-workflow.md` for detailed PR process.

---

## Scripts

- `scripts/init_skill.py` - Initialize skill directory structure
- `scripts/package_skill.py` - Package skill for distribution
- `scripts/quick_validate.py` - Validate SKILL.md format

## References

- `references/recognizing-learnings.md` - Patterns for spotting valuable learnings
- `references/validation-criteria.md` - Detailed validation guidelines
- `references/pr-workflow.md` - PR process and templates
- `references/contribution-examples.md` - Real contribution examples
- `references/progressive-disclosure-research.md` - Research on skill organization
