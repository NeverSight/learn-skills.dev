---
name: antislop-master
description: "The master AI-slop taxonomy: a severity-tiered catalog of ~180 indicators across visual, layout, content, UX, and code. Use to audit any design — web, SaaS, dashboard, mobile, Flutter — and to find slop by evidence, not by vibes. The canonical audit source for anti-ai-slop."
allowed-tools: Read Write Edit Glob Grep
---
# antislop-master

> The master AI-slop taxonomy for **anti-ai-slop**.
>
> Use this when you need a comprehensive, evidence-based audit of any interface — landing page, SaaS app, dashboard, mobile, Flutter, or design system — and you want to catch AI slop *by pattern and purpose*, not by a gut feeling that "this looks AI".
>
> This is a catalog, not a style guide. It names indicators and a severity tier. It never decides the design — your `DESIGN.md` does.

---

## The core idea

AI slop is **not** any single technique. Gradient alone is not slop. A card grid is not slop. Inter is not slop.

**Slop is the unmarked combination** of generic defaults that repeats because no one chose them:

> **No hierarchy + no specificity + no restraint + no opinion.**

An indicator is slop only when it appears **without a product reason**. Two tests separate a default from a choice:

1. **Purpose test** — could you write one honest sentence explaining why *this* technique serves *this* product?
2. **Convergence test** — does the same technique appear across unrelated screens/sections for no reason?

If either answer is weak, flag it. This is why the catalog is tiered by severity instead of being a ban list.

---

## Severity tiers

| Tier | Name | Meaning | Action |
|------|------|---------|--------|
| **P0** | Instant tell | The single strongest "AI made this" signal | Fix before anything else |
| **P1** | Strong tell | Individually loud, usually wrong | Fix in this pass |
| **P2** | Suspicious pattern | Common AI default, may be earned | Justify or change |
| **P3** | Context dependent | A pattern that is only slop in the wrong context | Judge against product |
| **P4** | Quality / UX slop | Shipping incomplete experience | Ship-ready means no P4 |
| **P5** | Authenticity slop | Fake data, claims, or evidence | Never ship fake |
| **P6** | Code slop | Sloppy implementation of the design | Clean before merge |

**Scoring:** Severity is not a checklist count. Weight **P0 > P1 > P4 > P5 > P6 > P2 > P3**. A single P0 is a FAIL for any screen, even with zero others.

Use one of three audit levels:
- **Quick** — scan P0 + P1 only (2 min / screen).
- **Full** — scan P0–P3 + P6 (the shipped-size review).
- **Deep** — everything, including P4/P5 and the code-level pass.

---

## A. Color & Light

| # | Tier | Indicator |
|---|------|-----------|
| A-1 | P0 | The blue→purple→pink diagonal gradient, especially as a hero backdrop (the canonical tell) |
| A-2 | P1 | Gradient that runs right-to-left or diagonal with no brand logic to the angle |
| A-3 | P1 | Text set as a gradient fill (reads like a sticker, cheapens the headline) |
| A-4 | P2 | Default Tailwind slate/indigo palette with no custom tokens |
| A-5 | P2 | Cream / off-white "AI aesthetic" page background used as a default |
| A-6 | P2 | Neon glow where nothing emits light (cards, buttons, badges, text) |
| A-7 | P2 | Purple-and-black "future tech" scheme chosen for mood, not brand |
| A-8 | P2 | Pastel wash (mint/lavender/pale blue) as a substitute for a palette |
| A-9 | P3 | Glassmorphism / heavy blur on nav + card + modal + sidebar at once |
| A-10 | P3 | Excessive transparency (overlay-on-overlay) that fights readability |
| A-11 | P3 | Aurora / mesh gradient blobs as a hero filler |
| A-12 | P3 | Decorative dot-grid or blueprint grid background with no identity tie |
| A-13 | P3 | Gradient border on cards/tables used as the default "edge" treatment |
| A-14 | P3 | 1px gray border on nearly every component (so nothing is elevated) |
| A-15 | P2 | The same 2–3 color family used everywhere with no single accent role |

**Passing standard:** one deliberate accent role, a real palette that comes from brand, and every gradient/glow/blur tied to a reason.

---

## B. Typography

| # | Tier | Indicator |
|---|------|-----------|
| B-1 | P1 | Inter (or the same default grotesque) with no typeface decision documented |
| B-2 | P1 | The 64–80px hero headline on every page regardless of content length |
| B-3 | P2 | Monospace used "because it looks technical" (Geist Mono & friends) |
| B-4 | P2 | Uppercase eyebrow label above every section title (stamped template) |
| B-5 | P2 | Gradient headline → duplicate of A-3 |
| B-6 | P3 | Extreme letter-spacing on body text (reads airy, not intentional) |
| B-7 | P3 | One weight hierarchy everywhere — every heading the same size/weight |
| B-8 | P3 | All-caps navy micro-labels that repeat identically across sections |
| B-9 | P3 | Body text max-width + center that ignores real line-length differences |

