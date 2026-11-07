---
name: platform-visual-standards
description: "Current platform visual standards: iOS 26 Liquid Glass and SF Symbols 7, Material 3 Expressive (HCT, Dynamic Color, spring physics), web CSS 2025-2026 (container queries, view transitions, anchor positioning), plus watchOS, tvOS, and automotive. Use when a design must feel native to its platform."
---

# Platform Visual Standards

## Why Platform Visual Standards Matter

Every platform has a visual language — materials, motion curves, typography rules, spacing systems, and interaction idioms. A professional app respects these conventions because users have muscle memory and visual expectations formed by their OS. Ignoring platform standards makes an app feel alien. This skill ensures Sumi knows the current visual standards for every major platform so recommendations are platform-native, not platform-generic.

## Reference Architecture

| File | Contents | Use When |
|------|----------|----------|
| `references/ios-26-liquid-glass.md` | iOS 26/iPadOS 26 Liquid Glass design system: material tiers, vibrancy levels, SF Symbols 7 (rendering modes, variable color, animations), Dynamic Island, StandBy mode, Live Activities, SwiftUI implementation patterns, Safe Areas, Dynamic Type. | Designing for iPhone, iPad. Recommending iOS-native patterns. Implementing Liquid Glass correctly. |
| `references/material-3-expressive.md` | Material Design 3 Expressive: 35-shape library (morphing shapes), spring-physics motion (mass, stiffness, damping), HCT color space, Dynamic Color (wallpaper extraction), M3 component gallery, Jetpack Compose patterns, canonical layouts for tablets/foldables. | Designing for Android, Wear OS. Recommending Material-native patterns. Implementing Dynamic Color. |
| `references/web-css-2025-2026.md` | Modern CSS capabilities: container queries (@container), view transitions API (same-doc + cross-doc), scroll-driven animations, oklch()/lch() color functions, anchor positioning, CSS nesting, :has() selector, subgrid, @layer cascade layers, @scope (scoped styles), @starting-style (entry animations), interpolate-size: allow-keywords (animate to height: auto), text-wrap: balance/pretty, transition-behavior: allow-discrete, @property (typed/animatable custom properties), field-sizing: content, scroll-snap-stop: always, Figma Sites/new products. | Building web interfaces. Recommending modern CSS patterns. Avoiding outdated approaches. Entry/exit animations without JS. Height auto transitions. |
| `references/watchos-tvos-automotive.md` | Watch design (Apple Watch, Wear OS): complications, glanceability, Digital Crown. TV design (tvOS, Android TV, Fire TV): 10-foot UI, D-pad navigation, focus system, overscan. Automotive (CarPlay, Android Auto): glanceability, driver safety, touch targets. | Designing for non-phone/tablet devices. Understanding unique constraints of each form factor. |
| `references/spatial-xr-design.md` | Spatial computing: visionOS (windows, volumes, spaces, Liquid Glass), Meta Quest (Horizon OS, 2D panels, immersive), WebXR, AR overlay patterns. Depth, gaze, gesture interaction models. | Designing for AR/VR/MR. Understanding spatial UI constraints. visionOS app design. |
| `references/cross-platform-harmony.md` | How to maintain one design system across 9 form factors: phone, tablet, desktop, TV, watch, spatial, automotive, kiosk, e-ink. Token architecture for multi-platform. Platform adaptation patterns. When to diverge vs. converge. | Building cross-platform design systems. Deciding platform-specific vs. shared patterns. Multi-device strategy. |

---

## 1. iOS 26 Liquid Glass

### Design Philosophy

Liquid Glass is Apple's unified material language introduced in iOS 26. It replaces the layered frosted-glass approach of previous iOS versions with a single, continuously adaptive translucent material that responds to the content behind it. The philosophy centers on three principles: contextual transparency (the interface reveals the world behind it), adaptive luminance (glass brightens or darkens to maintain legibility), and unified surface language (every chrome element uses the same material system, creating visual coherence across the entire OS).

Liquid Glass is not a blur effect. It is a rendering pipeline that composites specular highlights, refraction-simulated distortion, and dynamic tinting into a single material layer. The effect is computed in real time by the GPU, using environment maps derived from the content beneath the glass surface.

### Translucency System

The translucency system operates on a spectrum rather than discrete tiers. However, Apple defines four practical material weights for developers:

- **Ultra-thin glass** — Barely visible tint, maximum background passthrough. Used for large surfaces where content beneath must remain fully readable (e.g., full-screen overlays during media playback).
- **Thin glass** — Light tint with subtle refraction. The default for navigation bars, tab bars, and toolbars. Background content is visible but softened.
- **Regular glass** — Moderate tint and blur. Used for popovers, action sheets, and modal presentations. Provides clear visual separation while maintaining environmental context.
- **Thick glass** — Heavy tint approaching opacity. Used for alerts, critical dialogs, and contexts where background content would be distracting. Still technically translucent but functionally near-opaque.

### Vibrancy Levels

Vibrancy controls how text and icons render on glass surfaces. It uses compositing blend modes to ensure legibility regardless of the background content:

- **Primary vibrancy** — Full contrast. For titles, primary labels, and interactive elements. Uses "vibrant light" or "vibrant dark" compositing depending on the interface style.
- **Secondary vibrancy** — Reduced contrast (approximately 60% relative to primary). For subtitles, secondary labels, and supplementary information.
- **Tertiary vibrancy** — Minimal contrast (approximately 30%). For placeholder text, disabled states, and decorative elements.
- **Quaternary vibrancy** — Near-invisible (approximately 15%). For separator lines and the faintest structural hints.

