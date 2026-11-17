---
name: typescript-dev
description: Full-stack TypeScript with Vite 8, React 19, Tailwind v4, shadcn/ui, Biome, Vitest, and Hono 4. Use when setting up or working in a TypeScript project - components, styling, build and HMR, tests, lint/CI, or a Hono API with type-safe RPC.
metadata:
  version: "0.5.0"
  categories: "development"
  topics: "typescript, vite, react, tailwind, hono"
  openclaw:
    homepage: https://github.com/tenequm/skills/tree/main/skills/typescript-dev
    emoji: "🟦"
  upstream: "vite@8.3.6, @vitejs/plugin-react@6.2.1, @rolldown/plugin-babel@0.3.0, react@19.3.1, typescript@7.0.2, tailwindcss@4.3.4, @biomejs/biome@2.6.5, vitest@5.1.0, babel-plugin-react-compiler@1.0.0, class-variance-authority@0.7.1, hono@4.13.16, @hono/node-server@2.1.6, shadcn@4.23.0, cn@0.5.2"
---

# TypeScript Frontend Development

One coherent stack for building type-safe TypeScript apps: **Vite 8** (build + dev server, Rolldown-powered), **React 19.3** with the React Compiler, **TypeScript 7.0** (strict, Go-native), **Tailwind CSS v4.3 + shadcn/ui** for styling, **Biome 2.6** for linting and formatting, **Vitest 5** for testing, and **Hono 4** for the backend/edge API. The pieces are designed to fit together - this skill covers how they wire up and the sharp edges that span more than one of them. Hono's RPC client (`hc`) shares server types directly with the React frontend, so the front and back end stay type-safe end to end without codegen.

The body below is the cross-cutting layer: the rules that bite when these tools meet, plus one working end-to-end setup. Each tool also has a deep-dive reference - read the one you need:

- **[references/vite.md](references/vite.md)** - Vite 8 config, dev server, proxy, HMR, Rolldown, code splitting, build optimization, deployment.
- **[references/react.md](references/react.md)** - React 19 patterns: Actions, `use()`, Activity, `<ViewTransition>`, Fragment refs, `useEffectEvent`, document metadata, and the React Compiler.
- **[references/typescript.md](references/typescript.md)** - Strict TypeScript 7.0 config and patterns: tsconfig defaults, the 6.0 compat path for API-consuming tools, generics, `import defer`.
- **[references/tailwind.md](references/tailwind.md)** - Tailwind CSS v4 CSS-first config, OKLCH theming, dark mode, v4.3 utilities.
- **[references/shadcn.md](references/shadcn.md)** - shadcn/ui CLI, component authoring with CVA + `data-slot`, the `cn` package, registries, Base UI / Radix / React Aria.
- **[references/biome.md](references/biome.md)** - Biome config, `biome check`, domains, type-aware linting, GritQL, ESLint/Prettier migration.
- **[references/vitest.md](references/vitest.md)** - Vitest 5 config, Testing Library, mocking, coverage, browser mode, projects, v4->v5 migration, test speed.
- **[references/hono.md](references/hono.md)** - Hono 4 web framework: routing, context, middleware, validation (Zod), end-to-end type-safe RPC, OpenAPI, helpers, and multi-runtime deployment (Workers/Node/Bun/Deno).

## Version targets

| Tool | Version | Note |
|------|---------|------|
| Vite | 8.3.6 | Rolldown is the single default bundler |
| @vitejs/plugin-react | 6.2.1 | v6 removed the inline `babel` option |
| @rolldown/plugin-babel | 0.3.0 | runs the React Compiler for plugin-react v6 |
| React / react-dom | 19.3.1 | React Compiler is stable (1.0); 19.3.1 patches a critical RSC RCE |
| babel-plugin-react-compiler | 1.0.0 | pin with `--save-exact` |
| TypeScript | 7.0.2 | Go-native, ~10x faster; ships no JS API (6.0 compat path in typescript.md) |
| Tailwind CSS | 4.3.4 | CSS-first config, no JS config file |
| shadcn/ui CLI | 4.23.0 | Base UI is the default base; `cn` is its own package |
| Biome | 2.6.5 | single binary for lint + format + imports (2.6 adds Markdown, SCSS, YAML) |
| Vitest | 5.1.0 | Vite-native test runner; reuses vite.config |
| Hono | 4.13.16 | Web Standards backend/edge framework; v5 is a release candidate (`hono@next`) |

