---
name: cc-debugging
description: "Applies Code Complete's scientific debugging method: STABILIZE → LOCATE → HYPOTHESIZE → EXPERIMENT → FIX → TEST → SEARCH. For active bug investigation, not QA process design or test coverage planning (use cc-quality-practices)."
user-invocable: false
---

# cc-debugging

Most debugging time goes to finding and understanding the defect; the fix is usually obvious once you understand it. Every action tests a hypothesis — no guessing, no random changes.

First action on any bug: run the failing test or repro and read its actual output. Do this before reading the source in depth and before editing anything — the observed failure, not the code you infer it from, is what you debug. If the usual runner is unavailable (e.g. no `pytest`), fall back to a runnable form (`python3 -c`, a direct script) and capture that output now, not after a fix.

Shared numeric thresholds (20:1 debugger variation, ~50% of fixes wrong first time): `Read(${CLAUDE_PLUGIN_ROOT}/references/cc-foundations.md)`.

## Scientific Debugging Method

```
STABILIZE → LOCATE → HYPOTHESIZE → EXPERIMENT → FIX → TEST → SEARCH
```

### Step 1: STABILIZE

Get a reliable reproduction — you cannot debug what you cannot reproduce.

**Precondition on editing:** the first tool action of the session is running the failing test or repro, and its output is captured, BEFORE any Edit to implementation code. The order is run-test → then edit, never edit-then-test. If the standard runner is missing, run the repro another way (`python3 -c`, a direct script) and capture that — the missing runner does not excuse skipping the observed failure.

- Reduce to the smallest case that still fails.
- Intermittent failures are usually initialization errors, timing issues, or dangling pointers.
- Record the exact conditions: inputs, environment, order of operations.

### Step 2: LOCATE

Narrow the suspicious region before forming a hypothesis.

- Binary search: disable code sections until the failure disappears → the bug is in what you removed.
- Check recently changed code first (defects cluster around changes).
- Check modules with prior defect history (defects cluster by module).
- Look for patterns: specific data? specific user? specific environment?

### Step 3: HYPOTHESIZE

Form a specific, testable hypothesis — not "the bug is somewhere in module X."

- Good: "The counter isn't reset between requests because X shares state with Y."
- Use all available data: logs, stack traces, variable values, test outputs.
- One hypothesis at a time; rank competing candidates; brainstorm alternatives before committing.

### Step 4: EXPERIMENT

Design a test that will **disprove** the hypothesis, not confirm it.

- Add targeted logging or assertions at the suspected site, or write a failing test that would pass if the hypothesis holds.
- Observe before changing production code.
- Record results; update or discard the hypothesis based on what you see.

### Step 5: FIX

Fix the root cause, not the symptom.

- Understand the program vicinity (hundreds of lines, not just the bug line).
- Rule out competing hypotheses before committing to the diagnosis.
- Make one change at a time; keep the original source.

### Step 6: TEST

Verify the fix actually works.

- Triangulate: multiple different test cases, not just the original repro.
- Add a regression test that would have caught this bug.
- Run the full test suite and report the result.

### Step 7: SEARCH

Defects cluster — if this bug existed, similar ones likely exist nearby.

**Precondition on completing:** before reporting the fix complete, a search for the same defect pattern (grep/Glob) has been run and its result recorded.

- Search for the same pattern elsewhere in the codebase.
- Check the module's other methods for similar logic.
- Check other code from the same author or era.

---

## Common Defects Quick Check

Rule these out before deep investigation:

- Off-by-one: loop bounds (`<` vs `<=`), array index vs length
- Null / undefined dereference before checking
- Race condition (intermittent, timing-dependent)
- Uninitialized variable
- Incorrect operator precedence (add explicit parentheses)
- Floating-point equality (`==` instead of epsilon comparison)
- Resource leak: file handle, connection, or lock not released on an error path
- Logic inversion: wrong branch taken

When quick checks fail and the systematic method stalls, the brute-force techniques (full code review, isolate in a harness, rewrite the section) and the full defect catalog are in `Read(${CLAUDE_SKILL_DIR}/checklists.md)`.

---

## Confessional debugging

Explain the problem out loud, to a person or a rubber duck. Articulation frequently reveals the bug before the listener responds.

---

## Chain

| After | Next |
|---|---|
| Root cause found | Fix + add regression test (Steps 6–7 above) |
| Defect is in untested legacy code | `Skill(code-foundations:welc-legacy-code)` — get it under test first |
| Fix requires structural refactoring | `Skill(code-foundations:cc-refactoring-guidance)` |
