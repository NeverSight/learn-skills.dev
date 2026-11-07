---
name: linear
description: Post to Linear through the Linear MCP server - create and update issues (title, team, assignee, labels, parent), post and edit comments, and reply in comment threads. Gives Linear's collapsible block syntax, mentions, and safe description updates with `patch` that keep Linear's issue tags. The text comes from clins:post, in the user's languages. Use whenever you file, write up, update or comment on a Linear issue.
user-invocable: true
argument-hint: "[issue | comment | reply] [issue ID or URL to update] [any language changes]"
---

# /clins:linear — Post to Linear

This skill sends a post to Linear. The text (leads, details blocks, languages, footer, check) comes from [`clins:post`](../post/SKILL.md). Pass any language changes the user asked for through to it. The footer names `clins:linear`.

## Rules

- Write only what the user asked for. Do not change an issue's state, assignee, priority or cycle unless the user asked.
- Never close or delete an issue on your own.
- Send text with real newlines, not `\n`.
- Do not mention people unless the post needs their action. A mention notifies them.

## Preflight

1. The Linear MCP tools are connected (`save_issue`, `get_issue`, `save_comment`, `list_comments`). If they are deferred, load them first. If they are missing, tell the user to connect the Linear connector, and stop. This skill does not cover the Linear GraphQL API yet ([`CONTRIBUTING.md`](../../CONTRIBUTING.md#ideas) lists it as an open idea).
2. For a new issue, find the team: from the user, the repo's `AGENTS.md`/`CLAUDE.md`, or `list_teams`. Ask if more than one team fits.
3. Read how the team writes issues: open 2 or 3 recent issues in that team (`list_issues`) for title style, language and labels.

## Linear syntax

- Collapsed block: `>>> 🇬🇧 More details · 3 min read`, a blank line, the content, a blank line, `>>>`. Never GitHub's `<details>`.
- Footer: the line from `clins:post`, with a `---` divider directly above it and blank lines around the divider.
- Do not put a collapsed block inside a list.
- Divider: `---` with blank lines around it.
- Mention: `@displayName` (the Linear display name, not a GitHub login).
- Linear stores links as `[text](<url>)`. That is normal, and the check accepts it.
- Check with `check_post.py --platform linear --skill linear`.

## New issue

1. **Title:** imperative and short, with code names as they are. Match the team's language and style.
2. **Description:** write it with `clins:post`. Headings inside the details: Context, Work, Done when. Add To decide or Sub-issues only when they have content. Translate them for each other language, for example in japanese: 背景, やること, 完了条件.
3. **Fields:** only the ones the user gave or the team clearly uses: `assignee` (a name, email or `"me"`), `labels` (names from `list_issue_labels`), `project`, `parentId` (for a sub-issue), `priority`. To add a label to an existing issue, use `addLabels`: `labels` replaces the whole set. Use names exactly as Linear returns them. Status names can carry an emoji prefix, and a bare name can fail silently, so copy the full name from `list_issue_statuses`.
4. `save_issue` with the title, team, description and fields. Give the user the issue ID and URL.

## Update an issue description

1. `get_issue` and copy the description exactly as it comes back.
2. Linear turns issue IDs in a description (for example `ENG-123`) into `<issue id="..." href="...">` tags. Keep those tags as they are.
3. Change the text with `clins:post` ("Updating a post").
4. Save with `save_issue`, `id`, and `patch` operations (`replace` with an exact `old_string`, `insert_after`, `append`, ...). Every anchor must match the current text exactly once, so copy it from what `get_issue` returned. Do not send a full description written again from memory: the tags would not match, and someone else's edits could be lost.

## Comment

1. Write it with `clins:post`. A short post (lead only) is often right for a comment.
2. `save_comment` with the issue ID and the body.
3. To reply in a thread, pass `parentId` (the top comment's ID, from `list_comments`) and `body`, with no `issueId`.
4. To edit your own comment, `save_comment` with its `id` and the new `body`. Comments keep issue IDs as plain text, so no `patch` is needed.
