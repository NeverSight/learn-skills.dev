---
name: resolve-ai-pr-reviews
description: Resolve PR review feedback from CodeRabbit and Gemini using the gh CLI. Use when asked to fetch AI review comments, summarize unresolved items in Japanese, implement fixes, manually resolve Gemini review threads, push changes, and request a new Gemini review with /gemini review.
---

# Resolve AI PR Reviews

## Overview

Triage AI PR feedback, fix code, close Gemini threads, and re-request review.

## Workflow

### 1) Gather context

- Identify repo owner/name and PR number.
- Ask for direction when a comment conflicts with current policy or implementation.

### 2) Collect AI comments

- Fetch both review comments and issue comments.
- Filter authors matching `coderabbitai` or `gemini` (case-insensitive).
- Track unresolved items only.

```bash
OWNER=$(gh repo view --json owner --jq .owner.login)
REPO=$(gh repo view --json name --jq .name)
PR=$(gh pr view --json number --jq .number) # or set PR explicitly

gh api repos/$OWNER/$REPO/pulls/$PR/comments --paginate --jq \
  '.[] | select(.user.login | test("coderabbitai|gemini"; "i")) |
   {id, user: .user.login, path, line, body, url: .html_url}'

gh api repos/$OWNER/$REPO/issues/$PR/comments --paginate --jq \
  '.[] | select(.user.login | test("coderabbitai|gemini"; "i")) |
   {id, user: .user.login, body, url: .html_url}'
```

### 3) Summarize and confirm decisions

- Respond in Japanese.
- Provide a concise update with these sections:
  - Current status (AI comments scanned + unresolved count)
  - Unresolved list (file/path + action)
  - Commands executed
  - Decision request (if policy choice is needed)

### 4) Apply fixes and validate

- Implement changes with minimal diffs and follow project conventions.
- Run relevant tests/lint when feasible; state if skipped.

### 5) Resolve Gemini review threads

- Do not resolve CodeRabbit threads (it auto-closes).
- Resolve Gemini review threads manually after fixes are complete.
- Before resolving a Gemini thread, add a short reply comment noting what was fixed
  (e.g., "対応しました。: <summary>").
- For Gemini feedback, always leave a reply comment and then resolve the thread.

```bash
THREAD_IDS=$(gh api graphql -f query='
query($owner:String!, $repo:String!, $number:Int!) {
  repository(owner:$owner, name:$repo) {
    pullRequest(number:$number) {
      reviewThreads(first:100) {
        nodes {
          id
          isResolved
          comments(first:50) {
            nodes { author { login } }
          }
        }
      }
    }
  }
}' -F owner=$OWNER -F repo=$REPO -F number=$PR --jq \
  '.data.repository.pullRequest.reviewThreads.nodes[] |
   select(.isResolved == false) |
   select([.comments.nodes[].author.login] | any(test("gemini"; "i"))) |
   .id')

for id in $THREAD_IDS; do
  gh api graphql -f query='
mutation($id:ID!) {
  resolveReviewThread(input: {threadId: $id}) {
    thread { isResolved }
  }
}' -F id=$id
done
```

### 6) Push and request re-review

- Commit and push if appropriate for the repo workflow.
- Post `/gemini review` on the PR after push.
- `/gemini review` の後は時間がかかるため、ユーザーが確認してから再度スキルを実行する。

```bash
gh pr comment $PR --body "/gemini review"
```

### 7) Report back

- Confirm fixes applied, tests run, Gemini threads resolved, and re-review requested.
- List any remaining unresolved items or decisions.
