---
name: apple-human-interface-guidelines
description: "Apple Human Interface Guidelines (HIG) reference for designing iOS, iPadOS, macOS, tvOS, visionOS, watchOS apps. Covers UI components, layout, accessibility, typography, navigation, inputs, and platform technologies. Use when designing Apple platform UIs, reviewing SwiftUI/UIKit patterns, or applying HIG design principles to any app."
---

# Apple Human Interface Guidelines

Comprehensive design reference covering all Apple platforms. Use this skill when:
- Designing or reviewing UI for any Apple platform
- Implementing SwiftUI or UIKit components following Apple conventions
- Making decisions about layout, typography, color, accessibility, or interaction patterns
- Integrating Apple technologies (Apple Pay, HealthKit, Game Center, etc.)
- Applying Apple's design principles to web or cross-platform development

## How to Use This Skill

1. Identify the task category (platform design, component, pattern, input, or technology)
2. Find the matching reference below
3. Load the specific reference file(s) needed
4. For cross-cutting concerns (accessibility, color, typography), load the relevant foundations reference alongside any component reference

---

## Quick Reference: Common Tasks

| Task | Load These References |
|---|---|
| Building a login/auth screen | `foundations/privacy.md`, `technologies/sign-in-with-apple.md`, `patterns/managing-accounts.md` |
| Designing a settings screen | `patterns/patterns-settings.md`, `components/selection-and-input/toggles-guidelines.md` |
| Choosing colors / dark mode | `foundations/color-guidelines.md`, `foundations/dark-mode.md` |
| Implementing navigation | `components/navigation-and-search/tab-bars.md`, `components/navigation-and-search/sidebars.md`, `components/layout-and-organization/split-views.md` |
| Typography / text sizing | `foundations/typography-guidelines.md`, `foundations/writing-guidelines.md` |
| Accessibility audit | `foundations/accessibility.md`, `technologies/voiceover-guidelines.md` |
| Designing a form | `patterns/entering-data.md`, `components/selection-and-input/text-fields.md`, `components/selection-and-input/pickers.md` |
| Building a list/table view | `components/layout-and-organization/lists-and-tables.md`, `components/presentation/scroll-views.md` |
| Adding search | `patterns/searching-patterns.md`, `components/navigation-and-search/search-fields.md` |
| Creating an app icon | `foundations/app-icons.md` |
| Designing notifications | `patterns/managing-notifications.md`, `components/system-experiences/notifications-component.md` |
| Building widgets | `components/system-experiences/widgets-design-guidelines.md` |
| Implementing payments | `technologies/apple-pay.md`, `technologies/in-app-purchase.md` |
| Designing charts/data viz | `patterns/charting-data.md`, `components/content/components-charts.md` |
| Building for visionOS | `getting-started/designing-for-visionos.md`, `foundations/spatial-layout.md`, `foundations/immersive-experiences.md` |
| Modal presentations | `patterns/modality-guidelines.md`, `components/presentation/sheets-guidelines.md`, `components/presentation/alerts-component.md` |
| Onboarding flow | `patterns/onboarding.md`, `patterns/launching.md` |
| Video/audio playback | `patterns/playing-video.md`, `patterns/playing-audio.md` |
| Game design | `getting-started/designing-for-games.md`, `inputs/game-controls.md`, `technologies/game-center.md` |
| RTL / internationalization | `foundations/right-to-left.md`, `foundations/inclusion-guidelines.md` |
| Sharing / collaboration | `patterns/collaboration-and-sharing.md`, `components/menus-and-actions/activity-views.md` |
| Generative AI features | `technologies/generative-ai-guidelines.md`, `technologies/machine-learning-design.md` |

---

## 1. Getting Started — Platform Design Fundamentals

Load these when starting design for a specific platform or needing platform constraints (screen sizes, input methods, ergonomics).

