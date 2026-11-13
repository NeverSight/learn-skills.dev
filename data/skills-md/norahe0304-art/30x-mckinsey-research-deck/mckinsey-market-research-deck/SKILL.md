---
name: mckinsey-market-research-deck
description: >
  End-to-end playbook for producing a top-tier, McKinsey-style market-research deck
  (HTML page-turning presentation + print-ready PDF) for a brand or product category.
  Covers the research methodology (TAM/SAM/SOM bottom-up, Good/Better/Best framework,
  competitor profiling, customer pain points, unit economics, business case), the
  locked McKinsey visual design system, a reusable Python deck engine, an adversarial
  verify workflow for decision-grade numbers, an image-generation handoff, and a
  full QC checklist. Use when the user asks to "do market research", build a
  "market research deck / report", a "McKinsey-style deck / presentation", a
  "GBB / Good-Better-Best analysis", "market sizing", "competitive landscape deck",
  "投资/商业案例 deck", or to turn research into a polished slide deck or PDF.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - Agent
  - Workflow
---

# McKinsey-Style Market-Research Deck

Build a research-backed, visually elite, page-turning deck (HTML reviewed on screen → PDF for sharing).
This skill is the distilled, reusable playbook. **Read the four reference files as you reach each phase** —
do not try to hold all of it in head at once.

