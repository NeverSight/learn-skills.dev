---
name: travel-guide
description: >-
  Create personalized, source-grounded travel dossiers from a destination, dates,
  duration, travelers, and constraints. Ask only the questions that change the
  plan, use explicitly permitted personal context without exposing it, research
  current logistics, and produce a cited, visually coherent PDF or responsive
  companion web page. Use when someone wants an individualized itinerary, trip
  brief, travel field guide, or shareable travel website. Do not use for real-time
  booking, ticket purchasing, visa or legal advice, or generic destination
  summaries without a specific traveler and trip.
license: MIT
compatibility: >-
  Requires an Agent Skills-compatible host, access to current web sources for
  live travel facts, and a print-capable browser or document renderer for PDF
  output. Bundled Python scripts require Python 3.8+ and only the standard
  library.
metadata:
  category: travel
  tags: travel, itinerary, trip-planning, dossier, pdf, web, personalization
---

# Travel Guide

Create a commissioned travel dossier, not a generic list of attractions. The
finished guide should answer: **why this place, for these travelers, at this
moment?** It should leave room for discovery while making the trip feel
considered.

## When to use

Use this skill when the traveler wants one or more of the following:

- an individualized itinerary or trip brief;
- a beautifully designed travel PDF or printable field guide;
- recommendations shaped by permitted preferences, constraints, or companions;
- a shareable, responsive web page for travel companions;
- a private and sanitized version of the same trip plan.

## When not to use

- For booking, purchasing tickets, changing reservations, or handling payment.
- For visa, immigration, medical, safety, or legal decisions that require an
  authoritative professional or government source.
- For a generic destination summary when there is no concrete traveler or trip.
- For extracting text from an existing document. Route that to `anydoc`; it reads
  documents but does not author or validate them.

## Progressive routing

Read only the references needed for the request:

| Need | Read |
|---|---|
| Personal context, consent, pointed questions, or group trade-offs | [references/intake-and-personalization.md](references/intake-and-personalization.md) |
| Current places, hours, prices, reservations, transit, or source quality | [references/research-and-evidence.md](references/research-and-evidence.md) |
| Trip thesis, anchor selection, day structure, or editorial voice | [references/editorial-structure.md](references/editorial-structure.md) |
| Private/shareable editions or redaction | [references/privacy-and-sharing.md](references/privacy-and-sharing.md) |
| HTML, PDF, print CSS, rendering, or visual QA | [references/pdf-rendering.md](references/pdf-rendering.md) |

Use [templates/trip-brief.json](templates/trip-brief.json) as the structured
source of truth. Use [templates/dossier-outline.md](templates/dossier-outline.md)
when drafting content before entering JSON.

## Workflow

Match the process to the request. A narrow question - one neighborhood, one
restaurant, one transfer, one practical fact - can be answered directly with
sources in a short reply. Run the full dossier pipeline only when the traveler
wants a guide, PDF, companion page, or a multi-day plan. The dossier format is
a deliverable choice, not an automatic output for every travel question.

### 1. Establish the trip contract

Collect, or confirm:

- destination or route;
- arrival and departure dates, or at least the intended season;
- duration and approximate pace;
- who is traveling and any real differences in needs;
- budget range and currency, if relevant;
- mobility, dietary, sensory, language, or booking constraints;
- desired output: private PDF, shareable PDF, companion web page, or all three;
- intended audience: the traveler, the travel party, or wider sharing. The
  working model is private by default; ask who the output is for when it is
  not clear.

If a missing answer would change the recommendations, ask a pointed question.
Do not run a long questionnaire. Read the intake reference for the question
budget and personalization boundary.

### 2. Handle personal context explicitly

If the host can retrieve user preferences or history, use only context that is
relevant to this trip and permitted for this purpose. Internally classify each
personal signal as `known`, `relevant memory`, `hypothesis`, `ask first`, or
`do not use`. Never copy a raw private note into the guide. When personalization
would be surprising, explain the relevant basis briefly or ask permission.

### 3. Research current facts

