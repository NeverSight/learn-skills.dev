---
name: lingui-framework-setup
description: Set up Lingui in a React framework. Use when adding Lingui to a Next.js App Router, Vite, React Router 7, Remix, or TanStack Start project, when wiring locale detection, locale-prefixed URLs, or SSR locale resolution, or when a working setup breaks after a framework or build-tool upgrade.
---

# Lingui Framework Setup

Correct Lingui setup is framework-shaped: what works in a Vite SPA breaks in React Server Components, and a module-level `i18n` singleton that is fine in the browser bleeds locales across requests under SSR. This skill routes to a framework-native recipe instead of a generic `I18nProvider` answer.

**Work in this order: detect the stack → apply the common steps → follow the framework reference → run the verification sequence.**

## Step 1 — Detect the stack

Read `package.json` and the build config before recommending anything. Never guess the compiler — the macro transform silently does nothing when wired into the wrong one.

| Signal | Stack | Reference |
|---|---|---|
| `next` in deps, `app/` or `src/app/` with `layout.tsx` | Next.js App Router | [nextjs-app-router.md](references/nextjs-app-router.md) |
| `next` in deps, `pages/` with `_app.tsx`, no `app/` | Next.js Pages Router | Supported by Lingui, brief notes in [nextjs-app-router.md](references/nextjs-app-router.md) |
| `@tanstack/react-start` in deps | TanStack Start (SSR) | [tanstack-start.md](references/tanstack-start.md) |
| `@react-router/dev` in devDeps + `react-router.config.*` | React Router 7 framework mode (SSR) | [react-router-remix.md](references/react-router-remix.md) |
| `@remix-run/dev` ≥ 2.7 in devDeps + `vite` | Remix v2 (Vite build, SSR) | [react-router-remix.md](references/react-router-remix.md) |
| `vite` + `react`, none of the above | Vite SPA (incl. declarative React Router, TanStack Router) | [vite-spa.md](references/vite-spa.md) |

Macro transform (decides what to install). On every Vite stack the default is the **native transform** in `@lingui/vite-plugin` 6.9.1+, whatever the React plugin; the Vite compiler rows are **fallbacks**, and [vite-spa.md](references/vite-spa.md) lists when they apply:

