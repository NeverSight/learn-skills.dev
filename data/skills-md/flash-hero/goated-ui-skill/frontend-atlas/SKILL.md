---
name: frontend-atlas
description: Verified 2026 implementation cookbook for Awwwards-grade front ends (474 recipes, type-checked and browser-audited). Covers motion and easing tokens, GSAP ScrollTrigger + Lenis choreography (pin, scrub, horizontal, stacked cards, SplitText), CSS scroll-driven animations, modern CSS (@starting-style, anchor positioning, @property, container queries), text effects and font pairing, hover/cursor/micro-interactions, view and route transitions, preloaders and menus, CSS/SVG/canvas backgrounds, WebGL shaders and Three.js/R3F, 21st.dev / Aceternity / Magic UI / React Bits components, OKLCH color, layout and hero composition, 30 aesthetic directions, performance and accessibility. Use when building, styling, animating or redesigning any website, landing page, portfolio or UI component, or when the user asks for an effect ("make it feel premium", "scroll animations", "smooth scroll", "parallax", "text reveal", "shader background", "page transition", "custom cursor", "bento", "marquee"), even if no library is named.
---

# Frontend Atlas

The implementation layer for premium front ends. Sibling skills judge *whether* and *what*
(`taste-skill` anti-slop rules, `impeccable` critique/audit/polish, `soft-skill`, `minimalist-skill`,
`brutalist-skill`). This skill knows *how*: verified, copy-pasteable recipes for the motion, scroll,
type, hover, transition, background, shader and component effects that ship on the best sites in
2026, plus the judgment to pick the right one and tune it until it feels inevitable.

Verified 2026-09-27 against: gsap 3.15 (every plugin free, new SplitText), @gsap/react 2.1,
motion 13.4 (`motion/react`), lenis 1.3 (`lenis/react`), three r186, @react-three/fiber 9.8,
drei 10.7, animejs 4.5, tailwindcss 4.3, next 16.3, react 19.3. All TS/TSX recipes type-check
against those packages; the signature recipes were run in Chromium and audited with the scripts below.
Project rules beat this file (a project that is "GSAP only" stays GSAP only).

## How to use

