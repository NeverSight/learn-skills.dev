---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---

# Writing Skills

## Overview

**Writing skills IS Test-Driven Development applied to process documentation.**

Skills use a 3-tier progressive disclosure model:
1. **Frontmatter** (always loaded, ~30 tokens) -- `name` + `description` only
2. **SKILL.md body** (loaded on trigger, <=150 lines) -- Quick Start, core principles, reference table
3. **`references/`** (loaded on demand, unlimited) -- detailed guides, examples, checklists

This skill demonstrates the pattern it teaches: core workflow here, deep detail in `references/`.

**REQUIRED:** superpowers-bd:test-driven-development, superpowers-bd:rule-of-five-plans

## Quick Start

1. **Confirm need** -- Is this a repeated failure pattern? (Not one-off, not project-specific, not already documented)
2. **Set up** -- `skills/skill-name/SKILL.md` + `references/` directory if content exceeds <=150 line budget
3. **Write frontmatter:**
   ```yaml
   ---
   name: skill-name-with-hyphens
   description: Use when [triggering conditions only, <=300 chars]
   ---
   ```
   **THE TRAP:** Description must be triggering conditions ONLY -- never summarize workflow. Claude will follow the description instead of reading the full skill body.
   ```yaml
   # BAD: Claude follows this shortcut instead of reading the skill
   description: Use when executing plans - dispatches subagent per task with code review between tasks
   # GOOD: Forces Claude to read the skill for workflow details
   description: Use when executing implementation plans with independent tasks in the current session
   ```
4. **RED** -- Run pressure scenarios WITHOUT skill -> document baseline failures and rationalizations verbatim
5. **GREEN** -- Write SKILL.md addressing those specific failures -> verify agents comply with skill present
6. **REFACTOR** -- Close loopholes, build rationalization table, re-test until bulletproof
7. **Validate:**
   ```bash
   npx claude-skills-cli validate <skill-dir> --lenient
   ```
8. **Rule-of-five-plans** if >50 lines -> commit

## SKILL.md Template

```markdown
---
name: skill-name
description: Use when [triggering conditions, symptoms, situations -- NOT workflow]
---

# Skill Name

## Overview
Core principle in 1-2 sentences. What is this and why does it matter?

## Quick Start
Numbered steps: what to do RIGHT NOW.

## [Core Content Section]
The non-negotiable rules, patterns, or techniques.
Keep this focused -- "what do I do now?" belongs here.
"How do I do it well?" belongs in references/.

## Reference Files
| File | When to read |
|------|-------------|
| `references/guide.md` | When you need [specific detail] |

## Common Mistakes
What goes wrong + fixes. Keep to top 3-5.
```

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS to existing skills. No exceptions.

Write skill before testing? Delete it. Start over.
- Don't keep untested changes as "reference"
- Don't "adapt" while running tests
- Delete means delete

## Description Writing

**THE critical discovery:** description = triggering conditions ONLY.

Testing proved that workflow summaries in descriptions cause Claude to skip reading the full skill body. The description is a trigger, not a summary.

- Start with "Use when..." -- third person, <=300 chars
- Describe the *problem* not *language-specific symptoms*
- Include concrete triggers, symptoms, situations
- **NEVER** summarize the skill's process or workflow

Full guide with examples: `references/description-and-discovery.md`

## Reference Files

- `references/3-tier-model.md`: understanding the progressive disclosure model and validation
- `references/skill-structure.md`: directory layout, skill types, frontmatter fields for all components
- `references/description-and-discovery.md`: writing descriptions, CSO, token efficiency, flowcharts, naming
- `references/tdd-for-skills.md`: TDD mapping, phase tasks, RED-GREEN-REFACTOR detail, testing by type
- `references/bulletproofing.md`: rationalization tables, loophole closing, anti-patterns
- `references/creation-checklist.md`: full 40-item checklist, STOP directive, validation step
- `references/anthropic-best-practices.md`: official Anthropic skill authoring guidance
- `references/testing-skills-with-subagents.md`: pressure scenario methodology, meta-testing
- `references/persuasion-principles.md`: psychology research behind bulletproofing (Cialdini, Meincke)
- `references/graphviz-conventions.dot`: Graphviz style rules for flowcharts
- `references/examples/`: worked examples (CLAUDE_MD_TESTING.md)

## Validation

Before committing any skill:

```bash
npx claude-skills-cli validate <skill-dir> --lenient
```

Must pass. Fix errors, address warnings. Checks: body <=150 lines, <=2000 words, valid frontmatter.

<!-- compressed: 2026-02-11, original: 702 words, compressed: 638 words -->
