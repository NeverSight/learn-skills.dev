---
name: syncing-obsidian
description: Use when reading or writing files in an Obsidian vault that is synced with obsync. Ensures changes are pulled before reading and pushed after writing. Also covers sync status, file history, version restore, and diagnosing sync issues.
---

# Syncing Obsidian

Sync Obsidian vaults from the command line using the `obsync` CLI. Works with Obsidian Sync servers alongside official Obsidian clients.

## CRITICAL: Sync Before Reading, Sync After Writing

If `obsync watch` is running, the vault is kept in sync automatically — no manual sync is needed before reading or after writing.

If watch mode is **not** running, always sync manually:

**Before reading vault files**, pull the latest from the server:

```bash
obsync sync /path/to/vault
```

**After writing or modifying vault files**, push your changes:

```bash
obsync sync /path/to/vault
```

If you skip these steps and watch is not running, you will read stale content or your changes will not reach other devices.

`obsync sync` does both pull and push in one call, so it is safe to use in both cases.

## When to Use This Skill

Use this skill when:
- Reading files from an Obsidian vault (sync first to get latest)
- Writing or editing files in an Obsidian vault (sync after to push changes)
- The user asks to sync their vault
- Checking what files have changed or need syncing
- Viewing or restoring file version history
- Diagnosing why a file isn't syncing
- Setting up a new vault for syncing

## Setup (One-Time)

```bash
# Log in
obsync login

# List available vaults
obsync vaults

# Initialize a vault in a directory
obsync init <vault-id> /path/to/vault
```

After init, all commands run from within the vault directory (or pass the directory as the last argument).

## Common Operations

### Sync a vault

```bash
obsync sync [directory]
```

Pulls remote changes, resolves conflicts, then pushes local changes. If directory is omitted, uses the current working directory.

### Pull or push only

```bash
obsync pull [directory]   # download remote changes only
obsync push [directory]   # upload local changes only
```

### Watch and sync continuously

```bash
obsync watch [directory]
```

Keeps the WebSocket connection open, pulls remote changes in real-time via push notifications, and scans for local changes every 30 seconds. Reconnects automatically on connection loss. Stop with Ctrl+C.

Only one obsync process can run per vault (file lock in `.obsync/obsync.lock`). If watch is running, `obsync sync` will fail with a lock error — this is expected since watch handles syncing.

### Check sync status

```bash
obsync status [directory]
```

Shows vault info, file counts, and any files that have changed since last sync.

### View file history

```bash
obsync history "path/to/file.md" [directory]
```

Shows all versions with UID, timestamp, device, and size. Use the UID to restore.

### Restore a version

```bash
obsync restore "path/to/file.md" <version-uid> [directory]
```

### Run diagnostics

```bash
obsync diag [directory]
```

Tests connectivity, push/echo round-trip, vault size, and deleted file count.

### Debug mode

Add `--debug` before any command to see WebSocket messages and protocol details on stderr:

```bash
obsync --debug sync
```

## Reading the Activity Log

Every sync appends to `.obsync/sync.log` inside the vault:

```
2026-02-02 14:47:25 sync started
2026-02-02 14:47:26 pull "meeting.md" downloaded from server
2026-02-02 14:47:26 pull "draft.md" deleted (server deleted)
2026-02-02 14:47:26 pull "notes.md" kept local version
2026-02-02 14:47:26 push "new-note.md" uploaded (1234 bytes)
2026-02-02 14:47:26 push "old-note.md" server has current version
2026-02-02 14:47:26 sync complete
```

**Log entry meanings:**
- `downloaded from server` — server version was newer, wrote to disk
- `deleted (server deleted)` — file was deleted on another device, removed locally
- `kept local version` — local edits preserved over server changes
- `merged (text)` — both sides changed a markdown file, three-way merge applied
- `merged (json)` — both sides changed a config JSON, shallow merge applied
- `uploaded (N bytes)` — file pushed to server
- `server has current version` — server already had this version, no upload needed

## Diagnosing Sync Issues

### File not syncing up

```bash
obsync status
```

If the file doesn't appear as changed, it's already marked as synced. Run `obsync push` and check the activity log.

### File not syncing down

Run `obsync sync` and check `.obsync/sync.log`. If the file doesn't appear, the server hasn't sent a notification for it. Try `obsync --debug sync` and look for push notifications mentioning the file.

### Deletion not propagating

Deletions require the `initial` flag to be cleared. Run `obsync sync` once to clear it, then deletions from other devices will be processed on subsequent syncs.

### Checking the database directly

The sync state lives in `.obsync/state.db` (SQLite):

```bash
# Files that need pushing (changed locally since last sync)
sqlite3 .obsync/state.db "SELECT path FROM local_files WHERE hash != synchash"

# Server-side deleted files
sqlite3 .obsync/state.db "SELECT path FROM server_files WHERE deleted = 1"

# Current sync metadata
sqlite3 .obsync/state.db "SELECT * FROM metadata"
```

### Forcing a file to re-sync

Reset its sync state so it appears as changed:

```bash
sqlite3 .obsync/state.db "UPDATE local_files SET synchash='' WHERE path='path/to/file.md'"
obsync push
```

### Replaying missed server changes

Roll back the version cursor to re-receive push notifications:

```bash
# Check current version
sqlite3 .obsync/state.db "SELECT value FROM metadata WHERE key='last_version'"

# Roll back (e.g., by 10 versions)
sqlite3 .obsync/state.db "UPDATE metadata SET value='7040' WHERE key='last_version'"
obsync sync
```

## What Gets Synced

- All files in the vault regardless of extension
- Folders (as metadata entries)

## What Gets Excluded

- Dotfiles and dotfolders (`.git/`, `.obsidian/`, `.obsync/`)
- `workspace.json` and `workspace-mobile.json`
- Files larger than ~199 MB

Note: `.obsidian/` config files are synced by the server (they arrive as push notifications) even though the local scanner skips dotfolders.

## Conflict Resolution

When both local and remote changed the same file:

| File type | Resolution |
|-----------|-----------|
| Markdown (`.md`) | Three-way merge using common ancestor |
| JSON in `.obsidian/` | Shallow merge (server keys win, local-only keys kept) |
| Everything else | Local version wins |

A backup is saved before any merge.
