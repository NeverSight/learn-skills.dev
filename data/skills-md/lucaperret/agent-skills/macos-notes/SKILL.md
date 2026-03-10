---
name: macos-notes
description: Create, read, search, and manage macOS Notes via AppleScript. Use when the user asks to take a note, jot something down, save an idea, create meeting notes, read a note, search notes, or anything involving Apple Notes on macOS. Triggers on requests like "note this down", "save this as a note", "create a note about X", "show my notes", "search my notes for X", "what did I write about X". macOS only.
license: MIT
compatibility: Requires macOS with Notes.app. Uses osascript (AppleScript) and python3 for JSON parsing.
metadata:
  author: lucaperret
  version: "1.0.0"
  openclaw:
    os: macos
    emoji: "\U0001F4DD"
    homepage: https://github.com/lucaperret/agent-skills
    requires:
      bins:
        - osascript
        - python3
---

# macOS Notes

Manage Apple Notes via `$SKILL_DIR/scripts/notes.sh`. Notes content is stored as HTML internally; the script accepts plain text or HTML body and returns plaintext when reading.

## Quick start

### List folders

Always list folders first to discover accounts and folder names:

```bash
"$SKILL_DIR/scripts/notes.sh" list-folders
```

Output format: `account → folder` (one per line).

### Create a note

```bash
echo '<json>' | "$SKILL_DIR/scripts/notes.sh" create-note
```

JSON fields:

| Field | Required | Default | Description |
|---|---|---|---|
| `title` | yes | - | Note title (becomes the first line / heading) |
| `body` | no | "" | Note content (plain text — converted to HTML automatically) |
| `html` | no | "" | Raw HTML body (overrides `body` if both provided) |
| `folder` | no | default folder | Folder name (from list-folders) |
| `account` | no | default account | Account name (from list-folders) |

### Read a note

```bash
echo '<json>' | "$SKILL_DIR/scripts/notes.sh" read-note
```

JSON fields:

| Field | Required | Default | Description |
|---|---|---|---|
| `name` | yes | - | Note title (exact match) |
| `folder` | no | all folders | Folder to search in |
| `account` | no | default account | Account to search in |

### List notes

```bash
echo '<json>' | "$SKILL_DIR/scripts/notes.sh" list-notes
```

JSON fields:

| Field | Required | Default | Description |
|---|---|---|---|
| `folder` | no | default folder | Folder name |
| `account` | no | default account | Account name |
| `limit` | no | 20 | Max notes to return |

### Search notes

```bash
echo '<json>' | "$SKILL_DIR/scripts/notes.sh" search-notes
```

JSON fields:

| Field | Required | Default | Description |
|---|---|---|---|
| `query` | yes | - | Text to search for in note titles |
| `account` | no | default account | Account to search in |
| `limit` | no | 10 | Max results to return |

## Interpreting natural language

Map user requests to commands:

| User says | Command | Key fields |
|---|---|---|
| "Note this down: ..." | `create-note` | `title`, `body` |
| "Save meeting notes" | `create-note` | `title: "Meeting notes — <date>"`, `body` |
| "What did I write about X?" | `search-notes` | `query: "X"` |
| "Show my notes" | `list-notes` | (defaults) |
| "Read my note about X" | `read-note` | `name: "X"` |
| "Save this in my work notes" | `create-note` | Match closest `account`/`folder` from list-folders |

## Example prompts

**"Note down the API key format: prefix_xxxx"**
```bash
echo '{"title":"API key format","body":"Format: prefix_xxxx"}' | "$SKILL_DIR/scripts/notes.sh" create-note
```

**"Show my recent notes"**
```bash
echo '{}' | "$SKILL_DIR/scripts/notes.sh" list-notes
```

**"What did I write about passwords?"**
```bash
echo '{"query":"password"}' | "$SKILL_DIR/scripts/notes.sh" search-notes
```

**"Read my note about Hinge"**
```bash
echo '{"name":"Hinge"}' | "$SKILL_DIR/scripts/notes.sh" read-note
```

**"Create a meeting summary in my iCloud notes"**
```bash
"$SKILL_DIR/scripts/notes.sh" list-folders
```
Then:
```bash
echo '{"title":"Meeting summary — 2026-02-17","body":"Discussed roadmap.\n- Q1: launch MVP\n- Q2: iterate","account":"iCloud","folder":"Notes"}' | "$SKILL_DIR/scripts/notes.sh" create-note
```

## Critical rules

1. **Always list folders first** if the user hasn't specified an account/folder — folder names are reused across accounts
2. **Specify both account and folder** when targeting a specific location — `folder: "Notes"` alone is ambiguous
3. **Password-protected notes are skipped** — the script cannot read or modify them
4. **Pass JSON via stdin** — never as a CLI argument (avoids leaking data in process list)
5. **All fields are validated** by the script (type coercion, range checks) — invalid input is rejected with an error
6. **All actions are logged** to `logs/notes.log` with timestamp, command, and note title
7. **Body uses plain text** — newlines in `body` are converted to `<br>` automatically; use `html` for rich formatting
8. **Note title = first line** — Notes.app treats the first line of the body as the note name
