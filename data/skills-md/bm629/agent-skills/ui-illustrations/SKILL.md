---
name: ui-illustrations
description: >
  Use when adding illustrations or imagery to a web app UI — empty states,
  onboarding, error pages (404/500), success moments — or when deciding whether
  imagery helps or clutters a screen. Covers sourcing from the established free
  libraries (unDraw, Storyset, LottieFiles) with license compliance, recoloring
  SVGs to your design tokens so they follow light/dark themes, integrating SVG
  into React/Vite correctly (inline vs img, layout-shift and bundle discipline),
  animated imagery (Lottie) with reduced-motion accessibility, and empty-state
  craft (anatomy, variants, consistency). Keywords: illustration, empty state,
  imagery, SVG, unDraw, Storyset, Lottie, dark mode illustration, onboarding
  art, error page illustration, alt text, decorative image.
extensions:
  claude: {}
  copilot: {}
  cursor: {}
  gemini: {}
  codex: {}
version: "1.0.0"
forge:
  status: reviewed
  forged: 2026-07-11
  reviewed: 2026-07-11
---

# ui-illustrations — Illustration and imagery for product UIs

## Overview

Sources, brands, integrates, and ships illustration in web application UIs. The center
of gravity is the data-dense product tool that today shows bare text where imagery would
carry warmth and clarity — empty states, onboarding, and error pages — without tipping
into decoration. The skill covers the placement doctrine (where imagery helps vs
clutters), the free-library sourcing landscape with its license traps, recoloring
sourced SVGs to design tokens so one asset follows both themes, correct SVG-in-React
integration, animated imagery done accessibly, and the craft of a good empty state. It
sources and integrates existing illustration; it does not teach drawing original art.

## When to activate

- ✅ A screen shows a bare "No items yet" (or worse, nothing) and needs a real empty state.
- ✅ Adding onboarding/first-run, error-page (404/500/permission), or success-moment imagery.
- ✅ Choosing an illustration source, checking whether attribution is required, or matching sourced art to the app's palette and dark mode.
- ✅ Embedding an SVG or Lottie file in a React codebase and wiring its accessibility.

**Do NOT activate when:**

- Icons are the need — icon systems (lucide, Heroicons) are a separate asset class with their own conventions.
- UI element/interaction motion is the need (transitions, micro-interactions) — a motion-implementation skill owns that; this skill owns imagery, including animated imagery *files*.
- Original illustration must be drawn or a full illustration design language authored — that is designer/vendor work; this skill selects and integrates.
- Marketing-site hero/photography art direction.

## Workflow

### Step 1: Placement — does imagery belong here at all?

| Placement | Imagery? | Why |
|---|---|---|
| Empty states (first-run, cleared list, no results) | Yes — the canonical placement | Turns a dead end into orientation + action |
| Onboarding / first-run moments | Yes, sparingly | Sets tone once; not on every visit |
| Error pages (404, 500, permission denied) | Yes | Softens failure, keeps trust |
| Success/completion moments | Optional, small | Reward without delay |
| Persistent data surfaces (tables, dashboards mid-flow) | **No** | Users are reading data; art is noise |
| Loading/progress moments | **No** (usually) | Skeletons/spinners are the pattern — perceived-performance territory, not imagery; a motion skill owns them |
| Auth screens (sign-in split panel) | Acceptable | An established pattern — brand-tone imagery beside the form is fine; still one family, still restrained |
| Beside forms/settings as decoration | **No** | Message-free imagery is clutter (the auth split-panel above is the exception, not the license) |

Proportionality: an ops/admin tool wants restraint — a handful of consistent
illustrations at the placements above; a consumer product tolerates more. If the
illustration carries no message the adjacent text doesn't already carry, cut it.

### Step 2: Source — the decision path

1. **Default: unDraw.** One consistent style across hundreds of concepts, on-site
   primary-color customization, and a permissive license: commercial use and
   modification allowed, **no attribution required**. Its main prohibitions are
   redistributing the assets as packs/competing collections and using them for
   AI-model training.
