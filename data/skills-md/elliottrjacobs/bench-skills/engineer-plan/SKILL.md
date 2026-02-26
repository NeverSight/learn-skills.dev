---
name: engineer-plan
description: Create structured implementation plans using parallel research agents. Use when the user says "plan this", "create a plan", "implementation plan", or after completing a tech spec. Breaks specifications into ordered, actionable tasks with effort estimates.
allowed-tools: ["Read", "Glob", "Grep", "Task", "TodoWrite", "AskUserQuestion", "Write"]
argument-hint: "[spec-path]"
---

# /engineer-plan — Implementation Planning

Create structured implementation plans that break specs into ordered, actionable tasks. Plans bridge architecture (tech spec) and execution (engineer-work).

## When to Use

- User says "plan this", "create a plan", "implementation plan"
- After completing a tech spec and ready to break it into tasks
- When a feature needs structured decomposition before building

## Process

### Step 1: Gather Context

Check for existing specs (in priority order):
1. `docs/tech-specs/` — Most detailed, preferred source
2. `docs/prds/` — Product requirements if no tech spec
3. User-provided description or `$ARGUMENTS`

Also check `docs/solutions/` for relevant past solutions.

### Step 2: Research (Parallel Agents)

Spawn 2 agents IN PARALLEL using the Task tool:

#### Agent 1 — Codebase Analyst
```
Task(subagent_type: "general-purpose", description: "Analyze codebase for planning")
prompt: Analyze this project to inform an implementation plan for [FEATURE].
  Focus on: existing patterns to follow, files/directories that need modification,
  related code that could be affected, test patterns, tech stack (check package.json,
  config files). Return findings relevant to planning.
```

#### Agent 2 — Practices Researcher
```
Task(subagent_type: "general-purpose", description: "Research best practices")
prompt: Research implementation best practices for [FEATURE TYPE] given the
  project's tech stack. Focus on: recommended implementation order, common
  integration challenges, testing strategies. Return practical guidance.
```

**If the feature involves unfamiliar framework APIs or third-party integrations**, launch an additional agent:

#### Agent 3 — Docs Researcher (conditional)
```
Task(subagent_type: "general-purpose", description: "Research framework docs")
prompt: Research [specific framework/API] documentation for [FEATURE].
  Check version compatibility with the project's package.json.
  Focus on: correct API usage, deprecation notices, common pitfalls.
```

Skip this agent if the feature uses well-established patterns already present in the codebase.

### Step 3: Choose Detail Level

Use AskUserQuestion:
- "What level of detail for this plan?" (header: "Detail")
  - "Minimal — task list with descriptions" — For small features, <1 day
  - "Standard — tasks with acceptance criteria (Recommended)" — For most features, 1 day - 1 week
  - "Comprehensive — detailed tasks with code guidance" — For complex features, >1 week

### Step 4: Write Plan

Write the plan to `docs/plans/YYYY-MM-DD-<name>.md`.

**Planning rules:**
- Tasks ordered by dependency (what must be done first)
- Each task is independently implementable and testable
- Include clear acceptance criteria (standard/comprehensive)
- Mark parallel-safe tasks
- Effort estimates: S (single file), M (multiple files), L (cross-cutting)
- Include Task 0 for setup (branch, dependencies) if needed

**Minimal plan format:**
```markdown
# Plan: [Feature Name]
**Date:** YYYY-MM-DD | **Spec:** [link] | **Detail:** Minimal

## Tasks
| # | Task | Description | Effort | Depends On |
|---|------|-------------|--------|------------|
| 0 | Setup | Branch, dependencies | S | — |
| 1 | ... | ... | S/M/L | — |
```

**Standard plan format** — adds per-task sections with:
- Key files to modify
- Acceptance criteria (2-4 bullets)
- Test expectations
- Dependency graph

**Comprehensive plan format** — adds per-task:
- Implementation guidance with code patterns
- Detailed test specifications
- Rollback procedures
- Risk assessment

### Step 5: Handoff

Use AskUserQuestion:
- "Plan is ready. What's next?" (header: "Next step")
  - "Start building (`/engineer-work`)" — Execute the plan
  - "Refine the plan" — Adjust tasks or detail
  - "Done for now" — Save and close

## Output

Save to: `docs/plans/YYYY-MM-DD-<name>.md`

## Next Steps

- Ready to build? → `/engineer-work`
- Need a tech spec first? → `/product-tech-spec`
- Want to review after building? → `/engineer-review`
