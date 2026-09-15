---
name: poster-style-transfer
description: Analyze an uploaded or local reference poster, extract its reusable design system, and transpose that system to an original poster with a new theme, title, subtitle, or campaign copy.
license: MIT
compatibility: Works with Codex and Agent Skills-compatible runtimes. Direct generation requires image viewing and image-generation capabilities.
metadata:
  author: jiemianduan
  version: "0.1.0"
---

# Poster Style Transfer

Extract poster grammar, not poster content. Preserve the reference's design system while rebuilding its subject matter, copy, symbols, and narrative for the user's new theme.

## Select the mode

Infer the mode from the request:

1. **Direct generation** — Use when the user supplies a reference poster plus a new theme or copy. Analyze internally, build the prompt, generate the poster, validate it, and return the result.
2. **Style Spec only** — Use when the user asks to analyze, archive, or reuse the poster style but says not to generate yet. Return a structured `Poster Style Spec`, not a general aesthetic review.
3. **Variable template** — Use when the user asks for a reusable prompt. Return a copy-ready prompt with editable variables for theme, title, subtitle, hero, props, palette, date, location, ratio, and supporting copy.

If the user invokes the skill but only asks “what style is this?”, explain that the skill produces a reusable production specification and return the compact Style Spec. Do not turn the response into art-history commentary.

## Validate the reference

Require at least one usable poster image. For a local image, inspect it at the highest available detail before analysis.

Confirm that the reference has poster characteristics such as a deliberate canvas, typography hierarchy, hero visual, information modules, and designed reading order. If it is not a poster, ask for a poster reference instead of applying the workflow to a generic image.

Treat one image as the primary reference by default. If several posters are supplied, identify which one controls layout, typography, hero treatment, and color; do not silently average contradictions.

## Collect the brief

Require only:

- a reference poster;
- a new theme for direct generation.

Accept these optional fields: main title, subtitle, supporting copy, date, location, target audience, poster purpose, aspect ratio, brand assets, and target image model.

Infer tasteful missing details when the user authorizes direct generation. Do not invent factual addresses, prices, schedules, official slogans, logos, or endorsements. Label invented campaign information as concept copy when it could be mistaken for a real announcement.

## Extract the design system

Read [poster-style-spec.md](references/poster-style-spec.md) and fill every high-impact field supported by visible evidence. Classify the reference using [poster-archetypes.md](references/poster-archetypes.md), then prioritize the dimensions associated with that archetype.

Analyze in this order:

1. poster archetype and communication purpose;
2. canvas, grid, margins, zones, and reading path;
3. typography hierarchy and text behavior;
4. hero visual mechanism, scale, crop, and layering;
5. color relationships and contrast distribution;
6. graphic devices, decoration density, and repetition;
7. image treatment, materials, lighting, and finishing texture;
8. information density, negative space, and overall rhythm.

Use relative measurements such as percentages of canvas width or height. Prefer “title occupies the upper-left 38%” over “large title at the top.” Describe visible behavior rather than guessing font names, artists, brands, lenses, engines, or original generation settings.

## Separate constants from variables

Create three lists before writing the generation prompt.

### Hard lock

Preserve the reference's highest-impact design rules: aspect ratio, grid family, margin rhythm, title footprint, hero-to-canvas ratio, dominant overlap behavior, palette relationship, typography category, primary image treatment, and density map.

### Soft lock

Preserve with adaptation: decoration count, secondary modules, texture intensity, lighting direction, local rotations, small labels, and accent shapes.

### Must replace

Replace the reference's people, characters, products, props, scenery, logos, wording, brand identifiers, copyrighted character designs, and theme-specific symbols. Do not trace a unique illustration or reproduce the complete composition pixel for pixel.

Preserve spatial grammar rather than exact coordinates. Adapt the grid when the new title length, script, or hero silhouette requires it.

## Translate the new theme

Convert the user's theme into a coherent content system before prompting:

- core message;
- hero subject and action;
- setting or backdrop;
- 2–5 supporting props;
- visual metaphor or symbol;
- emotional tone;
- copy hierarchy.

Choose elements that belong to the new theme and can be rendered through the reference's visual technique. Keep every prop purposeful. Do not carry over a reference object merely because it is visually prominent.

## Build the generation prompt

Write a structured prompt in this order:

`output intent → reference role → new theme → locked layout → typography → new hero → environment/props → color → material/lighting → exact text → constraints/avoid list`

State that the input image is a style and design-system reference only. Explicitly list both the traits to preserve and the content to replace.

Quote all literal copy. Require verbatim rendering and prohibit extra text. Minimize in-image copy when the user has not supplied it.

For short headlines, render text in the image. For dense copy or exact Chinese typography, prefer a two-layer workflow: generate the visual with reserved text zones, then add exact copy using a deterministic vector, HTML, or document-layout tool when available. Do not claim text accuracy without checking the image.

## Generate and iterate

Use the available image-generation tool for direct generation. Pass the reference as a style reference, not an edit target. Never request preservation of the reference's specific person, logo, wording, or proprietary character.

After generation, inspect:

- subject and theme relevance;
- composition and hierarchy;
- text accuracy;
- hard-lock fidelity;
- forbidden reference content;
- artifacts, random letters, and unwanted logos.

Read [fidelity-rubric.md](references/fidelity-rubric.md) and score the result. If a single issue dominates, make one targeted revision and repeat the invariants. Do not rewrite the entire prompt for a local text or placement defect.

If the built-in image service fails, retry once. Do not switch to a CLI/API path that requires credentials unless the user explicitly authorizes it. If both the reference path and pure-generation path fail, return the final prompt and report the service failure clearly.

## Output contracts

### Direct generation

Return:

1. the generated poster;
2. a compact note listing the preserved style mechanisms and replaced content;
3. the final prompt or a concise prompt summary;
4. the saved path when a local artifact path is available.

### Style Spec only

Return:

1. poster archetype;
2. compact `Poster Style Spec`;
3. Hard lock / Soft lock / Must replace;
4. recommended variable slots;
5. fidelity priorities.

Do not generate an image.

### Variable template

Return:

1. a variable list;
2. a complete copy-ready prompt template;
3. a small filled example only when it clarifies usage.

Include at least: `[主题]`, `[英文主标题]`, `[中文主标题]`, `[副标题]`, `[主视觉]`, `[动作]`, `[主题道具]`, `[主色]`, `[强调色]`, `[日期]`, `[地点]`, `[宣传语]`, and `[画幅比例]`.

## Quality rules

- Optimize for “same visual system, new original poster,” not “similar colors.”
- Keep observations separate from inferred production suggestions.
- Do not name an artist or recover a supposed original prompt without evidence.
- Do not retain a real person's identity unless the user explicitly requests identity preservation and has supplied that person as an intended subject.
- Do not present invented event details as factual.
- Reject outputs that preserve mood but lose the reference's layout, type hierarchy, or hero mechanism.
