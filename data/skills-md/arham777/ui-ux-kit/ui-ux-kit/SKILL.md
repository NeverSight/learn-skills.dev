---
name: ui-ux-kit
description: >-
  Design and improve ANY web or app interface with a taste-first,
  anti-AI-slop workflow, then document the result in a project DESIGN_SYSTEM.md
  so every future page stays visually consistent. Universal: routes the brief to
  the right rules for a landing/marketing page, dashboard/admin, product/app UI,
  e-commerce/store, content/editorial/docs, mobile/native app, a redesign, or a
  design-system-only task. The engine is web-first (CSS/tokens/Tailwind); for
  iOS/Android it layers platform-idiom guidance over that engine and defers deep
  platform-component work to HIG/Material. Use when the user
  asks to design, build, redesign, audit, or polish any interface — especially
  when they mention a brand name, color palette, mood/style, fonts, animations,
  card style, image source, framework, or platform (web / iOS / Android).
  Triggers: "design a landing page", "build a dashboard", "design a mobile app",
  "build a store / product page / checkout", "design a docs or blog site",
  "redesign this", "make the UI look premium", "create a design system", "audit
  the UX", "clean up the design", "find design references / inspiration", "make it
  faster", "improve performance / Core Web Vitals".
---

# UI/UX Kit

Design interfaces that look intentional and brand-specific — never templated — and
leave behind a single source of truth (`DESIGN_SYSTEM.md`) that keeps every future page
consistent. Works for every surface: marketing, dashboards, apps, stores, content/docs,
mobile, redesigns, and standalone design systems.

Follow the steps in order. Four are non-negotiable:
- **Step 1 routing** — apply the *right* rules, not one recipe.
- **Step 2.7 concept** — commit to one distinctive idea before building.
- **Step 4.5 adversarial review** — judge the work as a critic, not its author.
- **Step 5 documentation** — leave a `DESIGN_SYSTEM.md` behind, always.

One law above all: **read the brief and adapt.** Every rule is the smart default, not a
reflex. When the brief contradicts a default, the brief wins — say so and proceed.

This file is the always-loaded core. Heavier detail lives in `references/` and is loaded
on demand:
- **`references/surface-rules.md`** — per-surface rules (landing, dashboard, app, mobile,
  store, content). Load your Step 1 profile's section before building.
- **`references/quality-floor.md`** — Step 3/4 depth: the contrast computation, gradients/
  glass, icons, images, the full accessibility floor, the nine performance levers, and the
  official-design-system table. Load it when you reach Step 3.
- **`references/experiential.md`** — 3D/WebGL/physics tier. Load only if Step 2 picks it.
- **`references/component-libraries.md`** — capability→library cheatsheet.
- **`references/DESIGN_SYSTEM.template.md`** — the Step 5 deliverable template.

---

## Step 1 — Analyze the request, then ROUTE (REQUIRED)

### 1a. Extract the brief
Identify: **surface type** (landing/marketing, dashboard/admin, app/product, mobile,
store, portfolio, redesign, design-system-only), **brand**, **industry**, **audience**,
**design style**, **color system** (map to 60/30/10), **typography intent**,
**animation level**, **card/section style**, **image strategy**, **tech stack/platform**.
If the user gave only colors + a name, infer the rest from industry and style — but list
your inferences so they can correct you.

### 1b. State a one-line Design Read
> **"Reading this as: a `<surface>` for `<audience>`, `<style>` direction,
> `<color/type/motion summary>`, built in `<stack>`."**

### 1c. Route to a surface profile (first match wins; note hybrids)

Match the profile, then **immediately use the Read tool to open the listed
`references/surface-rules.md` section before building** — its rules and per-surface gate
are required, not optional. A hybrid brief reads two sections.