Vibrancy is not opacity. Setting label opacity to 0.6 produces muddy, illegible text on glass. Vibrancy uses additive or subtractive blend modes that maintain sharpness at any contrast level.

### Material Types

| Material | Background Blur Radius | Saturation Boost | Use Case |
|----------|----------------------|------------------|----------|
| `ultraThinMaterial` | 8pt | 1.2x | Full-screen ambient overlays |
| `thinMaterial` | 16pt | 1.4x | Navigation bars, tab bars |
| `regularMaterial` | 24pt | 1.6x | Popovers, sheets |
| `thickMaterial` | 40pt | 1.8x | Alerts, critical modals |
| `ultraThickMaterial` | 64pt | 2.0x | Focused input contexts |

### Tab Bar Specifications

The iOS 26 tab bar is a floating element:

- **Shape**: Capsule (fully rounded ends), not a rectangle pinned to screen edge
- **Position**: Floating 8pt above the bottom safe area inset
- **Height**: 49pt (compact), 56pt (regular)
- **Material**: `thinMaterial` with 1pt specular highlight on top edge
- **Corner radius**: Full capsule (height / 2)
- **Icon size**: 24x24pt (SF Symbols, medium weight)
- **Label typography**: SF Pro Text, 10pt, medium weight, secondary vibrancy
- **Selected state**: Filled SF Symbol variant + primary vibrancy + circular tinted background (accent color at 20% opacity)
- **Spacing**: Equal distribution with minimum 44pt tap targets per item
- **Maximum items**: 5 (additional items overflow to "More" tab)
- **Scroll behavior**: Collapses to a compact pill showing only the selected icon on scroll-down; re-expands on scroll-up or tap

### Navigation Bar Specifications

- **Height**: 44pt (standard), 96pt (large title)
- **Material**: `thinMaterial`, matching the tab bar material for visual unity
- **Large title font**: SF Pro Display, 34pt, bold
- **Standard title font**: SF Pro Text, 17pt, semibold
- **Large-to-standard transition**: Title shrinks and moves to center on scroll, driven by scroll offset (not a snap, a continuous interpolation)
- **Back button**: Chevron (SF Symbol `chevron.backward`) + previous screen title, 17pt, accent color
- **Safe area**: Content insets below the nav bar glass, never renders beneath it

### Blur Values and Rendering

- Blur is Gaussian, applied to a snapshot of the content layer beneath the glass
- Blur radius is measured in points, not pixels (retina-independent)
- Saturation boost prevents the blur from appearing "washed out" — colors behind the glass stay vivid
- A specular highlight (1pt, white at 10-15% opacity) runs along the top edge of every glass surface to simulate a physical glass bevel
- In Dark Mode, the specular highlight shifts to white at 5-8% opacity and a subtle inner shadow appears at the bottom edge

### When to Use Glass vs Solid

| Context | Recommendation | Reason |
|---------|---------------|--------|
| Chrome (bars, toolbars) | Glass | Users expect to see content continuity |
| Cards in scrollable lists | Solid | Glass-on-glass creates visual noise and rendering cost |
| Full-screen content (video, photo) | Solid or ultra-thin | Content is the focus, glass distracts |
| Modals and sheets | Glass (regular) | Maintains spatial context |
| Text-heavy reading views | Solid | Glass behind paragraphs of text reduces readability |
| Interactive controls (buttons) | Solid with tint | Glass buttons lack the affordance of tappability |
| Onboarding overlays | Glass (thick) | Focus attention while showing the app beneath |

### Liquid Glass Color Tinting

Glass surfaces can be tinted with the app's accent color:

- **Tint intensity**: 5-15% of the accent color blended into the glass material
- **Automatic adjustment**: iOS modulates tint intensity based on the luminance of the background content. Over bright backgrounds, tint increases to remain visible. Over dark backgrounds, tint decreases to avoid muddiness.
- **Per-element tinting**: Individual glass elements (e.g., the selected tab indicator) can carry a stronger tint (20-30%) to indicate selection state
- **System colors**: Using system accent colors guarantees accessibility. Custom tint colors must pass APCA contrast checks against both light and dark backgrounds.

### Floating Tab Bar Behavior

The floating tab bar introduced in iOS 26 has distinct behavioral states:

1. **Resting** — Full capsule with icons and labels, floating above content
2. **Scrolling down** — Shrinks to a compact pill (icons only, no labels), reducing content occlusion
3. **Scrolling up** — Re-expands to full capsule with a spring animation (damping 0.8, response 0.35s)
4. **Long press** — Reveals a context menu for the tapped tab (e.g., "Open in New Window" on iPad)
5. **Hidden** — Fully dismissed during immersive content (video playback, full-screen maps). A swipe-up from the bottom edge re-summons it.

### SF Symbols Integration

SF Symbols 7 is tightly coupled with Liquid Glass:

- **Rendering modes**: Monochrome (single vibrancy color), Hierarchical (primary/secondary/tertiary layers), Palette (custom multi-color), Multicolor (system-defined full color)
- **Variable color**: Symbols animate through fill levels (0.0 to 1.0) to indicate progress, signal strength, or volume
- **Symbol effects**: Bounce, pulse, variable color, scale, appear, disappear, replace, wiggle, rotate, breathe
- **Preferred weight on glass**: Medium (not regular). Medium weight maintains legibility against translucent backgrounds.
- **Preferred scale on glass**: Medium (not small). Minimum 22x22pt bounding box for tap targets.
- **Automatic vibrancy**: When placed on a glass material, SF Symbols automatically adopt the appropriate vibrancy level based on their label style assignment

---

## 2. Material Design 3 Expressive

### Dynamic Color (Tonal Palettes from Source Color)

