---
name: apple-design-skill
description: Provides Apple's Human Interface Guidelines (HIG) for designing, building, and reviewing native UI/UX on iOS, iPadOS, macOS, watchOS, tvOS, and visionOS. Covers system components (buttons, sheets, menus, lists, pickers, navigation), input methods (gestures, Apple Pencil, Digital Crown, Camera Control, keyboards), foundational design elements (color, typography, materials, motion, SF Symbols, accessibility, dark mode, app icons), interaction patterns (onboarding, search, drag and drop, notifications, undo/redo), platform-specific considerations, and technologies (Siri, Apple Pay, HealthKit, SharePlay). Use whenever the user is designing, building, or reviewing UI for an Apple platform, choosing between system components, asking what Apple recommends for an interaction or visual element, checking HIG compliance, or asking about Apple design terminology — even without saying "HIG" explicitly.
metadata:
  content-source: "Apple Human Interface Guidelines, mirrored via sosumi.ai"
  content-owner: "Apple Inc."
---

# Apple Design (Human Interface Guidelines)

This skill bundles a local mirror of Apple's Human Interface Guidelines under `references/`. It is unofficial content
extracted via sosumi.ai — all HIG content belongs to Apple Inc. Ground answers in these files rather than
general/training knowledge: HIG guidance is specific, precise, and changes over time.

## Coverage

Six HIG sections are mirrored under `references/`:

| Section         | Path                          | Covers                                                                                                                                                                                   |
|-----------------|-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Getting started | `references/getting-started/` | Cross-platform design principles, plus one article per platform (iOS, iPadOS, macOS, watchOS, tvOS, visionOS, games)                                                                     |
| Foundations     | `references/foundations/`     | Color, typography, materials, motion, SF Symbols, icons, accessibility, dark mode, privacy, layout, branding, writing                                                                    |
| Patterns        | `references/patterns/`        | Common tasks/experiences: onboarding, search, drag and drop, notifications, undo/redo, feedback, multitasking, settings                                                                  |
| Components      | `references/components/`      | System-defined UI components, in 8 categories: content, layout and organization, menus and actions, navigation and search, presentation, selection and input, status, system experiences |
| Inputs          | `references/inputs/`          | Input methods: gestures, Apple Pencil, Digital Crown, keyboards, pointing devices, Camera Control, Action button, remotes, eyes                                                          |
| Technologies    | `references/technologies/`    | Platform technologies to integrate: Siri, Apple Pay, HealthKit, SharePlay, AirPlay, Sign in with Apple, and more                                                                         |

Every section has an `index.md` landing page. **Components is the one section with an extra nesting level** — its
`index.md` lists 8 category folders, each with its own `index.md` plus the individual component articles. The other five
sections are flat: the section `index.md` links directly to article files in the same folder.

