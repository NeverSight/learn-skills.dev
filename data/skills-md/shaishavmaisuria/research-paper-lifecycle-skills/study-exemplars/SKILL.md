---
name: study-exemplars
description: Studies exemplar papers from a target venue and produces an original style-and-structure brief — fetches best-paper awardees and top-cited papers on demand (DBLP, Semantic Scholar, Unpaywall, arXiv, open-access ACM DL) and analyzes section architecture, contribution framing, evaluation patterns, and figure/table conventions. Use when the user wants to study best papers or award-winning papers at a venue, find the most-cited papers and how they are structured, learn how successful papers at a conference are written ("what do winning SIGSPATIAL papers look like", "analyze NeurIPS best papers before I draft"), or model a draft on a venue's strongest work. Copyright-safe by design - papers are fetched from legal open-access sources and processed transiently, never bundled, stored, or committed; the output is metadata plus original analysis. Trigger words - exemplar, best paper, award-winning, most cited, top cited, model paper, venue style, paper structure.
---

# Study Exemplars

Turns a target venue's strongest papers — best-paper awardees and top-cited
work — into an **original style-and-structure brief** the user can write
against: how winning papers at this venue architect their sections, frame
contributions, design evaluations, and use figures and tables. Papers are
fetched on demand from legal open-access sources and processed transiently.
The deliverable contains metadata and original analysis only — never paper
text. Sits between `select-venue`/`parse-cfp` (choosing the target) and the
writing skills (`write-abstract`, `draft-related-work`, `tailor-to-venue`).

## When to use

- "What do best papers at <venue> look like?" / "analyze the award winners"
- "Show me the most-cited <venue> papers and how they're structured"
- "I'm submitting to <venue> for the first time — how do successful papers
  there frame contributions / run evaluations / lay out sections?"
- Before drafting: build a venue style brief that other writing skills consume
- NOT for finding papers on a topic (`find-papers`) or reviewing the
  literature for content (`literature-review`) — this skill studies *form*

## Inputs

- A target venue, ideally with a profile `venues/conferences/<id>.yml`
  (schema: `venues/schema.yml`); otherwise resolve aliases per
  [references/finding-exemplars.md](references/finding-exemplars.md)
- Optional: year window (default: the last 3–4 *completed* proceedings
  years), exemplar count (default 5–8), the user's paper type (research /
  short / demo) so analysis targets the right track
- `CONTACT_EMAIL` env var — required by every script (polite-pool identity);
  scripts prompt interactively if unset, or exit nonzero with instructions
- Optional: `S2_API_KEY` env var for reliable Semantic Scholar access

## Process

### 1. Resolve the venue and lock the target

- Read the venue profile if one exists. Take `aliases.s2_venue` and
  `aliases.dblp_key` from its `aliases:` block; note the track, page limit,
  and template the user will write for.
- **Re-verify critical facts against the live `cfp_url` before the user
  relies on them** — the brief will state format conventions (page budget,
  template, required sections), and profiles go stale. If the profile's
  `verified.date` is older than the current CFP cycle, fetch the CFP and
  reconcile first.
- No profile? Resolve aliases via the `find-papers` skill's venue-aliases
  table or live DBLP venue search before any query — a wrong S2 venue
  string silently returns zero papers.

### 2. Build the exemplar set (two complementary lists)

**Best-paper awardees** (the venue's own quality signal):

- Find award pages live — the venue/SIG awards page, year-site news posts,
  or the jeffhuang.com aggregator. Source map and verification protocol:
  [references/finding-exemplars.md](references/finding-exemplars.md).
- Awards exist in **no API**. Never assert a winner from memory. Every
  award claim needs (a) a source URL fetched this session AND (b) a DBLP
  metadata match:

  ```bash
  python3 scripts/lookup_exemplar.py --title "Exact Title From The Award Page"
  ```

  If either is missing, drop the paper or label it explicitly unverified.

**Top-cited** (the community's quality signal):

```bash
# S2 venue string from the profile aliases — NOT the acronym
python3 scripts/rank_top_cited.py --venue "SIGSPATIAL/GIS" --year 2020-2023 --top 10
# or read the alias straight from a profile:
python3 scripts/rank_top_cited.py \
    --venue-profile venues/conferences/sigspatial-2026.yml --year 2020-2023 --top 10
```

One polite request ranks the whole venue-year window by citation count.
Rank a window ending 2–3 years back — current-year counts are near zero
and meaningless. More selection caveats (survey inflation, influential
citations, DBLP cross-checks): [references/finding-exemplars.md](references/finding-exemplars.md).

Target 5–8 papers total: 3–4 verified awardees + 3–4 top-cited, spread
across years, matching the user's track (don't study 10-page research
papers to write a 4-page demo). Confirm the final set with the user before
fetching.

### 3. Fetch each exemplar on demand — transiently

- One paper at a time, never in bulk. Resolve the OA copy with the
  `fetch-paper` skill (`scripts/resolve_oa.py <DOI> --json` there), or use
  the OA hints both scripts here print (S2 `openAccessPdf`, arXiv HTML,
  `dl.acm.org/doi/pdf/<doi>` for post-2026 open-access ACM papers — that
  host blocks scripted downloads, so open it in a browser).
- Read the paper, extract observations, discard the file. Never write the
  PDF, its text, or its abstract into the repo or any committed file.
- No legal OA copy (Unpaywall `is_oa: false`, no arXiv version)? **Skip the
  paper and say so** — list it in the brief as "not analyzed (no open
  copy)". Never bypass a paywall or use shadow libraries.

### 4. Analyze each paper against the rubric

