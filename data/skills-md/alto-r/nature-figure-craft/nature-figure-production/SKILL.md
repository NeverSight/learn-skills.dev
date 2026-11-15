---
name: nature-figure-production
description: >-
  Produce, style and audit submission-ready research figures once the chart type
  is settled. Use for Nature-family artwork, matplotlib styling, distributions,
  forest plots, compositions, fits, densities, timelines, matrices, Sankey flows,
  small multiples, maps, quadrant plots, chord diagrams and multi-panel assembly,
  or when a figure looks unprofessional or bare. Applies landed type sizes,
  88/180 mm widths, semantic palettes, editable PDF/SVG plus PNG previews,
  standalone legends and a submission checklist. For chart-type selection use
  chart-type-chooser first. Excludes slides, posters, dashboards and conceptual
  schematics without data.
license: CC-BY-4.0
---

# Nature Figure Production

## Client compatibility

Use this skill in Claude Code or OpenAI Codex with the same workflow and resources.
Resolve `assets/` and `references/` relative to this `SKILL.md`, not the user's
working directory. Copy the needed plotting modules into the user's figure-code
directory, or add the installed `assets/` directory to the script's import path.
Run plotting scripts in the user's project and keep exports there.

In Codex, invoke explicitly with `$nature-figure-production` or let the client
select it. Reuse the data paths, chosen claim, filters, chart type and encoding
plan already agreed with `chart-type-chooser` or in another client session.
When the chart type is already fixed, use this skill directly.

## Overview

Most figure advice stops at "use Arial and 300 dpi". That is not what gets a figure
through production. Nature-branded journals impose a **physical** specification —
column widths in millimetres, a landed type-size window, an editable-vector
requirement, and a 50 MB per-file cap — and a **house style** that reviewers read as
a signal of competence long before they read the data.

This skill covers three layers, in the order they must be decided:

1. **Spec layer** — non-negotiable print-engineering constraints.
2. **Style layer** — house-style typography, axes, colour, and composition.
3. **Production layer** — how a real multi-panel journal figure is actually built
   (panels rendered separately, legends exported standalone, assembled in a vector tool).

Layers 1 and 2 mostly take things away. That is the right default and it is also the
easy failure: a panel can pass every rule here and still be one nobody reads. Step 3d
runs once in the other direction — what does this panel still need — before export.

Load references on demand:

- **[references/spec.md](references/spec.md)** — official final-artwork requirements, size tables, format rules
- **[references/style.md](references/style.md)** — typography, axes, colour system, colormap selection
- **[references/panels.md](references/panels.md)** — the recurring data-panel families: distributions, coefficients, compositions, fits, density panels, state timelines, matrices, flow panels, small-multiple grids
- **[references/palettes.md](references/palettes.md)** — palette gallery: worked diverging, sequential, ordinal, qualitative, semantic, 2×2 and region-fill schemes, with hexes, the job each does, and the measured lightness that makes it check out
- **[references/composition.md](references/composition.md)** — ten reusable multi-panel layout templates, flagged by whether they need coordinates
- **[references/quadrant.md](references/quadrant.md)** — region plots: where the dividing lines come from, sensitivity, naming, layering, marginals, insets, the legend-as-schematic
- **[references/maps.md](references/maps.md)** — map panels: the layer stack, basemap presets, points vs polygons, implementation traps, which layer to turn on. Skip if the data has no coordinates
- **[references/workflow.md](references/workflow.md)** — panel-separated production pipeline, assembly, checklist
- **[assets/nature_style.py](assets/nature_style.py)** — drop-in module: `panel()`, `apply_style()`, `landed_report()`, the palettes from `palettes.md` as importable constants, `diverging_cmap()`, `palette_report()`, `save_all()`, `export_legend()`
- **[assets/nature_panels.py](assets/nature_panels.py)** — the recurring panel families: `violin_box()`, `forest()`, `stacked_bars()`, `grouped_bars()`, `fit_line()`, `density_field()`, `runs()`, `state_bands()`, `matrix_panel()`, plus `auto_unit()`, `headroom()`, `stat_box()`, `ragged_grid()`, `tidy_grid()`
- **[assets/nature_map.py](assets/nature_map.py)** — map panel layers: basemap, polygon outlines, choropleth, density field, ringed value points, marginal profiles, data-driven colormap choice
- **[assets/nature_quadrant.py](assets/nature_quadrant.py)** — region plots: `threshold()`, `gmm_threshold()`, `sensitivity()`, `regions()`, `region_background()`, `divider()`, `bubble_scatter()`, marginals, `zoom_inset()`, `label_points()`, `counts_table()`, `partition_legend()`
- **[assets/nature_chord.R](assets/nature_chord.R)** — chord diagram (circlize): magnitude-encoded ribbon opacity, sub-threshold ribbons hidden without shrinking sectors, landed-pt label sizing, vector PDF export, and an opt-in grouping layer (group arcs, labels, and a gap budget)

