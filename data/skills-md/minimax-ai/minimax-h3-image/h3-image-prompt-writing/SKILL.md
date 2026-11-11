---
name: h3-image-prompt-writing
description: Write H3Image prompts for text-to-image generation and reference-image editing. Use to turn an idea or brief into a complete image prompt, refine an existing prompt, or describe edits and reference-guided compositions.
---

# H3Image Prompt Writing

Turn ideas, briefs, existing prompts, and reference images into ready-to-use H3Image prompts.

## Workflow

1. Read the relevant guide, including its examples:
   - [T2I](references/t2i-en.txt): compose an image from text.
   - [Edit](references/edit-en.txt): preserve, change, or borrow reference-image content, including for a new composition. Inspect the relevant images in their supplied order.
2. For a new prompt, develop the brief into concrete visible content and complete ordinary unspecified details. For an existing prompt, apply the requested revision while retaining its other constraints.
3. Ask only when missing information prevents a useful prompt. Do not require a finished draft from someone asking you to write one, or invent source facts to fill an evidence gap.
4. Check the finished prompt against the user's content, exact wording, counts, spatial relationships, and exclusions.

## Delivery

- Deliver the prompt itself. This skill writes prompts; it does not generate images.
- Use English visual narration; visible lettering and authored copy retain their required language.
- Organize T2I descriptions naturally. Follow the Edit guide's single-paragraph source–relationship–change structure.
- When the user or downstream tool needs generation settings, give the aspect ratio separately. Preserve explicit ratios or derive it from requested dimensions.