| Profile | Pick when | → Read now |
|---|---|---|
| **Landing / Marketing** | landing, marketing, campaign, portfolio, long-form | `references/surface-rules.md` §B1 — page anatomy + hero + conversion |
| **Dashboard / Admin / Data** | dashboard, admin, analytics, console, internal tool | `references/surface-rules.md` §B2 — density, tables, charts |
| **App / Product UI** | web app, SaaS surface, settings, onboarding, flows | `references/surface-rules.md` §B3 — navigation + forms + full state set |
| **E-commerce / Store** | store, shop, catalog, PDP, cart, checkout | `references/surface-rules.md` §B5 — listing, PDP, cart, checkout, trust |
| **Content / Editorial / Docs** | blog, article, docs, KB, news, long reading | `references/surface-rules.md` §B6 — reading measure, TOC, prose |
| **Mobile / Native** | iOS, Android, React Native, Flutter | `references/surface-rules.md` §B4 — HIG/Material, touch, safe areas |
| **Redesign** | "redesign / improve / fix / clean up" existing UI | Audit first (1d), then Read the matching profile's section |
| **Design-system-only** | "create a design system / tokens / DESIGN_SYSTEM.md" | Skip page building → Step 3 → 4 → 5; the artifact IS the deliverable |

### 1d. Redesign audit (Redesign profile only)
Before changing anything, read the existing code/UI and list (a) what works and must be
preserved (brand, palette, IA, components), (b) the concrete slop/quality issues scored
against Step 3 + the pre-flight gate, (c) the minimal set of changes that fixes the most.
Never overhaul what isn't broken. **Seeing the current UI is part of auditing it** — the
"don't open a browser unless asked" rule is about verification theater *after* building,
not this. You **may** render/screenshot the current state to ground the audit (say so);
if you can't, note the audit is code-only with reduced confidence.

### 1e. The category-reflex test (run before choosing colors/theme)
If someone could guess your palette from the **domain alone** — "fintech → navy + gold",
"healthcare → white + teal", "crypto → neon on black", "coffee → cream + brown", "AI
startup → purple gradient on dark" — that's the training reflex, not a decision. Rework
until the answer is no longer obvious from the category. The brief overrides only when it
explicitly names those colors.

---

## Step 2 — Clarify only what's missing (REQUIRED)

**Use what the user gave. Only ask for genuine gaps.** Re-asking provided info is its own
failure.

1. **Inventory the prompt** — mark each checklist item **provided** (even if loosely
   phrased — "fintech startup", "brand blue #1A4FFF", "Next.js repo" all count) or
   **missing**.
2. **Ask only missing items** via `AskUserQuestion`, batched ≤4 (usually ≤1 round, often
   zero). If all provided, skip questions and restate the brief.
3. **Never re-ask, never override** a named framework/palette/niche/library.

**Checklist (ask each ONLY if missing):**
1. **Niche / industry** — drives mood + imagery.
2. **Tech stack / platform** — adopt an existing project's stack without asking.
3. **Design direction** — offer: Minimal, Modern, Editorial, Bold, Luxury, Brutalist,
   Playful.
4. **Color scheme** — don't assume. Propose 2–3 named palettes (with hex) or ask for
   theirs. If given, map to 60/30/10 and move on.
5. **Animation level + library** — None / Subtle / Smooth / Motion-rich, **and** GSAP /
   Framer Motion / CSS-only.
6. **Image / asset strategy** — AI-generated, stock, web, or user-provided.
7. **Experience tier** — **Standard** (DOM + CSS/GSAP/Framer — the right default) or
   **Experiential** (3D/WebGL/physics — only when the user wants an immersive experience
   and the content justifies it; if picked, **Read `references/experiential.md` before
   building the scene**). Match the tier to the need — never force 3D, never flatten an
   immersive brief.

**Logo is a separate question** (ask on its own only if unhandled): offer AI-generated /
niche web image / text wordmark, and tell the user up front to supply logos as SVG/PNG.

After answers, restate the full brief in one paragraph, then proceed.

---

## Step 2.5 — AI asset generation (never silently bail)

