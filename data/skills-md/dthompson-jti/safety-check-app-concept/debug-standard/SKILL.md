---
name: debug-standard
description: Systematic root cause analysis for reproducible bugs. Use when you have a bug that can be reproduced.
---

# Debug Standard

Systematic root cause analysis for reproducible bugs.

## When to Use
- Reproducible bugs
- Clear symptoms
- Standard complexity

## Scope Escalation
If fix touches >5 files or shared component API, escalate to `debug/deep`.

## Artifacts
- `DEBUG-PLAN-[BUG-ID].md` (optional)
- `task.md` updated via `task_boundary`

## Approach

### Phase 1: Observation & Reproduction
Document:
- **Steps to Reproduce**: Numbered list
- **Expected Behavior**: What should happen
- **Actual Behavior**: What happens instead
- **Environment**: Browser, OS, relevant state

### Phase 2: Hypothesis & Investigation
Generate **3-4 hypotheses**:

| # | Hypothesis | Confidence | Evidence Needed | Investigation |
|---|------------|------------|-----------------|---------------|
| 1 | ... | High | Check X | `grep` for pattern |
| 2 | ... | Medium | Trace Y | Add logging |
| 3 | ... | Low | Log Z | Run with --verbose |

### Phase 3: Root Cause & Fix
1. Confirm root cause with evidence
2. Plan fix using holistic principles
3. **Reflexion**: Hostile QA — list 2-3 regression risks

### Phase 4: Implementation
Apply fix, run verification:
- `npm run lint`
- `npm run build`
- User verifies in browser

## Constraints
- Prefer holistic fixes over one-off patches
- Fix the pattern, not just the instance
- If fix fails, iterate (max 3 attempts)
