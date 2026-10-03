---
name: figure-rhetoric
description: 'Evaluate whether figures and plots in a manuscript effectively communicate the claims they support. Audits chart-type fit, axis design, visual hierarchy, data density, caption interpretation, perceptual accuracy, and narrative arc across 8 dimensions. Triggers on: "do my figures work", "check my plots", "are my graphs clear", "figure audit", "do my figures support my claims", "visualization review", "figure rhetoric", "plot review", "chart critique", "visual argument check". Companion to manuscript-review §12 (legibility) and figure-table-quality (rendering).'
metadata:
  version: 1.0.0
  complements: [manuscript-review, figure-table-quality, manuscript-typography]
  category: review
  tags: [figures, visualization, rhetoric, plots, charts]
  difficulty: advanced
  phase: review
---

# Figure Rhetoric Audit

**Pipeline position:** Phase 1b (content audit). Runs in parallel with
manuscript-review. Requires compiled PDF. No prior dependencies.
See `/manuscript-pipeline` for full execution order.

## Purpose

Evaluate every figure in a manuscript as a *rhetorical act* — a visual
argument that must land with the reader. Each figure exists to communicate
a specific claim. This skill audits whether the figure actually achieves
that communication, or whether it undermines, obscures, or contradicts
the author's intent.

A figure that is technically correct but rhetorically ineffective is a
wasted opportunity. Reviewers form judgments from figures before reading
the methodology. A figure that fails to show what the text claims creates
doubt even when the underlying data supports the claim.

## Relationship to Other Skills

| Concern | This skill (figure-rhetoric) | manuscript-review | manuscript-typography |
|---------|------------------------------|-------------------|-----------------------|
| Chart type selection | Is this the right chart for this claim? | N/A | N/A |
| Visual emphasis | Does the figure draw attention to the right thing? | N/A | N/A |
| Prose-figure alignment | Does a reader SEE what the text SAYS? | Does the text match the figure? (§24) | N/A |
| Data selection | Should different data be plotted? | N/A | N/A |
| Axis design | Do axes help or hide the story? | Axis labels present? (§12) | Font consistency |
| Figure quality | N/A | Resolution, colorblind, chartjunk (§12) | Backgrounds, framing |
| Figure rendering | N/A | Legibility at print scale (§23) | Caption formatting |
| Provenance | N/A | N/A (→ manuscript-provenance) | N/A |

**Boundary:** manuscript-review §24 checks "does the prose match the figure?"
This skill checks "does the figure *communicate* what the prose needs it to?"
§24 catches factual mismatches (text says 14.3%, figure shows 13.8%).
This skill catches rhetorical failures (text says "dramatic improvement,"
figure shows bars that look identical because the y-axis starts at 0).

## Workflow

### 1. Ingest

**CRITICAL: This skill requires visual inspection.** LaTeX source alone is
insufficient. The entire point of this audit is what the reader *sees*.

Obtain the rendered figures by one of:
1. **Compiled PDF** (preferred) — use the Read tool on the PDF file to inspect
   each page containing a figure at actual rendered size
2. **Individual figure files** — use the Read tool on each `.pdf`, `.png`,
   `.jpg` figure file referenced by `\includegraphics`
3. **If neither is available** — ask the user to compile the PDF or provide
   figure files. Do NOT proceed with source-only analysis. A rhetoric audit
   without seeing the figures is meaningless.

For each figure:

1. **Visually inspect the figure.** Read the figure file or the PDF page
   containing it. Before reading any prose, record what the figure
   communicates at first glance — the immediate visual takeaway. What
   pattern, trend, comparison, or relationship does a naive reader see?

2. **Extract the claim context.** Read the 2-3 paragraphs surrounding the
   first `\ref{fig:X}` reference. Identify the specific claim the figure
   is supposed to support. Write it down as a one-sentence assertion.

3. **Read the caption.** Does the caption tell the reader what to see, or
   does it just describe the axes?

4. **Compare.** Does the visual takeaway (step 1) match the claimed
   assertion (step 2)? The figure must be evaluated through the reader's
   eyes, not the author's intent.

