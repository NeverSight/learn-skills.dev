---
name: cleanup-progress
description: Use when a feature is complete and PROGRESS.md needs cleaning up by replacing verbose execution notes with a concise completion summary
---

# Cleanup Feature Progress

Clean up PROGRESS.md for a completed feature, leaving only essential completion information.

## Purpose

After a feature is fully complete, validated, and reviewed, consolidate all the detailed progress notes into a concise completion summary. This keeps PROGRESS.md maintainable while preserving critical information for future reference.

## Step 1: Read PROGRESS.md

**MANDATORY FIRST STEP:**

1. Read `PROGRESS.md`
2. Identify the feature section to clean up (usually the most recent one)
3. Extract key information:
   - What was the feature about
   - What tests passed
   - What manual tests weren't performed or didn't pass
   - How the core functionality was validated

## Step 2: Create Concise Completion Summary

Replace the entire feature section with a clean, concise summary:

```markdown
## Feature: [Feature Name]

**Status**: ✅ Complete
**Completed**: [Date]
**Plan**: .agents/plans/[feature-name].md

### Core Validation
[1-2 sentence summary of how the core functionality was validated to be working correctly]

### Test Status
- Automated Tests: ✅ All passing ([X] unit, [Y] integration, [Z] e2e)
- Manual Tests: [Status]
  - ⚠️ Not performed: [list manual tests not done]
  - ❌ Failed: [list any failed manual tests]
  - ✅ Passed: [list passed manual tests if any were done]

### Notes
[Any important notes, gotchas, or follow-up items - keep brief]

---
```

## Step 3: Archive Detailed Information (Optional)

**If the detailed progress notes contain valuable information:**

1. Create `.agents/progress-archive/[feature-name]-progress.md`
2. Move the full detailed section there
3. Add reference in PROGRESS.md summary:
   ```markdown
   **Detailed Progress**: See .agents/progress-archive/[feature-name]-progress.md
   ```

**Only do this if the detailed notes are worth preserving for future reference.**

## Step 4: Update PROGRESS.md

Use Edit tool to replace the verbose feature section with the concise summary.

**Result:**
- PROGRESS.md is clean and scannable
- Essential completion info is preserved
- Future agents can quickly see what was done and what's left
- Detailed notes archived if valuable

## Guidelines

**Keep in summary:**
- ✅ Feature name and completion status
- ✅ Core validation approach (how it was verified to work)
- ✅ Test status (what passed, what didn't, what wasn't done)
- ✅ Critical notes or gotchas

**Remove from summary:**
- ❌ Detailed execution logs
- ❌ Step-by-step task descriptions
- ❌ Full execution reports
- ❌ Full system reviews
- ❌ Verbose divergence analysis

**Archive if valuable:**
- Detailed execution report with divergences
- System review findings
- Complex troubleshooting notes
- Important architectural decisions

## Example Before/After

### Before (Verbose)
```markdown
## Feature: Add User Authentication

### Planning Phase
**Status**: Complete
**Started**: 2024-01-15 10:00
**Plan File**: .agents/plans/add-user-auth.md

Planning in progress...

### Execution Phase
**Status**: Complete
**Started**: 2024-01-15 11:00
**Completed**: 2024-01-15 14:00

#### What Was Accomplished
[50 lines of detailed task descriptions...]

#### What's Left to Do
[10 lines of future work...]

#### Manual Tests Required
[20 lines of test procedures...]

#### Automated Tests Status
[30 lines of test results...]

### Execution Report
[100 lines of detailed analysis...]

### System Review
[150 lines of process analysis...]
```

### After (Concise)
```markdown
## Feature: Add User Authentication

**Status**: ✅ Complete
**Completed**: 2024-01-15
**Plan**: .agents/plans/add-user-auth.md

### Core Validation
Authentication flow validated through comprehensive automated tests covering registration, login, logout, and session management. Manual testing confirmed UI flows work correctly.

### Test Status
- Automated Tests: ✅ All passing (15 unit, 8 integration, 5 e2e)
- Manual Tests:
  - ✅ Passed: UI registration flow, UI login flow
  - ⚠️ Not performed: Password reset email (requires production email service)

### Notes
- JWT tokens expire after 24 hours
- Refresh token rotation implemented
- Rate limiting: 5 login attempts per 15 minutes

**Detailed Progress**: See .agents/progress-archive/add-user-auth-progress.md

---
```

## Output

After cleanup, confirm to CLI:

```
✅ PROGRESS.md cleaned up for feature: [Feature Name]

Summary:
- Verbose progress notes: [REMOVED / ARCHIVED to .agents/progress-archive/]
- Concise completion summary: ✅ Added
- Essential info preserved: ✅ Test status, validation approach, notes

PROGRESS.md is now clean and ready for the next feature.
```
