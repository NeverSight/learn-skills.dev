---
name: markdown-lint-cleanup
description: Fix markdown lint warnings by enforcing headings, blank lines around lists, and language-tagged code fences for clean documentation.
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# Markdown Lint Cleanup

## Overview

Use this skill to clean markdown files so they pass lint checks with zero warnings. It focuses on consistent headings, spacing, and fenced code block language tags.

## When to Use

- Markdown lint warnings appear (MD022, MD032, MD036, MD040, MD031)
- Documentation updates need a clean lint pass
- Large docs need formatting normalization without content changes

## Core Rules (Required)

1. **Headings must be proper headings**
   - Replace bold-only headings with `##`, `###`, etc.
2. **Blank lines around lists**
   - Add a blank line before and after lists
3. **Blank lines around fenced code blocks**
   - Surround code fences with blank lines
4. **Language tags on fenced code blocks**
   - Use `bash`, `php`, `sql`, or `text` as appropriate

## Common Fixes

### MD036: Emphasis used instead of a heading

**Replace**:

**Section Title**

**With**:

## Section Title

### MD032: Blanks around lists

Ensure blank lines before and after lists:

Text paragraph.

- Item one
- Item two

Next paragraph.

### MD022: Blanks around headings

Add a blank line before and after headings:

Paragraph text.

#### Heading

- List item

### MD040: Fenced code language

Add a language identifier:

```text
Example output line
```

### MD031: Blanks around fences

Ensure fences are separated from other text:

Paragraph text.

```bash
php scripts/verify_uom_system.php
```

## File Safety

- Do not change meaning or content structure
- Only adjust formatting to satisfy lint rules
- Preserve links and references exactly

## Recommended Workflow

1. Identify lint warnings and their line numbers
2. Apply targeted fixes (headings, spacing, code fence languages)
3. Re-check lint until clean

## Output Expectations

- No markdown lint warnings
- No content meaning changes
- Consistent formatting across documents