**Passing standard:** type scale that responds to content, a chosen typeface with a reason, and no "technical" styling without a technical use.

---

## C. Layout & Composition

| # | Tier | Indicator |
|---|------|-----------|
| C-1 | P0 | Centered hero → subtitle → two CTAs → three-card grid (the SaaS formula) |
| C-2 | P1 | The exact same section rhythm repeated for every section (title/copy/CTA) |
| C-3 | P1 | Perfect symmetry with no asymmetry to create a focal point |
| C-4 | P2 | Bento grid because it is trendy, not because content needs it |
| C-5 | P2 | Card grid as the universal answer to every content type |
| C-6 | P2 | Everything centered — hero, CTAs, cards, even long-form text |
| C-7 | P2 | All cards identical width/structure regardless of content weight |
| C-8 | P3 | A CTA section dumped at the end of every page by default |
| C-9 | P3 | FAQ present only because landing templates include one |
| C-10 | P3 | Metric cards with the same 3-up pattern regardless of data |
| C-11 | P3 | Wide whitespace that is leftover, not structural (no grid intent) |
| C-12 | P3 | Repeated template sections that ignore actual content needs |

**Passing standard:** composition follows real content hierarchy; one clear focal point per screen; asymmetry earned, not avoided.

---

## D. Components

| # | Tier | Indicator |
|---|------|-----------|
| D-1 | P1 | `rounded-2xl` on everything with no radius system |
| D-2 | P1 | Every interactive element is a pill (no hierarchy of shape) |
| D-3 | P2 | Icon floated inside a rounded square on every card, even where an icon adds nothing |
| D-4 | P2 | Left-border accent card / colored left stripe as a filler pattern |
| D-5 | P2 | Gradient "pill" button as the primary CTA |
| D-6 | P2 | `hover:scale-105` or a lift on every card, button, and badge |
| D-7 | P2 | Glassmorphic / floating navbar with no clear scroll behavior |
| D-8 | P3 | Generic tab set that duplicates what is already visible |
| D-9 | P3 | Status pills / badges (PASS, NEW, PRO) with no function |
| D-10 | P3 | A mega-footer full of dead links and fake link groups |
| D-11 | P3 | Identical card component used for fundamentally different content |

**Passing standard:** shape and radius carry hierarchy; badges and tabs do work; nav and footer are functional.

---

## E. Content / Copy

| # | Tier | Indicator |
|---|------|-----------|
| E-1 | P1 | The hype-verb stack: Supercharge, Transform, Unlock, Elevate, Unleash |
| E-2 | P1 | "Seamlessly", "Revolutionary", "Next-generation" with nothing to back it |
| E-3 | P1 | "The future of <noun>" / "Built for modern teams" / "Trusted by thousands" |
| E-4 | P2 | "Powerful", "Innovative", "Robust" as the only substance |
| E-5 | P2 | Fake statistics, testimonials, or customer logos |
| E-6 | P2 | Generic feature descriptions that could describe any product |
| E-7 | P2 | The em dash and the em-dash-feeling throat-clear opener ("So...") |
| E-8 | P3 | A headline that promises but never names the actual thing |

**Passing standard:** every claim is specific and true; numbers have a source; copy names the real product.

---

## F. Interaction & Motion

| # | Tier | Indicator |
|---|------|-----------|
| F-1 | P2 | Fade-in on every section (the universal scroll micro-animation) |
| F-2 | P2 | Scroll-reveal + parallax with no hierarchy (everything moves equally) |
| F-3 | P3 | Floating/looping idle animation on a hero blob |
| F-4 | P3 | Pulse glow on a CTA to "draw the eye" |
| F-5 | P3 | Micro-animation on every hover, so nothing feels important |
| F-6 | P3 | Motion with no purpose or easing logic (all identical) |

**Passing standard:** motion has a UX reason; only the focal element animates; easing and timing are intentional.

---

## G. Product / UX Slop (P4 — ship-ready means none)

| # | Tier | Indicator |
|---|------|-----------|
| G-1 | P4 | A button or link that does nothing (decorative interactivity) |
| G-2 | P4 | Dead links / nav items that point nowhere |
| G-3 | P4 | No empty state for a list/table/canvas |
| G-4 | P4 | No loading / skeleton state (content just "appears") |
| G-5 | P4 | No error state, no recovery, and no way to retry a failed call |
| G-6 | P4 | Form with no validation, no inline error, and no success confirmation |
| G-7 | P4 | No offline / disconnected handling for an app that needs data |
| G-8 | P4 | No edge-case design (empty search, zero results, delete confirmation) |
| G-9 | P4 | Keyboard focus state missing or invisible |
| G-10 | P4 | Keyboard navigation doesn't reach every interactive element |
| G-11 | P4 | The UI looks done but the underlying function is unfinished |

