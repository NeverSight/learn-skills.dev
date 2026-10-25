---
name: apple-hig
description: >-
  Apple Human Interface Guidelines distilled for React Native projects, organized by platform
  (iOS, iPadOS, macOS, tvOS, visionOS, watchOS) with concrete RN implementation mappings, exact
  metrics, and review checklists. Use this skill whenever building, reviewing, or restyling any
  UI that runs on an Apple platform — screens, navigation, sheets, modals, alerts, lists, forms,
  buttons, tab bars, toolbars, typography, color, dark mode, Liquid Glass, animation, haptics,
  safe areas, Dynamic Type, accessibility, VoiceOver, widgets, notifications, or App Store
  requirements like permissions and account deletion. Also use it when the user asks whether
  something "feels native", "looks like an Apple app", follows the HIG, or should be adapted
  for iPad/Mac/TV/Vision Pro — and when porting an Android or web design to iOS, where platform
  conventions are most often lost. Prefer this skill over general design intuition for any
  Apple-platform UI decision, even when Apple or the HIG isn't mentioned by name.
---

# Apple Human Interface Guidelines for React Native

The complete HIG (172 pages) distilled into 35 reference files, each pairing Apple's rules with
concrete React Native implementations, exact metrics, and a review checklist.

**Never guess at a value.** Every number in this skill comes from the HIG — hit targets, type
scales, safe area insets, contrast ratios, spacing. Look them up rather than approximating.

## Design principles

Apple's seven principles. When two pieces of guidance conflict, these arbitrate.

- **Purpose** — create value, keep focused, find new ways to solve the problem rather than
  re-creating existing solutions.
- **Agency** — stay out of the way; let people explore without being locked into flows; **help
  people recover from mistakes**, because knowing an action is reversible is what makes an
  interface inviting.
- **Responsibility** — be transparent about what the product does and why; collect only what's
  needed; anticipate misuse.
- **Familiarity** — use concepts people know, keep visuals and interactions consistent, provide
  clear feedback.
- **Flexibility** — design for everyone (accessibility from the start, not retrofitted);
  preserve people's context across platforms; support many input methods; **approach every
  platform with intention** rather than shipping one design everywhere.
- **Simplicity** — include just what's necessary (simplicity isn't minimalism), be concise,
  establish hierarchy.
- **Craft** — quality sets the tone; experiment and iterate; **shipping isn't the finish line**.

## How to use this skill

**1. Identify what you're working on** and read the matching reference file(s) below. Most tasks
need one or two. Each file is self-contained and ends with a checklist you can apply directly.

**2. Read the platform file** for any platform you're targeting beyond iOS. Platform differences
are real and substantial — tvOS body text is 29 pt Medium, visionOS buttons need 60 pt center
spacing, macOS has no Dynamic Type.

**3. Apply the checklist** at the end of each file you read before considering the work done.

**4. For a review**, work through the relevant checklists rather than reading prose. They're
written to be scannable and mechanically verifiable.

## Routing table

### Foundations — the cross-cutting rules

| Read this | When you're… |
|---|---|
| [color-and-materials.md](references/foundations/color-and-materials.md) | Choosing colors, building a theme, implementing dark mode, using blur or Liquid Glass |
| [typography.md](references/foundations/typography.md) | Defining a type scale, handling Dynamic Type, writing UI copy, error messages, empty states |
| [layout.md](references/foundations/layout.md) | Structuring a screen, handling rotation/resizing, safe areas, notches, breakpoints, RTL |
| [accessibility.md](references/foundations/accessibility.md) | Building any interactive component; VoiceOver, hit targets, contrast, Reduce Motion |
| [motion.md](references/foundations/motion.md) | Adding any animation, transition, or gesture-driven interaction |
| [icons-and-images.md](references/foundations/icons-and-images.md) | Choosing icons, SF Symbols, exporting assets, app icons, branding |
| [privacy.md](references/foundations/privacy.md) | Requesting permissions, storing credentials, building sign-in |

### Patterns — how flows should behave

| Read this | When you're… |
|---|---|
| [modality-and-multitasking.md](references/patterns/modality-and-multitasking.md) | Presenting sheets or modals, going full screen, handling backgrounding and audio interruption |
| [feedback-and-loading.md](references/patterns/feedback-and-loading.md) | Handling async state, errors, confirmations, undo, destructive actions, rating prompts |
| [launching-and-onboarding.md](references/patterns/launching-and-onboarding.md) | Building a splash screen, first-run flow, in-app tips, state restoration |
| [data-entry-search-settings.md](references/patterns/data-entry-search-settings.md) | Building forms, search, settings, sign-in/sign-up, account deletion |
| [media-and-haptics.md](references/patterns/media-and-haptics.md) | Playing audio or video, adding haptic feedback |
| [notifications-sharing-files.md](references/patterns/notifications-sharing-files.md) | Sending push notifications, sharing, drag and drop, documents, printing |

