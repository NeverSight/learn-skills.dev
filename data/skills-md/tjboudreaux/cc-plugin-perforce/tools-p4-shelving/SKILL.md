---
name: tools-p4-shelving
description: Perforce shelving for code review, sharing work-in-progress, backup, and collaboration workflows.
---

# Perforce Shelving

## Overview

Shelving stores pending changes on the Perforce server without submitting them. This enables code review, work-in-progress backup, sharing between workspaces, and collaboration.

## When to Use

- Backing up work-in-progress
- Sharing changes for code review
- Switching between tasks
- Transferring work between workspaces
- Parking changes temporarily
- Pre-submit review (Swarm)

## Core Concepts

### Shelving vs Submitting

| Feature | Shelving | Submitting |
|---------|----------|------------|
| Stored on server | Yes | Yes |
| Creates revision | No | Yes |
| Visible to others | Yes (optional) | Yes |
| Reversible | Easy delete | Need revert |
| Affects depot | No | Yes |
| Builds triggered | Usually no | Usually yes |

## Basic Shelving

### Shelve Changes

```bash
# Shelve all files in changelist
p4 shelve -c 12345

# Shelve specific files
p4 shelve -c 12345 file1.txt file2.txt

# Shelve and keep files open
p4 shelve -c 12345

# Shelve default changelist
p4 shelve

# Replace existing shelf
p4 shelve -f -c 12345

# Shelve with delete of local files (submit-like)
p4 shelve -c 12345
p4 revert -c 12345 //...
```

### View Shelved Changes

```bash
# List shelved changelists
p4 changes -s shelved

# List your shelved changelists
p4 changes -s shelved -u $P4USER

# Describe shelved changelist
p4 describe -S 12345

# List files in shelf
p4 describe -S -s 12345

# Diff shelved file vs depot
p4 diff2 //depot/file.txt //depot/file.txt@=12345
```

### Unshelve Changes

```bash
# Unshelve to same changelist
p4 unshelve -s 12345

# Unshelve to different changelist
p4 unshelve -s 12345 -c 12346

# Unshelve to new changelist
p4 unshelve -s 12345 -c default
# Then move to new CL if desired

# Unshelve specific files
p4 unshelve -s 12345 file.txt

# Force unshelve (overwrite local changes)
p4 unshelve -s 12345 -f
```

### Delete Shelf

```bash
# Delete shelved files from changelist
p4 shelve -d -c 12345

# Delete specific files from shelf
p4 shelve -d -c 12345 file.txt

# Delete shelf completely
p4 shelve -d -c 12345 //...

# Promote shelf to commit (delete shelf after submit)
p4 submit -e 12345
```

## Shelving Workflows

### Work-in-Progress Backup

```bash
# End of day - shelve your work
p4 shelve -c 12345 -f

# Next day - continue working
# Files already open, shelf is backup

# If workspace lost, unshelve to recover
p4 unshelve -s 12345
```

### Task Switching

```bash
# Working on Feature A (CL 12345)
# Urgent bug needs fixing

# Shelve Feature A work
p4 shelve -c 12345

# Revert local changes (keep shelf)
p4 revert -c 12345 //...

# Work on bug fix
p4 edit bugfile.cs
# ... fix bug ...
p4 submit -d "Fix critical bug"

# Resume Feature A
p4 unshelve -s 12345
```

### Code Review Workflow

```bash
# Developer: Shelve for review
p4 shelve -c 12345
echo "Please review CL 12345"

# Reviewer: Get shelved changes to review workspace
p4 unshelve -s 12345 -c default

# Review code...

# Reviewer: Revert after review (or keep to test)
p4 revert //...

# Developer: After approval, submit
p4 submit -c 12345
p4 shelve -d -c 12345  # Clean up shelf
```

### Share Between Workspaces

```bash
# Workspace A: Shelve changes
p4 shelve -c 12345

# Workspace B: Get shelved changes
# (in different workspace)
p4 unshelve -s 12345 -c default

# Now both workspaces have the changes
```

### Pre-Integration Testing

```bash
# Shelve feature branch changes
p4 shelve -c 12345

# In integration workspace:
# Sync to main
p4 sync //depot/main/...

# Unshelve feature changes
p4 unshelve -s 12345

# Test integration
# ... run tests ...

# If tests pass, developer can submit
# If tests fail, developer can fix
```

## Advanced Shelving

### Shelve with Resolve