1. Write the **Design Read** (below) before any code. Five lines, no more.
2. Find the effect: the shortlist below, or search `references/INDEX.md` (every recipe with its anchor).
3. Open ONLY the section you need. Reference files are long (700-3000 lines); never load them whole
   unless you are choosing between many options (then read that file's Decision guide table first).
4. Copy the recipe, then tune the values under **Tune** to the chosen motion personality.
5. Verify in a real browser with `scripts/motion-audit.mjs` (see Verification). Not watched = not done.

## Reference map

| File | Open when |
|------|-----------|
| `references/INDEX.md` | Looking up any effect by name (474 entries, grouped by file). |
| `references/motion-principles.md` | Easings, durations, springs, stagger, choreography, 7 motion personality presets. Read before any animation-heavy build. |
| `references/scroll-gsap.md` | Lenis smooth scroll, ScrollTrigger reveals, pinning, scrub, horizontal galleries, stacked cards, SplitText on scroll, image sequences, video scrub, Flip, Observer slides, refresh discipline. |
| `references/scroll-css-native.md` | Zero-JS scroll effects: `animation-timeline: scroll()/view()`, progress bars, reveals, parallax, CSS carousels, `scroll-state()` queries, fallbacks, native-vs-GSAP split. |
| `references/css-modern.md` | `@starting-style`, dialog/popover, anchor positioning, `interpolate-size`, `@property`, container/style queries, `:has()`, OKLCH, `text-wrap`, `sibling-index()`, `corner-shape`, customizable select, Tailwind v4 mapping, support matrix. |
| `references/text-effects.md` | Split-text reveals, scramble, typewriter, rotating words, text roll, variable-font play, marquees, counters, gradient/shimmer text, text on path, fitted wordmarks, kinetic intros. |
| `references/typography.md` | Type scale, fluid type, tracking/leading, OpenType, 27 font pairings with sources and licences, loading without CLS, editorial type layouts. |
| `references/interactions.md` | Custom cursor, magnetic, hover reveals, image trail, button/link hovers, tilt, spotlight cards, tabs indicator, accordion, popovers, toasts, drawers, dock, drag, micro-feedback, feel-tuning table. |
| `references/page-transitions.md` | View Transitions (same-doc, cross-doc), React `<ViewTransition>` in Next 16, shared elements, GSAP overlay transitions, Swup/Barba/Astro, preloaders, intro gating, fullscreen menus, route hygiene. |
| `references/backgrounds-svg-canvas.md` | Mesh/aurora/grain/grid backgrounds, conic borders, SVG draw/morph/goo/displacement, canvas particles/dot grids/flow fields, Lottie vs Rive. |
| `references/webgl-shaders-3d.md` | WebGL loading shell, shader library (GLSL), image distortion, DOM-to-WebGL galleries, fluid cursor, particles, R3F glass hero, globes, post-processing, Paper Shaders, WebGPU/TSL. |
| `references/component-recipes.md` | 67 named components (21st.dev, Aceternity, Magic UI, React Bits, Motion Primitives, Cult UI...): install commands, self-owned code, overuse scores, section combos. |
| `references/color-surfaces.md` | OKLCH ramps, semantic tokens, contrast (WCAG/APCA), dark mode, gradients, glass and liquid glass, shadows, borders, radius, image treatment. |
| `references/layout-composition.md` | Breakout grid, 12-col/subgrid, fluid space, 10 hero skeletons, bento, section patterns, sticky/overlap layouts, navigation, responsive strategy. |
| `references/aesthetic-directions.md` | Choosing or executing one of 30 visual directions, each with tokens, fonts, motion signature, real reference sites, AI-slop tells. |
| `references/libraries.md` | Choosing/setting up any of 37 libraries: size, install, SSR caveats, status, recommended stacks per project type. |
| `references/performance-a11y.md` | Before shipping anything animated: property cost, jank debugging, pausing offscreen work, CLS from pins, reduced motion done right, WCAG motion criteria, QA checklist. |
| `references/inspiration-sources.md` | Finding references, components, fonts, icons, assets, tools; reverse-engineering an effect seen on a live site. |

## Effect shortlist (most requested)

| Effect | Where |
|---|---|
| Smooth scroll (Lenis on the GSAP ticker) | `scroll-gsap.md#1-setup-and-lenis-sync` |
| Reveal on scroll, zero JS | `scroll-css-native.md#5-reveal-on-enter-fade--slide--clip--blur` |
| Staggered card reveal | `scroll-gsap.md#3-batch-reveal-on-enter` |
| Headline line-mask reveal | `text-effects.md#1-line-mask-reveal-splittext-mask-lines` |
| Kinetic hero intro timeline | `text-effects.md#27-kinetic-headline-intro-sequence`, `motion-principles.md#9-orchestrating-a-hero-intro-gsap-motion-css` |
| Pinned hero zoom / clip expand | `scroll-gsap.md#6-pinned-hero-zoom-and-clip-expansion` |
| Pinned multi-step story | `scroll-gsap.md#7-pinned-multi-step-timeline-with-label-snap` |
| Horizontal scroll gallery | `scroll-gsap.md#8-horizontal-scroll-gallery`, CSS: `scroll-css-native.md#10-horizontal-scroll-section-sticky--view-timeline` |
| Stacked cards | `scroll-gsap.md#9-stacked-cards`, CSS: `scroll-css-native.md#11-stacking-cards` |
| Sticky split scrollytelling | `scroll-gsap.md#10-sticky-split-layout` |
| Parallax | `scroll-css-native.md#6-parallax-layers`, `scroll-gsap.md#11-parallax-layers` |
| Words light up as you scroll | `scroll-gsap.md#5-text-fills-as-you-scroll`, `scroll-css-native.md#12-text-fill--word-by-word-highlight-on-scroll` |
| Scroll-velocity skew / marquee | `scroll-gsap.md#13-scroll-velocity-skew-and-marquee` |
| Apple image sequence / video scrub | `scroll-gsap.md#17-scroll-scrubbed-video-and-image-sequence` |
| Full-screen slide sections | `scroll-gsap.md#15-observer-full-screen-slides` |
| Reading progress, sticky header shrink | `scroll-css-native.md#4-reading-progress-bar-page-and-per-article`, `#8-sticky-header-compact--frosted-on-scroll` |
| Scramble / decrypt text | `text-effects.md#6-scramble--decode--decrypted-text` |
| Rotating words, text roll on hover | `text-effects.md#8-rotating-words-height-masked-slot`, `#9-text-roll-on-hover` |
| Cursor-proximity variable type | `text-effects.md#12-cursor-proximity-variable-type` |
| Giant fitted footer wordmark | `text-effects.md#14-fit-text-to-width-giant-wordmark-footer` |
| Marquee (CSS / velocity) | `text-effects.md#22-css-only-infinite-marquee`, `#23-velocity-reactive-marquee` |
| Number counters | `text-effects.md#24-number-animation` |
| Font pairing | `typography.md#9-font-pairing-playbook-2026` |
| Custom cursor, magnetic buttons | `interactions.md#1-custom-cursor-with-trailing-ring`, `#2-magnetic-elements` |
| Hover image reveal list, image trail | `interactions.md#3-hover-image-reveal-and-image-trail` |
| Button hover/press system | `interactions.md#4-button-hover-and-press-system` |
| Spotlight glow card grid | `interactions.md#7-spotlight-glow-card-grid` |
| Tabs sliding indicator | `interactions.md#8-tabs-indicator-and-nav-hover-highlight` |
| Micro kit (hold, copy, like, switch) | `interactions.md#13-micro-interaction-kit` |
| Route transitions in Next 16 (native) | `page-transitions.md#4-react-193-viewtransition--next-16-routes` |
| Shared element list -> detail | `page-transitions.md#5-shared-element-list-detail-3-ways` |
| Curtain / overlay route transition | `page-transitions.md#7-gsap-overlay-route-transitions-the-awwwards-default` |
| Theme toggle circle reveal | `page-transitions.md#10-circle-reveal-from-the-click-point-theme-toggle--routes` |
| Preloader + gated hero intro | `page-transitions.md#18-counter-0-100--curtain-skipped-on-repeat-visits`, `#19-intro-gate-store-hero-waits-for-preloader` |
| Fullscreen menu, hide-on-scroll nav | `page-transitions.md#23-fullscreen-menu-overlay`, `#24-nav-hide-on-scroll-down--show-on-up` |
| Dialog / popover enter-exit in CSS | `css-modern.md#1-enterexit-from-displaynone-starting-style--allow-discrete` |
| Mesh gradient, aurora, grain | `backgrounds-svg-canvas.md#1-layered-radial-mesh-gradient`, `#2-aurora-blobs`, `#3-grain-noise-overlay` |
| Border beam / rotating conic border | `backgrounds-svg-canvas.md#8-border-beam-along-the-edge`, `#7-animated-conic-border` |
| SVG line drawing, morphing | `backgrounds-svg-canvas.md#14-stroke-drawing`, `#15-shape-morphing` |
| Interactive dot grid, constellation | `backgrounds-svg-canvas.md#29-interactive-spring-dot-grid`, `#27-constellation-network` |
| Shader gradient background | `webgl-shaders-3d.md#1-gatekeeping-and-loading-shell-next-16` + `#3-shader-library-glsl` |
| WebGL image hover / gallery | `webgl-shaders-3d.md#4-image-effects-and-dom-to-webgl` |
| Fluid cursor, particle morph | `webgl-shaders-3d.md#5-cursor-fluid-simulation`, `#6-particles-morphing-points-mouse-repulsion-gpgpu` |
| 3D glass hero (R3F) | `webgl-shaders-3d.md#7-r3f-hero-scene-glass-environment-gltf-scroll-camera-3d-text` |
| Globe | `component-recipes.md#14-globe-cobe`, `webgl-shaders-3d.md#8-globes-cobe-three-globe-custom` |
| Bento grid | `layout-composition.md#7-bento-grids-done-right`, `component-recipes.md#43-bento-grid` |
| Proven section combos | `component-recipes.md#recipe-combos` |
| Hero layouts | `layout-composition.md#6-hero-paradigms-10-skeletons` |
| Palette from one brand color | `color-surfaces.md#2-12-step-ramp-generator-ts-gamut-aware` |
| Dark mode, no theme flash | `color-surfaces.md#10-dark-mode-done-right`, `#11-theme-switch-without-fouc` |
| Glass / liquid glass | `color-surfaces.md#15-glassmorphism-done-right`, `#16-liquid-glass-approximations-tiered` |
| Choosing a visual direction | `aesthetic-directions.md#decision-guide---choosing-a-direction-from-a-brief` |

## Design Read (always first)

```
Direction:           <one entry from aesthetic-directions.md, or a named blend of two>
Motion personality:  <preset from motion-principles.md#21-motion-personality-presets>
Signature moment:    <the ONE effect a visitor will remember, and where it lives>
Supporting layer:    <one reveal system + hover/press/focus feedback + transitions>
Stack:               <CSS-native | Motion | GSAP+Lenis | +OGL/R3F> because <reason>
```

If the brief is vague ("make it premium"), infer from the product, audience and existing brand,
state the read, and proceed. Ask only when two very different directions are equally plausible.

## Choosing the stack

Pick the lightest tool that can express the effect:

1. **CSS only**: hover/press/focus, popover/dialog enter-exit (`@starting-style`), accordions,
   reveal-on-enter and progress bars (scroll-driven animations, with a fallback), marquees,
   gradient/conic animations (`@property`). Zero JS, off the main thread.
2. **Motion (`motion/react`)**: React app UI. Layout animations, `layoutId` shared elements,
   presence/exit, gestures and drag, springs, reorderable lists.
3. **GSAP + ScrollTrigger + Lenis**: scroll storytelling and timelines. Pinning, scrubbed
   multi-step sequences, horizontal sections, SplitText, Flip, DrawSVG/MorphSVG, intro sequences.
4. **WebGL (OGL for 2D shader effects, R3F for scenes)**: only when the concept needs it. Always
   ship a static poster fallback through the loading shell (webgl recipe 1).

Motion and GSAP can live in one project for different jobs, never on the same element.
One smooth-scroll instance, one RAF loop (drive Lenis from `gsap.ticker` when GSAP is present).

## Platform facts that change the code (verified 2026-09-27)

- CSS scroll-driven animations: Chrome 115+, Safari 26+, Firefox only from 159 (scheduled
  2026-10-27). Not Baseline: always `@supports (animation-timeline: view())` + a fallback.
- View Transitions: same-document in all engines (Firefox 144+), cross-document not in Firefox.
  React 19.3 stable exports `<ViewTransition>` / `addTransitionType`; Next 16.3 needs no flag.
- **Default GSAP `pin: true` causes CLS**: measured 0.75 at pin + 1.0 at unpin per 100vh section
  in Chromium (scroll is not an excluding input). CSS `position: sticky` + scrub and
  `pinType: "transform"` both measured 0. Prefer sticky tracks where the layout allows.
- ScrollTriggers created out of page order (lazy sections, a `useLenis()` value in useGSAP
  `dependencies`) fire early by the pin length. Higher `refreshPriority` refreshes first, and any
  `refreshPriority` enables auto-sorting by page position. (The official gsap-scrolltrigger skill
  states this backwards; the source is authoritative.)
- Chromium-only today: `interpolate-size`, `corner-shape`, CSS carousels (`::scroll-marker`),
  `scroll-state()` queries, `if()`, `@function`. Use them as progressive enhancement only.
- API changes that break older snippets: cobe 2 has no `onRender` (drive `globe.update()` from your
  own rAF); drei 10 `PresentationControls` takes `damping`, not `config`; `THREE.Clock` is deprecated
  (r183+); Next 16 `Image` uses `preload` instead of `priority`; Motion's `AnimateView` imports from
  `motion/react-animate-view`; tsParticles v4 uses `ParticlesProvider`.
- Inline `style={{ position: ... }}` on a wrapper overrides a caller's `absolute inset-0` class and
  collapses it to 0 px: keep positioning in classes for any component that accepts `className`.

## Page choreography blueprint

| Layer | Budget | Typical recipe |
|-------|--------|----------------|
| Arrival | hero readable in under 1.2 s | optional preloader only for a real brand moment or heavy assets, then a hero timeline: headline line-mask reveal, media scale/clip-in, nav fade last |
| Signature | exactly one per page | pinned scrub sequence, horizontal gallery, stacked cards, WebGL hero, or kinetic headline |
| Rhythm | one system for every section | same ease, distance (24-48 px), stagger (40-80 ms) for all reveals; no per-section novelty |
| Feedback | every interactive element | hover/press/focus at 120-250 ms; magnetic or cursor effects only on pointer:fine |
| Transitions | route and state changes | view transitions or a curtain matching the direction |
| Finale | footer | giant fitted wordmark, marquee, or a quiet sign-off; not another spectacle |

- One hero effect per viewport. Two competing motions cancel each other.
- Motion follows the spatial model: things enter from where they logically come from and leave
  toward where they go. Keep direction consistent across the page.
- Lead with the largest element, follow with detail. Text last when media carries the moment,
  text first when the headline is the moment.
- Exits are faster than entrances (about 0.75x). High-frequency actions get little or no motion.
- Reveal once. Re-animating content every time it re-enters the viewport is noise.
- Scroll-linked motion must feel attached to the finger: scrub with slight smoothing
  (`scrub: 0.5` to `1`), never time-based animations that fight the scroll.
- Never hijack scroll speed or direction on content pages. Pin, do not trap.

## Non-negotiables

- `prefers-reduced-motion`: replace movement with opacity or the static end state; stop parallax,
  auto-play, marquees and scroll-jacking; keep all content visible (`performance-a11y.md#15-reduced-motion-reduce-dont-remove`).
- Auto-moving content longer than 5 s (marquees, carousels, video backgrounds) needs a pause control
  or pause on hover/focus (WCAG 2.2.2).
- Animate `transform` and `opacity` by default. `filter`, `backdrop-filter`, `clip-path` and `mask`
  are fine on small or short-lived elements; never scrub them on full-viewport surfaces.
- Pointer effects (custom cursor, magnetic, tilt, hover reveals) only under
  `(hover: hover) and (pointer: fine)`, with a touch-friendly equivalent. Hide-until-hover states
  must be gated the same way (a landscape tablet is `lg` wide and cannot hover).
- The LCP element is never hidden behind a long preloader. Server-render content; animate from a
  visible or quickly revealed state. Loaders and intro curtains are opt-in: hidden unless a head
  script sets `html[data-intro="run"]`, so no-JS visitors and failed bundles never see a blank screen.
- Split text keeps an accessible label (`aria-label` on the parent, split pieces `aria-hidden`).
- Clean up everything: `useGSAP` scope, ScrollTriggers, Lenis, RAF loops, observers, WebGL contexts.
  No `window` at module scope (SSR).
- Tokens, not magic numbers: durations, easings, distances and staggers live in CSS custom
  properties or one TS constants module.
- Test in both themes (if the site has two), at 375 px and 1440 px, and with CPU throttled 4x.

## Verification protocol

Scripts live in this skill's `scripts/` folder and need `playwright-core` (or `playwright`) in the
project plus an installed Chrome/Edge (or set `AUDIT_BROWSER`). `<skill-dir>` below is this skill's
base directory (shown when the skill loads; `~/.claude/skills/frontend-atlas` for a manual install).

1. Start the dev server, then run
   `node <skill-dir>/scripts/motion-audit.mjs http://localhost:3000 --out motion-audit --widths 1440,390 --steps 16`.
   It scrolls with real wheel input (so Lenis/ScrollTrigger react), screenshots intro frames and
   every scroll step, and runs again with `prefers-reduced-motion: reduce`. It reports console
   errors, horizontal overflow with the culprit element, content that entered the viewport but was
   never visible (reveals that never fired), CLS with the shifting nodes, frame pacing and long
   animation frames. Headless numbers are for before/after comparison, not field data.
2. `node <skill-dir>/scripts/contact-sheet.mjs motion-audit --match motion-1440-scroll`
   builds one image of the whole scroll: read it to check choreography, pins and crossfades.
3. When a scroll effect fires early or late, compare `ScrollTrigger.getAll().map(t => [t.trigger, t.start])`
   with each trigger's `getBoundingClientRect().top + scrollY` (creation-order bug, see facts above).
4. Keyboard pass: tab through menus, dialogs and transitions; focus stays visible and trapped
   where it should be. Then run the `web-design-guidelines` skill over the changed files.

Maintaining this skill: after editing any reference, run `node scripts/maintenance/build-index.mjs`
(regenerates `references/INDEX.md`) and `node scripts/maintenance/check-links.mjs --links` from the
skill folder. Re-verify changed recipes in a browser before trusting them.

## Companion skills

Recommended alongside this skill (install commands in the repository README); when installed, use
them as deep API references once the stack is chosen:

- `gsap-core`, `gsap-timeline`, `gsap-scrolltrigger`, `gsap-plugins`, `gsap-react`, `gsap-utils`,
  `gsap-performance`, `gsap-frameworks`: official GreenSock skills (`greensock/gsap-skills`). Where
  `gsap-scrolltrigger` describes `refreshPriority` ordering, trust the platform fact above.
- `vercel-react-view-transitions`: deep patterns for React `<ViewTransition>` in Next.
- `web-design-guidelines`: Vercel's Web Interface Guidelines as a final review pass.
- `vercel-react-best-practices`: React/Next performance rules (all three from `vercel-labs/agent-skills`).
- Taste and critique: `taste-skill`, `redesign-skill`, `soft-skill` (`Leonxlnx/taste-skill`) and
  `impeccable` (`pbakaus/impeccable`).

Precedence: project rules > this skill's stack decision > a companion's default ("recommend
GSAP" in the GSAP skills does not override choosing CSS or Motion when they are lighter).

## Motion slop to refuse (quick list)

- Fade-up on every section with identical timing, the default AI reveal. Use one crafted reveal
  system and let some sections simply be there.
- Bounce or elastic easing on UI, scale-from-zero, spinning or wobbling decorations.
- Purple-to-blue aurora + grid + beams + shimmer button + bento as a stack of defaults
  (`aesthetic-directions.md#global-ai-slop-tells-evidence-ranked`).
- Tilt, glow and magnetic effects on everything at once.
- Custom cursor on a content or product site with no reason for it.
- Parallax on text blocks, parallax ratios above about 0.3 on content, horizontal scroll for
  plain text content.
- Preloaders that exist only to show a counter.
- Typewriter headlines, gradient text on every heading, glitch effects outside a clear concept.

When a request would land in this list, pick the tasteful variant from the relevant reference file
and say briefly why.
