---
name: ladder-execute
description: >-
  Executes a Ladder phase spec step-by-step with commit discipline and progress
  tracking. Use when ready to implement a spec, resume an interrupted phase, or
  when the user says "ladder execute."
compatibility: Requires git, Claude Code with plan mode and Task tool support
---

# Ladder Execute

Implement a phase spec one step at a time with plan mode, commit discipline, progress tracking, subagent delegation, and mid-session resume.

## When to Use

- User says "execute phase," "run phase," "ladder execute," "start phase," or "/ladder-execute"
- User provides a spec file path to implement
- Resuming an interrupted phase execution

## When NOT to Use

- `.ladder/OVERVIEW.md` doesn't exist → "Run `/ladder-init` first"
- Spec is not in canonical format → "Run `/ladder-refine` first"
- User wants to create a new spec → use `/ladder-create`
- User wants to fix a malformed spec → use `/ladder-refine`

## Quick Reference

| Field | Value |
|-------|-------|
| **Input** | Spec file path (`.ladder/specs/L-<N>-<slug>.md`) |
| **Output** | Implemented code, updated `progress.md`, commits per step |
| **Commits** | `type(L<N>-S<N>): description` per step, `chore(L<N>): complete phase execution` at end |
| **Prerequisites** | `.ladder/OVERVIEW.md`, canonical spec, entry criteria met |
| **Delegation** | medium + large steps → sub-agent; small steps → inline |

## Iron Laws

1. **Specs are immutable** — never edit a spec during execution. Log deviations in progress.md Decisions.
2. **Evidence before completion** — never mark acceptance criteria met without running a command and showing output.
3. **`progress.md` is the single source of truth** for execution state.
4. **User approval before execution** — confirm plan before beginning.
5. **One step, one commit** — each step gets exactly one commit.
6. **Delegate to preserve context** — medium and large steps run in sub-agents. The main agent orchestrates; sub-agents implement.
7. **Progress and commit are part of the step, not after it** — a step is not complete until progress.md is updated AND the atomic commit is made. Never proceed to the next step without both.

## Execution Checkpoints

**After Every Step:**
1. Acceptance criteria verified with evidence → 2. progress.md updated (status "done") → 3. Atomic commit (code + progress.md) → 4. SHA recorded in progress.md → **THEN** proceed to next step

**After All Steps (Phase Completion):**
1. Non-UAT exit criteria verified → 2. UAT checklist presented to user → 3. User confirms UAT pass → 4. progress.md finalized → 5. OVERVIEW.md updated → 6. Final commit → **THEN** suggest next phase

## Hard Gates

<HARD-GATE>
SPEC VALIDATION: Before executing, validate spec against ALL 5 rules from `references/spec-format.md`. If any rule fails → print failures and say "Run `/ladder-refine <path>` first." STOP.
</HARD-GATE>

<HARD-GATE>
ENTRY CRITERIA: All entry criteria must be verified against `progress.md` before proceeding. If predecessor phases are not "done" → print what's missing and STOP.
</HARD-GATE>

<HARD-GATE>
PLAN MODE: You MUST use EnterPlanMode before beginning execution. No exceptions. The user must approve the execution plan.
</HARD-GATE>

<HARD-GATE>
EVIDENCE REQUIRED: NEVER mark acceptance criteria as met without running a command and showing its output. "I believe this works" is not evidence. Run the test. Show the output.
</HARD-GATE>

<HARD-GATE>
SPEC IMMUTABILITY: Do NOT edit the spec file during execution. If a deviation is needed, log it in progress.md Decisions section. If the spec is wrong, STOP and suggest `/ladder-refine`.
</HARD-GATE>

<HARD-GATE>
CONTEXT ISOLATION: For steps with complexity "medium" or "large", you MUST delegate to a sub-agent via Task tool unless the user explicitly opted out during plan approval. Inline execution of medium/large steps wastes main context and degrades quality on later steps.
</HARD-GATE>

