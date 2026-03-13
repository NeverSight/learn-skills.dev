---
name: address-pr-feedback
description: Fetches PR review comments, categorizes each as Will Fix / Won't Fix / New Issue, addresses fixable feedback using TDD, commits, pushes, and posts a summary.
---

# Address PR Feedback

Fetch all review comments on a pull request, categorize them, fix what should be fixed using TDD, and summarize the results.

## Step 1: Identify the Pull Request

Determine which PR to work on using this priority order:

1. **`$ARGUMENTS` provided** — If the user passed a PR number or URL, use it directly:
   - A number like `42` → `gh pr view 42`
   - A URL like `https://github.com/owner/repo/pull/42` → extract the number and use it
2. **Current branch has a PR** — Run `gh pr view --json number,url,title,state` to detect a PR for the current branch
3. **Ask the user** — If neither works, ask: "I couldn't detect a PR for the current branch. Please provide a PR number or URL."

Validate that the PR is in an `OPEN` state. If it is merged or closed, inform the user and stop.

Store the PR number, URL, repo owner, and repo name for later steps. Extract owner and repo with:

```bash
gh repo view --json owner,name --jq '.owner.login + "/" + .name'
```

## Step 2: Fetch All Review Comments

Collect comments from three GitHub API sources. Consult `references/gh-api-examples.md` for the expected response shapes.

### 2a. Inline code review comments

```bash
gh api repos/{owner}/{repo}/pulls/{number}/comments --paginate
```

These are comments attached to specific lines in the diff. Capture: `id`, `node_id`, `body`, `path`, `line` (or `original_line`), `diff_hunk`, `user.login`, `user.type`, `created_at`, `in_reply_to_id`. The `node_id` is needed later to look up thread IDs for resolution.

### 2b. Conversation-level comments

```bash
gh api repos/{owner}/{repo}/issues/{number}/comments --paginate
```

These are general comments on the PR conversation thread. Capture: `id`, `body`, `user.login`, `user.type`, `created_at`.

### 2c. Review summaries

```bash
gh pr view {number} --json body,reviews,author
```

Extract actionable feedback from review summaries, especially those with `CHANGES_REQUESTED` state.

### 2d. Filter out noise

Skip comments that are:

- **From the PR author** — self-comments are usually context, not feedback
- **CI/infrastructure bots** — skip bots that don't provide code review feedback (e.g. `dependabot`, `codecov`, `netlify`, `vercel`). **Keep** comments from code review bots like `coderabbitai`, `github-actions`, `pr-agent`, `codeclimate`, `sonarcloud`, etc. — these are valuable review feedback and should be categorized like any other reviewer
- **Non-substantive** — less than 10 characters after stripping whitespace and emoji (pure reactions)
- **Already resolved** — check review thread resolution status via `gh api repos/{owner}/{repo}/pulls/{number}/comments` and look for threads where the conversation has been marked resolved

Group reply chains together — if a comment has `in_reply_to_id`, attach it to the parent thread rather than treating it as separate feedback.

Present the count: "Found **N** actionable review comments (M inline, K conversation-level). Proceeding with categorization."

If zero actionable comments, inform the user and stop: "No actionable review comments found on PR #N. Nothing to address."

## Step 3: Categorize Each Comment

For each comment or comment thread, assign one of three categories:

### Will Fix

The feedback is valid, actionable, and within the scope of this PR:

- Points out a bug, missing edge case, or incorrect behavior
- Requests a reasonable improvement to code this PR touches
- Identifies a missing or inadequate test
- Flags a security or performance concern in changed code

### Won't Fix

The feedback is not worth acting on:

- Style preference that contradicts the project's established conventions
- Suggestion that would significantly expand PR scope without clear benefit
- Based on a misunderstanding of the code or requirements
- Already addressed in a different part of the code (explain where)

### New Issue

The feedback is valid but out of scope for this PR:

- Identifies a real problem in code this PR did not change
- Suggests a feature enhancement beyond the PR's intent
- Points out tech debt that predates this PR
- Requests a refactor that would touch many files beyond the diff

### Present and confirm

Show the categorization as a table:

