---
name: close-issue-flow
description: Use this skill when the user asks to close an issue, wrap up an issue, "close issue", "close-issue-flow", or finish up after a fix has been merged. Requires Gitee MCP Server to be configured.
version: 1.0.0
requires:
  mcp-servers:
    - gitee
---

> **Note**: If you have `mcporter` installed locally, you should use `mcporter` to invoke the MCP tool instead of directly calling the MCP tool. The `mcporter` CLI provides a more convenient interface and better error handling.

# Close Issue Flow via Gitee MCP

Execute the complete Issue closing workflow: verify the fix is merged → post a closing comment → update the Issue status.

## Prerequisites

- Gitee MCP Server configured (tools: `get_repo_issue_detail`, `list_repo_pulls`, `comment_issue`, `update_issue`)
- User must provide: repository owner, repository name, Issue number
- Typically run after the related PR has been merged or the problem has been resolved

## Steps

### Step 1: Fetch Issue Details

Use `get_repo_issue_detail` to retrieve Issue information:
- Title, description, labels
- Current state (check if it's already closed)
- Existing comments (to understand how it was resolved)

If the Issue is already closed, notify the user and stop.

### Step 2: Confirm Linked PR Status

Use `list_repo_pulls` to query the repository's PRs, filtering for:
- State: `merged`
- Description containing `closes #[issue number]` or `fixes #[issue number]`

Based on the results:
- If a merged linked PR is found → confirm the fix is live
- If the related PR is still open → notify the user that the PR has not been merged yet
- If no linked PR exists → ask the user how the Issue was resolved

### Step 3: Post Closing Comment

Use `comment_issue` to post a closing note. Choose the appropriate template:

**When a linked PR was merged:**
```
This issue has been fixed and merged via PR #[number].

**Fix summary**: [brief description of the fix]

Thanks for the report! If the problem persists, feel free to reopen this issue or submit a new one.
```

**When resolved directly (no PR):**
```
This issue has been resolved.

**Solution**: [description of how it was resolved]

If the problem persists, feel free to reopen this issue or submit a new one.
```

**When unable to reproduce or request was declined:**
```
[Explanation, e.g., "Unable to reproduce this issue" or "After discussion, we've decided not to implement this feature at this time."]

If you have new information, feel free to reopen the issue with additional details.
```

### Step 4: Close the Issue

Use `update_issue` to update the Issue state:
- `state`: `closed`

Optionally:
- Update labels (e.g., add `fixed` or `resolved`)
- Assign to a milestone (add to a completed milestone)

### Step 5: Output Summary

```
## Issue Closed

- Issue: #[number] [title]
- Reason: [Fixed / Cannot reproduce / Declined]
- Linked PR: #[number] (if any)
- Closing comment posted ✅
- Issue status updated to closed ✅
```

## Notes

- Always confirm the issue is genuinely resolved before closing, to avoid premature closure
- When closing a bug reported by a user, thank them for the report
- When declining a feature request, explain the reason and close politely
- Using `closes #N` in a PR description will auto-close the Issue on merge — this skill is for cases where manual closure or an explanatory comment is needed
