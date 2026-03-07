---
name: project-directory-migration
description: Migrate Claude Code project sessions when renaming directories. TRIGGERS - directory rename, move project, migrate sessions, project path change, workspace reorganization, rename folder.
allowed-tools: Read, Bash, Glob, Grep, AskUserQuestion
---

# Project Directory Migration

> Safely migrate Claude Code project context (sessions, memory, history) when renaming a project directory.

## When to Use This Skill

Use this skill when:

- Renaming a project directory (e.g., `my-old-name/` to `my-new-name/`)
- Moving a project to a different path
- User says "No conversations found" after a directory rename
- Reorganizing workspace directories
- Package rename requires matching directory name to GitHub repo name
- Recovering sessions that became orphaned after a directory move

## Interactive Workflow

### Phase 1: Gather Facts

Use AskUserQuestion to collect source and target paths.

```
Question 1 (header: "Source"): "What is the current project directory path?"
  Options:
    - "Use current directory: $PWD" (Recommended)
    - "Specify a different path"

Question 2 (header: "Target"): "What should the new directory path be?"
  Options:
    - (User provides via "Other" free text)
```

### Phase 2: Dry-Run Audit

Run the migration script in `--dry-run` mode to discover what needs migrating:

```bash
bash "<skill-scripts>/claude-code-migrate.sh" --dry-run "$OLD_PATH" "$NEW_PATH"
```

Present findings to user:

- Number of session files found
- Number of history.jsonl entries to rewrite
- Whether auto-memory (MEMORY.md) exists
- Environment tooling detected (mise, uv, direnv, asdf)

### Phase 3: Scope and Confirm

```
Question 3 (header: "Scope", multiSelect: true):
  "What should be included in migration?"
  Options:
    - "Claude Code sessions + history (Recommended)"
    - "Auto-memory (MEMORY.md) (Recommended)"
    - "Backward-compatibility symlink (Recommended)"
    - "Auto-fix environment: mise trust, venv recreate (Recommended)"

Question 4 (header: "Execute"):
  "Ready to migrate? The script creates a timestamped backup first."
  Options:
    - "Execute migration now (Recommended)"
    - "Export copy-paste commands for manual execution"
    - "Cancel"
```

**If user chooses "Export copy-paste commands"**: Generate the exact commands they can paste into their terminal after closing Claude Code. This is the safest option since Claude Code won't be accessing the project files during migration.

### Phase 4: Post-Migration Report

After migration completes, report:

- Sessions migrated, history entries rewritten
- Environment fixups applied (mise trust, venv recreated)
- Remaining manual steps (git remote update, etc.)
- Rollback command if anything goes wrong

---

## Quick Reference

### Claude Code Path Encoding

Claude Code encodes directory paths by replacing `/` with `-`:

```
/Users/alice/projects/my-app  -->  -Users-alice-projects-my-app
```

### Storage Locations

| Asset         | Location                                                    |
| ------------- | ----------------------------------------------------------- |
| Sessions      | `~/.claude/projects/{encoded-path}/*.jsonl`                 |
| Memory        | `~/.claude/projects/{encoded-path}/memory/MEMORY.md`        |
| Session index | `~/.claude/projects/{encoded-path}/sessions-index.json`     |
| History       | `~/.claude/history.jsonl`                                   |
| Subagents     | `~/.claude/projects/{encoded-path}/{session-id}/subagents/` |

### What Contains Path References

| File                   | Fields with paths                                             | Needs rewriting? |
| ---------------------- | ------------------------------------------------------------- | ---------------- |
| `sessions-index.json`  | `originalPath`, `entries[].projectPath`, `entries[].fullPath` | **Yes**          |
| `history.jsonl`        | `project` field per entry                                     | **Yes**          |
| Session `.jsonl` files | None                                                          | No               |
| `MEMORY.md`            | None (content only)                                           | No               |

---

## Migration Script

Located at `scripts/claude-code-migrate.sh`.

### Usage

```bash
# Dry run (preview what would happen)
bash scripts/claude-code-migrate.sh --dry-run /old/path /new/path

# Execute migration
bash scripts/claude-code-migrate.sh /old/path /new/path

# Rollback from most recent backup
bash scripts/claude-code-migrate.sh --rollback

# Show help
bash scripts/claude-code-migrate.sh --help
```

### 9-Phase Execution

1. **Pre-flight validation** — 7 checks (paths, Claude Code dir, python3, no running sessions)
2. **Backup** — Timestamped copy to `~/.claude/migration-backup-YYYYMMDD-HHMMSS/`
3. **Move project directory** — Rename in `~/.claude/projects/`
4. **Rewrite sessions-index.json** — Update projectPath, fullPath, originalPath
5. **Rewrite history.jsonl** — Update project field (JSON-safe, preserves Unicode)
6. **Backward-compatibility symlink** — Old encoded path symlinks to new
7. **Rename repo directory** — `mv /old/path /new/path`
8. **Environment fixups** — mise trust, venv recreate, direnv/asdf warnings
9. **Post-flight verification** — Sessions count, memory, symlink, env health

---

## Reference Documentation

- [Session Storage Anatomy](./references/session-storage-anatomy.md) — How Claude Code stores project data
- [Troubleshooting Guide](./references/troubleshooting.md) — Common post-migration issues and fixes
- [Evolution Log](./references/evolution-log.md) — Skill improvement history

---

## Troubleshooting

| Issue                         | Auto-fixed?          | Manual Solution                        |
| ----------------------------- | -------------------- | -------------------------------------- |
| mise trust error after rename | **Yes** (Phase 8)    | `mise trust <new-path>`                |
| `(old-name)` in shell prompt  | **Yes** (Phase 8)    | Restart terminal or `uv sync`          |
| VIRTUAL_ENV path mismatch     | **Yes** (Phase 8)    | `uv sync --dev` recreates venv         |
| "No conversations found"      | **Yes** (Phase 4)    | Re-run migration script                |
| `.envrc` not allowed          | **Warned** (Phase 8) | `direnv allow`                         |
| Git push auth fails           | No                   | Update credential helper or remote URL |
| Session subdirs missing       | No                   | Use `--rollback`, retry                |
