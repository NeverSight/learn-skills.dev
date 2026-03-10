---
name: triage-issues
description: Use this skill when the user asks to triage issues, organize the issue list, "triage issues", "show me all open issues", "categorize issues", "triage-issues". Requires Gitee MCP Server to be configured.
version: 1.0.1
requires:
  mcp-servers:
    - gitee
---

> **Note**: If you have `mcporter` installed locally, you should use `mcporter` to invoke the MCP tool instead of directly calling the MCP tool. The `mcporter` CLI provides a more convenient interface and better error handling.

# Triage Issues via Gitee MCP

Batch-process a repository's Issues: classify by priority, add labels, identify duplicates, and generate a clear action list.

## Prerequisites

- Gitee MCP Server configured (tools: `list_repo_issues`, `get_repo_issue_detail`, `update_issue`, `comment_issue`)
- User must provide: repository owner, repository name
- Optional: filter criteria (bugs only / unassigned only / specific milestone, etc.)

## Steps

### Step 1: Fetch the Issue List

Use `list_repo_issues` to retrieve open Issues:
- `state`: `open` (open Issues only)
- Paginate if there are many Issues (20 per page)

### Step 2: Batch Analysis

For each Issue, quickly evaluate:

**Type classification (use labels)**
| Type | Label | Description |
|------|-------|-------------|
| Bug | `bug` | something is broken, throwing errors, or crashing |
| Feature | `feature` | request for new functionality |
| Enhancement | `enhancement` | improvement to existing functionality |
| Question | `question` | usage question |
| Documentation | `docs` | documentation-related |
| Duplicate | `duplicate` | same as an existing Issue |

**Common additional labels**
| Label | Use Case |
|-------|----------|
| `help wanted` | Needs external contribution |
| `wontfix` | Will not be addressed |
| `invalid` | Invalid or spam |
| `security` | Security-related |
| `performance` | Performance-related |
| `ui/ux` | User interface improvements |
| `backend` | Backend-related |
| `frontend` | Frontend-related |

**Priority assessment**
- `P0 - Critical`: affects core functionality, production bug, security vulnerability
- `P1 - High`: significant functional defect, affects many users
- `P2 - Medium`: general improvement, workaround exists
- `P3 - Low`: nice-to-have, cosmetic improvement

**Status assessment**
- Whether there are sufficient reproduction steps (for bugs)
- Whether more information is needed
- Whether a PR is already addressing it

### Step 3: Generate Triage Report

Output a structured report:

```
## Issue Triage Report
Repository: [owner/repo]
Date: [date]
Total open issues: [N]

---

### 🔴 P0 Critical (needs immediate attention)
| # | Title | Type | Labels | Note |
|---|-------|------|--------|------|
| #N | [title] | bug | bug, security | [one sentence explaining urgency] |

### 🟠 P1 High Priority
| # | Title | Type | Labels | Note |
|---|-------|------|--------|------|

### 🟡 P2 Medium Priority
| # | Title | Type | Labels | Note |
|---|-------|------|--------|------|

### 🟢 P3 Low Priority
| # | Title | Type | Labels | Note |
|---|-------|------|--------|------|

---

### Needs More Information
- #N [title]: [what information is missing]

### Possible Duplicates
- #N may be a duplicate of #M: [explanation]

### Recommended for Closure
- #N [title]: [reason, e.g., long inactive / already resolved another way]
```

### Step 4: Update Issue Labels (requires user confirmation)

Ask the user whether to automatically update labels and priorities.

After confirmation, use `update_issue` to:
- Add type labels (`bug`, `feature`, `enhancement`, `question`, `docs`, `duplicate`)
- Add additional labels based on context (`help wanted`, `security`, etc.)
- Add priority indicator (if supported by the repository)

**Label assignment examples:**
- A bug report → add `bug` label
- A feature request with good description → add `feature` label
- An enhancement suggestion → add `enhancement` label
- A simple question → add `question` label
- Needs external help → add `help wanted`

For Issues that need more information, use `comment_issue` to ask:

```
Thanks for submitting this issue!

To help us address it more effectively, could you please provide:
- [Missing reproduction steps]
- [Environment and version info]
- [Expected behavior vs. actual behavior]

Thank you!
```

## Notes

- Triage focuses on classification and organization — no need to deep-dive into technical details of each Issue
- Always confirm with the user before performing bulk updates to avoid unintended changes
- If there are more than 50 Issues, consider processing in batches or filtering by a specific label
- Use consistent labels to help contributors find Issues matching their interests
- Check existing labels in the repository first — some projects may have custom label names
