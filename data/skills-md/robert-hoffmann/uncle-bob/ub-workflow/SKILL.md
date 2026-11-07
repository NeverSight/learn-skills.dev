---
name: ub-workflow
description: >-
  Use this skill when work needs durable planning, adaptive product slicing,
  discovery before delivery, resumable sprint execution, wave or initiative
  scaffolding, source-pack routing, closeout evidence, final audits, or
  repeatable product-agile workflow structure. Do not use it for small direct
  fixes that do not need a durable artifact, or for governance-only questions
  that belong to ub-governance.
argument-hint: "overview | scaffold | source-atlas | wave | initiative | discovery | sprint | audit | archive | what-next"
user-invocable: true
disable-model-invocation: false
---

# UB Workflow

## Overview

Use this skill as the portable workflow layer for work that is too large,
risky, cross-cutting, or stateful to run from chat history alone.

The default operations root is `./.ub-workflows/` unless the host deliberately
chooses another root.

The normalized model is product-agile hybrid:

```text
Product Vision -> Product Options -> Outcome Waves -> Initiatives -> Discoveries -> Sprints
```

The model combines:

1. dual-track agile: discovery validates options before delivery pulls work;
2. goal-oriented roadmapping: product vision stays broad while waves and
   initiatives carry current outcomes;
3. Scrum-like sprint execution: one sprint goal, inspect/adapt, and explicit
   start approval when reviewed mode is active;
4. Kanban-style flow controls: explicit policies, WIP limits, pre-commitment
   options, feedback loops, and stale-candidate revalidation;
5. Shape Up influence: lightweight bet framing, appetite, circuit breakers,
   and no backlog sludge;
6. appetite-boxed forecast calibration: candidate counts are forecasts, and
   expansion requires operator choice after scoped options and tradeoffs.

## Canonical Layout

```text
PROJECT_ROOT/
  AGENTS.md
  SOURCE_ATLAS.md
  .ub-workflows/
    AGENTS.md
    vision.md
    options.md
    status.md
    WORKFLOW_ATLAS.md
    SOURCE_PACK_ATLAS.md
    source-packs/
      .gitkeep
      YYYY-MM-DD-slug/
    waves/
      .gitkeep
      wNN-wave-slug/
        wave.md
        discoveries/
          .gitkeep
          wNN-dNN-slug.md
        source-packs/
          .gitkeep
          YYYY-MM-DD-slug/
        initiatives/
          .gitkeep
          iNN-initiative-slug/
            initiative.md
            options.md
            roadmap.md
            index.md
            discoveries/
              .gitkeep
              wNN-iNN-dNN-slug.md
            sprints/
              .gitkeep
              wNN-iNN-sNN-sprint-slug/
                sprint.md
                decision-log.md
                closeout.md
                evidence/
                  .gitignore
                  index.md
```

Naming rules:

1. wave IDs are project-sequenced: `w01`, `w02`, etc.;
2. initiative IDs reset per wave: `i01`, `i02`, etc.;
3. wave-level discoveries use `wNN-dNN-slug.md` and reset per wave;
4. initiative discoveries use `wNN-iNN-dNN-slug.md` and reset per initiative;
5. sprints use `wNN-iNN-sNN-sprint-slug/` and reset per initiative;
6. source packs use `YYYY-MM-DD-slug/` using creation, original research,
   earliest known history, or migration date with a note.

## Lanes

Choose the lane that lets the accepted objective be completed, validated, and
recovered without unrelated expansion:

1. direct bounded work: a small single-session change with no durable planning
   surface needed;
2. wave/initiative workflow: multi-session, staged, risky, product-shaping,
   or cross-cutting work that needs options boards, discovery, roadmaps,
   sprints, closeouts, and resumable evidence.

Promote lanes when the current lane no longer provides enough durable surface
to finish and prove the accepted objective.
Record the promotion reason in the artifact that now owns the work.

## Embedded Contract

1. Keep reusable workflow rules in this skill, not in one repository overlay.
2. Keep repository overlays thin: project facts, current pointers, local
   validation commands, domain boundaries, and repository-specific constraints.
3. `vision.md` owns the adaptable product north star.
4. Root `options.md` owns curated product-level, future-wave, and
   unknown-owner options before commitment. It is not a backlog ledger,
   completion history, or execution authorization surface.
5. `status.md` owns current product posture, wave sequencing, active pointers,
   blockers, WIP state, candidate tracks, retained-context routes, and next
   allowed action.
6. `SOURCE_ATLAS.md` owns project-root source routing. Bootstrap seeds it with
   a one-time scan; later updates are event-based when source boundaries move.
7. Root `AGENTS.md` owns the local agent overlay. Bootstrap creates or patches
   only a small managed workflow-routing section.
8. A workflow-root guide, split product/live-state startup files, and a root
   specs lane are not canonical workflow surfaces.
