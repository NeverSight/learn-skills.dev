---
name: gitcode-pr
description: Handle GitCode PR workflow for OpenHarmony - commit changes, push to fork remote, create issue, create PR from fork to upstream using repo's .gitee/PULL_REQUEST_TEMPLATE.zh-CN.md with issue linking via #number. Use when user wants to submit/create PR or commit changes. Auto-checks if PR exists and only pushes when PR already exists.
---

# GitCode PR Workflow for OpenHarmony

Handles complete GitCode PR submission for OpenHarmony repositories with intelligent remote detection and issue-PR linking. Use the gitcode mcp. If gitcode mcp is not present, warn the user and terminate the skill immediately.

## Intelligent Remote Detection

### Identification Algorithm

Never assume remote names. Use this algorithm to identify upstream and fork:

```bash
# Step 1: List all remotes
git remote -v

# Step 2: Parse each remote
for remote in $(git remote); do
  url=$(git remote get-url $remote)
  
  # Parse owner from URL
  # Format: https://gitcode.com/<owner>/<repo> or https://gitcode.com/<owner>/<repo>.git
  if [[ "$url" =~ https://gitcode\.com/([^/]+)/(.+) ]]; then
    owner="${BASH_REMATCH[1]}"
    repo=$(echo "${BASH_REMATCH[2]}" | sed 's/\.git$//')
    
    # Determine type
    if [ "$owner" = "openharmony" ]; then
      echo "$remote: UPSTREAM ($owner/$repo)"
    else
      echo "$remote: FORK ($owner/$repo)"
    fi
  fi
done
```

### Remote Classification

| Owner | Type | Usage |
|-------|-------|--------|
| `openharmony` | UPSTREAM | Source for PR template, target for PR base, issue creation |
| Other usernames | FORK | Push target, PR head source |

### Decision Matrix

| Upstream Remotes | Fork Remotes | Action |
|-----------------|-------------|--------|
| Found | Found | Use both: create issue/PR on upstream, push to fork |
| Found | None | Ask user: "Found upstream but no fork. Need to fork first?" |
| None | Found | Use fork as both push target and PR target (uncommon) |
| None | Multiple (no openharmony) | Ask user to select: "Which remote to use?" |
| None | Single (no openharmony) | Use as fork, warn: "No upstream (openharmony) remote found" |

### User Prompting

When remote is ambiguous, prompt user:

```markdown
I found these GitCode remotes:

- **remote_name**: owner/repo (UPSTREAM/FORK)

Which remote should I use for:
- Pushing changes?
- Creating the PR?

Please specify the remote name, or press Enter to use [default].
```

## Workflow

Follow this workflow when user requests PR submission:

### 1. Check Current State

Check git status and branch:
```bash
git status
git branch --show-current
git remote -v
```

Determine:
- What is the current branch name?
- Identify upstream and fork remotes using algorithm above

### 2. Check if PR Exists

Use `gitcode_list_pull_requests` to check for existing PRs:

```bash
# Get upstream owner/repo (parse from upstream remote URL)
UPSTREAM_REMOTE=$(detect_upstream_remote)
UPSTREAM_URL=$(git remote get-url $UPSTREAM_REMOTE)
# Parse: openharmony/security_code_signature from URL

# List PRs for upstream repo
gitcode_list_pull_requests --owner $UPSTREAM_OWNER --repo $UPSTREAM_REPO

# Search for PR with matching branch name and owner name
```

**If PR exists**: Only push to fork and inform user.

```bash
git push -u $FORK_REMOTE <branch-name>
```

**If PR does not exist**: Continue to steps 4-6 to create issue and PR.

### 3. Create Issue

Load issue template and create issue:

1. Read issue template: `references/issue_template.md`
2. Fill in template fields based on context (commit messages, changed files, etc.)
3. Use `gitcode_create_issue` with upstream owner/repo

Note: Use commit message and git diff to generate issue description automatically.

### 4. Push to Fork

Push to your fork (the detected fork remote):

```bash
git push -u $FORK_REMOTE <branch-name>
```

### 5. Create PR from Fork to Upstream

Load PR template from upstream repository and create PR linking to issue:

1. **Get upstream PR template**:
   ```bash
   # Try local copy first
   if [ -f .gitee/PULL_REQUEST_TEMPLATE.zh-CN.md ]; then
     cat .gitee/PULL_REQUEST_TEMPLATE.zh-CN.md
   else
     # Fetch from upstream
     git fetch $UPSTREAM_REMOTE master
     git show $UPSTREAM_REMOTE/master:.gitee/PULL_REQUEST_TEMPLATE.zh-CN.md
   fi
   ```

2. **Fill template**:
   Follow the direction in the template.

