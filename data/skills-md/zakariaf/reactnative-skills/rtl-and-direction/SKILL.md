---
name: rtl-and-direction
description: Makes Expo apps right-to-left correct - logical styles, guarded direction restart, mirroring, digits, bidi. Use when adding Arabic or Hebrew, a row, icon, number, language switch or RTL test. Not for translation (i18n-strings-and-catalogs).
---

# Right-to-left layout and direction

Makes an Expo app correct in right-to-left languages on iOS and Android: screens mirror by
themselves through logical styles, the layout direction is decided before the app starts and
changes with exactly one guarded restart (never a loop), text reads in its own direction, physical
surfaces and non-directional icons stay put, numbers show the language's digits, and a
zero-dependency checker proves the code keeps it that way.

## Rules that must hold

1. **Style with logical keys and build rows with `flexDirection: 'row'`.** `marginStart/End`,
   `paddingStart/End` or `paddingInline`, `start`/`end`, `border*Start*/*End*` radii and widths;
   never physical left/right keys in a style (Reanimated styles and typed style helpers included),
   never `row-reverse`, never `scaleX: -1` on content. Why: React Native 0.86 does swap physical
   keys to start/end in a right-to-left layout, but only while a global, persisted native
   preference (`swapLeftAndRightInRTL`) is on, which any library can turn off; next to a logical
   key on the same element the swapped key wins in RTL only; react-native-web never swaps. A
   truly physical position (a drag thumb) is `transform: [{ translateX }]`, never `left`.
   (`physical-style-key`, `row-reverse`, `scale-x-flip`)
2. **Render text through `AppText` and align with `align="start" | "end"`.** Only the design
   system's text style hook maps start/end to `textAlign` and sets `writingDirection`; only AppText
   imports `Text`. Why: `textAlign: 'auto'` follows a text's first letter, not the layout, and
   React Native swaps `'left'`/`'right'` in a right-to-left layout, so `'right'` lands on the end
   (left) edge (verified on iOS).
   (`text-align-literal`, `writing-direction`, `text-import`)
3. **Keep one layout-direction source.** Only `src/i18n/direction.ts` touches `I18nManager`; layout
   decisions (icon flips, coordinate maps, navigators) read `useDirection()` or
   `readLayoutDirection()`, never `directionOf(language)`; text takes its language's direction
   through `TextLocaleProvider`. Why: `isRTL` is fixed for the whole JS run, so between a language
   change and the restart the language and the layout differ. (`i18nmanager`, `layout-direction`)
4. **Decide the direction before the app starts.** `DirectionGate` is the root layout's first,
   outermost element (only effect-free wrappers such as `GestureHandlerRootView` around it); the
   startup work with effects (database open, migrations, stores, providers) lives in its child. Why: a restart re-runs every module and startup step, so work done before the
   decision happens twice. (`direction-before-render`)
5. **Change direction only through `restartForDirection()`.** It records the pending direction in
   the guard first, sets `allowRTL` and `forceRTL` together, awaits the optional `beforeReload`
   hook (an app with audio passes `() => services.audio.dispose()`, to `DirectionGate`'s
   `beforeReload` prop too), and reloads once; call it from a
   mounted component after the language is saved. A flip that does not take becomes a reported
   give-up. Why: reloading during bundle evaluation crashed a Release build, and without the guard a
   failed flip restarts forever. (`direction-module`, `reload-outside-direction`,
   `reload-at-module-scope`)
