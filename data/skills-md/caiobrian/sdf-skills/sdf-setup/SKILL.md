---
name: sdf-setup
description: "Initializes project constitution (CLAUDE.md) and LessonsLearned.md for the SDF workflow. Activates when onboarding a new repository, starting a new project, or when no CLAUDE.md exists. Triggers include 'setup sdf', 'iniciar projeto', 'configurar sdf', '/sdf-setup'."
---

# SDF Setup — Project Constitution

Initialize foundational artifacts: `.claude/CLAUDE.md` and `LessonsLearned.md`.

## Process

### Step 1: Analyze the codebase

Examine: stack, framework, bundler, runtime, code patterns, test framework, linters/formatters, folder structure, package scripts.

If the project is empty, ask for preferences.

### Step 2: Generate `.claude/CLAUDE.md`

Keep under 60 lines. Do NOT include what linters already enforce.

```markdown
# Project Constitution

## Stack
- [detected]
- Prohibited: [what NOT to use]

## Tech Decisions
- [e.g., Data fetching: TanStack Query, never fetch + useEffect]

## Code Conventions
- [extracted from codebase]

## Quality Standards
- [from linter/formatter configs]

## Prohibited Actions
- Never install new dependencies without explicit approval

## Folder Structure
- [mapped from project]

## Commands
- Build: [cmd]
- Test: [cmd]
- Lint: [cmd]
```

### Step 3: Generate `LessonsLearned.md`

```markdown
# Lessons Learned
<!-- Format: LL-XXX: Title | Context | Rule | Date -->
```

### Step 4: Confirm

Present output and ask (in the user's preferred language):
- If any important convention is missing
- If there are any specific prohibitions

## Rules
- Detect patterns from REAL codebase, never assume defaults
- Always communicate in the user's preferred language
