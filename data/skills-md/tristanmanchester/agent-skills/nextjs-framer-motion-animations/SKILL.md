---
name: nextjs-framer-motion-animations
description: Adds production-safe Motion for React or Framer Motion animations to Next.js apps, including reveal, hover and tap micro-interactions, whileInView, stagger, AnimatePresence, layout and layoutId transitions, reorder, scroll-linked UI, and lightweight route-content transitions. Use when the user asks to add, refactor, or debug Motion or Framer Motion in App Router or Pages Router codebases, especially around server/client boundaries, reduced motion, LazyMotion, bundle size, hydration, or route transitions. Avoid for GSAP-style timelines, WebGL or 3D scenes, heavy scroll storytelling, or CSS-only effects unless Motion is explicitly requested.
license: MIT
compatibility: Designed for Next.js projects with React 18.2+ and Node package tooling. Works with App Router and Pages Router. Supports legacy framer-motion repos and the current motion package. Bundled scripts use Node.js.
metadata:
  author: openai
  version: "4.0.0"
  category: frontend-animation
  keywords: nextjs,framer-motion,motion,react,animation,ui
allowed-tools: Bash(node:*) Bash(npm:*) Bash(pnpm:*) Bash(yarn:*) Bash(bun:*) Read Write
---

# Next.js + Motion/Framer Motion

## Mission
Build small, purposeful, accessible animations in Next.js using Motion for React (the current package) or legacy `framer-motion`, without breaking server/client boundaries, performance, or usability.

## Use this skill for
- First-render reveals and section entrances
- Hover, tap, and focus feedback on buttons, links, cards, tabs, and navigation
- Scroll-triggered reveals and modest scroll-linked effects
- Modals, drawers, dropdowns, accordions, tabs, and other enter/exit UI
- Layout and shared-element transitions with `layout` and `layoutId`
- Reorderable lists and light route-content transitions
- Debugging Motion behaviour in Next.js

## Do not use this skill for
- GSAP-style timelines or cinematic sequences
- Canvas, WebGL, Three.js, or Lottie-led animation systems
- Heavy parallax or scroll-jacking storytelling
- Large creative-direction rewrites
- Pure CSS effects that do not justify client JavaScript, unless Motion is explicitly requested

## Non-negotiables
- Prefer the lightest Motion API that solves the task.
- Preserve repo consistency. Do not mix `motion` and `framer-motion` imports in the same diff unless the task is an explicit migration.
- Keep animated logic in the smallest possible Client Component boundary.
- Respect reduced motion globally with `MotionConfig reducedMotion="user"` and locally with `useReducedMotion()` when behaviour must change.
- Prefer reusable primitives, variants, and motion tokens over repeated inline animation objects.
- Do not add a global provider, root-layout Client Component, or route-wide animation system unless the request genuinely needs it.

## Default workflow

### 1) Audit the codebase first
Inspect:
- Router type: `app/`, `pages/`, or both.
- Current package: `motion`, `framer-motion`, or neither.
- Existing animation patterns and design-system components.
- Candidate transition boundaries: `app/layout.tsx`, `app/template.tsx`, `pages/_app.tsx`, shared UI shells.
- Whether the change is local animation, mount/unmount animation, layout animation, shared-element animation, reorder, or scroll-linked animation.

If shell access is available, run:
```bash
node scripts/audit-nextjs-motion.mjs --root /path/to/repo
node scripts/inspect-motion-target.mjs path/to/target-file.tsx --root /path/to/repo
node scripts/plan-motion-change.mjs --root /path/to/repo --target path/to/target-file.tsx --task "user request"
```

For broad skill iteration or repo-health checks, also run:
```bash
node scripts/check-motion-antipatterns.mjs --root /path/to/repo
```

### 2) Choose a package strategy
Default rules:
- **New work or modernised motion layer:** prefer the current `motion` package with imports from `motion/react`.
- **Existing repo already on `framer-motion`:** stay consistent unless the task explicitly includes migration.
- **Passive App Router component with no hooks or client-only logic:** `motion/react-client` can be appropriate, but it is an exception, not the default.
- **Leaf animations with hooks, route state, presence, reorder, or interactivity:** use a small Client Component boundary.

See `references/MIGRATION.md` and `references/DECISION_TREE.md`.

### 3) Choose the lightest correct API
Use this decision rule:
- **Simple local animation:** `motion.*`
- **Bundle-sensitive shared shell:** `m.*` with `LazyMotion`
- **Repeated parent/child orchestration:** variants plus `stagger`
- **Mount/unmount or route exits:** `AnimatePresence`
- **Layout changes from React re-render:** `layout`
- **Shared-element transition:** `layoutId`
- **Sibling layout coordination or namespaced shared layout IDs:** `LayoutGroup`
- **Simple scroll reveal:** `whileInView`
- **Scroll-linked progress or parallax:** `useScroll` plus motion values
- **Imperative sequence or external trigger:** `useAnimate`
- **Design-system component wrapper:** `motion.create()` with ref forwarding

See `references/EXPERT_PLAYBOOK.md` and `references/DECISION_TREE.md`.

### 4) Wire it correctly for the router
#### App Router
- **Passive, hook-free animation in a server-friendly file:** consider `motion/react-client`.
- **Interactive or hook-driven UI:** create a small Client Component leaf and keep data fetching server-side.
- **Client wrapper around server-rendered children:** useful for modal shells, drawers, and local visibility wrappers.
- **Route enter/exit choreography:** mount a persistent Client shell from a layout so `AnimatePresence` stays mounted.
- **Segment replay on navigation:** `template.tsx` is useful when you want remount semantics at a specific segment boundary.