Each asset module runs its own self-test on synthetic data:
`python nature_panels.py`, `python nature_quadrant.py`, `Rscript nature_chord.R`.

## When to use this skill

- Any matplotlib / seaborn / cartopy figure destined for a journal.
- A global or regional map panel — use the layer stack in Step 3b rather than
  starting from a blank basemap.
- Preparing or fixing final artwork before submission or at revision stage.
- A panel that is technically clean but reads as bare, or that a reader cannot orient
  themselves in — Step 3d.
- Assembling a multi-panel main figure.
- Auditing an existing figure against journal requirements.

## When NOT to use this skill

- Deciding **which chart type** to draw. Use `chart-type-chooser` first, then come back here.
- Slides, posters, or web dashboards. Different constraints entirely.
- Conceptual schematics with no data (Figure 1 motivated examples, method overviews).
  Those are drawn in PowerPoint / Figma / draw.io; only the spec layer applies.

---

## Core procedure

### Step 0 — Declare where each panel will be PLACED, not how big to draw it

This is the single most consequential decision and the one most often made last.

The rule everyone repeats — *"set `figsize` to the final size and write a fixed pt"* — is
correct only for a figure that is one panel at full column width. A real main figure
is 10–25 panels assembled in a vector tool, each placed at a different width. There
is no single "final size" for the script to use.

What is actually invariant is the arithmetic:

```
landed_pt = drawn_pt x (placed_width_mm / drawn_width_mm)
```

**`landed_pt` is what the journal constrains and what the reader measures. It is the
number to fix.** The drawn size follows from it.

```python
from nature_style import panel, apply_style, landed_report

# this panel will occupy 60 mm of a 180 mm three-across figure
p = panel(placed_mm=60, aspect=0.8)
apply_style(p)
fig, ax = plt.subplots(figsize=p.figsize)
...
landed_report(fig, p)     # measure before exporting
```

**The default type size is a range, and it depends on panel width.** Type does not
scale linearly with a panel: 6 pt reads comfortably across a 180 mm panel but looks
microscopic inside a 45 mm inset, where the eye judges it against a much smaller
frame. Narrow panels want proportionally *larger* type.

| Placed width | Default landed body | Notes |
|---|---|---|
| ≥ 160 mm | 9.0 pt | full double-column panel |
| 100–160 mm | 9.5 pt | half to two-thirds of a double-column figure |
| 60–100 mm | 10.0 pt | single column, or one of three across |
| < 60 mm | 10.5 pt | inset / small multiple |

**Axis labels, tick labels and legend text are all one size** — 0.5 pt below the
body size in the table. An axis label set larger than its own ticks reads as a heading
for the panel, which is the job the caption already does; and a legend sized on its own
makes an assembled multi-panel figure look assembled. The `body` size is left for
in-plot annotations, which do want a step up. The panel letter sits 1.5 pt above body,
capped at 12.

**On the 5–7 pt rule.** The official artwork guide asks for 5–7 pt as landed. This
skill deliberately does not target that window, and the reason is worth stating
because it contradicts most figure advice including earlier versions of this file.

5–7 pt is a floor-level *legibility* spec written for a printed page. Figures built
to the letter of it read as cramped everywhere people actually look at figures — on
screen, in a talk, in a PDF being skimmed. Accepted figures routinely run larger,
landing around 9–12 pt. Art editors reset
house style at production anyway, so being over the guide costs approximately
nothing, while sitting at the floor costs a figure nobody reads without zooming.

