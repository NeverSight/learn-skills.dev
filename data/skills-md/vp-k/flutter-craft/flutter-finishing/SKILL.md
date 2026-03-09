---
name: flutter-finishing
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of Flutter development work by presenting structured options
---

# Finishing a Flutter Development Branch

## Overview

Guide completion of Flutter development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up

**Announce at start:** "I'm using the flutter-finishing skill to complete this work."

## The Process

### Step 1: Verify Tests and Analysis

**Before presenting options, verify everything passes:**

```bash
# Static analysis
flutter analyze
# Expected: No issues found!

# All tests
flutter test
# Expected: All tests passed!

# Optional: Build check
flutter build apk --debug
# Expected: Built successfully
```

**If tests fail:**
```
Flutter tests failing (N failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

**STOP. Don't proceed to Step 2.**

**If tests pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
# Find merge base
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null

# Or ask: "This branch split from main - is that correct?"
```

### Step 3: Present Options

Present exactly these 4 options:

```
Implementation complete. All tests passing. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 4: Execute Choice

#### Option 1: Merge Locally

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify tests on merged result
flutter analyze
flutter test

# If tests pass, delete feature branch
git branch -d <feature-branch>
```

**Then:** Cleanup worktree (Step 5)

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<feature-title>" --body "$(cat <<'EOF'
## Summary
- Implemented [feature] following Clean Architecture
- Added [Layer] layer components
- [Test coverage details]

## Test Plan
- [ ] flutter analyze passes
- [ ] flutter test passes
- [ ] Manual testing of [scenarios]

## Flutter Version
- Flutter: X.X.X
- Dart: X.X.X

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Don't cleanup worktree** - might need for PR review fixes.

#### Option 3: Keep As-Is

Report: "Keeping branch `<name>`. Worktree preserved at `<path>`."

**Don't cleanup worktree.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch: <name>
- All commits: <commit-list>
- Worktree at: <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

**Then:** Cleanup worktree (Step 5)

### Step 5: Cleanup Worktree

**For Options 1, 2, 4:**

Check if in worktree:
```bash
git worktree list | grep $(git branch --show-current)
```

If yes:
```bash
# Navigate to main repo
cd <main-repo-path>

# Remove worktree
git worktree remove <worktree-path>
```

**For Option 3:** Keep worktree.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | ✓ | - |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (force) |

## Flutter-Specific Verification

Before allowing completion:

```bash
# 1. Analysis must pass
flutter analyze
# Must show: No issues found!

# 2. Tests must pass
flutter test
# Must show: All tests passed!

# 3. (Optional) Build verification
flutter build apk --debug
# Must show: Built build/app/outputs/...
```

## Common Mistakes

**Skipping test verification**
- Problem: Merge broken code, create failing PR
- Fix: Always verify tests before offering options

**Open-ended questions**
- Problem: "What should I do next?" → ambiguous
- Fix: Present exactly 4 structured options

**Automatic worktree cleanup**
- Problem: Remove worktree when might need it (Option 2, 3)
- Fix: Only cleanup for Options 1 and 4

**No confirmation for discard**
- Problem: Accidentally delete work
- Fix: Require typed "discard" confirmation

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request
- Skip flutter analyze

**Always:**
- Verify tests before offering options
- Present exactly 4 options
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only

## Integration

**Called by:**
- **flutter-subagent-dev** (after all tasks complete)
- **flutter-executing** (after all batches complete)

**Pairs with:**
- **flutter-worktrees** - Cleans up worktree created by that skill