9. Outcome waves are adaptive product slices; they may split, merge, grow, or
   shrink through reviewed discovery.
10. Initiatives are thematic wave-local bets; they may pause and resume.
11. Initiative-local `options.md` owns possible insertions before that
    initiative closes. Product-level or later-wave options move to root
    `options.md`.
12. Discoveries are normal upstream steering work, not exceptional ceremony.
13. Discoveries and sprint previews record user or operator evidence status as
    `used`, `not triggered`, or `deferred` so technical work still states
    whether real-user or operator feedback shaped the decision.
14. Sprints are delivery slices pulled from accepted discovery or a reviewed
    sprint preview.
15. Default WIP is constrained dual-track: one active delivery sprint and one
    active discovery per active initiative; wave discovery is active only for
    activation, transition, or reroute.
16. Future work may live in root or initiative-local options boards before
    commitment. Options are ordered by document order within horizon lanes, but
    are not delivery commitments, status ledgers, or execution queues.
17. Remove an option after it is promoted, rejected, merged, or completed and
    the receiving artifact owns the durable trace. Do not maintain a `Done`
    lane in options boards.
18. Before activating a new wave or initiative, review root options and
    unresolved local options from the closing initiative.
19. Before closing an initiative, promote, move, reject, or remove every local
    option. Do not archive completed cards in the options board itself.
20. Run options validation at wave or initiative transition, option promotion,
    initiative closeout, terminal audit, and when a sprint preview is pulled
    from an option.
21. Reusable workflow-system changes that affect artifact ownership,
    lifecycle gates, scaffold output, transition policy, or recovery context
    require a compact workflow-improvement discovery or equivalent accepted
    decision record.
22. Revalidate candidates on touch: any candidate not prepared from current
    evidence must pass fresh discovery or preview before execution. Use
    discovery when route-changing uncertainty exists; use reviewed preview
    only when a registered candidate is being freshly revalidated for start.
23. Discovery Triage is a fail-closed Routing Preflight, not a preview
    appendix. Before choosing a reviewed preview, record trigger categories and
    one outcome: `preview_ok`, `discovery_required`,
    `operator_decision_needed`, or `not_triggered`. Trigger categories include
    autonomy, authority, runtime-boundary, policy, evidence,
    interoperability, agent-behavior changes, agent loops, harnesses, loop
    continuation, goal judgment, budgets, and checkpoints. If triggered
    evidence may change route, contract, scope, validation, runtime boundary,
    or implementation path, record `discovery_required`; `preview_ok` is valid
    only when the route is already decided and trigger evidence cannot change
    those decisions. Use `not_triggered` only with a concrete reason.
24. Discovery-driven sequence changes must be promoted into the owning
    `roadmap.md` before acceptance; closeout-driven next-route changes must be
    promoted before sprint closeout.
25. Sprint previews identify repo-owned operational surfaces when triggered:
    owner, lifecycle, visibility, safety policy, validation path, and
    inventory/topology/registry/route-map impact. If uncertainty about those
    facts may change scope, architecture, risk, or acceptance criteria,
    promote discovery before execution.
26. Each wave and initiative records qualitative Outcome Signals for product
    or user value, delivery flow, quality or stability, and context or evidence
    cost. These are routing signals, not a metrics ledger.
27. Each initiative and sprint records lightweight bet framing: appetite,
    success evidence, circuit breaker, non-goals, and deferral path.
28. Waves and initiatives use Appetite-Boxed forecasting by default: forecast
    counts are not commitments, sequence expansion is not automatic
    adaptation, and adding work requires the agent to present options,
    tradeoffs, and a recommended path for explicit operator decision.
29. Wave and initiative charters record Forecast And Appetite; roadmaps record
    Forecast Control; discoveries and reviewed previews record Forecast Impact
    when they change sequence.
30. Sprint previews record Product Increment Contribution as `direct`,
    `enabling`, or `audit`; enabling sprints must name the visible increment
    they unblock and why a direct slice is not viable.
31. Two consecutive enabling or prerequisite sprints trigger a route review:
    propose shipping a vertical proof, cutting/deferring scope, rerouting, or
    explicitly buying more enabling work.
32. Major capability candidates decompose prerequisite risks and the first
    usable product increment before acceptance.
33. In reviewed mode, a request to move on opens a preview only; execution
    starts only after a later explicit approval.
34. New sprint packs include `decision-log.md`, `closeout.md`, and
    `evidence/index.md`.
35. `evidence/index.md` is the T4 claim-to-proof router. It records validated
    claims, evidence files, required objective gates, optional or
    not-triggered gates, redaction posture, promotion targets, and read policy
    without becoming a narrative closeout.
36. Generated runtime state under sprint evidence (any
    project-specific scratch directory) is local scratch by default.
    Commit only reviewed no-secret evidence files or an explicitly
    approved export.
