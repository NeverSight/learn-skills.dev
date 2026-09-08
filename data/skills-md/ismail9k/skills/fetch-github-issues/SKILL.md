---
name: fetch-github-issues
description: >
  Fetch and display open GitHub issues, including their complete bodies and
  metadata, from the repository recorded in docs/agents/issue-tracker.md or
  from a repository the user names explicitly. Use when the user asks to list,
  show, or review open issues; this is a read-only skill and does not create,
  edit, close, or triage issues.
---

# Fetch GitHub Issues

## When this applies

Use this when the user wants to see the open issues for a GitHub repository.
It reports what GitHub returns without changing any issue or label.

For one known issue, prefer `gh issue view <number>` instead of fetching the
whole list.

## Preconditions

1. Resolve the target repository before running `gh`:
   - If the user explicitly names an `owner/repo`, use it for this run.
   - Otherwise, read `docs/agents/issue-tracker.md` and use the `Location`
     recorded for its GitHub backend.
   - If the config is missing, does not name a GitHub repository, or is
     ambiguous, ask the user for the target. Do not guess from a directory
     name or silently substitute a Git remote.
2. Confirm the GitHub CLI is available with `command -v gh`. If it is not,
   direct the user to <https://cli.github.com/> and stop.
3. Run `gh auth status`. If authentication fails, preserve the useful part of
   the error, tell the user to run `gh auth login`, and stop.

## Fetch the issues

Request the fields needed for a complete report and set an explicit limit so
the GitHub CLI's small default does not silently omit open issues:

```bash
gh issue list \
  --repo <owner>/<repo> \
  --state open \
  --limit 1000 \
  --json number,title,body,labels,author,createdAt,url
```

Do not add label, assignee, milestone, search, or author filters unless the
user requests them. If the command returns exactly 1,000 issues, state that
the result may have reached the requested limit rather than claiming it is
the complete set; offer to continue with paginated GitHub API requests.

If `gh` fails, report its error and stop. Do not turn an authentication,
authorization, network, or missing-repository failure into an empty result.

## Present the result

If there are no open issues, say so and name the repository that was checked.

Otherwise, report the total returned and render every issue using this shape:

```markdown
## #<number> — <title>

- URL: <url>
- Labels: <comma-separated labels, or None>
- Author: <login, or Unknown>
- Created: <createdAt in an unambiguous date format>

### Body

<complete body, or _No body provided._>
```

Keep each issue body complete. Do not silently trim it, replace it with an
ellipsis, or summarize it unless the user explicitly asks for a summary. If
the complete result cannot fit in one response, stop only between issues,
state how many of the returned issues were displayed, and continue from the
next issue in the following response.

## What NOT to do

- Don't guess the repository when neither the user nor the tracker config
  identifies it.
- Don't rely on `gh issue list`'s default limit and call the result complete.
- Don't omit, shorten, or paraphrase issue bodies without the user's request.
- Don't hide command failures by reporting that there are no open issues.
- Don't create, edit, close, label, assign, or otherwise mutate issues; this
  skill is read-only.
