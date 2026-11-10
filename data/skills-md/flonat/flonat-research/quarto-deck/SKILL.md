---
name: quarto-deck
description: "Build a Quarto Reveal.js presentation (.qmd → HTML, optional PDF) with assertion titles, a narrative arc, a theme with layout classes, optional live R/Python cells, a mechanical lint, a rhetoric review and a visual check of every slide. Use when the user asks for a Quarto, Reveal.js or HTML slide deck, or teaching slides; a one-off deck, not a course website."
allowed-tools: Bash(quarto*), Bash(uv*), Bash(bash*), Bash(node*), Bash(npm*), Bash(pdftoppm*), Bash(pdfinfo*), Bash(mkdir*), Bash(ls*), Bash(cp*), Bash(open*), Bash(R*), Bash(Rscript*), Read, Write, Edit, Task
argument-hint: "[topic, content-path, or project-name]"
skill-dependencies: [beamer-deck]
---

# Quarto Deck

> Build browser-native slide decks with Quarto Reveal.js. Same rhetoric framework
> as `beamer-deck`, HTML output that can be shared as a URL, run live code, and
> still print to PDF.

## Purpose

Create one presentation as a `.qmd` file: assertion titles, a three-act arc, a
theme with reusable layout classes, speaker notes, figures generated from code,
and a deck that has been linted, reviewed and looked at slide by slide.

**Use this for:** teaching (workshops and classes), informal research talks,
web-shared decks, decks with live R/Python cells.
**Use `beamer-deck` for:** conference talks, seminars and anything that must be
PDF-native. Slides default to Beamer unless the user asks for Quarto or HTML.
**Use `quarto-course` for:** a course website with many lectures and exercises.

## Prerequisites

- Quarto ≥ 1.4 (`quarto --version`; 1.10 on the Mini).
- R with knitr for R chunks; `uv` for Python.
- For PDF export: Node.js and Google Chrome (set `CHROME` to the browser binary to override the macOS
  default). `puppeteer-core` installs itself once into
  `${XDG_CACHE_HOME:-~/.cache}/quarto-deck-print`; it downloads no browser.
- For page images: `pdftoppm` (poppler).

Bundled resources, referenced as `<this-skill>/...` (the directory holding this file):

| Path | What |
|---|---|
| `templates/deck.qmd`, `templates/theme.scss` | starter deck with every layout pattern, and its theme |
| `scripts/init-deck.sh` | scaffold a deck (never overwrites; respects an existing Quarto project) |
| `scripts/lint_deck.py` | mechanical lint, exit 1 on errors |
| `scripts/export-pdf.sh` (+ `print-pdf.mjs`, `package.json`) | render, print to PDF, write page images |
| `references/quarto-revealjs.md` | syntax: layout, fragments, notes, figures, live code, handouts |
| `references/chart-selection.md` | which chart for which claim |
| `references/quality-rubric.md` | deductions for the quality score |

---

## Critical Rules

0. **Python: ALWAYS use `uv run python` or `uv pip install`.** Never bare `python`, `python3`, `pip` or `pip3`. Include this in any sub-agent prompt that may run Python.
1. **One `.qmd` file = one deck.** `#` for section slides (act boundaries), `##` for content slides.
2. **Titles are assertions, not labels.** "Distance raises abortion costs", not "Results". The title states the slide's claim.
3. **One idea per slide.** If a slide makes two points, split it.
4. **Every number, quote and claim of fact is sourced** on the slide (`.source` line or `@citekey`). Never invent a statistic, and never leave a template placeholder in a delivered deck.
5. **Speaker notes in `::: notes`.** The slide anchors; the notes carry what is said.
6. **Styling lives in the theme `.scss`.** Use classes (`{.accent}`, `{.step-card}`); no inline `style=`.
7. **Figures first, from code, with alt text.** Scripts in `scripts/`, output in `figures/`, `fig-alt` on every image. Choose the chart with `references/chart-selection.md`.
8. **Build up with `.fade-in-then-semi-out` or `.incremental`**, never `.semi-fade-out` (it starts fully visible).
9. **Inside an existing Quarto project, follow its `_quarto.yml`.** Do not add a second theme or override its formats (e.g. the PB130/PB230 workshop decks: `live-revealjs` with webR, plus a `handout` profile).
10. **Nothing is done until it has been rendered and looked at.** Lint, then export page images and inspect them (Phase 4).

Academic exceptions: tables, equations and code may exceed the lint's word
limit. Split the slide rather than shrinking text below readable size.

---

## Rhetoric Principles

Same framework as `beamer-deck`. Full reference (Three Laws, MB/MC, Aristotelian
Triad, Narrative Arc, Pyramid Principle, Devil's Advocate, audience-specific
guidance): [`../shared/rhetoric-principles.md`](../shared/rhetoric-principles.md)

Reference palettes (Professional, Energetic, Academic) with CSS variants:
[`../shared/palettes.md`](../shared/palettes.md)

## Quality Scoring

- **Framework:** [`../shared/quality-scoring.md`](../shared/quality-scoring.md) — severity tiers, thresholds, verdict rules
- **Rubric:** [`references/quality-rubric.md`](references/quality-rubric.md) — issue-to-deduction mappings for this skill

Start at 100, deduct per issue found, apply the verdict. Compute the score in
Phase 6 and report it in the final output.

---

## Workflow: 6 Phases

