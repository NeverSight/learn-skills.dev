---
name: markdown-linting
description: Comprehensive markdown linting guidance using markdownlint-cli2. Run, execute, check, and validate markdown files. Fix linting errors (MD0XX rules). Configure .markdownlint-cli2.jsonc (rules and ignores). Set up VS Code extension and GitHub Actions workflows. Supports markdown flavors including GitHub Flavored Markdown (GFM) and CommonMark. Use when working with markdown files, encountering validation errors, configuring markdownlint, setting up linting workflows, troubleshooting linting issues, establishing markdown quality standards, or configuring flavor-specific rules for tables, task lists, and strikethrough.
allowed-tools: Read, Bash, Glob, Grep
---

# Markdown Linting

This skill provides comprehensive guidance for markdown linting using `markdownlint-cli2`, the industry-standard markdown linter that can be used in any project.

## Table of Contents

- [Overview](#overview)
- [When to Use This Skill](#when-to-use-this-skill)
- [Markdown Flavors](#markdown-flavors)
- [First Use: Installation and Setup](#first-use-installation-and-setup)
- [Setting Up Markdown Linting in Your Repo](#setting-up-markdown-linting-in-your-repo)
- [Quick Start](#quick-start)
- [Unified Tooling Architecture](#unified-tooling-architecture)
- [CRITICAL: Configuration Policy](#critical-configuration-policy)
- [CRITICAL: NO AUTOMATED SCRIPTS](#critical-no-automated-scripts)
- [Running Linting Locally](#running-linting-locally)
- [Intelligent Fix Handling](#intelligent-fix-handling)
- [VS Code Extension Setup (Optional/Advanced)](#vs-code-extension-setup-optionaladvanced)
- [GitHub Actions Integration (Optional/Advanced)](#github-actions-integration-optionaladvanced)
- [Customizing Rules (Requires Approval)](#customizing-rules-requires-approval)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Resources](#resources)
- [Evaluation Scenarios](#evaluation-scenarios)
- [Multi-Model Testing Notes](#multi-model-testing-notes)
- [Version History](#version-history)
- [Last Updated](#last-updated)

## Overview

This tooling enables enforcement of strict markdown quality standards through automated linting. Markdown files can be validated using `markdownlint-cli2` with a unified tooling approach that ensures zero configuration drift across VS Code, CLI, and CI/CD environments.

**Core Philosophy:**

- Single source of truth: `.markdownlint-cli2.jsonc` contains all configuration (rules, ignores, options)
- Unified tooling: Same `markdownlint-cli2` engine everywhere (VS Code, CLI, CI/CD)
- Strict enforcement: Fix content to comply with rules, not rules to accommodate content
- Quality-first: Linting rules are intentional and enforce documentation quality

## When to Use This Skill

This skill should be used when:

- User encounters markdown linting errors (MD001, MD013, MD033, etc.)
- User asks about markdown validation, formatting, or quality standards
- User needs to configure `.markdownlint-cli2.jsonc` (rules, ignores, or options)
- User asks about configuration file setup or structure
- User wants to set up VS Code markdown linting extension
- User needs to troubleshoot markdown linting issues
- User asks how to run markdown linting locally
- User wants to understand GitHub Actions markdown validation
- User is working with markdown files and needs quality guidance

## Markdown Flavors

markdownlint-cli2 supports multiple markdown flavors. By default, it validates GitHub Flavored Markdown (GFM), which is recommended for most projects.

**Supported Flavors:**

| Flavor | Default | Best For |
|--------|:-------:|----------|
| **GFM** | ✓ | GitHub repos, most web projects |
| **CommonMark** | | Maximum portability, strict compliance |

**Quick Guidance:**

- **Use GFM (default)** for GitHub repos, typical web projects, and when you need tables/task lists
- **Use CommonMark** for cross-platform publishing or strict standards compliance

**For detailed flavor guidance**, see the dedicated reference files:

- [Flavors Overview](references/flavors/overview.md) - Comparison and selection guidance
- [GFM Configuration](references/flavors/gfm.md) - GitHub Flavored Markdown (default)
- [CommonMark Configuration](references/flavors/commonmark.md) - Strict base specification

**Flavor-Sensitive Rules:**

Some rules only apply to specific flavors. See [Markdownlint Rules Reference](references/markdownlint-rules.md) for rules tagged with their flavor compatibility.

## First Use: Installation and Setup

**If this is your first time setting up markdown linting**, see the comprehensive installation guide:

**[Installation and Setup Guide](references/installation-setup.md)**

This guide covers:

- Prerequisites (Node.js/npm)
- Detection of existing setup
- Two approaches: npx (zero setup) vs local install (full features)
- Configuration file creation (`.markdownlint-cli2.jsonc`)
- Configuring rules, ignores, and options in one file
- Verification steps
- Troubleshooting setup issues

**Quick detection check:**

```bash
# Check if you're already set up
ls .markdownlint-cli2.jsonc     # Configuration exists?
npm list markdownlint-cli2      # Package installed?
cat package.json | grep "lint:md"  # Scripts configured?
```

If any of these are missing, follow the [Installation and Setup Guide](references/installation-setup.md) first.

## Setting Up Markdown Linting in Your Repo

This section provides a complete guide for setting up markdown linting from scratch in any repository.

### Prerequisites

**Node.js 20+** is required. Install via [fnm](https://github.com/Schniz/fnm) (recommended):

```bash
# Windows (PowerShell as Admin)
winget install Schniz.fnm

# macOS/Linux
curl -fsSL https://fnm.vercel.app/install | bash
```

Then in Git Bash, add to `~/.bashrc`:

```bash
eval "$(fnm env --use-on-cd --shell bash)"
```

Install Node:

```bash
fnm install 24 && fnm default 24
```

**Why fnm?** Unlike nvm-windows, fnm works natively in Git Bash without [silent output bugs](https://github.com/coreybutler/nvm-windows/wiki/Common-Issues).

### Step 1: Create Configuration

Create `.markdownlint-cli2.jsonc` in your repo root:

```jsonc
{
  "gitignore": true,
  "config": {
    "default": true,
    "MD013": false
  }
}
```

See [Markdownlint Rules Reference](references/markdownlint-rules.md) for all rules.

### Step 2: Add to package.json

If you don't have a `package.json`, create one:

```json
{
  "name": "your-repo-name",
  "private": true,
  "scripts": {
    "lint:md": "markdownlint-cli2 \"**/*.md\"",
    "lint:md:fix": "markdownlint-cli2 \"**/*.md\" --fix"
  },
  "devDependencies": {
    "markdownlint-cli2": "^0.20.0"
  },
  "engines": {
    "node": ">=20.0.0"
  }
}
```

Then install:

```bash
npm install
```

### Step 3: Add to .gitignore

Ensure `node_modules/` is in your `.gitignore`:

```gitignore
node_modules/
```

### Step 4: Add CI Workflow (Optional)

Create `.github/workflows/markdown-lint.yml`:

```yaml
name: Markdown Lint

on:
  pull_request:
    paths: ['**.md']
  push:
    branches: [main]
    paths: ['**.md']

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: DavidAnson/markdownlint-cli2-action@v22
        with:
          globs: '**/*.md'
```

### Step 5: Run Linting

```bash
npm run lint:md        # Check
npm run lint:md:fix    # Auto-fix
```

### Verification Checklist

- [ ] `.markdownlint-cli2.jsonc` exists with your rules
- [ ] `package.json` has lint:md scripts
- [ ] `node_modules/` is in `.gitignore`
- [ ] `npm run lint:md` works locally
- [ ] CI workflow runs on PRs (if added)

## Quick Start

**Option 1: Using npx (zero setup required):**

```bash
# Check all markdown files
npx markdownlint-cli2 "**/*.md"

# Auto-fix issues
npx markdownlint-cli2 "**/*.md" --fix
```

**Option 2: Using npm scripts (if configured):**

```bash
# Check all markdown files for linting errors
npm run lint:md

# Auto-fix fixable linting issues
npm run lint:md:fix
```

**Option 3: VS Code extension for real-time linting (optional/advanced):**

1. Install `davidanson.vscode-markdownlint` from VS Code marketplace
2. Create `.markdownlint-cli2.jsonc` configuration (see installation guide)
3. Linting happens as you type with auto-fix on save enabled (if configured)

## Unified Tooling Architecture

When configured, `markdownlint-cli2` can be used everywhere to ensure zero configuration drift:

### Tooling Components

1. **CLI Tool** (`markdownlint-cli2`) - **Core component, use this first**
   - Can be run via npx (zero setup) or local install
   - Used for local validation and pre-commit checks
   - Foundation for all other integrations

2. **VS Code Extension** (`davidanson.vscode-markdownlint`) - **Optional/Advanced**
   - Uses same `markdownlint-cli2` engine as CLI
   - Real-time linting as you type
   - Auto-fix on save and paste (configurable in `.vscode/settings.json`)
   - See [VS Code Extension Setup](references/vscode-extension-setup.md)

3. **GitHub Actions** (`markdownlint-cli2-action`) - **Optional/Advanced**
   - Same engine as VS Code and CLI
   - Runs automatically on PRs that modify markdown files (when configured)
   - Same rules as local development (no surprises)
   - See [GitHub Actions Configuration](references/github-actions-config.md)

### Configuration Source

All tools read `.markdownlint-cli2.jsonc` in the project root as the single source of truth:

```jsonc
{
  "gitignore": true,
  "ignores": ["vendor/**/*.md"],
  "config": {
    "default": true,
    "MD013": false
  }
}
```

**What this contains:**

- `gitignore`: Automatically excludes files from `.gitignore`
- `ignores`: Additional glob patterns to exclude from linting
- `config`: Linting rules (all defaults enabled, MD013 disabled for long lines)

**Configuration precedence** (in decreasing order):

1. `.markdownlint-cli2.{jsonc,yaml,cjs}` file - **Single source of truth**
2. VS Code user/workspace settings (avoid - not portable)
3. Default configuration

**Note:** Changes to `.markdownlint-cli2.jsonc` apply instantly to all tools (VS Code, CLI, GitHub Actions)

## CRITICAL: Configuration Policy

**IMPORTANT - Read this before modifying any configuration:**

### Strict Policy - Never Modify Without Approval

- **DO NOT modify `.markdownlint-cli2.jsonc` without explicit approval**
- Strict linting rules are intentional and enforce documentation quality
- If linting errors occur, **fix the content to comply with the rules**, NOT the rules themselves
- Only request rule changes if there is a **compelling architectural reason**
- When in doubt, **ask before relaxing any linting rules**

### Why This Policy Exists

1. **Quality enforcement**: Linting rules maintain documentation consistency and professionalism
2. **Best practices**: Rules encode markdown best practices accumulated over years
3. **Accessibility**: Many rules improve screen reader and markdown parser compatibility
4. **Maintainability**: Consistent formatting makes documentation easier to maintain
5. **Collaboration**: Shared standards reduce friction in code reviews

### Proper Response to Linting Errors

**Correct approach:**

```markdown
Error: MD022/blanks-around-headings - Headings should be surrounded by blank lines

Action: Add blank lines before and after the heading in the markdown file
```

**Incorrect approach:**

```markdown
Error: MD022/blanks-around-headings - Headings should be surrounded by blank lines

Action: Disable MD022 rule in .markdownlint-cli2.jsonc
```

**Exception:** If you genuinely believe a rule should be modified, present your case to the user with:

- The specific rule and why it's problematic
- Examples of where it causes issues
- Architectural or usability rationale
- Proposed configuration change

The user will make the final decision on whether to modify the configuration.

## CRITICAL: NO AUTOMATED SCRIPTS

> **⚠️ SCRIPTS ARE STRICTLY PROHIBITED FOR MARKDOWN LINTING FIXES ⚠️**

**NEVER use automated scripts to fix markdown files.** This includes:

- Python/Bash scripts that modify multiple files at once
- Regex-based find-and-replace operations across files
- Any automated tool that makes bulk changes without human review per-change
- "Smart" fixers that detect and add language specifiers to code blocks

### Why This Policy Exists

**A) Scripts are dangerous - we have seen real issues:**

1. **Context blindness**: Scripts cannot understand semantic context (e.g., a code block showing tool output vs actual code that needs syntax highlighting)
2. **Over-application**: Scripts apply fixes uniformly, even where inappropriate
3. **Cascading damage**: One wrong assumption affects hundreds of files, requiring painful manual cleanup
4. **False language detection**: Adding `text` or other language specifiers to blocks that intentionally have none

**B) Manual fixes are slower but more accurate and safer:**

While manually fixing linting errors one-by-one takes longer, it ensures:

- Each change is reviewed in context before application
- Semantic meaning is preserved (not just syntactic correctness)
- Edge cases are handled appropriately
- No collateral damage to unrelated content

**The speed/accuracy trade-off is worth it.** A script that "saves time" but requires hours of cleanup is a net loss.

### Nested Code Blocks: A Critical Complexity

Documentation often contains **markdown within markdown** - examples showing how to write markdown, skill documentation with code samples, templates, etc. This creates nested structures that scripts cannot handle correctly:

**Example: A skill showing how to write a code block:**

`````markdown
Here's how to create a Python code block:

````markdown
```python
def hello():
    print("Hello, world!")
```
````
`````

In this example:

- The outer fence uses 4 backticks (`````markdown`)
- The inner fence uses 3 backticks (` ```python `)
- A script seeing ` ``` ` might incorrectly add language specifiers or break the nesting

**Common nested patterns to watch for:**

- ` ```{language} ` - Regular code block with syntax highlighting
- ` ````markdown ` - Wrapper showing markdown examples (uses 4+ backticks)
- Code blocks inside code blocks (documentation about documentation)
- Example output that should NOT have language specifiers

**Scripts cannot reliably distinguish:**

- Which backtick fence is the "real" one vs an example
- Whether a bare ` ``` ` is intentional (raw output) or needs a language
- The semantic purpose of each code block

### Real-World Failure Example

A script added `text` language specifiers to code blocks showing MCP tool output, Notion searches, and other non-code examples. These blocks were intentionally bare (no language specifier) to show raw output without syntax highlighting. The script's "fix" required hundreds of manual edits to undo.

### The ONLY Acceptable Approach

1. Run `markdownlint-cli2 --fix` for safe, built-in auto-fixes (trailing spaces, blank lines, etc.)
2. For "unfixable" errors (MD040, MD024, etc.), use the **Edit tool** to make targeted, contextual fixes one at a time
3. **Review each change before applying** - understand WHY the error exists and whether the fix is semantically correct
4. **Look at surrounding context** - is this a nested code block? An example? Raw output?
5. If a fix seems mechanical/repetitive, **STOP and ask the user** before proceeding

### If You Even Consider Using a Script

1. **STOP immediately**
2. **Ask the user explicitly**: "I'm considering automating this with a script. Are you sure? Scripts have caused painful cleanup in the past."
3. **Only proceed if user explicitly confirms** AND you've triple-checked the script logic
4. **Test on ONE file first** and show the user the diff before bulk application

### MD040 (fenced-code-language) Special Guidance

The MD040 rule requires code blocks to have language specifiers. However:

- **DO NOT** blindly add `text` to all blocks without language specifiers
- Some blocks intentionally have no language (showing raw output, examples, templates)
- Ask yourself: "Is this showing code that needs syntax highlighting, or raw output?"
- When in doubt, **ask the user** rather than guessing

**Questions to ask before adding a language specifier:**

1. Is this actual code, or example output/results?
2. Is this inside a larger markdown example (nested)?
3. Would syntax highlighting help or hurt readability here?
4. Did the author intentionally leave it bare?

## Running Linting Locally

### CRITICAL: Auto-Fix Workflow

**When running linting validation, ALWAYS automatically fix ALL errors (both fixable and "unfixable") without asking for user confirmation.**

**Workflow:**

1. Run linting validation command (npx or npm scripts)
2. If errors are found:
   - **IMMEDIATELY run the auto-fix command** (`--fix` flag) without prompting
   - Report what was auto-fixed
   - **For any remaining "unfixable" errors:**
     - Read the affected files to understand context
     - Analyze the error and surrounding content
     - Apply intelligent fixes based on context (see "Intelligent Fix Handling" below)
     - Re-run linting to verify fixes
3. If no errors are found, report success

**DO NOT ask "Would you like me to auto-fix?" or "Would you like me to investigate?" - just fix everything automatically.**

### Prerequisites

**For npx approach (zero setup):**

- Node.js 18+ and npm 8+ installed
- No additional setup required

**For local install approach:**

```bash
# Install dependencies (first time only)
npm install
```

If your project doesn't have `markdownlint-cli2` installed, see the [Installation and Setup Guide](references/installation-setup.md).

### Check All Markdown Files

**With npx:**

```bash
npx markdownlint-cli2 "**/*.md"
```

**With npm scripts (if configured):**

```bash
npm run lint:md
```

**What this does:**

- Runs `markdownlint-cli2` against all `.md` files in the project
- Automatically excludes `node_modules` directory
- Outputs errors with file paths and line numbers
- Exit code 0 if no errors, non-zero if errors found

**Example output:**

```text
docs/setup-guide.md:45:1 MD022/blanks-around-headings Headings should be surrounded by blank lines
README.md:12:81 MD009/no-trailing-spaces Trailing spaces
```

### Auto-Fix Fixable Issues

**With npx:**

```bash
npx markdownlint-cli2 "**/*.md" --fix
```

**With npm scripts (if configured):**

```bash
npm run lint:md:fix
```

**What this does:**

- Automatically fixes issues that can be safely corrected
- Modifies files in place
- Reports remaining unfixable issues

**Fixable issues include:**

- Trailing spaces (MD009)
- Missing blank lines (MD012, MD022)
- List marker consistency (MD004, MD007)
- Code fence style (MD048)

**Non-fixable issues require intelligent analysis and manual fixes:**

- Heading structure (MD001, MD025)
- Duplicate headings (MD024)
- Line length (MD013, if enabled)
- Link references (MD051, MD052)

### Intelligent Fix Handling

**When "unfixable" errors remain after auto-fix, automatically analyze and fix them.**

For detailed strategies on handling each error type, see the dedicated guide:

**[Intelligent Fixing Guide](references/intelligent-fixing-guide.md)**

This guide covers:

- MD024 - Duplicate Headings (context-aware renaming or removal)
- MD001/MD025 - Heading Structure (hierarchy fixes)
- MD051/MD052 - Link References (anchor and reference link corrections)
- MD013 - Line Length (intelligent wrapping)
- General principles for context-aware analysis
- Verification and reporting best practices
- Performance optimization with parallel Task agents

**Quick summary:**

1. Run auto-fix first: `npx markdownlint-cli2 "**/*.md" --fix`
2. For remaining errors, read affected files to understand context
3. Apply intelligent fixes based on error patterns (see guide)
4. Always re-run linting to verify all errors are resolved
5. Report what was fixed and how

## VS Code Extension Setup (Optional/Advanced)

**For VS Code integration**, see the dedicated guide:

**[VS Code Extension Setup Guide](references/vscode-extension-setup.md)**

The VS Code extension (`davidanson.vscode-markdownlint`) provides real-time linting in your editor. The guide covers:

- Extension installation and verification
- Auto-fix configuration (format on save, format on paste)
- Interactive linting features (squiggly underlines, quick fixes)
- Keyboard shortcuts for all fix methods
- Configuration precedence and troubleshooting
- Best practices for team usage

**This is optional but highly recommended for regular markdown work.**

## GitHub Actions Integration (Optional/Advanced)

**For CI/CD integration**, see the dedicated guide:

**[GitHub Actions Configuration Guide](references/github-actions-config.md)**

GitHub Actions can automatically validate markdown files on PRs and pushes. The guide covers:

- Complete workflow file configuration
- Trigger setup (PR and push events with path filtering)
- Action versions (checkout@v5, markdownlint-cli2-action@v22)
- Workflow execution flow and results interpretation
- Viewing and fixing CI failures
- Advanced configuration (custom globs, auto-fix, branch protection)
- Troubleshooting common issues

**This is optional but highly recommended for team projects.**

## Customizing Rules (Requires Approval)

**WARNING: Only modify with explicit approval per policy above.**

**For detailed rule information**, see the comprehensive guide:

**[Markdownlint Rules Reference](references/markdownlint-rules.md)**

The rules reference covers:

- All 60+ MD rules with descriptions and examples
- Rule categories (auto-fixable vs manual-fix required)
- Configuration syntax for customizing rules
- Common rule modifications (disable, configure parameters)
- Inline comment syntax for per-file overrides
- Links to official documentation for each rule

**Quick syntax reminder:**

```json
{
  "default": true,        // Enable all defaults
  "MD013": false,         // Disable specific rule
  "MD033": {              // Configure with options
    "allowed_elements": ["br"]
  }
}
```

## Troubleshooting

**Common issues and solutions:**

### Issue: "Command not found: markdownlint-cli2"

**Solution:** Run `npm install` or use npx: `npx markdownlint-cli2 "**/*.md"`

### Issue: Too many linting errors to fix manually

**Solution:**

1. Run auto-fix: `npx markdownlint-cli2 "**/*.md" --fix`
2. Fix remaining errors in batches
3. See [Installation Guide](references/installation-setup.md) for detailed troubleshooting

### Issue: VS Code or GitHub Actions problems

**For detailed troubleshooting**, see the dedicated guides:

- **VS Code issues**: [VS Code Extension Setup](references/vscode-extension-setup.md#troubleshooting)
- **GitHub Actions issues**: [GitHub Actions Configuration](references/github-actions-config.md#troubleshooting)

### Issue: Unclear rule violations

**Solution:** Check [Markdownlint Rules Reference](references/markdownlint-rules.md) for rule explanations, examples, and official documentation links.

## Best Practices

For comprehensive best practices on markdown linting, configuration management, collaboration, and skill automation:

**[Best Practices Guide](references/best-practices.md)**

The guide covers:

- Writing markdown effectively with linting in mind
- Configuration management and rule customization
- Collaboration patterns and team workflows
- Skill automation for Claude Code usage
- When and how to use parallel Task agents for efficiency

## Resources

### Official Documentation

- **markdownlint-cli2 README:** [github.com/DavidAnson/markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2)
- **markdownlint rules:** [github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- **VS Code extension:** [marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)
- **GitHub Action:** [github.com/DavidAnson/markdownlint-cli2-action](https://github.com/DavidAnson/markdownlint-cli2-action)

### Project Configuration Files

These files should be created in your project root (see installation guides for setup):

- **Configuration:** `.markdownlint-cli2.jsonc` (required for custom rules)
- **NPM scripts:** `package.json` (optional, for npm run commands)
- **VS Code settings:** `.vscode/settings.json` (optional, for auto-fix on save)
- **GitHub workflow:** `.github/workflows/markdown-lint.yml` (optional, for CI/CD)

### Supporting Documentation

This skill includes reference documentation in the `references/` directory:

- [references/installation-setup.md](references/installation-setup.md) - **Start here:** Installation and first-time setup
- [references/intelligent-fixing-guide.md](references/intelligent-fixing-guide.md) - Strategies for fixing "unfixable" errors
- [references/markdownlint-rules.md](references/markdownlint-rules.md) - Detailed rule explanations and customization
- [references/best-practices.md](references/best-practices.md) - Best practices for writing, configuration, collaboration, and automation
- [references/vscode-extension-setup.md](references/vscode-extension-setup.md) - VS Code integration guide (optional/advanced)
- [references/github-actions-config.md](references/github-actions-config.md) - CI/CD workflow setup (optional/advanced)

## Evaluation Scenarios

These scenarios are used to evaluate skill activation, guidance quality, and multi-model compatibility.

### Scenario 1: First-time setup

```json
{
  "name": "First-time setup",
  "query": "I need to set up markdown linting in my project",
  "context": "User has no existing markdown linting configuration",
  "files": [],
  "expected_behavior": [
    "Skill activates successfully",
    "Loads references/installation-setup.md for comprehensive guidance",
    "Provides step-by-step installation instructions",
    "Distinguishes between npx (zero-setup) and local install approaches",
    "Guides through .markdownlint-cli2.jsonc configuration",
    "Includes verification steps"
  ],
  "test_models": ["sonnet", "haiku", "opus"]
}
```

### Scenario 2: Fix linting errors

```json
{
  "name": "Fix linting errors",
  "query": "I'm getting MD022 errors, how do I fix them?",
  "context": "User has linting errors and needs guidance on fixes",
  "files": ["sample-file.md"],
  "expected_behavior": [
    "Skill activates for error type and rule explanation",
    "Explains MD022 rule (blanks around headings)",
    "Provides auto-fix command (npx markdownlint-cli2 --fix)",
    "Explains both automatic and intelligent fix approaches",
    "References intelligent-fixing-guide.md if needed",
    "Provides verification steps"
  ],
  "test_models": ["sonnet", "haiku", "opus"]
}
```

### Scenario 3: VS Code integration

```json
{
  "name": "VS Code integration",
  "query": "How do I enable auto-fix on save in VS Code?",
  "context": "User wants to integrate markdown linting into their editor workflow",
  "files": [],
  "expected_behavior": [
    "Skill activates for VS Code integration",
    "Loads references/vscode-extension-setup.md",
    "Provides extension installation instructions",
    "Explains auto-fix configuration in .vscode/settings.json",
    "Documents keyboard shortcuts and interactive features",
    "Includes troubleshooting for common VS Code issues"
  ],
  "test_models": ["sonnet", "haiku", "opus"]
}
```

### Scenario 4: GitHub Actions CI setup

```json
{
  "name": "GitHub Actions CI setup",
  "query": "Add markdown linting to GitHub Actions",
  "context": "User wants to automate markdown validation in CI/CD pipeline",
  "files": [".github/workflows/"],
  "expected_behavior": [
    "Skill activates for GitHub Actions integration",
    "Loads references/github-actions-config.md",
    "Provides complete workflow file configuration",
    "Explains trigger setup (PR and push events)",
    "Documents workflow execution and results interpretation",
    "Includes configuration for auto-fix and branch protection"
  ],
  "test_models": ["sonnet", "haiku", "opus"]
}
```

### Scenario 5: Configuration customization

```json
{
  "name": "Configuration customization",
  "query": "How do I disable MD013 line length rule?",
  "context": "User needs to customize linting rules for their project",
  "files": [".markdownlint-cli2.jsonc"],
  "expected_behavior": [
    "Skill activates for rule customization",
    "Explains configuration policy (fix content, not rules)",
    "Provides .markdownlint-cli2.jsonc configuration example",
    "Shows syntax for disabling/configuring specific rules",
    "References references/markdownlint-rules.md for rule details",
    "Emphasizes verification of changes across all tools"
  ],
  "test_models": ["sonnet", "haiku", "opus"]
}
```

## Multi-Model Testing Notes

**Tested with**:

- **Claude Sonnet**: Optimal performance, follows hub architecture well
- **Claude Haiku**: (To be tested - should work given explicit instructions)
- **Claude Opus**: (To be tested - may over-analyze, content is appropriately scoped)

**Observations**: Skill's explicit command examples and clear decision trees should work well across all model tiers.

## Version History

- v2.0.0 (2025-11-30): Migrated to code-quality plugin in claude-code-plugins repo
- v1.2.0 (2025-11-17): Extracted Intelligent Fixing Guide - moved detailed error fixing strategies to separate reference file, reduced SKILL.md size for better token efficiency
- v1.1.0 (2025-11-17): Deduplicated content - removed duplicated reference material, streamlined to hub architecture
- v1.0.2 (2025-11-17): Version updates - updated to markdownlint-cli2 v0.19.0, Node 20+ requirement, action v21
- v1.0.1 (2025-01-09): Improved portability - removed repository-specific language, enhanced first-use guidance
- v1.0.0 (2025-01-09): Initial release - migrated from `.claude/memory/workflows.md`

## Last Updated

**Date:** 2026-01-17
**Model:** claude-opus-4-5-20251101
