---
name: debug
description: Load this skill when diagnosing a defect, failure, crash, or unexpected behavior - reproduce, observe, isolate, hypothesize, fix the root cause minimally, and verify.
user-invocable: true
---

# Debug

Category: Development (Engineering) - Troubleshooting

## Purpose

Find the root cause of a failure and fix it with the smallest safe change -
not silence it, not patch around it.

## Workflow

1. **Reproduce.** Establish deterministic steps that trigger the failure. If
   it cannot be reproduced, suspect environment, data, or timing - in that
   order - and vary one of them at a time. An unreproducible bug is an
   unfixable bug; say so early.
2. **Observe.** Read the actual error message, log, stack trace, and state.
   The error text is data, not noise. Never hypothesize before reading what
   the system actually said.
3. **Isolate.** Cut the system down until the failure's location is narrow:
   - Recent changes first: `git log` / `git diff` on the touched area,
     bisect if needed.
   - Cut the input to the smallest case that still fails.
   - Log at boundaries; check what crosses the seam where two components
     meet - bugs cluster at boundaries, not in the middle of functions.
4. **Hypothesize.** One falsifiable hypothesis at a time. Change exactly one
   thing, re-run the reproduction, observe. The hypothesis is either
   confirmed or you learned something - both are progress; write down which.
5. **Fix.** Fix the root cause with a minimal diff. Fixing a symptom is
   acceptable only as a temporary, labeled stopgap.
6. **Verify.** Write the failing test first (or reproduce it), confirm it
   fails, apply the fix, confirm it passes, then run the surrounding suite
   to prove no collateral damage.
7. **Close the loop.** State why the bug escaped and add the cheapest guard
   that prevents its return (a test, an assertion, a validation).

## Heuristics

- The bug is usually at a boundary: input parsing, serialization,
  permissions, time zones, null handling, concurrency.
- "It worked before" -> diff against the last known-good state before
  theorizing.
- Flaky = real. Intermittent failures are usually uninitialized state,
  race conditions, or shared data - treat them as bugs, not noise.

## Stop conditions

- Two failed attempts with the same approach: stop, re-read the evidence,
  change strategy fundamentally, or ask the user one concrete question.
- Never "fix" by adding a catch block that swallows the error, deleting
  the failing test, or widening a condition until the symptom disappears.
