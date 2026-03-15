---
name: build-a-skill
slug: build-a-skill
description: "Use when creating or modifying a skill: follow SKILL.md rules, define commands and dependencies, validate locally, version correctly, and publish"
version: 1.0.1
author:
  name: askill
  github: askill
tags:
  - official
  - development
  - askill
---

# Build a Skill

Use this skill when creating or updating a skill that must work with askill CLI and registry conventions.

## Authoring Standard

A valid skill requires one entry file:

- `SKILL.md` (required)

Optional supporting files:

- `scripts/` for executable commands
- `assets/` for templates or reference material

Recommended layout:

```text
my-skill/
├── SKILL.md
├── scripts/
│   └── main.js
└── assets/
```

## Minimal SKILL.md Template

```markdown
---
name: my-skill
slug: my-skill
description: One-line purpose of the skill
version: 0.1.0
---

# My Skill

## Overview
What this skill does and when to use it.

## Usage
Step-by-step instructions the agent can execute.
```

## Frontmatter Rules

Required:

- `name` - lowercase letters/numbers/hyphens only
- `description` - concise summary

Strongly recommended:

- `version` - valid semver (`1.0.0`, `1.1.0-beta.1`)
- `slug` - publish identifier (`@author/slug`)

Optional:

- `author`, `tags`, `dependencies`, `commands`, `repository`, `license`

Dependencies format:

- Published: `@author/skill-name` or `@author/skill-name@^1.2.0`
- Indexed GitHub: `gh:owner/repo@skill-name` or `gh:owner/repo/path`

Commands format:

```yaml
commands:
  analyze:
    run: node scripts/analyze.js
    description: Analyze current repository
  _setup:
    run: npm ci
    description: Install command dependencies
```

## Write for Agents, Not Humans

Your markdown body should be executable guidance:

- include clear preconditions
- include exact commands
- include expected outputs/artifacts
- include failure handling and recovery paths

Good instruction pattern:

1. Check prerequisites
2. Run command
3. Verify output
4. Handle common failures

## Development Loop (Local)

Use this loop while building:

```bash
# 1) scaffold
askill init ./my-skill

# 2) validate schema/fields
askill validate ./my-skill/SKILL.md

# 3) install locally for testing
askill add ./my-skill -a claude-code -y

# 4) run commands
askill run my-skill:<command>

# 5) inspect installed state
askill list
```

When iterating quickly, reinstall with `askill add ./my-skill -y` after changes.

## Publish Workflow

Publishing uses `slug` as publish intent.

```bash
askill login --token ask_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
askill whoami
askill publish ./my-skill
```

Alternative (publish from GitHub SKILL.md URL):

```bash
askill publish --github https://github.com/owner/repo/blob/main/path/to/SKILL.md
```

Important:

- `askill publish` requires `name`, `slug`, and valid semver `version`
- local publish uses logged-in user as author
- GitHub URL publish uses repo owner as author (supports org namespace)
- successful publish creates canonical slug `@author/<slug>`
- bump `version` before republishing updates
- `askill submit <github-url>` requests indexing and can trigger slug-driven publish flows

## Quality Checklist Before Release

- `askill validate` passes with no errors
- all documented commands exist in frontmatter
- command descriptions are present and specific
- prerequisites are explicit and testable
- instructions avoid hardcoded agent paths
- at least one end-to-end example is included

## Common Mistakes to Avoid

- vague instructions like "run the script"
- missing `run` or `description` in commands
- undocumented prerequisites (runtime/tooling)
- relying on unpublished assumptions instead of explicit steps
- hardcoding `.claude/skills/...` paths instead of `askill run`

## Maintenance Guidance

For updates:

1. change skill behavior/instructions
2. bump semver in `version`
3. validate locally
4. republish

For breaking changes, increment major version.
