---
name: investigate-failing-tests
description: Use when diagnosing and coordinating fixes for failing WebdriverIO tests across context gathering, test runs, and implementation skills, while limiting retry loops and avoiding rabbit holes.
---

# Investigate Failing Tests

Orchestrate diagnosis and repair of failing WebdriverIO tests.

This skill is a reasoning and routing layer. It does **not** write code or run tests directly. It delegates those actions to other skills/agents and manages decision points.

## Delegation Contract

- Does not directly edit test files.
- Does not directly execute test commands.
- Delegates to:
  - `running-webdriverio-tests` for execution
  - `gathering-context` for artifact collection
  - `analyze-website` for route/component structure context when missing
  - `writing-webdriverio-code` for test-side fixes
  - `managing-project-customizations` for stale/missing context refresh
  - `skipped-test-manager` for confirmed app bugs

## When to Use

- A user reports failing WDIO tests and needs diagnosis + fix orchestration.
- Failure details are partial and need structured investigation.
- There is risk of repeated blind retries or trial-and-error edits.

## When Not to Use

- You only need to run tests (`running-webdriverio-tests`).
- You already know the exact test fix and only need implementation (`writing-webdriverio-code`).
- You only need artifact/context gathering (`gathering-context`).

## Inputs

Extract and normalize from user input:

- failing spec file/path
- failing test name/title
- error message and stack (if provided)
- environment target (local/dev/staging/prod)
- any recent change context from the user

### Target Resolution Rule

For `references/website-analysis/<target>/...`, resolve `<target>` from:

1. explicit user URL, else
2. project `baseUrl` host, else
3. `unknown-target`

If error/stack is missing, delegate to `running-webdriverio-tests` to reproduce and collect failure details.

## Workflow

1. Parse user input and capture known failure facts.
2. Load `.webdriverio-skills/project-context.*` and `.webdriverio-skills/custom-rules.md` if present.
3. Load `references/website-analysis/<target>/website-analysis.*` when available to accelerate route/component reasoning.
4. If critical details are missing, delegate a focused test run to obtain error + stack.
5. Delegate to `gathering-context` with normalized failure details.
6. If route/component intent is unclear, delegate `analyze-website` and merge results into hypothesis.
7. Analyze evidence + recent code changes to form a primary root-cause hypothesis.
8. Confirm findings with the user before implementation (accept/adjust).
9. If issue is test-side, delegate fix implementation to `writing-webdriverio-code`.
10. Delegate test execution to validate.
11. Repeat triage/fix loop with strict attempt limits.

## Hypothesis and Confirmation

Before requesting a fix, provide the user:

- likely root cause (1 primary, 1 secondary)
- why evidence supports it
- intended fix direction
- expected validation command scope

Require explicit user confirmation or correction before implementation delegation.

## Ralph Wiggum Loop (Bounded)

Use a bounded attempt loop for test-side fixes:

- attempt 1: implement best-supported fix
- attempt 2: adjust based on new failure evidence
- attempt 3: final focused adjustment

If still failing after 3 attempts:

1. Stop iterative fixing.
2. Refresh context via `managing-project-customizations` if stale/missing signals exist.
3. Ask the user for missing constraints, assumptions, or environment facts.

Never continue blind fix loops past 3 attempts.

## Rabbit-Hole Guardrails

- Do not widen test scope unless evidence requires it.
- Do not mix multiple speculative fixes in one attempt.
- Do not switch environments without an explicit reason.
- Do not treat retries/timeouts as root-cause fixes.
- Prefer narrowing to single failing test before suite-wide validation.

## Recent Change Analysis

Correlate failure evidence with recent modifications:

- changed selectors/page objects
- setup/auth/session utilities
- config/reporter/service changes
- env/script changes impacting execution mode

Use this correlation to prioritize hypotheses.

## Routing Real App Bugs

If evidence indicates product/app behavior regression (not test defect):

- classify as app bug
- route to `skipped-test-manager`
- include gathered evidence and reproduction details

## Output Format

Return concise orchestration summaries with:

- known inputs
- current hypothesis
- delegated action in progress
- attempt count (if in loop)
- stop/escalation reason when bounded loop exits

## Common Mistakes

- Running unbounded trial-and-error fix loops.
- Requesting code changes before confirming hypothesis with user.
- Skipping context refresh when evidence is stale.
- Treating app bugs as test-only fixes.
