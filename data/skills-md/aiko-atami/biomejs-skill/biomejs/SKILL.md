---
name: biomejs
description: Configure and operate BiomeJS in JavaScript/TypeScript projects, including installation, `biome.json` setup, formatter/linter/check workflows, VCS integration, and CI usage. Use when users ask to adopt Biome, tune rules/includes, set up monorepo/shared configs, or troubleshoot Biome command behavior.
---

# BiomeJS

Use this skill to implement and operate BiomeJS with predictable steps and minimal disruption.
For ESLint/Prettier migration, use the dedicated `eslint-prettier-migration` skill.

## Workflow

1. Identify intent:
- Fresh setup
- Config tuning
- CI/VCS integration
- Diagnostics troubleshooting

2. Apply the matching path:
- Fresh setup: follow `references/getting-started.md`
- Config and file-scoping: follow `references/configuration-and-vcs.md`
- Advanced config templates: follow `references/advanced-configuration-templates.md`
- CLI options/reporters: follow `references/cli-basics.md`
- Monorepo and shared config strategy: follow `references/monorepo-and-upgrades.md`
- Performance debugging: follow `references/performance-tracing.md`
- Pre-commit hooks and CI recipes: follow `references/automation-ci-and-hooks.md`

3. Verify with a no-write pass before auto-fixing:
- Run `biome check .`
- Then run `biome check --write` only after confirming scope and intended changes

## Operational Defaults

Use these defaults unless user asks otherwise:
- Pin Biome version when installing (`-E` with package managers that support it).
- Keep config in project root (`biome.json` or `biome.jsonc`).
- Run `biome check --write` for unified format+lint+organize imports.
- Run `biome ci` in CI pipelines.

## References

- Setup and baseline commands: `references/getting-started.md`
- Configuration, includes, and VCS integration: `references/configuration-and-vcs.md`
- Advanced configuration templates and migration-safe patterns: `references/advanced-configuration-templates.md`
- Useful CLI commands and options: `references/cli-basics.md`
- Monorepo setup and v1->v2 upgrade notes: `references/monorepo-and-upgrades.md`
- Slowness investigation and tracing spans: `references/performance-tracing.md`
- Git hooks and CI recipes: `references/automation-ci-and-hooks.md`