6. **Give `expo-localization` `supportedLocales` only.** Never `supportsRTL` or `forcesRTL` (nor in
   `extra`). Why: the native module re-applies them from the device language at every launch and
   undoes an in-app choice (read in expo-localization 57.0.2's source). An app with no language
   choice of its own may opt into the `directionSource: "device"` profile in `contracts/rtl.json`:
   no restart machinery and no RTL flag needed (`supportsRTL` is tolerated but makes iOS follow the
   device language too), `forcesRTL` still banned. (`expo-localization-rtl`)
7. **A root drawn outside the app's providers sets its own text locale.** The restart screen, the
   root `ErrorBoundary` (its fallback component, or the JSX it draws inline) and any other outside
   root render `<TextLocaleProvider value={{ language, direction: directionOf(language) }}>`, with
   the language their text is in (the crash fallback: `languageNow()`, the source of its copy). Why:
   without it AppText falls back to English, left to right, and Arabic text is laid out backwards
   in the Latin line height. (`root-direction-provider`)
8. **Physical surfaces stay left to right.** Maps, media scrubbers, drawing pads and boards built
   from views sit in `PhysicalDirectionView` (list them in `contracts/rtl.json`); content that reads
   in the language's direction opts in with `mirrorsInRtl`. Gestures and safe-area insets stay
   physical: take insets symmetrically, never as left/right style keys. Why: north does not move to the right in Arabic, and media time runs left to right.
   (`physical-surface-ltr`)
9. **Flip only icons that point along the reading direction, inside `Icon`.** `DIRECTIONAL_ICONS`
   equals the directional names (`back`, `forward`, `chevron`, `undo`, `redo` by default) that
   exist in the icon set; play, clocks, checks and pictures never flip. Why: a call site always
   forgets, and a flipped play button is wrong. (`directional-icons`)
10. **Show every number in the language's digits.** Format with the tag from
    `localeTagFor(language, digits)` (`createNumberFormatter`, `{n, number}` messages); never
    `String(n)`, `.toString()` or `.toFixed()` for display; storage keeps plain numbers. Why: Hermes
    ignores the numbering system without the polyfill and the tag, and CLDR defaults move.
    (`number-to-text`; i18n-strings-and-catalogs checks `Intl.NumberFormat` itself)
11. **Isolate free text, never hand-write bidi controls.** `t()` and `isolate()` wrap interpolated
    free text in FSI…PDI; a whole left-to-right text in a right-to-left row is `<AppText
    direction="ltr">`; the person's own text (a task title) takes `firstStrongDirection(text)`. Why:
    marks and embeddings break on one platform and in copy, search and screen readers; iOS shifted a
    wrapped English line 4.4 pt when laid right to left. (`bidi-in-source`)
12. **Prove the layout on screen, on both platforms.** Jest renders with an explicit language and
    direction and cannot see layout; every changed screen is captured in a right-to-left language
    on an iOS simulator and an Android emulator. Why: mirroring, clipping and fonts only show on a
    device.

## Workflow

1. **Detect.** Read `src/i18n/languages.ts` (i18n-strings-and-catalogs creates it): with no
   right-to-left language in `RTL_LANGUAGES`, rules 1, 2, 9 and 11 still apply (they keep a future
   right-to-left language cheap) and the checker notes that the direction rules do not apply. The
   prerequisites are i18n-strings-and-catalogs (languages, digits, bidi, the forced polyfills),
   design-system-structure (`AppText`, `TextLocaleProvider`) and architecture-and-boundaries (the
   composition root). Decide who sets the direction: the default is the app (a language setting,
   or the resolved language, decides it through the gate); an app that only ever follows the
   device language may declare `"directionSource": "device"` in `contracts/rtl.json` and skip
   step 2's gate and guard (read "An app that only follows the device" in the direction-switch
   reference first: Android then follows the device locale even when the app falls back).
2. **First time: the direction layer.** Read [references/direction-switch.md](references/direction-switch.md).
   Copy `templates/src/` and `templates/test/` to the same paths, but never overwrite
   `src/i18n/languages.ts`, `digits.ts` or `bidi.ts`: they are i18n-strings-and-catalogs' files and
   hold the app's own `LANGUAGES` and numbering; copy them only when the app has none. The
   canonical composition root already has `directionGuard`; an app whose own predates it adds it to
   `Services`, `createDeviceServices` (the kv-store adapter), `createTestServices` and their test.
   Restructure the root layout as [examples/root-layout.md](examples/root-layout.md) shows: `RootLayout` decides (adapters and the
   saved language only), `DirectionGate` renders `AppRoot`, which does everything with effects; give
   the crash fallback its own `TextLocaleProvider`. Copy `templates/contracts/rtl.json` when a
   default does not fit (physical surfaces, another icon set or root file).