Work through [references/analysis-rubric.md](references/analysis-rubric.md)
— the dimensions are: identity card, title/abstract patterns, section
architecture, contribution framing, method presentation, evaluation
patterns, figure/table conventions, related-work positioning,
reproducibility apparatus, writing micro-style. Record **facts and original
observations** (section names, counts, orderings, framing moves), not
prose. Quotes: at most one short attributed fragment (<25 words) per paper,
only when the exact wording is the observation.

As you record each paper's counts, also log the **measurable** ones (pages,
references, figures, tables, abstract words, teaser/badge booleans, section
skeleton) into a small per-paper JSON — these feed step 6.

### 5. Synthesize the style-and-structure brief

- Cross-paper synthesis first (what ≥ half the exemplars do = the venue
  convention; splits = noted as variants), then one exemplar card per
  paper. Templates for both are at the end of the rubric.
- Reconcile with the venue profile: if exemplars contradict the current CFP
  (e.g. older 8-page exemplars vs. a 10-page limit today), the **live CFP
  wins** — flag the delta so the user doesn't imitate an outdated rule.
- Cite every exemplar by verified metadata (title, authors, year, DOI). If
  any entry will land in the user's bibliography, route it through
  `verify-citations`.

### 6. Cache a measured exemplar bundle (data hygiene)

The session's measurable facts are the on-family distribution downstream
skills score drafts against. When a downstream skill's *live* exemplar fetch
is skipped or rate-limited, it falls back to the venue/family profile's
`exemplar_distribution:` block — which for most venues is **hand-estimated**,
never measured. Cache yours so that fallback rests on real exemplars:

```bash
python3 scripts/build_exemplar_bundle.py measurements.json --out block.yml
```

This aggregates your per-paper measurements (from step 4) into a schema-
conforming block: density **bands** (never fabricated single points), rates,
and the modal skeleton, each stamped with `measured: true`, `n`, `recency`,
and `as_of: <date>`. Paste it into the relevant profile under review
(`venues/conferences/<id>.yml`, or `venues/families/<family>.yml` when the
set spans the family), **replacing any hand-estimated block**. Bands from
fewer than 3 papers are left `null` and the block is marked
`measured-low-confidence` rather than overclaiming. Full rules and the input
schema: [references/analysis-rubric.md](references/analysis-rubric.md) §14.

Because the block carries `measured` + `as_of`, every score a consumer
derives from it is labelled **cache-vs-live** (`live` / `family-prior
(measured, as_of <date>)` / `family-prior (hand-estimated)` / `none`) — a
cache-derived score never reads as if measured live.

## Output

A markdown brief (default `exemplar-brief-<venue>.md` in the working
directory, or wherever the user asks) containing:

1. **Exemplar roster** — the 5–8 papers with metadata, selection reason
   (award + source URL / citation rank + count), and OA link used
2. **Venue conventions** — the cross-paper synthesis across all rubric
   dimensions, each claim tagged with which exemplars exhibit it
3. **Exemplar cards** — one compact per-paper analysis each
4. **Deltas & caveats** — exemplar habits that conflict with the live CFP,
   papers skipped for lack of OA copies, unverified award claims dropped
5. **Provenance** — scripts run, award-page URLs, date, and the note that
   citation counts are a snapshot (Semantic Scholar, ODC-BY, attributed)

Plus, when measurements were taken, a **cached `exemplar_distribution:`
block** (step 6) pasted into the relevant venue/family profile — the measured
fallback downstream skills use when a live fetch fails, stamped `measured`,
`n`, and `as_of`.

The brief contains **only** metadata and original analysis — no abstracts,
no reproduced passages, no extracted figures.

## References

- [references/analysis-rubric.md](references/analysis-rubric.md) — the
  analysis dimensions, what to record per paper, copyright line for
  outputs, synthesis + exemplar-card templates, and §14 caching the measured
  exemplar bundle (input schema + provenance labelling)
- [references/finding-exemplars.md](references/finding-exemplars.md) —
  award sources and the verification protocol, top-cited selection
  methodology and caveats, OA resolution order, alias gotchas
- `scripts/build_exemplar_bundle.py` — aggregates per-paper measurements into
  a provenance-stamped `exemplar_distribution:` block (offline, stdlib;
  invents nothing, suppresses thin bands)

## Guardrails

- **Never bundle paper content.** No paper text, abstracts, figures, or
  PDFs in the repo, the brief, or any committed file — fetch on demand,
  process transiently, keep metadata (DOI, title, BibTeX fields) and
  original analysis only. Quotes ≤25 words, attributed, at most one per paper.
- **Never fabricate exemplars.** Every award claim needs a live source URL
  plus a DBLP match; every citation count comes from a script run this
  session; anything entering a bibliography goes through `verify-citations`.
- Legal OA sources only; single polite fetches (the scripts enforce ≤1
  req/s per host, contact-email User-Agent, 429 backoff, caching under
  `.cache/study-exemplars/`); never bulk-harvest a proceedings.
- Venue profiles are a starting point, never ground truth — re-verify
  page limits, templates, and required sections against the live `cfp_url`
  before the user relies on them.
- **Cache measurements, not text, and never overclaim them.** The cached
  `exemplar_distribution:` block is counts/bands/section-names only (safe to
  commit); never put paper text in it. It is a *fallback*, not ground truth —
  a live corpus for the target venue still wins. Emit bands only from ≥3
  papers (thinner → `null` / `measured-low-confidence`), never a fabricated
  single point, and label every cache-derived score `cache-vs-live` so it
  never reads as measured live this session.
- Studying exemplars means learning *conventions*, not copying — never
  reproduce a specific paper's text, structure verbatim, or ideas without
  attribution. Never submit anything to any system on the user's behalf.
