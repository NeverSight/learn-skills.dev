---
name: slash-command-factory
description: Generate custom Claude Code slash commands via guided question flow. TRIGGERS - create slash command, generate command, custom command.
---

# Slash Command Factory

A comprehensive system for generating production-ready Claude Code slash commands through a simple question-based workflow.

## When to Use This Skill

- Creating new custom slash commands for Claude Code
- Generating command templates from presets
- Validating slash command YAML frontmatter syntax
- Organizing commands into proper folder structures
- Converting workflows into reusable slash commands

---

## Overview

This skill helps you create custom slash commands for Claude Code by:

- Asking 5-7 straightforward questions about your command needs
- Generating complete command .md files with proper YAML frontmatter
- Providing 10 powerful preset commands for common use cases
- Validating command format and syntax
- Creating well-organized folder structures
- Offering installation guidance

**Output**: Complete slash commands ready to use in Claude Code

---

## Command Structure Patterns

Three official patterns from Anthropic documentation:

| Pattern | Name        | Best For                                          | Structure                     |
| ------- | ----------- | ------------------------------------------------- | ----------------------------- |
| A       | Simple      | Straightforward tasks (code review, file updates) | Context -> Task               |
| B       | Multi-Phase | Complex discovery (audits, system mapping)        | Discovery -> Analysis -> Task |
| C       | Agent-Style | Specialized roles (experts, orchestrators)        | Role -> Process -> Guidelines |

Full templates and when-to-use guidance: [Command Patterns](./references/command-patterns.md)

---

## Naming Convention

All slash command files MUST follow kebab-case: `[verb]-[noun].md`

**Rules**: Lowercase only, 2-4 words, `[a-z0-9-]` characters, no underscores/camelCase

| Input                        | Output              |
| ---------------------------- | ------------------- |
| "Review pull requests"       | `pr-review.md`      |
| "Generate API documentation" | `api-document.md`   |
| "Audit security compliance"  | `security-audit.md` |

Full conversion algorithm and examples: [Naming Convention](./references/naming-convention.md)

---

## Bash Permission Rules

**Critical**: Blanket `Bash` permission is prohibited. Must use subcommand-level specificity.

```yaml
# WRONG - too broad
allowed-tools: Bash(git:*)

# CORRECT - subcommand-level
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git push:*)

# OK - simple commands without subcommand hierarchies
allowed-tools: Bash(cp:*), Bash(mkdir -p:*), Bash(date:*)
```

| Command Type    | Bash Permissions                            | Example Commands                |
| --------------- | ------------------------------------------- | ------------------------------- |
| Git Commands    | `git status, git diff, git log, git branch` | code-review, commit-assist      |
| Discovery       | `find, tree, ls, du`                        | codebase-analyze, structure-map |
| Analysis        | `grep, wc, head, tail, cat`                 | search-code, count-lines        |
| Data Processing | `awk, sed, sort, uniq`                      | parse-data, format-output       |

Full patterns and selection guide: [Bash Permissions](./references/bash-permissions.md)

---

## Two Paths to Generate Commands

### Path 1: Quick-Start Presets (30 seconds)

Choose from 10 powerful preset commands:

| #   | Command            | Purpose                                                |
| --- | ------------------ | ------------------------------------------------------ |
| 1   | /research-business | Comprehensive market research and competitive analysis |
| 2   | /research-content  | Multi-platform content trend analysis and SEO strategy |
| 3   | /medical-translate | Medical terminology to 8th-10th grade (German/English) |
| 4   | /compliance-audit  | HIPAA/GDPR/DSGVO compliance validation                 |
| 5   | /api-build         | Complete API integration code with tests               |
| 6   | /test-auto         | Auto-generate comprehensive test suites                |
| 7   | /docs-generate     | Automated documentation creation                       |
| 8   | /knowledge-mine    | Extract and structure insights from documents          |
| 9   | /workflow-analyze  | Analyze and optimize business processes                |
| 10  | /batch-agents      | Launch and coordinate multiple agents                  |

Full YAML configs and details: [Preset Commands](./references/preset-commands.md)

### Path 2: Custom Command (5-7 Questions)

Create a completely custom command by answering questions about:

1. **Purpose** - What should the command do?
2. **Arguments** - Auto-determined; all flags get mandatory short forms (`-b|--branch`)
3. **Tools** - Which Claude Code tools (Read, Write, Bash, Grep, Task, etc.)
4. **Agents** - Does it need to launch specialized agents?
5. **Output** - Analysis, files, action, or report?
6. **Model** - Default, Sonnet, Haiku, or Opus? (optional)
7. **Features** - Bash execution, file references, context gathering? (optional)

Full question scripts and argument conventions: [Question Flow](./references/question-flow.md)

---

## Generation & Installation

After collecting answers, the skill:

1. Generates YAML frontmatter with proper `allowed-tools`
2. Generates command body with purpose-specific instructions
3. Creates folder structure under `generated-commands/[command-name]/`
4. Validates format (YAML, arguments, tools, organization)
5. Provides installation instructions

```bash
# Install to project
cp generated-commands/[command-name]/[command-name].md .claude/commands/

# Install globally
cp generated-commands/[command-name]/[command-name].md ~/.claude/commands/
```

**Plugin invocation**: `/plugin-name:command-name [arguments]`

Full process, folder structure, and plugin invocation rules: [Generation Process](./references/generation-process.md)

---

## Validation

Every generated command is validated for:

- Valid YAML frontmatter (proper syntax, required fields)
- Correct argument format (`$ARGUMENTS`, not `$1 $2 $3`)
- Short forms for all flags (mandatory 1-2 letter shortcuts)
- Bash subcommand-level specificity (no blanket `Bash`)
- Clean folder organization

**If validation fails**, you get specific fix instructions.

Full validation checklist, best practices, and troubleshooting: [Validation Reference](./references/validation-reference.md)

---

## Quick Reference

### Usage

```
@slash-command-factory
Use the /research-business preset

@slash-command-factory
Create a custom command for analyzing customer feedback
```

### Key Rules

| Rule             | Detail                                    |
| ---------------- | ----------------------------------------- |
| Arguments        | Always `$ARGUMENTS` (never `$1`, `$2`)    |
| Flag short forms | Mandatory for all flags (`-b\|--branch`)  |
| Bash permissions | Subcommand-level only (`Bash(git add:*)`) |
| File naming      | kebab-case, 2-4 words                     |
| Output location  | `./generated-commands/[command-name]/`    |

### Ecosystem Integration

Works with: factory-guide, skills-guide, prompts-guide, agents-guide

More examples and integration details: [Usage Examples](./references/usage-examples.md)
