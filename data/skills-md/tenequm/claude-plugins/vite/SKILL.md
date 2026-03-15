---
name: vite
description: Configure and optimize Vite 7 for React projects. Covers build tooling, dev server, plugins, HMR, chunk splitting, Environment API, and Rolldown integration. Use when setting up Vite, configuring builds, optimizing bundles, managing plugins, or troubleshooting dev server. Triggers on vite, vite config, vite plugin, HMR, dev server, build optimization, chunk splitting, rolldown, vite proxy, environment api, rolldown-vite.
metadata:
  version: "0.1.0"
---

# Vite 7

Build tooling and dev server for React projects. Vite 7 (June 2025) is ESM-only, requires Node.js 20.19+ / 22.12+, and defaults browser target to `baseline-widely-available`. The user's stack uses `rolldown-vite` (Rust-based drop-in replacement), `@vitejs/plugin-react`, `@tailwindcss/vite`, `@tanstack/router-plugin`, `@cloudflare/vite-plugin`, and `@tanstack/react-start`.

## Critical Rules

### Plugin Order Matters

TanStack Start or TanStack Router plugin MUST come before `@vitejs/plugin-react`:

```ts
plugins: [
  tanstackStart(),      // or tanstackRouter() for SPA
  tailwindcss(),
  react(),              // ALWAYS last among framework plugins
]
```

Wrong order causes route generation failures and HMR breakage.

### Vite 7 is ESM-Only

Vite 7 distributes as ESM only. Your `vite.config.ts` must use `import`/`export` syntax. CJS `require()` is not supported in config files. Node.js 20.19+ supports `require(esm)` natively, so Vite can still be required by CJS consumers.

### No `tailwind.config.js`

Tailwind CSS v4 uses CSS-first configuration. Never create `tailwind.config.js`/`tailwind.config.ts`. Use `@tailwindcss/vite` plugin and configure in CSS via `@theme`, `@utility`, `@plugin`.

### Environment Variables Need VITE_ Prefix

Only variables prefixed with `VITE_` are exposed to client code via `import.meta.env`. Server-only secrets must NOT use this prefix. For type safety, augment `ImportMetaEnv` in `vite-env.d.ts`.

### splitVendorChunkPlugin Is Removed

Removed in Vite 7. Use `build.rollupOptions.output.manualChunks` for custom chunk splitting.

## Configuration

### vite.config.ts (Full Stack with TanStack Start)

```ts
import { defineConfig } from 'vite'
import { tanstackStart } from '@tanstack/react-start/plugin/vite'
import { cloudflare } from '@cloudflare/vite-plugin'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    tanstackStart(),
    cloudflare(),
    tailwindcss(),
    react(),
  ],
  resolve: {
    alias: {
      '@': new URL('./src', import.meta.url).pathname,
    },
  },
})
```

### vite.config.ts (SPA with TanStack Router)

```ts
import { defineConfig } from 'vite'
import { tanstackRouter } from '@tanstack/router-plugin/vite'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    tanstackRouter({ autoCodeSplitting: true }),
    tailwindcss(),
    react(),
  ],
  resolve: {
    alias: {
      '@': new URL('./src', import.meta.url).pathname,
    },
  },
})
```

### React Compiler

```ts
react({
  babel: {
    plugins: [['babel-plugin-react-compiler', {}]],
  },
})
```

Install: `pnpm add -D babel-plugin-react-compiler`. Auto-memoizes components and hooks - no manual `useMemo`/`useCallback`.

### Path Aliases

Use `import.meta.url` for ESM-compatible resolution (no `__dirname` in ESM):

```ts
resolve: {
  alias: {
    '@': new URL('./src', import.meta.url).pathname,
  },
}
```

Mirror in `tsconfig.json`: `"paths": { "@/*": ["./src/*"] }`

### Environment Variables

Files: `.env`, `.env.local`, `.env.[mode]`, `.env.[mode].local`. Only `VITE_`-prefixed vars exposed to client. Built-in constants: `import.meta.env.MODE`, `.DEV`, `.PROD`, `.SSR`, `.BASE_URL`.

Type augmentation in `src/vite-env.d.ts`:

```ts
interface ImportMetaEnv {
  readonly VITE_API_URL: string
}
interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

## Plugin Ecosystem

### @vitejs/plugin-react

Provides Fast Refresh (HMR for React), JSX transform, and optional Babel plugin pipeline. Always place last among framework plugins.

```ts
import react from '@vitejs/plugin-react'

