---
name: melech-plan-review
description: >-
  Review a solution before approving it, like a GitHub changes tab: a file tree
  of red and green pseudo-code the user can comment on inline, then answer
  Approve, Commented, or Rejected. Use when the user wants to see what would
  change, a git-like diff, or the PR as if it were ready.
disable-model-invocation: true
---

# Plan review

Foresee this solution before they approve it. Show what would change, and what
they should expect, as a file tree of git-like red and green lines, as if the
PR is ready and they are reviewing the changes tab.

The page is for them or a product reader. They are not looking to deep-dive
the code.

Mark each part of a file with a blue `@@ section @@` line. Indent the way a
diff would. Write a sentence when the behavior is the point. Write a short
code line when that is easier to read than the sentence. Do not paste the
surrounding implementation.

## Open it for review

Copy [template.html](template.html) to `<plan-name>-plan-review.html` next to
the plan file, or in the repo root when the plan lives only in the chat. Fill
every `{{TOKEN}}`.

Serve it in the background with `scripts/review_server.py` beside this file:

```bash
python3 <skill-dir>/scripts/review_server.py <plan-name>-plan-review.html
```

It opens the page and prints the URL and the review file path. Comments save
to `<plan-name>-plan-review.json` next to the page as the reader writes them.

## Wait for the verdict

Ask one question with three options: Approve, Commented, Rejected. Use your
question tool if you have one. Otherwise ask in chat and end the turn.

When they answer, read the review file. It has an overall `summary` and
`comments`. Each comment has a `body` and the `places` it points at: `file`,
`lines`, and the `quote` they selected. One comment can point at several
lines, or at places in several files. A `file` of `null` is the page header.

- Approve: the plan stands. Fold in any comments, then stop the server.
  Do not start implementing unless they ask.
- Commented: answer each comment in chat, change the plan where a comment
  asks, and rewrite the page. Rename the review file to
  `<plan-name>-plan-review-<round>.json`, ask them to refresh the tab, and ask
  again.
- Rejected: read the comments for why. If there are none, ask what is wrong.
  Do not rewrite the page until the direction is clear. Stop the server.
