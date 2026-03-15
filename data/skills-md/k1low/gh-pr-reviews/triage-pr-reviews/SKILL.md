---
name: triage-pr-reviews
description: >
  Triages unresolved PR review comments using gh-pr-reviews.
  Analyzes code context and classifies each comment as Agree / Partially Agree / Disagree.
  Use when the user wants to triage, review, or analyze unresolved PR comments.
compatibility: Requires gh CLI and gh-pr-reviews extension (gh extension install k1LoW/gh-pr-reviews)
---

# Triage PR Review Comments
1. Run `gh pr-reviews [arg] --json` to get unresolved review comments as JSON. If no argument is given, use the current branch's PR. Note: this command uses Copilot for classification and may take a while depending on the number of comments — use a longer timeout. Each JSON object contains:
   - `comment_id` (int): REST API comment ID — usable for replying via `gh api`
   - `thread_id` (string, only for `type: "thread"`): inline review thread ID
   - `type`: `"thread"` (inline review) or `"comment"` (PR-level)
   - `author`, `body`, `url`: comment metadata
   - `commit_id`, `path`, `line`, `diff_hunk` (only for `type: "thread"`): file location and diff context
   - `category`: one of `suggestion`, `nitpick`, `issue`, `question`, `approval`, `informational`
   - `resolved` (bool), `reason` (string): resolution status and rationale
2. Check if PR metadata (number, title, url) is already available from conversation context. If not (e.g., when a PR number/URL is explicitly passed as argument), run `gh pr view [arg] --json number,title,url` to get it.
3. For `type: "thread"` comments, use `path`, `line`, and `diff_hunk` from the JSON response to identify the exact file location. For `type: "comment"` (PR-level), there is no file location.
4. Check code context for each comment. Leverage any existing conversation context first. Only fetch additional context via `gh pr diff` or file reads when necessary.
5. Evaluate each comment against the code context. Classify as **Agree**, **Partially Agree**, or **Disagree** with a rationale and suggested action.
6. Output results in this format:

```
## Unresolved Review Comments Analysis

**PR**: #<number> (<title>)
**Unresolved comments**: <count>

---

### Comment 1 — [<category>] by @<author>
> <comment body>

**File**: `<path>` (line <line>)
**Assessment**: Agree | Partially Agree | Disagree
**Rationale**: <1-3 sentences>
**Suggested action**: <recommended action>

---

## Summary
- Agree: n — should be addressed
- Partially Agree: n — worth discussing
- Disagree: n — can be explained or dismissed
```

Do NOT write to GitHub (no commenting, resolving, or any mutations). Do NOT commit or push. If code context is unclear, search the codebase to verify before making a judgment. Prefer `gh` commands for GitHub data.
