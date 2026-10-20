---
name: building-powerpoint-decks
description: Build, edit, audit and present PowerPoint decks with Claude — via COM automation of desktop PowerPoint on Windows, or python-pptx anywhere. Load when creating or editing a .pptx, auditing a deck, preparing to present one, adding animation, video or AI images to slides, or when PowerPoint automation on Windows is failing.
---

# Building PowerPoint decks

Rules, traps and helper scripts for producing decks that render correctly the first time. Detail lives in
[`reference/`](reference/); helper scripts in [`scripts/`](scripts/README.md). Read this file fully, then open
only the reference file the task needs.

## Start here

| Task | Read, in order |
|---|---|
| **New deck** | The [checklist below](#new-deck--the-checklist); detail in [WORKFLOW](reference/WORKFLOW.md#new-deck-in-detail), patterns in [BUILDER](reference/BUILDER.md) |
| **Edit an existing deck** | Snapshot first · `scripts/read_deck.py` before judging ([AUDIT](reference/AUDIT.md)) · find the open deck by name ([COM](reference/COM.md)) · rebuilding a generated deck? `scripts/harvest_edits.py` first |
| **Improve a deck someone already has** | [Restyle or keep the look](#existing-deck-restyle-or-keep-the-look) below |
| **Review / audit a deck** | `scripts/lint_deck.py` first (any OS) · `scripts/fix_deck.py deck.pptx --out fixed.pptx` (or `--in-place`, or `--dry-run`; one is required) for the mechanical fixes · then [AUDIT](reference/AUDIT.md): taste pass → anchor exceptions → contact sheet |
| **Before a talk** | Audit clean first, then [PRESENTING](reference/PRESENTING.md) |
| **Images, video, Remotion, Veo** | [MEDIA](reference/MEDIA.md), then [ANIMATION](reference/ANIMATION.md) if it moves |
| **PowerPoint automation failing (Windows)** | [SETUP](reference/SETUP.md) → Troubleshooting |
| **No Windows (Linux, macOS, CI)** | [AUTOMATION](reference/AUTOMATION.md) → *Building .pptx without PowerPoint* |
| **Company template / brand** | `build_deck.py --inspect brand.potx`, then `--template brand.potx` → [BUILDER](reference/BUILDER.md#building-into-a-company-template); hand-built: [LAYOUT](reference/LAYOUT.md) → *Building from a template* |
| **Corporate / labelled deck** | [LABELS](reference/LABELS.md) before choosing a toolchain |


## Fast path - one or more new decks from briefs (2 calls per deck)

Everything a clean brief needs is on this page; open a reference file only when a check line points at it.

```
1. Write    one spec per deck (JSON; shape: examples/spec/sample-deck.json; fields: build_deck.py --print-schema)
2. Check    python scripts/build_deck.py a.json b.json c.json --check --apply     (one call for every deck)
3. Look     open the all-sheet: line's contact-all.png once (one row per deck); read the slides: lines
4. Done     batch summary all `clean`; else fix every listed item in one edit per spec and repeat 2 for those
```

- `--check --apply` already writes the ready edits and auto-fixes (`--plan` first is optional), builds, lints,
  renders and prints per deck a `slides:` table (pattern, title, findings or `ok`). Without `--out` each deck goes
  beside its spec; with several specs `--out` names a folder. Decks build three at a time; exit = worst deck.
- Patterns: `big_number bullets chart compare cost_table email image image_text kpi kpi_chart matrix metrics
  next_steps process quiz quote risks section statement table timeline title`. Every slide: `id`, `pattern`, a claim
  `title`, `notes.say` (2-5 spoken sentences) and `notes.assumptions` for anything not in the brief; deck: `direction`,
  `footer`, `"sources": ["the brief"]`, numbers in `facts`.
- Do not open the per-slide PNGs or re-read specs after `--apply`: the summary already says what changed (`applied:`).

## New deck — the checklist

```
1. Spec      content first: audience, claim titles, notes; numbers in `facts` with {sum}/{change}/{share}
2. --plan    python scripts/build_deck.py spec.json --plan --apply  (writes every ready edit; lists `question:`s)
3. Answer    one edit: each `question:` (a cost, a target number, points - only you have them); skim `applied:`
4. --check   python scripts/build_deck.py spec.json --out deck.pptx --check --apply
5. Look      open the contact sheet it names - once, all slides together
6. Done      exit 0, no `question:` and a sheet that looks right; else one more edit and step 4
```

- `--plan` checks everything it can before a build: spec limits and warnings, word budgets, title wraps, and a dry
  build (fit and layout lint, deleted after). Each fixable finding gets a ready edit (`suggest: field: 'old' ->
  'new'`, measured; it only removes or abbreviates words, the removed text goes to the notes as `MOVED FROM SLIDE:`);
  `--apply` writes them, and the auto-fixes, into the spec (`<spec>.before-apply.json` keeps the previous file).
  What needs new content stays a `question:`; a cut that might change the sense is only a `proposal`.
- `--check` = build + lint + `render_lo.py --sheet` (when LibreOffice is installed) + `visual_check.py` on the
  renders (`visual_*`: empty bands and empty card bottoms, list-like stacks, lopsided or crowded slides) + one
  summary with a `CHECK-JSON` line. Exit 0 clean, 2 spec error, 3 text that still does not fit.
- Text that does not fit is fixed first (filler words, short units, detail moved to the notes as
  `MOVED FROM SLIDE:`, a split where `"allow_split": true`); each change prints as `auto:`. `--no-auto` reports only.
- Pick patterns that show the thing itself, give the deck a `footer` and the ask a `decision` with its `figure`
  ([BUILDER](reference/BUILDER.md), [DESIGN](reference/DESIGN.md)). Treat `spec warning:` lines as content to fix.
- First-draft habits that cost a rebuild: an ask without its cost (`"..., 3 FTE, cost from Finance"`), a target
  without a number (`">= 90 % of sprints"`), a quiz `reveal: slide` without `answer_title`, points over ~60
  characters. Write them right in the spec and `--plan` is clean.
- Icons come bundled (Lucide, editable vector shapes in the accent): `"icon"` on tiles, cards, steps and stages, or
  chosen from the words automatically (`"auto_icons": false` to stop); a picture beside points is `image_text`,
  `alt` required ([BUILDER](reference/BUILDER.md#icons-and-pictures)).
- Keep list items, stage labels and chart captions short (a phrase, ~4 words for a stage): short items get numbered
  bands, level label cards and full-width charts; long ones fall back to plain layouts. A pilot timeline gets a
  `window` (`"Jan-Jun"`) so a month past it is flagged.
- Chart each data series once: a summary slide states its conclusions in words or KPI figures (no `trend`), the
  detail slides carry the charts - two slides charting the same numbers is a spec warning ([CONTENT](reference/CONTENT.md#a-summary-states-conclusions-the-detail-slides-carry-the-charts)).
- **4+ slides in one design:** showcase-first - `--slides 1,3 --check`, look, then the rest; unattended, approve it
  yourself and say so ([WORKFLOW](reference/WORKFLOW.md#showcase-first-for-multi-slide-sections)).
- Three fixes on the same defect without success: escalate - [iteration loop](reference/WORKFLOW.md#iteration-loop--build-render-look-critique-fix).

## Existing deck: restyle or keep the look

Ask (or read from the request) whether the deck must keep its design - a company template, a deck others keep
editing, "just tidy it" - or may take the skill's design.

| | **Restyle** - rebuild in the skill's design | **Keep the look** - improve in place |
|---|---|---|
| When | The design is weak or ad hoc; the content is what matters | Brand, template or the owner's design must stay |
| Steps | `extract_spec.py old.pptx --out spec.json` → read the `flag:` lines, edit the spec (claim titles, better patterns, the moved text) → `build_deck.py spec.json --out new.pptx --check` → `extract_spec.py old.pptx --compare new.pptx` | Snapshot → `improve_deck.py old.pptx --out improved.pptx` (safe fixes + DRAFT notes + lint report) → fix what the report leaves by hand ([AUDIT](reference/AUDIT.md)) |
| Notes | Existing notes kept as the script; missing ones drafted from the slide's words | Missing or script-less notes drafted from the slide's words; originals kept below the divider |

- Both write drafts only from what the slide shows. Review every DRAFT and add the figures' sources before
  presenting - never fill a gap with an invented fact (core rule 9).
- The extracted spec is a starting point: nothing is dropped (text with no room goes to the notes as
  `MOVED FROM SLIDE:`), so `--compare` must report every word and figure kept before the old deck is retired.

## Core rules

These apply to every deck. Each links to its full explanation.

1. **Snapshot before anything destructive** — `scripts/backup_snapshot.py`. Undo is not a backup. ([COM](reference/COM.md#snapshot-before-any-risky-bulk-edit))
2. **Never trust `ActivePresentation`** — find the deck by exact name, then substring. ([COM](reference/COM.md#multi-presentation-safety--never-trust-activepresentation))
3. **Rebuild, don't patch** — one idempotent `build_slide_NN.py` per non-trivial slide; name every shape. Three patches = rewrite. ([COM](reference/COM.md#idempotent-build-scripts))
4. **Never overwrite people's edits** — `scripts/harvest_edits.py` before regenerating a deck. ([COM](reference/COM.md#a-generated-deck-that-people-also-edit-in-powerpoint-harvest-before-you-overwrite))
5. **Full HD = 1440 × 810 pt**, set before inserting slides. ([LAYOUT](reference/LAYOUT.md#slide-size--set-it-before-inserting-anything))
6. **About 10 visible words per slide (by anchor type), body ≥ 18 pt on a 960-pt slide — ≥ 27 pt on Full HD (1440 pt)**, claim titles. ([LAYOUT](reference/LAYOUT.md#anchor-types-and-word-budgets), [CONTENT](reference/CONTENT.md#titles-make-a-claim-not-a-topic))
7. **No text baked into images or video** — overlay it in PowerPoint. ([MEDIA](reference/MEDIA.md#generate-images-without-text--overlay-text-in-powerpoint))
8. **Crop pictures, never stretch them.** ([LAYOUT](reference/LAYOUT.md#pictures-stretch--crop-to-fill-never-pass-both-sizes-blindly))
9. **The slide carries the punch, the notes carry the depth** — notes on every slide, written first: a spoken script (`say`: 2-5 sentences the presenter says, point first, each figure with its source in the sentence), then a brief presenter-only reference. Never invent facts beyond the brief: put anything you add in the notes' `assumptions` (written after the script as `Assumed (confirm before presenting):`); when the brief is the only source, say so — deck-level `"sources": ["the brief"]`. An ask states its reasons and its cost or impact. A goal you add (per person, per month) is derived from the stated target and adds up to it; each objection / FAQ answer gives claim, proof and action (6+ words), the full answer in `say`. ([CONTENT](reference/CONTENT.md#every-slide-gets-notes-never-invent-facts-beyond-the-brief), [ask](reference/CONTENT.md#the-ask-states-its-reasons-and-its-cost), [goals](reference/CONTENT.md#invented-goals-must-add-up-to-the-stated-target), [objections](reference/CONTENT.md#objection-answers-claim-proof-action))
10. **Lint, then render and LOOK** before calling anything done — `scripts/lint_deck.py` catches what the file shows (overlaps, stretched pictures, small text, missing alt text) on any OS; the render catches the rest. Render via Save As JPEG on Windows, not `Slide.Export`; `scripts/render_lo.py` elsewhere (approximate). (Loop below; [LAYOUT](reference/LAYOUT.md#embedded-fonts-slideexport-renders-a-fallback--use-save-as-jpeg))

## Error reports - always ask first

A script that exits with code **4** (stderr: `ERROR-REPORT-PENDING: <file>`) hit an unexpected error whose report
is waiting. Ask the user exactly "Do you want to send this error message?" (AskUserQuestion, Yes / No) and show
what would be sent. Only on **Yes** run the `send_error_report.py <file> --yes` command it printed; on **No** run
it with `--no`. PowerPoint Live says `ERROR-REPORT-PENDING` in its error message: ask the same question, then call
`powerpoint_send_error_report` with `send=true` only on Yes (`false` on No). Never send without the user's yes.

## Version-specific facts (as of 2026-10)

These depend on upstream releases. Re-check them when something that used to work breaks:

- Veo model ids `veo-3.1-generate-preview` and `veo-3.1-fast-generate-preview` are confirmed; a `lite` id is not ([MEDIA](reference/MEDIA.md#key-details)).
- `Slide.Export` shows fallback fonts for embedded fonts; `scripts/render_slides.py` does not.
- python-pptx 1.0.2 behaviour is assumed in the slide-copy notes ([COM](reference/COM.md#a-generated-deck-that-people-also-edit-in-powerpoint-harvest-before-you-overwrite)).

## Anti-patterns

The catalogue of silent failures that have shipped broken slides - trusting `ActivePresentation`, the
`HasTextFrame` filter, moving text without its backing, skipping the LOOK step, both sizes on `AddPicture`,
inventing facts, adding up by hand and more - is in [WORKFLOW](reference/WORKFLOW.md#anti-patterns-recurring-com--build-traps).
Skim it before a non-trivial COM patch; add a row there when a new one bites.
