---
name: find-skills
description: |
  Discovers and installs agent skills from the open ecosystem. Enriches search results with descriptions fetched from skills.sh.

  Use when a user asks "how do I do X", "find a skill for X", "is there a skill that can...", or wants to extend agent capabilities. Use for skill discovery, skill search, skill install, finding tools.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://skills.sh/'
---

# Find Skills

## Overview

Searches the open agent skills ecosystem and installs matching skills via the Skills CLI (`pnpm dlx skills`). Includes an enrichment script that fetches descriptions from skills.sh for each result, giving users context beyond raw skill names.

**When to use:** User asks for help with a domain that might have existing skills, wants to browse available skills, or asks to extend agent capabilities.

**When NOT to use:** User already knows the exact skill and install command, or the task has nothing to do with skill discovery.

## Quick Reference

| Action              | Command                                                                         | Notes                                |
| ------------------- | ------------------------------------------------------------------------------- | ------------------------------------ |
| Search skills       | `pnpm dlx skills find [query]`                                                  | Interactive or keyword search        |
| Enriched search     | `node scripts/enrich_find.js "query"`                                           | Adds descriptions from skills.sh     |
| Install skill       | `pnpm dlx skills add <source> -s <name> -a claude-code -y`                      | Default to Claude Code agent         |
| Install globally    | `pnpm dlx skills add <source> -s <name> -a claude-code -g -y`                   | User-level install                   |
| Install all skills  | `pnpm dlx skills add <source> --all`                                            | All skills, all agents, skip prompts |
| Multi-agent install | `pnpm dlx skills add <source> -s <name> -a claude-code opencode github-copilot` | Target multiple agents               |
| List repo skills    | `pnpm dlx skills add <source> --list`                                           | Preview without installing           |
| List installed      | `pnpm dlx skills list`                                                          | Project-level; add `-g` for global   |
| Remove skill        | `pnpm dlx skills remove <name>`                                                 | Interactive if no name given         |
| Check updates       | `pnpm dlx skills check`                                                         | Shows available updates              |
| Update skills       | `pnpm dlx skills update`                                                        | Updates all installed                |
| Init new skill      | `pnpm dlx skills init <name>`                                                   | Scaffolds SKILL.md                   |
| Browse online       | `https://skills.sh/`                                                            | Web catalog                          |

## Common Skill Categories

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Common Mistakes

| Mistake                              | Correct Pattern                                          |
| ------------------------------------ | -------------------------------------------------------- |
| Using `npx skills`                   | Use `pnpm dlx skills` for consistent package management  |
| Forgetting `-y` on install           | Add `-y` to skip interactive confirmation prompts        |
| Vague search terms like "help"       | Use specific keywords: "react testing", "pr review"      |
| Not checking skills.sh first         | Browse `https://skills.sh/` for curated listings         |
| Installing without reviewing         | Check the skill page on skills.sh before installing      |
| Installing without `-a claude-code`  | Always specify agent: `-a claude-code` (or target agent) |
| Using `owner/repo` for private repos | Use SSH URL: `git@github.com:Org/repo.git`               |
| Running enrichment without Node.js   | Script requires Node.js with `https` module (built-in)   |

## Delegation

- **Skill search execution**: Run `pnpm dlx skills find` or the enrichment script directly
- **Skill installation**: Run `pnpm dlx skills add` after user confirms
- **Detailed skill info**: Browse the skill page on skills.sh before recommending

> If the `skill-management` skill is available, delegate skill creation, auditing, and validation to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s skill-management -a claude-code -y`

If no matching skill is found, offer to help directly and suggest `pnpm dlx skills init` to create a custom skill.

## References

- [Discovery workflow and search strategies](references/discovery-guide.md)
- [Enriched search script usage and options](references/enriched-search.md)
- [Installing skills from private repositories](references/private-repos.md)
