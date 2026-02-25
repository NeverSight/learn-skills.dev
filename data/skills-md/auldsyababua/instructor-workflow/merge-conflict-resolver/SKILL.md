---
name: merge-conflict-resolver
description: Analyze branch divergence, detect potential conflicts, and guide merge resolution for any Git repository. Auto-detects current branch or accepts parameters.
tags:
  - git
  - merge
  - conflict-resolution
  - devops
version: 1.0.0
author: DevOps Agent (Clay)
---

# Merge Conflict Resolver Skill

## Overview

A comprehensive skill for analyzing Git branch divergence, detecting potential merge conflicts before they occur, and guiding users through systematic conflict resolution. This skill provides both automated analysis and manual resolution workflows.

## Features

### 1. Intelligent Auto-Detection
- Detects current branch automatically if not specified
- Auto-discovers repository root using `git rev-parse --show-toplevel`
- Defaults to `origin/main` as target branch (configurable)
- Works in any Git repository without hardcoded paths

### 2. 8-Step Analysis Workflow
1. **Branch Verification** - Validates current branch state
2. **Status Display** - Shows recent commits and current HEAD
3. **Fetch Latest** - Updates remote branch information
4. **Commit Comparison** - Analyzes branch divergence (merge-base analysis)
5. **Change Analysis** - Shows commits unique to each branch
6. **File Changes** - Lists modified files in both branches
7. **Conflict Detection** - Identifies files changed in both branches (potential conflicts)
8. **Merge Attempt** - Attempts automatic merge with detailed reporting

### 3. Color-Coded Output
- **RED** - Errors and conflict detection
- **GREEN** - Success messages and confirmations
- **YELLOW** - Warnings and important information
- **BLUE** - Section headers and step markers

### 4. Multiple Resolution Strategies
- **Automated** - `resolve-merge-conflicts.sh` (orchestrator)
- **Detailed Analysis** - `analyze-and-merge.sh` (8-step workflow with guidance)
- **Simple Merge** - `simple-merge.sh` (basic merge helper)
- **Status Check** - `check-merge-status.sh` (non-destructive analysis)

## Usage

### Quick Start (Recommended)

```bash
# Auto-detect current branch, merge from origin/main
cd /path/to/your/repo
/path/to/skills/merge-conflict-resolver/scripts/resolve-merge-conflicts.sh

# Specify branches explicitly
./scripts/resolve-merge-conflicts.sh feature/my-branch origin/main

# Or just specify source branch
./scripts/resolve-merge-conflicts.sh feature/my-branch
```

### Detailed Analysis

```bash
# Run comprehensive 8-step analysis before merging
./scripts/analyze-and-merge.sh feature/my-branch origin/main

# Auto-detect branches
./scripts/analyze-and-merge.sh
```

### Status Check Only

```bash
# Check current state without making any changes
./scripts/check-merge-status.sh
```

### Simple Merge Helper

```bash
# Basic merge workflow (less verbose)
./scripts/simple-merge.sh feature/my-branch origin/main
```

## When to Use This Skill

### Perfect For:
- ✅ Resolving merge conflicts in feature branches
- ✅ Pre-merge analysis to detect potential conflicts
- ✅ Understanding branch divergence before creating PRs
- ✅ Teaching merge conflict resolution workflows
- ✅ Automated merge workflows in CI/CD pipelines
- ✅ Multi-developer teams with frequent branch conflicts

### Not Suitable For:
- ❌ Automated conflict resolution (requires human judgment)
- ❌ Rebasing workflows (use `git rebase` instead)
- ❌ Interactive conflict resolution (use `git mergetool`)
- ❌ Cherry-picking specific commits (use `git cherry-pick`)

## Output Examples

### Success Case (No Conflicts)

```
==================================================================
✓ SUCCESS: Merge completed without conflicts!
==================================================================

New HEAD:
abc1234 Merge origin/main into feature/my-branch
def5678 Latest feature commit
...

Next steps:
1. Review the merge: git log --oneline -10
2. Push to remote: git push origin feature/my-branch
```

### Conflict Case (Manual Resolution Needed)

```
=================================================
✗ MERGE CONFLICTS DETECTED
=================================================

Conflicting files:
UU src/main.py
UU config/settings.json

⚠ Files changed in both branches:
src/main.py
config/settings.json

Resolution steps:
1. Review conflicts in the files listed above
2. Edit each file to resolve conflicts (look for <<<<<<< markers)
3. git add <resolved-file>
4. Repeat for all files
5. git merge --continue

Or to abort:
git merge --abort
```

### Pre-Merge Analysis

```
[Step 7] Checking for potential conflicts...
✓ No overlapping file changes detected
Merge should be clean!

Files changed in our branch:
  src/feature.py
  tests/test_feature.py

Files changed in origin/main:
  src/unrelated.py
  docs/README.md
```

## Configuration

### Environment Variables

```bash
# Override default target branch
export DEFAULT_TARGET_BRANCH="origin/develop"

# Disable color output (for CI/CD logs)
export NO_COLOR=1

# Auto-abort on conflicts (for automation)
export AUTO_ABORT_ON_CONFLICT=1
```

### Script Parameters

All scripts accept optional parameters:

```bash
./scripts/resolve-merge-conflicts.sh [source-branch] [target-branch]
```

**Parameter Defaults**:
- `source-branch`: `$(git branch --show-current)` (current branch)
- `target-branch`: `origin/main` (or `$DEFAULT_TARGET_BRANCH`)

## Error Handling

### Common Errors

