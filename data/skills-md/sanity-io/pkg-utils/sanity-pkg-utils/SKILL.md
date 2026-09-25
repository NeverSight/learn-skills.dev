---
name: sanity-pkg-utils
description: Build, watch, and validate Sanity npm libraries with the pkg CLI and @sanity/pkg-utils. Use when a package has Sanity-style package.json exports, package.config.ts, pkg build, pkg watch, or pkg check, and when deciding whether to stay with pkg-utils or use @sanity/tsdown-config directly.
license: MIT
metadata:
  author: sanity-io
  version: '13'
---

# `@sanity/pkg-utils`

Use `pkg` for conventional Sanity library packages whose authored `package.json#exports` describe
what to build. `@sanity/pkg-utils` composes tsdown with `@sanity/tsdown-config`, adds
browserslist-derived targets and Sanity package conventions, and reconciles generated exports.

For direct `tsdown.config.ts` builds, install and use the `sanity-tsdown-config` skill instead.
Use the separate `tsdown` skill for generic tsdown options.

## Install and run

`@sanity/pkg-utils` 13.x requires Node.js `^22.18.0 || ^24.11.0 || >=26.0.0`.

```sh
pnpm add -D @sanity/pkg-utils
```

Prefer the short `pkg` binary in scripts; `pkg-utils` is an alias:

```json
{
  "scripts": {
    "build": "pkg build --strict --check",
    "watch": "pkg watch"
  }
}
```

Useful commands:

```sh
pkg build                 # build once
pkg build --strict        # enable configured strict checks
pkg build --check         # build, then run pkg check
pkg build --no-clean      # preserve dist for this run
pkg build --quiet         # show only errors, warnings, and checks
pkg watch                 # rebuild on source/config changes
pkg check                 # validate the package without building
```

`pkg init` is an interactive raw-TTY command. Do not automate it through piped input; edit or
scaffold package files directly in non-interactive agent environments.

## Treat exports as the build manifest

Unlike a bare tsdown project, pkg-utils derives entries, formats, and runtime-specific builds from
the hand-written `exports` map:

```json
{
  "type": "module",
  "exports": {
    ".": {
      "source": "./src/index.ts",
      "default": "./dist/index.js"
    },
    "./package.json": "./package.json"
  }
}
```

`pkg build` keeps local `exports` source-aware for development and writes publishable,
source-free targets to `publishConfig.exports`. It does this in CI too. For `browser` or `node`
conditions it creates the additional platform builds required by the map.

After changing entries, conditions, formats, `type`, `main`, or `module`, run a full `pkg build`
and review both export maps. Preserve condition order deliberately: earlier matching conditions
win.

## Configure with `package.config.ts`

`pkg build` never loads `tsdown.config.*`. Its only config file is `package.config.ts` (also
`.mts`, `.js`, or `.mjs`):

```ts
import {defineConfig} from '@sanity/pkg-utils'

export default defineConfig({
  tsconfig: 'tsconfig.dist.json',
})
```

Most packages need little configuration because package metadata supplies the entries. Common
options include:

- `tsconfig` (`'tsconfig.json'` by default)
- `dist` to override the output directory inferred from authored export targets (commonly `dist`)
- `clean` (`true`), `sourcemap` (`true`), and `minify` (`false` for full minification)
- `runtime` (`'*'`), `deps`, `dts`, `define`, and extra Rolldown `plugins`
- `reactCompiler`, `styledComponents`, `vanillaExtract`, `css`, and `bundleAnalyzer`
- `tsdoc` (`true`)
- `bundles` for entry points such as workers or CLIs that are built but not exported

Public entries come from `package.json#exports`, not a `src` config option. `process.env.PKG_VERSION`
is always replaced with the package version, or with the
`PKG_VERSION` environment override. Values in `define` are serialized before forwarding.

## Understand the composed defaults

pkg-utils starts from `@sanity/tsdown-config`, so it inherits source maps, compress-only
minification with preserved names, dependency-subpath resolution, and runtime
circular-dependency warnings. The default `'*'` build uses the wrapper's neutral platform;
`browser` and `node` export conditions create matching platform builds instead. pkg-utils then
owns these differences:

