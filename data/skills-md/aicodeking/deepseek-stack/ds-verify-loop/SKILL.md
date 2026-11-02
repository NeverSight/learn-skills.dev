---
name: ds-verify-loop
description: "Run edit, real check, read the actual error, fix the root cause, rerun, until the check passes or the cap is hit. Use when you change code that has tests, a type checker, a build, or a runnable app, or before you claim any fix works. Invoke as /ds-verify-loop."
---

# ds-verify-loop

Prove a change works by running the real check and fixing what it reports, not what you expect it to report.

## Steps

1. Pick the check before you edit: the narrowest real command that proves the change, such as one test file, a typecheck, a build, or a run of the app with one request. Write the command down.
2. Run it once before the edit if you can, so you know the baseline (already failing, already passing, or broken for another reason).
3. Make the smallest edit that should satisfy the check.
4. Run the exact command. Read the full error output, including the first error, the file and line, and the stack frame in your code. Do not skim to the last line.
5. State the root cause in one sentence, based on the output. If you cannot, add one print or log line, or read the failing code, and rerun. Do not guess.
6. Fix the cause, not the symptom. Do not add a special case for the one input that the test uses.
7. Rerun the same command. Count this as one iteration.
8. When the narrow check passes, run the wider one once (the full test suite, the build, or a lint) to catch breakage elsewhere.
9. Paste the final passing output (the command and its last lines) in your reply or in PROGRESS.md.

## Stop when

- The check passes and you have pasted the output. A claim without output does not count.
- You reach 5 iterations without passing. Stop editing, report the last error, and switch to ds-unstick.
- The same error appears twice after two different fixes. Switch to ds-unstick now. Do not wait for iteration 5.

## Rules

- Never weaken, skip, delete or loosen a test, assertion, type or lint rule to make the check pass. If the test is wrong, say why and ask first.
- Never mock away the thing under test.
- Run the real command every time. Do not reason about what it would print.
- Change one thing per iteration so that you know what fixed it.
- If no check exists, write the smallest one that fails without your change, then use the loop.
