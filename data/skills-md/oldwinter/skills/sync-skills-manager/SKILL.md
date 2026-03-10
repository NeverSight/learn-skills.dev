---
name: sync-skills-manager
description: Manage synchronization workflows between repository skills and local system skill directories.
---

# Sync Skills Manager

Manage synchronization between repository skills and local/system skill directories.

## Scripts

### `sync-skills.sh` (canonical manager)

Sync between repository-canonical categories and runtime installs (`~/.claude/skills` + other agents).

| Command | Description |
|---------|-------------|
| `./sync-skills.sh diff` | Preview system-only skills |
| `./sync-skills.sh pull` | Sync `~/.claude/skills` -> repo (add new skills) |
| `./sync-skills.sh push` | Sync repo -> `~/.claude/skills` and refresh agent links |
| `./sync-skills.sh link-all` | Rebuild other agent dirs as symlinks to `~/.claude/skills` |
| `./sync-skills.sh dedupe` | Remove duplicate entries from `~/.gemini/skills` |
| `./sync-skills.sh status` | Show sync status |

### `sync-skills-3way.sh` (recommended)

Incremental 3-way sync across:

- `~/.codex/skills` (including `.system`)
- `~/.claude/skills` (canonical)
- repository skills tree

Key behavior:

- Incremental only (`rsync --update`), never deletes files.
- New skills missing in repo are added to `tools-skills/` by default (or legacy `system-skills/tools-skills/` if present).
- For duplicate skill names in repo, the newest `SKILL.md` copy is treated as canonical for repo -> local sync.

| Command | Description |
|---------|-------------|
| `./sync-skills-3way.sh sync` | Run 3-way incremental sync (default) |
| `./sync-skills-3way.sh status` | Show counts and name-level diffs |
| `./sync-skills-3way.sh help` | Show usage |

### `scripts/skills_profiles.py` (profiles manager)

Manage *which* skills are enabled per agent by creating/removing symlinks that point to the canonical registry (`~/.claude/skills`).

This solves two common issues:
- New skills created/edited in one tool (e.g. Codex) not showing up in others (e.g. Cursor).
- Too many skills loaded everywhere (context bloat) while still keeping one global registry.

**Config**
- Default config file: `system-skills/sync-skills-manager/skills-profiles.json`

**Safety model**
- `apply` and `normalize` default to **dry-run**. Use `--apply` to change files.
- Only “managed skills” are modified: a directory in the registry that contains `SKILL.md`.
- Non-skill folders (no `SKILL.md`, e.g. `dist/`) are treated as **unmanaged** and never touched.
- `normalize` always moves existing entries into a backup folder before replacing them with symlinks.

**Commands**
```bash
# Show registry + per-agent status
python3 system-skills/sync-skills-manager/scripts/skills_profiles.py status

# Preview what would change (desired vs current)
python3 system-skills/sync-skills-manager/scripts/skills_profiles.py diff

# 1) Sync Codex/registry/repo (incremental, no delete)
python3 system-skills/sync-skills-manager/scripts/skills_profiles.py sync

# 2) Normalize drift (copies/non-canonical links -> canonical symlinks, with backups)
python3 system-skills/sync-skills-manager/scripts/skills_profiles.py normalize --dry-run
python3 system-skills/sync-skills-manager/scripts/skills_profiles.py normalize --apply

# 3) Apply enable/disable sets (remove extra canonical links, add missing links)
python3 system-skills/sync-skills-manager/scripts/skills_profiles.py apply --dry-run
python3 system-skills/sync-skills-manager/scripts/skills_profiles.py apply --apply

# One-shot daily workflow (sync -> normalize -> apply)
python3 system-skills/sync-skills-manager/scripts/skills_profiles.py refresh --apply

# Manage by star ratings (1-7)
# Keep only 7-star skills (other agents). claude-code registry itself is skipped.
python3 system-skills/sync-skills-manager/scripts/skills_profiles.py stars --mode only --stars 7 --dry-run
python3 system-skills/sync-skills-manager/scripts/skills_profiles.py stars --mode only --stars 7 --apply

# Batch install by stars (e.g. add 6-star and 5-star)
python3 system-skills/sync-skills-manager/scripts/skills_profiles.py stars --mode install --stars 6,5 --apply

# Batch uninstall by stars
python3 system-skills/sync-skills-manager/scripts/skills_profiles.py stars --mode uninstall --stars 5 --apply
```

**Backups**
- Default backup root: `~/.claude/skills-backups/<timestamp>/<agent>/<skill>/...`

**Tests**
```bash
python3 -m unittest -q
```

### `scripts/agent_skills_audit.py` (agent installation + diff auditor)

Check which supported agents are installed locally, list recognized skills, and diff skill sets between agents.

```bash
# Scan all supported agents
python3 system-skills/sync-skills-manager/scripts/agent_skills_audit.py scan

# Only installed agents, with skills preview
python3 system-skills/sync-skills-manager/scripts/agent_skills_audit.py scan --installed-only --with-skills

# List full skills for selected agents
python3 system-skills/sync-skills-manager/scripts/agent_skills_audit.py skills --installed-only --agent codex,cursor

# Diff codex vs cursor
python3 system-skills/sync-skills-manager/scripts/agent_skills_audit.py diff --left codex --right cursor

# Diff one baseline against multiple agents
python3 system-skills/sync-skills-manager/scripts/agent_skills_audit.py diff --left codex --right cursor,amp,claude-code

# Sync check: compare installed agents against canonical claude-code
python3 system-skills/sync-skills-manager/scripts/agent_skills_audit.py sync-check --canonical-agent claude-code --installed-only

# Sync check for selected agents
python3 system-skills/sync-skills-manager/scripts/agent_skills_audit.py sync-check --canonical-agent claude-code --agent codex,cursor,amp
```

### `scripts/reclassify_system_skills.py` (category rebalancer)

Rebalance `system-skills` category distribution (defaults to reclassifying `tools-skills` into domain categories).

```bash
# Preview reclassification plan
python3 system-skills/sync-skills-manager/scripts/reclassify_system_skills.py --from-category tools-skills

# Apply reclassification
python3 system-skills/sync-skills-manager/scripts/reclassify_system_skills.py --from-category tools-skills --apply
```

### `scripts/flatten_system_skills_layout.py` (layout simplifier)

Flatten legacy `system-skills/<category>/<skill>` into repo-root `<category>/<skill>` while preserving `system-skills/sync-skills-manager/`.

```bash
# Preview flatten/migration actions
python3 system-skills/sync-skills-manager/scripts/flatten_system_skills_layout.py

# Apply migration actions
python3 system-skills/sync-skills-manager/scripts/flatten_system_skills_layout.py --apply
```

## Usage

### Daily 3-way sync
```bash
./sync-skills-3way.sh sync
```

### Quick status check
```bash
./sync-skills-3way.sh status
```

## Configuration

`sync-skills.sh` uses `sync-config.json`:

```json
{
  "system_skills_path": "~/.claude/skills",
  "repo_skills_path": "./",
  "exclude_patterns": ["sync-skills-manager"],
  "sync_mode": "incremental",
  "default_command": "diff"
}
```
