---
name: zoonk-github-issues
description: "Create and manage GitHub issues with advanced features: issue types, dependencies, and sub-issues. Use this skill after planning issues with zoonk-issue-planning."
license: MIT
metadata:
  author: zoonk
  version: "1.0.0"
---

# GitHub Issues Skill

Create and manage GitHub issues with advanced features: issue types, dependencies, and sub-issues.

For **planning** what issues to create, see [zoonk-issue-planning](./../zoonk-issue-planning/SKILL.md).

## Quick Start

### Create a Basic Issue

```bash
gh issue create --title "Issue title" --body "Description"
```

### Create Issue with Labels

```bash
gh issue create --title "Issue title" --body "Description" \
  --label "main:catalog"
```

### Create Issue from File

```bash
gh issue create --title "Issue title" --body-file ./issue-body.md
```

## Labels

### Always Fetch Labels First

Before creating issues, check available labels to use existing ones or follow patterns for new ones:

```bash
gh label list --repo zoonk/zoonk
```

### Naming Convention

Format: `{prefix}:{feature}`

Prefix groups with consistent colors:

| Prefix       | Color            | Description         |
| ------------ | ---------------- | ------------------- |
| `main:*`     | Blue (#1d76db)   | main app features   |
| `editor:*`   | Purple (#5319e7) | editor app features |
| `packages:*` | Green (#0e8a16)  | packages            |

### When to Create a New Label

Labels typically map to route groups (e.g., `(catalog)`, `(settings)`), but the real question is:

**"Can someone work independently on this feature without causing git conflicts?"**

Guidelines:

- **One label per route group by default** - e.g., `main:settings` covers all settings pages
- **Separate label if truly independent** - e.g., `main:home` is separate from `main:catalog` even though home is within the catalog route group, because they don't share code
- **Keep connected features together** - Course page and lesson page are both `main:catalog` because they're tightly coupled and would cause conflicts

Think of it in terms of teams/squads: if two agents could work on different parts simultaneously without stepping on each other's code, those might be separate labels.

### Creating New Labels

When a new label is needed, use the same color as existing labels in that group:

```bash
gh label create "main:newfeature" --color "1d76db"
gh label create "editor:newfeature" --color "5319e7"
gh label create "packages:newpackage" --color "0e8a16"
```

## Issue Types

Issue types help categorize issues (Epic, Bug, Task, Enhancement, etc.). This requires organization-level issue types to be enabled.

### Get Available Issue Types

```bash
gh api graphql -f query='
  query($owner: String!) {
    organization(login: $owner) {
      issueTypes(first: 20) {
        nodes { id name description }
      }
    }
  }' -f owner='zoonk'
```

### Get Issue Node ID

Required for all GraphQL mutations:

```bash
gh api graphql -f query='
  query($owner: String!, $repo: String!, $number: Int!) {
    repository(owner: $owner, name: $repo) {
      issue(number: $number) { id }
    }
  }' -f owner='zoonk' -f repo='zoonk' -F number=123
```

### Set Issue Type

```bash
gh api graphql -f query='
  mutation($issueId: ID!, $issueTypeId: ID!) {
    updateIssueIssueType(input: {issueId: $issueId, issueTypeId: $issueTypeId}) {
      issue { id title issueType { name } }
    }
  }' -f issueId="ISSUE_NODE_ID" -f issueTypeId="TYPE_NODE_ID"
```

## Dependencies (Blocked-By)

Dependencies track when one issue blocks another. Use the REST API with **database IDs** (integers), not node IDs.

### Get Issue Database ID

The REST API for dependencies requires the integer database ID, not the GraphQL node ID:

```bash
# Get database ID for an issue
gh api repos/zoonk/zoonk/issues/123 --jq '.id'
# Returns something like: 3858025102
```

### Add Dependency (Issue A blocks Issue B)

First get the blocking issue's database ID, then use `-F` (uppercase) to pass it as an integer:

```bash
# Get the blocking issue's database ID
BLOCKING_DB_ID=$(gh api repos/zoonk/zoonk/issues/BLOCKING_NUMBER --jq '.id')

# Add dependency: BLOCKED_NUMBER is blocked by BLOCKING_NUMBER
gh api repos/zoonk/zoonk/issues/BLOCKED_NUMBER/dependencies/blocked_by \
  --method POST \
  -F issue_id=$BLOCKING_DB_ID
```

**Important**: Use `-F` (uppercase) not `-f` (lowercase). The `-F` flag passes the value as a raw integer, while `-f` passes it as a string which will cause a 422 error.

### Verify Dependencies

```bash
gh api repos/zoonk/zoonk/issues/ISSUE_NUMBER --jq '.issue_dependencies_summary'
# Returns: {"blocked_by":1,"blocking":0,"total_blocked_by":1,"total_blocking":0}
```

### Remove Dependency

```bash
gh api repos/zoonk/zoonk/issues/BLOCKED_NUMBER/dependencies/blocked_by/BLOCKING_DB_ID \
  --method DELETE
```

## Sub-Issues

Sub-issues create parent-child relationships, useful for breaking down epics.

### Add Sub-Issue

```bash
gh api graphql -f query='
  mutation($parentId: ID!, $childId: ID!) {
    addSubIssue(input: {issueId: $parentId, subIssueId: $childId}) {
      issue { title }
      subIssue { title }
    }
  }' -f parentId="PARENT_NODE_ID" -f childId="CHILD_NODE_ID"
```

### Remove Sub-Issue

```bash
gh api graphql -f query='
  mutation($parentId: ID!, $childId: ID!) {
    removeSubIssue(input: {issueId: $parentId, subIssueId: $childId}) {
      issue { title }
      subIssue { title }
    }
  }' -f parentId="PARENT_NODE_ID" -f childId="CHILD_NODE_ID"
```

### List Sub-Issues

```bash
gh api graphql -f query='
  query($owner: String!, $repo: String!, $number: Int!) {
    repository(owner: $owner, name: $repo) {
      issue(number: $number) {
        subIssues(first: 50) {
          nodes { number title state }
        }
      }
    }
  }' -f owner='zoonk' -f repo='zoonk' -F number=123
```

## Common Workflows

### Zoonk Feature Development Pattern

When developing a new feature at Zoonk, follow this pattern:

1. **Create an Epic issue** for the feature (use the `Epic` issue type)
2. **Create Task issues** for each implementation step
3. **Link tasks as sub-issues** of the epic
4. **Set dependencies** between tasks that have ordering requirements

Example workflow:

```bash
# 1. Create the epic
EPIC_URL=$(gh issue create --title "Feature: User Notifications" \
  --body "Implement notification system for users" \
  --label "main:notifications")
EPIC_NUM=$(echo $EPIC_URL | grep -oE '[0-9]+$')

# 2. Get epic's node ID
EPIC_ID=$(gh api graphql -f query='
  query($owner: String!, $repo: String!, $number: Int!) {
    repository(owner: $owner, name: $repo) {
      issue(number: $number) { id }
    }
  }' -f owner='zoonk' -f repo='zoonk' -F number=$EPIC_NUM \
  --jq '.data.repository.issue.id')

# 3. Create sub-tasks
TASK1_URL=$(gh issue create --title "Add notifications table" \
  --body "Create Prisma schema for notifications")
TASK1_NUM=$(echo $TASK1_URL | grep -oE '[0-9]+$')

TASK2_URL=$(gh issue create --title "Add notification API endpoints" \
  --body "Create API routes for notification CRUD")
TASK2_NUM=$(echo $TASK2_URL | grep -oE '[0-9]+$')

# 4. Get task node IDs
TASK1_ID=$(gh api graphql -f query='
  query($owner: String!, $repo: String!, $number: Int!) {
    repository(owner: $owner, name: $repo) {
      issue(number: $number) { id }
    }
  }' -f owner='zoonk' -f repo='zoonk' -F number=$TASK1_NUM \
  --jq '.data.repository.issue.id')

TASK2_ID=$(gh api graphql -f query='
  query($owner: String!, $repo: String!, $number: Int!) {
    repository(owner: $owner, name: $repo) {
      issue(number: $number) { id }
    }
  }' -f owner='zoonk' -f repo='zoonk' -F number=$TASK2_NUM \
  --jq '.data.repository.issue.id')

# 5. Link as sub-issues
gh api graphql -f query='
  mutation($parentId: ID!, $childId: ID!) {
    addSubIssue(input: {issueId: $parentId, subIssueId: $childId}) {
      issue { title }
    }
  }' -f parentId="$EPIC_ID" -f childId="$TASK1_ID"

gh api graphql -f query='
  mutation($parentId: ID!, $childId: ID!) {
    addSubIssue(input: {issueId: $parentId, subIssueId: $childId}) {
      issue { title }
    }
  }' -f parentId="$EPIC_ID" -f childId="$TASK2_ID"

# 6. Add dependency (Task 2 blocked by Task 1)
# Note: Dependencies use database ID (integer), not node ID
TASK1_DB_ID=$(gh api repos/zoonk/zoonk/issues/$TASK1_NUM --jq '.id')
gh api repos/zoonk/zoonk/issues/$TASK2_NUM/dependencies/blocked_by \
  --method POST -F issue_id=$TASK1_DB_ID
```

### Get Issue Node ID Helper

Use this frequently, so here's a compact version:

```bash
get_issue_id() {
  gh api graphql -f query='
    query($owner: String!, $repo: String!, $number: Int!) {
      repository(owner: $owner, name: $repo) {
        issue(number: $number) { id }
      }
    }' -f owner='zoonk' -f repo='zoonk' -F number=$1 \
    --jq '.data.repository.issue.id'
}

# Usage: get_issue_id 123
```

## Quick Reference

| Action            | Command                                                           |
| ----------------- | ----------------------------------------------------------------- |
| Create issue      | `gh issue create --title "..." --body "..."`                      |
| Get issue node ID | `gh api graphql ... -F number=N --jq '.data.repository.issue.id'` |
| List issue types  | `gh api graphql ... organization(login: ...) { issueTypes ... }`  |
| Set issue type    | `gh api graphql ... updateIssueIssueType(input: ...)`             |
| Add dependency    | `gh api repos/.../issues/N/dependencies/blocked_by --method POST` |
| Add sub-issue     | `gh api graphql ... addSubIssue(input: ...)`                      |
| List sub-issues   | `gh api graphql ... issue(number: N) { subIssues ... }`           |

## Common Mistakes

- Use GitHub sub-issues feature, which automatically lists sub-issues, no need to list all sub-issues manually in the issue body
- Similarly, when we add issue dependencies, it automatically adds that dependency to the UI, so you don't need to add `Parent: #ISSUE_NUMBER` - GitHub already does that when you add the relationship
- Plus, you shouldn't add references to our temporary files to the GitHub issue body like this: `specs, see /tasks/specs/whatever`. Instead write the full spec to the issue body
- When you have multiple issues to add, you may want to create a temporary bash script to process them in batch instead of running each command individually

### Never Trust #NUMBER References from Specs

When creating issues from specs:

1. **Spec numbers are NOT GitHub issue numbers** - A spec named `18-get-org-courses.md` does NOT correspond to GitHub issue #18

2. **Handle #NUMBER references carefully**:
   - Remove "Blocked by: #X" lines entirely (use GitHub API instead)
   - For context references like "Out of scope, see #X":
     - If creating issues fresh: don't keep those spec references in the issue body, those are our internal spec numbers
     - If issue already exists: verify the GitHub issue number is correct first

3. **Build a mapping as you create issues**:
   - Track: Spec filename → GitHub issue number
   - Use this mapping to fix cross-references in issue bodies

4. **Cross-references ARE okay** when they're verified GitHub issues:
   - GOOD: "Out of scope, handled by #1234" (verified this is a real issue)
   - BAD: "See #18 for details" (spec number, not verified)

### Content That Should NOT Be in Issue Bodies

Remove before creating (GitHub handles these automatically):

- `**Blocked by**: #X` - Use GitHub blocked-by relationship
- `**Type**: Feature` - Use GitHub issue type
- Summary tables listing sub-issues - Use GitHub sub-issue feature
- Numbered lists of child issues - Use GitHub sub-issue feature
- `Parent: #X` - GitHub shows parent automatically
- Don't add any metadata that GitHub manages or displays in the UI already, focus only on the task

## Troubleshooting

### "Resource not accessible by integration"

- Ensure you have write access to the repository
- Check that GitHub Issues is enabled for the repo
- Verify your `gh` CLI is authenticated: `gh auth status`

### "Issue type not found"

- Issue types must be enabled at the organization level
- Verify available types with the "Get Available Issue Types" query
- Ensure you're using the node ID, not the type name

### "Cannot add sub-issue"

- Both issues must be in the same repository
- The child issue cannot already have a parent
- Circular references are not allowed

### "GraphQL node ID invalid"

- Node IDs are base64-encoded and version-specific
- Always fetch fresh node IDs before mutations
- Don't cache node IDs across sessions

### "Invalid property /issue_id: is not of type integer" (HTTP 422)

- The REST API for dependencies requires the **database ID** (integer), not the GraphQL node ID
- Use `-F` (uppercase) to pass integers: `-F issue_id=$DB_ID`
- Don't use `-f` (lowercase) which passes strings: `-f issue_id="..."` will fail
- Get database ID with: `gh api repos/zoonk/zoonk/issues/NUMBER --jq '.id'`
