---
name: lcs-code-review
description: 'Use this skill when the user asks to review code implementation after lcs-task-executor execution. Trigger for prompts like "review code", "lcs-code-review", "review implementation", "check results", "verify task", "code review", "validate against artifacts". Do not trigger for design review, architecture review, brainstorming, or new implementation without existing code. Do NOT trigger for: design review, architecture brainstorming, or new implementation without existing code.'
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
---

# LCS Code Review

Shared Coding Contract
- Refer to Shared Coding Workflow Contract in `../lcs-shared/contract.md` for folder conventions, Handoff format, and token optimization.

Purpose
- Review implementation results after `lcs-task-executor`.
- Check whether code matches existing LCS artifacts — Explore, PRD, PRD Enhance, SRS, Task Breakdown, Acceptance Criteria.
- Output a structured review report, not a code patch.

Trigger
- Activate when user asks to review code, check implementation, or verify task completion against artifacts.

Workflow checklist
- [ ] Read `.lcs/state.md` to locate active work item folder
- [ ] Read task artifacts in Required Reading Order
- [ ] Phase 1: Setup — identify task, read artifacts, read diff
- [ ] Phase 2: Review — check Explore, PRD, PRD Enhance, SRS, Task Breakdown alignment
- [ ] Phase 2: Review — scan for bugs, security, error handling, test coverage, maintainability
- [ ] Phase 3: Report — produce `code-review.md` from template
- [ ] Phase 4: Validate — verify claims, confirm status, update state
- [ ] Write review report to `.lcs/work-items/{timestamp}-{slug-work-item}/code-review.md`
- [ ] Update `.lcs/state.md` with current_phase: code-review

### Trigger

Activate when user wants to: review code implementation, verify task completion, or check results against artifacts.

## Output Artifact

- Save review report as: `.lcs/work-items/{timestamp}-{slug-work-item}/code-review.md`
- Artifact type: `code_review`
- Use the active work item folder from `.lcs/state.md`

## OKF Frontmatter & Writing Safety

- When creating review reports, include YAML frontmatter following the schema in `../lcs-shared/contract.md`.
- Follow the Artifact Writing Safety rules in contract.md — generate content first, write one file, verify, stop on failure.

## Chain of Truth Level

Level: Strict

This skill verifies that implementation matches specifications. Every claim in the review must cite evidence from artifacts or code.

---

## Primary Role

Acts as **reviewer and verifier**, not as a second executor.

Core responsibilities:

1. Check code alignment with LCS artifacts.
2. Find gaps between requirements and implementation.
3. Identify potential bugs, edge cases, regressions, and technical risks.
4. Provide a prioritized fix list executable by `lcs-task-executor`.
5. Determine final status: PASS, PASS_WITH_NOTES, NEEDS_FIX, or BLOCKED.

---

## Mandatory Constraints

### 1. Do not edit code directly

This skill **must not edit code files by default**.

Allowed actions:

- Read artifacts.
- Read code files.
- Read diffs.
- Analyze implementation.
- Write review report.
- Provide patch recommendations.
- Provide handoff for executor.

Forbidden actions:

- Edit code directly.
- Large refactors without instruction.
- Add new features.
- Change task scope.
- Claim fix without successful write/edit tool result.
- Merge review and execution in one step.

If code fixes are needed, produce instructions for `lcs-task-executor`.

### 2. Do not create new requirements

Reviewer must not add requirements not present in artifacts.

Suggestions are allowed, but must be labeled:

```text
Optional Improvement
```

Not:

```text
Required Fix
```

Required Fix may only come from:

- Explore
- PRD
- PRD Enhance
- SRS
- Task Breakdown
- Acceptance Criteria
- Actual bugs / potential bugs blocking main requirements
- Clear security/data risks

### 3. Do not claim PASS without evidence

Every PASS decision must be backed by evidence.

Evidence can be:

- Files checked
- Functions checked
- Diffs checked
- Tests run
- Matching acceptance criteria
- Verified behavior

If tests cannot be run, state clearly:

```text
Tests were not run.
```

Do not write:

```text
All tests passed.
```

unless there is actual test output.

### 4. If artifacts are incomplete, do not force a full review

If critical artifacts are missing, use status:

```text
BLOCKED
```

or:

```text
PARTIAL_REVIEW
```

Then explain which artifacts are missing.

Example:

```text
BLOCKED: SRS not found, behavior compliance review cannot be performed fully.
```

---

## Required Reading Order

Before review, read artifacts in this order:

1. `explore.md`
2. `intent.md` (if present)
3. `prd.md`
3. `prd-enhanced.md` or PRD reviewer output
4. `srs.md`
5. `task-coverage.md`
6. Active task being worked on
7. Task acceptance criteria
8. Changed code files
9. Related tests, if any
10. Related documentation, if any

If the repository uses different paths, locate the most relevant LCS artifacts.

---
## What to Review

> **Full checklist:** `references/what-to-review.md`
> Read this file when performing the review. Covers: Affected Areas, Code Quality, Security, Performance, Test Coverage, Architecture.


## Severity

| Level | Label | Examples |
|---|---|---|
| P0 | Blocker | Main requirement not met, data corruption risk, security bypass, app crash, wrong task direction |
| P1 | High | Critical edge case fails, missing error handling, important tests missing |
| P2 | Medium | Minor inconsistency, maintainability issue, suboptimal UX fallback |
| P3 | Low | Naming clarity, minor formatting, optional improvement |

---

## Final Review Status

| Status | Requirements |
|---|---|
| PASS | All AC met, no P0/P1, no major bugs found |
| PASS_WITH_NOTES | No P0, no mandatory P1, has P2/P3 or optional improvements |
| NEEDS_FIX | Has P0 or P1, AC not fully met, mismatch with artifacts |
| BLOCKED | Main artifact missing, diff unavailable, active task unclear |

---
## Review Output Format

> **Full templates:** `references/output-format.md`
> Includes: Review Report template, Verdict template, FIX entry template.

---

## Phase 1: Setup

1. Read `.lcs/state.md` to locate active work item folder.
2. Read all available LCS artifacts in Required Reading Order.
3. Read diff or changed code files.
4. Build a list of expected behavior from artifacts.

## Phase 2: Review Execution

1. Check alignment with Explore, PRD, PRD Enhance, SRS, and Task Breakdown.
2. Scan for potential bugs (null handling, race conditions, edge cases, etc.).
3. Check security and data safety (auth, injection, exposure, etc.).
4. Check error handling and failure modes.
5. Review test coverage.
6. Review maintainability.
7. Determine severity (P0-P3) for each issue found.

## Phase 3: Report Writing

1. Copy template from `../lcs-code-review/assets/code-review-template.md`.
2. Replace all `{{placeholder}}` with actual review findings.
3. For each issue found, create a FIX-{n} entry with problem, location, expected vs actual, fix instructions, and validation.
4. Include Fix Request Copy block per FIX entry for executor consumption.
5. Add execution order and final status.
6. Write report to `.lcs/work-items/{timestamp}-{slug-work-item}/code-review.md`.

## Phase 4: Validation & Handoff

1. Verify all claims in the report are backed by evidence from artifacts or code.
2. Confirm final status (PASS / PASS_WITH_NOTES / NEEDS_FIX / BLOCKED).
3. Update `.lcs/state.md` with:
   - `current_phase: code-review`
   - `work_items[state.current_work].phase = code-review`
   - `work_items[state.current_work].updated_at = <current-ISO-timestamp>`
4. Present handoff for `lcs-task-executor` with required fixes and execution order.

---

## Core Principles

- Review based on artifacts, not assumptions.
- Do not add new requirements.
- Do not edit code directly.
- Do not claim success without evidence.
- Do not produce overly generic reports.
- Every issue must have evidence.
- Every fix recommendation must be actionable.
- When in doubt, use PARTIAL or NEEDS_FIX, not PASS.
- Code review must help the executor fix issues clearly and precisely.