Dynamic Color extracts a source color from the user's wallpaper and generates a complete tonal palette:

1. **Source color extraction** — The system samples the wallpaper and selects a representative hue using the HCT (Hue, Chroma, Tone) color space
2. **Tonal palette generation** — From the source hue, five tonal palettes are generated:
   - **Primary** — The source hue at varying tones (0-100)
   - **Secondary** — Source hue with reduced chroma (more muted)
   - **Tertiary** — Complementary or analogous hue (system-chosen for harmony)
   - **Neutral** — Source hue at minimal chroma (near-gray with a hint of warmth/coolness)
   - **Neutral Variant** — Slightly more chromatic neutral
3. **Tone mapping** — Each palette has 13 tonal stops: 0, 10, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 95, 98, 99, 100
4. **Role assignment** — Design tokens like `colorPrimary`, `colorOnPrimary`, `colorSurface`, `colorOnSurface` are mapped to specific tonal stops
5. **Light/dark switching** — Light theme uses high-tone backgrounds (tone 98-99) with low-tone text (tone 10-20). Dark theme inverts: low-tone backgrounds (tone 6-10) with high-tone text (tone 80-90).

### Motion System

M3 Expressive uses spring physics, not cubic beziers:

- **Emphasized motion** — Mass: 1.0, Stiffness: 300, Damping ratio: 0.8. For hero transitions, page changes, and large-scale movements. Overshoots slightly before settling.
- **Standard motion** — Mass: 1.0, Stiffness: 500, Damping ratio: 1.0 (critically damped). For small UI responses, button presses, toggles. No overshoot.
- **Spatial motion paths** — Elements moving across the screen follow arced paths, not straight lines. The arc is computed using a control point offset perpendicular to the start-end vector.
- **Stagger patterns** — Lists and grids animate children with a 20-40ms stagger delay per item, creating a cascade effect. Maximum total stagger duration: 300ms.
- **Shared element transitions** — An element morphs between two screens using a container transform animation that interpolates position, size, corner radius, and elevation simultaneously.

### Shape System (Morph Shapes)

M3 Expressive introduces 35 shape tokens organized into families:

| Family | Corner Style | Use Case |
|--------|-------------|----------|
| **Extra Small** | 4dp radius | Chips, small badges |
| **Small** | 8dp radius | Cards, text fields |
| **Medium** | 12dp radius | Dialogs, menus |
| **Large** | 16dp radius | Sheets, FAB |
| **Extra Large** | 28dp radius | Large surfaces, navigation drawer |
| **Full** | 50% radius (circle/pill) | FAB in resting, avatar, pill buttons |

Morph shapes animate between corner families during state transitions. A FAB morphing into a bottom sheet transitions from Full to Extra Large with a spring animation.

### Component Theming

Every M3 component exposes a theming API with three layers:

1. **Color scheme** — Automatically applied from Dynamic Color. Components consume role tokens, not raw colors.
2. **Shape scheme** — Corner radius, corner family (rounded, cut). Applied per component size variant.
3. **Typography scheme** — Text style assignment per component element (headline, body, label).

Overriding a theme at the component level uses the `*Defaults` and `*Colors` Compose APIs:

```kotlin
ButtonDefaults.buttonColors(
    containerColor = MaterialTheme.colorScheme.tertiary,
    contentColor = MaterialTheme.colorScheme.onTertiary
)
```

### Elevation with Tonal Surfaces

M3 replaced drop shadows with tonal elevation:

| Elevation Level | Shadow | Tonal Overlay | Use Case |
|----------------|--------|---------------|----------|
| Level 0 | None | None | Flat surfaces |
| Level 1 | None | +3% primary | Cards, list items |
| Level 2 | None | +5% primary | Elevated cards, menus |
| Level 3 | Subtle | +8% primary | Navigation drawer, FAB |
| Level 4 | Medium | +11% primary | App bar (scrolled state) |
| Level 5 | Prominent | +14% primary | Modal bottom sheet |

Tonal overlay means the surface color shifts toward the primary color as elevation increases. This replaces the "gray shadow" model with a more colorful, dynamic depth system.

### Typography Scale

| Role | Font | Size | Weight | Line Height | Tracking |
|------|------|------|--------|-------------|----------|
| Display Large | Brand/Serif | 57sp | 400 | 64sp | -0.25sp |
| Display Medium | Brand/Serif | 45sp | 400 | 52sp | 0sp |
| Display Small | Brand/Serif | 36sp | 400 | 44sp | 0sp |
| Headline Large | Brand/Sans | 32sp | 400 | 40sp | 0sp |
| Headline Medium | Brand/Sans | 28sp | 400 | 36sp | 0sp |
| Headline Small | Brand/Sans | 24sp | 400 | 32sp | 0sp |
| Title Large | Sans | 22sp | 400 | 28sp | 0sp |
| Title Medium | Sans | 16sp | 500 | 24sp | 0.15sp |
| Title Small | Sans | 14sp | 500 | 20sp | 0.1sp |
| Body Large | Sans | 16sp | 400 | 24sp | 0.5sp |
| Body Medium | Sans | 14sp | 400 | 20sp | 0.25sp |
| Body Small | Sans | 12sp | 400 | 16sp | 0.4sp |
| Label Large | Sans | 14sp | 500 | 20sp | 0.1sp |
| Label Medium | Sans | 12sp | 500 | 16sp | 0.5sp |
| Label Small | Sans | 11sp | 500 | 16sp | 0.5sp |

### Material You Personalization

Material You goes beyond color. The full personalization stack includes:

- **Wallpaper-derived color** — Dynamic Color tonal palettes (described above)
- **Themed icons** — App icons on the home screen adopt the user's tonal palette as a monochrome tint
- **Widget theming** — Glance widgets consume `DynamicColors` to blend with the home screen
- **Clock face and lock screen** — The lock screen clock uses Display Large typography with the primary color from the user's wallpaper
- **Cross-device sync** — The selected wallpaper color syncs across phone, tablet, Wear OS watch, and Chromebook via the user's Google account

---

## 3. Modern CSS 2025-2026

### Container Queries (`@container`)

Container queries allow components to respond to their parent container's size rather than the viewport:

```css
.card-grid {
  container-type: inline-size;
  container-name: card-grid;
}
@container card-grid (min-width: 600px) {
  .card { grid-template-columns: 1fr 1fr; }
}
@container card-grid (min-width: 900px) {
  .card { grid-template-columns: 1fr 1fr 1fr; }
}
```

Container query units: `cqw` (container query width), `cqh` (height), `cqi` (inline), `cqb` (block), `cqmin`, `cqmax`. Use `cqi` for fluid typography within containers: `font-size: clamp(1rem, 3cqi, 1.5rem)`.

### `:has()` Selector

The parent selector CSS never had until now. Select elements based on their descendants:

```css
/* Card with an image gets different padding */
.card:has(img) { padding: 0; }
/* Form group with invalid input shows error styling */
.form-group:has(:invalid) { border-color: var(--color-error); }
/* Nav with more than 5 items switches to hamburger */
nav:has(> :nth-child(6)) { /* hamburger layout */ }
```

### View Transitions API

Page and state transitions with cross-fade, morph, and slide animations:

```css
::view-transition-old(main) {
  animation: fade-out 200ms ease-out;
}
::view-transition-new(main) {
  animation: fade-in 300ms ease-in;
}
.hero-image {
  view-transition-name: hero;
}
```

Multi-page view transitions (MPA) work across full page navigations. Same-document view transitions use `document.startViewTransition()` for SPA-style morphs.

### Anchor Positioning

Position elements relative to other elements without JavaScript:

```css
.tooltip {
  position: fixed;
  position-anchor: --trigger;
  top: anchor(--trigger bottom);
  left: anchor(--trigger center);
  position-try-fallbacks: flip-block, flip-inline;
}
.trigger {
  anchor-name: --trigger;
}
```

`position-try-fallbacks` provides automatic repositioning when the anchored element would overflow the viewport.

### CSS Nesting

Native nesting without preprocessors:

```css
.card {
  background: var(--surface);
  & .title { font-size: var(--title-md); }
  & .body { color: var(--on-surface-variant); }
  &:hover { box-shadow: var(--elevation-2); }
  @media (width >= 768px) {
    & { flex-direction: row; }
  }
}
```

### `@scope`

Scoped styles that apply only within a defined subtree:

```css
@scope (.card) to (.card-footer) {
  p { margin-block: 0.5em; }
  a { color: var(--primary); }
}
```

Styles apply from `.card` down to but not including `.card-footer`. Prevents style leakage in component architectures.

### Scroll-Driven Animations

Bind animations to scroll progress instead of time:

```css
@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.reveal {
  animation: fade-in linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}
```

Two timeline types: `scroll()` (tracks scroll container progress) and `view()` (tracks element visibility within scroll container).

### Subgrid

Child elements inherit the parent grid's track sizing:

```css
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3; /* Aligns internal rows with siblings */
}
```

Subgrid solves the "cards with different content heights but aligned internal rows" problem that has plagued CSS grid layouts.

### `@layer` Cascade Layers

Control the cascade priority without specificity wars:

```css
@layer reset, base, components, utilities;
@layer reset { * { margin: 0; box-sizing: border-box; } }
@layer base { body { font-family: var(--font-sans); } }
@layer components { .btn { /* ... */ } }
@layer utilities { .sr-only { /* ... */ } }
```

Layers declared later win over earlier layers regardless of selector specificity. Unlayered styles beat all layers.

### `@property` Registered Custom Properties

Type-safe custom properties with animation support:

```css
@property --hue {
  syntax: "<number>";
  initial-value: 220;
  inherits: true;
}
.element {
  --hue: 220;
  background: oklch(70% 0.15 var(--hue));
  transition: --hue 0.5s ease;
}
.element:hover { --hue: 280; }
```

Without `@property`, custom properties cannot be animated — they snap between values. With `@property`, the browser knows the type and can interpolate.

### `color-mix()`, `oklch()`, `oklab()`

```css
/* Mix two colors in oklch space */
--primary-soft: color-mix(in oklch, var(--primary) 60%, white);
/* Define colors in perceptually uniform space */
--accent: oklch(65% 0.2 145); /* lightness, chroma, hue */
/* Predictable lightness stepping for a tonal scale */
--tone-10: oklch(10% 0.05 var(--hue));
--tone-50: oklch(50% 0.12 var(--hue));
--tone-90: oklch(90% 0.04 var(--hue));
```

oklch produces perceptually uniform lightness steps. HSL does not — `hsl(60, 100%, 50%)` (yellow) appears far brighter than `hsl(240, 100%, 50%)` (blue) at the same declared lightness.

### `light-dark()`

Single-declaration light/dark mode values:

```css
:root { color-scheme: light dark; }
body {
  background: light-dark(#ffffff, #1a1a1a);
  color: light-dark(#111111, #eeeeee);
}
```

Eliminates the need for duplicate custom properties or `prefers-color-scheme` media queries for simple value swaps.

### `field-sizing`, Popover API, `<dialog>`

