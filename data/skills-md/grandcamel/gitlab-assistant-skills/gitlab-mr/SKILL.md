---
name: "gitlab-mr"
description: "GitLab merge request operations. ALWAYS use this skill when user wants to: (1) list merge requests, (2) view MR details, (3) create new MRs, (4) approve/merge MRs, (5) checkout MR branches, (6) add notes/comments, (7) rebase MRs."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# Merge Request Skill

Merge request operations for GitLab using the `glab` CLI.

## Quick Reference

| Operation | Command | Risk |
|-----------|---------|:----:|
| List MRs | `glab mr list` | - |
| View MR | `glab mr view <id>` | - |
| Create MR | `glab mr create` | ⚠️ |
| Checkout MR | `glab mr checkout <id>` | - |
| Approve MR | `glab mr approve <id>` | ⚠️ |
| Merge MR | `glab mr merge <id>` | ⚠️⚠️ |
| Update MR | `glab mr update <id>` | ⚠️ |
| Close MR | `glab mr close <id>` | ⚠️ |
| Reopen MR | `glab mr reopen <id>` | ⚠️ |
| Delete MR | `glab mr delete <id>` | ⚠️⚠️ |
| Rebase MR | `glab mr rebase <id>` | ⚠️ |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User wants to work with merge requests
- User mentions "MR", "merge request", "pull request", or related terms
- User wants to review, approve, or merge code

**NEVER use when:**
- User wants bulk operations on 10+ MRs (use gitlab-bulk instead)
- User is only searching/filtering MRs (use gitlab-search instead)

## Available Commands

### List Merge Requests

```bash
glab mr list [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `--assignee=@me` | Filter by assignee (use @me for yourself) |
| `--reviewer=@me` | Filter by reviewer |
| `--author=<username>` | Filter by author |
| `--label=<labels>` | Filter by comma-separated labels |
| `--state=<state>` | Filter by state: opened, closed, merged, all |
| `--source-branch=<branch>` | Filter by source branch |
| `--target-branch=<branch>` | Filter by target branch |
| `-P, --per-page=<n>` | Number of items per page |

**Examples:**
```bash
# List MRs assigned to you
glab mr list --assignee=@me

# List review requests for you
glab mr list --reviewer=@me

# List open MRs with specific label
glab mr list --state=opened --label=bug

# List MRs targeting main branch
glab mr list --target-branch=main
```

### View Merge Request Details

```bash
glab mr view <id> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-w, --web` | Open MR in browser |
| `-c, --comments` | Show MR comments and notes |
| `-s, --system-logs` | Show system activities/logs |

**Examples:**
```bash
# View MR details in terminal
glab mr view 123

# Open MR in browser
glab mr view 123 --web

