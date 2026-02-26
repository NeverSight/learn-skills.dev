---
name: eslint-prettier-migration
description: Migrate projects from ESLint and/or Prettier to BiomeJS with safe sequencing, flag selection (`--include-inspired`, `--include-nursery`), config-translation review, ignore parity checks, and post-migration stabilization. Use when users ask to replace ESLint/Prettier, port legacy or flat ESLint configs, migrate Prettier options/ignores, or troubleshoot migration command limits and behavior differences.
---

# ESLint + Prettier Migration

Use this skill to migrate existing lint/format toolchains to BiomeJS with predictable risk.
Run ESLint migration first, then Prettier migration.

## Workflow

1. Confirm migration scope:
- ESLint only
- Prettier only
- Both ESLint and Prettier

2. Follow the migration playbook:
- `references/eslint-prettier-migration.md`

3. Run migration with explicit flag choices:
- `biome migrate eslint --write`
- Optionally add `--include-inspired` if user wants broader parity with inspired rules.
- Optionally add `--include-nursery` only when user accepts unstable rules.
- `biome migrate prettier --write` after ESLint migration.

4. Review migration output before mass rewrites:
- Verify generated `biome.json` for renamed rules, overrides, globals, and ignore behavior.
- Confirm ESLint migration may overwrite prior Biome baseline (for example, `linter.rules.recommended` can change).

5. Validate and stabilize:
- Run `biome check .`
- Then run `biome check --write .` after confirming file scope
- If migration introduces too many new lint failures, use:
  `biome lint --write --unsafe --suppress="suppressed due to migration"`

6. Finalize CI checks:
- Run `biome ci .`

## Operational Defaults

Use these defaults unless user asks otherwise:
- Ensure `biome.json` exists before migration (`biome init` if needed)
- Use official migration commands before manual config editing
- Review generated rule mapping and overrides manually
- Align ignore behavior via VCS integration when needed (`vcs.enabled`, `vcs.clientKind`, `vcs.useIgnoreFile`)
- Use EN docs as canonical references when migration behavior is ambiguous

## References

- ESLint/Prettier migration playbook: `references/eslint-prettier-migration.md`
