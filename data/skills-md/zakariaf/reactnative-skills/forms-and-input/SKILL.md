---
name: forms-and-input
description: "Builds react-hook-form + valibot forms: one schema, catalog-key errors, TextField kinds (keyboard, autofill), focus chain. Use when adding a form, text field or validation, or the keyboard hides a field. Not for sign-in (auth-and-secure-storage)."
---

# Forms and input

Makes every form in an Expo app one valibot schema behind react-hook-form, whose every message is a
catalog key, rendered with one labelled `TextField` whose kind sets the keyboard, autofill and
capitalization, chained by the return key, kept above the keyboard on iOS and Android, and checked
asynchronously only outside the schema. One zero-dependency checker proves it on the app's source.

## Rules that must hold

1. **One valibot schema per form, behind `valibotResolver`.** `useForm<Input, unknown, Output>({
   resolver: valibotResolver(schema) })`; the field types are `v.InferInput`, the submitted draft is
   `v.InferOutput`; no `rules` on a Controller (`form-resolver`). Why: one definition gives the type,
   the runtime check and every message, so a field can never validate one way and save another.
2. **Every message is a catalog key, translated at the field.** Each validation action carries a
   literal key of the source catalog (`v.nonEmpty('task-editor.title.required')`,
   `schema-message-key`); `setError` passes a key too (`error-message-key`); `fieldMessageKey` turns
   anything else into the generic key. Why: an action without a message shows valibot's English
   default ("Invalid length: Expected !0 but received 0") in every language.
3. **The schema is synchronous and Hermes-safe.** No `*Async` API in a form schema (`schema-async`);
   no graphemes or words actions unless `Intl.Segmenter` is polyfilled (`schema-segmenter`). Why: the
   resolver runs the whole schema on every validation, with no pause, cancel or deadline, and Hermes
   has no `Intl.Segmenter` (it throws on the phone while Jest on Node passes).
4. **An async check ("is this name free?") runs in `useAsyncFieldCheck`, never in the schema.** It
   starts only for a valid shape, waits for typing to pause, lets the newest value win, has a
   deadline, stops on unmount, and says which value it answers; submit needs a pass for exactly the
   value sent, and the server still judges at write time (a refusal becomes `setError` with a key).
   Why: a check per keystroke floods the server and an old answer can land on a newer value.
5. **Digits in any script are read.** A schema that matches `\d` or calls `Number()` transforms the
   text with `toLatinDigits` first, or, for a decimal, money or quantity field, with
   value-objects-money-and-units' `normalizeDecimalInput` (`latin-digits`). Why: Arabic, Persian and
   Devanagari keyboards, and the iOS pads in those languages, type ٣٠ or ۳۰ (and `٫` or `,` for the
   decimal point), which `/^\d+$/` and `Number()` refuse.
6. **Screens render `TextField`, never a raw `TextInput`** (`raw-text-input`). `TextInput` lives only
   in the field folder (`src/ui/form/`), whose components join the component catalogue. Why: label,
   error, hint, live region, keyboard and autofill are solved once; a raw input forgets one of them.