See `references/APP_ROUTER.md`.

#### Pages Router
- Keep `AnimatePresence` stable in `pages/_app.tsx` for route transitions.
- Key routed children by a stable value that changes when you actually want a transition. For dynamic routes, `router.asPath` is usually safer than `router.route`.
- Do not rewrite `_app.tsx` for a one-off local animation.

See `references/PAGES_ROUTER.md`.

### 5) Apply the motion budget
Default ranges unless the user or design system says otherwise:
- **Micro-interactions:** 0.12s to 0.22s, scale no larger than 1.03, travel no more than 4px.
- **Reveal / list entrance:** 0.18s to 0.35s, travel 8px to 24px.
- **Page / route transition:** 0.22s to 0.45s, mostly opacity plus small Y translation.
- **Layout animation:** prefer Motion springs or `layout`; do not fake these with large manual transforms.

See `references/EXPERT_PLAYBOOK.md` and `references/PERFORMANCE.md`.

### 6) Validate before finishing
Always check:
- No server/client boundary mistakes
- Reduced motion works
- Focus is preserved for interactive UI
- No unnecessary layout shift or stretched content
- No duplicate or conflicting route wrappers
- Project still builds

Run repo checks when available:
```bash
npm run lint
npm run build
```

For repo audits or skill iteration, also run:
```bash
node scripts/check-motion-antipatterns.mjs --root /path/to/repo
```

Use `references/CHECKLIST.md` before finalising. When improving the skill itself, use `references/EVALUATION.md` and `node scripts/run-evaluation-pack.mjs`.

## Implementation rules
- Prefer animating **transform** and **opacity**. Avoid animating `top`, `left`, large filters, and large shadows on big surfaces.
- When possible, turn the existing root element into a Motion element instead of adding a new wrapper. Extra wrappers often break layout, refs, selectors, or spacing.
- If using `m` plus `LazyMotion`, use:
  - `domAnimation` for standard animations, variants, exit, hover, tap, and focus.
  - `domMax` only when you need layout animations or drag/pan.
- Use `AnimatePresence initial={false}` for app-level wrappers unless first-load animation is explicitly desired.
- Use `AnimatePresence mode="wait"` only when a single child should fully exit before the next enters.
- Never key exit-sensitive children by array index.
- Start with `layout` before manual height choreography. If content stretches, add `layout` to the affected children or switch to `layout="position"` for aspect-ratio changes.
- If the scroll container is not the window, configure `viewport.root` or use `useInView` with the correct root.
- When animating `next/image` or image wrappers, preserve the layout box and animate transform or opacity rather than intrinsic size.
- When wrapping design-system components, call `motion.create()` outside render and make sure the wrapped component forwards its ref.
- If the user did not explicitly ask for Motion and the effect is just a tiny hover or focus style on a static server-rendered element, CSS may be the cleaner answer.

## Scripts
- `scripts/audit-nextjs-motion.mjs` - inspects a repo, ranks likely target files, and emits JSON recommendations.
- `scripts/inspect-motion-target.mjs` - inspects one file and recommends boundary, import path, risks, and likely pattern fit.
- `scripts/plan-motion-change.mjs` - combines repo audit, target inspection, and task wording into a structured expert plan.
- `scripts/check-motion-antipatterns.mjs` - scans a repo for common Motion and Framer Motion anti-patterns and emits JSON findings.
- `scripts/run-evaluation-pack.mjs` - runs the bundled fixture-and-golden evaluation pack for skill iteration.
- `scripts/scaffold-motion-primitives.mjs` - copies template components from `assets/` into a target directory, with optional import rewriting for legacy `framer-motion`.

## Reference map
- `references/EXPERT_PLAYBOOK.md` - API selection, heuristics, motion tokens, anti-patterns
- `references/DECISION_TREE.md` - fast pattern and boundary selection
- `references/APP_ROUTER.md` - App Router boundaries, route shells, `template.tsx`, and server-friendly patterns
- `references/PAGES_ROUTER.md` - `_app.tsx`, keys, dynamic route nuances
- `references/RECIPES.md` - copy/paste implementations
- `references/PERFORMANCE.md` - bundle size, LazyMotion, layout and scroll performance
- `references/ACCESSIBILITY.md` - reduced motion, focus, modal guidance
- `references/MIGRATION.md` - `framer-motion` to `motion` package strategy
- `references/TROUBLESHOOTING.md` - failure modes and fixes
- `references/CHECKLIST.md` - final review before finishing
- `references/EVALUATION.md` - trigger tests, scenario fixtures, anti-pattern scans, and golden-output review

## Output expectations
When modifying a repo, finish with:
1. The files changed
2. The Motion API and pattern chosen
3. Boundary strategy and package migration decision, if any
4. Reduced-motion handling
5. Performance or bundle-size choices, if relevant
6. Manual validation notes or commands run
7. Any caveats the developer should know

## Typical request mapping
- "Make this button feel better" -> micro-interaction recipe
- "Animate cards in on scroll" -> reveal recipe; variants if staggered
- "Add a smooth route transition in App Router" -> persistent layout-mounted shell or content wrapper, not a root rewrite by default
- "Animate this accordion or tab underline" -> `layout` / `layoutId` / `LayoutGroup`
- "Make this drag list reorder smoothly" -> `Reorder.Group` / `Reorder.Item`
- "This breaks in App Router" -> inspect boundary and import path before editing
- "Modernise our Framer Motion setup" -> audit first, then use `references/MIGRATION.md`
