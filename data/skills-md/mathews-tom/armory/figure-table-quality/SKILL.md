---
name: figure-table-quality
description: 'Readability and rendering audit for figures and tables in academic manuscripts. Computes effective font/marker sizes at display scale from generation scripts, checks label collisions, color/hatch accessibility, axis-range efficiency, table formatting, and cross-figure consistency. Triggers on: "check figure quality", "audit plots", "readability check", "figure rendering", "are my figures readable", "table formatting check". Companion to figure-rhetoric (visual argument) and manuscript-typography (typesetting).'
metadata:
  version: 1.0.0
  complements: [figure-rhetoric, manuscript-review, manuscript-typography]
  category: review
  tags: [figures, tables, readability, rendering, latex]
  difficulty: advanced
  phase: review
---

# Figure & Table Quality Audit

**Pipeline position:** Phase 2.5 (between Grounding/Polish and Submission).
Runs after figure-rhetoric (content) and before arxiv-preflight (compliance).
See `/manuscript-pipeline` for full execution order.

## Purpose

Verify that every figure and table in a manuscript renders at readable size
in the compiled PDF. figure-rhetoric checks whether figures communicate the
right message. This skill checks whether the reader can physically read them.

## Execution

### Step 1 — Build the display-scale map

For every `\includegraphics` in the .tex source:

1. Extract the display width (e.g., `\textwidth`, `0.7\textwidth`, `0.55\textwidth`)
2. Compute the effective display width in inches using the document geometry
3. Read the figure generation script to find the `figsize` for each figure
4. Compute: `scale = display_width / figsize_width`

Also extract from the generation script or config:
- Base font sizes: title, label, tick, legend, annotation
- Marker sizes, line widths
- Bar widths (for grouped bar charts)

### Step 2 — Per-figure audit (all 9 checks)

For each figure, compute effective values at display scale and check:

#### 2a. Font size at render
```
effective_font = script_font × scale
```
| Element | Minimum | Warning |
|---------|---------|---------|
| Axis title | 7pt | 8pt |
| Tick labels | 6pt | 7pt |
| Legend text | 6pt | 7pt |
| Annotations | 6pt | 7pt |
| Panel titles | 7pt | 8pt |

**FAIL** if any element falls below minimum.
**WARN** if any element falls below warning threshold.

#### 2b. Label collision
Check for overlapping text in:
- X-axis tick labels (especially with rotation < 45° and > 3 labels)
- Y-axis tick labels (long text strings)
- Data annotations near each other
- Legend entries overlapping data

For rotated labels: compute horizontal footprint as
`len(label) × char_width × cos(rotation)`. If footprint > tick spacing, **FAIL**.

#### 2c. Marker and line visibility
```
effective_marker = script_marker × scale
effective_linewidth = script_linewidth × scale
```
- Markers below 4pt effective: **WARN**
- Line widths below 0.5pt effective: **WARN**

#### 2d. Bar chart readability
For grouped bar charts:
- Compute effective bar width in inches
- Check if bars are distinguishable (minimum 3pt effective width)
- Check if hatch patterns render at effective size
- Check for bar-label alignment

#### 2e. Color and hatch accessibility
- Are all series distinguishable in grayscale?
- Do hatch patterns provide redundant encoding for color?
- Are there more than 5 colors without hatching? **WARN**
- Are similar colors used for unrelated series?

#### 2f. Axis range efficiency
- Compute data range vs axis range
- If less than 40% of axis range contains data: **WARN** (wasted space)
- If data touches axis boundary: **WARN** (clipped data)

#### 2g. Annotation readability
- Do any data annotations overlap each other?
- Are annotations positioned to avoid occluding data?
- Do annotations use consistent formatting (fontsize, weight)?

#### 2h. Legend placement
- Does the legend overlap any data points or bars?
- Is the legend in a consistent position across similar figures?
- For multi-panel figures: is the legend in the first panel only (not repeated)?

#### 2i. Whitespace and margins
- Does `tight_layout()` or equivalent handle margins?
- Are panel titles cut off?
- Is there excessive whitespace (> 30% of figure area empty)?

### Step 3 — Table audit

For each `\begin{tabular}` or `\begin{table}`:

1. **Column alignment** — Are numeric columns right-aligned? Text left-aligned?
2. **Rule style** — Uses booktabs (`\toprule`, `\midrule`, `\bottomrule`)? No vertical rules?
3. **Caption position** — Table captions above, figure captions below?
4. **Width** — Does the table overflow margins? Check for `\resizebox` or `\small` hacks.
5. **Number formatting** — Consistent decimal places? Aligned decimal points?
6. **Header clarity** — Are column headers unambiguous?

### Step 4 — Cross-figure consistency

1. **Shared elements** — Do figures that share axes use the same scale?
2. **Color scheme** — Is the same color used for the same condition across all figures?
3. **Label vocabulary** — Are condition/model labels identical across all figures?
4. **Font family** — Same font across all figures?

## Output format

```markdown
## Figure & Table Quality Report

### Display Scale Map
| Figure | figsize | display | scale | verdict |
|--------|---------|---------|-------|---------|
| fig1   | 7×4     | 6.27"   | 90%   | OK      |

### Per-Figure Findings
#### Figure 1 (fig1_resolve_rates.pdf)
- [PASS] Font sizes: tick 8.1pt, legend 8.1pt
- [PASS] No label collisions
- [WARN] Bar width 3.2pt — borderline at print size
...

### Table Findings
#### Table 1 (table1_resolve.tex)
- [PASS] Booktabs rules
- [PASS] Caption above tabular
...

### Cross-Figure Consistency
- [PASS] Color scheme consistent
- [FAIL] Label mismatch: fig2 uses "cmd", other figures use "Yuj"

### Summary
- [count] FAIL (must fix)
- [count] WARN (should fix)
- [count] PASS
```

## Auto-Fix Rules

**AUTO-FIX** (apply directly):
- Rotation increase for overlapping x-labels (20°/15° → 45°)
- figsize reduction to match display context (eliminate >25% downscaling)
- Missing `tight_layout()` calls
- Inconsistent label text across figures (align to config/source of truth)

**HUMAN-REQUIRED** (present and wait):
- Figure redesign (different layout, panel arrangement)
- Axis range changes
- Color scheme changes
- Font size increases that affect layout
- Table restructuring

## Integration

This skill reads:
- `.tex` source (`\includegraphics` directives, `\geometry` settings)
- Figure generation scripts (figsize, font sizes, rotations, annotations)
- Figure config files (shared settings)
- Generated figure files (visual spot-check if PDF readable)
- Table `.tex` files

It does NOT:
- Evaluate whether figures communicate the right message (that's figure-rhetoric)
- Check arXiv format compliance (that's arxiv-preflight)
- Audit prose or claims (that's manuscript-review)
