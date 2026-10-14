---
name: krea2-prompt-suite
description: Create, reverse-engineer, expand, repair, convert, evaluate, and batch-generate prompts specifically for Krea 2. Use for KREA2/Krea 2 text-to-image, image-to-image, image reverse prompting, multi-image reference fusion, style or moodboard planning, typography and poster prompts, RAW/Turbo presets, prompt scoring, A/B variants, prompt conversion, and ComfyUI or RunningHub/Qwen3-VL system prompts. Also trigger on Chinese requests such as Krea2提示词、反推、扩写、改写、融合参考图、节点系统提示词. Do not use for unrelated models unless converting their prompt into Krea 2 format.
---

# Krea 2 Prompt Suite

## Core objective

Turn an idea, an existing prompt, one or more images, or a failed generation into a production-ready Krea 2 prompt and an actionable generation plan. Support multiple modes rather than forcing every request through one template.

## Operating principles

1. Identify the requested mode before writing the prompt. Infer the mode from context; do not ask a clarifying question when a reasonable assumption is possible.
2. Distinguish hosted Krea 2 Medium/Large from open-weight Krea 2 RAW/Turbo. Never mix their parameters or capabilities.
3. Treat Krea 2 as a natural-language model. Prefer concrete visual relations over generic quality tags or disconnected keyword stuffing.
4. Use short prompts deliberately for exploration and dense prompts for control. Do not assume longer is automatically better.
5. Bind every attribute to the correct subject. State counts, left/right placement, pose, gaze, object interaction, foreground/midground/background, and occlusion when they matter.
6. Preserve user constraints exactly: aspect ratio, title text, number of people, pose, palette, medium, reference-image roles, and requested omissions.
7. Never invent details during image reverse prompting. Mark uncertain readings as likely or unclear. Transcribe visible text exactly when legible.
8. For Turbo at CFG 0, express important exclusions as positive constraints because a traditional negative prompt may not affect the result. Provide a negative prompt only when the downstream workflow actually uses one.
9. Do not conflate Krea 2 with FLUX.1 Krea [dev].
10. When current release details, API parameters, licenses, or nodes may have changed, verify against official Krea, Hugging Face, GitHub, or ComfyUI sources before stating them as facts.

## Mode router

Select one primary mode and any useful secondary mode:

- `create`: Convert a concept or brief into a new Krea 2 prompt.
- `reverse`: Analyze an image and reconstruct a generation-ready prompt.
- `recreate`: Reverse prompt plus control recommendations for close image-to-image reconstruction.
- `expand`: Expand a short prompt without changing its core subject or intent.
- `refine`: Improve an existing Krea 2 prompt while preserving requested content.
- `repair`: Diagnose a failed result and rewrite only the modules causing failure.
- `convert`: Convert prompts from SDXL, Pony, FLUX, Midjourney, Ideogram, tag syntax, or Chinese shorthand into Krea 2 natural language.
- `multi-reference`: Assign roles to multiple images and fuse subject, pose, composition, style, palette, material, or atmosphere without accidental attribute mixing.
- `typography`: Create posters, covers, packaging, UI mockups, signs, or any image with exact visible text.
- `variants`: Produce controlled A/B variants or an exploration matrix with one variable changed per version.
- `evaluate`: Score a prompt, identify contradictions, missing control information, and likely failure points.
- `node-system`: Produce system prompts for Qwen3-VL, RunningHub LLM API Pro, or another vision/LLM node.
- `batch`: Generate a consistent prompt family for multiple titles, products, scenes, or aspect ratios.

Read [references/modes.md](references/modes.md) when the task involves reverse prompting, conversion, multi-reference fusion, evaluation, node prompts, or batch output.

## Input normalization

Extract or infer these fields:

- Goal: exploration, controlled generation, close recreation, editing, or prompt analysis.
- Target: hosted Medium/Large, open RAW/Turbo, or unknown.
- Inputs: concept, text prompt, image count, and role of each image.
- Output profile: `compact`, `production`, `exhaustive`, or `machine`.
- Image format: aspect ratio and whether the composition must reserve text or negative space.
- Hard constraints: exact text, subject count, adult status where relevant, pose, body orientation, direction of gaze, placement, palette, exclusions.
- Soft direction: mood, aesthetic, level of realism, movement, complexity, and experimentation.

If the target variant is unknown, write a variant-neutral prompt and label parameter advice as conditional.

## Universal workflow

### 1. Build a scene graph

Represent the image as entities and relations before writing prose:

- Entities: people, animals, objects, architecture, terrain, text.
- Attributes: appearance, clothing, materials, colors, scale.
- Actions: posture, gesture, contact, movement, gaze.
- Relations: left/right, near/far, in front of/behind, inside/on top of, overlapping, facing, holding, pointing toward.
- Layers: foreground, middle ground, background, atmosphere.

For two or more similar subjects, describe each independently to prevent attribute leakage.

