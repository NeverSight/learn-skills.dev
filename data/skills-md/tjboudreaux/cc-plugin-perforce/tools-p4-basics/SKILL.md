---
name: tools-p4-basics
description: Fundamental Perforce operations including sync, edit, add, delete, submit, revert, and file state management.
---

# Perforce Basics

## Overview

Perforce (P4) is a centralized version control system optimized for large codebases and binary assets. This skill covers essential daily operations.

## When to Use

- Syncing latest changes
- Editing files for modification
- Adding new files
- Deleting files
- Submitting changes
- Reverting unwanted changes

## Core Concepts

### File States

| State | Description | Command to Change |
|-------|-------------|-------------------|
| **Not in depot** | File exists locally but not tracked | `p4 add` |
| **Synced** | File matches depot version | - |
| **Edited** | Open for edit, modified locally | `p4 edit` then modify |
| **Added** | Marked for addition to depot | `p4 add` |
| **Deleted** | Marked for deletion from depot | `p4 delete` |
| **Out of date** | Depot has newer version | `p4 sync` |

### Revision Specifiers

```bash
# Specific revision number
file.txt#3

# Head revision (latest)
file.txt#head

# Changelist number
file.txt@12345

# Label
file.txt@release_1.0

# Date/time
file.txt@2024/01/15
file.txt@2024/01/15:14:30:00

# Revision range
file.txt#2,#5
file.txt@10000,@12000
```

## Sync Operations

### Basic Sync

```bash
# Sync entire workspace to head
p4 sync

# Sync specific path
p4 sync //depot/project/...

# Sync specific file
p4 sync //depot/project/file.txt

# Sync to specific revision
p4 sync //depot/project/...#head
p4 sync //depot/project/...@12345

# Sync to specific changelist
p4 sync @12345
```

### Sync Options

```bash
# Preview sync (don't actually sync)
p4 sync -n //depot/project/...

# Force sync (re-download even if up to date)
p4 sync -f //depot/project/...

# Parallel sync (faster for many files)
p4 sync --parallel=threads=4 //depot/project/...

# Safe sync (don't clobber writable files)
p4 sync -s //depot/project/...

# Sync and show affected files
p4 sync //depot/project/... 2>&1 | head -50
```

### Selective Sync

```bash
# Sync only specific file types
p4 sync //depot/project/....cs
p4 sync //depot/project/....prefab

# Sync excluding paths (use workspace view instead)
# Or sync specific subdirectories
p4 sync //depot/project/Assets/Scripts/...
```

## Edit Operations

### Opening Files for Edit

```bash
# Edit single file
p4 edit file.txt

# Edit multiple files
p4 edit *.cs

# Edit files in directory
p4 edit Assets/Scripts/...

# Edit with specific changelist
p4 edit -c 12345 file.txt

# Edit to default changelist
p4 edit -c default file.txt
```

### Check Edit Status

```bash
# See files open for edit
p4 opened

# See files open in specific changelist
p4 opened -c 12345

# See files open by all users
p4 opened -a //depot/project/...

# See who has file open
p4 opened -a //depot/project/file.txt
```

## Add Operations

### Adding New Files

```bash
# Add single file
p4 add newfile.txt

# Add multiple files
p4 add *.cs

# Add files recursively
p4 add Assets/NewFeature/...

# Add to specific changelist
p4 add -c 12345 newfile.txt

# Add with specific file type
p4 add -t binary+l largefile.bin
p4 add -t text+x script.sh
```

### File Types

```bash
# Common file types
text        # Text file, diff/merge enabled
binary      # Binary file, no diff/merge
unicode     # Unicode text
symlink     # Symbolic link

# Modifiers
+l          # Exclusive lock (only one user can edit)
+w          # Always writable on client
+x          # Executable bit
+S          # Only head revision stored (saves space)
+F          # Check for RCS keywords

# Examples
p4 add -t binary+l Assets/Textures/hero.psd    # Locked binary
p4 add -t text Assets/Scripts/Player.cs         # Text file
```

## Delete Operations

### Deleting Files

```bash
# Delete single file
p4 delete file.txt

# Delete multiple files
p4 delete *.bak

# Delete in specific changelist
p4 delete -c 12345 file.txt

# Delete files matching pattern
p4 delete //depot/project/....tmp
```

