---
name: dev
description: >
  Personal development workflow orchestrator. Use when starting any development
  task — bug fixes, features, refactors, or explorations. Runs a 5-stage process:
  Research, Plan, Scaffold, Build, Validate. First three stages have user
  approval gates; Build and Validate run autonomously.
license: MIT
compatibility: >
  Works with any agent that supports the Agent Skills standard. On Claude Code,
  research can be delegated to a dedicated subagent for efficiency.
metadata:
  author: zackbart
  version: "0.4.0"
argument-hint: "[werk] <task description>"
allowed-tools: "Read, Grep, Glob, Bash, Write, Edit, Agent, TaskCreate, TaskUpdate, TaskList, TaskGet, AskUserQuestion"
---

# Motif Development Workflow

You are running the motif workflow — a 5-stage development process. The first three stages have user approval gates. Build and Validate run autonomously.

## Argument Parsing

If the first word of $ARGUMENTS is "werk", strip it and use the remainder as the task description. In the Scaffold stage, use the `/werk` skill for task creation instead of native task tracking tools.

Otherwise, use all of $ARGUMENTS as the task description and native task tracking tools throughout.

## Complexity Assessment

Before starting, assess task complexity on a 3-point scale:

- **Light** (quick bug fix, small tweak, config change): abbreviated research, minimal planning, 1-3 tasks
- **Medium** (feature addition, moderate refactor, new test coverage): standard research, full planning, 3-8 tasks
- **Heavy** (large refactor, new system, architecture change): deep research, thorough planning with tradeoff analysis, 8+ tasks

State your assessment to the user before beginning Stage 1.

---

## Pause Point Protocol

After completing Stages 1-3, present a summary and ask:

> **[Stage Name] complete.** [Brief summary]
>
> Ready for [Next Stage]?
> - **go** — proceed
> - **skip** — skip next stage
> - **redo** — re-run with feedback
> - **stop** — end here

Do not auto-advance through stages 1-3. Stages 4-5 run without pausing.

---

## Stage 1: Research

Read-only codebase exploration. Do not create, edit, or delete any files.

If a subagent capability is available (e.g., a dedicated research agent), delegate to it. Otherwise, perform research directly.

**Depth Calibration:**
- **Light**: Find the 1-3 most relevant files. Check for obvious patterns. Minimize tool calls.
- **Medium**: Map the relevant module structure, identify patterns, check test coverage, review recent git history.
- **Heavy**: Comprehensive module mapping, dependency tracing, git archaeology, related test suites, documentation review, similar precedents.

**Research Process:**
1. **Orient** — project structure (package.json, Cargo.toml, pyproject.toml, go.mod, etc.; top-level directories)
2. **Locate** — find files relevant to the task
3. **Understand** — read key files to understand current implementation
4. **Context** — git history for recent changes (`git log --oneline -20 -- <path>`)
5. **Patterns** — coding conventions, testing patterns, architectural decisions
6. **Toolchain** — find the test, build, and lint commands so you can run them in later stages

**Output:**
- **Relevant Files** — each with a 1-line description
- **Patterns & Conventions** — how similar work is done in this codebase
- **Constraints** — build/CI requirements, type system, linting rules
- **Toolchain** — exact commands for test, build, lint
- **Risks** — fragile areas, edge cases, missing coverage

---

## Stage 2: Plan

Using research findings, produce an implementation plan.

**Output:**
- **Approach** — what will change and how (be specific about the technique, not just "modify X")
- **Files** — which files will be created, modified, or deleted
- **Testing** — what tests to write or update, how to verify correctness
- **Tradeoffs** (medium/heavy only) — alternatives considered and why this approach wins

Scale depth to complexity. A light plan can be a few sentences. A heavy plan needs alternatives and risk assessment.

---

## Stage 3: Scaffold

Decompose the plan into a task list. Each task should be a single, verifiable unit of work.

**Native mode** — use the available task tracking tools (TaskCreate, TaskUpdate, etc.) to create and manage tasks.

**Werk mode** — use the `/werk` skill to create and manage tasks.

For both modes:
- Set dependencies where order matters
- Include test tasks alongside the code they verify (not as a separate "write all tests" task)
- Final task: validate the overall goal

Present the task list. The user may add, remove, or reorder before approving.

---

## Stage 4: Build

**This stage runs autonomously.** Work through tasks in order without stopping for approval on each one.

For each task:
1. Mark in-progress
2. Implement the change
3. If tests are part of this task, write and run them
4. Mark completed

**When to stop and ask:**
- A task requires a design decision not covered by the plan
- Tests fail in a way that suggests the plan is wrong (not just a typo)
- You discover the plan missed something significant

For routine issues (lint errors, minor test fixes, small deviations), handle them and keep going. Use your judgment — the plan is a guide, not a contract.

After all tasks complete, proceed directly to Validate.

---

## Stage 5: Validate

Run automatically after Build completes.

1. **Goal check** — does the implementation satisfy the original task description?
2. **Tests** — run the test command discovered in Research. Report pass/fail.
3. **Diff summary** — all files changed with a brief description of each change
4. **Loose ends** — anything incomplete, TODO comments added, known limitations

Present the validation report. If issues exist:
- **fix** + details → go back to Build for targeted fixes
- **done** → accept current state