### 2. Per-Figure Analysis

For each figure, evaluate across 8 dimensions:

---

**Dimension 1 — Claim-Figure Alignment**

The central question: does a reader who looks at this figure *see* the
claim the text makes?

- Identify the prose claim (e.g., "Method A converges faster than B")
- Identify the visual impression (e.g., "Two nearly identical curves")
- If these differ: the figure fails its rhetorical purpose regardless
  of whether the data technically supports the claim

Failure modes:
- **Invisible difference:** The text claims a meaningful difference but
  the figure's scale, aspect ratio, or data density makes the difference
  imperceptible. The data is there; the visual isn't.
- **Wrong emphasis:** The figure shows many things, the text discusses one.
  The reader doesn't know where to look.
- **Contradictory impression:** The visual impression actively suggests
  the opposite of the claim (e.g., "convergence" but the curve is still
  trending; "improvement" but the bars look equal).
- **Unstated context:** The figure requires domain knowledge to interpret
  that the surrounding text doesn't provide.

---

**Dimension 2 — Chart Type Appropriateness**

Is this the right type of visualization for this claim?

| Claim type | Effective chart | Ineffective chart |
|------------|----------------|-------------------|
| Comparison across categories | Grouped bar, dot plot | Pie chart, stacked bar (hard to compare) |
| Trend over time/sequence | Line plot | Bar chart (obscures continuity) |
| Distribution | Histogram, violin, box plot | Bar chart of means (hides variance) |
| Correlation / relationship | Scatter plot | Table of paired values |
| Composition / proportion | Stacked area, stacked bar | Multiple pie charts |
| Difference / improvement | Difference plot, waterfall | Side-by-side bars at full scale |
| Ranking | Horizontal bar (sorted) | Vertical bar (unsorted) |
| Spatial | Heatmap, contour | Table of values |
| Part-to-whole | Treemap, stacked bar | Grouped bar |
| Flow / process | Sankey, alluvial | Static diagram |
| Confusion / classification | Confusion matrix (heatmap) | Table of numbers |
| Ablation contributions | Waterfall chart | Table or grouped bar |

Flag when a more effective chart type exists for the claim being made.

---

**Dimension 3 — Axis and Scale Design**

Axes can make or break the visual argument.

- **Y-axis origin:** Starting at 0 when differences are small makes them
  invisible. Starting above 0 when showing absolute quantities is
  misleading. The choice must serve the claim:
  - Showing "our method is better" → zoom in on the relevant range
  - Showing "the effect is small relative to the total" → start at 0
  - Always: clearly label the axis range; broken axes with `//` if needed

- **Axis scale:** Linear vs logarithmic. Log scale appropriate when data
  spans orders of magnitude or when relative differences matter more than
  absolute. Flag linear scale with data spanning 3+ orders of magnitude.

- **Axis range:** Does the range include all relevant data? Does it extend
  far beyond the data (wasting space)? Is the range chosen to exaggerate
  or minimize visual differences?

- **Aspect ratio manipulation:** A very wide or very narrow plot can
  exaggerate or flatten trends. The slope of a trend line should be
  perceptible but not exaggerated.

- **Dual axes:** Almost always confusing. Two different y-axes invite
  incorrect visual comparisons. Prefer: two separate panels with
  aligned x-axes.

---

**Dimension 4 — Visual Hierarchy and Emphasis**

Does the figure guide the reader's eye to the right element?

- **Primary element:** The data series, region, or comparison that the
  text discusses should be visually dominant (thicker line, bolder color,
  larger markers, foreground position).

- **Secondary elements:** Context, baselines, and reference data should
  be visually recessive (thinner lines, gray, smaller markers, background).

- **Annotations:** If the text references a specific point, region, or
  threshold, it should be annotated in the figure (arrow, callout, shaded
  region, dashed reference line). The reader should not have to decode
  coordinates to find what the text describes.

- **Cognitive load:** Count the number of distinct visual elements the
  reader must track. More than 5-7 series/groups in one plot exceeds
  working memory. Split into panels or highlight the comparison of interest.

