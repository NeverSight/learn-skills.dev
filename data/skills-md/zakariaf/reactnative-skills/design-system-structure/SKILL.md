---
name: design-system-structure
description: "Structures a design system: two-tier tokens, contrast-proven light/dark palettes, the theme provider, makeStyles, text roles, fonts. Use when touching colours, dark mode, fonts or theme files. Not for components (ui-component-library)."
---

# Design system structure

Makes every visual value in an Expo app come from one token file through one typed theme: semantic
colour roles in light and dark palettes that are proven readable pair by pair, `makeStyles` and one
`AppText` with type roles on the device pixel grid at every text size, the system font (bundled,
pinned fonts as an opt-in), motion tokens with complete springs, and one press surface whose look is
a token choice. Two checkers prove the theme equals the token file, the navigator and the root view
follow it, and that no raw colour, size, weight, radius, duration, spring, palette import, platform
shadow or second theme hides in the app's code.

## Rules that must hold

1. **The token file is the only source; theme modules copy it.** `design/tokens.json` holds primitives
   (tier 1) and semantic roles (tier 2); `tokens.ts`, `type-styles.ts`, `motion.ts` and `palette.ts`
   copy it, and every mapped export is compared value by value (`theme-mismatch`). A retyped value
   drifts by one digit and nobody notices until a screen looks wrong.
2. **Components read semantic roles only, through the theme.** Colours come from
   `theme.colors.<role>` through `makeStyles` or `useTheme`; no colour literal (hex, `rgb()`, `hsl()`,
   or a named colour such as `color="white"` on a colour prop) or raw radius lives outside `src/theme`
   (`no-color-literal`, `no-raw-radius`), no palette module, token file or `APP_THEMES` is imported
   there (`no-palette-import`), and no second theme (the create-expo-app `constants/theme.ts`, another
   `useTheme`) sits beside it (`second-theme-system`). A colour read any other way is frozen to one
   scheme: it breaks dark mode and every palette flavour at once.
3. **Every palette is generated and proven readable, pair by pair.** `write-palette.mjs` writes
   `palette.ts` only when every pair passes (text 4.5:1; edges, focus and icons 3:1; filled shapes
   3:1 off their ground or edge), with translucent colours painted over their ground first. The
   pairs are the app's `contracts/contrast.json` (accessibility-as-code owns that contract and the
   rule to declare every pair there), or the default pairs until it exists; the core pairs are
   checked whatever the contract says (no exception accepts one), and `palette.test.ts` keeps them
   in Jest. Contrast belongs to pairs, so it is tested as pairs, from one table.
4. **Light and dark are two hand-tuned sets that follow the person on iOS and Android, everywhere.**
   `AppThemeProvider` resolves the saved preference against the phone, mirrors it to `Appearance`
   and paints the root view (`SystemUI.setBackgroundColorAsync`); `NavigationThemeProvider` sits
   inside it and hands the navigator colours mapped from the theme (`navigation-theme-mapped`: never
   a bare `DarkTheme`/`DefaultTheme`); the app config says `userInterfaceStyle: 'automatic'` with no
   `ios` or `android` override saying otherwise, and `expo-system-ui` is installed; a runtime file
   (the routes layout, or `App.tsx` with React Navigation) renders the provider imported from
   `src/theme/theme-provider` (`color-scheme-config`, `theme-provider-behaviour`,
   `theme-provider-mounted`). Miss one and iOS reports light forever, Android ignores the setting,
   or headers and screen backgrounds stay light in dark mode.
5. **A makeStyles factory builds with StyleSheet.create and returns it.** Styles are cached per
   theme object (`make-styles-factory`). That keeps tsc's excess-property check and the style lint
   rules; a plain object loses both.