- The authored exports map decides entries, formats, and browser/node build variants.
- JS targets are derived from the package browserslist (Sanity's browserslist config by default),
  split for browser and Node builds and combined for the `'*'` build.
- `tsdoc` defaults to `true` for builds and checks, but is skipped in watch mode.
- `publint` runs through `pkg check`, not tsdown's build hook.
- Per-file tsdown reports are disabled in favor of pkg-utils output.
- `reactCompiler: true` defaults to the Babel implementation for compatibility. Install
  `babel-plugin-react-compiler`. Set `{transform: 'oxc'}` and install `oxc-transform-react` to opt
  into Oxc.
- Full minification happens only with `minify: true`; the default still performs compression and
  dead-code elimination while preserving names.
- Watch mode does not rewrite `package.json` exports, avoiding a watcher loop. Run a full build
  after changing package metadata.

Do not create both `package.config.ts` and `tsdown.config.ts` expecting them to merge. The latter
is ignored by `pkg`.

## Dependencies and declarations

Use tsdown's dependency controls:

```ts
export default defineConfig({
  deps: {
    neverBundle: [/^react(\/|$)/],
    alwaysBundle: ['small-runtime-helper'],
  },
})
```

Strings match exactly or as globs; use a regular expression to include package subpaths. Type
inlining follows bundling decisions. Declaration generation is enabled for TypeScript entries
unless `dts: false`; a package with `@typescript/native-preview` in `devDependencies` defaults to
the `tsgo` generator.

Keep a distribution tsconfig focused on publishable source. Declaration generation does not
replace a separate type-check command.

## React and CSS

- `reactCompiler` and `styledComponents` are opt-in.
- pkg-utils does not support `reactCompiler.reactServer`. Use tsdown with
  `@sanity/tsdown-config` directly for that dual build.
- `vanillaExtract: true` emits and conditionally exports `bundle.css`.
- `css: {...}` uses the optional `@tsdown/css` peer for plain CSS, CSS modules, preprocessors, or
  PostCSS and conditionally exports `style.css`.
- A `.css` export subpath with a `source` automatically enables the CSS pipeline.
- Add emitted CSS to `sideEffects` so consumer tree-shaking does not remove it.

Example standalone stylesheet export:

```json
{
  "sideEffects": ["*.css"],
  "exports": {
    "./ui/styles.css": {"source": "./src/ui/styles.css"}
  }
}
```

## Common pitfalls

- Do not hand-author source entries only in `package.config.ts`; pkg-utils discovers public entries
  from `package.json#exports`. Use `bundles` only for non-exported artifacts.
- Do not run `pkg watch` as the final package validation. Run `pkg build --strict --check` so
  exports are reconciled and TSDoc/publint checks execute.
- Do not use `--no-clean` by default. It can leave stale outputs that make package validation
  misleading.
- Do not fully minify libraries by default. The inherited compression already removes dead code,
  and preserved names aid debugging.
- Do not publish bundle-analyzer output. Exclude `dist/analyze-data.md` from `package.json#files`.
- Do not forget `sideEffects` for emitted CSS.
- Do not assume declaration bundling type-checks source. Run the repository's type-check command.
- Do not use removed pre-v12 options such as `babel`, `extract`, `rollup`,
  `reactCompilerOptions`, or `jsxImportSource`; use the current top-level options.
- `external` is deprecated but still supported with a warning. Migrate it to `deps.neverBundle`
  or `deps.alwaysBundle`.

## When to use direct `@sanity/tsdown-config`

Stay with `pkg` when package exports are the desired source of truth and its option surface covers
the build. Switch to tsdown plus `@sanity/tsdown-config` when you need:

- arbitrary stock tsdown options through `mergeConfig`
- multiple tsdown configs or programmatic build control
- `reactCompiler.reactServer`
- a build whose entries or outputs do not fit pkg-utils' exports-driven model

Do not bypass pkg-utils merely to gain Sanity's shared defaults; it already composes the wrapper.
