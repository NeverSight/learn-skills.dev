---
name: liquid-glass
description: >-
  Generate web UI components with Apple's Liquid Glass aesthetic: real refraction,
  specular rims and spring motion, in plain CSS with an optional vanilla JS engine.
  Use this skill when creating or restyling navigation bars, tab bars, toolbars,
  sidebars, docks, modals, popovers, toasts, floating buttons, switches, sliders or
  any chrome/control layer element with a translucent glass appearance. Do NOT use
  for content-layer elements like article cards, table cells or feeds. Always
  enforce WCAG AA contrast and the reduced transparency, increased contrast, reduced
  motion and forced colors fallbacks.
license: MIT
metadata:
  version: "2.1.0"
  author: "jcm-developer"
  repo: "https://github.com/jcm-developer/liquid-glass-components"
---

# Liquid Glass: web design skill

Build accessible web components with Apple's Liquid Glass material using CSS, SVG and vanilla
JavaScript only.

## Quick start

1. Copy `snippets/tokens.css` and load it first.
2. Copy the component snippets you need (`snippets/glass-*.css`). The usage markup is in the
   docblock at the top of each file; use it as written.
3. Optional but recommended: copy `snippets/liquid-glass.js` and load it with `defer`. It adds
   real refraction to elements with `data-refract`, sliding selection indicators, switch
   toggling, slider fill and dock magnification.
4. For a custom glass element, use `.glass-surface` from `snippets/glass-surface.css`.

```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="glass-button.css">
<script src="liquid-glass.js" defer></script>

<button class="glass-btn" type="button" data-refract>Continue</button>
```

## Core principles

1. **Layer separation.** Glass belongs ONLY to the navigation/chrome layer: tab bars,
   toolbars, sidebars, docks, popovers, sheets, modals, toasts, floating buttons. NEVER on
   content (articles, feeds, table cells, list items).
2. **No glass on glass.** Never stack glass elements. Controls inside a glass surface use flat
   fills: `.glass-btn--plain`, `var(--glass-fill)`.
3. **Glass needs something behind it.** It reads over photos, video, maps, wallpapers and
   scrolling content. Over a flat colour it is just a tinted box.
4. **Concentric radii.** Inner radius = outer radius minus the padding between them.
5. **Accessibility first.** Every component includes fallbacks for reduced transparency,
   increased contrast, reduced motion and forced colours.
6. **Mobile budget.** At most 3 glass surfaces visible at once on mobile.

## The material

Liquid Glass is not frosted glass. It has three layers:

| Layer | What it does | Tokens |
|---|---|---|
| Refraction | Bends the backdrop at the bezel like the rim of a lens, with a slight chromatic fringe | `--glass-refraction`, `--glass-bezel`, `--glass-chroma` |
| Frost | A light blur: 2px with refraction, 8px without | `--glass-blur`, `--glass-blur-fallback` |
| Light | A faint tint, two specular rims (top-left strong, bottom-right soft) and a pointer sheen | `--glass-tint`, `--glass-rim` |

Refraction is a progressive enhancement: `liquid-glass.js` renders it through
`backdrop-filter: url()` in Chromium on desktop. Safari, Firefox, touch devices and users with
reduced transparency, increased contrast or forced colours get the CSS blur. Every component
must look complete without it.

## Design tokens

`snippets/tokens.css` holds everything. Key tokens:

| Token | Default | Purpose |
|---|---|---|
| `--glass-tint` | `0.08` | Surface fill opacity |
| `--glass-rim` | `0.6` | Specular rim intensity, 0 to 1 |
| `--glass-blur` | `2px` | Frost while refraction is active |
| `--glass-blur-fallback` | `8px` | Frost without refraction |
| `--glass-saturation` | `180%` | Backdrop saturation boost |
| `--glass-refraction` | `48` | Displacement strength in px |
| `--glass-bezel` | `22px` | Width of the curved lens edge |
| `--glass-chroma` | `0.5` | Chromatic dispersion, 0 to 1 |
| `--glass-press-scale` | `1.08` | How much a pressed control swells |
| `--glass-easing-spring` | `linear(...)` | Native CSS spring curve |

Override any primitive on any element (`style="--glass-tint: .2"`); derived tokens are
recomputed per component.

### Schemes

Glass adapts to what is **behind** it. The default scheme suits dark or colourful backdrops
(white text). `prefers-color-scheme: light` switches to the light scheme (dark text, denser
tint). Pin a scheme on any container: `data-glass-scheme="dark"` or `"light"`.

## Base glass surface

```css
.glass-surface {
  position: relative;
  isolation: isolate;
  border-radius: var(--glass-radius-lg);
  background: var(--glass-bg);
  -webkit-backdrop-filter: blur(var(--glass-blur-fallback)) saturate(var(--glass-saturation));
  backdrop-filter: blur(var(--glass-blur-fallback)) saturate(var(--glass-saturation));
  box-shadow: var(--glass-shadow-rim), var(--glass-shadow);
  outline: 1px solid transparent; /* becomes visible in forced-colors mode */
  outline-offset: -1px;
  color: var(--glass-text-primary);
  text-shadow: var(--glass-text-shadow);
}
```

`--glass-shadow-rim` is the specular light: two inset highlights and a faint inner glow. Do
not draw rims with `border-image` (incompatible with `border-radius`).

## Refraction

