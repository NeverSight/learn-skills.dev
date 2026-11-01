---
name: no-ai-slop
description: Use when building, generating, or reviewing UI for a website, web app, or mobile app to make it look intentionally designed rather than AI-generated. Removes the common AI/template "tells" (default fonts like Inter/Geist, indigo and purple-blue gradients, cream backgrounds, grey low-contrast text, pill/eyebrow over heroes, icon-card grids, shadcn-default cards, em-dashes, forced/orphan headlines, fade-up-everything, model-generated icons, missing imagery, inconsistent components, missing mobile menus) and applies a chosen visual style direction. Full catalog is TELLS.md.
---

# No AI Slop

AI- and template-built UIs share a recognizable set of "tells." The root cause is always the same: **uniformity + unconsidered defaults** - one font, one accent, one card, one centered template applied to everything. Build UI that looks deliberately designed by applying both layers.

## How to use
- Generating UI -> apply Layer 1 always + the active Layer 2 style.
- Reviewing UI -> scan against Layer 1 and fix every hit (use the self-check).
- Full reference: `TELLS.md` (~100 tells across 9 categories). This file is the distilled, always-on set.

## Layer 1 - Universal anti-tells

### Fonts & type
- Don't ship default fonts: Inter, Geist, or the "Space Grotesk + Instrument-Serif-italic + Inter" trio. Choose a face with a point of view; pair display + body with real contrast.
- Solid heading color - no gradient-clipped text.
- Real weight hierarchy - not `font-semibold`/`font-medium` as the heaviest weight on the page.
- Headings wrap naturally: no manual `<br>`, no `text-balance` on everything, no 4-line or orphan-word headlines. Keep them tight (~5-9 words).
- Left-aligned body/subtitles run to the container's content width; only CENTERED text gets a max-width measure. Never a thin floating column.
- Sentence case for headings/buttons. No spaced-out eyebrow/kicker over headings (pill, rule+caps, or spaced-caps) - the heading leads.
- `tabular-nums` for prices/stats; no negative tracking on body.

### Color & background
- No indigo/violet-600 default primary, no "VibeCode purple" #8B5CF6, no purple-to-blue (or amber-to-pink) gradients.
- No cream/#faf8f4 default background; no dotted-grid, mesh-blob, aurora, or spotlight backgrounds; no glassmorphism by default.
- High-contrast body text (near-black on light, slate-200+ on dark) - never gray-400/500 as body. Verify WCAG AA.
- One deliberate accent (not blue/purple by reflex), used sparingly, built as a ramp. No raw Tailwind status colors; no default blue focus ring.
- Don't default to dark-only. Avoid uniform soft shadows; use borders/contrast + a real elevation ramp.

### Layout
- No default centered hero (eyebrow / H1 / subhead / two equal buttons / screenshot). Asymmetric grid, one dominant CTA.
- Break the canonical section order and the all-3-equal-columns reflex. Vary alignment, column weight, spacing rhythm.
- No "feature soup" icon-card grid; no fat 4-column footer or hero-mirroring CTA band unless earned.

### Components
- No shadcn-default card (`rounded-xl border shadow-sm`) reused for everything; no one-side colored border; no "soft SaaS" rounded-2xl + soft-shadow on all. Commit to one deliberate radius + elevation system.
- No hero pill badge; no primary+ghost "Get Started / Learn More" duo; no gradient buttons.
- No 3-tier "Most Popular" `scale-105` pricing reflex; no count-up stats; no green-check/red-X comparison circles.

### Imagery & icons
- Real imagery, not text+gradients alone: product screenshots first; Unsplash/Pexels for photography. No 3D blobs, mesh "art", duotone, tilted-browser-on-gradient mockups, or model-generated people/logos/charts.
- Icons from an established library (Heroicons, Lucide, Phosphor, Hugeicons, Tabler) - never model-generated SVGs. Sparingly; no one-icon-in-a-rounded-square per feature; no emoji-as-icons; no sparkle=AI.

### Copy & motion
- No em-dashes (spaced hyphens/periods). No filler (elevate/unlock/supercharge/seamless), "delve/tapestry/boasts" diction, rule-of-three tics, "Not just X - it's Y", or "Transform your X / Simple, transparent pricing".
- Specific copy, real/odd numbers, named proof, real CTA labels (the action, not "Get Started").
- No fade-up-on-everything, uniform `hover:scale-105`, count-up/marquee/parallax reflex. Sparing, intentional motion; respect `prefers-reduced-motion`.

### Consistency
- Every instance of a component looks AND behaves identically: all buttons share the same hover/active/focus states, all cards the same border/shadow/radius, all links the same treatment. Inconsistency (some buttons press, some only hover) reads as careless and generated.
- Define each interaction and component style ONCE - a shared class or token - and reuse it. Do not re-type utility strings per instance; that is exactly how inconsistency creeps in.
- Spacing, radius, shadow, and color all come from one scale, used everywhere.

### Responsive & mobile (build AND test both)
- Mobile is not an afterthought. Every layout must work at ~375px wide with no horizontal overflow.
- A nav whose links are hidden on mobile MUST ship a hamburger button and a working mobile menu. AI routinely hides the links and forgets the menu - never ship that.
- Reflow grids to 1-2 columns, keep tap targets >=44px, scale type down sensibly.
- Actually test at mobile width before calling it done, not just desktop.

## Layer 2 - Style direction
A direction is the positive "build like this" spec (type, color, layout, surfaces, motion) for a chosen look. This open base ships ONE sample direction below. More directions - each with a matching **UI kit** of prebuilt components the AI assembles from, so output is consistent, not just tasteful - are the commercial layer (see the project README).

### Editorial Bold (sample direction)
- **Type:** display = Archivo 800-900, large, left-aligned, tracking ~-0.02em. Body = Newsreader (serif), 18px lead / 17px body, line-height ~1.6. Labels = Archivo, small, medium, sentence case.
- **Color:** paper #ffffff, ink #14120f, secondary text #44423d (high contrast). One accent: vermilion #e0402b, used sparingly (one CTA, links, a hairline rule).
- **Layout:** 12-col, asymmetric. Hero = headline + full-width subtitle + CTAs on the left, a real framed image on the right. Generous, purposeful whitespace; left-aligned.
- **Surfaces:** small radius (4-6px) or square. 1px hairline borders (ink ~12%). No drop shadows - separation via borders/contrast.
- **Imagery:** real screenshots/photography in clean hairline frames. No gradients/blobs.
- **Icons:** Heroicons/Phosphor, sparingly, inline at text size.
- **Motion:** minimal; at most one subtle reveal; reduced-motion aware.
- **Detail:** editorial structure - a hairline rule, a numbered index, strong hierarchy; tabular-nums for prices.

## Self-check (fix any "yes")
Default font (Inter/Geist)? Gradient or purple anything? Cream bg or blob/grid background? Grey body text? Pill/eyebrow over the hero? Icon-card grid? shadcn-default card or soft-shadow-everything? Em-dash? Orphaned / 4-line / `<br>` headline? Narrow floating subtitle? Model-generated or emoji icons? No real images? Fade-up on everything? Buttons with inconsistent hover/active? No hamburger + mobile menu? Breaks at 375px? Untested on mobile?

## Reference
`TELLS.md` (full catalog). `examples/aerolaunch-hero/` (the sample direction applied to a real hero).
