---
name: bmad
description: >-
  Use this skill to run BMad (Breakthrough Method of Agile AI-Driven Development) as a
  harness-agnostic control-plane protocol that turns human intent into bounded,
  inspectable, resumable agent work. Compress intent into a five-field contract (Why,
  Capabilities, Constraints, Non-goals, Success signal); classify work as
  direct/bounded/initiative and route to the smallest safe path; carry decisions in
  durable artifacts; review as triage; route failure to the layer where ambiguity
  entered; and gate autonomy on observable acceptance with machine-readable status
  (draft/ready-for-dev/in-progress/in-review/done/blocked). Use when a change request,
  feature, delegated build, or multi-agent epic needs intent capture, bounded
  implementation, review, and resumability in any agent harness. Do not use for
  validating whether a problem is real (product-discovery), shaping bets before
  planning (product-shaping), formal spec/gate pipelines (spec-driven-development),
  or the issue-to-PR delivery flow (neckbeard).
license: MIT
metadata:
  source: https://github.com/magnus919/agent-skills/tree/main/bmad
  tags: bmad, bmad-method, agentic-engineering, intent-contract, spec, work-classification,
    review-triage, autonomy, dark-factory, control-plane, bounded-work, human-in-the-loop
---

# BMad: Intent-to-Delivery Control-Plane Protocol

BMad is a software-delivery method built on one idea: human intent should be
progressively clarified, recorded, reviewed, and handed to agents as durable context
rather than improvised in chat. This skill turns that method into a protocol any
agent harness can follow — no official BMad installer required.

The loop: **classify** the request → **compress** intent into a contract → **route**
to the smallest safe path → **implement** one bounded unit → **review** as triage →
**route failure** to the layer where ambiguity entered → **gate autonomy** on
observable acceptance → **learn** from completed work.

## When to use this skill

Load when a change request, feature, bug report, delegated build, or multi-agent epic
needs:

- intent capture before implementation — a contract, not a vibe;
- a decision about how much ceremony the work deserves;
- durable artifacts so work is resumable across sessions or agents;
- review that triages findings instead of enumerating noise;
- autonomy that stops safely when the boundary is unsafe.

## Work classification (smallest safe path)

| Class | Shape | Process |
|---|---|---|
| Direct | clear goal, local change, established patterns, small blast radius | implement immediately after minimal clarification |
| Bounded | coherent change needing a short contract and plan | intent contract → plan → implement → review |
| Initiative | cross-component, multi-story, high-risk, or strategically uncertain | analysis → planning → solutioning → implementation → learning |

Load [references/classification.md](references/classification.md) for the decision
table, the one-question rule, and stop conditions.

## The intent contract (five fields)

For bounded or initiative work, establish a contract before implementation:

1. **Why** — the outcome and why it matters.
2. **Capabilities** — what the system must be able to do.
3. **Constraints** — technical, operational, legal, security, privacy, time, cost, organizational boundaries.
4. **Non-goals** — what is explicitly out of scope.
5. **Success signal** — how we will know the result works and is acceptable.

If a field is materially ambiguous, ask **one** high-leverage question, propose a
recommended answer, and wait for the decision. For trivial changes the contract can be
five bullets in conversation; for larger work it becomes a versioned spec file.

Load [references/spec.md](references/spec.md) for SPEC authoring and the status
vocabulary. Templates: [templates/SPEC.md](templates/SPEC.md) and
[templates/INTENT.md](templates/INTENT.md).

## The canonical loop

1. Inspect the repository and available context before asking anything.
2. Classify the work; state the proposed route.
3. Establish or resume the intent contract; ask at most one material question.
4. Present a plan for non-trivial work; wait at the approval checkpoint.
5. Implement the smallest coherent change; run focused tests first, then broader checks.
6. Review for correctness, scope, security, regressions, maintainability.
7. Repair findings that belong to this change; defer unrelated findings explicitly.
8. Report intent, behavior, files, risk, verification, findings disposition, and an accept / rework / investigate choice.

## Spec status vocabulary

Machine-readable status for resumable work:

| Status | Meaning |
|---|---|
| `draft` | Spec exists but is not ready |
| `ready-for-dev` | Passed readiness; ready to implement |
| `in-progress` | Implementation underway |
| `in-review` | Review or triage underway |
| `done` | Workflow completed successfully |
| `blocked` | Cannot safely continue unattended |

`blocked` is a routing signal, not failure: a higher-level orchestrator, another
workflow, or a human takes over. Validate a spec deterministically with
[scripts/check-spec.py](scripts/check-spec.py).

## Failure routing

When something is wrong, diagnose the layer where the failure entered:

