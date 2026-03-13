---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---

# Systematic Debugging

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## Phase Task Enforcement

Create native tasks for each phase:

1. **"Phase 1: Root Cause Investigation"** — Read errors, reproduce, check changes, gather evidence. MUST understand WHAT and WHY before proceeding.
2. **"Phase 2: Pattern Analysis"** — Find working examples, compare, identify differences. `addBlockedBy: [phase-1-id]`
3. **"Phase 3: Hypothesis & Testing"** — Form single hypothesis, test minimally, verify. `addBlockedBy: [phase-2-id]`
4. **"Phase 4: Implementation"** — Create failing test, implement single fix, verify. `addBlockedBy: [phase-3-id]`

**ENFORCEMENT:**
- TaskList shows blocked phases — you CANNOT propose fixes until Phase 1-3 show `status: completed`
- Blocked tasks cannot be marked in_progress — no skipping ahead
- Task state is visible proof of process — rationalizing around this is visible
- Mark each phase complete only when its success criteria are met

## When to Use

**Any technical issue:** test failures, bugs, unexpected behavior, performance problems, build failures.

**Especially when:** under time pressure, "just one quick fix" seems obvious, previous fix didn't work.

**Don't skip when:** issue seems simple, you're in a hurry, manager wants it fixed NOW.

## The Four Phases

Complete each phase before proceeding to the next.

**Phase 1: Root Cause Investigation** — Read errors, reproduce, check recent changes, gather evidence at boundaries, trace data flow. **Success:** Understand WHAT and WHY. See `references/phase-1-investigation.md`

**Phase 2: Pattern Analysis** — Find working examples, compare completely, identify all differences, understand dependencies. **Success:** Differences identified. See `references/phase-2-pattern-analysis.md`

**Phase 3: Hypothesis and Testing** — Form single specific hypothesis, test with smallest change, verify. **Success:** Hypothesis confirmed or replaced. See `references/phase-3-hypothesis-testing.md`

**Phase 4: Implementation** — Create failing test, implement single fix for root cause, verify no regressions. If 3+ fixes failed, question architecture. **Success:** Bug resolved, tests pass. See `references/phase-4-implementation.md`

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

## When Process Reveals "No Root Cause"

If investigation reveals issue is truly environmental, timing-dependent, or external: document what you investigated, implement handling (retry, timeout, error message), add monitoring. **But:** 95% of "no root cause" cases are incomplete investigation.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Here are the main problems: [lists fixes without investigation]"
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (see Phase 4). See `references/rationalizations.md` for common excuses.

## Reference Files

- `references/phase-1-investigation.md`: Detailed Phase 1 steps
- `references/phase-2-pattern-analysis.md`: Detailed Phase 2 steps
- `references/phase-3-hypothesis-testing.md`: Detailed Phase 3 steps
- `references/phase-4-implementation.md`: Detailed Phase 4 steps
- `references/rationalizations.md`: Common excuses and user signals
- `references/real-world-impact.md`: Systematic vs random debugging statistics
- `references/root-cause-tracing.md`: Backward tracing for deep call stacks
- `references/defense-in-depth.md`: Multi-layer validation after root cause
- `references/condition-based-waiting.md`: Condition polling to replace timeouts
- `references/condition-based-waiting-example.ts`: TypeScript example
- `references/find-polluter.sh`: Script to find test pollution sources
- `references/CREATION-LOG.md`: Skill creation history
- `references/tests/`: Pressure test scenarios

<!-- compressed: 2026-02-11, original: 853 words, compressed: 621 words -->
