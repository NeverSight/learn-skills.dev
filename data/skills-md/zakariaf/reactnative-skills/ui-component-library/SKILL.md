---
name: ui-component-library
description: "Builds shared src/ui components (buttons, rows, dialogs, toasts, cards): token sizes, every state, a required testID, a test each. Use when adding or changing a shared component. Not for tokens (design-system-structure)."
---

# UI component library

Gives an Expo app one shared component library in `src/ui/`: forty presentational components
listed in a repo-owned catalogue (`contracts/component-library.json`), each sized from specs
generated from the token file, pressed through the one press surface, showing every state with a
cue beyond colour, named for VoiceOver and TalkBack, addressed by a required testID whose parts it
derives itself, and proven by its own test. Two zero-dependency scripts prove the catalogue, the
specs and the component rules, including the device lessons for iOS and Android.

## Rules that must hold

1. **The catalogue lists every shared component, with its parts and the looks it may have.** Each
   `src/ui` component is an entry (`component-missing`, `component-unlisted`) and exports
   `function <Name>` and `type <Name>Props` (`component-export`). Why: a checker can only hold what
   it knows, and a flag (`mayShadow`, `mayRotate` ...) allows a look exactly where it is meant.
2. **Measurements come from the generated specs, never a typed number.** The token file's
   `components` block is the source; `write-component-specs.mjs` writes `component-specs.json` and
   components read `COMPONENT_SPECS` (`specs-missing`, `specs-mismatch`, `measurement-literal`); an
   override carries its reason (`spec-override-reason`). Why: a retyped value drifts by one digit and
   nobody notices until a screen looks wrong.
3. **One press implementation.** Every pressable composes design-system-structure's
   `PressableSurface`; no `Pressable`, Touchable, core `Button` or gesture-handler button anywhere
   else (`press-outside-host`; a provider-free crash fallback states why in a
   `// press-outside-host: <reason>` comment), no hand-written pressed look (`own-press-look`), and
   each press host runs the injected feedback, except a switch, whose handler plays its own
   (`press-feedback`). Why:
   every control then answers, sounds and announces the same way, and the look is one token.
