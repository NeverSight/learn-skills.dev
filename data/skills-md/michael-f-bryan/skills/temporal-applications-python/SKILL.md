---
name: temporal-applications-python
description: Design, implement, and refactor high-quality Temporal workflows and activities in Python. Use when building or changing Temporal Python applications; when designing activities (injectable deps, Pydantic params/result, business logic outside); when implementing workflows with dynamic inputs or Continue-As-New; or when configuring reliability (timeouts, retries, idempotency), determinism, or testing. Covers boundaries, typed contracts, bounded history, and progressive disclosure via resources.
---

# Temporal Applications in Python

Guidance for designing and implementing Temporal workflows and activities in Python so they are testable, type-safe, reliable, and keep orchestration separate from business logic. Use this skill when **designing** new workflows or activities, **refactoring** or **extending** existing ones, or when you need patterns for determinism, timeouts, retries, idempotency, or testing.

**Load the skill first; then use the Resource index below to load only the resource(s) relevant to your task.**

---

## When to use this skill

- You are building or changing **Temporal Python** applications (workflows and activities on the official Python SDK).
- Tasks include: defining activity classes and workflow logic; structuring params and results; implementing long-running or unbounded workflows (e.g. processing a growing list with Continue-As-New); configuring timeouts, retries, and idempotency; ensuring workflow determinism; or testing workflows and activities.

**Next step:** Infer your task from the user request, then use the **Resource index** table below to choose which `resources/` file(s) to load.

---

## Boundaries

1. **Workflows** — Orchestrate only. No I/O or non-deterministic APIs in workflow code. Use SDK APIs for time/random/UUID. State that must survive Continue-As-New lives in a **serialisable params model**; copy from params into workflow instance at the start of `run`. Details and examples → [resources/workflows-continue-as-new.md](resources/workflows-continue-as-new.md), [resources/determinism.md](resources/determinism.md).

2. **Activities** — Thin wrappers. Dependencies (DB, HTTP client, browser, etc.) are **injected at construction** (e.g. in worker bootstrap). Each activity method has **one Pydantic params type** and **one result type**; no tuples or multiple return values. **Business logic** lives in a separate, testable module or function that the activity calls. Details and examples → [resources/activities.md](resources/activities.md).

3. **Child workflows vs activities** — Use **child workflows** for per-item orchestration (e.g. one child per item in a batch); use **activities** for side effects (I/O, external APIs). Keep history small by extracting loops into child workflows and passing state via params when using Continue-As-New.

---

## Success criteria

Before considering the work done, check:

- [ ] **Boundaries** — Workflows orchestrate only; activities are thin wrappers with injected deps and single params/result models; business logic is in separate, testable code.
- [ ] **Contracts** — Pydantic params and result models; shared types between workflows and activities; serialisable workflow state in params for Continue-As-New.
- [ ] **Determinism** — No I/O or non-deterministic APIs in workflow code; use `workflow.now()`, `workflow.random()`, `workflow.uuid4()`; version workflow changes with patching when needed. See [resources/determinism.md](resources/determinism.md).
- [ ] **Bounded history** — Long-running or unbounded list/queue workflows use Continue-As-New with state in params; drain in-flight work before `continue_as_new` when using N-in-flight. See [resources/workflows-continue-as-new.md](resources/workflows-continue-as-new.md).
- [ ] **Reliability** — Start-to-close timeout set for activities; schedule-to-close and retry policy as needed; heartbeats for long activities; idempotent design for side-effecting activities. See [resources/reliability.md](resources/reliability.md).
- [ ] **Testability** — Business logic testable without Temporal; activity/workflow tests use ActivityEnvironment and time-skipping WorkflowEnvironment as appropriate. See [resources/testing.md](resources/testing.md).

---

## Resource index

Load **only** the resource(s) that match your task. SKILL.md (this file) is the entry point; resources hold the detailed guidance and examples.

| Intent / task                                                                                                 | Resource(s) to load                                                                                                                                                                                                                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Design or refactor an **activity** (class shape, deps, params/result, thin wrapper, heartbeats)               | [resources/activities.md](resources/activities.md)                                                                                                                                                                                                                                                                                              |
| Design or refactor an activity and care about **timeouts, retries, or idempotency**                           | [resources/activities.md](resources/activities.md) + [resources/reliability.md](resources/reliability.md)                                                                                                                                                                                                                                       |
| Implement or refactor a **workflow** with a list/queue, long-running, or **Continue-As-New**                  | [resources/workflows-continue-as-new.md](resources/workflows-continue-as-new.md)                                                                                                                                                                                                                                                                |
| Workflow code rules: **determinism**, replay, what’s allowed in workflow vs activity, **versioning/patching** | [resources/determinism.md](resources/determinism.md)                                                                                                                                                                                                                                                                                            |
| **Timeouts**, **retries**, heartbeats, or **idempotency** for activities                                      | [resources/reliability.md](resources/reliability.md)                                                                                                                                                                                                                                                                                            |
| **Testing** activities, workflows, or replay (ActivityEnvironment, WorkflowEnvironment, Replayer)             | [resources/testing.md](resources/testing.md)                                                                                                                                                                                                                                                                                                    |
| Refactor existing workflow/activity (determinism, replay, testability)                                        | [resources/workflows-continue-as-new.md](resources/workflows-continue-as-new.md) and/or [resources/activities.md](resources/activities.md) + [resources/determinism.md](resources/determinism.md) + [resources/testing.md](resources/testing.md); add [resources/reliability.md](resources/reliability.md) if timeouts/idempotency are involved |
| General “build a Temporal Python app”                                                                         | Start with this SKILL; add resources by sub-task (activity design → activities.md; workflow with list → workflows-continue-as-new.md; etc.)                                                                                                                                                                                                     |

**Cross-references:** Resources may point to other resources (e.g. “For idempotency see reliability.md”). Load those when the task requires it.

---

## Out of scope

- **Worker bootstrap** — Wiring task queues, registering workflows/activities, and process lifecycle are not covered here; see SDK and deployment docs.
- **Signals** — Pushing data into running workflows via signals is not detailed; use SDK docs when needed.
- **Saga/compensation, search attributes, local activities** — Out of scope for this skill; refer to Temporal docs for advanced patterns.
