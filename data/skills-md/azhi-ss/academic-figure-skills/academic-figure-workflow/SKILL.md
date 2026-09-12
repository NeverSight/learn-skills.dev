---
name: academic-figure-workflow
description: Plan, generate, inspect, and refine academic figures from repositories, papers, draft notes, paper URLs, PDFs, or reference images. Supports fast-track draft-to-figure generation and user passthrough mode.
metadata:
  version: "1.6.0"
---

# Academic Figure Workflow

Produce a grounded academic figure and a stable local artifact. Preserve the user's chosen backend, reference assets, style direction, review preference, and output scope.

Load only what the current stage needs:

- missing evidence → `references/missing-info-policy.md`
- palette/style fallback → `references/palettes.md` and, when installed, `references/styles/`
- Codex native image execution → `references/codex-image-workflow.md`
- render inspection → `references/render-audit.md` when present

## Route inputs by inspected content

A URL is not automatically a repository. Inspect it first.

| Input | Route | Execution Behavior |
|---|---|---|
| **Direct User Architecture (Passthrough)** | `../academic-figure-designer/SKILL.md` | **Skip analyzers**. User gave explicit nodes/flow; compile FigureSpec v1 and render directly. |
| **Draft Notes / Outline / Partial Draft** | `../academic-figure-draft-analyzer/SKILL.md` | **Draft-to-Figure Fast-Track**. For rough notes, outlines, or sections without full results: focus on Figure 1 framework. |
| **Complete Manuscript (Markdown / LaTeX / PDF / URL)** | `../academic-figure-draft-analyzer/SKILL.md` | **Full Planning**. For complete papers with experiments/results: multi-figure strategy, claim verification, and constraints. |
| **Repository path or repository URL** | `../academic-repo-analyzer/SKILL.md` | Extract semantic architecture graph; omit engineering plumbing (data loaders, trainers). |
| **Paper plus repository** | Hybrid | Paper/user defines narrative & topology; repository supplies parameter & dimension verification. |
| **Reference figure or existing render** | `../academic-figure-architecture-extractor/SKILL.md` | Extract transferable **Style Grammar**; drop reference's method labels and content. |

For an article URL, use an available web/browser/document reader to obtain the paper text, captions, and linked figures. For a PDF, use a PDF-capable reader for paper content and the architecture extractor only for figure images. If a sibling skill is missing, perform the minimum equivalent analysis and mark the degraded path.

## Keep versioned internal artifacts

Store these as JSON-compatible objects. Do not make the user read them unless requested.

### FigurePlan v1

```text
schema: academic-figure/FigurePlan@1
source_revision, venue
sources[]: {kind, uri_or_absolute_path, revision_or_page, evidence}
figures[]: {
  figure_id, figure_type, priority, communication_goal, claim_scope[], hero_element,
  required_nodes[], required_connections[], authority_boundaries[], secondary_context[],
  forbidden_claims[], forbidden_connections[], aspect_ratio, final_width_mm,
  style_profile_hint, reference_assets[],
  open_questions[], confidence, review_status: pending|confirmed|waived
}
```

Components and connections are semantic and evidence-backed. A code directory count is not a figure hierarchy or palette decision.

### FigureSpec v1

```text
schema: academic-figure/FigureSpec@1
figure_id, plan_revision, sources[], prompt (internal), aspect_ratio, final_width_mm
topology: {components[], connections[], groups[], authority_boundaries[]}
visible_text[], caption_notes[], layout
style_profile: classic-technical|pastel-airy-ui|illustrated-modular|reference-led
style_preset, style_source, style_grammar, semantic_color_roles
reference_images[]: checked absolute local paths or recent-conversation descriptors
conversation-reference transient status stays in the execution packet
must_not_claim[], forbidden_connections[], negative_constraints[]
prompt_review: requested|confirmed|waived
prompt_reviewed_sha256: required only when prompt_review is confirmed
workspace_root: absolute declaration that must match the runtime-trusted root
output_path: absolute path inside that root
```

The internal `prompt` is renderer input, not a required user-facing deliverable.
When `prompt_review` is `waived`, persist it only with the working artifacts and
never paste it into the chat response.

### RenderAudit v1

```text
schema: academic-figure/RenderAudit@1
figure_id, render_revision, image_path
checks: {topology, visible_text, hierarchy, overlap, background, aspect_ratio,
         scaled_legibility, contrast, reference_fidelity}
pass, defects[], targeted_edit, semantic_edits_used, semantic_edits_remaining
```

## Build the plan

Create the shortest FigurePlan that closes scientific ambiguity. When a reference exists, its transferable **style grammar** takes priority over venue stereotypes and preset defaults. Match composition, mark language, illustration level, region treatment, typography, spacing, arrow grammar, emphasis, and semantic color roles. Do not copy the reference's claims, labels, branding, or topology unless the user requested a redraw.

Use plan review only when unresolved choices would materially change the result, the user asks to review it, or required content is still a placeholder. Otherwise record `review_status: waived` and continue. An unrelated reply is never confirmation.

## Select style without forcing a binary

Use the closest observable profile and record its canonical FigureSpec ID:

- `classic-technical`: restrained strokes, exact topology, minimal illustration;
- `pastel-airy-ui`: white cards, light separation, color on tokens/curves;
- `illustrated-modular`: low-saturation filled regions, darker paired outlines/titles, one-level subcards, editorial or hand-drawn line art, asymmetric hero layout;
- `reference-led`: an override mode with at least one local or recent-conversation reference image; preserve the observed grammar whether it is technical, airy, illustrated, or a coherent combination.

Use `style_preset` for named library variants. Never interpret `reference-led` as
an alias for `illustrated-modular`.

