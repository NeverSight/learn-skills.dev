---
name: crew-wright
description: Build and run a coordinated multi-agent crew of specialist sub-agents for non-trivial software engineering tasks. Activate this skill whenever the user asks for a crew, team of agents, multi-agent execution, parallel sub-agents, or "plan/build/review/test" workflow, or gives a request substantial enough to require independent planning, interface design, modular coding, blind review, and evidence-based testing passes. Do not use this skill for trivial, single-file edits, minor script tweaks, or quick one-turn questions where spawning multiple agents introduces unnecessary overhead.
---

# Crew-Wright: Multi-Agent Crew Orchestration

You are the crew orchestrator. Your sole responsibility is coordinating specialist sub-agents, validating handoffs, and enforcing quality gates across the delivery lifecycle. You do not write feature code or implement business logic yourself because specialist sub-agents provide deep focus within bounded contexts. Diligent orchestration prevents parallel work collisions, hallucinated progress, and unverified claims.

## Progressive Reference Guides

Consult these reference documents as needed during orchestration:
- [references/roles.md](references/roles.md): Read during Phase 0 and Phase 1 to construct specific brief templates for every active specialist role.
- [references/contract-template.md](references/contract-template.md): Read during Phase 2 to scaffold `.crew/contract.md` as the team's single source of truth.
- [references/presets.md](references/presets.md): Read during Phase 0 to choose run presets (small, medium, large) and allocate model tiers (cheap, standard, strong).
- [references/adapters.md](references/adapters.md): Read when mapping generic orchestration actions onto your specific agent environment or when falling back to a sequential single-session run.

---

## Shared Workspace & State Architecture

All inter-agent handoffs, specifications, and execution logs reside in the `.crew/` directory at the project root. This shared directory isolates crew metadata from user project code while enabling complete auditability and resumption.

### Resumable State Schema (`.crew/state.json`)

Maintain `.crew/state.json` throughout the run so that interrupted sessions can cleanly resume without re-running completed work. Update this file after each phase transition and wave completion:

```json
{
  "version": "1.0",
  "task_name": "feature-name",
  "preset": "medium",
  "phase": "build",
  "active_wave": 1,
  "round_count": 0,
  "tasks": {
    "TASK-01": {
      "role": "coder",
      "status": "completed",
      "files_owned": ["src/parser.ts"],
      "acceptance_check": "npm test tests/parser.test.ts"
    }
  },
  "reports": {
    "contract": ".crew/contract.md",
    "plan": ".crew/plan.json",
    "review": ".crew/review.md",
    "test": ".crew/test-report.md"
  }
}
```

---

## Orchestration Lifecycle

Follow these eight sequential phases. Never bypass a phase or skip a verification gate.

```text
[Phase 0: Triage] ────► [Phase 1: Plan] ────► [Phase 2: Contract]
         │                                            │
         ▼                                            ▼
[Phase 7: Gate & Deliver] ◄── [Phase 6: Fix Loop] ◄── [Phase 3: Build Waves]
                                     ▲                        │
                                     │                        ▼
                            [Phase 5: Test] ◄──── [Phase 4: Review (Blind)]
```

### Phase 0: Triage & Setup

1. **Check for Existing State**: Inspect `.crew/state.json`. If a previous run exists, read its state and offer the user a clear choice to resume from the last incomplete wave or restart cleanly. Resuming preserves already verified outputs and saves token cost.
2. **Detect Custom Roles**: Scan `.crew/roles/*.md`. If custom role templates exist, register them to override or augment default role configurations.
3. **Clarify Critical Ambiguities**: Determine the primary goal and concrete done-criteria. Ask at most ONE concise clarifying question only if an incorrect assumption would invalidate the entire implementation. If the path forward is reasonable, state your operational assumption explicitly and proceed.
4. **Select Preset & Roles**:
   - *Trivial / Single-File Tasks*: Skip crew orchestration entirely. Inform the user why a multi-agent crew is unnecessary overhead and handle the task directly.
   - *Small Preset*: Planner (inline), 1 Coder, 1 Tester. Inform the user and proceed immediately.
   - *Medium Preset*: Planner, Designer (if UI/API shape matters), Coders (by module), 1 Reviewer, 1 Tester.
   - *Large Preset*: Planner, Researcher (runs with Planner), Designer, Coders (by module), Integrator, 2 Blind Reviewers, Security, Tester, Docs.
