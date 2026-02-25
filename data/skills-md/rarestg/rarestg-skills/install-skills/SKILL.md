---
name: install-skills
description: >-
  Install, discover, remove, and update agent skills using the npx skills CLI.
  Use when asked to install a skill, add a skill from a repo, find or search
  for skills, list installed skills, remove or uninstall a skill, update skills,
  or check for updates. Triggers on: "install X skill", "add the Y skill",
  "find skills for Z", "what skills are available", "remove skill", "update
  my skills", "check for skill updates", "search for a skill that does X".
---

# Install Skills

Manage skills using the `npx skills` CLI. All commands use `npx --yes` (skip npx install prompt) and `-a openclaw -y` (target OpenClaw, skip confirmation).

## Install scope: project vs global

- **Project** (default): installs to workspace. Skills work but are **not tracked** for `check`/`update`.
- **Global** (`--global`): installs to `~/.agents/skills/` and creates a lock file. Enables `check`/`update`.

Use `--global` for skills that should be kept up to date. Use project scope for experiments.

## List skills in a repo

Always list before installing an unfamiliar repo:

```bash
npx --yes skills add owner/repo --list -a openclaw -y
```

## Install a skill

```bash
# Project scope (no update tracking)
npx --yes skills add owner/repo --skill <skill-name> -a openclaw -y

# Global scope (enables check/update)
npx --yes skills add owner/repo --skill <skill-name> -a openclaw -y --global
```

Install one skill at a time unless explicitly asked to install multiple.

### Source formats

```bash
# GitHub shorthand (preferred)
npx --yes skills add owner/repo --skill <name> -a openclaw -y

# Full GitHub URL
npx --yes skills add https://github.com/owner/repo --skill <name> -a openclaw -y

# Direct path to a specific skill in a repo
npx --yes skills add https://github.com/owner/repo/tree/main/skills/my-skill -a openclaw -y

# Local path
npx --yes skills add ./my-local-skills --skill <name> -a openclaw -y
```

### Install all skills from a repo

```bash
npx --yes skills add owner/repo --skill '*' -a openclaw -y
```

## Verify installed skills

```bash
npx --yes skills list -a openclaw
npx --yes skills list -a openclaw --global
```

## Find skills

Search the skills directory by keyword:

```bash
npx --yes skills find <query>
```

## Remove a skill

```bash
npx --yes skills remove <skill-name> -a openclaw -y
npx --yes skills remove <skill-name> -a openclaw -y --global
```

## Check for updates and update

Requires skills to have been installed with `--global`:

```bash
npx --yes skills check
npx --yes skills update
```

## Defaults

- Prefer GitHub shorthand `owner/repo` over full URLs.
- `--list` before installing an unfamiliar repo.
- One skill at a time unless asked otherwise.
- Always `-a openclaw -y` for deterministic, non-interactive installs.
- Use `--global` when the user wants skills kept up to date.
