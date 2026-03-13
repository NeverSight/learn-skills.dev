---
name: cursor-rules-synchronizer
description: Synchronizes Cursor Rules (.mdc files in .cursor/rules/) to CLAUDE.md by generating a Rules section with context-efficient descriptions and usage instructions. Use when setting up Cursor Rules for the first time, after adding or modifying rules, or when the Rules section in CLAUDE.md is missing or outdated.
---

# Cursor Rules Synchronizer

## Overview

Synchronizes Cursor Rules to CLAUDE.md, creating a self-contained Rules section that enables Claude Code to discover and apply rules in future sessions.

## When to Use

Run this skill when:

- Setting up Cursor Rules in a project for the first time
- After adding new Cursor Rule files
- After modifying existing rule descriptions or organization
- When the Rules section in CLAUDE.md is missing, incomplete, or outdated

## Synchronization Workflow

Follow these steps to synchronize Cursor Rules to CLAUDE.md:

### Step 1: List Rules

Use the helper command to get all Cursor Rule file paths:

```bash
ai skill cursor-rules-synchronizer list
```

This outputs one file path per line (e.g., `.cursor/rules/meta/creating-rules.mdc`).

### Step 2: Read All Rules

Read each rule file using the Read tool to understand:

- Frontmatter metadata (description, globs, alwaysApply)
- Full rule content
- Purpose and when the rule should be applied

### Step 3: Generate Descriptions

For each rule, generate a context-efficient description following the Description Writing Standards below.

### Step 4: Update CLAUDE.md

Add or update the Rules section in CLAUDE.md with:

1. **Rules Discovery Instructions** (if not already present):

   - Explain how to use the Rules section
   - Instruct to review descriptions and read relevant rule files

2. **Rules Section**:
   - Organize rules by category (extract from directory structure)
   - List each rule with path and generated description

## Description Writing Standards

When generating descriptions for CLAUDE.md, follow Claude Skill description best practices:

**Format requirements:**

- Third person perspective ("This rule should be used when..." not "Use this rule when...")
- Concrete language specifying what the rule does
- Include specific triggers (contexts, file types, tasks)
- Keep under 2 sentences for context efficiency

**Adaptation process:**

- Use the rule's frontmatter description as starting point
- Read full rule content to understand complete purpose
- Transform into third-person, trigger-rich format
- Prioritize discovery information over implementation details

<example type="valid">
**Input** (from rule):
```yaml
description: USE WHEN creating Mermaid diagrams
globs: **/*.{md,mdc}
```

**Output** (for CLAUDE.md):
"This rule should be used when creating Mermaid diagrams for AI consumption in markdown or .mdc files. Provides standards for inline comments, self-contained diagrams, and embedded context to eliminate external documentation dependencies."
</example>

<example type="invalid">
**Output:**
"Use for diagrams."

❌ Not third person, too vague, missing triggers, doesn't specify what rule provides.
</example>

## CLAUDE.md Structure

The Rules section should follow this structure:

```markdown
## Project Rules

Review rule descriptions below to identify relevant rules for the current task. Read full rule files when determined to be relevant.

### [category]

- **[path-to-rule]**: [description]
- **[path-to-rule]**: [description]
```

## Helper Command

```bash
ai skill cursor-rules-synchronizer list
```

Lists all Cursor Rule file paths in the project.

**Output:** One file path per line, suitable for reading with the Read tool.

## Context Efficiency Requirements

CLAUDE.md is always loaded into context, so minimize token usage:

- Descriptions under 2 sentences each
- Focus on "what" and "when", not "how"
- Implementation details stay in rule files
- Only essential discovery information in CLAUDE.md
