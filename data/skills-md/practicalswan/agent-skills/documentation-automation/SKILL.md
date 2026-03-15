---
name: documentation-automation
description: Automate doc generation with JSDoc/TSDoc, linters, and pre-commit hooks. Use when setting up markdownlint, configuring doc linting pipelines, integrating JSDoc/TSDoc, or building automated documentation workflows.
license: Complete terms in LICENSE.txt
---

# Documentation Automation

Use this skill when documentation quality should be enforced by scripts, CI, or local hooks instead of manual review alone.

## Activation Conditions

- Adding `docs:*` scripts to a project
- Setting up markdownlint, cspell, lychee, or remark-lint
- Generating API docs from source comments
- Adding pre-commit or CI validation for docs
- Standardizing documentation checks across repositories

## Automation Targets

- Build generated API docs
- Lint Markdown structure and style
- Check internal and external links
- Validate code examples and commands
- Enforce changelog or README updates when behavior changes

## Recommended Pipeline

1. Add local commands that can run without CI.
2. Make CI call the same commands.
3. Keep failure output actionable and fast.
4. Prefer incremental checks in pre-commit and fuller checks in CI.

## References & Resources

### Documentation
- [Automated Tools](./references/tools.md) - Current doc tooling options by language and validation task

### Scripts
- [Docs Pipeline Scaffold](./scripts/docs-pipeline-scaffold.py) - Print starter `docs:*` scripts and a CI checklist for Node or Python projects

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-authoring](../documentation-authoring/SKILL.md) | Generate docs that automation tools process |
| [devops-tooling](../devops-tooling/SKILL.md) | Pre-commit hooks and CI pipeline integration |
| [documentation-verification](../documentation-verification/SKILL.md) | Automated validation in doc pipelines |
