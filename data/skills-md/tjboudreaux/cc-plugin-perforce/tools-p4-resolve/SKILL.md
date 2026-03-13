---
name: tools-p4-resolve
description: Perforce conflict resolution including merge strategies, 3-way merge, resolve workflows, and handling binary conflicts.
---

# Perforce Conflict Resolution

## Overview

Conflicts occur when multiple users modify the same file. Perforce provides powerful resolve tools for merging changes. This skill covers all resolve strategies and workflows.

## When to Use

- After syncing when files have conflicts
- Before submitting changes
- When integrating between branches
- Handling binary file conflicts
- Resolving content vs attribute conflicts

## Core Concepts

### Conflict Types

| Type | Description | Resolution |
|------|-------------|------------|
| **Content** | Both versions modified same lines | Merge or choose version |
| **Attribute** | File type or permissions changed | Choose attribute |
| **Delete** | File deleted in one version, modified in other | Keep or delete |
| **Move/Delete** | File moved and deleted | Choose action |
| **Binary** | Binary file modified by both | Choose version (no merge) |

### Three-Way Merge

```
Base (common ancestor)
    |
    +-- Theirs (depot/source)
    |
    +-- Yours (workspace)
    |
    v
Merged Result
```

## Basic Resolve

### Check for Conflicts

```bash
# Preview resolve (see what needs resolving)
p4 resolve -n

# See files that need resolving
p4 resolve -n //depot/project/...

# Check specific file
p4 resolve -n file.txt
```

### Automatic Resolve

```bash
# Auto-resolve all (safe merge where possible)
p4 resolve -am

# Auto-resolve accepting merge result
p4 resolve -am //depot/project/...

# Auto-resolve specific file
p4 resolve -am file.txt
```

### Resolve Strategies

```bash
# Accept automatic merge (only if no conflicts)
p4 resolve -am

# Accept theirs (depot version)
p4 resolve -at

# Accept yours (workspace version)
p4 resolve -ay

# Force accept theirs even with conflicts
p4 resolve -at //...

# Force accept yours even with conflicts
p4 resolve -ay //...
```

## Interactive Resolve

### Launch Interactive Resolve

```bash
# Interactive resolve for all files
p4 resolve

# Interactive resolve for specific file
p4 resolve file.txt

# Interactive with specific merge tool
p4 resolve -t p4merge file.txt
```

### Interactive Menu Options

```
Diff results:
  1: Accept theirs (loses your changes)
  2: Accept yours (loses depot changes)
  3: Accept merge result
  4: Edit merge result
  5: Show differences (base to theirs)
  6: Show differences (base to yours)
  7: Show differences (yours to theirs)
  8: Skip this file
  9: Help

Choose option:
```

### Interactive Workflow

```bash
# 1. Start resolve
p4 resolve file.txt

# 2. View differences
# Option 5, 6, or 7 to understand changes

# 3. Choose resolution
# Option 1 (theirs), 2 (yours), or 3 (merge)

# 4. If merge has conflicts, option 4 to edit

# 5. Accept final result
# Option 3 to accept merge
```

## Merge Tools

### Configure P4 Merge Tool

```bash
# Set P4MERGE environment variable
export P4MERGE=/usr/local/bin/p4merge

# Or use other merge tools
export P4MERGE=/usr/local/bin/code  # VS Code
export P4MERGE=/usr/local/bin/meld  # Meld
export P4MERGE=/usr/bin/vimdiff     # Vim
```

### P4Merge Workflow

```bash
# Launch P4Merge for conflict
p4 resolve -t file.txt

# P4Merge shows four panes:
# - Base (original)
# - Theirs (depot)
# - Yours (local)
# - Result (merged)

# Edit result pane, save, close
# Accept result in terminal
```

### Visual Studio Code Merge

```bash
# Set VS Code as merge tool
export P4MERGE="code --wait --merge"

# Resolve using VS Code
p4 resolve file.txt
```

## Resolve Scenarios

### Simple Auto-Merge

```bash
# Both changed different parts of file
p4 sync
# File needs resolve...
p4 resolve -am
# Merge successful - changes combined
```

### Conflicting Changes

```bash
# Both changed same lines
p4 sync
p4 resolve -am
# Conflicts detected...

# Option 1: Accept theirs
p4 resolve -at file.txt

# Option 2: Accept yours
p4 resolve -ay file.txt

# Option 3: Manual merge
p4 resolve file.txt
# Choose option 4 to edit
# Fix conflicts in editor
# Save and accept
```

### Binary File Conflicts

```bash
# Binary files can't be merged
p4 sync
p4 resolve -n
# Binary conflict on image.psd

# Accept theirs (depot version)
p4 resolve -at image.psd

# Or accept yours (your version)
p4 resolve -ay image.psd
```

### Delete vs Edit Conflict

