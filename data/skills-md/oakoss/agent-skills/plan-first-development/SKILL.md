---
name: plan-first-development
description: |
  Planning methodology and session management for software projects.
  Covers markdown plan creation, iterative refinement, multi-model blending,
  phase-based implementation docs, and cross-session progress tracking.

  Use when starting new projects, adding major features, breaking large work
  into phases, resuming after context clears, or managing multi-phase implementations.
license: MIT
metadata:
  author: oakoss
  version: '1.2'
---

# Planning

## Overview

Plan-first development methodology where 80%+ of time goes to planning before implementation begins. Planning tokens are cheaper than implementation tokens, and models reason better about a detailed plan that fits their context window than about a sprawling codebase.

**When to use:** Starting new projects, adding major features, breaking complex work into phases, resuming work after context clears, managing multi-session implementations, coordinating multiple agents on the same codebase.

**When NOT to use:** Quick bug fixes, one-file changes, exploratory prototyping where requirements are unknown, trivial refactors where the change is obvious.

## Quick Reference

| Planning Phase          | Description                                    |
| ----------------------- | ---------------------------------------------- |
| 1. Initial plan         | Write goals, intent, workflows, tech stack     |
| 2. Iterative refinement | 4-5 rounds of review until suggestions plateau |
| 3. Multi-model blend    | Get competing plans, merge best-of-all-worlds  |
| 4. Convert to tasks     | Self-contained tasks with dependency structure |
| 5. Polish tasks         | 6+ rounds of cross-model review                |

| Phase Type     | Scope                                 | Max Files | Duration  |
| -------------- | ------------------------------------- | --------- | --------- |
| Infrastructure | Scaffolding, build config, deployment | 3-5       | 1-3 hours |
| Database       | Migrations, schema, seed data         | 2-4       | 2-4 hours |
| API            | Routes, middleware, validation        | 3-6       | 3-6 hours |
| UI             | Components, forms, state, styling     | 4-8       | 4-8 hours |
| Integration    | Third-party services, webhooks        | 2-4       | 3-5 hours |
| Testing        | E2E tests, integration tests          | varies    | 3-6 hours |

| Pattern               | Purpose                             | Key Points                              |
| --------------------- | ----------------------------------- | --------------------------------------- |
| When to plan vs build | Decision tree by complexity signals | Match planning depth to task complexity |
| Risk assessment       | Probability x impact matrix         | Focus on high-risk items first          |

| Session Lifecycle | Action                                                        |
| ----------------- | ------------------------------------------------------------- |
| Start             | Read SESSION.md, check "Next Action", continue                |
| Work              | Implement, verify, debug (repeat)                             |
| Checkpoint        | Git commit with structured format, update SESSION.md hash     |
| Wrap              | Update SESSION.md, git checkpoint, set concrete "Next Action" |
| Resume            | Read SESSION.md + planning docs, continue from "Next Action"  |

| Document              | When to Generate                               |
| --------------------- | ---------------------------------------------- |
| Implementation phases | Always -- core plan doc for every project      |
| Session tracking      | Always -- navigation hub for progress          |
| Database schema       | 3+ tables                                      |
| API endpoints         | 5+ endpoints                                   |
| Architecture overview | Multiple services or complex system boundaries |
| Critical workflows    | Complex setup steps, order-sensitive workflows |

| Good Plan               | Great Plan                                |
| ----------------------- | ----------------------------------------- |
| Describes what to build | Explains WHY you are building it          |
| Lists features          | Details user workflows and interactions   |
| Mentions tech stack     | Justifies tech choices with tradeoffs     |
| Has tasks               | Has tasks with dependencies and rationale |
| ~500 lines              | ~3,500+ lines after refinement            |

## Common Mistakes

| Mistake                                             | Correct Pattern                                                                               |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Starting implementation before planning is complete | Spend 80%+ of time on planning; finish all refinement rounds before writing code              |
| Writing vague next actions like "continue API work" | Be specific: "Implement PATCH /api/tasks/:id in src/routes/tasks.ts:47"                       |
| Session tracking doc over 200 lines                 | Collapse completed phases to summaries; reference planning docs for details                   |
| Creating phases with 10+ files                      | Auto-split into sub-phases of 5-8 files that fit in one 2-4 hour session                      |
| Single-round plan review                            | Iterate 4-5 rounds until suggestions plateau; use multi-model blending for fresh perspectives |
| Copying code into session docs                      | Reference file paths and line numbers instead of pasting code                                 |
| Duplicating planning doc content in session doc     | Link to sections with anchors; session doc is a navigation hub                                |
| No verification criteria on phases                  | Every phase needs specific, testable exit criteria (status codes, user flows, constraints)    |
| Skeleton-first coding before a plan exists          | One thorough plan beats incremental skeleton-first coding                                     |
| Planning without prototyping unknown tech           | Build a spike first for unfamiliar frameworks, then create the plan                           |
| Over-planning simple tasks                          | Match planning depth to complexity; skip for trivial work                                     |
| Not validating assumptions early                    | Run a spike for the riskiest assumption first                                                 |

## Delegation

- **Explore existing codebase for architecture decisions**: Use `Explore` agent to survey file structure, patterns, and dependencies before planning
- **Execute phase implementation with verification**: Use `Task` agent to implement individual phases, run verification criteria, and create checkpoint commits
- **Design architecture and decompose into phases**: Use `Plan` agent to create implementation phases with dependency ordering and gate criteria

## References

- [Planning process and iterative refinement](references/planning-process.md)
- [Session management and context tracking](references/session-management.md)
- [Phase-based implementation planning](references/phase-planning.md)
- [Review workflows and multi-model blending](references/review-workflows.md)
- [Decision tracking and conditional documents](references/decision-tracking.md)
- [Planning document templates](references/document-templates.md)
