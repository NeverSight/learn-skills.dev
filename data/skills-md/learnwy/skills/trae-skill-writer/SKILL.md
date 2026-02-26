---
name: trae-skill-writer
description: "Create Trae IDE skills (SKILL.md files) for reusable AI capabilities. Use when user wants to: create a skill, make a reusable workflow, automate repetitive tasks, turn a conversation into a skill, or encapsulate a process for AI to follow. Triggers on: '创建 skill', 'write a SKILL.md', 'make this reusable', '.trae/skills/', 'I keep doing the same thing every time'. Do NOT use for rules (use trae-rules-writer) or agents (use trae-agent-writer)."
---

# Trae Skill Writer

Create Trae IDE skills by analyzing project patterns first, then designing skills that automate real workflows.

## Workflow

```
1. ANALYZE  → Scan project for repetitive patterns (ls scripts/, .trae/skills/)
2. IDENTIFY → What workflows need automation?
3. DESIGN   → Structure skill for on-demand loading
4. CREATE   → Write SKILL.md with clear triggers
```

## Skill Structure

```
skill-name/
├── SKILL.md               # Required - Core instructions (<500 lines)
├── scripts/               # Optional - Executable automation
├── references/            # Optional - Detailed docs (loaded on-demand)
└── assets/                # Optional - Templates, files for output
```

## SKILL.md Format

```markdown
---
name: skill-name
description: What it does. When to use. Trigger phrases. Do NOT use for X.
---

# Skill Name

Brief intro.

## Workflow

[Steps or flowchart]

## Quick Reference

[Tables, commands]

## References

- [doc.md](references/doc.md) - When to read
```

**Description is the primary trigger mechanism.** Include:
- What the skill does
- When to use it (specific phrases)
- When NOT to use it

## Skill Types

| Type    | Location            | Scope           |
| ------- | ------------------- | --------------- |
| Global  | `~/.trae/skills/`   | All projects    |
| Project | `.trae/skills/`     | Current project |

## Good Skill Candidates

- Multi-step workflows (code review, deployment)
- Complex domain logic (order processing, pricing)
- Repetitive tasks (report generation, migrations)
- Tool integration (database setup, test running)

**Don't make skills for:** Simple one-step tasks, generic AI knowledge, continuous constraints (use rules instead).

## Example

```
User: "Create a skill for our code review process"

Analysis:
- Found: scripts/lint.sh, .github/workflows/ci.yml
- Workflow: lint → test → review checklist

Creating: .trae/skills/code-review/SKILL.md

---
name: code-review
description: Code review for this project. Use when reviewing PRs or checking code quality. Triggers on 'review', 'PR', 'check this code'.
---

# Code Review

1. Run linter: `npm run lint`
2. Run tests: `npm test`
3. Check review checklist

## Checklist

- [ ] No TypeScript errors
- [ ] Tests pass
- [ ] No console.log in production
```

## References

- [Advanced Patterns](references/advanced-patterns.md) - Multi-variant skills, domain organization
- [Skill Template](assets/skill.md.template) - Starter template