react()                          // zero-config default
react({ fastRefresh: false })    // disable for debugging HMR issues
```

### @tailwindcss/vite

Native Vite integration for Tailwind CSS v4. Replaces PostCSS-based setup - no `postcss.config.js` needed.

```ts
import tailwindcss from '@tailwindcss/vite'

tailwindcss()  // zero-config, reads @theme from CSS
```

### @tanstack/router-plugin/vite

File-based route generation for TanStack Router. Must come before `react()`.

```ts
import { tanstackRouter } from '@tanstack/router-plugin/vite'

tanstackRouter({ autoCodeSplitting: true })
```

### @tanstack/react-start/plugin/vite

Full-stack plugin for TanStack Start. Includes router plugin internally - do NOT add both.

```ts
import { tanstackStart } from '@tanstack/react-start/plugin/vite'

tanstackStart()                           // default SSR
tanstackStart({ spa: { enabled: true } }) // SPA mode (no SSR)
```

### @cloudflare/vite-plugin

Runs Worker code inside `workerd` during dev, matching production behavior. Uses Vite's Environment API for runtime integration.

```ts
import { cloudflare } from '@cloudflare/vite-plugin'

cloudflare()  // reads wrangler.jsonc by default

// Programmatic config (no wrangler file needed)
cloudflare({
  config: {
    name: 'my-worker',
    compatibility_flags: ['nodejs_compat'],
  },
})
```

## Dev Server

### Proxy Configuration

```ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8787',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, ''),
    },
    '/ws': { target: 'ws://localhost:8787', ws: true },
  },
}
```

### HMR Troubleshooting

| Symptom | Fix |
|---------|-----|
| Full reload instead of HMR | Check `plugin-react` is loaded |
| HMR not connecting | Set `server.hmr.clientPort` if behind reverse proxy |
| Stale state after edit | Component must export a single component |
| CSS not updating | Ensure `@tailwindcss/vite` is in plugins |

Behind a reverse proxy:

```ts
server: {
  hmr: { protocol: 'ws', host: 'localhost', port: 5173, clientPort: 443 },
}
```

### File Warmup

```ts
server: {
  warmup: {
    clientFiles: ['./src/components/*.tsx', './src/routes/__root.tsx'],
  },
}
```

## Build Optimization

### Default Browser Target

Vite 7 targets `baseline-widely-available` (Chrome 107+, Edge 107+, Firefox 104+, Safari 16+). Override: `build.target: 'es2020'` or `['chrome90', 'safari14']`.

### Manual Chunks

```ts
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        'react-vendor': ['react', 'react-dom'],
        'tanstack': ['@tanstack/react-router', '@tanstack/react-query'],
      },
    },
  },
}
```

Dynamic splitting by function:

```ts
manualChunks(id) {
  if (id.includes('node_modules')) {
    if (id.includes('react')) return 'react-vendor'
    if (id.includes('@tanstack')) return 'tanstack'
    return 'vendor'
  }
}
```

### Bundle Analysis

```bash
pnpm add -D rollup-plugin-visualizer
```

```ts
import { visualizer } from 'rollup-plugin-visualizer'

