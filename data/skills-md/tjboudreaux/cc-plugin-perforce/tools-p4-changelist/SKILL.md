---
name: tools-p4-changelist
description: Perforce changelist management including creating, editing, moving files between changelists, and pending change workflows.
---

# Perforce Changelist Management

## Overview

Changelists in Perforce group related file changes together for atomic submission. This skill covers creating, managing, and organizing changelists effectively.

## When to Use

- Organizing work into logical units
- Separating multiple tasks in progress
- Preparing changes for code review
- Managing pending vs submitted changes
- Moving files between changelists

## Core Concepts

### Changelist Types

| Type | Description |
|------|-------------|
| **Default** | Auto-created changelist for quick edits |
| **Numbered** | Named changelist with description |
| **Pending** | Not yet submitted |
| **Submitted** | Already committed to depot |
| **Shelved** | Changes stored on server, not submitted |

## Creating Changelists

### Create New Changelist

```bash
# Create changelist (opens editor)
p4 change

# Create with description directly
p4 change -o | sed 's/<enter description here>/Fix player movement/' | p4 change -i

# Create changelist and get number
CL=$(p4 change -o | sed 's/<enter description here>/My description/' | p4 change -i | grep -o '[0-9]*')
echo "Created changelist: $CL"
```

### Changelist Spec Format

```
Change: new
Client: your_workspace
User:   your_username
Status: pending
Description:
    Fix player movement bug
    
    - Fixed velocity calculation
    - Added ground check
    - Updated unit tests

Files:
    //depot/project/Player.cs    # edit
    //depot/project/Movement.cs  # edit
```

## Viewing Changelists

### List Changelists

```bash
# Your pending changelists
p4 changes -s pending -u $P4USER

# All pending changelists for a path
p4 changes -s pending //depot/project/...

# Recent submitted changelists
p4 changes -s submitted -m 20 //depot/project/...

# Changelists by specific user
p4 changes -u john.doe -m 10

# Changelists in date range
p4 changes -s submitted @2024/01/01,@2024/01/31

# Long output with full description
p4 changes -l -m 10 //depot/project/...
```

### View Specific Changelist

```bash
# View changelist details
p4 describe 12345

# View changelist without diffs
p4 describe -s 12345

# View changelist with shelved files
p4 describe -S 12345

# View changelist spec
p4 change -o 12345
```

## Editing Changelists

### Modify Changelist Description

```bash
# Edit changelist (opens editor)
p4 change 12345

# Update description programmatically
p4 change -o 12345 | sed 's/old description/new description/' | p4 change -i
```

### Change Changelist Owner

```bash
# Admin operation - change owner
p4 change -o 12345 | sed 's/User:.*/User: new_owner/' | p4 change -i -f
```

## Moving Files Between Changelists

### Reopen Files to Different Changelist

```bash
# Move single file to different changelist
p4 reopen -c 12345 file.txt

# Move file to default changelist
p4 reopen -c default file.txt

# Move all files from one changelist to another
p4 reopen -c 12346 //...@=12345

# Move files matching pattern
p4 reopen -c 12345 *.cs
```

### Split Changelist

```bash
# Create new changelist for some files
p4 change  # Creates new CL, note the number

# Move specific files to new changelist
p4 reopen -c NEW_CL file1.txt file2.txt

# Verify split
p4 opened -c 12345
p4 opened -c NEW_CL
```

### Merge Changelists

```bash
# Move all files from CL2 to CL1
p4 reopen -c 12345 //...@=12346

# Delete empty changelist
p4 change -d 12346
```

## Default Changelist

### Working with Default Changelist

```bash
# See files in default changelist
p4 opened -c default

# Edit file to default changelist
p4 edit file.txt

# Move from default to numbered changelist
p4 reopen -c 12345 file.txt

# Submit only default changelist
p4 submit

# Move all default files to new changelist
NEW_CL=$(p4 change -o | sed 's/<enter description here>/WIP: Feature X/' | p4 change -i | grep -o '[0-9]*')
p4 reopen -c $NEW_CL //...@=default
```

## Changelist Operations

### Delete Changelist

```bash
# Delete empty pending changelist
p4 change -d 12345

# Delete changelist with files (must revert or move files first)
p4 revert -c 12345 //...
p4 change -d 12345

# Or move files then delete
p4 reopen -c default //...@=12345
p4 change -d 12345

# Force delete (admin)
p4 change -d -f 12345
```

### Fix Submitted Changelist Description

```bash
# Admin operation - fix description after submit
p4 change -o 12345 | sed 's/typo/fixed/' | p4 change -i -f -u
```

