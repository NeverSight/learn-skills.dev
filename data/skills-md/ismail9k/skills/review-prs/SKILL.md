---
name: review-prs
description: >
  Use when the user asks to review one or more GitHub pull requests — "review
  PR #12", "review the open PRs", "check the PRs the agents opened" — in
  Claude Code, Codex, or any other agent. Not for reviewing uncommitted local
  changes.
---

# Review PRs

Review pull requests and leave the findings on each one as inline comments,
with a suggested change wherever the fix is concrete, so the author can apply
it with one click. Each pull request gets two passes: does it do what its
intent issue asks, and is the code right?

Suggested changes are a GitHub feature, so this skill needs a GitHub
repository and `gh`. The issue tracker can still be anything — GitHub, Jira,
or local markdown.

This skill names actions — "dispatch a reviewer" — not tools. Use your
platform's equivalents.

## Stage 1 — Pick the pull requests

1. Confirm `gh` is installed and `gh auth status` passes; otherwise say why
   and stop.
2. Repository: the one the user names, else this checkout's GitHub
   repository (`gh repo view --json nameWithOwner`). Say which you used.
3. Pull requests: the ones the user names; for "all" or "the open ones",
   `gh pr list --repo <owner/repo> --state open --limit 1000 --json number,title,url,isDraft`.
   Leave drafts out unless the user named them.
4. Print the list and say that findings will be posted on each pull request
   as comments. The user's confirmation of the list is the go-ahead to post.

## Stage 2 — Gather each pull request's context

1. `gh pr view <number> --json title,body,baseRefName,headRefOid` gives the
   description and the head commit. Fetch the commits so they can be
   reviewed locally — `git fetch origin pull/<number>/head <base>` — then set
   `HEAD_SHA` to the head commit and `BASE_SHA` to
   `git merge-base origin/<base> <HEAD_SHA>`.
2. Find the intent issue it links to: look for the references in
   `docs/agents/issue-tracker.md`'s Linking section in the title and body —
   on GitHub, `Closes #<number>` or `Relates to #<number>` — and read the
   issue with the Reading method. With no linked issue or no tracker config,
   skip the intent pass for that pull request and say so in its review.
3. Read the comments already on it —
   `gh api --paginate repos/<owner>/<repo>/pulls/<number>/comments` — so a
   finding already raised isn't posted twice.

## Stage 3 — Review

**Intent pass (you).** Compare the diff with the issue's Proposed outcome and
Constraints. Report what the issue asks for that the pull request doesn't do,
what the pull request does that the issue doesn't ask for, and every
Constraint the diff breaks.

**Code pass (a reviewer).** Use Superpowers' `requesting-code-review`:
dispatch its code reviewer with the pull request's title and description as
the description, the intent issue — or the pull request's body, when there is
none — as the requirements, and `BASE_SHA` and `HEAD_SHA`. Dispatch it on the
most capable model your platform offers. Reviews change nothing, so dispatch
the reviewers for several pull requests at the same time. Without subagent
support, review each diff yourself.

**Check every finding before it is posted.** Open the code each finding
points at and confirm it holds. A reviewer can be wrong, and a wrong comment
on someone's pull request costs them more than a missing one. Drop what
doesn't hold up, and note why for the report.

## Stage 4 — Comment with suggested changes

Post one review per pull request, as `event: "COMMENT"`.

- Anchor each finding to the changed lines it is about: `path`, `line`, and
  `side: "RIGHT"`, plus `start_line` and `start_side` when it spans several
  lines. GitHub accepts only lines that appear in the pull request's diff.
- Open each comment with its severity — Critical, Important, or Minor — and
  one sentence on the consequence.
- When the fix is concrete, end the comment with a suggestion block holding
  the complete new text of exactly the anchored lines, in the file's own
  indentation:

  ````markdown
  **Important** — an invalid address reaches the queue and fails later in
  the worker, where the user never sees the error.

  ```suggestion
  if (!isValidEmail(email)) throw new ValidationError("email");
  await queue.add("confirm", { email });
  ```
  ````

- When the fix needs a design discussion, or touches lines outside the diff,
  explain it without a suggestion block, or put it in the review body.

```bash
gh api --method POST repos/<owner>/<repo>/pulls/<number>/reviews --input review.json
```

```json
{
  "commit_id": "<HEAD_SHA>",
  "event": "COMMENT",
  "body": "<counts by severity, and the intent pass's result>",
  "comments": [
    {
      "path": "src/signup.ts",
      "start_line": 41,
      "start_side": "RIGHT",
      "line": 42,
      "side": "RIGHT",
      "body": "<severity and consequence, then the suggestion block>"
    }
  ]
}
```

With no findings, post one review whose body says so, with no inline
comments.

## Stage 5 — Report

One table: pull request, linked issue, findings posted by severity, and the
review's URL. Then list the findings dropped in the check step, and why.

## What NOT to do

- Don't approve or request changes — post reviews as `COMMENT` only;
  approval is the user's.
- Don't push commits to a pull request's branch; suggestions are the
  author's to apply.
- Don't post a finding you haven't checked against the code.
- Don't write a suggestion that replaces more or fewer lines than its comment
  is anchored to, or that isn't the complete new text of those lines.
- Don't anchor a comment to a line outside the pull request's diff.
- Don't post a finding that is already on the pull request.
- Don't skip the intent pass silently — when there is no linked issue, say so
  in the review body.
