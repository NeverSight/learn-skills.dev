---
name: context-curation
description: "Analyzes staged git changes and evaluates agentic context files (Claude, Codex, Cursor, etc.) to suggest additions or removals. Use after staging changes before committing."
---

# Context Curation

Analyze staged git changes and evaluate whether agentic context files need to be updated to reflect those changes.

## When to Use This Skill

- After staging changes, before committing
- When introducing new patterns, conventions, or APIs
- When deprecating or removing significant functionality
- When refactoring code that may invalidate existing context documentation
- Periodically to audit context file freshness

## Supported Context File Locations

This skill scans for agentic context files across multiple platforms:

| Platform | Locations |
|----------|-----------|
| Claude Code | `.claude/`, `CLAUDE.md` |
| Codex | `.codex/`, `codex.md` |
| Cursor | `.cursor/`, `.cursorrules` |
| Aider | `.aider/`, `.aider.conf.yml` |
| GitHub Copilot | `COPILOT.md`, `.github/copilot-instructions.md` |
| Generic | `AGENTS.md`, `AI.md`, `CONTEXT.md` |
| Project docs | `docs/`, `README.md` (architecture sections) |

## Analysis Workflow

### Step 1: Inspect Staged Changes

Run `git diff --staged` to understand what's being committed:
- New files and their purposes
- Modified functions, classes, or modules
- Deleted code and removed dependencies
- Changed APIs, interfaces, or contracts

### Step 2: Scan Existing Context Files

Locate all agentic context files in the repository and extract:
- Documented patterns and conventions
- Architecture decisions and rationale
- API references and usage examples
- Project-specific rules and guidelines

### Step 3: Compare and Analyze

Cross-reference staged changes against existing context:
- **New patterns**: Code introduces conventions not yet documented
- **API changes**: Public interfaces modified or extended
- **Deprecated code**: Removed functionality still referenced in context
- **Stale references**: Context mentions files, functions, or patterns that no longer exist

### Step 4: Generate Recommendations

Produce actionable suggestions with clear rationale.

## Output Format

### Additions Needed

For each suggested addition:
```
## ADD: [Brief description]

**Context file**: [path to file that should be updated]
**Rationale**: [Why this should be documented]
**Suggested content**:
[Proposed text to add]

**Evidence from staged changes**:
- [file:line] - [relevant code snippet or change]
```

### Removals Needed

For each suggested removal:
```
## REMOVE: [Brief description]

**Context file**: [path to file containing outdated content]
**Current content**: [text that should be removed or updated]
**Rationale**: [Why this is now stale]

**Evidence from staged changes**:
- [file] - [deleted or changed code that invalidates this]
```

### No Changes Needed

If context files are already aligned with staged changes:
```
## Context files are up to date

Reviewed [N] context files against staged changes.
No updates recommended.
```

## Instructions

1. First, run `git diff --staged --stat` to get an overview of staged changes
2. Run `git diff --staged` to examine the actual changes in detail
3. Search for all supported context file locations listed above
4. Read each context file found
5. Analyze whether staged changes introduce patterns, APIs, or conventions that should be documented
6. Analyze whether staged changes remove or deprecate anything referenced in context files
7. Present findings using the output format above
8. If no context files exist, suggest creating one appropriate for the project