When the user chooses **AI-generated**, produce real images — don't probe for an API key,
find none, and downgrade to a placeholder. Order:
1. **`/chatgpt-image-gen` — PREFERRED, no API key.** Drives the user's logged-in ChatGPT
   via browser. If not logged in, tell them clearly ("A Chrome window is open — log in,
   then tell me") and **WAIT** for confirmation. **Non-interactive/headless runs** (no one
   to log in): skip straight to option 2, and if that's unavailable, scaffold with a
   clearly-marked placeholder asset module and note it must be regenerated — never block a
   headless run waiting on a login that can't happen.
2. **`/ai-image-generation`** (inference.sh) when `INFERENCE_API_KEY` is set or supplied;
   if missing, ask or offer to switch to `/chatgpt-image-gen`.

For *reference* images before building, consider `/imagegen-frontend-web` (one per
section) or `/imagegen-frontend-mobile`. Fall back to a custom SVG/text mark only if the
user explicitly agrees. Keep generated assets isolated (one `Logo` component / assets
module) so they're swappable from one file.

---

## Step 2.6 — Pull real design references (REQUIRED for non-trivial work)

Ground the design in proven award-winning work, not the model's averaged defaults — one
of the strongest anti-slop moves. Skip only if the user says "no research" or supplies
references.

**If web access is unavailable:** say so, then compensate — reason from named exemplars
("Linear's density / Stripe's restraint / Arc's playfulness") and lean harder on Step 2.7
and the category-reflex test. State that references were unavailable.

**The style word is a first-class search driver.** When the brief names a direction
(minimal, editorial, brutalist, luxury, bold, playful, modern, swiss…), run **three**
style-keyed searches and let them set the design before building:
- **Reference designs of that style** — "`<style>` `<surface>` design awards".
- **Color schemes for that style** — "best palettes for `<style>` `<industry>`" — then run
  results through the category-reflex test before committing.
- **Fonts for that style** — "best fonts for `<style>` `<surface>`" — confirm/sharpen the
  Move A→C pick.

**How:** WebSearch the galleries, then WebFetch the top hits for concrete patterns.
**Text-fetching image-heavy galleries (Awwwards, Dribbble) returns little visual signal**
— for true visual grounding prefer a vision browse (`/use-my-browser` / `/agent-browser`
to screenshot) or named exemplars; use `WebFetch` mainly for structure, names, copy. For
login-gated sources use the browser skills with a live session. Deep sweep: `/deep-research`.

**Sources:** Landing/brand → Awwwards, Godly, Land-book, Lapa Ninja, Httpster, Refero.
App/dashboard → Mobbin, Page Flows, UI Sources, Refero. Mobile → Mobbin, Apple/Google
galleries. Mood → Dribbble, Behance, Cosmos, Savee.

**Translate, never clone.** Adapt every reference into the project's own tokens. Output a
short "References pulled" note: 3–5 links + the specific move adapted from each.

---

## Step 2.7 — Commit to ONE design concept (REQUIRED)

Avoiding banned patterns still leaves clean-but-bland. The fix is positive: commit to a
single distinctive concept before building, and let it drive specific decisions.

Write it as one sentence — a concrete organizing idea, not an adjective:
> **"The concept is: `<one specific idea>` — expressed through `<layout>`, `<type>`,
> `<color>`, `<motion>`."**

- *Weak:* "modern, clean, professional fintech dashboard." (defaults, not a concept)
- *Strong:* "a trading terminal that feels like precision instrumentation — mono numerals
  everywhere, hairline grid, near-black field with one signal-green accent, data animates
  in like a ticker."

The concept must be **falsifiable** (if it could describe any competitor, sharpen it) and
show up in ≥3 of {layout, type, color, motion, imagery}. Record it as the design system's
"Design personality / concept." The adversarial review checks it landed.

---

## Step 3 — Design with taste (the quality bar)

**Shared laws below apply to every surface.** Before building you must have **Read** both
your Step 1 profile's section in `references/surface-rules.md` **and**
`references/quality-floor.md` (contrast math, gradients/glass, icons, images, the full a11y
floor, the nine perf levers, the official-design-system table). Apply those on top of these
laws. If you haven't opened them yet, do it now.

