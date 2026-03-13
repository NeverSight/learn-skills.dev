---
name: code-examples-sync
description: Synchronize and verify code examples in documentation. Use when function signatures change, API interfaces update, imports shift, or documentation snippets become outdated and need correction.
license: Complete terms in LICENSE.txt
---

# Code Example Synchronization

Use this skill when docs contain code snippets that are likely to drift from the real implementation.

## Activation Conditions

- Function signatures changed
- Imports or package names changed
- Request or response contracts changed
- Framework guidance or recommended patterns changed
- A doc snippet compiles conceptually but no longer matches the codebase

## Workflow

1. Find the canonical implementation first.
2. Update every affected snippet in docs, examples, and READMEs.
3. Verify syntax, imports, and expected outputs.
4. Note any intentional divergence, such as simplified tutorial snippets.

## Quality Checklist

- [ ] Snippet matches current API shape
- [ ] Imports and package names are current
- [ ] Async, error handling, and setup steps still make sense
- [ ] Output examples match current behavior
- [ ] Duplicate snippets across docs were updated together

## References & Resources

### Documentation
- [Code Example Verification](./references/verification.md) - Checks for examples, imports, outputs, and compatibility

### Scripts
- [Example Sync Check](./scripts/example-sync-check.py) - Audit Markdown files for untyped fences, placeholder text, and obviously stale examples

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-verification](../documentation-verification/SKILL.md) | Validate code examples before merging docs |
| [documentation-authoring](../documentation-authoring/SKILL.md) | Keep authored docs in sync with code changes |
| [breaking-changes-management](../breaking-changes-management/SKILL.md) | Update examples after breaking API changes |
