---
name: academic-figure-designer
description: Unified academic figure designer, semantic color & surface decision engine, and FigureSpec v1 compiler. Handles style selection, reference palette derivation, colorblind-safe token binding, SVMC visual metaphors, and normalized compact prose prompt compilation across classic-technical, pastel-airy-ui, illustrated-modular, and reference-led profiles.
metadata:
  version: "2.1.0"
  stages: [writing, research, review]
---

# Academic Figure Designer and Spec Engine

Design evidence-grounded academic figures, make semantic color & surface decisions, and compile clean `academic-figure/FigureSpec@1` specifications and normalized structured rendering briefs. This skill serves as the single authoritative designer and prompt compiler for all figure styles.

Load only as needed:

- spec contract → `json-schema.md` and `figure-spec.schema.json`
- prompt compilation → `references/json-to-prompt.md`
- visual brief guidance → `references/image-prompt-guide.md`
- composition scaffolds → `references/prompt-templates.md`
- visual anchors & SVMC → `references/architecture-icons.md`
- palette/style fallback → `references/palettes.md` and optional `references/styles/`
- missing evidence → `references/missing-info-policy.md`

## Supported Style Profiles

Select one canonical `style_profile` (or compose with layer overlays from `docs/styles/`):

1. **`classic-technical` (经典学术框线风)**:
   - Clean white background, thin 1.5pt crisp outlines, restrained subtle tints (Okabe-Ito, Nature Blue, Cool Gray).
   - High contrast, orthogonal alignment, strict box/arrow engineering topology.
   - High-density tabular parameters and formal sans-serif typography (Helvetica/Inter).
2. **`pastel-airy-ui` (现代柔彩空气风)**:
   - White canvas with floating white cards and faint borders.
   - Generous negative space, floating pills/tokens (P1 Warm, P2 Cool, P3 Earthy), and lightweight curves.
   - Interface-like feel without multi-level nested boxes.
3. **`illustrated-modular` (编辑手绘模块风 / 有色语义分区图示风)**:
   - White canvas with content-driven soft-tinted semantic zones (I1 paired tokens: `{soft_fill, dark_outline, title_text, icon_accent}`).
   - Strong same-hue 1.5–2.5px dark outlines and **no drop shadows**.
   - Asymmetric hero region (~35–55% visual focus) with supporting modules arranged by real semantics.
   - Content-grounded editorial line art tied to declared semantics.
4. **`reference-led` (参考图驱动自由风格)**:
   - Extracts observable visual grammar (composition, marks, stroke, typography, illustration level, paired color fills/outlines) directly from a user-supplied reference image without copying proprietary content or topology.

## Direct Input Normalization Protocol (自然语言直通归一化)

When the user provides direct natural-language architecture descriptions (bypassing upstream analyzers), deterministically normalize the input into `FigureSpec v1`:

1. **Source Mapping**:
   - `sources`: `[{"kind": "user_instruction", "uri_or_path": "conversation", "evidence": "<exact user request text>"}]`
   - `plan_revision`: `"r1"`
2. **Topology Synthesis**:
   - Extract stages/modules as snake_case IDs (`input_data`, `encoder`, `fusion_block`, `loss_head`, `output`).
   - Derive directed connections from temporal or dataflow verbs (e.g. "送入", "经过", "transforms to").
   - Default `must_not_claim: []`, `forbidden_connections: []`, and standard `negative_constraints`.

## Semantic Color & Accessibility Decision (Domain-Adaptive Presets)

The default rules below serve as **recommended presets for ML, AI4Science, and Systems papers**. Domain-specific figures (e.g. monochrome print, inverted microscopy, multi-channel bio, astrophysics) may customize palette and background while preserving readability:

1. **Recommended ML / Systems Role Binding (Preset)**:
   - Multi-stage pipeline: Stage 1 (Green input) -> Stage 2 (Blue encoder) -> Stage 3 (Peach transformation) -> Stage 4 (Purple loss) -> Stage 5 (Gold output).
   - Deep Learning: Features/Data (Green) -> Backbone (Blue) -> Fusion/Attention (Peach) -> Loss/Constraint (Purple) -> Head/Task (Gold).
   - Interactive / Agentic: Policy/Reasoning (Blue), Context/Observation (Green), Tool/Harness (Peach), Advisory/Feedback (Purple), Memory/Storage (Cyan), Output (Gold), Guardrail/Stop (Coral).
2. **Domain-Specific Extensions**:
   - **Monochrome Print**: High-contrast grayscale tints (`#FFFFFF` fill, `#24323D` stroke, dashed vs solid line dual-encoding).
   - **Dark/Microscopy / Astrophysics**: Dark canvas allowed when reference or domain data requires inverted emission contrast.
3. **Accessibility & Grayscale Invariants**:
   - Ensure title and label texts meet WCAG AA contrast against their card backgrounds.
   - Dual-encode critical paths with shape, border style (solid vs dashed), or iconography so meaning survives grayscale printing and color vision deficiencies.

## Strict Prompt Formatting Standard (Prose Normalization)

All generated image prompts **MUST be compiled as normalized structured natural language (Compact Prose)**:

> [!IMPORTANT]
> **Zero Markdown Syntax in Image Prompts**:
> Never use Markdown formatting symbols (such as `#` headers, `**bold**`, `*italic*`, markdown bullet lists `- item`, backticks, or ASCII markdown tables `| --- |`) inside the prompt string sent to diffusion/image models. Image models frequently hallucinate and render Markdown syntax tokens as literal text on the canvas.
> Use clean, comma-and-sentence structured prose grouped by numbered container blocks or semantic zones.

