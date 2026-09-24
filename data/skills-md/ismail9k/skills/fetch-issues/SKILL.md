---
name: fetch-issues
description: >
  Use when the user asks to list, show, or review open issues — from the
  tracker recorded in docs/agents/issue-tracker.md, whether GitHub, Jira,
  local markdown, or another backend, or from a repository or project the
  user names. Read-only: not for creating, editing, closing, or triaging
  issues.
---

# Fetch Issues

## When this applies

Use this when the user wants to see the open issues in their tracker. It
reports what the tracker returns without changing any issue.

For one known issue, read just that issue — on GitHub,
`gh issue view <number>` — instead of fetching the whole list.

## Preconditions

1. Resolve the tracker and target before fetching anything:
   - If the user explicitly names a repository or project for this run, use
     it.
   - Otherwise, read `docs/agents/issue-tracker.md`: its Backend, Location,
     and Reading sections.
   - If the config is missing, doesn't identify a target, or is ambiguous,
     ask the user. Do not guess from a directory name or silently substitute
     a Git remote.
2. Confirm the backend is reachable:
   - **GitHub:** run `command -v gh`; if it is missing, direct the user to
     <https://cli.github.com/> and stop. Then run `gh auth status`; if it
     fails, preserve the useful part of the error, tell the user to run
     `gh auth login`, and stop.
   - **Local markdown:** confirm the recorded Location exists.
   - **Other backends:** use the method in the Reading section's "List open
     issues" line. If the config has no Reading section, ask how to list
     issues rather than guessing. If the recorded tool isn't available — a
     CLI not installed, an MCP server not connected — say so and stop.

## Fetch the issues

**GitHub.** Request the fields needed for a complete report and set an
explicit limit, so the GitHub CLI's small default doesn't silently omit open
issues:

```bash
gh issue list \
  --repo <owner>/<repo> \
  --state open \
  --limit 1000 \
  --json number,title,body,labels,author,createdAt,url
```

If the command returns exactly 1,000 issues, state that the result may have
reached the requested limit rather than claiming it is the complete set;
offer to continue with paginated GitHub API requests.

**Local markdown.** Read, in full, every intent file the Reading section
counts as open.

**Other backends.** Run the recorded method and request complete bodies. If
the tool pages or caps its results, say where the result stopped rather than
calling it complete.

For every backend: don't add label, assignee, milestone, search, or author
filters unless the user requests them. If the fetch fails, report its error
and stop. Do not turn an authentication, authorization, network, or
missing-target failure into an empty result.

## Present the result

If there are no open issues, say so and name the tracker and target that
were checked.

Otherwise, report the total returned and render every issue using this
shape, where `<reference>` is the tracker's own form — `#<number>` on GitHub,
a key such as `PROJ-123` on Jira, a file path for local markdown:

```markdown
## <reference> — <title>

- URL: <url or file path>
- Labels: <comma-separated labels, or None>
- Author: <login or name, or Unknown>
- Created: <creation time in an unambiguous date format, or Unknown>

### Body

<complete body, or _No body provided._>
```

Keep each issue body complete. Do not silently trim it, replace it with an
ellipsis, or summarize it unless the user explicitly asks for a summary. If
the complete result cannot fit in one response, stop only between issues,
state how many of the returned issues were displayed, and continue from the
next issue in the following response.

## What NOT to do

- Don't guess the tracker or target when neither the user nor the tracker
  config identifies it.
- Don't apply GitHub commands to a backend that isn't GitHub, or invent a
  command for a tracker whose Reading section is missing.
- Don't rely on a tool's default page size or limit and call the result
  complete.
- Don't omit, shorten, or paraphrase issue bodies without the user's request.
- Don't hide command failures by reporting that there are no open issues.
- Don't create, edit, close, label, assign, or otherwise mutate issues; this
  skill is read-only.
