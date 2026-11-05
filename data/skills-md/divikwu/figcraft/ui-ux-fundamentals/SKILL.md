---
name: ui-ux-fundamentals
description: "Universal design quality rules: color, typography, spacing, content, iconography, elevation, composition, accessibility. Always applies regardless of library mode."
---

# UI/UX Fundamentals — Shared Design Rules

Universal design quality rules. Apply regardless of library mode.

> **Scope**: Aesthetic direction + structural quality.
> Auto-layout sizing rules are handled by Quality Engine lint.
> Platform-specific rules → `platform-ios` / `platform-android`.
> Responsive breakpoints → `responsive-design`.
> Content state patterns → `content-states`.

## Skill Boundaries

- Use this skill for **universal design quality rules** (color, typography, spacing, content, accessibility).
- Always loaded — applies in both library and no-library modes.
- If library is selected, also load [design-guardian](../design-guardian/SKILL.md) for token priority rules.
- If no library, also load [design-creator](../design-creator/SKILL.md) for intentional design rules.
- Platform-specific rules (screen sizes, safe areas, native typography) → [platform-ios](../platform-ios/SKILL.md) / [platform-android](../platform-android/SKILL.md).
- Responsive web breakpoints → [responsive-design](../responsive-design/SKILL.md).

## Color

- MUST choose colors with intent — define semantic roles (primary action, surface, border, text) before picking hues
- SHOULD follow 60-30-10 distribution: 60% neutral/surface, 30% secondary, 10% accent/primary
- MUST use neutral/primary text color for headings and body — hierarchy comes from font size and weight, not color
- NEVER use accent/emphasis color for heading text — reserve emphasis for inline highlights, error text, or interactive labels
- MUST ensure neutral palette has sufficient range: at least 3 levels (background, surface, border)
- NEVER use saturated colors for large surface areas — reserve high saturation for small accent elements
- SHOULD derive on-surface text color from surface background using contrast ratio (≥ 4.5:1), not guesswork
- Dark mode: reverse surface/text luminance — light text on dark surfaces, reduce shadow reliance, use surface brightness or subtle borders instead

> **Note**: Palette size limits and specific color-picking guidance are in `design-creator` (no-library) and `design-guardian` (library mode).

## Spacing

- MUST use 4px as the base spatial unit; spacing scale: 2 | 4 | 8 | 12 | 16 | 24 | 32 | 48 | 64 | 80 | 96
- MUST use 8px as the primary spacing step for padding and gaps: 8 | 12 | 16 | 24 | 32 | 48 | 64 | 80 | 96
- MUST use larger spacing between groups than within groups (Gestalt proximity)
- SHOULD follow vertical rhythm: element gap < module gap < section gap < page gap
- SHOULD use spacing as primary separator — prefer whitespace over dividers/borders
- NEVER use non-scale values for spacing (5px, 7px, 13px, etc.)

## Sizing (4px Grid)

- SHOULD set frame/container width and height as multiples of 4 (e.g. 36, 44, 48, 52, 60, 64, 80, 120, 160, 200, 240, 320, 360, 400)
- SHOULD set icon size as multiples of 4 (16, 20, 24, 32, 40, 48)
- Does NOT apply to: fontSize, lineHeight, cornerRadius, strokeWeight — these follow their own scales defined elsewhere
- Does NOT apply to: platform-specific dimensions (device screen sizes like 402×874, safe area insets like 34px home indicator)
- When a design-system token or WCAG requirement conflicts with the 4px grid, the token/requirement wins

## Grid & Layout

- SHOULD use 12-column grid (divisible by 2, 3, 4, 6); mobile: 4-column
- Common layouts: 4+8 (sidebar-content), 3+6+3, 6+6, 4+4+4, 12 (single column)
- MUST constrain reading text to 65-75ch max width (600-800px at desktop)
- SHOULD constrain form fields and dialogs to a reasonable max width

## Typography

- MUST create clear visual distinction between heading and body (≥ 2 weight levels apart)
- SHOULD limit to ≤ 3 typographic tiers per view (heading, subheading, body)
- SHOULD limit to ≤ 3 font weights total
- Minimum readable size: 12px desktop, 14px mobile
- Reading text: 45–75 characters per line, never exceed 85ch
- SHOULD tighten line-height for large headings, loosen for body text
- SHOULD use tabular-nums for data tables, prices, and time displays
- When headings stack (H2 → H3), reduce gap ~50% — heading belongs to content below it

## Content

- MUST use realistic, contextually appropriate text — never "Lorem ipsum" or "Text goes here"
- SHOULD match content length to real-world usage
- NEVER leave placeholder labels like "Button", "Title", "Label" — give them purpose
- SHOULD show content count or status in section headers when data is loaded (e.g. "3 items", "Updated 2m ago")
- Buttons: verb-first, 1–3 words, specific action ("Create account", "Save changes" — not "OK" or "Submit")
- Sentence case for UI labels ("Sign in" not "Sign In"), except proper nouns and acronyms
- Placeholders: show example format ("name@example.com", "(555) 123-4567"), not instructions
- Error messages: state what happened + how to fix ("Password is too short. Use at least 8 characters.")
- For language-specific UI copy rules (Chinese/English), load `get_creation_guide(topic:"ux-writing")`