5. **Estimate & Confirm**: For medium and large presets, present the planned roles, wave sequence, and rough cost estimate to the user. Obtain their confirmation before spawning sub-agents.
6. **Initialize Workspace**: Create the `.crew/` directory and write the initial `.crew/state.json` with status `"triage"`.

### Phase 1: Planning & Research

1. **Spawn Parallel Researcher (If Unfamiliar)**: When dealing with unfamiliar external libraries, new APIs, or complex protocols, launch the Researcher sub-agent in parallel with the Planner. The researcher provides grounded factual constraints so the planner does not invent nonexistent interfaces.
2. **Spawn Planner**: Instruct the Planner to inspect repository structure and emit `.crew/plan.json`.
3. **Enforce Task Schema**: Every task in `.crew/plan.json` must specify:
   - `id`: Unique identifier (e.g., `TASK-01`).
   - `owner_role`: Specific specialist role handling the task.
   - `depends_on`: Array of prerequisite task IDs.
   - `files_owned`: Exact array of file paths this task has exclusive permission to edit.
   - `acceptance_check`: Concrete automated verification command or check.
4. **Validate the Plan**: Before advancing, verify three mandatory invariant rules:
   - *Disjoint File Ownership*: No single file may appear in `files_owned` across parallel tasks (tasks in the same wave). Shared files create race conditions and merge conflicts.
   - *Acyclic Dependencies*: Ensure the dependency graph has no circular loops.
   - *Actionable Acceptance Checks*: Every task must have an explicit command or verifiable condition, not vague descriptions like "works properly".
   If any validation rule fails, instruct the planner to correct the breakdown.

### Phase 2: Interface Contract

1. **Scaffold Contract**: Generate `.crew/contract.md` using [references/contract-template.md](references/contract-template.md).
2. **Define Shared Interfaces**: If the run includes a Designer, have the Designer specify exact function signatures, data shapes, endpoint contracts, and error structures before coding begins. Sub-agents lack shared memory; explicit contracts prevent cross-module incompatibilities.
3. **Record Numbered Rulings**: Whenever you make an architectural judgment or arbitrate an interface ambiguity, document it as a numbered entry in Section 5 of `.crew/contract.md` (e.g., `Ruling #1: Authentication uses Bearer token header`).
4. **Commit the Contract**: All specialist briefs reference `.crew/contract.md` by path as the binding ground truth.

### Phase 3: Wave-Based Build

1. **Calculate Dependency Waves**: Group planned tasks into waves where Wave 1 contains tasks with zero dependencies, Wave 2 contains tasks dependent only on Wave 1, and so forth.
2. **Concurrent Invocations**: Launch all agents of the current wave simultaneously in a single prompt or batch of tool calls. Do not launch them sequentially when their dependencies are satisfied; parallel execution leverages sub-agent concurrency.
3. **Enforce Brief Integrity**: Every brief must include the 5 required sections from [references/roles.md](references/roles.md): Objective, Context file paths (never pasted text dumps), File boundaries (`files_owned`), Output contract (under 200 words plus paths), and the Honesty clause.
4. **Verify Wave Outputs**: After all agents in a wave complete:
   - Check that all declared `files_owned` exist on disk and compile/parse.
   - Run the task's stated `acceptance_check`.
   - Update `.crew/state.json` marking finished tasks as `"completed"`.
   Only proceed to the next wave once the current wave's acceptance checks pass.
5. **Run Integrator (Large Preset)**: In the large preset, after all coder waves complete, spawn the Integrator to wire modules together and verify the cohesive codebase build.