| Signal | Compiler | Macro transform |
|---|---|---|
| Any Vite stack | none needed | `lingui({ macroTransform: true })` |
| `@vitejs/plugin-react-swc` | SWC | `@lingui/swc-plugin` (pin exactly — see the swc-plugin-compatibility skill) |
| `@vitejs/plugin-react` `^5` or lower | Babel | `@lingui/babel-plugin-lingui-macro` via the plugin's `babel` option |
| `@vitejs/plugin-react` `^6`+, Vite 8 | Babel, standalone pass | v6 removed the `babel` option — run the macro as its own pass: `@rolldown/plugin-babel` + `linguiTransformerBabelPreset()`. Keeps the stock React plugin |
| `@vitejs/plugin-react` `^6`+, Vite ≤ 7 | Babel, standalone pass | Same, via `vite-plugin-babel` (no Rolldown). Switching to `@vitejs/plugin-react-swc` also works, at the cost of an exact pin |
| Next.js, no `.babelrc` | SWC | `@lingui/swc-plugin` via `experimental.swcPlugins` |
| Next.js with `.babelrc` | Babel | `@lingui/babel-plugin-lingui-macro` in `.babelrc` (a Babel config disables Next's SWC) |

One more distinction that changes everything: `react-router` in deps **without** `@react-router/dev` is a declarative SPA (`<Routes>` in JSX) — that is the Vite SPA reference, not the framework-mode one. Route-module `loader`/`+types` code written into a declarative SPA is dead on arrival.

## Step 2 — Common steps (every framework)

**Version gate.** Lingui 6 is current: ESM-only, requires Node ≥ 22.19 (or ≥ 24). Install `@lingui/core@^6 @lingui/react@^6` and dev `@lingui/cli@^6`. If the project cannot meet the Node requirement, pin every `@lingui/*` package to `^5` — do not mix majors. Do not install `@lingui/macro`: since v5 the macros live at `@lingui/react/macro` and `@lingui/core/macro`.

**Per-stack extras** (details in each reference):

| Stack | Extra runtime | Extra dev |
|---|---|---|
| Next.js App Router | — | `@lingui/swc-plugin` (exact pin) |
| Vite SPA | `@lingui/detect-locale` | `@lingui/vite-plugin` (also transforms macros) |
| React Router 7 / Remix | — | `@lingui/vite-plugin` (also transforms macros), `@lingui/format-po` |
| TanStack Start | — | `@lingui/vite-plugin` (also transforms macros) |

`@lingui/detect-locale` is browser-only (`navigator`, `localStorage`, `window.location`). Never install it on an SSR stack — it throws on the server or desyncs hydration; SSR stacks resolve locale from the request (cookie / `Accept-Language`) instead.

**Config and catalogs.** Create `lingui.config.ts` with `sourceLocale`, `locales`, and one `catalogs` entry; the lingui-best-practices skill owns catalog hygiene (build-script wiring, gitignore rules, CI drift check) and the single-sourced locale module (`locales.ts` with `resolveLocale`, `getDirection`, `localeDisplayName`) — reuse both, do not re-derive them.

**Two catalog-loading models.** On Vite-based stacks, `@lingui/vite-plugin` compiles `.po` on import — `await import('./locales/en/messages.po')` just works, there are no compiled artifacts to script or gitignore. Next.js has no Vite pipeline: run `lingui compile` prepended to `dev`/`build` scripts and import the compiled catalogs (`@lingui/loader` is webpack-only and Turbopack is the Next 15/16 default, so a loader-based setup is a trap).

## Step 3 — Framework reference

Read the matching reference file fully before editing the project. Every reference follows the same section contract, in order:

**packages → build-tool integration → `lingui.config` → locale resolution → provider/layout wiring → routing strategies → language switcher → gotchas → verification**

If the project needs locale-prefixed URLs, every reference offers the same three strategies — unprefixed source locale, all locales prefixed, or no URL locale (cookie/storage only). Restructuring routes is invasive: ask the user which strategy they want before moving files.

## Step 4 — Verify

Run in this order; each step must pass before the next:

```bash
npx lingui extract --clean   # catalogs regenerate; count matches expectations
npx lingui compile           # only on stacks with compiled catalogs (Next.js)
npx tsc --noEmit             # types resolve, incl. catalog imports
npm run build                # macro wiring errors surface here
```

**Then prove the transform ran.** A green build does not: a mis-wired macro transform is silently a no-op and the app ships in the source language. Translate one string in a non-source catalog, run the app in that locale, and confirm the translation reaches the browser (each reference gives the stack's exact check — `curl` the server-rendered HTML on SSR stacks, hard-load a deep link on the SPA). The setup is done when you have seen a translated string, not when the build is green.

Raw untranslated text at that point is a compiler wiring problem — wrong plugin, bare-string SWC entry, or the `@vitejs/plugin-react@6` babel trap; see the swc-plugin-compatibility skill. On the native transform, a missing `macroTransform: true` is not silent: the untransformed macro import throws "being executed outside the context of compilation" in the browser.

## Adding a new framework

Another stack (a new meta-framework, a new build tool) costs two edits: one row in the Step 1 detection table, and one file under `references/` following the Step 3 section contract. Framework-specific facts go in the reference; anything true of every stack — the version gate, the two catalog-loading models, the SSR `detect-locale` rule — stays here, stated once. Every non-obvious rule carries a one-sentence why.

## Related skills

- **lingui-best-practices** — macro selection, catalog hygiene, the shared locale module. This skill assumes it; don't duplicate it.
- **swc-plugin-compatibility** — SWC plugin version pinning and the silent-failure modes of a mis-wired transform.
- **migrate-i18next-to-lingui** — if the project already has i18next, migrate first, then return here for framework wiring.
