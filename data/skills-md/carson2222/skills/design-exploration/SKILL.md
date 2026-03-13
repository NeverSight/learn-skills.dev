---
name: design-exploration
description: Generates multiple distinct design variants of a component or page, each with a completely different visual direction, then implements the chosen one. Use when the user asks to redesign, restyle, explore design options, create multiple visual directions, or compare design approaches for any UI element -- components, pages, sections, dashboards, landing pages, or full layouts.
license: Apache-2.0
---

# Design Exploration

Generate N distinct design variants for a given component, page, or section. Each variant takes a fundamentally different visual direction. Present all for comparison, then fully implement the chosen one.

## When to Trigger

### 1. New project
The user is bootstrapping a frontend from scratch. No existing design system -- the variants define it.

### 2. Existing app
The user has an established design language and wants multiple approaches for a new or existing component, section, or page. Every variant must stay consistent with the app's existing patterns and tokens.

### Bypass: Detailed design spec provided
If the user provides exact fonts, colors, hex values, border radii, and specific styling instructions -- skip Phase 2 entirely. This is an implementation request, not an exploration request. Do not suggest alternatives or inject creative direction. Read each target file, preserve all logic, apply exactly the specified changes. Go directly to Phase 3.

## Phase 1: Research

Before designing anything:

1. **Read the existing code** -- understand every component, import, animation, and logic in the target files.
2. **Study the design language** -- globals.css, tailwind config, component library, existing patterns (spacing, colors, typography, card styles).
3. **Identify constraints** -- what must NOT change: data, logic, API calls, routing, state management.
4. **Understand the content model** -- what data is displayed, edge cases (long text, many items, empty states).
5. **Check assets** -- verify images, icons, and assets exist with correct formats (transparency, resolution, aspect ratio). If assets need preprocessing (background removal, format conversion), handle that before building variants on top of them.
6. **Look beyond the brief** -- find data values available in the codebase but not currently displayed, existing assets that could be repurposed, values that could be visualized differently (charts, progress bars, indicators instead of plain text), opportunities for grouping or layering information.

## Phase 2: Generate Variants

Create exactly the number requested (default: 5). Determine mode automatically based on project state -- do not ask.

### Mode A: New Project

No existing design system to follow.

1. **Research broadly** -- search for design approaches across disciplines: product design, editorial, print, architecture, fashion branding, game UI, packaging. Do not rely on memorized style lists.
2. **Analyze context** -- product purpose, audience, intended mood. A trading app has different needs than a portfolio.
3. **If context is insufficient, ask** -- what is the product, who is it for, what feeling should it evoke. Exception: if the user explicitly wants broad exploration, skip this.
4. **Select styles optimal for this project** -- each must be a plausible direction for this exact product, not a showcase of range. Respect explicit style exclusions as hard constraints. Do NOT fall into deterministic patterns of always picking the same style families.
5. **Maximize diversity** -- every variant must differ in spatial thinking, typographic voice, and emotional register. Not "same layout, different colors."

### Mode B: Existing App

Established styles, tokens, components, and patterns exist.

1. **Study the design system first** -- globals.css, tailwind config, theme tokens, color palette, typography, spacing, animation conventions, border radii, card styles.
2. **The app's style is the baseline** -- all variants must be consistent with the existing system. You are exploring different layouts and compositions, not different design systems.
3. **Vary structure, not identity** -- differ in layout, information hierarchy, component composition, animation approach, and density. Do NOT differ in font families, color palette, or border radius unless the user explicitly asks for a style refresh.
4. **Align with surrounding UI** -- match sizing, spacing, and alignment of adjacent elements. If next to a button, match its height. If inside a card grid, follow the same padding and gap.
5. **Style change escape hatch** -- if the user explicitly asks for a style change, break from the existing system. Treat it closer to Mode A but use the current app as context.

### Required Differentiation

Each variant MUST differ across ALL of these axes:

| Axis | Mode A (New) | Mode B (Existing) |
|------|-------------|-------------------|
| **Typography** | Different font pairing per variant | Use app fonts; vary weight, size, hierarchy |
| **Color** | Different accent, background, contrast approach | Use app palette; vary application and emphasis |
| **Layout** | Grid vs. list vs. asymmetric vs. card-based vs. dense vs. airy | Different arrangement within app conventions |
| **Mood** | Distinct personality per variant, discovered through research | Distinct compositional approach, shared personality |
| **Border/radius** | Sharp vs. rounded vs. pill vs. mixed | Use app's existing radius |
| **Motion** | Different animation philosophy | Different choices within app motion conventions |
| **Background** | Solid vs. gradient vs. texture vs. pattern vs. atmospheric | Use app patterns; vary section treatments |

