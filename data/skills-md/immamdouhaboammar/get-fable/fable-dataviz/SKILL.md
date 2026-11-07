---
name: fable-dataviz
description: "Design and generate accessible, cohesive data visualizations, SVG charts, metric cards, and dashboard tiles with theme-adaptive styling and verified viewports. Use when creating SVG charts, rendering metrics plots, designing dashboard visuals, or visualizing performance trends — even if the user does not explicitly say \"fable-dataviz\" (e.g. \"make a chart of this data\", \"plot these benchmarks\", \"create an SVG graph\", \"visualize these metrics\"). Do NOT use for non-visual text-only data summaries or generic code edits."
version: 1.3.0
pack: system
inputs:
  - data_source
requires:
  - metric_specs
produces:
  - visualization_artifact
  - svg_chart
gates:
  - theme_contrast_valid
  - viewbox_defined
fallback: fable-execute
mutatesWorkspace: true
parallelSafe: true
neural_links:
  precursors:
    - fable-discover
  continuations:
    - fable-artifact
    - fable-run
    - fable-verify
  lateral_peers:
    - fable-artifact
  recovery: fable-recover
---

# Fable DataViz

Turn data into a visual claim that is easy to read **without changing what the data actually says**.

## Mission
A chart is an argument about magnitude, trend, distribution, relationship, uncertainty, or composition. The first job is to choose a visual encoding that matches that question. The second is to preserve statistical meaning. Styling comes after both.

A valid SVG with attractive colors can still be a bad visualization if it truncates axes deceptively, aggregates incompatible groups, hides missing data, implies causality from correlation, or invents precision the source does not support.

## Activate When
- a metric/trend/distribution/comparison/relationship needs visual explanation;
- benchmark/eval results need charts or stat graphics;
- a report/artifact needs an evidence-backed visual;
- raw data must be transformed into SVG/chart code or a visual specification.

## Do Not Activate When
- there is no actual data and the request would require inventing values;
- a plain table is more accurate/readable for a small lookup task;
- the core task is document structure rather than visual encoding (`fable-artifact`);
- the user requests an illustrative image rather than a data visualization.

## Question Classification
| Question | Useful first encoding | Typical misuse |
| --- | --- | --- |
| Compare categories | bar/dot plot | pie with many similar slices |
| Trend over ordered time | line/area with careful baseline | unordered category line chart |
| Distribution | histogram/box/violin/dot | average-only bar |
| Relationship | scatter/bubble with scale caveats | dual-axis correlation theater |
| Part-to-whole | stacked bar/100% bar; limited pie | sum components that are not one whole |
| Ranking | sorted bar/dot | alphabetic order hiding rank |
| Single KPI + context | stat + baseline/change | giant number without denominator/timeframe |
| Uncertainty | interval/band/error bars | precise point with hidden variance |

## Protocol
### Stage 1 — Establish data provenance and semantic contract
Record:
- source/dataset/version/time window;
- unit and denominator;
- category/time definitions;
- missing/null semantics;
- whether values are counts, rates, percentages, currency, estimates, or modeled outputs;
- uncertainty/precision available.

If source or metric meaning is ambiguous, stop and resolve it before rendering.

### Stage 2 — State the visual question
Write one sentence: `This chart should help the reader see ___`.

If there are multiple unrelated questions, create separate views rather than forcing one overloaded chart.

### Stage 3 — Validate transformations
Before plotting, explicitly define:
- filters;
- grouping/aggregation;
- normalization/denominator;
- sorting;
- date bucketing/time zone;
- handling of missing/outliers;
- derived metrics/calculations.

Check totals/ranges before and after transformation. Never silently drop records that change the claim.

### Stage 4 — Choose encoding and scales
Use position/length for precise comparisons where possible. Choose linear/log/percentage scales based on metric semantics.

Baseline rules:
- bar length usually needs meaningful zero because length encodes magnitude;
- line/scatter axes may use non-zero domains if clearly labeled and not exaggerating the story;
- log scales require positive values and explicit labeling;
- dual axes are high-risk and need strong justification.

### Stage 5 — Encode uncertainty and data quality
If estimates have intervals/variance/sample sizes, show or state them when material. Mark missing periods/categories rather than connecting them as if observed.