```bash
# File deleted in depot, edited locally
p4 sync
p4 resolve -n
# Delete vs edit conflict...

# Keep your edited version
p4 resolve -ay file.txt

# Or accept delete
p4 resolve -at file.txt
```

## Advanced Resolve

### Partial Resolve

```bash
# Resolve only content, not attributes
p4 resolve -c //...

# Resolve only attributes
p4 resolve -A //...

# Resolve specific attribute type
p4 resolve -Aa //...  # All attributes
p4 resolve -Ab //...  # Branch action
p4 resolve -At //...  # File type
```

### Re-Resolve

```bash
# Re-resolve already resolved file
p4 resolve -f file.txt

# Re-resolve with different strategy
p4 resolve -f -at file.txt
```

### Resolve During Integration

```bash
# Integrate between branches
p4 integrate //depot/dev/... //depot/main/...

# Resolve integration conflicts
p4 resolve -am //depot/main/...

# If conflicts remain
p4 resolve //depot/main/...
```

### Safe Resolve Workflow

```bash
# 1. Preview what needs resolving
p4 resolve -n

# 2. Try automatic merge first
p4 resolve -am

# 3. Check what remains
p4 resolve -n

# 4. Handle remaining manually
p4 resolve remaining_file.txt

# 5. Verify resolve complete
p4 resolve -n  # Should show nothing
```

## Conflict Markers

### Understanding Markers

When editing merge result manually:

```
<<<<<<< THEIRS (depot version)
code from depot
=======
code from your workspace
>>>>>>> YOURS (workspace version)
```

### Resolving Markers

```bash
# Edit file to remove markers
vim file.txt

# Original with markers:
<<<<<<< THEIRS
function getValue() {
    return this.value;
}
=======
function getValue() {
    return this.cachedValue || this.value;
}
>>>>>>> YOURS

# Resolved (choose best version or combine):
function getValue() {
    return this.cachedValue || this.value;
}

# Save and mark resolved
p4 resolve -am file.txt
```

## Resolve Workflows

### Pre-Submit Workflow

```bash
#!/bin/bash
# pre-submit-resolve.sh

# Sync latest
p4 sync

# Check for conflicts
CONFLICTS=$(p4 resolve -n 2>&1 | grep -c "resolve")

if [ "$CONFLICTS" -gt 0 ]; then
    echo "Found $CONFLICTS files needing resolve"
    
    # Try auto-merge
    p4 resolve -am
    
    # Check remaining
    REMAINING=$(p4 resolve -n 2>&1 | grep -c "resolve")
    
    if [ "$REMAINING" -gt 0 ]; then
        echo "Manual resolve needed for $REMAINING files"
        p4 resolve -n
        exit 1
    fi
fi

echo "Ready to submit"
```

### Integration Workflow

```bash
# 1. Integrate from source to target
p4 integrate //depot/feature/... //depot/main/...

# 2. Preview conflicts
p4 resolve -n //depot/main/...

# 3. Auto-resolve safe merges
p4 resolve -am //depot/main/...

# 4. Handle remaining conflicts
p4 resolve //depot/main/...

# 5. Test merged code

# 6. Submit integration
p4 submit -d "Integrate feature to main"
```

### Batch Resolve Pattern

```bash
# Accept all theirs (when their changes are correct)
p4 resolve -at //depot/project/...

# Accept all yours (when your changes are correct)
p4 resolve -ay //depot/project/...

# Mixed resolution
p4 resolve -at //depot/project/Assets/...  # Accept art assets
p4 resolve -am //depot/project/Scripts/... # Merge code
```

## Undoing Resolve

### Revert and Re-Sync

```bash
# If resolve went wrong, revert and start over
p4 revert file.txt
p4 sync file.txt
p4 edit file.txt
# Re-apply your changes manually
```

### Back Out Bad Merge

```bash
# After bad submit, can sync to previous and re-submit
p4 sync //depot/project/file.txt#head-1
p4 edit file.txt
p4 sync -f //depot/project/file.txt#head-1
p4 resolve -ay file.txt
p4 submit -d "Revert bad merge"
```

## Best Practices

1. **Sync frequently** - Smaller merges are easier
2. **Resolve before submit** - Never submit unresolved
3. **Preview first** with `p4 resolve -n`
4. **Try auto-merge** before manual
5. **Use visual merge tool** for complex conflicts
6. **Test after resolve** - Merged code may have bugs
7. **Keep changelists small** - Easier to resolve
8. **Communicate with team** about conflicting areas
9. **Use exclusive locks** for binary files
10. **Document conflict resolution** in submit description

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Must resolve before submit" | Run `p4 resolve` |
| "No file(s) to resolve" | Already resolved or no conflicts |
| Merge tool not launching | Check P4MERGE setting |
| Markers left in file | Edit to remove, re-resolve |
| Wrong resolution accepted | Revert, sync, re-resolve |
| Binary conflict | Must accept one version (-at or -ay) |