| Reference | When to Consult |
|---|---|
| `reference/getting-started/designing-for-ios.md` | iPhone app design: display characteristics, ergonomics, control placement, appearance adaptation |
| `reference/getting-started/designing-for-ipados.md` | iPad app design: large display, multitasking, multiple input modes, widgets |
| `reference/getting-started/designing-for-macos.md` | macOS app design: window management, menu bar, keyboard shortcuts, Dock |
| `reference/getting-started/designing-for-tvos.md` | tvOS/Apple TV: 8+ ft viewing, focus system, Siri Remote, cinematic presentation |
| `reference/getting-started/designing-for-visionos.md` | visionOS/Vision Pro: spatial design, immersion levels, eye/hand input, comfort |
| `reference/getting-started/designing-for-watchos.md` | watchOS: glanceable UI, Digital Crown, complications, Always On |
| `reference/getting-started/designing-for-games.md` | Game design across platforms: text sizes, controls, onboarding, accessibility |

## 2. Foundations — Cross-Cutting Design Principles

Core design principles applicable across platforms. Many of these apply to **web and cross-platform development** too.

### Universally Applicable (any platform)
| Reference | When to Consult |
|---|---|
| `reference/foundations/accessibility.md` | Vision, hearing, mobility, speech, cognitive accessibility requirements and contrast ratios |
| `reference/foundations/color-guidelines.md` | Color choices, theming, contrast, system color specs, dark mode color values |
| `reference/foundations/dark-mode.md` | Dark mode implementation: adaptive colors, contrast (4.5:1 min), icon/image adaptation |
| `reference/foundations/typography-guidelines.md` | Font sizes, weights, leading, Dynamic Type specs, text styles per platform |
| `reference/foundations/writing-guidelines.md` | UX writing: voice/tone, button labels, error messages, capitalization |
| `reference/foundations/inclusion-guidelines.md` | Inclusive language, diverse representation, cultural sensitivity |
| `reference/foundations/layout-guidelines.md` | Visual hierarchy, adaptive layout, safe areas, device dimensions |
| `reference/foundations/motion-guidelines.md` | Animation best practices, accessibility, frame rates |
| `reference/foundations/privacy.md` | Permission flows, purpose strings, tracking rules, data protection |
| `reference/foundations/branding-guidelines.md` | Brand integration: accent colors, custom fonts, logos, content-first design |

### Apple Platform–Specific
| Reference | When to Consult |
|---|---|
| `reference/foundations/app-icons.md` | App icon design: layers, shapes, sizes, dark/tinted, platform-specific specs |
| `reference/foundations/icons-guidelines.md` | Interface icons/glyphs, SF Symbol name mapping, macOS document icons |
| `reference/foundations/images-guidelines.md` | Image resolution, scale factors, file formats, tvOS layered images |
| `reference/foundations/sf-symbols.md` | SF Symbols: rendering modes, variable color, weights, animations, custom symbols |
| `reference/foundations/materials-guidelines.md` | Liquid Glass, vibrancy, material thickness, platform-specific materials |
| `reference/foundations/right-to-left.md` | RTL interfaces: text alignment, numeral handling, control/image flipping |
| `reference/foundations/spatial-layout.md` | visionOS: field of view, depth, 60pt min center-to-center spacing |
| `reference/foundations/immersive-experiences.md` | visionOS immersion: mixed/progressive/full, passthrough, comfort |

## 3. Patterns — Interaction & UX Patterns

Recurring UX patterns. Many are **applicable beyond Apple platforms**.

### Data & Content
| Reference | When to Consult |
|---|---|
| `reference/patterns/charting-data.md` | Data visualization: chart simplicity, accessibility, chart type selection |
| `reference/patterns/entering-data.md` | Form design: validation, secure input, offering choices over text |
| `reference/patterns/searching-patterns.md` | Search: field placement, suggestions, privacy, Spotlight integration |
| `reference/patterns/file-management.md` | Document apps: auto-save, Quick Look, open/save dialogs |

### Feedback & Status
| Reference | When to Consult |
|---|---|
| `reference/patterns/feedback-patterns.md` | Status, errors, task completion, warnings |
| `reference/patterns/loading-patterns.md` | Progress indicators, placeholder content, background downloads |
| `reference/patterns/playing-haptics.md` | Haptic feedback: predefined patterns, custom haptics |