6. **Text renders only through AppText with a type role or style.** No raw `fontSize` or
   `letterSpacing`, inline or as a branch of a conditional (`no-raw-font-size`, `no-letter-spacing`);
   the templates use the system font (`null` in `SCRIPT_FONTS`, weight by `fontWeight`); a bundled
   family is one face per weight, so never `fontWeight` with it (`no-font-weight`: there is no face to
   choose, Android fakes a bold and iOS swaps files); changing numbers use tabular figures
   (`tabular-digits`); headings set the header role; font scaling caps at 200 % (`MAX_FONT_SCALE`).
7. **Line heights sit on the device pixel grid at the current font scale, and glyphs are never
   nudged.** `lineHeight = snapToPixels(fontSize * ratio * fontScale) / fontScale`, because React
   Native multiplies line heights by the font scale and rounds every text box up to whole pixels
   (`line-height-grid`, `no-rounded-line-height`); no per-size padding, margin or translate on text
   (`no-glyph-nudge`): a nudge breaks every height built on exact boxes.
8. **Tall scripts get their own line heights and an overflow guard from font metrics.** A tall ratio
   is never tighter than the base one and meets the contract's device-proven minimums
   (`tall-script-line-height`); `TALL_SCRIPT_METRICS` equals the TTF's hhea values and AppText pads
   the line from them at the drawn size (style times font scale; shifted on iOS, grown on Android)
   inside a wrapper that keeps the testID (`tall-script-overflow-guard`). iOS otherwise clips the
   tops of tall glyphs, worst at the large text sizes people choose to read better.
9. **Display text wraps balanced.** AppText runs `useBalancedWrap` for display text; the hook
   updates state functionally and probes only narrower widths (`balanced-display`). The obvious
   search passes Jest and stalls on a device.
10. **The contract declares the fonts: `"system"` by default; bundled files (opt-in) are pinned and
    named once.** With files listed, one `expo-font` plugin entry embeds every one (`font-plugin`);
    file name = PostScript name = `fontFamily` (`font-family`), because Android finds a font by file
    name and iOS by the name inside it; each file's sha256 is recorded and its licence ships
    (`font-files`); `fonts.ts` and the contract agree either way (`font-family`); with a bundled
    Latin family every script of the app's languages has its own family or an explicit `null`
    (`font-script-coverage`). Expo's object syntax (one family name plus `fontWeight`) is the
    fenced alternative, `fonts.weightBy: "fontWeight"`.
11. **One press surface; its look is a token choice, and persistent states move by layout.**
    `PressableSurface` owns the press look (`PRESS.kind`: `opacity` by default, `scale`, or the
    opt-in `sink`), the Android ripple, the disabled style, the feedback seam and the accessibility
    state. A sinking key that stays pushed in moves with `top: elevation`, never a transform
    (`pressed-by-layout`, checked wherever the sink look exists), because VoiceOver, TalkBack and
    Maestro report layout frames. Static shadows use `shadow()`/`ring()` (boxShadow); legacy
    `shadow*` and `elevation` keys are banned (`no-legacy-shadow`): `shadowOffset`, `shadowOpacity`
    and `shadowRadius` draw on iOS only, `elevation` is Android's own shadow, and `shadowColor`
    only tints it on Android 9+.
12. **Motion comes from tokens, springs are complete, and every moment has a reduce-motion
    alternative.** No duration or delay number in an animation (`no-raw-duration`: `withTiming`,
    `withDelay`, `withRepeat`, `Animated.timing`, `LayoutAnimation`, `.duration(n)` layout-animation
    builders, CSS transition keys) and no spring numbers in a component (`no-raw-spring`): inline, in
    a same-file const (`{ duration: FADE_MS }`, `.duration(SLIDE)`, `withSpring(1, BOUNCE)`) or inside
    an expression (`isSlow ? 600 : 200`, `index * 50`); every spring token writes damping,
    stiffness and mass (`spring-config-complete`: Reanimated 4.5.1 defaults mass to 4); functional
    timers never shorten. Domain layers (`src/core`, `src/data` ...) are not scanned: a task's
    duration is data.
