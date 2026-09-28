---
name: prism
description: "The unified design-engineering skill for building award-grade, immersive websites and web interfaces in React. Use whenever the user wants to design, build, redesign, polish, critique, or animate any frontend — landing pages, portfolios, marketing sites, product UI, dashboards, hero sections, navbars, bento grids, cards, forms, modals, pricing tables, footers, testimonials — OR add 3D and immersive experiences with React Three Fiber, Three.js, WebGL, WebGPU, custom GLSL shaders, scroll-driven animation, GSAP, Lenis, or Motion. Covers UI component patterns, visual design (typography, color, spacing, layout, grid, hierarchy), motion and micro-interactions, 3D/WebGL scenes, shaders, postprocessing, performance budgets, Core Web Vitals, accessibility, and anti-AI-slop craft. Produces production-ready code on the React + React Three Fiber + GSAP stack. This is the single source of truth for all design, UI, animation, and immersive 3D work and supersedes separate UI/design/motion skills."
trigger: /prism
---

# Prism

One skill for the whole surface: UI design, visual systems, motion, micro-interactions, and immersive 3D. It generates **production-ready code** on a fixed stack — **React + React Three Fiber + GSAP** — and refuses the defaults that make generated interfaces look generated.

Prism consolidates the craft of nine prior design skills (typography, color, layout, the motion bible, anti-slop bans, design-language presets) and adds the layer none of them had: **real WebGL/3D**. The reference files hold the depth; this file is the operating procedure. Read the reference for whatever you're actually building — do not dump all of them.

---

## The one rule that governs everything

Awwwards (the bar for "award-grade") scores **Design 40% · Usability 30% · Creativity 20% · Content 10%**. Spectacle — 3D, shaders, GSAP — lives almost entirely in the **20% Creativity** slice, and it is *penalized* under Usability when it slows load or breaks navigation. **Design + Usability = 70% of the verdict.**

So the immersive layer is a multiplier on a sound interface, never a substitute for one. **3D fallbacks, lazy-loading, mobile scaling, reduced-motion, and Core Web Vitals are non-negotiable parts of every build — not polish you add if there's time.** A janky 3D hero scores *worse* than a crisp static one. Internalize this before writing a single shader.

---

## Procedure (run every time)

1. **Setup.** Is this new or a redesign? For a redesign, read the existing code first (framework, styling system, tokens, components) and work *with* the stack — audit-then-fix, don't rewrite (→ `reference/redesign.md`). For new work, check `package.json` before importing anything. **Backend contract (light pairing):** before building data-driven UI, look for a `contract/openapi.json` (project root, a sibling/`backend/` folder, or ask the user for its path/URL). If one exists it is a **light** backend's contract — wire to it instead of mocking: generate types with `npx openapi-typescript <path>/contract/openapi.json -o src/api/schema.ts`, create a typed client with `openapi-fetch` (`createClient<paths>({ baseUrl })`) or vendor `contract/client.ts`, set the base URL from env (`VITE_API_URL`), read `contract/README.md` for base URL + auth flow + CORS origin, and build components against those real types with proper loading/empty/error states. No contract → proceed with realistic mock data as usual.

2. **Design Read (one line, out loud).** State it before any code:
   > *"Reading this as: a `<page kind>` for `<audience>`, in a `<vibe>` language, using the `<design-language>` preset, at **3D Tier `<0-3>`**."*
   The audience picks the aesthetic, not your taste. If the brief genuinely forks, ask **one** question (Linear-clean vs Awwwards-experimental?), else proceed.

3. **Set the dials + tier.** `VARIANCE` (1 symmetric → 10 chaotic), `MOTION` (1 static → 10 cinematic), `DENSITY` (1 airy → 10 cockpit). Baseline **8 / 6 / 4**. Then pick the **3D Tier** (table below). Dials and tier come from the Design Read; see `reference/design-languages.md` for presets and the variance engine.

4. **Lock the system.** Choose ONE design language, lock the palette (OKLCH, ≤1 accent), type pairing (≤3 families), radius scale, and spacing grid. These do not drift between sections (→ `reference/foundations.md`).

5. **Architect.** Plan the page as distinct layout families — **no family repeats**, max 2 zigzags in a row, bento has exactly N cells for N items. Map sections to the component taxonomy (→ `reference/components.md`).

