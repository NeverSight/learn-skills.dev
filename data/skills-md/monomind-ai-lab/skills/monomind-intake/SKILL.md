---
name: monomind-intake
description: "Clarify ambiguous product or engineering work into a confirmed intent brief. Use when a request lacks a clear user, outcome, success signal, binding constraint, or non-goals; when the user asks to stress-test an idea; or when a named solution such as a dashboard may not solve the real problem. Skip mechanical edits and already-specified work."
---

# Monomind Intake

Resolve the decisions that would materially change the work before producing a spec or implementation. Finding repository facts is the agent's job; choosing product intent and tradeoffs belongs to the user.

## Build the decision tree

1. Inspect the smallest amount of project evidence needed to distinguish facts from choices. Read local instructions and relevant existing behavior; do not ask the user for facts that inspection can answer.
2. State a one-sentence hypothesis of the intended outcome, an honest confidence estimate, and what is still missing.
3. Map the open decisions as a tree. A decision enters the **frontier** only when its prerequisites are settled.
4. Ask from the frontier. Attach a recommended answer and the concrete tradeoff to every question.
   - Ask one question when its answer will reshape later questions.
   - Batch only mutually independent frontier questions.
   - Do not turn preference decisions into technical fact-finding.
5. Probe conventional solution language. If the request names an artifact such as a dashboard, service, rewrite, or migration, test whether that artifact is the goal or merely the first familiar solution.
6. Recompute the frontier after each answer. Stop when every outcome-changing branch is resolved or explicitly marked open.

## Confirm the intent brief

Restate the result in the user's vocabulary:

```markdown
## Intent

- User or operator:
- Problem and why now:
- Desired outcome:
- Success evidence:
- Binding constraints:
- Out of scope:
- Open decisions:
```

For work with meaningful cost, external effects, or several plausible outcomes, obtain explicit confirmation before treating the brief as authoritative. For small reversible work, surface the remaining assumption and proceed when the user's request already supplies enough direction.

Persist the brief only when the user requests a durable artifact or the work will span sessions. Do not silently turn intake into a spec, task list, or implementation.

## Completion criteria

- The intended user, outcome, success evidence, constraint, and non-goals are either known or visibly open.
- Technical facts came from project evidence or a cited current source.
- No unresolved decision is being disguised as an implementation assumption.
- The next activity—specification, planning, or direct execution—is unambiguous.
