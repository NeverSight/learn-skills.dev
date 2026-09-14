---
name: build-scientific-visualizations
description: Use when creating, redesigning, planning, or visually auditing scientific figures, flowcharts, method schematics or model-architecture diagrams, graphical abstracts, dense many-panel compound figures, domain-specific omics visualizations, and conference or journal figure sets, including Nature-style main, Extended Data, and Supplementary figures. Independently owns visual construction, figure legends, source-data preparation, and visual QA; does not rewrite the scientific analysis or manuscript claims.
---

# Build Scientific Visualizations

Turn scientific evidence into a legible visual argument. Choose one mode, lock the
claim and source-data boundary, prove the whole-page hierarchy, then build from a
canonical scene and inspect the rendered artifact at final size.

This directory is independently complete. No other skill is required: read the user's
scientific sources and current venue or funding-call instructions directly, build the
visual and its legend, and deliver source data, editable source and checked exports.
Another writing or workflow skill may supply that context, but is an optional collaborator.
Do not let absent companion skills prevent source-grounded preparation or rendering.

## Select one mode

| Mode | Use it for | Mode reference |
|---|---|---|
| `layout-sketch` | A disposable reading-order or panel-layout draft when structure is unresolved | `references/mode-router.md` |
| `flowchart` | One scientific flowchart, mechanism workflow, method schematic, or model architecture | `components/flowchart/guide.md` |
| `compound-figure` | One complete figure combining schematic, data, image, and text panels | `components/compound-figure/guide.md` |
| `conference-figure-set` | A coordinated compact set for a conference paper, such as motivation, framework, and results figures | `references/mode-router.md` |
| `journal-figure-set` | Main, Extended Data, and Supplementary figures with shared semantics and exact geometry | `components/journal-figure-set/guide.md` |

Do not select a mode by visual taste. Select it from the requested deliverable. A
layout sketch is never a final figure. A flowchart cannot replace measured evidence,
and a journal figure set is not merely one compound figure repeated many times.