### Handling Deleted Files

```bash
# See deleted files in depot
p4 files //depot/project/...@head | grep "delete change"

# Recover deleted file (sync old revision, then add)
p4 sync //depot/project/file.txt#head-1
p4 add file.txt

# Or use obliterate (admin only) to permanently remove
```

## Revert Operations

### Reverting Changes

```bash
# Revert single file
p4 revert file.txt

# Revert all files in changelist
p4 revert -c 12345 //...

# Revert all open files
p4 revert //...

# Revert unchanged files only
p4 revert -a //...

# Revert with preview
p4 revert -n //...
```

### Revert to Specific Revision

```bash
# Sync to old revision (makes file read-only)
p4 sync //depot/project/file.txt#3

# To actually revert content and submit:
p4 sync //depot/project/file.txt#head
p4 edit file.txt
p4 sync -f //depot/project/file.txt#3
p4 resolve -ay file.txt
# Now submit
```

## Submit Operations

### Submitting Changes

```bash
# Submit default changelist (opens editor for description)
p4 submit

# Submit specific changelist
p4 submit -c 12345

# Submit with description
p4 submit -d "Fix player movement bug"

# Submit specific files from default changelist
p4 submit file.txt

# Submit and reopen files for further editing
p4 submit -r -c 12345
```

### Pre-Submit Checks

```bash
# Check what will be submitted
p4 opened -c default

# Check for conflicts before submit
p4 sync
p4 resolve

# Verify files are correct
p4 diff -se //...  # Files that differ from depot

# Check changelist description
p4 change -o 12345
```

## Status Commands

### Workspace Status

```bash
# Files open for edit/add/delete
p4 opened

# Files that need sync
p4 sync -n //...

# Files modified but not opened (reconcile needed)
p4 status

# Reconcile local changes with depot
p4 reconcile //...
```

### Depot Status

```bash
# List files in depot
p4 files //depot/project/...

# List files with specific pattern
p4 files //depot/project/....cs

# Get file info
p4 fstat //depot/project/file.txt

# Detailed file info
p4 fstat -Ol //depot/project/file.txt
```

## Reconcile Operations

### Finding Untracked Changes

```bash
# Find all local changes not in Perforce
p4 reconcile //...

# Preview reconcile
p4 reconcile -n //...

# Reconcile specific types
p4 reconcile -e //...  # Edited files
p4 reconcile -a //...  # Added files
p4 reconcile -d //...  # Deleted files

# Reconcile to specific changelist
p4 reconcile -c 12345 //...
```

## Common Workflows

### Daily Sync Workflow

```bash
# 1. Check for open files
p4 opened

# 2. Sync latest
p4 sync

# 3. Resolve any conflicts
p4 resolve

# 4. Continue working
```

### Edit-Submit Workflow

```bash
# 1. Open file for edit
p4 edit file.txt

# 2. Make changes
# ... edit file ...

# 3. Verify changes
p4 diff file.txt

# 4. Submit
p4 submit -d "Description of changes"
```

### Add New Files Workflow

```bash
# 1. Create files locally
# ... create files ...

# 2. Add to Perforce
p4 add newfile.txt

# 3. Verify
p4 opened

# 4. Submit
p4 submit -d "Add new feature files"
```

## Best Practices

1. **Always sync before editing** - Avoid conflicts
2. **Use descriptive changelist descriptions** - Help others understand
3. **Submit related changes together** - Atomic commits
4. **Revert unchanged files** with `p4 revert -a`
5. **Check `p4 opened`** before leaving for the day
6. **Use `p4 reconcile`** to catch local changes
7. **Preview with `-n`** before destructive operations
8. **Use exclusive locks** for binary files
9. **Don't submit broken code** - Test first
10. **Keep changelists small** - Easier to review/revert

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "File not on client" | Run `p4 sync` first |
| "Can't edit - not synced" | Sync file, then edit |
| "Can't clobber writable file" | Use `p4 sync -f` or fix permissions |
| "File already open" | Check `p4 opened -a` for who has it |
| "Out of date" | Sync and resolve before submit |
| "No such file" | Check path, use `p4 files` to verify |
