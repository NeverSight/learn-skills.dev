---
name: make-slides
description: Builds a conference talk deck (Beamer or Marp markdown) from a paper draft - problem-first narrative, one claim per slide, figures reused straight from the paper's LaTeX source, sized to the real slot (12-20 minute full talk vs 5-minute lightning). Use when the user asks to make slides, build a presentation or talk deck for an accepted paper, turn a paper into a talk, prepare a conference presentation, fit a talk into N minutes, or check and trim an existing deck that is too long or too text-heavy. Inventories the paper's figures by in-text reference count, computes a minutes-and-slides budget per section, drafts the deck, and deterministically lints pacing, overfull slides, missing or unrenderable figures, and generic non-claim titles. Venue profiles give context only; the slot length must come from the venue's presenter instructions or acceptance email.
---

# Make Slides

Turn an accepted (or nearly-done) paper into a conference talk deck —
Beamer `.tex` or Marp markdown — built around a problem-first story, one
claim per slide, the paper's own figures, and a slide count the slot can
actually afford. The deck is the deliverable; the timed word-by-word
script and Q&A drill are separate skills (`write-talk-script`,
`rehearse-qa`).

## When to use

- The paper got accepted and a talk slot is coming: build the deck.
- The user has a slot length ("12 minutes plus 3 Q&A", "5-minute
  lightning") and needs a deck that fits it.
- An existing deck is overlong, text-heavy, or paper-shaped and needs to
  be cut down to a talk.

Related skills: `write-talk-script` (timed speaker script for the deck),
`rehearse-qa` (hostile/curious Q&A drill), `make-poster` (poster +
2-min/5-min pitches), `study-exemplars` (how strong papers at the venue
frame contributions), `verify-citations` (gate for any reference that
appears on a slide).

## Inputs

- The paper's main `.tex` file (preferred — figures are harvested from
  source) or the PDF plus the figure files.
- The slot length and Q&A split, from the venue's **presenter
  instructions or acceptance email**. This is the one fact the skill
  cannot look up: venue profiles do not encode talk slots (they change
  year to year and per track). If the user does not know it, stop and ask
  — see [references/venue-timing.md](references/venue-timing.md).
- Optional: `venues/conferences/<id>.yml` for venue context (name, track,
  live URLs). Re-verify anything taken from a profile against the live
  `cfp_url` / venue site before the user relies on it.
- Output format choice: Beamer (LaTeX toolchain, vector figures reused
  as-is) or Marp (markdown, fast iteration, figures must be PNG/SVG).
  Decision guide: [references/deck-formats.md](references/deck-formats.md).

## Process

### 1. Pin down the slot, then budget the deck

Confirm slot minutes and Q&A minutes with the user (ask; never assert a
slot length from memory or from a venue profile — typical shapes and the
verification checklist are in
[references/venue-timing.md](references/venue-timing.md)). Then run, from
the repo root:

```
python3 skills/make-slides/scripts/slide_budget.py --minutes <slot> --qa <qa> \
    [--format auto|full|lightning] [--venue-profile venues/conferences/<id>.yml] [--json]
```

It prints the content-slide target (~1 slide per speaking minute, hard max
1.25x) and a problem-first section allocation (minutes + slides per
section) in the full-talk shape (12-20 min) or the lightning shape
(<= 7 min). Treat the allocation as the storyboard skeleton.

### 2. Inventory and harvest the paper's figures

```
python3 skills/make-slides/scripts/extract_figures.py path/to/main.tex \
    --copy-to talk/assets [--json]
```

It follows `\input`/`\include`, resolves `\graphicspath`, and ranks every
figure by how often the text references it — the most-referenced figures
are usually the ones the talk is built around. It also counts table
environments: tables almost never survive as slides; redesign each one as
a chart or a single highlighted number. TikZ-only figures (no graphics
file) must be recompiled or screenshot from the paper PDF.

