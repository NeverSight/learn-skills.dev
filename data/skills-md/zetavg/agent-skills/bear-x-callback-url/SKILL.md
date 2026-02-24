---
name: bear-x-callback-url
description: Bear app x-callback-url scheme guidance for building callback URLs, understanding parameters, and using Bear actions (create, open, search, tags, selection, and related operations). Use when a user asks how to use Bear's x-callback-url scheme, when composing a Bear callback URL, or when building an integration that needs to drive Bear via x-callback-url.
---

# Bear X-Callback-URL

## Overview

Use this skill to build Bear x-callback-url links, explain parameters, and describe expected results. This skill includes a concise, reformatted version of the official documentation so agents do not need to fetch the URL. The official reference URL is kept only to help update content if needed: https://bear.app/faq/x-callback-url-scheme-documentation.

## Scheme Basics

Bear supports the x-callback-url protocol. URLs follow this pattern:

`bear://x-callback-url/[action]?[action parameters]&[x-callback parameters]`

Standard x-callback parameters like `x-success` and `x-error` are supported when needed by an integration.

## Shared Notes

- Encode all query parameter values for URL safety.
- macOS-only parameters include `new_window`, `float`, and `show_window`.
- Actions that accept `selected=yes` require an API token; see [references/token-generation.md](references/token-generation.md).
- Some actions return data only if `token` is provided; see each action file.
- URL builder links are for humans only. Do not open them as an agent; only share them with human users who want a UI to compose URLs.

## Action Index

You can read only the files you need. Each action link includes a short description to guide selection.

- [references/open-note.md](references/open-note.md) - Open a note by title or id and return its content.
- [references/create.md](references/create.md) - Create a new note and optionally attach content or a file.
- [references/add-text.md](references/add-text.md) - Append, prepend, or replace text in an existing note by title or id.
- [references/add-file.md](references/add-file.md) - Append, prepend, or replace a file in an existing note by title or id.
- [references/tags.md](references/tags.md) - List all tags shown in the sidebar (token required).
- [references/open-tag.md](references/open-tag.md) - Show notes matching a tag or any of multiple tags.
- [references/rename-tag.md](references/rename-tag.md) - Rename an existing tag.
- [references/delete-tag.md](references/delete-tag.md) - Delete an existing tag.
- [references/trash.md](references/trash.md) - Move a note to Trash by id or search.
- [references/archive.md](references/archive.md) - Move a note to Archive by id or search.
- [references/untagged.md](references/untagged.md) - Show untagged notes (returns data only with token).
- [references/todo.md](references/todo.md) - Show todo notes (returns data only with token).
- [references/today.md](references/today.md) - Show today notes (returns data only with token).
- [references/locked.md](references/locked.md) - Show the Locked sidebar item.
- [references/search.md](references/search.md) - Search notes by term and/or tag.
- [references/grab-url.md](references/grab-url.md) - Create a note from a web page URL.

## Usage Guidance

- Confirm the target action, required parameters, and whether a token is needed.
- Clarify whether the user wants to open UI or return results via callbacks.
- Mention any restrictions (locked state, encrypted notes) listed in the action file.
