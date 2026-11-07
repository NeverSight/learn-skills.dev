---
name: apple-hig
description: >
  Design and build interfaces that follow Apple's Human Interface Guidelines for
  iOS, iPadOS, macOS, watchOS, tvOS, and visionOS. TRIGGER on: "iOS app",
  "iPadOS", "macOS", "watchOS", "tvOS", "visionOS", "SwiftUI", "UIKit", "AppKit",
  "HIG", "Apple design", "iPhone UI", "Mac app", "Apple Watch app", "Vision Pro",
  "SF Symbols", "Dynamic Type", "Dark Mode", "Liquid Glass", or any request to
  build, mock, or review a user interface meant to ship on an Apple platform —
  even when "HIG" is not said. Also trigger on web or Figma mockups that the
  user explicitly wants to feel native to Apple. Always run Phase 0 (ask
  targeting questions) before generating any code or design spec.
---

# apple-hig

Make Claude actually follow Apple's Human Interface Guidelines when building
for iOS, iPadOS, macOS, watchOS, tvOS, or visionOS. Works with SwiftUI, UIKit,
AppKit, and Apple-native-feeling web/Figma mockups.

> **Status: stable · v1.0.0.** Feature-complete. 68 reference files across
> foundations, patterns, components, inputs, platforms, and technologies,
> each cited to the live HIG. If HIG guidance evolves (WWDC releases, policy
> changes), update the matching file's `Last verified:` date and revise.

---

## How to use this skill

1. Identify the **target platform(s)** (iOS, iPadOS, macOS, watchOS, tvOS,
   visionOS) and the **component or pattern in play** (e.g., settings screen,
   modal sheet, list, toolbar).
2. Load only the reference files you need. Do not load the whole `references/`
   tree.
3. Never generate code or a design spec without consulting: **(a)**
   `references/foundations/accessibility.md`, **(b)** the relevant
   `references/platforms/<target>.md`, and **(c)** the relevant component or
   pattern file.
4. Apply the non-negotiables below on every output.
5. Run the final review checklist before calling work complete.

---

## Phase 0 — Ask before generating

Before writing any code or design spec, resolve targeting. Use
`AskUserQuestion` to ask the user **up to two** of the following in a single
turn. Skip any question the user has already answered in their message.

1. **Target platform(s)?** (multi-select)
   - iOS / iPhone
   - iPadOS
   - macOS
   - watchOS
   - tvOS
   - visionOS

2. **Framework?** (multi-select)
   - SwiftUI
   - UIKit / AppKit
   - Web or Figma-native

3. **What are you building?** (single-select)
   - A new full screen / window
   - A single component
   - A design spec (no code)
   - Reviewing existing UI

