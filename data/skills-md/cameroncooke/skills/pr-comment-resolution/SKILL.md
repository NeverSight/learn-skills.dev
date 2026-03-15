---
name: pr-comment-resolution
description: Audit and resolve GitHub pull request review comments with an evidence-based workflow. Use when asked to "address PR comments", "resolve review feedback", "handle inline comments", "reply to review threads", or "close out PR review notes".
---

Audit PR feedback independently, then (after user approval) implement and reply/resolve in GitHub.

Path rule: treat `<skill-dir>` as the directory containing this `SKILL.md`.

## Preconditions

- `gh` is installed and authenticated.
- `python3` 3.11+ is available.
- Run from repository root.

## Step 1: Collect PR feedback

Default command:

```bash
python3 <skill-dir>/scripts/collect_pr_feedback.py --pr 1234
```

This collects:
- `review_threads` for inline review feedback
- `issue_comments` for general PR comments not tied to a line

Review summaries are separate. If you need to audit summary-level feedback, rerun with:

```bash
python3 <skill-dir>/scripts/collect_pr_feedback.py --pr 1234 --include-review-summaries
```

If PR is not provided, the script will try branch-based detection. If detection is ambiguous or empty, ask the user for PR number/URL and rerun.

You must read `<skill-dir>/references/classification-rubric.md` before auditing.
If you have not read it, stop and read it before continuing. Do not audit PR feedback without it.

## Step 2: Audit each feedback item

Fail the workflow if you have not read `<skill-dir>/references/classification-rubric.md` first.

Audit all actionable feedback from the collected JSON:
- `review_threads`
- `issue_comments`
- `reviews` when Step 1 used `--include-review-summaries`

Do not treat an empty `reviews` array as proof that no review summaries exist unless you explicitly collected them.

First, triage each item. Skip any that are clearly non-actionable:
- Comments authored by the PR author (own comments)
- Bot-generated metadata (CI status, preview links, install commands, changelog entries)
- Simple acknowledgements, emoji reactions, or "thanks" replies
- Comments that are neither review feedback nor genuine questions about the PR

Skipped items do not get a full audit — they appear only in the "Skipped" section of the report.

Use two separate audit paths.

### Path A: Inline review threads

Use this path for `review_threads`. Keep it as the default path for normal line-attached review feedback.
Treat each `review_thread` as one audit item anchored to the first substantive reviewer comment. Ignore non-actionable replies inside an otherwise actionable thread unless they materially change the concern.

For each inline item:
1. Restate the concern briefly.
2. Start from the thread location and nearby diff.
3. Verify the exact reported issue in code/diff/tests directly.
4. Classify as one of:
   - `valid`
   - `invalid`
   - `contentious`
   - `already-addressed`
   - `out-of-scope`
5. Gather evidence — concrete file/line references and short code snippets.
6. For anything likely to be `valid`, identify the exact defect pattern, then perform a second bounded pass over the related changed PR surface to check for the same problem.
7. Decide the best resolution (or two options only if truly contentious).

For a likely `valid` inline item, use two passes:
- First pass: confirm the exact reported issue.
- Second pass: check the same bug pattern in the related changed PR surface before finalising the proposed resolution.

### Path B: Non-inline PR feedback

Use this path for `issue_comments` and collected `reviews`.

Do not skip a comment just because it is not attached to a line. General PR comments and review summaries are actionable when they raise a real review concern or ask a genuine question about the PR's behavior, correctness, tests, edge cases, or design.

For each non-inline item:
1. Restate the concern or question briefly.
2. Identify the narrowest relevant changed code path.
   - Start from any files, symbols, tests, APIs, or behavior named in the comment.
   - If the comment is broad, infer the smallest related changed PR surface that can answer it and read that code/tests directly.
3. If the item is a question, answer it directly from code evidence before explaining the classification.
4. Classify as one of:
   - `valid`
   - `invalid`
   - `contentious`
   - `already-addressed`
   - `out-of-scope`
5. Gather evidence — concrete file/line references where available, plus the code path you inspected.
6. For anything likely to be `valid`, identify the exact defect pattern, then perform a second bounded pass over the related changed PR surface to check for the same problem.
7. Decide the best resolution (or two options only if truly contentious).

For a likely `valid` non-inline item, use the same two-pass rule:
- First pass: confirm the reported concern in the relevant changed code path.
- Second pass: check the same bug pattern in the related changed PR surface before finalising the proposed resolution.

Shared scope rules for both paths:
- Start from the reported location or inferred relevant code path.
- Include other changed files only when they participate in the same code path or duplicate the same introduced logic.
- Stay on the same defect class.
- Do not expand into unrelated cleanup, untouched historical code, different issue classes, or opportunistic refactors.

Do not return shallow summaries. Make the rationale specific enough that a reviewer can verify the decision quickly.

## Step 3: Present findings and ask approval

Do not edit code before explicit user approval. Present findings using this format:

````markdown
## PR Comment Audit — <repo>#<number>

<N> feedback item(s) reviewed on **<pr_title>**

---

# <short title summarising the concern>

`<classification>` · <review thread | general PR comment | review summary>

## What the reviewer said

> <feedback content only — preserve meaning, strip HTML/UI chrome, bot footers, and non-feedback metadata>

## Analysis

<Discussion-style paragraph(s) explaining what you found when you checked the code. Reference specific files and lines naturally in prose, e.g. "In `src/foo.ts:42`, the value is already validated before this point..." Include short inline code snippets where they help. For question-style items, answer the question directly in the first sentence, then explain the supporting evidence and classification. State whether the concern is warranted and why. For `valid` items, explain both passes: how you confirmed the exact reported issue, then how you checked the bounded related changed PR surface for the same defect pattern.>