### Lifecycle & Navigation
| Reference | When to Consult |
|---|---|
| `reference/patterns/launching.md` | Launch screens (no text/branding), state restoration |
| `reference/patterns/onboarding.md` | First-run: interactive teaching, TipKit, permission timing |
| `reference/patterns/modality-guidelines.md` | Modal usage: when, dismiss conventions, avoiding stacked modals |
| `reference/patterns/going-full-screen.md` | Full-screen modes: layout, control visibility, gesture deferral |
| `reference/patterns/multitasking.md` | App switching, background tasks, multi-window |

### Media
| Reference | When to Consult |
|---|---|
| `reference/patterns/playing-audio.md` | Audio categories, interruptions, Spatial Audio |
| `reference/patterns/playing-video.md` | Video playback: aspect ratio, PiP, system player, visionOS immersive video |
| `reference/patterns/live-viewing-apps.md` | Live TV/streaming: EPG, content footers, cloud DVR |

### Social & Commerce
| Reference | When to Consult |
|---|---|
| `reference/patterns/collaboration-and-sharing.md` | Share button, collaboration popover, share sheet |
| `reference/patterns/managing-accounts.md` | Login flows, passkeys, biometrics, account deletion requirements |
| `reference/patterns/managing-notifications.md` | Interruption levels, Focus, marketing notification rules |
| `reference/patterns/ratings-and-reviews.md` | Rating prompts: timing, frequency, system prompt |

### Utility
| Reference | When to Consult |
|---|---|
| `reference/patterns/drag-and-drop.md` | Drag & drop: move/copy, visual feedback, multi-item, accessibility |
| `reference/patterns/offering-help.md` | TipKit, tooltips (macOS/visionOS), contextual help |
| `reference/patterns/printing-pattern.md` | Print action placement, macOS print panel customization |
| `reference/patterns/undo-and-redo.md` | Undo/redo: multi-level, platform-specific shortcuts/gestures |
| `reference/patterns/patterns-settings.md` | Settings placement, defaults, macOS settings windows |
| `reference/patterns/workouts-pattern.md` | Fitness/workout UI: session screens, metrics, Activity rings |

## 4. Components — UI Building Blocks

### Content
| Reference | When to Consult |
|---|---|
| `reference/components/content/components-charts.md` | Chart components: mark types, axes, color, interaction, accessibility |
| `reference/components/content/image-views.md` | Image display: overlays, animation, tvOS layered, visionOS spatial |
| `reference/components/content/text-views.md` | Multiline text views: when to use, legibility, editing |
| `reference/components/content/web-views.md` | Embedded web content: navigation, avoiding browser replication |

### Layout & Organization
| Reference | When to Consult |
|---|---|
| `reference/components/layout-and-organization/components-boxes.md` | GroupBox/NSBox: grouping content, titles, nesting |
| `reference/components/layout-and-organization/collections-component.md` | Grid/row visual layouts: galleries, padding, dynamic changes |
| `reference/components/layout-and-organization/column-views.md` | macOS column (browser) views for deep hierarchies |
| `reference/components/layout-and-organization/disclosure-controls.md` | Disclosure triangles/buttons: expandable sections |
| `reference/components/layout-and-organization/components-labels.md` | Static labels: color hierarchy (primary→quaternary), legibility |
| `reference/components/layout-and-organization/lists-and-tables.md` | Lists/tables: styles, editing, selection, per-platform rules |
| `reference/components/layout-and-organization/lockups-tvos.md` | tvOS lockups: cards, posters, focus expansion |
| `reference/components/layout-and-organization/outline-views.md` | macOS outline views: hierarchical data, sorting, disclosure |
| `reference/components/layout-and-organization/split-views.md` | Multi-pane layouts: dividers, resizing, per-platform rules |
| `reference/components/layout-and-organization/tab-views.md` | Tabbed content panes: max tabs, labeling, alternatives |