- **`field-sizing: content`** — Textarea and input elements auto-size to their content. No JavaScript auto-resize needed.
- **Popover API** — `<div popover>` creates a top-layer element with built-in light-dismiss, focus trapping, and stacking context. Replaces custom tooltip/dropdown JavaScript.
- **`<dialog>`** — Native modal with `::backdrop`, `showModal()`, auto-focus management, and Escape-to-close. The `<dialog>` element sits in the top layer, above all stacking contexts.

---

## 4. Watch / Wear OS Design

### Apple Watch Specifications by Size

| Case Size | Screen Width | Screen Height | Corner Radius | Scale Factor |
|-----------|-------------|---------------|---------------|-------------|
| 42mm (SE) | 176px | 215px | 36px | 2x |
| 44mm (S10) | 198px | 242px | 36px | 2x |
| 46mm (S10) | 208px | 254px | 40px | 2x |
| 49mm (Ultra 3) | 205px | 251px | 40px | 2x |

### Complication Design

Complications are small data displays on the watch face:

- **Circular Small** — 32x32pt. Icon or single metric only.
- **Modular Small** — 52x52pt. Short text or icon with one data point.
- **Modular Large** — Full width (varies). Multi-line content: title + up to 3 lines of body.
- **Rectangular** — 154x68pt (varies by watch size). Rich content: images, gauges, text combinations.
- **Corner** — Curved text along the watch face edge. Maximum 4-5 characters.

Design rules: complications must be readable at arm's length (approximately 30cm). Use SF Compact Rounded for complication text. Minimum font size 13pt. Tint color should be a single accent per complication.

### Glanceable Information Hierarchy

Watch content must be parsed in under 3 seconds:

1. **Primary metric** — The single most important number/status. Largest text, highest contrast.
2. **Context label** — What the metric means. Secondary vibrancy, smaller text.
3. **Trend indicator** — Arrow, spark line, or color shift showing direction.
4. **Action hint** — One obvious tap target or instruction. Maximum one action per screen.

Never show more than 3 information groups on a single watch screen. If content requires scrolling, use a paginated layout (vertical page dots), not a long scroll.

### Crown and Bezel Interactions

- **Digital Crown scroll** — Default scroll behavior for lists. Haptic detents every 4pt of scroll offset.
- **Digital Crown precise input** — Used for pickers (time, date, numeric). Each detent maps to one value step.
- **Bezel rotation (Wear OS)** — Equivalent to Digital Crown. Rotary input events map to scroll or value selection.
- **Double-tap gesture (Apple Watch)** — Primary hand gesture for one-handed interaction. Maps to the "primary action" on the current screen.

### Small Screen Typography

| Role | Font | Size | Weight |
|------|------|------|--------|
| Large Title | SF Compact Rounded | 22pt | Bold |
| Headline | SF Compact Rounded | 17pt | Semibold |
| Body | SF Compact Rounded | 15pt | Regular |
| Caption | SF Compact Rounded | 13pt | Regular |
| Minimum readable | SF Compact Rounded | 11pt | Medium |

Line lengths: maximum 20-25 characters per line on a 44mm watch. Use sentence fragments, not full sentences. Abbreviate aggressively: "Mon" not "Monday", "3h 22m" not "3 hours 22 minutes".

---

## 5. TV / 10-Foot UI

### Focus-Based Navigation

TV interfaces have no cursor or touch. Navigation is entirely focus-based:

- **Focus ring** — A visible highlight (border, scale, or glow) indicating the currently focused element. Minimum 4px visible border or 1.05x scale increase.
- **Focus movement** — D-pad (up/down/left/right) moves focus between elements. Focus movement must be predictable: pressing "right" should move to the element visually to the right.
- **Focus memory** — When a user navigates away from a section and returns, focus should restore to the last-focused element within that section.
- **Focus trapping** — Modals and overlays trap focus within their bounds. D-pad navigation cycles through the modal's focusable elements.

### Overscan Safe Area

Legacy TVs crop the outer edges of the signal. Even modern TVs may overscan slightly:

- **Action safe area** — 5% inset from all edges (where interactive elements must live)
- **Title safe area** — 10% inset from all edges (where text must live)
- **Modern practice** — Most streaming apps use a 48px inset from all edges as a safe margin on 1080p, or 96px on 4K

### Reading Distance Typography

TV viewers sit 2-3 meters from the screen. Typography must be sized accordingly:

| Role | Minimum Size (1080p) | Minimum Size (4K) | Notes |
|------|---------------------|--------------------|-------|
| Hero title | 48px | 72px | Maximum 2 lines |
| Section title | 32px | 48px | Single line preferred |
| Card title | 24px | 36px | Maximum 2 lines |
| Metadata/subtitle | 18px | 28px | Single line |
| Minimum readable | 16px | 24px | Never go below this |

Font weight: use medium to bold weights. Thin and light weights disappear at TV viewing distance. Prefer sans-serif families with open counters and generous x-height.

### D-Pad Navigation Patterns

- **Grid navigation** — Focus moves in a 2D grid. Arrow keys move one cell. Wrap-around is optional but must be consistent (all rows wrap or none do).
- **Rail/carousel navigation** — Horizontal list of cards. Left/right moves between cards. Up/down exits the rail to the rail above/below.
- **Nested focus** — Pressing Select on a card expands it or navigates into a detail view. Back button returns to the previous focus context.
- **Long-press** — Reserved for secondary actions (add to watchlist, info panel). Never required for primary interactions.

### Remote Control UX

- **Minimize button count** — Assume 5 buttons: D-pad (4 directions + select) and Back. Design every flow to be completable with these 5 inputs.
- **Voice search** — Provide voice input as a shortcut for text entry. On-screen keyboards are painful with D-pad navigation.
- **Idle timeout** — If no input for 4+ hours, show a "still watching?" prompt to avoid burning static UI into OLED panels.

