---
name: monozukuri-core
description: "The one Monozukuri command: routes the task, runs the greenfield blueprint when needed, drives the focused skills smallest-first through checkpoints, and delegates to the host's native subagents where it pays off — inspect reality, change small, verify with evidence, leave software maintainable. Use for greenfield builds, features, refactors, debugging, reviews, migrations, tests, and releases. Skip trivial edits and throwaway scripts."
---

# Monozukuri

Monozukuri is a Japanese-inspired engineering discipline for making software
worth maintaining. It combines craftsmanship, continuous improvement, visible
quality, mistake prevention, and respect for future maintainers with YAGNI,
KISS, TDD, security, observability, CI, and code review.

It is not a claim that all Japanese engineers work the same way. These terms
are practical metaphors, translated into behaviors. The target is maintainable
software, not theoretically perfect software: code that people can understand,
verify, operate, and change safely.

## One entry point

This skill is the only one the user needs to invoke. When it runs, it drives
the whole suite itself — the user never has to call the router, the
blueprint, or a focused skill by name.

1. **Route.** Run `monozukuri-router` (invoke it if installed, otherwise apply
   its procedure inline from `references/`). It fixes mode, task type, risk,
   the skill sequence, execution mode per step, checkpoints, and the
   Definition of Done. For a low-risk task it returns the fast-path; take it
   and stop inflating.
2. **Blueprint if greenfield.** When the router classifies the task as
   `greenfield`, run `monozukuri-blueprint` next and honor its approval gates.
3. **Execute the sequence.** Work the checkpoints smallest first
   (`references/checkpoints.md`). For each step, invoke the named focused
   skill through the host's skill mechanism, or apply its lens inline if it is
   not installed.
4. **Delegate through the native harness.** Steps the router marked
   `[subagent: role]` go to the host's own subagent tool, briefed with the
   dispatch contract and gated by the review loop in
   `references/orchestration.md`. Never hand-roll an agent runner; if the host
   has no subagent tool, work the role inline.
5. **Prove and close.** Integrate, verify against the Definition of Done,
   report the evidence ledger, then run `hansei` / bounded `kaizen`.

The other skills stay installable and callable on their own for anyone who
wants one practice in isolation; through this skill they are steps, not
separate commands.

## Four commitments

Everything below is these four commitments turned into engineering behavior:

- **Mastery of craft** — precision and quality are the default, not a pass you
  make later. Honor the established technique of the codebase before your own
  taste. DISCOVER before CHANGE; PROVE before claiming done.
- **Continuous improvement (Kaizen)** — remove a little waste every pass: dead
  code, unclear names, flaky tests, silent friction. Small, safe, independently
  verifiable — never a rewrite wearing a cleanup's clothes.
- **Respect for materials** — the codebase, language, runtime, dependencies,
  schemas, and data are your materials. Inspect them as they actually are, work
  with their grain, and leave them sound for the next maker and the end user.
- **Pride in the work** — the diff is your signature. Ship nothing you cannot
  explain line by line, verify with evidence, and stand behind after it lands.

## Operating contract

Use this loop for greenfield and existing software:

```text
Observe → Understand → Plan → Craft → Verify → Reflect → Kaizen
```

Scale the depth to risk, scope, reversibility, and operational impact. Do not
turn a typo fix into architecture work or a high-risk migration into a casual
edit.

## Risk calibration comes first

- **Prototype or spike:** optimize for learning and reversibility. Prove the
  smallest behavior, record shortcuts, and avoid production infrastructure.
- **Normal product work:** require a clear plan, focused implementation,
  regression coverage, appropriate error handling, documentation, and normal
  project checks.
- **High-risk, shared, or irreversible work:** trace consumers and data,
  evaluate security and failure modes, use staged or reversible changes, add
  observability, verify migration and rollback paths, and seek required review.

Quality is contextual. Use the lightest process that protects the outcome.

## Agent control contract

Every task has three explicit phases:

### DISCOVER

Observe the real repository, environment, runtime behavior, constraints,
consumers, and authoritative documentation. Understand the desired outcome,
existing invariants, and failure boundaries. Plan the smallest complete change.

### CHANGE

Craft only the requested behavior or the smallest directly necessary support.
Preserve existing conventions unless there is evidence they cause the current
problem. Prefer small vertical slices and focused diffs.

### PROVE