**Liquid Glass** (Apple's current cross-platform material) isn't one article — it's referenced across
`foundations/materials.md`, `foundations/color.md`, `foundations/motion.md`, and specific component articles
(`buttons.md`, `tab-bars.md`, `toolbars.md`, `sidebars.md`, `widgets.md`, and others). For any "liquid glass" request,
start with `foundations/materials.md`, then layer in the specific component's article.

## Finding the right article

1. **Fast path**: grep `references/topic-index.md` — a flattened list of every article with its path and one-line
   description — for the component, pattern, or technology name (or a close synonym). This is almost always faster than
   browsing.
   ```
   grep -i "sheet" references/topic-index.md
   ```
2. **Browse path**: if the keyword search doesn't turn up a clear match, read the relevant section's `index.md` (for
   Components, read `references/components/index.md` first to pick a category, then that category's `index.md`).
3. Read the matched article in full before answering. HIG articles are short and structured (anatomy, behavior,
   guidelines, platform-specific considerations) — read the whole thing rather than skimming.

The rest of this file assumes a single question with a single answer. The next two sections cover generative tasks —
designing a new component or a whole screen — which need to synthesize several articles into one deliverable instead.

## Designing a new component

Use this workflow for requests like "design a liquid glass primary button" or "create a segmented control variant for X":

1. Find the closest existing system component in `references/components/` via `topic-index.md` — start from and extend
   it, don't invent a component from scratch.
2. Pull in the cross-cutting foundations that shape the visual/interaction treatment: `foundations/materials.md`
   (material/Liquid Glass treatment), `foundations/color.md`, `foundations/typography.md`, `foundations/motion.md`
   (interaction feedback and animation).
3. Check `foundations/accessibility.md` — contrast, Dynamic Type, VoiceOver, and minimum hit target (e.g. the
   44×44pt / 60×60pt-on-visionOS rule already documented in `components/menus-and-actions/buttons.md`).
4. If the component must work across platforms, check the relevant `getting-started/designing-for-<platform>.md` for
   device-specific constraints.
5. Produce the deliverable using this template:

   ```markdown
   # <Component name>

   **Base system component:** <name + references/ path>
   **Purpose:** <what it's for>

   ## Anatomy
   <parts that make up the component>

   ## States & variants
   <default, pressed/hover, disabled, selected, sizes, etc.>

   ## Sizing & spacing
   <concrete values pulled from the HIG article, not invented>

   ## Material & color
   <e.g. Liquid Glass treatment, tint, contrast behavior in light/dark>

   ## Motion & feedback
   <press/hover/transition behavior>

   ## Accessibility
   <contrast, Dynamic Type, VoiceOver label/traits, minimum hit target>

   ## Platform notes
   <differences across iOS/iPadOS/macOS/watchOS/tvOS/visionOS, if any>

   ## Implementation note
   This spec covers design intent (look, behavior, states, sizing, accessibility) grounded in HIG text. It does not
   specify SwiftUI/UIKit/AppKit API names — verify exact modifiers/APIs against current framework documentation
   rather than assuming them from HIG prose, which never contains API references.
   ```

## Designing a screen

Use this workflow for requests like "build a library screen which shows all my books": HIG documents components and
patterns, not whole screens, so decompose the request first.

1. Decompose into three parts:
   - **Navigation shell** — tab bar vs. sidebar vs. navigation stack; see `components/navigation-and-search/` and the
     target platform's `getting-started/designing-for-<platform>.md`.
   - **Primary content component** — `components/layout-and-organization/` for lists, tables, grids, split views;
     `components/content/` for images, text, charts.
   - **Supporting patterns** — `patterns/searching.md`, `patterns/loading.md`, `patterns/onboarding.md`, and empty/error
     state handling.
2. For any piece that needs customization beyond default guidance, apply the "Designing a new component" workflow above
   to it.
3. State which platform(s) the screen targets explicitly — composition conventions (tab bar vs. sidebar, full-screen vs.
   multi-pane) differ by platform.
4. Produce the deliverable using this template:

   ```markdown
   # <Screen name>

   **Purpose:** <what the screen is for>
   **Platform(s):** <iOS/iPadOS/macOS/watchOS/tvOS/visionOS>

   ## Navigation shell
   <tab bar / sidebar / navigation stack choice, and why, per platform if it differs>

   ## Primary content
   <component(s) used to present the core content, with references/ paths>

   ## Supporting patterns
   <search, loading, onboarding, etc., with references/ paths>

   ## States
   <loading / empty / error / populated>

   ## Accessibility
   <notable considerations beyond what's already covered per-component>

   ## Implementation note
   Same boundary as component specs: this is design intent, not API syntax.
   ```

## Answering

- Cite what the article actually says. Don't invent guidance that isn't there.
- HIG articles frequently cover **multiple platforms in one file**, with platform-specific subsections (look for
  headings like "iOS, iPadOS", "macOS", "watchOS", "visionOS"). State which platform(s) your answer applies to — don't
  assume iOS guidance carries to macOS or watchOS.
- When a question spans more than one section (e.g. "how should I show a destructive action?" touches a Components
  article like `buttons.md` as well as Foundations' `color.md` or Patterns' `feedback.md`), check more than one file
  rather than stopping at the first match.
- If the question falls outside the mirrored content entirely, say so explicitly and fall back to general Apple platform
  knowledge rather than presenting a guess as HIG guidance.
- Article images are real `docs-assets.developer.apple.com` URLs with alt text, not stripped out — fetch/view them
  directly when a visual or anatomy detail matters more than the prose description.
- This skill is authoritative on design intent, never on API names — that boundary applies to every answer, not just
  component/screen specs.

## Gotchas

- `references/components/navigation-and-search/tab-bars.md` and
  `references/components/layout-and-organization/tab-views.md` are different components — a tab *bar* navigates between
  top-level app sections, a tab *view* switches panes of content in place. Don't conflate them.
- Cross-platform design principles live in `references/getting-started/design-principles.md`; per-platform device
  characteristics live in `references/getting-started/designing-for-<platform>.md` — neither is under Components.
- This is a static content mirror, not a compliance checker. It won't automatically catch a specific app's HIG
  violations — reason about the user's actual UI against the guidance in the matched article.
