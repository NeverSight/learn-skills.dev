---
name: lcs-task-executor
description: 'Use this skill whenever the user asks to implement, execute, or continue a specific task from sliced tasks. Trigger on "Eksekusi TASK-###", "Eksekusi task-###.md", "continue TASK-###", "implement TASK-###". Always read .lcs/state.md first, check dependencies, analyze and recommend Normal vs TDD mode, confirm with user, and update task status and .lcs/state.md when done. Do NOT trigger for: design review (use lcs-code-review), brainstorming (use lcs-explore), documentation (use lcs-doc-finalizer), or debugging (use lcs-debug).'
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
---

# LCS Task Executor Skill

Shared Coding Contract
- Refer to Shared Coding Workflow Contract in `../lcs-shared/contract.md` for folder conventions, Handoff format, and token optimization.

Purpose
- Execute a single task (`task-###.md`), update its status to `done` (or `blocked`), and support Normal or TDD development flows with automatic analysis and user recommendation.

Trigger
- Activate when the user requests to "Eksekusi TASK-###", "Eksekusi task-###.md", "continue TASK-###", or "implement TASK-###".

## OKF Frontmatter & Writing Safety

- When creating or updating `task-###.md`, include YAML frontmatter following the schema in `../lcs-shared/contract.md`.
- After execution, update task status in task file frontmatter and include execution evidence or verification result.
- Follow the Artifact Writing Safety rules in contract.md — generate content first, write one file, verify, stop on failure.


### Trigger

Activate when user requests related to this skill's purpose. See description field in YAML frontmatter for trigger phrases.

Behavior checklist
1. Read `.lcs/state.md` first to identify active work-item directory: `.lcs/work-items/{timestamp}-{slug-work-item}/`.
2. Locate and read target task file `.lcs/work-items/{timestamp}-{slug-work-item}/task/task-###.md`.
3. **Check task type field**:
   - If `Type: HITL` (human-in-the-loop), output plan and STOP with message: "⚠️ HITL GATE: This task requires human approval before execution. Review the plan above and confirm to proceed."
   - If `Type: AFK` (autonomous), proceed with execution.
   - If type field missing or unclear, default to HITL (safer).
4. Read dependencies (`Depends on` field). If dependencies exist, verify they are completed:
   - Check each dependency task file has `status: done` in frontmatter
   - If any dependency not met, STOP with error listing incomplete dependencies
5. Read `task-coverage.md` if present to validate this task is in the coverage matrix.
6. Read `srs.md`, `prd-enhanced.md` or `prd.md`, and `tests.md` to understand acceptance criteria and test strategy.
7. Analyze the task and recommend execution approach:
3. Read Source coverage from the task file. If Source coverage is missing or empty, update the task status to `blocked`, report `Task lacks Source coverage. Re-run lcs-task-slicer to repair task slicing.`, and stop.
4. Read every referenced source artifact from Source coverage before implementation:
    - `SRC-###` -> Source Requirement Ledger in `prd-enhanced.md` or `prd.md`
    - `FR-###`/`BR-###`/`VR-###`/`EC-###` -> `srs.md`
    - `AC-###` -> `srs.md` Acceptance Criteria section
    - `TEST-###` -> `tests.md`
    If a referenced artifact is missing, mark the task `blocked` and report the missing source.
5. Check task dependencies listed in `Depends on`. If they are not `done` (or not met), update the task status to `blocked`, report the blocker, and stop.
6. Analyze task requirements and recommend development mode:
    - **TDD Mode Criteria**: Logic-heavy, complex state transitions, algorithm/data transformations, high-risk code, or tasks explicitly requiring testing.
    - **Normal Mode Criteria**: UI/styling only, configurations, plain boilerplates, low-risk documentation, or trivial chores.
    - *Action*: Present the recommendation with brief rationale. Ask user for confirmation.
7. If **Normal mode** is chosen:
    - Implement target logic.
    - Add/update tests if relevant.
    - Run validation commands (linter, tests).
    - Record execution results.
8. If **TDD mode** is chosen (based on vertical slices / tracer bullets):
    - **Step A: Plan Interfaces & Behaviors**: Confirm public interfaces and testable behaviors first. Avoid vertical slicing of private details.
    - **Step B: Tracer Bullet (RED -> GREEN)**: Write ONE failing test checking ONE public behavior. Implement minimal code to pass.
    - **Step C: Incremental Vertical Slices**: Loop writing one failing test and minimal implementation for each remaining behavior. Do not write all tests first.
    - **Step D: Refactor**: Extract duplication, deepen modules (keep interfaces small/simple), and apply SOLID principles. *Never refactor while test is RED*.
