---
name: documentation-verification
description: Validate documentation before merging - check completeness, broken links, code example accuracy, and factual correctness. Use when reviewing docs for quality gates or running pre-merge doc validation.
license: Complete terms in LICENSE.txt
---

# Documentation Verification

Use this skill when a docs change needs evidence, not just a writing pass.

## Activation Conditions

- Reviewing docs before merge or release
- Checking README, setup, or config accuracy
- Verifying local links, commands, and code samples
- Confirming docs changed alongside user-facing behavior

## Verification Workflow

1. Confirm the docs cover the changed behavior.
2. Check relative links and referenced files.
3. Validate commands and snippets where feasible.
4. Report missing coverage and stale claims explicitly.

## Review Checklist

- [ ] Public behavior changes are documented
- [ ] Local links resolve
- [ ] Examples and commands still make sense
- [ ] Setup steps reflect current tool versions
- [ ] README and CHANGELOG were updated when required

## References & Resources

### Documentation
- [Validation Procedures](./references/validation.md) - Practical checks for links, examples, config, and coverage

### Scripts
- [Doc Link Check](./scripts/doc-link-check.py) - Validate relative Markdown links across one file or an entire docs tree

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-quality](../documentation-quality/SKILL.md) | Quality standards to verify against |
| [documentation-authoring](../documentation-authoring/SKILL.md) | Verify authored docs before publishing |
| [code-examples-sync](../code-examples-sync/SKILL.md) | Validate code examples are current and working |
