---
name: pipeline
description: >-
  Autonomous build-phase orchestrator. Manages slice queue, TDD pair dispatch,
  full-team code review, mutation testing, CI integration, and auto-merge with
  quality gates. Replaces manual coordinator overhead during build phase.
  Activate when running factory mode with ensemble-team.
license: CC0-1.0
metadata:
  author: jwilger
  version: "1.0"
  requires: [tdd, code-review, mutation-testing, task-management, ci-integration]
  context: [test-files, domain-types, source-files, ci-results, task-state, git-history]
  phase: build
  standalone: false
---

# Pipeline

**Value:** Flow -- continuous, gated progression from slice to shipped code
eliminates idle coordination overhead and makes quality evidence accumulate
automatically.

## Purpose

Orchestrates the build phase end-to-end: takes vertical slices from the queue,
dispatches TDD pairs, runs full-team code review before push, enforces mutation
testing and CI gates, and merges or escalates. The pipeline controller handles
all operational tasks (running tests, pushing code, managing git) so team member
agents focus exclusively on creative work.

## Practices

### Slice Queue Management

The pipeline reads vertical slices from event model output and maintains their
state in `.factory/slice-queue.json`. See `references/slice-queue.md` for the
full queue schema and operations.

Each slice carries a `context` block with enriched metadata for downstream
pipeline stages: boundary annotations on each GWT scenario (so the gate can
verify boundary coverage), an event model source path (so the TDD pair can
consult the original model), related slice IDs for cross-slice dependency
tracking, domain types referenced by the slice (enabling pre-implementation
type discovery), and UI components referenced (triggering conditional context
gathering when the slice touches the interface layer).

**Ordering strategy:** Walking skeleton first (the thinnest end-to-end path),
then by dependency graph (slices whose predecessors are complete), then by
priority. The first slice in any project must always be a walking skeleton.

**Slice states:** pending, active, blocked, completed, escalated. Only one
slice may be active at a time unless running at full autonomy level, where
parallel slices operate in isolated git worktrees (one worktree per active
slice at `.factory/worktrees/<slice-id>`). See `references/autonomy-levels.md`.

### Per-Slice Pipeline

Each slice flows through a fixed sequence of stages. Every stage has a binary
quality gate. A gate failure routes back for rework; it never skips forward.

1. **Decompose** -- Invoke `task-management` to break the slice into leaf
   tasks with acceptance criteria. Output: task tree in
   `.factory/audit-trail/slices/<slice-id>/decomposition.json`.

2. **Implement** -- Before dispatching the TDD pair, the pipeline gathers
   pre-implementation context: architecture docs, glossary, existing domain
   types matching the slice's referenced types, and event model context from
   the slice. If the slice touches UI, design system components are included.

   **TDD dispatch (the pipeline controller IS the orchestrator):**
   The pipeline controller performs capability detection (per TDD skill's
   hierarchy) and dispatches directly. Do NOT spawn a single "orchestrator"
   subagent -- that hides work and bypasses strategy detection.

   - **TeamCreate available:** Create a pair team (e.g.,
     `pair-<slice-id>`), spawn two developer agents into it, bootstrap
     both with pre-implementation context and the ping-pong protocol from
     `tdd/references/ping-pong-pairing.md`. The pair exchanges handoffs
     via SendMessage. The pipeline controller monitors via task updates
     and handles operational tasks (running tests, git commits) directly.
   - **Task available (no TeamCreate):** The pipeline controller acts as
     the serial subagent orchestrator per `tdd/references/orchestrator.md`,
     spawning per-phase agents (RED, DOMAIN, GREEN, COMMIT) using the
     Task tool with fresh context each time.
   - **Neither available:** The pipeline controller runs chaining mode,
     playing each TDD role sequentially per the TDD skill's chaining
     section.

   The TDD pair then works through red-green-domain-commit cycles without
   consensus rounds. No team discussion during implementation. Output: passing
   tests, committed code, cycle evidence in
   `.factory/audit-trail/slices/<slice-id>/tdd-cycles/`.

3. **Review** -- Before pushing, invoke `code-review` with the full team for
   three-stage mob review (spec compliance, code quality, domain integrity).
   All review findings must be addressed before proceeding. See
   `references/gate-definitions.md` for review gate criteria.

4. **Address feedback** -- Route review findings back to the TDD pair. The
   pair fixes via their existing ping-pong process. Re-review scoped to
   flagged concerns only (unless critical-category feedback).