### Color — strategy first, then 60/30/10, in OKLCH
- **Pick a strategy first:** **Restrained** (tinted neutrals + one accent ≤10% — product/
  dashboard default), **Committed** (one saturated color carries 30–60%), **Full palette**
  (3–4 named roles), **Drenched** (the surface IS the color). The "≤10%" rule is
  Restrained-only — don't collapse everything to it by reflex.
- **60/30/10:** 60% dominant (backgrounds/large surfaces), 30% secondary (raised sections/
  cards), 10% accent (buttons/links/focus rings).
- **Work in OKLCH.** Reduce chroma near L 0 or 100. **Tint every neutral toward the brand
  hue** (chroma ~0.005–0.01) rather than using raw `#000`/`#fff` — *unless the concept
  explicitly calls for pure ink* (brutalist, hard-edged editorial, true-OLED black), in
  which case pure `#000`/`#fff` is a deliberate, documented choice, not a default.
- **One palette per project.** No warm/cool drift; no surprise CTA color in section 7.
- **Dark mode is derived, not inverted.** Theme semantic tokens (`--bg`, `--surface`,
  `--surface-raised`, `--text`, `--text-muted`, `--accent`) — never flip raw hex. In dark:
  tinted near-black (~L 0.15–0.20), **raise surfaces by getting lighter** (shadows barely
  read), **lower accent chroma / raise its lightness**, and re-verify every text pair's
  contrast independently.

### Separation by depth first, not borders-by-reflex
- **Background contrast + (hue-tinted) shadow is the *primary* way to separate and elevate
  containers — not a border drawn around everything.** A border is not banned outright; it
  is the wrong *default* for elevation. Borders are legitimate and expected for: input/
  control outlines that need a perceivable edge on a flat surface, thin token dividers in
  dense data UIs, table cell/row rules, and `:focus-visible` rings. Use them for those
  jobs; don't use them as the go-to device for separating cards and sections.
- Never nest an elevated surface in another (no card-in-card-in-card).
- One depth hierarchy: **page base → raised section → floating element.**
- **Elevation/selection state changes through background color**, not by toggling a
  decorative border on and off.

### Text contrast (enforce — never ship gray-on-white body)
- **Body/supporting text meets WCAG AA (≥4.5:1)**; large text (≥24px or ≥19px bold) and
  UI/graphical elements ≥3:1. Light-gray on near-white (e.g. `#9aa` on `#fff`) is a fail.
- **Verify by computing, not by eye**, in light and dark separately — the linearization
  formula and the OKLCH-Δ45 pre-check are in `references/quality-floor.md`. Don't assert
  "passes AA" without the number.
- Muted/secondary copy is still high-contrast — darken until it reads clearly.

### Typography — choose fonts FOR THE BRAND, then lock one scale
Typography is the fastest way a design reads as generic. **Never reuse the same fonts by
reflex.** Choose in three moves:

**Move A — name the personality** (1–2 words): corporate-clean, editorial-luxury,
warm-human, bold-loud, playful/funky/cartoon, minimal-swiss, brutalist-technical,
elegant-fashion. **There is always a personality** — if the brief states none, infer one
from industry + audience. Inferring is what makes type read as chosen, not templated.

**No-signal default = a neutral grotesque, never a serif.** When the personality is
neutral/modern/corporate/minimal (the common "professional/clean/unstated" case), pick a
self-hostable grotesque sans from the Corporate-clean row below and **say which and why**
— rotate by sub-nuance (Geist, Hanken Grotesk, Mona Sans, Neue Montreal, Space Grotesk all
qualify) rather than reaching for the same one every time; mandating a single font is its
own reflex. Reach for a serif/display face only when the personality is *explicitly*
editorial-luxury, elegant-fashion, or heritage — a serif on a "modern minimal" brief is a
mis-inference and a fail.

