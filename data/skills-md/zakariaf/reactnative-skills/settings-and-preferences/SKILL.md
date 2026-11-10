---
name: settings-and-preferences
description: Builds app settings - saved fields, defaults, rows, each setting's effect, resets that keep them. Use when adding a setting or toggle, or a setting is ignored or lost on restart. Not for theme tokens (design-system-structure).
---

# Settings and preferences

Every setting is saved in one place, changed by one action, shown by one row, and applied by code
outside the settings screen, at once and without a Save button; data resets never touch it, and a
checker proves the whole chain against the app's own settings contract on iOS and Android alike.

## Rules that must hold

1. **One settings model, one owner.** Every saved preference is a field of one strict valibot object
   (`SETTINGS_SCHEMA` in `src/stores/settings/`) and is listed in `contracts/settings.json` with its
   validator, first-launch value, action and effect; nothing else keeps a copy (no `useState` mirror,
   no side cache, no zustand `persist`, no second key-value write). Why: one place to read, change
   and decode, so a restart can never show an older value. (`settings-schema`, `single-writer`)
2. **Saved through one synchronous adapter, read before the first paint.** Default: `expo-sqlite/kv-store`
   behind `SettingsStoragePort`, one JSON value under one key, read in the root layout's first-render
   initializer. Why: the first frame already has the saved theme and language, and one key is one
   atomic write. (`hydrate-sync`)
3. **Reduce, persist, then publish; a failed write publishes nothing.** The screen never shows a value
   that is not saved, the failure is shown (`settings.save-failed`), and storage that cannot be read
   runs the session in memory without overwriting it. No Save button, no delayed write.
   (`persist-then-publish`)
4. **One pure reducer action per change; ranges clamped in the reducer.** Imperative kebab-case
   (`set-theme`), a no-op returns the same object (nothing written), integer percent rounded and
   clamped with a property test. Why: every change is testable without React and replays the same.
   (`reducer-action`)
5. **Decode field by field; a stored field never changes shape in place.** A missing field takes its
   default quietly, an unreadable one falls back alone and is recorded, a new meaning gets a new field
   name, and a frozen sample of every shipped shape keeps decoding. Why: the key-value store has no
   migrations, and one bad value must never reset every setting.
6. **First-launch values follow the phone; noise is opt-in.** Settings that mirror a phone setting
   (language, theme, reduce motion, digits) start at `'system'`/`null`; sound and anything that
   interrupts start off; every other value is a product decision written in the contract.
   (`settings-default`)
7. **Every setting has an effect outside the settings code, applied at once**, through one of four
   mechanisms: a provider re-render (`PreferencesRoot` feeds `I18nProvider`, `AppThemeProvider
   preference`, the reduce-motion preference context the root stack's `RootMotion` hands to
   `MotionConfig`), a store subscription started at startup that returns its
   unsubscribe (sound), an adapter that reads the store at call time (the haptics gate: created
   before the services, connected once the store opens, silent until then), or a feature hook
   reading a selector. Why: a setting nothing reads is a bug people see. (`setting-effect`)
8. **Store canonical units; convert at the edge.** The volume is integer percent; `toSoundOutput`
   divides by 100 for the 0..1 an audio API takes; a 0..1 slider dispatches only when the whole
   percent changes. (`unit-scale`)
9. **Every row dispatches its action; rows that do not apply are hidden, never greyed.** Visibility
   is the pure `settingsGroupsFor(context)` over facts (haptics supported, Premium owned, a consent
   entry point needed), each rule unit-tested; testIDs and label keys come from one typed table.
   Why: a disabled control nobody can enable is noise for VoiceOver and TalkBack. (`row-dispatch`)
10. **A language change switches the text at once; only a layout-direction flip restarts, after
    the person confirms.** `planLanguageChange` compares the new language's direction with the
    layout's and the choice is saved either way. Why: React Native applies a direction at the next
    start, and a needless restart throws away state. (`restart-on-direction-only`)
11. **Resets never touch the settings.** "Delete all data" (`createDataResets`) deletes data through
    the data layer (persistence-and-migrations owns the SQL) and keeps settings and purchases (and
    first-run flags, unless the product decides otherwise); no code outside the storage adapter
    clears a whole key-value store (`Storage.clearSync()`, `AsyncStorage.clear()`); a failed delete
    is shown, never silent; "Reset settings" is its own action and confirmation; a save-document
    reset is one write inside `updateAndPublish`'s callback. (`reset-keeps-settings`, `reset-publish`)