// Add to plugins array
visualizer({ filename: 'stats.html', open: true, gzipSize: true })
```

See [build-optimization.md](references/build-optimization.md) for detailed chunking strategies, CSS splitting, asset inlining, source maps, and performance tuning.

## Rolldown Integration

### What is rolldown-vite

`rolldown-vite` is a Rust-based drop-in replacement for Vite's bundler, developed by the Vite team (sponsored by VoidZero). It replaces both esbuild and Rollup with a single high-performance tool built on Rolldown and the Oxc toolkit. Build time reductions of 3x to 16x have been reported, with memory usage cut by up to 100x on large projects.

Rolldown will become the default bundler in Vite 8 (currently in beta). Using `rolldown-vite` today prepares your project for the transition.

**Note:** Vite 7 requires Vitest 3.2+ for compatibility. Earlier Vitest versions will not work.

### Installation

In `package.json`, alias `vite` to `rolldown-vite`:

```json
{
  "devDependencies": {
    "vite": "npm:rolldown-vite@latest"
  }
}
```

For monorepos or frameworks with Vite as a peer dependency, use overrides:

```json
{
  "pnpm": {
    "overrides": {
      "vite": "npm:rolldown-vite@latest"
    }
  }
}
```

Then run `pnpm install`. No config changes needed - it is a drop-in replacement.

### Key Differences from Standard Vite

- **No esbuild dependency** - Oxc handles all transforms and minification (config still shows `minify: 'esbuild'` but the underlying engine is Oxc)
- **Faster builds** - Rust-native bundling, especially for large projects
- **Same plugin API** - Rollup/Vite plugins work without changes in most cases
- **Patch versions may break** - `rolldown-vite` follows Vite major/minor but patches are independent

### Compatibility Notes

Most frameworks and Vite plugins work out of the box. Check the [rolldown-vite repo](https://github.com/nicepkg/rolldown-vite) for known issues and changelog. Some warnings about unsupported options may appear during the transition period.

## Environment API

Experimental API introduced in Vite 6, improved in Vite 7 with the `buildApp` hook. Enables multi-target builds (browser, Node.js, edge runtimes) from a single Vite config.

### How It Works

Each environment has its own module graph, plugin pipeline, and build config. The `@cloudflare/vite-plugin` uses this to run Worker code inside `workerd` during dev, matching production behavior.

### buildApp Hook (Vite 7)

Frameworks coordinate building multiple environments. Config-level form (most common):

```ts
export default defineConfig({
  builder: {
    async buildApp(builder) {
      await builder.build(builder.environments.client)
      await builder.build(builder.environments.server)
    },
  },
})
```

Plugin hook form (for plugin authors):

```ts
{
  name: 'my-framework',
  buildApp: async (builder) => {
    const environments = Object.values(builder.environments)
    return Promise.all(
      environments.map((env) => builder.build(env))
    )
  },
}
```

### Multi-Environment Config

```ts
export default defineConfig({
  environments: {
    client: {
      build: { outDir: 'dist/client' },
    },
    server: {
      build: { outDir: 'dist/server' },
    },
  },
})
```

For most projects, the `@cloudflare/vite-plugin` or `@tanstack/react-start` handles environment configuration automatically. Direct Environment API usage is for framework authors.

## Deployment

### Cloudflare Workers (via TanStack Start)

Add `cloudflare()` to plugins and create `wrangler.jsonc`:

```jsonc
// wrangler.jsonc
{
  "name": "my-app",
  "compatibility_date": "2025-01-01",
  "compatibility_flags": ["nodejs_compat"],
  "main": "./dist/server/index.js",
  "assets": { "directory": "./dist/client" }
}
```

```bash
pnpm vite build && pnpm wrangler deploy
```

### Static SPA

Build produces `dist/`. Deploy to any static host (Cloudflare Pages, Vercel, Netlify).

### Prerendering (SSG)

```ts
tanstackStart({ prerender: { enabled: true, crawlLinks: true } })
```

## Best Practices

1. **Plugin order** - framework plugins first, then utilities, then `react()` last
2. **Use rolldown-vite** - drop-in replacement with 3-16x faster builds
3. **Set `staleTime` in dev** - avoid unnecessary refetches during HMR reloads
4. **Warm up critical files** - use `server.warmup` for frequently accessed modules
5. **Split vendor chunks** - separate `react`, `@tanstack/*` into stable chunks for caching
6. **Never use `transition-all`** - specific properties only for CSS transitions
7. **Use `import.meta.url`** for path resolution in ESM config files
8. **Analyze bundles regularly** - use `rollup-plugin-visualizer` before deploys
9. **Keep `VITE_` prefix discipline** - only public values; secrets go in server functions
10. **Set `build.sourcemap` for production** - `'hidden'` for error tracking without exposing source

## Resources

- **Vite Docs**: https://vite.dev/guide/
- **Vite 7 Blog**: https://vite.dev/blog/announcing-vite7
- **Migration Guide**: https://vite.dev/guide/migration
- **Build Options**: https://vite.dev/config/build-options
- **Server Options**: https://vite.dev/config/server-options
- **Env Variables**: https://vite.dev/guide/env-and-mode
- **Rolldown-Vite**: https://voidzero.dev/posts/announcing-rolldown-vite
- **Cloudflare Vite Plugin**: https://developers.cloudflare.com/workers/vite-plugin/
- **Plugin React**: https://github.com/vitejs/vite-plugin-react
- **GitHub**: https://github.com/vitejs/vite
