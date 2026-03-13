---
name: acceptance-criteria-validate
description: Use when an agent executing an implementation plan claims to have finished, to validate that all acceptance criteria were actually met. Locates acceptance criteria from the plan file, acceptance_criteria.md, or the request itself, then investigates the codebase and surfaces a pass/fail verdict per criterion.
---

# Acceptance Criteria: Validate

## Step 0: Check for Context

If no request, task description, or plan file was provided as context (the skill was invoked with no arguments and nothing in the conversation identifies what was implemented):

- Output: "This skill needs context to validate against. Please provide the request description, a plan file path, or point me to an acceptance_criteria.md file."
- **STOP — do not continue.**

---

## Step 1: Locate Acceptance Criteria

Work through the following sources in order, stopping as soon as criteria are found.

### Source 1: Plan file referenced in context

Check whether the context references a plan file (a `.md` path, usually under `.agents/plans/`).

**If a plan file is identified:**
- Read the entire plan file
- Search for any of these headings (case-insensitive):
  - `## ACCEPTANCE CRITERIA`
  - `## Acceptance Criteria`
  - `## Success Criteria`
  - `## Completion Criteria`
  - `## Done When`
- Also scan the `## COMPLETION CHECKLIST` section — individual checklist items there may function as acceptance criteria even if not labeled as such
- Extract all criteria found. **If criteria exist here → proceed to Step 2 with these.**

### Source 2: `acceptance_criteria.md` file

If no criteria were found in the plan file, search for `acceptance_criteria.md` in:
- `.agents/acceptance_criteria.md`
- `acceptance_criteria.md` (project root)

**If found:**
- Read the file
- Identify whether any section title or context summary matches the current request or feature (by name, date, or description similarity)
- If a matching section exists → extract its criteria and **proceed to Step 2 with these**
- If the file exists but no section matches → note this and continue to Source 3

### Source 3: Criteria embedded in the request itself

If neither of the above yielded criteria, re-read the current request (the message that triggered this skill or the broader conversation context). Look for:
- Explicit "success criteria", "acceptance criteria", or "done when" statements
- Numbered or bulleted requirements the user stated
- Phrases like "I expect...", "it should...", "the feature is done when..."

**If found in the request → proceed to Step 2 with these.**

### Source 4: Ask the user

If no criteria were found in any source:

First, derive your own suggested criteria based on the request description and any plan content you have read (apply the same dimension framework as the `acceptance-criteria-define` skill: functional correctness, error handling, integration/E2E, validation, non-functional, out of scope).

Then use **AskUserQuestion**:

Question: "I couldn't find any acceptance criteria for this request. Here's what I'd suggest — do these look right, or would you like to define your own?"

Present the suggested criteria in the question context, then offer:
1. "Use your suggested criteria" — proceed with what you proposed
2. "I'll define them myself" — wait for the user to provide criteria before continuing

**Do not proceed to Step 2 until criteria are confirmed.**

---

## Step 2: Validate Each Criterion

For each criterion, investigate whether it has been met. Use a structured approach per criterion:

### Investigation methods (use as appropriate per criterion)

**Code inspection:**
- Read the relevant source files called out in the plan or implied by the criterion
- Check for the presence and correct implementation of expected logic, endpoints, functions, or behaviors
- Verify error handling paths, not just happy paths

**Test evidence:**
- Look for test files covering the criterion (unit, integration, or E2E)
- Check test names and assertions — do they specifically validate the criterion's stated behavior?
- Note: a passing test suite does not automatically mean a criterion is met if the tests don't cover the specific behavior

**Configuration and wiring:**
- For criteria involving config, env vars, or startup wiring: read entry point files (`main.py`, `app.py`, etc.) and verify the wiring is actually present, not just documented
- For criteria involving external services or MCP tools: check URL construction, auth headers, and connection logic

**Documentation and artifacts:**
- Check `PROGRESS.md` for notes indicating the criterion was addressed or explicitly deferred
- Check `.agents/execution-reports/` for any execution report for this feature
- Check git diff / recently changed files if helpful context is needed

**Run validation commands (if safe and appropriate):**
- If the plan's `## VALIDATION COMMANDS` section lists commands and it is safe to run them in the current environment, run them and use the results as evidence
- Do not run commands that could have side effects (migrations, deployments, destructive ops) without confirmation

**Deferred demo/script validation — MANDATORY structural probe:**
When a demo script or CLI is marked UNVERIFIABLE or deferred due to environmental constraints (live server, external auth, human approval step), do NOT accept the deferral without running a structural probe:
1. `python -c "import <module>"` — verifies no import/syntax errors
2. Run the script up to its first blocking dependency (live server call, `input()`, etc.) — catches encoding errors, misconfigured subprocess invocations, and wiring bugs before the environmental gate
3. Inspect any new subprocess invocations for inherited env-var hazards (especially `CLAUDECODE`, `PATH`, secret vars)
Mark as PARTIAL (not UNVERIFIABLE) if these structural checks are skipped. "Covered at unit level" is only a valid deferral for library behavior, never for the executable surface of the deliverable.

