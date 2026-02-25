---
name: review
description: Review PR comments, discuss improvements, and reply with resolution status
version: "1.1.0"
---

## Identify Target PR

Parse `$ARGUMENTS` to extract a PR number or URL.
If not provided, detect from the current branch:

```
gh pr view --json number --jq '.number' 2>/dev/null
```

If no PR is found, ask the user to specify one.

## Step 1: Collect Review Comments

Fetch all review comments on the PR (both human and bot/AI):

```
gh api repos/{owner}/{repo}/pulls/{number}/comments --jq '.[] | {id: .id, path: .path, line: .line, body: .body, user: .user.login, created_at: .created_at}'
```

Also fetch PR-level review summaries:

```
gh api repos/{owner}/{repo}/pulls/{number}/reviews --jq '.[] | {id: .id, user: .user.login, state: .state, body: .body}'
```

Include all reviewers — human teammates and AI bots alike. Do NOT filter by user type.

## Step 2: Analyze Each Suggestion

For each review comment:

1. Read the referenced file and surrounding code context (at least 20 lines around the mentioned line).
2. Understand the reviewer's suggestion in the context of the actual code.
3. Evaluate the suggestion's validity:

| Category | Criteria |
|----------|----------|
| **Valid** | Real bug, security issue, or meaningful improvement |
| **Debatable** | Stylistic preference or trade-off that could go either way |
| **Can Safely Ignore** | Misunderstands the code, already handled elsewhere, or not applicable |

## Step 3: Present Findings

Group findings by category and present to the user:

```
## Review Analysis for PR #{number}

### ✅ Valid Suggestions (recommended to apply)

1. **[file.py:42]** {summary}
   - Reviewer said: {brief quote}
   - Assessment: {why this is valid, what the fix should be}

### 🤔 Debatable

1. **[file.py:78]** {summary}
   - Reviewer said: {brief quote}
   - Pros: {benefits of applying}
   - Cons: {reasons to skip}

### ❌ Can Safely Ignore

1. **[file.py:15]** {summary}
   - Reviewer said: {brief quote}
   - Why: {reason this is not applicable — e.g., misunderstood context, project convention differs}
```

## Step 4: Discuss and Apply

For each Valid or Debatable suggestion:
1. Ask the user whether to apply the change.
2. If approved, make the code change using Edit.
3. After all approved changes are applied, suggest a commit message following the project's commit convention (e.g., `fix: 리뷰 피드백 반영`).

## Step 5: Reply to Review Comments

After the commit is created, reply to each review comment on GitHub to record the resolution.

For each comment that was discussed (Valid, Debatable, or Ignored):

```
gh api repos/{owner}/{repo}/pulls/{number}/comments/{comment_id}/replies -f body="{reply_body}"
```

### Reply format (concise, bulleted)

Write the reply body in the language configured in the project's CLAUDE.md. If no language is configured, follow the user's conversational language. Examples below are in Korean:

**If applied:**
```
- ✅ 반영 완료
- 커밋: {short_sha}
- 변경: {1-line summary of what was changed}
```

**If not applied (with reason):**
```
- ⏭️ 미반영
- 사유: {concise reason — e.g., 프로젝트 컨벤션과 상충, 이미 다른 방식으로 처리됨}
```

Present all planned replies to the user for approval before posting.

**Important:**
- Do NOT apply any code changes without explicit user approval for each item.
- Do NOT post reply comments without explicit user approval.
- Read the actual code context before judging — do not rely solely on the review comment.
- Consider the project's existing patterns, conventions, and CLAUDE.md instructions.
- Be honest when a review catches a genuine issue — do not dismiss valid feedback.
- If no review comments are found, inform the user.