If the user gives a clear enough brief ("I'm building an iPhone onboarding
screen in SwiftUI"), skip Phase 0 and go straight to loading references.

---

## Decision tree — what to load

| What the user is doing | Load these references |
|---|---|
| Building a list or feed screen | `components/lists-and-tables.md` + `platforms/<target>.md` + `foundations/layout.md` + `foundations/accessibility.md` |
| Designing a settings screen | `patterns/settings.md` + `platforms/<target>.md` + `components/lists-and-tables.md` |
| Adding a modal / sheet | `patterns/modality.md` + `components/sheets-and-popovers.md` + `platforms/<target>.md` |
| Onboarding flow | `patterns/onboarding.md` + `platforms/<target>.md` + `foundations/writing.md` |
| Navigation structure | `patterns/navigation.md` + `components/bars.md` + `platforms/<target>.md` |
| Search experience | `patterns/search.md` + `components/bars.md` |
| Forms / data entry | `patterns/entering-data.md` + `components/text-inputs.md` + `components/pickers-and-menus.md` |
| Picking colors | `foundations/color.md` + `foundations/dark-mode.md` |
| Icons / glyphs | `foundations/sf-symbols.md` (+ `foundations/app-icons.md` if launcher icon) |
| Typography decisions | `foundations/typography.md` + `foundations/accessibility.md` |
| Motion / animation | `foundations/motion.md` + `foundations/accessibility.md` |
| macOS window / toolbar | `platforms/macos.md` + `components/bars.md` + `components/split-views.md` |
| iPad sidebar / split view | `platforms/ipados.md` + `components/split-views.md` + `components/bars.md` |
| watchOS complication or glance | `platforms/watchos.md` + `technologies/widgets-and-live-activities.md` |
| tvOS focus-driven screen | `platforms/tvos.md` + `inputs/focus-and-remote.md` |
| visionOS window / ornament | `platforms/visionos.md` + `foundations/materials.md` + `foundations/spatial-layout.md` |
| Live Activity / Dynamic Island | `technologies/widgets-and-live-activities.md` + `technologies/dynamic-island.md` |
| Widget | `technologies/widgets-and-live-activities.md` + `platforms/<target>.md` |
| Web / Figma mockup, Apple-native feel | `foundations/typography.md` + `foundations/color.md` + `foundations/layout.md` + `foundations/sf-symbols.md` |

If a referenced file doesn't exist yet (see Status note above), fetch the
matching HIG URL, apply the same rules, and tell the user the file is pending.

---

## Core non-negotiables

Apply on every output:

- **Touch / focus targets.** iOS ≥ 44×44pt. watchOS ≥ 44×44pt on 44mm+ / ≥ 40pt
  on smaller. tvOS: every actionable view must be focusable. macOS pointer
  targets ≥ 28×28pt. Reason: HIG ergonomic floors; missing them fails
  accessibility review.
- **Dynamic Type.** Use text styles (`.body`, `.headline`, `.title`) or
  `UIFontMetrics`. Never hardcode point sizes for body copy. Reason: users who
  size up text must not get clipped UI.
- **Dark Mode.** Use semantic colors (`Color(.label)`,
  `Color(.systemBackground)`, `Color.accentColor`) or asset catalog colors with
  any/dark variants. No hex literals in production UI. Reason: hardcoded hex
  breaks in dark mode, increased contrast, and tinted app icons.
- **VoiceOver.** Every non-decorative view has an accessibility label.
  `.accessibilityLabel(...)`, `.accessibilityHint(...)`, correct
  `.accessibilityAddTraits(...)`. Decorative images get
  `.accessibilityHidden(true)`.
- **SF Symbols first.** If a system glyph exists
  (`checkmark`, `xmark.circle.fill`, `magnifyingglass`, etc.), use it — don't
  ship a custom icon. Custom icons only when no equivalent exists.
- **Reduce Motion.** Respect `@Environment(\.accessibilityReduceMotion)` /
  `UIAccessibility.isReduceMotionEnabled`. Swap parallax / spring animations
  for cross-fades.
- **Platform-correct navigation.** iOS → tab bar or navigation stack. macOS →
  menu bar + toolbar + sidebar; don't ship a tab bar. iPadOS → sidebar / split
  view for regular size class. watchOS → page navigation or hierarchical.
  tvOS → focus-driven. visionOS → ornaments + glass windows.
- **Safe areas.** Respect `.safeAreaInset(...)` / safe area layout guides.
  Full-bleed backgrounds only below content, never under interactive elements.
- **RTL-safe layout.** Leading / trailing, not left / right. Mirror arrows and
  directional icons when appropriate.
- **Writing.** "Tap" on touch platforms, "Click" on macOS, "Select" or "Choose"
  when platform-agnostic. Sentence case in buttons and labels (not Title Case,
  unless it's a title).

---

## Common mistakes without this skill

- Using a custom font when SF Pro / SF Compact / New York would be correct.
- Hardcoded hex colors that break dark mode and tinted icons.
- Too-small tap targets (<44pt) on iOS.
- Modal-happy flows — sheets for things that should be a push, alerts for
  things that should be a toast or inline validation.
- iOS tab bars on macOS; macOS window chrome on iOS.
- Centering a nav bar title on iOS when the convention is leading-aligned (or
  vice versa on macOS toolbars).
- Ignoring safe areas; content slides under the home indicator or notch.
- Forgetting Reduce Motion; sending motion-sensitive users through a parallax
  onboarding.
- Light-mode-only screens.
- Missing VoiceOver labels on icon-only buttons.
- Using "Click" on iOS or "Tap" on macOS.
- Inventing non-standard navigation paradigms instead of `NavigationStack` /
  `NavigationSplitView` / menu bar.
- Writing an AppKit window that behaves like an iOS screen (full-bleed, no
  window chrome affordances).

---

## Final review checklist (run before calling work complete)

Load `assets/checklists/pre-submission-hig-review.md` and
`assets/checklists/accessibility-review.md` and confirm every item passes.
Minimum bar (subset):

- [ ] Touch / focus target minimums met for target platform
- [ ] Dynamic Type scales without clipping
- [ ] Dark Mode verified — no hex literals
- [ ] VoiceOver labels on every interactive view
- [ ] SF Symbols used where a system glyph exists
- [ ] Reduce Motion path exists for any non-trivial animation
- [ ] Navigation paradigm matches target platform
- [ ] Safe-area respected
- [ ] Writing tone matches platform (Tap vs Click, sentence case)
- [ ] References cited at top of any generated design doc

---

## Reference tree

```
references/
├── foundations/   typography, color, dark-mode, layout, sf-symbols, materials,
│                   motion, accessibility, inclusion, privacy, writing,
│                   app-icons, branding
├── patterns/      navigation, modality, onboarding, search, settings, loading,
│                   feedback, entering-data, drag-and-drop, file-management,
│                   offering-help, managing-accounts, in-app-purchase,
│                   multitasking, printing, ratings-and-reviews,
│                   undo-and-redo, managing-notifications, charting-data,
│                   going-full-screen, live-viewing-apps, workouts
├── components/    bars, buttons, lists-and-tables, collections-and-scrolling,
│                   sheets-and-popovers, alerts, text-inputs,
│                   pickers-and-menus, segmented-controls,
│                   sliders-steppers-toggles, progress-and-activity,
│                   labels-and-badges, split-views, system-experiences
├── inputs/        touch-and-gestures, pointer-and-keyboard, apple-pencil,
│                   digital-crown, focus-and-remote, spatial-input,
│                   game-controllers
├── platforms/     ios (deep), macos (deep), ipados, watchos, tvos, visionos
└── technologies/  widgets-and-live-activities, dynamic-island, control-center,
                    lock-screen, shortcuts-and-siri, app-clips,
                    share-extension, carplay, homekit, imessage-apps,
                    game-center, generative-ai
```

Load files lazily, only as the task requires.

---

## Maintenance

HIG updates yearly around WWDC. After each release, re-verify the `Last
verified` date at the top of each reference file and update any sizing numbers
or API deprecations. The 2025 Liquid Glass refresh (iOS 26 / macOS 26) is
covered in `foundations/materials.md`, `foundations/app-icons.md`, and the
per-platform files.