**Move B — map personality → category → pick a face** (self-hostable / Google Fonts unless
the brand owns one). The **personality→category→face lookup table is in
`references/quality-floor.md`** — pick the row that fits *this* brief's nuance, and write
one line tying the face to the personality (if it'd read the same on any brief, you picked
by reflex).

**Move C — pair with intent.** Heading carries the personality; body stays quiet and
readable; both in the same emotional family. Max 2 families (+ optional mono). Emphasis =
italic/bold of the *same* family.

**Anti-reflex (enforce):** don't default to Inter; for a no-signal brief pick a grotesque
sans (never a serif) and justify the specific face; don't reach for serif just because the
brief says "creative/premium"; a playful/cartoon brand must NOT get a corporate grotesque.

- **Define the type scale ONCE as tokens** (`display`, `h1`, `h2`, `h3`, `body-lg`,
  `body`, `body-sm`, `caption`, `button`) and reference them everywhere — no inline
  one-off sizes; same role = same size every section.
- **Minimums:** body never below **16px**; captions ~13–14px; line-height ~1.5; line length
  60–75ch.
- **Responsive scaling is part of the scale** — prefer fluid `clamp()`; headings scale down
  on mobile; never clip or truncate.

### Components (build them reusable)
Buttons, cards, badges, navbar, footer, forms, inputs, feature/CTA sections — plus
feedback primitives (Toast, Spinner, Modal, Skeleton, empty/error state) — each defined
once and reused. Interactive states live inside the primitive. No one-off inline variants.
Select a component base by capability (see `references/component-libraries.md`); **one
styled base per project**, re-themed to your tokens — never a library's default look.

### Interaction feedback & states (nothing static or silent)
- **Every interactive element ships its full state set:** default, hover,
  **focus (`:focus-visible`, not `:focus`)**, **active/pressed** (visible — slight
  scale-down + shadow shift, fires immediately), disabled.
- **Focus ring uses `:focus-visible` so it appears for keyboard/programmatic focus only and
  stays hidden on mouse click.** A ring that flashes on every mouse click reads as slop —
  but the fix is `:focus-visible`, **never** `outline:none` or deleting the ring (that
  fails WCAG 2.4.7 and locks out keyboard users). Many component libraries ship `:focus`
  (mouse-visible) by default — re-map them to `:focus-visible`.
- **Floating elements stay on-screen.** Tooltips, dropdowns, popovers, menus, selects, and
  date pickers must use collision-aware positioning — flip/shift to stay inside the
  viewport, never overflow or get clipped at an edge. Use the Popover API / `anchor`
  positioning or a positioning engine (Floating UI, or Radix/Headless UI which bundle it);
  never hand-position with a fixed offset that runs off-screen near the edges.
- **Async actions** show a **loading state** the moment they start (label → working verb +
  spinner, or skeleton). Never freeze the UI unexplained.
- **Resolve every action** with explicit success/error (toast / inline / micro-feedback)
  — paired with icon or label, never color alone.
- **Forms:** inline validation on blur (not keystroke), errors below the field, visible
  required markers, helper text, label above input (never placeholder-as-label). Disable
  submit only with a visible reason.
- **Data views design three states:** empty (helpful, branded), loading (skeleton/spinner),
  error (recoverable + retry). Drive all from shared components + motion tokens.

### Motion
- Consistent, purposeful; reuse the same durations/easings. Micro-interactions ~150–300ms;
  ease-out entering, ease-in exiting; avoid linear. Animate **only `transform`/`opacity`**.
- **Motion must be motivated** — communicates hierarchy, feedback, storytelling, or state.
  If you can't name what it communicates in one sentence, drop it.
- **Always support `prefers-reduced-motion`** — instant, content fully visible. Pointer
  cursor on all interactive elements.

### UX copy & content (write like a person, not a placeholder)
- **Specific over generic.** Headlines say what the thing *does* for *this* audience — not
  "Elevate your workflow / Seamless solutions / Next-gen platform." If it fits any company
  in the category, rewrite it.
- **Verb-first CTAs:** "Start the 14-day trial" > "Get started"; one label per intent.
- **Real or honestly-marked mock data** — never "Acme / John Doe / Lorem ipsum" shipped as
  real; no invented fake-precise stats.
