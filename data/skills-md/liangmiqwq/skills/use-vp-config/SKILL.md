---
name: use-vp-config
description: Configure JavaScript and TypeScript projects with Liangmi's @liangmi/vp-config presets for Vite+. Use when you are requested to migrate to `@liangmi/vp-config` or create a project with `@liangmi/vp-config`
---

# Use @liangmi/vp-config

`@liangmi/vp-config` exports one function, `liangmi()`, used in `vite.config.ts`. It reads committed files (`package.json`, `tsconfig.json`, `index.html`, workspace manifests), works out what kind of project each package is, and emits Vite+ config for `lint`, `fmt`, `pack`, `test`, `run` and `staged`. The user config is merged on top.

So most of the job is not writing config. It is making the committed files describe the project correctly, then writing only the config that differs from the preset.

Requires `vite-plus@1.0.0` or later. Vite+ docs: `node_modules/vite-plus/docs` or https://viteplus.dev/guide/.

## How projects are detected

Each project gets traits. Every trait comes from a committed file:

| Trait                         | Comes from                                                      | Changes                                                         |
| ----------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| `lib`                         | `exports` in `package.json`                                     | pack: `.d.ts` via tsgo, fixed extensions, refined `exports`     |
| `cli`                         | `bin` in `package.json`                                         | pack: Node target, minified. lint: `console`, `process.exit` ok |
| `node`                        | `bin` in `package.json`, or `"node"` in tsconfig `types`        | lint: Node globals and rules. test: `node` environment          |
| `browser`                     | `index.html` next to `package.json`, or `DOM` in tsconfig `lib` | lint: browser rules. test: `happy-dom` / `jsdom` if installed   |
| `react`, `vue`, `tailwindcss` | Any dependency field in `package.json`                          | lint: component rules. fmt: JSX quotes, class sorting           |

`node` and `browser` are independent. A project can have both, or neither (then it gets no `test` environment and no runtime rules).

