---
name: vite
description: |
  Vite build tool configuration and ecosystem. Covers vite.config.ts setup, plugin authoring and popular plugins, dev server configuration (proxy, HMR, HTTPS), build optimization (chunking, tree-shaking, manual chunks, rollupOptions), library mode for publishing packages, SSR configuration, environment variables (.env handling), multi-page apps, CSS handling (PostCSS, CSS modules, preprocessors), and asset handling.

  Use when configuring Vite projects, authoring Vite plugins, optimizing builds, setting up dev server proxies, configuring SSR, handling environment variables, or troubleshooting Vite issues.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://vite.dev/guide/'
user-invocable: false
---

# Vite

## Overview

Vite is a next-generation frontend build tool that provides instant dev server start via native ES modules and optimized production builds via Rollup. It supports TypeScript, JSX, CSS preprocessors, and static assets out of the box with zero configuration.

**When to use:** Single-page apps, multi-page apps, library publishing, SSR applications, monorepo packages, any modern frontend project needing fast dev feedback and optimized builds.

**When NOT to use:** Legacy browsers requiring ES5 output without transpilation, projects locked to Webpack-specific loaders with no Vite equivalents, non-JavaScript build pipelines.

## Quick Reference

| Pattern            | API                                         | Key Points                        |
| ------------------ | ------------------------------------------- | --------------------------------- |
| Config file        | `defineConfig({})`                          | Type-safe config with IDE support |
| Conditional config | `defineConfig(({ command, mode }) => ({}))` | Different config per command/mode |
| Path alias         | `resolve.alias`                             | Map `@/` to `src/`                |
| Dev proxy          | `server.proxy`                              | Forward API requests to backend   |
| HMR config         | `server.hmr`                                | WebSocket host/port/protocol      |
| HTTPS dev          | `server.https`                              | Pass TLS cert/key options         |
| Build target       | `build.target`                              | ES module target for output       |
| Manual chunks      | `build.rollupOptions.output.manualChunks`   | Control code splitting            |
| Library mode       | `build.lib`                                 | Publish ES/CJS/UMD packages       |
| SSR build          | `build.ssr` + `ssr` options                 | Server-side rendering config      |
| Env variables      | `import.meta.env.VITE_*`                    | Client-exposed env vars           |
| loadEnv            | `loadEnv(mode, root, prefix)`               | Load env vars in config           |
| CSS modules        | `css.modules`                               | Scoped CSS class names            |
| Preprocessors      | `css.preprocessorOptions`                   | Sass/Less/Stylus options          |
| PostCSS            | `css.postcss`                               | Inline or external PostCSS config |
| Static assets      | `import url from './img.png'`               | Returns resolved public URL       |
| Plugin             | `{ name, transform, load }`                 | Hook-based plugin system          |
| Virtual module     | `resolveId` + `load` hooks                  | Generate modules at build time    |
| Multi-page         | `build.rollupOptions.input`                 | Multiple HTML entry points        |

## Common Mistakes

| Mistake                                             | Correct Pattern                                                                            |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Exposing secrets via `VITE_` prefix                 | Only prefix client-safe vars with `VITE_`; use `loadEnv` in config for server-only secrets |
| Using `process.env` in client code                  | Use `import.meta.env.VITE_*` (Vite replaces at build time)                                 |
| Modifying `rollupOptions.input` without `resolve()` | Always use `path.resolve()` or `import.meta.dirname` for absolute paths                    |
| Not externalizing peer deps in library mode         | Add React/Vue to `rollupOptions.external` to avoid bundling                                |
| Creating QueryClient-style singletons in SSR        | Ensure per-request state in SSR to avoid cross-request leaks                               |
| Inline PostCSS config alongside `postcss.config.js` | Use one or the other; inline config disables config file search                            |
| Setting `base` without trailing slash               | `base` should be `/path/` with trailing slash or full URL                                  |
| Using `__dirname` in ESM config                     | Use `import.meta.dirname` (Node 21+) or `fileURLToPath`                                    |

## Delegation

- **Plugin discovery**: Use `Explore` agent
- **Build analysis**: Use `Task` agent
- **Config review**: Delegate to `code-reviewer` agent

> If the `vitest-testing` skill is available, delegate test configuration and Vitest setup to it.
> If the `tailwind` skill is available, delegate Tailwind CSS configuration and utility patterns to it.
> If the `react-patterns` skill is available, delegate React component patterns and hooks to it.
> If the `typescript-patterns` skill is available, delegate TypeScript configuration and type patterns to it.
> If the `pnpm-workspace` skill is available, delegate monorepo workspace configuration to it.

## References

- [Configuration fundamentals and defineConfig patterns](references/configuration.md)
- [Plugin authoring and popular plugins](references/plugins.md)
- [Dev server setup: proxy, HMR, HTTPS, and middleware](references/dev-server.md)
- [Build optimization: chunking, tree-shaking, and output control](references/build-optimization.md)
- [Library mode for publishing packages](references/library-mode.md)
- [SSR configuration and Express integration](references/ssr-configuration.md)
- [Environment variables and .env file handling](references/environment-variables.md)
- [CSS handling: PostCSS, CSS modules, preprocessors, and asset management](references/css-and-assets.md)
