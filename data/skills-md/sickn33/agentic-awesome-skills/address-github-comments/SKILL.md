---
name: address-github-comments
description: "Use when you need to address review or issue comments on an open GitHub Pull Request using the gh CLI."
risk: critical
source: community
date_added: "2026-02-27"
---

# Address GitHub Comments

## Overview

Efficiently address PR review comments or issue feedback using the GitHub CLI (`gh`). This skill ensures all feedback is addressed systematically.

## Prerequisites

Ensure `gh` is authenticated.

```bash
gh auth status
```

If not logged in, run `gh auth login`.

## Workflow

### 1. Inspect Comments

Fetch the comments for the current branch's PR.

```bash
gh pr view --comments
```

`--comments` shows conversation comments; it does not enumerate every inline review thread.
Use the available GitHub connector or the GraphQL `pullRequest.reviewThreads` connection
with pagination to inspect inline comments, file/line anchors, and resolution state.
Record the repository, PR number, current head SHA, thread IDs, and requested changes.

### 2. Categorize and Plan

- List the comments and review threads.
- Propose a fix for each.
- Address feedback already covered by the user's requested scope. Ask only when feedback conflicts, expands scope, or requires a consequential choice.

### 3. Apply Fixes

Read the surrounding implementation, preserve unrelated edits, and apply the changes for the selected comments. Run the relevant repository checks and bind the result to the updated head before reporting a fix.

### 4. Respond to Comments

When the user authorizes posting replies, respond with the commit and verification evidence.
A conversation comment does not resolve an inline review thread. Resolve the specific thread
through the supported GitHub API only after its request is actually addressed and resolution
is authorized; otherwise leave a proposed reply for the user.

```bash
gh pr comment <PR_NUMBER> --body "Addressed in <commit SHA>; verified with <check and result>."
```

## Common Mistakes

- **Applying fixes without understanding context**: Always read the surrounding code of a comment.
- **Not verifying auth**: Check `gh auth status` before starting.

## When to Use
Use when an existing PR has review threads or issue comments that require a scoped code repair and an evidence-backed response.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