12. **A switch plays its feedback once, after the dispatch** (the model input `onToggled`, which
    calls `playUiFeedback(services, 'toggle')`; never the press feedback); sliders and segments play
    none. Why: the feedback reads the settings at call time, so "sound off" is
    already silent. (`toggle-feedback`, when the contract sets it)
13. **Reduce motion is tri-state.** The switch shows the resolved value (`useReduceMotion()`) and
    writes the opposite explicitly (`'on'`/`'off'`); accessibility-as-code owns the resolution and the
    ban on Reanimated's `useReducedMotion`, and design-system-structure owns the theme provider.

## Workflow

1. Read [references/settings-model.md](references/settings-model.md): where each piece lives, the
   fields and first-launch values, persistence, decoding, the effects table, iOS and Android, resets,
   the contract keys and every checker rule.
2. **New settings model.** `npx expo install expo-sqlite expo-localization`, then
   `npm install -E zustand@5.0.15 valibot@1.5.0` (stack table, verified 2026-10-03; re-verify with
   `npm view zustand@5 version`). Copy `templates/src/stores/settings/` (schema, codec, reducer and
   its `settings-reducer-cases.ts` table, selectors, store), `templates/src/services/settings-storage/`,
   `templates/src/data/open-device-settings.ts` and `templates/contracts/` to `contracts/`. Replace the
   Tasks fields with the app's own, in the contract first, then the schema, defaults, codec
   `v.fallback` lines, actions, reducer cases and selectors.
3. **Wire the startup** (copy `templates/src/features/settings-effects/`): in the root layout's
   `decideStartup` create the gate (`createHapticsGate()`) before `createDeviceServices`, whose haptics
   adapter takes `gate.isEnabled`, and resolve the language from `readSavedLanguage(...)`
   ([examples/root-layout.tsx](examples/root-layout.tsx)); in AppRoot's `startApp`, after the data
   layer and the error sink, open the store (`openDeviceSettings(errorLog)`), then
   `gate.connect(settings)` and `connectSoundSettings` (audio-and-haptics-feedback owns both ports);
   render `SettingsStoreProvider` and `PreferencesRoot` in place of fixed provider values; the
   canonical `root-stack.tsx` stays as it is (its `RootMotion` reads the preference `PreferencesRoot`
   provides) ([examples/app-root.tsx](examples/app-root.tsx),
   [examples/app-providers.tsx](examples/app-providers.tsx)).