### Menus & Actions
| Reference | When to Consult |
|---|---|
| `reference/components/menus-and-actions/activity-views.md` | Share sheets: custom activities, icon sizing |
| `reference/components/menus-and-actions/buttons.md` | Button design: hit regions, styles, roles, per-platform types |
| `reference/components/menus-and-actions/context-menus.md` | Context menus: ordering, previews, destructive actions |
| `reference/components/menus-and-actions/dock-menus.md` | macOS Dock menus |
| `reference/components/menus-and-actions/edit-menus.md` | Edit menus: system vs custom, per-platform behavior |
| `reference/components/menus-and-actions/home-screen-quick-actions.md` | iOS/iPadOS long-press quick actions (4-action limit) |
| `reference/components/menus-and-actions/menus-design-guidelines.md` | Menu design: labeling, icons, grouping, submenus |
| `reference/components/menus-and-actions/ornaments-visionos.md` | visionOS ornaments: window-associated floating controls |
| `reference/components/menus-and-actions/pop-up-buttons.md` | Pop-up buttons: mutually exclusive option selection |
| `reference/components/menus-and-actions/pull-down-buttons.md` | Pull-down buttons: action menus, destructive actions |
| `reference/components/menus-and-actions/menu-bar-guidelines.md` | macOS/iPadOS menu bar: standard menus, required items, shortcuts |
| `reference/components/menus-and-actions/toolbars.md` | Toolbars: item grouping, overflow, navigation bars |

### Navigation & Search
| Reference | When to Consult |
|---|---|
| `reference/components/navigation-and-search/path-controls.md` | macOS path controls: standard/pop-up styles |
| `reference/components/navigation-and-search/search-fields.md` | Search fields: placement, scope controls, tokens |
| `reference/components/navigation-and-search/sidebars.md` | Sidebars: hierarchy, hide/show, per-platform rules |
| `reference/components/navigation-and-search/tab-bars.md` | Tab bars: tab count, badges, Liquid Glass, sidebar adaptation |
| `reference/components/navigation-and-search/token-fields.md` | macOS token fields: text-to-token conversion |

### Presentation
| Reference | When to Consult |
|---|---|
| `reference/components/presentation/action-sheets.md` | Action sheets: destructive buttons, Cancel, vs alerts/menus |
| `reference/components/presentation/alerts-component.md` | Alerts: titles, button placement, destructive styling |
| `reference/components/presentation/page-controls.md` | Page indicators: placement, interaction, customization |
| `reference/components/presentation/panels.md` | macOS panels/HUDs: floating supplementary windows |
| `reference/components/presentation/popovers.md` | Popovers: positioning, sizing, dismissal |
| `reference/components/presentation/scroll-views.md` | Scroll views: nesting, paging, edge effects, zoom |
| `reference/components/presentation/sheets-guidelines.md` | Sheets: detents, button placement, grabber, modal/nonmodal |
| `reference/components/presentation/windows-component.md` | Windows: types, states, visionOS volumes, glass backgrounds |

### Selection & Input
| Reference | When to Consult |
|---|---|
| `reference/components/selection-and-input/color-wells.md` | Color picker/wells |
| `reference/components/selection-and-input/combo-boxes.md` | macOS combo boxes |
| `reference/components/selection-and-input/digit-entry-views.md` | tvOS PIN/digit entry |
| `reference/components/selection-and-input/image-wells.md` | macOS image wells (drag-and-drop image editing) |
| `reference/components/selection-and-input/pickers.md` | Pickers/date pickers: styles, modes, per-platform |
| `reference/components/selection-and-input/segmented-controls.md` | Segmented controls: modes, segment limits |
| `reference/components/selection-and-input/sliders.md` | Sliders: direction, tick marks, labels, circular (macOS) |
| `reference/components/selection-and-input/components-steppers.md` | Steppers: value visibility, pairing with text fields |
| `reference/components/selection-and-input/text-fields.md` | Text fields: sizing, placeholder, validation, keyboard types |
| `reference/components/selection-and-input/toggles-guidelines.md` | Toggles/switches/checkboxes/radio buttons |
| `reference/components/selection-and-input/virtual-keyboards.md` | Virtual keyboards: types, custom input views, extensions |

