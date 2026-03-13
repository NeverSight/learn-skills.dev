---
name: agently-triggerflow
description: Use when the user needs workflow orchestration such as branching, concurrency, approvals, waiting and resume, runtime stream, restart-safe execution, mixed sync/async function or module orchestration, event-driven fan-out, process-clarity refactors that make stages explicit, performance-oriented refactors that collapse split requests, or explicit draft-review-revise style multi-stage flows. The user does not need to say TriggerFlow explicitly.
---

# Agently TriggerFlow

Use this skill when the solution clearly needs orchestration semantics rather than one request family.

The user does not need to say TriggerFlow or Agently. Scenario language such as resumable approval flow, branching automation, output-fan-out refactor, mixed sync/async pipeline, process-clarity refactor, or draft-review-revise pipeline should still route here once orchestration is clearly the owner layer.

## Native-First Rules

- prefer TriggerFlow for explicit multi-stage quality loops, branching, concurrency, waiting/resume, restart-safe execution, output-fan-out performance refactors, process-clarity refactors, or mixed sync/async orchestration
- keep workflow stages visible instead of hiding nested request loops
- combine with `agently-model-response` when one workflow step must reuse one model result as text, parsed data, metadata, or partial updates
- combine with `agently-output-control` when downstream branches need stable structured fields or required keys

## Anti-Patterns

- do not invent a custom event bus or state machine before checking TriggerFlow
- do not hide draft/judge/revise or similar loops inside one opaque helper

## Read Next

- `references/overview.md`