## Iconography

- MUST use a single icon style per design: outline, filled, or duotone — never mix
- SHOULD keep icon stroke weight consistent with the typography weight
- NEVER use decorative icons without functional meaning

## Elevation & Shadows

- MUST limit to ≤ 3 shadow levels with consistent blur/offset ratios
- SHOULD use smaller blur + offset for elements closer to surface, larger for floating elements
- NEVER stack multiple shadow effects on a single element
- Shadow progression: higher elevation → larger Y-offset, larger blur, lower opacity
- Light source direction MUST be globally consistent (typically top-left)
- MUST keep sibling elements at the same elevation — do not mix shadowed and flat cards in the same container (lint: `elevation-consistency`)
- MUST maintain parent > child shadow hierarchy — child shadows should never be stronger than parent (lint: `elevation-hierarchy`)
- Dark mode: shadows are nearly invisible — use surface brightness increase or subtle light borders instead

## Corner Radius

- SHOULD define 4–5 radius tokens in ascending scale (e.g. 4 → 8 → 12 → 16 → full)
- SHOULD vary radius across hierarchy: container > card > button; consistent within same level
- Nested radius rule: inner radius = outer radius − padding (when padding ≥ outer radius, inner = 0)

## Composition

- MUST establish a clear visual focal point
- SHOULD prefer asymmetry over symmetry when it serves the content hierarchy; whitespace is a design element
- NEVER arrange all children in equal-width, equal-height uniform grids

## Quality / Anti-Slop

- NEVER cheap gradients (purple/rainbow/oversaturated) or glow effects as primary visual affordance
- NEVER more than 1 accent color per semantic role per view
- NEVER default to blue/gray palette without intentional justification

## Component Patterns

### Buttons
- Every view: only 1 primary CTA; use secondary/tertiary for other actions
- All buttons MUST define: default, hover, focus-visible, active, disabled, loading states
- Size tiers from spacing scale; touch target ≥ 44×44px regardless of visual size
- Horizontal padding ≥ 1/3 of button height

### Form Inputs
- Height MUST match same-tier button height for visual alignment
- Label: always visible above input — NEVER use placeholder as label
- Placeholder: format hints only (e.g. "YYYY-MM-DD")
- Error: colored border + icon + message below field
- Required: asterisk (*) after label or "(required)" text

### Cards
- Uniform padding on all sides (from spacing scale)
- Content order: image (optional) → title → description → meta → actions
- Clickable cards: entire card is one tap target — no nested click targets
- Elevation: subtle shadow or border; hover/selected state with slight lift or border highlight

### Navigation
- Top-level items: max 7±2 (Miller's Law)
- Current page/section: visually distinct (weight, color, underline, or background)
- Mobile: collapse to hamburger menu or bottom tab bar (max 5 tabs)
- Breadcrumbs: use when depth > 2; current page is plain text (not a link)

### Modals & Dialogs
- Max width constrained; never full-screen on desktop unless intentional takeover
- Scrolling: content scrolls, header/footer fixed
- Close button: top-right corner; scrim click optional

### Toast / Notifications
- Position: top-right or bottom-center, consistent within app
- Stack: new pushes old, max 3 visible simultaneously

### Data Tables
- Header: bold weight, distinct background, sticky on scroll
- Number columns: right-aligned, tabular-nums
- Sort/filter/selection: design visual affordances (arrows, checkboxes, chips) even for static mockups
- Mobile overflow: horizontal scroll with sticky first column
- Empty table: show empty state, not blank skeleton

## Accessibility (WCAG 2.2 AA)

- MUST text contrast ratio ≥ 4.5:1 (large text ≥ 18px: 3:1)
- MUST UI component contrast ≥ 3:1
- MUST focus indicator contrast ≥ 3:1, at least 2px outline
- MUST minimum touch target: 44×44px (recommended), 24×24px (minimum per WCAG 2.5.8)
- MUST adjacent touch targets spaced ≥ 8px apart
- NEVER convey meaning by color alone — pair with icon, pattern, or text

## CJK & Internationalization

- MUST include CJK fallback fonts in font stack (e.g. "PingFang SC", "Noto Sans JP")
- CJK body line-height: 1.6–1.8 (vs Latin 1.5–1.6); headings can tighten to 1.4
- CJK minimum body size: 14px (complex strokes need more pixels)
- NEVER add positive letter-spacing to CJK body text
- Buttons, tabs, nav items: use padding not fixed width — text length varies across languages
- Text containers: NEVER set fixed height — content length varies by language