### Components — specific controls

| Read this | When you're… |
|---|---|
| [menus-and-actions.md](references/components/menus-and-actions.md) | Buttons, toolbars, menus, context menus, pull-down/pop-up buttons, share sheets, quick actions |
| [navigation-and-search.md](references/components/navigation-and-search.md) | Tab bars, sidebars, search fields — choosing a navigation structure |
| [presentation.md](references/components/presentation.md) | Sheets, alerts, action sheets, popovers, scroll views, page controls, panels |
| [selection-and-input.md](references/components/selection-and-input.md) | Text fields, toggles, pickers, sliders, steppers, segmented controls, keyboards |
| [layout-and-organization.md](references/components/layout-and-organization.md) | Lists, tables, collections/grids, split views, tab views, disclosure, labels |
| [content-and-charts.md](references/components/content-and-charts.md) | Charts and data visualization, image views, text views, web views |
| [status.md](references/components/status.md) | Progress indicators, gauges, Activity rings, rating indicators |
| [system-experiences.md](references/components/system-experiences.md) | Widgets, Live Activities, notification content, Controls, App Shortcuts, status bars |

### Platforms — read the one(s) you ship to

| Read this | RN support |
|---|---|
| [ios.md](references/platforms/ios.md) | First-class |
| [ipados.md](references/platforms/ipados.md) | First-class (same target; layout, input, resizing) |
| [macos.md](references/platforms/macos.md) | `react-native-macos`, or Mac Catalyst |
| [tvos.md](references/platforms/tvos.md) | `react-native-tvos` |
| [visionos.md](references/platforms/visionos.md) | `react-native-visionos` (windowed UI only) |
| [watchos.md](references/platforms/watchos.md) | **None** — SwiftUI only; read for the design rules that affect your iOS app |

### React Native implementation

| Read this | When you're… |
|---|---|
| [design-tokens.md](references/rn/design-tokens.md) | Starting a project or building a theme layer — copy-pasteable token files |
| [navigation.md](references/rn/navigation.md) | Wiring navigators, headers, tab bars, sheets — native-stack vs stack, detents, dismissal guards |
| [lists-and-performance.md](references/rn/lists-and-performance.md) | Building any list or grid — FlatList vs FlashList, row metrics, virtualization, row accessibility |
| [liquid-glass.md](references/rn/liquid-glass.md) | Implementing glass/blur surfaces, scroll edge effects |
| [platform-strategy.md](references/rn/platform-strategy.md) | Deciding project structure, libraries, or which platforms to target |

### Inputs and technologies

| Read this | When you're… |
|---|---|
| [inputs.md](references/inputs.md) | Implementing gestures, keyboard shortcuts, hover, focus, Pencil, sensors |
| [identity-and-commerce.md](references/technologies/identity-and-commerce.md) | Sign in with Apple, Apple Pay, in-app purchase, Wallet, Tap to Pay |
| [system-integration.md](references/technologies/system-integration.md) | Generative AI, Siri/App Intents, Maps, SharePlay, iCloud, App Clips, Mac Catalyst |

## Critical metrics

Look these up rather than guessing. Full tables in the linked files.

### Hit targets and spacing

| Platform | Default | Minimum |
|---|---|---|
| iOS, iPadOS, watchOS | **44 × 44 pt** | 28 × 28 pt |
| macOS | 28 × 28 pt | 20 × 20 pt |
| tvOS | 66 × 66 pt | 56 × 56 pt |
| visionOS | **60 × 60 pt** | 28 × 28 pt |

Padding: **~12 pt** around bezeled controls, **~24 pt** around borderless ones. visionOS
additionally requires **≥ 60 pt between button centers** and **≥ 16 pt margins**.

### Type

| Platform | Body | Minimum | Dynamic Type |
|---|---|---|---|
| iOS, iPadOS | 17 pt | 11 pt | Yes, to **~3.1×** (53 pt at AX5) |
| macOS | 13 pt | 10 pt | **No** — fixed sizes |
| tvOS | 29 pt **Medium** | 23 pt | Yes |
| visionOS | 17 pt (bolder) | 12 pt | Yes |
| watchOS | 16 pt | 12 pt | Yes (+ AX1–AX3) |

### Contrast

**4.5:1** minimum for text up to 17 pt · **3:1** at 18 pt+ or bold · **7:1** target for custom
small text. Verify in **both** appearances.

### Safe areas

iOS/iPadOS: use `useSafeAreaInsets()` as **padding**, including `left`/`right` in landscape.
**tvOS: 60 pt top/bottom, 80 pt left/right** — RN doesn't apply these.

## The mistakes that most often make an RN app look non-native

Ranked by how frequently they appear and how visible they are:

1. **`@react-navigation/stack` instead of `@react-navigation/native-stack`** — wrong push
   animation, no interactive back-swipe, no large titles, no real sheets.
