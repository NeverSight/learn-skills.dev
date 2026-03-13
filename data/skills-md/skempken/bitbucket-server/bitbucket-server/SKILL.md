---
name: bitbucket-server
description: This skill enables interaction with BitBucket Server REST API for Pull Request management. Use when the user wants to create, review, comment on, merge, list pull requests, read comments, or manage tasks on BitBucket Server.
---

# BitBucket Server

This skill provides tools for interacting with BitBucket Server's REST API, focusing on Pull Request management workflows.

## Prerequisites

The following environment variables must be set:

- `BITBUCKET_URL` - Base URL of the BitBucket Server instance (e.g., `https://bitbucket.example.com`)
- `BITBUCKET_USER` - Username for authentication
- `BITBUCKET_TOKEN` - Personal access token for authentication

## Available Commands

The `scripts/bitbucket_api.py` script provides a CLI for BitBucket Server operations. Execute it with Python 3:

```bash
python3 scripts/bitbucket_api.py <command> [options]
```

### Pull Request Commands

| Command | Description |
|---------|-------------|
| `list-prs` | List pull requests with optional status filter |
| `get-pr` | Get details of a specific pull request |
| `create-pr` | Create a new pull request |
| `get-diff` | Get the diff of a pull request |
| `approve` | Approve a pull request |
| `merge` | Merge a pull request |
| `decline` | Decline a pull request |

### Comment Commands

| Command | Description |
|---------|-------------|
| `get-comments` | Get all comments and activities on a pull request |
| `add-comment` | Add a general or inline comment to a pull request |
| `reply-comment` | Reply to an existing comment |

### Task Commands

| Command | Description |
|---------|-------------|
| `get-tasks` | List all tasks on a pull request |
| `complete-task` | Mark a single task as completed |
| `complete-tasks` | Mark multiple tasks as completed at once |
| `reopen-task` | Reopen a single completed task |
| `reopen-tasks` | Reopen multiple tasks at once |

## Command Usage Examples

### List Pull Requests

```bash
# List all open PRs in a repository
python3 scripts/bitbucket_api.py list-prs --project MYPROJ --repo my-repo

# List PRs with specific state
python3 scripts/bitbucket_api.py list-prs --project MYPROJ --repo my-repo --state MERGED
```

### Get Pull Request Details

```bash
python3 scripts/bitbucket_api.py get-pr --project MYPROJ --repo my-repo --pr-id 42
```

### Create a Pull Request

```bash
python3 scripts/bitbucket_api.py create-pr \
  --project MYPROJ \
  --repo my-repo \
  --title "Add new feature" \
  --from-branch feature/my-feature \
  --to-branch main \
  --description "Description of changes"
```

### Get Diff

```bash
python3 scripts/bitbucket_api.py get-diff --project MYPROJ --repo my-repo --pr-id 42
```

### Work with Comments

```bash
# Get all comments
python3 scripts/bitbucket_api.py get-comments --project MYPROJ --repo my-repo --pr-id 42

# Add a general comment
python3 scripts/bitbucket_api.py add-comment \
  --project MYPROJ --repo my-repo --pr-id 42 \
  --text "This looks good!"

# Add an inline comment on a specific file and line
python3 scripts/bitbucket_api.py add-comment \
  --project MYPROJ --repo my-repo --pr-id 42 \
  --text "Consider renaming this variable" \
  --file-path src/main.py --line 42 --line-type ADDED

# Reply to a comment
python3 scripts/bitbucket_api.py reply-comment \
  --project MYPROJ --repo my-repo --pr-id 42 \
  --comment-id 123 --text "Fixed!"
```

### Work with Tasks

Tasks in BitBucket Server are comments with BLOCKER severity. They are managed via the Comments API.

```bash
# List all tasks (BLOCKER comments)
python3 scripts/bitbucket_api.py get-tasks --project MYPROJ --repo my-repo --pr-id 42

# Complete a single task
python3 scripts/bitbucket_api.py complete-task --project MYPROJ --repo my-repo --pr-id 42 --comment-id 456

# Complete multiple tasks at once (comma-separated IDs)
python3 scripts/bitbucket_api.py complete-tasks --project MYPROJ --repo my-repo --pr-id 42 --comment-ids 456,789,123

# Reopen a single task
python3 scripts/bitbucket_api.py reopen-task --project MYPROJ --repo my-repo --pr-id 42 --comment-id 456

# Reopen multiple tasks at once
python3 scripts/bitbucket_api.py reopen-tasks --project MYPROJ --repo my-repo --pr-id 42 --comment-ids 456,789
```

### PR Actions

```bash
# Approve a PR
python3 scripts/bitbucket_api.py approve --project MYPROJ --repo my-repo --pr-id 42

# Merge a PR
python3 scripts/bitbucket_api.py merge --project MYPROJ --repo my-repo --pr-id 42

# Decline a PR
python3 scripts/bitbucket_api.py decline --project MYPROJ --repo my-repo --pr-id 42
```

## Workflow Guidelines

### Reviewing a Pull Request

1. Get PR details to understand the context
2. Get the diff to review code changes
3. Get existing comments to see discussion
4. Add comments or inline comments as needed
5. Check and manage tasks if present
6. Approve or request changes

### Creating a Pull Request

1. Ensure the source branch exists and has commits
2. Create the PR with a descriptive title and description
3. The script returns the PR ID and URL on success

### Managing Tasks

Tasks in BitBucket Server are comments with BLOCKER severity. Use `get-tasks` to list all tasks and their status (returns comment IDs), then `complete-task` or `reopen-task` to change their state. The comment ID from `get-tasks` output is used as `--comment-id` for task operations.

## Error Handling

The script outputs JSON for successful operations and error messages for failures. Common errors:

- Missing environment variables: Ensure `BITBUCKET_URL`, `BITBUCKET_USER`, and `BITBUCKET_TOKEN` are set
- Authentication failed: Verify credentials and token permissions
- Resource not found: Check project, repository, and PR ID values

## Additional Reference

For detailed API endpoint documentation, see `references/api_endpoints.md`.
