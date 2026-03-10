---
name: implement-issue
description: Use this skill when the user asks to implement an issue, "work on this issue", "implement issue", "develop based on an issue", "implement-issue". Requires Gitee MCP Server to be configured.
version: 1.0.0
requires:
  mcp-servers:
    - gitee
---

> **Note**: If you have `mcporter` installed locally, you should use `mcporter` to invoke the MCP tool instead of directly calling the MCP tool. The `mcporter` CLI provides a more convenient interface and better error handling.

# Implement Issue via Gitee MCP

Complete the full development loop starting from a Gitee Issue: requirements analysis → coding → creating a PR → linking back to the Issue.

## Prerequisites

- Gitee MCP Server configured (tools: `get_repo_issue_detail`, `list_repo_issues`, `create_pull`, `comment_issue`, `update_issue`)
- User must provide: repository owner, repository name, Issue number (or select from a list)
- **Local repository path**: This skill must be executed in the local checkout of the issue's repository, OR the user must provide the local path to the repository clone. This is required for the Coding Agent to read and modify source files.

## Steps

### Step 1: Fetch Issue Details

Use `get_repo_issue_detail` to retrieve full Issue information:
- Title and full description
- Labels (feature / bug / enhancement, etc.)
- Priority and milestone
- Existing comments (to understand discussion context)

Also use `list_issue_comments` to review comments and check:
- Existing technical design discussions
- Relevant background context
- Whether someone else is already working on it

### Step 2: Requirements Analysis

Based on the Issue content, produce a requirements analysis:

```
## Requirements Analysis: [Issue title]

**Type**: [Feature / Bug Fix / Performance / Other]

**Goal**:
[One sentence describing what needs to be implemented]

**Scope** (estimated):
- [Modules / files likely involved]
- [APIs / database tables likely involved]

**Implementation Plan**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Potential Risks**:
- [Things to watch out for]

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

### Step 3: Assist with Implementation

Based on the requirements analysis, help the user by:
- Providing concrete code implementation approaches
- Giving code examples for key logic
- Pointing out which files need to be modified

If the user has already finished coding, proceed to the next step.

### Step 4: Record Progress in the Issue

Use `comment_issue` to post a progress update on the Issue:

```
Starting work on this issue. Expected changes:
- [Main change 1]

Implementation approach:
[Brief summary]
```

This keeps other contributors informed and avoids duplicated effort.

### Step 5: Create a Linked PR

Use `create_pull` to create a PR. The PR description should include:
- Summary of changes
- Implementation approach overview
- Testing notes
- `closes #[issue number]` (to auto-close the linked Issue on merge)

### Step 6: Update the Issue

After the PR is created:
1. Use `comment_issue` to post the PR link on the Issue
2. If the Issue status needs updating, use `update_issue` to change it

Comment template:
```
PR #[PR number] has been created to address this issue.
Please review: [PR link]
```

## Notes

- Before starting, confirm the Issue has not been claimed by someone else (check assignees)
- For significant design decisions, discuss and confirm in the Issue comments before coding
- The `closes #N` syntax in the PR description will automatically close the Issue when the PR is merged