7. **The visible label is the input's accessible name; the error is never colour alone.** The label
   sits above the input; on iOS the input carries it as `accessibilityLabel` (the label view hidden
   from VoiceOver), on Android it points at the label view with `accessibilityLabelledBy` (an
   EditText's content description loses to its typed text). The error or hint is the input's
   `accessibilityHint` and sits in a polite live region, and an invalid field gets a bold edge and a
   sentence (`input-label`). Why: a placeholder vanishes when typing starts and is not read as a
   name, and about 1 in 12 men cannot tell the error colour apart.
8. **A field kind sets the keyboard, autofill, capitalization, autocorrect and secure entry
   together** (`FIELD_KINDS`; a raw input that hides text sets `autoComplete`, an email keyboard sets
   `autoCapitalize`: `input-preset`). Why: a password without `autoComplete` gets no password manager
   on either platform, and an email field that capitalizes breaks every address.
9. **Fields bind the React Native way: `onChangeText`, `onBlur`, `ref`** (`useTextField`; never
   `onChange={field.onChange}`, `{...field}` or `register`: `field-on-change`; the ref is passed on:
   `field-ref`). Why: react-hook-form reads `event.target.value`, which a React Native change event
   lacks, so the field would hold `undefined`; without the ref nothing can focus the field.
10. **Errors wait for the first blur, and a refused submit goes to the first problem.** `mode:
    'onTouched'` (`form-mode`), `shouldFocusError` left on (`focus-error`), and the refusal is
    announced. Why: `onChange` mode shouts "invalid email" at the first letter; focusing the field
    moves VoiceOver and TalkBack there too.
11. **The return key walks the form.** A single-line field names the next field (`enterKeyHint`
    `next`, `submitBehavior` `submit`, `setFocus`), the last one submits (`done`), a multiline field
    makes new lines. Why: closing and reopening the keyboard between fields flickers and loses the
    user's place.
12. **The keyboard never hides the field or swallows a tap.** `KeyboardProvider` wraps the root
    (`keyboard-provider`); forms scroll in `KeyboardAwareScrollView` (`keyboard-aware-scroll`) with
    `keyboardShouldPersistTaps="handled"` (`keyboard-persist-taps`); a feature with a number,
    decimal or phone pad renders `KeyboardDoneBar` (`pad-done-bar`), and the scroll view keeps the
    focused field above the bar (`useDoneBarSpace`: `bottomOffset` = the bar's measured height plus
    a gap). Why: Android's edge-to-edge window no longer resizes for the keyboard, the first tap on
    Save would only close it, the iOS pads have no return key, and the bar sits on the keyboard,
    over whatever the scroll view keeps just above it.
13. **Submit is one void intent that never loses input.** The model calls `handleSubmit(...)()` and
    catches its promise, shows `isSubmitting` (from `useFormState`) as busy, resets the form only
    after the save returned `ok` and `handleSubmit` has settled, and keeps every typed character on
    a failure. Why: `handleSubmit` rethrows what the save throws, a reset before the write is data
    loss, and a reset inside the save is undone (the form stays "submitted" and the next draft
    shows errors from its first keystroke).

## Workflow

1. **Look first.** From the repo root run `node ${CLAUDE_SKILL_DIR}/scripts/check-forms.mjs .`.
   NOT APPLICABLE means the app has no form yet; otherwise the problems are the work list. Read
   [references/checks-and-tests.md](references/checks-and-tests.md) for each rule's fix.
2. **Prerequisites.** These come from their owner skills and must exist first: the theme, `AppText`
   and `PressableSurface` (design-system-structure), `t()`/`useT`, `MessageKey` and the catalogs
   (i18n-strings-and-catalogs), `useServices` and the error log (architecture-and-boundaries),
   `Result` (error-handling-typed-results), the latest-request, `delayOrAbort` and `withTimeout`
   helpers (async-safety), `useAnnounce`/`useReduceMotion` (accessibility-as-code), the render
   helpers (unit-and-component-tests). Install, verified 2026-10-03 (re-verify:
   `npm view react-hook-form version`): `npx expo install react-native-keyboard-controller`
   (1.21.9, in the SDK 57 map, included in Expo Go) and
   `npm install -E react-hook-form@7.89.0 @hookform/resolvers@5.9.1 valibot@1.5.0`.
3. **Copy the field kit** from `templates/` to the path on each file's first line: `src/ui/form/`
   (`field-kinds.ts`, `text-field.tsx`, `field-note.tsx`, `keyboard-done-bar.tsx`), `src/hooks/`
   (`use-text-field.ts`, `field-message-key.ts`, `use-async-field-check.ts`,
   `use-done-bar-space.ts`),
   `src/core/text/latin-digits.ts`, `test/forms/i18n-form-wrapper.tsx`, each with its test; merge
   the `forms.*` keys of `templates/src/i18n/catalogs/*.json` into every catalog and translate them.
   `__mocks__/react-native-keyboard-controller.ts` is the canonical root mock (keep it as is).
4. **Wire the root.** Wrap the root stack in `KeyboardProvider`, inside `GestureHandlerRootView`
   and outside the motion and navigation-theme providers
   ([examples/root-stack-keyboard-provider.tsx](examples/root-stack-keyboard-provider.tsx)). The
   canonical `root-stack.tsx` of app-startup-and-bootstrap already renders it: check it is there; in an
   older root, add the import and the element and keep the file's header (the `device-only` marker).
5. **List the field components.** If `contracts/component-library.json` does not exist yet, create
   it from ui-component-library's catalogue template first (with `src/ui/form/` in place, that
   skill's `check-components` fails `catalogue-missing` without it), then add the three entries of
   `assets/component-library-entries.json`.
6. **Write the schema first, with its test.** Copy the `task-editor` templates as the pattern and
   rename them: bounds from the data layer, a key per message, `toLatinDigits` before digits
   (`normalizeDecimalInput` for a decimal, money or quantity field), local
   duplicate checks through a factory. Read
   [references/schemas-and-messages.md](references/schemas-and-messages.md).
7. **Write the model hook**: `useForm` with the resolver and `mode: 'onTouched'`, one `useTextField`
   per field with its kind and `next`/`onSubmit`, the submit intent, labels translated
   ([references/fields-and-autofill.md](references/fields-and-autofill.md),
   [references/keyboard-focus-and-submit.md](references/keyboard-focus-and-submit.md)).
8. **Add an async check only when the answer lives elsewhere** (a server, another store): a
   `FieldCheck` port, `useAsyncFieldCheck`, the status and error on the field, submit gated on
   `hasPassed(value)` ([references/async-checks-and-server-errors.md](references/async-checks-and-server-errors.md),
   [examples/list-name-availability.ts](examples/list-name-availability.ts)).
9. **Write the screen** as a pure view: `KeyboardAwareScrollView` with
   `keyboardShouldPersistTaps="handled"`, one `TextField` per field spread from the model, the save
   failure in a live region, `KeyboardDoneBar` when a pad kind is used, its `onHeightChange` and the
   scroll view's `bottomOffset`/`extraKeyboardSpace` from the model's `useDoneBarSpace()`.
10. **Test**: the schema (every message is a key in every catalog), the model (focus, refused submit,
    failed save keeps input, digits), the screen by label and role ending in the pressable audit
    ([references/checks-and-tests.md](references/checks-and-tests.md)).
11. **Run the checks**: run, fix, rerun until `RESULT: PASS`. Then run the neighbours' checkers
    named in Related skills (component catalogue, accessibility, catalogs).

## Definition of done

- [ ] Every form has one valibot schema behind `valibotResolver`; its test proves every message it
      can produce is a key in every catalog.
- [ ] Screens render `TextField` with a kind; `TextInput` appears only in `src/ui/form/`.
- [ ] Each field shows a visible label, its error under it after the first blur, and the return key
      moves to the next field or submits.
- [ ] Async checks go through `useAsyncFieldCheck`; submit requires `hasPassed(value)`; server
      refusals become `setError` with a catalog key.
- [ ] `KeyboardProvider` wraps the root; forms scroll in `KeyboardAwareScrollView` with
      `keyboardShouldPersistTaps="handled"`; pad fields have `KeyboardDoneBar`, and the scroll
      view's `bottomOffset` comes from `useDoneBarSpace` (the screen test asserts it).
- [ ] A failed save keeps the input; only a saved draft resets the form, after `handleSubmit`
      settled.
- [ ] `contracts/component-library.json` exists and lists `TextField`, `FieldNote` and
      `KeyboardDoneBar`.
- [ ] Tested by hand once on an iOS simulator and an Android emulator, each named for the job: the
      focused field stays above the keyboard and the Done bar (also at the largest text size), Next
      walks the fields, autofill offers the right entries, and VoiceOver and TalkBack read each
      field's label, empty and filled (record the result in fields-and-autofill.md).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-forms.mjs .` prints `RESULT: PASS` (or NOT APPLICABLE
      before the first form). The only SKIP it may print is
      `SKIP src/i18n/catalogs/en.json [schema-message-key] not yet created (i18n-strings-and-catalogs creates it)`.