Do not show more decimal places than source precision justifies.

### Stage 6 — Design for reading and accessibility
Prioritize:
- descriptive title stating metric/context;
- direct labels where they reduce legend decoding;
- readable typography/spacing;
- contrast and non-color cues;
- accessible title/description for SVG;
- responsive `viewBox`/appropriate container behavior;
- units and source note.

Do not rely on red/green or hue alone for meaning.

### Stage 7 — Validate the rendered artifact
Check:
- chart renders without clipping/overlap;
- data coordinates match source values;
- axes/ticks/labels/legend are correct;
- small/large screens when responsive;
- light/dark theme if required;
- accessibility metadata;
- no transformation/render code silently changes ordering or values.

### Stage 8 — Run a deception audit
Ask:
- would a reasonable reader infer a larger/smaller effect than raw data supports?
- is the denominator/time window obvious?
- are missing values hidden?
- does annotation imply causality not established?
- are categories incomparable due to different bases?

Fix the visual claim, not only the pixels.

## Decision Rules
- Never invent data, labels, sample sizes, sources, or benchmark results.
- A percentage without denominator/base often needs contextualization before visualization.
- Avoid pie/donut when readers need precise comparison or categories are numerous.
- Do not downsample by simply dropping points when extrema/events matter; use a documented aggregation/sampling strategy.
- Missing values are not zero unless the domain explicitly defines them that way.
- Sort categories to support the question unless natural/order semantics require otherwise.
- Use zero baseline for bars by default; exceptions require an encoding where truncation is not misleading and must remain visible.
- Correlation chart/temporal coincidence does not justify causal annotation.
- If a chart cannot remain legible at target size, simplify/segment rather than shrink labels into illegibility.

## Invariants
- Every plotted mark maps to source/transformation logic.
- Units, denominator, and timeframe remain truthful.
- Missing/uncertain data is not silently converted into certainty.
- Scale choices do not intentionally exaggerate magnitude.
- Accessibility does not depend on color alone.
- Rendered output can be traced back to source data and transformation steps.

## Failure Taxonomy
### Wrong chart question
Encoding answers composition while reader needs precise comparison. Re-select chart by analytical question.

### Aggregation distortion
Grouping/normalization changes denominator or hides important subgroup behavior. Recompute and document transformation.

### Scale deception
Axis/domain makes modest changes look extreme. Restore appropriate baseline/domain and labels.

### Missing-data fiction
Null periods are plotted as zero/interpolated without justification. Mark gaps or document imputation.

### Overplotting/crowding
Marks/labels overlap and conceal distribution. Aggregate, facet, sample responsibly, or change encoding.

### Accessibility failure
Contrast/color-only meaning/text size prevents interpretation. Add non-color cues/direct labels/accessible metadata.

### Source uncertainty
Metric meaning or provenance is unclear. Stop rendering and resolve source contract.

## Anti-Patterns
- starting with "make it a donut" before understanding the question;
- truncating bar axes to dramatize change;
- dual axes used to manufacture correlation;
- treating missing values as zero;
- inventing sample data to make the chart look complete;
- downsampling away spikes without disclosure;
- 3D/perspective effects that distort area/length;
- rainbow palettes with no semantic reason;
- title like "Revenue" with no unit/timeframe;
- declaring a chart verified because SVG syntax parses.

## Visualization Packet
```text
Question / intended takeaway:
Source + version/timeframe:
Metric definition / unit / denominator:
Transformations:
Missing/outlier/uncertainty handling:
Encoding + scale rationale:
Accessibility choices:
Rendered validation:
Deception audit:
Source note:
```

## Completion Criteria
Visualization completes when:
- visual question and metric semantics are explicit;
- transformations are reproducible and totals/ranges checked;
- encoding/scale match the analytical task without distortion;
- missing/uncertain data is honest;
- artifact renders accessibly at target size/theme;
- source/data-to-mark traceability exists;
- no claim exceeds what the data supports.

## Progressive Resources
- Deep guide: `references/truthful-chart-selection-and-validation.md`
- Existing design system: `references/dataviz-design-system.md`
- Example: `examples/render-bar-chart.md`
