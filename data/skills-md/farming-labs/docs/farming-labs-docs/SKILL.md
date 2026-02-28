---
name: farming-labs-docs
description: Get started with @farming-labs/docs — MDX-based documentation for Next.js, SvelteKit, Astro, and Nuxt. Use when setting up docs, scaffolding with the CLI, choosing themes, or writing docs.config. Covers init, --template, manual setup, and theme CSS.
---

# @farming-labs/docs — Getting Started

**Always consult the project docs (and `/docs` routes when available) for the latest API and examples.**

@farming-labs/docs is a modern, flexible MDX-based documentation framework. Write markdown, get a polished docs site. Supported frameworks: **Next.js**, **SvelteKit**, **Astro**, **Nuxt**.

---

## Quick reference

### CLI

| Scenario | Command |
| -------- | ------- |
| Add docs to existing app | `npx @farming-labs/docs init` |
| Start from scratch (bootstrap project) | `npx @farming-labs/docs init --template <next \| nuxt \| sveltekit \| astro> --name <project-name>` |

### CLI flags

| Flag | Description |
| ---- | ----------- |
| `--template <name>` | Bootstrap a project: `next`, `nuxt`, `sveltekit`, `astro`. Use with `--name`. |
| `--name <project>` | Project folder name when using `--template`; prompt if omitted (e.g. `my-docs`). |
| `--theme <name>` | Skip theme prompt (e.g. `--theme fumadocs`, `--theme greentree`). |
| `--entry <path>` | Skip entry path prompt (default `docs`). |

### Packages by framework

| Framework | Core + adapter | Theme package |
| --------- | -------------- | -------------- |
| Next.js | `@farming-labs/docs`, `@farming-labs/next` | `@farming-labs/theme` |
| SvelteKit | `@farming-labs/docs`, `@farming-labs/svelte` | `@farming-labs/svelte-theme` |
| Astro | `@farming-labs/docs`, `@farming-labs/astro` | `@farming-labs/astro-theme` |
| Nuxt | `@farming-labs/docs`, `@farming-labs/nuxt` | `@farming-labs/nuxt-theme` |

### Themes (all frameworks)

`fumadocs`, `darksharp`, `pixel-border`, `colorful`, `greentree`. Theme name in config must match the theme’s CSS import path (e.g. `greentree` → `@farming-labs/theme/greentree/css` for Next).

---

## Critical: theme CSS

**Every setup must import the theme’s CSS** in the global stylesheet. Without it, docs pages will not be styled.

- **Next.js:** `app/global.css` → `@import "@farming-labs/theme/<theme>/css";` (e.g. `default`, `greentree`).
- **SvelteKit:** `src/app.css` → `@import "@farming-labs/svelte-theme/<theme>/css";`
- **Astro:** Import in the docs layout or page file: `import "@farming-labs/astro-theme/<theme>/css";`
- **Nuxt:** `nuxt.config.ts` → `css: ["@farming-labs/nuxt-theme/<theme>/css"]`

Use the same theme name in `docs.config` and in the CSS import.

---

## Core config: `defineDocs`

All frameworks use a single config file (`docs.config.ts` or `docs.config.tsx`):

```ts
import { defineDocs } from "@farming-labs/docs";
import { fumadocs } from "@farming-labs/theme"; // or svelte-theme, astro-theme, nuxt-theme

export default defineDocs({
  entry: "docs",
  contentDir: "docs", // SvelteKit/Astro/Nuxt
  theme: fumadocs(),
  metadata: {
    titleTemplate: "%s – Docs",
    description: "My documentation site",
  },
});
```

- **Next.js:** `docs.config.tsx` at project root; wrap Next config with `withDocs()` from `@farming-labs/next/config`.
- **SvelteKit:** `src/lib/docs.config.ts`; routes under `src/routes/docs/`.
- **Astro:** `src/lib/docs.config.ts`; pages under `src/pages/<entry>/`.
- **Nuxt:** `docs.config.ts` at project root; `server/api/docs.ts` and `pages/docs/[...slug].vue`.

---

## Doc content and frontmatter

Docs live under the `entry` directory (e.g. `docs/` or `app/docs/`). Each page is MDX (or Markdown) with frontmatter:

```mdx
---
title: "Installation"
description: "Get up and running"
icon: "rocket"
---

# Installation

Content here.
```

Routing is file-based: `docs/getting-started/page.mdx` → `/docs/getting-started`.

---

## Path aliases (CLI)

When running `init`, the CLI may ask about path aliases:

- **Next.js:** `@/` (e.g. `@/docs.config`) vs relative paths.
- **SvelteKit:** `$lib/` vs relative.
- **Nuxt:** `~/` vs relative.

If the user chooses “no alias”, generated code uses relative paths to `docs.config` (e.g. `../../docs.config`), and `tsconfig` may omit the `paths` block.

---

## Common gotchas

1. **Theme CSS missing** — Docs look unstyled until the theme CSS is imported in the global stylesheet (or Nuxt `css`).
2. **Wrong theme package** — Use the theme package for the same framework (e.g. `@farming-labs/svelte-theme` for SvelteKit, not `@farming-labs/theme`).
3. **From scratch** — Use `--template` with `--name <project>`; the CLI bootstraps a project with that name and runs install.
4. **Existing project** — Run `init` in the project root; the CLI detects the framework and scaffolds files.

---

## Resources

- **Repo:** [farming-labs/docs](https://github.com/farming-labs/docs)
- **Docs site:** Check the project’s `/docs` (e.g. installation, CLI, configuration).
- **Examples:** `examples/next`, `examples/nuxt`, `examples/sveltekit`, `examples/astro` in the repo.
