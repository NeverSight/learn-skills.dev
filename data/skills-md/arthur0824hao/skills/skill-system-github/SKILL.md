---
name: skill-system-github
description: "GitHub operations skill for gh CLI issue, label, template, and workflow management. Use when requests include: create issue, list issues, apply label, manage templates, check workflow, or gh operations."
license: MIT
metadata:
  os: linux, macos, windows
---

# Skill System GitHub

Run consistent GitHub operations through `gh` with explicit safety checks for workflow writes and predictable return shapes.

## Decision Matrix

| Task Intent | Operation | Primary Backend | Notes |
|---|---|---|---|
| Create/list/comment/close/reopen issues | `manage-issues` | `gh issue` | Check duplicates before creating new issues |
| Create/update/delete labels, apply labels to issue | `manage-labels` | `gh label`, `gh issue edit` | Confirm destructive delete before execution |
| Bootstrap/update issue templates | `manage-templates` | file read/write tools | Edit `.github/ISSUE_TEMPLATE/*` directly |
| List/check/create/update workflows | `manage-workflows` | `gh workflow`, file read/write tools | Run `safety-check` before pushing workflow changes |
| Decide workflow push path based on token scope | `safety-check` | `gh auth status`, `gh api` | Use API fallback when `workflow` scope is missing |

## Core Patterns

### Pattern 1: Resolve repository and perform issue operation

```bash
gh issue list --repo <owner/repo> --state open --limit 50
gh issue create --repo <owner/repo> --title "<title>" --body "<body>"
```

### Pattern 2: Label lifecycle and issue label application

```bash
gh label create "<name>" --repo <owner/repo> --description "<desc>" --color "<hex>"
gh label edit "<name>" --repo <owner/repo> --new-name "<new>" --description "<desc>" --color "<hex>"
gh issue edit --repo <owner/repo> <number> --add-label "<label1>,<label2>"
```

### Pattern 3: Workflow visibility and recent run checks

```bash
gh workflow list --repo <owner/repo>
gh run list --repo <owner/repo> --workflow "<name>" --limit 5
```

### Pattern 4: Workflow scope gate before writing `.github/workflows/*`

```bash
gh auth status
gh api repos/<owner>/<repo>/contents/.github/workflows/<file> \
  --method PUT \
  -f message="update workflow via api" \
  -f content="<base64-content>" \
  -f branch="<branch>"
```

## Guidelines

- Always resolve `owner/repo` first; infer from `git remote get-url origin` when not provided.
- Always check duplicate issue titles before issue creation.
- Always ask for explicit confirmation before label deletion.
- Always run `safety-check` before workflow writes that require push permissions.
- Always use file tools for `.github/ISSUE_TEMPLATE/*` and `.github/workflows/*` edits.
- Never include secrets in issue/comment/template/workflow bodies.
- Return structured output with `status`, `url`, and `error` fields for all operations.