So: house target **9–10.5 pt** body, hard ceiling **12 pt**, hard floor 5 pt.
`landed_report` fails anything outside 5–12 and separately *notes* how much text sits
outside the guide's 5–7 window, so the information is never lost — it is just no
longer the thing being optimised. If a target journal genuinely enforces 5–7,
override with `panel(..., body_pt=6.5)` and set `LANDED_MAX = 7`.

**`draw_scale` is a comfort knob and changes nothing.** `panel(..., draw_scale=2)`
renders the panel at twice the size so you can read the preview PNG without zooming.
Because type, rules, ticks and markers are all multiplied together, the landed result
is identical at any draw scale — verified, not assumed:

```
draw_scale=1.0:   9.5 pt drawn -> 9.5 pt landed
draw_scale=2.0:  19.0 pt drawn -> 9.5 pt landed
draw_scale=4.0:  38.0 pt drawn -> 9.5 pt landed
```

Height ceiling depends on caption length (see `references/spec.md`); for a typical
<300-word caption it is ~130 mm single-column, ~185 mm double-column.

### Step 1 — Apply the global style block

`apply_style(p)` installs everything below from the panel spec. Paste it inline only
if you cannot import the module — and if you do, remember that every hard-coded
number here is a *drawn* value that must be multiplied by your own draw scale.

```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 9.5,            # LANDED sizes; multiply by draw_scale
    'axes.labelsize': 9,         # axis label = tick = legend, deliberately
    'axes.titlesize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'axes.linewidth': 0.6,       # line weights scale with type, or they
    'xtick.major.width': 0.6,    # break when the panel is shrunk
    'ytick.major.width': 0.6,
    'xtick.major.size': 2.5,
    'ytick.major.size': 2.5,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'lines.linewidth': 1.0,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'pdf.fonttype': 42,          # TrueType -> text stays editable (REQUIRED)
    'ps.fonttype': 42,
    'svg.fonttype': 'none',
    'axes.unicode_minus': False,
    'mathtext.fontset': 'custom',
    'mathtext.rm': 'Arial',
    'mathtext.it': 'Arial:italic',
    'mathtext.bf': 'Arial:bold',
    'mathtext.default': 'regular',
})
```

`pdf.fonttype = 42` is not optional. Without it, text is emitted as Type 3 outlines
and the production team cannot edit it — a direct violation of the artwork guide.

**Verify, do not trust.** `landed_report(fig, p)` walks the real `Text` artists in
the figure rather than reading back rcParams, so it catches hard-coded `fontsize=`
arguments, seaborn overrides and colorbar labels — which is where out-of-spec type
almost always hides. Run it on every panel before export.

### Step 2 — Define a semantic colour dictionary before plotting

One physical quantity gets one colour, fixed for the entire paper — main text,
supplement, and response-to-reviewers alike. Readers learn the code from Figure 1 and
stop consulting legends.

```python
QUANTITY = {
    'Component A': '#4C72B0',
    'Component B': '#DDAA33',
    'Component C': '#808080',
    'Component D': '#8172B3',
    'Component E': '#d47d49',
    'Component F': '#C44E52',
}
```

Rules: ≤6 saturated colours; give the elements the figure is arguing about more
visual weight than the rest; dual-encode (colour + linestyle / marker / hatch) so the
figure survives greyscale printing.

Pick the *shape* of the scheme before the hues, and pick it from the variable:
diverging only where there is a real midpoint, sequential where there is not,
an ordered ramp for ranked categories, a qualitative set only for unranked ones.
**[references/palettes.md](references/palettes.md)** has a worked scheme for each of
those, ready to copy, and the same schemes are importable from `nature_style.py`:

```python
from nature_style import DIVERGING, diverging_cmap, CLASSES6, NPG, palette_report

cmap = diverging_cmap()                       # neutral pinned to 0.5, not 0.583
palette_report(QUANTITY, name='QUANTITY')     # check it before it spreads
```

Rules for colour, and colormap selection: `references/style.md` §9–13.

### Step 3 — Draw the panel, applying house style

Checklist per axes. Most of these remove something, which is right for a first pass —
Step 3d then checks what the panel still needs:

- [ ] No `ax.set_title()` on a data panel — the caption is the title
- [ ] Axis labels in **Sentence case** with units as **negative exponents**:
      `r'Flux (mol m$^{-2}$ s$^{-1}$)'`, never `mol/m2/s`
