---
name: paper-figures-tables
description: Create, revise, and validate publication-ready academic paper figures and tables. Use for LaTeX tables, related-work comparison tables, result tables, notation/dataset/taxonomy tables, precise source-data-driven experiment plots from CSV/JSON/logs, generated conceptual figures such as system overviews/pipelines/architectures/threat models, captions, artifact specs, source-data traceability, and paper-ready PDF/SVG/PNG/LaTeX exports. Do not use for prose-only paper writing, self-review, reviewer response, rebuttal drafting, or external literature-management workflows.
---

# Paper Figures & Tables

Use this as the single entrypoint for paper artifacts: tables, precise data figures, generated conceptual figures, captions, and artifact QA. It combines public integrity defaults, optional house artifact style, data-visualization judgment, conceptual-figure planning, and experiment artifact checks.

## Priority Model

Always load `references/priority-model.md` first. Load only the task-specific references needed for the current artifact.

Authority order:

1. Core integrity constraints from the sibling `paper-policy` skill.
2. User-provided data, manuscript facts, approved evidence, and explicit instructions.
3. Verified venue requirements.
4. Writing handoff specs from `paper-writing`, when present.
5. Hard rules from all activated policy sets, including house rules only after explicit opt-in.
6. Enabled soft guidance, optional house artifact style, and precise-plot advice.

Do not let generic artifact advice override user facts, enabled policy rules, or route boundaries. Do not impose disabled house rules as public requirements.

## Task Routing

| Task | Load |
|---|---|
| Decide table vs figure | `artifact-routing.md`, `captions.md` |
| Related Work comparison table | `tables.md`, `captions.md`; add `dense-empirical-tables.md` for a load-bearing multi-axis matrix and `layered-capability-matrix.md` when 8+ dimensions form explicit semantic layers |
| Result table, findings index, sample ledger, taxonomy table, risk matrix | `tables.md`, `captions.md`, `quality-checks.md`; add `dense-empirical-tables.md` when hierarchy or density is high |
| Precise experiment/data plot from CSV/JSON/logs | `data-figures.md`, `data-profiling.md`, `chart-selection.md`, `visual-pitfalls.md`, `figure-contract.md`, `plot-patterns.md`, `captions.md`, `quality-checks.md` |
| Journal/venue-specific plot sizing or export | `journal-specs.md`, `visual-qa.md`, `publication-checklist.md`, then the relevant artifact reference |
| Conceptual figure, Figure 1, architecture, pipeline, threat model | `conceptual-figures.md`, `figure-contract.md`, `captions.md`, `quality-checks.md` |
| Statistical summary for artifact creation | `source-data-and-statistics.md`, then `tables.md` or `data-figures.md` |
| Caption-only task | `captions.md` plus the relevant artifact reference |
| Artifact QA or cleanup | `quality-checks.md`, then the relevant artifact reference |

For final figures/tables, source-data artifacts, Related Work tables, or any
artifact feeding submission readiness, also load `policy-integration.md`.

## Artifact Constraints And Defaults

- Use source data or user-provided values. Do not invent numbers, baselines, methods, p-values, error bars, or visual trends.
- Every artifact must support one explicit paper claim or comparison.
- Every data-driven artifact must identify its source file or state that source data is missing.
- Use `booktabs` as an optional clean default; require it only when `TABLE.BOOKTABS_FINAL` is active or the venue specifies it.
- Align tables to the target width without unnecessary scaling. Require the house `\resizebox` pattern only when `TABLE.FINAL_TARGET_WIDTH` or its enabled soft companion calls for it.
- Tables should be compact argumentative artifacts, not storage for every available dimension. Prefer single-column tables after pruning to the few dimensions that support the claim; use `table*` only when the argument would become misleading or unreadable in one column.
- Use an axis-based Related Work comparison table when it improves the argument. Require the table and house dimension/placement defaults only when their strict rules are enabled.
- Precise experiment data figures must be source-data-driven Python/Matplotlib/Seaborn plots. Do not use image generation for numeric plots.
- Choose the renderer for non-data conceptual figures from topology, editability, venue constraints, and available tools. Use a generative image model by default only when `FIG.CONCEPT_HOUSE_STYLE` is active.
- Apply the one-or-two conceptual-figure preference only when `FIG.CONCEPT_COUNT` is enabled.
- Apply the pure-white, no-texture conceptual style only when `FIG.CONCEPT_HOUSE_STYLE` is active.
- When `FIG.CONCEPT_TYPOGRAPHY` is active, require the image model itself to render Times New Roman for every non-mathematical label and a dedicated manuscript- or venue-compatible math font for variables, symbols, and equations. Regenerate or stop when those font roles are wrong or unverifiable; never repair them with a later overlay.
- When `FIG.CONCEPT_MODEL_NATIVE_OUTPUT` is active, keep all visible text, mathematics, arrows, icons, components, and boundaries in the accepted model output. Corrections must use another model generation or model-editing pass; allow only non-semantic crop, resize, compression, color-profile, or format-packaging operations afterward.
- Put interpretation in captions. Forbid in-figure titles only when `FIG.NO_IN_FIGURE_TITLE` is active or the venue requires that style.
- Use a 3x source canvas with visible paper-figure text near or above 24pt by
  default. Smaller source text is an allowed soft adaptation only when the
  rendered artifact remains comfortably readable at the actual LaTeX column or
  text width. Final-width visual QA is mandatory for final figures.