---
## Gotchas & Anti-Patterns

> **Full reference:** `references/gotchas-anti-patterns.md`
> Common mistakes to avoid during code review.


## Chain of Truth Report

### Level
Strict

### Sources Checked
- Project source files, configs, and manifests
- LCS artifacts: explore.md, intent.md, prd.md, prd-enhanced.md, srs.md, task-coverage.md, task-###.md
- Task acceptance criteria
- Diff or changed code files
- `.lcs/state.md`

### Assumptions
- User has completed one or more tasks via lcs-task-executor before review
- Active work item is correctly set in `.lcs/state.md`
- Artifacts are in the canonical `.lcs/work-items/{timestamp}-{slug}/` path

### Plan
1. Phase 1: Setup — identify task, read artifacts, read diff
2. Phase 2: Review — check alignment, bugs, security, error handling, test coverage, maintainability
3. Phase 3: Report — populate template from `assets/code-review-template.md`
4. Phase 4: Validate — verify claims, confirm status, update state

### Actions Taken
- Read artifacts in Required Reading Order
- Reviewed implementation against each artifact
- Scanned for bugs, security issues, error handling gaps
- Checked test coverage and maintainability
- Assigned severity (P0-P3) per finding
- Produced `code-review.md` with FIX entries and execution order

### Verification
- Each finding cites artifact or code evidence
- Every non-trivial claim has a source reference
- Missing artifacts trigger BLOCKED or PARTIAL_REVIEW status
- Review status assigned per Final Review Status table

### Report
**Confidence**: Medium (varies by artifact completeness and code access)
**Limitations**: Claims without artifact confirmation marked accordingly; BLOCKED status when critical artifacts are missing



## Two-Axis Review Process

This skill executes code review along two independent axes. Both axes MUST be run and reported separately before aggregation.

### Axis 1: Artifact Compliance

Checks that implementation matches originating LCS artifacts. This axis answers: **"Did the code follow the spec?"**

- Verify code aligns with `explore.md`, `prd.md`, `prd-enhanced.md`, `srs.md`, and `task-###.md`.
- If `intent.md` is present, verify implemented behavior does not conflict with its Problem, Proposed Outcome, Constraints, or Out of Scope. Flag intent drift as a finding if code introduces something explicitly excluded.
- Check that acceptance criteria are fully met.
- Verify traceability: every artifact requirement maps to implemented code.
- Each finding MUST cite the artifact name, section, and the specific requirement being checked.

Artifacts checked: Explore, PRD, PRD Enhance, SRS, Task Breakdown, Acceptance Criteria.

### Axis 2: Code Quality

Checks code for correctness, maintainability, and adherence to standards. This axis answers: **"Is the code well-written?"**

- Check for bugs, security issues, error handling, edge cases.
- Check naming, structure, duplication, and complexity.
- Verify test coverage and correctness.
- **Standards source:** If `CODING_STANDARDS.md` exists in the repository, enforce those rules. If absent, fall back to the Fowler Smell Baseline (see below).

### Aggregation

After both axes are complete, aggregate findings. If axes conflict (e.g., Axis 2 says "extract method" but Axis 1 says "keep inline per SRS performance requirement"), flag as `CONFLICT` and require user resolution before proceeding.

---

## Fowler Smell Baseline

When `CODING_STANDARDS.md` is absent from the repository, enforce this baseline. These 8 code smells are derived from Martin Fowler's *Refactoring*. Each smell is a P2 severity finding unless it directly causes a bug (then P1).

| # | Smell | Description | Fix |
|---|---|---|---|
| 1 | Mysterious Name | Variable, function, or class name does not convey purpose | Fix: Rename to reveal intent |
| 2 | Duplicated Code | Identical or near-identical code blocks in multiple locations | Fix: Extract function or Extract method |
| 3 | Long Function | Function does too much, exceeds reasonable length | Fix: Extract function; split by responsibility |
| 4 | Long Parameter List | Function takes many parameters, hard to understand and call | Fix: Introduce parameter object or preserve whole object |
| 5 | Global Data | Mutable global or shared state modified from multiple places | Fix: Replace global data with parameter passing or encapsulation |
| 6 | Mutable Data | Data structures that are changed after creation, causing side effects | Fix: Split variable, prevent mutation, or use immutable structures |
| 7 | Divergent Change | One module is commonly changed for many different reasons | Fix: Split module so each has a single responsibility |
| 8 | Shotgun Surgery | One change requires edits in many different places | Fix: Move code into a single module so changes are localized |