2. **Animated: LottieFiles free tier (Lottie Simple License)** — commercial use,
   modification, no required attribution (credit encouraged); modifications are
   share-alike (derivatives redistribute under the same license); no compiling the
   files into a competing collection. **Storyset (Freepik)** for animated/richer SVG
   scenes — free tier **requires visible attribution** ("Designed by Freepik" + link,
   clearly findable); a paid Freepik-company subscription removes it (which tier the
   terms name has drifted — confirm on the live terms at adoption); no
   resale/redistribution or trademark/logo use.
3. **Record the license at adoption.** Terms drift (the table above is a dated
   snapshot — forged 2026-07-11); re-check the source's live license page when
   adopting, and record source URL + license + date next to the asset (a
   `assets/illustrations/LICENSES.md` works). An attribution obligation is a shipping
   requirement, not a footnote.
4. AI-generated illustration exists as an option; its caveats — style drift across
   generations and licensing ambiguity — make it a deliberate choice, not the default.

### Step 3: Keep one style family

Style consistency beats volume: 5 illustrations from one family read as designed; 50
mixed ones read as clip-art. Hold constant across every illustration in the product:
geometric-vs-organic, flat-vs-dimensional, line treatment, detail level, and (for
character art) proportions and diversity. Practically: pick one library/family in Step 2
and stay in it; when a concept is missing, choose the nearest in-family metaphor rather
than importing an off-family asset.

### Step 4: Brand-match — recolor to tokens

- Quick path: unDraw's on-site color picker sets the accent to your primary before
  download.
- Durable path: inline the SVG and replace hardcoded fills with semantic tokens —
  `fill="#6c63ff"` → `fill: var(--primary)` (style attribute or CSS) — so the SAME
  asset follows theme switches, including dark mode. Keep skin tones and true neutrals
  literal; tokenize accents, clothing, objects, and background shapes.
- Details in `references/svg-integration-and-theming.md` (incl. the three dark-mode
  strategies — most light-theme art breaks on dark backgrounds unaltered).

### Step 5: Integrate correctly

- **Inline component** (Vite: `import Art from "./empty.svg?react"` via the SVGR
  plugin) when you need token recoloring or a11y control from CSS/React.
- **`<img src>`** (`import artUrl from "./empty.svg?url"`) for larger static art:
  cacheable, lazy-loadable (`loading="lazy"`), no CSS reach inside.
- Always prevent layout shift: the SVG keeps its `viewBox`, and the slot has explicit
  dimensions or `aspect-ratio`.
- Bundle discipline: inlined SVG ships in the JS bundle — inline the small
  above-the-fold empty-state art, `img`+lazy the rest.
- Full decision table + Lottie embedding: `references/svg-integration-and-theming.md`.

### Step 6: Accessibility defaults

- Empty-state/decorative art: `aria-hidden="true"` (inline) or `alt=""` (img) — the
  adjacent heading/text carries the message. An image that itself informs gets real
  `alt` text.
- Animated imagery must respect `prefers-reduced-motion` (render the static first
  frame) and, if the auto-playing motion runs longer than 5 seconds total (looping or
  not), needs a pause control (WCAG 2.2.2).
- Contract details + the empty-state anatomy and variants:
  `references/empty-states-and-a11y.md`.

## Rules

**Hard rules (never violate):**

- **Check the license before shipping an asset**; record source + license + date next
  to the asset. Ship required attribution visibly (Storyset free tier) or don't ship
  the asset.
- **No imagery on persistent data surfaces** — empty states, onboarding, errors, and
  success moments only, unless the owner explicitly directs otherwise.
- **One style family per product.**
- **Decorative imagery is hidden from assistive tech** (`aria-hidden`/empty `alt`);
  informative imagery gets real alternative text.
