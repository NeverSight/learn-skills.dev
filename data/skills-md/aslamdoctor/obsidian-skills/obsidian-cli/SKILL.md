---
name: obsidian-cli
description: >
  Interact with Obsidian vaults using the Obsidian CLI (`obsidian` command).
  Use for any Obsidian-related task that can be accomplished from the terminal:
  creating/reading/editing notes, searching vaults, managing daily notes,
  working with properties/tags/links, managing tasks, handling plugins/themes,
  syncing, publishing, file history, and vault automation.
  Triggers when user mentions Obsidian, vaults, notes (in Obsidian context),
  daily notes, or wants to automate Obsidian workflows.
---

# Obsidian CLI

Control Obsidian vaults from the terminal using the `obsidian` command.

## Prerequisites

- Obsidian 1.12.4+ with CLI enabled (Settings > General > CLI)
- Obsidian app must be running (first command launches it if needed)
- For setup help, see [references/setup.md](references/setup.md)

## Command Syntax

```
obsidian [vault=<name>] <command> [params] [flags]
```

- **Parameters**: `key=value` (quote values with spaces: `content="Hello world"`)
- **Flags**: boolean switches like `open`, `overwrite`, `total`
- **Vault targeting**: `vault=<name>` before command, or `cd` into vault dir
- **File targeting**: `file=<name>` (wikilink/fuzzy) or `path=<path>` (exact from vault root)
- **Multiline**: `\n` for newlines, `\t` for tabs
- **Clipboard**: append `--copy` to any command

## Common Workflows

### Create and edit notes

```bash
obsidian create name="Meeting Notes" content="# Meeting\n\n- Topic:" open
obsidian create path="Projects/idea.md" template="Project Template"
obsidian read file="My Note"
obsidian append file="Journal" content="\n## New Entry\nContent here"
obsidian prepend file="Tasks" content="- [ ] New task"
```

### Daily notes

```bash
obsidian daily                              # Open today's daily note
obsidian daily:read                         # Read daily note contents
obsidian daily:append content="- Did X"     # Append to daily note
obsidian daily:path                         # Get path (even if not created)
```

### Search

```bash
obsidian search query="meeting" limit=10
obsidian search:context query="TODO" format=json
obsidian search query="keyword" path=Projects total
```

### Properties and tags

```bash
obsidian property:set name=status value=done file="Note"
obsidian property:read name=tags file="Note"
obsidian tags sort=count counts
obsidian tag name=project verbose
```

### Tasks

```bash
obsidian tasks todo                         # All incomplete tasks
obsidian tasks daily                        # Today's daily note tasks
obsidian task file=Recipe line=8 done       # Mark task complete
obsidian task daily line=3 toggle           # Toggle task status
```

### Links and graph analysis

```bash
obsidian backlinks file="Note"
obsidian links file="Note"
obsidian orphans                            # Files with no backlinks
obsidian deadends                           # Files with no outgoing links
obsidian unresolved counts                  # Broken links
```

### Plugins

```bash
obsidian plugins filter=community versions
obsidian plugin:install id=dataview enable
obsidian plugin:reload id=my-plugin
```

### Files and folders

```bash
obsidian files folder=Projects ext=md
obsidian folders
obsidian move file="Old" to="Archive/Old.md"
obsidian delete file="Trash Me"
```

## Full Command Reference

For complete command documentation with all parameters and flags, see [references/commands.md](references/commands.md).

Command categories: General, Files/Folders, Daily Notes, Search, Properties, Tags, Links, Tasks, Templates, Outline, Bookmarks, Bases, Plugins, Themes/Snippets, Sync, Publish, Vault, Workspaces/Tabs, Unique Notes, Word Count, Web Viewer, Random Notes, File History, Developer.

## Important Notes

- Always use `obsidian` as the command (not `obs` or other aliases)
- The Obsidian desktop app must be running for CLI commands to work
- When targeting a specific vault, place `vault=<name>` before the command
- Use `file=` for fuzzy/wikilink matching, `path=` for exact paths
- `format=json` is useful when parsing output programmatically
- `total` flag returns only the count instead of listing items
- `--copy` on any command copies output to system clipboard
