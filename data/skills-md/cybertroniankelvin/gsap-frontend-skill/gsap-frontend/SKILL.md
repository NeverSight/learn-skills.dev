---
name: gsap-frontend
description: >-
  Build distinctive, production-grade animated frontends with GSAP + ScrollTrigger
  (Next.js/React/Tailwind first, adaptable to any stack). Use when creating landing
  pages, marketing sites, hero sections, or any UI with scroll animations. Triggers
  include "GSAP", "gsap", "ScrollTrigger", "scroll animation", "scroll-triggered",
  "parallax", "pinned section", "sticky scroll", "horizontal scroll", "marquee",
  "kinetic typography", "reveal on scroll", "count-up", "gradient mesh",
  "glassmorphism", "animated landing page", "hero animation", or building a site
  "like cash.app / getduel / magic-receipt / pushapp". Covers GSAP setup, reusable
  primitives, copy-paste scroll patterns, performance + prefers-reduced-motion, and
  a catalog of design languages with reference screenshots.
---

# GSAP Frontend

Build fast, accessible, distinctive animated frontends with GSAP + ScrollTrigger.
This skill ships ready-to-copy animation primitives, copy-paste pattern recipes, a
catalog of design languages (with reference screenshots), and the hard-won
performance/accessibility fixes that keep scroll animations smooth and non-janky.

Default stack: **Next.js (App Router) + React + Tailwind v4**. The GSAP core and all
patterns are framework-agnostic — see `references/setup.md` for adapting to Vite,
plain React, or vanilla JS.

## Build workflow

1. **Confirm the brief & stack.** What page (landing/hero/section)? What brand
   (colours, fonts)? Which framework? If the user named a vibe or a site
   ("like cash.app", "bold and dark", "premium glassy"), map it to a design
   language in step 3.
2. **Install GSAP.** `npm i gsap @gsap/react` (GSAP is fully free incl. all plugins).
3. **Drop in the engine.** Copy `assets/anim/{gsap.ts,Reveal.tsx,Counter.tsx,Marquee.tsx}`
   into the project (e.g. `src/components/anim/`) and paste `assets/anim/globals-snippet.css`
   into the app's global stylesheet. Replace the example `@theme` tokens with the brand's
   colours/fonts. Read `references/setup.md`.
4. **Pick a design language.** Browse `references/design-languages.md` (a catalog of 13+
   styles with reference screenshots in `assets/references/`). Each style maps to a motion
   vocabulary and a set of patterns. Offer the user 2–4 options if the direction is open.
5. **Compose the page from patterns.** Build sections using the copy-paste recipes in
   `references/patterns.md` (headline reveal, pinned horizontal scroll, sticky product
   story, parallax, colour-flip, count-up, marquee, gradient mesh, glass cards, two-tone
   headings). Keep content in a single data module so sections stay tidy.
6. **Apply the golden rules** (below) and skim `references/gotchas.md` before finishing.
7. **Verify.** Follow `references/verify.md` — production build + lint pass, scroll forward
   and back, check `prefers-reduced-motion` (content fully visible, no motion) and a mobile
   width (no overflow). Use the bundled `scripts/capture-screenshots.py` to grab frames.

## Golden rules (non-negotiable)

These prevent ~90% of the bugs encountered building real animated sites:

1. **Register GSAP once, centrally** (`assets/anim/gsap.ts`) and always animate inside
   `useGSAP(() => { … }, { scope: ref })`. Never `registerPlugin` ad-hoc in components.
2. **Gate every animation behind motion preference.** Wrap motion in
   `gsap.matchMedia("(prefers-reduced-motion: no-preference)", () => {…})` and
   `return () => mm.revert()`. Content must be **fully visible by default** — apply the
   hidden start state only *inside* GSAP (so no-JS and reduced-motion users see everything).
3. **Refresh ScrollTrigger after images load.** Call `refreshAfterAssets(root.current)`
   from `gsap.ts` inside `useGSAP` and run its cleanup. This is the **#1 fix for "jumpy"
   scroll** — async images change section heights and stale trigger positions.
4. **Animate transforms/opacity only.** Add `will-change-transform` / `transform-gpu` to
   scrubbed, parallax, and marquee layers. Use a **numeric `scrub` (≈1–1.2)** for smooth
   pinned scroll; `scrub: true` for 1:1 parallax; `scrub: 0.6` for snappy.