6. **Build.** Production React. Every component using motion, scroll, pointer physics, or WebGL is an isolated `'use client'` leaf. The WebGL canvas is **always code-split and lazy-mounted** (→ `reference/performance.md`). Motion follows the decision framework and timing tables (→ `reference/motion.md`). 3D follows `reference/immersive-3d.md`. Source assets (3D, HDRIs, textures, components, icons, fonts, stock) from `reference/resources.md` — and for paid/client work ship only **commercial-cleared** licenses (its Comm. column). **Build to the production-grade gate, not to "it renders":** every interactive element actually *works* (no fake/decorative components — a slider seeks, a form validates, a link smooth-scrolls), carries the full state matrix (`:hover :active :focus-visible :disabled` + empty/loading/error), and its micro-interactions have **zero layout shift** and snappy, task-appropriate press feedback (→ `reference/craft.md`).

7. **Self-audit, then verify (the ship gate).** Be your own senior reviewer — adversarially, in this order (→ `reference/craft.md` Part 3):
   - **Slop pass.** Thumbnail test, font-only test, the "who" test. Default to *fail* and make the design earn the pass — could anyone tell an AI made this?
   - **Works pass.** Click / tab / scroll **every** interactive thing. Does it do what it implies? Any layout shift on a state change? Keyboard-operable with a visible focus ring? Reduced-motion honored?
   - **Pixels pass.** **Drive the build through the verifier** — `node <this-skill-dir>/driver.mjs <url-or-dir>` — which sweeps horizontal overflow at 5 widths, captures console/page errors, and screenshots desktop + mobile + **every GSAP pin (the stop-and-read beats)** + reduced-motion, then prints PASS/FAIL. **Then READ the screenshots it saves and judge them with your eyes** — PASS means no overflow/errors, *not* that it looks good (→ `reference/verify.md`).
   - Finally run `reference/preflight.md` top to bottom. Never ask the user to check what you can check yourself.

---

## The 3D tier decision

The tier is the single biggest architectural choice. Default **down**, not up — earn each tier with a reason.

| Tier | What it is | Use when | Cost / fallback obligation |
|---|---|---|---|
| **0 — Flat** | No WebGL. CSS + Motion + GSAP only. | Content sites, B2B, docs, dashboards, accessibility-first, perf-critical. | None. Often the *right* answer; a flawless flat site beats a shaky 3D one. |
| **1 — Accent** | One lazy-loaded scene or shader background. Small, bounded canvas. | Most marketing/landing pages. A hero object, a shader gradient, a product shot. | Static poster fallback; canvas deferred past LCP; paused under reduced-motion. |
| **2 — Integrated** | Scroll-driven 3D woven through the page via one shared `GlobalCanvas` tracking DOM proxies (r3f-scroll-rig). | Portfolios, agencies, product showcases. 3D that follows the scroll narrative. | All of Tier 1 + mobile-scaled scenes + full reduced-motion static path. |
| **3 — Immersive** | Full-viewport WebGL world, cinematic camera (Theatre.js / GSAP), heavy shaders, postprocessing. | Experiential / SOTD ambitions, launches, brand worlds. | All of Tier 2 + a genuinely good non-WebGL experience for the 30% Usability score. |

**Non-negotiable at every tier ≥ 1:** a reduced-motion path that pauses 3D and shows a static frame; a mobile strategy (scale down or fall back); the canvas behind a dynamic import + `Suspense`; and a Core Web Vitals budget that survives the scene. If you can't ship those, drop a tier.

---

## The stack (fixed)

Generate for this stack. Verify versions against the project's `package.json` before pinning — these libraries move fast (the pins below are a floor, current at research time, not gospel).

```bash
# Core
npm i react react-dom three @react-three/fiber @react-three/drei
# Motion
npm i gsap @gsap/react motion lenis
# Immersive (Tier ≥ 1 as needed)
npm i @react-three/postprocessing
npm i @14islands/r3f-scroll-rig        # Tier 2: shared canvas tracking DOM
npm i @theatre/core @theatre/studio @theatre/r3f   # Tier 3: cinematic scroll camera (studio is dev-only)
npm i ogl                              # optional: lightweight shader backgrounds
```

