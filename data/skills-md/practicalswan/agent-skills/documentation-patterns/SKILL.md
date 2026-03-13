---
name: documentation-patterns
description: Templates and structural patterns for API docs, feature docs, config guides, and REST endpoint documentation. Use when structuring docs, applying Markdown templates, or standardizing doc formats.
license: Complete terms in LICENSE.txt
---

# Documentation Patterns

Use this skill when the main problem is document shape and consistency rather than writing quality alone.

## Activation Conditions

- Creating a new API, feature, or config guide
- Standardizing Markdown sections across repositories
- Writing migration or runbook documents
- Picking the right template for a doc request

## Pattern Selection

- API docs: endpoints, auth, request and response schema, errors
- Feature docs: purpose, UX, dependencies, rollout, support
- Config docs: env vars, defaults, examples, failure modes
- Migration docs: changed behavior, upgrade path, verification

## References & Resources

### Documentation
- [API Documentation Templates](./references/api-templates.md) - Endpoint, SDK, and function documentation patterns
- [Feature Documentation Templates](./references/feature-templates.md) - Feature overview, rollout, and troubleshooting patterns
- [Configuration Documentation Templates](./references/config-templates.md) - Config and environment variable templates

### Scripts
- [Doc Template Picker](./scripts/doc-template-picker.py) - Print a starter Markdown template for `api`, `feature`, `config`, or `migration`

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-authoring](../documentation-authoring/SKILL.md) | Use patterns when creating new documents |
| [documentation-quality](../documentation-quality/SKILL.md) | Quality standards that patterns should follow |
| [breaking-changes-management](../breaking-changes-management/SKILL.md) | Templates for migration guides and changelogs |