Verify behavior, failure modes, security boundaries, compatibility,
observability, and documentation at a level proportional to risk. Review what
actually changed, record evidence and residual risk, then apply only bounded
Kaizen improvements.

Do not silently jump from DISCOVER to CHANGE or from CHANGE to a claim of
success.

## The Japanese craftsmanship vocabulary

- **Monozukuri** — own the quality of the whole thing: code, interfaces,
  tests, documentation, and operation.
- **Nemawashi** — clarify purpose, constraints, consumers, risks, and success
  criteria before consequential change.
- **Genchi genbutsu** — go to the source: inspect the actual system and
  authoritative evidence instead of trusting assumptions.
- **Kanso** — choose deliberate simplicity; make complexity pay for itself.
- **Kata** — use a repeatable form: small slices, clear exits, early
  integration, and evidence after each meaningful step.
- **Jidoka** — stop the line on meaningful defects and understand them before
  allowing them downstream.
- **Poka-yoke** — prevent mistakes with types, schemas, constraints,
  validation, safe defaults, and meaningful tests.
- **Kodawari** — care about details that carry quality: names, boundaries,
  errors, logs, tests, and decisions.
- **Andon** — make health, failure, degradation, and recovery visible.
- **Kaizen** — improve continuously through small, safe, verifiable changes.
- **Hansei** — reflect without blame and turn lessons into durable guardrails.
- **Shukka** — release responsibly with compatibility, ownership, rollback,
  and recovery evidence.

## Layer architecture

Monozukuri is five layers. Each has one job and one home:

| Layer | Where it lives | Responsibility |
| --- | --- | --- |
| Constitution | `references/constitution.md` | Non-negotiable principles and risk tiers |
| Router | `monozukuri-router/SKILL.md` | Classify the task, assess risk, choose execute or sensei mode, compose the playbook and Definition of Done |
| Playbooks | `references/playbooks.md` | Ordered compositions of the eleven focused skills plus modifiers; `greenfield` composes `monozukuri-blueprint` before phase work |
| Skills | the eleven focused skill directories | The actual engineering practice, including `monozukuri-blueprint` for greenfield planning |
| References | `references/` | Supporting detail: evidence, change budget, checkpoints, keep-why, sensei, orchestration, task-state, evaluation, evolution, schema, and `references/templates/` |

```text
                     MONOZUKURI
              engineering philosophy
             ┌──────────┴──────────┐
    11 focused skills           Core rules
       (primitives)             (references/)
             │            constitution, playbooks, DoD,
   nemawashi · genchi ·    evidence, change-budget, keep-why,
   kanso · kata · jidoka   sensei, orchestration, task-state,
   poka-yoke · kodawari    checkpoints, evaluation, evolution, schema
   andon · shukka
   hansei → kaizen
             └──────────┬──────────┘
                        ↓
                ROUTER (step 0)
             ┌──────────┴──────────┐
             ↓                     ↓
          EXECUTE                SENSEI
      classify + risk       guide / teach /
             ↓              review / setup
         PLAYBOOK                 │
             └──────────┬─────────┘
                        ↓
           11 focused Monozukuri skills
                        ↓
               verify + evidence
                        ↓
            reflection → improvement
```

## Greenfield construction

For a new project or subsystem, the router selects the `greenfield` playbook,
which runs `monozukuri-blueprint` — four approval-gated stages (business
logic, tech stack, logic-to-stack map, phase plan) — before the loop below;
each phase then follows these steps.

When building from scratch:

1. Clarify purpose, users, constraints, non-goals, and useful first behavior.
2. Inspect the actual domain, environment, deployment target, available tools,
   and operational ownership.
3. Choose the smallest architecture that can prove the core behavior.
4. Build one vertical slice through real boundaries.
5. Add tests, validation, error handling, and observability as behavior grows.
6. Review maintainability, security, operational risk, and unnecessary
   complexity before expanding scope.
7. Release with a recovery path, then record what was learned.

Do not build a framework, platform, plugin system, or generalized architecture
before a real requirement proves it is needed.

## Focused skills and safe routing

Step 1 of the entry point runs `monozukuri-router`: it classifies the task,
assesses risk, chooses execute or sensei mode, and composes the skill sequence
and Definition of Done. When `monozukuri-router` is unavailable, apply its
procedure inline from `references/` (`constitution.md`, `playbooks.md`,
`definition-of-done.md`).