- [ ] Tick values live in 0.1–999; convert units rather than showing `1e-3`
- [ ] `ax.spines['top'].set_visible(False)`; same for `'right'`
- [ ] Grid on y only: `ax.grid(axis='y', ls='--', lw=0.4, alpha=0.3)`; x grid off
- [ ] Legend `frameon=False`, no legend title
- [ ] A reference line where one exists (zero line, 1:1 diagonal, median cross)
- [ ] Dense marks get white separation: `edgecolor='white', linewidth=0.2–0.3`
- [ ] Panel letter: lowercase, bold, no parentheses, `transform=ax.transAxes`

```python
ax.text(-0.14, 1.06, 'a', transform=ax.transAxes,
        fontsize=8, fontweight='bold', va='top', ha='left')
```

- [ ] Scatter with n > ~5,000: `rasterized=True` (keeps the PDF under 50 MB)

Multi-panel: only outer axes carry axis labels; use `fig.supylabel()` for a shared
label and clear the inner ones.

### Step 3a — The recurring panel families

The checklist above is generic. Most panels also belong to one of a handful of
**families**, each with two or three decisions that the checklist cannot see
because nothing about the rendered panel looks wrong when they are made badly.

Full recipes in **[references/panels.md](references/panels.md)**; code in
`assets/nature_panels.py`.

```python
from nature_panels import violin_box, forest, stacked_bars, fit_line, density_field

violin_box(ax, groups, spec=p, labels=names, show_n=True)   # Tukey whiskers, real n
forest(ax, names, beta, ci_lo, ci_hi, spec=p, order=ORDER)  # bounds, not distances
stacked_bars(ax, x, components, spec=p)                     # total as its own mark
fit_line(ax, x, y, spec=p)                                  # band stops at the data
```

The decisions worth knowing before drawing anything:

1. **Violins hide `n` and fake their whiskers.** Matplotlib's default extrema
   run to the data min/max, so whisker length encodes sample size. Redraw at
   Tukey 1.5 × IQR and print `n` whenever groups are unbalanced.
2. **`xerr` wants distances; `conf_int()` returns bounds.** Passing bounds
   straight through renders happily and is wrong. `forest()` takes bounds.
3. **A stacked bar shows composition, not totals.** Only the bottom segment
   sits on a common baseline. Draw the total as its own line-and-marker layer.
4. **A confidence band must stop where the data stops**, and the caption must
   say whether it is a CI on the fitted line or a prediction interval.
5. **Above ~5,000 points a scatter is a silhouette.** Switch to a density
   panel — and give it a colour bar, or the reader cannot tell 60% from 99%.
6. **Intervals, never asterisks.** Colour by whether the interval excludes the
   reference. A star hides the effect size, and its p-value is inflated
   wherever observations are clustered. See panels.md §4.
7. **A ragged bottom row breaks the outer-ring label rule.** The test is
   `i + n_cols >= n`, not `row == n_rows - 1`, or whole columns lose their
   x axis. `tidy_grid()` handles it.

Sankey and alluvial panels are covered in panels.md §11 (plotly or R, with the
legend drawn separately in matplotlib and placed at assembly).

### Step 3b — Maps: five layers, chosen against the claim

Skip this step entirely if the data has no coordinates.

Full recipe in **[references/maps.md](references/maps.md)**; code in
`assets/nature_map.py`. A map is the one chart type where writing it from
scratch reliably produces something both ugly and un-submittable, because the
failure is structural: the basemap is a large amount of ink encoding no
variable, and it will dominate the marks unless actively suppressed.

```
1  basemap     land / ocean / coastline / borders, all near-invisible
2  polygons    reference or administrative regions: outlined, or filled by value
3  field       a continuous surface: density, interpolation, raster
4  points      one mark per site, encoded by value
5  marginals   profiles along longitude / latitude beside the panel
```

```python
from nature_map import map_axes, value_points, add_colorbar

fig, ax = map_axes(p)                   # global Robinson; pass extent= for a region
sc = value_points(ax, lon, lat, value, spec=p)
add_colorbar(fig, ax, sc, 'Value (unit)', spec=p)
```

Most maps need two or three layers. The four decisions that matter:

1. **Preset.** `published_linework` (near-white land, near-black hairline
   coastline, no frame, labelled graticule) over `global_points` (filled grey
   land, frame, no graticule) for a global point map. Filled land is a mid-grey
   mass that competes with the marks; drawn land costs almost no visual weight
   and leaves the colour ramp all of the contrast. **Frame and graticule are a
   pair** — mixing the halves is what makes degree labels pile up at the curved
   edges of a Robinson panel.
2. **Points or polygons**, decided by the unit of observation, not by taste. A
   choropleth of site averages silently encodes region area, which is not a
   variable in the analysis.
3. **Which layers to turn on** — maps.md §8 has the table.
4. **Colormap from the data, not from habit.** `pick_cmap` returns diverging
   centred on the reference value when the variable straddles it, sequential
   when it does not, and never a rainbow.

Region names belong to the text layer, added at assembly.

### Step 3c — Chart families that carry their own geometry

Two families defeat a generic styling pass, for the same reason a map does: the
thing that makes them work is structural, so a panel can pass every rule in
Step 3 and still be unreadable.

#### Region plots (quadrants)

Full method in **[references/quadrant.md](references/quadrant.md)**; code in
`assets/nature_quadrant.py`. The four rules that decide the panel:

1. **It is a classifier displayed over a scatter**, not a scatter with two
   lines on it. Test: delete the points — if the panel still says something, it
   is a region plot. If not, the lines are clutter and you want a plain scatter.
2. **Every dividing line carries a stated rule.** Definitional (`y = x`, zero,
   a standard) > model-derived (mixture crossing, *with* its ΔBIC) >
   distributional (median, *with* a sensitivity recount) > eyeballed, which is
   never acceptable. The rule and its number go in the caption.
3. **The background is the classifier evaluated on a grid**, so the fill and the
   statistics cannot disagree — they are one code path. This also removes the
   four-rectangle assumption: diagonals and curves compose for free.
4. **The legend is a thumbnail of the partition**, generated by that same
   classifier, not a column of swatches.

```python
from nature_quadrant import threshold, regions, region_background, divider, bubble_scatter

t = threshold(df.cost, "median", unit="USD kWh$^{-1}$")   # value + caption string
part = regions([("Viable, low cost",  lambda x, y: y >= x and x <= t.value),
                ("Viable, high cost", lambda x, y: y >= x)],
               default="Unviable")
region_background(ax, part, xlim, ylim)
divider(ax, x=t.value, diagonal=True, spec=p)   # grey median, accent break-even
bubble_scatter(ax, df.cost, df.price, size=df.flow, spec=p)
```

#### Chord diagrams

Code in `assets/nature_chord.R`. Kept in R because circlize solves the ribbon
and sector geometry and a hand-rolled version does not.

- **Readable at ~10–15 sectors, decorative above ~30.** Past that nobody can
  trace a ribbon end to end. Aggregate to the group level and draw the
  group-level matrix, or switch chart: Sankey if the flow is staged, heatmap
  matrix if the claim is really "which pairs are large".
- **Hide small ribbons by setting their alpha to zero, never by dropping their
  rows.** Dropping rows shrinks the sectors, so the arc lengths stop being the
  totals the caption claims.
- **Opacity carries magnitude** (on a sqrt scale, so mid-sized flows stay
  visible); **colour carries a category**, never a second continuous variable.
- **Grouping is opt-in** (`group=` a column, or `group_fun=` a function). Once
  on, you get group arcs, group labels, and a gap budget — **a small gap within
  a group, a large one between** — which is what turns a picket fence into
  readable blocks. Off by default, because a grouping invented by the plotting
  code is a claim about the data's structure.
- `cell.padding = c(0,0,0,0)` is mandatory when small sectors exist; the
  default padding is wider than a small sector and circlize drops it silently.
- Size labels in landed points, not in raw `cex`, and export **PDF**. A
  600-dpi PNG is a preview, not final artwork.
- Export through `cairo_pdf()`, never `pdf()` + extrafont: the extrafont path
  leaves Arial unembedded with broken widths, and viewers render the labels
  as garbage while the PNG preview still looks right.
- A chord has no axis and circlize draws no legend — export one separately.

### Step 3d — Add what the panel is missing

Every step so far removes something: chart types, ink, titles, spines, colours. That
bias is useful right up until it produces a technically compliant panel nobody wants
to read. This step runs the other direction, once, before export.

