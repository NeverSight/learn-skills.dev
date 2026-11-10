---
name: liquid-glass-ui
description: Build or refine natural, accessible Apple-inspired Liquid Glass interfaces for web projects. Use when adding translucent navigation, cards, controls, toolbars, floating panels, or glass materials in HTML/CSS/JavaScript, React, Next.js, Vue, Svelte, or Angular; when installing or using LiquidGlass UI Web Components; or when reviewing glass UI for hierarchy, legibility, motion, performance, and macOS-like visual quality.
---

# Liquid Glass UI

Create restrained glass interfaces that preserve content hierarchy and remain
usable across backgrounds, themes, input methods, and accessibility settings.
Treat the material as an accent for controls and navigation, not a decoration
for every container.

## Workflow

1. Inspect the project's framework, existing styles, backgrounds, and package
   manager. Preserve its conventions.
2. Choose the lightest integration:
   - For an existing build system, install
     `github:hwyuanzi/LiquidGlass-UI`, import the scoped module once on the
     client, and import its `/css` entry.
   - For a static prototype, start from [assets/starter.html](assets/starter.html).
   - For a custom design, reuse the documented tokens and component API instead
     of recreating an unrelated glass effect.
3. Place glass primarily on navigation, controls, inspectors, toolbars, and
   focused cards. Keep dense reading surfaces more opaque.
4. Select context:
   - Default for dark or colorful imagery.
   - Add `.lg-on-light` on a wrapper over bright content.
   - Use `appearance="clear"` for low-emphasis controls.
   - Use `appearance="tinted"` when readability needs a stronger material.
5. Keep motion calm. Do not add cursor-tracking glare, 3D tilt, noisy
   displacement, large hover jumps, or decorative wobble.
6. Test keyboard focus, reduced motion, reduced transparency, high contrast,
   light and dark backdrops, mobile width, and a browser without refraction.
7. Run `node <skill-dir>/scripts/verify-install.mjs [project-root]` and the
   project's normal tests before finishing.

## Integration rules

- In SSR frameworks, load the registration module in a client boundary. The
  package itself is SSR-safe, but custom elements become interactive only in
  the browser.
- Treat `refraction` as a progressive enhancement. Safari and Firefox retain
  the blur, tint, rim, and sheen without the Chromium-only edge displacement.
- Prefer semantic content inside slots. Provide visible labels or `aria-label`
  for icon-only controls.
- Use `disabled` for unavailable buttons. Set `target="_blank"` only when a new
  tab is intentional.
- Never place untrusted URL schemes into `href` or `link`; the component rejects
  executable schemes, and callers should validate application data too.
- Avoid permanent `will-change`, full-page backdrop filters, and many stacked
  refracting surfaces.

## Visual standard

- Let background color softly inform the material; avoid neon saturation.
- Keep the rim brightest at the upper edge and subtle elsewhere.
- Preserve concentric corner relationships between a surface and nested
  controls.
- Use system typography and predictable action placement.
- Prefer a 1–2px lift and 180–280ms response for interactive surfaces.
- Increase opacity before increasing blur when text contrast is weak.

Read [references/design-guidelines.md](references/design-guidelines.md) before
changing the optical treatment. Read
[references/frameworks-and-api.md](references/frameworks-and-api.md) for exact
imports, attributes, slots, tokens, and framework examples.