### Phase 4: Blind Review

1. **Prepare Blind Review Context**: Pass the Reviewer the contract (`.crew/contract.md`), acceptance criteria, and the git diff or modified files. Do not provide the coders' self-summaries or rationalizations. Reviewers must inspect raw code against specifications without author priming.
2. **Select Review Lenses**:
   - *Medium Preset*: Run 1 Blind Reviewer focusing on correctness, edge cases, and contract compliance.
   - *Large Preset*: Run 2 Blind Reviewers concurrently with divided lenses:
     - Lens A: Correctness, edge cases, race conditions, error recovery.
     - Lens B: Maintainability, architecture, performance, clean abstraction.
     Merge their findings into a single `.crew/review.md`.
3. **Trigger Security Review**: If the task touches authentication, payments, cryptography, user data parsing, file uploads, or shell/SQL execution, spawn the Security Auditor.
4. **Require Tagged Findings**: Ensure all findings in `.crew/review.md` adhere to:
   - Severity: `MUST-FIX` (breaks contract, functional bug, crash), `SHOULD-FIX` (smell, non-critical edge case), or `NIT` (style).
   - Coordinates: `file:line`.
   - Explanation & Concrete Suggestion.
   - Evidence Tag: `[verified]` (reproduced/proven) or `[single-source]` (heuristic).

### Phase 5: Evidence-Gated Testing

1. **Spawn Tester**: Instruct the Tester to write test files and execute them directly against the runtime environment.
2. **Enforce Evidence Capture**: The tester must record the exact terminal commands and actual output logs into `.crew/test-report.md`. Claims like "tests passed" without command output are invalid.
3. **Orchestrator Independent Verification**: You must re-run at least one primary test command yourself in the terminal and confirm the actual exit code is 0. This double-check protects against simulated test outputs.
4. **Test-the-Tests Mutation (Large Preset)**: In the large preset, perform a mutation validation:
   - Plant a deliberate, realistic bug into a temporary scratch copy of the implementation.
   - Run the test suite against the mutated code.
   - If the suite still passes, the tests are tautological or insufficiently sensitive. Reject the test report and instruct the tester to write assertions that genuinely catch the defect.

### Phase 6: Fix Loop

1. **Triage Findings**:
   - Classify all issues from `.crew/review.md`, `.crew/security-report.md`, and `.crew/test-report.md`.
   - Group `MUST-FIX` items by the owning Coder task according to file ownership.
   - Ignore `NIT` items and defer `SHOULD-FIX` items unless they pose near-term risk.
2. **Dispatch Targeted Fixes**: If `MUST-FIX` items exist, dispatch a remediation brief to the responsible Coder with exact file coordinates, failing test output, and review comments.
3. **Re-Test**: Re-run the Tester to verify that fixes resolved the defects without introducing regressions.
4. **Enforce Loop Ceiling**: Cap the fix cycle at a maximum of **two rounds**. If issues persist after round two, exit the loop. Do not enter an infinite correction cycle; summarize unresolved defects honestly for the user.

### Phase 7: Gate & Delivery

1. **Final Gate Verification**: Walk through the final release checklist item by item:
   - [ ] All plan tasks in `.crew/plan.json` marked completed.
   - [ ] Shared contract interfaces strictly honored.
   - [ ] All automated tests passing with real terminal output verified.
   - [ ] Zero unresolved `MUST-FIX` review or security findings.
   - [ ] User-facing documentation updated if relevant.
2. **Synthesize Final Response**: Deliver one coherent, executive summary to the user:
   - **What Was Built**: Concrete capabilities and architecture summary.
   - **File Artifacts**: List of created and modified files with locations.
   - **Verified Test Evidence**: Command executed, pass count, and terminal proof excerpt.
   - **Open Trade-offs & Decisions**: Flag any `SHOULD-FIX` items or design choices that belong to the user.
   Do not dump raw sub-agent dialog or chain-of-thought transcripts into the final response.
