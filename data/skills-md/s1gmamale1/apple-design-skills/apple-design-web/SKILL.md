---
name: apple-design-web
description: "Use when building an apple.com-style marketing/product page — the landing-page formula (sticky translucent nav, product-as-hero, full-bleed feature sections, bento grids, fat footer), scroll-driven storytelling, plus the interaction inventory that makes a flagship page feel ALIVE (continuous damped scroll-progress, theme morph, sticky-stack pinning, text wipe, ambient float), the hero media pipeline (video scrub, image sequence, asset sourcing), and Apple's front-end engineering (progressive enhancement, vanilla JS, perf discipline). Part of the apple-design family. Keywords: apple.com, marketing page, landing page, hero, scrollytelling, video scrub, interaction inventory, cross-section theme morph, sticky-stack, chaptered pinning, ambient float, canvas image sequence, createImageBitmap, WebGL 3D viewer, parallax, animation-timeline, scroll-driven animation, IntersectionObserver, progressive enhancement, srcset lazy load, frosted nav, media assets, device frame, CC0, asset sourcing."
---

# Apple Design — Web (apple.com language · scrollytelling · engineering)

Recreating apple.com: the page formula, the signature scroll effects, and how it's actually built.

## When to use
- Building a premium marketing/product landing page.
- Implementing scroll-driven animation (frame-scrub, pinning, parallax, reveals).
- Deciding the front-end architecture for an Apple-grade page.

## Core rules
- **Light-first (do this before anything else).** apple.com is predominantly **light** (`#f5f5f7`/white); a dark hero is the *exception*, used for ≤1 purposeful moment — never the default. **Show the real product** in a real device frame (a real screenshot), never an abstract placeholder. Restraint > gratuitous effects — see `apple-design`'s `references/restraint-and-antislop.md`.
- **Commit to motion on flagship pages (motion IS the substance here).** On a flagship/marketing/product surface, a page with only static one-shot fades is a *dead template*, not Apple-grade. Commit to the interaction inventory — continuous **damped scroll-progress** transforms (the #1 differentiator), sticky-pinned choreographed scenes, cross-section **theme morph** (light↔dark), and **ambient float** so it breathes when scrolling stops. This does NOT weaken light-first/real-product/restraint — both must hold: **alive AND tasteful**. The motion budget scales by surface (utility surfaces get far less); see the inventory at the top of `references/scrollytelling-techniques.md` and the surface axis in `apple-design`'s `references/restraint-and-antislop.md`.
- **The formula:** slim sticky translucent nav (~44–48px, blur, chapter-adaptive color) → big centered product hero (name + one tagline + "Learn more ›"/"Buy ›") → alternating full-bleed feature sections, *one idea each* → bento feature grid → tech specs → fat multi-column footer.
- **Scrollytelling decision tree (current apple.com is VIDEO-first):** cinematic hero clip → **video `currentTime` scrub** (what apple.com ships — `preload=none` + lazy scroll-triggered src + static start/end-frame JPEG fallback + reduced-motion→static frame; mobile-Safari scrub flaky → ImageBitmap hybrid); interactive 3D product the user rotates → **WebGL-3D scroll viewer** (three.js + GLTF, KTX/Basis textures — Apple's own product-viewer pattern); many crisp frames / frame-exact at low count → **canvas image-sequence** *(the classic pre-2022 alternative — preload, draw on rAF, sliding-window `createImageBitmap` decode + `.close()`)*; continuous element motion → **damped scroll-progress** (lerp a shadow-scroll value; engine in `apple-design-motion`); light↔dark chapters → **cross-section theme morph** (IO discrete-snap default, rAF-lerp or `animation-timeline` variants); chaptered card deck → **sticky-stack** (CSS `position:sticky` staggered `top` + ascending `z-index`, JS recede enhancement); simple reveal/parallax → **CSS `animation-timeline: view()/scroll()`** with `@supports` + IntersectionObserver fallback. The reusable damped-scroll + pointer-reactive engine lives in `apple-design-motion`; this skill composes it into page-level scenes. Media sourcing, encoding, frame-decode + delivery → `references/media-assets-and-delivery.md`.
- **Engineering:** apple.com is **progressive-enhanced HTML/CSS/vanilla JS** (observed: Browserify `ac-*` bundles), **not** a heavy SPA. Responsive `<picture>`/`srcset`, `loading="lazy"`, content-hashed immutable assets, deferred JS.
- **Never scroll-jack**, never ship huge unoptimized frame sets, always guard motion with `prefers-reduced-motion`.

## References
| File | Use for |
|---|---|
| `references/web-applecom-language.md` | Page anatomy + measured specs; nav/hero/feature/footer HTML+CSS recipes |
| `references/scrollytelling-techniques.md` | The apple.com/iphone **interaction inventory** (ranked alive behaviors, must-consider core vs flourishes) + working code: canvas scrubber, sticky scene, IO reveals, CSS scroll-driven animation, **cross-section theme/background morph**, **sticky-stacked chaptered cards** |
| `references/web-frontend-engineering.md` | Observed apple.com architecture, image/font/perf strategy, PE patterns |
| `references/media-assets-and-delivery.md` | How current apple.com delivers hero media (video-first reverse-spec, WebGL-3D viewer, content-hash URLs) · updated technique decision tree · licensed code patterns (provenance + LICENSE) · asset-sourcing IP may/may-not + ship-only-our-own guardrail · encoding/caching/frame-decode (`createImageBitmap`, sliding window, video keyint=5) |

## Common mistakes
- Cluttered hero / multiple competing CTAs; weak whitespace; busy backgrounds behind product.
- Shipping a heavy framework for a static marketing page; render-blocking JS; unoptimized images.
- Janky non-rAF scroll handlers; no reduced-motion fallback; content hidden behind animation.
- **Under-animating a flagship page** — only static one-shot IO fades = a dead template. On a marketing/product surface, commit to continuous damped scroll-progress + theme morph + ambient float (the inventory). Equally: over-animating a *utility* surface — match the motion budget to the surface axis.

**Related:** the damped-scroll + pointer-reactive engine → apple-design-motion · type/color/grid → apple-design-foundations · the nav glass → apple-design-materials · CDN/image delivery → apple-design-backend · copy & persuasion → apple-design-tactics.