If the deck will be Marp, convert harvested PDFs to PNG/SVG now
(commands in [references/deck-formats.md](references/deck-formats.md));
Marp cannot render PDF images.

### 3. Storyboard: problem first, one claim per slide

Map the paper onto the budget's sections using
[references/narrative-storyboard.md](references/narrative-storyboard.md).
The non-negotiables:

- **Problem-first**: open with why the problem matters, not an outline or
  the paper's section order. The talk is an advertisement for the paper,
  not a compression of it.
- **One claim per slide**: every slide title is a full assertion — the
  sentence to be remembered if the audience reads nothing else ("LRU
  evicts the tiles a burst is about to revisit", not "Background").
  Evidence (a figure, one number) supports the title; bullets are a last
  resort.
- Numbers and claims on slides come from the paper or the user — never
  invent, round up, or extrapolate. Any cited work shown on a slide goes
  through `verify-citations` first.
- Proofs, secondary ablations, and related-work depth move to backup
  slides after the final slide — they cost nothing against the budget.

Write the storyboard as a list (slide title-claim, supporting visual,
~seconds of talk) and confirm it with the user **before** drafting slides.

### 4. Draft the deck

Build the deck from the approved storyboard using the skeletons in
[references/deck-formats.md](references/deck-formats.md):

- **Beamer**: `aspectratio=169`, frame title = the claim, reuse paper PDFs
  via `\includegraphics`, speaker-note stubs in `\note{}`, backup frames
  after `\appendix`.
- **Marp**: `marp: true` front matter, `#`/`##` title = the claim,
  PNG/SVG images only, speaker-note stubs in `<!-- -->` comments, backup
  slides titled `Backup: ...`.

Write the deck and assets under `talk/` next to the paper (or where the
user prefers); never overwrite an existing deck without confirming.

### 5. Lint, fix, re-lint

```
python3 skills/make-slides/scripts/deck_lint.py talk/slides.md|slides.tex \
    --minutes <SPEAKING minutes = slot - Q&A> [--strict] [--json]
```

Deterministic checks: pacing vs the slot, overfull slides (>100 words is
a document, not a slide), bullet overload, generic non-claim titles,
missing image files, Marp-unrenderable PDF images, tiny Beamer fonts.
Fix every RISK and re-run until RISK-free; resolve pacing by cutting or
merging slides, never by planning to talk faster.

### 6. Verify it builds, then hand off

Compile the deck if the toolchain is available (`latexmk -pdf` for
Beamer, `marp` CLI for Marp — commands in
[references/deck-formats.md](references/deck-formats.md)); otherwise say
explicitly that it was not compiled. Deliver the deck, the figure
inventory, and the lint report, and point the user at `write-talk-script`
to time the narration and `rehearse-qa` before the session. Remind them
to re-check slot length, room aspect ratio, and any pre-recording
requirement against the venue's presenter instructions.

## Output

- `talk/slides.md` (Marp) or `talk/slides.tex` (Beamer) — RISK-free under
  `deck_lint.py` for the stated speaking time, with speaker-note stubs
  and backup slides.
- `talk/assets/` — the paper figures the deck uses, harvested by
  `extract_figures.py` (converted for Marp).
- The slide budget and figure inventory as the paper trail for what was
  cut and why.

## Guardrails

- Never invent results, numbers, or comparisons for a slide; every figure
  and number traces to the paper or the user. Pending results get an
  explicit `[RESULT]` placeholder, flagged in the handoff.
- Never fabricate citations on slides; anything cited goes through
  `verify-citations`.
- Never assert slot lengths, room formats, or recording rules from memory
  or from a venue profile — presenter instructions and the acceptance
  email are ground truth; label anything unconfirmed as UNVERIFIED.
- Never bundle or paste another paper's slides or text as a template;
  exemplar study happens transiently via `study-exemplars`.
- Never upload or submit the deck anywhere on the user's behalf.