### Card-Based Layouts

TV UI is overwhelmingly card-based:

- **Standard card** — 16:9 landscape thumbnail with title below. Focus state scales the card to 1.05x-1.1x with an elevation increase.
- **Wide card** — 2.39:1 cinematic ratio for hero/featured content.
- **Tall card** — 2:3 portrait for book covers, profiles, app icons.
- **Card spacing** — 16-24px gap between cards. Enough to clearly separate but not so much that the screen feels empty.
- **Row labels** — Left-aligned, above each carousel rail. 24-32px font size with 16px gap to the first card.

---

## 6. Automotive / HUD

### Driver Distraction Guidelines

The National Highway Traffic Safety Administration (NHTSA) defines strict limits:

- **Single glance time** — Maximum 2 seconds per glance away from the road
- **Total task time** — Maximum 12 seconds cumulative for any single task (e.g., setting a destination)
- **Total glances** — Maximum 6 glances for a single task
- **Eyes-off-road time** — 85th percentile total eyes-off-road time must not exceed 12 seconds

These are not suggestions. Automotive OEMs certify against these guidelines. Infotainment UI that exceeds these limits can result in regulatory action.

### NHTSA Compliance Checklist

1. No scrolling text or animations that require sustained attention
2. No tasks requiring more than 6 sequential inputs
3. Voice-first for any task exceeding the 12-second glance budget
4. Automatic lockout of complex functions when the vehicle is in motion (above 5 mph)
5. Haptic or audio confirmation for every touch input (driver cannot look to confirm)
6. No video playback on the driver-facing display while in motion

### Glance Time Limits by Content Type

| Content | Max Glance | Interaction |
|---------|-----------|-------------|
| Current song / station | 1s | None (read-only) |
| Navigation next turn | 1s | None (read-only) |
| Temperature adjustment | 1.5s | Single tap or voice |
| Contact selection | 2s | Voice-preferred |
| Destination entry | Voice only | Text entry locked at speed |
| Message reading | Voice only | Read aloud, never displayed |

### Night Mode

Automotive displays must support an aggressive night mode:

- **Background**: Pure black (#000000) to minimize light emission
- **Text**: Amber or red-shifted white (color temperature 2700K-3200K) to preserve scotopic (night) vision
- **Brightness**: Auto-dimming to 1-5 nits in full darkness (phone screens are typically 200-1000 nits)
- **No white surfaces**: Even "light gray" backgrounds can cause glare on the windshield
- **HUD (head-up display)**: Green or white monochrome, 15-25pt text projected at optical infinity (focused at 2-3 meters ahead of the windshield)

### Large Touch Targets

Drivers interact with gloved hands, without looking, while the vehicle vibrates:

- **Minimum touch target**: 18mm x 18mm (approximately 72px at typical automotive DPI)
- **Recommended touch target**: 24mm x 24mm
- **Spacing between targets**: Minimum 8mm gap
- **Physical controls preferred**: Climate, volume, and hazard lights should remain physical knobs/buttons, not touchscreen-only

### Voice-First Interaction

For tasks exceeding a single glance:

- Voice is the primary input, touch is the fallback
- Provide confirmation prompts: "Navigating to 123 Main Street. Is that correct?"
- Wake word should be configurable (users in noisy environments may prefer push-to-talk)
- Visual feedback for voice state: listening, processing, confirming (simple icon states, not text)

---

## 7. Spatial / XR Design (visionOS)

### Depth and Layering

visionOS places UI at specific depths in the user's physical space:

- **Windows** — 2D content panels floating at arm's length (approximately 1-2 meters from the user). Default depth: 0 (the "base plane").
- **Volumes** — 3D content containers. Objects within a volume have real depth and can be viewed from different angles.
- **Full Spaces** — Immersive environments that replace or augment the user's entire visual field.

Layering rules:
- Glass windows sit at depth 0
- Popovers and menus sit at depth +20pt (closer to user)
- Alerts sit at depth +40pt
- Never place interactive UI behind the base plane (negative depth). Users cannot comfortably focus on content behind them.

### Eye Tracking Targets

Eye tracking replaces cursor hover on visionOS:

- **Minimum target size**: 60x60pt (eye tracking has lower precision than touch or cursor)
- **Hover effect**: Elements subtly highlight when the user's gaze lands on them. A gentle scale-up (1.02x) and specular highlight shift indicates "this is focusable."
- **Gaze duration**: Do not trigger actions on gaze alone. Gaze selects, pinch confirms. Avoid dwell-to-activate patterns (they cause Midas touch problems).
- **Gaze feedback latency**: Hover effects must appear within 50ms of gaze landing. Any delay feels unresponsive in spatial UI.

### Hand Tracking Gestures

| Gesture | Action | Notes |
|---------|--------|-------|
| Pinch (index + thumb) | Select / tap | Primary interaction. Works at any hand position in view. |
| Pinch and drag | Scroll, move, resize | Equivalent to touch drag |
| Two-hand pinch and pull | Zoom / scale | Both hands pinch, then move apart |
| Wrist rotation | Fine adjustment | Used in precision controls (e.g., 3D rotation) |
| Open palm push | Dismiss | Push a window away to close it |

Design for indirect interaction: the user's hands rest in their lap, not reaching toward the UI. Gestures are detected by downward-facing cameras, so all hand gestures must work in a low, relaxed hand position.

### Spatial Audio

- UI sounds should be spatialized to the source window's position. A notification from a window to the user's left should sound like it comes from the left.
- Ambient sounds (background music, environment audio) should be non-directional (omnidirectional).
- Feedback sounds (tap, toggle, error) should be subtle and spatialized. Loud or harsh sounds are jarring in a head-mounted context.

### Window Placement and Ornaments

- **Default placement**: New windows appear centered in the user's forward gaze, at approximately 1.5 meters distance.
- **Window bar**: A grab handle at the bottom of every window allows repositioning. Users can place windows anywhere in their space.
- **Ornaments**: Small UI elements (toolbars, tab bars) that float just outside the window's edge. Ornaments are attached to the window and move with it.
- **Window size**: Recommended minimum 800x600pt. Maximum varies by content but avoid exceeding 2000pt in any dimension (requires excessive head movement to scan).
- **Multi-window**: Users can open multiple windows simultaneously. Design for the possibility that your app is one of several visible apps.

### Passthrough Considerations

In augmented reality (passthrough) mode, the user sees their real environment with your UI overlaid:

- Glass materials work exceptionally well because they harmonize with any physical background
- Avoid large opaque surfaces that block the user's view of their room
- Dark mode is generally preferred in passthrough: it minimizes the "floating screen" effect
- Shadows cast by windows onto the passthrough feed increase the sense of physical presence
- Test your UI against diverse real-world backgrounds (bright window, dark room, cluttered desk)

---

## 8. Cross-Platform Harmony (9 Device Types)

### Device Matrix

| Device | Screen Range | Input | Viewing Distance | Primary Context |
|--------|-------------|-------|-------------------|----------------|
| Phone | 320-430pt width | Touch | 30cm (handheld) | Mobile, one-handed |
| Tablet | 744-1024pt width | Touch + Pencil | 40-50cm (lap/table) | Lean-back, productivity |
| Desktop | 1024-2560pt width | Mouse + keyboard | 50-70cm (desk) | Focused work |
| Watch | 162-205px width | Crown + tap | 25-30cm (wrist) | Glanceable |
| TV | 1920-3840px width | D-pad + voice | 2-4 meters (couch) | Lean-back entertainment |
| Car | 800-1920px width | Touch + voice | 50-70cm (dash) | Distracted, safety-critical |
| XR Headset | Virtual canvas | Eye + hand | 1-3m (virtual) | Immersive |
| Foldable | 320-886pt width | Touch | 30-40cm (handheld) | Dual-mode |
| E-Ink | 758-1872px width | Touch (slow) | 30cm (handheld) | Reading, low-power |

### Shared Design Tokens

A cross-platform design system defines tokens at three levels:

1. **Global tokens** — Platform-agnostic values: brand colors (oklch), font scale ratios, spacing multipliers, border-radius scale
2. **Alias tokens** — Semantic mappings: `color-surface`, `color-on-surface`, `spacing-md`, `radius-card`. Same name everywhere, different values per platform.
3. **Component tokens** — Platform-specific overrides: `button-height` is 44pt on iOS, 48dp on Android, 36px on web, 72px on TV.

### Platform-Specific Adaptations

| Pattern | iOS | Android | Web | Watch | TV |
|---------|-----|---------|-----|-------|-----|
| Primary nav | Bottom tab bar (floating) | Bottom nav bar | Top nav or sidebar | Page-based scroll | Top rail + sidebar |
| Back navigation | Swipe from left edge | System back button/gesture | Browser back or breadcrumb | Swipe right | Back button on remote |
| Selection | Checkmark | Checkbox | Checkbox | Tap highlight | Focus + select |
| Destructive action | Swipe-to-delete | Long-press menu | Button with confirmation | Force Touch menu | Focus + hold |
| Search | Pull-down search bar | Top app bar search | Search field in header | Scribble or voice | Voice or on-screen keyboard |

### Responsive Breakpoints by Device

| Breakpoint | Width | Target |
|-----------|-------|--------|
| xs | 0-319pt | Small watch |
| sm | 320-430pt | Phone |
| md | 431-743pt | Large phone / foldable inner |
| lg | 744-1023pt | Tablet |
| xl | 1024-1365pt | Small desktop / tablet landscape |
| 2xl | 1366-1920pt | Standard desktop |
| 3xl | 1921pt+ | Large desktop / TV |

### Foldable-Specific Considerations

- **Outer screen** — Treat as phone (320-430pt). Show condensed single-column layout.
- **Inner screen (unfolded)** — Treat as small tablet (744-886pt). Show two-pane layout.
- **Fold-aware layout** — Content should not cross the fold hinge. Place the layout seam on the hinge, creating a natural two-pane boundary.
- **Continuity** — When the user unfolds the device, the app must seamlessly transition from the outer layout to the inner layout without losing state or scroll position.

### E-Ink Considerations

- **No animation** — E-ink refresh is 200-500ms. Animations appear as ghostly smears. Use instant state changes.
- **High contrast** — E-ink displays have lower contrast ratios than LCD/OLED. Use pure black on pure white. Avoid grays below #333333 or above #CCCCCC.
- **No color dependency** — Most e-ink displays are grayscale. Never encode meaning in color alone.
- **Large text** — Minimum 14pt body text. E-ink pixel density is typically 212-300 PPI (lower than phones at 400-600 PPI).
- **Minimal chrome** — Every pixel of UI chrome is a pixel not showing content. On a reading device, content is everything.

---

## 9. Platform Detection Patterns

### When to Adapt vs When to Unify

**Adapt to the platform** when:
- The OS provides a native control that users expect (e.g., iOS date picker, Android bottom sheet)
- Navigation patterns differ fundamentally (tab bar vs navigation drawer)
- System gestures conflict with custom gestures (iOS swipe-back, Android system back)
- Accessibility APIs differ (VoiceOver vs TalkBack rotor patterns)
- Legal requirements differ by platform (NHTSA for automotive, WCAG for web)

**Unify across platforms** when:
- Brand identity requires visual consistency (color palette, typography, iconography)
- The interaction is domain-specific and has no platform equivalent (e.g., a custom chart interaction)
- Users frequently switch between platforms and expect continuity (e.g., Figma on web vs desktop app)
- The cost of maintaining platform-specific implementations exceeds the UX benefit

### User Expectations Per Platform

| Platform | Users Expect | Users Reject |
|----------|-------------|-------------|
| iOS | Smooth 60fps, system gestures respected, Liquid Glass materials, SF Symbols | Android-style hamburger menus, Material FABs, system font overrides |
| Android | Material components, Dynamic Color, predictable back behavior | iOS-style non-standard back navigation, tab bars without labels |
| Web | Fast load times, keyboard accessibility, URL-based state, responsive | Native app idioms forced onto web (e.g., mobile tab bar on desktop) |
| Watch | Instant information, minimal interaction, complications | Full-screen forms, long text, complex navigation hierarchies |
| TV | Focus-visible at all times, large text, card grids | Tiny text, hover-dependent interactions, touch assumptions |
| Car | Voice-first, huge touch targets, zero cognitive load | Text-heavy displays, small buttons, multi-step flows |
| XR | Spatial depth, gaze responsiveness, comfortable ergonomics | Flat 2D panels with no spatial awareness, tiny targets |

---

## 10. Design Token Mapping Across Platforms

### CSS Custom Properties to SwiftUI Environment to Compose Theme

| Semantic Role | CSS Custom Property | SwiftUI | Compose (M3) |
|--------------|--------------------|---------|----|
| Primary color | `--color-primary` | `Color.accentColor` | `MaterialTheme.colorScheme.primary` |
| Surface | `--color-surface` | `Color(.systemBackground)` | `MaterialTheme.colorScheme.surface` |
| On-surface text | `--color-on-surface` | `Color(.label)` | `MaterialTheme.colorScheme.onSurface` |
| Error | `--color-error` | `Color(.systemRed)` | `MaterialTheme.colorScheme.error` |
| Border radius (sm) | `--radius-sm: 8px` | `.clipShape(RoundedRectangle(cornerRadius: 8))` | `shape = RoundedCornerShape(8.dp)` |
| Border radius (lg) | `--radius-lg: 16px` | `.clipShape(RoundedRectangle(cornerRadius: 16))` | `shape = RoundedCornerShape(16.dp)` |
| Spacing unit | `--space-md: 16px` | `.padding(16)` | `Modifier.padding(16.dp)` |
| Elevation (low) | `box-shadow: 0 1px 3px` | `.shadow(radius: 2)` | `tonalElevation = 1.dp` |
| Elevation (high) | `box-shadow: 0 8px 24px` | `.shadow(radius: 8)` | `tonalElevation = 4.dp` |
| Body font | `font-family: var(--font-body)` | `.font(.body)` | `MaterialTheme.typography.bodyLarge` |
| Title font | `font-family: var(--font-title)` | `.font(.title)` | `MaterialTheme.typography.titleLarge` |
| Caption font | `font-family: var(--font-caption)` | `.font(.caption)` | `MaterialTheme.typography.labelSmall` |

### Token Translation Strategy

1. **Define once in a neutral format** — Use JSON or YAML as the source of truth (e.g., Style Dictionary, Tokens Studio)
2. **Transform per platform** — Generate CSS custom properties, SwiftUI extensions, and Compose theme objects from the same source
3. **Override at the platform layer** — iOS gets `thinMaterial` for surface, Android gets tonal elevation, web gets `backdrop-filter: blur()`
4. **Test with a visual diff** — Render the same screen on all three platforms and compare. Token mapping is correct when the screens feel like siblings, not clones.

### Token File Structure

```
tokens/
  global/
    color.json        # oklch values, brand palette
    spacing.json      # 4px base unit scale
    typography.json    # font scale ratios
    radius.json       # border-radius scale
  platform/
    ios.json          # SwiftUI overrides, Liquid Glass materials
    android.json      # M3 overrides, Dynamic Color hooks
    web.json          # CSS custom property names, rem conversions
    watch.json        # Compact sizing overrides
    tv.json           # 10-foot UI sizing overrides
    car.json          # Large touch target overrides
    xr.json           # Spatial depth tokens
```

---

## Cross-References

- **`visual-design-mastery`** — Visual principles that apply across all platforms. This skill adapts those principles to platform-specific conventions.
- **`mobile-ux-design`** — Mobile UX patterns. This skill provides the current visual standards those patterns render within.
- **`desktop-app-design`** — Desktop patterns. This skill provides web/macOS/Windows visual standards.
- **`component-patterns-code`** — Code implementations. This skill ensures code targets the right platform APIs.
- **`design-systems-architecture`** — Token architecture. This skill defines platform-specific token overrides.
- **`interaction-motion-design`** — Motion patterns. This skill provides platform-specific animation curves and APIs.
- **`accessibility-inclusive-design`** — Platform-specific accessibility APIs (VoiceOver, TalkBack, ARIA).

## Commands Powered by This Skill

| Command | How This Skill Is Used |
|---------|----------------------|
| `/grade` | Adapts visual direction to target platform conventions |
| `/component` | Generates platform-native component code |
| `/screen` | Uses platform-specific screen patterns and safe areas |
| `/responsive` | Cross-device adaptation using platform breakpoints |
| `/generate` | Informs AI generation prompts with platform constraints |
| `/generate` | Generates assets at platform-correct sizes and formats |