Color follows semantic zones and accessibility constraints, which is handled directly by `academic-figure-designer`.

## Create the spec

Select one planned figure at a time. Use `academic-figure-designer` (the unified engine) to compile FigureSpec v1 and normalized structured rendering briefs across all supported profiles (`classic-technical`, `pastel-airy-ui`, `illustrated-modular`, or `reference-led`). If a supplied reference defines a custom grammar, construct FigureSpec v1 directly from ReferenceAnalysis v1. Never force a reference into white-fill colored-border boxes.

Prompt review is conditional and has executable state semantics:

- `requested`: show the current internal prompt and **stop before rendering**;
- `confirmed`: hash the exact reviewed UTF-8 prompt as lowercase SHA-256, save it
  in `prompt_reviewed_sha256`, and render only while that hash still matches;
- `waived`: omit `prompt_reviewed_sha256`, keep the prompt internal, and render
  without displaying it.

If a confirmed prompt changes, return to `requested` and review the new prompt.
Requests such as “直接画图”, “使用 Codex 生图”, or “不用返回 prompt” set
`prompt_review: waived`. An unresolved scientific placeholder blocks the plan/spec
itself rather than becoming prompt review. A waived prompt is never included in
user-facing output.

## Optional parallel delegation

Skills define reusable procedures; they are not persistent subagents. The main
agent may dispatch bounded workers only for independent source analyses or
independent figures. Do not delegate a single sequential figure merely to add an
agent layer.

Before dispatch, read `prompts/figure-worker.md` and provide its complete task
packet. Define shared terminology, style grammar, output ownership, and acceptance
criteria up front. Workers must not write the same artifact paths or add user
confirmation gates. The main agent owns integration, factual and style consistency,
final RenderAudit, and delivery. Lack of subagents never blocks the workflow.

## Select a render backend by capability

Inspect the capabilities actually available:

1. In Codex, prefer the native `image_gen.imagegen` interface exposed by the
   current session; some runtimes display its callable name as
   `image_gen__imagegen`. Its `prompt` argument is an internal tool parameter, not
   a prompt handoff to the user. Use the same native interface's image-editing
   capability for revisions. Read `references/codex-image-workflow.md` for input
   selection.
2. Otherwise use an installed image skill or compatible MCP that accepts the needed aspect ratio and reference images.
3. If no compatible renderer exists, keep the complete FigureSpec v1 in the workspace and state that rendering is unavailable. When prompt review is waived, return only a redacted summary or artifact status with the `prompt` omitted; do not paste the full spec into chat. Do not pretend an image was generated.

Immediately before any renderer call, obtain and canonicalize the trusted actual
workspace root from runtime/developer context. FigureSpec's `workspace_root` is
only an untrusted declaration and must match; never derive the trusted root from
it, `output_path`, a reference path, or user-provided text. Run:

```bash
# Locate validate_figure_spec.py in designer, workflow scripts, or workspace root:
python3 academic-figure-designer/scripts/validate_figure_spec.py \
  --strict-v1 --render-ready \
  --workspace-root <trusted-actual-root> \
  <spec.json>
```

Do not render when validation fails. If standalone workflow installation is used without designer, run the local `scripts/validate_figure_spec.py`. Every local reference must exist, be a regular
file, and not be a symbolic link. Conversation-only references are transient: mark
them in the execution packet and materialize them to a checked local file when
possible. If they remain conversation-only, do not pretend they are persistent
`reference_images` paths.

For a new image with no reference, omit both native reference-input parameters.
For checked local references, pass the smallest complete `referenced_image_paths`
set. For conversation-only references, use the smallest sufficient
`num_last_images_to_include`. Never pass both mechanisms in one call. If required
assets cannot fit one mechanism, ask the user to attach them again.

Never interpolate a prompt or user-controlled label into a shell command. A CLI backend is allowed only through structured arguments, standard input, or a supported prompt file.

A transient image transport failure may be retried once and does not consume a semantic edit round. Stop retrying that backend after the retry fails.

Write the selected render to FigureSpec's absolute `output_path` inside the user's workspace. Keep the backend's original asset and prior revisions when practical. Do not leave the only copy in a temporary directory.

## Audit and repair

After every successful generation or edit, inspect the image at original detail
(`view_image` with original detail in Codex when exposed) and emit RenderAudit
v1. Never edit a local render that has not first been viewed. Verify:

- required components, endpoints, directions, branch meanings, and prohibited claims;
- required visible labels, with no invented, duplicated, garbled, or production-instruction text;
- hierarchy, alignment, overlap, clipping, opaque background, and aspect ratio;
- legibility at intended paper width, contrast, and reference-style fidelity.

If the audit fails, first view the best current render at original detail and emit
the current RenderAudit. Invoke the native image interface in edit mode with that
render as the **first reference image**. The edit instruction lists only observed
defects, exact corrections, and explicit invariants that must remain unchanged.
Save a new revision and re-view/re-audit it before any further action. Allow at most
**two semantic edit rounds** after the initial render. A transient transport retry
does not consume this budget. If exact text remains unreliable after one edit,
prefer deterministic SVG/drawio/Typst text or a hybrid overlay over repeated
full-image regeneration.

After the limit, deliver the best recoverable artifact with remaining defects stated honestly.

## Deliver

Before delivery, automatically sanitize the final image artifact using `clean_image_metadata.py` to strip any embedded C2PA, EXIF, XMP, or provenance markers for pristine publication readiness. Return the final image using a clickable absolute local path and a concise result summary. Keep FigurePlan v1, FigureSpec v1, and final RenderAudit v1 beside the image when the workspace permits. Do not use `file://` and never append a waived prompt. Stop before rendering if the user asked only for analysis or planning.