### Status
| Reference | When to Consult |
|---|---|
| `reference/components/status/activity-rings.md` | Activity rings: colors, backgrounds, label RGB values |
| `reference/components/status/gauges.md` | Gauges/level indicators: styles, gradients |
| `reference/components/status/progress-indicators.md` | Progress bars, spinners, refresh controls |
| `reference/components/status/rating-indicators.md` | Star ratings (macOS only) |

### System Experiences
| Reference | When to Consult |
|---|---|
| `reference/components/system-experiences/app-shortcuts.md` | App Shortcuts: Siri, Spotlight, voice interaction design |
| `reference/components/system-experiences/watchos-complications.md` | watchOS complications: families, image sizes, templates |
| `reference/components/system-experiences/controls-system-experience.md` | iOS Controls: Control Center, Lock Screen, Action button |
| `reference/components/system-experiences/live-activities.md` | Live Activities: anatomy, layout, dimensions per device |
| `reference/components/system-experiences/notifications-component.md` | Notification content, actions (4 max), badges, watchOS looks |
| `reference/components/system-experiences/status-bars.md` | iOS/iPadOS status bar: visibility, readability |
| `reference/components/system-experiences/top-shelf.md` | tvOS Top Shelf: templates, image dimensions |
| `reference/components/system-experiences/watch-faces.md` | watchOS watch faces: sharing, complications, previews |
| `reference/components/system-experiences/widgets-design-guidelines.md` | Widgets: families, sizes, rendering modes, exact dimensions |

## 5. Inputs — Interaction Methods

| Reference | When to Consult |
|---|---|
| `reference/inputs/action-button.md` | iPhone/Watch Action button: labeling (3-word max), behaviors |
| `reference/inputs/apple-pencil-and-scribble.md` | Apple Pencil: hover, double tap, squeeze, Scribble, PencilKit |
| `reference/inputs/camera-control.md` | iPhone 16 Camera Control: overlays, viewfinder layout |
| `reference/inputs/digital-crown.md` | Digital Crown: watchOS scrolling/navigation, visionOS system use |
| `reference/inputs/visionos-eyes-input.md` | visionOS gaze: hover effects, spacing (60pt centers), comfort |
| `reference/inputs/focus-and-selection.md` | Focus navigation: iPadOS, tvOS (5 states), visionOS |
| `reference/inputs/game-controls.md` | Game input: touch, game controllers, keyboard, visionOS spatial |
| `reference/inputs/gestures.md` | Gesture specs per platform, custom gestures, visionOS direct/indirect |
| `reference/inputs/gyro-and-accelerometer.md` | Motion sensing: permission copy, accessibility |
| `reference/inputs/keyboards-guidelines.md` | Physical keyboard shortcuts, modifier keys, Full Keyboard Access |
| `reference/inputs/nearby-interactions.md` | Ultra Wideband proximity/spatial awareness |
| `reference/inputs/pointing-devices.md` | Pointer/mouse/trackpad: effects, hit regions, magnetism |
| `reference/inputs/remotes-tvos.md` | Siri Remote: gestures, button behavior, focus integration |

## 6. Technologies — Platform Integrations

### Payments & Commerce
| Reference | When to Consult |
|---|---|
| `reference/technologies/apple-pay.md` | Apple Pay: button types/styles/sizing, checkout, subscriptions |
| `reference/technologies/in-app-purchase.md` | IAP: subscription sign-up, offer codes, refunds, Family Sharing |
| `reference/technologies/tap-to-pay-on-iphone.md` | Tap to Pay: merchant flows, checkout UX, error handling |

### Identity & Privacy
| Reference | When to Consult |
|---|---|
| `reference/technologies/sign-in-with-apple.md` | Sign in with Apple: button specs (min 140×30pt), custom buttons, UX flow |
| `reference/technologies/id-verifier.md` | ID Verifier: age/identity verification, data minimization |
| `reference/technologies/wallet-design-guidelines.md` | Wallet passes: styles, image specs, order tracking, identity |

### Health & Fitness
| Reference | When to Consult |
|---|---|
| `reference/technologies/healthkit-guidelines.md` | HealthKit: privacy, Activity rings rules, Health icon usage |
| `reference/technologies/carekit.md` | CareKit: task views, charts, contacts, care plans |
| `reference/technologies/researchkit.md` | ResearchKit: onboarding flow order, surveys, active tasks |

