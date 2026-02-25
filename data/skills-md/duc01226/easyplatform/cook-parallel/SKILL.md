---
name: cook-parallel
description: '[Implementation] ⚡⚡⚡ Parallel implementation - multiple tasks simultaneously'
argument-hint: [tasks]
---

Execute these tasks in parallel for maximum efficiency:
<tasks>$ARGUMENTS</tasks>

**Mode:** PARALLEL - Multiple subagents working concurrently.

## ⚠️ Anti-Hallucination Reminder

**Before modifying ANY code:** Verify assumptions with actual code evidence. Search for usages, read implementations, trace dependencies. If confidence < 90% on any change, investigate first or ask user. See `.claude/skills/shared/anti-hallucination-protocol.md` for full protocol.

## Workflow

### 1. Task Decomposition

- Analyze tasks for independence
- Group into parallelizable work units
- Identify dependencies between units
- Create dependency graph

### 2. Parallel Research (if needed)

Launch multiple `researcher` subagents simultaneously:

```
Task A research ──┐
Task B research ──┼──► Synthesis
Task C research ──┘
```

### 3. Parallel Planning

- Use `planner` subagent with synthesized research
- Create plan with parallel-safe phases
- Mark file ownership boundaries (prevent conflicts)

### 4. Parallel Implementation

Launch multiple `fullstack-developer` subagents:

```
Phase 1 (Backend API) ──┐
Phase 2 (Frontend UI) ──┼──► Integration
Phase 3 (Tests)       ──┘
```

**Critical:** Each subagent must stay within file ownership boundaries.

### 5. Integration & Testing

- Merge parallel outputs
- Use `tester` subagent for integration tests
- Use `debugger` if integration issues found

### 6. Review & Report

- Use `code-reviewer` for final review
- Consolidate all changes
- Report to user

## Parallelization Rules

| Rule                 | Description                                    |
| -------------------- | ---------------------------------------------- |
| **File Ownership**   | Each subagent owns specific files - no overlap |
| **Dependency Order** | Respect dependency graph                       |
| **Max Concurrent**   | 3 subagents max to prevent conflicts           |
| **Sync Points**      | Integration checkpoints between phases         |

## When to Use

- Multi-component features (backend + frontend)
- Large refactoring across independent modules
- Parallel test writing
- Documentation updates alongside code

## Example Task Split

```
"Add user authentication with login UI"
├── Backend API (subagent 1)
│   ├── auth-controller.ts
│   └── auth-service.ts
├── Frontend UI (subagent 2)
│   ├── login-page.component.ts
│   └── login-form.component.ts
└── Tests (subagent 3)
    ├── auth.spec.ts
    └── login.e2e.ts
```

## Trade-offs

| Aspect       | Parallel             | Sequential |
| ------------ | -------------------- | ---------- |
| Speed        | ~2-3x faster         | Baseline   |
| Coordination | Higher complexity    | Simple     |
| Conflicts    | Risk of merge issues | None       |
| Context      | Split across agents  | Unified    |

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
