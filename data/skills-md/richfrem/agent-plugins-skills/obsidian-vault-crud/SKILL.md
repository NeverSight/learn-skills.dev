---
name: obsidian-vault-crud
description: "Safe Create/Read/Update/Delete operations for Obsidian Vault notes. Implements atomic writes, advisory locking, concurrent edit detection, and lossless YAML frontmatter handling. Use when reading, writing, updating, or appending to any vault note."
allowed-tools: Bash, Read, Write
dependencies: ["pip:ruamel"]
---
# Obsidian Vault CRUD

**Status:** Active
**Author:** Richard Fremmerlid
**Domain:** Obsidian Integration
**Depends On:** `obsidian-markdown-mastery` (WP05)

## Core Mandate

This skill provides the **disk I/O layer** for all agent interactions with the Obsidian Vault. It does NOT handle syntax parsing (that belongs to `obsidian-markdown-mastery`). Instead, it ensures that every file write is:

1. **Atomic** — via POSIX `os.rename()` from a `.tmp` staging file
2. **Locked** — via an advisory `.agent-lock` file at the vault root
3. **Conflict-aware** — via `mtime` comparison before/after read
4. **Lossless** — via `ruamel.yaml` for frontmatter (never PyYAML)

## Available Commands

### Read a Note
```bash
python ./scripts/vault_ops.py read --file <path>
```

### Create a Note
```bash
python ./scripts/vault_ops.py create --file <path> --content <text> [--frontmatter key=value ...]
```

### Update a Note
```bash
python ./scripts/vault_ops.py update --file <path> --content <text>
```

### Append to a Note
```bash
python ./scripts/vault_ops.py append --file <path> --content <text>
```

## Safety Guarantees

### Atomic Write Protocol
1. Write content to `<target>.agent-tmp`
2. Verify the `.agent-tmp` file was written completely
3. `os.rename('<target>.agent-tmp', '<target>')` — atomic on POSIX
4. If any step fails, the `.agent-tmp` is cleaned up

### Advisory Lock Protocol
- Before any write batch: create `<vault_root>/.agent-lock`
- After write batch completes: remove `.agent-lock`
- Other agents check for `.agent-lock` before writing
- This is advisory (does not block Obsidian UI)

### Concurrent Edit Detection
- Capture `os.stat(file).st_mtime` before reading
- Before writing, check `st_mtime` again
- If mtime changed → another process edited the file → **ABORT**

### Frontmatter Handling
- Uses `ruamel.yaml` (NOT `PyYAML`) to preserve comments, indentation, and array styles
- Ensures Dataview and Obsidian Properties remain intact
