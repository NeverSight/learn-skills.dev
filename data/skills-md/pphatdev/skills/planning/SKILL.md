---
name: planning
description: Load this skill when turning a goal, request, or research findings into an executable plan - scope, sequencing, milestones, risks, and per-step acceptance criteria. Load before starting any multi-step change.
user-invocable: true
---

# Planning

Category: Design (Product) - Strategy

## Purpose

Convert a goal into a sequenced plan where every step is independently
verifiable and the endpoint is defined before work starts.

## Workflow

1. **Restate the goal.** One paragraph: what will be true when this is done
   (acceptance criteria), and what is explicitly out of scope (non-goals).
   If you cannot write the acceptance criteria, the goal is not ready to
   plan - clarify first.
2. **Inventory the surface.** List what the work touches: files, callers of
   those files, tests that exercise them, data or schemas affected, and
   anything that must not change. Read before listing - a plan built on an
   unexamined codebase is fiction.
3. **Decompose.** Break the work into steps small enough that each one can
   be verified on its own (a test, a command, an observable behavior). A
   step that cannot be verified alone is two steps.
4. **Sequence.** Order by dependency; mark which steps can run in parallel.
   Put riskiest and least understood steps early - cheap to fail, cheap to
   replan.
5. **Identify risks.** For each risk: the trigger, the mitigation, and the
   fallback (fix-forward vs. rollback). Include blast-radius actions
   (migrations, deploys, deletions) explicitly; they need approval.
6. **Present.** Numbered plan, per-step verification, risks, and assumptions
   the plan depends on but has not validated.

## Output

- Numbered plan with a verification method per step.
- Acceptance criteria and non-goals.
- Risks with mitigations; assumptions labeled as such.
- Rollback or abort condition for the whole plan.

## Anti-patterns

- Plans whose steps have no verification - "done" becomes a mood.
- Scope creep disguised as thoroughness (refactors nobody asked for).
- Estimating without stating assumptions; give ranges and the assumptions
  behind them, not false precision.

## Escalate when

- A step requires an action with blast radius (deploy, migration, force
  operations) - get explicit approval for that step.
- The plan depends on unvalidated assumptions about systems you cannot
  inspect - say which ones before starting.
