---
name: apple-design
description: Apple Human Interface Guidelines (HIG) reference for designing or reviewing UI on iOS, iPadOS, macOS, watchOS, visionOS, tvOS. Use when the user asks how a screen, navigation structure, or interaction should be designed to feel native on an Apple platform; whether a design follows Apple's guidelines; which system control to use in SwiftUI/UIKit; how to set a color, font, spacing, or animation; how to design an app icon or pick an SF Symbol; how to use Liquid Glass; or how to design for accessibility — including when the user never says "HIG" or "Apple design guidelines".
---

# Apple Design (Apple Human Interface Guidelines reference skill)

This skill distills Apple's official design resources (`developer.apple.com/design/`) into ready-to-use reference material, so you can give interface design and review advice for iOS / iPadOS / macOS / watchOS / visionOS / tvOS apps that is grounded in current official guidance.

## Grounded, or guessing

Every specific claim you make — a point value, a contrast ratio, a component's official name, an API name — is either **grounded** or it's a guess:

- **Grounded** — you read it in a `references/` file in this skill, or you just fetched the official page.
- **Guess** — it came from training memory.

State guesses as guesses, never as specs. The HIG is retuned almost every year around WWDC, and June 2025 replaced the entire materials, icon, and control-appearance system with **Liquid Glass** — so training memory of "Apple design guidelines" likely predates that change, or mixes specs across platforms. When a claim can't be grounded, say so and hand the user the official URL.

Qualitative advice ("keep the primary action reachable one-handed") doesn't need this treatment. Numbers, official names, and specs do.

## The overall structure of the HIG

The official HIG (`developer.apple.com/design/human-interface-guidelines/`) is organized into six top-level sections, from abstract to concrete:

1. **Getting started** — Design principles, plus per-platform overviews (iOS/iPadOS/macOS/tvOS/visionOS/watchOS/games)
2. **Foundations** — Elements that run through every interface: Accessibility, App icons, Color, Materials, Typography, Layout, SF Symbols, Motion, Privacy, Dark Mode, etc.
3. **Patterns** — Design guidance for common tasks/experiences: Onboarding, Searching, Undo and redo, Multitasking, Modality, Notifications, etc.
4. **Components** — System components, grouped into eight subcategories: Content / Layout and organization / Menus and actions / Navigation and search / Presentation / Selection and input / Status / System experiences
5. **Inputs** — Input methods: Gestures, Digital Crown, Apple Pencil, Eyes, Game controls, etc.
6. **Technologies** — Integrating specific Apple technologies: Siri, Wallet, HealthKit, SharePlay, etc.

The complete sitemap and every page URL live in [references/hig-sitemap.md](references/hig-sitemap.md).

## How to use this skill

Identify the **target platform(s)** first. Ergonomics, input methods, and component conventions differ substantially across platforms — read the relevant section of [references/platforms.md](references/platforms.md) before carrying an iPhone-shaped assumption over to Apple Watch or Vision Pro. Then take the branch that matches the request.

### Branch A — designing something new

1. Decide whether this is a **foundation** question or a **specific component/pattern** question:
   - Color, typography/type size, SF Symbols, materials (especially Liquid Glass), icons, layout/safe areas, accessibility → the matching file in the reference index below
   - How to use a specific control (buttons, tab bars, sidebars, lists, toolbars) → [references/components.md](references/components.md); for anything it doesn't cover, look up the slug in [references/hig-sitemap.md](references/hig-sitemap.md)
   - An interaction pattern (onboarding flows, search, undo, gestures) → [references/patterns-gestures.md](references/patterns-gestures.md)
2. Explain the **why**, not just the what. Ground advice in the design principles in [references/principles.md](references/principles.md), or in the concrete official rationale ("so the control stays comfortable to hit at Apple's 44×44pt default size," not "because Apple says so").
3. When it's time to produce actual design files or prototypes, point to the official UI Kits, fonts, SF Symbols, and Icon Composer in [references/resources.md](references/resources.md) instead of having the user redraw standard system controls from scratch.

**Done when** every number, component name, and API name in the answer is grounded, and each recommendation carries its rationale.

### Branch B — reviewing an existing design

Walk **all eight principles** in [references/principles.md](references/principles.md) in order, giving each an explicit verdict: conforms / violated (naming the specific element) / not applicable here. Then check the specs the review actually touches — hit targets, type sizes, contrast, safe areas — against [references/accessibility.md](references/accessibility.md) and [references/layout.md](references/layout.md).

**Done when** all eight principles carry a verdict — including the ones that turned out fine, so the user can see the review was exhaustive — and every spec cited is grounded.

### Branch C — looking up one fact

Check the reference index below first; those summaries answer most questions. When a summary doesn't mention the component you need, or the user needs an exact point value or API name, open the matching URL from [references/hig-sitemap.md](references/hig-sitemap.md).

**Fetching HIG pages**: they are JavaScript-rendered single-page apps, so a plain WebFetch often captures only the page title, not the body. If a fetch comes back suspiciously short, switch to a browser tool (navigate → wait 1-2s → get_page_text). If it still fails, give the user the URL and tell them the content wasn't retrieved.

## The eight design principles (quick reference)

Full explanations live in [references/principles.md](references/principles.md); here's the one-line version, useful for quickly figuring out which direction a design tradeoff should lean:

- **Purpose** — Get clear on what actually matters to people before deciding how to build it
- **Agency** — Stay out of the user's way, let them explore freely, and keep the cost of mistakes low (undo, recover)
- **Responsibility** — Be accountable for people's data and trust; be transparent about permissions and data use
- **Familiarity** — Borrow concepts people already know and stay visually/interactionally consistent, to lower the learning curve
- **Flexibility** — Accessibility is a starting point, not a patch; adapt to different devices, input methods, and contexts
- **Simplicity** — Keep only what's necessary and build a clear hierarchy — simplicity isn't the same as minimalism
- **Craft** — Every detail reflects how much you care; keep refining instead of treating shipping as the finish line
- **Delight** — Know what emotion you're trying to evoke, but never let delight upstage the task at hand

## Platform quick reference (details in references/platforms.md)

| Platform | One-line positioning | Primary navigation | Key input methods |
|---|---|---|---|
| iOS | On-the-go, single-handed, fragmented usage | Floating tab bar (Liquid Glass) | Multi-touch, voice |
| iPadOS | Large-screen productivity and creation, multitasking | Tab bar ↔ sidebar, adaptive | Touch, external keyboard/trackpad, Apple Pencil |
| macOS | Long focused work sessions, multiple windows | Menu bar + sidebar | Keyboard, pointing devices |
| watchOS | Glance-and-go, sub-minute interactions on the wrist | Digital Crown navigation | Digital Crown, Action button, simple gestures |
| visionOS | Spatial computing, windows floating in real space | Floating tab bar / sidebar | Eyes + indirect/direct gestures |

tvOS isn't summarized in [references/platforms.md](references/platforms.md) — for tvOS questions, fetch `designing-for-tvos` via [references/hig-sitemap.md](references/hig-sitemap.md). (tvOS specs *are* covered in the accessibility, typography, and layout reference files.)

## Liquid Glass in one paragraph

Introduced in 2025, this new material is meant for the **control and navigation layer** (tab bars, sidebars, toolbars) — not the content layer. Standard system components pick it up automatically; custom components should use it sparingly. It comes in two variants: **regular** (preserves legibility, use for most cases) and **clear** (emphasizes visibility of a rich media background underneath). By default it has no inherent color and tints itself from what's behind it — apply color sparingly, and prefer tinting the background rather than the symbols/text on top of it. Full rules in [references/materials-color.md](references/materials-color.md).

## Accessibility specs (condensed; [references/accessibility.md](references/accessibility.md) is authoritative)

| Spec | iOS/iPadOS | macOS | tvOS | watchOS | visionOS |
|---|---|---|---|---|---|
| Default text size | 17pt | 13pt | 29pt | 16pt | 17pt |
| Minimum text size | 11pt | 10pt | 23pt | 12pt | 12pt |
| Default control size | 44×44pt | 28×28pt | 66×66pt | 44×44pt | 60×60pt |
| Minimum control size | 28×28pt | 20×20pt | 56×56pt | 28×28pt | 28×28pt |
| Text contrast (≤17pt) | 4.5:1 (WCAG AA) | same | same | same | same |

**Default is the design target; minimum is the floor.** Quote 44×44pt (iOS/iPadOS/watchOS) and 60×60pt (visionOS) as what a control should be — the [Buttons guidance](references/components.md) states those as a floor for buttons specifically. The much smaller "minimum control size" row is an absolute lower bound from the accessibility page; don't hand it to a user as a design target.

Full accessibility guidance (vision, hearing, mobility, speech, cognitive) lives in [references/accessibility.md](references/accessibility.md).

## Reference file index

| File | Contents |
|---|---|
| [references/principles.md](references/principles.md) | Full explanation of the eight design principles and how to apply them |
| [references/platforms.md](references/platforms.md) | Device characteristics, ergonomics, and best practices for iOS/iPadOS/macOS/watchOS/visionOS |
| [references/materials-color.md](references/materials-color.md) | The full rules for Materials, Liquid Glass, and the Color system |
| [references/typography-symbols.md](references/typography-symbols.md) | Font families, Dynamic Type, and SF Symbols rendering modes/weights/animations |
| [references/layout.md](references/layout.md) | Visual hierarchy, size classes, safe areas, adaptability |
| [references/accessibility.md](references/accessibility.md) | **Authoritative specs table** plus guidance across the five accessibility dimensions |
| [references/components.md](references/components.md) | Best practices for Buttons, Tab bars, Sidebars, Lists/Tables, Toolbars |
| [references/app-icons.md](references/app-icons.md) | Layered icon design, the Icon Composer workflow, Liquid Glass icon appearances |
| [references/patterns-gestures.md](references/patterns-gestures.md) | Gesture design principles, standard per-platform gestures, common interaction patterns |
| [references/resources.md](references/resources.md) | Official UI Kits, fonts, SF Symbols, Icon Composer, and other downloads |
| [references/hig-sitemap.md](references/hig-sitemap.md) | Full URL index of the HIG, for looking up anything this skill doesn't already cover |

## A note on quoting official content

HIG text is copyrighted by Apple. When explaining something to a user, **paraphrase the core rule and rationale in your own words** rather than pasting large blocks of the original text. When exact wording matters (e.g. for marketing copy or legal-adjacent language), hand the user the official URL and let them read the source themselves rather than reproducing it verbatim in your reply.
