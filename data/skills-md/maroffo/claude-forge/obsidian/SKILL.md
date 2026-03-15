---
name: obsidian
description: "Obsidian vault operations via CLI. Use for note management, search, daily notes, knowledge graph analysis, tasks, properties. Not for Notion sync (use notion-sync)."
compatibility: "Requires Obsidian 1.12+ with CLI support and app running. macOS: /Applications/Obsidian.app/Contents/MacOS/obsidian"
---

# ABOUTME: Obsidian vault management via official CLI (1.12+)
# ABOUTME: CRUD, search, daily notes, tags, properties, graph analysis, tasks, templates

# Obsidian Vault Operations

**CLI reference:** See `../_OBSIDIAN.md` for full command reference.
**Integration:** See `../_SECOND_BRAIN.md` for category routing when adding knowledge.

## Capabilities

1. **Note CRUD**: create, read, append, prepend, move, delete
2. **Search**: full-text with folder filtering, JSON output
3. **Daily Notes**: read, append, prepend to today's note
4. **Tags & Properties**: list, set, read, remove frontmatter properties and tags
5. **Knowledge Graph**: backlinks, outgoing links, orphans, dead-ends, unresolved links
6. **Tasks**: list, toggle, mark done/todo across vault or daily note
7. **Templates**: list, read (with variable resolution), create from template
8. **History**: diff versions, restore from file recovery or sync

## Common Workflows

### Quick capture to daily note
```bash
obsidian daily:append content="- [ ] <task or note>" silent
```

### Find related notes
```bash
obsidian backlinks file=<name> counts
obsidian links file=<name>
```

### Vault health check
```bash
obsidian orphans total
obsidian deadends total
obsidian unresolved verbose
```

### Search and read
```bash
obsidian search query="<term>" matches limit=10
obsidian read file=<result>
```

### Add knowledge to Second Brain
```bash
# 1. Read existing content to check for duplicates
obsidian read file="Second Brain - <Topic>"
# 2. Append extracted content (follow _SECOND_BRAIN.md template)
obsidian append file="Second Brain - <Topic>" content="<extracted>"
# 3. Update timeline
obsidian append file="Second Brain - Timeline" content="- **YYYY-MM-DD** | [Topic] | Source: ..."
```

### Onboard project to vault
```bash
# Run the project onboarding protocol from _VAULT_CONTEXT.md
# Detects project info from CLAUDE.md, creates Overview/Log/Solutions, registers in MOC
# See _VAULT_CONTEXT.md "Project Onboarding" for full steps
```

## Fallback: Direct File Access

When the Obsidian CLI is unavailable (app not running, CLI errors, tool not found), access vault markdown files directly.

**Vault path:** `'/Users/maroffo/Library/Mobile Documents/iCloud~md~obsidian/Documents'`

- Use Read/Write/Edit/Glob/Grep tools on `.md` files in the vault path
- Note names map to `<vault>/<note name>.md` (subfolders for organized notes)
- Frontmatter is standard YAML between `---` delimiters
- Daily notes: `<vault>/Daily Notes/YYYY-MM-DD.md`
- Search: use Grep on vault path instead of `obsidian search`
- Append: use Edit tool to add content at end of file

## Rules

- Always use `silent` flag for create/append when user doesn't need the note opened
- Prefer `file=<name>` (wikilink resolution) over `path=` for convenience
- For Second Brain operations, follow `../_SECOND_BRAIN.md` routing
- Multiline content: use `\n` for newlines in content strings
- **CLI first, direct file access as fallback.** Try CLI; on failure, switch to direct access silently.
