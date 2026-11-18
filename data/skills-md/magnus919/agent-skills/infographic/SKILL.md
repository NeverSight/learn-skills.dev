---
name: infographic
description: >-
  Design, create, or improve an infographic, visual explainer, illustrated guide,
  comparison poster, process graphic, or data story for any audience. Use for
  turning evidence and ideas into a clear, polished visual explanation, including
  choosing information structure, visual encoding, and a distinct aesthetic.
  Do not use for standalone decorative artwork, complete brand identity systems,
  statistical analysis alone, or ordinary document formatting.
license: MIT
---

# Infographic

Produce a visual explanation that helps its intended reader understand, compare,
choose, or act. A beautiful image with incorrect relationships or unreadable
content is unfinished. This skill supplies judgment and design specifications;
it does not install a renderer or confer access to an image-generation service.

## When not to use

Use [brand-designer](../brand-designer/SKILL.md) for identity systems,
[data-scientist](../data-scientist/SKILL.md) for statistical inference,
[documents](../documents/SKILL.md) for office/PDF production, and
[color-management](../color-management/SKILL.md) for ICC/profile operations.
These optional companion skills can support an infographic without replacing its
editorial decisions. If a companion is not installed, use available tool guidance;
do not assume a sibling path or capability exists.
For decorative artwork alone, use the available image tool's own workflow.

## Workflow

1. **Frame the communication contract.** Establish who will read it, what they
   already know, and what they should understand or do afterward. Identify the
   real viewing context, dimensions, language, accessibility needs, and requested
   deliverables. Infer low-risk defaults and state them briefly; ask only for
   missing information that materially changes correctness or usefulness. Scale
   the process to the request: a small family guide does not need a long brief.
   Use [the brief](templates/brief.md) for complex work.
2. **Ground the message.** Read [evidence and editorial judgment](references/evidence.md)
   for factual, quantitative, persuasive, or source-poor requests. Write the
   principal takeaway and the few supporting claims before decorating. Preserve
   material limitations beside affected claims. Do not invent statistics,
   citations, or causal relationships. A request for impressive numbers does not
   supply evidence. If sources are missing, research when available or produce
   a clearly qualitative/illustrative version and explain the limitation.
3. **Choose the information structure.** Read [layouts and encodings](references/layouts.md)
   when composing or revising. Match the reader's task and real relationships to
   a comparison, sequence, timeline, mechanism, hierarchy, geography, data story,
   or reference arrangement. Sketch the reading order and focal point. Arrows,
   areas, containers, proximity, and numbering all make claims; use them deliberately.
4. **Choose a visual language separately.** Read [style recipes](references/styles.md)
   when a style is requested or needs choosing. Select a coherent direction
   appropriate to the reader, subject, medium, and supplied brand constraints.
   Offer a few genuinely different directions only when the choice is consequential;
   otherwise choose and explain one. A timeline can be a spare editorial graphic,
   a playful cut-paper story, or a technical plate without changing chronology.
5. **Execute with real capabilities.** Read [production](references/production.md)
   before rendering. Check available tools, fonts, export formats, and inspection
   routes. Use deterministic geometry and typesetting for exact numerical charts
   and dense required copy. Use image generation for expressive conceptual imagery
   where available; hybrid assembly is valid. Follow the active image tool's rules.
   A text prompt is a production specification, not a rendered artifact. Do not
   claim execution or file formats that were not produced.
6. **Inspect and improve the actual export.** Read [review and polish](references/review.md)
   before delivery. Verify evidence, geometry, visual semantics, hierarchy,
   actual-size legibility, accessibility, and export integrity separately. Repair
   content and structure before cosmetic details. Re-render after consequential
   edits; check the final file, not only the source or previous preview.
7. **Deliver what exists.** Provide the requested visual, editable source when
   available, an accessible text equivalent, and traceable source notes. Briefly
   state meaningful limitations and what was tested. If rendering is unavailable,
   deliver a usable specification and exact copy, explicitly marked unrendered.
   Stop when the artifact meets its communication contract and review gates, or
   when a specific missing capability/source prevents completion. After two
   non-improving repair attempts on the same defect, change the approach or report
   the blocker rather than cycling indefinitely.

## Resources on demand

- [Composition specification](templates/composition.md): for tool handoffs, hybrids,
  or layouts with multiple information layers.
- [Generation prompt](templates/generation-prompt.md): when using an image backend;
  adapt to its actual capabilities and keep verified text/data separately.
- [Sources and reuse](references/sources.md): when checking methodological claims,
  citing foundations, or selecting outside assets.

Local artifact creation is the default. Publishing, sending, or overwriting an
external artifact changes external state: confirm target, scope, and rollback
path before the first mutation, using authorization already given in the conversation.
