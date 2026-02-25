---
name: rspress-v2-upgrade
description: Migrate Rspress projects from v1 to v2. Use when a user asks to upgrade Rspress, follow the v1-to-v2 guide, update configs/themes, or validate the upgrade.
---

# Rspress v1 to v2 Upgrade

## Workflow

1. **Confirm current setup**
   - Read `package.json` to identify Rspress and plugin packages in use.
   - Locate the Rspress config file (commonly `rspress.config.(ts|js|mjs|cjs)`).
   - Check for custom theme files and MDX usage.

2. **Open the official upgrade guide**
   - Use the v1 → v2 guide as the source of truth:
     - <https://rspress.rs/guide/migration/rspress-1-x>

3. **Plan the upgrade path**
   - List breaking changes that apply to the project's current config, plugins, and theme.
   - Note any removed or renamed packages, options, and APIs.

4. **Update dependencies**
   - Replace `rspress` with `@rspress/core@^2.0.0`.
   - Remove packages now built into `@rspress/core` (e.g. `rspress`, `@rspress/plugin-shiki`, `@rspress/plugin-auto-nav-sidebar`, `@rspress/plugin-container-syntax`, `@rspress/plugin-last-updated`, `@rspress/plugin-medium-zoom`, `@rspress/theme-default`, `@rspress/runtime`).
   - Bump remaining Rspress plugins to latest versions via `npx taze major --include /rspress/ -w -r`.
   - Ensure Node.js >= 20.9.0.

5. **Apply config and code changes**
   - Update import paths (`rspress/runtime` → `@rspress/core/runtime`, `rspress/theme` → `@rspress/core/theme`, `@rspress/theme-default` → `@rspress/core/theme-original`).
   - If the project has a custom theme (in `theme` directory), use `@rspress/core/theme-original` to import the original theme components.
   - Update the Rspress config to match v2 options and defaults.
   - Remove deprecated or unsupported settings.

6. **Validate**
   - Run the build and dev server.
   - Fix any warnings or errors that appear in the new version. If errors or warnings occur, please refer to the [Official Upgrade Guide](https://rspress.rs/guide/migration/rspress-1-x) and first check if it's caused by any omitted or incomplete migration steps.
