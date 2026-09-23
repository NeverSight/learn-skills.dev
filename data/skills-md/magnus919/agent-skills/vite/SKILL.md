---
name: vite
description: >-
  Operate Vite projects: inspect versions and configuration, run bounded development
  and production builds, diagnose dependency and asset failures, and configure
  environment-aware frontend delivery. Use when a task names Vite, vite.config,
  Vite plugins, import.meta.env, dev-server behavior, or Vite build output. Do not
  use for frontend architecture or visual implementation (route to frontend-engineering),
  CI/platform provisioning (route to platform-engineering), browser automation
  (route to playwright), or accessibility design (route to web-accessibility).
license: MIT
compatibility: Requires Python 3.8+ for the bundled diagnostic script; Node.js and the project's package manager are required for Vite commands.
metadata:
  source: https://vite.dev/guide/
  spec: https://vite.dev/config/
---

# Vite Operations

Use this skill for the Vite toolchain itself: project discovery, config and plugin behavior, environment loading, dev-server diagnostics, production builds, and asset/deployment boundaries. Keep application architecture and UI implementation with [frontend-engineering](../frontend-engineering/SKILL.md), infrastructure and CI design with [platform-engineering](../platform-engineering/SKILL.md), browser tests with [playwright](../playwright/SKILL.md), and accessibility implementation/review with [web-accessibility](../web-accessibility/SKILL.md).

## Operating contract

1. **Discover before changing.** Read `package.json`, lockfile, `vite.config.*`, `tsconfig*.json`, scripts, framework plugin, and deployment assumptions. Identify the package manager from the lockfile; do not invent a command.
2. **Check the actual toolchain.** Run `scripts/vite-doctor --json` from this skill or the project root to capture Node, package-manager, Vite package, config, and environment evidence. A Vite version in documentation is not proof of the installed version.
3. **Keep configuration explicit.** Review `root`, `base`, `resolve.alias`, plugins, `server.host/port`, `preview`, `build.outDir`, `build.rollupOptions`, and `define`. Treat `define` and `import.meta.env` as compile-time/public data; never place secrets in `VITE_*` variables or client bundles.
4. **Build before claiming success.** Use the project's existing script (normally `npm run build`, `pnpm build`, `yarn build`, or `bun run build`) with a bounded timeout. Inspect output files and warnings, then exercise the built app at its deployed base path when possible.
5. **Treat mutations as gated.** Read-only discovery may proceed. Before installing packages, editing config, deleting output, starting a server, or changing deployment settings, confirm the target, scope, and rollback path. Prefer a new output directory or version-controlled change and never overwrite a user's uncommitted work.
6. **Keep evidence bounded.** Summarize logs and errors; do not paste `.env` contents, tokens, full bundles, or generated dependency trees.

## Common workflow

- **New project or migration:** verify Node and package manager, inspect the existing app entry point, choose the framework plugin, preserve the lockfile, and use the official Vite scaffold only when the target directory is empty or explicitly approved.
- **Config change:** make the smallest change, explain why `base` and asset paths remain correct, and run a production build. Config files are executable code; do not load arbitrary config values into `define`.
- **Environment issue:** distinguish `.env`, `.env.local`, mode-specific files, and process environment. Only variables prefixed `VITE_` are exposed by default; restart the dev server after changes. Validate required values without printing their values.
- **Dev-server issue:** check port/host/proxy and whether the request is same-origin. A server reachable from another device may require an explicit host and network policy review; do not expose it casually.
- **Build issue:** capture the first actionable error, check plugin and Node/Vite compatibility, clear only reproducible caches after approval, and rerun the smallest failing command. Do not paper over a module-resolution failure with broad alias changes.
- **Deployment issue:** confirm `base`, SPA fallback, static asset caching, and the hosting platform's output directory. A successful build does not prove deep links or client routing work.

## Reference routing

| Load when | Reference |
|---|---|
| Config, plugins, modes, env variables, aliases, or public assets | `references/config-and-environments.md` |
| Build output, dependency failures, performance, or deployment | `references/build-and-deploy.md` |
| Dev server, proxy, preview, diagnostics, or safe operations | `references/dev-server-and-diagnostics.md` |

## Verification boundary

A Vite task is complete when the requested config or artifact exists, the relevant command exits successfully, and the boundary is checked: build output for builds, a reachable route and assets for deployment, and user-visible browser behavior through [playwright](../playwright/SKILL.md) for E2E claims. State any untested browser, host, mode, or deployment assumption explicitly.

## When not to use

- Frontend component architecture, state, responsive UI, or general web implementation: [frontend-engineering](../frontend-engineering/SKILL.md).
- Infrastructure, CI runners, containers, hosting topology, or release policy: [platform-engineering](../platform-engineering/SKILL.md).
- Authoring or operating browser automation: [playwright](../playwright/SKILL.md).
- WCAG audits, accessible interaction design, or semantic accessibility remediation: [web-accessibility](../web-accessibility/SKILL.md).
- Rollup internals or a non-Vite bundler migration: use the relevant tool or methodology skill; Vite-specific behavior may still be consulted for an existing Vite project.