- **Motion library:** `motion` (the rebranded Framer Motion). Import from `motion/react`. `framer-motion` still works as a legacy alias; prefer `motion/react` in new code.
- **Smooth scroll:** `lenis` — the spine that GSAP ScrollTrigger and scroll-driven 3D ride on.
- **Continuous values** (scroll progress, pointer, magnetic hover) use `useMotionValue` / `useScroll` / `useFrame` — **never** `useState`; it re-renders the tree every frame and collapses on mobile.
- **Component pattern banks** (treat as *taxonomy and source to copy*, not stack mandates): **React Bits** (130+ components on this exact R3F + drei + postprocessing + GSAP + ogl + motion stack — the closest match), **Aceternity UI** (named patterns: Resizable Navbar, Hero Parallax, Bento Grid, Animated Modal, 3D Marquee, Infinite Moving Cards), **shadcn/ui** (`npx shadcn@latest add` copies source into the project — controllable base primitives; still pulls Radix via npm). Copy these as structure/mechanics to RE-SKIN, never paste-and-ship — their stock styling (e.g. Aceternity hero-parallax, moving-cards) is itself a recognizable AI tell; restyle to the locked system before it counts as yours.

---

## Core laws (condensed — depth in the references)

These are the deduplicated non-negotiables. The full bans and rationale live in `reference/foundations.md` and `reference/motion.md` — and the bar that governs all of them, the line between AI-slop, looks-fine demo-ware, and shippable production craft, is `reference/craft.md`. Read it before you call anything done.

**Anti-slop.** If someone could say "AI made that," it failed. No Inter/Geist/Space Grotesk by default — they are the AI-default tell; choose a display face with a point of view (font-only test: strip color + layout, does the type alone read as THIS brand?), sourced intentionally from `reference/resources.md` and never reused across builds. Inter/Geist are permitted ONLY as a deliberate neutral workhorse *under* a distinctive display face, or for Linear-clean / accessibility-first briefs — never the identity (Geist Mono is fine in mono roles). No AI purple-blue gradient glow. No pure `#000`. No emojis in UI. No three-identical-card row. No eyebrow above every section (≤1 per 3). No fake-precise numbers. No "Elevate / Seamless / Unleash / Next-Gen / Delve." No Lucide-by-default (Phosphor / Tabler / Radix). No div "fake screenshots." No gradient-clip text. No ghost-card (1px border + big soft shadow). No `h-screen` (use `min-h-[100dvh]`).

**Type.** Premium display family; scale ratio ≥1.25; body 65–75ch; display letter-spacing floor −0.04em; hero `clamp()` max ~6rem; `text-wrap: balance` on h1–h3; headline ≤2–3 lines (a 4-line hero is a font-size error).

**Color.** OKLCH. One accent, saturation <80%. One gray family. Tint shadows to the background hue. **Verify contrast** on every text, button, and placeholder: WCAG AA 4.5:1 body / 3:1 large. If both light + dark ship, define them as ONE semantic-token system (not two hardcoded palettes); dark mode is near-black tinted to the brand hue (never `#000`), elevation by lightness not glow, and contrast AA is re-verified in BOTH modes.

**Layout.** Asymmetry over centered when `VARIANCE > 4`. Macro whitespace (`py-24`→`py-40`). Grid for 2D, flex for 1D — never `calc()` percentage math. Max-width container ~1400px. Cards only when elevation means hierarchy; nested cards never. Design mobile (360px) as a first-class layout, not a reflow afterthought — no horizontal overflow at 360/768/1024/1440/1920, clip decor with `overflow:clip`, fluid `clamp()` type, 44px targets; the asymmetric desktop grid must resolve to an intentional small-screen order, never a default centered stack.

**Motion.** Custom cubic-bezier, never `linear`/`ease-in-out` as a default. Enter `ease-out`, exit `ease-in` at **65–75% of the enter duration**. Animate **only `transform` and `opacity`** (GPU); ≤~20 animated elements per viewport; logic <10ms/frame. Springs for natural/interruptible motion. Never animate from `scale(0)` — start `scale(0.95)` + opacity. Motion must be *motivated* (hierarchy, feedback, continuity, explanation) — never "it looked cool." Marquee ≤1/page.

**Accessibility & states.** `prefers-reduced-motion` is a *transformation*, not a switch: strip movement, keep opacity, kill loops, halve durations, pause scroll-3D/parallax. Always ship loading (skeleton), empty (composed), and error (inline) states. `:active` → `scale(0.97)` over ~0.12s with `var(--ease-out)` (snappy, never bouncy; a deeper dip + spring-on-release only for explicitly playful briefs). Visible focus rings. 44px touch targets.

