---
name: seenry-apps
description: "Design and build native-feeling mobile app screens and flows (SwiftUI, UIKit, React Native, Expo, Flutter, mobile web prototypes) that match top App Store apps. Use for onboarding, tab and stack navigation, lists, forms, settings, paywalls, players, sheets and empty or error states. Researches whole journeys in real apps via Seenry MCP (the flow from the app it is based on, the look from the app it should look like), then enforces navigation doors, a mechanical slop pre-flight and a beat-the-reference gate."
license: Apache-2.0
metadata:
  author: Seenry
  version: "0.1.0"
---

# Seenry Apps

Mobile quality is mostly platform fidelity plus the same discipline as the web system: a strict grid, components built in layers, few type sizes, one accent, and every state designed. Work in the project's existing stack and components.

## Workflow

1. **Name the jobs.** Write `research/brief.md`: what the product is based on (the flow), what it should look like (the look), and what job the signature screen does (the edge). "Based on X, designed like Y" means X gives the flow and Y gives the look; one named app gives both; none means choosing the look on purpose. Follow [research](references/research.md).
2. **Study real apps, whole journeys.** With Seenry MCP, find apps by name (`search_app_flows {q: "<app>"}`) and walk complete flows in order (`get_app_flow`, paging to the end). At least three complete flows for any flow you build (the based-on app plus best-in-class leaders, for onboarding Headspace, Duolingo, Calm or Noom), at least 8 screens of the look app across 2–3 flows, 10+ screens of each other screen type, and one `borrow_references` pass for the edge. Stop at saturation, when new screens stop changing the spec. App screens carry a small watermark; ignore it.
3. **Write the spec before code.** `research/flows.md` charts each flow's spine (per step: asks, gives, presentation), `.seenry/look.md` holds the look app's palette, type, numerals and named signature components, `research/patterns.md` splits table stakes, edge and opening, and `research/decisions.md` lists each decision with the screen ids it came from, plus the navigation map. Every onboarding screen carries one of the look's signature components with this product's content.
   **Take the signature, not the defaults.** The look app's platform defaults (system blue, white grouped sheets, SF Pro, grey rows) are not its look; every app has them. Its look is the signature components and the attitude behind them. The product gets its own identity on top: an accent from its own idea (never iOS blue or indigo unless the brand owns it), a display or numeral treatment people will remember, and a color world that fits the subject (a sleep product lives at night). If the screens could be any app's onboarding with the logo swapped, it is slop, however faithful the research.
