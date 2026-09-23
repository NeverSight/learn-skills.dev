---
name: sdd
description: >
  Spec-driven development workflow for implementing features with structured documentation.
  Use when starting a new feature, task, or implementation that benefits from upfront planning.
  Triggers: /sdd, spec-driven, create spec, implementation plan, or when user describes a feature/task to implement.
---

# SDD - Spec Driven Development

A structured workflow for implementing features through documentation-first development.

## Directory Setup

Create spec directory for the task:

```bash
mkdir -p ./.specs/{task-name}
```

Name `{task-name}` based on the task (e.g., `create-article-component`, `add-user-auth`).

## Phase Overview

```
1. Context Analysis    → 1-context.md
2. Prototyping (opt)   → 2-prototyping-learnings.md
3. Requirements        → 3-requirements.md
4. Design              → 4-design.md
5. Implementation Plan → 5-implementation-plan-{N}.md
6. Implementation      → (PR loop)
```

Each phase: Create document → Present to user → Get approval → Next phase

## Phase 1: Context Analysis

Analyze the existing codebase to understand patterns and constraints.

Create `.specs/{task-name}/1-context.md`. See [references/templates.md](references/templates.md#1-context) for format.

Contents:

- Tech stack and frameworks
- Relevant existing code/components
- Project conventions (naming, structure)
- Constraints or limitations

Present to user and get approval before proceeding.

## Phase 2: Prototyping (Optional)

Rapidly build a throwaway prototype to understand user experience before defining requirements.

**Ask the user if they want to do prototyping before proceeding.**

### Purpose

- Quickly validate the user experience and usability
- Discover requirements that are hard to imagine without trying
- All code changes will be discarded after confirmation

### Guidelines

- **Ignore all type errors and lint errors** - speed over correctness
- Build the minimum to experience the feature
- Focus on the "feel" of using it, not the implementation quality
- No tests, no clean code - just make it work enough to try

### Setup

Create a prototype branch using git worktree:

```bash
git worktree add ../prototype-{task-name} -b prototype/{task-name}
```

Work in the worktree directory. The main working directory stays clean.

### Process

1. Build a rough prototype in the worktree (ignore tsc/lint errors)
2. User tries the prototype and provides feedback
3. Document learnings in `.specs/{task-name}/2-prototyping-learnings.md` (in main directory)
4. Include useful code snippets in the learnings doc for later reference
5. Remove the worktree and branch:
   ```bash
   git worktree remove ../prototype-{task-name}
   git branch -D prototype/{task-name}
   ```
6. Proceed to Requirements phase with new insights

Create `.specs/{task-name}/2-prototyping-learnings.md`. See [references/templates.md](references/templates.md#2-prototyping-learnings) for format.

Contents:

- What worked well in the prototype
- What felt awkward or wrong
- Discovered requirements or constraints
- UX insights that should influence design

Present learnings to user and get approval before proceeding.

## Phase 3: Requirements Definition

Define WHAT the task should accomplish, not HOW.

Create `.specs/{task-name}/3-requirements.md`. See [references/templates.md](references/templates.md#3-requirements) for format.

**If prototyping was done**: Reference `2-prototyping-learnings.md` to incorporate discovered insights.

Guidelines:

- Use user story format
- List acceptance criteria as checkboxes
- Define scope boundaries (in/out of scope)
- Keep concise: max 5 items per section
- No technical implementation details
- Mark ambiguous requirements with `[NEEDS CLARIFICATION]` (e.g., `User can authenticate [NEEDS CLARIFICATION: OAuth? Password?]`)

All `[NEEDS CLARIFICATION]` markers must be resolved before approval.

Present to user and get approval before proceeding.

## Phase 4: Design

Define the implementation direction at an architectural level. Not implementation details.

Create `.specs/{task-name}/4-design.md`. See [references/templates.md](references/templates.md#4-design) for format.

Contents:

- **Domain Models**: Core type definitions only (not utility types or internal details)
- **Feature Boundaries**: What features exist, their responsibilities (1 line each), dependencies between them
- **Directory Structure**: Feature-level package structure only (not detailed files within each feature)
- **Main Flow**: Key processing steps with data transformation (e.g., `validateInput: FormInput → ValidatedInput`)
- **Layer Structure**: Where each logic belongs in the project's layer hierarchy

### Design Principle: Push Logic to Core

Write core logic first, independent of framework or infrastructure. The core should not know whether it's used by React, CLI, server, etc.

Every project has a layer hierarchy (inner = more pure, outer = more side-effectful). Always push logic as far inward as possible.

Example (React project):

```
Core (pure functions) → State (jotai) → Hooks → Components
```

Example (Backend project):

```
Domain Logic → Application Service → Controller → HTTP Handler
```

Identify your project's layers and document where each logic belongs. Benefits: easier testing, better reusability, clearer boundaries.

Present to user and get approval before proceeding.

## Phase 5: Implementation Plan

Break down the design into PR-sized units.

Create `.specs/{task-name}/5-implementation-plan-{N}.md` for each PR. See [references/templates.md](references/templates.md#5-implementation-plan) for format.

### PR Structure Strategy

Choose based on task characteristics:

- **Vertical (by feature)**: Slice through all layers for one feature. Preferred when features are independent and early feedback is valuable.
- **Horizontal (by layer)**: Build one layer at a time. Use when core design needs to be solid before building on top.

### Guidelines

- One file per PR
- PR unit = reviewable size
- Each PR must define how it will be reviewed (tests, types, working UI, etc.)
- Include checkbox tasks for progress tracking
- Show task dependencies (what can run in parallel)
- Commits are suggestions, adjust during implementation

Present all plans to user and get approval before proceeding.

## Phase 6: Implementation

Execute implementation plans PR by PR.

### PR Loop

For each `5-implementation-plan-{N}.md`:

```
1. Execute tasks (check boxes as you go)
2. Suggest commit messages (do NOT run git commands)
3. Run verification: tsc, lint, test
4. Check: Do learnings require updates to 3-requirements.md or 4-design.md?
   - Yes → Update documents, review impact on remaining plans
   - No → Continue
5. Present to user for approval
6. User OK → Next PR
   User NG → Address feedback, repeat from step 3
```

### Important Rules

- Follow 3-requirements.md and 4-design.md strictly
- Update specs directly when learnings emerge (no separate learnings file)
- Suggest commit messages but never execute git commands
- Run `tsc`/`lint`/`test` before user confirmation
