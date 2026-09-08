---
name: rslib-modern-package
description: Opinionated Rslib recommendations for modern JS/TS npm package design covering pure ESM, strict TypeScript, explicit exports, small stable APIs, pragmatic dependencies, accurate sideEffects, correct declarations, package validation, provenance, README.md, and AGENTS.md. Use when the user wants to make a JS/TS package more modern, check whether the current package setup is healthy, review package.json/exports/types/dependencies/docs/release readiness, or apply a modern library baseline.
---

# Rslib Modern Package

Use this skill when creating a new Rslib library, modernizing an existing JS/TS package, or reviewing a package against an opinionated modern library standard.

This skill is opinionated: it describes a recommended modern package contract and may suggest breaking changes when they make the package simpler, safer, and easier for modern consumers.

## Standard

Default recommendation for new JS/TS libraries:

- ESM-first, preferably pure ESM.
- Strict TypeScript and correct declaration files.
- Explicit public API through `package.json#exports`.
- Small named-export API surface.
- Few runtime dependencies, without treating zero dependencies as a religion.
- Small, tree-shakeable output with accurate `sideEffects`.
- Clear dependency placement: runtime dependencies, peer dependencies, optional dependencies, and dev dependencies are not interchangeable.
- Published package is tested as an artifact, not just as source files.
- Release flow is automated, traceable, and SemVer-aware.
- README.md explains usage for humans; AGENTS.md preserves package invariants for future agents.

## Workflow

1. **Inspect the package contract first**
   - Read `package.json`, lockfile/package manager, `rslib.config.*`, `tsconfig*`, CI/release config, README.md, AGENTS.md, and existing `dist` output.
   - Identify package kind: Node utility, browser library, isomorphic utility, CLI, UI/component library, framework plugin, SDK, or adapter.
   - List supported runtimes, current entry points, deep imports, runtime dependencies, peer dependencies, optional integrations, files with side effects, and published files.
   - Run `npm pack --dry-run` early when changing package shape so the real tarball contents guide the review.

2. **Define target environments explicitly**
   - Do not say "supports modern environments" without defining them.
   - Verify the current Node.js release schedule before choosing `engines`.
   - As of May 9, 2026, Node.js 22 and 24 are LTS, and Node.js 20 is EOL. For new Node-facing packages, recommend `engines.node >=22` unless real consumers need an older runtime.
   - Browser packages should state whether they require native ESM, a bundler, Workers support, SSR compatibility, DOM APIs, CSS processing, or specific browser baselines.
   - Compatibility drops are breaking changes: old Node/browser versions, undocumented deep imports, default/named export shape, bundled vs external dependency behavior, and import side effects.

3. **Prefer pure ESM, but explain compatibility cost**
   - New packages should use `"type": "module"` and ESM source/output.
   - Rslib's default format is ESM; keep that default unless there is a clear reason to add another format.
   - Evaluate compatibility from real consumers and supported runtimes instead of assuming every historical module format is required.
   - Modern Node.js can load synchronous ESM from CommonJS via `require(esm)`; do not assume CJS consumers always require a separate CJS build.
   - If you rely on `require(esm)` compatibility, document and test its constraints: supported Node versions, no top-level `await` in the loaded graph, namespace-object return shape, default export behavior, and CJS/ESM cycle limits.
   - Prefer Node built-in specifiers such as `node:fs/promises`.

4. **Make `exports` the public API**
   - Treat `package.json#exports` as the product contract.
   - Export only paths users are meant to import.
   - Do not allow imports like `pkg/dist/foo.js` by exporting `./dist/*`. That makes the generated output layout part of the public API and turns internal file moves into breaking changes.
   - Instead, expose only intentional public paths such as `pkg` and `pkg/foo.js`, mapped to the actual files in `dist`.
   - Keep subpath style consistent: either all with extensions such as `./foo.js`, or all without extensions. Prefer paths with extensions when browser import maps matter.
   - Keep `"types"` first inside conditional exports.
   - Adding `exports` to an older package can be breaking because undeclared deep imports stop working.
   - Add `./package.json` only when consumers legitimately need package metadata.