- **Microcopy carries UX:** empty states explain the next action; errors say what happened
  + how to fix (never bare "Something went wrong"); loading buttons name the work.

> **Icons, images, gradients/glass, the full accessibility floor, and the
> official-design-system honesty table now live in `references/quality-floor.md` — apply
> them as part of this step.**

---

## Step 4 — Build (source-of-truth first, modular always)

1. **Tokens first.** One tokens layer (CSS vars / theme / Tailwind config) for every color,
   the type scale, spacing, radii, shadows, motion durations/easings. **Nothing hardcodes a
   value.** Mirrors `DESIGN_SYSTEM.md` exactly.
2. **Modular components, small files.** Reusable primitives once, then compose pages. One
   responsibility per file; split when a file grows. States live in the primitive.
3. Use only approved colors + defined components; animate from shared motion tokens; use
   matched imagery; make every page responsive (verify each section per breakpoint).
4. **Layer cleanly** — primitives hold no business logic / no data fetching; feature modules
   own data/state; shared logic lives in a common location, not cross-imported.
5. **Verify dependencies** — check `package.json` before importing; output the install
   command if missing. Match the project's package manager (detect from lockfile; no
   lockfile → `pnpm`).
6. **Experiential tier is code-split and isolated** (see `references/experiential.md`) — the
   Standard page renders and is usable before and without the 3D layer.

### Performance & delivery (production-ready means fast)
Target **Core Web Vitals: LCP < 2.5s, CLS < 0.1, INP < 200ms.** Apply all **nine levers**
— the full list is in `references/quality-floor.md`. In short: perceived speed, smaller
first load, critical-path-first CSS, ship less JS, lazy-load below-fold, protect the main
thread, stable layouts (CLS), optimized images, smart caching.

### Engineering principles
- **DRY / KISS / YAGNI** — any value/logic appearing twice is declared once; simplest thing
  that works; build only what's needed now.
- **Code lazily (`/ponytail` ladder):** native HTML/CSS before a JS lib (`<dialog>`,
  `<details>`, scroll-snap, `:has()` before a dependency); installed dep before a new one;
  one line before fifty; fewest files. Mark deliberate shortcuts with a `ponytail:` comment.
  If `/ponytail` is installed, invoke it for non-trivial components; if not, just follow the
  ladder.
- **Ponytail governs *how you implement*, not *what the design requires*.** Never lazy away:
  the token layer, reusable primitives, the full state set, empty/loading/error states,
  accessibility, the adversarial review, or `DESIGN_SYSTEM.md`. Be lazy on mechanism; never
  on the design system itself.

---

## Step 4.5 — Adversarial review (REQUIRED before documenting)

Judge as an adversary, not the author. **Your goal this pass is to make the case that the
design is generic.** Any "yes-it's-generic" is a finding to fix:
1. **Concept test.** Cover the brand name — could this be any competitor? If yes, sharpen
   and re-apply the Step 2.7 concept.
2. **Reflex test (1e), as attacker.** Is the palette guessable from the category? Is the
   type the familiar default? Assume yes; try to prove yourself wrong with specifics.
3. **Reference test.** Name the specific premium move each section earns. Any section whose
   honest answer is "the default AI layout" gets reworked.
4. **One real weakness.** State the single weakest part out loud and fix it. A review that
   finds nothing didn't review.
5. **Hero composition self-check (landing/marketing).** Name out loud which composition the
   hero uses — centered editorial / oversized-typographic / full-bleed / asymmetric-off-grid
   / split. **If the answer is "split,"** write the one specific distinctive move that earns
   it; if you can't, it's the reflex left-text/right-image template — rebuild it as a
   non-split composition. Also confirm: hero vertically centered, no empty band above it, no
   sparkle/AI-icon or vague-tagline eyebrow. (When no browser is available to screenshot,
   this stated self-check is your last line of defense against the render-only hero slop.)

