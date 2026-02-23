---
name: tdd
description: >-
  Adaptive test-driven development cycle. Detects harness capabilities and routes
  to guided (manual phase control) or automated (orchestrated) mode. Invoke with
  /tdd for automated or /tdd red|domain|green|commit for guided.
license: CC0-1.0
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: [test-files, domain-types, source-files]
  phase: build
  standalone: true
---

# TDD

**Value:** Feedback -- short cycles with verifiable evidence keep AI-generated
code honest and the human in control. Tests express intent; evidence confirms
progress.

## Purpose

Teaches a five-step TDD cycle (RED, DOMAIN, GREEN, DOMAIN, COMMIT) that
adapts to whatever harness runs it. Detects available delegation primitives
and routes to guided mode (human drives each phase) or automated mode
(system orchestrates phases). Prevents primitive obsession, skipped reviews,
and untested complexity regardless of mode.

## Practices

### The Five-Step Cycle

Every feature is built by repeating: RED -> DOMAIN -> GREEN -> DOMAIN -> COMMIT.

1. **RED** -- Write one failing test with one assertion. Only edit test files.
   Write the code you wish you had -- reference types and functions that do not
   exist yet. Run the test. Paste the failure output. Stop.
   Done when: tests run and FAIL (compilation error OR assertion failure).

2. **DOMAIN (after RED)** -- Review the test for primitive obsession and
   invalid-state risks. Create type definitions with stub bodies (`todo!()`,
   `raise NotImplementedError`, etc.). Do not implement logic. Stop.
   Done when: tests COMPILE but still FAIL (assertion/panic, not compilation error).

3. **GREEN** -- Write the minimal code to make the test pass. Only edit
   production files. Run the test. Paste passing output. Stop.
   Done when: tests PASS with minimal implementation.

4. **DOMAIN (after GREEN)** -- Review the implementation for domain violations:
   anemic models, leaked validation, primitive obsession that slipped through.
   If violations found, raise a concern and propose a revision.
   Done when: types are clean and tests still pass.

5. **COMMIT** -- Run the full test suite. Stage all changes and create a git
   commit referencing the GWT scenario. This is a **hard gate**: no new RED
   phase may begin until this commit exists.
   Done when: git commit created with all tests passing.

After step 5, either start the next RED phase or tidy the code (structural
changes only, separate commit).

A compilation failure IS a test failure. Do not pre-create types to avoid
compilation errors. Types flow FROM tests, never precede them.

Domain review has veto power over primitive obsession and invalid-state
representability. Vetoes escalate to the human after two rounds.

### User-Facing Modes

**Guided mode** (`/tdd red`, `/tdd domain`, `/tdd green`, `/tdd commit`):
Each phase loads `references/{phase}.md` with detailed instructions for that
step. For experienced engineers who want explicit phase control. Works on
any harness -- no delegation primitives required. The human decides when to
advance phases.

**Automated mode** (`/tdd` or `/tdd auto`):
The system detects harness capabilities, selects an execution strategy, and
orchestrates the full cycle. The user sees working code, not sausage-making.
For verbose output showing phase transitions and evidence, use `/tdd auto --verbose`.

### Capability Detection (Automated Mode)

When automated mode activates, detect available primitives in this order:

1. **Agent teams available?** Check for TeamCreate tool. If present, use the
   **agent teams** strategy with persistent pair sessions.
2. **Subagents available?** Check for Task tool (subagent spawning). If present,
   use the **serial subagents** strategy with focused per-phase agents.
3. **Fallback.** Use the **chaining** strategy -- role-switch internally between
   phases within a single context.

Select the most capable strategy available. Do not attempt a higher strategy
when its primitives are missing.

### Execution Strategy: Chaining (Fallback)

Used when no delegation primitives are available. The agent plays each role
sequentially:

1. Load `references/red.md`. Execute the RED phase.
2. Load `references/domain.md`. Execute DOMAIN review of the test.
3. Load `references/green.md`. Execute the GREEN phase.
4. Load `references/domain.md`. Execute DOMAIN review of the implementation.
5. Load `references/commit.md`. Execute the COMMIT phase.
6. Repeat.

Role boundaries are advisory in this mode. The agent must self-enforce phase
boundaries: only edit file types permitted by the current phase (see
`references/phase-boundaries.md`).

### Execution Strategy: Serial Subagents

Used when the Task tool is available for spawning focused subagents. Each
phase runs in an isolated subagent with constrained scope.

- Spawn each phase agent using the prompt template in `references/{phase}-prompt.md`.
- The orchestrator follows `references/orchestrator.md` for coordination rules.
- **Structural handoff schema** (`references/handoff-schema.md`): every phase
  agent must return evidence fields (test output, file paths changed, domain
  concerns). Missing evidence fields = handoff blocked. The orchestrator does
  not proceed to the next phase until the schema is satisfied.
- Context isolation provides structural enforcement: each subagent receives
  only the files relevant to its phase.

### Execution Strategy: Agent Teams

Used when TeamCreate is available for persistent agent sessions. Maximum
enforcement through role specialization and persistent pair context.

- Follow `references/ping-pong-pairing.md` for pair session lifecycle, role
  selection, structured handoffs, and drill-down ownership.