```bash
# When unshelving conflicts with current workspace

# Preview unshelve conflicts
p4 unshelve -n -s 12345

# Unshelve and resolve
p4 unshelve -s 12345
p4 resolve -am  # Auto-merge

# Or force overwrite
p4 unshelve -f -s 12345
```

### Update Existing Shelf

```bash
# Make more changes
p4 edit file.txt
# ... edit file ...

# Update shelf with new changes
p4 shelve -f -c 12345

# -f (force) replaces existing shelf
```

### Partial Shelving

```bash
# Shelve only some files from changelist
p4 shelve -c 12345 important.cs critical.cs

# Leave other files unshelved but still open
```

### Shelve Across Streams

```bash
# Shelve in one stream
p4 shelve -c 12345

# Unshelve to different stream (if mappings allow)
# May need branch mapping
p4 unshelve -s 12345 -b branch_mapping
```

## Shelf Management

### Find Old Shelves

```bash
# Find your old shelves
p4 changes -s shelved -u $P4USER

# Find shelves older than 30 days
p4 changes -s shelved -u $P4USER | while read line; do
    CL=$(echo $line | awk '{print $2}')
    DATE=$(p4 change -o $CL | grep "^Date:" | awk '{print $2}')
    echo "$CL: $DATE"
done
```

### Clean Up Old Shelves

```bash
#!/bin/bash
# cleanup-shelves.sh

# Delete shelves older than 30 days
CUTOFF=$(date -v-30d +%Y/%m/%d)

p4 changes -s shelved -u $P4USER | while read line; do
    CL=$(echo $line | awk '{print $2}')
    DATE=$(echo $line | awk '{print $4}')
    
    if [[ "$DATE" < "$CUTOFF" ]]; then
        echo "Deleting old shelf: $CL ($DATE)"
        p4 shelve -d -c $CL //...
    fi
done
```

### Shelf Statistics

```bash
# Count files in shelf
p4 describe -S -s 12345 | grep "^\.\.\." | wc -l

# Size of shelved files
p4 describe -S -s 12345 | grep "^\.\.\." | while read line; do
    FILE=$(echo $line | awk '{print $1}')
    p4 fstat -Ol "$FILE@=$CL" 2>/dev/null | grep fileSize
done
```

## Swarm Integration

### Shelve for Swarm Review

```bash
# Create review-ready changelist
p4 change  # Add description with review info

# Shelve for Swarm
p4 shelve -c 12345

# Swarm automatically detects and creates review
# Or trigger manually:
# POST to Swarm API
```

### Update Review

```bash
# Make changes based on feedback
p4 edit file.txt
# ... make changes ...

# Update shelf (triggers review update in Swarm)
p4 shelve -f -c 12345
```

### Commit After Approval

```bash
# After review approved in Swarm
p4 submit -e 12345

# -e submits shelved files directly
# Cleans up shelf automatically
```

## Best Practices

1. **Shelve frequently** - Backup work in progress
2. **Use descriptive changelist names** - Easy to identify shelves
3. **Clean up old shelves** - Don't leave orphaned shelves
4. **Force update** with `-f` when re-shelving
5. **Verify unshelve** - Check files are correct
6. **Delete shelf after submit** - Keep server clean
7. **Use for code review** - Before committing
8. **Don't rely solely on shelves** - Not a permanent backup
9. **Communicate shelf numbers** - For collaboration
10. **Test unshelved code** - Before submitting

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Files not shelved" | Check files are open in changelist |
| "Can't unshelve - conflicts" | Use `-f` to force or resolve |
| "Shelf not found" | Check changelist number, may be deleted |
| "No permission to unshelve" | Check protections, may need owner |
| "Files differ" | Use `-f` to replace or resolve |
| "Can't delete shelf" | Must delete all files first |

## Common Commands Reference

```bash
# Shelve
p4 shelve -c CL                    # Shelve changelist
p4 shelve -f -c CL                 # Replace existing shelf
p4 shelve -d -c CL                 # Delete shelf

# Unshelve
p4 unshelve -s CL                  # Unshelve to same CL
p4 unshelve -s CL -c TARGET        # Unshelve to different CL
p4 unshelve -f -s CL               # Force unshelve

# View
p4 describe -S CL                  # View shelved changelist
p4 changes -s shelved              # List all shelves
p4 changes -s shelved -u USER      # List user's shelves

# Submit shelved
p4 submit -e CL                    # Submit shelf directly
```