13. **Colour is never the only signal, and a colour-blind variant must change colours.** Shape and
    text carry meaning (accessibility-as-code checks the cues); a `colorBlind` palette that changes
    no primary or status colour is refused (`palette-colorblind`). Brand-invariant roles stay equal
    in every palette (`palette-invariant`).

Visual policies such as flat paint, a maximum radius or the sinking key look are the app's choice,
switched on in the contract or the tokens (`no-gradient`, `no-pill`, `PRESS.kind`), not library rules.

## Workflow

1. **Detect first.** If `package.json` has another styling system (NativeWind, Tamagui, Restyle,
   Unistyles, styled-components) and no `src/theme`, the checkers print NOT APPLICABLE: extend that
   system in its own idiom (Expo's `expo-design-system` skill) and never add a second one. A
   create-expo-app project's `src/constants/theme.ts`, `src/hooks/use-theme.ts`,
   `use-color-scheme*.ts`, `themed-text.tsx` and `themed-view.tsx` are values to migrate, not a
   system to keep: map them into the token file and delete them (tokens-and-contract.md, "Adopting
   the create-expo-app theme"). Routes in `app/` at the repo root are found; an app without `src/`
   adds `rn-skills.config.json` `{ "srcDir": "." }` (tokens-and-contract.md, "Layout keys").
2. **Set up the theme (once).** Read [references/tokens-and-contract.md](references/tokens-and-contract.md),
   [references/layout-and-shape-tokens.md](references/layout-and-shape-tokens.md) (spacing and layout
   steps, the edge-to-edge screen frame, wide windows, strokes, elevation) and
   [references/theme-in-react-native.md](references/theme-in-react-native.md). Copy
   `templates/src/theme/`, `templates/src/ui/`, `templates/contracts/` and `templates/design/` to the
   same paths in the app. Replace the demo values in `design/tokens.json` with the design's, then
   copy them into `tokens.ts`, `type-styles.ts` and `motion.ts` (the token file first, always),
   including the press look (`press` in the token file, `PRESS` in `tokens.ts`).
3. **Write the palette.** Read [references/palettes-and-contrast.md](references/palettes-and-contrast.md).
   Run `node ${CLAUDE_SKILL_DIR}/scripts/write-palette.mjs . --dry-run` until it prints
   `RESULT: PASS`, then without `--dry-run`. When a component puts a colour on a new ground, declare
   the pair in `contracts/contrast.json` (accessibility-as-code's template, or the shape in the
   reference) and rerun; never keep a second table.
4. **Fonts.** Read [references/text-and-fonts.md](references/text-and-fonts.md). The templates use
   the system font (contract `"fonts": "system"`, every script `null` in `SCRIPT_FONTS`), which needs
   nothing more. Bundle a font only when the design names one: copy the TTFs (each named after its
   PostScript name) and their licences into `assets/fonts/`, replace the contract's `"system"` with
   the files and each `shasum -a 256`, add the `expo-font` plugin entry (`npx expo install expo-font`),
   name a family per weight in `src/theme/fonts.ts`, and copy each tall script's hhea values into
   `TALL_SCRIPT_METRICS` (the checker prints them; the reference gives Noto Sans as a worked example).
5. **Wire dark mode and the providers.** Set `userInterfaceStyle: 'automatic'`, run
   `npx expo install expo-system-ui`, and mount `AppThemeProvider` (with `onError` from the error
   log), `TextLocaleProvider`, `PressFeedbackProvider` and `NavigationThemeProvider` once in
   `src/app/_layout.tsx`, replacing the template's `ThemeProvider value={DarkTheme | DefaultTheme}`,
   as [examples/root-layout.tsx](examples/root-layout.tsx) shows (React Navigation: `App.tsx`, the
   appendix in the theme reference).
6. **Style a component or screen.** Imitate [examples/task-summary-card.tsx](examples/task-summary-card.tsx):
   `makeStyles` with `const styles = StyleSheet.create(...); return styles;`, tokens and roles only,
   AppText variants and tones, `PressableSurface` for the pressable part, `shadow()` for static
   parts. Motion: [references/motion-tokens.md](references/motion-tokens.md).
7. **Run the checks from the repo root** and loop until all pass: `npm run typecheck`,
   `npx eslint . --max-warnings 0`, `npx jest --ci`, then
   `node ${CLAUDE_SKILL_DIR}/scripts/check-design-system.mjs .` and
   `node ${CLAUDE_SKILL_DIR}/scripts/check-raw-values.mjs .`. Every `FAIL` line names the file, the
   rule and the fix: fix the code or the token file, never the contrast pairs.
8. **Report** in plain words what changed, which checks passed, which SKIP lines remain and who
   creates their targets, and any value chosen where the design was silent (the decision log). Ask
   the reviewer before changing a token the design fixed or adding a contrast exception.

## Definition of done

- [ ] `design/tokens.json` holds the design's values in two tiers, and `contracts/design-system.json`
      maps every theme export and palette to it.
- [ ] The theme modules, AppText, the balance hook, the press surface and the feedback context are in
      `src/theme` and `src/ui`, and their tests pass (`npx jest --ci`, iOS and Android projects).
- [ ] `src/theme/palette.ts` was written by `write-palette.mjs` with every pair of
      `contracts/contrast.json` (or the default pairs) passing in light and dark, and the
      colour-blind variant if any.
- [ ] Bundled fonts: each file is in `assets/fonts/` with its licence and recorded sha256, named after
      its PostScript name, listed in the `expo-font` entry, and named per weight in `fonts.ts`. System
      font (the default): the contract says `"fonts": "system"` and every script of `SCRIPT_FONTS` is `null`.
- [ ] `userInterfaceStyle` is `'automatic'`, `expo-system-ui` is installed, and the root layout mounts
      `AppThemeProvider` with `NavigationThemeProvider` inside it (and `TextLocaleProvider` in a
      multi-script app); no second theme (`constants/theme.ts`, another `useTheme`) is left.
- [ ] `npm run typecheck`, `npx eslint . --max-warnings 0` and `npx jest --ci` pass.
- [ ] Expected SKIP lines only while their target is not created yet:
      `SKIP src/i18n [text-locale-provided] not yet created (i18n-strings-and-catalogs creates it)`,
      `SKIP src/app/_layout.tsx [theme-provider-mounted]` and `[navigation-theme-mapped] not yet created (expo-project-bootstrap creates it)` (`App.tsx` with React Navigation),
      `SKIP app.config.ts [font-plugin]` (bundled fonts only) and `[color-scheme-config] not yet created (expo-project-bootstrap creates it)`.
      Note lines (which pairs judged each palette, what was scanned) are information, not problems.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-design-system.mjs .` and `node ${CLAUDE_SKILL_DIR}/scripts/check-raw-values.mjs .` print `RESULT: PASS`

## Anti-patterns

- **Retyping a value from a mockup or from memory.** It drifts by one digit; change the token file,
  copy it, rerun the checker.
- **Fixing contrast by editing the pairs, or keeping a second table.** Move the colour's lightness in
  the token file and regenerate; declare pairs once, in `contracts/contrast.json`.
- **A dark theme computed by inverting light.** Ratios do not survive inversion; tune dark as its own
  set and let the pairs judge both.
- **`PALETTE.light.primary` in a component.** It never changes with dark mode or the palette; read
  `theme.colors` through `makeStyles` or `useTheme`.
- **Keeping only the template's navigation `ThemeProvider`, or swapping it for the app's.** The first
  leaves the app theme unmounted, the second leaves headers and screen backgrounds light in dark
  mode; mount `AppThemeProvider` outside and `NavigationThemeProvider` inside.
- **Keeping create-expo-app's `constants/theme.ts` and `useTheme` beside `src/theme`.** Two hooks
  with different shapes, and colours no pair ever judged; migrate the values and delete the files.
- **Bundling a typeface because a template or another app did.** A typeface is a design's decision;
  keep `"fonts": "system"` until the design names one, then bundle and pin exactly those files.
- **`fontWeight: '700'` on a bundled family.** Each weight is its own family, so there is no face to
  choose: Android fakes a bold, iOS keeps the face or swaps in another; pick it through a type style.
- **A font file renamed to something friendly.** `Inter Bold.ttf` works on one platform only; the
  file name is the PostScript name.
- **Rounding a line height to whole points, or nudging text a point to match a screenshot.** Boxes
  round up to pixels, so only `snapToPixels` keeps them exact; first check the role the design uses.
- **An overflow guard from the unscaled size, or a measured offset.** At 200 % text it covers half the
  overflow; the guard comes from the font's metrics at the drawn size.
- **A balance search that reads state from its closure or probes wider after a failure.** It stalls
  on a device while Jest passes; copy `use-balanced-wrap.ts`.
- **A second press implementation outside PressableSurface** (a `TouchableOpacity`, a hand-rolled
  translate). Every control must answer, sound and announce the same way; compose the press surface
  and change its look through `PRESS`.
- **A transform for a key that stays pushed in.** Screen readers and Maestro see the frame above it;
  use `top: elevation`.
- **`shadowRadius` or `elevation` "just for this card".** They look different on each platform; use
  `shadow()`, and give a pressable card the press surface.
- **A spring with only damping and stiffness, or a spring config written in a component.** It
  inherits mass 4 and a slow, bouncy release; use `SPRINGS`.
- **Importing `src/services` into `src/ui` for a tap sound.** The lint boundary rejects it; read
  `usePressFeedback()`.
- **A colour-blind setting whose palette changes nothing.** Change status colours, or drop the
  variant and carry meaning by shape and text.
- **Treating a checker pass as proof a screen looks right.** It proves tokens, pairs and bans; the
  look of a screen is proven by design-visual-parity.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/tokens-and-contract.md](references/tokens-and-contract.md) | Two tiers, the token file format (plain and DTCG), the colour roles, module mapping, every contract key, flavours, the decision log, multi-package | Workflow step 2, and before changing a token |
| [references/layout-and-shape-tokens.md](references/layout-and-shape-tokens.md) | Spacing scale and named layout steps, the screen frame under Android 15/16 edge-to-edge and safe-area insets, the centred column on wide windows, radii, strokes (dashed state cues, icon strokes), elevation levels, touch targets, component measurements | Workflow step 2, and when laying out a screen |
| [references/theme-in-react-native.md](references/theme-in-react-native.md) | File map, mounting with the navigation theme (Expo Router, React Navigation appendix), the root view, dark mode on both platforms, makeStyles, shadows, the press surface looks, RTL, what is verified | Workflow steps 2 and 5 |
| [references/palettes-and-contrast.md](references/palettes-and-contrast.md) | Pairs, the contrast contract, core and default pairs, shapes, translucent colours, exceptions, write-palette, fixing a pair, dark sets, colour-blind variants, palette rule ids | Workflow step 3, any contrast question |
| [references/text-and-fonts.md](references/text-and-fonts.md) | AppText and its direction on both platforms, roles, the pixel grid and the font scale, glyph nudges, tall scripts and the guard, balanced text, tabular figures, bundled fonts and the demo fonts' source, the system font, the object-syntax alternative, font scaling | Workflow step 4, any text work |
| [references/motion-tokens.md](references/motion-tokens.md) | Motion tokens, complete springs, what no-raw-duration and no-raw-spring see, the reduce-motion table, reduce motion in code | Any animation |
| `templates/src/theme/` | Theme types, token modules (with `PRESS`), fonts (system font by default), palette and its core-pair test, contrast, theme set, context, `AppThemeProvider`, `NavigationThemeProvider`, makeStyles, text locale and its hook, text style hook, shadow helpers (each with its test); synced from the canonical copy | Workflow steps 2 and 5 (copy) |
| `templates/src/ui/` | AppText (+ iOS, Android and balance tests), the balance hook (+ test), the press feedback context (+ test; all synced), PressableSurface (+ iOS and Android tests) | Workflow step 2 (copy) |
| `templates/contracts/` | `design-system.json` (the contract) and its JSON Schema | Workflow step 2 (copy and edit) |
| `templates/design/` | `tokens.json`: the demo token file in two tiers (synced) | Workflow step 2 (copy, then replace the values) |
| [examples/task-summary-card.tsx](examples/task-summary-card.tsx) | A themed card with one pressable action, roles and tokens only | Workflow step 6 |
| [examples/task-summary-card.test.tsx](examples/task-summary-card.test.tsx) | Its test: header, tabular count, press, dark theme | Workflow step 6 |
| [examples/root-layout.tsx](examples/root-layout.tsx) | The root layout mounting the providers and the navigation theme | Workflow step 5 |
| [examples/tokens-dtcg-excerpt.json](examples/tokens-dtcg-excerpt.json) | The DTCG spellings the token reader accepts | Importing tokens from a design tool |
| `scripts/check-design-system.mjs` | Checker: contract, modules vs token file, palettes against the contrast pairs, text metrics at the font scale, tall scripts, balance, tabular, springs, press surface, fonts, dark-mode config, the provider's behaviour and mounts, the mapped navigation theme, no second theme | Workflow step 7 and at the end |
| `scripts/check-raw-values.mjs` | Checker: raw colours (named colours on colour props too), sizes, weights, tracking, radii, durations and springs (inline, in a same-file const or in an expression), palette imports, rounded line heights, legacy shadows, makeStyles factories, opt-in policies; scans `src` and the routes folder | Workflow step 7 and at the end |
| `scripts/write-palette.mjs` | Generator: `palette.ts` from the token file, refused while a pair fails | Workflow step 3 |
| `scripts/selftest.mjs` | Proves the three scripts on the shipped templates and every planted bug | After changing a script or a template |
| `scripts/check-lib.mjs` | Shared script helper, synced (do not edit here) | Never by hand |
| `scripts/lib/` | Token file reader, contract reader, contrast maths and the contrast-contract reader, font table reader, source and import helpers, the synced TypeScript module loader | Never directly |
| `assets/shared.json` | Declares the synced files (check-lib, the module loader, the canonical theme, AppText, the balance hook, the press feedback context and the demo token file) | When adding a shared file |
| `assets/default-contrast.json` | The default pairs: a verbatim copy of accessibility-as-code's `contracts/contrast.json` template, read when the app has no contrast contract | Never by hand (copy the template again when it changes) |
| `tests/fixtures/` | Overlay cases per script: good, planted bad, SKIP, NOT APPLICABLE and note cases | When adding a rule |
| `tests/bases/` | The base app (the bundled-font variant: stub fonts with real metrics, their `fonts.ts` and contract; app config, root layout) and the raw-values base with silent planted findings in installed skills | When a case needs a new base file |

## Related skills

- `ui-component-library` - buttons, rows, dialogs and the rest, built on this theme, AppText and the press surface.
- `accessibility-as-code` - the contrast contract and its rule, the reduce-motion hook, shape and text cues, 200 % text.
- `navigation-and-routing` - the navigator, and where the navigation theme mapping lives.
- `i18n-strings-and-catalogs` - the UI language that feeds `TextLocaleProvider`.
- `rtl-and-direction` - direction, digits and bidi isolation.
- `settings-and-preferences` - the saved theme preference and its restore before first paint.
- `motion-and-animation` - the moment catalogue that spends the motion tokens.
- `audio-and-haptics-feedback` - what the press feedback plays.
- `icons-app-icon-and-splash` - icons and the app icon in the theme's colours.
- `design-visual-parity` - proves a built screen matches its design baseline.
- `typescript-and-lint-rules` - the lint config behind the Text, Pressable and colour-literal bans.
- Expo's `expo-design-system` and `expo-native-ui` skills - other styling systems and platform colours.
