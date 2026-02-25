---
name: notesmd
description: Work with Obsidian vaults (plain Markdown notes) via notesmd-cli. Use when the user asks to create, read, search, list, move, delete notes, manage frontmatter, or interact with their Obsidian vault from the terminal. Works without Obsidian running.
---

# NotesMD CLI

Interact with Obsidian vaults using `notesmd-cli`. Works without Obsidian running — operates directly on the vault's Markdown files.

## Vault basics

Obsidian vault = a normal folder on disk containing `*.md` files.

Vault config lives at `~/Library/Application Support/obsidian/obsidian.json` on macOS.

## Setup

Set default vault (once):

```bash
notesmd-cli set-default "{vault-name}"
```

Check current default:

```bash
notesmd-cli print-default
notesmd-cli print-default --path-only
```

All commands accept `--vault "{vault-name}"` to target a specific vault.

## Commands

### Read

```bash
notesmd-cli print "{note-name-or-path}"
notesmd-cli list                          # vault root
notesmd-cli list "subfolder"
```

### Search

```bash
notesmd-cli search                        # fuzzy search note names
notesmd-cli search-content "term"         # search inside note content
```

Add `--editor` to open selected note in `$EDITOR` instead of Obsidian.

### Create / Update

```bash
notesmd-cli create "{note-name}" --content "..."
notesmd-cli create "{note-name}" --content "..." --overwrite   # replace existing
notesmd-cli create "{note-name}" --content "..." --append      # append to existing
notesmd-cli create "{note-name}" --open                        # open after create
```

### Move / Rename

Updates `[[wikilinks]]` across the vault automatically.

```bash
notesmd-cli move "{old-path}" "{new-path}"
```

### Delete

```bash
notesmd-cli delete "{note-path}"
```

### Daily note

```bash
notesmd-cli daily
```

### Open in Obsidian

```bash
notesmd-cli open "{note-name}"
notesmd-cli open "{note-name}" --section "{heading}"
```

### Frontmatter

```bash
notesmd-cli frontmatter "{note}" --print
notesmd-cli frontmatter "{note}" --edit --key "status" --value "done"
notesmd-cli frontmatter "{note}" --delete --key "draft"
```

## Tips

- Note paths are relative to vault root (e.g. `"Folder/Note"`)
- For direct edits, modify the `.md` file directly — Obsidian picks up changes
- Prefer `notesmd-cli move` over `mv` to keep wikilinks consistent
- `--editor` flag uses `$EDITOR` env var (defaults to `vim`)
- For CLI bugs or unexpected behavior, refer to [notesmd-cli](https://github.com/Yakitrak/notesmd-cli)