For high-stakes briefs, run this as a genuinely separate pass (fresh read or subagent).
Record the concept-test verdict in the design system, then run the countable gate.

---

## Step 5 — Document in DESIGN_SYSTEM.md (REQUIRED)

After any full design **or** improvement, create `DESIGN_SYSTEM.md` at the project root
from `references/DESIGN_SYSTEM.template.md`, filling every section with the **actual values
used** (real hex/OKLCH, real fonts, real component specs) across all 14 sections. Record the
**surface profile** (Step 1) in section 1 so future work routes the same way. Then tell the
user, verbatim:

> "Your project now includes a `DESIGN_SYSTEM.md` file. Use this file as the design guide
> for future pages, sections, and components so the full website remains visually
> consistent."

---

## Pre-flight check — COUNTABLE anti-slop gate (the single source of truth)

Anti-slop is **counted**. Any failure means not done. This gate is the canonical list —
`DESIGN_SYSTEM.template.md` §12 points back here rather than restating it, so there is one
list to maintain. Run the universal gate below, plus your profile's gate at the end of its
`references/surface-rules.md` section.

### Hard bans (any hit = fail)
- ❌ Any color outside the approved palette; default purple/blue-purple gradient (unless
  approved); raw `#000`/`#fff` **used by default** (pure ink is allowed only when the
  concept explicitly calls for it — brutalist / hard editorial / true-OLED — and it's
  documented).
- ❌ Lucide by default; mixed icon families; emojis as structural icons.
- ❌ Low-contrast text (any body/supporting pair <4.5:1, light OR dark).
- ❌ Body text below 16px; any inline one-off size not mapped to a scale step.
- ❌ Typography not matching personality (playful brand on corporate grotesque; editorial on
  generic sans; a serif as the no-signal default where a grotesque sans is correct); the
  same pairing reused by reflex instead of chosen via Move A→C.
