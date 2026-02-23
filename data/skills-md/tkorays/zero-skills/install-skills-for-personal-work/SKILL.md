---
name: install-skills-for-personal-work
description: Automatically install all personal development skills in a fresh environment. Use when setting up a new computer, workspace, or when the user asks to configure/initialize their dev environment with required skills.
---

# Install Skills for Personal Work

## Overview

Quickly install personal development skills in any new environment using the `npx skills` CLI tool.

## When to Use

- First time working on a new computer
- Starting a new development project
- Entering a new workspace environment
- User asks to "configure dev environment", "install my skills", "add skill X", or "remove skill Y"

## Core Pattern

1. **Check current skills**: `npx skills list -g`
2. **Install/remove from user's skill list**: Use `--skill` flag for multi-skill repos
3. **Verify**: `npx skills list -g`

## Quick Reference

| Command | Purpose |
|---------|---------|
| `npx skills list -g` | List installed skills |
| `npx skills add <pkg> --skill <name> -g -y` | Install skill(s) |
| `npx skills remove <name> -g` | Remove skill |
| `npx skills find <query>` | Search for skills |

## Implementation

### Step 1: Check Current State

```bash
npx skills list -g
```

### Step 2: Install Skills

**Multi-skill repository (use `--skill` for each):**
```bash
npx skills add <owner>/<repo> --skill <skill-1> --skill <skill-2> -g -y
```

**Single skill package:**
```bash
npx skills add <skill-name> -g -y
```

### Step 3: Remove Skills

```bash
npx skills remove <skill-name> -g
```

### Step 4: Verify

```bash
npx skills list -g
```

## User's Personal Skill List

| Install Command | Description |
|----------------|-------------|
| `npx skills add obra/superpowers --skill brainstorming -g -y` | Brainstorming Ideas Into Designs |
| `npx skills add obra/superpowers --skill writing-plans -g -y` | Writing Plans |
| `npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices -g -y` | Vercel React Best Practices |
| `npx skills add anthropics/skills --skill skill-creator -g -y` | creating effective skills |
| `npx skills add supabase/agent-skills --skill supabase-postgres-best-practices -g -y` | Supabase Postgres Best Practices |
| `npx skills add wshobson/agents --skill sql-optimization-patterns -g -y` | SQL Optimization Patterns |
| `npx skills add kepano/obsidian-skills --skill obsidian-markdown -g -y` | Obsidian Flavored Markdown Skill |
| `npx skills add kepano/obsidian-skills --skill json-canvas -g -y` | JSON Canvas Skill |
| `npx skills add kepano/obsidian-skills --skill obsidian-bases -g -y` | Obsidian Bases Skill |
| `npx skills add ComposioHQ/awesome-claude-skills --skill video-downloader -g -y` | YouTube Video Downloader |
| `npx skills add Shubhamsaboo/awesome-llm-apps --skills project-planner -g -y` | Project Planner |
| `npx skills add vercel-labs/agent-browser --skill agent-browser -g -y` | Browser Automation with agent-browser |
| `npx skills add wshobson/agents --skill python-project-structure -g -y` | Python Project Structure & Module Architecture |
| `npx skills add wshobson/agents --skill python-packaging -g -y` | Python Packaging |
| `npx skills add anthropics/skills --skill pdf -g -y` | PDF Processing Guide |

## Common Mistakes

- **Forgetting --skill flag**: Always use `--skill` when installing from a multi-skill repository
- **Missing -y flag**: Required for non-interactive installation
- **Forgetting Node.js**: Ensure Node.js is installed (required for npx)
- **Wrong scope**: Use `-g` for global (user-level) installation
- **Network issues**: Check connection if install fails
