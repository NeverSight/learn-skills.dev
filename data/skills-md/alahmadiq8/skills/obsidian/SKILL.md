---
name: obsidian
description: Edit and manage Obsidian vaults — create, read, update, and delete notes, manage properties/frontmatter, handle links and backlinks, work with tags, tasks, daily notes, templates, bases, and more. Uses the Obsidian CLI for safe vault operations when available, with direct file editing as fallback. Use this skill whenever the user mentions Obsidian, vault, knowledge base notes with wikilinks, frontmatter/properties on markdown files, daily notes, or any task involving an Obsidian vault — even if they just say "my notes" or reference a folder that looks like a vault (has .obsidian/ directory).
---

# Obsidian Vault Editor

You are an expert at working with Obsidian vaults. Obsidian stores notes as plain-text Markdown files in a folder (the "vault"). There is no proprietary database — everything is files on disk, which makes them accessible to you via CLI or direct file operations.

This skill covers the full spectrum: creating and editing notes, managing frontmatter properties, handling internal links and backlinks, working with tags, tasks, daily notes, templates, bases, search, and vault-level operations.

## Decision: CLI vs Direct File Editing

**Always prefer the Obsidian CLI** when Obsidian is running. The CLI communicates with the live Obsidian instance, keeping the metadata cache in sync and auto-updating links on rename/move. Direct file edits bypass the cache and can cause stale state.

### Check CLI availability

```bash
command -v obsidian && obsidian version
```

If the `obsidian` command exists and returns a version, use CLI commands. If not, fall back to direct file operations (with extra care around links and frontmatter).

The CLI requires Obsidian to be running. If it's not, the first CLI command will launch it.

### Vault targeting

- If your terminal's CWD is inside a vault folder, that vault is used automatically.
- Otherwise, specify: `obsidian vault="My Vault" <command>`
- Use `obsidian vaults verbose` to list all vaults with paths.

---

## Markdown Links: Use Standard Markdown, Not Wikilinks

Obsidian supports two link formats — Wikilinks (`[[Note]]`) and standard Markdown links (`[Note](Note.md)`). **Always use standard Markdown links.** LLMs produce and parse standard Markdown far more reliably than the Obsidian-specific Wikilink syntax, and Markdown links are portable across tools.

Recommend the user enable this in their vault:

**File:** `VAULT_ROOT/.obsidian/app.json`
```json
{
  "useMarkdownLinks": true
}
```

Or: Settings → Files and Links → disable "Use [[Wikilinks]]"

Even with Markdown links enabled, Obsidian still resolves any wikilinks it encounters — existing notes aren't broken.

When generating links in note content, always use:
```markdown
[Display Text](Note%20Name.md)
[Display Text](folder/Note%20Name.md)
[Display Text](Note%20Name.md#Heading)
[Display Text](Note%20Name.md#^block-id)
```

Spaces in paths must be percent-encoded (`%20`).

---

## Core Operations

### Create a Note

**CLI:**
```bash
# Simple note
obsidian create name="Meeting Notes" content="# Meeting Notes\n\nAttendees:\n- "

# With template
obsidian create name="Trip to Paris" template=Travel open

# At specific path
obsidian create path="Projects/2026/kickoff.md" content="# Project Kickoff"

# Overwrite existing
obsidian create path="README.md" content="# Updated readme" overwrite
```

**Direct (fallback):** Create the `.md` file at the desired vault-relative path. If the note needs frontmatter, include it at the very top of the file.

### Read a Note

**CLI:**
```bash
obsidian read file=Recipe
obsidian read path="Templates/Recipe.md"
```

**Direct:** Read the file from disk.

### Update a Note

**CLI — Append (adds to end):**
```bash
obsidian append path="journal/2026-02-27.md" content="\n## Evening\nReflections..."
obsidian append file=Recipe content="\n- 1 tsp salt" inline  # no extra newline
```

