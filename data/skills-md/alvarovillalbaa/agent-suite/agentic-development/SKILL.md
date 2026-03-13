---
name: agentic-development
description: End-to-end repository execution workflow for implementing, debugging, refactoring, reviewing, instrumenting, explaining architecture, assessing refactor impact, and shipping code in any software repo. Use when the assistant needs to orient in an unfamiliar codebase, choose between direct execution and supervised harness loops, keep specs, plans, and tests distinct, coordinate builder and reviewer passes, handle PR feedback, inspect observability, or land cross-cutting frontend and backend changes without leaving loose ends.
---

# Agentic Development

Drive work through one loop: orient, classify the task, choose the execution mode, implement, review, verify, and compound. Treat repo-local instructions and existing architecture as the source of truth. For repeated or long-running work, keep the loop supervised: fresh context each iteration, state on disk, one task at a time, hard gates, and explicit reviewer output.

## Start Here

1. Run the repo scan helper if the skill bundles one; otherwise do the same discovery manually from the repo root.
2. Map the repo before touching code: instruction files, package or service boundaries, entrypoints, build and test commands, deployment surfaces, and current git state.
3. For frontend-heavy work, map framework boundaries, route ownership, design-system sources, shared primitives, state owners, and existing analytics or error-reporting seams before choosing an edit path.
4. Decide the task type and execution mode: implementation, review, architecture explanation, debugging, refactor, instrumentation, or release cleanup; then choose direct execution or a supervised harness loop if code will be written.
5. Choose the authoritative path for the change or explanation: the existing module, service, component, hook, page, command, model, or workflow that already owns the behavior.
6. Decide the proof before editing: what command, test, log, screenshot, trace, dependency search, or reviewer output will confirm the result.
7. Load only the reference files relevant to the current task.

## Core Rules

- Prefer repo-local instructions over generic advice. If `AGENTS.md`, `CLAUDE.md`, `SOUL.md`, `PRINCIPLES.md`, `PLANS.md`, `README.md`, `CONTRIBUTING.md`, or service/package docs exist, follow them in the hierarchy the repo defines.
- Work with the current git reality. Do not force a branch or worktree change just because `main` is active; choose the safest path that fits the user's intent.
- Extend existing seams. Reuse current services, hooks, stores, component primitives, models, logging, analytics, and scripts instead of creating parallel abstractions.
- Architecture claims need evidence. Trace entrypoints, ownership, dependencies, and contracts before explaining how the system works or what a refactor will affect.
- Separate concerns intentionally: specs define behavior, plans define execution, progress files record loop state, tests prove behavior, and instrumentation explains production behavior.
- Treat context as scarce. Keep instruction files, prompts, and scratchpads compact; use index files and on-demand references instead of stuffing every loop with full docs.
- One task per loop. If work spans multiple iterations, persist state on disk and restart with fresh context instead of dragging a swollen transcript forward.
- Hard gates decide readiness. In harness or agent-loop mode, gates that can block or advance work must be binary pass or fail, not advisory.
- Structured review beats narrative when another agent or loop must consume the result. Emit compact findings with severity, file, line, risk, and expected fix.
- When broad permissions or network access are required, prefer the smallest blast radius: isolated branch or worktree, sandbox or ephemeral environment, and least-privilege credentials.
- Verification gates claims. Do not say fixed, complete, passing, or ready without fresh evidence.
- Frontend work is product behavior, not decoration. Preserve design systems, router conventions, state ownership, accessibility, and interaction quality the same way you would preserve API boundaries in a backend.
- Choose the right frontend artifact level before coding: primitive, composed control, domain component, page section, hook, store, or route. A bad boundary choice causes more churn than a small implementation bug.
- Finish cleanly. Make the next integration step explicit instead of silently leaving the repo in an ambiguous state.

## Execution Modes

- Direct execution: use for small, clear changes with a single coherent proof path.
- Supervised harness loop: use for repeated or backlog-style work only when the spec is clear, the change surface is isolated, and the repo has trustworthy gates. Keep each iteration fresh and single-purpose.
- Review or explanation mode: use for architecture mapping, impact analysis, code review, or debugging passes where the immediate output is understanding or findings rather than code.

Switch modes when the evidence changes. If a harness starts flailing, shrink the task, tighten the spec, or return to direct execution.

## Architecture Bias