A figure has two failure modes, not one. **Cluttered** is the famous one. **Bare** is
the one a compliance checklist cannot see, because every individual rule passes. A
scatter with no reference line, no units and no n; a bar chart stripped of the value
labels that made it readable; a frameless map with hairline coastlines, no borders and
one grey point cloud — each violates nothing and tells the reader nothing.

#### First, the layers this chart family can turn on

Map panels: the table in **[references/maps.md](references/maps.md) §8** —
borders, coastline weight, frame, graticule and its labels, resolution, marginal
profile, inset. Region plots: marginals, the zoom inset, and direct labels on
the marks the claim points at ([quadrant.md](references/quadrant.md) §7–9). Any
panel: a reference line, a colour bar, a value label, a stated n.

#### Then read the panel cold

Look at the rendered PNG as if you had not made it, and answer four questions:

1. **Where am I?** On a map: could a reader name the region without the caption? On a
   plot: do the axis labels and ticks say what is being compared, without prose?
2. **What am I supposed to look at first?** If the answer is "the biggest blob" and
   the biggest blob is not the finding, the emphasis is wrong — see `style.md` §9.
3. **What is missing that I would have to ask for?** Units, n, a reference line, a
   colour bar, the identity of an outlier. Data-derived ones belong in the script.
4. **Would I stop on this panel while skimming?** Not "is it decorated" — decoration
   does not survive review. Does it look like it has something to say.

If a question fails, the fix is usually adding a layer, not removing one. Record what
was added and why, the same way rejected chart types get recorded in
`chart-type-chooser`.

**This does not license decoration.** Nothing here overrides the Non-negotiables
below: no 3D, no drop shadows, no gradient that encodes nothing, no colour spent on a
variable that is not in the analysis. The test for an added layer is whether it
answers one of the four questions — not whether it fills space.

### Step 4 — Keep the text layer out of the script

A journal figure has two layers, and they are produced by different tools at different
times:

| Layer | Contains | Made in | When |
|---|---|---|---|
| **Data layer** | marks, axes, ticks, tick labels, axis labels, colorbar | matplotlib | in the script |
| **Text layer** | panel letters, callouts, arrows, brackets, region names, "n = 412", "P < 0.001", schematic insets | Illustrator / PowerPoint | at assembly |

This is a division of labour, not a minimalism rule. Everything in the right-hand
column still gets added — just later, by the tool that can place it properly. Step 3d
above is where the script's own layers get *added*; this step only decides which
layers are not the script's job.

**Default to the data layer only.** The script should emit a clean, self-explanatory
panel, and leave the rest for assembly:

- **No `ax.set_title()`** — the caption is the title.
- **No explanatory `ax.text()` inside the plot area** unless the annotation is
  data-derived and must move when the data moves (a bar-top value, a fitted R²).
- **No arrows, brackets, or highlight boxes** in the script.
- **No inline notes** like "higher is better" or "our method".

Three reasons, in order of how much time they save:

1. **Text changes constantly; data does not.** Wording gets revised at every round of
   co-author comments and every reviewer response. If the text lives in the script,
   each wording tweak means re-running the analysis. If it lives in the assembly file,
   it is a click.
2. **The journal requires editable text anyway.** Overlay elements must remain
   independent vector objects. Text placed in Illustrator satisfies this by
   construction; text baked into a matplotlib PDF is one `fonttype` setting away from
   being unfixable.
3. **Positioning is a layout decision, not a plotting decision.** Where a callout goes
   depends on the assembled multi-panel figure, which does not exist yet when the
   script runs. Placing it in the script means guessing, then fighting `bbox_inches`.

**The simplicity test**: if a panel needs a sentence of explanation drawn on top of it
to be understood, the chart type is usually wrong. Fix the chart rather than captioning
it in place. Annotation should point at something, not explain it.

Note the limit of that test. It says a panel should not need *prose* to be understood.
It does not say a panel should be sparse: a missing reference line, colour bar, unit,
or map layer also makes a panel need explaining, and there the fix is to add the thing,
not to remove more.

**Legitimate exceptions** — annotations that are functions of the data and must
regenerate with it:

```python
ax.text(x, total + pad, f'${total/1000:.1f}k', ha='center', va='bottom', fontsize=6)
ax.text(0.05, 0.92, f'$R^2$ = {r2:.3f}', transform=ax.transAxes, fontsize=6)
ax.text(x, y, '***', ha='center', fontsize=6)   # significance, computed not typed
```

Panel letters sit on the boundary: bake them in if the panel grid is fixed, add them
at assembly if the layout is still moving. Adding them at assembly is safer.

### Step 5 — Export panels separately, plus a standalone legend

Do **not** try to assemble a complex non-rectangular main figure inside matplotlib.
Render each panel as its own file and assemble in a vector tool.

```python
from nature_style import save_all, export_legend

save_all('fig2_a_map', fig)          # -> pdf/, svg/, png/
export_legend(handles, labels, 'fig2_legend', ncol=3)
```

A standalone legend file can be placed anywhere during assembly — bottom row,
right column, inside whitespace — without re-running the analysis.

### Step 6 — Assemble in a vector tool

Illustrator (preferred) or PowerPoint (acceptable if everything stays editable).

1. Set the artboard to the exact final size: 88 mm or 180 mm wide.
2. Place the panel PDFs and align them on a grid.
3. Position the standalone legend where the layout wants it.
4. **Now add the text layer** — panel letters, callouts, arrows, brackets, group
   labels, sample sizes. This is the first moment the whole figure is visible, and
   therefore the first moment these placements can be decided rather than guessed.
5. Keep every added element as a live text or vector object. Never outline the type,
   never rasterise, never flatten.

Never assemble in Word or Photoshop.

### Step 7 — Run the submission audit

Go through the checklist in `references/workflow.md`. Report every violation with a
severity (CRITICAL / MAJOR / MINOR) and the exact fix.

---

## Non-negotiables (CRITICAL if violated)

| Rule | Why |
|---|---|
| Vector (PDF/EPS/AI) for charts, schematics, maps, line art | PNG/JPG rejected as final artwork |
| Text 5–12 pt **as landed on the page** (house target 9–10.5), Arial or Helvetica | The guide asks 5–7; this skill targets larger on purpose — see Step 0. Below 5 or above 12 is a real failure. Verify with `landed_report()`, not by reading the script |
| Figure width exactly 88 mm or 180 mm | Fixed column grid |
| `pdf.fonttype = 42` | Text must remain editable |
| RGB for original research | Colour-mode requirement |
| Raster components ≥ 300 dpi, never upsampled | Upsampling adds no information |
| No drop shadow, 3D rotation, bevel, or gradient that encodes nothing | Rasterises on export; reads as chartjunk |
| Overlays (arrows, scale bars, labels) on a raster base stay as separate vector objects | Explicit requirement for mixed figures |
| ≤ 50 MB per final figure file | Hard submission limit |
| Third-party imagery cleared for rights; no web-scraped images | Legal requirement |

## Integrity rules

- Never invent data to make a figure look better. Every mark traces to a data file.
- Regenerate figures from the **published source-data file**, not from intermediate
  results, so figure numbers can never drift from the text.
- Honest axis ranges. If a truncated axis is necessary, mark the break explicitly.
- Error bars must be labelled in the caption as SD, SE, or CI, with n stated.
- Say what is shown: if a panel shows medians rather than means, the caption says so.

## Output format

When this skill produces or audits a figure, report:

1. **Panel geometry** — for each panel: placed mm, drawn mm, draw scale, and the
   landed body/tick/letter sizes, with `landed_report` output for any panel that
   carries hard-coded font sizes
2. **Style block** — confirmed applied, with any deviations justified
3. **Colour assignment** — the semantic dictionary used
4. **Panel inventory** — each panel, its chart type, its export filename
4b. **Region plot / chord specifics (Step 3c)**, when either is present — for a
   region plot: the rule and value behind every dividing line, the class counts
   including the empty classes, and the sensitivity recount. For a chord: the
   number of sectors, the visibility cutoff and how many ribbons it hides, and
   confirmation that sector sizes are still the full totals
4c. **Addition pass (Step 3d)** — map layers turned on and why; what the cold read
   found; what was added in response, or an explicit "nothing needed"
5. **Audit** — spec table above, pass/fail per row
6. **Severity summary** — n CRITICAL, m MAJOR, k MINOR, top three fixes first