3. **Building or changing a screen or component.** Read
   [references/styling-and-mirroring.md](references/styling-and-mirroring.md) and imitate
   [examples/mirrored-row.md](examples/mirrored-row.md). Strings arrive translated, numbers arrive
   formatted.
4. **Numbers, mixed-direction text, fonts.** Read
   [references/digits-bidi-and-text.md](references/digits-bidi-and-text.md): format in the model
   hook with `createNumberFormatter(localeTagFor(language, digits))`; give the person's own text its
   first-strong direction; check a bundled right-to-left font against its list.
5. **Language screens.** Follow [examples/language-choice.md](examples/language-choice.md): save
   first, then `restartForDirection` when the direction changes (first run: on Continue; Settings:
   after a Restart / Later dialog). Stop audio and flush pending work before the reload.
6. **Physical surfaces.** Wrap each in `PhysicalDirectionView` and list its component name in
   `contracts/rtl.json` `physicalSurfaces`; a Skia canvas mirrors (or not) in its own layout
   (skia-canvas-rendering).
7. **Tests.** Read [references/testing-rtl.md](references/testing-rtl.md). Keep the template tests
   green; render through `test/test-app.tsx`'s `language` (and layout `direction`) options (the
   canonical file has them) and give each new component with text or a row one right-to-left render.
8. **Run the checks** from the repo root, fix every `FAIL` line (each names the file, the rule and
   the fix) and rerun until it prints `RESULT: PASS`:
   `node ${CLAUDE_SKILL_DIR}/scripts/check-rtl.mjs .` (multi-package: add `--app-dir apps/mobile`).
   Then `npm run typecheck`, `npx eslint . --max-warnings 0` and `npx jest --ci`.
9. **Look at it.** Capture every changed screen in a right-to-left language on an iOS simulator and
   an Android emulator, each named (light and dark, phone and tablet, 200 % text), with the
   recipes and the checklist in the testing reference; run the language-switch flow
   (`templates/.maestro/flows/rtl/01-language-switch.yaml`) after any change to the language screens or
   the startup.
10. **Report** what changed, which checks passed, which SKIP or note lines remain and who creates
    their targets, and what was verified on which platform (Android restart behaviour is not yet
    device-verified by this skill: say so until you have run it).

## Definition of done

- [ ] No physical left/right style key, `row-reverse`, `textAlign` literal, hand-set
      `writingDirection`, `Text` import or `scaleX: -1` outside their one allowed file.
- [ ] With a right-to-left language and the default `directionSource` (`app`):
      `src/i18n/direction.ts` is the only `I18nManager` user, forces both flags and records the
      guard before its single reload; the root layout renders `DirectionGate` first and outermost and does no
      startup work with effects in the same component; no reload runs at import time or bypasses
      `restartForDirection` for a language change.
- [ ] `expo-localization` has `supportedLocales` and no `supportsRTL`/`forcesRTL`; navigators and
      `DirectionProvider` follow the layout; the restart screen and the crash fallback mount their
      own `TextLocaleProvider`.
- [ ] Physical surfaces sit in `PhysicalDirectionView`; `DIRECTIONAL_ICONS` is exactly the
      directional icons that exist; numbers are formatted with the locale tag; free text is
      isolated and no bidi control is hand-written.
- [ ] The template tests pass (`npx jest src/i18n src/services/direction-guard src/ui test/direction-guard --ci`),
      and each new component with text or a row has a right-to-left render.
