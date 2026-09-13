---
name: mascot-logo-generator
description: Generate mascot-inspired logo creative directions, image-generation prompts, and optionally direct logo images by extracting the most recognizable feature from an animal, character, object, celestial body, fictional figure, or mascot-like source. Use when the user asks for animal feature abstraction, mascot logo design, paw/head/antler/tusk/alien/crescent-style symbol ideas, mascot-derived brand marks, direct mascot logo image generation, or revisions to an existing mascot-symbol concept.
---

# Mascot Logo Generator

Use this skill to turn a mascot-like source into a practical logo creative package, and to generate a logo image when the user explicitly asks to create or render one. This skill uses the same brand-system-board presentation style as `base-logo-generator`, but its symbol logic is mascot-feature extraction instead of general abstract logo design.

## Workflow

1. Identify the logo type: company/brand, product, cultural/creative merchandise, campaign/advertising, event, app, sub-brand, personal brand, or other.
2. Understand the object being branded: name, audience, offering, brand values, usage surfaces, market context, and any style constraints.
3. Identify the mascot source: animal, fictional figure, object, celestial body, character, or other recognizable entity.
4. Extract 2-4 symbolic routes from the source's most recognizable features: paw/claw, head profile, horn/antler/ear shape, tusks, alien eyes, mask, tail curve, crescent/moon fragment, helmet, fruit cutout, or another unmistakable part.
5. Choose one strongest feature route and simplify it into a trademarkable silhouette. Explain what is being exaggerated, what is being omitted, and why the result works at small sizes.
6. If the user provides a visual reference, extract only the transferable design method: layout, spacing, color restraint, typography mood, silhouette economy, scale hierarchy, presentation format, and production constraints. Do not copy the reference mark, wordmark, protected silhouette, or trademark-specific proportions.
7. Generate platform-ready prompts. If the user specifies `target_platform`, focus on that platform; otherwise include Universal, GPT Image, Midjourney, Flux, and Ideogram variants.
8. For direct image generation, default to a brand-system-board presentation unless the user asks for a standalone logo, transparent asset, app icon, or another format. The board should use a square brand guideline grid with numbered modules: main logo, favicon, seal version, wordmark lockup, black/ivory applications, mockup, embossed application, symbol meaning, and a footer value strip.
9. If the user asks to "generate", "render", "create an image", "出图", "直接生成", or sets `render_image: true`, use the strongest GPT Image or Universal prompt to call the `imagegen` skill/tool or another available image-generation tool after preparing the creative direction. Generate one polished primary image unless the user asks for variants.
10. If image generation is requested but no image-generation tool is available, return the creative package and clearly identify the final prompt to paste into an image model.
11. If `revision_notes` are provided, preserve the useful parts of the prior direction and revise only the requested aspects.

## Output

Return these sections:

- Logo Direction
- Mascot Feature Concept
- Visual System Notes
- Brand System Board Layout
- Final Image Prompts
- Generated Logo, only when direct image generation is requested and available

Read `prompt.md` for detailed style constraints, anti-patterns, and output templates.
