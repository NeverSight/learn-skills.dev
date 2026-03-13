---
name: pr-sweep
description: >-
  This skill should be used when the user asks to "sweep PR comments",
  "check PR feedback", "handle review comments", "auto-resolve comments",
  "address PR reviews", "fix PR comments", "resolve review threads",
  "go through PR feedback", "clear PR reviews", or wants to triage and
  resolve GitHub pull request review comments.
version: 0.1.0
allowed_tools:
  - Bash(gh pr view:*)
  - Bash(gh api:*)
  - Bash(gh repo view:*)
  - Bash(git diff:*)
  - Bash(jq:*)
  - Read
  - Grep
  - Glob
  - Task
  - TaskCreate
  - TaskList
  - TaskGet
  - TaskUpdate
---

# PR Sweep

Triage unresolved GitHub PR review threads: auto-resolve comments already addressed by current code, reply with context, and create actionable tasks for remaining items.

## Prerequisites

Verify before starting:

1. A PR exists for the current branch
2. The `gh` CLI is authenticated

```bash
gh pr view --json number,url,title,baseRefName,headRefName 2>/dev/null || echo "NO_PR"
```

If no PR exists, report this and stop.

## Workflow

### Step 1 - Gather Context

Collect repository and PR metadata:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
gh pr view --json number,url,title,baseRefName,headRefName
```

Extract `owner`, `repo`, and `pr_number` from the output.

### Step 2 - Fetch Unresolved Review Threads

Run this GraphQL query and pipe through `jq` to return only the fields needed for triage — keeps response lean and avoids flooding context with metadata:

```bash
gh api graphql -F owner='OWNER' -F repo='REPO' -F pr=PR_NUMBER \
  -f query="$(cat << 'GRAPHQL'
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          path
          line
          comments(first: 1) {
            nodes {
              body
              author { login }
            }
          }
        }
      }
    }
  }
}
GRAPHQL
)" | jq '[.data.repository.pullRequest.reviewThreads.nodes[]
  | select(.isResolved == false)
  | {id, path, line, author: .comments.nodes[0].author.login, comment: .comments.nodes[0].body}]'
```

The result is a compact array — one object per unresolved thread with only `id`, `path`, `line`, `author`, and `comment`.

### Step 3 - Analyze Each Unresolved Thread

For each unresolved thread:

1. **Read the file** at `path` with context around `line`
2. **Check staged/unstaged changes** for the file: `git diff <baseRefName>...HEAD -- <path>` (where `baseRefName` is from Step 1) and `git diff --cached <path>`
3. **Determine if addressed** by checking whether:
   - Current code implements the suggested fix
   - Code was refactored in a way that makes the suggestion moot
   - Style, naming, or structural issues are now corrected
   - Missing tests or documentation were added

Resolution criteria: only mark as addressed when the feedback is **fully** resolved. When in doubt, leave unresolved and add to the task list.

### Step 4 - Resolve Addressed Comments

For each comment determined to be addressed:

1. **Reply** to the thread explaining what was done:

```bash
gh api graphql \
  -f query="$(cat << 'GRAPHQL'
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {
    pullRequestReviewThreadId: $threadId,
    body: $body
  }) {
    comment { id }
  }
}
GRAPHQL
)" -F threadId='THREAD_NODE_ID' -F body='REPLY_BODY' \
  | jq -r '.data.addPullRequestReviewThreadReply.comment.id'
```

2. **Resolve** the thread:

```bash
gh api graphql \
  -f query="$(cat << 'GRAPHQL'
mutation($threadId: ID!) {
  resolveReviewThread(input: { threadId: $threadId }) {
    thread { isResolved }
  }
}
GRAPHQL
)" -F threadId='THREAD_ID' \
  | jq -r '.data.resolveReviewThread.thread.isResolved'
```

Keep replies concise - one or two sentences explaining the fix.

### Step 5 - Plan Remaining Comments

For comments still needing work:

1. Group by file
2. Create a task per unresolved item using TaskCreate
3. Include the comment text, author, file path, and line number in the task description
4. Add a suggested implementation approach based on the comment feedback and current code structure

### Output Format

```
## Auto-Resolved Comments (X)

### [file:line] - Thread ID
**Comment:** <summary>
**Reply:** <what was posted>
**Resolved because:** <reasoning>

---

## Remaining Comments (Y)

### [file:line] - Thread ID
**Comment:** <full comment text>
**Author:** <username>
**Suggested fix:** <implementation suggestion>

---

## Created Tasks
<task list summary>
```

## Important Notes

- Only resolve comments where the feedback is fully addressed
- Always reply before resolving so reviewers see the context
- For comments about missing tests or documentation, verify those were actually added
- For refactoring suggestions, confirm the new code achieves the same goal
- Batch-resolve carefully: a false positive erodes reviewer trust
