---
name: debugging
description: >-
  Systematic root-cause debugging: reproduce, investigate, hypothesize, fix with
  verification. Use when debugging, troubleshooting, or facing errors, stack
  traces, broken tests, flaky tests, or regressions.
---

# Debugging

## The Iron Law

Never propose a fix without first identifying the root cause. "Quick fix now, investigate later" is forbidden — it creates harder bugs.

**Trivially obvious bugs** are their own root cause — state the cause and fix directly. A bug is trivially obvious only when the **cause** is in the error message (e.g., `ModuleNotFoundError: no module named foo`, a typo in a string literal). If the error shows **where** something fails but not **why** (e.g., `TypeError: Cannot read 'id' of undefined`), it is not trivially obvious — investigate why the value is undefined.

## Root Cause Analysis

Root cause identification is the core deliverable of debugging — not the fix itself. A fix without a confirmed root cause is guesswork.

- **Trace backward**: Start at the symptom, walk the call chain in reverse to find where behavior diverges from expectation
- **Differential analysis**: Compare working vs broken state across dimensions (code version, data, environment, timing, configuration)
- **Regression hunting**: Use `git bisect` to pinpoint the exact commit that introduced the issue
- **Evidence-based**: Document root cause with `file:line` references, log output, and concrete reproduction proof
- **Competing hypotheses**: When the cause is ambiguous, generate multiple hypotheses and rank by evidence strength (see Escalation section below)

## Environment Diagnostics

Before investigating, capture the environment state using [collect-diagnostics.sh](./scripts/collect-diagnostics.sh):

```bash
bash collect-diagnostics.sh           # print to stdout
bash collect-diagnostics.sh diag.md   # write to file
```

Collects system info, language versions, git state, project files, and environment variables. Use during differential analysis to compare working vs broken environments, or attach to bug reports.

## Process

**0. Read the error.** Read the full error message, stack trace, and line numbers before doing anything. Error messages frequently contain the exact fix. Don't skim -- read the entire output.

**1. Reproduce** — make the bug consistent. If intermittent, run N times under stress or simulate poor conditions (slow network, low memory) until it triggers reliably.

**2. Investigate** — trace backward through the call chain from the symptom. Add diagnostic logging at each component boundary. Compare working vs broken state using a differential table (environment, version, data, timing — what changed?).

**3. Hypothesize and test** — one change at a time. If a hypothesis is wrong, fully revert before testing the next. Use `git bisect` to find regressions efficiently.

**4. Fix and verify** — create a failing test FIRST, then fix. Run the test. Confirm the original reproduction case passes. No completion claims without fresh verification evidence (see `verification-before-completion`).

## Three-Fix Threshold

After 3 failed fix attempts, STOP. The problem is likely architectural, not a surface bug. Escalate to the user before attempting further fixes. Step back and question assumptions about how the system works. Read the actual code path end-to-end instead of spot-checking.

**Architectural problem indicators** — signals the bug is structural, not a surface fix:
- Each fix reveals new shared state or coupling you didn't expect
- Fixes require massive refactoring to implement correctly
- Each fix creates new symptoms elsewhere in the system

**No root cause found:** If investigation is exhausted without a clear root cause, say so explicitly. Document what was checked, what was ruled out, and what instrumentation to add for next occurrence. An honest "unknown" with good diagnostics beats a fabricated cause.

## Escalation: Competing Hypotheses

When the cause is unclear across multiple components, use Analysis of Competing Hypotheses:
- Generate hypotheses across failure modes: logic error, data issue, state problem, integration failure, resource exhaustion, environment
- Investigate each with evidence: Direct (strong), Correlational (medium), Testimonial (weak)
- Cite evidence with `file:line` references
- Rank by confidence. If multiple hypotheses are equally supported, suspect compound causes.

## Intermittent Issues

