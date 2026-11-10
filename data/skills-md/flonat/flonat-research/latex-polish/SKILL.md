---
name: latex-polish
description: "Inspect a cleanly compiling LaTeX document for source pathologies and rendered visual defects by linting and viewing selected PDF pages. Use when compilation succeeds but title pages, floats, tables, figures, or layout still need publication-quality review. Not for basic compilation health; use $latex-health-check."
allowed-tools: Bash(ls*, mkdir*, cp*, pdftoppm*, pdftocairo*, pdfinfo*, grep*, sed*, awk*, find*, chktex*, latexindent*, cat*, head*, tail*, wc*, sort*, uniq*, rm*, mktemp*), Read, Write, Edit, Glob, Grep
argument-hint: "[tex-path] [--no-vision] [--pages 'auto|1,3,5']"
skill-dependencies: [latex]
---

# LaTeX Polish — Source Lint + Vision-On-Rendered-PDF

> Heavier-weight visual-quality review than `latex`. Combines the Phase 4 source-pathology lint with vision-model inspection of selected rendered PDF pages. Designed to catch the failure class that `latex` Phase 4 source-grep misses: blank pages, clipped tables, illegible shrunken figures, weird title-page line spacing that the regex couldn't fingerprint, bad float placement, overlap.

## When to Use

- Pre-submission visual check on a paper, proposal, thesis, or deck
- After major restructuring (new sections, table re-layouts, figure swaps) when you want eyes on the rendered output
- When `latex` reports a clean build but something still "looks weird"
- When preparing for a panel / supervisor read where presentation matters

## When NOT to Use

| Need | Use instead |
|------|-------------|
| Compile-fix loop | `latex` |
| Citation audit | `latex` (Phase 5) or `bib-validate` |
| Prose / academic-argument review | `proofread` |
| Single-figure analysis | `figure-feedback` |
| Continuous integration | This skill renders + vision-inspects pages; too expensive to run on every save |

## Inputs

- **`.tex` path** — auto-discovered or user-provided. Prefer the user's argument.
- **PDF path** — assumed at `<project>/<basename>.pdf` (per `latex` convention). If absent or older than `.tex`, the skill aborts and suggests `latex` first.
- **`--no-vision`** — skip the vision-rendering phases (Page rendering onward), run the source-pathology lint only.
- **`--pages auto|N,N,N`** — page selection override. Default `auto`.

## Hard Rules

1. **Do not compile.** This skill presupposes a clean PDF. If the PDF is missing or stale, abort and suggest `latex` first.
2. **Read-only with respect to source files.** Exception: Pattern-1 (spacing-hack) opt-in fix, which is offered with a diff and only applied on explicit user yes.
3. **No deploy actions.** This skill produces a report; it does not commit, push, or modify build infrastructure.
4. **Cap render cost.** Max 8 pages rendered per invocation. If page selection would exceed 8, prioritise: title page, worst-overfull page, first table/figure page, then arbitrary sample.
5. **Cap vision-prompt cost.** One Read per rendered page. No per-page back-and-forth.

## Protocol — 7 Phases

### Phase 1: Pre-flight

1. Resolve `.tex` path. If a directory was given, find `main.tex` or single `.tex` inside.
2. Resolve PDF path: `<dirname>/<basename without .tex>.pdf`. If missing or older than `.tex`, abort with: "Stale or missing PDF — run `latex` first."
3. Verify `pdftoppm` is on PATH. If not, abort with install hint (`brew install poppler` on macOS).
4. Create render dir: `mktemp -d /tmp/latex-polish.XXXXXX`. Track this as `$RENDER_DIR`.

### Phase 2: Source-pathology re-run (Phase 4 of `latex`)

Run the 9 grep-based source-pathology detectors from `<skills-root>/latex/references/source-pathologies.md`, plus `chktex` and `latexindent -k` if installed. Collect findings into a structured list.

This phase is identical to `latex` Phase 4 and is rerun here for self-containment (so `latex-polish` can be invoked without a prior `latex` run).

### Phase 3: Page selection

Determine which pages to vision-inspect. Default `auto`:

| Page | Why | Mandatory if available |
|------|-----|------------------------|
| 1 | Title / cover — high-stakes visual real estate; title-page failure mode is common | Yes |
| Page containing any overfull vbox > 50pt | Vertical overflow is almost always visually broken | Yes |
| Page containing the largest overfull hbox | The "worst" horizontal overflow seen | Yes |
| First page containing a table | Tables produce the most common visual pathologies | Yes |
| First page containing a figure | Same | If figures exist |
| Last body page before bibliography | Catches widow/orphan and end-of-content layout issues | If pages > 5 |
| Bibliography page 1 | Citation formatting + hanging indent regressions | If bib exists |

