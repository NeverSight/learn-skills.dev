---
name: cinematic-motion
description: |
  Genre pack: the site-of-the-day aesthetic — the page as a film projected on studio print. Warm paper canvas, near-black ink type, one vivid electric-blue accent, grotesk display, alternating scene canvases, a scrubbed index counter, text-dissolve pins, and a drag-driven card carousel. For portfolios, product launches, agencies, and any brief that wants premium scroll-driven storytelling. Requires taste-gsap for the implementation. Stack on the design-taste core skill.
triggers:
  - "cinematic"
  - "awwwards"
  - "site of the day"
  - "scroll driven"
  - "scroll story"
  - "studio"
  - "premium motion"
  - "immersive"
  - "showreel"
  - "portfolio award"
---

# cinematic-motion

> One identity: **opening credits, projected on studio print — the scroll is the projector, the paper is the screen, and one electric blue is the light.**

## 1. PALETTE (Fixed)

- Canvas: `#F7F5E7` (warm studio paper — never white, never grey). Cards: `#FCFBF4`. Hairline rules: `rgba(18,18,18,0.14)`.
- Ink: `#121212` (all primary type). Muted: `rgba(18,18,18,0.55)` (labels, secondary). On dark scenes invert: ink canvas, paper type, `rgba(247,245,231,0.16)` hairlines.
- Accent — exactly one: `#0F4BFD` (electric blue). Used for: the accent word, one hairline, stats, one fill. That's the budget.
- **The canvas flips are the rhythm:** paper scenes alternate with ink scenes and one full blue scene. Scene-hops are the signature; max two ink scenes (the index and the roadmap own them) and one blue section per page.
- NO gradients (the paper is the texture — clean, flat, no grain, no blends), NO second accent, NO pure black (`#000`), NO white sections.

## 2. TYPOGRAPHY (Fixed)

- **Display:** a tight grotesk (`Inter Tight`), weights 500–700, sentence case. NO serifs, no italics — the accent word earns attention by color alone.
- Headlines: `clamp(3rem, 9vw, 8rem)`, weight 600, leading 0.94, tracking `−0.04em`. One blue accent word per headline, never two.
- Scene h2s: same family, weight 600, `clamp(1.6rem, 3.4vw, 2.6rem)`, tracking `−0.02em`, with mono kickers.
- **Labels/metadata:** mono caps (`ui-monospace`/`IBM Plex Mono`), `letter-spacing: 0.14em`, 10–11px, muted. Numbered kickers: `01 — THE LEAK`, `02 — THE INDEX`.
- No body text below 14.5px; body in the grotesk at 400, line-height 1.65–1.7, muted for secondary.
- CTAs are pills (this pack allows them): ink pill, blue fill sweeps up on hover (`::before` + `transform: translateY` transition). Max one pill per viewport besides the nav.

## 3. COMPOSITION (Fixed)

- **The film structure:** hero with a live product screen (paper) → statement brief (paper) → the pinned index (ink) → marquee (paper, outlined type) → statement brief (full blue) → drag carousel (paper) → detail accordion (paper) → the pinned roadmap (ink) → evidence (paper) → the close (blue) → footer (ink).
- **One pinned index + one pinned roadmap = two pins total** — the budget (see taste-gsap: desktop-only, `+=` ends).
- The giant scrubbed index numeral (the `63%` beat) sits pinned, counting with the scrub; the roadmap pin scrubs its four steps up a rail whose fill climbs in blue (steps build, they never crossfade-swap).
- **Hero presence without video:** the live product screen — a CSS-built dashboard (live counter that ticks, funnel bars, a playing waveform, stat cells) that reads like product footage without a single video frame. All its loops are CSS keyframes, killed under reduced motion; the tick is a JS interval, gated.
- **The accordion is native `<details>/<summary>`** — first item `open` by default, rotating `+` medallion, no JS required to work, no-JS complete by construction.
- Hero atmosphere: a blue particle field (canvas, ~60 dots, upward drift, ≤ 0.16 alpha) and one dashed orbit ring, rotating slowly — both JS-gated, both dead under reduced motion.
- Index numerals: giant, weight 600, sitting in scene corners where kitchen-sink kits would put pictures.