- [ ] Right-to-left screenshots of every changed screen on iOS and Android show mirrored rows,
      start-aligned text, unflipped physical surfaces and icons, the language's digits, nothing
      clipped at 200 %.
- [ ] Expected SKIP lines only while their target is not created yet:
      `SKIP src/i18n/languages.ts [direction-module] not yet created (i18n-strings-and-catalogs creates it)`,
      `SKIP src/i18n/languages.ts [direction-before-render] not yet created (i18n-strings-and-catalogs creates it)`,
      `SKIP src/app/_layout.tsx [direction-before-render] not yet created (expo-project-bootstrap creates it)`.
      Note lines (`physical-surface-ltr: no physical surfaces declared`, the no-right-to-left-language
      note, the `directionSource is "device"` note) are information, not problems.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-rtl.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **"Fixing" RTL with `row-reverse`, `isRtl ? … : …` or swapped `marginLeft`/`marginRight`.** React
  Native already swaps left and right in a right-to-left layout, so it double-flips. Use `row` and
  logical keys.
- **`left: x` for a drag thumb or scrubber.** React Native swaps it to `start` in Arabic, so the
  thumb runs backwards. Use `transform: [{ translateX: x }]` or a `PhysicalDirectionView`.
- **`paddingLeft: insets.left`.** The swap moves the notch padding to the wrong side; use
  `paddingInline: Math.max(gutter, insets.left, insets.right)` or `SafeAreaView edges`.
- **`textAlign: 'right'` for Arabic.** In a right-to-left layout `'right'` is the end edge, so the
  text lands on the left. Use `AppText align`.
- **`reloadAppAsync()` (or `Updates.reloadAsync()`) after a language change, at import time, or from
  an arbitrary module.** It skips the guard and the forced direction, and at import time it crashes
  Release builds. Use `restartForDirection` from a press handler or an effect.
- **Opening the database or hydrating stores in the component that renders the gate.** A restart
  repeats it; move it into the gate's child.
- **Deriving the layout direction from the language** (`DirectionProvider direction={directionOf(language)}`
  around the app, a navigator's `direction` from the language). Icons and navigation flip before the
  rows do; follow `readLayoutDirection()`.
- **A crash or restart screen without its own `TextLocaleProvider`.** Its Arabic text is laid out
  left to right with Latin line heights.
- **`supportsRTL: true` "to enable RTL".** React Native allows RTL by default; the flag makes the
  device language overwrite the in-app choice at every launch.
- **Flipping a whole map, a media scrubber, a clock or a play icon.** Only reading-direction arrows
  flip; a surface that mirrors maps its coordinates.
- **`String(count)` or a hard-coded locale in `Intl.NumberFormat`.** Latin digits in every language.
- **Pasting RLM, LRM or embeddings to nudge text into place.** Isolate free text, use `direction` for
  whole texts.
- **Trusting a green Jest run for layout.** Jest has no layout engine and reports left to right;
  only screenshots show mirroring.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/direction-switch.md](references/direction-switch.md) | Verified facts, the modules, deciding first in the root layout, the three flows, text vs layout direction, navigation, roots outside the providers, expo-localization, Android specifics, follow-the-device apps, React Navigation appendix, multi-package | Workflow steps 2 and 5 |