If overfull-box locations are not known (no log file or out/main.log missing), skip those entries. Cap total at 8 pages; if the selection would exceed 8, drop the lowest-priority entries.

Pull overfull-box page locations by reading `<project>/out/<basename>.log`:

```bash
awk '/Overfull \\(v|h)box/ { for(i=1;i<=NF;i++) if($i ~ /\[[0-9]+\]/) print substr($i,2,length($i)-2) }' out/main.log | sort -u
```

For each candidate page, also record WHY it was selected (used to pick the right vision-prompt later).

### Phase 4: Page rendering

```bash
for P in $SELECTED_PAGES; do
    pdftoppm -r 150 -f $P -l $P -png "$PDF" "$RENDER_DIR/page-$P"
done
```

150 DPI is enough for layout analysis without ballooning file sizes. Each PNG lands at `$RENDER_DIR/page-<N>-<P>.png` (pdftoppm pads the page number).

### Phase 5: Vision analysis

For each rendered page, `Read` the PNG and apply the per-page-type prompt from [`references/vision-prompts.md`](references/vision-prompts.md):

- **Title page** prompt: focuses on alignment, line-spacing consistency, weight hierarchy, vertical block separation, font-size jumps
- **Body page** prompt: focuses on paragraph spacing, hyphenation/justification artefacts, ragged margins, widow/orphan lines, float positioning
- **Table/figure page** prompt: focuses on caption position, alignment with surrounding text, legibility at this rendered size, clipping, awkward whitespace
- **Bibliography page** prompt: focuses on hanging indent, entry alignment, consistent inter-entry spacing
- **General** prompt: catches anything unmatched

Each Read produces a structured finding list per page. Output schema per page:

```
Page N (selection reason: "title page" | "overfull at L<line>" | …):
  - Finding 1: <one-sentence description> [Tier: Major/Moderate/Minor]
  - Finding 2: …
  Verdict: PASS / NOTES / REVISE
```

If `--no-vision` was passed, skip Phases 3–5 entirely.

### Phase 6: Report consolidation

Write the polish report to `<project>/reviews/<paper-slug>/latex-polish/<YYYY-MM-DD-HHMM>.md` (per `rules/review-artefact-routing.md`), where `<paper-slug>` is the paper being reviewed (e.g. `paper-jtp`, `paper-philtech`):

```markdown
# LaTeX Polish Report — YYYY-MM-DD HH:MM

**Document:** <path>
**PDF age:** <minutes/hours since last build>
**Pages rendered for vision:** N
**Source detectors run:** 9 grep + chktex + latexindent

## Source pathologies (Phase 2)

<table from Phase 4 spec>

## Per-page vision findings (Phase 5)

### Page 1 — title
<verdict and findings>

### Page <N> — <reason>
<verdict and findings>

...

## Consolidated verdict

PASS / NOTES / REVISE — based on the worst finding tier across both phases.

## Suggested remediations

<prioritised list, max 10 items>
```

### Phase 7: Quality score

Read [`references/quality-rubric.md`](references/quality-rubric.md). Compute deductions across:
- Source-pathology findings (mirrors `latex` rubric)
- Vision findings (this skill's distinct contribution)

Verdict thresholds per `skills/shared/quality-scoring.md`. Append the Score Block to the report.

## Pattern-1 opt-in auto-fix

If Phase 2 detects a Pattern-1 (spacing-hack) issue, the report includes an `**Offer:**` block:

```markdown
**Offer:** Wrap `<env-name>` in `\begin{singlespace}…\end{singlespace}` and delete the negative kerns at L<N1>, L<N2>. Apply? (Y/N)
```

Wait for explicit user approval. If yes, apply via narrow `Edit` calls and recompile via `latexmk`. If no, leave the report as-is. Do not silently apply.

This is the only auto-fix offered. All other findings are report-only.

## What `latex-polish` does NOT do

- Compile or fix compile errors (use `latex` first)
- Modify prose or argument (`proofread` covers that)
- Audit citations (`latex` Phase 5 or `bib-validate`)
- Replace `figure-feedback` for standalone figure-file analysis
- Auto-commit, auto-push, or modify settings.json / hooks / rules

## Cross-references

| Skill / File | Relationship |
|---|---|
| `latex` | Compile + Phase 4 grep lint + citation audit. `latex-polish` is the deeper sibling for visual-quality review. |
| `figure-feedback` | Vision pattern this skill reuses for per-page analysis |
| `proofread` | Prose / argument review; non-overlapping concern |
| `<skills-root>/latex/references/source-pathologies.md` | Shared detector catalogue |
| `rules/review-artefact-routing.md` | Where the polish report is filed |
| `rules/manuscript-edit-budget.md` | Why this skill is report-only by default |