4. **Every component a test or flow addresses takes a required `testID`, derives its parts from it,
   and puts it on the box the design measures** (`testid-required`, `part-not-derived`,
   `testid-on-inner-text`; the grammar is naming-conventions'). Why: screens never build part ids by
   hand, and on iOS a testID inside an accessible element vanishes from the tree E2E tools read.
5. **Every pressable has a role, a translated name and its state; decorative parts hide themselves**
   from VoiceOver and TalkBack with both props (`decorative-not-hidden`). Why: a screen reader then
   reads one element ("Daily reminder, switch, on"), not a list of pieces. Touch targets and
   `hitSlop` are accessibility-as-code's rules.
6. **Components are presentational.** Props in, JSX out: no translation API (`ui-translates`), no
   stores or services (architecture-and-boundaries), strings arrive translated, numbers formatted,
   `isReducedMotion` from the screen model (motion-and-animation's hooks, once adopted, read it
   themselves), icons through an `IconSlot`. Why: a component stays
   testable without the app and works in every language and icon set.
7. **Shape before colour, and a test holds each cue.** Every state keeps a non-colour cue: a check, a
   written state, a wider dot, a bold edge, a dash. Each cue has a component test that fails when
   the cue is removed (a derived part such as `.check`, or `toHaveStyle` for a width or an edge).
   Why: about 1 in 12 men cannot tell the status colours apart, and an untested cue disappears in
   the next restyle while a colour-only assertion stays green.
8. **Flat by default.** Shadows and rotation only on components the catalogue marks
   (`shadow-outside-allowed`, `rotate-outside-allowed`). Why: a shadow says "floats" or "press me";
   on a card it promises an action that is not there.
9. **Motion has a reduced alternative, and a functional timer ignores reduce motion.** Fades instead
   of drops, nothing instead of confetti; the hold timer passes `ReduceMotion.Never`
   (`hold-reduce-motion`). Why: under Reduce Motion Reanimated finishes a timing at once, and the hold
   would confirm on touch.
10. **Faces grow with their text, and cells grow without a zero basis** (`fixed-text-height`,
    `pair-cell-flex`). Why: a fixed height clips at 200 % text, and `flex: 1` in a column cell
    collapsed a row of keys to 0 pt on a device while every Jest test passed.
11. **The scrim is the modal root: it renders in React Native's Modal, carries
    `accessibilityViewIsModal`, and closes on Android back** (`modal-root`, `modal-back`). Why: a modal
    card hid the scrim's testID from the tree, and a dialog that ignores back traps Android users.
12. **The device lessons hold:** underlines are drawn bars (`drawn-underline`), a hold fill sits in a
    track pinned to the face edges (`hold-fill-track`), a scatter lays out left to right
    (`scatter-ltr`). Why: no platform sets an underline's thickness, Yoga takes an absolute child's
    percentage inside the padding, and `start` offsets mirror in right-to-left.
13. **Every component has a test** rendered through `renderWithProviders`, asserting role, name,
    state and parts, ending with the `findInaccessiblePressables` audit (`component-untested`). Why:
    a missing role or a renamed part then fails a test, not a person or a flow.
14. **Never build a design's stand-ins** (an ad box, an OS consent sheet) listed under `mockOnly`
    (`mock-only-built`). Why: a stand-in ships as a fake.

## Workflow

1. **Look first.** From the repo root run `node ${CLAUDE_SKILL_DIR}/scripts/check-components.mjs .`.
   NOT APPLICABLE means no library yet; `catalogue-missing` lists the app's existing `src/ui`
   components and the file rules they break: that is the work list. Read
   [references/component-catalogue.md](references/component-catalogue.md).
2. **Prerequisites.** The theme, AppText, PressableSurface and the press feedback context come from
   design-system-structure; `test/render-with-providers.tsx` from unit-and-component-tests;
   `test/a11y/find-inaccessible-pressables.ts` from accessibility-as-code. `prerequisite-missing`
   names any that is missing and who creates it.
3. **Measurements.** Merge the `components` block of `assets/components-block.json` into
   `design/tokens.json` (the canonical demo token file may already carry the same block) and replace
   the values with the design's
   ([references/measurements-and-specs.md](references/measurements-and-specs.md)); then run
   `node ${CLAUDE_SKILL_DIR}/scripts/write-component-specs.mjs .`.
4. **Copy the library.** From `templates/` to the same paths: `contracts/component-library.json`
   (and its schema), `src/ui/component-specs.ts`, `icon-slot.ts`, `variant-paint.ts`,
   `use-hold-to-confirm.ts`, and each component the app needs with its test (a component's own
   imports name the others it needs). Remove catalogue entries the app does not adopt. Keep the
   values; adapt only what the app's design changes, reading
   [references/actions-and-inputs.md](references/actions-and-inputs.md) or
   [references/lists-surfaces-and-overlays.md](references/lists-surfaces-and-overlays.md) first.
   When the design asks for platform-native controls instead, hand off to Expo's `expo-ui` skill.
5. **Moments.** When the app has motion-and-animation's moment catalogue, declare the Toggle,
   Toast and hold moments with those files in `files`, swap BusyIndicator for
   [examples/busy-indicator-with-moments.tsx](examples/busy-indicator-with-moments.tsx) and drop
   Confetti for `<CelebrationBurst>` (building-a-component.md, "With motion-and-animation's moment
   catalogue"); then its `check-motion.mjs` passes on `src/ui/`.
6. **Contrast.** Each colour on a new ground is a pair in `contracts/contrast.json`
   (accessibility-as-code). Beyond the canonical palette pairs, the templates paint `primary` on
   `sunken` (the progress and slider fills): add it under `shapes`, then run accessibility-as-code's
   `check-contrast.mjs`.
7. **Wire into screens.** The screen model builds strings with `t()`, formats numbers, reads
   reduce motion and passes base ids; imitate [examples/reminder-settings.tsx](examples/reminder-settings.tsx)
   and its test. testIDs and roles: [references/testids-and-accessibility.md](references/testids-and-accessibility.md).
8. **A new component** follows [references/building-a-component.md](references/building-a-component.md):
   one file, specs, semantic paint, AppText, the press surface, a required testID with derived parts,
   a test, a catalogue entry with its flags, its measurements in the token file. The device traps:
   [references/layout-and-platform-lessons.md](references/layout-and-platform-lessons.md).
9. **Older primitives** (a `PrimaryButton` on a raw Pressable): move each caller to the library
   component, then delete the old file and say so in the report (building-a-component.md,
   "Replacing older primitives").
10. **Run the checks from the repo root** until all pass: `npm run typecheck`,
   `npx eslint . --max-warnings 0`, `npx jest --ci`, then the two scripts below (use `--only <Name>`
   while building a subset, never at the end). Every FAIL line names the file, the rule and the fix;
   [references/catalogue-contract-and-checks.md](references/catalogue-contract-and-checks.md)
   explains each rule and every catalogue key.
11. **Report** in plain words which components were added or changed, which checks passed, any
    override and its reason, files deleted, and the open questions touched
    ([references/defaults-and-open-questions.md](references/defaults-and-open-questions.md)). Ask the
    reviewer before changing a value the design fixed.

## Definition of done

- [ ] `contracts/component-library.json` lists every `src/ui` component with its parts and flags,
      and nothing the app does not have.
- [ ] The token file has the design's `components` block; overrides (if any) each give a reason.
- [ ] Each component composes the press surface (no other press, no own pressed look), takes a
      required testID and derives its parts, hides its decorative parts, reads every size from
      `COMPONENT_SPECS` or a token, and has a test that ends with the pressable audit.
- [ ] Every non-colour state cue has a test that fails without it: removed once, the test went red,
      then the cue was put back.
- [ ] The pairs the components paint are in `contracts/contrast.json` and pass.
- [ ] `npm run typecheck`, `npx eslint . --max-warnings 0` and `npx jest --ci` pass (iOS and Android
      projects).
- [ ] No SKIP lines are expected; NOT APPLICABLE only while the app has no library yet.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/write-component-specs.mjs . --check` prints `RESULT: PASS`
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-components.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **A quick `TouchableOpacity` or a `({ pressed }) => ({ opacity })` style.** Compose the press
  surface or use Button, ListRow, IconButton; change the look in `PRESS`, once.
- **A shadow on a card to make it look important.** It promises a press; put a button in the card or
  use ActionCard.
- **A part id built in the screen** (`'tasks.add-button' + '.label'`) **or an index key**
  (`${testID}.${index}`). Pass the base id; key repeated items by data.
- **`t()` or a store inside `src/ui`.** The screen model builds the strings and reads the stores.
- **Editing `component-specs.json` to make a layout fit.** Fix the layout; change a measurement in the
  token file, or add an override with the design's reason.
- **A testID on the text inside a chip, badge or header.** E2E tools then measure only the words; put
  it on the View with `accessible`, role and label.
- **`flex: 1` on a tile in a grid cell.** A zero vertical basis; use `{ flexGrow: 1 }`.
- **Centring a badge with the parent's `alignItems`.** Its own `alignSelf` wins; wrap it in a row with
  `justifyContent: 'center'`.
- **`accessibilityViewIsModal` on the dialog card**, or a dialog drawn in the tree with no back
  handling. Use the Scrim: Modal, the flag on the scrim, `onRequestClose`.
- **`textDecorationLine` for a designed underline.** Draw the bar.
- **A percentage width on an absolute child of a padded face.** Put it in a track pinned to the edges.
- **Confetti placed with `start: x` and no `direction: 'ltr'`.** It mirrors in Arabic or Hebrew.
- **A fixed `height` on a face that holds text.** Use `minHeight`.
- **A hold-to-confirm that finishes under Reduce Motion, or that only a finger can do.** Pass
  `ReduceMotion.Never`; offer the activate action.
- **Labelling every icon inside a row, or un-hiding a decorative part to measure it.** The row carries
  the name; give the measured element the id.
- **Calling the sound or haptic API from a component or screen for a press.** The press host already
  plays the tap, so a second call doubles it; a switch's handler plays its own toggle feedback, and
  what plays is audio-and-haptics-feedback's choice.
- **Building the design's ad box or consent sheet.** The SDK and the OS draw the real ones.
- **Treating a green checker as proof a screen looks right.** It proves structure and rules; looks
  are proven on device screenshots (design-visual-parity).

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/component-catalogue.md](references/component-catalogue.md) | The forty components (file, role, parts, flags), support files, prerequisites, other owners, mock-only parts, games, when multi-package | Workflow step 1, every time |
| [references/actions-and-inputs.md](references/actions-and-inputs.md) | The press model; buttons, hold, tiles, cards, checkbox, toggle, segmented control, slider, option card, progress bar: anatomy, states, accessibility | Changing or wiring a pressable or an input |
| [references/lists-surfaces-and-overlays.md](references/lists-surfaces-and-overlays.md) | Lists and rows, tiles, cards, callouts, badges, chips, app bar, scrim and dialogs, toasts, empty state, stats and charts, drawn marks, confetti | Changing or wiring a flat part or an overlay |
| [references/building-a-component.md](references/building-a-component.md) | File anatomy, specs and paint, the icon slot, composing the press surface, motion, the test, lint limits, the catalogue entry, replacing older primitives, the moment catalogue table | A new component; workflow steps 5, 8 and 9 |
| [references/measurements-and-specs.md](references/measurements-and-specs.md) | The components block, references, the generator, reasoned overrides, browser-rendered borders, turning specs off | Workflow step 3; any measurement question |
| [references/testids-and-accessibility.md](references/testids-and-accessibility.md) | Required testIDs and derived parts per component, ids on measured boxes, what E2E tools see on iOS and Android, decorative parts, roles, the pressable checklist | Wiring screens, writing tests |
| [references/layout-and-platform-lessons.md](references/layout-and-platform-lessons.md) | The device traps behind the layout rules, on iOS and Android: pair cells, alignContent, alignSelf, absolute percentages, underlines, scatters, fixed heights, the modal root and back, directions, press looks | Before changing layout code |
| [references/catalogue-contract-and-checks.md](references/catalogue-contract-and-checks.md) | Every catalogue key and flag, options and rn-skills.config.json keys, every rule with its fix, passing output, adopting in an existing app | Editing the catalogue; reading a FAIL line |
| [references/defaults-and-open-questions.md](references/defaults-and-open-questions.md) | Defaults the templates choose and why, states to decide, what to verify on devices | Reporting; before changing a default |
| `templates/src/ui/` | The forty components, each with its test (`scrim.android.test.tsx` for Android back); `component-specs.json` and `.ts`; `icon-slot.ts`; `variant-paint.ts` and `use-hold-to-confirm.ts` with their tests | Workflow step 4 (copy) |
| `templates/contracts/` | `component-library.json` (the catalogue) and `component-library.schema.json` | Workflow step 4 (copy, then edit) |
| [examples/reminder-settings.tsx](examples/reminder-settings.tsx) | A feature's settings group built from ListGroup, ListRow, SubRow and Slider with base ids and props from the model | Workflow step 7 |
| [examples/reminder-settings.test.tsx](examples/reminder-settings.test.tsx) | Its test: switch, adjustable, hidden row, audit | Workflow step 7 |
| [examples/busy-indicator-with-moments.tsx](examples/busy-indicator-with-moments.tsx) | BusyIndicator looping through motion-and-animation's `useMotionLoop` (same props; the template's test passes on it) | Workflow step 5, when the app has the moment catalogue |
| `assets/components-block.json` | The demo component tier the templates were built from | Workflow step 3 (merge into the token file) |
| `assets/shared.json` | Declares the synced files: check-lib, the source scanner, the canonical demo token file the fixtures use | When adding a shared file |
| `scripts/check-components.mjs` | Checker: catalogue, prerequisites, specs, files, exports, testIDs and parts, tests, one press implementation, the component and device rules | Workflow steps 1 and 10, and at the end |
| `scripts/write-component-specs.mjs` | Generator: `component-specs.json` from the token file (`--check` compares and names the first difference and why) | Workflow step 3, and at the end |
| `scripts/lib/component-source.mjs` | Catalogue loading and validation, the spec derivation, StyleSheet and JSX scanners | When a rule needs changing |
| `scripts/lib/source-scan.mjs` | Shared import scanner and resolver (synced, do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared script helper (synced, do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both scripts on the shipped templates and every planted bug | After changing a script, a template or a fixture |
| `tests/` | The base app (prerequisite stubs, the synced token file) and overlay cases: good, one bad case per rule, pass and error cases | When adding a rule |

## Related skills

- `design-system-structure` - tokens, themes, AppText, PressableSurface and the press look these components build on.
- `accessibility-as-code` - touch targets, hitSlop, contrast pairs, reduce motion, overlays and screen-reader checks app-wide.
- `naming-conventions` - the testID grammar, file and export names.
- `unit-and-component-tests` - renderWithProviders, test forms and the Jest set-up.
- `react-components-and-hooks` - component and hook rules, effects, lists.
- `architecture-and-boundaries` - why `src/ui` imports no stores or services.
- `icons-app-icon-and-splash` - the icon set the icon slots draw from.
- `forms-and-input` - text fields and form controls, which join this catalogue.
- `ui-states-and-feedback` - when to show an empty state, a toast, a banner or a dialog.
- `screen-contracts` - screens composed from these components and their ids.
- `design-visual-parity` - proves a built screen matches its approved design.
- `motion-and-animation` - the app's moment catalogue and celebrations.
- `audio-and-haptics-feedback` - what the press feedback plays.
- `rtl-and-direction` - direction switching, mirroring and bidi.
- `e2e-maestro` - flows that select these testIDs on iOS and Android.
- `game-session-host` - game parts (level tiles, star ratings, a game's top bar) built to the same rules.
- Expo's `expo-ui` skill - platform-native SwiftUI and Jetpack Compose controls (@expo/ui).