## Expanded issues found

<Only for `valid` items. List any additional same-pattern instances found during the second bounded pass, with short file/line references and one-line explanations. If none were found, say so plainly.>

## Proposed resolution

<What to do and why. For `no change`, explain why no action is needed. For code/doc changes, describe the specific change clearly. Keep it brief — one or two sentences is fine. For `valid` items, the fix on offer should cover both the originally reported issue and any additional same-pattern instances listed above.>

---

# <short title summarising the concern>

`<classification>` · <review thread | general PR comment | review summary>

## What the reviewer said

> ...

## Analysis

...

## Proposed resolution

...

---

## Skipped (non-actionable)

- **<author>**: <short description of comment> — <reason skipped, e.g. "own comment", "bot preview link", "CI status update">
- ...

---

## Next steps

<N> item(s) need changes. If you approve, I will:
  1. <change 1, covering the reported issue plus any same-pattern instances listed in Expanded issues found>
  2. <change 2, covering the reported issue plus any same-pattern instances listed in Expanded issues found>
  3. Run quality checks, then come back for commit/push approval before posting GitHub replies
````

Formatting rules:
- Each item starts with a `#` heading that describes the concern in plain language.
- Classification and comment type go on one line directly under the heading using inline code + separator.
- Reviewer words always in blockquotes — clearly separated from agent analysis.
- Analysis reads like prose, not bullet lists. Weave file references into sentences naturally.
- For inline items, make it clear that the audit started from the review thread location and nearby diff.
- For non-inline items, make it clear which changed code path you inspected and why it was the right place to answer the concern.
- For question-style items, answer the question directly in the first sentence of `Analysis`.
- For `valid` items, explicitly show the two-pass audit: the exact reported issue first, then the bounded same-pattern pass.
- For `valid` items, include an `Expanded issues found` section, even when the answer is that no additional instances were found.
- For non-`valid` items, omit the `Expanded issues found` section entirely.
- Horizontal rules (`---`) separate items.
- When bot comments contain large HTML/autofix blocks, keep only the feedback-relevant text.

## Step 4: Implement approved fixes

Keep changes minimal and in scope.

For each approved `valid` item:
1. Fix the exact reported issue you already confirmed in the first audit pass.
2. Fix every additional same-pattern instance you already found in the second bounded pass.
3. For non-inline concerns, keep the implementation anchored to the relevant changed code path you identified during the audit.
4. Keep the implementation aligned with the approved `Expanded issues found` section.
5. Leave unrelated findings alone, even if you notice them while checking nearby code.

In scope:
- the same defect class
- the same changed file/hunk
- nearby changed code within the related changed PR surface
- sibling instances caused by duplicated new logic in the current PR
- directly related changed call sites or helpers that participate in the same bug mechanism

Out of scope:
- repository-wide hunts
- untouched historical code outside the related changed area
- unrelated cleanup
- different issue classes that merely look similar
- opportunistic refactors

Run relevant quality checks before proposing commit/push (for example: lint, format, type-check, build, tests for touched areas).
If no code changed, state that checks were not required.
Ask before commit/push.

## Step 5: Reply and resolve after push

After user approves commit/push and push succeeds:

1. Build an action JSON.
2. Include commit references in reply bodies (for example: `Fixed in abc1234`).
3. Dry-run first, then apply:

```bash
cat <<'JSON' | python3 <skill-dir>/scripts/apply_resolution_actions.py
[
  {
    "action": "reply_review_comment",
    "repo": "owner/repo",
    "pr_number": 123,
    "comment_id": 456789,
    "body": "Fixed in abc1234."
  }
]
JSON
```

```bash
cat <<'JSON' | python3 <skill-dir>/scripts/apply_resolution_actions.py --apply
[
  {
    "action": "reply_review_comment",
    "repo": "owner/repo",
    "pr_number": 123,
    "comment_id": 456789,
    "body": "Fixed in abc1234."
  }
]
JSON
```

Action requirements:
- `reply_review_comment`: `repo`, `pr_number`, `comment_id`, `body` (REST endpoint — publishes immediately, no pending review)
- `resolve_thread`: `thread_id` (GraphQL node ID)
- `create_issue_comment`: `repo`, `pr_number`, `body`

Collector-to-action mapping:
- `review_threads[].comments[0].databaseId` → `reply_review_comment.comment_id` (must be the **first** comment in the thread — replies to replies are not supported by the GitHub API)
- `review_threads[].id` → `resolve_thread.thread_id`
- `issue_comments` and `reviews` do not map to thread resolution; answer them with `create_issue_comment`

For non-threaded feedback (`issue_comments`, `reviews`), post a top-level PR comment that clearly answers the concern and references the reviewer when appropriate.

Never claim a thread is resolved unless the resolve action succeeds.
Only resolve a thread when the concern is actually addressed in code (or reviewer/user explicitly agrees).
Do not resolve `contentious`, `invalid`, or `out-of-scope` items by default.

## Optional flags (only when needed)

`collect_pr_feedback.py`:
- `--include-resolved-threads`
- `--include-review-summaries`
- `--exclude-outdated-threads`
- `--exclude-bot-comments`
- `--view counts|bodies|thread-locations`

Examples:

```bash
python3 <skill-dir>/scripts/collect_pr_feedback.py --pr 1234 --include-review-summaries
python3 <skill-dir>/scripts/collect_pr_feedback.py --pr 1234 --view counts
python3 <skill-dir>/scripts/collect_pr_feedback.py --pr 1234 --view bodies
python3 <skill-dir>/scripts/collect_pr_feedback.py --pr 1234 --view thread-locations
```
