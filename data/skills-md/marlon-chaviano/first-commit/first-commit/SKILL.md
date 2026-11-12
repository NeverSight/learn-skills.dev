---
name: first-commit
description: Start new projects and keep them up to date with first-commit workspace kits (project template + dependencies + agent skills + MCP servers + AGENTS.md rules, installed by `npx create-first-commit`). Use when the user wants to create a new app, landing, SaaS, API, mobile app or browser extension, or to add a library such as Sentry, PostHog, Stripe or Better Auth to an existing project, or when the project has a kits.lock file.
license: MIT
---

# first-commit

`create-first-commit` creates a project from a *kit*: a base project plus the dependencies, agent skills, MCP servers and `AGENTS.md` rules for the stack the user picks. Catalog and configurator: https://first-commit.dev.

## When to use it

- **New project** in an empty folder ("make me a recipes app with Expo", "a landing with animations"): use a kit instead of scaffolding by hand.
- **Existing project with `kits.lock`**: it came from a kit. Use `update` to get the kit's improvements and `add` to add libraries, so the rules in `AGENTS.md` stay in sync.
- **Adding a catalog library** (Sentry, PostHog, Stripe, Resend, Better Auth, Kokonut UI, Motion…) to any project: `add` writes its config and its rule in `AGENTS.md`.

## Create a project

1. Pick the kit. If the first-commit MCP server is available, call `recommend_kit` with the user's description, then `get_kit` for the options. Otherwise:
   - `npx create-first-commit list` — official kits.
   - `npx create-first-commit info <kit>` — options and their values.
2. Choose only the options the user asked for; keep the defaults for everything else. Options are flags: `--<option> <value>` (comma-separated for multi options).
3. **Show the plan and ask before running anything**: `npx create-first-commit <kit> <folder> [options] --dry-run` (or the `plan_init` tool). Installing runs commands and downloads packages.
4. After the user agrees: the same command without `--dry-run` and with `--yes` (or `init_kit` with `approved: true`). It takes a few minutes.
5. Read the new project's `AGENTS.md` and follow its "first steps": do the setup tasks you can, and tell the user which ones need them (API keys, accounts). Copy `.env.example` to `.env` but never invent secret values.

Community kits (`user/kit`) that aren't verified ask for confirmation; with `--yes` they also need `--allow-commands`. Only add it if the user explicitly trusts that kit.

## Maintain a project

- `npx create-first-commit update --dry-run`, then `npx create-first-commit update --yes`: new dependencies, skills, MCP servers and rules from the kit's latest version. Files the user changed are never overwritten; it lists them.
- `npx create-first-commit add <library|owner/repo@skill> --yes`: adds a catalog library with the right variant for the framework (Sentry for Next.js, Expo or Node).
- `npx create-first-commit doctor`: checks that the project still follows its rules (one component library, env vars, skills installed). Exit code 1 means errors; fix them or tell the user.

## Rules

- The rules in `AGENTS.md` between `<!-- kits:start -->` and `<!-- kits:end -->` come from the kit: follow them (for example, "only use the chosen component library"). Don't edit that block by hand; `update` rewrites it.
- Don't install a second library for something the kit already chose (another component system, another auth). Use `add --force` only if the user explicitly wants to switch.