- ❌ Borders used as the *primary* device for separating/elevating cards and sections, or an
  elevation/selection state changed by toggling a decorative border. (Input outlines, token
  dividers, table rules, and focus rings are fine — they're not elevation.)
- ❌ Nested elevated surfaces (card-in-card-in-card).
- ❌ A static interactive element (missing hover/focus/active/disabled); a silent async
  action (no loading + success/error); a blank empty/loading/error screen.
- ❌ Clipped hero text; truncated mobile text; any content clipped/overflowing at any
  breakpoint — incl. a hero overflowing vertically at ~700–800px laptop height, or
  top-aligned instead of centered, or an **empty full-width band/gap above the hero**
  (a stray spacer or empty section pushing content down off-center).
- ❌ **The left-text / right-image (or right-mockup/video) hero split is a FAIL by default**
  — it is the single most templated hero on the web. It counts as done *only* if you wrote
  down the specific distinctive move that earns it (asymmetric ratio, image bleeds off the
  edge, an overlap/depth or motion move) AND it lands. A plain 50/50 text-left + rounded
  image-card-right is an automatic fail — pick another composition (centered editorial,
  oversized-typographic, full-bleed, asymmetric/off-grid) instead.
- ❌ A **decorative sparkle / ✨ / ✦ / magic-wand / "AI" star icon** in an eyebrow, badge, or
  pill (the "✨ AI-powered" tell); an eyebrow that's a vague tagline ("From colors to a
  complete system") rather than a real section label/category. Eyebrows carry information,
  not decoration.
- ❌ A focus ring that appears on **mouse click** (used `:focus` instead of `:focus-visible`,
  or shipped a library's mouse-visible default) — fix with `:focus-visible`, never by
  removing the ring.
- ❌ A floating element (tooltip / dropdown / popover / menu / select / datepicker) that
  **overflows or is clipped at the viewport edge** — must flip/shift to stay on-screen via
  collision-aware positioning.
- ❌ A designed horizontal card row with a visible native scrollbar (incl. the phantom
  vertical bar from `overflow-x:auto` — set `overflow-y:hidden` + hide bars); raw
  `overflow-x` with no snap/controls/smoothing; hard-cut edges with no `mask-image` fade; a
  half-clipped card beside a scrollbar.
- ❌ Gradient text (`background-clip:text`); decorative glass; side-stripe `border-left/right`
  accents.
- ❌ Giant do-everything files.
- ❌ 3D forced onto a brief that didn't ask, or an immersive brief flattened; a WebGL scene
  with no fallback / no mobile degrade / no reduced-motion static; copy baked into canvas;
  heavy 3D/animation bundle in the critical path.
- ❌ Generic AI-SaaS layout pasted without adapting; palette guessable from the category;
  a design that fails the concept test; generic filler copy.
- ❌ A library/registry component in its **default theme** (stock shadcn/Aceternity/Magic UI,
  default gradients, demo copy); more than one styled component base in one project.
- ❌ A hand-rolled `div`+onClick widget where an accessible primitive exists; or a whole
  library pulled for what native HTML/CSS or an installed dep already does.

### Countable limits
- **Eyebrows** (small uppercase tracked labels): **≤ ceil(sections ÷ 3)**, and each must be
  a real label/category — no decorative sparkle/AI icon, no vague tagline as an eyebrow.
- **Consecutive zigzag** (alternating image+text rows): **≤ 2 in a row**; the 3rd breaks the
  pattern.
- **One label per CTA intent** across the whole page.
- **One primary CTA style**, reused; secondary quieter; CTA text one line (≤3 words primary).
- **Marquee ≤ 1 per page.** **Theme:** light/dark inversion must be a deliberate, repeated
  system, never accidental drift; every text pair passes AA in both. Utility surfaces stay
  single-theme per view.
- **Layout-family repetition:** a multi-section page uses ≥3 different section layout families.
- **Fake-precise numbers / generic names / filler copy** = 0 unless real or marked mock.

### Performance gates
- ❌ Any image/media/embed without `width`/`height` or `aspect-ratio`.
- ❌ Hero/LCP image not prioritized; below-fold images/components not lazy.
- ❌ Animating any property other than `transform`/`opacity`.
- ❌ Web fonts without `display: swap`; render-blocking non-critical CSS/JS on the critical
  path.
- ❌ A heavy/3D bundle on the initial path; continuous scroll/mouse driven through component
  state.
- ✅ **All nine levers applied.** The CWV numbers are the goal those levers serve — state them
  as "targeted via the levers"; report a number only if you actually measured it.

---

## Verify before done

1. **Typecheck.** Run the project's typecheck (`<pm> run typecheck`, or `<pm> exec tsc
   --noEmit`, or the lint command) using the detected package manager. Don't run a
   production build just to find errors.
2. **Compute, don't eyeball, the things that are computable.** Run the contrast ratios in a
   one-off script (formula in `references/quality-floor.md`). This is required, not optional.
3. **Render-verify the things that are *only* observable after layout — this is not
   verification theater, it is the only way to confirm them.** The gate asserts several
   *rendered* outcomes that cannot be read from source: the hero fits inside `100svh` at
   ~700px and ~800px laptop heights, nothing clips/overflows at 375/768/1280 widths, and a
   horizontal rail shows no phantom scrollbar. For those specific items, **take a quick
   headless screenshot at those viewports** (`/use-my-browser`, `/agent-browser`, or
   Playwright) and confirm — *or*, if you genuinely cannot render, say so explicitly and
   downgrade the claim from "verified" to "built to target, not visually confirmed." Do not
   assert a render-only gate item passes without having looked. (This is the one sanctioned
   exception to "don't open a browser to verify"; the rule still bans decorative
   after-the-fact screenshotting of things you already know from the code.)
4. **Adversarial review (4.5) + the countable gate**, one final time, before declaring
   complete.

## Future work & updates
Every future page reuses the colors, typography, spacing, components, icons, cards,
animation, and image style from `DESIGN_SYSTEM.md` — no new visual style unless the user
updates it. If anything changes, update `DESIGN_SYSTEM.md` immediately so it never drifts.