<HARD-GATE>
STEP COMPLETION: A step is NOT complete until: (1) acceptance criteria verified with evidence, (2) progress.md updated with status "done", (3) atomic commit made containing both code changes + progress.md. Do NOT begin the next step until all three are confirmed. Self-monitoring: if you find yourself thinking "I'll update progress.md later" or "I'll batch commits" — STOP. Complete the protocol now.
</HARD-GATE>

<HARD-GATE>
PHASE COMPLETION: A phase is NOT complete until: (1) progress.md finalized with status "done" and Completed date, (2) OVERVIEW.md Phase Registry updated with status "done", (3) final commit made containing both progress.md + OVERVIEW.md. Do NOT print next-phase suggestion until all three are confirmed.
</HARD-GATE>

<HARD-GATE>
UAT HANDOFF: UAT (User Acceptance Testing) is performed by the human, not the agent. You MUST present UAT checklist items from spec Section 8 to the user and wait for their pass/fail response. Do NOT self-validate UAT items. Do NOT mark the phase as "done" without user UAT confirmation.
</HARD-GATE>

## Pre-Execution Checklist

Before starting, verify:
- [ ] `.ladder/OVERVIEW.md` exists and is readable
- [ ] `.ladder/progress.md` exists and is readable
- [ ] Spec file exists at the provided path
- [ ] Spec passes all 5 validation rules
- [ ] All entry criteria are met
- [ ] Plan mode approved by user
- [ ] Plan will include per-step protocol (progress update + commit) for every step

## Workflow

### Phase 1: Startup Sequence

#### Step 1 — Load Context

Read these files, building a mental model of the project:
1. `.ladder/OVERVIEW.md` — product vision, tech stack, phase registry
2. `.ladder/progress.md` — execution state for all phases
3. The spec file provided as argument
4. All files from `.ladder/refs/` referenced in the spec's "References" section

#### Step 2 — Validate Spec Format

Check spec against `references/spec-format.md` validation rules:
1. All 11 required sections present (section 12 optional)
2. Step Sequence uses `S<N>` format with sequential IDs
3. Every step has an **Acceptance** list with at least one criterion
4. Entry Criteria references predecessor phase or Baseline
5. Exit Criteria includes "UAT checklist items pass"

If validation fails → print which rules failed and suggest: "Run `/ladder-refine <path>` first."

#### Step 3 — Validate Entry Criteria

Check each entry criterion against `.ladder/progress.md`:
- Predecessor phases must have status "done"
- Baseline must exist if referenced

If entry criteria not met → print what's missing and exit.

#### Step 4 — Resume Detection

Check `.ladder/progress.md` for this phase:

**Case A — Phase status "done":**
Print: "Phase L-<N> already complete. Nothing to do." Exit.

**Case B — Phase status "in-progress" (RESUME):**
1. Find the last step with status "done" in the Steps table
2. Verify its commit SHA exists in git log
3. If SHA missing → mark that step as "pending" (will redo it)
4. Print: "Resuming L-<N> from step S<X>."
5. Continue to Plan Mode with remaining steps only

**Case C — Phase not in progress.md (FRESH START):**
1. Add phase section to `.ladder/progress.md` with all steps "pending"
2. Set phase status to "in-progress", Started to today's date
3. Commit progress.md: `chore(L<N>): begin phase execution`
4. Continue to Plan Mode with all steps

### Phase 2: Plan Mode

#### Step 5 — Enter Plan Mode

Use `EnterPlanMode` to present the execution plan.

#### Step 6 — Present Plan

Build the plan from the spec's Step Sequence:
- List remaining steps (skip completed ones on resume)
- For each step show: ID, title, complexity, deliverable, dependencies
- Adapt approach to current codebase state (read relevant existing files)
- **Default to delegation** for steps with complexity "medium" or "large"
- **Inline only** for "small" complexity steps or steps the user explicitly opts out of delegation
- Present each step's execution mode (delegated/inline) in the plan for user approval

**CRITICAL — Per-Step Protocol:** Every step in the plan MUST end with these explicit mandatory actions written out for every single step (not summarized, not "repeat for all steps"):
```
After implementing S<N>:
  1. Verify all acceptance criteria (run commands, show output)
  2. Update progress.md: set S<N> status to "done", add notes if deviations
  3. Commit: stage code changes + progress.md together
     Message: type(L<N>-S<N>): description
  4. Record commit SHA in progress.md Commit column
```