## Anti-patterns

- **`onPress={form.handleSubmit(save)}`.** The promise is dropped and a throwing save becomes an
  unhandled rejection. Call `form.handleSubmit(save, onInvalid)().catch(record)` inside a void intent.
- **`v.checkAsync(isNameFree)` in the schema.** It runs on every keystroke after the first blur,
  never cancels and has no deadline. Use `useAsyncFieldCheck`.
- **`placeholder="Email"` as the only label.** It disappears while typing and screen readers do not
  treat it as the name. Show a label above the field.
- **`watch()` to show live values or derive submit state.** React Compiler cannot memoize it (lint
  `react-hooks/incompatible-library`) and it re-renders the whole form per keystroke. Use
  `useWatch({ name })` or `useFormState`.
- **`disabled` on the Save button until the form is valid.** The user cannot find out what is wrong.
  Keep Save pressable; a refused submit focuses and announces the first problem.
- **Wrapping the screen in React Native's `KeyboardAvoidingView` or a plain `ScrollView`.** Android
  edge-to-edge ignores the resize, and the focused field ends up under the keyboard.
- **`keyboardType="numeric"` plus `Number(text)`.** The decimal separator and the digits depend on
  the keyboard's language. Use the `integer` or `decimal` kind and `toLatinDigits` in the schema.
- **`form.reset()` right after calling the save, or inside `handleSubmit`'s callback.** A failed
  write throws the input away; a reset inside the callback leaves the form "submitted". Reset in
  the `.then` after `handleSubmit(...)()`, only when the save returned `ok`.
- **Translating in the schema (`v.nonEmpty(t('...'))`).** The schema is built once, the language can
  change, and the checkers cannot see the key. Pass the key; the field translates.
