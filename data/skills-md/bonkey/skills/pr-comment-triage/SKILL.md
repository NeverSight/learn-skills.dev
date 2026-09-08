---
name: pr-comment-triage
description: "Reviews all comments on the current pull request, evaluates whether each one still needs action, and decides whether to address it or resolve it. Holds remarks written by AI review agents to a stricter evidence bar, because they judge a diff without the context a human reviewer carries. Use when the user asks to triage PR comments, review feedback, resolve review threads, or decide which PR comments still matter."
---

# PR Comment Triage

Review every comment on the current PR and make a careful decision for each one: address it in code, reply for clarification, or resolve it when it is already handled. Resolve every review thread you have confirmed is handled, and always leave a short explanation reply when you resolve one.

A remark is a claim about the code, not a fact about it. That is true of every author and doubly true of AI review agents, which judge one diff hunk without the context a human reviewer carries. Confirm each claim against the code before it changes a line.

## Scope

Use this skill when the user wants help with the current PR's feedback, including requests like:

- "go through the PR comments"
- "triage review feedback"
- "check whether these PR comments still need work"
- "resolve addressed review comments"

This skill is for the **current PR on the current branch**.

## Rules

- Be conservative about *whether* a thread is handled, but once you have confirmed it is, resolve it — do not leave verified-handled threads open.
- Always leave a short explanation reply on a thread before resolving it, regardless of why it is being resolved (fixed in code, invalid, obsolete, or settled by discussion).
- Mark every comment you post to the PR (thread replies and top-level comments alike) with a trailing attribution line: `🤖 Generated with Claude Code`. Put it on its own line at the end of the comment body.
- Report every comment you post. Capture each comment's URL from the API response at post time — never reconstruct or guess a link — and list them all at the end of the run, each abridged to one or two sentences.
- Read every page of every API response. GitHub returns at most 100 items per page, so an un-paginated fetch is an incomplete inventory — see [Identify the current PR](#1-identify-the-current-pr) for the paginated commands.
- This skill is repeatable. Assume it may be run many times on the same PR, and each run fetch the live state fresh — never rely on a previous run's inventory. On every run, pick up comments added since last time and re-check open threads that the code may have made addressed or obsolete.
- Distinguish between **review threads** and **top-level PR comments**:
  - Review threads can be resolved.
  - Top-level PR conversation comments cannot be marked resolved in GitHub; they can only be replied to or left as-is.
- Never batch-resolve everything blindly.
- Read the current code and the surrounding discussion before deciding.
- If a comment is ambiguous, conflicts with other feedback, or would require a product/architecture decision, ask the user instead of guessing.
- **Treat every AI-authored remark as an unverified claim.** Review agents — Copilot, CodeRabbit, Devin, Greptile, Graphite, any `[bot]` account, and any in-house review agent the repository runs — read a diff without the repository's history, conventions, callers, or tests. They report defects the surrounding code already prevents, cite symbols and APIs this project does not have, and ask for changes the project decided against. Confident wording is not evidence. See [Hold AI-authored remarks to a higher bar](#hold-ai-authored-remarks-to-a-higher-bar).
- **Never change code to satisfy an agent you could not confirm.** An unconfirmed claim is a rejected claim, not a cheap precaution. Say in the reply what the code actually does.
- Skepticism is not dismissal. An agent can be right, and a confirmed remark is addressed like any other. What changes is the burden of proof, not the willingness to act.

## Workflow

### 1. Identify the current PR

Get the current PR for the checked-out branch.

Preferred command:

```sh
gh pr view --json number,title,url,headRepositoryOwner
```

Use `gh api graphql` to fetch review threads, since `gh pr view` may not expose the full thread inventory you need.

Fetch:

- PR number, title, URL
- Review threads with:
  - thread id
  - resolved state
  - file path / line if available
  - all comments in the thread
- Top-level issue comments on the PR conversation

#### Read every page

GitHub caps each response at 100 items, and `gh pr view --json comments,reviews` returns only the first page. A truncated fetch hides comments without any error, so pass `--paginate` on every list call and follow cursors until `hasNextPage` is `false`.

REST endpoints — `--paginate` follows the `Link` header to the last page:

```sh
gh api --paginate repos/OWNER/REPO/issues/PR_NUMBER/comments   # top-level conversation
gh api --paginate repos/OWNER/REPO/pulls/PR_NUMBER/comments    # review thread comments
gh api --paginate repos/OWNER/REPO/pulls/PR_NUMBER/reviews     # review summaries
```

GraphQL — the query must declare an `$endCursor` variable and request `pageInfo { hasNextPage endCursor }`, otherwise `--paginate` cannot advance:

```sh
gh api graphql --paginate -F owner='OWNER' -F repo='REPO' -F pr=PR_NUMBER -f query='
query($owner:String!, $repo:String!, $pr:Int!, $endCursor:String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100, after: $endCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          comments(first: 100) {
            pageInfo { hasNextPage endCursor }
            nodes { id author { login __typename } createdAt body url }
          }
        }
      }
    }
  }
}'
```

`--paginate` follows one connection per query — `reviewThreads` here. Nested connections keep their own limit, so a thread whose `comments` reports `hasNextPage: true` needs its own follow-up query for the rest of that thread.

#### Record who wrote each comment

`author.__typename` is `Bot` for a GitHub App account such as Copilot or CodeRabbit; the REST equivalent is `user.type`. Agents that post through an ordinary user account come back as `User`, so also match the login against the review agents this repository runs; an in-house agent is indistinguishable from a human by type alone. Mark every comment `human` or `agent` in the inventory. The mark decides how much proof the remark needs before it changes code.

If no PR exists for the current branch, stop and tell the user.

### 2. Build a complete comment inventory

Collect **all feedback** that may require action, from humans and from agents alike. Build this fresh on every run so repeated runs stay in sync with the live PR:

- Unresolved review threads — including any added since the last run
- Open threads whose concern the current code may now have addressed (resolve them) or made obsolete (the code they referenced was changed, moved, or removed)
- Resolved review threads that may have been resolved incorrectly
- Top-level PR comments in the conversation
- Review summaries when they include actionable requests

Confirm the inventory is complete before you evaluate anything: every list call used `--paginate`, every cursor ran until `hasNextPage` is `false`, and the thread and comment counts match the PR page. If they do not match, fetch again rather than triaging a partial list.

For each item, capture:

- comment/thread identifier
- author, and whether that author is a human or an AI agent
- timestamp
- location in code if applicable
- raw comment text
- replies / thread context
- current resolved state

Ignore obvious bot noise — nitpick spam, duplicated review summaries, coverage chatter — unless the user asked to include it. A substantive remark from an AI agent is not noise: keep it on the list and verify it. When you cannot tell noise from substance, keep it.

### 3. Evaluate each comment carefully

For every comment, classify it into one of these buckets:

1. **Address in code**
   - The feedback is valid and not yet handled.
   - A code/config/document change is still needed.

2. **Already addressed, safe to resolve**
   - The requested change is already present in the current branch.
   - Or the thread was superseded by a better implementation and the original concern is no longer applicable.

3. **Needs discussion / user decision**
   - The comment is ambiguous.
   - The request conflicts with other requirements.
   - The suggested fix is risky, architectural, or subjective.

4. **No action needed, but cannot be resolved automatically**
   - Usually applies to top-level PR comments, because GitHub does not support resolving them.
   - Optionally draft a reply explaining why no further change is needed.

5. **Unfounded**
   - The code contradicts the claim: the premise is wrong, the cited symbol does not exist, the caller already guarantees the invariant, or the case is impossible.
   - Reply with what the code actually does, then resolve. Rejected AI-authored remarks land here.

### 4. Verify against the current code

Before deciding that something is addressed:

- Read the relevant files.
- Check whether the requested behavior is actually implemented.
- Check whether later commits or replies already handled the concern.
- Prefer evidence from the codebase over assumptions.

Do not treat "I think this is fine" as enough reason to resolve a thread.

#### Hold AI-authored remarks to a higher bar

An AI review agent sees a diff, not the project. It cannot know which invariant the caller enforces, which branch is unreachable, which pattern the repository chose on purpose, which test already covers the case, or which version of a dependency is pinned. So its remarks arrive fluent, specific, and missing exactly the context that decides whether they are true.

For every remark from an agent, do all of this before you write any code:

1. **Restate the claim so it can be false.** "`parseConfig` panics when `path` is empty" can be checked. "Error handling could be improved" cannot — ask for the concrete case or reject it.
2. **Find the claim in the code.** Read the function, its callers, and its tests. A remark about a line means nothing until you have read what reaches that line.
3. **Test the premise the remark depends on.** Agents routinely assume a nil, a type, a race, a config key, or an API that this repository does not have. Grep for the symbols the remark names.
4. **Decide from the evidence.** Confirmed — address it. Contradicted — reject it, and name the code that contradicts it. Neither — it is not confirmed: reject it or ask the user, and leave the code alone.

Two remarks that agree are not two pieces of evidence; agents repeat each other's guesses. A remark that blocks a required check is not thereby correct — a red gate is a fact about the gate, not about the code.

Never widen the diff for an agent. A refactor, a new abstraction, an extra defensive check, a new dependency, or a broader rename needs a human's request before you make it.

Suggested-change blocks are proposals, not patches. Read the surrounding lines and write the fix yourself; never commit a suggestion block unread.

### 5. Present a triage summary before acting

Produce a concise summary grouped by decision:

- **Address**
- **Resolve**
- **Unfounded** — with the code that contradicts each claim
- **Needs user input**
- **Top-level comments with no further action**

For each item include:

- author
- short quote or paraphrase
- decision
- one-sentence rationale

If the user asked you to act, proceed after the summary unless a decision is ambiguous or risky.

## Acting on the decisions

### When a comment should be addressed

- Make the smallest correct change that resolves the underlying concern.
- Keep the fix scoped to the feedback.
- After changing code, re-check the thread against the new code, then resolve it with a short reply describing the fix (see below).

### When a review thread should be resolved

Resolve only review threads, not top-level PR comments.

**Always post a short explanation reply before resolving the thread**, regardless of why it is being resolved. One or two sentences is enough; the reply tells the reviewer what happened:

- **fixed in code** — name the change and, when useful, the commit or `file:line`
- **invalid** — explain why the concern does not apply to the actual implementation, and for an agent's claim name the `file:line` that contradicts it
- **obsolete** — the relevant code was removed or replaced
- **settled by discussion** — point to the reply or decision that resolved it

End every reply body with the attribution line `🤖 Generated with Claude Code` on its own line.

Required approach (do both, in this order):

1. Post the explanation reply on the thread.
2. Resolve the thread via GitHub GraphQL.

Example shape:

```sh
# 1. Reply with a short explanation (end the body with the attribution line).
#    Request `url` back and keep it — it is the direct link for the posted-comments list.
gh api graphql -f query='mutation($threadId:ID!,$body:String!) { addPullRequestReviewThreadReply(input:{pullRequestReviewThreadId:$threadId, body:$body}) { comment { id url } } }' -F threadId='THREAD_ID' -F body='Fixed in <commit> — extracted the helper as requested.

🤖 Generated with Claude Code'

# 2. Resolve the thread
gh api graphql -f query='mutation($threadId:ID!) { resolveReviewThread(input:{threadId:$threadId}) { thread { isResolved } } }' -F threadId='THREAD_ID'
```

If the thread is already resolved, do not touch it unless you discovered it was resolved incorrectly; in that case, tell the user rather than silently changing history.

### When the item is a top-level PR comment

Top-level PR comments cannot be resolved. Instead:

- decide whether code changes are needed
- optionally draft or post a short reply
- report it as addressed / no action needed in your summary

`gh pr comment` prints the URL of the comment it created — keep that URL for the posted-comments list:

```sh
gh pr comment PR_NUMBER --body 'Confirmed — the rate limit is enforced by the gateway, so no change here.

🤖 Generated with Claude Code'
```

Do not claim you resolved something GitHub does not allow you to resolve.

## Output format

Use a compact checklist or table with columns like:

- `kind` (`thread`, `top-level`, `review-summary`)
- `author`
- `author kind` (`human`, `agent`)
- `location`
- `decision`
- `reason`
- `action`

### Comments posted

End every run with a list of the comments posted during that run, in the order they were posted. Give each one a single bullet: one or two sentences abridging what the comment says, followed by a direct link to it.

```markdown
## Comments posted

- Extracted the retry helper into `client.go:88` as requested, then resolved the thread — [reply](https://github.com/owner/repo/pull/123#discussion_r456789)
- Explained that the nil check is unreachable because the caller validates the input — [reply](https://github.com/owner/repo/pull/123#discussion_r456790)
- Confirmed the rate limit is enforced by the gateway, so no change is needed — [comment](https://github.com/owner/repo/pull/123#issuecomment-99887766)
```

Use the URLs returned by the API when posting. If the run posted no comments, say so instead of omitting the list.

## Decision standard

A thread is safe to resolve only when at least one of these is true:

- the requested change is now present in code
- the concern is invalid based on the actual implementation
- a later discussion explicitly settled the issue
- the thread is obsolete because the relevant code was removed or replaced

If none of those are clearly true, do not resolve it.

Code changes carry a second bar. An AI-authored remark earns a code change only after you have found the defect in the code yourself. A suggested diff, a confident tone, and a red review status are not that evidence. When the claim cannot be confirmed either way, reject it or hand it to the user — never implement it just to be safe.

## Troubleshooting

- If `gh` is not authenticated, tell the user to run `gh auth login`.
- If GraphQL fields differ by GitHub version or API shape, fall back to a custom `gh api graphql` query.
- If a comment you know exists is missing from the inventory, the fetch was truncated. Re-run it with `--paginate`, and check nested connections such as a thread's `comments` for their own `hasNextPage`.
- If the current branch has no PR, stop and tell the user.
- If you cannot determine whether a comment is addressed from the code alone, ask the user instead of guessing.
- If an AI-authored remark cites a function, flag, field, or API you cannot find, treat the remark as wrong about this codebase rather than your search as incomplete. Say so in the reply and name what the code has instead.
- If an agent re-posts a remark you already rejected, link your earlier reply instead of re-arguing it, and tell the user the agent is looping.
