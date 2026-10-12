---
name: apple-design
description: Apple's Human Interface Guidelines and design resources, offline — 158 HIG pages pulled from developer.apple.com plus the design kits, fonts, SF Symbols, and Icon Composer links. Use when designing, building, or reviewing UI for iOS, iPadOS, macOS, watchOS, tvOS, or visionOS (SwiftUI, UIKit, AppKit); when the user asks what Apple's guidelines say about a component, pattern, or platform; for an app icon, Liquid Glass, Dark Mode, Dynamic Type, or accessibility check; or to find an Apple Figma/Sketch kit, system font, or SF Symbols download.
---

# apple-design

Apple's design guidance as local reference. The agent's job is to **cite**: open the page, quote
the rule, name the system component. Read before you cite; Apple rewrote large parts of the HIG
for Liquid Glass (2025) and reintroduced its design principles (June 2026), so recall is stale.

| Path | What it is |
| --- | --- |
| `references/hig-index.md` | Routing table: every HIG page grouped as Apple groups them, with Apple's one-line summary, platforms, and the date Apple last changed it |
| `references/hig/<slug>.md` | One file per HIG page, Apple's own wording and headings, all six platforms. `## Specifications` sections hold the numbers (type sizes, control sizes, contrast, icon sizes) |
| `references/resources.md` | The rest of developer.apple.com/design: Figma/Sketch kits, fonts, SF Symbols, Icon Composer, bezels, the learning pathway |
| `scripts/pull_hig.py` | Regenerates `hig/` and `hig-index.md` from Apple's site. Not needed for a task |

## Steps

1. **Pin the platform and the artifact.** Which platforms (iOS, iPadOS, macOS, watchOS, tvOS,
   visionOS), which framework, and what is in front of you: a screenshot, a mockup, source, a
   description, or a question. Say what the artifact cannot show (a code fragment shows no
   contrast; a JPEG shows no exact colors).

2. **Load the pages, then read them.** Start from the always-load set for the branch, add pages
   from the routing table below, and take anything else from `hig-index.md`. About ten files, never
   the whole directory.
   - **Review or build a screen:** `design-principles.md`, `designing-for-<platform>.md`,
     `accessibility.md`, `layout.md`, `typography.md`, `color.md`, then the routed pages.
   - **Single component or pattern:** its page, plus `designing-for-<platform>.md` if platform
     behaviour matters.
   - **Question about a guideline:** the page alone.
   - **Resource, kit, font, tool:** `resources.md`.

3. **Do the task against the pages.**
   - **Review:** filter through the eight principles first (Purpose, Agency, Responsibility,
     Familiarity, Flexibility, Simplicity, Craft, Delight, defined in `design-principles.md`), then
     accessibility, platform conventions, visual design, interaction, writing. Each finding is
     **What** (with numbers), **Why** (`file.md › Heading` plus a short quote), **Fix** (the system
     component, modifier, or value to use). Rate Critical for accessibility failures and
     convention breaks that confuse, High for friction and looks-foreign, Medium for missed
     system components, Low for polish.
   - **Build:** reach for the system component before a custom view and name it (`TabView`,
     `NavigationSplitView`, `.sheet`, `.searchable`, `NSToolbar`). A custom control still needs
     its press, hover, focus, and disabled states, Dynamic Type, both appearances, and safe areas.
   - **Question:** quote the guideline, cite the file and heading, add the developer link the page
     gives.

4. **Done when** every element on screen has been checked against a page you opened, every
   claim carries a `file.md › Heading` citation or is labelled *judgment*, and every number
   (contrast ratio, control size, type size, icon size) comes from a `## Specifications` table
   rather than recall.

## Routing

| The design shows, or the question is about | Load |
| --- | --- |
| Tabs, sidebar, split view, navigation bar, toolbar | `tab-bars.md`, `sidebars.md`, `split-views.md`, `toolbars.md` |
| Buttons, menus, actions | `buttons.md`, `menus.md`, `context-menus.md`, `pop-up-buttons.md`, `pull-down-buttons.md` |
| Sheets, alerts, popovers, panels, modal flows | `modality.md`, `sheets.md`, `alerts.md`, `action-sheets.md`, `popovers.md`, `panels.md` |
| Forms, text entry, pickers, toggles, sliders | `entering-data.md`, `text-fields.md`, `pickers.md`, `toggles.md`, `sliders.md`, `virtual-keyboards.md` |
| Lists, tables, collections, outlines, cards | `lists-and-tables.md`, `collections.md`, `outline-views.md`, `labels.md`, `scroll-views.md` |
| Search | `searching.md`, `search-fields.md` |
| Liquid Glass, blur, translucency, vibrancy | `materials.md › Liquid Glass`, `color.md › Liquid Glass color` |
| Dark appearance | `dark-mode.md`, `color.md` |
| Icons, symbols, app icon, artwork | `icons.md`, `sf-symbols.md`, `app-icons.md`, `images.md` |
| Motion, haptics, sound | `motion.md`, `playing-haptics.md`, `playing-audio.md` |
| Loading, progress, feedback, errors, empty states, copy | `loading.md`, `feedback.md`, `progress-indicators.md`, `writing.md` |
| First run, sign-in, permissions | `launching.md`, `onboarding.md`, `managing-accounts.md`, `privacy.md`, `sign-in-with-apple.md` |
| Settings | `settings.md` |
| Windows, menu bar, keyboard, pointer, Dock (Mac) | `windows.md`, `the-menu-bar.md`, `keyboards.md`, `pointing-devices.md`, `focus-and-selection.md`, `dock-menus.md` |
| Multitasking, drag and drop, undo, files | `multitasking.md`, `drag-and-drop.md`, `undo-and-redo.md`, `file-management.md` |
| Notifications, widgets, Live Activities, complications | `notifications.md`, `managing-notifications.md`, `widgets.md`, `live-activities.md`, `complications.md` |
| Charts | `charting-data.md`, `charts.md` |
| AI, Siri, shortcuts | `generative-ai.md`, `machine-learning.md`, `siri.md`, `app-shortcuts.md` |
| Payments, subscriptions, ratings | `apple-pay.md`, `in-app-purchase.md`, `ratings-and-reviews.md` |
| Watch | `designing-for-watchos.md`, `digital-crown.md`, `always-on.md`, `watch-faces.md` |
| Vision Pro | `designing-for-visionos.md`, `spatial-layout.md`, `immersive-experiences.md`, `eyes.md`, `ornaments.md` |
| TV | `designing-for-tvos.md`, `remotes.md`, `top-shelf.md`, `focus-and-selection.md` |
| Games | `designing-for-games.md`, `game-controls.md`, `game-center.md` |
| Brand, personality | `branding.md`, `design-principles.md` |

## Report shape for a review

```text
## Design review: <name> — <platform>
Summary: two sentences, rating Excellent / Good / Needs work / Critical issues.
### Critical    — What / Why (`file.md › Heading`: "quote") / Fix
### Improvements — same shape, tagged High / Medium / Low
### What works  — specific enough to survive the next iteration
```

Only sections with content appear. A strong design gets a short review.

## Refreshing the references

```bash
python3 scripts/pull_hig.py            # stdlib only; add --cache /tmp/hig-cache to keep the raw JSON
```

Apple stamps each page with its last change; `hig-index.md` carries the dates, and
<https://developer.apple.com/design/whats-new/> lists them. A second run over unchanged pages
writes nothing, and the script refuses to delete more than a tenth of the pages without
`--force-prune`.