**Assets.** Real, art-directed, content-true images — generate them. `picsum.photos/seed/<descriptive>/w/h` is a LAST-RESORT layout placeholder only (never the hero, never in a client deliverable); keep seeds consistent so the set reads intentional. Real SVG logos (Simple Icons). Never hand-drawn sketchy SVG as a fallback.

---

## Reference router

Load only what the task needs.

| File | When to read it |
|---|---|
| `reference/craft.md` | **The quality spine — read on every build and before every "done."** The line between AI-slop, looks-fine demo-ware, and shippable production craft: the anti-slop bible (default tells + antidotes), the production-grade gate (components that actually work, the state matrix, micro-interaction physics, a11y, no-CLS, the optical 1%), and the self-audit you run on your own output. |
| `reference/foundations.md` | Typography scale, OKLCH color, spacing grid, layout, hierarchy, the full anti-slop ban list. Read for any new visual system. |
| `reference/components.md` | Building specific UI: nav, hero, bento, cards, forms, modals, marquee, footer, pricing, testimonials, accordion. Code per component. |
| `reference/motion.md` | Any animation. Emil decision framework, duration/easing tables, GSAP ScrollTrigger skeletons, Lenis, Motion, springs, page/view transitions, reduced-motion. |
| `reference/immersive-3d.md` | Tier ≥ 1. R3F setup, camera/lights/materials, drei, custom GLSL shaders, scroll-driven 3D, postprocessing, particles, model pipeline, WebGPU/TSL. |
| `reference/performance.md` | Tier ≥ 1, or any heavy motion. Instancing, LOD, KTX2/Draco, on-demand frameloop, DPR clamp, lazy-mount, mobile, Core Web Vitals / INP budgets. |
| `reference/design-languages.md` | Choosing the aesthetic. Five presets (Ethereal Glass, Editorial Minimal, Industrial Brutalist, Soft Structural, Immersive Cinematic) + the variance engine. |
| `reference/redesign.md` | Existing project. Audit → diagnose → fix flow, fix-priority order, strategic omissions. |
| `reference/preflight.md` | Before shipping anything. The merged pre-flight checklist. Mandatory. |
| `reference/verify.md` | The committed browser driver (`driver.mjs`): launch a build, sweep overflow, capture errors + GSAP pins + mobile + reduced-motion, screenshot. Prism's verify harness — run it every preflight. |
| `reference/resources.md` | Sourcing **any** asset — 3D models, HDRIs, textures, components (21st.dev + the shadcn ecosystem), motion, icons, fonts, stock, AI-3D, the Blender→web pipeline. **License + commercial-use flagged per source.** Read before pulling anything into a build; **mandatory for paid/client work** (ship only commercial-cleared licenses). |

---

## Modes (optional)

Prism runs the full procedure by default. A leading verb scopes it:

- **`build <thing>`** — full flow, new surface. (Default.)
- **`immersive <thing>`** — lead with the 3D tier decision and `reference/immersive-3d.md`.
- **`animate <target>`** — motion pass only; `reference/motion.md`.
- **`redesign <target>`** — audit-first on existing code; `reference/redesign.md`.
- **`audit <target>`** — evaluate against `reference/preflight.md`, report findings, don't rewrite.
- **`polish <target>`** — final-quality pass: contrast, easing, states, fallbacks.

No verb → run the procedure from the Design Read.

---

## Definition of done

Not "it renders." There are two ways to fail and done means beating **both**: it doesn't look like the AI default (**slop**), and every component genuinely *works* (not **demo-ware**). Concretely: the Design Read was declared; the system is locked and consistent; the layout has no repeated families; every interactive element works and carries the full state matrix; micro-interactions have zero layout shift; contrast passes; motion is motivated and has a reduced-motion path; if Tier ≥ 1, the canvas is lazy-mounted, mobile-handled, and reduced-motion-safe, and Core Web Vitals survive; the **craft self-audit passes** (slop pass + works pass + pixels pass, → `reference/craft.md`); and `reference/preflight.md` passes top to bottom. The bar: **a senior designer AND a senior engineer would both sign off.** If either would send it back, it's not done — keep going. Browser verification via `driver.mjs` is mandatory, not optional — run it and read the screenshots before claiming done.
