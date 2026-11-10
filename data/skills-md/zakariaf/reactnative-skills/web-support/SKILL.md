---
name: web-support
description: "Ships the web build of an Expo app: platform files, APIs missing in react-native-web, expo-sqlite headers. Use when adding web, a .web.tsx file or expo export --platform web. Not for responsive layout (adaptive-layout)."
---

# Web support

Makes an Expo app's web build a deliberate, working target: the web is declared or left out on
purpose, platform files resolve the way Metro and TypeScript expect, nothing in the web bundle
imports a module or calls a React Native API that fails in a browser, expo-sqlite gets its wasm,
isolation headers, warm-up and single-tab lock, and the exported site is opened in a real browser
before it ships. Two zero-dependency checkers prove it; every fact below was measured in headless
Chrome against an export of a canonical Tasks app (Expo SDK 57, react-native-web 0.21.3, 2026-10-14).

## Rules that must hold

1. **The web is a target on purpose, with an explicit output.** Expo adds web whenever `react-dom` is
   installed; either set `platforms: ['ios', 'android']` (or remove `react-dom`, `react-native-web`
   and the `web` script), or keep `react-native-web`, set `web.output` in `app.config.ts`, and record
   it with the host in `contracts/web.json`. Default: `static` on EAS Hosting. Why: an untested web
   target ships a crash, and the output decides what runs in Node and which headers reach the host.
   (`web-target`, `web-contract`)
2. **Platform files come in matching pairs.** Every `x.web.ts`, `x.native.ts`, `x.ios.ts` or
   `x.android.ts` has a base `x.ts` with the **same extension**; a platform route has its base route.
   Why: Metro tries every platform for `.ts` before `.tsx`, so `x.ts` shadows `x.web.tsx`; without a
   base TypeScript resolves nothing and the web cannot resolve a lone `.native` file.
   (`web-platform-pair`)
3. **A web file is held to its base.** It exports exactly the base's value names and types them with
   `import type * as Native from './x'` (`typeof Native.name`). Why: every importer is type-checked
   against the base only; a web file that drifts compiles and throws in the browser.
   (`web-variant-exports`, `web-variant-typed`)
4. **No package that fails in a browser reaches the web bundle.** `react-native-google-mobile-ads`,
   `expo-tracking-transparency`, `expo-iap`, `expo-secure-store`, `expo-file-system`,
   `expo-notifications`, `react-native/Libraries/*` and the contract's `nativeOnlyPackages` are imported
   only by files the web replaces with a `.web` adapter that tells the truth (unsupported, unavailable).
   Why: they break the bundle, throw at import, or throw on the first call, and a green export proves
   none of it. (`web-module-support`)
5. **No React Native API react-native-web lacks, ignores or answers wrongly.** No use of a missing
   export (`ToastAndroid`, `PlatformColor`, `Settings`, ...), missing member
   (`AccessibilityInfo.isBoldTextEnabled`, `Appearance.setColorScheme`, `Linking.openSettings`,
   `Alert.prompt`, ...), silent member (`Alert.alert`, `announceForAccessibility`) or wrong member
   (`AccessibilityInfo.isScreenReaderEnabled` always `true`, `I18nManager.isRTL`) in the web bundle,
   unless a guard keeps it off the web: a `Platform.OS` check for web, `ios` or `android`, a function
   value under a `Platform.select` key the web never picks, or a `typeof` test (every plain value of a
   `Platform.select` object runs on the web). Why: a missing member throws `TypeError`
   (seen in the canonical app), a silent one makes a confirmation vanish, a wrong one takes the wrong
   branch for every visitor. (`web-rn-api`)
6. **Browser globals live only in `.web` files.** `window`, `document`, `navigator`, `localStorage`,
   `sessionStorage`, `indexedDB`, `matchMedia` never appear in a file iOS and Android load. Why: the
   tsconfig `DOM` lib types them everywhere, so tsc accepts code that crashes on a phone.
   (`web-browser-global`)
7. **With static or server output, nothing reads the browser at import.** A `.web` file reads a browser
   global inside a function, or behind `typeof window === 'undefined'` on the same line. Why: Expo
   evaluates every module of the web bundle in Node at export time. (`web-ssr-scope`)
