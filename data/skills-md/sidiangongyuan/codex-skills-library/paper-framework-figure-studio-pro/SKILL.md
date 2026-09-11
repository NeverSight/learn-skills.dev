---
name: paper-framework-figure-studio-pro
description: Use when planning a source-grounded method overview, architecture, pipeline, system/data-flow, mechanism, or agent-workflow figure for a CS or deep-learning paper. Produces an editable figure brief before image generation or manual redrawing; not for plots, tables, or general prose.
license: MIT
---

# Paper Framework Figure Studio Pro

This is a lightweight local adapter inspired by
`c-narcissus/paper-framework-figure-studio-pro`. It keeps the useful
paper-grounded S0-S5 co-design flow while avoiding the upstream package's heavy
asset vendoring, mandatory checkpoint zip behavior, and fixed personal response
rules.

## Default Boundaries

- Work in conversation by default. Do not create project files, reports,
  checkpoints, generated images, or restore bundles unless the user explicitly
  asks for them.
- Treat image generation as opt-in. S2 and S5 are planning handoff stages unless
  the user explicitly asks to generate images.
- Keep the workflow human-in-the-loop. Execute at most one public stage per
  response unless the user explicitly requests a compact text-only bundle such
  as "do S0/S1 together."
- Stop after S5. The human chooses the final candidate, performs manual
  redrawing/editing, and decides final caption and paper placement.
- Route final plot/table polish, Matplotlib/LaTeX edits, captions, and rendered
  validation to `$paper-visual-craft`.

## Input Discipline

Before designing the figure, identify the available evidence:

- Paper source: PDF, LaTeX, abstract/method text, notes, or user summary.
- Target role: method overview, architecture, pipeline, data flow, mechanism,
  or agent workflow.
- Venue/style constraints: CVPR/ICCV/ECCV/NeurIPS/ICLR/ICML/CoRL, double
  column, grayscale safety, line-art preference, space budget.
- Existing visuals: reference figures, current draft figure, or explicit
  instruction not to inspect an existing paper diagram.
- User constraints: must-show modules, forbidden claims, terminology, symbols,
  and whether image generation is allowed.

If inputs are incomplete, state the assumptions and ask only for missing facts
that materially affect the diagram contract. Do not invent paper modules,
symbols, arrows, metrics, or evidence.

## Local S0-S5 Workflow

Use `references/workflow.md` when a task needs the full staged process.

- **S0 Paper foundation**: inventory sources, extract core modules, terms,
  equations/symbols, data/control/model flow, evidence anchors, and ambiguity
  risks.
- **S1 Figure strategy**: define the reader question, figure type, story path,
  semantic graph, visible text budget, style family, and source-grounded prompt
  contract.
- **S2 Sketch exploration**: only if explicitly requested, generate or describe
  first-round candidate directions. Default to text-only candidate briefs.
- **S3 Direction select**: compare candidates against the source contract and
  user preference; record what to keep, avoid, simplify, or repair.
- **S4 Formal candidate brief**: prepare the final candidate matrix or image
  prompts with strict source-fidelity, symbol, connector, and density rules.
- **S5 Candidate image**: only if explicitly requested, generate final raster
  candidates. Otherwise hand off prompt packages or a manual-redraw brief.

For ordinary requests, start with S0/S1 and return a concise figure brief rather
than a full staged dossier.

## Source-Faithful Figure Contract

Every visible entity, label, symbol, connector, and visual metaphor must be:

- directly supported by the paper/user material, or
- explicitly marked as an inference with the reasoning chain, or
- marked unsupported and excluded from the figure.

Use these checks before proposing prompts or candidates:

- Do arrows have evidence for both source and target semantics?
- Are variables, metrics, weights, losses, or thresholds shown as edge/port/tag
  information instead of peer modules when appropriate?
- Does one symbol/color/line style mean exactly one thing?
- Is the diagram explaining the paper's actual contribution rather than a
  generic architecture pattern?
- Can dense details move to caption, legend, or prose without weakening the
  first-glance story?

If the contract is not supportable, stop at the risk register and ask for the
missing paper detail or user decision.

## Default Output

Unless the user requested files or images, answer in conversation with:

- `figure role`
- `reader question`
- `source-backed core modules`
- `semantic flow`
- `visible text contract`
- `style / surface recommendation`
- `must-include / must-exclude`
- `risks or unsupported parts`
- `candidate directions`
- `next action`

Use `templates/figure-brief-template.md` when the user asks for a structured
brief or when a worker needs a handoff.

## Reference Routing

- Read `references/source-map.md` before discussing provenance, upstream
  licensing, or vault updates.
- Read `references/workflow.md` before running a full S0-S5 planning session.
- Use `templates/figure-brief-template.md` for reusable handoff briefs.