Apply these defaults unless the repo clearly prefers something else:

- Maximize reuse and minimize total LOC.
- Prefer one authoritative implementation path over duplicated variants.
- Avoid repeated logic and near-duplicate code with the same purpose.
- Do not over-modularize. Split only when independence, ownership, or readability materially improves.
- Favor cohesive vertical slices over scattering one concept across many files.
- Push business logic and async orchestration out of leaf UI where possible; keep views readable and state ownership explicit.
- Prefer composition, slots, or subcomponents over boolean-heavy component APIs and prop matrices.
- Treat loading, empty, error, success, and responsive states as part of the implementation, not post-hoc polish.

## Workflow Router

### Orientation and repo policy

Read [repo-orientation.md](./references/repo-orientation.md) for startup discovery, instruction-file handling, repo-shape detection, and initial command selection.

### Harness loops and persistent task state

Read [harness-loops.md](./references/harness-loops.md) when the task is large enough for repeated agent iterations, when specs or plans live on disk between runs, when builder and reviewer passes should be split, or when you need to decide whether a repo is ready for higher-autonomy execution.

### Architecture analysis and refactor impact

Read [architecture-analysis.md](./references/architecture-analysis.md) when the user asks how the system works, wants dependency or data-model relationships explained, or needs impact analysis before a rename, move, extraction, or schema change.

### Git, branches, worktrees, and PR flow

Read [collaboration-and-git.md](./references/collaboration-and-git.md) when the task touches branching strategy, worktrees, PRs, merges, or cleanup.

### Spec-driven, plan-driven, and test-driven delivery

Read [specs-plans-tests.md](./references/specs-plans-tests.md) when the user asks for a plan or spec, when scope is fuzzy, or when TDD should drive the work.

### Subagents and parallel work

Read [subagents-and-parallelism.md](./references/subagents-and-parallelism.md) for controller and worker patterns, review loops, and safe parallelization.

### Reviews, comments, and PR feedback

Read [reviews-and-comments.md](./references/reviews-and-comments.md) when reviewing code, receiving review feedback, or addressing GitHub, Sentry, or CI comments.

### Observability and debugging

Read [observability.md](./references/observability.md) before adding logs or instrumentation, and whenever debugging should start from existing signals instead of guesswork.

### Backend execution

Read [backend-development.md](./references/backend-development.md) for service-layer, data-model, API, async, and architecture heuristics.

### Frontend execution

Read [frontend-development.md](./references/frontend-development.md) for framework boundary detection, reusable component design, UI implementation, refactor workflow, async UX, accessibility, responsive quality, performance priorities, and analytics.

### Verification and completion

Read [verification-and-finish.md](./references/verification-and-finish.md) before declaring success, opening or merging a PR, or cleaning up a branch or worktree.

## Standard Execution Loop

1. Orient: inspect repo instructions, architecture, git state, and current task context.
2. Classify: decide whether this is implementation, architecture analysis, debugging, review, refactor, instrumentation, or release work.
3. Anchor: find the existing owner of the behavior and the minimal safe change surface.
4. Implement: make the smallest coherent change that solves the right problem, not just the nearest symptom.
5. Verify: run the focused proof first, then any broader regression evidence the repo or user expects.
6. Compound: surface follow-up risks, documentation updates, rollout notes, or cleanup the next engineer will need.

## Skill Orchestration

If the current environment exposes more specialized skills, route work through them instead of bloating this skill:

- Use `create-plan` when the user explicitly asks for a plan.
- Use `quality-assurance` when verification strategy, flaky tests, review findings, or CI triage becomes the bottleneck.
- Use `gh-address-comments` for GitHub review-thread triage and inline replies.
- Use `gh-fix-ci` when GitHub Actions checks are failing.
- Use dedicated component-building, frontend-design, refactoring, browser-testing, observability, analytics, or release skills when they exist. Otherwise, use the references in this skill.

## Completion Hook

If the host supports stop hooks or pre-finish hooks, wire in [check-completion.sh](./hooks/check-completion.sh). The hook blocks premature stopping and forces a final pass over the original request, plan or spec state, verification evidence, recent errors, and integration cleanup.

Example Claude-style hook registration:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/agentic-development/hooks/check-completion.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Set `AGENTIC_DEV_MAX=0` for no continuation cap, or any positive integer to limit repeated stop interceptions.
