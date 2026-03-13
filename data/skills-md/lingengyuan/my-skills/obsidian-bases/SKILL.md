---
name: obsidian-bases
description: Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries. Use when working with .base files, creating database-like views of notes, or when the user mentions Bases, table views, card views, filters, or formulas in Obsidian.
allowed-tools:
  - Read
  - Write
  - Edit
---

# Obsidian Bases Skill

This skill enables Claude Code to create and edit valid Obsidian Bases (`.base` files) including views, filters, formulas, and all related configurations.

## Overview

Obsidian Bases are YAML-based files that define dynamic views of notes in an Obsidian vault. A Base file can contain multiple views, global filters, formulas, property configurations, and custom summaries.

## Core Schema

```yaml
# Global filters apply to ALL views
filters:
  and: []  # or: [], not: []

# Define formula properties
formulas:
  formula_name: 'expression'

# Configure display names
properties:
  property_name:
    displayName: "Display Name"

# Define summary formulas
summaries:
  custom_summary: 'values.mean().round(3)'

# Define views
views:
  - type: table | cards | list | map
    name: "View Name"
    limit: 10
    filters: { and: [] }
    order: [file.name, property_name]
    summaries: { property_name: Average }
```

## Quick Examples

### Example 1: Task Tracker

```yaml
filters:
  and:
    - file.hasTag("task")

formulas:
  priority_label: 'if(priority == 1, "🔴", if(priority == 2, "🟡", "🟢"))'

properties:
  formula.priority_label:
    displayName: Priority

views:
  - type: table
    name: "Tasks"
    order: [file.name, status, formula.priority_label]
```

### Example 2: Reading List

```yaml
filters:
  or:
    - file.hasTag("book")
    - file.hasTag("article")

views:
  - type: cards
    name: "Library"
    order: [file.name, author, status]
```

### Example 3: Daily Notes

```yaml
filters:
  and:
    - file.inFolder("Daily Notes")

views:
  - type: table
    name: "Recent"
    order: [file.name, file.mtime]
```

## Validation Rules

### Required Structure
- File extension: `.base`
- Valid YAML syntax
- At least one view defined

### Filters
- Can be string: `filters: 'status == "done"'`
- Can be object: `filters: { and: [...] }`
- Supported operators: `==`, `!=`, `>`, `<`, `>=`, `<=`, `&&`, `||`, `!`

### View Types
- `table`: Spreadsheet-like view
- `cards`: Visual card grid
- `list`: Simple list view
- `map`: Requires Maps plugin + lat/lng properties

### Property Types
1. Note properties: `note.author` or `author`
2. File properties: `file.name`, `file.path`, `file.mtime`, `file.tags`, etc.
3. Formula properties: `formula.my_formula`

## Summary Functions

| Name | Type | Description |
|------|------|-------------|
| Average | Number | Mathematical mean |
| Sum | Number | Sum of all numbers |
| Min/Max | Number | Smallest/Largest number |
| Count | Any | Count of values |
| Earliest/Latest | Date | Earliest/Latest date |

## Common Formulas

```yaml
# Conditional
status_icon: 'if(done, "✅", "⏳")'

# Date formatting
created: 'file.ctime.format("YYYY-MM-DD")'

# Arithmetic
total: 'price * quantity'

# String
display_name: 'author + " - " + title'
```

## YAML Quoting Rules

- Single quotes for formulas with double quotes: `'if(done, "Yes")'`
- Double quotes for simple strings: `"View Name"`
- Escape nested quotes in complex expressions

## Important Notes

1. **Filter scoping**: Use `sources` to limit search scope
2. **Markdown only**: Bases only work with `.md` files
3. **Property references**: Use `file.`, `note.`, or `formula.` prefix
4. **Date arithmetic**: Use duration strings like `"1d"`, `"1M"`, `"1h"`

## Detailed Documentation

For complete API documentation, see [REFERENCE.md](REFERENCE.md):
- Filter syntax and patterns
- All formula functions (100+ functions)
- View type configurations
- Complete examples
- Troubleshooting guide
