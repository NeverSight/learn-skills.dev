---
name: flutter-worktrees
description: Use when starting feature work that needs isolation from current workspace - creates isolated git worktrees with Flutter project setup
---

# Using Git Worktrees for Flutter Development

## Overview

Git worktrees let you work on multiple branches simultaneously in separate directories. Each worktree is fully independent - you can run different Flutter versions, have different dependencies, without affecting your main workspace.

**Core principle:** Isolated workspace = safe experimentation + parallel development

**Announce at start:** "I'm using the flutter-worktrees skill to create an isolated workspace."

## When to Use

- Starting a new feature that needs isolation
- Working on experimental changes
- Need to compare implementations side-by-side
- Want to keep main workspace clean
- Running long-running tests in background

## The Process

### Step 1: Create Worktree

```bash
# From main repository
git worktree add ../flutter-app-feature-auth feature/auth

# Or create new branch
git worktree add -b feature/auth ../flutter-app-feature-auth main
```

**Naming convention:** `../[project-name]-[feature-name]`

### Step 2: Navigate to Worktree

```bash
cd ../flutter-app-feature-auth
```

### Step 3: Flutter Setup (Critical for Flutter Projects!)

```bash
# Install dependencies
flutter pub get

# Verify Flutter is working
flutter doctor

# If needed, run code generation
flutter pub run build_runner build --delete-conflicting-outputs
```

### Step 4: Verify Setup

```bash
# Check project state
flutter analyze
flutter test

# Should show no issues if setup is correct
```

### Step 5: Work on Feature

Follow normal development workflow:
- flutter-brainstorming
- flutter-planning
- flutter-executing

All changes stay isolated in this worktree.

### Step 6: Cleanup (After Merge/Discard)

```bash
# From main repository
cd ../flutter-app  # Back to main

# Remove worktree
git worktree remove ../flutter-app-feature-auth

# If branch was merged, it's already in main
# If discarded, the branch still exists and can be deleted:
git branch -D feature/auth
```

## Worktree Directory Structure

```
parent-directory/
├── flutter-app/                  # Main repository
│   ├── lib/
│   ├── test/
│   ├── pubspec.yaml
│   └── .git/                     # Main git directory
├── flutter-app-feature-auth/     # Worktree 1
│   ├── lib/
│   ├── test/
│   ├── pubspec.yaml
│   └── .git                      # File pointing to main .git
└── flutter-app-feature-profile/  # Worktree 2
    ├── lib/
    ├── test/
    ├── pubspec.yaml
    └── .git
```

## Flutter-Specific Considerations

### Dependencies

Each worktree has its own:
- `.dart_tool/` directory
- `pubspec.lock` (can differ if experimenting with versions)
- Build cache

**Always run `flutter pub get` after creating worktree!**

### Code Generation

If project uses code generation (freezed, json_serializable, etc.):

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

### IDE Setup

**VS Code:** Open worktree folder as new workspace
**Android Studio:** Open worktree folder as new project

### Platform-Specific Builds

Each worktree can have different:
- iOS simulator running
- Android emulator connected
- Web server running

No conflicts between worktrees!

## Example Workflow

```bash
# 1. Create isolated workspace for auth feature
git worktree add -b feature/auth ../flutter-app-auth main

# 2. Navigate and setup
cd ../flutter-app-auth
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs

# 3. Verify
flutter analyze
flutter test

# 4. Work on feature (using flutter-craft skills)
# ... implement auth feature ...

# 5. When done, back to main
cd ../flutter-app

# 6. Merge if ready
git merge feature/auth

# 7. Cleanup
git worktree remove ../flutter-app-auth
```

## Red Flags

**Never:**
- Forget `flutter pub get` in new worktree
- Edit main repository while expecting changes in worktree
- Delete worktree directory manually (use `git worktree remove`)
- Have same file open in IDE from both main and worktree

**If worktree has issues:**
```bash
# List all worktrees
git worktree list

# Prune stale worktree references
git worktree prune
```

## Integration with Other Skills

**After creating worktree:**
- Use **flutter-brainstorming** to design feature
- Use **flutter-planning** to create implementation plan
- Use **flutter-executing** or **flutter-subagent-dev** to implement

**After feature complete:**
- Use **flutter-finishing** to decide merge/PR/keep/discard
- Cleanup worktree after merge

## Quick Reference

| Command | Purpose |
|---------|---------|
| `git worktree add <path> <branch>` | Create worktree |
| `git worktree add -b <new-branch> <path> <base>` | Create with new branch |
| `git worktree list` | List all worktrees |
| `git worktree remove <path>` | Remove worktree |
| `git worktree prune` | Clean stale references |
| `flutter pub get` | **Required after creating!** |