**Not in a Git repository**:
```
ERROR: Not in a Git repository
Run this script from inside a Git repository
```

**Branch doesn't exist**:
```
ERROR: Branch 'feature/nonexistent' not found
Available branches: git branch -a
```

**Already up to date**:
```
✓ Already up to date with origin/main
No merge needed.
```

**Dirty working directory**:
```
ERROR: Working directory has uncommitted changes
Commit or stash changes before merging:
  git stash
  git commit -am "Save work"
```

## Rollback and Recovery

### Abort Merge in Progress

```bash
# Cancel merge and return to pre-merge state
git merge --abort
```

### Reset to Before Merge

```bash
# Reset to previous state (ORIG_HEAD)
git reset --hard ORIG_HEAD

# Or reset to remote branch
git reset --hard origin/feature/my-branch
```

### Preserve Work Before Resetting

```bash
# Save current work
git stash

# Reset to clean state
git reset --hard origin/feature/my-branch

# Restore work
git stash pop
```

## Integration Examples

### CI/CD Pipeline (GitHub Actions)

```yaml
name: Check Merge Conflicts

on:
  pull_request:
    branches: [main]

jobs:
  check-merge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for merge-base

      - name: Check for conflicts
        run: |
          ./skills/merge-conflict-resolver/scripts/check-merge-status.sh

      - name: Analyze merge
        run: |
          export NO_COLOR=1  # Disable colors in CI logs
          ./skills/merge-conflict-resolver/scripts/analyze-and-merge.sh
        continue-on-error: true  # Allow conflicts
```

### Pre-Merge Hook

```bash
#!/bin/bash
# .git/hooks/pre-merge-commit

# Run conflict analysis before allowing merge
/path/to/skills/merge-conflict-resolver/scripts/check-merge-status.sh

if [ $? -ne 0 ]; then
  echo "Merge conflict detected. Resolve before committing."
  exit 1
fi
```

### Automated Merge Script

```bash
#!/bin/bash
# automated-merge.sh

set -euo pipefail

FEATURE_BRANCH="$1"
TARGET_BRANCH="${2:-origin/main}"

# Check for conflicts first
if ! ./skills/merge-conflict-resolver/scripts/analyze-and-merge.sh "$FEATURE_BRANCH" "$TARGET_BRANCH"; then
  echo "Automatic merge failed - manual intervention required"
  exit 1
fi

# Push if successful
git push origin "$FEATURE_BRANCH"
```

## Troubleshooting

### Merge Failed with Many Conflicts

Try rebase instead:

```bash
git merge --abort
git rebase origin/main

# Resolve conflicts one commit at a time
git add <resolved-file>
git rebase --continue
```

### Lost Changes After Merge

```bash
# Check reflog for lost commits
git reflog

# Restore from reflog
git reset --hard HEAD@{N}  # Replace N with appropriate index
```

### Scripts Not Executable

```bash
# Make scripts executable
chmod +x skills/merge-conflict-resolver/scripts/*.sh
```

## Best Practices

### Before Merging

1. ✅ **Always fetch first**: `git fetch origin`
2. ✅ **Check branch status**: Run `check-merge-status.sh`
3. ✅ **Analyze potential conflicts**: Run `analyze-and-merge.sh` first
4. ✅ **Commit or stash changes**: Clean working directory before merge
5. ✅ **Review recent commits**: Understand what you're merging

### During Conflict Resolution

1. ✅ **Read conflict markers carefully**: `<<<<<<<`, `=======`, `>>>>>>>`
2. ✅ **Test after each resolution**: Don't resolve all at once
3. ✅ **Keep both changes when possible**: Merge functionality, don't just delete
4. ✅ **Preserve security fixes**: Don't accidentally revert critical changes
5. ✅ **Document complex resolutions**: Add comments explaining why

### After Merging

1. ✅ **Review the merge commit**: `git show HEAD`
2. ✅ **Run tests**: Ensure nothing broke
3. ✅ **Check for unintended changes**: `git diff HEAD~1`
4. ✅ **Update documentation**: Note conflicts resolved
5. ✅ **Push promptly**: Don't leave resolved merges unpushed

## File Structure

```
skills/merge-conflict-resolver/
├── SKILL.md                          # This file
├── README.md                         # Usage guide
└── scripts/
    ├── resolve-merge-conflicts.sh    # Main orchestrator
    ├── analyze-and-merge.sh          # Detailed 8-step analysis
    ├── simple-merge.sh               # Basic merge helper
    └── check-merge-status.sh         # Status checker
```

## Contributing

### Adding Features

1. Keep auto-detection logic in all scripts
2. Maintain color-coded output conventions
3. Provide clear error messages with actionable steps
4. Test with multiple Git repository types
5. Update both SKILL.md and README.md

### Testing

```bash
# Test in various scenarios
cd /tmp
git init test-repo
cd test-repo
git remote add origin <test-repo-url>

# Test auto-detection
/path/to/scripts/check-merge-status.sh

# Test with parameters
/path/to/scripts/analyze-and-merge.sh feature/test origin/main
```

## Version History

- **v1.0.0** (2025-11-17) - Initial release
  - 8-step analysis workflow
  - Auto-detection of branches and repository
  - Color-coded output
  - Multiple resolution strategies
  - Comprehensive error handling

## License

MIT License - Use freely in any Git workflow

## Support

For issues or questions:
1. Check this documentation first
2. Review example outputs in README.md
3. Examine script comments for implementation details
4. Test in a safe repository before production use

---

**Remember**: Merge conflict resolution requires human judgment. These scripts analyze and guide, but you make the final decisions about which changes to keep.
