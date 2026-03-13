---
name: wave-planner
description: Plan and execute large multi-step, multi-stack changes with contract-first waves, parallel worker ownership, user approval gates, ordered integration, and final verification/docs updates. Use only when the task spans multiple areas (for example frontend, backend, tests, errors, docs) or has dependency-heavy sequencing.
---

# Wave Planner

Create and run a Wave-Driven Development plan for large, cross-stack tasks.

## Objective

Produce:
- Vision and scope boundaries
- Decision Log
- Wave 0 contracts
- Wave 1..N parallel implementation waves
- Integration wave
- Final verification wave
- Documentation update step
- Ready-to-send worker prompts and execution checklist

## Workflow

1. Decide whether to use this skill:
- Use only if work is large, multi-step, and touches multiple parts/stacks.
- If not large enough, do not use this skill.
2. Ask for Gate 1 user approval before planning:
- Send a short reason: "I recommend Wave method because <short reason>. Do you agree?"
- Stop until user accepts or declines.
3. If accepted, draft the plan:
- Clarify done criteria and out-of-scope.
- Build Decision Log (naming, API shape, error model, logging, tests, style constraints).
- Define Wave 0 contracts first (types/interfaces/schemas, boundaries, API shapes, constants, flags/migrations).
4. Choose wave and agent count with balancing rules:
- Use the minimum number of waves that still avoids conflicts.
- Group independent tasks into the same wave.
- Move dependency-bound tasks to later waves.
- Keep each worker task medium-sized (not tiny and not overloaded).
- Ensure each worker has explicit file/module ownership.
5. Produce a one-line execution preview before full detail:
- One line per wave.
- One line per worker with task summary.
6. Produce the full plan with complete shared context:
- Include full vision and all waves so each worker sees global intent.
- Include worker-specific goals, files, constraints, and verification.
- Include explicit wave order for execution (Wave 0, then Wave 1..N, then Integration, then Final Verification, then Docs).
7. Ask for Gate 2 user approval before execution:
- "Plan is ready. Execute now?"
- Stop until user accepts or declines.
8. If accepted, load and use `acpx` skill, then execute:
- Use `acpx` to create/run named sessions per worker in current wave.
- Run workers in parallel inside a wave, but execute waves sequentially.
- Wait for all workers in wave to finish and validate handoffs before next wave.
- Close worker sessions after completion.
9. After all waves:
- Main agent reviews merged result and runs verification tests.
- Main agent updates existing docs if needed, or adds new docs for new features.
- Follow existing documentation format and conventions.

## Global Rules

- Gating rule: planning and execution require explicit user approvals (Gate 1 and Gate 2).
- Ownership rule: workers edit only assigned files.
- Dependency rule: if outside scope is needed, return a Dependency Note instead of editing.
- Consistency rule: follow existing repo patterns; do not invent new architecture unless requested.
- Verifiability rule: each worker includes at least one concrete verification method.
- Ordering rule: wave order is strict; do not start next wave early.
- Session rule: one named session per worker; close finished sessions.
- Docs rule: docs update is mandatory in final step (update existing docs or add new).

## Model Routing Configuration

Read `templates/model-routing.md` before choosing models.

Rules:
- Classify each worker task as `hard`, `middle`, or `easy`.
- Select the first available model from that class's ordered list.
- If a model fails/unavailable, fallback to the next model in order.
- If placeholder guidance still exists in routing config, stop and tell user to edit routing first.

## Mandatory Worker Handoff Format

1. Summary (1-3 lines)
2. Files changed (exact list)
3. Patch/diffs (or exact edits)
4. How to test (commands + expected result)
5. Risks/TODOs/Dependency Notes
6. Main plan log entry (what to append to shared execution log)
7. Completion marker: `WAVE {WAVE_ID} / {AGENT_NAME} DONE`

## Output Contract

Always output the final plan using this section order:
- A) Vision
- B) Decision Log
- C) Contracts (Wave 0)
- D) Waves (1..N with agents)
- E) Integration + Final Verification + Docs
- F) Worker prompts
- G) Execution checklist (acpx sessions + wave order)

Use templates from `templates/` when helpful.
