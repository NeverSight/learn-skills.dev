---
name: uninstall
description: Uninstall Claude tools from global or project locations
allowed-tools: AskUserQuestion, Bash(python*), Read, Glob
argument-hint: [list]
---

# Uninstall Skill

Safely removes installed Claude tools (skills, agents, commands) from global or project locations.

## Quick Reference

| Command | Action |
|---------|--------|
| `/uninstall` | Interactive uninstall wizard |
| `/uninstall list` | Show installed tools |

## Workflow

### Handling "list" Argument

If the user runs `/uninstall list`, skip the interactive workflow and show installed tools for both locations:

```bash
python {SKILL_DIR}/uninstall.py --target global --list
python {SKILL_DIR}/uninstall.py --target project --list
```

### Step 1: Choose Target Location

Use AskUserQuestion to ask:

**Where do you want to uninstall from?**
- Global (`~/.claude/`) - Tools available in all projects
- Project (`.claude/`) - Tools only in current project

### Step 2: Show Installed Tools

Run the discovery script:
```bash
python {SKILL_DIR}/uninstall.py --target <choice> --list
```

This shows all installed tools with their components and installation mode (symlink/copy).

### Step 3: Select Tools to Remove

If there are installed tools:
1. Display them as a numbered list
2. Ask the user to enter tool numbers (e.g., "1,2" or "all")
3. Parse the response and map numbers back to tool names

If no tools are installed, inform the user and end the workflow.

### Step 4: Execute Uninstall

Run the uninstall with user choices:
```bash
python {SKILL_DIR}/uninstall.py --target <choice> --tools <tool1,tool2,...>
```

### Step 5: Report Results

Show the user what was removed:
- Skills removed from `{target}/skills/{tool_name}/`
- Agents removed from `{target}/agents/`
- Commands removed from `{target}/commands/`

## Example Session

```
User: /uninstall

[Uses AskUserQuestion for target selection]

User selects: Global

[Runs: python uninstall.py --target global --list]

Claude: Installed tools in ~/.claude:
  1. brainstorm - skills/brainstorm/ (symlink), 3 agents
  2. viz        - skills/viz/ (symlink)

Enter tool numbers to uninstall (e.g., 1,2 or 'all'):

User enters: 1

Claude: Uninstalling brainstorm...

[Runs: python uninstall.py --target global --tools brainstorm]

Removing brainstorm...
  Unlinked skills/brainstorm/
  Unlinked agents/pragmatic-explorer.md
  Unlinked agents/creative-challenger.md

Uninstall complete!
```

## Safety Features

- Only operates on `~/.claude/` or `.claude/` directories
- Only removes tools that exist in the repository (known tools)
- Validates target paths before any deletion
- Handles both symlinks and copied files appropriately
- Skips tools that aren't installed (no-op, not an error)

## Notes

- Uninstalling removes the tool from the target location only
- The source files in the repository are never modified
- Re-install anytime using `/install`