Research only what the guide needs. Prefer official venue, operator, transit,
government, tourism-board, and booking sources. Record URLs and retrieval dates
in the source ledger. Separate:

- verified current facts;
- editorial interpretation about fit;
- estimates and assumptions;
- facts that remain unknown.

Do not present a search snippet, stale memory, or unsourced price as current
truth. Read the research reference before making logistics or cost claims.

### 4. Build the editorial model

Write a one- or two-sentence trip thesis. Select a small set of anchors rather
than ranking everything. Every anchor must state why it fits these travelers,
when it works best, what it costs or requires, and what could make it fail.

Shape each day around:

1. one anchor;
2. one meal, drink, or local texture;
3. one walk, neighborhood, or ordinary-life encounter;
4. one pause or recovery space;
5. one weather, energy, or closure alternative.

Include a short “skip this” section when famous options are poor fits. Read the
editorial reference before drafting the dossier.

### 5. Render the artifacts

Work in a dedicated working folder for this trip: create one explicitly (for
example `$(mktemp -d)` on macOS/Linux, or a named folder under the system
temp directory) and keep the trip model, rendered HTML, sanitized editions,
and PDFs there. Never write outputs into the skill directory or the user's
home directory root. The examples below use `$WORK` for that folder.

Keep content separate from layout. Validate the content model first:

```bash
python3 scripts/validate-trip-brief.py "$WORK/trip-brief.json" --strict --json
```

Render a print-oriented HTML dossier:

```bash
python3 scripts/render-travel-guide.py "$WORK/trip-brief.json" \
  --mode dossier --output "$WORK/travel-dossier.html" --json
```

For a responsive companion page, use the same model:

```bash
python3 scripts/render-travel-guide.py "$WORK/trip-brief.json" \
  --mode companion --output "$WORK/index.html" --json
```

The renderer embeds the bundled CSS and local image assets when possible. Use a
print-capable browser or the repository's `documents` skill to turn the dossier
HTML into a PDF. The PDF is not complete until it has been structurally checked
and visually inspected. Read the PDF reference for the exact gate.

### 6. Produce a shareable edition when requested

Keep the private model as the source of truth. Create a sanitized copy rather
than painting over a finished PDF:

```bash
python3 scripts/sanitize-trip-brief.py "$WORK/trip-brief.json" \
  --profile shareable --output "$WORK/trip-brief-shareable.json" --json
```

Render and validate the sanitized model separately. Do not assume that a
shareable version may expose exact dates, lodging, companions, addresses,
booking identifiers, contact details, or private notes.

## Required dossier sections

Adapt the length to the trip, but preserve the information hierarchy:

1. cover: destination, trip line, duration/route, and image credit;
2. the brief: the reason this trip fits these travelers;
3. anchors: high-confidence experiences with fit and logistics;
4. day architecture: anchors, texture, pauses, and alternatives;
5. make it special: specific gestures that are not generic search results;
6. practical field notes: transit, reservations, etiquette, costs, and caveats;
7. skip this: attractive but poor-fit options, where useful;
8. sources and freshness: links, retrieval dates, and unresolved uncertainty.

The visual default is a dark photographic cover with a route journey line, warm
gold eyebrow, white headline, restrained red accent, generous white content
pages, ghost section numbers, a color-coded day strip right after the brief,
pace and budget meters, compact cards, a unified warm photo grade on anchor
images, readable tables, and a bottom-of-page footer per section: a content-
derived field note (failure mode, plan B, recheck item, or skip reason) when
one exists, a next-section line, and a ghost route mark. Preserve contrast and
selectable text. Do not let decoration hide uncertainty or practical caveats.
The footer is informational, never a schedule: it repeats model content in one
line, it does not invent new plans.

## Exit criteria

Stop when all requested artifacts exist and:

- the trip model passes the bundled validator;
- current claims have source URLs and retrieval dates or are labeled uncertain;
- the PDF has passed structural and visual QA, if requested;
- a companion page has been checked at narrow and wide widths, if requested;
- private and shareable outputs are clearly distinguished;
- the delivery names the source model, renderer, validation result, and known
  limitations.