## 4. CONTENT TREATMENT

- Numbered kickers keep the filmic beat structure: `01 — THE LEAK` → `05 — THE CLOSE`. The footer is the colophon: `A SKITTIE FILM — PRODUCED IN 60 FPS`.
- Copy is quiet, confident, filmic: short lines, no exclamation marks, no superlatives. One blue accent word per headline carries the emotion.
- No emoji. No icons — typographic marks (`✳`) and CSS-drawn mini-data-visuals only (funnel bars, wave bars, cohort grids — ink shapes with one blue cell).
- One primary CTA per viewport; the secondary action is a mono text link with a blue underline.

## 5. MOTION (The Soul — See taste-gsap)

- The page runs on a `gsap.context` + `matchMedia` shell: everything animated lives inside `(prefers-reduced-motion: no-preference)` and heavy effects inside `(min-width: 768px)`.
- **The signature moments, in order:** preloader (percentage counter ≤ 2s, slides away, only when JS + motion are active — hidden by default in CSS) → hero intro timeline (`expo.out`, masked line rises, the product screen slides in from the right, ≤ 1.4s) → the index pin: giant numeral counts `0 → 63` scrubbed with snapping, lines dissolve in stagger, progress hairline fills → marquee (CSS, outlined) → the drag carousel (Draggable + inertia, `bounds` from `scrollWidth − offsetWidth`, force-snapped native scroll as no-JS fallback, cursor swaps to a blue "DRAG" medallion) → the roadmap pin: four steps rise along a rail as its blue fill climbs, scrubbed → metric count-ups on entry.
- **The atmosphere layer:** Lenis smooth scroll (see taste-gsap §1), difference-blended custom cursor (lerped with `quickTo`, grows on interactive hover, DRAG label over the carousel, hidden on coarse pointers), magnetic primary CTA (≤ 5px pull), scroll-progress hairline in the nav. The hero's live counter ticks on an interval — a cheap "it's alive" beat that dies with the rest under reduced motion.
- Durations 0.9–1.6s; easing `power3.out` / `expo.out`; scrub smoothing `0.6–1`. All motion on `transform`/`opacity` (see taste-gsap §3). The close headline's accent word renders hollow-outlined (stroke, transparent fill) — a still-frame moment that doesn't move at all.
- The page must be complete and beautiful with JS off and with reduced motion on — pins collapse to stacked sections, the carousel becomes a native scroll-snap strip, the index shows its final value. If the still frame is boring, it fails.

## 6. CHECKLIST (Fail the Page If…)

- [ ] Any gradient, any second accent, any pure black, any white section.
- [ ] The accent blue used for a full section *and* the close — only one full-blue scene allowed.
- [ ] More than two ink (dark) scenes — the index and the roadmap own them.
- [ ] A headline with no blue accent word, or two of them.
- [ ] Any serif or italic type — this identity is grotesk-only.
- [ ] More than one marquee, or a marquee that runs under reduced motion.
- [ ] No numbered kickers / no film metaphor in the copy.
- [ ] More than two pins total, any pin below 768px, or animation without matchMedia gating.
- [ ] A drag carousel with no native scroll-snap fallback (JS off), or one that can't be reached with a keyboard.
- [ ] An accordion built with anything but native `<details>/<summary>` — it must work with JS off.
- [ ] Hero "video" (or a live screen) that keeps animating under reduced motion.
- [ ] A preloader that could ever show without JS, or that runs under reduced motion.
- [ ] A custom cursor visible on touch devices, or content that depends on cursor feedback.
- [ ] Animated layout properties or a reveal that hides content permanently if JS fails.
- [ ] The page's wow depends on the animation — the still frame must carry it.