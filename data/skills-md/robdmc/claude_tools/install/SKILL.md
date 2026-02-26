---
name: install
description: Install Claude tools from this repository to global or project locations
allowed-tools: AskUserQuestion, Bash(python*), Read, Glob
argument-hint: [list]
---

# Install Skill

Discovers and installs Claude tools (skills, agents, commands) from this repository.

## Quick Reference

| Command | Action |
|---------|--------|
| `/install` | Interactive installation wizard |
| `/install list` | Show available tools |

## Workflow

### Step 1: Discover Available Tools

Run the discovery script:
```bash
python {SKILL_DIR}/install.py --list
```

This shows all tools in the repository with their components:
- **skills/** - Skill definitions with optional scripts/, references/, assets/
- **agents/** - Agent definition markdown files
- **commands/** - Legacy command markdown files

### Step 2: Present Numbered Tool List

Display the tools as a numbered list for the user:

```
Available tools:
  1. brainstorm    - skills + 3 agents
  2. duckdb_sql    - skills with references
  3. implement     - skills + task-worker agent
  4. presentation  - skills with scripts/references
  5. scribe        - skills with scripts/references
  6. viz           - skills with scripts/references
```

### Step 3: Gather User Choices

Use AskUserQuestion to get:

1. **Target location:**
   - Global (`~/.claude/`) - Available in all projects
   - Project (`.claude/`) - Only available in current project

2. **Installation mode:**
   - Copy - Files are copied (portable, independent)
   - Symlink - Links to source (updates automatically, requires repo access)

3. **Tools to install:**
   - Ask the user to enter tool numbers (e.g., "1,3,5" or "all")
   - Parse the response and map numbers back to tool names

### Step 4: Execute Installation

Run the installation with user choices:
```bash
python {SKILL_DIR}/install.py --install --target <global|project> --mode <copy|symlink> --tools <tool1,tool2,...>
```

### Step 5: Report Results

Show the user what was installed:
- Skills installed to `{target}/skills/{tool_name}/`
- Agents installed to `{target}/agents/` (flat)
- Commands installed to `{target}/commands/` (flat)

## Installation Mapping

| Source | Destination |
|--------|-------------|
| `{tool}/skills/` (entire tree) | `{target}/skills/{tool}/` |
| `{tool}/agents/*.md` | `{target}/agents/` (flat) |
| `{tool}/commands/*.md` | `{target}/commands/` (flat) |

## Example Session

```
User: /install

Claude: Available tools:
  1. brainstorm    - skills + 3 agents
  2. duckdb_sql    - skills with references
  3. implement     - skills + task-worker agent
  4. presentation  - skills with scripts/references
  5. scribe        - skills with scripts/references
  6. viz           - skills with scripts/references

[Uses AskUserQuestion for target and mode]
[Asks user: "Enter tool numbers to install (e.g., 1,3,5 or 'all'):"]

User selects: Global, Symlink, enters "1,6"

Claude: Installing brainstorm and viz...

[Runs: python install.py --install --target global --mode symlink --tools brainstorm,viz]

Installation complete!
  Linked skills/brainstorm/ -> /path/to/repo/brainstorm/skills
  Linked skills/viz/ -> /path/to/repo/viz/skills
  Linked agents/pragmatic-explorer.md
  Linked agents/creative-challenger.md
  Linked agents/devils-advocate.md
```

## Handling "list" Argument

If the user runs `/install list`, skip the interactive workflow and just display the tool list:
```bash
python {SKILL_DIR}/install.py --list
```

## Notes

- Symlink mode requires the repository to remain accessible
- Copy mode creates independent copies that won't auto-update
- Existing installations are replaced (no merge)
- The skill directory structure is preserved (SKILL.md, scripts/, references/, assets/)
