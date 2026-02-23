---
name: atxp-backup
description: Free cloud backup for agent identity and memory files (.md only)
compatibility: Requires Node.js >=18 and npx
tags: [backup, identity, memory, agent-files, sync]
metadata:
  homepage: https://docs.atxp.ai
  source: https://github.com/atxp-dev/cli
  npm: https://www.npmjs.com/package/atxp
  requires:
    binaries: [node, npx]
    node: ">=18"
    env:
      - name: ATXP_CONNECTION
        description: Auth token (created by npx atxp@latest login or agent register)
        required: true
---

# ATXP Backup — Agent Identity & Memory Backup

Back up and restore your agent's `.md` files (SOUL.md, MEMORY.md, memory/*.md, AGENTS.md, USER.md, etc.) to ATXP servers. If your workspace is lost, pull your backup to a fresh machine and resume where you left off.

## Security Model

- **Only `.md` files** are collected and transmitted. No credentials, JSON configs, binaries, or other file types are ever sent.
- Files are sent to ATXP servers over **HTTPS**, associated with the authenticated agent's identity.
- `push` **replaces** the server snapshot entirely (latest snapshot only, no history).
- `pull` is **non-destructive** — it writes server files to the local directory but does not delete local files absent from the server.
- **Filesystem access**: reads from `--path` directory (push), writes to `--path` directory (pull). No other directories are touched.
- **No modification** of OpenClaw config or auth files.

## When to Use

| Situation | Command |
|-----------|---------|
| After meaningful changes to SOUL.md, MEMORY.md, or at end of session | `push` |
| Bootstrapping a fresh workspace or recovering from environment loss | `pull` |
| Verify backup exists before risky operations | `status` |

## Commands Reference

| Command | Description |
|---------|-------------|
| `npx atxp@latest backup push --path <dir>` | Recursively collect all `*.md` files from `<dir>` and upload to server |
| `npx atxp@latest backup pull --path <dir>` | Download backup from server and write files to `<dir>` |
| `npx atxp@latest backup status` | Show file count, total size, and last sync time |

### Options

| Option | Required | Description |
|--------|----------|-------------|
| `--path <dir>` | Yes (push/pull) | Directory to push from or pull to |

## Path Conventions

Typical OpenClaw workspace paths:

```
~/.openclaw/workspace-<id>/
~/.openclaw/workspace-<id>/SOUL.md
~/.openclaw/workspace-<id>/MEMORY.md
~/.openclaw/workspace-<id>/memory/
~/.openclaw/workspace-<id>/AGENTS.md
~/.openclaw/workspace-<id>/USER.md
```

## Limitations

- **`.md` files only** — all other file types are ignored during push and not present in pull.
- **Latest snapshot only** — each push overwrites the previous backup. There is no version history.
- **Requires ATXP auth** — run `npx atxp@latest login` or `npx atxp@latest agent register` first.
- **`--path` is required** — there is no auto-detection of workspace location.