| [references/styling-and-mirroring.md](references/styling-and-mirroring.md) | Logical keys, rows and grids, text alignment, safe areas, which icons flip, the design system's RTL checklist, physical surfaces, gestures | Workflow steps 3 and 6 |
| [references/digits-bidi-and-text.md](references/digits-bidi-and-text.md) | Digit tags and outputs, numbering systems per language, numbers outside messages, the digits setting, isolation, a whole LTR text in an RTL row, the person's own text, Android first-strong, fonts for RTL scripts | Workflow step 4 |
| [references/testing-rtl.md](references/testing-rtl.md) | What Jest sees, the tests to keep, right-to-left renders, iOS simulator and Android emulator recipes (named devices), the Maestro flow, screen readers, the screenshot matrix | Workflow steps 7 and 9 |
| [examples/root-layout.md](examples/root-layout.md) | The root layout, app root, composition-root and crash-fallback changes, verified in the reference app | Workflow step 2 |
| [examples/mirrored-row.md](examples/mirrored-row.md) | A task row that mirrors, keeps the title's own direction, its test and the wrong versions the checker catches | Workflow step 3 |
| [examples/language-choice.md](examples/language-choice.md) | The Settings language model hook: save, ask, restart once | Workflow step 5 |
| `templates/src/i18n/` | `direction.ts`, `direction-plan.ts`, `direction-gate.tsx`, `direction-restart.tsx`, `direction-context.tsx` (synced; this skill owns the canonical copy), `create-number-formatter.ts`, `text-direction.ts`, each with its test; `languages.ts`, `digits.ts`, `bidi.ts` synced from i18n-strings-and-catalogs (do not edit here) | Workflow step 2 (copy) |
| `templates/src/services/direction-guard/` | The guard port, the `expo-sqlite/kv-store` adapter, the fake and its test (synced; this skill owns the canonical copy) | Workflow step 2 (copy) |
| `templates/src/ui/` | `PhysicalDirectionView` and its test | Workflow steps 2 and 6 (copy) |
| `templates/test/direction-guard/` | The adapter's test on kv-store's real SQL over `node:sqlite` (synced; this skill owns the canonical copy) | Workflow step 2 (copy) |
| `templates/contracts/` | `rtl.json` (the app's direction facts and the `directionSource` profile, every key optional) and its JSON Schema | Workflow step 2, when a default does not fit |
| `templates/.maestro/flows/rtl/01-language-switch.yaml` | Maestro flow: switch to a right-to-left language, one restart, data kept | Workflow step 9 (copy, fill the testIDs) |
| `scripts/check-rtl.mjs` | Checks the 18 rule ids named in the rules above, across the app source (routes included), config plugins and the app config | Workflow step 8, after every layout change |
| `scripts/selftest.mjs` | Proves the checker passes the templates over a small Tasks app and catches each planted bug | After changing the checker or a fixture |
| `scripts/check-lib.mjs` | Shared script helper, synced (do not edit here) | Never by hand |
| `scripts/lib/` | The source scanner and the literal reader the checker uses, synced (do not edit here) | Never by hand |
| `assets/shared.json` | Declares the synced files | When adding a shared file |
| `assets/template-placeholders.json` | Tasks-app testIDs that fill the Maestro flow when the templates are verified | When changing the flow's placeholders |
| `tests/bases/app/` | The small Tasks app the fixtures start from | When a case needs a new base file |
| `tests/fixtures/` | Overlay cases: good, one planted bug per rule, SKIP and note cases, the device profile, multi-package, bad input | When adding a rule |

## Related skills

- `i18n-strings-and-catalogs` - texts, keys, plurals, `t()`, the polyfills, languages, digits and bidi helpers.
- `design-system-structure` - `AppText`, `TextLocaleProvider`, fonts and tall-script line heights.
- `architecture-and-boundaries` - the composition root the guard joins, nothing at import time.
- `settings-and-preferences` - the saved language and digits settings and their screens.
- `error-handling-typed-results` - the root crash fallback that needs its own text locale.
- `skia-canvas-rendering` - canvas surfaces that mirror in their layout mapping.
- `accessibility-as-code` - screen-reader order, reduce motion, 200 % text.
- `unit-and-component-tests` - `test/test-app.tsx` and the render helpers.
- `e2e-maestro` - running the language-switch flow.
- `ios-simulator-build` - named simulators and the builds for the right-to-left captures.
- `android-emulator-build` - named emulators and the builds for the Android right-to-left captures.
- `app-startup-and-bootstrap` - the startup order around `DirectionGate` (RootLayout, gate, AppRoot).
- `design-visual-parity` - comparing right-to-left screens with the approved baseline.
