---
name: react-spa-vite
description: Scaffold and build production-ready static SPAs with Vite, React, Tailwind CSS v4, PWA support, Subresource Integrity (SRI), and image optimization. Use when creating a new React SPA, setting up a Vite + React + Tailwind stack, enabling offline/PWA behavior, hardening build output with SRI, adding image optimization, or configuring optional Vitest/Playwright testing.
---

# React SPA Vite

Create a production-ready static React SPA and keep decisions consistent.

## Workflow

1. Confirm required inputs:
- App name
- Package manager (`pnpm` preferred)
- Need for PWA and offline support
- Need for SRI hardening
- Need for image optimization
- Need for optional testing setup (Vitest, Playwright, both, or none)

2. Initialize the project with Vite React SWC TypeScript template.

3. Configure core stack:
- Tailwind CSS v4 via `@tailwindcss/vite`
- TypeScript strict settings
- Vite aliases when requested

4. Add production features requested by the user:
- PWA via `vite-plugin-pwa`
- SRI via `vite-plugin-sri-gen` (must be last in Vite plugin order)
- Image optimization via `vite-imagetools`

5. Apply sensible defaults for static deployment:
- Keep `index.html` in project root
- Keep source assets in `src/assets/*`
- Keep deployable static output in `dist/`

6. Validate setup:
- Install dependencies
- Run type checks and build
- Run preview
- Run tests only if test tooling was added

## Reference Map

Load only the reference needed for the current request:

- `references/quickstart.md`
Use for project bootstrap, dependency installation, scripts, and baseline file structure.

- `references/configuration.md`
Use for Vite plugin setup, Tailwind v4, PWA, SRI, image optimization, env vars, fonts, and common implementation patterns.

- `references/testing.md`
Use only when the user asks for unit/component tests (Vitest) or E2E tests (Playwright).

- `references/troubleshooting.md`
Use only when diagnosing build, plugin, PWA, Tailwind, asset, or dev server issues.

## Guardrails

- Keep `SKILL.md` focused on orchestration; put detailed snippets in references.
- Do not inline large templates in the main skill body.
- Prefer minimal, working defaults first; add advanced options only when requested.
- Prefer `pnpm` commands unless the user requests another package manager.
