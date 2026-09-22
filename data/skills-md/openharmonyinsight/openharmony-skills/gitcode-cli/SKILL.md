---
name: gitcode-cli
description: Use when managing GitCode repositories from the terminal with oh-gc CLI — auth, issues, PRs, reviewers, testers, labels, releases, and repo config. Triggers on oh-gc commands, GitCode issue/PR management, or when user wants to interact with GitCode without a browser.
---

# oh-gc CLI — GitCode Command Line Tool

**Version:** 0.7.4 | **Updated:** 2026-04-10

`oh-gc` is a CLI for [GitCode](https://gitcode.com), modeled after GitHub CLI (`gh`). Manages authentication, issues, pull requests, releases, and repo configuration from the terminal.

**Package:** `npm install -g @oh-gc/cli` (requires Node.js 18+)

## ⚠️ MANDATORY FIRST STEP — DO NOT SKIP

**Run `oh-gc --version` as the VERY FIRST command before ANY other oh-gc command.**

- If not found → `npm install -g @oh-gc/cli@{version}` (use the version shown at the top of this document)
- If the version does not match **{version}** → `npm install -g @oh-gc/cli@{version}` to install the exact matching version
- **Do NOT run `oh-gc auth`, `oh-gc issue`, `oh-gc pr`, or any other command until the version is confirmed matching.**

## Prerequisites

After confirming the version matches, check the following:

1. **Token configured?** Run `oh-gc auth status`
   - If not logged in → `oh-gc auth login` (prompts for GitCode personal access token)
   - Token obtained at: GitCode → 个人设置 → 访问令牌
2. **Repository context?** Either:
   - Inside a git repo with a `gitcode.com` remote (remote name configurable via `oh-gc repo set-remote <name>`), OR
   - Use `--repo owner/repo` flag to specify any repository

## Global Flags

All commands support:
- `--json` — output raw JSON instead of formatted table
- `--help` — show command help

## Repository Flag

Most commands that operate on a repository support the `--repo` flag, which allows specifying a target repository without being inside a git clone:

- `--repo owner/repo` — target repository in OWNER/REPO format

This is useful for:
- Operating on repositories you haven't cloned locally
- Cross-repo operations (e.g., creating a PR from fork to upstream)
- CI/CD scripts that need to interact with multiple repositories

```bash
# List issues in any repository
oh-gc issue list --repo openharmony/arkui_ace_engine

# Create an issue without cloning
oh-gc issue create --repo owner/repo --title "Bug report"

# View a PR on another repo
oh-gc pr view 123 --repo owner/repo

# Cross-repo PR (fork to upstream) — use owner:branch for --head
oh-gc pr create --repo upstream-owner/repo --head myname:my-feature --base main
```

## Command Reference

### Authentication

```bash
oh-gc auth login          # Log in with personal access token (interactive prompt)
oh-gc auth logout         # Remove stored token
oh-gc auth status         # Show current user info
```

Token stored at `~/.config/gitcode-cli/config.json`.

### Issues

```bash
# List
oh-gc issue list                              # Open issues (default)
oh-gc issue list --state closed               # Closed issues
oh-gc issue list --state all                  # All issues
oh-gc issue list --assignee alice             # Filter by assignee
oh-gc issue list --search "login bug"         # Search by keyword
oh-gc issue list --limit 50                   # Max results (default: 30)

# View
oh-gc issue view 12                           # Show issue detail + recent comments

# Create
oh-gc issue create                            # Interactive mode
oh-gc issue create --title "Bug" --body "..."         # With flags
oh-gc issue create --repo owner/repo --title "Bug"    # On another repo
oh-gc issue create --assignee alice --labels "bug,P0" # With metadata

# Comment
oh-gc issue comment 12                        # Interactive prompt
oh-gc issue comment 12 --body "Confirmed"     # With flag

# Close/Reopen
oh-gc issue close 12                          # Close an issue
oh-gc issue reopen 12                         # Reopen a closed issue

# Labels
oh-gc issue labels 12 bug,feature             # Add labels
oh-gc issue labels 12 bug --remove            # Remove label

# History
oh-gc issue history 12                        # View modification history of an issue

# Reactions
oh-gc issue reactions 12                      # List emoji reactions on issue

# Linked PRs
oh-gc issue prs 12                            # List PRs linked to an issue
oh-gc issue prs 12 --mode 1                   # Only mergeable PRs

# Related branches
oh-gc issue branches 12                       # List branches related to an issue
oh-gc issue branches 12 --set feature-x,fix-y # Set related branches

# Comment management
oh-gc issue comment-get <id>                  # Get a single comment
oh-gc issue comment-edit <id> --body "new"    # Edit a comment
oh-gc issue comment-delete <id>               # Delete a comment
oh-gc issue comment-history <id>              # View comment edit history
oh-gc issue comment-reactions <id>            # List reactions on a comment
```

### Pull Requests

```bash
# List
oh-gc pr list                                 # Open PRs (default)
oh-gc pr list --state merged                  # Merged PRs
oh-gc pr list --state all                     # All PRs
oh-gc pr list --author alice                  # Filter by author
oh-gc pr list --reviewer bob                  # Filter by reviewer
oh-gc pr list --assignee carol                # Filter by assignee
oh-gc pr list --limit 50                      # Max results (default: 30)

# View
oh-gc pr view 5                               # Show PR detail

# Create
oh-gc pr create                               # Interactive mode
oh-gc pr create --title "Fix bug" --base main         # From current branch
oh-gc pr create --head feature --base main --draft    # Draft PR
oh-gc pr create --repo owner/repo --head myname:feature  # Cross-repo PR (fork→upstream, use owner:branch)

# Update
oh-gc pr update 5 --title "New title"         # Update title
oh-gc pr update 5 --body "New description"    # Update body
oh-gc pr update 5 --state closed              # Close PR
oh-gc pr update 5 --state open                # Reopen PR
oh-gc pr update 5 --draft                     # Mark as draft
oh-gc pr update 5 --labels "bug,wip"          # Set labels

# Close/Reopen
oh-gc pr close 5                              # Close a PR
oh-gc pr reopen 5                             # Reopen a closed PR

# Diff
oh-gc pr diff 5                               # Show full diff with colors
oh-gc pr diff 5 --name-only                   # Only changed file names
oh-gc pr diff 5 --color never                 # No color (for piping)

# Merge
oh-gc pr merge 5                              # Merge commit (default)
oh-gc pr merge 5 --method squash              # Squash merge
oh-gc pr merge 5 --method rebase              # Rebase merge

# Comment
oh-gc pr comment 5 --body "LGTM!"                                    # General comment
oh-gc pr comment 5 --body "Fix this" --path src/main.ts --line 10    # Line comment
oh-gc pr comment 5 --repo owner/repo --body "Note"                   # On another repo

# List/delete comments
oh-gc pr comments 5                                   # List all comments
oh-gc pr comments 5 --limit 10 --latest               # Latest 10 comments first
oh-gc pr comments 5 --full-body                       # Show full comment bodies
oh-gc pr comments 5 --comment-type diff_comment       # Only diff/line comments
oh-gc pr comments 5 --comment-type pr_comment         # Only general comments
oh-gc pr comments 5 --delete 12345                    # Delete by note_id

# Reactions
oh-gc pr reactions 5                          # List emoji reactions on PR

# Commits
oh-gc pr commits 5                            # List commits in PR

# Reviewers
oh-gc pr reviewers 5 alice,bob                # Assign reviewers
oh-gc pr reviewers 5 alice --append           # Add to existing reviewers
oh-gc pr reviewers 5 alice --remove           # Remove reviewer

# Testers
oh-gc pr testers 5 alice,bob                  # Assign testers
oh-gc pr testers 5 alice --append             # Add to existing testers
oh-gc pr testers 5 alice --remove             # Remove tester

# Review & Test approval
oh-gc pr review 5                             # Approve PR review
oh-gc pr review 5 --force                     # Force approve
oh-gc pr test 5                               # Mark test passed
oh-gc pr test 5 --force                       # Force mark

# Labels
oh-gc pr labels 5 bug,enhancement             # Add labels
oh-gc pr labels 5 bug --remove                # Remove label
oh-gc pr labels 5 bug,feature --replace       # Replace all labels

# Link issues
oh-gc pr link 5 1,2,3                         # Link issues to PR
oh-gc pr link 5 1,2 --remove                  # Unlink issues

# Operation logs
oh-gc pr logs 5                               # Show PR operation history

# Files
oh-gc pr files 5                              # List changed files in PR

# History
oh-gc pr history 5                            # View PR modification history

# Linked issues
oh-gc pr linked-issues 5                      # List issues linked to PR

# Assignees
oh-gc pr assignees 5 --add alice,bob          # Assign users
oh-gc pr assignees 5 --reset                  # Reset assignee status
oh-gc pr assignees 5 --reset --all            # Reset all assignees
oh-gc pr assignees 5 --remove alice           # Remove assignee

# PR settings
oh-gc pr settings                             # View repo PR settings
oh-gc pr settings-update --merge-method squash --delete-branch-on-merge  # Update settings

# Option reviewers
oh-gc pr option-reviewers 5                   # List users eligible to review

# Comment management
oh-gc pr comment-get <id>                     # Get a single PR comment
oh-gc pr comment-edit <id> --body "new"       # Edit a PR comment
oh-gc pr comment-delete <id>                  # Delete a PR comment
oh-gc pr comment-history <id>                 # View comment edit history
oh-gc pr comment-reactions <id>               # List reactions on a comment
```

### Releases

```bash
oh-gc release create                          # Use version from package.json
oh-gc release create v1.0.0                   # Specific version
oh-gc release create --prerelease             # Mark as prerelease
oh-gc release create v1.0.0 --notes "..."     # Custom release notes
```

### Repo Configuration

```bash
oh-gc repo list                               # List your repositories
oh-gc repo list --org myorg                   # List org repositories
oh-gc repo create myrepo                      # Create a new repository
oh-gc repo create myrepo --org myorg          # Create under an org
oh-gc repo delete --yes                       # Delete current repo (no prompt)
oh-gc repo fork                               # Fork current repo to your account
oh-gc repo fork --org myorg                   # Fork into an organization
oh-gc repo forks                              # List forks of current repo
oh-gc repo settings                           # View repo advanced settings
oh-gc repo settings --disable-fork           # Update a setting
oh-gc repo languages                          # Show language breakdown
oh-gc repo contributors                       # List contributors
oh-gc repo contributors --stats               # Show detailed contribution stats
oh-gc repo events                             # List repository events
oh-gc repo events --filter push               # Filter by event type
oh-gc repo stats --branch main                # Commit stats per author
oh-gc repo stats --downloads                  # Download stats by date
oh-gc repo archive --password secret          # Archive a repository
oh-gc repo archive --open --password secret   # Unarchive a repository
oh-gc repo transition                         # View permission inheritance mode
oh-gc repo transition --mode 2               # Set to independent mode
oh-gc repo module --wiki --issues            # Enable wiki and issues modules
oh-gc repo module --no-fork                  # Disable fork module
oh-gc repo roles                              # List customized roles
oh-gc repo list --user alice                  # List user's public repos
oh-gc repo list --visibility private          # List private repositories
oh-gc repo get-remote                         # Show which remote oh-gc uses
oh-gc repo set-remote upstream                # Use a different remote
oh-gc repo view                               # View repository info
oh-gc repo update --description "..."         # Update repository settings
oh-gc repo transfer <new-owner>               # Transfer repository ownership
```

Remote override stored at `.gitcode/oh-gc-config.json` in repo root.

### Search

```bash
oh-gc search repos "keyword"                  # Search repositories
oh-gc search issues "keyword"                 # Search issues across repos
oh-gc search code "keyword"                   # Search code across repos
```

### User

```bash
oh-gc user view                               # View your profile
oh-gc user view alice                         # View another user's profile
oh-gc user edit --name "New Name" --bio "..."  # Update your profile
oh-gc user edit --avatar "https://..."          # Update avatar
oh-gc user emails                             # List your email addresses
oh-gc user followers                          # List your followers
oh-gc user following                          # List users you follow
oh-gc user events alice                       # List user activity events
oh-gc user events alice --year 2024           # Filter events by year
oh-gc user search alice                       # Search users
oh-gc user search bob --sort joined_at        # Sort by registration time
oh-gc user namespace alice                    # Get namespace by path
oh-gc user namespaces                         # List all your namespaces
oh-gc user namespaces --mode project          # Filter namespace mode
oh-gc user keys                               # List your SSH keys
oh-gc user key-add --title "My Key" --key "ssh-rsa ..."  # Add SSH key
oh-gc user key-delete 123                     # Delete SSH key by ID
oh-gc user starred                            # List your starred repos
oh-gc user starred alice                      # List another user's starred repos
oh-gc user subscriptions                      # List your watched repos
oh-gc user subscriptions alice                # List another user's watched repos
oh-gc user issues                             # List your issues across all repos
oh-gc user issues --state closed --filter created  # Filter user issues
oh-gc user issues --since "2024-01-01T00:00:00Z"  # Issues updated since date
oh-gc user prs                                # List your PRs across all repos
oh-gc user prs --state merged --scope assigned_to_me  # Filter user PRs
oh-gc user prs --source-branch feature --target-branch main  # Filter by branches
oh-gc user orgs alice                         # List user's organizations
oh-gc user membership myorg                   # View your org membership
oh-gc user leave-org myorg                    # Leave an organization
```

### Branches

```bash
oh-gc branch list                             # List all branches
oh-gc branch list --protected                 # List only protected branches
oh-gc branch get <name>                       # Get branch details
oh-gc branch create <name> --ref <sha/branch> # Create a new branch
oh-gc branch delete <name>                    # Delete a branch
oh-gc branch protect <name>                   # Set branch protection rules
oh-gc branch protect <name> --enforce-admins                    # Enforce protection for admins
oh-gc branch protect <name> --require-status-checks ci,lint     # Require status checks
oh-gc branch protect <name> --dismiss-stale-reviews             # Dismiss stale PR reviews
oh-gc branch protect <name> --unprotect       # Remove branch protection
oh-gc branch protect-rules                    # List all branch protection rules
oh-gc branch protect-rule-create <pattern> --pusher <roles> --merger <roles>  # Create protection rule
oh-gc branch protect-rule-update <pattern> --pusher <roles> --merger <roles>  # Update protection rule
oh-gc branch protect-rule-delete <pattern>    # Delete protection rule
```

### Commits

```bash
oh-gc commit list                             # List commits
oh-gc commit list --sha main                  # List commits from specific branch
oh-gc commit get <sha>                        # Get commit details
oh-gc commit diff <sha>                       # View commit diff
oh-gc commit compare <base> <head>            # Compare two commits or branches
oh-gc commit comments <sha>                   # List comments on a commit
oh-gc commit comment <sha> --body "text"      # Create a commit comment
```

### Files

```bash
oh-gc file get <path>                         # Get file contents (base64 encoded)
oh-gc file raw <path> --ref main              # Get raw file contents
oh-gc file list                               # List repository files
oh-gc file create <path> --content "text" --message "msg"  # Create a file
oh-gc file update <path> --sha <sha> --content "text" --message "msg"  # Update a file
oh-gc file delete <path> --sha <sha> --message "msg"       # Delete a file
```

### Collaborators

```bash
oh-gc collaborator list                       # List repository collaborators
oh-gc collaborator add <username>             # Add a collaborator
oh-gc collaborator remove <username>          # Remove a collaborator
oh-gc collaborator permission <username>      # Get collaborator permission level
```

### Labels

```bash
oh-gc label list                              # List repository labels
oh-gc label create                            # Create a new label
oh-gc label update <name>                     # Update a label
oh-gc label delete <name>                     # Delete a label
```

### Milestones

```bash
oh-gc milestone list                          # List milestones
oh-gc milestone get <number>                  # Get milestone details
oh-gc milestone create                        # Create a new milestone
oh-gc milestone update <number>               # Update a milestone
oh-gc milestone delete <number>               # Delete a milestone
```

### Webhooks

```bash
oh-gc hook list                               # List repository webhooks
oh-gc hook get <id>                           # Get webhook details
oh-gc hook create                             # Create a webhook
oh-gc hook delete <id>                        # Delete a webhook
```

### Tags

```bash
oh-gc tag list                                # List repository tags
oh-gc tag create <name> --ref <sha/branch>    # Create a tag
oh-gc tag delete <name>                       # Delete a tag
oh-gc tag protect <name>                      # Protect a tag
oh-gc tag protect-get <name>                  # Get protected tag details
oh-gc tag protect-create <name> --access-level 40  # Create protected tag rule
oh-gc tag protect-update <name> --access-level 30  # Update protected tag rule
oh-gc tag protect-delete <name>               # Delete protected tag rule
```

### Organizations

```bash
oh-gc org list                                # List your organizations
oh-gc org view <org>                          # Get organization details
oh-gc org members <org>                       # List organization members
```

## Workflow: Full PR Lifecycle

Complete workflow from code change to merged PR:

```
Step 1: Create PR
  oh-gc pr create --title "Add feature X" --base main
  → outputs PR number (e.g., #42)

Step 2: Assign people
  oh-gc pr reviewers 42 alice,bob
  oh-gc pr testers 42 carol

Step 3: Add metadata
  oh-gc pr labels 42 feature,v2.0
  oh-gc pr link 42 15,16           # Link related issues

Step 4: Review cycle
  oh-gc pr diff 42                 # Reviewer checks diff
  oh-gc pr comments 42             # Check existing feedback
  oh-gc pr comment 42 --body "LGTM"
  oh-gc pr review 42               # Approve review
  oh-gc pr test 42                 # Mark test passed

Step 5: Merge
  oh-gc pr merge 42 --method squash
```

## Workflow: Issue Triage

```
Step 1: Find issues
  oh-gc issue list --search "crash"
  oh-gc issue list --state all --assignee alice

Step 2: Inspect
  oh-gc issue view 15

Step 3: Respond
  oh-gc issue comment 15 --body "Investigating, likely related to #12"

Step 4: Create follow-up
  oh-gc issue create --title "Fix crash on login" --labels "bug,P0" --assignee bob
```

## Workflow: Cross-Repo PR (Fork → Upstream)

For contributing to repositories you don't own, use `--head owner:branch` format to specify the fork owner and branch:

```
Step 1: Create PR from fork to upstream
  oh-gc pr create --repo upstream-owner/repo --head myname:my-feature --base master --title "Fix bug"

Step 2: Manage on the upstream repo
  oh-gc pr view 42 --json    # Check status
```

Note: `--repo` targets the upstream repo. `--head` uses `owner:branch` format (colon separator) where `owner` is your GitCode username and `branch` is the branch name in your fork. Do NOT use `owner/branch` (slash) — the API requires a colon.

## Configuration

| Setting | Location | How to set |
|---------|----------|------------|
| Auth token | `~/.config/gitcode-cli/config.json` | `oh-gc auth login` |
| Remote override | `.gitcode/oh-gc-config.json` | `oh-gc repo set-remote <name>` |
| Proxy | `https_proxy` / `HTTPS_PROXY` env var | Automatic |

## Decision Tree

```
User wants to interact with GitCode
  ↓
Version matches? (oh-gc --version)
  ↓ No → npm install -g @oh-gc/cli@{version}
  ↓ Yes
Logged in? (oh-gc auth status)
  ↓ No → oh-gc auth login
  ↓ Yes
Inside git repo with gitcode.com remote?
  ↓ No → Use --repo flag, or cd to repo
  ↓ Yes
What does user want?
  ├─ List/view issues      → oh-gc issue list / issue view
  ├─ Create issue           → oh-gc issue create
  ├─ Update issue           → oh-gc issue update
  ├─ Close/reopen issue     → oh-gc issue close / issue reopen
  ├─ Comment on issue       → oh-gc issue comment
  ├─ Manage issue labels    → oh-gc issue labels
  ├─ View issue history     → oh-gc issue history
  ├─ View issue reactions   → oh-gc issue reactions
  ├─ List/view PRs          → oh-gc pr list / pr view
  ├─ Create PR              → oh-gc pr create
  ├─ Update PR              → oh-gc pr update
  ├─ Close/reopen PR        → oh-gc pr close / pr reopen
  ├─ View PR reactions      → oh-gc pr reactions
  ├─ Review PR diff         → oh-gc pr diff
  ├─ Comment on PR          → oh-gc pr comment (general) or --path --line (line-level)
  ├─ Assign reviewers       → oh-gc pr reviewers
  ├─ Assign testers         → oh-gc pr testers
  ├─ Approve review         → oh-gc pr review
  ├─ Mark test passed       → oh-gc pr test
  ├─ Manage labels          → oh-gc pr labels
  ├─ Link issues to PR      → oh-gc pr link
  ├─ Merge PR               → oh-gc pr merge
  ├─ View PR history        → oh-gc pr logs
  ├─ Create release         → oh-gc release create
  ├─ Search repos/issues    → oh-gc search repos / search issues / search code
  ├─ View user profile      → oh-gc user view
  ├─ Edit user profile      → oh-gc user edit
  ├─ List user events       → oh-gc user events
  ├─ Search users           → oh-gc user search
  ├─ Manage SSH keys        → oh-gc user keys / user key-add / user key-delete
  ├─ View starred repos     → oh-gc user starred
  ├─ View watched repos     → oh-gc user subscriptions
  ├─ View namespaces        → oh-gc user namespace / user namespaces
  ├─ Manage branches        → oh-gc branch list / branch get / branch protect
  ├─ View commits/files     → oh-gc commit list / file get
  ├─ Manage collaborators   → oh-gc collaborator list / add / remove
  ├─ Manage labels          → oh-gc label list / create / update / delete
  ├─ Manage milestones      → oh-gc milestone list / create / update
  ├─ Manage webhooks        → oh-gc hook list / create / delete
  └─ Configure remote       → oh-gc repo set-remote / repo get-remote
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| "Not logged in" | No token configured | `oh-gc auth login` |
| "Authentication failed" | Token expired or invalid | Re-run `oh-gc auth login` with new token |
| "Remote not found" | Not in a git repo or remote missing | `cd` to repo, check `git remote -v` |
| "Not a GitCode repository" | Remote URL isn't `gitcode.com` | Add a gitcode.com remote |
| "Could not connect" | Network issue or proxy not set | Check internet; set `https_proxy` env var if behind proxy |
| "Rate limit exceeded" | Too many API calls | Wait and retry |
| "API error 405" | Wrong HTTP method (internal) | Update oh-gc to latest version |
| "Can not find the branch" | `--head` missing fork owner prefix | Use `--head owner:branch` (colon, not slash) for cross-repo PRs |

## URL Format

When constructing GitCode URLs for issues and PRs, use the **singular** form for PRs:

- Issue: `https://gitcode.com/{owner}/{repo}/issues/{number}` (plural: issues)
- PR: `https://gitcode.com/{owner}/{repo}/pull/{number}` (**singular**: pull, NOT pulls)

**Common mistake:** Using `/pulls/` (GitHub style) instead of `/pull/`. GitCode uses singular `pull`, not `pulls`.

## Tips

- Use `--json` to pipe output to `jq` for scripting: `oh-gc pr list --json | jq '.[].title'`
- Use `--repo owner/repo` to operate on any repository without cloning it first
- Interactive mode (no flags) prompts for required fields — useful for one-off operations
- `oh-gc pr comments --comment-type diff_comment` filters to only code review comments
- `oh-gc pr reviewers --append` adds reviewers without replacing existing ones
- `oh-gc pr update --state closed` is the way to close a PR without merging
- When reporting PR links to the user, always use `https://gitcode.com/{owner}/{repo}/pull/{number}` (singular `pull`)