Failure modes:
- All lines/bars have equal visual weight — reader doesn't know what's important
- The "our method" line is the same width and style as 10 baseline lines
- Text says "note the divergence at epoch 100" but nothing in the figure marks epoch 100
- Legend has 15 entries — reader must constantly reference it

---

**Dimension 5 — Data Density and Simplification**

Is the figure showing the right amount of data for its claim?

- **Overloaded:** Too many series, categories, or data points for a
  single plot. The claim is about the relationship between 2 methods
  but the plot shows 12. Simplify: show the comparison of interest
  prominently; relegate others to supplementary material or a secondary
  panel.

- **Underloaded:** The plot shows so little data that the claim isn't
  convincing. A single point where a trend is claimed. Two bars where
  a distribution is relevant. Three epochs where convergence behavior
  matters.

- **Summarized when raw matters:** Showing only means when the variance
  is the story (or when it would undermine the story — flag both).
  Confidence intervals, error bars, or violin plots for stochastic results.

- **Raw when summary matters:** Individual data points where the
  aggregate pattern is the claim. A scatter plot of 10,000 points where
  a density plot or binned heatmap would show the structure.

---

**Dimension 6 — Caption as Interpretation Guide**

The caption should tell the reader *what to see*, not just *what the axes are*.

**Levels of caption quality:**

1. **Descriptive only** (weak): "Training loss over epochs for five methods."
   The reader must figure out the takeaway.

2. **Directive** (adequate): "Training loss over epochs. Method A (red)
   converges in ~50 epochs while baselines require 150+."
   Points the reader to the claim.

3. **Interpretive** (strong): "Training loss over epochs. Method A (red)
   converges 3x faster than the nearest baseline (blue), supporting the
   claim that architectural change X reduces optimization difficulty."
   Connects the visual to the argument.

For each caption, identify its level and recommend upgrading if Level 1.
Level 2 is the minimum for effective communication. Level 3 is ideal for
key figures supporting core claims.

---

**Dimension 7 — Perceptual Accuracy**

Does the visual encoding accurately represent the underlying data?

- **Area encoding for quantities:** If using bar width, bubble size, or
  area to encode values, the mapping must be proportional to area (not
  radius or diameter). A value 2x larger should have 2x the area, not
  2x the radius (which is 4x the area).

- **3D effects:** 3D bar charts, 3D pie charts, perspective effects —
  these distort perception of values through foreshortening. Flag any
  3D visualization of 2D data.

- **Color scale linearity:** Sequential color maps (viridis, plasma)
  have perceptually uniform steps. Rainbow/jet color maps have
  perceptual discontinuities that create artificial boundaries in
  continuous data. Flag rainbow/jet for continuous data.

- **Truncated axes without indication:** Y-axis not starting at 0
  without a visible break (`//` notation) can mislead readers about
  relative magnitudes.

- **Aspect ratio distortion:** Pie charts not circular. Bar widths
  inconsistent. Maps with incorrect projections (rare in ML papers
  but common in spatial analysis).

---

**Dimension 8 — Redundancy and Narrative Arc**

Do the figures as a *set* tell a coherent story?

- **Redundant figures:** Two figures showing essentially the same
  information in different forms. Unless each adds distinct insight,
  merge or choose the more effective one.

- **Missing figures:** Is there a key claim in the text that has no
  visual support but would benefit from one? A figure that isn't there
  is a missed opportunity if the claim is central.

- **Figure ordering:** Do the figures appear in the order of the paper's
  argument? Architecture → training → results → analysis is a natural
  arc. Figures out of narrative order confuse the reader's mental model.

- **Visual consistency across figures:** Same method → same color/marker
  across all figures. Same data → same axis scale when comparison is
  relevant. Cross-reference with manuscript-review §12 (visual language
  consistency).

---

### 3. Common Antipatterns

Quick-reference of frequently occurring rhetorical failures:

| Antipattern | Description | Fix |
|-------------|-------------|-----|
| **The Invisible Win** | Method outperforms by 0.3% but y-axis spans 0-100% | Zoom to relevant range; use difference plot |
| **The Spaghetti Plot** | 10+ overlapping lines, all same weight | Highlight 2-3 of interest; gray out rest |
| **The Bar Chart of Means** | Bars showing means without error bars/CI | Add error bars; consider violin/box plots |
| **The Orphan Claim** | Text discusses a specific region/point with no annotation | Add arrow, shaded region, or reference line |
| **The Pie Chart** | Comparing proportions across >5 categories | Horizontal bar chart, sorted |
| **The Rainbow Heatmap** | Jet/rainbow colormap for continuous data | Use perceptually uniform colormap (viridis) |
| **The Giant Legend** | Legend with 15 entries reader must cross-reference | Direct labeling on lines; or reduce series count |
| **The Wrong Chart** | Line chart for categorical data; bar chart for trends | Match chart type to data type and claim |
| **The Dual Axis** | Two y-axes implying false correlation | Two separate panels, aligned x-axis |
| **The Data Dump** | All results in one figure "for completeness" | Show what matters; appendix the rest |
| **The Missing Baseline** | Results without visual reference point | Add dashed line for baseline/random/human performance |
| **The Abstract Figure** | Text says "see Figure 3" but Figure 3 requires 5 minutes of study | Simplify; annotate; upgrade caption |

---

### 4. Generate Report

For each figure, produce:

```markdown
## Figure [N]: [brief description]

**Prose claim:** [one-sentence claim the figure is supposed to support]

**Visual takeaway:** [what a reader actually sees at first glance]

**Alignment:** [STRONG | ADEQUATE | WEAK | CONTRADICTORY]

**Issues:**

1. [Dimension]: [specific problem]
   - **Impact:** [how this affects the reader's understanding]
   - **Fix:** [specific recommendation with concrete changes]

**Caption assessment:** [Level 1/2/3] — [recommendation if upgrade needed]

**Recommended changes:** [prioritized list]
```

Then a summary section:

```markdown
## Figure Set Assessment

**Overall narrative coherence:** [figures tell a coherent story / gaps exist / redundancies]

**Strongest figure:** Figure [N] — [why it works]
**Weakest figure:** Figure [N] — [primary issue]

**Priority fixes:**
1. [Most impactful change across all figures]
2. [Second most impactful]
3. [Third most impactful]

**Missing figures:** [claims that need visual support but lack it]
**Redundant figures:** [figures that could be merged or cut]
```

### 5. Output

Save report as `[manuscript-name]-figure-rhetoric-report.md`.

Present:
- Count of figures by alignment rating (STRONG / ADEQUATE / WEAK / CONTRADICTORY)
- Top 3 fixes by impact
- Any CONTRADICTORY figures (highest priority — these actively hurt the paper)

## Core Principles

- **The reader is naive.** Do not evaluate figures through the author's
  eyes. The author knows what the figure "should" show. The reader sees
  only what is visually present. Every judgment in this audit is from
  the reader's perspective.

- **Claim first, then figure.** Read the prose claim before looking at
  the figure. The figure's job is to support that specific claim. If the
  figure is beautiful but doesn't support the claim, it fails.

- **One figure, one message.** A figure trying to show three things shows
  none of them clearly. If the text makes three claims about one figure,
  the figure is overloaded or the text should point to three figures.

- **Visual perception trumps data accuracy.** A figure can be numerically
  correct but perceptually wrong (e.g., differences invisible due to
  scale). The reader's visual impression IS the communication. If the
  impression doesn't match the claim, the figure has failed.

- **Concreteness over abstraction.** Recommendations specify the exact
  change: "change y-axis range from 0-100 to 85-95," not "consider
  adjusting the axis." Include suggested chart types, axis ranges,
  color choices, and annotation text.

- **Severity scales with claim importance.** A weak figure supporting
  a minor methodological point is LOW priority. A weak figure supporting
  the paper's core result is CRITICAL — it's the first thing a reviewer
  scrutinizes.
