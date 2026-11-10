---
name: accessibility-as-code
description: Enforces a11y labels, 44pt targets, 200% text, VoiceOver, TalkBack. Use when adding a pressable, swipe or a11y label, text clips when large, contrast fails or Reduce Motion is missed. Not for RTL (rtl-and-direction).
---

# Accessibility as code

Every control is reachable and named for VoiceOver and TalkBack in every locale the app ships,
every target's own box is at least 44 pt, text grows to 200 % without clipping, every colour pair
the UI and its canvases paint is declared once and meets WCAG 2.2 AA in every colour set, motion
follows one live reduce-motion source, every swipe, drag or hold has a tap or a named action, custom
canvases speak a summary, and overlays keep both screen readers inside.
Scripts and tests prove what a machine can see; a human screen-reader pass covers the rest.

## Rules that must hold

1. **Give every interactive element a role and a translated name** (`t()`, as `accessibilityLabel`
   or `aria-label`; `aria-labelledby` alone names it on Android and the web only), a hint only when
   the outcome is not obvious (the result, never the gesture), and its state (`accessibilityState`
   or `aria-*`; React Native's `Pressable` and Touchables derive `disabled` themselves, Gesture
   Handler's do not). A pressable no screen reader should focus (a backdrop) is `accessible={false}`
   and its action exists elsewhere. Why: both screen readers read role, name and state, and
   `getByRole` finds exactly that.
2. **Make every touch target's own box at least 44 × 44 pt (`a11y.minTouchPt`, 48 for Material);
   never `hitSlop`.** Custom hit regions prove their smallest cell in a unit test. Why: `hitSlop`
   is invisible in layout, overlaps neighbours and does not move the screen reader's focus frame.
3. **Let text grow to at least 200 %:** never `allowFontScaling={false}`; any
   `maxFontSizeMultiplier` sits on the text primitive and is never below the cap (`a11y.maxFontScale`,
   default 2); `minHeight` instead of `height`; no `numberOfLines` on sentences; rows stack when
   `fontScale >= 1.25` (iOS XXXL and up, Android 1.3 and up: Android reports 1.3 as 1.2999999523).
   Why: WCAG 1.4.4, and a clipped or truncated label is unreadable.
4. **Declare every colour pair the UI paints in `contracts/contrast.json`, the app's one pair table
   (the theme palette and every other colour table: charts, tags; a Skia canvas surface keeps its
   pairs in its own `canvas-contrast.json`), and meet WCAG 2.2 AA in every colour set:** text 4.5:1,
   icons, edges, focus and chart lines 3:1, a filled shape 3:1 off its edge or its ground;
   translucent colours composited first. Why: a palette never says which colour sits on which, and
   design-system-structure's palette tools read the same table, so it is kept once.
5. **Never convey meaning by colour alone.** Every state carries an icon, shape or word, and
   colours that alone tell categories apart (`distinct` lists: chart series, tags) stay 0.07 apart
   in OKLab under protanopia, deuteranopia and tritanopia. Why: about 1 in 12 men cannot tell
   red from green, and status colours collide (0.013 apart under deuteranopia).
6. **Reduce motion only through `useReduceMotion()` and `<MotionConfig>`**; never Reanimated's
   `useReducedMotion()` or `AccessibilityInfo` outside `systemA11yStore`; every moment that moves
   has a reduced alternative; functional timers pass `ReduceMotion.Never`. Why: Reanimated's hook
   is a module-load constant that misses live changes and the in-app setting.
7. **Expose each information-bearing canvas as one image** labelled with `t()` of a pure
   `describe(state)`, or mark it decorative; **announce events with `useAnnounce()`** (one short
   sentence per action, only while a screen reader runs, queued so a screen change cannot cut it
   off; a live region for status text on Android). Why: Skia content is invisible to screen
   readers, and stray announcements talk over the user.
8. **Keep overlays (dialogs, sheets, menus, popovers, drawers) modal on both platforms and reading
   order visual:** Expo Router modal routes or RN `<Modal>` first; an in-tree overlay sets
   `accessibilityViewIsModal` on its root (the scrim, never the card; `aria-modal` works only on
   `Pressable` and TouchableOpacity/Highlight/NativeFeedback, and on the web) and hides what is
   behind it on Android (`aria-hidden` on the screen's side, not inside the layer) in the same
   component; an in-tree overlay host wraps the navigator, so the header and tab bar are hidden too.
   Never nest a pressable in another: a card's opener and action are siblings, and the text layer
   drawn above the opener has `pointerEvents: 'none'`, both in one shared `src/ui/` card component
   (only `src/ui/` may import `Pressable`). Sliders are adjustable with declared
   actions; other-language text sets `accessibilityLanguage`. Why: otherwise focus wanders behind
   dialogs, inner actions are unreachable, taps on a card's text do nothing and sliders cannot move.
9. **Give every gesture-only action (long press, swipe, drag, pinch) one tap or a named action:**
   `accessibilityActions` with translated labels and `onAccessibilityAction` on the focused element
   (the VoiceOver Actions rotor, the TalkBack actions menu), plus a single-pointer way for drags. An
   essential gesture is a reviewed `a11yGestureExceptions` entry, never a dummy action. Why: both
   screen readers take over swipes to move focus (WCAG 2.5.1, 2.5.7).
10. **Query by role and name in tests, and end every screen test with the
    `findInaccessiblePressables` audit.** Why: a missing role or name then fails a test, not a user.
11. **Run a human VoiceOver and TalkBack pass on every release candidate**, in one left-to-right
    and (when shipped) one right-to-left locale; ask for it, never claim it, and turn every reported
    problem into a failing test first. Why: no checker can hear whether the spoken output makes sense.
12. **Never weaken a pair, a gate or a check to go green.** An accepted failure is a contract
    exception with a `reason` and `approvedBy`, added only after the developer agrees, and printed
    on every run. Why: a silenced contrast failure ships unreadable text.

## Workflow

1. **First time.** Copy `templates/src/ui/a11y/` to `src/ui/a11y/` and `templates/test/a11y/` to
   `test/a11y/`. Start the store once in the root layout (`src/app/_layout.tsx`):
   `useEffect(() => watchSystemA11y(reportError), [])`, and wrap the app in
   `<MotionConfig preference={reduceMotionPreference}>` (`"system"` when the app has no setting;
   settings-and-preferences owns a saved one); render everything that reads `useReduceMotion()`
   below it. motion-and-animation's `check-motion` proves this wiring (`reduce-motion-root`).
   Make sure `quality-gates.json` has the `a11y` block (`minTouchPt` 44, `maxFontScale` 2,
   `textContrastMin` 4.5, `nonTextContrastMin` 3, `minCvdDistanceOk` 0.07; quality-gates owns
   the file).
2. **Contrast contract.** Copy `templates/contracts/contrast.json` and its schema to `contracts/`.
   Its `app` entry describes design-system-structure's palette (`src/theme/palette.ts`, synced here
   with `contrast.ts` and `theme-types.ts`; copy those three only when the app has none), and that
   skill's `write-palette` and `check-design-system` read the same entry. Add a pair whenever a
   component puts a colour on a new ground (a label over a growing fill needs one per ground), and a
   palette entry for every other colour table (charts, tags). Read
   [references/contrast-and-colour.md](references/contrast-and-colour.md).
3. **Building or changing a component or screen.** Read
   [references/roles-names-and-screen-readers.md](references/roles-names-and-screen-readers.md)
   and imitate [examples/accessible-task-row.md](examples/accessible-task-row.md): shared `src/ui/`
   controls, names from `t()` in the model hook, the right role and state, a 44 pt box, headers via
   the text primitive, a card's opener and action as siblings with the text layer passing touches
   through (opener and text layer in one `src/ui/` card the feature composes), every swipe or drag
   action also a named accessibility action on a shared row, overlays modal on both platforms.
4. **Large text and motion.** Read
   [references/text-scaling-and-motion.md](references/text-scaling-and-motion.md): stack at large
   text, `minHeight` everywhere, taller line heights for scripts with tall glyphs, and the reduced
   alternative of each moving moment.
5. **Custom canvases and announcements.** Label each canvas from a pure `describe(state)` through
   `t()` and unit-test `describe()`; announce results with `useAnnounce()`, once per action.
6. **Tests.** Read [references/testing-accessibility.md](references/testing-accessibility.md).
   Query by role and name, assert state, end every screen test with the audit line, and keep
   `test/a11y/app-contrast.test.ts` green.
7. **Run the checks** from the repo root, fix every `FAIL` line (each names the file, the rule and
   the fix) and rerun until both print `RESULT: PASS`:
   - `node ${CLAUDE_SKILL_DIR}/scripts/check-a11y-code.mjs .`
   - `node ${CLAUDE_SKILL_DIR}/scripts/check-contrast.mjs .`
   A contrast failure is fixed in the colours or taken to the developer (rule 12), never silenced.
8. **Large text on devices.** Copy `templates/.maestro/flows/a11y/01-large-text-core-screens.yaml`
   to `.maestro/flows/a11y/`, replace its testIDs with the app's, and run it at the largest size on a
   named iOS simulator and a named Android emulator (e2e-maestro's runner does it per locale; the
   commands by hand are in the testing reference). Read every
   screenshot for clipping, overlap and rows that should have stacked; reset the size afterwards.
9. **Before a release (human step).** Ask the developer to run the screen-reader checklist in the
   testing reference on the release candidate, on both platforms; turn every reported problem into
   a failing test first.

## Definition of done

- [ ] Every pressable has a role, a translated name, its state, and an own box of at least the
      minimum without `hitSlop`; labels and hints come from `t()` with ICU plurals.
- [ ] Text scales to at least 200 %: no `allowFontScaling={false}`, no lower cap, no fixed heights
      around text, rows stack at large text; the large-text flow's screenshots on iOS and Android
      show nothing clipped.
- [ ] Reduce motion goes through `useReduceMotion()` / `<MotionConfig>`; each moving moment has its
      reduced alternative; canvases are one labelled image or decorative; announcements use
      `useAnnounce()`; overlays are modal on both platforms; no nested pressables, and card text
      layers pass touches to their opener.
- [ ] Every long press, swipe, drag and pinch action is also a named accessibility action (and a
      single-pointer control for drags); any essential gesture is a reviewed exception.
- [ ] `contracts/contrast.json` declares every pair the UI paints, for the theme palette and every
      other colour table, and each canvas surface has its `canvas-contrast.json`;
      `test/a11y/app-contrast.test.ts` and the `src/ui/a11y/` tests pass; every screen test ends
      with the audit line.
- [ ] No contract exception without a reason and an approver; no gate below its floor.
- [ ] The developer has been asked for the release-candidate VoiceOver and TalkBack pass.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-a11y-code.mjs .` prints `RESULT: PASS`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-contrast.mjs .` prints `RESULT: PASS` (the one SKIP it
      may print while the app has no gates file: `SKIP quality-gates.json [a11y-gates] not yet
      created (quality-gates creates it)`).

## Anti-patterns

- **A raw `Pressable` in a screen with a hard-coded English label.** Use the shared `src/ui/`
  controls and pass `t('…')` from the model hook.
- **`hitSlop={10}` on a 24 pt icon.** Make the button's own box 44 pt and centre the glyph.
- **Turning text scaling off, or capping it at 1.3, because a layout breaks at 200 %.** Stack the
  row, use `minHeight`, let it wrap.
- **Adding a contract exception, lowering a gate or deleting a pair to make the check pass.**
  Change the colour (keep the hue, move the lightness), or stop and ask the developer.
- **Red and green status dots with no icon or word.** Give every state a shape cue; make only
  colour-only categories a `distinct` list and pick them from Okabe-Ito.
- **`useReducedMotion()` from Reanimated, or reading `AccessibilityInfo` in a screen.** It misses
  live changes and the setting; use `useReduceMotion()` and the store.
- **A second reduce-motion hook for screenshot runs.** Pass `preference="on"` to `<MotionConfig>`
  from the test-only setup instead.
- **`announceForAccessibility` on every tap or frame.** One short announcement per action, only
  while a screen reader runs; a live region for status text on Android.
- **An action nested inside a card's `Pressable`.** The screen reader reads the outer element and
  never reaches the action; make the opener and the action siblings.
- **A card's text layer drawn above its opener without `pointerEvents: 'none'`.** The topmost view
  takes the touch, so tapping the title does nothing on a device while every RNTL test passes. Keep
  the opener and its text layer in one `src/ui/` card, never a shared opener with the layer in each
  feature.
- **Swipe-to-delete or drag-to-reorder with no `accessibilityActions`.** Screen-reader swipes move
  focus, so the action is unreachable; add named actions on the row's opener.
- **`accessibilityViewIsModal` alone on an in-tree overlay, or on the card inside the scrim.**
  TalkBack still reaches the screen behind, and a modal card hides the scrim's testID; put the flag
  on the scrim and hide the content behind with `aria-hidden`, or use RN `Modal`.
- **`aria-modal` alone on a `View`.** React Native 0.86.3 drops it there (only `Pressable` and
  TouchableOpacity/Highlight/NativeFeedback map it), so VoiceOver leaves the sheet; add
  `accessibilityViewIsModal`. react-native-web honours `aria-modal` and `aria-labelledby` on a View,
  so a web-enabled app keeps `aria-modal` next to the iOS flag (web-support).
- **`aria-hidden` on a grip or icon inside the sheet as the "Android half".** It hides nothing
  behind the layer; hide the sibling that holds the screen (`aria-hidden={isOpen}`).
- **`disabled` alone on a Gesture Handler `Pressable` or `enabled` on a `RectButton`.** Gesture
  Handler turns the gesture off but never reports it, so VoiceOver reads an active button; add
  `accessibilityState={{ disabled }}` (React Native's own `Pressable` derives it).
- **A second pair table (a test-local list, a copy in a design tool export).** Two tables drift;
  add the pair to `contracts/contrast.json`, which this skill and design-system-structure both read.
- **Labelling every icon inside a row.** Give the row one name; decorative parts stay silent.
- **Reporting "VoiceOver works" without the human pass.** Automated checks cannot hear the output.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/roles-names-and-screen-readers.md](references/roles-names-and-screen-readers.md) | Pressable checklist, roles and states per element, names and plurals, 44 pt targets, sliders and holds, card opener plus sibling action, canvases, announcements and live regions, overlays on iOS and Android, languages, a platform table | Workflow steps 3 and 5 |
| [references/contrast-and-colour.md](references/contrast-and-colour.md) | WCAG maths, the contract keys, filled shapes and translucent colours, never colour alone, the colour-blind check and its calibration, exceptions, focus and Increase Contrast, the Jest twin | Workflow step 2 |
| [references/text-scaling-and-motion.md](references/text-scaling-and-motion.md) | iOS fontScale table, Android font scale and its non-linear curve, the cap, large-text layout, tall glyphs, one reduce-motion source, moments and their reduced alternatives, spring mass | Workflow step 4 |
| [references/testing-accessibility.md](references/testing-accessibility.md) | RNTL role queries and the audit, the tests to keep, large text with Maestro on a named simulator and emulator, inspector tools, the VoiceOver and TalkBack release checklist, report to test | Workflow steps 6, 8 and 9 |
| [examples/accessible-task-row.md](examples/accessible-task-row.md) | A task row: plural labels from `t()`, a shared `src/ui/` `ActionCard` (opener, text layer, action slot) the feature's row composes, shape cues, the audited test | Workflow step 3 |
| `templates/src/ui/a11y/` | `system-a11y-store.ts` (reduce motion, screen reader, Bold Text), `use-reduce-motion.ts`, `motion-config.tsx`, `use-announce.ts` (queued), each with its test; owned here and synced from the library (edit the canonical copy, never this one) | Workflow step 1; copy to `src/ui/a11y/` |
| `templates/src/theme/` | `contrast.ts`, `palette.ts`, `theme-types.ts` from design-system-structure (synced; do not edit here): the WCAG maths and the palette the contract template describes | Workflow step 2; copy only when the app has none |
| `templates/test/a11y/` | `find-inaccessible-pressables.ts` (+ test), `cvd.ts`, `contrast-contract.ts` (+ test), `app-contrast.test.ts` (the Jest twin of check-contrast) | Workflow step 1; copy to `test/a11y/` |
| `templates/contracts/contrast.json` | The contrast contract: the app's one pair table, starting with the canonical palette's pairs; owned here and synced from the library (design-system-structure reads the same file) | Workflow step 2; copy to `contracts/` |
| `templates/contracts/contrast.schema.json` | Its JSON schema (every key explained; synced with the contract) | With the contract |
| `templates/.maestro/flows/a11y/01-large-text-core-screens.yaml` | Maestro flow for core screens at the largest text size, with screenshots | Workflow step 8; copy to `.maestro/flows/a11y/` |
| `scripts/check-a11y-code.mjs` | Checks 20 code rules over `src/` (every workspace `src/` too; route files are not judged as overlays; `--src`, `--routes-dir`, `--min-touch`, `--font-cap`, `--screen-test`; reads `srcDir`, `routesDir` and `a11yGestureExceptions` from `rn-skills.config.json`) | Workflow step 7 |
| `scripts/check-contrast.mjs` | Checks the contract (unknown keys refused), that the theme palette and every colour table under `src/` are declared, every declared pair in every set, every canvas surface's `canvas-contrast.json` in every palette set, `distinct` lists, `--categorical` lists and the a11y gates (`--contract`, repo-relative; reads `contrastContract` and `canvasSurfaceDirs` from `rn-skills.config.json` and `paletteSets`/`surfaces` from `contracts/canvas-surfaces.json`) | Workflow steps 2 and 7 |
| `scripts/lib/wcag.mjs` | Contrast, compositing and colour-blind maths | Read only when changing a rule |
| `scripts/lib/load-ts-constants.mjs` | Loads a data-only TypeScript palette without packages | Read only when changing the checker |
| `scripts/lib/source-scan.mjs` | JSX, call and import scanning helpers (synced from the library; do not edit here) | Never by hand |
| `scripts/lib/object-literal.mjs` | Object-literal reader for style objects (synced from the library; do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared script helper (synced from the library; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both checkers pass the templates plus a neutral app and catch each planted bug | After changing a script, template or fixture |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/` | `bases/` (a neutral Tasks app with planted findings under `skills/`, `.agents/skills/` and a vendored `SKILL.md` folder that must stay silent; a chart palette and a canvas surface) and `fixtures/` (one overlay suite per checker) | When adding a rule |

## Related skills

- `design-system-structure` - the palette, tokens, text primitive and `contrast.ts`; its palette tools read this contract.
- `ui-component-library` - the buttons, rows, checkboxes and dialogs these rules apply to.
- `forms-and-input` - text input names (`input-label`) and font scaling in `TextField`.
- `i18n-strings-and-catalogs` - catalog keys and ICU plurals behind every label and hint.
- `rtl-and-direction` - reading order and layout in right-to-left locales.
- `motion-and-animation` - the moment catalog, timings and reduced alternatives, loops, native stack and CSS transitions, and the check that the root mounts `<MotionConfig>` and starts the store.
- `settings-and-preferences` - the saved "Reduce motion" preference passed to `MotionConfig`.
- `skia-canvas-rendering` - canvases, their `describe()` summary and reduced timelines.
- `canvas-gestures-and-hit-testing` - hit regions and their 44 pt test.
- `unit-and-component-tests` - `renderWithProviders` and the Jest setup.
- `e2e-maestro` - the runner for the large-text flow on named devices.
- `design-review-workflow` - the end-of-build sweep across text sizes, themes and directions.
- `quality-gates` - `quality-gates.json` and its a11y budgets.