### 2. Select only useful prompt modules

Use the K2-SCENE architecture from [references/prompt-architecture.md](references/prompt-architecture.md):

- Medium and image type
- Primary subject and hierarchy
- Appearance and identity-defining visual traits
- Pose, expression, gaze, and interaction
- Composition, shot, camera position, perspective, focus
- Environment and spatial layering
- Lighting and color system
- Materials and surface behavior
- Style, production method, and texture
- Exact typography
- Positive constraints

Do not force every module into simple prompts. Add detail only when it improves control.

### 3. Compile coherent natural language

Write one coherent English paragraph by default because it is directly reusable in Krea 2 and transferable across modern image models. Use Chinese for analysis and notes unless the user requests another language.

Prefer:

`A low-angle three-quarter portrait of one adult woman standing on the right third of the frame...`

Avoid:

`masterpiece, best quality, woman, sexy, cinematic, 8K, detailed, perfect hands`

Use commas for compact grouping when clear, but do not create an unstructured tag dump.

### 4. Validate before output

Check:

- No conflicting subject counts, poses, camera angles, lighting directions, media, or aspect ratios.
- Every clothing item, color, action, and prop is attached to the intended subject.
- The composition fits the requested ratio.
- Exact text is quoted and its position, hierarchy, font class, and line breaks are described.
- No unsupported camera model, focal length, brand, identity, or hidden detail was invented.
- No generic filler substitutes for visible information.
- Constraints are positive and executable, especially for Turbo.
- The prompt is not needlessly long.

Use the scoring rubric in [references/evaluation.md](references/evaluation.md) for formal evaluations or difficult repairs.

## Image reverse prompting

When images are provided, inspect them directly. Do not merely paraphrase the user's description.

1. Separate observation from inference.
2. Record subject count, pose geometry, camera framing, spatial layers, lighting direction, palette, material cues, medium, and text.
3. Reconstruct the prompt in visual priority order, not arbitrary category order.
4. For close recreation, additionally recommend image-to-image strength/denoise bands and reference controls as conditional workflow guidance. State that a prompt alone cannot guarantee pixel-level reconstruction.
5. For multiple images, assign explicit roles such as `Image 1 = pose`, `Image 2 = palette`, `Image 3 = clothing`, and prevent cross-role contamination.

Read [references/reverse-and-reference.md](references/reverse-and-reference.md) for the full procedure.

## Output profiles

### Compact

Return only the final prompt, or the exact format requested by the user.

### Production (default)

Return:

1. `Final Prompt (EN)` in one copyable block.
2. `Positive Constraints` only when they add control not already expressed.
3. `Negative Prompt` only when the target workflow supports it.
4. `Suggested Settings` with variant-specific facts separated from recommendations.
5. `Assumptions` only when uncertainty affects the result.

### Exhaustive

Add scene graph, module breakdown, risk analysis, two controlled variants, and generation strategy.

### Machine

Return valid JSON matching [assets/krea2-request.schema.json](assets/krea2-request.schema.json), with no Markdown around the JSON unless requested.

## Variant handling

### Open-weight RAW

Use for malleability, fine-tuning, post-training, and LoRA training. Official repository guidance currently uses 52 steps and CFG 3.5 at up to roughly 1K. Treat these as implementation-specific official defaults, not universal laws.

### Open-weight Turbo

Use for fast inference. Official repository guidance currently uses 8 steps, CFG 0, `mu 1.15`, and roughly 1K–2K. Prefer positive constraints over reliance on a negative prompt.

### Hosted Medium/Large

Do not apply RAW/Turbo sampler settings. Use hosted controls such as creativity, style references, moodboards, or generative sliders only when the user's environment exposes them. Medium is generally positioned as more stable and cost-efficient; Large as more textured, flexible, and photorealism-oriented. Verify current API/UI details when precision matters.

Read [references/krea2-core.md](references/krea2-core.md) before giving model facts or parameter recommendations.

## Specialized tasks

- Read [references/genre-presets.md](references/genre-presets.md) for photography, fashion, anime, cinematic, product, poster, architecture, ink art, surreal, and abstract prompts.
- Read [references/comfyui-node-prompts.md](references/comfyui-node-prompts.md) when the user wants a system prompt for image-to-text reverse prompting or LLM prompt compilation.
- Copy ready-to-use node prompts from `assets/system-prompts/` when the user requests the exact system prompt rather than an explanation.
- Use `scripts/krea2_prompt_compiler.py` when structured JSON must be deterministically converted into a consistent paragraph.

## Response discipline

- Follow the user's requested output count and format exactly.
- When the user says “只给提示词”, output only the prompt.
- Do not repeat the same information in English and Chinese unless requested.
- Do not alter exact title text, proper nouns, or quoted on-image text.
- For batch tasks, keep the shared visual system consistent while varying the requested subject or title.
- Separate verified facts from recommendations and mark uncertainty instead of guessing.
