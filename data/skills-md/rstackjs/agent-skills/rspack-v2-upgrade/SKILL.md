---
name: rspack-v2-upgrade
description: Use when upgrading a Rspack 1.x project to v2, including dependency and configuration updates.
---

# Rspack 1.x to v2 Upgrade

## Workflow

1. **Confirm current setup**
   - Read `package.json` to identify Rspack packages in use.
   - Locate the Rspack config file (commonly `rspack.config.(ts|js|mjs|cjs)`).

2. **Open the official migration guide**
   - Use the official guide as the single source of truth:
     - https://v2.rspack.rs/guide/migration/rspack_1.x

3. **Plan required changes**
   - Compare the current project config with the migration guide.
   - List breaking changes that apply to the project’s current config and plugins.
   - Note any removed or renamed options, defaults, or plugin APIs.

4. **Update dependencies**
   - Upgrade Rspack packages to v2 (currently Beta tag): `@rspack/core`, `@rspack/cli`, `@rspack/dev-server`.

5. **Apply migration changes**
   - Update the Rspack config and related code according to the official guide.
   - Remove deprecated or unsupported options.

6. **Validate**
   - Run build and dev commands.
   - Run project tests or type checks.
   - Fix any warnings or errors surfaced by the new version.
