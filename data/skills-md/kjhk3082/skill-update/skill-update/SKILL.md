---
name: skill-update
description: Use when the user wants to check whether installed agent skills are outdated or update them - "update my skills", "are my skills up to date", "스킬 업데이트", "스킬 최신화" - for skills installed with npx skills, as git clones, or as Claude Code plugins, across Claude Code, Codex, Cursor, Gemini CLI and other agents.
---

# skill-update

Finds every skill installed on this machine, works out where each one came from, compares it with its upstream and updates what is outdated, with a backup first. The engine is `scripts/skill_update.py` (Python 3.9+, standard library; the network is only touched through `git`).

Run it as `python3 "<this skill's folder>/scripts/skill_update.py" ...`. The folder is the "Base directory" shown when this skill loads.

## Workflow

1. **Check** (changes nothing): `check --json`. A cold first run can take up to a minute.
2. **Summarize** for the user, in their language. Count what is outdated and list each outdated item with its name, source and size of change (`changes`). Call out separately:
   - `modified: true`: the user edited that skill, and an update overwrites the edits after a backup.
   - `setup_script: true`: a git clone with a setup script. A plain `update` leaves it out (see `skipped[]`). Offer to update it by name, and tell the user to run its setup script themselves.
   - `blocked`, `error`, `unknown`: say why, using `notes`. Do not retry in a loop.
   - `unmanaged`: only a count; these have no upstream to compare with.
3. **Ask** which to update (default: all outdated). Do not run `update` until the user agrees.
4. **Update**: `update --yes [names...]`. Add `--keep-modified` when the user wants their edits protected. Use `--dry-run` first when they want a preview. Naming a skill is the only way to update a `setup_script` clone.
5. **Report** `results` (updated, unchanged, failed) and `skipped[]` with each reason, plus the `run_id` and how to undo it: `rollback <run_id>`. Relay `notes`: plugin changes need a restart, and new skill versions load in a new session.

## Rules

- Never pass `--yes` before the user approved the list.
- Never run scripts that an updated skill ships (`setup`, `install.sh`, `npm install`). When a result mentions one, tell the user and let them decide.
- A source such as `owner/repo` can be passed to `check` and `update` to select everything from that source.
- A failure on one item never blocks the others; report it and move on.

## Commands

| Command | What it does |
|---|---|
| `check [--json] [--refresh] [names]` | List what is outdated. `--refresh` also refreshes the plugin marketplaces first. |
| `update [names] --yes [--dry-run] [--keep-modified] [--no-backup] [--refresh]` | Apply updates. `--no-backup` is refused while a skill has local edits. |
| `rollback [run_id] [--list]` | Undo an update run. |
| `scan` | Show which skill folders were found. |

Limit a run with `--only lock|git|plugin`, leave a skill out with `--ignore NAME`, scan another folder with `--root DIR`.

## JSON fields

`items[]`: `name`, `kind` (lock, git, plugin, unmanaged), `status` (outdated, current, blocked, unknown, error, unmanaged), `source`, `agents`, `locations`, `modified`, `setup_script` (only when true), `changes` (`added`, `modified`, `removed`, `files`), `notes`.
`update` returns `results[]` (`outcome`: updated, unchanged, failed), `skipped[]` (`name`, `reason`), `run_id` and `notes`.