## Changelist Workflow Patterns

### Feature Branch Pattern

```bash
# Create changelist for feature
p4 change -o | sed 's/<enter description here>/Feature: Player Dash Ability/' | p4 change -i
# Note the changelist number (e.g., 12345)

# All edits go to this changelist
p4 edit -c 12345 Player.cs
p4 edit -c 12345 PlayerAbilities.cs
p4 add -c 12345 DashAbility.cs

# Work on feature...

# When ready, submit
p4 submit -c 12345
```

### Bug Fix Pattern

```bash
# Quick fix to default
p4 edit BuggyFile.cs
# ... fix bug ...
p4 submit -d "Fix: Null reference in PlayerController"
```

### Multiple Tasks Pattern

```bash
# Create changelist for each task
p4 change  # CL for Task A
p4 change  # CL for Task B

# Work on Task A
p4 edit -c TASK_A_CL FileA.cs

# Switch to Task B
p4 edit -c TASK_B_CL FileB.cs

# Submit Task A when ready
p4 submit -c TASK_A_CL

# Continue Task B
```

### Work In Progress Pattern

```bash
# Create WIP changelist
WIP_CL=$(p4 change -o | sed 's/<enter description here>/WIP: Do not submit/' | p4 change -i | grep -o '[0-9]*')

# All experimental work goes here
p4 edit -c $WIP_CL experimental.cs

# When ready to submit, update description
p4 change $WIP_CL  # Edit description, remove WIP

# Submit
p4 submit -c $WIP_CL
```

## Querying Changelists

### Search Changelists

```bash
# Find changelists with keyword in description
p4 changes -l //depot/... | grep -B5 "player"

# Find changelists affecting specific file
p4 changes //depot/project/Player.cs

# Find your changelists from last week
p4 changes -u $P4USER -s submitted @$(date -v-7d +%Y/%m/%d),@now

# Count changelists per user
p4 changes -s submitted -m 1000 //depot/project/... | awk '{print $6}' | sort | uniq -c | sort -rn
```

### Changelist Statistics

```bash
# Files in changelist
p4 describe -s 12345 | grep "^\.\.\." | wc -l

# Lines changed in changelist
p4 describe 12345 | grep "^@@" | wc -l

# File types in changelist
p4 describe -s 12345 | grep "^\.\.\." | sed 's/.*#//' | sort | uniq -c
```

## Integration with Workflows

### Pre-Submit Checklist

```bash
#!/bin/bash
CL=$1

# Check changelist has description
DESC=$(p4 change -o $CL | grep -A100 "Description:" | grep -v "Description:" | head -1)
if [ -z "$DESC" ] || [ "$DESC" = "	<enter description here>" ]; then
    echo "ERROR: Changelist needs description"
    exit 1
fi

# Check for files
FILES=$(p4 opened -c $CL 2>/dev/null | wc -l)
if [ "$FILES" -eq 0 ]; then
    echo "ERROR: No files in changelist"
    exit 1
fi

# Check for unresolved
UNRESOLVED=$(p4 resolve -n //...@=$CL 2>&1 | grep -c "must resolve")
if [ "$UNRESOLVED" -gt 0 ]; then
    echo "ERROR: Unresolved files in changelist"
    exit 1
fi

echo "Changelist $CL ready to submit ($FILES files)"
```

### Changelist Template

```bash
# Create changelist with template
cat << 'EOF' | p4 change -i
Change: new
Description:
    [TYPE]: Brief description
    
    ## Changes
    - Change 1
    - Change 2
    
    ## Testing
    - [ ] Unit tests pass
    - [ ] Manual testing done
    
    ## Related
    - Jira: GOD-XXXX
EOF
```

## Best Practices

1. **Use numbered changelists** for any non-trivial work
2. **Write descriptive descriptions** - What and why
3. **One logical change per changelist** - Atomic commits
4. **Don't mix refactoring with features** - Separate CLs
5. **Prefix WIP changelists** to prevent accidental submit
6. **Review before submit** with `p4 describe -s`
7. **Keep changelists small** - Easier review and rollback
8. **Use consistent naming** - Team conventions
9. **Link to issue tracker** in description
10. **Clean up empty changelists** regularly

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Can't delete non-empty changelist" | Revert or move files first |
| "Changelist unknown" | Check number, may be submitted |
| "Can't edit submitted changelist" | Need admin `-f` flag |
| Files in wrong changelist | Use `p4 reopen -c` |
| Lost changelist number | `p4 changes -s pending -u $USER` |
| Description too long | Some triggers limit length |