- **`KeyboardToolbar` from react-native-keyboard-controller as the Done bar.** In 1.21.9 its buttons
  speak fixed English labels and cap their text at 130 %; check-forms does not count it unless the
  app lists it in `forms.doneBars`. Use `KeyboardDoneBar`.
- **A fixed `bottomOffset` next to a sticky bar.** The bar rides on the keyboard and covers the
  bottom of the focused field. Take the offset from `useDoneBarSpace`.

## Files in this skill

| File | What it is | Read/run when |
| --- | --- | --- |
| `references/schemas-and-messages.md` | valibot and the resolver, input and output types, message keys, digits, Segmenter, cross-field and date fields | writing a schema (step 6) |
| `references/fields-and-autofill.md` | TextField, the kinds, autofill on iOS and Android (verified mapping), labels and screen readers, RTL | adding a field or a kind (step 7) |
| `references/keyboard-focus-and-submit.md` | modes, focus chain, keyboard-controller, edge-to-edge, Done bar, submit, drafts, leaving a dirty form | wiring the model and screen (steps 4, 7, 9) |
| `references/async-checks-and-server-errors.md` | useAsyncFieldCheck design, races, timing, server refusals to fields | an async or server check (step 8) |
| `references/checks-and-tests.md` | every check-forms rule with its fix, config keys, limits, test recipes | running the checker, writing tests (steps 1, 10, 11) |
| `templates/src/ui/form/` | `field-kinds.ts`, `text-field.tsx` (with an Android-preset test), `field-note.tsx`, `keyboard-done-bar.tsx`, with tests | step 3 |
| `templates/src/hooks/` | `use-text-field.ts`, `field-message-key.ts`, `use-async-field-check.ts`, `use-done-bar-space.ts`, with tests | step 3 |
| `templates/src/core/text/` | `latin-digits.ts`: digits of any script to ASCII, with its test | step 3 |
| `templates/src/features/task-editor/` | the New task form: schema, model, screen, tests (the pattern to copy) | step 6 |
| `templates/src/i18n/catalogs/` | `en.json`, `ar.json`: the `forms.*` and `task-editor.*` keys to merge | step 3 |
| `templates/test/forms/i18n-form-wrapper.tsx` | test providers with the real catalogs, failing on a missing key | step 10 |
| `templates/__mocks__/react-native-keyboard-controller.ts` | canonical root Jest mock (synced, owned here) | step 3 |
| `examples/root-stack-keyboard-provider.tsx` | where KeyboardProvider goes in the root stack | step 4 |
| `examples/list-name-availability.ts` | an async availability check wired to a field and to submit | step 8 |
| `examples/server-field-errors.ts` | server `rejected` codes mapped to field keys with `setError` | step 8 |
| `examples/account-fields.ts` | name, email and new-password kinds chained for autofill | step 7 |
| `assets/component-library-entries.json` | the field components' entries for the component catalogue | step 5 |
| `assets/shared.json` | the files synced from the library's canonical copies | maintainers only |
| `scripts/check-forms.mjs` | the checker (17 rules) | steps 1 and 11 |
| `scripts/selftest.mjs` | proves the checker against `tests/fixtures/` | after changing the checker |
| `scripts/check-lib.mjs` | shared checker library (synced; do not edit) | never by hand |
| `scripts/lib/` | `source-scan.mjs`, the shared source lexer and JSX helpers (synced; do not edit) | never by hand |
| `tests/fixtures/` | planted-bug cases (one `bad-*` per rule), `pass-*`, `error-*` and `good/` | after changing the checker |
| `tests/bases/app/` | the small Tasks base the fixtures start from (with the templates) | after changing the checker |

## Related skills

- `ui-component-library` - the component catalogue the field components join; buttons and rows.
- `i18n-strings-and-catalogs` - catalogs, keys and translation of every label and message.
- `accessibility-as-code` - touch targets, contrast, Dynamic Type and screen-reader rules.
- `error-handling-typed-results` - `Result`, failures and never losing data on an error path.
- `async-safety` - the latest-request, delay and deadline helpers the async check builds on.
- `networking-and-server-state` - the `ApiClient`, mutations and `rejected` failures.
- `auth-and-secure-storage` - sign-in flows, passwords and tokens.
- `dates-streaks-and-statistics` - date fields holding a calendar day.
- `value-objects-money-and-units` - `normalizeDecimalInput`, money and quantity parsing for amount fields.
- `rtl-and-direction` - mixed-script text and logical alignment.
- `navigation-and-routing` - leaving a form with unsaved changes; the root stack order.
- `unit-and-component-tests` - render helpers, mocks and Jest setup.