```skill-manifest
{
  "schema_version": "2.0",
  "id": "skill-system-github",
  "version": "1.0.0",
  "capabilities": ["github-issue", "github-label", "github-template", "github-workflow", "github-safety"],
  "effects": ["net.fetch", "proc.exec", "git.read", "fs.read", "fs.write"],
  "operations": {
    "manage-issues": {
      "description": "Create, list, comment on, close, or reopen GitHub issues with duplicate detection before create.",
      "input": {
        "action": { "type": "string", "required": true, "description": "One of: create, list, comment, close, reopen" },
        "repo": { "type": "string", "required": false, "description": "Target repo in owner/repo format" },
        "title": { "type": "string", "required": false, "description": "Issue title for create" },
        "body": { "type": "string", "required": false, "description": "Issue body for create or comment body" },
        "number": { "type": "number", "required": false, "description": "Issue number for comment/close/reopen" },
        "state": { "type": "string", "required": false, "description": "Issue listing state: open, closed, all" },
        "limit": { "type": "number", "required": false, "description": "List limit" },
        "label": { "type": "string", "required": false, "description": "Optional label filter for listing" }
      },
      "output": {
        "description": "Operation status and issue URL when applicable.",
        "fields": { "status": "string", "url": "string", "error": "string" }
      },
      "entrypoints": {
        "agent": "scripts/manage-issues.md"
      }
    },
    "manage-labels": {
      "description": "Create, update, delete labels, and apply labels to issues in a GitHub repository.",
      "input": {
        "action": { "type": "string", "required": true, "description": "One of: create, update, delete, apply" },
        "repo": { "type": "string", "required": false, "description": "Target repo in owner/repo format" },
        "name": { "type": "string", "required": false, "description": "Label name for create/update/delete" },
        "new_name": { "type": "string", "required": false, "description": "New label name for update" },
        "description": { "type": "string", "required": false, "description": "Label description for create/update" },
        "color": { "type": "string", "required": false, "description": "Hex color without #, for create/update" },
        "number": { "type": "number", "required": false, "description": "Issue number for apply" },
        "labels": { "type": "string", "required": false, "description": "Comma-separated labels for apply" },
        "confirm_delete": { "type": "boolean", "required": false, "description": "Explicit confirmation for delete" }
      },
      "output": {
        "description": "Operation status and optional resource URL.",
        "fields": { "status": "string", "url": "string", "error": "string" }
      },
      "entrypoints": {
        "agent": "scripts/manage-labels.md"
      }
    },
    "manage-templates": {
      "description": "Bootstrap and update repository issue templates under .github/ISSUE_TEMPLATE.",
      "input": {
        "action": { "type": "string", "required": true, "description": "One of: bootstrap, update" },
        "repo": { "type": "string", "required": false, "description": "Target repo in owner/repo format" },
        "template_type": { "type": "string", "required": false, "description": "Template selector: bug_report, feature_request, config" },
        "content": { "type": "string", "required": false, "description": "Updated YAML content for update action" }
      },
      "output": {
        "description": "Operation status and changed path details.",
        "fields": { "status": "string", "url": "string", "error": "string" }
      },
      "entrypoints": {
        "agent": "scripts/manage-templates.md"
      }
    },
    "manage-workflows": {
      "description": "List or check workflow runs and create/update workflow YAML files safely.",
      "input": {
        "action": { "type": "string", "required": true, "description": "One of: list, check, create, update" },
        "repo": { "type": "string", "required": false, "description": "Target repo in owner/repo format" },
        "workflow_name": { "type": "string", "required": false, "description": "Workflow display name or filename for check/update" },
        "workflow_file": { "type": "string", "required": false, "description": "Workflow filename under .github/workflows" },
        "content": { "type": "string", "required": false, "description": "Workflow YAML content for create/update" },
        "branch": { "type": "string", "required": false, "description": "Branch for API fallback updates" }
      },
      "output": {
        "description": "Operation status and workflow URL when available.",
        "fields": { "status": "string", "url": "string", "error": "string" }
      },
      "entrypoints": {
        "agent": "scripts/manage-workflows.md"
      }
    },
    "safety-check": {
      "description": "Check gh auth token scopes for workflow writes and choose push or gh api fallback path.",
      "input": {
        "repo": { "type": "string", "required": false, "description": "Target repo in owner/repo format" },
        "workflow_file": { "type": "string", "required": false, "description": "Workflow filename to write under .github/workflows" },
        "workflow_content": { "type": "string", "required": false, "description": "Workflow YAML content used for API fallback" },
        "branch": { "type": "string", "required": false, "description": "Target branch name" },
        "commit_message": { "type": "string", "required": false, "description": "Commit message for API fallback" }
      },
      "output": {
        "description": "Decision and recommended write path.",
        "fields": { "status": "string", "url": "string", "error": "string" }
      },
      "entrypoints": {
        "agent": "scripts/safety-check.md"
      }
    }
  },
  "stdout_contract": {
    "last_line_json": false,
    "note": "Agent-executed operations; procedures are defined in markdown entrypoint scripts."
  }
}
```