5. **`overflow-x-clip`, never `overflow-hidden`,** on any ancestor of a `position: sticky`
   element (overflow-hidden silently breaks sticky).
6. **Pin the whole section** (heading + content) when building pinned scroll, so the
   heading stays visible while content slides. Pin at `start: "top 120px"` to clear a
   sticky header.
7. **Dark sections need explicit heading colour.** If global CSS sets a heading `color`,
   a white headline on a dark background is invisible — add `text-white`/brand colour.
8. **Select with scoped class strings inside `useGSAP`** (e.g. `gsap.from(".hero-word", …)`).
   Never collect elements by mutating a ref array during render (lint: `react-hooks/refs`).

## Choosing a design language (quick map)

Browse `references/design-languages.md` for the full catalog + screenshots. Fast map:

| Vibe the user wants | Design language | Signature motion |
|---|---|---|
| Bold, playful, colourful, "snappy" | Cash App / kinetic | colour-flip pinned statements, oversized word-reveal, marquee, count-up |
| Premium, dark, gym/tech energy | getDuel / DUELR (bold dark) | two-tone uppercase line-reveal, glowing pill, dark bordered cards, staggered reveals |
| Sleek, cinematic, app/product | magic-receipt / pushapp | gradient-mesh blobs, parallax floaters, glassmorphism cards, device float |
| Clean, trustworthy, content-led | minimal / editorial / Swiss | restrained reveal-on-scroll, subtle parallax, generous type |
| Story-driven product demo | sticky product story | scroll-synced sticky frame, sliding device screens, pinned horizontal gallery |

## Reference files

- `references/setup.md` — install, the central registrar, `useGSAP`/`matchMedia`/cleanup
  skeleton, `refreshAfterAssets`, Tailwind `@theme` tokens, adapting to other stacks.
- `references/patterns.md` — **the heart**: copy-paste recipes for every scroll pattern,
  each with its exact ScrollTrigger config and motion gate.
- `references/gotchas.md` — symptom → cause → fix checklist of the real bugs (sticky,
  jumpy scroll, marquee jitter, ultrawide breaks, grid-gap stretching, etc.).
- `references/design-languages.md` — catalog of 13+ styles, each mapped to patterns,
  with reference screenshots in `assets/references/` and live worked examples.
- `references/verify.md` — the Playwright verification playbook (build/lint, scroll,
  reduced-motion, mobile) using the bundled capture script.
- `references/extending.md` — how to add sites you like to the catalog (self-extend).

## Bundled assets

- `assets/anim/` — drop-in `gsap.ts`, `Reveal.tsx`, `Counter.tsx`, `Marquee.tsx`, and
  `globals-snippet.css` (keyframes + example tokens). Brand-agnostic; copy as-is.
- `assets/references/` — screenshots of cash.app, getduel.co.uk, magic-receipt.ai,
  pushapp.co.uk, and example Lazybooks builds (home + v1–v4) for visual reference.
- `scripts/capture-screenshots.py` — self-contained Playwright CLI for capturing reference
  and verification screenshots (`--help`). Playwright is **optional** (only this script needs
  it; building sites does not). If it's missing, run the script with `--install` or install
  with `python3 -m pip install playwright && python3 -m playwright install chromium`.

## Extend this skill (add sites you like)

This skill is self-extending. When the user shares URLs of sites whose style they like
(e.g. "add stripe.com and linear.app to the catalog"), follow `references/extending.md`:
WebSearch/WebFetch the site to read its design language, run `scripts/capture-screenshots.py`
to save hero + scrolled screenshots into `assets/references/`, then append a catalog entry to
`references/design-languages.md` (vibe, palette, type, layout, motion→patterns, screenshots).
The skill edits its own files in place; maintainers commit + push to share.

## Quick tips

- **Hero image crop:** use `object-cover` + `object-[50%_38%]` (or similar) to keep faces
  / focal points in frame when an image is constrained to an aspect ratio.
- **Worked examples:** https://lazybooks-nextjs.vercel.app/ and its `/v1`–`/v4`, `/versions`
  routes are full implementations of the patterns and design languages here.
- **Verify before done:** run the prod build, toggle `prefers-reduced-motion`, and check a
  ~390px mobile width.