### Media & Communication
| Reference | When to Consult |
|---|---|
| `reference/technologies/airplay-guidelines.md` | AirPlay: streaming, mirroring, icon specs, terminology |
| `reference/technologies/shareplay.md` | SharePlay: activity sharing, visionOS Persona templates |
| `reference/technologies/live-photos.md` | Live Photos: frame adjustments, sharing, badges |
| `reference/technologies/shazamkit.md` | ShazamKit: mic privacy, iCloud opt-in |
| `reference/technologies/imessage-apps-and-stickers.md` | iMessage apps/stickers: views, icon/sticker sizes, formats |

### AI & Machine Learning
| Reference | When to Consult |
|---|---|
| `reference/technologies/generative-ai-guidelines.md` | Gen AI: transparency, privacy, hallucination mitigation |
| `reference/technologies/machine-learning-design.md` | ML UX: feedback, calibration, confidence, corrections |

### Platform Extensions
| Reference | When to Consult |
|---|---|
| `reference/technologies/app-clips.md` | App Clips: card specs, Code sizing, privacy constraints |
| `reference/technologies/mac-catalyst.md` | Mac Catalyst: iPad→Mac adaptation, idiom selection, navigation mapping |
| `reference/technologies/carplay-design-guidelines.md` | CarPlay: layout specs, icon sizes, audio behavior |
| `reference/technologies/siri-integration-guidelines.md` | Siri/Shortcuts: intents, voice UX, shortcut phrases, custom UI |

### Accessibility
| Reference | When to Consult |
|---|---|
| `reference/technologies/voiceover-guidelines.md` | VoiceOver: alt labels, image descriptions, reading order, rotor |

### Other Integrations
| Reference | When to Consult |
|---|---|
| `reference/technologies/always-on-display.md` | Always On: privacy redaction, dimming, layout consistency |
| `reference/technologies/augmented-reality.md` | AR/ARKit: object placement, coaching overlays, multiuser |
| `reference/technologies/game-center.md` | Game Center: access point, achievements, leaderboards, image specs |
| `reference/technologies/homekit-guidelines.md` | HomeKit: terminology, setup flows, Siri patterns, branding |
| `reference/technologies/icloud-guidelines.md` | iCloud: syncing, conflict resolution, storage, game saves |
| `reference/technologies/maps-guidelines.md` | MapKit: annotations, overlays, clustering, place cards |
| `reference/technologies/nfc-guidelines.md` | NFC: scanning UX, terminology, background tag reading |
| `reference/technologies/photo-editing-extensions.md` | Photo editing extensions: toolbar, previews, cancel confirmation |

---

## Cross-Platform Applicability

These references contain principles useful **beyond Apple platforms** (web, Android, cross-platform):

- **Accessibility** (`foundations/accessibility.md`, `technologies/voiceover-guidelines.md`) — contrast ratios, screen reader patterns, cognitive considerations
- **Color & Dark Mode** (`foundations/color-guidelines.md`, `foundations/dark-mode.md`) — theming, contrast, adaptive design
- **Typography** (`foundations/typography-guidelines.md`) — hierarchy, sizing, Dynamic Type concepts
- **Writing** (`foundations/writing-guidelines.md`) — UX copy, error messages, tone
- **Inclusion** (`foundations/inclusion-guidelines.md`) — inclusive language, representation
- **Privacy** (`foundations/privacy.md`) — permission patterns, data minimization
- **Motion** (`foundations/motion-guidelines.md`) — animation accessibility, reduced motion
- **Layout** (`foundations/layout-guidelines.md`) — responsive/adaptive patterns, visual hierarchy
- **Generative AI** (`technologies/generative-ai-guidelines.md`) — responsible AI design principles
- **ML Design** (`technologies/machine-learning-design.md`) — confidence display, correction patterns
- **Patterns** — Most patterns (onboarding, feedback, loading, modality, search, settings, data entry) encode universal UX wisdom