8. **No secret in browser storage.** The web sibling of an expo-secure-store adapter keeps the session in
   memory or a server-set httpOnly cookie, never `localStorage`, `sessionStorage`, IndexedDB or
   `document.cookie`. Why: any script on the page reads them. (`web-token-storage`)
9. **expo-sqlite on the web has its wasm and its isolation headers, in development and deployed.**
   `module.exports = withWebSqlite(config)` in `metro.config.js`; the host sends
   `Cross-Origin-Embedder-Policy: require-corp` and `Cross-Origin-Opener-Policy: same-origin` (the
   expo-router plugin's `headers` on EAS Hosting, which needs `static` or `server` output; the host's
   headers file elsewhere). Never `credentialless`, which Expo's expo-sqlite page shows: Safari and every
   iOS browser ignore it. Why: without wasm the export fails; without isolation there is no
   `SharedArrayBuffer` and no storage. (`web-sqlite-setup`)
10. **Storage waits for the warm-up, and one tab owns it.** With expo-sqlite in the web bundle, the
    root layout returns `<WebStorageGate>` as its outermost element, `DirectionGate` directly inside it
    (one web step outside app-startup-and-bootstrap's startup order; list the gate in
    `contracts/rtl.json` `gateWrappers`): `warmUp` from `useState(openDeviceWebStorage)`, `onError`, and
    a `WebStorageNotice` for each of `inUseElsewhere` and `unsupported`. An adapter the layout reads
    itself before the gate (the saved language) gets a `localStorage` `.web` sibling. Why: the first
    synchronous call (the direction guard's) times out while the SQLite worker starts, a second tab
    cannot open the database files, a page without isolation would crash instead of saying so, and a
    first render that differs from the static HTML is a hydration error. (`web-sqlite-warm-up`)
11. **The page carries the visitor's direction and language.** `src/i18n/direction.web.ts` keeps the
    layout direction on `<html dir>` (react-native-web's `I18nManager` answers left to right for every
    language), and `syncDocumentLanguage(language)` runs in the language provider's effect. Why:
    otherwise an Arabic visitor's page reloads, gives up and stays left to right, and screen readers
    read it in the source language. (`web-rn-api`, `browser-direction`)
12. **The error net listens to the window on the web.** `app-error-net.web.ts` builds the canonical net
    from `error` and `unhandledrejection` events. Why: there is no `ErrorUtils` or `HermesInternal` in a
    browser, so crashes go unrecorded. (`web-error-net`)
13. **Every dynamic route has a page or a rewrite.** With `static` output on a static host, a `[param]`
    route exports `generateStaticParams` or is listed in `clientRoutes` with the host's rewrite. Why: a
    reload of `/tasks/t-42` is a 404 otherwise. (`web-static-routes`)
14. **The export renders in a real browser before it ships.** `check-web-export.mjs --browser auto`
    serves the export with its headers and opens every smoke route: the testID shows, no console error,
    no uncaught exception, isolated when expo-sqlite is installed, `<html dir lang>` right in a
    right-to-left browser. Why: native modules throw only in a browser; the plain canonical app
    exported cleanly and crashed on load. (`export-*`, `browser-*`)

## Workflow

1. **Decide the target.** Read [references/web-target-and-output.md](references/web-target-and-output.md)
   sections 1-3. No web build: set `platforms: ['ios', 'android']` and stop (both checkers then print
   `NOT APPLICABLE`). A web build: keep `react-native-web`, set `web.output`, copy
   `templates/contracts/web.json` and `web.schema.json` to `contracts/` (output, host, smoke routes with
   the testID each home screen renders).
2. **Run the source checker first** to see the gaps: `node ${CLAUDE_SKILL_DIR}/scripts/check-web-support.mjs .`.
3. **The root.** Copy `templates/src/app/+html.tsx` (static or server output) and its test
   `templates/test/web/root-html.test.tsx`. Copy `templates/src/services/error-net/app-error-net.web.ts`
   and `window-error-hooks.ts` with their tests (error-handling-typed-results owns the net). Copy
   `templates/src/i18n/direction.web.ts` and `document-language{,.web}.ts` with their tests, and call
   `syncDocumentLanguage(language)` in the `I18nProvider` effect
   ([references/web-target-and-output.md](references/web-target-and-output.md) section 4).
4. **expo-sqlite.** Read [references/sqlite-on-web.md](references/sqlite-on-web.md). Copy
   `templates/scripts/metro/web-sqlite-metro.ts` and wrap the config in `metro.config.js`; copy
   `templates/src/data/expo-sqlite-warm-up-adapter{,.web}.ts`, `open-device-web-storage.ts`,
   `expo-file-system-database-files-adapter.web.ts` (persistence-and-migrations' snapshot pruning finds no files on the web) and
   `templates/src/features/root-navigator/web-storage-gate.tsx` and `web-storage-notice.tsx` with their
   tests; return the gate outermost in the root layout, around `DirectionGate`, with `inUseElsewhere`
   and `unsupported` notices, and add it to `contracts/rtl.json` `gateWrappers` (section 4 of the
   reference has the layout and the hand-offs; add the four catalog keys).
   Add the `require-corp` isolation headers for the host:
   [references/hosting-and-headers.md](references/hosting-and-headers.md).
5. **Modules.** For each `web-module-support` line, read [references/module-support.md](references/module-support.md)
   and give the adapter a `.web.ts` sibling in the shape of
   [references/platform-files.md](references/platform-files.md) section 5 and
   [examples/share-task-web-adapter.md](examples/share-task-web-adapter.md). A native-only package the
   table does not know goes into `nativeOnlyPackages`.
6. **React Native APIs.** For each `web-rn-api` line, read [references/rn-api-gaps.md](references/rn-api-gaps.md):
   a guard in one of the shapes of its section 6 for a one-line difference, a platform file for more.
7. **Layout and input.** Read [references/layout-and-input.md](references/layout-and-input.md); imitate
   [examples/task-row-web.tsx](examples/task-row-web.tsx) for hover, focus and keyboard.
8. **Tests.** Follow [references/testing-web.md](references/testing-web.md) section 2: web files are
   tested in the unit project by explicit `.web` imports; logic stays in plain functions.
9. **Check the source.** `npm run typecheck`, `npx eslint <changed paths> --max-warnings 0`, the Jest
   tests, then `node ${CLAUDE_SKILL_DIR}/scripts/check-web-support.mjs .` until `RESULT: PASS`
   (`--app-dir apps/mobile` inside a monorepo).
10. **Export and smoke.** `APP_VARIANT=production EXPO_PUBLIC_APP_VARIANT=production npx expo export --platform web`,
    then `node ${CLAUDE_SKILL_DIR}/scripts/check-web-export.mjs . --browser auto` until `RESULT: PASS`.
    Read the first `browser-console` line first; export with `--dev` for readable React errors.
11. **By hand, before a web release:** testing-web.md section 5 (resize, keyboard only, a second tab,
    deep URL reload, a screen reader, Safari and Firefox, then Safari on a named iOS simulator and
    Chrome on a named Android emulator: isolated, no storage notice). **Deploying publishes the site:
    stop and ask the developer before `eas deploy` or any host upload** (Expo's `eas-hosting` skill
    has the commands).

## Definition of done

- [ ] The app config either leaves web out of `platforms`, or sets `web.output`, and
      `contracts/web.json` records the same output, the host and the smoke routes.
- [ ] Every platform file has a base of the same extension; every `.web` file exports the base's names
      and types them with `import type * as Native from './<base>'`.
- [ ] No web-bundled import of a failing package; each such adapter has a truthful `.web.ts` sibling.
- [ ] No unguarded missing or silent React Native API in the web bundle; no browser global outside
      `.web` files; none at module scope with static output.
- [ ] With expo-sqlite: `withWebSqlite` in `metro.config.js`, `require-corp` isolation headers from the
      host, `WebStorageGate` outermost in the root layout (both notices, `DirectionGate` inside it), and
      a second tab shows the other-tab notice.
- [ ] `direction.web.ts` and `document-language{,.web}.ts` are in place with their tests, and the
      language provider calls `syncDocumentLanguage(language)`.
- [ ] `app-error-net.web.ts` and `window-error-hooks.ts` are in place with their tests.
- [ ] `npm run typecheck`, ESLint `--max-warnings 0` and Jest pass.
- [ ] The production web export exists:
      `APP_VARIANT=production EXPO_PUBLIC_APP_VARIANT=production npx expo export --platform web`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-web-support.mjs .` prints `RESULT: PASS`. The only SKIP line
      it may print: `SKIP app.config.ts [web-target] not yet created (expo-project-bootstrap creates it)`.
      Without a web target it prints `NOT APPLICABLE: the app config platforms (ios, android) leave out web`
      (or that react-dom is not installed), and so does the export check.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-web-export.mjs . --browser auto` prints `RESULT: PASS`.

## Anti-patterns

- **"The export succeeded, so the web works."** Native modules return `{}` during static rendering and
  throw only in a browser; run the browser smoke.
- **`x.ts` with `x.web.tsx`.** Metro loads `x.ts` on the web and the variant never runs; same extension.
- **A `Platform.OS === 'web'` branch around a native-only import.** The import still runs; move it into
  a platform file.
- **`if (typeof window !== 'undefined')` in shared code.** React Native defines `window` too; browser
  code goes in a `.web` file.
- **Falling back to `localStorage` for a token on the web.** Any script reads it; memory or an httpOnly
  cookie.
- **`web.output: 'single'` on EAS Hosting with expo-sqlite.** No routes manifest, no isolation headers,
  a crash on load.
- **Calling `openDatabaseSync` on the first render in the web build without the gate.** It times out
  while the worker starts.
- **Trusting `AccessibilityInfo.isScreenReaderEnabled()` on the web.** It always answers `true`; read
  it only off the web, and design for screen readers there always.
- **Copying `Cross-Origin-Embedder-Policy: credentialless` from Expo's expo-sqlite page.** Every iPhone
  visitor gets no isolation and no storage; send `require-corp` and give cross-origin resources a
  `Cross-Origin-Resource-Policy` header.
- **`Alert.alert('Delete task?', ...)` for a confirmation.** Nothing appears on the web, so nothing is
  ever confirmed; use the app's dialog.
- **Publishing source maps with the site, or deploying without asking.** Maps go to the crash reporter;
  a deploy is the developer's call.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/web-target-and-output.md](references/web-target-and-output.md) | Web as a target, the three outputs (what each export writes, measured), the default, `+html.tsx` on SDK 57, static rendering in Node, dynamic routes, commands, decisions | Workflow steps 1 and 3 |
| [references/platform-files.md](references/platform-files.md) | Metro's and TypeScript's resolution, platform routes, the one shape, the typed variant, `Platform.OS` branches, where variants live, pitfalls | Workflow steps 2 and 5 |
| [references/module-support.md](references/module-support.md) | How each stack package behaves in a browser (measured), the three failure kinds, web adapters, re-verify method | Workflow step 5 |
| [references/rn-api-gaps.md](references/rn-api-gaps.md) | React Native exports and members react-native-web lacks, ignores or answers differently, and what to use instead | Workflow step 6 |
| [references/sqlite-on-web.md](references/sqlite-on-web.md) | expo-sqlite in a browser: wasm, isolation, the warm-up gate, one tab, persistence, the failure ladder | Workflow step 4 |
| [references/hosting-and-headers.md](references/hosting-and-headers.md) | Headers and rewrites per host (EAS Hosting, Netlify, Cloudflare Pages, Vercel, own server), caching, what never ships | Workflow steps 4 and 11 |
| [references/layout-and-input.md](references/layout-and-input.md) | Window, styles, hover, keyboard and focus, text, scrolling, links and back, assets, missing feedback | Workflow step 7 |
| [references/testing-web.md](references/testing-web.md) | Jest recipes for web files, both checkers' rules and options, the browser smoke, checks by hand, the realistic run, limits, debugging | Workflow steps 8-11 |
| [examples/share-task-web-adapter.md](examples/share-task-web-adapter.md) | Example (shape only): port, native adapter, typed web adapter, fake, test | Workflow step 5 |
| [examples/task-row-web.tsx](examples/task-row-web.tsx) | Example (shape only): a row with hover, focus ring and keyboard behaviour | Workflow step 7 |
| `templates/src/app/+html.tsx` | The root HTML: language, direction, `viewport-fit=cover`, scroll reset, ground colour of both schemes | Workflow step 3 |
| `templates/test/web/root-html.test.tsx` | The root HTML's test (route folders hold routes only) | Workflow step 3 |
| `templates/src/services/error-net/` | `app-error-net.web.ts` (the net from window events) and `window-error-hooks.ts`, each with its test | Workflow step 3 |
| `templates/src/i18n/` | `direction.web.ts` (the layout direction on `<html dir>`, saved across the direction restart) and `direction-web.test.ts`; `document-language.ts` (nothing on devices) and `.web.ts` (`syncDocumentLanguage` sets `<html lang>`) with `document-language-web.test.ts` | Workflow step 3 |
| `templates/src/data/` | `expo-sqlite-warm-up-adapter.ts` (no warm-up on devices) and `.web.ts` (tab lock, async warm-up), each with its test (`-web.test.ts` for the web file), `open-device-web-storage.ts` (the seam the root layout calls) with its test; `expo-file-system-database-files-adapter.web.ts` (lists and removes nothing) with `-web.test.ts` | Workflow step 4 |
| `templates/src/features/root-navigator/` | `web-storage-gate.tsx` (holds the root until storage answers, or shows `inUseElsewhere` / `unsupported`) and `web-storage-notice.tsx` (the notice for either reason, outside every provider), each with its test | Workflow step 4 |
| `templates/scripts/metro/` | `web-sqlite-metro.ts` (`withWebSqlite`: wasm asset, dev isolation headers) and its test | Workflow step 4 |
| `templates/contracts/` | `web.json` (output, host, smoke routes, client routes, source maps, native-only packages) and `web.schema.json` | Workflow step 1 |
| `scripts/check-web-support.mjs` | The source checker for rules 1-13 (`--help` lists the rule ids) | Workflow steps 2 and 9 |
| `scripts/check-web-export.mjs` | The export check and, with `--browser`, the headless Chrome smoke (rules 11 and 14) | Workflow step 10 |
| `scripts/selftest.mjs` | Proves both checkers on the fixtures | After changing a checker |
| `scripts/lib/web-target.mjs` | This skill's helpers both checkers share: app config, web target fact, contract | When changing a checker |
| `scripts/check-lib.mjs` | Shared script library (CLI, reporting, layout, repo walk, self-test), synced (do not edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Shared source lexer and import helpers, synced (do not edit here) | Never by hand |
| `assets/web-support-table.json` | The measured package and React Native API table the checker reads | Workflow steps 5-6; re-verify after an upgrade |
| `assets/shared.json` | Declares the synced files | When adding a shared file |
| `tests/bases/` | The small Tasks web app (`app/`) and export (`export/`) the fixtures start from | When adding a rule |
| `tests/fixtures/` | Overlay cases: good, one planted bug per rule, passing profiles, bad input | When adding a rule |

## Related skills

- `adaptive-layout` - window classes and panes; the browser window resizes freely.
- `architecture-and-boundaries` - ports, adapters, the composition root, API routes and server files.
- `persistence-and-migrations` - the SqlDriver and data layer the warm-up protects.
- `auth-and-secure-storage` - sessions and tokens; the web keeps none in browser storage.
- `error-handling-typed-results` - the canonical error net the web variant feeds.
- `app-startup-and-bootstrap` - owns the root layout and startup order; the web adds the storage gate outside DirectionGate.
- `accessibility-as-code` - the system accessibility store, `aria-modal`, live regions.
- `rtl-and-direction` - owns `direction.ts`, the guard and DirectionGate; `direction.web.ts` keeps their contract.
- `i18n-strings-and-catalogs` - `I18nProvider` (where `syncDocumentLanguage` runs) and the notice copy.
- `app-variants-and-environment` - `metro.config.js`, `EXPO_PUBLIC_*` values (public in a web bundle).
- `dependency-management` - adding or removing `react-dom` and `react-native-web`.
- `navigation-and-routing`, `deep-links-and-universal-links` - URLs, links and `.well-known` files.
- `forms-and-input`, `ui-states-and-feedback` - fields, dialogs and toasts that replace native ones.
- `unit-and-component-tests` - Jest projects and helpers.
- `crash-reporting-and-observability` - source maps and crash reports from the web.
- `skia-canvas-rendering` - loading CanvasKit before a canvas renders on the web.
- Expo's official `eas-hosting` and `expo-dom` skills - deploy commands; DOM components inside a native
  app (both in the expo/skills repository, verified 2026-10-16).