2. **`<SafeAreaView style={{flex:1}}>` as the outermost element** — leaves a colored band under
   the notch and stops content short of the screen edges. React Native's own `SafeAreaView` is
   also deprecated (0.81+) — use `react-native-safe-area-context` insets instead.
3. **Hard-coded hex where `PlatformColor` exists** — stops adapting to appearance and contrast
   settings, and drifts after OS updates.
4. **`backgroundColor` on a native header or tab bar** — overrides the Liquid Glass material.
5. **Module-scope `Dimensions.get('window')`** — correct until the first rotation or iPad resize.
6. **Fixed row `height` instead of `minHeight`** — truncates at large Dynamic Type sizes.
7. **A JS tab bar instead of a native one** — no material, no scroll-under, no selection haptic.
8. **Alert used where an action sheet belongs** — alerts are for the unexpected; action sheets
   are for choices following an intentional action.
9. **Missing `hitSlop`** on icon buttons smaller than 44 pt.
10. **The Android share glyph on iOS** instead of `square.and.arrow.up`.
11. **A tab that performs an action** rather than being a destination.
12. **Gesture-only interactions** with no button or accessibility-action alternative.
13. **`AsyncStorage` for tokens** instead of Keychain/SecureStore.
14. **A full-screen spinner** as a loading state instead of skeletons.
15. **No `accessibilityLabel`** on icon-only controls.
16. **A bottom tab bar carried over to tvOS** — tvOS tab bars sit at the **top** of the screen. Rare,
    but it's the first thing anyone notices on a TV port.

## Universal review checklist

Applies to essentially any Apple-platform screen. Per-topic checklists in each reference file
are more thorough — use these when you need one pass.

**Layout**
- [ ] Content and backgrounds reach all four screen edges; content scrolls under floating bars.
- [ ] Safe areas applied as padding, with landscape side insets handled.
- [ ] `useWindowDimensions()` used; layout verified after rotation and (iPad) resize.
- [ ] Rows use `minHeight`; no fixed heights on anything containing text.
- [ ] Logical `start`/`end` spacing properties, not `left`/`right`.

**Color and type**
- [ ] `PlatformColor` / `DynamicColorIOS` used; no hard-coded hex where a semantic color exists.
- [ ] Grouped and system background sets not mixed within a screen.
- [ ] Type scale mirrors the HIG text styles; `lineHeight` set explicitly.
- [ ] Layout verified at maximum Larger Accessibility Text.
- [ ] Text contrast ≥ 4.5:1 in light **and** dark.
- [ ] No in-app appearance toggle.

**Interaction**
- [ ] Hit targets ≥ the platform minimum, using `hitSlop` where glyphs are smaller.
- [ ] Every custom button has a visible press state.
- [ ] At most one primary action per view; destructive actions never styled as primary.
- [ ] Every gesture has a button or `accessibilityAction` equivalent.
- [ ] Native navigation, tab bar, menus, and sheets used rather than JS reimplementations.

**Accessibility**
- [ ] Every interactive element has an `accessibilityRole` and a meaningful label.
- [ ] Related content grouped into single focus stops; decorative images hidden.
- [ ] Reduce Motion honored (translations become fades, springs damped, autoplay stopped).
- [ ] No information conveyed by color alone.
- [ ] Actually navigated with VoiceOver, not just linted.

**Feedback and state**
- [ ] Skeletons rather than a full-screen spinner; determinate progress where computable.
- [ ] Errors explain the remedy and sit next to their cause.
- [ ] Alerts reserved for the unexpected; action sheets for intentional-action choices.
- [ ] Confirmations only for unexpected irreversible loss; undo offered otherwise.
- [ ] Media pauses on background and resumes on foreground.

**Platform integrity**
- [ ] Platform-standard symbols used for standard actions.
- [ ] Permissions requested at point of use, with purpose strings stating the benefit.
- [ ] Secrets in Keychain/SecureStore.
- [ ] Account deletion reachable, if accounts exist.
- [ ] Each targeted platform's own checklist applied — not just iOS's.

## Source and currency

Distilled from all 172 pages of the Human Interface Guidelines
(<https://developer.apple.com/design/human-interface-guidelines>), current as of the site's
December 2025 revisions — which includes the Liquid Glass material introduced across platforms
and the iOS 26-era guidance.

Two things worth knowing about how to treat this content:

- **Specific color values and spring constants drift.** Apple explicitly says not to hard-code
  system color values, and doesn't publish spring constants at all. Where this skill lists hex
  values, they are design-time reference for building an Android palette or a mock; resolve them
  at runtime via `PlatformColor`. Where it lists animation values, they are practical starting
  points, labeled as such.
- **RN library recommendations age faster than the HIG.** The guidance to prefer packages that
  wrap real UIKit components over JS reimplementations will outlast any specific package name.