**CRITICAL — Phase Completion Protocol:** After the last step, the plan MUST include:
```
After all steps complete:
  1. Validate non-UAT exit criteria from spec
  2. Present UAT checklist (spec Section 8) to user for manual testing
  3. Wait for user UAT confirmation before proceeding
  4. Update progress.md: phase status "done", Completed date, Decisions, Blockers
  5. Update OVERVIEW.md Phase Registry: set phase status to "done"
  6. Final commit: stage progress.md + OVERVIEW.md together
     Message: chore(L<N>): complete phase execution
```

Present the plan and ask the user:
- Approve the plan as-is, OR
- Reject delegation for specific steps (will run inline instead), OR
- Reorder steps (only if dependencies allow), OR
- Skip specific steps (mark as "skipped" in progress.md)

#### Step 7 — Exit Plan Mode

After user approval, exit plan mode and begin execution.

### Phase 3: Execution Loop

For each step in the approved order:

#### Step 8 — Announce Step

Print:
```
--- S<N>: <title> [<complexity>] ---
```

Update progress.md step row: status = "in-progress".

#### Step 9 — Implement, Verify, Record, Commit

**A. Implement** (delegated or inline):

**Delegated execution (default for medium + large steps):**
1. Prepare a sub-agent context package following `references/delegation-context.md` — all context inlined in the prompt, no file path references
2. Launch sub-agent via Task tool (`subagent_type: "general-purpose"`)
3. After sub-agent completes: independently verify ALL Acceptance criteria yourself (run commands, show output)
4. If criteria fail, fix inline before proceeding

**Inline execution (for small steps or user-opted-out steps):**
1. Implement the step's deliverable following the Details guidance
2. Check each Acceptance criterion — run commands, show output
3. If a criterion fails, fix before proceeding

**B. Update Progress:**

Update `.ladder/progress.md` step row:
- Status → "done"
- Notes → any deviations from spec (empty if none)

**C. Atomic Commit:**

Stage both the step's code changes AND `.ladder/progress.md`, then commit together:
```
type(L<N>-S<N>): description
```

Type selection: `feat` | `fix` | `refactor` | `test` | `chore` | `docs`

Each step commit atomically captures the implementation and its progress entry. After committing, update the progress.md Commit column with the 7-char short SHA.

**D. Confirm completion before continuing:**

- [ ] Acceptance criteria all passed with evidence
- [ ] progress.md step row shows "done"
- [ ] Commit exists with both code and progress.md
- [ ] Commit SHA recorded in progress.md
- → If any missing, complete it now. Do NOT proceed.

#### Step 10 — Loop

Return to Step 8 for the next step. If all steps complete, proceed to Phase 4.

### Phase 4: Phase Completion

#### Step 11 — Validate Exit Criteria and UAT Handoff

**A. Validate non-UAT exit criteria:**

Check each exit criterion from the spec (excluding "UAT checklist items pass"). If any criterion fails:
1. Print which criteria failed
2. Ask the user whether to fix now or mark as blocked

**B. Present UAT checklist to user:**

Extract all UAT items from the spec's Section 8 (UAT Checklist) and present them to the user:

```
Phase L-<N> implementation complete. Please perform these UAT checks:

- [ ] UAT-1: description
- [ ] UAT-2: description
- [ ] ...

Mark each item pass/fail. I'll wait for your results before finalizing the phase.
```

Do NOT self-validate UAT items. Do NOT assume they pass. Do NOT proceed to Step 12 until the user responds.

**C. Process UAT results:**

- If all UAT items pass → proceed to Step 12
- If any UAT items fail → ask user whether to fix now or mark as blocked in progress.md Blockers

#### Step 12 — Finalize Progress and OVERVIEW

**A. Update progress.md:**

Update `.ladder/progress.md`:
- Phase status → "done"
- Completed → today's date
- Decisions → list any deviations recorded during execution, or "(none)"
- Blockers → "(none)" if all exit criteria pass

