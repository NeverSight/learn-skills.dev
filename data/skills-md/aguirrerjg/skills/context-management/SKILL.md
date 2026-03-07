---
name: context-management
description: Set up and optimize context management for any project. Use this skill when the user says "set up context management", "optimize my CLAUDE.md", "context setup", "configure compact instructions", "set up rules", or when starting a new project and wanting best practices for long sessions, memory, compaction, and subagent delegation. Also trigger when the user mentions problems with context loss, compaction losing info, or sessions getting slow.
---

# Context Management Setup

Automates context management best practices for Claude Code projects.
Analyzes the current project and generates optimized configuration files.

## When to Use

- Starting a new project (no CLAUDE.md exists)
- Existing project needs context optimization
- User reports context loss after compaction
- User wants to set up rules, memory, or subagent guidelines
- Before a long coding session

## Workflow

### Step 1: Analyze the Project

Before generating anything, read the project to understand its shape:

1. Read `package.json`, `Cargo.toml`, `pyproject.toml`, or equivalent to detect stack
2. Read existing `CLAUDE.md` if present (will update, not overwrite)
3. Check for `.claude/rules/` directory
4. Scan `src/` structure to identify major areas (api, components, lib, tests, etc.)
5. Check for existing `tsconfig.json`, `.eslintrc`, `prettier.config` for conventions
6. Read `README.md` if present for project context

Collect this into a mental model of the project before proceeding.

### Step 2: Generate or Update CLAUDE.md

The CLAUDE.md MUST stay under 200 lines. Use @references for details.

Structure to follow:

```markdown
# [Project Name]

[1-2 sentence description from README/package.json]

## Stack
[Detected stack — language, framework, DB, key libs]

## Key Commands
[Detected from package.json scripts, Makefile, etc.]
- Dev: `[command]`
- Build: `[command]`
- Test: `[command]`
- Lint: `[command]`

## Architecture
[Brief description of src/ structure — max 5-8 lines]
- @[key-file-1] for [purpose]
- @[key-file-2] for [purpose]

## Conventions
[Detected from config files — indent, quotes, semicolons, naming]

## Context Management

### Compact Instructions
When compacting, always preserve:
- List of modified files and their purpose
- Failing tests with error messages
- Architectural decisions made this session
- Current task status and next steps

When compacting, safe to discard:
- File contents that were only read for exploration
- Search results that didn't lead anywhere
- Verbose command output already acted upon

### Subagent Guidelines
- Use Explore agent for codebase searches requiring > 3 queries
- Use background agents for running test suites
- Use Plan agent before refactors touching > 5 files
- Delegate file-heavy research to subagents to protect main context

### Rules
See .claude/rules/ for scoped coding rules.
```

**Important:** If CLAUDE.md already exists, MERGE — don't replace. Add missing sections only.

### Step 3: Generate Scoped Rules

Create `.claude/rules/` with rules scoped to relevant paths.
Only create rules for areas that actually exist in the project.

Read `references/rule-templates.md` for templates per area.

**Rules to consider creating (only if the area exists):**

| File | Scope | Creates when |
|------|-------|-------------|
| `code-style.md` | `**/*` | Always — general conventions |
| `api.md` | `src/api/**`, `src/routes/api/**` | API routes exist |
| `components.md` | `src/components/**`, `src/lib/components/**` | UI components exist |
| `testing.md` | `**/*.test.*`, `**/*.spec.*` | Test files exist |
| `database.md` | `prisma/**`, `src/db/**`, `drizzle/**` | ORM/DB config exists |

Each rule file should be 10-30 lines max. Use the templates from references.

### Step 4: Initialize Memory Structure

If auto-memory is enabled, create initial memory notes:

```
~/.claude/projects/<project-hash>/memory/MEMORY.md
```

Content:
```markdown
# [Project Name] Memory

## Project
- Stack: [detected]
- Key paths: [detected]

## Patterns
[Leave empty — Claude fills as it learns]

## Debugging
[Leave empty — Claude fills as issues arise]
```

### Step 5: Summary Report

After setup, show the user a summary:

```
Context Management Setup Complete
==================================
CLAUDE.md:     [created/updated] (X lines)
Rules:         [N] files in .claude/rules/
Memory:        [initialized/already exists]

Files created:
  - .claude/rules/code-style.md
  - .claude/rules/[others...]

Recommendations:
  - [Any project-specific suggestions]
```

## Important Constraints

- CLAUDE.md must stay under 200 lines
- Each rule file must stay under 30 lines
- Never overwrite existing files without showing diff first
- Detect conventions from config files, don't assume
- If stack is unknown, ask the user before generating
- Use @references in CLAUDE.md instead of inlining large content