**Passing standard:** every state is designed, every interaction responds, and function is ahead of polish.

---

## H. Authenticity (P5 — never ship)

| # | Tier | Indicator |
|---|------|-----------|
| H-1 | P5 | Fabricated metrics, market-sizing, or ROI numbers with no source |
| H-2 | P5 | Fake testimonials with invented names / AI avatars |
| H-3 | P5 | Fake customer logos (named brands you don't have) |
| H-4 | P5 | Compliance, security, or performance claims you can't back up |
| H-5 | P5 | Vague evidence ("99% of users..." with no study), as a rule not an exception |

**Passing standard:** empty is better than deceptive. Everything factual is sourced.

---

## I. Design-System Consistency (P2/P3)

| # | Tier | Indicator |
|---|------|-----------|
| I-1 | P2 | Radius, spacing, and color reuse across screens with no token definition |
| I-2 | P2 | Spacing rhythm that is ad-hoc (8px, then 13px, then 26px) |
| I-3 | P2 | The same visual treatment on the entire page (nothing is special) |
| I-4 | P3 | Repeating components that contradict the tokens in `DESIGN.md` |
| I-5 | P3 | Light/dark themes where one is visibly unfinished |

**Passing standard:** tokens are real and used; the page has hierarchy, not uniformity.

---

## J. Code / Implementation Slop (P6)

| # | Tier | Indicator |
|---|------|-----------|
| J-1 | P6 | Classes from a generator that fight each other (e.g. `px-4 md:px-6 lg:px-8` repeated inline with no system) |
| J-2 | P6 | A one-off, copy-pasted component instead of a shared one |
| J-3 | P6 | Magic numbers for colors/spacing instead of tokens |
| J-4 | P6 | The whole page is a single flattened markup block with no componentization |
| J-5 | P6 | Accessibility ignored in markup (no labels, no `aria`, no semantic elements) |
| J-6 | P6 | External script that patches styles at runtime instead of fixing the source |
| J-7 | P6 | AI-slop comments (`// ======`, `// Step 1`, `// Main logic`, decorative emoji) |

**Passing standard:** the implementation matches the design intent, is componentized, and is accessible in markup.

---

## K. Platform-specific

### Mobile
| # | Tier | Indicator |
|---|------|-----------|
| K-1 | P1 | Horizontal overflow or clipped content on the narrowest real device |
| K-2 | P2 | Desktop grid that just shrinks instead of reflowing |
| K-3 | P2 | Tap targets smaller than ~44×44px |
| K-4 | P3 | Hover-only interactions with no touch equivalent |
| K-5 | P3 | Fixed bars that cover content |

### Flutter / native
| # | Tier | Indicator |
|---|------|-----------|
| K-6 | P2 | Same web-framework look copied straight into native without platform consideration |
| K-7 | P2 | Material/Cupertino widgets forced into a web-like layout |
| K-8 | P3 | The web "centered hero + cards" formula on a mobile screen |

---

## Audit protocol

Run the master at the level you need, then report:

1. **Choose level** — Quick / Full / Deep.
2. **Scan every screen** against the catalog. Note only the indicators present **and** unearned.
3. **Apply the two tests** (purpose, convergence) — if weak, it stays.
4. **Weight severity** — P0/P1/P4/P5 first.
5. **Output** a numbered findings list, each citing the code (e.g. `C-1`) and one honest reason.

**Findings format:**

```
[N] P0 — C-1: SaaS formula hero. No product reason for the centered-hero → 2 CTAs → 3 cards stack.
    Fix: rebuild hero around the actual primary action; drop the generic two-CTA split.
```

The agent **does not change anything until the user approves specific findings**. Unapproved findings stay untouched.

---

## Relationship to the other skills

- `antislop` — the always-on core filter (rules, purpose test, delivery gate).
- `antislop-master` — this catalog: the *where to look* list and severity tiers.
- The domain skills (`-ui`, `-layout`, `-dashboard`, `-forms`, `-motion`, `-nav`, `-authenticity`, `-designsystem`, `-imagery`, `-mobile`, `-copywriting`, `-human`, `-layoutmobile`, `-code`) — a deeper dive into one area, each mapping back to these codes.

The core prevents slop but cannot invent direction. `DESIGN.md` (yours) is where direction comes from.