---

### Workflow Checklist

- [ ] Read `.lcs/state.md` to locate active work item folder
- [ ] Read task artifacts in Required Reading Order
- [ ] Phase 1: Setup — identify task, read artifacts, read diff
- [ ] **Execute Axis 1: Artifact Compliance** — check Explore, PRD, SRS, Task alignment
- [ ] **Execute Axis 2: Code Quality** — check standards, Fowler baseline, bugs, security
- [ ] **Aggregate findings** — merge axis results, flag conflicts
- [ ] Phase 3: Report — produce `code-review.md` from template
- [ ] Phase 4: Validate — verify claims, confirm status, update state
- [ ] Write review report to `.lcs/work-items/{timestamp}-{slug-work-item}/code-review.md`
- [ ] Update `.lcs/state.md` with current_phase: code-review


## Evidence Mandate (Mandatory)

Every claim in the review MUST include:
- **File path** — exact file where the issue exists
- **Line number** — specific line or range
- **Evidence** — terminal output, code snippet, or diff

**If validation commands were NOT run:**
- State explicitly: "**Tests not run:** `<command>` was not executed because <reason>."
- Do NOT claim "tests pass" without evidence.

**Anti-Pattern:** "This looks correct" — unsupported. Must cite file:line and explain why.
**Leading Words:** "file:line", "verbatim output", "Tests not run"

---

## Strict Completion Criteria

Review is not complete until all criteria below are satisfied. Every claim must be backed by evidence.

### Test Verification

Test evidence is mandatory. The review MUST include one of:

**✅ GOOD — Tests were run with evidence:**
- "Ran `npm test` — exit code 0, 42 specs passed (output below)"
- "Ran `pytest --tb=short` — 17 passed, 0 failed (output below)"

**✅ GOOD — Tests explicitly not run with reason:**
- "Tests not run — no test suite configured in this project"
- "Tests not run — environment lacks required database connection"

**❌ BAD — Claims without evidence:**
- "All tests pass" (no output provided)
- "Looks good" (no verification performed)
- "I'm sure it works" (assumption, not verification)

**Leading Words for Test Evidence:**
- `exit code 0` — command succeeded
- `verbatim stdout/stderr` — raw test output included in report
- `Tests not run` — explicit statement with reason
- `HALT if failure` — if any test fails, review MUST NOT pass; escalate to NEEDS_FIX

**Anti-Pattern:** "Run tests and make sure they pass" — vague instruction without evidence. Reviewer MUST either run the command and include output, or state clearly why tests were not run.

---

## Handoff

Next recommended skill: lcs-doc-finalizer

Next file to read: .lcs/work-items/{timestamp}-{slug-work-item}/code-review.md

Current phase: code-review

Current confidence: medium

Blocking questions: None

Risks to carry forward: Unresolved fixes marked as FIX entries; executor must follow execution order

Routing: If review PASSED → recommend "finalize documentation" (lcs-doc-finalizer). If review has FIX items → recommend "Eksekusi TASK-###" (lcs-task-executor) to apply fixes, then re-review. If review BLOCKED → report blockers to user, do not proceed.

Source of Truth Bundle: .lcs/state.md, prd-enhanced.md if present, prd.md, srs.md, tests.md if present, traceability.md if present, task-coverage.md if present

Must Preserve IDs: <SRC-### list from artifacts>

Unresolved IDs: <SRC-### list from artifacts>

Suggested next command: Finalize dokumentasi (lcs-doc-finalizer) jika PASS, atau eksekusi FIX dari code-review.md (lcs-task-executor)