4. **The screen.** Read [references/rows-and-controls.md](references/rows-and-controls.md). Copy
   `templates/src/features/settings/` and `templates/src/config/external-links.ts`, merge
   `templates/src/i18n/catalogs/*.json` into the app's catalogs (translate for every app language),
   add the route as [examples/settings-route.tsx](examples/settings-route.tsx) and the view as
   [examples/settings-screen.tsx](examples/settings-screen.tsx) with the ui-component-library rows and
   the three confirm dialogs; gather the row facts (signed in, haptics, Premium, consent) and the
   `dataResets` wiring (`updateAndPublish` around the data layer's reset) as
   [examples/use-settings-input.ts](examples/use-settings-input.ts). Fill `PRIVACY_POLICY_PAGE`: its
   test fails while the placeholder is left in. The account rows hand off to auth-and-secure-storage.
5. **Adding or changing a setting:** follow "Adding or changing a setting" in the model reference:
   contract, schema and defaults, codec line and a frozen sample, action (test first), selector, row,
   effect. A new setting is a product decision: ask the developer first.
6. **Save document instead of the key-value store** (persistence-and-migrations' document mode): use
   [examples/settings-contract-document-mode.json](examples/settings-contract-document-mode.json) as
   the contract and read the model reference's appendix.
7. **Test**, then `npm run typecheck`:

   ```bash
   npx jest src/stores/settings src/services/settings-storage src/features/settings \
     src/features/settings-effects src/config --ci --maxWorkers=2
   ```

8. **On devices**, after a change to the storage or the startup: change the theme, kill and relaunch on
   a named iOS simulator and a named Android emulator (commands in the rows reference); the first frame
   must show the saved theme. Without devices, say in the report that this check is owed.
9. **Run the checker** from the repo root: `node ${CLAUDE_SKILL_DIR}/scripts/check-settings.mjs .`;
   fix every `FAIL` line (file, rule and fix are printed) and rerun until it prints `RESULT: PASS`.

## Definition of done

- [ ] `contracts/settings.json` lists every field (validator, first-launch value, action, effect) and
      every action; schema and defaults match it, and the codec has a `v.fallback` line per field.
- [ ] The store hydrates synchronously, persists before it publishes, publishes nothing on a failed
      write, and never writes when the saved settings could not be read; its tests pass.
- [ ] Every action has a reducer case and a test; every range is clamped with a property test; the
      codec test holds a frozen sample of every shipped shape.
- [ ] Every row dispatches its action; hidden rows follow `settingsGroupsFor` and its tests; row
      testIDs and labels come from the typed tables and every app catalog has the keys.
- [ ] Every field's effect is wired and tested outside the settings code; percent values are
      converted at the edge.
- [ ] A language of the other direction opens "Restart to apply"; the same direction switches at once.
- [ ] Data resets keep the settings and purchases (first-run flags as the product decided), and a
      failed delete shows `settings.delete-all-data.failed`; "Reset settings" is its own confirmed
      action.
- [ ] The Privacy policy row opens the app's real https page (`PRIVACY_POLICY_PAGE` filled in).
- [ ] The restart check passed on a named iOS simulator and a named Android emulator, or the report
      says it is owed.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-settings.mjs .` prints `RESULT: PASS` (expected only
      before the data layer exists: `SKIP src/data/reset-data.ts [reset-keeps-settings] not yet
      created (persistence-and-migrations creates it)`; an app with no settings prints `NOT APPLICABLE`).

## Anti-patterns

- **A local `useState` copy of a setting in the screen.** It drifts from the store and skips the save;
  read the store and dispatch.
- **A Save button or a debounced write.** Every change is saved at once; the store already persists
  before it publishes.
- **Loading settings with an async API after the first render.** The app flashes the default theme
  and language; read synchronously in the first-render initializer.
- **zustand's `persist` middleware or AsyncStorage for settings.** A second, unversioned copy that
  publishes before it saves; use the storage port.
- **One storage key per field.** A two-field change becomes two writes and can be half saved; one
  JSON value under one key.
- **Resetting every setting because one saved value is unreadable.** Decode field by field.
- **Reading `settings.reduceMotion` or `settings.theme` directly in a component.** `'system'` must
  resolve against the phone; the providers and `useReduceMotion()` do that.
- **Passing the stored percent to a 0..1 API or a 0..1 slider value straight into the store.**
  Convert at the edge; dispatch only whole-percent changes.
- **Greying out rows that do not apply.** Hide them, from the pure visibility function.
- **Restarting for every language change**, or opening the restart dialog after a failed save (the
  restart comes back in the old language).
- **Clearing the whole key-value store in "Delete all data"** (`Storage.clearSync()`,
  `AsyncStorage.clear()`): the settings go with it. Delete through the data layer.
- **Playing the toggle sound in the row component, or before the dispatch.** It sounds twice, and
  "sound off" still clicks.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/settings-model.md](references/settings-model.md) | Homes, fields, defaults, persistence, decoding, actions, effects, iOS and Android, resets, adding a setting, document mode, multi-package, contract keys, checker rules | Workflow steps 1, 5 and 6 |
| [references/rows-and-controls.md](references/rows-and-controls.md) | Route, model and view; each row kind with VoiceOver and TalkBack; slider pitfall; language list and restart; dialogs; copy keys; testIDs and device flows; tests; React Navigation appendix | Workflow steps 4 and 8 |
| `templates/src/stores/settings/` | Schema and defaults, codec, reducer and `settings-reducer-cases.ts` (the rules as data, also read by state-management-zustand's reducer checker), selectors, store, store context, each with its test (synced canonical copies: never edit here) | Workflow step 2 |
| `templates/src/services/settings-storage/` | `SettingsStoragePort` and its fake with a test (synced), and the `expo-sqlite/kv-store` adapter | Workflow step 2 |
| [templates/src/data/open-device-settings.ts](templates/src/data/open-device-settings.ts) | Creates the store over the key-value adapter (composition root) | Workflow steps 2 and 3 |
| `templates/src/features/settings-effects/` | `PreferencesRoot` (language, digits, theme, reduce motion), `connectSoundSettings`, `createHapticsGate`, `readSavedLanguage` (for rtl-and-direction's `DirectionGate`), with tests | Workflow step 3 |
| `templates/src/features/settings/` | Rows and visibility (with the account group), preference handlers, `data-resets.ts` ("Delete all data" after its confirmation), the model hook, the language-change plan, with tests | Workflow step 4 |
| `templates/src/config/` | `external-links.ts` (privacy policy page, store review page per platform, support mail) and its test | Workflow step 4 |
| `templates/src/i18n/catalogs/` | The settings copy keys in `en` and `ar`, merged into the app's catalogs | Workflow step 4 |
| `templates/contracts/` | `settings.json` (the Tasks contract) and `settings.schema.json` | Workflow steps 2 and 5 |
| [examples/root-layout.tsx](examples/root-layout.tsx) | The canonical root layout with the haptics gate and the saved language in `decideStartup` | Workflow step 3 |
| [examples/app-root.tsx](examples/app-root.tsx) | The canonical AppRoot opening the store, connecting the effects and rendering `PreferencesRoot` | Workflow step 3 |
| [examples/app-providers.tsx](examples/app-providers.tsx) | AppRoot's outer providers with `SettingsStoreProvider` after the data layer | Workflow step 3 |
| [examples/settings-route.tsx](examples/settings-route.tsx) | Thin Expo Router route and its feature hook shape (row hand-offs, the three dialogs) | Workflow step 4 |
| [examples/settings-screen.tsx](examples/settings-screen.tsx) | The pure screen view over the model: rows, failure notes heard on both platforms, confirm dialogs | Workflow step 4 |
| [examples/use-settings-input.ts](examples/use-settings-input.ts) | Where the row facts, locales, layout direction and the data-reset wiring come from | Workflow step 4 |
| [examples/settings-contract-document-mode.json](examples/settings-contract-document-mode.json) | The contract for settings kept in the save document | Workflow step 6 |
| `scripts/check-settings.mjs` | Checker for the contract, schema, defaults, actions, store, writers, rows, effects, units, resets, restarts and feedback | Workflow step 9, and at the end |
| `scripts/selftest.mjs` | Proves the checker passes the templates and catches every planted bug | After changing the checker |
| `scripts/check-lib.mjs` | Shared script helpers, synced from the library (do not edit here) | Never by hand |
| `scripts/lib/object-literal.mjs` | Shared object-literal reader, synced (do not edit here) | Never by hand |
| `assets/shared.json` | Declares the synced files (check-lib, the object-literal reader, the canonical store and port files) | When adding a shared file |
| `assets/template-placeholders.json` | Sample values for the template placeholders (`__PRIVACY_POLICY_URL__`) used when the templates are verified | When adding a placeholder |
| `tests/` | `bases/app/` (a minimal app) and `fixtures/` (overlay cases over the templates, including document mode and silent decoys) | When adding a rule to the checker |

## Related skills

- `state-management-zustand` - the store pattern, selectors and `useShallow`, `updateAndPublish`.
- `persistence-and-migrations` - the key-value boundary, the save document, data resets.
- `design-system-structure` - `AppThemeProvider` and its `preference` prop.
- `accessibility-as-code` - `MotionConfig`, `useReduceMotion()`, roles and targets.
- `i18n-strings-and-catalogs` - `I18nProvider`, language resolution, digits, catalogs.
- `rtl-and-direction` - the layout direction and the restart that applies it.
- `audio-and-haptics-feedback` - the audio and haptics ports the effects drive.
- `ui-component-library` - the row, slider, segmented and dialog components.
- `auth-and-secure-storage` - the Sign out and Delete account rows' flows.
- `navigation-and-routing` - the settings routes and sub-screens.
- `in-app-purchases`, `admob-ads-and-consent` - the Premium and privacy-choices rows.
- `local-notifications`, `permissions-and-system-prompts` - reminder settings and system settings links.
- `e2e-maestro` - the restart flow on named devices.