## Resolve the installed skill before using tools

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`. Every runtime resource
is below that directory; never resolve through the package parent. For `layout-sketch`,
read only `references/mode-router.md` and preserve the evidence boundary without loading
final-render requirements. For every other mode, read the selected component guide and
the relevant material under `shared/figure-core/`; load layout, rendering, and QA
references only when that mode needs a final artifact.

For every schema-1.2 final artifact, read the directly routed
[page blueprint contract](references/page-blueprint-contract.md). Read the
[domain visualization selection matrix](references/domain-visualization-selection.md)
when choosing data displays or scientific glyphs. Read the
[source-data contract](references/source-data-contract.md) whenever the figure contains
data, images, structures, repository objects, or a reviewer-facing delivery.

For Nature-family flowcharts and compound figures, read the relevant cases in
[panel design lessons](references/nature-panel-design-lessons.md) when deciding how to
connect method transformations, tissue/ROI context, experimental timing or cluster
summaries with measured evidence. These cases guide design without fixing a template.

For many-panel or visually crowded figures, read
[dense compound design](references/dense-compound-design.md). Plan page, evidence
groups and internal views together; budget actual label/image space and retain all
requested scientific roles before considering a justified figure split.
For input-level recipes, select only the relevant reference:
[spatial and single-cell](references/recipes-spatial-single-cell.md),
[proteomics, metabolomics and glycobiology](references/recipes-molecular-omics.md), or
[genomic, structural and clinical views](references/recipes-genomic-structural-clinical.md).
The [runnable 18-panel synthetic example](examples/multimodal-18-panel/README.md)
demonstrates unequal allocations, nested ROI context, full molecular labels, measured
tables, explicit missingness and paired-unit uncertainty without another installed skill.

For a conference method schematic or `conference-figure-set`, read
[conference figure design](references/conference-figure-design.md) for source-grounded
method contrasts, dependency-versus-training semantics and manuscript insertion QA.

For every new or redesigned flowchart, architecture, motivation, method, mechanism or
other scientific schematic, use **GPT Image 2.5 concept generation, then native editable
PPTX reconstruction** by default. First inspect relevant excellent examples and borrow
their composition and visual reasoning, not their artwork or scientific claims.
This includes schematic panels inside compound,
conference and journal figure sets; no separate image-first or PPTX request is needed.
Read [image concept to editable vector](references/image-concept-to-vector.md) for the
required sequence, model-identity reporting and scoped exceptions. Data plots
and measured images remain source-derived. The
[design template library](references/design-template-library.md) provides inspected
paper precedents and original editable examples. This route separates visual concept
generation from source-correct native reconstruction; it does not make a bitmap editable.

For Nature-inspired or top-CS diagram styling and selectable colour schemes, read
[diagram style profiles](references/diagram-style-profiles.md). It defines two visual
grammars, six palettes and new-project selection; style never changes scientific content.

When no project contract exists, initialize one with the shared script. Its canonical
records are `figure_spec.json`, `content_ledger.json`, `asset_manifest.json`,
`venue_contract.json`, `layout_blueprint.json`, and `source_data_manifest.json`, plus
`flowchart_spec.json` when applicable. Run scripts by their resolved package paths,
not by assuming the user's working directory.

## Build the evidence contract first

Read the manuscript passage, caption, plotting code, data outputs, source images, and
prior figure that establish the visual. For every panel or stage, record:

- its scientific question, claim, and exact source anchor;
- required objects, comparisons, labels, controls, and units;
- whether each element is observed, predicted, prospective, schematic, or decorative;
- the prohibited implication and the control that would distinguish it;
- the independent unit, exclusions, and dropped-row count behind a quantitative plot.

Give every data-bearing panel a complete source-data record. A purely schematic panel
may use `not_applicable` only with a reason. Controlled data use a stable pointer,
conditions, and request route; never copy the restricted object into a delivery tree.
Bind every claim-supporting processed asset to non-empty `source_dataset_ids` in the
asset manifest. An asset's distribution label cannot relax its source datasets' access
class.

If two interpretations change a claim, comparison, or arrow direction, surface the
conflict before drawing. Do not use a pleasing composition to decide scientific
content. Illustrative numbers and stand-in images must be labelled as such.

A partial brief is not a reason to collapse the requested page into one generic starter
panel. If the user explicitly names evidence states, panel roles, paths, or display
families, carry those named items into the ledger, semantic graph, and page blueprint as
unresolved placeholders. Mark absent assay identities, values, directions, effects, and
source anchors as unresolved; never fill them by inference. A useful layout proof may be
built from these bounded placeholders, but detailed claim-bearing rendering remains
`not_run` until the sources exist.

## Prove the page before detailed drawing

State one complete-page question, narrative job, and decision unlocked. Choose the
visual anchor from evidential importance and legibility. Group panels by scientific
transition, assign relative area and shared encodings, and record the reading path in
`layout_blueprint.json` before placing detailed scientific assets.

Run `run_workflow.py <project> --phase layout` to validate the records and render a
placeholder-only whole-page proof. Inspect that proof at final physical width. Record
all seven layout checks as `PASS` in `qa/layout_review.json` only after hierarchy,
whitespace, text/image allowance, shared encodings, mechanical-grid risk, and semantic
coverage are satisfactory. The layout phase also records resolved page geometry in
`qa/layout_proof.json`. Any changed blueprint revision, panel order, composite size, or
placement box invalidates the review. Do not proceed to claim-bearing drawing while the
review is `REVISE`.

Equal panel sizes are allowed when the scientific comparison makes them appropriate.
For four or more equal panels, record `uniform_size_rationale`; otherwise treat the
validator's mechanical-grid warning as a required design review.

## Lock final-size geometry and semantics

Read the target venue's current official instructions when width, type size, raster
policy, file format, or generated-image policy matters. Put the exact journal, article
type, submission stage, authority URL, and checked date in `venue_contract.json`.
Bundled profiles are dated engineering snapshots, not current venue authority. Legacy
aliases remain readable but cannot pass a final journal-submission gate.
Caption-dependent final-artwork profiles require a project-relative caption file before
final validation; fixed and resolved caption-band height limits apply to the composite
page, not only to a separate PDF-checking command.

Author at the final insertion width. Define one registry for notation, abbreviations,
units, category colours, markers, line styles, hatches, panel letters, and arrow roles.
For charts and diagrams, colour cannot carry category identity alone; use marker, line
style, hatch, shape, or direct labels as a second channel. For channel-based measurement
images, use a local channel key, direct labels, or separate channel views instead of
adding synthetic marks to the evidence. Do not repair a wrong page size with
document-level rescaling or `bbox_inches="tight"`.

## Render from one canonical scene

For the shared renderer, keep visible copy, coordinates, dimensions, colours, and asset
placement only in `figure_spec.json`. For the native PPTX route, use one authoritative
presentation object scene and validate that export separately. The default schematic
route delivers that editable PPTX plus the vector exports needed by the manuscript;
it does not turn measured panels into generated illustrations. Keep scientific hierarchy
in the blueprint, source coverage in the
source-data manifest, and method meaning in `flowchart_spec.json`. Quantitative plots
must be generated from their declared source data. Count every excluded row and make
the total reconcile with the input. Use native vector primitives where possible and
preserve editable source.

For `conference-figure-set`, define the narrative job of every figure before fixing
the count. A gap or motivation figure, a framework figure, and a results figure are a
useful pattern only when each has distinct evidence and the current venue permits the
chosen formats. Verify rendered font size at the actual manuscript insertion width.

For generated or modified conceptual assets, verify the exact venue and publisher
policy first. Never generate or alter a measurement, specimen, molecular structure,
microscopy field, or other claim-bearing evidence.

## Refine complete schematic drafts

After the first source-faithful render, apply
[rendered schematic refinement](references/visual-refinement.md) to each diagram or
schematic panel, including those inside conference and journal figure sets. It uses
three focused passes by default: whole composition, individual scientific graphics,
then final-size harmonization. Preserve versions, compare actual renders, keep the
better result and stop early when further changes add no value. This is authoring work,
not another schema gate; measured evidence remains unchanged.

## Validate, inspect, and deliver

Run `run_workflow.py <project> --phase final` only after layout review passes. It runs
a final-readiness check before detailed rendering, then repeats strict final validation
after composition before QA. A standalone `validate_figure_project.py --stage final`
requires declared output files to exist. Use the PDF geometry validator with the venue
contract or exact dated profile. A passing schema does not establish visual quality.
Inspect the PDF or SVG at its real aspect ratio and final physical width for:

- claim fidelity and evidence-versus-schematic boundaries;
- clipping, collisions, arrow attachment, alignment, and reading order;
- axes, legends, uncertainty, scale bars, units, condition labels, and crop context;
- embedded fonts, vector retention, grayscale, and colour-vision-deficiency decoding;
- agreement among panel letters, captions, manuscript references, and source data.

Preserve the last accepted version. Deliver the formats required by the selected mode
and user brief; the default schematic route includes native editable PPTX even when
no format was named. Respect an explicit narrower deliverable request. Include editable
source, the content contract, audience-safe source data, and a concise QA note.
Before reviewer or public packaging, declare each authorized rendered
file in `source_data_manifest.json.delivery_outputs`; never assume the author composite
is safe merely because its input assets are excluded. Packaging includes only declared
source files and rendered outputs for the requested audience and excludes controlled raw
objects and private locators. A mixed-access external package accepts only an explicitly
source-bound quantitative PDF or SVG; it excludes the full composite and layout proof.
The packager reruns strict final validation and fresh visual QA against the current files;
it does not trust a previously saved PASS report after any output or contract mutation.
Exclude prompts, agent metadata,
approval records, private workflow state, and internal provenance artifacts from
reviewer-facing or public material.

## Boundary with the other public skills

This skill owns visual construction, figure legends and visual QA. Other skills may
request its modes or use its exported artifacts; none is a mandatory dependency.
Obtain experimental definitions and claim scope from the user's source material and
project authority. Preserve them while plotting. Manuscript-wide rewriting, new
scientific analyses and external submission remain outside this visual task.