When a trait is wrong, fix the source file first: add `"types": ["node"]` to `tsconfig.json`, add `exports` or `bin` to `package.json`, and so on. `vp pack` never creates `exports` or `bin`, so they must be committed anyway. Use `.option()` only when fixing the file is not reasonable (see [API](#api)).

Only `tsconfig.json` in the project directory is read (with its `extends` chain). Settings only in `tsconfig.app.json` or similar are not seen.

## Where config goes

Vite+ only reads `lint` and `fmt` from the workspace root. The preset follows this:

| `vite.config.ts` location | Emits                                                                       |
| ------------------------- | --------------------------------------------------------------------------- |
| Single-package repo       | Everything                                                                  |
| Workspace root            | `lint`, `fmt`, `staged`, `run`, with per-project overrides for every member |
| Workspace member          | `pack`, `test`, `run` for that member                                       |

A workspace root is a directory with `pnpm-workspace.yaml` or `workspaces` in `package.json`. Use `liangmi()` in the root config and in every member config.

Passing `lint` or `fmt` in a member config, or chaining lint methods there, throws an error. Put member-specific lint and fmt changes in the root config, with `files` globs relative to the workspace root (for example `packages/cli/**`).

## Migrate an existing project

1. **Get onto Vite+ first.** If the project does not use Vite+ yet, run `vp migrate` at the workspace root and follow `node_modules/vite-plus/docs/guide/migrate.md`. Don't hand-port ESLint, Prettier, tsup or Vitest setups. Vite+ handles that.
2. **Install** at the workspace root: `vp add -D @liangmi/vp-config`. Members resolve it from the root. If the workspace uses a pnpm catalog, add it there to match.
3. **Check the facts** for every project against the table above. Fix `package.json` and `tsconfig.json` where they are wrong or missing. Ask the user when the intent is unclear, such as whether a package is published as a library.
4. **Rewrite each `vite.config.ts`** to use `liangmi()`. Write only what the preset does not already cover:
   - `pack.entry` is never derived. Set it for every `lib` or `cli` project.
   - Drop `fmt` options, lint rules, `test.environment`, and `pack` defaults that the preset already sets. Keep options that really differ, and tell the user which ones you kept.
   - Convert an existing `lint` object to flat config entries (see [Lint](#lint)), not a top-level object.
   - Keep `vite`, `server`, `plugins` and other app config unchanged. `liangmi()` passes them through.
5. **Update scripts** to the cached tasks, for example `"build": "vp run cpack"`, `"test": "vp run ctest"`, `"check": "vp run ccheck"`. Add `"prepare": "vp config"` so the commit hook is installed. Remove separate `tsc --noEmit` steps, because lint type checking already covers them.
6. **Run `vp check`** and fix what it reports. See [Fixing lint errors](#fixing-lint-errors).
7. **Run `vp test`** and `vp pack` / `vp build` for projects that have them.

## Create a new project

1. Scaffold with `vp create` (`vite:library`, `vite:application`, `vite:monorepo`, or a framework template). Read `node_modules/vite-plus/docs/guide/create.md` if unsure.
2. Follow steps 2 to 7 of the migration. In a new project, set the facts while scaffolding: `exports` for libraries, `bin` for CLIs, `types: ["node"]` for Node code, `lib: ["DOM", ...]` for browser code.

## API

```ts
import { liangmi } from '@liangmi/vp-config'

export default liangmi({
  pack: { entry: ['./src/index.ts'] }
})
```

- `liangmi(config)` takes the same input as Vite+'s `defineConfig`: an object, a promise, or a function of `ConfigEnv`. It already calls `defineConfig`, so don't wrap it again.
- Export the chainable builder directly. Vite+ resolves it when loading the config.
- `fmt`, `pack`, `run`, `staged` and `test` are deeply merged over the preset. `lint` is a flat config array, appended after the preset.
- `.only([...parts])` keeps only those preset parts. `.exclude([...parts])` drops them. Parts: `fmt`, `lint`, `pack`, `run`, `staged`, `test`. User config for a dropped part still applies, just without the preset under it.
- `.option([{ path, ...traits }])` declares traits in the **root** config. `path` is relative to the workspace root (`'.'` for the root). Declared traits override detected ones, and undeclared ones are still detected. A path that is not a workspace member is added as an extra project. Calling `.option()` in a member throws. Members load the root config module to read its declarations before deriving their presets.

```ts
export default liangmi().option([
  { path: 'apps/api', node: true },
  { path: 'packages/ui', browser: true, vue: true }
])
```

The exported types are `LiangmiConfig`, `UserConfigFunction`, `ConfigPart`, `DeclaredProject`, `ProjectFacts` and `ProjectTraits`.

## Lint

`lint` is an ESLint-style flat config array from [`oxlint-flat-config`](https://github.com/liangmiQwQ/oxlint-flat-config). Later entries override earlier ones, and nothing is deeply merged.

```ts
export default liangmi({
  lint: [
    { rules: { 'no-console': 'warn' } },
    { files: ['packages/cli/**'], rules: { 'no-console': 'off' } }
  ]
})
```

To change preset entries instead of adding new ones, chain composer methods on `liangmi()`: `override`, `replace`, `remove`, `insertBefore`, `insertAfter`, `append`, `prepend`, `overrideRules` and `removeRules`. They run after the user entries are appended.

```ts
export default liangmi()
  .override('liangmi/options', { options: { typeCheck: false } })
  .remove('liangmi/style')
```

Preset entry names:

- `liangmi/ignores`, `liangmi/options`
- `liangmi/correctness`, `liangmi/perf`, `liangmi/suspicious`, `liangmi/nursery`: whole categories, with plugin-prefixed rule names like `eslint/no-shadow`
- `liangmi/restriction`, `liangmi/pedantic`, `liangmi/style`: selected rules, mostly unprefixed like `no-console`
- Per trait: `liangmi/node`, `liangmi/browser`, `liangmi/cli`, `liangmi/react`, `liangmi/vue`
- Per file role: `liangmi/test`, `liangmi/script`, `liangmi/config-file`

In a workspace, member entries include the path, like `liangmi/packages/cli/react`. `overrideRules` and `removeRules` match rule names exactly as written, so use the spelling from the entry that defines the rule. To find it, search `node_modules/@liangmi/vp-config/dist/index.mjs`.

## Fixing lint errors

The preset is strict, and `denyWarnings` is on, so warnings fail too. A migration usually brings a wave of new reports. Fix the code first. Don't turn rules off in bulk without asking the user.

- Many reports are fixable. Run `vp check --fix` first, then fix the rest by hand.
- Relative imports need file extensions (`./util.ts`). TypeScript projects need `allowImportingTsExtensions` (with `noEmit`) or `rewriteRelativeImportExtensions` in `tsconfig.json`.
- Classes are an error (`max-classes-per-file: 0`). Prefer functions and plain objects.
- `console` is an error, except in `cli` projects and script files. `**/*.config.ts` files allow default exports but not `console`.
- Test files must be named `*.test.ts`. `*.spec.ts` files are linted as tests, but reported for their name.
- File roles apply inside each project: `scripts/**`, `script/**` and top-level `*.ts` / `*.js` files are Node scripts.
- `bin/**` is ignored.
- Only `oxlint-disable` comments count. `eslint-disable` comments are ignored, so convert existing ones. Unused disable comments are reported. When a disable is justified, use `// oxlint-disable-next-line <rule> -- <reason>`.
- Type checking runs inside lint. Type errors show up in `vp check`.

## Verify the result

Print the resolved config to confirm the detected traits:

```bash
node -e "const c = (await import('./vite.config.ts')).default; console.log(JSON.stringify(c, null, 2))"
```

Run it in the directory of the config you want to check. Node 22.18+ can import a TypeScript config directly. If the config is a function, use `await c({ command: 'build', mode: 'production' })` instead of `c`. Check that the expected `liangmi/<path>/<trait>` entries appear in `lint.overrides`, that `test.environment` is right, and that `pack` has the `lib` or `cli` defaults.

## Cached tasks

Every config adds these tasks. Run them with `vp run <task>` (or `vpr <task>`):

| Task      | Runs        |
| --------- | ----------- |
| `cbuild`  | `vp build`  |
| `cpack`   | `vp pack`   |
| `clint`   | `vp lint`   |
| `cfmt`    | `vp fmt`    |
| `cformat` | `vp format` |
| `ccheck`  | `vp check`  |
| `ctest`   | `vp test`   |

Use them in `package.json` scripts so the Vite+ task cache applies. Change cache inputs under `run.tasks.<name>.cache`. The root config also sets `staged` to run `vp check --fix` on staged files.
