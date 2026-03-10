---
name: groove-groovebook-publish
description: "Publish a workflow learning to the groovebook shared commons as a GitHub PR. Use after groove-work-compound when a learning is worth sharing."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(gh:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-groovebook-publish

Use $ARGUMENTS as the learning text if provided.

## Outcome

A learning from the current project is published to the configured groovebook repo as a pull request, stripped of any project-specific context, ready for community review.

## Acceptance Criteria

- Learning is published as a PR to `<groovebook>` repo
- PR uses the groovebook PR template format (Summary, Context, Learning, Groove skill area)
- File is written at `learned/<topic>/<YYYY-MM-DD>-<slug>.md` in the groovebook repo
- PR URL is printed to the user

## Steps

1. Read `groovebook:` from `.groove/index.md`; if absent, exit with:
   `groovebook is not configured. Add 'groovebook: <owner>/<repo>' to .groove/index.md to enable.`

2. Check `gh auth status`; if not authenticated, exit with:
   `Not authenticated with GitHub. Run: gh auth login`

3. Verify the groovebook repo is accessible: `gh repo view <groovebook>`; if it fails, exit with a clear message.

4. Get the learning text:
   - If $ARGUMENTS is provided, use it as a starting point
   - Otherwise: ask "What's the learning you'd like to publish? (paste it or describe briefly)"
   - Ask for a one-sentence summary (used as PR title and filename slug)

5. Show a preview of the learning text and ask:
   `Does this contain any repo-specific context to redact? (file paths, internal names, product names)`
   - If yes: help the user redact it — replace specific names with generic descriptions
   - If no: proceed

6. Ask for topic (e.g. `patterns`, `tools`, `anti-patterns`, `workflow`) and skill area (e.g. `compound`, `plan`, `review`, `daily`)

7. Generate slug: lowercase the summary, replace spaces with hyphens, strip special characters, truncate to 40 chars. Construct:
   - Branch name: `learning/<YYYY-MM-DD>-<slug>`
   - File path: `learned/<topic>/<YYYY-MM-DD>-<slug>.md`

8. Fork the groovebook repo if not already forked: `gh repo fork <groovebook> --clone=false`
   - If fork already exists, skip silently

9. Create the branch and file:
   - `gh api repos/<user-fork>/git/refs` to check if branch exists; if so, append a short unique suffix
   - Write the file content (see format below) and commit via `gh api`
   - Or: use `git` operations against the fork URL if `gh api` approach is too complex — prefer the simpler path

10. Open the PR:
    ```
    gh pr create --repo <groovebook> \
      --title "<one-sentence summary>" \
      --body "<formatted body>" \
      --head "<fork-user>:<branch-name>"
    ```

11. Print the PR URL

## Learning file format

```markdown
---
date: YYYY-MM-DD
topic: <topic>
skill-area: <skill-area>
source: groovebook-publish
---

# <One-sentence summary>

## Context

<What triggered this learning — what problem were you solving? Generic, no project specifics.>

## Learning

<The insight itself — what to do, what to avoid, or what pattern works.>

## Groove skill area

`<skill-area>` (e.g. `groove-work-compound`, `groove-work-plan`)
```

## PR body format

```
## Summary
<one-sentence summary>

## Context
<what triggered this>

## Learning
<the insight>

## Groove skill area
`<skill-area>`

---
*Published via groove-groovebook-publish*
```

## Constraints

- Never publish learning text that contains project-specific names, file paths, or internal identifiers without explicit user confirmation that it's intentional
- If the fork step fails due to permissions: suggest the user fork manually and set their fork as the `groovebook:` value
- Slug must be safe for use as a filename: lowercase, hyphens only, no path separators or special characters
- If branch already exists: append `-2`, `-3`, etc. until a free name is found