| # | Comment (truncated) | Author | Category | Rationale |
|---|---------------------|--------|----------|-----------|
| 1 | "This should handle null..." | reviewer1 | Will Fix | Valid edge case in changed code |
| 2 | "Consider using a factory..." | reviewer2 | New Issue | Refactor beyond PR scope |
| 3 | "I'd prefer const here..." | reviewer3 | Won't Fix | Project uses let per convention |

Ask: "Here's how I'd categorize the feedback. Want to adjust any categories before I start making fixes?"

**Wait for the user to confirm or adjust before proceeding to Step 4.**

## Step 4: Execute Fixes (TDD Style)

Delegate all coding work to **SDET subagents** — specialized test-and-fix agents. See `references/sdet-agent.md` for the full agent prompt.

### 4a. Detect the test framework (once)

Check the project for its test setup — cache the result for all fixes:

- Read `package.json` for test scripts and dependencies (`jest`, `vitest`, `bun:test`, `mocha`, `pytest`, `rspec`, etc.)
- Look for config files (`jest.config.*`, `vitest.config.*`, `pytest.ini`, `.rspec`, etc.)
- Examine existing test files for import patterns and naming conventions
- Determine the test run command (e.g., `bun test`, `npm test`, `pytest`)

This context will be included in every agent prompt so agents don't each have to rediscover it.

### 4b. Group fixes for parallelization

Analyze the "Will Fix" items and group them by file independence:

- **Independent fixes** touch different files (or different, non-overlapping parts of the codebase). These can run in parallel.
- **Dependent fixes** touch the same file or closely related code. These must be serialized within a single agent to avoid conflicts.

Create parallel groups. For example, if you have 5 fixes where #1 and #2 both touch `parser.ts`, and #3, #4, #5 each touch different files:

| Group | Fixes | Why |
|-------|-------|-----|
| Agent 1 | #1, #2 | Both touch `parser.ts` — run sequentially within one agent |
| Agent 2 | #3 | Independent — `api.ts` |
| Agent 3 | #4 | Independent — `validator.ts` |
| Agent 4 | #5 | Independent — `utils.ts` |

All agents run in parallel. Fixes within a single agent run sequentially.

### 4c. Spawn SDET subagents

For each parallel group, spawn a **general-purpose** subagent with `model: "sonnet"`. Launch all groups as **parallel Agent tool calls in a single message** to maximize concurrency.

Each agent prompt must include:

1. The SDET role and workflow from `references/sdet-agent.md`
2. The test framework details from step 4a (framework, test command, file conventions)
3. The specific "Will Fix" item(s) assigned to this agent, including:
   - The reviewer's comment body
   - The file path and line number (if an inline comment)
   - The diff hunk for context (if available)
4. Instructions to follow the TDD loop: write failing test, implement fix, verify, run full suite

Example agent prompt structure:

```
You are an SDET agent. [Include references/sdet-agent.md content]

## Project test setup
- Framework: bun:test
- Run command: bun test
- Test location: tests/ directory
- Naming convention: <module>.test.ts

## Your assignments

### Fix 1: Handle null input in parser
- Reviewer: @reviewer1
- File: src/parser.ts, line 42
- Comment: "This should handle the null case — currently throws an unhandled TypeError"
- Diff context: [include diff_hunk]

Follow the TDD loop for each fix. Report back what you changed and whether all tests pass.
```

### 4d. Collect results

As agents complete, collect their reports. Each agent should report:

- Which comment(s) it addressed
- Files changed (source and test)
- Tests added or modified
- Whether the full suite passes
- Any issues encountered

If any agent reports a failing test suite, spawn an additional SDET agent to resolve the issue before proceeding.

### 4e. Final test suite run

After all agents complete, run the full test suite once more to catch any cross-agent conflicts:

```bash
<test run command>
```

If tests fail, the most likely cause is parallel agents modifying shared imports or test fixtures. Spawn another SDET agent to fix the conflicts before proceeding.

## Step 5: Commit and Push

After all fixes are complete:

### 5a. Stage changes

Stage only files modified as part of the fixes. Use `git add <specific-files>` — do not use `git add -A` or `git add .`.

### 5b. Commit

Write a descriptive commit message referencing the PR number:

```
Address PR #<number> review feedback

- Fix: <brief description of fix 1>
- Fix: <brief description of fix 2>
- Test: <brief description of tests added/updated>

Addresses review comments from <reviewer1>, <reviewer2>.
```