5. **Design a small API surface**
   - Prefer named exports for multi-API packages.
   - Avoid default-export objects that gather every function into one object.
   - Public functions should be few, stable, well-named, and semver-maintained.
   - Keep internal types, caches, helper functions, adapter details, and error internals private unless they are part of the contract.
   - Avoid top-level work during import: file scans, network calls, timers, process mutation, global registration, DOM access, prototype mutation, or environment detection with side effects.
   - Async APIs that may be canceled should accept `AbortSignal`.
   - Prefer stable error classes, error codes, or typed error shapes over string matching.

6. **Use Rslib as the implementation path, not the whole standard**
   - For detailed Rslib configuration guidance, use the `rslib-best-practices` skill.
   - In this skill, only check whether Rslib output, declarations, `package.json#exports`, `files`, dependencies, and docs agree with the modern package contract.
   - Keep Rslib configuration small and intentional; avoid adding build complexity that does not improve the package contract.

7. **Keep dependencies small and intentional**
   - Start from platform APIs, not from dependency search.
   - Prefer built-ins when the runtime supports them: `URL`, `URLSearchParams`, `Intl`, `fetch`, `AbortController`, `structuredClone`, `crypto.randomUUID`, Web Streams, `TextEncoder`, `TextDecoder`, `node:fs/promises`, and `node:crypto`.
   - Small runtime dependencies are fine when they reduce maintenance risk or implementation complexity.
   - Avoid large utility packages for one or two helpers.
   - Evaluate dependencies for ESM support, `exports`, types, transitive dependency count, package size, license, maintenance activity, security history, install scripts, side effects, native install fragility, and granular imports.
   - Put required runtime packages in `dependencies`.
   - Put host-owned frameworks and toolchains in `peerDependencies`, such as React, Vue, Svelte, Rspack, Rsbuild, webpack, TypeScript, and framework runtimes.
   - Keep peer ranges reasonably broad; do not pin peers to a patch version unless required.
   - Put build tools, test tools, type tools, docs tools, and Rsbuild/Rspack plugins in `devDependencies`.
   - Use `optionalDependencies` or optional peers via `peerDependenciesMeta` for optional integrations.

8. **Make TypeScript strict and package-oriented**
   - Prefer TypeScript source for TS libraries; otherwise use high-quality JSDoc plus generated declarations.
   - With TypeScript 6 or tsgo-era defaults, strict checking may already be enabled; preserve that default and do not turn it off. For older TypeScript versions or inherited configs, set `strict: true` explicitly.
   - In Rslib projects, consider enabling `lib.dts.tsgo` to speed up declaration generation when the project can use tsgo.
   - Keep `module` and `moduleResolution` aligned with how declarations are emitted and how consumers resolve the package; NodeNext and bundler-style resolution are both valid in the right toolchain.
   - Use `verbatimModuleSyntax` so type-only imports/exports are explicit.
   - Use `isolatedDeclarations` when practical so exported APIs are explicit enough for declaration-oriented tooling.
   - Emit declarations; use declaration maps when editor navigation matters.
   - Use `import type` and `export type` for type-only dependencies.
   - Do not rely on consumers setting `skipLibCheck` to hide broken package types.
   - Test declarations as consumers see them, especially when using subpath exports.

9. **Keep `sideEffects` accurate**
   - Use `sideEffects: false` only when importing package files has no top-level side effects.
   - If CSS, polyfills, registrations, global listeners, prototype changes, or other import-time mutations exist, list the files with side effects instead.
   - Do not set `sideEffects: false` just to improve bundle size; incorrect values can remove required CSS or setup code.
   - Do not change globals just because a file is imported. If setup is required, expose an explicit `setup()` or `install()` function and let users call it themselves.

10. **Make `package.json` authoritative**
    - Required modern shape: `"type": "module"`, explicit `exports`, correct declarations, `files` allowlist, accurate `sideEffects`, sensible `engines`, and release scripts.
    - Include README.md, AGENTS.md, and LICENSE in `files` when they exist.
    - `files` should prevent tests, fixtures, private docs, build caches, local configs, and large generated artifacts from leaking into the tarball.
    - Avoid stale `main`/`module` fields unless compatibility evidence requires them; if kept, they must agree with `exports`.
    - Keep runtime dependency fields accurate. A package that works locally only because a runtime dependency is in `devDependencies` is broken.

