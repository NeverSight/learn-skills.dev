---
name: install-skills
description: 'Automatically install and manage Agent Skills from GitHub repositories. Use when asked to "install a skill", "add a skill", "find skills", "browse skills", "get skills from GitHub", or when the user needs a specific capability that might exist as a community skill. Supports anthropics/skills, github/awesome-copilot, and custom GitHub repositories.'
---

# Install Skills

A meta-skill for discovering, browsing, and installing Agent Skills from online repositories. This skill helps you find and install community-created skills to enhance your capabilities.

## skills.sh CLI Integration

If the user has the [skills.sh](https://skills.sh/) CLI installed (via `npx add-skill`), these scripts will automatically detect it and use the skills.sh CLI instead of the manual installation process. This provides:

- **Better cross-agent compatibility**: Automatic detection and installation for Claude Code, OpenCode, Cursor, and other agents
- **Auto-detection of agents**: The CLI knows where to install skills for each installed agent
- **Access to skills registry**: Browse and install from the community skills marketplace

To use the skills.sh CLI directly:
```bash
# List skills from a repository
npx add-skill anthropics/skills --list

# Install a specific skill
npx add-skill anthropics/skills --skill release-notes

# Install to global/personal directory
npx add-skill anthropics/skills -g
```

## When to Use This Skill

- User asks to "install a skill", "add a skill", or "get a skill"
- User mentions needing capabilities that might exist as community skills
- User wants to browse available skills from known repositories
- User wants to install a skill from a specific GitHub repository
- User asks "what skills are available?"

## Supported Skill Sources

### Primary Repositories

| Repository | Description |
|------------|-------------|
| `anthropics/skills` | Official Anthropic skills collection |
| `github/awesome-copilot` | GitHub's community-curated skills in `skills/` directory |
| `microsoft/agent-skills` | Skills for Microsoft AI SDKs and Azure services in `.github/skills/` directory |

### Custom Repositories

Any GitHub repository with skills in one of these structures:
- `skills/<skill-name>/SKILL.md`
- `.github/skills/<skill-name>/SKILL.md`
- `.claude/skills/<skill-name>/SKILL.md`

## Installation Locations

Skills can be installed to:

| Location | Scope | Path |
|----------|-------|------|
| Project | Current repo only | `.github/skills/<skill-name>/` |
| Personal | All projects | `~/.copilot/skills/<skill-name>/` |

**Default**: Project skills (`.github/skills/`) - only install to personal profile if user explicitly requests it

## Workflow: Browse Available Skills

### Step 1: List Skills from Known Repositories

Use the `scripts/list-skills.sh` script:

```bash
# List skills from default repository (anthropics/skills)
./scripts/list-skills.sh

# List skills from a specific repository
./scripts/list-skills.sh anthropics/skills
./scripts/list-skills.sh github/awesome-copilot
```

### Step 2: Display Skills to User

Present skills in a table format:

| Skill Name | Repository | Description |
|------------|------------|-------------|
| skill-name | source/repo | Brief description from SKILL.md |

### Step 3: Get Skill Details

Fetch and display the SKILL.md content for any skill the user is interested in.

## Workflow: Install a Skill

**IMPORTANT**: Always use the scripts in `scripts/` folder to install skills. Do NOT manually fetch and write skill files.

### Step 1: Identify the Skill Source

Parse the user's request to determine:
- Skill name
- Source repository (default to searching known repos)
- Installation scope (project by default, personal only if user explicitly requests)

### Step 2: Run the Install Script

Use the `scripts/install-skill.sh` script to install the skill:

```bash
# For project installation (DEFAULT)
./scripts/install-skill.sh <skill-name> <source-repo> .github/skills

# For personal installation (only if user explicitly requests)
./scripts/install-skill.sh <skill-name> <source-repo> ~/.copilot/skills
```

The script handles:
- Creating the destination directory
- Fetching the skill via sparse checkout
- Trying multiple skill locations (skills/, .github/skills/, .claude/skills/)
- Copying all skill files (SKILL.md, scripts/, references/, assets/, templates/, etc.)
- Displaying the skill description

### Step 3: Confirm Installation

The script will output:
- Skill name installed
- Installation location
- Brief description of what the skill does

## Workflow: Search for Skills

When the user describes a capability they need:

1. Search known repositories for skills with matching keywords
2. Read SKILL.md descriptions to find relevant matches
3. Present options to the user
4. Install the selected skill

## Workflow: Install from Custom Repository

When given a GitHub URL or owner/repo reference:

1. Parse the repository reference
2. Check for skills in standard locations:
   - `skills/`
   - `.github/skills/`
   - `.claude/skills/`
3. List available skills
4. Install selected skill(s)

## Example Commands

| User Says | Action |
|-----------|--------|
| "Install the webapp-testing skill" | Run `./scripts/install-skill.sh webapp-testing <repo> .github/skills` |
| "What skills are available?" | Run `./scripts/list-skills.sh` for known repos |
| "Install pdf skill from anthropics/skills" | Run `./scripts/install-skill.sh pdf anthropics/skills .github/skills` |
| "I need help with image manipulation" | Search for relevant skills with list script, suggest matches |
| "Add the github-issues skill to this project" | Run `./scripts/install-skill.sh github-issues <repo> .github/skills` |
| "Install skill to my personal profile" | Run `./scripts/install-skill.sh <skill> <repo> ~/.copilot/skills` |
| "Install all skills from anthropics/skills" | Batch install using the install script for each |

## Installation Scripts

This skill includes helper scripts in `scripts/` that MUST be used for all installation operations:

### scripts/install-skill.sh

```bash
# Usage: ./scripts/install-skill.sh <skill-name> [source-repo] [install-path]

# Install to project (default)
./scripts/install-skill.sh webapp-testing anthropics/skills .github/skills

# Install to personal profile (only when user explicitly requests)
./scripts/install-skill.sh webapp-testing anthropics/skills ~/.copilot/skills
```

### scripts/list-skills.sh

```bash
# Usage: ./scripts/list-skills.sh [source-repo]

./scripts/list-skills.sh                    # Lists from anthropics/skills
./scripts/list-skills.sh github/awesome-copilot  # Lists from specific repo
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Skill not found | Check spelling, try searching with keywords |
| Permission denied | Ensure write access to installation path |
| Skill conflicts | Check for existing skill with same name |
| Missing dependencies | Read skill's prerequisites section |

## Post-Installation

After installing a skill:
1. **Restart the CLI** to load the new skill (exit and reopen your terminal session)
2. Once restarted, Copilot will automatically load it when relevant based on the description

## Uninstalling Skills

To remove an installed skill:

```bash
# Personal skill
rm -rf ~/.copilot/skills/<skill-name>

# Project skill
rm -rf .github/skills/<skill-name>
```
