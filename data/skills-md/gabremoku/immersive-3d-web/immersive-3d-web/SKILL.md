---
name: immersive-3d-web
description: "Reference skill for building high-end interactive 3D websites (WebGL hero scenes, scroll-driven camera moves, product-style renders) using Three.js, React Three Fiber, drei, and GSAP ScrollTrigger — including retrofitting 3D into an existing site (restyle/redesign) without breaking its current routes, content, or accessibility. Use when the user wants to build, restyle, review, or debug a 3D/WebGL web experience — hero canvases, scroll-jacked sections, particle fields, instanced objects, hub/navigation scenes, or performance issues in a Three.js/R3F scene, on a new or existing project. Complements the frontend-design skill: frontend-design covers general UI/UX craft (layout, color, accessibility), this skill covers the 3D/WebGL implementation layer."
---

# Immersive 3D Web

Curated from official public documentation (threejs.org/manual, threejs.org/docs, r3f.docs.pmnd.rs, drei.docs.pmnd.rs, gsap.com/docs) — not a training-data guess. Extracted structure, not a copy of the docs: mental models, decision rules, and the failure modes that actually tank these builds in practice.

## Why this exists

Sites like premium 3D-asset showcases (bold hero motion, scroll-scrubbed camera paths, product-grade lighting) are built from a small, well-documented stack — the hard part isn't finding an API, it's knowing which of the five ways to do something is the one that won't fall over at 60fps on a mid-range phone. This skill front-loads those decisions.

## How to use this

- **Starting any new hero scene → read `reference/concept-to-form.md` first, before anything else, including `three-core.md`.** This skill makes it easy to build a technically excellent 3D hero that has no actual relationship to the site it's on — a faceted polyhedron floating center-screen looks equally "premium" on a watch brand, a bouldering gym, or a SaaS dashboard, which is exactly the problem. Decide the object's form and motion from the site's actual subject before writing geometry code, not after.
- Building from scratch → read `reference/three-core.md` first (the mental model), then `reference/r3f-drei.md` if working in React.
- Adding scroll-driven behavior → `reference/gsap-scroll.md`.
- Scene has many repeated objects (particles, crowds, data points) or is slow → `reference/performance.md`.
- Putting a hero/showcase scene together, or reviewing one for common mistakes → `reference/patterns-and-antipatterns.md` — this is the synthesis file, read it once the individual pieces make sense.
- Restyling or adding 3D to a site that already exists (not a greenfield build) → `reference/retrofit.md` **first** — integration strategy, what not to break, and platform-specific notes (e.g. Lovable/`vite_react_shadcn_ts` projects with a synced GitHub repo). Read this before the others when the target is an existing codebase.
- Dressing a hero section (background video/embedded-3D, glass cards, staggered entrance motion, fluid type) rather than building the 3D itself → `reference/hero-dressing.md`. Applies whether the background is R3F, an embedded Spline scene, or plain video — this is the CSS/motion layer around it, not the 3D layer.
- Polishing the rest of the site — nav links, buttons, cards — so it reads as a finished product instead of a hero-only demo → `reference/micro-interactions.md`. Site-wide, not hero-specific: animated nav underlines, button hover/press feedback, sheen sweeps, tilt/magnetic cursor-following cards, card hover lift, and why consistency across all of them matters more than any single effect. Always worth a pass on *any* build using this skill, not just ones with a flashy hero.
- Handling loading/selected/locked states, number/progress reveals, custom cursors, ticker tape, or one-shot celebration animations → `reference/state-and-feedback.md`. Feedback tied to *application state* rather than the cursor — the difference between a demo (only ever shows the finished state) and a real product (has to render every state honestly). Includes the decision rule for which of the two gradient-border techniques to use when (opaque double-background vs. `mask-composite` overlay).

## Core mental model (front-loaded, expand via reference/ as needed)

**Before any of this: form follows subject, not habit.** `icosahedronGeometry`/`torusGeometry`/`torusKnotGeometry` are the easy, always-looks-premium default — and exactly for that reason, easy to reach for without asking whether this specific site's subject actually calls for it. See `concept-to-form.md`.

**Stack:** Three.js (WebGL engine) → React Three Fiber / R3F (declarative React renderer for it, JSX maps 1:1 to `THREE.*` constructors) → drei (ready-made helpers: lighting rigs, loaders, camera controls) → GSAP ScrollTrigger (scroll-as-playhead for camera/object animation).

**The five Three.js primitives:** Scene (tree), Camera (viewpoint), Renderer (draws to canvas), Mesh = Geometry (shape) + Material (surface), Light (illumination — cost scales per light, cheapest first: Ambient/Hemisphere → Directional → Point/Spot → RectArea).

**The one performance decision that matters most:** many objects on screen → do they move independently after creation? No → merge geometries into one draw call. Yes → `THREE.InstancedMesh`. Never one `Mesh` per repeated item.

**The scroll-3D pattern:** GSAP `ScrollTrigger` with `scrub` turns scroll position into an animation playhead (`self.progress`, 0→1); read it in `onUpdate` and apply to camera/object transforms inside R3F's `useFrame` — don't rely on GSAP's default DOM tweening for Three.js object properties.

**Complementary skill:** for the surrounding page — typography, color, layout, accessibility of the non-3D UI — hand off to `frontend-design`. This skill stops at "how do I build/optimize the WebGL layer."

## Sourcing note

Docs fetched directly (see per-file source lines); where a page was inaccessible (e.g. the R3F+GSAP scroll tutorial returned 404), the pattern in `gsap-scroll.md`/`patterns-and-antipatterns.md` is an explicit synthesis of the verified primitives (ScrollTrigger's documented `onUpdate`/`scrub`, R3F's documented `useFrame`), flagged as such rather than presented as a quoted example.

`reference/hero-dressing.md` is sourced differently from the rest of this skill: distilled from real production prompts rather than official docs, flagged as such in that file.

`reference/micro-interactions.md` and `reference/state-and-feedback.md` are sourced from hands-on build/review work under this skill plus patterns confirmed independently in two real production codebases (a live financial dashboard and a personal site) — same caveat as `hero-dressing.md`.

`reference/concept-to-form.md` is sourced from a self-observed anti-pattern across four builds done under this skill in one session, named directly by the person using it — not from docs or an external codebase, flagged as such in that file.
