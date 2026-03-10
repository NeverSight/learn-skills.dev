---
name: flutter-executing
description: Use when you have a written implementation plan to execute with review checkpoints
---

# Executing Flutter Implementation Plans

## Overview

Load plan, review critically, execute tasks in batches, run Flutter verifications, report for review between batches.

**Core principle:** Batch execution with checkpoints for review.

**Announce at start:** "I'm using the flutter-executing skill to implement this plan."

## The Process

### Step 1: Load and Review Plan

1. **Read plan file**
   ```bash
   cat docs/plans/YYYY-MM-DD-<feature>-plan.md
   ```

2. **Check dependencies first**
   ```bash
   cat pubspec.yaml
   ```

3. **Install new dependencies if needed**
   ```bash
   flutter pub get
   ```

4. **Review critically:**
   - Are file paths correct?
   - Is layer order followed (Domain → Data → Presentation)?
   - Are there any gaps in the plan?

5. **If concerns:** Raise them before starting
6. **If no concerns:** Create TodoWrite and proceed

### Step 2: Execute Batch

**Default: First 3 tasks**

For each task:
1. Mark as in_progress in TodoWrite
2. Create/modify files as specified
3. Write complete code (from plan)
4. Run verification:
   ```bash
   flutter analyze lib/features/<feature>/
   ```
5. Commit:
   ```bash
   git add <files>
   git commit -m "<conventional commit message>"
   ```
6. Mark as completed in TodoWrite

### Step 3: Verify Batch

After completing 3 tasks, run full verification:

```bash
# Static analysis
flutter analyze
# Expected: No issues found!

# Run tests (if test files exist)
flutter test test/features/<feature>/
# Expected: All tests passed!

# Quick build check (optional)
flutter build apk --debug --target-platform android-arm64
# Expected: Built successfully
```

### Step 4: Report

When batch complete, report:

```markdown
## Batch N Complete

**Tasks completed:**
1. ✅ Task 1: [description]
2. ✅ Task 2: [description]
3. ✅ Task 3: [description]

**Verification:**
- flutter analyze: No issues found
- flutter test: X/X passed

**Files created/modified:**
- lib/features/.../entity.dart
- lib/features/.../repository.dart
- ...

**Ready for feedback.**
```

### Step 5: Continue

Based on feedback:
- Apply changes if needed
- Execute next batch of 3 tasks
- Repeat until all tasks complete

### Step 6: Complete Development

After all tasks complete and verified:

1. **Run final verification:**
   ```bash
   flutter analyze
   flutter test
   flutter build apk --debug  # or ios
   ```

2. **Announce:** "I'm using the flutter-finishing skill to complete this work."

3. **REQUIRED SUB-SKILL:** Use `flutter-craft:flutter-finishing`
   - Verify tests
   - Present 4 options (merge/PR/keep/discard)
   - Execute choice
   - Cleanup worktree if applicable

## Flutter-Specific Verification Commands

| Stage | Command | Expected Output |
|-------|---------|-----------------|
| Per-file | `flutter analyze lib/path/file.dart` | No issues found |
| Per-batch | `flutter analyze lib/features/<feature>/` | No issues found |
| Test | `flutter test test/features/<feature>/` | All tests passed |
| Final | `flutter build apk --debug` | Built successfully |

## When to Stop and Ask for Help

**STOP executing immediately when:**
- `flutter analyze` shows errors (not just warnings)
- Tests fail with unclear cause
- Missing dependency not in pubspec.yaml
- Plan has unclear instructions
- File path in plan doesn't match project structure
- State management pattern unclear

**Ask for clarification rather than guessing.**

## Layer Order Verification

**Before executing, verify plan follows this order:**

```
1. Domain Layer tasks first
   ├── Entities
   ├── Repository interfaces
   └── UseCases

2. Data Layer tasks second
   ├── Models
   ├── DataSources
   └── Repository implementations

3. Presentation Layer tasks third
   ├── State Management
   ├── Widgets
   └── Screens

4. Test tasks after implementation
   ├── Repository tests (priority 1)
   ├── State tests (priority 2)
   └── Widget tests (priority 3)
```

**If plan doesn't follow this order, raise concern before starting.**

## REQUIRED SUB-SKILL

### During Execution
After EACH batch, you MUST invoke:
→ **flutter-craft:flutter-verification** (verify before continuing)

### After All Tasks Complete
You MUST invoke:
→ **flutter-craft:flutter-finishing** (present completion options)

## Remember

- **Review plan critically first** - Don't blindly execute
- **Follow layer order** - Domain → Data → Presentation
- **Run flutter analyze per batch** - Catch errors early
- **Commit after each task** - Atomic commits
- **Report and wait** - Don't continue without feedback
- **Stop when blocked** - Don't guess, ask
