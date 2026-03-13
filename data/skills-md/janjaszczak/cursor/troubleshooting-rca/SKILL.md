---
name: troubleshooting-rca
description: Perform root-cause analysis for bugs/errors/regressions using logs, repro steps, and hypothesis testing. Use when the user reports “nie działa”, stack traces, failing tests, or regressions.
compatibility: Requires access to logs/tests and ability to run minimal diagnostics.
allowed-tools: Bash(*) Read FileSearch(*)
metadata:
  intent: Avoid RCA ritual when building greenfield features.
---

# troubleshooting-rca

## Activation gate (anti-noise)
Activate when:
- There is an error message, failing test, crash, regression, unexpected behavior, or logs.

Skip when:
- User requests implementation from scratch and no failure exists yet.

## Procedure
1. Restate symptom + expected behavior.
2. Collect minimal repro:
   - Command, input, environment, last known good commit.
3. Hypotheses (max 3) ranked by likelihood.
4. Test each hypothesis with the smallest possible check.
5. **Before Fix:** Root cause must be clearly stated; one minimal verification step must be given. Then: Fix + verify with test/run.
6. Add a prevention note (test, guard, logging).

## Output
- Symptom → Most likely cause → Fix → Verification command(s).