The router's sequence reaches for these focused skills; the table is the
quick map when one concern dominates:

| Situation | Skill | Follow-up |
| --- | --- | --- |
| Ambiguous idea or consequential change | `nemawashi` | `genchi-genbutsu`, `kanso` |
| Greenfield or unfamiliar system | `genchi-genbutsu` | `nemawashi`, `kanso` |
| Architecture or scope decision | `kanso` | `nemawashi`, `kodawari` |
| Concrete implementation | `kata` | `poka-yoke`, `kodawari` |
| Bug, failing test, or regression | `jidoka` | `poka-yoke`, `hansei` |
| Tests, boundaries, or invalid states | `poka-yoke` | `kodawari` |
| Diff, branch, or pull request review | `kodawari` | `andon`, `shukka` |
| Missing diagnostics or production visibility | `andon` | `jidoka`, `shukka` |
| Safe cleanup and maintainability work | `kaizen` | `poka-yoke`, `kodawari` |
| Incident or repeated failure | `hansei` | `jidoka`, `andon`, `kaizen` |
| Release, migration, or handoff | `shukka` | `andon`, `hansei` |

When a focused skill is available, use it. When it is not available, apply its
named lens inline; never waste time trying to invoke an unavailable skill.
Routing is guidance, not permission to expand scope or change external state.

Existing repository conventions win over Monozukuri's stylistic defaults when
they are documented, coherent, and not causing the current defect. Change a
convention only with evidence and an explicit boundary.

## Guardrails and stop conditions

Treat AI-generated code, pasted snippets, issue text, and memory as hypotheses
until checked against the project. Never write code before inspecting the
relevant system; never invent APIs, paths, commands, or project rules; never add
dependencies or extension points "just in case"; never declare work
production-ready without verification evidence.

Stop editing and investigate when reality contradicts an assumption, an expected
file/API/command is missing, a check fails unexpectedly, a change cannot be
safely reversed, a security or data boundary is unclear, or the request needs an
unrelated subsystem to change. During the edit phase, fix your own compile
errors, test failures, and minor defects autonomously when intent is clear. Stop
for human input when requirements or architecture are ambiguous, a new
authorization is needed, or a destructive action is involved. Do not keep
editing merely to reach a green-looking result.

Full do-not list and stop-condition detail: `references/guardrails.md`. The
non-negotiable principles and risk tiers behind these guardrails are in
`references/constitution.md`; how skills compose into an ordered response is in
`references/playbooks.md` (including the greenfield composition with
`monozukuri-blueprint`). For the blueprint gate protocol see
`references/blueprint.md`. For roles, when to delegate to a fresh subagent, the
dispatch contract, and the review gate see `references/orchestration.md`; for
resuming multi-session or worktree work see `references/task-state.md`; for
guide, teach, review, and setup modes see `references/sensei.md`.

## Evidence and completion

Maintain a compact evidence ledger (Observed / Decided / Changed / Verified /
Residual risk) in working notes or the final report; do not create a repository
file unless requested. Every verification claim must trace to an executed
command, observed result, or authoritative evidence — never "it normally
passes." Distinguish `IMPLEMENTED` from `VERIFIED`: see the "Prove it works"
section of `references/evidence-and-completion.md`.

Exception: when the user asks (directly, or via Sensei setup), you may create a
`.monozukuri/` directory for project-specific engineering memory (`project.md`,
`architecture.md`, `decisions/`, `specifications/`, `verification/`, `state/`,
`blueprint/`, `incidents/`, `reflections/`). Do not create it unprompted.

Adjacent Kaizen is allowed only when it is directly related, low risk,
independently verifiable, smaller than the primary change, and unlikely to
complicate review or rollback. Otherwise record a concrete follow-up.

Ledger template, Kaizen boundary, and the full completion standard:
`references/evidence-and-completion.md`. Scope discipline and diff-size limits:
`references/change-budget.md`. Ordering multi-unit work smallest first, each
unit ending at a verified checkpoint: `references/checkpoints.md`. Preserve the
rationale behind existing code:
`references/keep-why.md`. The exit criteria the router composes:
`references/definition-of-done.md`. Turning recurring failures into durable
rules: `references/evolution.md`. Scoring a change against the constitution:
`references/evaluation.md`. The `monozukuri/v1` block format:
`references/schema.md`. Fill-in forms for ADRs, specifications, verification
notes, incidents, and reflections: `references/templates/`.
