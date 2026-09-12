---
name: academic-figure-draft-analyzer
description: Plan evidence-backed figures for a paper draft, markdown notes, outline, manuscript, PDF, or paper webpage. Supports Draft-to-Figure fast-track for Markdown notes as well as comprehensive multi-figure planning for full manuscripts.
metadata:
  version: "1.4.0"
  stages: [research, review]
---

# Academic Draft and Paper Analyzer (Figure Planner)

Produce a human-readable figure strategy and a machine-readable **Figure Plan v1**. Plan figures around the paper's claims and reader questions, not around a fixed count or a generic pipeline template.

Read `references/missing-info-policy.md` when the paper is incomplete. If a repository handoff or extracted reference-style profile exists, carry it forward without renaming fields.

## Dual-Track Planning Workflow

The analyzer operates in one of two modes depending on the input:

1. **Draft-to-Figure Fast-Track (草稿敏捷直出)**:
   - **Trigger**: Input is notes, an outline, or an early draft (Markdown, text, or draft sections) without complete experimental/analysis results.
   - **Target**: Focus exclusively on **Figure 1: Overall Framework / Methodology Overview**.
   - **Policy**: Do NOT force a multi-figure plan (ablation/data behavior). Do NOT warn about missing experimental/analysis sections.
2. **Camera-Ready Multi-Figure Plan (完整定稿多图规划)**:
   - **Trigger**: Input is a complete manuscript with experimental results (Markdown, LaTeX, PDF, or full text).
   - **Target**: Systematically plan the multi-figure suite with claim verification and publication constraints.

## Input contract

- Prefer: manuscript text or source, abstract, method, experiments, target venue/page limit, semantic architecture handoff, and any reference figures.
- Accept: Markdown (`.md`) draft or notes, outline, title plus abstract, local PDF, paper URL/HTML, Word/LaTeX.
- A URL is a paper source only after its content is inspected; do not classify every URL as a code repository.
- If a PDF or webpage cannot be read in the current environment, report that limitation rather than inventing paper structure.

## Output contract

Include:

1. Paper overview: question, contribution, evidence, and intended venue constraints.
2. Completeness statement: sections and artifacts actually inspected.
3. Per-figure recommendation with a controlled type and `must`, `strong`, or `nice` priority (in Draft mode, emit exactly one primary Figure 1).
4. A one-sentence communication goal: what the reader should understand after viewing the figure.
5. Required nodes, edges, authority boundaries, and forbidden implications.
6. Aspect ratio and final publication width hint.
7. `Figure Plan v1` JSON.

Controlled figure types: `Overall Framework`, `Network Architecture`, `Module Detail`, `Comparison/Ablation`, `Data Behavior`, `Concept/Motivation`, `Protocol/Sequence`, `Timeline/Lifecycle`.

## Workflow

### 1. Identify Input Mode and Structure

- **In Draft Mode (`.md` notes / outline / unstructured prose / draft)**:
  - **Structured Markdown**:
    - Headers (`#`, `##`): Primary semantic container zones (e.g. Input Context, Core Framework, Optimization Objective).
    - Lists (`1. 2. 3.`, `- `) and arrows (`->`): Sequential stages, data flow, and pipeline steps.
    - Bold terms (`**Name**`): Canonical node/module labels (`visible_text`).
    - Inline code (`` `B x C x H x W` ``): Tensor dimensions or data descriptions.
  - **Unstructured / Plain Prose Notes**:
    - Extract entities, transforms, and dataflow by tracing the grammatical subject-verb-object sequence (e.g. "Input X is encoded by Y and supervised by loss Z").
    - Group into 3 canonical panels: *Input / Context* -> *Core Method / Interaction* -> *Output / Supervision*.
  - Skip formal claim verification and proceed straight to narrative topology for Figure 1.
- **In Full Paper Mode**:
  - Map Introduction, Method, Experiments, Analysis, and Limitations. For each claimed contribution, record the source span and the evidence that could support a visual statement.

### 2. Assign Visual Jobs

Recommend a figure only when a visual materially improves understanding:

| Reader question / Objective | Common type | Typical priority |
|---|---|---|
| What is the end-to-end idea and authority/data flow? | Overall Framework | must (Default for Drafts) |
| What is the conceptual motivation or problem setting? | Concept/Motivation | strong or must |
| What is the internal executable structure? | Network Architecture | must or strong |
| How does the central mechanism work? | Module Detail | must or strong |
| Which choices matter empirically? | Comparison/Ablation | strong |
| How does behavior change over data, time, or conditions? | Data Behavior | strong or nice |
| How do components interact over time or protocol? | Protocol/Sequence / Timeline | strong |

Do not use venue stereotypes or fixed counts as requirements. For draft notes, emit a single high-impact Figure 1.

### 3. Design the narrative topology

For each figure specify:

- `communication_goal` and `claim_scope`;
- `hero_element`: the dominant visual story, not merely the largest box;
- `required_nodes` and `required_connections` from source evidence or draft structure;
- `secondary_context` that may be dropped under space pressure;
- `forbidden_claims` and `forbidden_connections`;
- `authority_boundaries` when agents, tools, or external oracles are involved;
- `text_budget`: short labels, with detail reserved for the caption;
- `reference_style_profile` if the user supplied a reference image.

An Overall Framework need not be a left-to-right chain. Choose among a loop, storyboard, asymmetric modular collage, layered authority diagram, central mechanism with satellites, or pipeline according to the scientific story.

### 4. Set publication geometry

- Overall Framework: usually 16:9 or 3:2 at double-column width (183 mm).
- Network Architecture / Pipeline: 16:9, 3:2, or tall layout when topology requires it.
- Module Detail / Concept: commonly 4:3 or 1:1.
- Comparison/Ablation: match the number and reading order of panels.
- Data Behavior / Timeline: let axes and sequence determine geometry.

### 5. Emit Figure Plan v1

```json
{
  "schema": "academic-figure/FigurePlan@1",
  "source_revision": "<paper-or-repo-revision>",
  "venue": null,
  "sources": [],
  "figures": [
    {
      "figure_id": "fig1",
      "figure_type": "Overall Framework",
      "priority": "must",
      "communication_goal": "<one sentence>",
      "claim_scope": ["<evidence-backed claim or draft objective>"],
      "hero_element": "<loop|mechanism|modular collage|pipeline|other>",
      "required_nodes": ["<component-id>"],
      "required_connections": ["<from-id> -> <to-id>: <kind>"],
      "authority_boundaries": [],
      "secondary_context": [],
      "forbidden_claims": [],
      "forbidden_connections": [],
      "aspect_ratio": "16:9",
      "final_width_mm": 183,
      "style_profile_hint": null,
      "reference_assets": [],
      "open_questions": [],
      "confidence": "high|partial|sparse",
      "review_status": "pending|confirmed|waived"
    }
  ]
}
```

The example defines fields only. Replace every placeholder with sourced content or an explicit null/empty value.

## Sparse input & Draft Handling

- Single `.md` draft or notes: Extract pipeline directly from headers and bullet points; plan Figure 1 immediately.
- Title and abstract only: plan high-level visual jobs; do not invent submodules.
- Method without experiments: plan method framework; do not block or raise spurious errors.
- Repository handoff only: produce a system-centric plan and flag narrative review.
- Reference image only: analyze visual grammar, but request or locate the target system content before planning its topology.

## Stop

Stop after delivering the strategy and Figure Plan v1. Do not generate prompts or images unless the user requested the downstream workflow.

