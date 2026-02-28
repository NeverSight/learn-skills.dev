---
name: run-repair-loop
description: Iteratively review changes, run automated tests, and apply targeted fixes until issues are resolved (or a stop condition is reached).
tags: [automation, devops, eng-standards, optimization]
version: 0.1.0
license: MIT
related_skills: [review-code, review-diff, run-automated-tests, review-security, review-performance]
recommended_scope: both
metadata:
  author: ai-cortex
compatibility: Requires a shell and the repo's toolchains to run tests (language-dependent). May require git for diff-based review.
---

# Skill: Run Repair Loop (Review + Test + Fix)

## Purpose

Converge a codebase or change set to "clean" by running a **multi-iteration loop**:

1. **Review** (find problems early and prevent regressions),
2. **Test** (get executable signal),
3. **Fix** (apply the smallest correct patch),
4. Repeat until **no blocking issues remain** or a **stop condition** is hit.

## Use Cases

- "Keep fixing until tests pass."
- "Do a review-test-fix loop and make the repo green."
- "Stabilize this PR/change set with iterative testing and targeted fixes."
- "Run CI-like tests, fix failures, repeat until stable."

## Behavior

### 1. Pre-flight (must resolve once)

Confirm or default the following:

- **Target**: repo path (default `.`) and scope:
  - `diff` (default): focus on current changes, prioritize `review-diff`.
  - `codebase`: review a specified path set, prioritize `review-codebase`/language skills via `review-code`.
- **Definition of done**:
  - Tests: chosen test plan passes (fast/ci/full).
  - Review: no `critical`/`major` review findings remain.
  - If only `minor`/`suggestion` findings remain, list them and ask whether to address them.
- **Loop bounds**:
  - `max_iterations` default: `5`.
  - `time_budget` default: "best effort"; if user provides a time limit, honor it strictly.
- **Allowed actions** (ask if unclear; default to safer choice):
  - Modify repo files: **Yes** (this skill is for fixing), but keep changes minimal.
  - Install dependencies: **No** without confirmation.
  - Network access: **No** without confirmation.
  - Docker/services (DB/Redis/etc.): **No** without confirmation.
  - Large refactors: **No** without confirmation.

### 2. Iteration loop

For `i = 1..max_iterations`:

1. **Collect current signals (evidence-first)**
   - If scope = `diff`: run/perform a `review-diff` pass over the current diff/untracked additions.
   - If scope = `codebase` or user wants deeper review: run `review-code` (or the relevant atomic review skill(s)).
   - If a previous iteration had test failures, prioritize resolving those failures first.

2. **Run tests**
   - Use `run-automated-tests` to discover and run the best matching test command(s) in the selected mode:
     - `fast` (default): unit tests only, minimal setup.
     - `ci`: mirror CI steps as closely as possible.
     - `full`: include integration/e2e (only with explicit confirmation for dependencies/services).
   - Capture:
     - the first failing command + exit code
     - the most relevant error excerpt (do not dump massive logs unless asked)

3. **Synthesize a fix plan (smallest correct patch)**
   - Choose **one** primary issue to fix first:
     - First failing test/command usually wins (highest signal).
     - If review found a `critical` security/correctness issue, fix that before or alongside tests.
   - Prefer fixes that:
     - change the smallest surface area
     - preserve API/contracts unless explicitly approved
     - add or adjust tests when fixing a bug (when feasible)

4. **Apply fix**
   - Implement the patch.
   - Avoid unrelated formatting or churn.
   - If the fix requires a risky change (schema migration, auth changes, broad refactor), pause and ask.

5. **Re-run the minimal validation**
   - Re-run the most relevant failing test subset if the framework supports it; otherwise re-run the same test command.
   - If fixed, proceed to the next remaining failure/finding within the same iteration only if it is trivial; otherwise go to the next loop iteration.

6. **Stop early when converged**
   - If tests pass and there are no `critical`/`major` review findings, stop.

### 3. Stop conditions (must not loop forever)

Stop and ask the user for direction if any occur:

- **No progress**: the same failure repeats for 2 iterations with no new information.
- **Environment blocker**: missing toolchain, missing secrets, or unavailable dependency (DB/Docker) and user has not approved required setup.
- **Flaky tests**: non-deterministic failures suspected (e.g., passes on retry without changes).
- **Iteration limit reached**: `max_iterations` exhausted with remaining failures.

When stopping, provide the shortest path options:

- run a different test mode (`fast` -> `ci` -> `full`)
- allow installs/network/Docker
- narrow scope (fix only first failing test)
- increase iteration limit

## Input & Output

### Input

- Target path (default `.`)
- Scope: `diff` (default) or `codebase` (+ paths)
- Test mode: `fast` (default), `ci`, `full`
- Constraints: allow installs/network/Docker/services (yes/no)
- `max_iterations` (default `5`)
- Optional: time budget

### Output

- **Repair Loop Report**:
  - Definition of done used
  - Evidence sources (which files/CI configs informed test plan)
  - For each iteration:
    - test command(s) run and result
    - first failure excerpt (if any)
    - changes made (files touched + intent)
    - remaining failures/findings
  - Final state:
    - tests passing (which commands)
    - remaining review items (if any) and whether they are blocking

## Restrictions

- Do not install dependencies, use network, start Docker/services, or run destructive commands without explicit confirmation.
- Do not ask the user to paste secrets into chat. Prefer local env files or documented dev flows.
- Do not "fix" by disabling tests, weakening assertions, or deleting coverage unless the user explicitly approves and the tradeoff is documented.
- Avoid large refactors as a default; prioritize minimal patches that unblock correctness.
- Keep changes scoped to the target repository; do not modify unrelated sibling repos.

## Self-Check

- [ ] Pre-flight choices resolved (scope, test mode, permissions, max iterations).
- [ ] Each iteration produced at least one of: a new test result, a new review signal, or a concrete code change.
- [ ] Tests were rerun after fixes (at least the failing command or a targeted subset).
- [ ] Loop terminated due to convergence or an explicit stop condition (no infinite retries).
- [ ] Final report includes: commands run, failures (if any), patches applied, and remaining risks.

## Examples

### Example 1: Fix failing unit tests in a Node repo

User: "Make tests pass. Keep fixing until green."

Agent:

1. Pre-flight: scope=`diff`, test mode=`fast`, max_iterations=5; confirm installs allowed (`npm ci`) and network allowed.
2. Iteration 1: run `npm test`, fix first failing test, rerun `npm test`.
3. Iteration 2: run `review-diff` to catch edge cases introduced by the fix; rerun `npm test`.
4. Stop when `npm test` passes and there are no major review findings.

### Example 2 (Edge case): Integration tests require Docker and secrets

User: "Mirror CI and fix failures."

Agent:

1. Pre-flight: propose test mode=`ci`, but detect CI uses `docker compose` and env secrets.
2. Stop condition triggered: environment blocker (Docker + secrets not approved/available).
3. Ask the user to choose:
   - run only `fast` unit tests locally, or
   - allow Docker and provide a non-chat secret workflow, or
    - run only the failing CI job steps that don't require secrets.

---

## Appendix: Output contract

Each skill execution MUST produce a **Repair Loop Report** in this exact JSON format:

```json
{
  "repair_loop_report": {
    "definition_of_done": {
      "tests": "test command passes",
      "review": "no critical/major findings"
    },
    "scope": "diff | codebase",
    "mode": "fast | ci | full",
    "max_iterations": 5,
    "iterations": [
      {
        "iteration": 1,
        "review": {
          "skill_used": "review-diff",
          "findings_count": {"critical": 0, "major": 1, "minor": 2},
          "blocking": ["unused import in utils.js"]
        },
        "tests": {
          "command": "npm test",
          "status": "failed",
          "exit_code": 1,
          "first_failure": "FAIL src/utils.test.js"
        },
        "fix": {
          "files_changed": ["src/utils.js"],
          "intent": "remove unused import"
        },
        "re_run": {
          "command": "npm test",
          "status": "passed"
        }
      }
    ],
    "final_state": {
      "tests_passing": true,
      "commands_passed": ["npm test"],
      "blocking_issues_remaining": [],
      "minor_suggestions": ["consider adding type hints"]
    },
    "stop_condition": "converged | max_iterations | environment_blocker | no_progress"
  }
}
```

| Element | Type | Description |
| :--- | :--- | :--- |
| `definition_of_done` | object | What constitutes success |
| `scope` | string | `diff` or `codebase` |
| `mode` | string | Test mode: `fast`, `ci`, or `full` |
| `max_iterations` | number | Loop limit |
| `iterations` | array | Each iteration's review, test, fix, re-run |
| `final_state` | object | End state: tests passing, remaining issues |
| `stop_condition` | string | Why loop ended: `converged`, `max_iterations`, `environment_blocker`, `no_progress` |

This schema enables Agent consumption without prose parsing.

