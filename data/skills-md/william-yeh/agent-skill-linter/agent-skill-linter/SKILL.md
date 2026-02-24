---
name: agent-skill-linter
description: >
  Lint agent skills for spec compliance and publishing readiness.
  Checks SKILL.md frontmatter, LICENSE, README badges, CI workflow,
  installation/usage sections, content dedup, and body length.
  Auto-fixes common issues with --fix.
metadata:
  author: William Yeh <william.pjyeh@gmail.com>
  license: Apache-2.0
  version: 0.3.0
---

# Agent Skill Linter

A linter that checks agent skills for spec compliance and publishing readiness.

## What it checks

1. **SKILL.md spec compliance** — delegates to `skills-ref` for frontmatter validation
2. **LICENSE** — exists, Apache-2.0 or MIT, current year
3. **Author** — `metadata.author` in SKILL.md frontmatter
4. **README badges** — CI, license, Agent Skills badges
5. **CI workflow** — `.github/workflows/` has at least one YAML workflow
6. **Installation section** — README has install instructions with `npx skills` and agent directory table
7. **Usage section** — README has usage examples with starter prompts
8. **Content dedup** — flags heavy overlap between README.md and SKILL.md
9. **Body length** — SKILL.md body under 500 lines
10. **Directory structure** — flags non-standard directories

## Running

```bash
skill-lint check ./my-skill          # Lint a skill directory
skill-lint check ./my-skill --fix    # Auto-fix fixable issues
skill-lint check ./my-skill --format json  # JSON output for CI
```

Exit code 1 on errors, 0 otherwise.

## Templates

### Installation section (for README.md)

When fixing a missing or incomplete Installation section, use this template (replace `{owner}/{repo}` with the actual GitHub slug):

````markdown
## Installation

### Recommended: `npx skills`

```bash
npx skills add {owner}/{repo}
```

### Manual installation

Copy the skill directory to your agent's skill folder:

| Agent | Directory |
|-------|-----------|
| Claude Code | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` |
| Gemini CLI | `.gemini/skills/` |
| Amp | `.amp/skills/` |
| Roo Code | `.roo/skills/` |
| Copilot | `.github/skills/` |

### As a CLI tool

```bash
uv tool install git+https://github.com/{owner}/{repo}
```
````