- `references/methodology.md` — how to do the research and what each section must contain
- `references/design-system.md` — the locked visual contract (tokens, page types, layout laws)
- `../mckinsey-deck/assets/deck_engine.py` — **the canonical engine** (owned by the `mckinsey-deck`
  style skill; this skill consumes it — never fork a local copy, that's how drift starts)
- `references/qc-checklist.md` — the self-verify pass before delivery
- `references/image-handoff.md` — the template that hands product/cover images to an image generator

## The 7-page spine (always)

0. **The Answer** — one `answer_slide()` right after the cover: the governing thought (the full
   recommendation in one sentence) + 3–4 pillar conclusions with key numbers. Pyramid Principle:
   the answer comes first; the rest of the deck is its proof. Drafted in Phase 1.5, finalized last.
1. **Market Overview** — size, growth, channel, the structural shift
2. **Brand Landscape** — Good/Better/Best ladder + brand-by-brand profiles
3. **Product Categories** — per-subcategory competitor price ladder + pain points + the brand's lineup
4. **Customer Pain Points** — sourced failure modes, each one a selling-point opening
5. **Opportunities** — pain points → product direction
6. **The Solution** — positioning, pricing/packaging, the line plan, **and the decision pages** (bottom-up market sizing, economics, business case) + the thesis

End with a **full source register** (every URL, numbered).

## Workflow (run in order)

### Phase 0 — Scope + Day-1 hypothesis
Get: the brand, the parent retailer/company, the category, the geography, the SKU-count target,
and the strategic question (usually "what line should we build and why"). Confirm the deck is the
deliverable (pure market research), not a precursor needing first-party data.
Then **write the Day-1 hypothesis** — a one-paragraph draft of the answer ("we believe X because
A/B/C") *before* researching. It steers the research (80/20: go deep only on the branches that
confirm or kill it) and it is there to be **falsified, not defended** — revise it whenever the
evidence disagrees, and say so in the deck.

### Phase 1 — Research → one data file
Do the research per `references/methodology.md`. **Land everything in a single `<brand>-data.json`**
(the deck is data-driven from it). Every number must carry a `sourceUrl`. Schema in methodology.md.
Use WebSearch/WebFetch; capture competitor prices/plan tiers live with the capture date (shelf price
for goods, plan/ACV for software, cost-to-adopt for OSS/service).
**Source bar** (full rules in methodology.md § The source bar): prices from the vendor's own page
only; market sizes from named research, never an SEO aggregator alone; pains quoted verbatim from a
named venue; load-bearing inputs need 2 sources or an explicit "judgment call" label; floor of
≥1.5 unique URLs per content page with ≥50% primary/named-research — and zero padding URLs.

### Phase 1.5 — Ghost deck (dot-dash storyline)
Before rendering a single page, write the **headline-only outline**: every page as one action-title
sentence, in order, plus a one-line sketch of its exhibit. Then run the **horizontal-logic test**:
read the headlines top to bottom — they must read as one persuasive essay (SCQA arc: situation →
complication → question → answer). If a headline doesn't advance the argument, the page gets cut or
merged *now*, before any layout work is spent. Draft the §0 governing thought + pillars here too.

### Phase 2 — Generate the deck
Copy the canonical engine `~/.claude/skills/mckinsey-deck/assets/deck_engine.py` into the project
(single source of truth — engine fixes go back to that file, never to a project-local fork).
Point it at `<brand>-data.json`, set `BRAND`,
compose the 6-section `build()` (the engine ships the renderers + an example build). Render:
```bash
python3 deck_engine.py                       # writes <Brand>-Deck.html
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-pdf-header-footer --print-to-pdf="<Brand>-Deck.pdf" "<Brand>-Deck.html"
```
After EVERY build, assert structure: `div diff` must be 0 (an unclosed div breaks pagination).
```bash
python3 -c "h=open('<Brand>-Deck.html').read();print('div diff:',h.count('<div')-h.count('</div>'))"
```

### Phase 3 — Decision pages (adversarial verify)
The three pages that turn "opportunity scan" into "decision deck": **bottom-up market sizing
(TAM/SAM/SOM)**, **economics** (validate the value/margin claim with the buildup that fits the
category — landed COGS for goods, CAC/payback for SaaS, adoption→conversion for OSS), **business case**
(investment, 3 scenarios, payback). The questions are universal; the arithmetic forks by archetype —
see methodology.md (§ Decision pages) for each pattern, and set `exhibit.boldKeys` to mark the answer
rows. Generate + verify them with a Workflow pipeline — one analyst agent per page, then an adversarial
verifier that re-derives every number. Persist each verified page as `_decision_<id>.json`.

### Phase 4 — Images
List what's missing (cover hero + any product cutouts + optional dividers). Write the handoff with
`references/image-handoff.md`, hand it to the image generator, then wire the returned PNGs into the engine.

### Phase 5 — QC (mandatory, self-run)
Run `references/qc-checklist.md` end to end: render every page, eyeball for overlap / mid-word
truncation / >30% whitespace / unblended images, and programmatically verify the source register
count. Fix defects, re-render, re-check. Only then present.

## Hard design laws (baked in — never violate)

These are user-confirmed preferences; treat as non-negotiable defaults:
- **No eyebrow/kicker labels.** No small letter-spaced ALL-CAPS tags above titles or on the cover.
  The action-title headline carries the meaning.
- **Cover is ultra-minimal:** title + one italic subtitle, on the navy hero image. No KPI band,
  no method/evidence block, no "Prepared <date>".
- **Action-title headlines:** the headline is a full-sentence conclusion, not a topic label.
- **Charts ride beside their analysis.** Embed the donut/bar/heatmap in a content page's right rail
  (`essay_slide(side=...)`); never put a chart alone on a standalone page.
- **≥4 charts per deck, each centered-titled and load-bearing.** A deck has at least four charts
  (donut / bar / heatmap mix) that each carry a real finding; chart titles are always centered.
- **Notes pinned to a uniform bottom position** (`margin-top:auto`), same on every page.
- **Nothing overlaps the footer line.** `.pad` reserves bottom clearance.
- **Fill by composition, not by stretching — <30% whitespace.** Sparse prose spreads (`space-evenly`);
  sparse tables keep their uniform row height (header 34px / rows 52px, deck-wide) and take an
  `extra=` stat strip or more researched rows. Never balloon an element to hide thin content.
- **No mid-word truncation.** Use the engine's `clipw()` (word boundary + "…"), never raw `[:n]`.
- **Images:** clean cutout on pure white, no shadow, `mix-blend-mode:multiply` to blend; every image
  gets an italic caption. Cover/divider images are the only ones on navy.
- **Flat only:** no drop shadows, no bevels (navy cover/divider excepted).
- **Self-verify by rendering the PDF**, not by trusting the browser tab (an already-open tab won't
  reload — tell the user to hard-refresh with Cmd+Shift+R).

## Quality bar
Match AND exceed a reference McKinsey report on both content density and visual polish. Prose pages
use "bold theme + flowing paragraph", not terse bullets. Be honest about assumptions — flag the
load-bearing judgment calls rather than hiding them; that honesty is what reads as senior.

Two final gates before delivery:
- **Elevator test** — the §0 governing thought + thesis page must sell the recommendation in 30
  seconds, standalone. If it needs the rest of the deck to make sense, it isn't the answer yet.
- **Horizontal logic** — re-run the headline read-through on the *finished* deck (QC §C); page
  edits during build often break the essay.