Add `data-refract` to a glass element and load `liquid-glass.js`. Tune per element with
`data-refract-strength`, `data-refract-bezel`, `data-refract-blur`, `data-refract-chroma`, or
globally with the tokens. After changing a `--glass-*` property from script, call
`LiquidGlass.refresh(el)`.

- Use it on a few prominent surfaces (bars, sheets, a hero control), not on every chip.
- Refraction cannot see past an ancestor with `opacity` below 1, `filter`, `mask`,
  `clip-path` or its own `backdrop-filter`. Keep glass outside such containers.
- Opt-outs on `<html>`: `data-glass-refract="off"`; on touch devices it is off unless
  `data-glass-refract="always"`.

## Interaction

- **Pressed controls grow** (`scale: var(--glass-press-scale)`) and light up from the press
  point. Never shrink a glass control on press.
- **Switch and slider thumbs turn into a clear lens while held** (`:active`).
- **Selections slide.** Tab bars, segmented controls and sidebars move a stretching indicator
  between items (`liquid-glass.js`); without the script the selected item keeps a static fill.
- **Springs** use `--glass-easing-spring` over `--glass-duration-spring` (600ms). Shorter
  durations cut the overshoot.
- Selection state lives in ARIA: `aria-selected`, `aria-checked`, `aria-current`.

## Mandatory accessibility fallbacks

Include all four in every component:

```css
@media (prefers-reduced-transparency: reduce) {
  .glass-surface {
    background: var(--glass-solid-bg);
    color: var(--glass-solid-text);
    -webkit-backdrop-filter: none !important;
    backdrop-filter: none !important;
  }
}

@media (prefers-contrast: more) {
  .glass-surface {
    background: var(--glass-solid-bg);
    color: var(--glass-solid-text);
    outline: 2px solid currentColor;
    box-shadow: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .glass-surface { transition: none; animation: none; }
}

@media (forced-colors: active) {
  .glass-surface {
    background: Canvas;
    color: CanvasText;
    outline: 1px solid CanvasText;
    -webkit-backdrop-filter: none !important;
    backdrop-filter: none !important;
    box-shadow: none;
  }
}
```

The `!important` matters: refraction is applied as an inline style.

## Variants

- **Regular** (default): bars, sidebars, popovers, sheets.
- **Clear** (`--clear`): controls over photos and video. On bright media add a
  `rgba(0, 0, 0, 0.35)` dimming layer behind the control.
- **Prominent** (`--prominent`): accent-tinted, for the single primary action.

## Typography on glass

- Minimum 16px for body text, 14px for metadata.
- Minimum font weight 500. Never 300 or lighter.
- Never `mix-blend-mode` on text.
- Use the system font stack first (`--glass-font-sans`): it renders SF Pro on Apple devices.
  Never redistribute SF Pro or SF Symbols.

## Focus indicators

Use the dual ring (black outline plus white ring) so focus is visible on any backdrop:

```css
.glass-btn:focus-visible {
  outline: 2px solid #000000;
  outline-offset: var(--glass-focus-offset);
  box-shadow: var(--glass-shadow-rim), var(--glass-focus-ring);
}
```

## Performance rules

1. At most 3 glass surfaces visible at once on mobile.
2. Never `will-change: backdrop-filter` (iOS memory crashes).
3. Never animate `backdrop-filter`; animate opacity, scale or translate instead.
4. `backdrop-filter` makes an element the containing block of its `position: fixed`
   children; render tooltips and menus outside glass containers.
5. Pause decorative animation behind glass when it is off screen.

## Component snippets

| File | Component |
|---|---|
| `tokens.css` | Design tokens, schemes and accessibility overrides |
| `glass-surface.css` | Base material, sheen, clear and prominent variants |
| `liquid-glass.js` | Refraction engine and behaviours (optional) |
| `glass-button.css` | Button: regular, prominent, icon, small, plain |
| `glass-card.css` | Floating panel |
| `glass-dock.css` | Dock with proximity magnification |
| `glass-nav-bar.css` | Screen navigation bar: glass button groups, collapsing large title, scroll edge |
| `glass-modal.css` | Modal and bottom sheet on `<dialog>` |
| `glass-popover.css` | Contextual menu |
| `glass-search.css` | Search pill that widens on focus |
| `glass-segmented.css` | Segmented control with sliding indicator |
| `glass-sidebar.css` | Navigation sidebar with sliding indicator |
| `glass-slider.css` | Range slider with lens thumb |
| `glass-tab-bar.css` | Tab bar with sliding indicator |
| `glass-toast.css` | Notification |
| `glass-toggle.css` | Switch with lens thumb |
| `glass-toolbar.css` | Tool pill and fixed website header (brand and links) |

Each snippet includes its usage markup, hover, active, focus-visible and disabled states, and
all four accessibility fallbacks.

## Do and don't

### Do
- Reserve glass for the chrome layer, over content worth seeing through.
- Include every accessibility fallback, with `!important` on `backdrop-filter: none`.
- Pair `-webkit-backdrop-filter` with `backdrop-filter`.
- Make pressed controls grow; let selections slide.
- Keep text at weight 500 or more.

### Don't
- Don't apply glass to content, and don't stack glass on glass.
- Don't rely on refraction: it is Chromium only.
- Don't use a heavy blur (20px or more): that is frosted glass, not Liquid Glass.
- Don't use `will-change: backdrop-filter` or animate `backdrop-filter`.
- Don't use `border-image` with `border-radius`, or `mix-blend-mode` on text.
- Don't use WebGL for UI components.
