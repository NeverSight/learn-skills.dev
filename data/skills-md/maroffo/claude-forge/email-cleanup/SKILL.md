---
name: email-cleanup
description: "Clean up Gmail - archive old emails, delete promotions, manage storage. Use when user wants to clean inbox, archive emails, or free up space."
compatibility: "Requires gog CLI (Gmail CLI tool)."
tools: Bash, Read
---

# ABOUTME: Gmail bulk cleanup - archive old emails, delete promotions, free storage
# ABOUTME: Parameterized batch operations with safety-first approach

# Email Cleanup Skill

**Gmail:** See `../_GMAIL.md` for account config and commands.

## Safety Rules

1. **NEVER delete without confirmation** - show counts first
2. **Archive over delete** - prefer archiving (recoverable)
3. **Batch in chunks** - max 50 at a time

## Cleanup Targets

| Category | Query | Action |
|----------|-------|--------|
| Promotions | `category:promotions older_than:30d` | Archive |
| Social | `category:social older_than:14d` | Archive |
| Read updates | `category:updates is:read older_than:7d` | Archive |
| Large emails | `larger:10M` | Review individually |
| Unsubscribe candidates | `unsubscribe is:read older_than:30d` | Review |

## Workflow

### Step 1: Count each category
```bash
gog gmail search "<query>" --account=maroffo@gmail.com --json | jq '.resultSizeEstimate'
```

### Step 2: Present summary table with counts and suggested actions

### Step 3: Execute (with confirmation)
```bash
THREADS=$(gog gmail search "<query>" --account=maroffo@gmail.com --json --max=50 | jq -r '.threads[].id')
for tid in $THREADS; do
  gog gmail thread modify $tid --account=maroffo@gmail.com --remove-labels=INBOX
done
```

Process in batches of 50. Report progress.

## Quick Stats
```bash
gog gmail labels get INBOX --account=maroffo@gmail.com
gog gmail labels get CATEGORY_PROMOTIONS --account=maroffo@gmail.com
```