### Canonical Prompt Structure

1. **Lead & Purpose**: High-level figure goal, aspect ratio, canvas background (pure white `#FFFFFF`), and style profile. Default to an external paper caption with no canvas title. If the user, FigureSpec, or supplied reference explicitly requires a title, lock exactly one short non-banner title and reserve whitespace for it.
2. **Layout & Hero Focus**: Numbered container panels and proportions (e.g. 3-column sandwich layout, central hero region).
3. **Semantic Container Blocks**: For each container, describe inner title pill, sub-cards, data flow, and scientific visual metaphors (SVMC).
4. **Topology & Connections**: Explicit source -> destination connections, line styles (solid for forward, dashed for feedback/advisory), and edge labels.
5. **Visual Constraints**: Negative defect constraints (*No unintended or duplicated title banner, no floating text, no gradients, no 3D chrome, no photorealism, no shadows*).

## Text Budget

Visible text must remain structural and publication-legible:

| Element | Guideline |
|---|---|
| Region or module title | usually no more than 5 words |
| Short label | usually no more than 3 words |
| Arrow label | usually no more than 3 words |
| Core formula | at most one short sourced line |
| Parameters, evidence, caveats | caption only |

Drop secondary labels before reducing them below readable final-paper size.

## Output Contracts

This skill emits one of two deliverables based on the user's intent:

### A. Full Figure Design (Default)
Emits `FigureSpec v1` JSON and normalized compact prose prompt. Proceed to validate and render.

### B. Palette Decision (Color / Consultation Only)
When the user asks only for color palette advice, style recommendation, or accessibility review (`学术配图配色`, `论文配色方案`, `色盲友好配色`):
Emit a structured **Palette Decision** and stop:
- Canonical `style_profile` and decision branch (`user`, `reference`, `scene`, or `default`);
- Recommended palette / paired token set (and one alternate);
- Canvas, body text, outline, and neutral divider colors;
- Semantic-zone bindings mapped to the paper's actual roles;
- Accessibility & grayscale dual-encoding notes;
- Copy-ready token handoff.

## Workflow

### 1. Identify Task Scope (Design vs Palette-Only)
- If the request is palette/color/style consultation only, perform Step 3 (Bind Style & Color Tokens) and emit the **Palette Decision**, then **STOP**.
- If the request is full figure creation or prompt compilation, proceed through all steps.

### 2. Close the Semantic Graph & Geometry
Copy component IDs, labels, groups, and typed connections from upstream analysis or direct user input. Carry `must_not_claim`, `forbidden_connections`, and authority boundaries into the spec.

### 3. Choose Composition & Visual Metaphor (SVMC & Spatial Blueprints)
- **Spatial Container Allocation**: Express macro-containers with explicit canvas height/width percentages (e.g., 2-tier stacked containers with 30-35% top vs 65-70% bottom, or left-hero 40-50% vs right-stack 50-60%) to prevent empty canvas dead zones.
- **Nested Card Scaffolds**: Use outer macro-containers with subtle dashed borders and nest solid white sub-cards inside.
- **Micro-Visual Trinity Injection**: Never output empty blank boxes. For each key node, compile the **Micro-Visual Trinity** from `references/json-to-prompt.md` and `references/architecture-icons.md`:
  1. *Header / Icon Badge* (domain icon, e.g. 💡, 🔬, 🔍, 📊);
  2. *Concrete Scientific Schematic* (3D GP elevation mesh, 1D multi-peak acquisition curve, 3D tensor block, heatmap, or state DAG);
  3. *Micro Mathematical/Data Card* (equation card, uncertainty gauge, dialogue bubble, or mini table).

### 4. Bind Style & Color Tokens Semantically
Bind paired tokens to semantic regions: background, soft fill, dark outline/title, optional icon accent, and exception color from `docs/palettes.md`. Follow dual-fidelity and multi-role paired color rules (e.g. Coral Red for real/high-fidelity vs Slate Blue for surrogate/low-fidelity).

### 5. Emit FigureSpec v1
Conform to `figure-spec.schema.json`. Required features include:
- `style_profile`: `classic-technical`, `pastel-airy-ui`, `illustrated-modular`, or `reference-led`.
- unique component IDs, closed visible-text list, sources, typed connections with valid endpoints.
- `prompt_review: requested|confirmed|waived` and conditional `prompt_reviewed_sha256`.
- declared absolute `workspace_root` and `output_path`.

### 6. Validate FigureSpec v1
Immediately before every render or edit, run:

```bash
python3 academic-figure-designer/scripts/validate_figure_spec.py \
  --strict-v1 --render-ready \
  --workspace-root <trusted-actual-root> \
  <spec.json>
```

### 7. Hand off for Rendering & Repair
When called from `academic-figure-workflow`, pass the validated rendering package forward. Use the current session's native `image_gen.imagegen` interface. If prompt review is `waived`, keep prompt internal as a tool parameter and deliver the rendered image directly.

## Stop Condition

- **Palette-only requests**: Stop after emitting the complete **Palette Decision**. Do not demand topology or attempt image rendering.
- **Figure design requests**: Stop after emitting and validating `FigureSpec v1` (or delivering the rendered image in workflow mode).