- Prefer vector exports (`.pdf` and/or `.svg`) for precise plots and LaTeX inclusion. PNG is acceptable for review packets and generated conceptual figures.
- Keep one generated plot script per semantic figure unless the task explicitly asks for a multi-panel artifact.
- Prefer tables for exact comparisons and figures for trend shape, flow, geometry, and distribution, adapting this heuristic to the enabled policy sets.
- Writing prose belongs to `paper-writing`; this skill may polish captions and short artifact callouts but should not draft full paper sections.

## Output Contracts

For LaTeX tables:

1. Return package or macro requirements when needed.
2. Return compile-ready LaTeX.
3. Include `\caption{}` and `\label{}`.
4. Avoid up/down arrows in headers only when `TABLE.NO_DIRECTION_ARROWS` is enabled; otherwise follow the venue and manuscript notation.
5. Define markers such as `\cmark`, `\pmark`, and `\xmark` only when needed for readability, preferably in a short caption phrase rather than a separate note.
6. Select the compact default, dense empirical profile, or explicit layered capability matrix profile, then render at the actual target width before finalizing spacing, rules, or font size.

For data figures:

1. Create or update a compact `figure_spec.yaml` and the shared artifact record
   in `compliance-evidence.yaml`.
2. Profile source data before selecting the chart when raw tabular data is available.
3. Recommend the chart type from the paper claim and data shape; actively warn when the requested chart hides distribution, uncertainty, or sample size.
4. Save or describe outputs: `figure.pdf`, optional `figure.svg`, optional `figure.png`, script, source data path, and caption.
5. Validate source fonts, render at final paper width, run visual QA, and record
   the human evidence with the artifact ID.

For conceptual figures:

1. Read enough manuscript context before designing.
2. Produce a `brief.md`, `spec.json` or `figure_spec.yaml`, generation prompt, and caption draft.
3. Use the renderer selected by active policy and artifact needs; a generative image model is an opt-in house default, not a universal requirement.
4. Add `generated_conceptual_figure` to context features and artifact types whenever an image model produces the final conceptual artifact.
5. When image generation is selected for a topology-sensitive overview, create or update a precise editable `structure.svg` wireframe and use it only as a pre-generation structural reference.
6. Use Graphviz, Mermaid, TikZ, or final SVG only for an explicitly non-generative conceptual artifact; never use them to repair or redraw an accepted generated figure when the model-native rule is active.
7. Preserve the manuscript's structure; do not invent components not supported by the paper.
8. Inspect typography and semantics in the accepted model output. If they cannot be verified, regenerate or stop rather than adding post-generation content.

## Reference Map

- `references/priority-model.md`: source priority and conflict resolution.
- `references/policy-integration.md`: context resolution, artifact evidence, adaptive source fonts, final-width QA, and compliance handoff.
- `references/artifact-routing.md`: table vs figure selection.
- `references/tables.md`: LaTeX table style and resizebox rule.
- `references/dense-empirical-tables.md`: optional reference-paper-informed profile for grouped headers, compact empirical matrices, findings-at-a-glance tables, and sample ledgers.
- `references/layered-capability-matrix.md`: explicit profile for wide Related Work capability matrices with semantic column layers, conservative family-row evidence, and grounded coverage-delta highlights.
- `references/data-figures.md`: reproducible data-driven plotting workflow.
- `references/data-profiling.md`, `references/chart-selection.md`, `references/visual-pitfalls.md`: data profiling, chart selection, and visual-risk guidance.
- `references/journal-specs.md`, `references/visual-qa.md`, `references/publication-checklist.md`: venue sizing, final-size rendering, and visual QA.
- `references/conceptual-figures.md`: generated conceptual figure planning and rendering.
- `references/captions.md`: self-contained captions and artifact callouts.
- `references/source-data-and-statistics.md`: source data, statistical summaries, and placeholders.
- `references/quality-checks.md`: artifact QA checklist.
- `references/figure-contract.md`, `references/plot-patterns.md`, `references/plot-recipes.md`, `references/data-figure-style-source.md`: detailed plotting resources.

## Script Map

- `scripts/profile_data.py`: profile tabular data before chart selection.
- `scripts/paperfig_style.py`: reusable helper for paper plots and semantic color roles.
- `scripts/setup_style.py`, `scripts/export_figure.py`, `scripts/layout_tools.py`, `scripts/visual_qa.py`, `scripts/check_figure.py`: final-size styling, export, layout, preview QA, and file audit for precise data figures.