# View MR with comments
glab mr view 123 --comments
```

### Create Merge Request

```bash
glab mr create [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-t, --title=<title>` | MR title |
| `-d, --description=<desc>` | MR description |
| `-b, --target-branch=<branch>` | Target branch (default: default branch) |
| `-f, --fill` | Use commit messages for title/description |
| `--draft` | Create as draft MR |
| `-a, --assignee=<users>` | Comma-separated assignees |
| `-r, --reviewer=<users>` | Comma-separated reviewers |
| `-l, --label=<labels>` | Comma-separated labels |
| `-m, --milestone=<milestone>` | Milestone title |
| `--squash-on-merge` | Squash commits on merge |
| `--remove-source-branch` | Remove source branch on merge |
| `-w, --web` | Open created MR in browser |
| `-y, --yes` | Skip confirmation prompts |

**Examples:**
```bash
# Create MR with title and description
glab mr create -t "Add new feature" -d "This MR adds..."

# Create MR from commit messages
glab mr create --fill

# Create draft MR
glab mr create --draft -t "WIP: New feature"

# Create MR with reviewers and labels
glab mr create -t "Fix bug" -r "reviewer1,reviewer2" -l "bug,urgent"

# Create MR and open in browser
glab mr create -t "Feature" --web
```

### Checkout Merge Request Branch

```bash
glab mr checkout <id> [options]
```

**Shortcut:** `glab co <id>`

**Options:**
| Flag | Description |
|------|-------------|
| `-b, --branch=<name>` | Local branch name |
| `-t, --track` | Set up tracking for the remote branch |

**Examples:**
```bash
# Checkout MR branch
glab mr checkout 123

# Checkout with custom local branch name
glab mr checkout 123 -b my-local-branch

# Shortcut
glab co 123
```

### Approve/Revoke Merge Request

```bash
# Approve MR
glab mr approve <id>

# Revoke approval
glab mr revoke <id>

# View approvers
glab mr approvers <id>
```

### Merge/Close/Reopen

```bash
# Merge MR
glab mr merge <id> [options]

# Close MR
glab mr close <id>

# Reopen closed MR
glab mr reopen <id>
```

**Merge Options:**
| Flag | Description |
|------|-------------|
| `-s, --squash` | Squash commits |
| `-d, --remove-source-branch` | Delete source branch after merge |
| `--when-pipeline-succeeds` | Merge when pipeline succeeds |
| `-m, --message=<msg>` | Custom merge commit message |
| `-y, --yes` | Skip confirmation |

**Examples:**
```bash
# Merge with squash
glab mr merge 123 --squash

# Merge and delete source branch
glab mr merge 123 --remove-source-branch

# Auto-merge when pipeline succeeds
glab mr merge 123 --when-pipeline-succeeds
```

### Update Merge Request

```bash
glab mr update <id> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-t, --title=<title>` | Update title |
| `-d, --description=<desc>` | Update description |
| `-a, --assignee=<users>` | Update assignees |
| `-r, --reviewer=<users>` | Update reviewers |
| `-l, --label=<labels>` | Update labels |
| `--unlabel=<labels>` | Remove labels |
| `--draft` | Mark as draft |
| `--ready` | Mark as ready (remove draft status) |
| `--lock-discussion` | Lock discussion |
| `--unlock-discussion` | Unlock discussion |

**Examples:**
```bash
# Update title
glab mr update 123 -t "New title"

# Add reviewers
glab mr update 123 -r "user1,user2"

# Mark as ready (remove draft)
glab mr update 123 --ready

# Add and remove labels
glab mr update 123 -l "approved" --unlabel "needs-review"
```

### Add Note/Comment

```bash
glab mr note <id> -m "<message>"
```

**Examples:**
```bash
# Add comment
glab mr note 123 -m "LGTM!"

# Add closing note
glab mr note 123 -m "Closing because !456 supersedes this"
```

### Rebase Merge Request

```bash
glab mr rebase <id>
```

### View Diff

```bash
glab mr diff <id> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `--color=<when>` | When to show color: always, never, auto |

### Subscribe/Unsubscribe

```bash
# Subscribe to MR notifications
glab mr subscribe <id>

# Unsubscribe
glab mr unsubscribe <id>
```

### Add to Todo

```bash
glab mr todo <id>
```

## Common Workflows

### Workflow 1: Review and Approve

```bash
# 1. List MRs assigned for review
glab mr list --reviewer=@me

# 2. View MR details
glab mr view 123

# 3. Checkout to test locally
glab mr checkout 123

# 4. Run tests, review code...

# 5. Approve if good
glab mr approve 123

# 6. Add comment
glab mr note 123 -m "Reviewed and approved. Great work!"
```

### Workflow 2: Create Feature MR

```bash
# 1. Create branch and make changes
git checkout -b feature/my-feature

# 2. Commit changes
git add . && git commit -m "Add new feature"

# 3. Push branch
git push -u origin feature/my-feature

# 4. Create MR
glab mr create -t "Add new feature" -d "Description..." --draft

# 5. Mark ready when done
glab mr update <id> --ready
```

### Workflow 3: Quick Fix

```bash
# Create MR from current branch with commit info
glab mr create --fill --yes
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Authentication failed | Invalid/expired token | Run `glab auth login` |
| MR not found | Invalid ID or no access | Verify ID with `glab mr list` |
| Permission denied | Insufficient rights | Check project permissions |
| Cannot merge | Conflicts or pipeline failed | Resolve conflicts, wait for pipeline |
| Branch not found | Source branch deleted | Check if branch exists |

## Related Documentation

- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
