---
name: debugging
description: "You MUST use this when something is broken - a failing test, a crash, a regression - instead of guessing at a fix. The goal is to find the ROOT CAUSE and fix it test-first with a regression test that fails without the fix. You are not allowed to change code before you can reproduce the bug and explain the mechanism, or to patch the symptom. A standalone skill invoked on demand, not a workflow stage. Trigger phrases: debug this, why is this failing, root cause, it regressed, fix this crash."
argument-hint: "Describe the symptom, e.g. 'specs/001-auth T3 test fails' or 'checkout 500s on submit'."
---

# Debugging

The loop builds, reviews, and verifies. When something is **broken** — a failing test, a crash, an unexplained regression — treating the symptom is how the same bug comes back. This skill is a **standalone debugging practice**: find the **root cause** first, then fix it. Reach for it whenever there's a bug to chase; it stands on its own and does not depend on any workflow.

It is a discipline you apply on demand, alongside whatever workflow you happen to be in. If you're inside `fight`, the fix flows back through the normal loop (built test-first and re-verified); standalone, you still fix test-first and prove it. Either way, this skill owns _how_ you find the cause — not when.

## The Model

| Thing            | What it is                                                      | Where it lives       |
| ---------------- | --------------------------------------------------------------- | -------------------- |
| **Symptom**      | The observable wrong behavior (the failing assertion, the 500). | the command's output |
| **Reproduction** | The smallest, most deterministic way to see it fail on demand.  | a failing test       |
| **Cause**        | The specific line/decision that produces the symptom.           | named in your report |
| **Hypothesis**   | A falsifiable guess about the cause, tested before fixing.      | your notes           |
| **Regression**   | A test that fails without the fix and passes with it.           | the repo             |

The core discipline: **you do not understand the bug until you can reproduce it and explain the mechanism.** A fix without a cause is a guess that happens to pass.

## When to Use

- Something is broken: a failing test, a crash/500, an unexplained regression.
- A bug report names a symptom with no known cause.
- You're about to "just try" a fix — stop and run this instead.
- The user says **"debug this"**, **"why is this failing"**, or **"find the root cause"**.

**Do NOT use** to design new behavior (that's `brainstorming`/`system-design`), to write the fix as a feature (that's the loop's `implement`), or to simply _confirm_ a fix once the cause is known (that's `verify`/running the tests). Debugging finds the cause; the fix is then built and proven.

**Standalone by design.** This skill needs no orchestrator and gates no phase — it's a tool you pick up whenever there's a bug to chase, inside or outside any workflow.

## The Iron Law

```
REPRODUCE AND EXPLAIN THE CAUSE BEFORE YOU CHANGE THE CODE
```

A fix written before the cause is understood is a guess. Guesses pass by luck, ship the same bug elsewhere, and come back as regressions. Violating the letter of this rule is violating the spirit of it.

## Core Rules

- **Reproduce first, on demand.** Get a deterministic failure — ideally a failing test — before theorizing. "It broke once" is not a starting point; make it break every time.
- **Find the cause, not a cause.** Trace the failure to the specific line or decision responsible. If you can't point at it, you haven't found it.
- **One hypothesis at a time.** State the guess, then test it with the cheapest experiment that would prove it wrong. Don't change three things and hope.
- **Change one thing per experiment.** Bundled edits make the result uninterpretable — you won't know which change mattered.
- **Read the actual error.** The full stack trace, the real assertion diff, the log line — not your memory of what it usually is. The bug is usually in what you skipped.
- **Bisect when the cause is hidden.** `git bisect`, disabling half the inputs, narrowing the failing case — halving the search beats reading everything.
- **A fix ships with its regression test.** The fix's test fails without it and passes with it. That test is proof the cause was real.
- **Stop and ask when the cause is out of scope.** If the real cause is a spec/plan/design defect, don't patch around it — send it back (`brainstorming`/`planning`/`system-design`).

## Procedure

### 1. Capture the symptom

Write down the exact expected vs. actual, and the command that shows it. Read the **full** output: the whole stack trace, the failing assertion, the exit code. Identify the **first** wrong thing, not the loudest.

### 2. Reproduce deterministically

Get a failure you can trigger on demand. Write a failing test for it when you can (this becomes the regression test). If it's intermittent, that's a clue — a race, shared state, or an unhandled order — not a reason to move on; make it fail reliably first.

### 3. Isolate (bisect the space)

Narrow where the cause lives before guessing:

- **In the code:** `git bisect` from a known-good commit; or comment out / bypass halves of the path.
- **In the input:** shrink the failing case to the smallest input that still fails; find the smallest that doesn't.
- **In the layers:** is it the code, the data, the config, the environment, or the integration? Rule each out.

### 4. Hypothesize, then prove

State one falsifiable hypothesis ("the token check runs before the user is loaded, so `user` is null at line 42"). Design the **cheapest experiment that would disprove it** — a log line, a breakpoint, a one-off assertion, a focused test. Run it. Keep or discard the hypothesis on the evidence.

### 5. Find the actual cause

Repeat 3–4 until you can name the specific line/decision that produces the symptom, **and explain the mechanism** — why this input leads to this failure. If reaching "it works now" without that explanation, you got lucky; keep digging.

### 6. Fix it test-first, then prove it

With the cause named, write the fix **test-first**: the failing test from step 2 is the RED, the fix makes it GREEN. The fix must include the regression test — it fails without the fix and passes with it. Then prove the green with fresh evidence (the loop's `verify` gate). If you're inside fight mode, the fix continues through the normal loop; if not, you still commit the fix with its regression test.

## Red Flags

| Thought                                          | Reality                                                                                |
| ------------------------------------------------ | -------------------------------------------------------------------------------------- |
| "I'll just try changing this and see"            | That's a guess. Name the cause first; then test one hypothesis.                        |
| "It works now, ship it"                          | Without a mechanism you fixed a symptom. It will come back.                            |
| "Let me change a few things at once"             | You won't know what worked. One change per experiment.                                 |
| "I read the error, I know what it is"            | Read the _whole_ trace — the cause is usually in the frame you skipped.                |
| "It's flaky, I'll ignore it / re-run it"         | Flaky is a defect — a race or shared state. Make it fail on demand first.              |
| "The reviewer is wrong, my code's fine"          | Prove it — with the code path or a test — or accept the finding.                       |
| "I'll patch the test to make it pass"            | Changing the test to match a bug is hiding it. Fix the cause, keep the test.           |
| "The quick fix is easier than finding the cause" | Quick fixes stack into a regression you can't untangle. Find the cause.                |
| "The cause is really a spec/design defect"       | Then it's out of scope — send it back, don't patch around it.                          |
| "Same symptom as last time, apply the same fix"  | Re-check the cause — the same symptom can have a new cause. One change per experiment. |

## Completion Check

Debugging is done when ALL are true:

- [ ] The symptom is captured exactly (expected vs. actual, with the command and its full output read).
- [ ] The failure reproduces **deterministically** (ideally as a failing test), or its flakiness is understood as a clue.
- [ ] The search space was **isolated** (code/inputs/layers bisected), not guessed at.
- [ ] The **specific** cause is named, and the mechanism explained — not just "it works now".
- [ ] Hypotheses were tested **one at a time**, one change per experiment.
- [ ] The fix ships a **regression test that fails without it** and passes with it.
- [ ] The green was proven with fresh evidence (the loop's `verify` gate), not assumed.
- [ ] If the real cause was a spec/plan/design defect, it was sent back rather than patched around.
