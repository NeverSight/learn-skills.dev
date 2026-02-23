---
name: skill-creator
description: Create new Claude Code skills with proper structure, YAML frontmatter, and best practices. Use when creating reusable knowledge modules, adding specialized guidance, or building domain-specific expertise.
---

# Skill Creator

Create new Claude Code skills following the official format and best practices.

## Quick Reference

- **[Structure Guide](structure.md)** - Directory format and file organization
- **[Naming Rules](naming.md)** - Skill naming requirements
- **[Description Guide](description.md)** - Writing effective descriptions
- **[Templates](templates.md)** - Process, knowledge, and tool skill templates
- **[Examples](examples.md)** - Complete skill creation walkthroughs
- **[Validation](validation.md)** - Commands to validate new skills

## When to Use

- Creating a new reusable knowledge module
- Adding specialized guidance for specific tasks
- Building domain-specific expertise into Claude Code
- Need to ensure proper skill format and structure

## Required SKILL.md Format

Every skill requires a `SKILL.md` file with two parts:

1. **YAML frontmatter** (metadata between `---` markers on line 1)
2. **Markdown instructions** (guidance for Claude)

```markdown
---
name: skill-name
description: Brief description of what this skill does and when to use it
---

# Skill Title

## Instructions
Step-by-step guidance for Claude...
```

## YAML Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase letters, numbers, hyphens only (max 64 chars). Must match directory name. |
| `description` | Yes | What the skill does and when to use it (max 1024 chars). Claude uses this to match requests. |
| `allowed-tools` | No | Tools Claude can use without permission |
| `model` | No | Specific model to use |
| `context` | No | Set to `fork` for isolated sub-agent context |

## File Structure

```
skill-name/
├── SKILL.md              # Required - overview and navigation
├── reference.md          # Detailed docs - loaded when needed
├── examples.md           # Usage examples - loaded when needed
└── scripts/
    └── helper.sh         # Utility script - executed, not loaded
```

## Best Practices

- **Keep SKILL.md under 250 lines** - Use progressive disclosure
- **Write specific descriptions** - Include trigger terms users would naturally use
- **Link supporting files** - From SKILL.md using markdown links
- **Validate structure** - Check YAML syntax and file organization

See **[naming.md](naming.md)** for naming conventions and **[templates.md](templates.md)** for ready-to-use templates.
