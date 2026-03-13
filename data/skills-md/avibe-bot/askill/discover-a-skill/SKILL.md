---
name: discover-a-skill
slug: discover-a-skill
description: "Use when you need new capabilities: discover skills, inspect details, install to agents, run commands, and manage updates with askill"
version: 1.0.1
author:
  name: askill
  github: askill
tags:
  - official
  - askill
  - workflow
---

# Discover a Skill

Use this skill when you need to operate askill reliably as an AI agent: discover skills, install them, run commands, maintain updates, and troubleshoot install/runtime issues.

## Core Workflow

When a user asks for a capability that might be implemented as a skill:

1. Discover candidates: `askill find <query>`
2. Inspect details: `askill info <slug>`
3. Install: `askill add <source> -y`
4. Read installed instructions: `<skill-dir>/SKILL.md`
5. Execute commands if defined: `askill run <skill>:<command> [args]`

Always prefer reading the installed `SKILL.md` before improvising.

## Source Formats You Should Use

Use any supported install source:

- `@author/skill-name` - published skill slug from askill registry
- `owner/repo` - discover and install from a GitHub repo
- `owner/repo@skill-name` - install one named skill
- `owner/repo/path/to/skill` - install by explicit folder path
- `gh:owner/repo@skill-name` - explicit GitHub-prefixed format
- `https://github.com/owner/repo` - full GitHub URL
- `./local/path` - local skill directory for testing

Notes:

- `askill install`, `askill add`, and `askill i` are equivalent
- Prefer explicit, non-interactive calls (`-y`) in agent workflows

## Installation Patterns

### Non-interactive (agent-safe)

```bash
# Published skill slug
askill add @johndoe/awesome-tool -y

# Indexed GitHub skill slug
askill add gh:owner/repo@skill-name -y
```

### Install all discovered skills from a repo

```bash
askill add gh:owner/repo --all -y
```

### Preview before install

```bash
askill add gh:owner/repo --list
```

### Target specific agents

```bash
askill add gh:owner/repo@skill-name -a claude-code opencode -y
```

### Global install

```bash
askill add gh:owner/repo@skill-name -g -y
```

### Copy mode (avoid symlink)

```bash
askill add gh:owner/repo@skill-name --copy -y
```

## Where Skills Are Installed

askill installs to canonical directories and links into agent-specific paths.

- Project canonical: `.agents/skills/<skill>/`
- Global canonical: `~/.agents/skills/<skill>/`
- Agent paths: `.claude/skills/`, `.opencode/skills/`, `.cursor/skills/`, etc.

State and metadata:

- Lock file: `~/.agents/.skill-lock.json`
- Credentials: `~/.askill/credentials.json`
- Preferences: `~/.config/askill/config.json`

## Running Skill Commands

If the skill defines `commands` in frontmatter, run:

```bash
askill run <skill>:<command> [args...]
```

Examples:

```bash
askill run memory:save --key preference --value "TypeScript"
askill run memory:recall --key preference
askill run my-skill:_setup
```

Rules:

- Read available commands from the installed `SKILL.md`
- If command fails from missing dependencies, try `_setup` first
- Pass user arguments through after the command target

## Maintenance Commands

Use these routinely:

- `askill list` - show installed skills
- `askill check` - check update availability
- `askill update` - update tracked GitHub-installed skills
- `askill remove <skill>` - uninstall
- `askill validate [path]` - validate SKILL.md format

## Submit vs Publish

Treat these as different workflows:

- `askill submit <github-url>`: request indexing (and slug-driven publish pipelines)
- `askill publish [path]`: local publish, requires login token, author = logged-in user
- `askill publish --github <blob-url>`: GitHub publish, no login required, author = repo owner

Publishing requires frontmatter `slug` and `version`:

```yaml
---
name: my-skill
slug: my-skill
version: 1.0.0
---
```

## Troubleshooting Checklist

When something fails, check in this order:

1. Source is valid and reachable (`gh:` slug, URL, or local path)
2. Skill exists and parsed correctly (`askill add ... --list`, `askill info ...`)
3. Skill actually defines the command (`commands:` in installed `SKILL.md`)
4. `_setup` has run if runtime dependencies are needed
5. User is authenticated for publish (`askill whoami`)

## Agent Behavior Guidelines

- Prefer deterministic commands with `-y` for automation
- Do not assume command names; read installed `SKILL.md`
- Use `askill run` instead of running scripts by hardcoded paths
- Prefer explicit agent targeting with `-a` when environment is multi-agent
- Surface actionable errors and next commands when a step fails
