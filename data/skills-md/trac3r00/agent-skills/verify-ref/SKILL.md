---
name: verify-ref
description: Comprehension gate before porting, copying, or adapting an existing implementation. Proves understanding of the reference code before any new code is written. Use when the task is "port X", "copy how Y does it", "adapt Z", or reimplementing existing behavior.
version: 1.0.0
author: Hien Dinh
license: MIT
---

# Reference Verification

Prove you understand the reference implementation BEFORE porting it.
Misunderstood references produce confidently wrong ports.

<HARD-GATE>Write no implementation code until the user confirms the
comprehension proof below.</HARD-GATE>

## Process

1. **Locate the reference.** Use the argument or conversation context. If
   ambiguous, ask which implementation is the reference — don't guess.
2. **Set a behavioral boundary, then read it fully.** Read the referenced unit,
   its direct callers, and direct dependencies that affect observable behavior.
   Follow deeper calls only while they change outputs, side effects, errors, or
   ordering. List unresolved or external dependencies instead of recursively
   expanding without a stop condition.
3. **Produce the comprehension proof**, covering:
   - **Data flow:** inputs → transformations → outputs, in order
   - **Edge cases handled:** every guard, fallback, retry, and special case,
     and what each protects against
   - **Invariants:** what must remain true before/after (ordering, uniqueness,
     idempotency, transactional boundaries)
   - **Hidden dependencies:** globals, config, environment, call-order
     assumptions, side effects the signature doesn't show. For UI code, also
     name the framework semantics the reference leans on: lifecycle hooks that
     fire once vs. per-render, view identity, and task/cleanup-on-teardown
     behavior — these are where ports break silently.

   Proportionality: for a small same-repo adaptation (roughly ≤30 lines, no
   concurrency, no money/auth/persistence), a short proof of just **Data flow**
   and **What would break if I got this wrong?** suffices — but step 2's full
   read of the reference and its callers is never skipped; that read is where
   latent bugs surface.
4. **Self-challenge.** Add a section: "What would break if I got this wrong?" —
   name the 2-3 misreadings most likely to cause a subtly wrong port and say
   why your reading is correct (cite file:line evidence).
5. **Gate.** Ask the user to confirm the proof or correct it. Only after
   confirmation may implementation begin. A plan the user already approved that
   names this exact port also counts as confirmation — say the proof is being
   accepted under that approval and proceed. Otherwise, if no interactive user
   is available, stop after the proof and identify the exact uncertainty that
   needs review; do not silently treat the proof as approval.

## Output format

```
## Comprehension proof: <reference name> (<file:line range>)
### Data flow
### Edge cases handled
### Invariants
### Hidden dependencies
### What would break if I got this wrong?
```
