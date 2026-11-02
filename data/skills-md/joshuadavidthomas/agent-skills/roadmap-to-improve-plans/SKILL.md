---
name: roadmap-to-improve-plans
description: Use when turning a roadmap, repo priorities, architecture priorities, chosen opportunities, accepted feature outlines/plans, or “roadmap to plans” request into grouped improvement plan batches for future executors. Writes README.md indexes, 001-*.md/NNN-style plans, optional memo-*.md files, verification gates, drift checks, STOP conditions, rejected approaches, and executor handoff notes.
---

# Roadmap to Improve Plans

Turn selected strategic-roadmap opportunities or accepted feature slices into grouped batches of numbered improvement plans. This is the wide planning stage: preserve the audit judgment, feature decisions, and architecture diagnosis behind each selected item, then turn it into enough detail for future executors to work safely.

Treat plan writing as meta-work: the output should improve future execution loops by carrying forward impact, risk, confidence, design claims, regression checks, approval boundaries, and STOP conditions.

This owns this pipeline's NNN plan-bank contract directly.

## Source Frame

Before writing plans, load what applies:

- The selected `.agents/ROADMAP.md` or equivalent roadmap/opportunity artifact.
- Accepted feature-planning artifacts when splitting a feature outline or final plan into PR-sized improvement plans.
- `improve` for the original audit posture: category, evidence, impact, effort, risk, confidence, fix sketch, and “not worth doing” verdicts.
- The `coding-standards` skill as the canonical source for standards concerns. Load only the reference files matching the selected work; do not copy the standards into this skill or the plan.
- `improve-codebase-architecture` for architecture/deepening candidates: current friction, shallow-module diagnosis, deletion test, locality/leverage, and recommendation strength.
- DLS-style exemplar plans when present in the target repo, especially effort indexes, numbered plans, memos, rejected/deferred notes, and reconciliation logs.
- Project docs and commands: `AGENTS.md`, `README.md`, `CONTEXT.md`, architecture docs, ADRs, package/test config, CI config, and current VCS state.

## Workflow

1. **Select plan scope**
   - Start from selected roadmap items, accepted feature artifacts, or ask the user which items to plan.
   - Treat one effort directory as one improvement batch: one theme, one outcome, one README index.
   - Split unrelated projects, features, or outcomes into separate batches.
   - Preserve dependency order from the roadmap or feature outline; do not flatten everything into parallel tasks.

2. **Reconcile current state**
   - Read current project instructions and existing plans.
   - Check current VCS state and active branch/bookmark so the plan does not assume stale code.
   - Re-open source evidence from the roadmap before planning; old roadmap citations are leads, not facts.
   - Identify exact validation commands and any missing verification baseline.
   - Carry forward the roadmap's definition of “better”; if missing, define the plan-bank success criteria before decomposing work.
   - If credentials or secrets appear, reference only the file path, line, and credential type; never copy secret values into plans.

3. **Decompose into numbered plans**
   - Each `NNN-*.md` should be independently landable or have an explicit dependency on an earlier plan.
   - Preserve the source audit frame for roadmap/audit opportunities: audit category, impact, effort, risk, confidence, evidence, and fix sketch or direction.
   - Preserve the source feature frame for accepted feature artifacts: source design/outline, accepted decisions, phase/slice, dependencies, verification, and implementation routing.
   - Prefer vertical slices over layer-by-layer rewrites.
   - Include architecture/deepening language when relevant: module, interface, depth, seam, adapter, leverage, locality.
   - For architecture plans, carry forward the diagnosis: current friction, deletion test result, locality/leverage claim, recommendation strength, and ADR conflicts if any.
   - Do not pretend an unresolved seam or interface decision is implementation-ready. Route it to `feature-planning-artifacts`, a research/spike plan, or a memo instead.
   - Use the `coding-standards` skill to name the standards concern and design claim each plan protects.

4. **Write the effort index and plans**
   - Prefer `.agents/plans/improvements/<effort-slug>/` unless the repo already has an established planning convention.
   - Use [references/index-template.md](references/index-template.md) for `README.md`.
   - Use [references/plan-template.md](references/plan-template.md) for each numbered plan.
   - Use [references/memo-template.md](references/memo-template.md) only when a design fork or handback needs a durable answer.
   - Choose the next available `NNN-` prefix by inspecting the destination directory.

5. **Mark deeper-planning candidates and autonomy boundaries**
   - In the effort index, mark plans that deserve deeper feature-planning treatment because the audit confidence is low, the architecture shape is unsettled, the recommendation is speculative, or user decisions are required.
   - For each plan, state what can be done as routine execution, what needs design review, and what requires human approval.

## Plan Requirements

Every numbered plan must be self-contained for an executor with no planning-session context. Assume competence at following explicit instructions and weakness at filling gaps. Each plan must include:

- source frame: roadmap/audit category, impact, effort, risk, confidence, and fix sketch or direction when available; feature artifact, accepted decision, and slice dependency when splitting a feature;
- standards concern from the `coding-standards` skill, when the plan changes code shape;
- purpose and payoff;
- definition of “better” for this plan;
- current-state evidence with paths and line ranges where possible;
- desired end state;
- scope and out of scope;
- implementation sequence at PR-sized granularity;
- exact automated verification commands;
- evals or regression checks that catch the change getting worse;
- manual verification only when it proves something automation cannot;
- autonomy boundary for routine execution, design review, and human approval;
- drift checks to run before implementation;
- STOP conditions for stale assumptions, missing commands, design forks, or failed validation;
- rejected approaches and why they are not being used;
- executor handoff notes for a fresh executor.

Architecture plans must also include current friction, deepening direction, deletion-test result, locality/leverage claim, and recommendation strength. If those are unknown, the plan is not ready for routine implementation.

## Guardrails

- Do not implement source changes.
- Do not write giant all-or-nothing plans.
- Do not hide unresolved design questions in TODO prose; either stop for deeper planning or write a memo request.
- Do not turn speculative architecture into implementation instructions; preserve the uncertainty and route it to design review.
- Do not leave recurring decisions as repeated advice; turn them into a policy, memo, ADR suggestion, or plan-bank rule when durable.
- Do not keep old shapes by default. Prefer the intended end state unless migration compatibility is required.
- Do not invent validation commands. If commands are unknown, make establishing the verification baseline an explicit first plan or STOP condition.
- Do not copy secrets into plans, even as evidence.

## Done Criteria

The effort is done when the index explains plan order and readiness, each numbered plan can be handed to a fresh executor, and low-confidence or unsettled architecture work is flagged for deeper planning or design review instead of being marked ready prematurely.