3. **Create PR** using `gitcode_create_pull_request`:
   
   **IMPORTANT**: For cross-repo PRs, the `head` parameter format is CRITICAL.
   - Must be exactly: `<fork-owner>:<branch-name>` (no extra prefixes)
   - GitCode API strictly validates this format for cross-fork PRs
   
   Parameters:
   - `owner`: Upstream owner (e.g., `openharmony`)
   - `repo`: Upstream repo (e.g., `security_code_signature`)
   - `title`: Follow commit message format
   - `head`: `<fork-owner>:<branch-name>` (from fork remote parsing)
   - `base`: Target branch on upstream (typically `master` or `main`)
   - `body`: Template content with issue reference

Example:
```bash
# After detection
UPSTREAM_OWNER="openharmony"
UPSTREAM_REPO="security_code_signature"
FORK_OWNER="someone"
FORK_REMOTE="fork"

gitcode_create_pull_request \
  --owner $UPSTREAM_OWNER \
  --repo $UPSTREAM_REPO \
  --title "fix(code_signature): add null check for buffer pointer" \
  --head "$FORK_OWNER:$BRANCH_NAME" \
  --base "master" \
  --body "$(cat .gitee/PULL_REQUEST_TEMPLATE.zh-CN.md | \
    sed 's/^### 关联的issue：$/### 关联的issue：\n#$ISSUE_NUMBER/')"
```

## Templates

### Upstream PR Template

Located at `.gitee/PULL_REQUEST_TEMPLATE.zh-CN.md` in the upstream repository.

### Local Issue Template

See `references/issue_template.md` for standard issue format.

Key sections:
- **问题描述**: What is the problem or feature request?
- **复现步骤**: For bug reports (if applicable)
- **预期行为**: What should happen?
- **实际行为**: What actually happens?
- **环境信息**: Any relevant environment details

## Remote URL Parsing

Parse owner and repo from remote URLs:

```bash
# Function to parse GitCode URL
parse_gitcode_url() {
  local url="$1"
  
  # Remove .git suffix if present
  url=$(echo "$url" | sed 's/\.git$//')
  
  # Extract owner and repo
  if [[ "$url" =~ https://gitcode\.com/([^/]+)/(.+) ]]; then
    echo "${BASH_REMATCH[1]}|${BASH_REMATCH[2]}"
  fi
}

# Usage
result=$(parse_gitcode_url "https://gitcode.com/openharmony/security_code_signature")
owner="${result%%|*}"
repo="${result##*|}"
# owner=openharmony, repo=security_code_signature
```

## Issue Reference in PR Template

In `.gitee/PULL_REQUEST_TEMPLATE.zh-CN.md`, fill in issue reference:

```markdown
### 关联的issue：
#123
```

The PR will auto-close issue #123 when merged.

## GitCode MCP Tools

Use these tools for GitCode operations:

- `gitcode_list_pull_requests` - Check existing PRs (use upstream owner/repo)
- `gitcode_get_pull_request` - Get PR details
- `gitcode_create_pull_request` - Create new PR (head points to fork)
- `gitcode_update_pull_request` - Update existing PR
- `gitcode_create_issue` - Create new issue (use upstream owner/repo)
- `gitcode_get_issue` - Get issue details

## Error Handling

- **Authentication failure**: Check if GitCode token is configured
- **Branch not found on fork**: Push to fork first before creating PR
- **PR already exists**: Inform user and provide link, don't create duplicate
- **No upstream remote**: Ask user to configure upstream remote (owner=openharmony)
- **No fork remote**: Ask user which remote to push to, or if they need to fork first
- **Multiple non-openharmony remotes**: Ask user to select which is their fork
- **PR template not found**: Check if `.gitee/PULL_REQUEST_TEMPLATE.zh-CN.md` exists upstream
- **Owner/repo parsing error**: Validate remote URL format

## Decision Tree

```
User requests PR
  ↓
Check git status
  ↓
Changes uncommitted? → Yes → Commit changes
  ↓ No
List and parse remotes
  ↓
Detect upstream (owner=openharmony) and fork
  ↓
┌─────────────────────────────────────┐
│ Remote detection result:        │
│ - Upstream found?             │
│ - Fork found?                 │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│ Need user input?               │
│ - No fork?                   │
│ - Ambiguous remotes?           │
└─────────────────────────────────────┘
  ↓ Yes → Ask user
  ↓ No
Push to fork
  ↓
List PRs (upstream repo)
  ↓
PR exists for branch? → Yes → Inform user (PR already exists)
  ↓ No
Create issue (upstream repo)
  ↓
Get PR template from upstream (.gitee/PULL_REQUEST_TEMPLATE.zh-CN.md)
  ↓
Create PR (head: fork-owner:branch, base: upstream-branch)
  ↓
Done
```

## Context Gathering

When creating issue or PR, gather from:
- `git log -1` - Last commit message
- `git diff HEAD~1` - Changed files and diff
- Branch name - For feature context
- User input - Additional description if provided
- `git remote -v` - All remotes and their URLs
- Remote parsing - Upstream owner/repo and fork owner/repo
