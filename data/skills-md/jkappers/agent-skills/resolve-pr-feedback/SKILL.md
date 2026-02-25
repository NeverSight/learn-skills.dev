---
name: resolve-pr-feedback
description: Resolve open PR review discussions by evaluating applicability and value, then fixing valid feedback with conventional commits. Use when (1) addressing reviewer feedback on a pull request, (2) resolving open PR discussions systematically, (3) triaging PR review comments for actionability, (4) batch-fixing code review feedback, or (5) cleaning up unresolved PR conversations.
argument-hint: "<PR URL or number>"
user-invocable: true
compatibility: Requires gh CLI authenticated with repo access.
---

# Resolve PR Feedback

Process open review discussions in a GitHub pull request. Evaluate each for applicability and objective value. Fix valid feedback locally with conventional commits.

## Input

`$ARGUMENTS` — GitHub PR URL (e.g., `https://github.com/owner/repo/pull/123`) or PR number for the current repository.

Parse owner, repo, and PR number from the URL. If a bare number, use the current repository context.

## Workflow

1. Checkout the PR branch
2. Fetch all unresolved review threads
3. Process each thread sequentially — evaluate, then act
4. Report summary

### Step 1: Checkout PR Branch

```bash
gh pr checkout <number>
```

Verify the local branch is up to date with the PR head.

### Step 2: Fetch Unresolved Review Threads

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
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
              author { login }
              body
              createdAt
              path
              line
              startLine
            }
          }
        }
      }
    }
  }
}' -f owner="<owner>" -f repo="<repo>" -F number=<number>
```

Filter to threads where `isResolved` is `false`.

### Step 3: Process Each Thread

Evaluate each unresolved thread in order:

#### 3a: Check Applicability

Read the file and lines referenced by the thread. Compare current code against what the reviewer commented on.

| Condition | Action |
|-----------|--------|
| Referenced file no longer exists | Skip. Report: "File deleted — not applicable." |
| Referenced lines substantially changed | Skip. Report: "Code changed — feedback no longer applies." |
| `isOutdated` is `true` and current code differs from comment context | Skip. Report: "Outdated — code already modified." |
| Code matches what reviewer commented on | Proceed to value evaluation |

#### 3b: Evaluate Objective Value

| Criterion | Examples |
|-----------|----------|
| **Correctness** | Bug fix, logic error, off-by-one, null handling |
| **Security** | Input validation, injection prevention, auth check |
| **Performance** | N+1 query, unnecessary allocation, missing index |
| **Standards compliance** | Naming convention, code style, project pattern violation |
| **Maintainability** | Dead code removal, duplication, unclear naming |

**Valuable**: Feedback addresses at least one criterion with a concrete, actionable suggestion. Proceed to fix.

**Not valuable**: Feedback is subjective preference, bikeshedding, or stylistic without project convention backing. Report the specific reason and move to next thread.

#### 3c: Fix and Commit

1. Read full file context around the referenced lines
2. Implement the fix with minimal, targeted changes
3. Stage only the affected file(s)
4. Compose a commit message following the Commit Format below
5. Run `git commit -m "<message>"` (use a HEREDOC for multi-line messages)

**Scope each commit to a single discussion thread.** Do not batch fixes across threads.

### Step 4: Report Summary

```markdown
| # | File:Line | Feedback | Result |
|---|-----------|----------|--------|
| 1 | src/api/users.ts:42 | Add null check | Fixed (abc1234) |
| 2 | src/utils/parse.ts:15 | Rename variable | Skipped — subjective preference |
| 3 | src/models/order.ts:88 | Fix SQL injection | Fixed (def5678) |
| 4 | src/api/auth.ts:22 | Use different pattern | Not applicable — code changed |
```

## Commit Format

Follow Conventional Commits v1.0.0.

```text
<type>[optional scope]: <description>

[optional body]
```

| Type | Purpose |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Neither fix nor feature |
| `style` | Formatting, whitespace |
| `perf` | Performance improvement |
| `docs` | Documentation only |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |

**Description**: Imperative mood ("add feature" not "added feature"). Lowercase after prefix. No trailing period. Max 50 characters.

**Scope**: Optional. Derive from project directory or module names. Omit for cross-cutting changes.

**Body**: Separate from description with one blank line. Wrap at 72 characters. Explain what and why, not how.

**Prohibited**: AI attribution, emoji, time estimates, TODO items, file lists, hedging language.

## Constraints

- **Do not force-push or amend existing commits.** Create new commits only.
- **Do not resolve threads on GitHub.** The PR author decides when to mark discussions resolved.
- **Do not modify files outside the scope of the feedback.** No drive-by refactoring.
