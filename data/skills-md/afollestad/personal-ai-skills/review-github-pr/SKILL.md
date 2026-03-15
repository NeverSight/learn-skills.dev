---
name: review-github-pr
description: Review a PR and submit suggestions as comments, along with an optional approval/request for changes.
compatibility: Requires git, gh, jq, and internet access.
model: opus
argument-hint: "[PR URL]"
---

**Read-only:** Do not modify any files. Your job is to review, report, and submit feedback on GitHub. Do not to make local changes.

**Before proceeding, verify prerequisites:**
- Run `gh auth status` to confirm GitHub CLI is authenticated. If not, stop and tell the user to run `gh auth login`.
- Confirm you have a PR or diff to review. If unclear, ask the user what to review before proceeding.

## Instructions

Review a GitHub pull request, generate prioritized inline comments, and submit them as a batch review.

Use when: reviewing, evaluating, critiquing, auditing, or assessing a GitHub PR. Triggers on requests like "review this PR", "review PR #123", or when given a PR URL to review.

**All GitHub interactions must use the `gh` CLI tool.** Do not use `curl`, direct API URLs, or web fetching. Always use `gh pr`, `gh api`, or other `gh` subcommands.

### 1. Fetch the PR diff

Use `gh` CLI to get the full diff and PR metadata:

```bash
gh pr view <PR> --json number,title,body,baseRefName,headRefName
gh pr diff <PR>
```

If the user provides a URL, extract the repo and PR number from it. For private repos, always use `gh` CLI rather than fetching URLs directly.

### 2. Analyze the entire diff

- Read the **complete diff**, not just individual chunks. Understand the full scope of changes.
- Consider how changes across multiple files relate to each other.
- Check for correctness, security, performance, readability, and maintainability.
- **Do not include fluff, praise, or "LGTM"-style commentary.** Only include actionable findings: critical issues (P0/P1) and nits (P2/P3). Every comment must point to a specific problem or concrete suggestion. Comments that merely note something is "a good change" or compliment the author are not actionable — omit them entirely.

### 3. Generate prioritized comments

Organize all findings into priority levels:

- **P0 — Blocking:** Bugs, security vulnerabilities, data loss risks, broken functionality. These must be fixed before merge.
- **P1 — Important:** Logic errors, missing edge cases, poor error handling, test gaps. Strongly recommended to fix.
- **P2 — Suggestion:** Code style improvements, better naming, minor refactors, documentation gaps.
- **P3 — Nit:** Trivial style preferences, optional improvements, minor observations.

Before finalizing, review all findings — including P3 nits — and deliberately decide whether each is worth including. Do not silently drop nits; either include them or note that they were considered and omitted. Try to frame feedback as questions.

**Present the full list of comments to the user, grouped and sorted by priority, before submitting.** Each comment should include:
- An index of the feedback to be used in step 4 below.
- Priority level (P0/P1/P2/P3).
- File path and line number.
- The comment text.

### 4. Ask for review disposition

Ask the user if they want to submit all feedback, or just some, and how they want to submit the review:
- **Approve** — approve the PR with the comments.
- **Request changes** — request changes (appropriate when there are P0 or P1 items).
- **Comment** — submit comments without approving or requesting changes.

The user may skip submitting certain feedback by index (provided in part 3).

### 5. Submit as a single batch review

Construct a JSON payload and submit all comments as a single review using `gh api` with `--input`:

```bash
echo '<json_payload>' | gh api repos/{owner}/{repo}/pulls/{number}/reviews --method POST --input -
```

JSON payload format:

```json
{
  "event": "APPROVE|REQUEST_CHANGES|COMMENT",
  "body": "",
  "comments": [
    {
      "path": "relative/file/path.ext",
      "line": 42,
      "side": "RIGHT",
      "body": "**[P0]** Comment text here"
    }
  ]
}
```

Every comment body **must** start with the priority as a bold prefix: `**[P0]**`, `**[P1]**`, `**[P2]**`, or `**[P3]**`.

For the review body/summary, leave it **empty** (`"body": ""`). Do not include summaries, priority counts (e.g. "1 P1, 3 P2"), fluff, filler, or praise. All feedback belongs in inline comments only.

**Important — use `line` and `side`, NOT `position`:**
- `line`: The **file line number** in the new version of the file (the number shown after `+` in the diff hunk header, e.g. `@@ -45,15 +47,30 @@` means new lines start at 47). Count new-side lines (context lines and `+` lines, skipping `-` lines) from the hunk start to find the correct line number.
- `side`: Always `"RIGHT"` for comments on new/changed lines.
- Do **not** use the deprecated `position` field — it refers to a line's offset within the diff hunk and is error-prone across multi-hunk files.

Return the review URL to the user when complete.
