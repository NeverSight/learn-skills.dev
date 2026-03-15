---
name: implement-quick-fix
description: Atomic code changes for small fixes (≤30 lines, ≤5 files). Use for bug fixes, minor tweaks, and small improvements.
---

# Implement Quick Fix

Atomic code changes for small-scope fixes.

## When to Use
- Bug fixes
- Minor tweaks (≤30 lines, ≤5 files)
- Small improvements with clear scope

## Scope Gate
If scope exceeds ≤30 lines or ≤5 files, **STOP** and escalate to `plan/feature`.

## High Risk Gate
If touching `/config/`, `/security/`, or `/.github/`, **STOP** and notify user.

## Artifacts
- `task.md` updated via `task_boundary`

## Approach

### Phase 1: Scope Confirmation
Confirm:
- Estimated lines of change
- Files affected
- No high-risk paths

### Phase 2: Analysis
- Review holistic design principles
- Check for pattern consistency
- Identify regression risks

### Phase 3: Execution
1. Make the change
2. Run `npm run lint`
3. Run `npm run build`
4. If errors, fix (max 3 attempts)

### Phase 4: User Verification
**STOP** and present changes. Ask user to verify in browser.

## Constraints
- Do NOT use browser for testing — user will test manually
- If scope larger than expected, notify user immediately
- No hardcoded secrets or unauthorized network calls