5. **Mutation test** -- Invoke `mutation-testing` scoped to changed files.
   Required: 100% kill rate. Survivors route back to the TDD pair.

6. **Push and CI** -- Pipeline pushes the branch and waits for CI. On infra
   failures at standard or full autonomy, auto-retry once. On test failures,
   route to triage.

7. **Merge or flag** -- If all gates pass, merge (auto at full autonomy,
   manual otherwise). If any gate failed after exhausting rework budget,
   escalate to human.

### Quality Gates

Five binary gates. Each requires structured evidence. See
`references/gate-definitions.md` for full criteria, evidence schemas, and
failure routing.

| Gate | Pass Criteria | Failure Route |
|------|--------------|---------------|
| TDD | Acceptance test passes, all units pass, domain review approved | Back to tdd pair |
| Review | All three stages PASS | Back to tdd pair with findings |
| Mutation | 100% kill rate on changed files | Back to tdd pair with survivors |
| CI | Pipeline green | ci-integration triage |
| Merge | All upstream gates pass, no blocking escalations, branch current | Rebase and re-gate |

### Rework Protocol

Gate failures route back to the appropriate skill. Each gate allows a maximum
of 3 rework cycles per slice. After 3 failures at the same gate, the pipeline
halts the slice, compiles full context (all attempts, all evidence), and
escalates to the human. See `references/rework-protocol.md` for routing rules
and tracking schema.

### Progressive Autonomy

The pipeline operates at one of three autonomy levels configured in
`.factory/config.yaml`. See `references/autonomy-levels.md` for full details.

- **Conservative:** All gates enforced, no auto-merge, human notified of every
  gate result, human approves every merge.
- **Standard:** Auto-rework within budget, batch non-blocking findings, skip
  trivial review items, auto-retry CI on infra failures.
- **Full:** Auto-merge when all gates pass, parallel slice execution using
  git worktree isolation (each active slice gets its own worktree; conflicts
  are detected at merge time), pair selection and slice ordering optimization.
  If `git worktree` is not available, the pipeline falls back to sequential
  execution and logs a warning.

### Pipeline Operates Directly

Unlike the ensemble-team coordinator (which delegates everything), the pipeline
controller directly executes operational tasks: running test suites, invoking
mutation tools, pushing branches, checking CI status, managing git operations,
updating queue state. Team member agents are invoked only for creative work:
writing tests, writing code, conducting reviews.

### Audit Trail

Every pipeline action produces structured evidence in `.factory/audit-trail/`.
See `references/audit-trail-schema.md` for the directory layout and JSON
schemas. The audit trail enables retrospectives, trend analysis, and
reproducible escalation context.

## Enforcement Note

The pipeline provides structural enforcement through gating: no stage proceeds
without evidence from the prior stage, and gate failures mechanically route to
rework. The pipeline cannot prevent an agent from producing low-quality work,
but it can prevent low-quality work from reaching the main branch. Rework
budgets and human escalation provide a safety net when automated gates are
insufficient.

## Verification

After completing a slice through the pipeline, verify:

- [ ] Slice was decomposed into leaf tasks with acceptance criteria
- [ ] Pre-implementation context was gathered and passed to the orchestrator
- [ ] TDD pair implemented without consensus rounds (no team discussion)
- [ ] Full-team code review occurred before push (all three stages)
- [ ] All review findings were addressed before proceeding
- [ ] Mutation testing achieved 100% kill rate on changed files
- [ ] CI pipeline passed green
- [ ] Merge occurred only after all five gates passed
- [ ] Audit trail entries exist for every stage
- [ ] Acceptance test exercises the application boundary
- [ ] Rework cycles (if any) stayed within the 3-cycle budget per gate

## Dependencies

This skill requires other skills to function. It orchestrates them; it does not
replace them.

- **tdd:** Pair implementation engine. The pipeline dispatches TDD pairs and
  collects cycle evidence.
- **code-review:** Three-stage review protocol. The pipeline invokes full-team
  review before every push.
- **mutation-testing:** Quality gate for test effectiveness. The pipeline runs
  mutation testing scoped to changed files.
- **task-management:** Work decomposition. The pipeline decomposes slices into
  leaf tasks before implementation.
- **ci-integration:** CI pipeline monitoring. The pipeline pushes and waits for
  CI results.

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill tdd
```
