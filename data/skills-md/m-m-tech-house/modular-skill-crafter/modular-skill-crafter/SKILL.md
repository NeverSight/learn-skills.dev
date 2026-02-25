---
name: modular-skill-crafter
description: Guidelines and rules for creating new skills that adhere to the standard skill structure.
license: MIT
metadata:
  author: System
  version: "1.0.0"
---

# Skills Crafter

Comprehensive guide for creating, structuring, and maintaining agent skills.

## When to use this skill

Reference these guidelines when:

- Creating a new skill from scratch
- Refactoring an existing skill
- Adding new rules to a skill
- Organizing skill resources and examples
- Validating skill structure and compliance

## Rule Categories by Priority

| Priority | Category  | Impact   | Prefix     |
| -------- | --------- | -------- | ---------- |
| 1        | Structure | CRITICAL | `struct-`  |
| 2        | Metadata  | HIGH     | `meta-`    |
| 3        | Content   | MEDIUM   | `content-` |

## Quick Reference

### 1. Structure (CRITICAL)

- `struct-skill-scaffold` - Follow the strict directory hierarchy (`SKILL.md`, `rules/`, `examples/`).
- `struct-modular-rules` - Break rules into individual markdown files in the `rules/` directory.

### 2. Metadata (HIGH)

- `meta-frontmatter` - Include complete YAML frontmatter in `SKILL.md`.
- `meta-naming` - Use semantic, kebab-case naming for skills and files.
- `meta-rule-categories` - Define priority categories and use prefixes for rule files.

### 3. Content (MEDIUM)

- `content-rule-format` - Use the standard Why/Incorrect/Correct format for rule definitions.

## How to Use

Read individual rule files for detailed explanations and examples:

```
rules/struct-skill-scaffold.md
rules/meta-frontmatter.md
rules/meta-rule-categories.md
rules/content-rule-structure.md
```

Each rule file contains:

- Brief explanation of why it matters
- Incorrect example with explanation
- Correct example with explanation