**B. Update OVERVIEW.md:**

Update `.ladder/OVERVIEW.md` Phase Registry: set this phase's status to "done".

**C. Final Commit:**

Stage both `.ladder/progress.md` and `.ladder/OVERVIEW.md`:
```
chore(L<N>): complete phase execution
```

**D. Confirm phase closure:**

- [ ] progress.md phase status is "done" with Completed date
- [ ] OVERVIEW.md Phase Registry shows phase as "done"
- [ ] Final commit contains both files
- → Do NOT print next-phase suggestion until confirmed.

#### Step 13 — Next Phase Suggestion

Print:
> "Phase L-<N> complete. Next: `/ladder-execute <next-spec-path>` or `/ladder-create` for a new phase."

## Error Recovery

| Scenario | Action |
|----------|--------|
| Commit failure | Retry once, then pause and ask user |
| Step blocked (runtime issue) | Mark step "blocked" in progress.md Notes, proceed to next independent step |
| progress.md corrupted | Rebuild from git log by scanning for `L<N>-S<N>` commit message patterns |
| Subagent failure | Fall back to inline execution for that step |

## Concurrency Rules

- Multiple phases may execute concurrently if all entry criteria are met.
- Block if a predecessor phase is still "in-progress."

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Marking criteria met without evidence | No proof the code works | Run the command, show the output (Hard Gate) |
| Editing the spec during execution | Violates immutability | Log deviations in progress.md Decisions |
| Skipping plan mode | User can't review approach | EnterPlanMode is a HARD GATE |
| Deferring progress.md to phase completion | Progress.md out of sync, resume detection breaks | Complete Step 9B-9C before proceeding (STEP COMPLETION hard gate) |
| Forgetting OVERVIEW.md update at phase end | Phase Registry out of sync, next phase entry criteria may fail | Complete Step 12B-12C before next-phase suggestion (PHASE COMPLETION hard gate) |
| Continuing past failed entry criteria | Building on unstable foundation | STOP and resolve prerequisites first |
| Running medium/large steps inline | Context rot degrades later steps | Delegate via Task tool (Hard Gate) |
| Sending file paths instead of content to sub-agent | Sub-agent wastes turns reading files | Inline ALL context in the prompt |
| Self-validating UAT items | UAT is user acceptance testing — only humans can accept | Present UAT checklist to user and wait for response (UAT HANDOFF hard gate) |

## Red Flags — STOP

| Thought | Reality |
|---------|---------|
| "I'm sure this works, I don't need to test it" | Evidence is a HARD GATE — run the command |
| "I'll fix this spec issue while I'm here" | Specs are immutable during execution — use `/ladder-refine` |
| "Plan mode is overhead for this small phase" | Plan mode is mandatory — no exceptions |
| "I'll batch these steps into one commit" | One step, one commit — always |
| "The acceptance criteria are too strict, I'll skip some" | Every criterion must be verified with evidence |
| "I'll update progress.md later" | Update after every step — it's the source of truth |
| "I'll just do this inline, it's faster" | Delegation prevents context rot — speed now means degraded quality later |
| "The sub-agent might miss context" | That's why you package full context and verify independently after |
| "I'll commit everything at the end" | Each step gets its own atomic commit — STEP COMPLETION hard gate |
| "OVERVIEW.md can wait" | Phase is NOT complete until OVERVIEW.md is committed — PHASE COMPLETION hard gate |
| "The UAT items are straightforward, I can verify them myself" | UAT is human testing by definition — present the checklist and wait (UAT HANDOFF hard gate) |

## Integration

| Direction | Skill | Signal |
|-----------|-------|--------|
| **Requires** | `/ladder-init` | `.ladder/OVERVIEW.md` exists |
| **Requires** | `/ladder-create` or `/ladder-refine` | Canonical spec in `.ladder/specs/` |
| **Triggers** | `/ladder-refine` | When spec validation fails |
| **Enables** | `/ladder-execute` (next phase) | Phase marked "done" in progress.md |
