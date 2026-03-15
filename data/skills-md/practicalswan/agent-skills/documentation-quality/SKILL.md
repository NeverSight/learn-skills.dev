---
name: documentation-quality
description: Documentation quality standards and writing principles. Use when establishing formatting rules, reviewing doc quality metrics, creating writing guidelines, or enforcing consistent documentation style across a project.
license: Complete terms in LICENSE.txt
---

# Documentation Quality Standards

Use this skill when documentation should be judged against explicit standards instead of subjective preference.

## Activation Conditions

- Reviewing docs before merge
- Creating or updating a style guide
- Defining expectations for examples, structure, and terminology
- Auditing a docs set for consistency and readability

## Core Standards

- Clear audience and scope
- Stable heading hierarchy
- Runnable or honest examples
- Consistent terminology
- Explicit edge cases, constraints, and failure modes

## Quality Checklist

- [ ] Title and purpose are clear
- [ ] Heading levels do not jump unexpectedly
- [ ] Code examples have language tags and realistic inputs
- [ ] Commands match current tooling
- [ ] Links and file paths are accurate

## References & Resources

### Documentation
- [Writing Standards](./references/writing-standards.md) - Clarity, example quality, terminology, and formatting guidance

### Scripts
- [Doc Style Audit](./scripts/doc-style-audit.py) - Check Markdown files for heading jumps, long lines, tabs, and trailing whitespace

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-authoring](../documentation-authoring/SKILL.md) | Apply quality standards during doc creation |
| [documentation-verification](../documentation-verification/SKILL.md) | Verify quality metrics before merging docs |
| [documentation-patterns](../documentation-patterns/SKILL.md) | Patterns that enforce quality consistency |
