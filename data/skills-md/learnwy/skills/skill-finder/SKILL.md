---
name: skill-finder
description: Intelligent skill discovery and installation assistant. Helps users find community skills and install them to ~/.agents/skills/. Users manage customizations in their own repositories.
---

# Skill Finder

Intelligent assistant for discovering and installing AI assistant skills from the community repository.

## When to Use This Skill

Activate this skill when the user:
- Wants to find a skill for a specific purpose
- Mentions "skill", "find skill", "search skill", "install skill"
- Describes a problem that might be solved by a community skill
- Wants to create a new custom skill using `npx skills init`
- Asks about available skills or skill installation

## Core Capabilities

1. **Intelligent Search**: Parse natural language queries to find relevant skills
2. **Automated Installation**: Install skills to `~/.agents/skills/`
3. **Skill Creation**: Guide users in creating new skills with `npx skills init`

## Workflow Overview

```
[Search] → [Install to ~/.agents/skills/] → Done
              ↓
   User manages customizations in own repo

[Create] → [Guide structure] → User owns and manages
```

## Quick Reference

| Phase | Task | Reference File |
|-------|------|----------------|
| 1 | Search for skills | Read [phase1-search.md](references/phase1-search.md) |
| 2 | Install skills | Read [phase2-install.md](references/phase2-install.md) |
| 3 | Create new skills | Read [phase3-create.md](references/phase3-create.md) |

## Examples

Real usage examples:
- [Example 1: Search and install](examples/example-search-install.md)
- [Example 2: Create new skill](examples/example-create-skill.md)

## High-Level Execution Flow

### Phase 1: Search
1. Parse user intent and extract keywords
2. Execute `npx skills find [keywords]`
3. Present formatted results to user
4. **For details**: Read [phase1-search.md](references/phase1-search.md)

### Phase 2: Install
1. Confirm user's skill selection
2. Execute `npx skills add -g -y <skill-name>`
3. Verify installation in `~/.agents/skills/`
4. Provide success message
5. **For details**: Read [phase2-install.md](references/phase2-install.md)

### Phase 3: Create New Skill
1. Ask user for skill name
2. Execute `npx skills init <name>` to create template
3. Guide user through SKILL.md structure
4. User owns and manages the skill in their own repository
5. **For details**: Read [phase3-create.md](references/phase3-create.md)

## Key Algorithms

### Intent Analysis
- Extract keywords from natural language
- Identify problem domain (e.g., "React performance", "code review")
- Generate focused search terms (1-3 keywords)

### Search Result Formatting
- Parse `npx skills find` output
- Extract: skill name, owner/repo, URL
- Present in numbered list for easy selection

## Error Handling

Common errors and solutions:
- **Network errors**: Suggest retry and check connection
- **Skill not found**: Suggest alternative keywords or browse https://skills.sh/
- **Installation fails**: Check npm/npx availability, network connection
- **Permission denied**: Provide guidance on fixing permissions

## Tools Required

- **RunCommand**: Execute shell commands (npx)
- **AskUserQuestion**: Interactive prompts for skill selection
- **Grep**: Parse command output
- **Read**: Read created SKILL.md templates

## Important Notes

1. **User Manages Customizations**: Users maintain their own skill repositories
2. **No Version Management**: Users handle updates via their own git workflow
3. **Simple Installation**: Skills are only installed to `~/.agents/skills/`
4. **User Owns Created Skills**: Skills created with `npx skills init` belong to the user

## Summary

This skill provides streamlined skill discovery and installation:
- 🔍 **Search**: Natural language skill discovery using `npx skills find`
- 📦 **Install**: One-command installation to `~/.agents/skills/`
- 🆕 **Create**: Guided skill creation with `npx skills init`

Users manage skill customizations and versions in their own repositories.