| Failure | Route |
|---|---|
| Wrong outcome or wrong problem | intent / analysis |
| Missing or contradictory requirement | contract / planning |
| Conflicting technical approach | architecture |
| Incorrect local code | implementation |
| Insufficient test or evaluation | verification |
| Unrelated pre-existing issue | defer explicitly |
| Unsafe ambiguity | block and ask |

Do not keep patching code when the specification is the real problem.

## Autonomy gate

Autonomous execution is allowed only when all of these hold: intent contract coherent,
acceptance observable, boundary explicit, repository safe to modify, tests or
evaluations runnable, durable status writable, escalation defined. During autonomous
work: one coherent change at a time; never expand scope on unrelated improvements;
never merge, deploy, or change external systems without authorization; stop on intent
gaps, missing capability, destructive ambiguity, failed verification, or
non-convergent repair.

## Reference files

| Reference | Load when |
|---|---|
| [references/protocol.md](references/protocol.md) | You need the full paste-ready operating protocol for an agent |
| [references/classification.md](references/classification.md) | Classifying a request or choosing ceremony depth |
| [references/spec.md](references/spec.md) | Writing or resuming a SPEC / intent contract |
| [references/lifecycle.md](references/lifecycle.md) | Running an initiative through all four phases |
| [references/project-context.md](references/project-context.md) | Setting up or auditing repository rules (AGENTS.md) |
| [references/review-and-failure-routing.md](references/review-and-failure-routing.md) | Running a review or diagnosing a failure |
| [references/autonomy.md](references/autonomy.md) | Configuring or running autonomous (Build Auto) work |
| [references/party-mode.md](references/party-mode.md) | Deliberation, trade-offs, design debates, post-mortems |
| [references/adoption.md](references/adoption.md) | Adopting the protocol incrementally or mapping to a dark factory |

## Templates

| Template | Purpose |
|---|---|
| [templates/SPEC.md](templates/SPEC.md) | Versioned machine contract for bounded/initiative work |
| [templates/INTENT.md](templates/INTENT.md) | Lightweight five-field contract for bounded work |
| [templates/STORY.md](templates/STORY.md) | One bounded, dispatchable work unit |
| [templates/REVIEW.md](templates/REVIEW.md) | Final human checkpoint: intent → behavior → risk → verification |

## Scripts

| Script | When to run |
|---|---|
| [scripts/check-spec.py](scripts/check-spec.py) | After writing or editing a spec: validate five fields + status vocabulary (stdlib only, `--json` output) |

## Routing to adjacent skills

- **Upstream (before BMad):** `product-discovery` validates whether a problem is real;
  `product-shaping` sets an appetite and produces a pitch; `product-strategy` and
  `product-roadmapping-and-portfolio` frame strategic context.
- **Downstream (during BMad):** `spec-driven-development` for formal spec/gate
  pipelines; `implementation-planning` for a dependency-aware delivery plan;
  `adr-authoring` for architecture decisions; `software-architecture-analysis` for
  reverse-engineering an existing codebase.
- **Execution and gates:** `neckbeard` for the issue-to-PR delivery flow;
  `verification-methodology` for acceptance evidence; `qa-methodology` for test
  strategy; `agent-evals-and-observability` for independent evaluators; `agent-council`
  for Party-Mode-style multi-agent deliberation; `release-engineering` for deployment
  gates; `kanban-guru` for backlog and dispatch policy.

## When not to use

- **The problem itself is unvalidated** → `product-discovery`. BMad compresses intent;
  it does not establish whether the problem is real.
- **No decision yet on how much the work is worth** → `product-shaping` first (appetite,
  pitch, bet). BMad starts from a placed intent.
- **You need a formal spec format plus phase gates as the factory pipeline** →
  `spec-driven-development` owns SPEC format and gate mechanics; BMad provides the
  control-plane protocol around them.
- **You are executing an issue-to-PR delivery flow with its own gates** → `neckbeard`.
  BMad complements it; do not run two competing delivery lifecycles.
- **You need independent review** → role-play is not independence. Use `agent-council`,
  separate evaluators, or `agent-evals-and-observability`; never claim persona
  separation as independent review.
- **Operating the official BMad installer/tooling** → this skill emulates the method;
  it does not install or operate bmad-method npm packages.

## Version drift and attribution

BMad is actively evolving (official repository: bmadcode/bmad-method; BMAD™ and
BMAD-METHOD™ are trademarks of BMad Code, LLC). Older articles differ on name
expansion, agents, file names, and commands. When installing the official tooling,
treat the official docs and installed source as authoritative. This skill is an
original distillation of the method as a harness-agnostic protocol; it does not
reproduce official installer content.