**Hardcoded HTTP endpoint URLs:**
For any criterion involving HTTP calls introduced in the feature, verify at least one representative hardcoded URL against the live server's registered routes (e.g., `curl -I <url>` or check `main.py` router/mount registrations). A 404 on a newly introduced URL is a FAIL, not UNVERIFIABLE — incorrect URLs cause silent tool-call failures that are very hard to diagnose.

### Per-criterion verdict

For each criterion, produce one of:

- **PASS** — Evidence clearly shows the criterion is met (cite the specific file, line, test, or output)
- **FAIL** — Evidence shows the criterion is not met or was skipped (explain what is missing)
- **PARTIAL** — The criterion is partly met but not fully (describe what is done and what is missing)
- **UNVERIFIABLE** — Cannot determine from available artifacts whether the criterion is met (explain why — e.g., requires a live service, requires manual observation)

---

## Step 3: Produce the Validation Report

Format the report as follows:

```
## Acceptance Criteria Validation Report

**Feature / Request:** <short description>
**Plan File:** <path or "none">
**Criteria Source:** <Plan file / acceptance_criteria.md / Request / User-defined>
**Validated:** <date>

---

### Results

| # | Criterion | Verdict | Evidence |
|---|-----------|---------|----------|
| 1 | <criterion text> | PASS / FAIL / PARTIAL / UNVERIFIABLE | <1–2 sentence evidence summary> |
| 2 | ... | ... | ... |

---

### Summary

**PASS:** <n>
**FAIL:** <n>
**PARTIAL:** <n>
**UNVERIFIABLE:** <n>
**Total:** <n>

**Overall verdict:** ACCEPTED / REJECTED / NEEDS REVIEW

- ACCEPTED — all criteria PASS (UNVERIFIABLE items acknowledged)
- REJECTED — one or more criteria FAIL
- NEEDS REVIEW — one or more criteria PARTIAL or UNVERIFIABLE with no other FAILs

---

### Failures & Gaps

<For each FAIL or PARTIAL criterion:>

#### Criterion <#>: <criterion text>

**Verdict:** FAIL / PARTIAL
**What is missing:** <specific description>
**Where to look / fix:** <file path, function, or area of the codebase>
**Suggested next step:** <concrete action — e.g., "Implement X in file Y", "Add test case for Z">

---

### Notes

<Any UNVERIFIABLE items with explanation of what manual verification would require>
<Any observations about gaps in the criteria themselves>
```

---

## Step 4: Write or Display the Report

**If invoked as a background subagent** (spawned via the Agent tool from another skill, e.g., from the `execute` skill's post-execution flow):
- Always write the report to `.agents/acceptance-validations/<feature-name>-validation.md`
- Derive `<feature-name>` from the plan file name or the request title
- Return a concise summary to the caller: file path + overall verdict + list of any FAILs or PARTIALs
- This ensures the orchestrating agent can read the full results even if it cannot see subagent output directly

**If the caller requested output to a file** (e.g., "save the validation report", "write to a file"):
- Write the report to `.agents/acceptance-validations/<feature-name>-validation.md`
- Derive `<feature-name>` from the plan file name or the request title
- Output to the user: "Validation report written to `.agents/acceptance-validations/<feature-name>-validation.md`."

**If the caller requested output to the CLI** (default when invoked interactively with no file destination specified):
- Output the full report directly to the conversation

**In all cases**, end with one of these verdicts printed prominently:

```
Overall: ACCEPTED   — all acceptance criteria met, ready for commit/review
Overall: REJECTED   — <n> criteria not met, execution is incomplete
Overall: NEEDS REVIEW — <n> criteria need manual confirmation before accepting
```

---

## Step 5: Gate on Verdict

**If verdict is ACCEPTED:**
- Inform the caller (or the user) that execution is complete and the work meets the defined acceptance criteria
- If this skill was invoked from within the `execute` skill flow, return control to that skill to proceed with the Output Report

**If verdict is REJECTED or NEEDS REVIEW:**
- Do NOT declare execution complete
- List the failing or unresolved criteria clearly
- Ask the user (or return to the calling skill) with:

  "The following criteria were not met. Should I fix them now, or do you want to review first?"

  Options:
  1. "Fix them now" — proceed to address each FAIL/PARTIAL criterion, then re-run this skill
  2. "I'll review first" — stop here and hand control back to the user
  3. "Accept anyway" — override and mark as complete despite gaps (user takes responsibility)

**Do not silently pass failed criteria.**
