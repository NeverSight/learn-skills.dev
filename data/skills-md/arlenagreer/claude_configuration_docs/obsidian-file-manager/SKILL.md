---
name: obsidian-file-manager
description: >
  Manage documentation files in an Obsidian vault via the official Obsidian CLI (v1.12.4+)
  or direct file access. Use when creating session artifacts, moving planning documents to
  the vault, updating document lifecycle states (active/processed/archived), searching vault
  by tags or content, automating archival of old documents, reading/appending to daily notes,
  managing properties and tags, or integrating with task-startup/task-wrapup workflows.
allowed-tools: Bash(ruby *), Bash(obsidian *)
---

# Obsidian File Manager

Vault file management via the official Obsidian CLI with direct-file fallback.

## Vault

```
Path: /Users/arlenagreer/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian Vault
Name: Obsidian Vault
```

## Quick Reference: CLI Commands

For vault operations, prefer the `obsidian` CLI directly when no script workflow is needed:

```bash
# Search
obsidian search query="my topic"
obsidian search query="my topic" format=json

# Read/write
obsidian read path="folder/note.md"
obsidian create path="folder/note.md" content="# Title"
obsidian append path="folder/note.md" content="New content"
obsidian prepend path="folder/note.md" content="Top content"

# Move (link-safe — preserves all internal links)
obsidian move path="old/note.md" to="new/folder"

# Properties
obsidian property:set name="lifecycle" value="processed" path="folder/note.md"
obsidian property:read name="lifecycle" path="folder/note.md"

# Tags and structure
obsidian tags counts
obsidian files folder="sessions" ext=md
obsidian backlinks file="My Note"
obsidian orphans

# Daily notes
obsidian daily:read
obsidian daily:append content="- Meeting notes here"
```

## Script Operations

Use scripts for workflows requiring naming conventions, frontmatter generation, and lifecycle management.

### create — Create new document with proper naming and tags

```bash
ruby ${CLAUDE_SKILL_DIR}/scripts/create_in_vault.rb \
  --type session --project myproject \
  --subject "feature work" \
  --content "# Session Notes\n\n..."
```

### move — Move external file into vault (link-safe via CLI)

```bash
ruby ${CLAUDE_SKILL_DIR}/scripts/move_to_vault.rb \
  --source /path/to/doc.md --type plan --project myproject
```

### update-lifecycle — Transition document lifecycle state

```bash
ruby ${CLAUDE_SKILL_DIR}/scripts/update_lifecycle.rb \
  --path sessions/myproject/session_myproject_20260310.md \
  --lifecycle processed
```

### search — Search vault with structured filters

```bash
ruby ${CLAUDE_SKILL_DIR}/scripts/search_vault.rb \
  --query "project:myproject lifecycle:active type:session"
```

### archive — Auto-archive old documents by retention policy

```bash
ruby ${CLAUDE_SKILL_DIR}/scripts/auto_archive.rb --dry-run
```

## File Organization

Files follow `{type}/{project}/filename.md` partitioning:

| Type | Directory | Purpose |
|------|-----------|---------|
| session | sessions/{project}/ | Development session artifacts |
| plan | planning/{project}/ | Implementation plans |
| prd | projects/{project}/ | Product requirements |
| adr, decision | decisions/{project}/ | Architecture decisions |
| investigation | investigations/{project}/ | Research and analysis |
| resource | resources/{project}/ | Reference materials |

Filenames use snake_case: `{type}_{subject}_{project}[_{date}][_{counter}].md`

## Lifecycle States

| State | Auto-Archive | Description |
|-------|-------------|-------------|
| master | Never | Reference docs |
| active | Never | Currently in use |
| processed | After 30 days | Work complete |
| trash | After 7 days | Abandoned |
| archived | N/A | Long-term storage |

## Fallback Behavior

All scripts try the CLI first. When Obsidian is not running, they fall back to direct file operations against the vault path. The CLI is preferred because `obsidian move` preserves internal links, and `obsidian search` uses the full index.

## Additional References

- For full parameter docs for each script, see [references/operations.md](references/operations.md)
- For vault config and tag system details, see [references/configuration.md](references/configuration.md)
- For workflow integration patterns, see [references/integration.md](references/integration.md)
