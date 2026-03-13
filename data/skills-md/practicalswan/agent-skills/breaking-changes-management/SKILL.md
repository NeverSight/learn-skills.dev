---
name: breaking-changes-management
description: Manage breaking API changes, migration guides, deprecation notices, and semver versioning. Use when introducing breaking changes, writing migration paths, updating changelogs, or releasing major versions.
license: Complete terms in LICENSE.txt
---

# Breaking Changes Management

Use this skill when behavior, interfaces, configuration, or compatibility contracts change in a way that can break consumers.

## Activation Conditions

- Releasing a major version
- Renaming or removing public APIs
- Changing request or response shapes
- Replacing config keys, env vars, CLI flags, or file formats
- Writing migration notes, deprecation notices, or upgrade checklists

## Workflow

1. Identify the exact consumer-visible break.
2. State who is affected and from which version.
3. Provide the replacement path or mitigation.
4. Add before/after examples.
5. Update `CHANGELOG.md` and any setup or usage docs that changed.

## Required Outputs

- Changelog entry with a clear `BREAKING` label
- Migration guide with old usage, new usage, and upgrade steps
- Deprecation timeline if removal is delayed
- Validation notes for any examples or scripts that changed

## Migration Checklist

- [ ] Old behavior described precisely
- [ ] New behavior described precisely
- [ ] Replacement path documented
- [ ] Upgrade steps ordered and testable
- [ ] Rollback or compatibility notes included
- [ ] README/setup docs updated if user-facing behavior changed

## References & Resources

### Documentation
- [Deprecation Procedures](./references/deprecation.md) - Deprecation wording, timelines, and migration guidance patterns

### Scripts
- [Migration Guide Scaffold](./scripts/migration-guide-scaffold.py) - Generate a migration guide skeleton with version, impact, and step sections

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-patterns](../documentation-patterns/SKILL.md) | Templates for migration guides and breaking change docs |
| [code-examples-sync](../code-examples-sync/SKILL.md) | Update code examples after breaking API changes |
| [development-workflow](../development-workflow/SKILL.md) | Versioning and release lifecycle management |