- Track with correlation IDs across distributed components
- Race conditions: look for shared mutable state, check-then-act patterns, missing locks. In async code (Node.js, Python asyncio): interleaved `.then()` chains, unguarded shared state between concurrent tasks, missing transaction isolation in DB operations
- Deadlocks: check for circular lock acquisition (DB row locks held across multiple queries), circular `await` dependencies in async code, connection pool exhaustion blocking queries that would release other connections
- Resource exhaustion: monitor memory growth, connection pool depletion, file descriptor leaks. Under load: check pool size vs concurrent request count, verify connections are returned on error paths (finally/dispose)
- Timing-dependent: replace arbitrary `sleep()` with condition-based polling — wait for the actual state, not a duration

## Defense-in-Depth Validation

After fixing, validate at every layer — not just where the bug appeared:
- **Entry**: does invalid input get caught?
- **Business logic**: does the fix handle edge cases?
- **Environment**: does it work across configurations?
- **Instrumentation**: add logging to detect recurrence

## Bug Triage

When multiple bugs exist, prioritize by:
- **Severity** (data loss > crash > wrong output > cosmetic) separately from **Priority** (blocking release > customer-facing > internal)
- Reproducibility: always > sometimes > once. "Sometimes" bugs need instrumentation before fixing.
- Quick wins: if a fix is < 5 minutes and unblocks others, do it first

## Common Patterns

- **Null/undefined access** — trace where the value was expected to be set, check all code paths
- **Off-by-one** — check `<` vs `<=`, array length vs last index, loop boundaries
- **Async ordering** — missing `await`, unhandled promise rejection, callback firing before setup completes
- **Type coercion** — `==` vs `===`, string-to-number conversion, truthy/falsy edge cases
- **Timezone** — always store UTC, convert at display. Check DST transitions.
- **Stale state** — cached values, stale closures, outdated config, old build artifacts. When behavior contradicts the code you're reading, verify you're running what you think you're running.

## Pattern Comparison

When the cause isn't obvious, find working similar code in the codebase and compare it structurally with the broken path. Read the working reference implementation completely — don't skim. List every difference between working and broken, however small. Don't assume any difference can't matter. The bug is in one of them.

## Anti-Patterns and Red Flags

When you catch yourself doing or thinking these things, **stop and return to Phase 1 (Reproduce/Investigate)**:

| What You're Doing / Thinking | What It Really Means |
|-----------------------------|---------------------|
| Shotgun debugging — random changes without a hypothesis | You're guessing. Form a hypothesis first, then revert and test one change. |
| Multiple simultaneous changes | You're making the problem harder to diagnose. One change at a time. |
| Fixing the symptom, not the cause | The same bug will resurface differently. Trace to root cause. |
| Ignoring intermittent failures ("works on my machine") | Instrument and reproduce under load instead. |
| "Quick fix for now, investigate later" | You don't understand the root cause. Later never comes. |
| "Skip the test, I can see it works" | You can't. Run the verification. See `verification-before-completion`. |
| "It's probably X" | "Probably" means you haven't verified. Trace the actual execution path. |
| "One more fix attempt" (after 2+ failures) | You've hit the three-fix threshold. Step back and question assumptions. |
| "I see the problem, let me fix it" | Seeing symptoms is not understanding root cause. Trace the actual execution path first. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I'll clean up the debugging later" | Remove diagnostic code now or it ships to production. |

## Signals You're Off Track

Watch for these signs from the user — they indicate you've left the systematic process:

- "Is that not happening?" — you assumed behavior without checking
- "Will it show us...?" — you're not gathering enough evidence
- "Stop guessing" — you're proposing fixes without root cause
- "We're going in circles" — same hypothesis repackaged, not a new approach
- Repeating the same type of fix with slight variations — that's not a new hypothesis

## Integration

This skill is referenced by:
- `workflows:work` — during task execution for bug investigation
- `writing-tests` — creating failing tests to reproduce bugs
- `verification-before-completion` — before claiming a bug is fixed

## Postmortem

After resolving non-trivial bugs, document a lightweight postmortem:

1. **Timeline**: when introduced, when detected, when resolved (include commit SHAs)
2. **Root cause**: one sentence — the actual cause, not the symptom
3. **Impact**: what broke, for how long, who was affected
4. **Fix**: what changed and why this fix addresses the root cause
5. **Prevention**: what test, monitor, or process change prevents recurrence
