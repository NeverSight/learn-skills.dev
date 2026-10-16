---
name: scientific-diagram-skill
description: Research diagram skill for draw.io/diagrams.net, Mermaid drafts, system block diagrams, method figures, signal-flow diagrams, agent workflows, experiment pipelines, and clean editable diagram exports. Use when the user asks to plan, generate, revise, review, or export a scientific or engineering diagram rather than a data plot.
---

# Scientific Diagram Skill

## Overview

Use this skill when the user needs a research diagram: a method overview,
system architecture, signal chain, experiment pipeline, paper figure schematic,
or agent workflow. It complements `matlab-plotting-skill`: MATLAB handles data
figures, while this skill handles diagrams that explain how a method or system
is organized.

For quick discussion, start with Mermaid. For an editable artifact, create or
revise a `.drawio` file for draw.io / diagrams.net.

## Workflow

1. Identify the diagram job: method flow, system blocks, signal path,
   experiment protocol, comparison map, or maintenance workflow.
2. Draft the structure in Mermaid when the user is still deciding the layout.
3. Move to draw.io when the user needs an editable file, a paper-ready export,
   or alignment and grouping that Mermaid cannot express cleanly.
4. Read `references/drawio-workflow.md` before writing `.drawio` XML or giving
   diagrams.net export steps.
5. Read `references/diagram-quality-checklist.md` before final review.
6. Read `references/export-and-provenance.md` before committing generated
   diagram files or advising what belongs in a public repository.

## Bundled Example

Use `assets/examples/research-method-flow.drawio` as the smallest editable
example of the intended file shape. It has a matching
`assets/examples/research-method-flow.svg` preview and
`assets/examples/provenance.md` note. `assets/examples/manifest.json` lists the
bundled examples for repository checks and automation. The first example is
clean-room and uses synthetic workflow labels.

Use `assets/examples/reproducible-figure-system.drawio` when a compact system
block diagram is a better fit. Its matching
`assets/examples/reproducible-figure-system.svg` preview keeps the same
clean-room and public-release boundaries.

Repository maintainers can run:

```bash
python3 scripts/check_diagram_examples.py
```

That check parses the `.drawio` XML and SVG preview, verifies expected labels,
and scans the example files for private paths, emails, obvious source markers,
and personal-data keywords.

## Diagram Defaults

- Keep labels short and technical. Prefer noun phrases over slogans.
- Use left-to-right flow for pipelines and top-to-bottom flow for staged
  procedures.
- Put inputs, processing, outputs, and validation in visibly separate groups.
- Use a restrained palette: one neutral base, one accent for the active method,
  and one warning color only when a risk or failure path matters.
- Prefer SVG for public docs and `.drawio` for editable source. Use PNG only for
  GitHub previews or screenshots.

## Safety Rules

- No Watermarks. Do not add school names, personal names, hidden signatures,
  emails, local paths, or decorative watermarks.
- Do not trace or copy figures from papers, slides, Nature/Science examples, or
  private screenshots. Rebuild the idea as a clean-room communication task.
- Do not include private logos unless the user confirms they are allowed.
- Do not commit raw screenshots, full slide decks, binary source bundles, or
  exports that contain private metadata.
- If a diagram is based on user-provided material, describe the source boundary
  in the final note and keep the public file free of personal traces.

## Handoff

When a diagram belongs with MATLAB figure work, keep the diagram and data figure
separate:

- `.drawio` source for the conceptual figure.
- SVG/PNG preview for README or docs.
- MATLAB-generated plots for numeric results.
- A short provenance note explaining what was generated, what was referenced,
  and what should not be uploaded.
