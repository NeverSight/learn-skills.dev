---
name: agents-md-best-practices
description: Create and update concise AGENTS.md files using proven best practices.
license: MIT
compatibility: opencode
disable-model-invocation: true
---

## Skill: agents-md-best-practices

**Base directory**: .opencode/skill/agents-md-best-practices

## What I do

I create or update AGENTS.md files so they are short, actionable, and focused on agent success:

- Keep content under 100 lines when possible
- Include only critical commands and workflows
- Emphasize progressive discovery via links to deeper docs
- Capture gotchas and verification steps over time

## When to use me

Use this when:

- Starting a new AGENTS.md
- Refactoring an overly long or confusing AGENTS.md
- Adding missing build/test commands or workflow steps
- Capturing newly discovered gotchas or verification steps

## How I work

### Step 1: Understand project essentials

I identify:

- Project type and stack
- Key folders and entry points
- Build and test commands
- Any agent-specific constraints

### Step 2: Draft the short guide

I include only these sections (with the docs index at the top):

- Docs index (deep dives)
- Project overview and structure
- Build/run commands
- Test commands
- Agent workflow (plan -> implement -> verify)

### Step 3: Capture feedback loops

I ensure the guide:

- Lists verification commands (linters/tests)
- Notes any known gotchas or slow commands
- Encourages updating the guide when surprises occur

## Output format

I produce a concise AGENTS.md with:

- Clear headings
- Short bullet lists
- Minimal examples
- Links to deeper docs

## Example output structure

````markdown
# AGENTS.md - project guide (short)

## Docs index (deep dives)
- [docs/architecture.md](docs/architecture.md)
- [docs/frontend.md](docs/frontend.md)

## Overview
- One line on what the project is
- One line on the stack

## Build and verify
- `pnpm dev`
- `pnpm test`

## Workflow
- Update plan or PRD first
- Implement with small diffs
- Run tests and note any gotchas
````

## Validation checklist

Before finalizing, I ensure:

- [ ] File is under 100 lines when feasible
- [ ] Commands are correct and minimal
- [ ] Verification steps are included
- [ ] Progressive discovery links are present
- [ ] No redundant or conflicting guidance
- [ ] Language matches the project (e.g., German UI notes)
