---
name: academic-figure-architecture-extractor
description: Extract semantic structure and transferable style grammar from academic figures, PDFs, and paper or figure URLs for analysis, redraws, or reference-conditioned generation. Do not use it for paper-text-only figure planning.
metadata:
  version: "1.3.0"
---

# Academic Figure Architecture Extractor

Turn supplied figures into grounded structure and reference-style evidence. Keep
scientific content separate from transferable visual grammar.

Load only when relevant:

- missing evidence → `references/missing-info-policy.md`
- local PDF helper → `scripts/extract_pdf_figures.py`

## Scope and inputs

Accept one or more local images, PDFs, public paper/figure URLs, or an existing
render that needs revision. Prefer the original figure image over a screenshot when
both exist. PDF extraction finds embedded images or rasterized pages; it is not an
architecture detector, and figure classification remains evidence-based judgment.

For an article URL, inspect the page with an available web or browser tool, locate
the requested figure and caption, and resolve its direct image or PDF source. Do not
classify a paper URL as a repository. If a renderer will need the reference, retain
or download it to an absolute local path without overwriting user files.

## Obtain candidates

- **Local image:** inspect it with an available image-viewing tool at original detail.
- **Remote figure:** open it, preserve its source URL and caption, then inspect the
  localized image when possible.
- **PDF:** use a PDF-capable reader for pages and captions. To extract candidates,
  run the bundled helper from the skill repository when available:

```bash
python3 academic-figure-architecture-extractor/scripts/extract_pdf_figures.py \
  /absolute/path/to/paper.pdf -o /absolute/path/to/extraction-directory
```

Useful optional flags are `--backend auto|pdfimages|pymupdf`, `--pages 1-3|all`,
`--dpi 150`, `--min-side 300`, and `--min-pixels 90000`. Read the generated
`extract-report.json`. If extraction tools are unavailable, use directly viewable
pages or ask for an exported figure; never invent a local path.

Record for every candidate: source URL/path, page or figure number, caption, pixel
size, local absolute path when available, and keep/drop/uncertain with a reason.

## Analyze semantic structure

For each kept figure, identify only what the image and caption support:

- components and their core/auxiliary roles;
- groups, hierarchy, reading direction, and dominant focal point;
- directed edges, branches, loops, annotations, and legend semantics;
- figure type and uncertain or illegible content.

Do not import the reference's labels, claims, metrics, or topology into a new method
figure. Those are reusable only when the user explicitly requests a faithful redraw.

## Extract the style grammar

Describe observable design decisions rather than reducing the figure to a palette
name. Capture:

```text
composition: storyboard|pipeline|loop|modular collage|nested mechanism|other
regions: panel geometry, grouping, asymmetry, whitespace and density
marks: vector, hand-drawn, editorial illustration, geometric, line-art, mixed
strokes: weight, curvature, joins, arrow and connector language
fills: flat/tinted/wash/white, border treatment, shadow and texture
color_roles: background, regions, primary structure, accents, exceptions
typography: family character, hierarchy, placement and approximate density
motifs: agents, scientific objects, tokens, icons, mini-plots, callouts
emphasis: focal scale, contrast, saturation and annotation strategy
avoid: visual traits absent from or conflicting with the reference
```

Do not force `classic` versus `pastel`, Nature Blue, white-fill boxes, or a venue
stereotype. A reference may define a third style family such as a hand-drawn
editorial scientific infographic. Treat exact hex values as observations, not as a
substitute for composition and hierarchy.

## ReferenceAnalysis v1 handoff

Emit one JSON-compatible object per kept figure:

```text
schema: academic-figure/ReferenceAnalysis@1
reference_id
source: {url_or_absolute_path, local_absolute_path, page_or_figure, caption, size}
semantic_structure: {components[], groups[], edges[], reading_order, uncertainties[]}
style_grammar: {composition, regions, marks, strokes, fills, color_roles,
                typography, motifs, emphasis, avoid[]}
transfer_policy: {reuse[], do_not_copy[]}
confidence: high|partial|sparse
```

Downstream FigurePlan v1 carries `reference_id` and `style_grammar`; FigureSpec v1
carries the reference's absolute local path whenever it can be materialized. If
the asset exists only in the current conversation, it may use the workflow's
transient recent-conversation descriptor for the immediate render, but should be
materialized before a reproducible rerun. A capable backend conditions on the
image itself. A later RenderAudit v1 compares observable style fidelity without
requiring content imitation.

Stop after the inventory if that is all the user requested. Otherwise stop when
ReferenceAnalysis v1 is complete or when a missing source image blocks honest
analysis.
