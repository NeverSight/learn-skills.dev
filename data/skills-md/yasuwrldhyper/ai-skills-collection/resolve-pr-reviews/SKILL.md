---
name: resolve-pr-reviews
description: PRの未解決レビューコメントを取得し、修正を実装してリプライ・スレッド解決・pushまで自動化する。レビューラリー（再レビュー後の新コメント）にも対応。
argument-hint: "[PR#]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# /resolve-pr-reviews Skill

Fetch unresolved PR review threads, implement fixes, reply to each thread, resolve them, and push.
Handles review rallies (new comments appearing after re-review) with up to 3 iteration loops.

**Model Selection Policy:**
- Code fix implementation uses the **default model** (current session). Do NOT specify `--model` or override.
- Opus-class / expensive reasoning models are **prohibited** — review fixes are small, targeted changes.
- If a comment requires complex architectural changes, **skip it** and reply asking for further discussion.

---

## Phase 1: Detect PR and Validate

### 1-1. Resolve PR number

If `$ARGUMENTS` is provided and is a number, use it as the PR number.

Otherwise, detect from the current branch:

```bash
gh pr view --json number,state,headRefName,baseRefName,title
```

### 1-2. Get owner and repo

```bash
gh repo view --json owner,name
```

Store as `OWNER` and `REPO`.

### 1-3. Validate PR state

If `state` is `CLOSED` or `MERGED`, stop immediately:

```
❌ PR #<number> is already closed/merged. Nothing to resolve.
```

---

## Phase 2: Fetch Unresolved Threads

### 2-1. GraphQL query for review threads

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          startLine
          comments(first: 50) {
            nodes {
              id
              databaseId
              body
              author { login }
              path
              line
            }
          }
        }
      }
    }
  }
}' -f owner="$OWNER" -f repo="$REPO" -F pr=<PR_NUMBER>
```

### 2-2. Filter threads

From the result, keep only threads where:
- `isResolved: false`
- `isOutdated: false` (skip outdated threads — the code has already changed)

### 2-3. Display summary

```
📋 PR #<number>: <title>

Unresolved review threads: <count>

  Thread 1  [feat/foo.ts:42]   @reviewer: "Variable name is unclear"
  Thread 2  [src/api.ts:17]    @reviewer: "Missing error handling"
  Thread 3  [README.md:5]      @reviewer: "Update the installation steps"
  ...

Skipped (outdated): <count>
```

If count is 0:
```
✅ No unresolved review threads found. Nothing to do.
```
Exit cleanly.

---

## Phase 3: Fix, Reply, and Resolve

Process each unresolved thread in sequence.

**Before processing threads**, initialize an empty list to track modified files:
```
MODIFIED_FILES=[]  # collect thread.path for every actionable fix applied
```

For each thread:

### 3-1. Classify the comment

Determine whether the comment is:

| Type | Action |
|------|--------|
| **Actionable fix** — clear code change request | Implement fix → reply → resolve |
| **Question / discussion** — asks for explanation or opinion | Reply only (do NOT resolve) |
| **Complex architectural change** — requires major redesign | Skip with reply asking for further discussion |
| **File deleted** — referenced file no longer exists | Reply explaining removal, skip fix |

For complex architectural changes, post a reply like:
```
Thanks for the feedback! This change would require significant architectural refactoring.
Could we discuss this further — perhaps in a follow-up issue or a separate PR?
I'll leave this thread open for now.
```
Do NOT attempt the fix. Do NOT resolve the thread.

### 3-2. Implement fix (actionable only)

Read the referenced file:

```bash
# Use Read tool with the file path from thread.path
```

Apply the minimal change that addresses the review comment using the Edit tool.
Do NOT refactor surrounding code. Do NOT add unrelated changes.

After applying the fix, **record the file path**:
```
MODIFIED_FILES.append(thread.path)  # used in Phase 4 for staging
```

### 3-3. Reply to thread

Use the REST API with the **databaseId** of the first comment in the thread:

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{databaseId}/replies \
  -f body="<reply-message>"
```

Reply format for a fix:
```
Fixed in this commit. <brief description of what was changed>
```

Reply format for a question:
```
<Answer to the question>
```

### 3-4. Resolve thread (actionable fixes only)

Use the **node id** of the thread:

```bash
gh api graphql -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: { threadId: $threadId }) {
    thread { id, isResolved }
  }
}'  -f threadId="<thread-node-id>"
```

Only resolve threads where a code fix was actually applied.
Do NOT resolve question/discussion threads or skipped threads.

---

## Phase 4: Commit and Push

After processing all threads in the iteration:

### 4-1. Stage changes

Use the file paths collected in `MODIFIED_FILES` during Phase 3:

```bash
git add <path1> <path2> ...  # deduplicated list from MODIFIED_FILES
```

Do NOT use `git add -p` (interactive) or `git add .` (too broad).
If a path contains spaces or special characters, quote it: `git add "path with spaces/file.md"`.

### 4-2. Commit

Follow Conventional Commits format:

```bash
git commit -m "fix: address PR #<number> review comments

- <thread 1 summary>
- <thread 2 summary>
..."
```

### 4-3. Push

```bash
git push origin HEAD
```

---

## Phase 5: Review Rally Check

After pushing, re-fetch unresolved threads (same GraphQL query as Phase 2).

- Filter for `isResolved: false` AND `isOutdated: false`
- If new threads exist that were not in the previous iteration, go back to **Phase 3**
- Maximum **3 total iterations** (including the first pass)

If the iteration cap is reached and unresolved threads remain:

```
⚠️  Reached maximum iteration limit (3). The following threads still need attention:

  Thread N  [path:line]  @reviewer: "..."
  ...

Please review and address these manually.
```

---

## Error Handling Reference

| Situation | Action |
|-----------|--------|
| PR is closed or merged | Stop immediately with message |
| No unresolved threads | Exit cleanly with success message |
| Referenced file deleted | Reply explaining deletion, skip fix, do NOT resolve |
| `isOutdated: true` | Skip silently (code already changed) |
| Comment is a question/discussion | Reply with answer, do NOT resolve |
| Complex architectural change | Reply asking for further discussion, skip, do NOT resolve |
| Rally loop cap reached (3) | Report remaining threads, stop |

---

## Final Summary

After all iterations complete, display:

```
✅ PR #<number> review resolution complete

  Fixed and resolved:  <count> threads
  Replied (no fix):    <count> threads
  Skipped:             <count> threads
  Remaining open:      <count> threads

Commits pushed to <branch-name>.
```
