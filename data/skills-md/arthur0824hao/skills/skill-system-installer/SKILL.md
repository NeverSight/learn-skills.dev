---
name: skill-system-installer
description: Install and update skills into the skill system from a curated list or a GitHub repo path. Use when a user asks to list installable skills, install a curated skill, update existing skills, or install a skill from another repo (including private repos).
metadata:
  short-description: Install and update skills from GitHub repos
---

# Skill Installer

Helps install skills. By default these are from https://github.com/openai/skills/tree/main/skills/.curated, but users can also provide other locations.

Use the helper scripts based on the task:
- List curated skills when the user asks what is available, or if the user uses this skill without specifying what to do.
- Install from the curated list when the user provides a skill name.
- Install from another repo when the user provides a GitHub repo/path (including private repos).

Install skills with the helper scripts.

## Communication

When listing curated skills, output approximately as follows, depending on the context of the user's request:
"""
Skills from {repo}:
1. skill-1
2. skill-2 (already installed)
3. ...
Which ones would you like installed?
"""

After installing a skill, tell the user: "Restart Codex to pick up new skills."

## Scripts

All of these scripts use network, so when running in the sandbox, request escalation when running them.

- `scripts/list-curated-skills.py` (prints curated list with installed annotations)
- `scripts/list-curated-skills.py --format json`
- `scripts/skills.sh` (unified wrapper for install, list, update, sync)
- `scripts/install-skill-from-github.py --repo <owner>/<repo> --path <path/to/skill> [<path/to/skill> ...]`
- `scripts/install-skill-from-github.py --url https://github.com/<owner>/<repo>/tree/<ref>/<path>`
- `scripts/update-skills.py --all`
- `scripts/update-skills.py --skill <skill-name> [--update] [--dry-run]`

## Update

Use `scripts/update-skills.py` to compare installed skill directories with hashes from `skills-lock.json`.

- `--all` checks every locked skill; `--skill <name>` checks one skill.
- Add `--update` to reinstall missing/drifted skills and refresh `computedHash`.
- Add `--dry-run` to report planned updates without making changes.
- Optional: `--lockfile <path>` and `--skills-dir <path>`.

## Behavior and Options

- Defaults to direct download for public GitHub repos.
- If download fails with auth/permission errors, falls back to git sparse checkout.
- Aborts if the destination skill directory already exists unless `--force` is set.
- Installs into `$CODEX_HOME/skills/<skill-name>` (defaults to `~/.codex/skills`).
- Multiple `--path` values install multiple skills in one run, each named from the path basename unless `--name` is supplied.
- Options: `--ref <ref>` (default `main`), `--dest <path>`, `--method auto|download|git`, `--force`.

## Notes

- Curated listing is fetched from `https://github.com/openai/skills/tree/main/skills/.curated` via the GitHub API. If it is unavailable, explain the error and exit.
- Private GitHub repos can be accessed via existing git credentials or optional `GITHUB_TOKEN`/`GH_TOKEN` for download.
- Git fallback tries HTTPS first, then SSH.
- The skills at https://github.com/openai/skills/tree/main/skills/.system are preinstalled, so no need to help users install those. If they ask, just explain this. If they insist, you can download and overwrite.
- Installed annotations come from `$CODEX_HOME/skills`.

```skill-manifest
{
  "schema_version": "2.0",
  "id": "skill-system-installer",
  "version": "1.0.0",
  "capabilities": ["skill-install", "skill-list", "skill-update", "skill-sync"],
  "effects": ["net.fetch", "fs.write", "proc.exec"],
  "operations": {
    "list": {
      "description": "List available curated skills with installed annotations and show local/global installed skills.",
      "input": {
        "format": { "type": "string", "required": false, "default": "text", "description": "Output format: text or json" }
      },
      "output": {
        "description": "List of curated skills with install status",
        "fields": { "skills": "array of {name, installed}" }
      },
      "entrypoints": {
        "unix": ["python3", "scripts/list-curated-skills.py", "--format", "{format}"],
        "windows": ["python", "scripts/list-curated-skills.py", "--format", "{format}"]
      }
    },
    "install": {
      "description": "Install a skill from GitHub repo path. The scripts/skills.sh wrapper provides a scoped alternative entrypoint.",
      "input": {
        "repo": { "type": "string", "required": true, "description": "GitHub owner/repo" },
        "path": { "type": "string", "required": true, "description": "Path to skill within repo" }
      },
      "output": {
        "description": "Installed skill path",
        "fields": { "installed_path": "string" }
      },
      "entrypoints": {
        "unix": ["python3", "scripts/install-skill-from-github.py", "--repo", "{repo}", "--path", "{path}"],
        "windows": ["python", "scripts/install-skill-from-github.py", "--repo", "{repo}", "--path", "{path}"],
        "unix_wrapper": ["bash", "scripts/skills.sh", "install", "--repo", "{repo}", "--path", "{path}"]
      }
    },
    "update": {
      "description": "Check skill drift against lockfile and optionally update drifted skills.",
      "input": {
        "scope": { "type": "string", "required": true, "description": "Either all or one" },
        "skill": { "type": "string", "required": false, "description": "Skill name when scope is one" },
        "apply": { "type": "boolean", "required": false, "default": false, "description": "Apply updates when true" },
        "dry_run": { "type": "boolean", "required": false, "default": false, "description": "Report only" }
      },
      "output": {
        "description": "Drift report and optional update actions",
        "fields": { "status": "ok | error", "table": "skill_name/local_hash/lock_hash/status" }
      },
      "entrypoints": {
        "unix": ["python3", "scripts/update-skills.py", "--all"],
        "windows": ["python", "scripts/update-skills.py", "--all"]
      }
    },
    "sync": {
      "description": "Synchronize global skills into the local workspace.",
      "input": {
        "strategy": { "type": "string", "required": false, "default": "copy", "description": "Sync strategy: copy or symlink" },
        "force": { "type": "boolean", "required": false, "default": false, "description": "Overwrite existing local skills when true" },
        "skills": { "type": "string", "required": false, "description": "Comma-separated skill names" }
      },
      "output": {
        "description": "Sync report and updated local lockfile",
        "fields": { "status": "ok | error", "skills": "array of synced or skipped skill names" }
      },
      "entrypoints": {
        "unix": ["bash", "scripts/skills.sh", "sync"]
      }
    }
  },
  "stdout_contract": {
    "last_line_json": false
  }
}
```
