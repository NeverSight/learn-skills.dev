---
name: find-skills
description: Discover and install third-party agent skills from the open skills ecosystem (skills.sh). This skill should be used when users want to find, install, update, or manage external skills for Claude Code or other AI agents, or when they mention skills.sh, npx skills, or want to extend their agent with community skills.
---

# Find Skills

Discover and install third-party agent skills from the open Agent Skills ecosystem powered by skills.sh.

## Overview

The **Agent Skills** format is an open standard for packaging procedural knowledge, workflows, and tools that AI agents load on demand. The `npx skills` CLI (maintained by Vercel Labs) serves as "npm for AI agents" -- enabling discovery and installation of community skills from any Git repository.

**skills.sh** is the public directory and leaderboard for the ecosystem, hosting thousands of skills across categories like frontend, backend, DevOps, and more.

### Built-in cc-arsenal Skills

Before installing third-party skills, note that cc-arsenal already provides:
- **agent-browser** -- AI-optimized headless browser automation (snapshot + refs system)
- **jira-cli** -- Interactive Jira issue, epic, and sprint management
- **skill-creator** -- Guide for creating new skills with progressive disclosure
- **find-skills** -- This skill (discovery and installation of third-party skills)

Only install external skills that provide capabilities not already covered above.

## Quick Start

### 1. Find Skills

```bash
# Interactive fuzzy search across skills.sh
npx skills find

# Search by keyword
npx skills find typescript
npx skills find react
npx skills find testing
```

### 2. Review Available Skills in a Repository

```bash
# List skills in a repository without installing
npx skills add owner/repo --list

# Example: list Vercel's official skills
npx skills add vercel-labs/agent-skills --list

# Example: list Anthropic's skills
npx skills add anthropics/skills --list
```

### 3. Install Skills

```bash
# Interactive installation (choose skills and target agents)
npx skills add owner/repo

# Install a specific skill for Claude Code
npx skills add owner/repo --skill skill-name -a claude-code

# Install globally (available across all projects)
npx skills add owner/repo --skill skill-name -a claude-code -g

# Install all skills from a repo to all detected agents
npx skills add owner/repo --all
```

## Essential Commands

| Command | Purpose |
|---------|---------|
| `npx skills find [query]` | Search skills.sh directory |
| `npx skills add <source>` | Install skills from a repository |
| `npx skills list` | View installed skills |
| `npx skills check` | Check for available updates |
| `npx skills update` | Update all installed skills |
| `npx skills remove [name]` | Uninstall a skill |
| `npx skills init [name]` | Create a new skill template |

## Installation Scopes

**Project scope** (default): Installs to `.claude/skills/` in the current project directory. Committed with the project and shared with team members.

**Global scope** (`-g` flag): Installs to `~/.claude/skills/` in the home directory. Available across all projects for the current user.

**Recommendation**: Install domain-specific skills (e.g., a framework skill) at project scope. Install general-purpose skills (e.g., code review, testing patterns) at global scope.

## Source Formats

The `add` command accepts multiple source formats:

```bash
# GitHub shorthand (most common)
npx skills add owner/repo

# Full GitHub URL
npx skills add https://github.com/owner/repo

# Direct path to a specific skill
npx skills add https://github.com/owner/repo/tree/main/skills/skill-name

# GitLab URL
npx skills add https://gitlab.com/org/repo

# Local directory (for development)
npx skills add ./my-local-skills
```

## Key Repositories

| Repository | Description |
|------------|-------------|
| `vercel-labs/agent-skills` | Vercel's official skill collection (React, Next.js, design) |
| `anthropics/skills` | Anthropic's example skills |
| `mgiovani/cc-arsenal` | This repository (browser, Jira, skill-creator, find-skills) |

## Reference Files

For detailed command reference, load: [references/commands.md](./references/commands.md)
- All CLI subcommands with complete flag documentation
- Source format details and installation paths
- Troubleshooting common issues

For discovery patterns and best practices, load: [references/workflows.md](./references/workflows.md)
- Discovery strategies by domain and framework
- Global vs project installation guidance
- Security review of skill sources
- Combining third-party skills with cc-arsenal
- Managing updates and versions

## Resources

- **Directory**: https://skills.sh
- **CLI Repository**: https://github.com/vercel-labs/skills
- **Open Specification**: https://agentskills.io
- **Anthropic Skills Docs**: https://code.claude.com/docs/en/skills