4. **Map the flow and its doors** with [flows](references/flows.md): what each screen is (push, modal, sheet, replace), what back does from it, and the one-way doors (finished onboarding, sign-in, purchase) where back must not re-enter. Onboarding asks one thing per screen, teaches with the answers, and ends on a payoff built from them before any permission or paywall.
5. **Explore the signature screen, then pick blind.** Build three directions of the screen the flow exists for (usually the payoff, with the welcome screen in the same direction) as separate files: one conventional control, two that each break a cliché, one built on the borrowed edge. They must differ in what the eye lands on first, not only in layout. Run `node ../seenry/scripts/pick.mjs a.html b.html c.html --brief <brief> --refs <look app screens>` and build the whole flow in the winner's direction.
6. **Spec each component** with the [four-layer construction](../seenry/references/components.md): grid → safe space → structure → type and states.
7. **Build the connected states** with real data: loading, empty, error, permission denied, offline, success, and the keyboard-open layout. Web prototypes start with `<!doctype html>`, `<meta charset="utf-8">` and a viewport meta.
8. **Pre-flight the counts:** `node scripts/app_preflight.mjs <source>` counts accent hue families, grey families, the radius scale, emoji in UI, gradients, type families, labels per intent, encoding and the document head. A failed count is a fix, not a judgment call; a deliberate exception from the look (Flighty's status colors) is written in `decisions.md`.
9. **Walk it on the simulator and record it.** Run the flow end to end on the iOS Simulator (or an Android emulator), web prototypes included: serve the folder, boot an installed iPhone (`xcrun simctl list devices available`, then `xcrun simctl boot <udid>`; one run per simulator), `xcrun simctl openurl booted http://127.0.0.1:<port>/`, screenshot each step with `xcrun simctl io booted screenshot NN-step.png`. A desktop browser at 390px does not show Safari's toolbars, safe areas, keyboard or real font rendering. Exercise every step, every back path (chevron, edge swipe, Android back), back after each one-way door, sheets dragged and cancelled mid-drag, the keyboard both ways, skip everything once. Record it (`xcrun simctl io booted recordVideo rec.mov`; Android `adb shell screenrecord /sdcard/rec.mp4`) and watch it twice, once at speed and once frame by frame, for wrong-theme flashes, layout jumps and dropped frames.
10. **Beat the reference, screen by screen.** Put each of your screens beside the best equivalent screen you studied. Any screen that reads worse goes back in the loop. Then run the gate: `node ../seenry/scripts/check.mjs --screens <screens in flow order> --video rec.mov --brief <brief>` and apply its fixes until PASS or STOP. In showcase mode, on STOP below the target, rebuild the signature screen and flow on a different direction from step 5 and run `check.mjs --new-direction` once before reporting. Use `--mode quick` by default (one critic round, fixes applied once), `--mode polish` when asked for production-ready work and `--mode showcase` only for a showcase. Report the score and level in the delivery: pass (9), leader level (8) or below leader level with the gaps. Without Seenry MCP, first run `node ../seenry/scripts/research.mjs --type app` so the critic has a bar. Write `.seenry/idea.md`, `.seenry/motion.md` and `DESIGN.md` as in `seenry`; the gate checks for them.
11. **Deliver the Seenry sheet** as in `seenry` ([the sheet](../seenry/references/sheet.md)): screenshots per state, the apps and flows studied with ids, the decisions and their sources, anatomy of the signature screen and guidelines. Use `sheet.py`; annotate simulator screenshots by hand where `anatomy.mjs` (web only) does not apply.

## Platform system

| | iOS | Android (Material 3) |
| --- | --- | --- |
| Grid | 4pt base, layout multiples of 8 | 4dp base, layout multiples of 8 |
| Screen margin | 16 (20 on large phones and inset grouped lists) | 16 (24 on larger) |
| Min touch target | 44×44 pt | 48×48 dp |
| Nav bar | 44 + large title 52 | Top app bar 64 |
| Tab bar | 49 + home indicator; 3–5 items; icon 24–28 + label 10/500 | Navigation bar 80; 3–5 items |
| List row | 44 min; 60–76 with subtitle or 40pt image | 56 one-line, 72 two-line |
| Grouped list | inset 16, radius 10–12, separators inset to text | cards or full-width with dividers |
| Buttons | 50 tall full-width primary, radius 12–14 or capsule | 40 filled/tonal, radius full |
| Sheets | detents medium/large, grabber, radius ~10 system | bottom sheet, drag handle 32×4 |
| Type | SF Pro: Large Title 34, Title 1 28, Title 2 22, Title 3 20, Headline 17/600, Body 17, Callout 16, Subhead 15, Footnote 13, Caption 12/11 | Roboto/Flex: Display 57/45/36, Headline 32/28/24, Title 22/16/14, Body 16/14/12, Label 14/12/11 |

Use Dynamic Type text styles (iOS) and `sp` with font scale (Android) instead of fixed sizes. Use the project's tokens, or the look studied in `.seenry/look.md`, mapped onto system semantic roles (`label`, `secondaryLabel`, `systemBackground`), so dark mode and increased contrast work; plain system colors only when there is neither. These metrics are the platform floor, not the style: a web prototype takes native sizes, targets and safe areas, not iOS default styling.

## Screen rules

- **One primary action per screen**, placed where the thumb is: a bottom-pinned full-width button above the home indicator, or the trailing nav bar item for "Save/Done".
- **Per component: ≤3 text styles.** A player card uses Headline, Subhead and Caption; nothing else.
- **Concentric corners** on nested shapes (`inner = outer − inset`), and continuous corner curves (`.continuous` / squircle) on iOS.
- **Content first.** Lists, media and records get the screen; summaries and headers stay compact. Large titles collapse on scroll.
- **Native controls** before custom: pickers, toggles, segmented controls, menus, share sheets, date pickers. A custom control must match their feedback (haptics, press states) and accessibility.
- **Safe areas and keyboard.** Nothing under the notch, Dynamic Island, home indicator or keyboard. Primary buttons ride above the keyboard.
- **Onboarding**: one idea per screen with visible progress and skip, the product's signature view in the first screen, choices as large rows, and permissions behind a pre-prompt at the moment they pay off. Length follows the studied flows: a personalized product earns 8–15 screens when every answer visibly changes the payoff; a tool with nothing to personalize gets 1–3. End on a payoff built from the answers before any paywall ([flows](references/flows.md)).
- **Paywall**: show what the product does (real screens or features), the plan choice with the recommended plan preselected, the price per period with trial terms in plain text directly under the CTA, restore purchase and terms links.
- **Settings**: grouped inset lists, sections of 2–6 rows, icon tiles 28–29 with radius 6–7 in one style, values trailing in secondaryLabel, destructive actions last and separate.
- **Empty and error states** inside the region, with one action that resolves them.

## Alignment

The same keyline, ink-level and optical rules apply natively ([alignment](../seenry/references/alignment.md), [optical](../seenry/references/optical.md)): align SF Symbols by their glyph (use `.imageScale` and baseline alignment with text, `alignmentGuide` for cap-height alignment), use `firstTextBaseline` alignment for icon + label rows, and check play/chevron glyph centering in circular buttons at 3x screenshots.

## Motion

Gate every animation by how often it is met ([flows](references/flows.md#motion-frequency-gate)): the platform's own for tabs, scroll, back and keyboard; under 150ms for presses; designed moments only where they are rare, like the onboarding payoff. Navigation motion comes from the platform (push, sheet, zoom). Custom motion: springs (`response 0.35–0.5, dampingFraction 0.8–0.9`), interruptible, 150–300ms feel, with haptic feedback on commit (selection, success, warning). Respect Reduce Motion. For web-based apps, use `seenry-motion` and the Seenry Transitions kit.

The same transitions the web kit provides, natively (apply them without being asked, by situation):

| Situation | SwiftUI | Jetpack Compose | React Native |
| --- | --- | --- | --- |
| Trigger becomes the surface (menu, card to detail) | `matchedGeometryEffect` or `.navigationTransition(.zoom(sourceID:in:))`; close lands where the trigger was | `SharedTransitionLayout` + `sharedBounds` | Reanimated shared element transitions |
| Sheet, dialog | `.sheet` with `.presentationDetents`; custom: `.spring(response: 0.4, dampingFraction: 0.86)` | `ModalBottomSheet`; `spring(dampingRatio = 0.86f, stiffness = 400f)` | `@gorhom/bottom-sheet`, spring damping 20-24 |
| Changing numbers | `.contentTransition(.numericText(value:))` inside `withAnimation` | `AnimatedContent` per digit, slide by direction | Reanimated per-digit `FadeIn/SlideIn` by direction |
| Tabs, segmented control | shared indicator via `matchedGeometryEffect` | animated indicator offset with `animateDpAsState` | Reanimated `withSpring` indicator translateX |
| List insert, remove, reorder | `.transition(.move(edge:).combined(with: .opacity))` on stable IDs | `Modifier.animateItem()` | `LinearTransition` / `FadeIn` layout animations |
| Button loading, success, error | `.symbolEffect` and `.contentTransition(.symbolEffect(.replace))`; `.sensoryFeedback` | `AnimatedContent` for the label; `HapticFeedback` | icon swap with scale 0.9→1 and opacity; `expo-haptics` |
| Toast, banner | from the top safe edge, spring in, 120ms ease-out out | `AnimatedVisibility(slideInVertically + fadeIn)` | Reanimated `SlideInUp` / `FadeOut` |

Exits are faster than entrances, only transform and opacity move in lists, and every custom animation has a Reduce Motion path (`@Environment(\.accessibilityReduceMotion)`, `Settings.Global.ANIMATOR_DURATION_SCALE`, `AccessibilityInfo.isReduceMotionEnabled`).

## Anti-slop for apps

| Tell | Fix |
| --- | --- |
| Web-style centered hero screens inside an app | Content-first native layout |
| Custom tab bar with glows, gradients or floating blobs | System tab bar or a quiet custom one with native metrics |
| Every row in its own colored gradient card | Grouped inset list |
| 12px body text, fixed font sizes | Dynamic Type styles, 17pt body |
| Paywall hiding price or trial terms | Price per period and terms under the CTA |
| Purple gradient onboarding with stock 3D illustrations | Show the product doing its job |
| A named look ("like Flighty") rendered as system blue on grouped lists | Signature components from `.seenry/look.md` and the product's own accent and color world |
| Every question the same white card with radio rows and a blue full-width button | Answers as the product's own objects (a time on the board, a pass filling in), a different input per kind of answer |
| Platform defaults copied from the reference and called its look | The reference's signature components and attitude; defaults are not identity |
| Web prototype without `<meta charset="utf-8">` and a viewport meta | Both in `<head>`; check punctuation renders and the layout fits 390pt |
| Buttons 36pt tall at the screen bottom edge | 50pt, inset 16, above the home indicator |

## Done, per flow

- [ ] Three or more complete flows and 8+ look-app screens studied; ids in `research/`; the pattern adopted for each screen named
- [ ] `.seenry/look.md` exists, its signature components appear in the build carrying this product's content, and the accent and color world are the product's own, not platform defaults
- [ ] Three directions of the signature screen built and picked blind with `pick.mjs`
- [ ] Navigation map written; back verified on every screen; one-way doors cannot be re-entered
- [ ] Onboarding ends on a payoff built from the answers; every permission has a pre-prompt and a soft way out; paywall terms in plain text under the CTA
- [ ] Loading, empty, error, permission-denied and long-content states designed, not defaulted
- [ ] `app_preflight.mjs` passes, or each exception is written in `decisions.md`
- [ ] Light and dark, largest Dynamic Type, safe areas and keyboard verified on screen
- [ ] The flow recording watched twice with no flash, jump or dropped frame
- [ ] Screens and recording captured on the iOS Simulator (or emulator), not a desktop browser
- [ ] Every screen holds up beside the best reference screen studied; `check.mjs` run in the requested mode, score and level reported

## Review

Screenshot the flow in order on device or simulator (light and dark, largest text size) and review with `seenry-review` or a fresh agent. The optional [flow gate](scripts/independent_flow_gate.py) sends ordered captures to fresh visual and flow reviewers when Codex CLI is installed. Static captures do not prove gestures, VoiceOver or calculations; exercise those on the device.