### 5c. Push

```bash
git push
```

If the push fails because the remote has new commits, rebase and retry:

```bash
git pull --rebase && git push
```

If the rebase produces conflicts, **stop and inform the user** rather than auto-resolving.

## Step 6: Reply, Resolve, and Summarize

### 6a. Create issues for "New Issue" items (optional)

Ask: "Want me to create GitHub issues for the N 'New Issue' items?"

If yes, for each item:

```bash
gh issue create --title "<suggested title>" --body "<context from review comment, link to PR>"
```

Do this **before** posting replies so the inline replies can reference the created issue numbers.

### 6b. Draft replies for user approval

For each categorized comment, draft a reply. Present **all** drafted replies to the user in a table for review before posting anything.

**Will Fix** replies — reference what was changed and the commit:

```
Fixed in <commit-sha>. Added null check for the input parameter and a test covering the empty input case.
```

**Won't Fix** replies — explain the reasoning concisely:

```
Keeping the current approach — the project convention uses `let` for variables that get reassigned in this pattern. See the style guide in CONTRIBUTING.md.
```

**New Issue** replies — reference the created issue (or explain the deferral):

```
Good catch — this predates this PR so I've split it into a dedicated issue: #89
```

Or if no issue was created:

```
Valid point, but this is outside the scope of this PR — the factory pattern would require refactoring across several modules. Recommend addressing it as a follow-up.
```

Present the drafts as a table:

| # | Comment (truncated) | Category | Drafted Reply |
|---|---------------------|----------|---------------|
| 1 | "This should handle null..." | Will Fix | Fixed in abc1234. Added null check + test for empty input. |
| 2 | "Consider using a factory..." | New Issue | Deferred to #89 — requires refactoring beyond this PR's scope. |
| 3 | "I'd prefer const here..." | Won't Fix | Keeping current approach — project convention uses let for reassigned vars. |

Ask: "Here are the replies I'd post to each thread. Want to edit any of these before I send them?"

**Wait for the user to confirm or adjust before posting.**

### 6c. Post approved replies

After the user approves, post each reply. Use the GitHub API to reply to the specific comment by its ID. See `references/gh-api-examples.md` for the exact API calls.

- **Inline review comments** (have a `path` and `line`) — reply in the thread using the review comment replies endpoint
- **Conversation-level comments** (not inline) — post a reply using the issues comment endpoint

### 6d. Resolve completed threads

After replying to each inline thread, resolve it to mark it as addressed. Thread resolution requires the GraphQL API:

```bash
gh api graphql -f query='
  mutation {
    resolveReviewThread(input: {threadId: "<thread_node_id>"}) {
      thread { isResolved }
    }
  }
'
```

To get the `thread_node_id`, use the `node_id` field from the **first comment in the thread** (the root comment, not replies). This is the `pullRequestReviewThread` node ID.

If the root comment's `node_id` is for an individual comment rather than a thread, query for the thread ID first:

```bash
gh api graphql -f query='
  query {
    node(id: "<comment_node_id>") {
      ... on PullRequestReviewComment {
        pullRequestReviewThread {
          id
          isResolved
        }
      }
    }
  }
'
```

Then use the returned thread `id` in the `resolveReviewThread` mutation.

Resolve threads for **all three categories** — Will Fix, Won't Fix, and New Issue — since each has been explicitly addressed with a reply.

### 6e. Summary table

Present a complete summary to the user:

**Will Fix (N items) — All addressed**

| Comment | Author | What was done | Files changed | Thread |
|---------|--------|---------------|---------------|--------|
| "Handle null input..." | reviewer1 | Added null check + test | src/parser.ts, tests/parser.test.ts | Replied + resolved |

**Won't Fix (N items)**

| Comment | Author | Reason | Thread |
|---------|--------|--------|--------|
| "Use const instead of let" | reviewer3 | Project convention uses let for reassigned variables | Replied + resolved |

**New Issue (N items)**

| Comment | Author | Suggested issue title | Thread |
|---------|--------|----------------------|--------|
| "Factory pattern would help" | reviewer2 | Refactor: Extract factory for widget creation (#89) | Replied + resolved |

Include test results and the commit SHA: "All N tests passing (M new, K modified). Commit `abc1234` pushed to branch `feature/my-branch`."
