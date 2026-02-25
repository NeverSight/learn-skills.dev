---
name: ruler-rules-init
description: Migrate and bootstrap Ruler-based AI rules across repositories with English-first templates, preset-based project detection, and safe, idempotent setup. Use when creating or standardizing `.ruler/*` files, generating `AGENTS.md`/`CLAUDE.md`, wiring `ruler:apply` into `package.json`, adding generated-file ignores in `.gitignore`, and designing `applyTo` scoping patterns such as `**` and `web/**`.
---

# Ruler Rules Migration

## Overview

Migrate a repository to a reusable Ruler rules structure with a safe audit/apply workflow.
Keep default templates in English and avoid overwriting existing repository-specific content unless explicitly forced.
Support different project types through preset-based template selection.

## Inputs

Collect these inputs before applying changes:

- Target repository root path.
- Whether to run in `audit` or `apply` mode.
- Template preset: `auto`, `base`, `nextjs`, `monorepo`, or `node-lib` (default: `auto`).
- Whether to include optional `skills:sync:claude` integration.
- Whether overwrite is allowed for differing files (`--force`).

## Presets

Presets control the content of project-specific template files (`10-project-context.md`, `20-dev-commands.md`, `30-coding-conventions.md`). Universal files (`ruler.toml`, `AGENTS.md`, `00-core-principles.md`) are always sourced from the base directory.

| Preset | Auto-detect Signal | Use Case |
|--------|-------------------|----------|
| `base` | Fallback | Any project, minimal with placeholders |
| `nextjs` | `next.config.*` exists | Next.js App Router projects |
| `monorepo` | `turbo.json` or `pnpm-workspace.yaml` exists | Turborepo / pnpm workspace |
| `node-lib` | `package.json` has `main` or `exports`, no `next.config.*` | Node.js libraries |

### Preset Selection Priority

1. Explicit `--preset <name>` flag (highest priority).
2. Auto-detection from target repo files (when `--preset auto` or omitted).
3. Falls back to `base` if no signals match.

## Workflow

1. Run the bootstrap script in `audit` mode.
2. Review missing files, differences, and manual actions.
3. Run in `apply` mode to create missing files and safe defaults.
4. Re-run `apply` to confirm idempotency.
5. Run `ruler:apply` in the target repo to generate root rule outputs.

## Decision Tree

1. Need only Ruler integration:
Use default behavior (do not pass `--with-optional-sync`).

2. Need optional Claude skills sync as well:
Pass `--with-optional-sync` to include `skills:sync:claude` suggestions.

3. Targeting a specific project type:
Pass `--preset nextjs`, `--preset monorepo`, or `--preset node-lib`.
Or let auto-detection choose the right preset.

4. Existing files differ from templates:
- Keep defaults safe: do not override without `--force`.
- Use `--force` only when intentional template replacement is required.

## Commands

Use these commands from this skill directory:

```bash
# Audit (default preset auto-detection)
node ./scripts/bootstrap-ruler.mjs --target /path/to/repo --mode audit

# Apply with auto-detected preset
node ./scripts/bootstrap-ruler.mjs --target /path/to/repo --mode apply

# Apply with explicit preset
node ./scripts/bootstrap-ruler.mjs --target /path/to/repo --mode apply --preset nextjs
node ./scripts/bootstrap-ruler.mjs --target /path/to/repo --mode apply --preset monorepo
node ./scripts/bootstrap-ruler.mjs --target /path/to/repo --mode apply --preset node-lib
node ./scripts/bootstrap-ruler.mjs --target /path/to/repo --mode apply --preset base

# With optional sync and force
node ./scripts/bootstrap-ruler.mjs --target /path/to/repo --mode apply --preset nextjs --with-optional-sync
node ./scripts/bootstrap-ruler.mjs --target /path/to/repo --mode apply --force
```

## Validation Checklist

After applying, verify:

1. `.ruler/ruler.toml` exists and defines `codex` + `claude` outputs.
2. Required `.ruler/*.md` templates exist.
3. `.gitignore` contains the Ruler generated-files block.
4. `package.json` contains `ruler:apply`.
5. If `is-ci` style guard is used, `is-ci` is installed (`pnpm add -D is-ci`).
6. `postinstall` follows the CI-skip recommendation or an explicit local alternative (preserve existing setup commands by chaining with `&& (...)`).
7. Running `ruler:apply` succeeds in the target repository.

## Resources

- Script:
`scripts/bootstrap-ruler.mjs`

- References:
`references/migration-playbook.md`
`references/applyto-patterns.md`

- Templates:
`assets/templates/base/.ruler/` (universal + fallback)
`assets/templates/presets/nextjs/.ruler/` (Next.js overlay)
`assets/templates/presets/monorepo/.ruler/` (monorepo overlay)
`assets/templates/presets/node-lib/.ruler/` (Node.js library overlay)