- Both engineers persist for the entire TDD cycle of a vertical slice.
  Handoffs happen via lightweight structured messages, not agent recreation.
- Track pairing history in `.team/pairing-history.json`. Do not repeat either
  of the last 2 pairings.
- The orchestrator monitors and intervenes only for external clarification
  routing or blocking disagreements.

### Phase Boundary Rules

Each phase edits only its own file types. This prevents drift. See
`references/phase-boundaries.md` for the complete file-type matrix.

| Phase | Can Edit | Cannot Edit |
|-------|----------|-------------|
| RED | Test files | Production code, type definitions |
| DOMAIN | Type definitions (stubs) | Test logic, implementation bodies |
| GREEN | Implementation bodies | Test files, type signatures |
| COMMIT | Nothing -- git operations only | All source files |

If blocked by a boundary, stop and return to the orchestrator (automated) or
report to the user (guided). Never circumvent boundaries.

### Walking Skeleton First

The first vertical slice must be a walking skeleton: the thinnest end-to-end
path proving all architectural layers connect. It may use hardcoded values or
stubs. Build it before any other slice. It de-risks the architecture and gives
subsequent slices a proven wiring path to extend.

### Outside-In TDD

Start from an acceptance test at the application boundary -- the point where
external input enters the system. Drill inward through unit tests. The outer
acceptance test stays RED while inner unit tests go through their own
red-green-domain-commit cycles. The slice is complete only when the outer
acceptance test passes.

A test that calls internal functions directly is a unit test, not an acceptance
test -- even if it asserts on user-visible behavior.

**Boundary enforcement by mode:**
- **Pipeline mode:** The CYCLE_COMPLETE evidence must include `boundary_type`
  and `boundary_evidence` on the acceptance test. The pipeline's TDD gate
  rejects evidence where the acceptance test calls internal functions directly.
- **Automated mode (non-pipeline):** The orchestrator checks boundary scope
  and re-delegates if the first test is not a boundary test. Advisory -- no
  gate blocks progression.
- **Guided mode:** The human is responsible for ensuring boundary-level tests.
  The skill text instructs correct behavior but cannot enforce it.

### Cycle-Complete Evidence

At the end of each complete RED-DOMAIN-GREEN-DOMAIN-COMMIT cycle, produce
a CYCLE_COMPLETE evidence packet containing: slice_id, acceptance_test
{file, name, output, boundary_type, boundary_evidence}, unit_tests
{count, all_passing, output}, domain_reviews [{phase, verdict, concerns}],
commits [{hash, message}], rework_cycles, pair {driver, navigator}.

When `pipeline-state` is provided in context metadata, the TDD skill
operates in **pipeline mode**: it receives a `slice_id` and stores
evidence to `.factory/audit-trail/slices/<slice-id>/tdd-cycles/cycle-NNN.json`.
When running standalone, the evidence is informational only (not stored).

See `references/cycle-evidence.md` for full schema.

### Harness-Specific Guidance

If running on Claude Code, also read `references/claude-code.md` for
harness-specific rules including hook-based enforcement. For maximum
mechanical enforcement, ask the bootstrap skill to install optional hooks
from `references/hooks/claude-code-hooks.json`.

## Enforcement Note

Enforcement is proportional to capability:

- **Guided mode**: Advisory. The skill text instructs correct behavior but
  cannot prevent violations. The human enforces by controlling phase
  transitions.
- **Automated mode (chaining)**: Advisory with self-enforcement. The agent
  follows phase boundaries by convention.
- **Automated mode (serial subagents)**: Structural enforcement via context
  isolation and handoff schemas. Subagents receive only phase-relevant files.
  Missing evidence blocks handoffs.
- **Automated mode (agent teams)**: Maximum enforcement through role
  specialization. Neither engineer can skip review because the other is
  watching. Persistent context means accumulated understanding, not just rules.
- **Optional hooks** (Claude Code): Mechanical enforcement. Pre-tool-use hooks
  block unauthorized file edits per phase. See `references/claude-code.md`.

No mode guarantees perfect discipline. If you observe violations -- production
code edited during RED, domain review skipped, commits missing -- point it out.

## Verification

After completing a cycle, verify:

- [ ] Every failing test was written BEFORE its implementation
- [ ] Domain review occurred after EVERY RED and GREEN phase
- [ ] Phase boundary rules were respected (file-type restrictions)
- [ ] Evidence (test output) was provided at each handoff
- [ ] Commit exists for every completed RED-GREEN cycle
- [ ] Walking skeleton completed first (first vertical slice)

**HARD GATE -- COMMIT (must pass before any new RED phase):**

- [ ] All tests pass
- [ ] Git commit created with message referencing the current GWT scenario
- [ ] No new RED phase started before this commit was made

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **domain-modeling:** Strengthens the domain review phases with parse-don't-validate,
  semantic types, and invalid-state prevention principles.
- **code-review:** Three-stage review (spec compliance, code quality, domain
  integrity) after TDD cycles complete.
- **mutation-testing:** Validates test quality by checking that tests detect
  injected mutations in production code.
- **ensemble-team:** Provides real-world expert personas for pair selection
  and mob review.

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill domain-modeling
```
