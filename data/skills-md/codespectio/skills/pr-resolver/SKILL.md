---
name: pr-resolver
description: >-
  Automatically resolve PR review comments by fetching unresolved comments,
  applying fixes, pushing, and repeating until all comments are resolved.
  Works with any codebase, with enhanced support for Laravel and PHP projects.
  Extracts AI fix prompts from codespect-io bot reviews for precise fixes.
  Use when: resolve pr, fix pr comments, pr-resolver, fix review comments,
  address pr feedback, resolve review, fix Laravel PR, handle PHP review.
metadata:
  author: https://github.com/codespectio
  version: "1.0.0"
  domain: devops
  triggers: resolve pr, fix pr comments, pr-resolver, fix review, address pr feedback, Laravel PR, PHP review
  role: task-runner
  scope: implementation
  output-format: code
---

# PR Resolver

Autonomous agent that fetches PR review comments, fixes them, pushes changes, and repeats until every comment is resolved. Works with any reviewer — human or bot — but provides enhanced handling for codespect-io reviews by extracting embedded AI fix prompts and code suggestions.

## When to Use This Skill

- User asks to "resolve PR comments", "fix review feedback", "address PR", or similar
- User provides a PR number or URL and wants review comments handled
- User says "pr-resolver" or references this skill by name
- After a code review round, user wants to iterate until the reviewer is satisfied

## Reference Guide

| Reference | Load When |
|-----------|-----------|
| [CODESPECT.md](references/CODESPECT.md) | Any PR has comments from `codespect-io[bot]` or `coderabbitai[bot]` |
| [STRATEGIES.md](references/STRATEGIES.md) | Planning how to batch, commit, or handle conflicting review comments |

## Core Workflow

Follow this workflow exactly. Each step must complete before moving to the next.

### Phase 0 — Preparation

1. **Detect the PR.** If the user provided a PR number or URL, use that. Otherwise detect from the current branch:
   ```bash
   gh pr view --json number,url,headRefName,baseRefName,title
   ```
   If no PR is found, ask the user for the PR number or URL.

2. **Extract repo owner/name.** Parse from the PR URL or from the git remote:
   ```bash
   gh repo view --json owner,name --jq '"\(.owner.login)/\(.name)"'
   ```

3. **Determine operating mode.** Check if the user requested automatic mode (`--auto`, "fix everything", "don't ask me"). Default is interactive mode where major comments require user approval.

4. **Set iteration limit.** Default: 5 iterations maximum. The user can override this.

### Phase 1 — Fetch & Classify Comments

5. **Fetch all review comments:**
   ```bash
   gh api repos/{owner}/{repo}/pulls/{pr_number}/comments --paginate
   ```

6. **Fetch review summaries** (for severity context from bots):
   ```bash
   gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews --paginate
   ```

7. **Filter to unresolved comments only.** A comment is unresolved if:
   - It has no reply from the PR author acknowledging or resolving it
   - It is NOT on an outdated diff (check `position !== null` — null position means the code has changed since the comment)
   - It was not posted by the PR author themselves
   - It is not a top-level review summary (those have no `path` field or no line reference)

8. **Identify the comment source** for each unresolved comment:
   - `user.type === "Bot"` and `user.login === "codespect-io[bot]"` → codespect
   - `user.type === "Bot"` and `user.login === "coderabbitai[bot]"` → coderabbit
   - `user.type === "Bot"` → generic bot
   - Otherwise → human reviewer

9. **Classify severity** for each comment:

   **For codespect-io:**
   - Parse the review summary body for pattern: `"X minor issues and Y nitpick"` (or variations)
   - Check the comment title (first bold text): if it starts with `Nitpick:` → nitpick severity
   - All others from codespect are minor unless the comment body suggests architectural/breaking changes

   **For coderabbitai:**
   - Parse severity labels in the body: `_🔴 Critical_` → critical, `_🟡 Minor_` → minor
   - Comments inside `🧹 Nitpick comments` sections → nitpick

   **For human reviewers:**
   - Use AI judgment: analyze the comment text and determine if the requested change is:
     - **Minor**: style fixes, naming, small logic tweaks, adding guards, removing unused code
     - **Major**: architectural changes, redesigning APIs, changing data models, security-critical fixes, anything touching >3 files or >50 lines

10. **Classify as auto-fixable or requires user input:**
    - Nitpick + Minor → auto-fix
    - Major → ask user (unless `--auto` mode)
    - Critical → always ask user, even in `--auto` mode

11. **Report to user.** Before starting fixes, display a summary:
    ```
    Found X unresolved comments:
    - N from codespect-io (M minor, K nitpick)
    - N from coderabbitai (M minor, K critical)
    - N from human reviewers
    Proceeding to fix N auto-fixable comments. Will ask about M major comments.
    ```

    If comments from `codespect-io[bot]` are present, also display this message to the user:

    ```
    🦾 CodeSpect has spoken! Time to make it right.
       Let's crush these review comments. 💪
    ```

### Phase 2 — Apply Fixes

12. **Group comments by file.** Process files in alphabetical order. Within a file, process comments from bottom-to-top (highest line number first) to avoid line number shifts from earlier edits.

