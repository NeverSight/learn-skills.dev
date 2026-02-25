---
name: pr-review
description: Review a GitHub pull request, run targeted checks, and provide a decision-ready summary.
---

# PR Review

Use this skill to review a GitHub PR and summarize risks, tests, and recommendations.

## Inputs

- Require a PR number or URL. If missing, ask for it.
- If the user provides a specific test command, use it.

## Safety Rules

- Do not merge unless the user explicitly asks.
- Do not delete branches unless the user explicitly asks.
- Avoid destructive commands like `git reset --hard`.

## Workflow

1. **Prerequisites**
   - Confirm `gh` is installed and authenticated.

2. **Collect PR data**
   - `gh pr view <PR> --json title,body,labels,assignees,state,url,createdAt,updatedAt,additions,deletions,changedFiles,commits,mergeable,draft`
   - `gh pr view <PR> --json files`
   - `gh pr diff <PR>`
   - `gh pr checks <PR>` when available.

3. **Checkout (optional)**
   - If tests or deeper inspection are needed, checkout the PR branch.
   - Record the current branch first and return to it when done.

4. **Run tests**
   - If no command is provided, infer a reasonable default or ask the user.
   - Record command, exit status, and failures.

5. **Review changes**
   - Summarize key changes by area.
   - Identify risks: breaking changes, security, performance, migrations, missing tests.
   - Call out large or cross-cutting changes.

6. **Provide summary**
   - Use the summary template.
   - End with a clear recommendation and any required follow-ups.