- **Animated imagery respects reduced motion** — static fallback under
  `prefers-reduced-motion`, pause control for auto-playing motion >5 s total.
- **Never redistribute sourced assets as collections** — every listed source prohibits
  it; use within your product only.

**Preferences (override-able):**

- unDraw as the default source; Storyset/Lottie when animation earns its place.
- Illustration supports, never dominates: cap empty-state art around 160–240 px tall
  on desktop, smaller on mobile.
- Tokenized recolor over per-theme asset pairs when the art allows it.

## Gotchas

- **Storyset's attribution is a real obligation** — "free" there means
  attribution-required; hiding the credit in a footer nobody can find fails the terms.
  unDraw and Lottie-Simple-License assets need none.
- **Light-theme art breaks silently on dark mode:** baked-in white shapes glow, dark
  strokes vanish. Audit every illustration in both themes; fix via tokenized fills or
  per-theme pairs — an untouched sourced SVG is almost never dark-safe.
- **The SVG's own `<title>` leaks:** many downloaded SVGs carry a `<title>`
  ("undraw_empty_4zx0") — AT announces it when `aria-hidden` is forgotten, and browsers
  show it as a hover tooltip regardless; strip it (or make it meaningful) when
  inlining, in addition to `aria-hidden`.
- **CLS from missing dimensions:** an SVG without reserved space pops the layout when
  it loads (especially `img` + lazy). Reserve the slot.
- **Inlining everything bloats the bundle:** a 40 kB illustration inlined into a shared
  chunk ships to every route. Inline only what needs CSS reach; `?url` the rest.
- **`currentColor` is not a palette:** it recolors monochrome glyphs, not multi-color
  illustrations — those need explicit token substitution per fill.
- **Lottie share-alike:** a modified Lottie-Simple-License animation redistributes
  under the same license — fine inside your app, a trap if you publish asset packs.

## Anti-patterns

- **"Add illustrations everywhere — it looks friendly."** Placement doctrine first;
  imagery without a message is clutter, and data surfaces stay clean.
- **"It's free, just use it."** Free tiers differ exactly on the obligation that bites
  (attribution); check and record the license.
- **"Mix the best illustration from each library."** Style-family consistency beats
  per-asset quality.
- **"Ship now, dark-mode the art later."** Later means a visual bug report; audit both
  themes at integration time.
- **"It's just decorative, skip the a11y attributes."** Decorative is an a11y decision
  you implement (`aria-hidden`/`alt=""`), not one you skip.

## Output

Illustrated UI surfaces in a React codebase: sourced, license-recorded assets under the
project's asset convention; empty states/onboarding/error pages carrying consistent,
token-recolored, theme-safe, accessible imagery; animated imagery gated on reduced
motion. Consumers are the codebase's reviewers and the design-system doc, which records
the product's chosen family and placement rules.

## Related

- A motion-implementation skill (Motion for React) owns UI element/interaction
  animation and the reduced-motion contract this skill's animated-imagery rules
  reference; imagery *files* (incl. Lottie) are owned here.
- An icon-system convention (lucide et al.) owns icons — a separate asset class.
- A design-system skill/doc records which family, tokens, and placements THIS product
  locked; this skill is the portable how-to it applies.
- A component-styling skill (Radix/Tailwind) owns the components the imagery sits in.

## Progressive disclosure

- `references/sourcing-and-licensing.md` — load when picking a source, checking terms,
  or handling attribution/generated-art questions.
- `references/svg-integration-and-theming.md` — load when embedding SVGs (inline vs
  img vs Lottie), recoloring to tokens, or fixing dark mode.
- `references/empty-states-and-a11y.md` — load when building empty states/onboarding/
  error pages or wiring imagery accessibility.
- `references/sources.md` — research provenance; load only when auditing claims.

## Body budget

- `description` ≤ 1,024 chars (agentskills.io cap).
- Body ≤ ~500 lines / 5,000 tokens soft target; overflow lives in `references/`.