9. Once task fully executed and verified:
   - Verify `task-coverage.md` updated with completion status for this task (mark executed SRC/FR/AC/TEST IDs).
   - Update Chain of Truth Report before Handoff with executed Source IDs, pass/fail result, tests run, and remaining uncovered IDs.
   - Update `Status: done` inside `.lcs/work-items/{timestamp}-{slug-work-item}/task/task-###.md` file.
10. Update `.lcs/state.md` with:
    - `current_phase: execution`
    - `work_items[state.current_work].phase = execution`
    - `work_items[state.current_work].updated_at = <current-ISO-timestamp>`
    - `last_session_note: Executed TASK-###: <task-name> successfully`
    - `timestamp: <current-ISO-timestamp>`
11. End with Handoff pointing to the next logical step (e.g., the next sequential task, `lcs-code-review` after all tasks, or `lcs-doc-finalizer`).

Prompt templates
- Starter Task Execution: "Eksekusi TASK-001"
- Starter TDD explicitly: "Eksekusi TASK-001 dengan TDD"
- Starter Normal explicitly: "Eksekusi TASK-001 mode normal"

Handoff example:

## Chain of Truth Report
### Level
Very Strict

### Sources Checked
- `.lcs/state.md`
- `.lcs/work-items/{timestamp}-{slug-work-item}/task/task-###.md`

### Assumptions
- [verified] Task dependencies met.
- [verified] Chosen mode (Normal/TDD) confirmed with user.

### Plan Before Action
1. Read state.md and task file.
2. Check dependencies.
3. Implement task.
4. Run validation.

### Actions Taken
- <Exact commands run with stdout/stderr captured>

### Verification
- <All test and lint commands run; results quoted verbatim>

### Proof of Result
```
<Quoted command outputs>
```

### Blocked Items
<None, or list with reasons>

### Confidence
<high/medium/low>

### Risk Notes
<None, or outstanding concerns>



## Seam Discipline & TDD Rules

- **Glossary:** A Seam is the public boundary you test at. Test ONLY at pre-agreed seams.

- **Anti-Patterns (STRICTLY FORBIDDEN):**

  1. *Implementation-coupled:* Mocking internal collaborators or testing private methods.

  2. *Tautological:* Assertion recomputes expected value the same way the code does `expect(add(a,b)).toBe(a+b)`).

  3. *Horizontal slicing:* Writing all tests first, then all implementation. MUST use vertical tracer bullets.

- **Rule:** Refactoring is NOT part of the red-green loop. It belongs to the review stage.


## Strict Completion Criteria (Mandatory)

Every validation step MUST follow this pattern:

```
- **Step: Execute Validation.**
  - **Action:** Run `<command>` (project-specific: npm test, pytest, cargo test, etc.)
  - **Completion Criterion:** Command MUST exit with code 0. The exact stdout/stderr MUST be captured verbatim in the `Verification` section of the Chain of Truth Report.
  - **Failure Handling:** If exit code ≠ 0, mark task status as `blocked`, record the error output verbatim, and HALT. Do not attempt to fix without user confirmation or a new task.
```

**Leading Words:** "exit code 0", "verbatim stdout/stderr", "HALT on failure"
**Anti-Pattern:** "Run tests and make sure they pass" — too vague, no capture mechanism.

## Handoff
Next recommended skill: lcs-code-review
Next file to read: .lcs/work-items/{timestamp}-{slug-work-item}/task/task-###.md
Current phase: execution
Current confidence: high
Blocking questions: None
Risks to carry forward: None
Source of Truth Bundle: target task, prd-enhanced.md if present, prd.md, srs.md if referenced, tests.md if referenced, traceability.md if present, task-coverage.md if present
Must Preserve IDs: <executed SRC/FR/AC/TEST IDs>
Unresolved IDs: <remaining uncovered IDs or None>
Suggested next command: Eksekusi TASK-002 jika ada, atau review hasil dengan lcs-code-review

## Chain of Truth Level

Level: Very Strict

This skill follows the LCS Chain of Truth protocol at the declared level.
Implementation tasks require explicit sources, assumption status, plan before action, surgical changes, verification command or manual check, and proof of result.