```
You (orchestrator)
├── Phase 1: Gather context         (direct)
├── Phase 2: Design structure        (direct; the user approves the outline)
├── Phase 3: Build the deck          (direct)
├── Phase 4: Lint and visual check   (direct)
├── Phase 5: Rhetoric review         (sub-agent, fresh context)
└── Phase 6: Apply and finalise      (direct)
```

### Phase 1: Gather context

Read the project files, content sources and audience brief. Check whether the
target folder sits inside a Quarto project (`_quarto.yml` in it or a parent).
Ask the user:

- **Audience and goal**: teaching, lab meeting, informal talk? What should they believe or do afterwards?
- **Duration**: sets the slide budget (roughly one content slide per 1–2 minutes).
- **Content source**: paper draft, notes, existing slides?
- **Live code**: should students run code in the browser (quarto-live)?
- **Output**: URL only, or also a PDF or handout?

### Phase 2: Design structure

1. Choose the rhetoric balance for the audience.
2. Outline the slide sequence with assertion titles, grouped into three acts.
3. Mark which slides need a figure, a number (with its source) or live code.
4. Pick the palette, or the project's existing theme.

Present the outline to the user for approval before building.

### Phase 3: Build the deck

1. **Scaffold** a standalone deck: `bash <this-skill>/scripts/init-deck.sh <dir> <name>`.
   In an existing project it copies only the `.qmd`; align its `format:` block with the project or delete it to inherit.
2. **Generate figures** from scripts into `figures/`.
3. **Write the slides** with the layout patterns in `references/quarto-revealjs.md`; replace every template placeholder.
4. **Add speaker notes** to every content slide that carries an argument.
5. Preview with `quarto preview <deck>.qmd`.

### Phase 4: Lint and visual check

1. **Lint:** `uv run python <this-skill>/scripts/lint_deck.py <deck>.qmd`.
   Fix every ERROR (missing images, placeholders). Treat WARNs as review prompts:
   label titles, text-heavy slides, long lists, inline styles, missing alt text,
   `.semi-fade-out`. INFO lines list slides without notes and unsourced percentages.
2. **Render and image every page:** `bash <this-skill>/scripts/export-pdf.sh <deck>.qmd --png <dir>/pages`
   (add `--profile handout` for a project's static profile).
3. **Look at every page image.** Read them in small batches or tile them into a
   contact sheet under 1,500 px. Check for overflow, clipped figures, unreadable
   axis text, collisions with the logo or footer, and broken maths. Fix and re-run.

### Phase 5: Rhetoric review (sub-agent, fresh context)

Launch a read-only reviewer that did not write the deck:

```
subagent_type: Explore
prompt: |
  You are a rhetoric reviewer for an academic Quarto Reveal.js presentation.
  Read the file at: [PATH TO .qmd]. Speaker notes are in `::: notes` blocks.
  Do not edit any file. Evaluate:

  1. Narrative arc: three acts (Problem → Investigation → Resolution)? Strong
     opening (question, number, or bold claim)? One memorable closing takeaway?
  2. MB/MC balance: is cognitive load spread evenly? Overloaded or empty slides?
  3. Titles: is every content-slide title an assertion (a claim), not a label?
  4. One idea per slide: list any slide carrying two ideas.
  5. Transitions: does the audience always know where they are in the argument?
  6. Pyramid principle: conclusion before support?
  7. Evidence: is every number and factual claim sourced on the slide?

  Return structured markdown with a rating per criterion and concrete,
  slide-numbered suggestions.
```

### Phase 6: Apply and finalise

1. Apply the review feedback; re-run the lint and the page-image check.
2. **Compute the quality score** from `references/quality-rubric.md`, listing every issue from Phases 4–5.
3. Export what was asked for: the HTML (`quarto render`; add `embed-resources: true` for a single file without live code), the PDF, or the handout profile.
4. Confirm all files are in place and report the score and verdict.

---

## Output Checklist

```
deck-folder/
├── <deck>.qmd          # the presentation
├── theme.scss          # standalone decks only; projects use their own theme
├── figures/            # generated figures
├── scripts/            # R/Python scripts that make the figures
├── <deck>.html         # rendered deck (or the project's output-dir)
└── <deck>.pdf          # if a PDF or handout was asked for
```

- [ ] Every content-slide title is an assertion
- [ ] One idea per slide; three-act arc with a single closing takeaway
- [ ] Every number, quote and fact sourced on the slide; no placeholders left
- [ ] Lint: 0 errors; every warning fixed or deliberately kept
- [ ] Every page image inspected; no overflow or clipping
- [ ] Alt text on every figure; palette readable in greyscale
- [ ] Speaker notes on every argument-carrying slide
- [ ] Rhetoric review (Phase 5) applied
- [ ] Quality score computed and reported

## Cross-References

| Skill | When to use instead or alongside |
|-------|-------------------------------|
| `beamer-deck` | Formal academic talks that need PDF-native output |
| `talk-deck` | A conference or seminar talk for a paper, with speaker script and talk page |
| `quarto-course` | A course website with many lectures, exercises and navigation |
| `translate-to-quarto` | Converting an existing Beamer deck to Quarto |
| `project-deck` | Project status updates (supervisor meetings, coauthor handoffs) |
| `proofread` | Post-hoc review of text quality |
| `literature` | Finding and verifying citations to include |