**CLI — Prepend (inserts after frontmatter, which is important — it won't corrupt YAML):**
```bash
obsidian prepend file=Recipe content=">[!tip] Updated recipe\n"
```

**Direct:** When editing files directly, be very careful:
- Parse and preserve YAML frontmatter (between the `---` fences at line 1).
- If prepending, insert content _after_ the closing `---` of frontmatter.
- If appending, add to end of file.
- For surgical edits, use `replace_string_in_file` with enough context to be unambiguous.

### Move / Rename

**CLI (preferred — auto-updates all links across the vault):**
```bash
obsidian move file=Recipe to="Archive/Recipe.md"
obsidian rename file=Recipe name="Grandma's Recipe"
```

**Direct:** Rename the file on disk, then manually search-and-replace all links pointing to the old name across the vault. This is error-prone — strongly prefer CLI.

### Delete

**CLI (sends to trash by default):**
```bash
obsidian delete file=Recipe           # to trash
obsidian delete file=Recipe permanent # permanent delete
```

**Direct:** Move file to vault's `.trash/` folder, or delete from disk.

---

## Properties (YAML Frontmatter)

Properties are structured metadata stored as YAML at the top of each note. They power search, Bases, Publish, and community plugins.

### Format

```yaml
---
title: My Note
tags:
  - project
  - active
aliases:
  - My Alias
date: 2026-02-27
cssclasses:
  - wide-page
custom_property: some value
---
```

The `---` fences must be on the very first line of the file. Property names are case-sensitive. Each name must be unique within a note.

### Property Types

| Type | Example | Notes |
|---|---|---|
| Text | `title: "Hello"` | Single line. Wikilinks must be quoted: `link: "[Note](Note.md)"` |
| List | `tags:\n  - a\n  - b` | Each item on own line with `- ` |
| Number | `year: 2026` | Integer or decimal |
| Checkbox | `draft: true` | `true` or `false` |
| Date | `date: 2026-02-27` | YYYY-MM-DD |
| Date & time | `time: 2026-02-27T10:30:00` | ISO 8601 |

Property types are vault-wide — once a property name gets a type, all notes use that type for it.

### Default Properties

- **`tags`**: Tag list (the Tags type — special, only for this property)
- **`aliases`**: Alternative names for the note (used in link resolution)
- **`cssclasses`**: CSS classes applied to the note's rendering

### CLI Property Commands

```bash
# Read a property
obsidian property:read name=status file=Recipe

# Set a property (creates frontmatter if missing)
obsidian property:set name=status value=draft file=Recipe
obsidian property:set name=due value=2026-03-01 type=date file=Recipe

# Remove a property
obsidian property:remove name=status file=Recipe

# List all properties in vault (with counts)
obsidian properties counts sort=count

# List properties for a specific file
obsidian properties file=Recipe
```

### Direct Frontmatter Editing

When editing YAML directly:
1. If the file has no frontmatter, add `---\n...\n---\n` at line 1.
2. Parse existing YAML carefully — don't clobber other properties.
3. Lists use the `- item` syntax, indented under the key.
4. Quote values containing special YAML characters (`:`, `#`, `[`, `]`, etc.).
5. Wikilinks in properties must be quoted: `link: "[[Note]]"` (but prefer standard Markdown links).

---

## Tags

Tags categorize notes. They can appear inline in body text or in frontmatter.

### Inline Tags
```markdown
This is about #project-alpha and #status/active work.
```

### Frontmatter Tags
```yaml
---
tags:
  - project-alpha
  - status/active
---
```

### Tag Rules
- Valid characters: letters, numbers, `_`, `-`, `/` (for nesting)
- Must contain at least one non-numeric character (`#2026` is invalid, `#y2026` is valid)
- Case-insensitive (`#Tag` = `#tag`)
- No spaces — use kebab-case, camelCase, snake_case, or PascalCase
- Nested tags: `#parent/child` — searching `#parent` matches all descendants

### CLI Tag Commands
```bash
obsidian tags counts                    # All tags with counts
obsidian tags file=Recipe               # Tags for a specific file
obsidian tag name=project-alpha verbose # Files tagged with this tag
```

---

## Internal Links

### Link Syntax (Standard Markdown)

```markdown
[Note Title](Note%20Title.md)               # Link to note
[Section](Note%20Title.md#Heading)           # Link to heading
[Block](Note%20Title.md#^block-id)           # Link to block
[Custom Text](folder/Note.md)                # Custom display text
![](image.png)                                # Embed  image
![](Note.md)                                  # Embed note (prefix with !)
```

### Link Resolution
Obsidian resolves links by shortest unique filename. `[Recipe](Recipe.md)` matches `Cooking/Recipe.md` if there's only one file named `Recipe.md`. If ambiguous, use the full vault-relative path.

### Block IDs
A block ID lets you link to a specific paragraph, list item, or block quote. Place `^block-id` at the end of a paragraph (with a space before the caret) or on a separate line after structured blocks:

```markdown
This is a key insight about productivity. ^key-insight

> A profound quote about life.

^quote-1
```

Block IDs: alphanumeric + hyphens only.

### Embeds
Prefix any internal link with `!` to embed its content inline:
```markdown
![](Note.md)                    # Embed entire note
![](Note.md#Heading)            # Embed a section
![](Note.md#^block-id)          # Embed a block
![](image.png)                  # Embed image
![](<image.png|500>)            # Embed with width
![](document.pdf#page=3)        # Embed PDF page
```

### CLI Link Commands
```bash
obsidian backlinks file=Recipe           # What links TO this note
obsidian backlinks file=Recipe counts    # With link counts
obsidian links file=Recipe               # What this note links TO
obsidian unresolved                      # Broken links across vault
obsidian unresolved verbose              # Include source files
obsidian orphans                         # Notes with no incoming links
obsidian deadends                        # Notes with no outgoing links
```

---

## Backlinks

A backlink is a reference FROM another note TO the current note. If Note A links to Note B, then Note A is a backlink of Note B.

Obsidian tracks two types:
- **Linked mentions**: explicit links (`[Note B](Note%20B.md)` or `[[Note B]]`)
- **Unlinked mentions**: plain-text occurrences of the note's filename (can be converted to links)

Understanding backlinks is essential for vault maintenance — they reveal the connective structure of the knowledge base. Use `obsidian backlinks` and `obsidian orphans` to audit link health.

---

## Tasks

Obsidian recognizes Markdown task lists as actionable items:

```markdown
- [ ] Incomplete task
- [x] Completed task
- [-] Cancelled task
- [?] Question task
```

### CLI Task Commands
```bash
obsidian tasks                          # All tasks in vault
obsidian tasks todo                     # Only incomplete tasks
obsidian tasks done                     # Only completed tasks
obsidian tasks file=Recipe              # Tasks in specific file
obsidian tasks daily                    # Tasks from today's daily note
obsidian tasks verbose                  # With file paths and line numbers

# Toggle/update a task
obsidian task ref="Recipe.md:8" toggle  # Toggle completion
obsidian task daily line=3 done         # Mark daily note task done
obsidian task file=Recipe line=8 status=-  # Set custom status
```

---

## Daily Notes

Daily notes are date-stamped notes (typically `YYYY-MM-DD.md`) created automatically.

### CLI Daily Notes Commands
```bash
obsidian daily                          # Open today's daily note
obsidian daily:path                     # Get daily note path (even if not yet created)
obsidian daily:read                     # Read today's daily note
obsidian daily:append content="- [ ] Buy groceries"
obsidian daily:prepend content="## Morning\nStarted at 7am"
```

---

## Templates

Templates are note scaffolds stored in a configured templates folder.

### CLI Template Commands
```bash
obsidian templates                      # List available templates
obsidian template:read name=Meeting     # Read template content
obsidian template:read name=Meeting resolve  # Resolve {{date}}, {{time}}, {{title}}
obsidian template:insert name=Meeting   # Insert into active file

# Create a note from a template
obsidian create name="Team Standup" template=Meeting open
```

Template variables: `{{date}}`, `{{time}}`, `{{title}}` — resolved on insertion.

---

## Search

### CLI Search Commands
```bash
obsidian search query="meeting notes"           # Find matching files
obsidian search query="TODO" path=Projects       # Search within folder
obsidian search query="meeting" total            # Just the count
obsidian search:context query="meeting notes"    # With line context (grep-style)
obsidian search query="meeting" format=json      # JSON output
```

### Search Operators (for search query syntax)
- `file:recipe` — match filename
- `path:folder/` — match path
- `tag:#project` — match tag
- `[property:value]` — match property
- `line:(word1 word2)` — words on same line
- `section:(under heading)` — within a section
- `"exact phrase"` — literal match

---

## Bases

Bases are Obsidian's structured data views (`.base` files) — like databases built on top of your notes. They display note properties in table/list/cards/map views with filters, formulas, sorting, and grouping. All data lives in your `.md` files — bases just provide views.

**For full Bases syntax, formulas, functions, and examples, read `references/bases-reference.md`.**

### Quick Reference

A `.base` file is YAML with `filters`, `formulas`, `properties`, and `views` sections. You can also embed bases inline in notes using a ` ```base ``` ` code block.

### CLI Quirks (important)
- `base:views` only works on the **active file** — use `obsidian open path="X.base"` first
- `base:query` accepts `file=`/`path=` targeting without needing the base active
- `file=` for bases requires the `.base` extension: `file="Tasks.base"`, not `file="Tasks"`
- `base:create` + frontmatter in `content=` doesn't parse correctly — create the note, then use `property:set`

```bash
obsidian bases                                              # List all .base files
obsidian base:query file="Projects.base" format=json        # Query as JSON
obsidian base:query path="Projects.base" view="Active" format=csv
obsidian base:create path="Projects.base" name="New Item"   # Create in base
```

---

## Other CLI Commands

For the full command reference with all parameters, read `references/cli-reference.md`.

### Vault & Files
```bash
obsidian vault                          # Vault name, path, file/folder counts, size
obsidian vaults verbose                 # All known vaults with paths
obsidian files                          # List all files
obsidian files folder=Projects ext=md   # Filter by folder and extension
obsidian folders                        # List all folders
obsidian file file=Recipe               # File info (name, path, size, dates)
obsidian outline file=Recipe format=json # Heading structure
obsidian wordcount file=Recipe          # Word and character count
```

### Aliases
```bash
obsidian aliases                        # All aliases in vault
obsidian aliases file=Recipe            # Aliases for specific note
```

Aliases are defined in frontmatter as `aliases: [AI, Machine Intelligence]` and provide alternative names for link resolution.

### Bookmarks & Workspace
```bash
obsidian bookmarks                      # List bookmarks
obsidian bookmark file=Recipe           # Bookmark a file
obsidian workspace                      # Current layout
obsidian tabs                           # Open tabs
obsidian recents                        # Recently opened files
```

### Plugins & Commands
```bash
obsidian plugins                        # List installed plugins
obsidian plugin:enable id=dataview      # Enable/disable/install/reload plugins
obsidian commands                       # List all command IDs
obsidian command id="editor:toggle-bold" # Execute any command
```

### Developer & Advanced
```bash
obsidian eval code="app.vault.getFiles().length"  # Run JS in Obsidian
obsidian dev:screenshot path=screenshot.png
obsidian dev:errors                     # JS errors
```

### File History & Sync
```bash
obsidian diff file=Recipe               # List versions
obsidian diff file=Recipe from=1        # Compare latest version to current
obsidian history:restore file=Recipe version=2
obsidian sync:status                    # Sync status
```

---

## Vault Structure Conventions

A typical vault looks like:

```
MyVault/
├── .obsidian/           # Config: app.json, plugins/, themes/, snippets/
│   ├── app.json         # Core settings (useMarkdownLinks, etc.)
│   ├── appearance.json
│   ├── plugins/         # Community plugin data
│   └── workspace.json   # Current layout (changes frequently)
├── .trash/              # Obsidian trash (if configured)
├── Attachments/         # Images, PDFs, etc. (configurable location)
├── Templates/           # Note templates
├── Daily Notes/         # Daily notes (configurable)
├── Projects/
│   ├── Project Alpha.md
│   └── Project Beta.md
├── Archive/
└── README.md
```

The `.obsidian/` folder should generally not be edited directly except for `app.json` settings like `useMarkdownLinks`. The `workspace.json` file changes constantly and is a good `.gitignore` candidate.

---

## Common Workflows

### Create a new project note with properties and links
```bash
obsidian create name="Project Alpha" content="---\ntags:\n  - project\n  - active\ndate: 2026-02-27\n---\n\n# Project Alpha\n\n## Overview\n\n## Tasks\n\n- [ ] Define scope\n- [ ] Set timeline\n\n## Related\n\n- [Project Beta](Project%20Beta.md)\n" open
```

### Audit vault link health
```bash
obsidian unresolved verbose   # Find broken links
obsidian orphans              # Find disconnected notes
obsidian deadends             # Find notes that link nowhere
```

### Bulk-query tasks across vault
```bash
obsidian tasks todo verbose format=json  # All incomplete tasks with locations
```

### Quick-capture to daily note
```bash
obsidian daily:append content="- [ ] $(date +%H:%M) Review PR #42"
```

---

## Safety Guidelines

1. **Never overwrite without the `overwrite` flag** — `obsidian create` won't overwrite by default.
2. **Never permanently delete without confirmation** — prefer trash (`obsidian delete` defaults to trash).
3. **Use CLI for rename/move** — it auto-updates links. Direct filesystem renames break links.
4. **Preserve frontmatter** — when editing files directly, always parse and preserve the YAML block. Corrupted frontmatter breaks Properties, search, and Bases.
5. **Check `useMarkdownLinks` setting** — recommend enabling it if not already set.
6. **Don't edit `.obsidian/workspace.json`** — it changes constantly and conflicts with manual edits.
7. **Test before bulk operations** — when doing vault-wide changes (tag renames, property migrations), start with a dry-run or a single note.
8. **Place backups outside the vault** — if you copy a folder inside the vault for backup, Obsidian indexes it and double-counts tags/notes. Always back up to a location outside the vault root.
9. **Use `property:set` after `base:create`** — frontmatter in `base:create`'s `content=` parameter may not be parsed correctly. Create the note first, then set properties separately via `property:set`.