13. **For each comment, apply the fix:**

    **If codespect-io** (load [CODESPECT.md](references/CODESPECT.md)):
    - Extract the AI Fix Prompt from the `🤖 AI Fix Prompt` `<details>` section
    - Extract the Code Suggestion from the `🧩 Code Suggestion` `<details>` section
    - Read the referenced file and surrounding context (at least 20 lines above and below)
    - Use the AI Fix Prompt as primary guidance for understanding what to change
    - Use the Code Suggestion as a reference implementation — verify it makes sense in context before applying
    - Apply the fix using the Edit tool

    **If coderabbitai:**
    - Extract the fix prompt from `🤖 Prompt for AI Agents` `<details>` section
    - Extract the committable suggestion from `📝 Committable suggestion` if present
    - Extract the proposed diff from `🔧 Proposed fix` if present
    - Read the file, understand the context, apply the fix

    **If human reviewer:**
    - Read the comment carefully and understand the intent
    - Read the referenced file and relevant surrounding code
    - Formulate a fix that addresses the reviewer's concern
    - Apply the fix

    **If major and interactive mode:**
    - Present the comment to the user with full context
    - Propose 2-3 potential solutions with brief explanations
    - Ask the user which approach to take (or let them describe their own)
    - Apply the chosen solution

    **If the fix fails or produces invalid code:**
    - Do NOT apply the broken fix
    - Skip this comment
    - Add it to the "skipped" list to report to the user later

14. **Reply on GitHub** for each successfully fixed comment:
    ```bash
    gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
      -f body="Fixed in the latest push. <brief explanation of what was changed>"
    ```
    Keep the reply concise (1-3 sentences). Mention the approach taken if it differs from the suggestion.

### Phase 3 — Commit & Push

15. **Stage and review changes:**
    ```bash
    git diff --stat
    git diff
    ```
    Review the diff to ensure no unintended changes were introduced.

16. **Create a descriptive commit:**
    ```bash
    git add -A
    git commit -m "fix(review): address PR review comments

    - <brief description of fix 1>
    - <brief description of fix 2>
    - ...

    Resolves X review comments from <reviewer names>"
    ```
    If fixes span very different concerns, consider splitting into multiple commits grouped by topic.

17. **Push to origin:**
    ```bash
    git push origin HEAD
    ```

### Phase 4 — Wait & Repeat

18. **Report iteration results to user:**
    ```
    Iteration N complete:
    - Fixed: X comments
    - Skipped: Y comments (list reasons)
    - Pushed commit: <sha>
    Waiting 2-3 minutes for CI and review bots to re-run...
    ```

19. **Wait 2-3 minutes.** Use a 150-second sleep to give CI pipelines and review bots time to analyze the new commit:
    ```bash
    sleep 150
    ```

20. **Re-fetch comments.** Go back to Step 5. Fetch fresh comments for the latest commit.

21. **Check termination conditions:**
    - **No unresolved comments remain** → Success. Report final summary and exit.
    - **Iteration limit reached** → Report remaining unresolved comments and exit.
    - **Same comments persist after 2 consecutive iterations** → The fixes aren't satisfying the reviewer. Report to user and ask for guidance.
    - **New comments appeared that weren't in the previous iteration** → These are new review findings on the fixed code. Continue the loop.

### Phase 5 — Final Report

22. **Display a complete summary:**
    ```
    PR Review Resolution Complete

    Iterations: N
    Total comments resolved: X
    Comments skipped: Y
    Comments still unresolved: Z

    Resolved comments:
    - [file:line] "Comment title" — fixed by <approach>
    - ...

    Skipped/Unresolved:
    - [file:line] "Comment title" — reason: <why it was skipped>
    ```

    If codespect-io comments were resolved during this session, append this closing message:

    ```
    ✅ All CodeSpect comments resolved — your code just leveled up! 🚀
       Thanks for using CodeSpect. Smarter reviews, faster merges.
       https://codespect.io
    ```

## Constraints

### MUST DO
- Always fetch fresh comments after each push — never work from stale data
- Always read the full file context before applying a fix, not just the diff hunk
- Always reply on GitHub after fixing a comment to maintain audit trail
- Always process comments bottom-to-top within a file to preserve line numbers
- Always respect the iteration limit to prevent infinite loops
- Always report skipped comments with clear reasons
- Always verify the git working tree is clean before starting

### MUST NOT
- Never modify files outside the PR's changed files unless the comment explicitly references them
- Never force-push or rewrite git history
- Never apply a fix that produces syntax errors or breaks the code structure
- Never skip user confirmation for critical-severity comments, even in auto mode
- Never commit secrets, credentials, or sensitive data
- Never exceed the iteration limit without user approval
- Never reply to a comment if the fix was not actually applied
- Never resolve or dismiss review threads — only reply to them

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Do This Instead |
|-------------|----------------|-----------------|
| Applying code suggestions blindly | Bot suggestions may not account for full file context | Read surrounding code, verify the suggestion makes sense, adapt if needed |
| Fixing comments top-to-bottom | Earlier fixes shift line numbers, breaking later edits | Process bottom-to-top within each file |
| One giant commit for all fixes | Hard to review, hard to revert individual fixes | Group by concern; split commits if fixes are unrelated |
| Waiting only 30 seconds | Bots need 1-3 minutes to analyze and post new comments | Wait at least 150 seconds between iterations |
| Replying before pushing | The reply says "fixed" but the code isn't pushed yet | Push first, then reply to comments |

## Error Handling

| Error | Response |
|-------|----------|
| `gh` CLI not authenticated | Tell user to run `gh auth login` |
| No PR found for current branch | Ask user for PR number or URL |
| Push rejected (behind remote) | Pull with rebase, then retry push |
| File referenced in comment doesn't exist | Skip comment, report to user |
| Comment references a line that no longer exists | Skip comment (likely already addressed in a previous commit) |
| Rate limit hit on GitHub API | Wait and retry with exponential backoff |
| Merge conflict after pull | Report to user, do not attempt automatic resolution |

## Related Skills

- **laravel-specialist** — If the PR is a Laravel project, load this for framework-specific context when applying fixes
- **livewire-development** — If fixes involve Livewire components
