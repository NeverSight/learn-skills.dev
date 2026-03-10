---
name: groove-groovebook-review
description: "Browse and review open learning PRs in the configured groovebook repo. Use to participate in the shared groove commons."
license: MIT
allowed-tools: Read Bash(gh:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-groovebook-review

## Outcome

Open learning PRs in the groovebook repo are listed; the user reviews one and submits a reaction (approve, comment, or request changes).

## Acceptance Criteria

- Open PRs are listed with title, author, and date
- User selects a PR to review; diff and body are shown
- User submits a reaction via `gh pr review`

## Steps

1. Read `groovebook:` from `.groove/index.md`; if absent, exit with:
   `groovebook is not configured. Add 'groovebook: <owner>/<repo>' to .groove/index.md to enable.`

2. Check `gh auth status`; if not authenticated, exit with:
   `Not authenticated with GitHub. Run: gh auth login`

3. List open PRs:
   ```
   gh pr list --repo <groovebook> --state open --json number,title,author,createdAt
   ```
   - If none open: print "No open learning PRs in <groovebook>." and exit
   - Display as a numbered list: `N. #<number> — <title> (by <author>, <date>)`

4. Ask: "Which PR would you like to review? (enter number or PR #)"

5. Show the PR:
   - `gh pr view <number> --repo <groovebook>` — show body
   - `gh pr diff <number> --repo <groovebook>` — show diff

6. Ask: "Your reaction? (approve / comment / request-changes)"
   - If `comment`: ask for the comment text
   - If `request-changes`: ask for the request text
   - If `approve`: confirm intent

7. Submit:
   ```
   gh pr review <number> --repo <groovebook> --<approve|comment|request-changes> --body "<text>"
   ```
   For approve: `gh pr review <number> --repo <groovebook> --approve`

8. Confirm submission and print the PR URL.

9. Optional follow-up: ask "Does this learning suggest a change to a groove skill? If so, consider opening a companion PR to the groove repo referencing this groovebook PR."

## Constraints

- Read-only until step 7 — do not modify any local files
- If `gh pr diff` output is very large (>200 lines), show only the first 50 lines and note it's truncated
- The `approve` reaction should always ask for confirmation before submitting — approvals are harder to undo than comments
