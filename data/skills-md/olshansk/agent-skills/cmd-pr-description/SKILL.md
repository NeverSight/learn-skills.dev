---
name: cmd-pr-description
description: Generate concise PR descriptions by analyzing the diff against a base branch
disable-model-invocation: true
---

# Quick PR Description <!-- omit in toc -->

Generate a concise PR description by analyzing the diff against a base branch.

Output the result in a markdown file named `PR_DESCRIPTION.md`.

Copy to clipboard: `cat PR_DESCRIPTION.md | pbcopy`

- [Instructions](#instructions)
  - [1. Determine the base branch](#1-determine-the-base-branch)
  - [2. Analyze the changes against the default branch](#2-analyze-the-changes-against-the-default-branch)
  - [3. Generate the description using the format below](#3-generate-the-description-using-the-format-below)
  - [4. Offer to update the GitHub PR](#4-offer-to-update-the-github-pr)
- [Output Format](#output-format)
- [Section Rules](#section-rules)
  - [tl;dr](#tldr)
  - [Summary](#summary)
  - [Feature Diff](#feature-diff)
  - [Details](#details)
  - [General Details](#general-details)
- [Example Output](#example-output)

## Instructions

### 1. Determine the base branch

First, determine the base branch using the repository's default branch.

Try these methods in order until one succeeds:

**Method 1 - GitHub CLI**

```bash
BASE_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name' 2>/dev/null)
```

**Method 2 - Git remote**

```bash
BASE_BRANCH=$(git remote show origin 2>/dev/null | grep "HEAD branch" | cut -d: -f2 | xargs)
```

**Method 3 - Git symbolic-ref**

```bash
BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
```

**IMPORTANT:** Do NOT assume `master` or `main` as a fallback. If all methods fail, ask the user which branch to use as the base.

### 2. Analyze the changes against the default branch

```bash
git diff $BASE_BRANCH --stat -- ":(exclude)*.lock" ":(exclude)package-lock.json" ":(exclude)pnpm-lock.yaml" ":(exclude)package.json"
git log $BASE_BRANCH..HEAD --oneline
```

### 3. Generate the description using the format below

### 4. Offer to update the GitHub PR

After writing `PR_DESCRIPTION.md`, use `AskUserQuestion` to ask the user if they want to update the GitHub PR description automatically.

If yes, run:

```bash
gh pr edit --body "$(cat PR_DESCRIPTION.md)"
```

## Output Format

```markdown
_tl;dr This is a single sentence summarizing the most important outcome of this PR in 100-200 characters._

## Summary

- **Subject/topic**: < 100 character explanation
- ...
- ...

## Feature Diff

| Component                          | Before                                     | After                                    |
| ---------------------------------- | ------------------------------------------ | ---------------------------------------- |
| 1-3 words describing the component | 1 sentence describing how it worked before | 1 sentence describing how it works after |
| ...                                | ...                                        | ...                                      |
| ...                                | ...                                        | ...                                      |

## Details

<details>
<summary>Technical Details</summary>

### Subsection Title

- **Subject/topic**: < 100 character explanation
- ...

### Another Subsection

- **Subject/topic**: < 100 character explanation
- ...

</details>
```

## Section Rules

### tl;dr

- Single sentence, max ~120 characters
- Product-level: what does the user/operator/developer get?
- No implementation details, no file names

### Summary

- 2-5 bullets, one per meaningful change (not per file)
- Min (2) and max (5) are hard floors and ceilings per section
- Bold phrase answers "what does the user/operator get?"
- Plain language after the dash: one sentence, no jargon
- No implementation details: reviewers will read the diff for that
- No fluff: skip "minor cleanup", "refactor", "update docs" unless they deliver real value
- Start from the most impactful change and work down

### Feature Diff

- **Always include this section**
- Should have anywhere from 1-10 rows depending on the size of the PR
- One row per component, module, config, API, or behavior that changed
- "Component" = the thing that changed (endpoint, table, config key, module, behavior, etc.)
- "Before" = previous state, or `N/A` if new
- "After" = new state, or `Removed` if deleted
- Keep cells concise — short phrases, not sentences
- Group related rows; aim for 3-10 rows
- Good component examples: API endpoint, DB table/column, config key, env var, dependency version, CLI flag, permission, error behavior

### Details

- **Only include for larger PRs** (5+ files changed or multiple logical groups)
- Use collapsible `<details>` tags
- Group by feature/concern, not by file
- This is where implementation specifics go (file names, function names, migration details)
- Use backticks for code references (`file.py`, `get_user()`, `/api/v1/users`)
- 1-3 subsections, each with 3-5 bullets

### General Details

- Use backticks for code references (`file.py`, `get_user()`, `/api/v1/users`)
- Italicize or bold keywords if it helps readability

## Example Output

```markdown
_tl;dr Users can now log in with email/password and stay authenticated across browser sessions._

## Summary

- **Session-based login**: Users authenticate with email/password and maintain sessions across browser restarts
- **Faster auth checks**: Session lookups use an indexed token column instead of scanning the full users table
- **Remember-me support**: Users can opt into 30-day sessions instead of the default 24-hour expiry

## Feature Diff

| Component        | Before                     | After                                           |
| ---------------- | -------------------------- | ----------------------------------------------- |
| Auth method      | API key only               | Email/password + session cookie                 |
| Session duration | N/A                        | 24 hours (default), 30 days (remember-me)       |
| `sessions` table | N/A                        | New table with `user_id`, `token`, `expires_at` |
| Token lookup     | Full table scan on `users` | Indexed lookup on `sessions.token`              |
| `/auth/login`    | N/A                        | New endpoint                                    |
| `/auth/logout`   | N/A                        | New endpoint                                    |

## Details

<details>
<summary>Technical Details</summary>

### Authentication Service

- **New login service**: Handles JWT issuance, session creation, and cookie management
- Add `login_service.py` with session create/validate/revoke methods
- Integrate `/auth/login` and `/auth/logout` endpoints in `routes/auth.py`
- Support `remember_me` flag to toggle 24h vs 30d expiry

### Database Schema

- **New sessions table**: Stores active sessions with automatic expiry
- Add `sessions` table with `user_id`, `token`, `expires_at` columns
- Add B-tree index on `token` for O(1) lookups
- Add index on `expires_at` for cleanup job performance

</details>
```
