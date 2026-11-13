---
name: debug
description: Use when encountering bugs, test failures, or unexpected behavior - find root cause before fixing
---

# Systematic Debugging

## The Rule

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## Four Phases

### Phase 1: Investigate

1. **Read error messages completely** - They often contain the solution
2. **Reproduce consistently** - Can you trigger it reliably?
3. **Check recent changes** - `git diff`, what changed?
4. **Trace data flow** - Where does the bad value come from?

### Phase 2: Find Pattern

1. Find working similar code in codebase
2. Compare working vs broken
3. List every difference

### Phase 3: Hypothesis

1. Form ONE hypothesis: "I think X because Y"
2. Make smallest possible change to test it
3. If wrong, form NEW hypothesis (don't pile fixes)

### Phase 4: Fix

1. Write failing test that reproduces bug
2. Implement single fix for root cause
3. Verify test passes
4. Verify no other tests broke

## Red Flags

If thinking:
- "Quick fix, investigate later" - STOP
- "Just try changing X" - STOP
- "I don't understand but this might work" - STOP

Return to Phase 1.

## 3+ Fixes Failed?

If you've tried 3+ fixes without success:
- STOP attempting more fixes
- Question the architecture
- Ask your orchestrator for guidance

## Quick Reference

| Phase | Do | Confirm |
|-------|-----|---------|
| Investigate | Read errors, reproduce, check changes | Understand WHAT and WHY |
| Pattern | Find working example, compare | Know the difference |
| Hypothesis | Single theory, minimal test | Confirmed or rejected |
| Fix | Test first, single fix, verify | Bug gone, tests pass |