37. Sprint closeout includes a required outcome and learning review with four
    prompts: what did this sprint achieve, how did it make the project better,
    what could have been done better, and whether the learning changes the
    next route, stays local, or suggests a workflow improvement.
38. Sprint closeout records Forecast Delta: planned versus actual, hidden
    prerequisite discovered, remaining forecast impact, and whether roadmap,
    index, or status were updated.
39. Material closeout claims must be backed by `evidence/index.md`. Required
    objective proof cannot be deferred while closing the original objective as
    passed; missing or failing required proof keeps the sprint active or
    blocked until the operator explicitly changes scope or the proof passes.
40. Sprint closeout includes a focused mini-retro: process friction, evidence
    cost, context cost, decision latency, workflow adjustment if needed, and a
    retro evidence check covering objective signal, controllability, and
    repeated friction.
41. Repeated or structural workflow friction is promoted into this skill;
    one-off repo friction stays local.
42. Project evolution mode defaults to `forward-only` unless a host records a
    reviewed compatibility-preserving decision.
43. When the active evolution mode requires forward migration, broad boundary
    changes must include an impact inventory and must update, remove, or
    explicitly defer each affected owned surface before closeout.
44. Source packs are retained context, not execution authorization, live state,
    or backlog.
45. Trace tokens are owner-only lookup anchors. Use triggered T3 initiative
    `index.md` trace routes before broad workflow search, and do not add trace
    tokens to discoveries, sprint packs, closeouts, decision logs, or evidence
    indexes.

## Interaction Modes

1. `reviewed` is the default: preview before execution, explicit later start
   approval, post-execution report, and pause after closeout.
2. `flow`: short pre-execution note, post-execution report, manual advancement.
3. `auto`: internal pre-execution analysis and automatic advancement unless a
   blocker, conflict, or path-shaping decision requires interruption.
4. `continuous` / `yolo`: no routine pauses, but all gates, artifacts, and
   interruption rules still apply.

Mode changes visibility and pause behavior. It does not weaken readiness,
evidence, or writeback requirements.

## Objective-Complete Rule

Choose an objective-complete action: implement and validate all work required
for the accepted sprint objective and exit criteria. Avoid unrelated expansion,
but do not cut, defer, or split required proof just to preserve scope or
budget.

When a sprint, preview, or closeout uses words like `smallest`, `narrow`, or
`only as needed`, interpret them as the smallest objective-complete vertical
slice, not the smallest patch that makes the first focused test pass. Every
repo-owned affected surface named by the sprint scope, every required evidence
gate, and every exit criterion remains in scope unless the operator explicitly
changes the objective.

## Load References By Trigger

- `[phase:lifecycle-detail]` Read `references/workflow-contract.md` for
  detailed operating rules, WIP policy, reviewed-mode previews, and recovery.
- `[phase:artifact-create|artifact-validate]` Read
  `references/artifact-contracts.md` when creating or validating workflow
  artifacts.
- `[edge:context-management|frontmatter|context-budget]` Read
  `references/context-management.md` when interpreting `context_tier`,
  `summary_budget_lines`, phase read budgets, atlas routes, context receipts,
  retained-context reads, or evidence/writeback receipt shapes.
- `[edge:trace-token|trace-lookup|workflow-search]` Read
  `references/trace-tokens.md` when searching workflow history, interpreting
  trace IDs or tags, adding trace metadata, or deciding where trace anchors
  belong.
- `[phase:gate-eval|closeout|readiness]` Read
  `references/validation-and-completion.md` when evaluating readiness,
  closeout, archive, or completion.
- `[edge:helper-use]` Read `references/scaffold-helper.md` before using or
  explaining the deterministic helper.
- `[edge:strict-placeholder-validation|options-validation]` Read
  `references/placeholder-contract.md` when strict placeholder validation is
  relevant. Read `references/validation-and-completion.md` when options-board
  validation, transition checks, or closeout checks are relevant.
- `[edge:governance-escalation]` Read `references/governance-bridge.md` only
  when explicit governance mapping is active.
- `[edge:authoring-conventions]` Read
  `../ub-authoring/references/authoring-conventions.md` when shared routing,
  naming, or choice-question authoring is being changed.

## Bundled Assets

Use `assets/operations-root/` and `assets/initiative-template/` as canonical
templates. Use `scripts/scaffold_workflow.py` for deterministic bootstrap,
wave, initiative, discovery, source-pack, sprint, and archive operations. Use
`scripts/check_workflow_options.py` for options-board transition, closeout,
terminal-audit, and stale-card validation.

## Output Requirements

For non-trivial workflow work, report:

1. lane and scale decision;
2. active artifact owner;
3. WIP and gate state;
4. chosen path and rejected alternative when path choice matters;
5. validation and evidence expectation;
6. next allowed action.