11. **Validate the published artifact**
    - Run normal lint, typecheck, tests, and `rslib build`.
    - Smoke test built ESM output.
    - Run type-level tests when the public API is type-heavy.
    - Run `npm pack --dry-run` and inspect included files.
    - In Rslib, prefer `rsbuild-plugin-publint` to run publint after build; use `npx publint` as a CLI fallback.
    - In Rslib, prefer `rsbuild-plugin-arethetypeswrong` to run Are The Types Wrong after build when declarations are shipped; use `npx --yes @arethetypeswrong/cli --pack .` as a CLI fallback.
    - Install the packed tarball into clean consumer fixtures for important packages.
    - Test ESM import, bundler import for browser/component libraries, CLI execution for `bin` packages, and every public subpath export.

12. **Prepare README.md and AGENTS.md before publishing**
    - Always check whether both files exist before publishing or modernizing a package.
    - If either file is missing, recommend adding it; for implementation tasks, create a concise version unless the user asks not to.
    - README.md should include: package name, one-sentence purpose, install/usage, key features or API links, supported environments, docs/related links, changelog or contribution link, and license.
    - AGENTS.md should include: stack, package contract, common commands, source layout, code style, validation commands, and release checklist.
    - Keep both files synchronized with `package.json#exports`, supported runtimes, and actual Rslib output.

13. **Publish with supply-chain hygiene**
    - Follow SemVer and document breaking changes.
    - Maintain a changelog for user-visible changes.
    - Use prerelease versions and dist-tags for beta/next channels.
    - Prefer CI publishing with npm provenance or trusted publishing.
    - Avoid long-lived publish tokens where trusted publishing is available.
    - Remember that a published package name/version pair cannot be reused safely.

## Review Red Flags

- `exports` is missing, points to files not emitted by Rslib, or allows public imports such as `pkg/dist/foo.js`.
- `module`/`main` fields disagree with `exports`.
- Type declarations do not match runtime entry points.
- Runtime dependency is accidentally listed only in `devDependencies`.
- React/Vue/Svelte/Rspack/Rsbuild/webpack/TypeScript is bundled or placed in `dependencies` when it should be a peer.
- `sideEffects: false` is set while importing CSS, polyfills, global registrations, global listeners, or prototype changes.
- Package has install scripts without a strong reason.
- Top-level import reads user files, starts timers, touches the network, mutates globals, or assumes `window`/`process`.
- Published tarball contains private source maps, tests/fixtures that are not useful to consumers, large generated docs, local config secrets, or build caches.

## Checklist

- [ ] Supported environments are explicit.
- [ ] Package is ESM-first, preferably pure ESM.
- [ ] `package.json` has `"type": "module"`.
- [ ] Public entry points are declared in `exports`.
- [ ] No accidental reliance on undeclared deep imports.
- [ ] Rslib output, declarations, `exports`, and `files` agree.
- [ ] TypeScript strict mode is enabled.
- [ ] Declarations are emitted and validated.
- [ ] Runtime dependencies are justified and small.
- [ ] Host frameworks/toolchains are peers.
- [ ] Build/test/type/docs tools are dev dependencies.
- [ ] `sideEffects` is accurate.
- [ ] `npm pack --dry-run` has been inspected.
- [ ] `publint` passes.
- [ ] Are The Types Wrong check passes when declarations are shipped.
- [ ] Built ESM smoke test passes.
- [ ] README.md exists.
- [ ] AGENTS.md exists.
- [ ] Release flow uses SemVer, changelog, and provenance/trusted publishing when available.

## Documentation

- For the latest Rslib docs, read https://rslib.rs/llms.txt
- Shipping ESM for CommonJS consumers: https://nodejs.github.io/package-examples/04-cjs-esm-interop/shipping-esm-for-cjs/
