---
name: merge-pr-check
description: Use this skill when the user asks to merge a PR, check if a PR is ready to merge, "merge PR", "can this PR be merged", "merge-pr-check". Requires Gitee MCP Server to be configured.
version: 1.0.0
requires:
  mcp-servers:
    - gitee
---

> **Note**: If you have `mcporter` installed locally, you should use `mcporter` to invoke the MCP tool instead of directly calling the MCP tool. The `mcporter` CLI provides a more convenient interface and better error handling.

# Merge PR Check via Gitee MCP

Check whether a Pull Request meets the criteria for merging, then execute the merge after confirmation.

## Prerequisites

- Gitee MCP Server configured (tools: `get_pull_detail`, `list_pull_comments`, `get_diff_files`, `merge_pull`)
- User must provide: repository owner, repository name, PR number

## Steps

### Step 1: Fetch PR Status

Use `get_pull_detail` to retrieve PR details and check:

**Basic status**
- Whether the PR is open (stop if already closed/merged)
- Whether it is a Draft — if so, inform the user it must be converted to a regular PR first
- Whether source and target branches are correct

**Pre-merge checklist**
- Whether the PR has a description explaining the purpose of the changes
- Whether a reviewer has been assigned

### Step 2: Analyze Comments and Review Feedback

Use `list_pull_comments` to retrieve all comments and check:
- Whether any reviewer has explicitly objected to merging (e.g., "NACK", "needs changes", "do not merge")
- Whether there are unresolved discussions (questions raised but not replied to)
- Whether there are any LGTM or Approved responses

### Step 3: Quick Diff Check

Use `get_diff_files` to inspect changed files:
- Whether there are obvious omissions (e.g., code changed but related config not updated)
- Whether unexpected files are included (debug code, temp files)
- Whether the scope of changes matches the PR description

### Step 4: Provide Merge Recommendation

Based on the checks above, output a merge assessment report:

```
## PR Merge Check Report

**PR**: #[number] [title]
**Status**: [Open/Draft/Closed]

### Checklist

✅ PR is in Open state
✅ Has a change description
⚠️  No reviewer approval yet
✅ Diff scope is reasonable

### Conclusion

[Ready to merge / Recommend waiting for review / Not recommended to merge]

Reason: [Specific explanation]
```

### Step 5: Execute Merge (requires user confirmation)

If the checks pass, ask the user to confirm the merge.

After confirmation, use `merge_pull` with these parameters:
- `merge_method`: merge strategy — `merge` (creates a merge commit), `squash` (squashes commits), or `rebase`
  - Default recommendation: `merge`; suggest `squash` if the PR has many messy commits
- `commit_message`: merge commit message (optional, defaults to PR title)

After a successful merge, output the result and ask whether the user wants to delete the source branch.

## Notes

- Merging is irreversible — always wait for explicit user confirmation before proceeding
- If there are conflicts, the Gitee API will return an error — prompt the user to resolve conflicts first
- It is recommended to confirm that CI has passed before merging (check the PR's status checks)
