---
name: obsidian-cli
description: Interact with an Obsidian vault via the Obsidian CLI. Use when the user asks to read, search, create, update, or inspect notes, daily notes, links, tasks, tags, or other vault content from the terminal.
---

# Obsidian CLI

## When to apply

- The user asks to work with an Obsidian vault from the terminal.
- The task mentions notes, markdown, daily notes, backlinks, tags, tasks, or vault search.
- The task is about using the Obsidian CLI rather than editing files directly.
- The task is part of ongoing coding work and the vault may hold useful project context, decisions, progress notes, or handover state.

## Core workflow

1. Confirm the target vault before running note commands. If it is unclear, run `obsidian vaults`.
2. If `obsidian vaults` shows exactly one open vault, use that vault by default.
3. If the command or syntax is uncertain, check help first with `obsidian help`, `obsidian help <command>`, or `obsidian <command> --help`.
4. Prefer read-only discovery first: search or read, then expand with `links` and `backlinks` once you find a relevant note.
5. Prefer updating an existing note with `append` or `prepend` over rewriting a whole note or creating a new one.
6. Re-read afterwards when the write matters operationally.

## Safe defaults

- Target a specific vault explicitly whenever the CLI supports it.
- Return or summarise CLI output directly. Do not open the GUI unless the user asks for it.
- Ask before destructive operations such as `delete`, `move`, `rename`, `history:restore`, or sync/history restore operations.
- Preserve existing frontmatter, headings, wikilinks, and note structure unless the user asks for a rewrite.
- For daily-note work, resolve the note first with `daily:path` or inspect it with `daily:read` before writing.
- If help output does not show the operation you want, assume the CLI may not support it directly and use a different workflow instead of inventing syntax.

## Coding use

- Treat the vault as external working memory for active coding work.
- Prefer updating an existing project, daily, or working note before creating a fresh note.
- Read `references/coding-workflows.md` when the task is about note choice, coding context, or what kind of update to record.
- Read `references/voice.md` only when you need help drafting the note text itself.

## Portability

- This skill may be installed into another project. Do not assume any repo-local layout.
- Always ask for or discover the vault path or vault target from the runtime environment.
- On WSL, `obsidian` may not be available on `$PATH`. If so, invoke the Windows CLI entrypoint directly, for example `"/mnt/c/Program Files/Obsidian/Obsidian.com" vaults`.

## Additional resources

- Start with [references/REFERENCE.md](references/REFERENCE.md) to choose the right supporting file.