### Variant Rules

- **No AI slop** -- no generic purple-on-white, no Inter/Roboto/Arial defaults, no cookie-cutter card grids, no Space Grotesk convergence across sessions.
- **No gimmick styles by default** -- never select neo-brutalism, terminal/hacker, retro-CRT, or vaporwave unless the user explicitly requests it. Default to styles that could ship in production.
- **Simplicity is valid** -- if the user asks for simple/clean/minimal, deliver exactly that. Clean typography, generous whitespace, conventional layout. No decorative elements, no effects.
- **Responsive required** -- every variant must work on mobile. Use `prefers-reduced-motion` and touch-friendly interactions.
- **Cross-browser safe** -- avoid bleeding-edge CSS that breaks in Safari or Firefox.
- **Mock data only** -- use realistic mock data covering edge cases. Do NOT wire up real API calls or state management during exploration. That happens in Phase 3.

### Variant Presentation

For each variant, provide:
1. **Name** -- short and evocative (e.g., "Ember", "Signal", "Nocturne")
2. **Description** -- 2-3 sentences on the aesthetic direction and why it fits
3. **Key choices** -- fonts, accent color, layout approach, motion style
4. **What changed** -- if the variant introduces new data, repurposes assets, restructures information, or deprioritizes existing data, state it explicitly
5. **Full implementation** -- working code with mock data

Implement a simple switching mechanism so the user can cycle through variants in the browser (e.g., a small floating selector, query param, or keyboard shortcut). The user must be able to compare all variants side by side or toggle between them without touching code.

### If All Variants Are Rejected

1. Ask what went wrong -- style direction, layout, quality, or everything.
2. Ask for a reference -- website, app, Dribbble shot, screenshot.
3. Offer 1-2 targeted variants based on feedback, not another blind batch.
4. If "just make it simple" -- drop exploration. One clean, conservative design.

## Phase 3: Implementation

Once the user picks a variant:

1. **Delete all other variants** -- clean up completely:
   - Search for remaining variant references, conditionals, and selection logic
   - Check for orphaned files, unused imports, unused CSS classes
   - Run the build to verify no broken imports
   - The codebase should look like the selected variant was the only implementation
2. **Wire up real data** -- replace all mock data with real API calls, state management, and logic.
3. **Preserve all existing functionality** -- every import, handler, and logic piece from the original must survive. Only visual styling changes.
4. **Read before writing** -- always read current file content before overwriting. Never work from memory.
5. **Verify animations** -- use GPU-accelerated properties (`transform`, `opacity`) instead of layout-triggering ones (`top`, `left`, `width`, `height`). Use `ease-out` for entrances, `ease-in-out` for state changes. If an animation looks janky, simplify it.
6. **Test responsive** -- verify at mobile, tablet, and desktop breakpoints.
7. **Verify no regressions** -- run build/lint if available. Check all imports resolve.

## Aesthetic Standards

These apply to every variant in every mode.

**Typography** -- pair a distinctive display font with a refined body font. Never default to system fonts or overused families. Each variant uses a different pairing (Mode A) or different weight/hierarchy treatment (Mode B).

**Color** -- commit to a dominant color with sharp accents. Timid, evenly-distributed palettes look undesigned. Use CSS variables for consistency.

**Motion** -- one well-orchestrated entrance sequence (staggered reveals, animation-delay) creates more impact than scattered micro-interactions. Prioritize page load and scroll-triggered moments over hover effects.

**Spatial composition** -- vary layouts meaningfully: asymmetry, overlap, diagonal flow, grid-breaking elements, controlled density, or generous negative space. Avoid defaulting to centered card grids.

**Background and depth** -- create atmosphere through gradient meshes, noise textures, geometric patterns, layered transparencies, or dramatic shadows. Solid white/gray backgrounds are a last resort, not a default.

**Anti-convergence** -- never converge on the same font, color scheme, or layout pattern across variants or across sessions. Each generation should feel curated by a different creative director.

## Critical Constraints

- **All data must be accounted for** -- every value and metric from the original must appear in every variant. Display format may change (text to chart, number to progress bar), but nothing is silently dropped. If a variant deliberately omits or deprioritizes a data point, it MUST be called out in the variant description.
- **No placeholder content** -- mock data during variants, real data in final implementation.
- **File completeness** -- write the ENTIRE file. No "rest remains the same" comments.
- **Font imports** -- update layout/entry file imports when changing fonts (next/font/google, @font-face, etc.).
- **Design tokens** -- update CSS variables/theme tokens to match the chosen variant. Do not hardcode colors inline when the app uses a token system.
