---
name: backlog
description: |
  Structured workflow for taking features from backlog to implementation.
  Use when picking tasks, refining PRDs, planning implementation, or implementing features.
  Invokes specialized agents: triager, refiner, planner, implementer, conductor.
---

# Backlog Workflow

A structured workflow for taking features from backlog to implementation using specialized agents.

## Workflow Overview

```
Backlog → Triage → PRD → Plan → Refine → PRD (refined) → Implement → Code
```

**Manual mode**: Each step is human-triggered. Agents do not auto-chain.

**Conductor mode**: Run the conductor workflow to orchestrate all phases automatically until complete or blocked.

## Workflow Actions

| Action                | Agent       | Purpose                                       | Optional command alias |
| --------------------- | ----------- | --------------------------------------------- | ---------------------- |
| Triage                | triager     | Select task from backlog, create blank PRD    | `/triage`              |
| Plan `[slug]`         | planner     | Create implementation plan                    | `/plan [slug]`         |
| Refine `[slug]`       | refiner     | Complete and validate PRD                     | `/refine [slug]`       |
| Implement `[slug]`    | implementer | Execute plan on feature branch                | `/implement [slug]`    |
| Conduct               | conductor   | Orchestrate all phases in a loop              | `/conduct`             |
| Conduct phased run    | conductor   | Run specific phases only (e.g., triage,plan)  | `/conduct --phases X`  |
| Conduct targeted run  | conductor   | Process specific feature only                 | `/conduct --slug X`    |

Slash commands are optional convenience wrappers. The workflow is designed to
work with plain prompts and subagent invocation across tools.

## Agents

Agents are minimal — they define role, boundaries, and tools. Methodology lives in skills.

| Agent           | Branch      | Writes To                               | Methodology Skill                   |
| --------------- | ----------- | --------------------------------------- | ----------------------------------- |
| **triager**     | main        | `.backlog/prds/`, `.backlog/backlog.md` | `skills/backlog/triage/SKILL.md`    |
| **refiner**     | main        | `.backlog/prds/`                        | `skills/backlog/refine/SKILL.md`    |
| **planner**     | main        | `.backlog/plans/`, `.backlog/prds/`     | `skills/backlog/plan/SKILL.md`      |
| **implementer** | feature/\*  | Source code                             | `skills/backlog/implement/SKILL.md` |
| **conductor**   | main + feat | `.backlog/`, source code, action log    | Orchestrates all of the above       |

## Naming Convention

The workflow uses descriptive **slugs** instead of numeric IDs:

| Artifact      | Format           | Example                           |
| ------------- | ---------------- | --------------------------------- |
| Backlog entry | `[slug] Title`   | `[user-auth] User Authentication` |
| PRD file      | `PRD-[slug].md`  | `PRD-user-auth.md`                |
| Plan file     | `PLAN-[slug].md` | `PLAN-user-auth.md`               |
| Branch        | `feat/[slug]`    | `feat/user-auth`                  |

Slugs: lowercase kebab-case, max 30 characters.

## Status Flow

### PRD Statuses

```
blank → refined → needs_review → approved
```

Only a human sets `approved`. The refiner sets `refined` or `needs_review`.

### Plan Statuses

```
draft → needs_review → approved → implemented | partially_implemented
```

Only a human sets `approved`. The planner sets `draft` or `needs_review`.

## Human Checkpoints

- After **Triage**: Review selected task, adjust if needed
- After **Plan**: Review plan, mark as `approved` if ready
- After **Refine**: Review PRD, mark as `approved` if ready
- After **Implement**: Review code, create PR manually

## Project Setup

Each project using this workflow needs a `.backlog/` directory:

```
your-project/
└── .backlog/
    ├── backlog.md
    ├── prds/
    └── plans/
```

## Example Usage

### Manual Mode (step-by-step)

```bash
# Triage the highest priority task
"Use the triager agent to pick the highest-priority pending task and create a PRD."

# Create implementation plan
"Use the planner agent to create the implementation plan for user-auth."

# Refine a specific PRD
"Use the refiner agent to refine PRD-user-auth."

# Execute the plan
"Use the implementer agent to implement the approved plan for user-auth."
```

### Conductor Mode (automated)

```bash
# Run full pipeline until complete or blocked
"Use the conductor agent to run the backlog pipeline until complete or blocked."

# Run only triage and plan phases
"Use the conductor agent and run only phases: triage,plan."

# Process specific feature only
"Use the conductor agent and process only slug: user-auth."

# Named conductor for parallel operation
"Use conductor name frontend and run phases triage,plan."
```

### Parallel Conductors

Multiple conductors can run in parallel when handling different phases:

```bash
# Terminal 1: Create PRDs and plans
"Use conductor name frontend and run phases triage,plan."

# Terminal 2: Review plans
"Use conductor name reviewer and run phase refine."

# Terminal 3: Implement approved plans
"Use conductor name builder and run phase implement."
```