**Node.js 22.12+** is the effective floor for the stack: Vite alone accepts 20.19+, but Vitest 5, `@rolldown/plugin-babel`, and Hono v5 require 22.12+, and `cn` 0.5 requires 22+.

## Cross-cutting critical rules

These are the rules that fail in confusing ways precisely because they sit at the seam between two tools. The single-tool details live in the references.

### Vite plugin order: framework plugins first, `react()` last

When a framework plugin (TanStack Router/Start, etc.) generates routes or transforms code, it must run before `@vitejs/plugin-react` so React's Fast Refresh transform sees the final output. Wrong order causes route-generation failures and broken HMR.

```ts
plugins: [
  tanstackStart(),   // or tanstackRouter() for SPA - framework first
  tailwindcss(),
  react(),           // React plugin last among framework plugins
]
```

### React Compiler replaces manual memoization - and changes how you wire Vite

React Compiler 1.0 auto-memoizes components, computations, and callbacks at build time. Write plain components; do not reach for `useMemo`/`useCallback`/`memo`. The catch lives at the Vite seam: **`@vitejs/plugin-react` v6 removed the inline `babel` option**, so the old `react({ babel: { plugins: [...] } })` wiring no longer works. The compiler now runs through a separate Babel plugin:

```ts
import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import babel from '@rolldown/plugin-babel'

plugins: [react(), babel({ presets: [reactCompilerPreset()] })]
```

Install: `pnpm add -D @rolldown/plugin-babel @babel/core babel-plugin-react-compiler @types/babel__core`.

Leave `@rolldown/plugin-babel`'s new `parallel` option (0.3) off here: `reactCompilerPreset()` cannot be sent to a worker thread, so `babel({ parallel: true, presets: [reactCompilerPreset()] })` fails the build.

plugin-react 6.1+ also ships an **experimental** native (Rust) compiler path, `react({ compiler: true })`, that skips Babel entirely - see [react.md](references/react.md) for its install trap. The Babel wiring above remains the stable route.

This also ripples into Biome: `useExhaustiveDependencies` can't tell the compiler is handling deps for you, so most compiler users turn it off (see [biome.md](references/biome.md)).

### Tailwind v4 is CSS-first - there is no `tailwind.config.js`

Tailwind v4 configures everything in CSS via `@theme`, `@utility`, `@plugin`, `@source`. Never create or look for `tailwind.config.js`/`.ts`. The Vite integration is the `@tailwindcss/vite` plugin (no PostCSS config either). If you find a `tailwind.config.js` in a v4 project, it is leftover - delete it and migrate the values into CSS. Full details in [tailwind.md](references/tailwind.md).

### Style with semantic tokens, never raw palette or dynamic class names

```tsx
<div className="bg-primary text-primary-foreground">   // respects theme + dark mode
<div className="bg-blue-500 text-white">               // breaks theming - avoid
```

And never assemble class names from fragments (`bg-${color}-500`) - Tailwind's scanner only sees complete literal strings, so dynamic names silently produce no CSS. Use a lookup map of full class strings.

### TypeScript 7.0: lean on the new defaults, and know it has no JS API

TS 6.0 and 7.0 bake in much of what used to be manual: `strict` and `noUncheckedSideEffectImports` are **on by default**, so drop them from a fresh tsconfig. Two defaults break a Vite app if ignored: `types` defaults to `[]`, and side-effect imports are now checked - so `import "./styles.css"` fails (TS2882) and `import.meta.env` is untyped (TS2339) until you add `"types": ["vite/client"]` (append `"node"` etc. as needed). `baseUrl` is deprecated - use prefixed `paths`.

A plain `pnpm add -D typescript` now installs **7.0**, which ships the `tsc` binary but **no programmatic API** (it returns until 7.1). This stack is fine - Biome, plugin-react, and the shadcn CLI never import `typescript` - but typescript-eslint, framework checkers (Vue, Astro, Svelte, MDX), and anything else that does `import ts from "typescript"` need the official 6.0 alias pair. See [typescript.md](references/typescript.md).

### Vite never type-checks - gate on `tsc -b`

`vite dev` and `vite build` only strip types, so a type error ships green unless something runs `tsc`. Use the create-vite solution layout - it also type-checks `vite.config.ts`, which an app-only `"include": ["src"]` never does - and put the check in front of the build:

```jsonc
// tsconfig.json - the solution file that `tsc -b` builds
{ "files": [], "references": [{ "path": "./tsconfig.app.json" }, { "path": "./tsconfig.node.json" }] }
```

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "typecheck": "tsc -b",
    "check": "biome check --write . && tsc -b && vitest run",
    "check:ci": "tsc -b && biome ci --error-on-warnings . && vitest run"
  }
}
```

`tsconfig.app.json` is the config in the end-to-end setup below; `tsconfig.node.json` covers the config file (`"include": ["vite.config.ts"]`, `"types": ["node"]`, `"module": "nodenext"`). Give each a `"tsBuildInfoFile": "./node_modules/.tmp/<name>.tsbuildinfo"` so incremental build info stays out of the source tree. `check` fixes locally; `check:ci` only verifies, and `--error-on-warnings` matters because `biome ci` exits 0 when only warnings remain. Run the project's own `tsc` (scripts or `pnpm exec tsc`), never a global `tsc` or `npx tsc` - a stale global TypeScript reports bogus option errors. With TanStack Router, commit `routeTree.gen.ts` (its FAQ says so): the plugin only regenerates it during `vite dev`/`build`, so a fresh clone's `tsc -b` fails without it.

### One Biome command, and `files.includes` is the only include key

Run `biome check` (or `biome ci`) - it formats, lints, and organizes imports in a single pass; never split into separate `lint`+`format` calls. And in Biome 2.x the only file-selection key is `files.includes` (with the `s`); `files.ignore`/`files.include`/`files.exclude` do not exist and throw `Found an unknown key`. Exclude with negation: `"includes": ["**", "!**/routeTree.gen.ts"]`. More in [biome.md](references/biome.md).

### Hono RPC ties the backend's types to the React frontend - keep them in sync

When the API is Hono, the React app talks to it through the `hc<AppType>()` client, which
imports the server's exported `typeof app` directly. That shared type is the seam: it only
works if **both sides run the same Hono version** and both `tsconfig.json` set `"strict": true`
(a mismatch throws "Type instantiation is excessively deep"). Two more rules that bite at this
seam: handlers must specify status codes (`c.json(data, 200)`) for the client to infer
responses, and routes the client calls must not use `c.notFound()`. As the route count grows,
compile the client type once (`hcWithType`) so the IDE stays fast. `import type { AppType }` is erased from the client bundle, so
there is no need to hand-mirror server types to keep server code out of it. Run `pnpm why hono` to catch a
second copy pulled in by an adapter's peer range. If Hono handles CORS behind the Vite dev server,
set `server.cors: false` in `vite.config.ts` so the two CORS layers don't conflict. Full details in
[hono.md](references/hono.md).

## End-to-end setup

A minimal but complete React + TypeScript + Tailwind + Biome project. Swap the framework plugin for your router/SSR choice (see [vite.md](references/vite.md) for TanStack and Cloudflare variants).

### vite.config.ts

```ts
import { defineConfig } from 'vite'
import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import babel from '@rolldown/plugin-babel'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    tailwindcss(),
    react(),
    babel({ presets: [reactCompilerPreset()] }),
  ],
  resolve: {
    alias: { '@': new URL('./src', import.meta.url).pathname },
  },
})
```

`import.meta.url` is the ESM-correct way to resolve paths - there is no `__dirname` in an ESM config, and Vite configs are ESM-only.

### tsconfig.app.json (TypeScript 7.0, also valid on 6.0)

```jsonc
{
  "compilerOptions": {
    // strict + noUncheckedSideEffectImports are ON by default since 6.0 - omitted on purpose
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.app.tsbuildinfo",
    "target": "es2023",
    "module": "preserve",
    "moduleResolution": "bundler",
    "moduleDetection": "force",
    "jsx": "react-jsx",
    "verbatimModuleSyntax": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "erasableSyntaxOnly": true,
    "skipLibCheck": true,
    "noEmit": true,
    "types": ["vite/client"],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["src"]
}
```

`module: preserve` + `moduleResolution: bundler` is the right pairing for a Vite-bundled app; use `nodenext` instead only for Node-executed code. `"types": ["vite/client"]` is load-bearing: it declares CSS/asset modules and `import.meta.env`, without which the default-on side-effect-import check rejects `import "./styles.css"`. Other ambient types stay out until you list them (`"node"`, `"vitest/globals"`). `exactOptionalPropertyTypes` means an optional prop that may receive `undefined` must be declared `prop?: T | undefined`.

### biome.json

```json
{
  "$schema": "./node_modules/@biomejs/biome/configuration_schema.json",
  "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true },
  "files": { "includes": ["**", "!**/components/ui", "!**/routeTree.gen.ts"] },
  "formatter": { "enabled": true, "indentStyle": "space", "lineWidth": 100 },
  "linter": {
    "enabled": true,
    "rules": { "preset": "recommended" },
    "domains": { "react": "recommended" }
  },
  "javascript": { "formatter": { "quoteStyle": "double" } },
  "assist": { "enabled": true, "actions": { "source": { "organizeImports": "on" } } }
}
```

### src/styles.css

```css
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));

:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --radius: 0.5rem;
}
.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);
}

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
}
```

The `@import "tailwindcss";` line is load-bearing: the `@tailwindcss/vite` plugin alone produces no styles without it - a missing import is the classic "Tailwind renders nothing" footgun. Use `@theme inline` (not plain `@theme`) for tokens that reference CSS variables, so they track dark-mode changes. The `@custom-variant dark` line makes `dark:` utilities follow the `.dark` class; without it they follow `prefers-color-scheme` while the tokens follow `.dark`, and the two disagree.

### A component, the way the whole stack wants it

Plain function, `ref` as a regular prop (no `forwardRef`), native element props via `React.ComponentProps`, variants via CVA, `data-slot` for styling hooks, and no manual memoization - the compiler handles it.

```tsx
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium transition-colors disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        outline: "border border-input bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
      },
      size: { default: "h-9 px-4 py-2", sm: "h-8 px-3", lg: "h-10 px-8" },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)

function Button({
  className,
  variant,
  size,
  ref,
  ...props
}: React.ComponentProps<"button"> & VariantProps<typeof buttonVariants>) {
  return (
    <button
      ref={ref}
      data-slot="button"
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  )
}
```

Note the `cn()` order: defaults first, consumer `className` last, so tailwind-merge's last-wins resolution lets callers override.

## Best practices

1. **Let the compiler optimize.** Write plain components and computations; reserve `useMemo`/`useCallback` for the rare case where you need a value to be a stable effect dependency.
2. **Model state as discriminated unions, not loose booleans** (`{ status: "loading" } | { status: "error"; error }`) so impossible states are unrepresentable.
3. **Extend native props with `React.ComponentProps<"el">`** instead of re-declaring HTML attributes by hand.
4. **Use `use()` over `useContext()`** - it works after early returns and inside conditionals.
5. **Semantic color tokens only**, and always pair `bg-*` with the matching `text-*-foreground`.
6. **`biome check --write`** is your one local command; `biome ci` in pipelines.
7. **Rolldown is the default bundler in Vite 8** - no opt-in needed; split stable vendor code with Rolldown's `codeSplitting` (see [vite.md](references/vite.md)).
8. **Pin exact versions for tooling that rewrites code** (`babel-plugin-react-compiler`, `@biomejs/biome`) to avoid surprise diffs between releases.
9. **Keep secrets off the client** - only `VITE_`-prefixed env vars reach browser code via `import.meta.env`.
10. **Test through `vite.config.ts`** - Vitest reuses your build config, so tests see the same aliases and transforms; `vitest run` in CI, `jsdom` for component tests.
11. **Bump one dependency at a time with pnpm.** `pnpm add <pkg>@~x.y.z` (or `^`) instead of a broad `pnpm update`, which drags in unrelated transitive bumps; check that the lockfile diff touches only that package and `pnpm why <pkg>` shows one copy. Pin pnpm itself with `packageManager` in `package.json` so shell, corepack, Docker, and CI agree. Under a `minimumReleaseAge` policy in `pnpm-workspace.yaml` a just-published `@latest` is refused - take the newest version past the cutoff instead of bypassing the gate - and dependency build scripts run only for packages approved in `allowBuilds`.

## Resources

- Vite: https://vite.dev/guide/ - Vite 8 blog: https://vite.dev/blog/announcing-vite8
- React 19.3: https://react.dev/blog/2026/09/09/react-19-3 - Compiler: https://react.dev/learn/react-compiler
- TypeScript 7.0: https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/
- Vitest 5: https://vitest.dev/blog/vitest-5 - Hono: https://hono.dev/docs/ - Hono v5 migration: https://hono.dev/docs/guides/migrating-to-v5
- Tailwind CSS: https://tailwindcss.com/docs - shadcn/ui: https://ui.shadcn.com/docs
- Biome: https://biomejs.dev/
