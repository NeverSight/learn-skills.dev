---
name: image-generation-enhanced
description: Generate and edit high-quality images with AI. Emphasize strong prompt design, structured JSON prompting, reference-image workflows, text rendering, and iterative refinement. Use any time the user needs an image generated.
license: MIT
prerequisites:
  - OpenRouter API key
metadata:
  author: Skill Atlas
  version: "0.1.0"
  homepage: https://skillatlas.sh/
---

# Image Generation

Use this skill when an agent needs to generate or edit images.

## Prerequisites

- **OpenRouter API key** — Image generation models are accessed via [OpenRouter](https://openrouter.ai/). You need an OpenRouter API key to use this skill.

This skill is about **getting better images**, not about any single tool. If the environment already provides a nimage tool, SDK, or wrapper, use that. If the agent has an OpenRouter API key but has not been given another image tool, **minibanana** is a good lightweight place to start.

This skill is intentionally biased toward **image quality** rather than minimal prompt length. The main idea is simple:

**Do not throw keyword soup at the model. Direct the image like a creative director.**

## What this skill is for

- Text-to-image generation from scratch
- Reference-guided image generation
- Image editing and compositing
- Product shots, posters, key art, concept art, social creatives, mockups
- Images that require deliberate control over composition, lighting, materials, camera, or text rendering

## Core principles

1. **Prompt quality is usually the biggest lever.** Better prompting often matters more than tiny model changes.
2. **Lead with intent.** Start with a strong verb such as `create`, `render`, `photograph`, `illustrate`, `design`, `edit`, `transform`, `replace`, or `remove`.
3. **Be specific about the visible result.** Subject, scene, composition, lighting, style, and materials should be explicit.
4. **Prefer positive framing.** Describe what should appear, not only what should be excluded.
5. **Use references deliberately.** Assign each reference image a role.
6. **Iterate surgically.** After each attempt, change the fewest prompt parts necessary.
7. **Use structured prompting for complex jobs.** Hybrid prompts with JSON often work very well for multi-element scenes and precise edits.

## Tooling options

Use whatever interface the environment already gives you:

- an existing image tool
- a direct SDK or HTTP client
- a local wrapper already available in the repo
- **`minibanana`** as a lightweight fallback when the agent has an OpenRouter API key but no other image tool

If you do use `minibanana`, first inspect the current CLI behavior in the environment:

```bash
minibanana --help
```

Minimal example:

```bash
minibanana --prompt "A friendly whale" --model "bytedance-seed/seedream-4.5" --out image.png
```

Practical defaults when using `minibanana`:

- Prefer **PNG** for edits, graphics, typography, diagrams, and anything sensitive to JPEG artifacts.
- Prefer **JPEG** when file size matters more than lossless output.
- Put any non-trivial prompt in a file and pass it with e.g. `--prompt @prompt.md`.
- Use repeated image inputs when you need references, and assign each one a role in the prompt.

## The working loop

Always use this loop:

1. **Classify the task**
   - text-to-image
   - reference-guided generation
   - edit / inpaint / remove / replace
   - typography-heavy graphic
   - diagram / infographic

2. **Choose the aspect ratio from the job**
   - `1:1` for avatars, tiles, concept squares
   - `4:5` for social posts and product ads
   - `9:16` for stories, reels, wallpapers
   - `16:9` for cinematic scenes, thumbnails, hero images
   - `21:9` for banners and panorama-style scenes

3. **Choose a model that fits the job**
   - use the user's requested model if they named one
   - otherwise prefer a model family suited to the task

4. **Write the first prompt with strong direction**
   - narrative prompt for simple scenes
   - hybrid narrative + JSON for complex scenes
   - editing prompt with explicit invariants for image edits

5. **Generate and inspect the image**
   - if the model produces multiple output images, **review every single output** before deciding which one(s) to use — do not just pick the first image
   - verify subject
   - verify composition
   - verify lighting
   - verify materials/textures
   - verify text rendering if present
   - verify whether the image actually matches the intended use case

6. **Revise surgically**
   - if composition is wrong, change composition language first
   - if mood is wrong, change lighting and palette first
   - if anatomy is wrong, simplify pose and framing
   - if text is wrong, shorten it and make it more explicit

## Model selection heuristics

Use the model the user explicitly asks for unless there is a strong reason not to. When choosing yourself, use simple task-based heuristics.

### Good current starting points

- **`bytedance-seed/seedream-4.5`**
  - strong visual aesthetics
  - improved editing consistency
  - good portrait refinement
  - stronger small-text rendering than many image models

- **`google/gemini-3-pro-image-preview`**
  - strong multi-image reasoning and blending
  - strong text rendering
  - strong identity preservation across multiple subjects
  - useful for storyboards, composites, and complex scene design

- **`google/gemini-3.1-flash-image-preview`**
  - strong quality-to-speed tradeoff
  - good for iterative editing and quick refinement
  - supports extended aspect ratios on OpenRouter

- **`openai/gpt-5-image`**
  - strong instruction following
  - strong text rendering
  - strong detailed editing

- **`sourceful/riverflow-v2-pro`** and **`sourceful/riverflow-v2-fast`**
  - strong text rendering and graphics-oriented work
  - useful when Sourceful-specific font inputs or super-resolution references are relevant

### Model choice by task

- **Fast iteration / concept exploration:** a faster image model is usually enough
- **High-fidelity editorial / concept art:** favor models known for aesthetics and composition quality
- **Precise edits / multi-image composition:** favor models known for multimodal reasoning
- **Typography-heavy posters / ads / infographics:** favor models with strong text rendering

## Prompt format: choose the right shape

### Use a plain narrative prompt when

- the scene is simple
- you want fast ideation
- you are exploring style directions loosely
- the image does not depend on many separate constraints

### Use a hybrid prompt when

- the request is high stakes
- multiple subjects or layers matter
- references have distinct roles
- there is product, brand, or material specificity
- composition must be tightly controlled
- text rendering matters
- you expect to iterate and patch only specific parts later

**Best default for serious work:**

1. one or two natural-language sentences that state the visual goal clearly
2. a structured JSON block that encodes the exact specification

This often works better than raw JSON alone because the natural-language lead establishes the overall intent, while the JSON gives the model a stable structure.

## Prompt anatomy

A strong image prompt usually covers these elements in roughly this order:

1. **Operation** — create, render, photograph, illustrate, edit, replace, remove, transform
2. **Primary subject** — who or what the image is really about
3. **Action / pose / state** — what the subject is doing
4. **Environment / context** — where the scene takes place
5. **Composition** — shot type, framing, angle, focal point, depth layers
6. **Lighting** — source, direction, softness, contrast, time of day, atmosphere
7. **Style / medium** — editorial photo, fantasy realism, watercolor, 3D render, film still
8. **Materials / textures** — leather, moss-covered stone, polished chrome, tweed, fog, wet pavement
9. **Color palette / grading** — warm neutrals, muted teal, rich contrast, desaturated sci-fi
10. **Text instructions** — exact text, font feel, placement, line count, language
11. **Constraints** — aspect ratio, realism level, keep background, preserve identity, no motion blur
12. **Negative prompt** — only targeted artifact suppression, not a giant trash list

## The simplest good formula

For text-to-image without references:

```text
[Verb] + [Subject] + [Action] + [Location/context] + [Composition] + [Lighting] + [Style] + [Materials/details] + [Output/use-case]
```

Example:

```text
Create a high-end editorial fashion portrait of a confident model wearing a tailored brown dress, sleek boots, and a structured handbag, standing in a statuesque pose against a seamless deep cherry-red studio backdrop. Medium-full shot, center-framed, photographed at a low three-quarter angle with soft cinematic key light and subtle rim light. Shot like a luxury fashion magazine campaign on medium-format analog film with pronounced grain, rich color, and realistic fabric texture.
```

## Prompt like a creative director

Do not stop at nouns. Control the scene deliberately.

#### 1. Direct the composition

Use terms such as:

- extreme close-up
- close-up
- medium shot
- medium-full shot
- wide shot
- aerial view
- top-down
- low angle
- high angle
- over-the-shoulder
- symmetrical framing
- centered composition
- rule-of-thirds placement
- foreground / midground / background layers

#### 2. Direct the camera and lens

Useful language:

- `24mm wide-angle` for environmental scale
- `35mm` for natural cinematic framing
- `50mm` for neutral human perspective
- `85mm portrait lens` for flattering compression
- `macro lens` for product and texture detail
- `shallow depth of field (f/1.8)` for subject separation
- `deep focus` for detailed environments

#### 3. Direct the lighting

Useful language:

- golden hour backlight
- overcast daylight
- soft studio softbox lighting
- three-point lighting
- harsh chiaroscuro lighting
- volumetric god rays
- fog diffusion
- neon edge lighting
- candlelit interior
- wet-surface reflections

#### 4. Direct materiality

This is one of the most underused quality levers. Name surfaces and imperfections.

Examples:

- weathered, cracked, moss-covered stone
- navy blue tweed with visible weave
- brushed aluminum with subtle micro-scratches
- rain-slick asphalt reflecting signage
- matte ceramic with fine glaze variation
- worn leather with creases and patina

#### 5. Direct the color story

Examples:

- muted teal and amber cinematic grading
- warm monochrome neutrals
- deep emerald and gold accents
- pastel candy palette with soft bloom
- high-contrast black-and-white with silver halation

## JSON prompting for high-control jobs

For complex or high-fidelity prompts, use a structured block. This is especially useful for:

- complex scenes with multiple subjects
- product shots with precise materials and layout
- image edits with clear preserve/change rules
- typography-heavy compositions
- iterative workflows where you need to patch one section later

### Hybrid JSON template

````md
Create a polished, high-fidelity image that feels intentional, cinematic, and production-ready.

```json
{
  "task": "text-to-image",
  "goal": "one-sentence visual objective",
  "subject": {
    "primary": "main subject",
    "secondary": ["supporting elements"]
  },
  "scene": {
    "location": "where it takes place",
    "time": "time of day",
    "weather": "weather or atmosphere",
    "story_moment": "what moment is being depicted"
  },
  "composition": {
    "framing": "wide shot / portrait / macro / etc.",
    "camera_angle": "low angle / eye level / aerial / etc.",
    "focus": "what the eye should land on first",
    "depth_layers": ["foreground", "midground", "background"]
  },
  "lighting": {
    "primary": "main light source",
    "secondary": ["secondary light sources"],
    "mood": "desired emotional tone"
  },
  "style": {
    "genre": "photorealistic / fantasy realism / 3D / watercolor / etc.",
    "visual_aesthetic": ["keywords"],
    "rendering": {
      "detail_level": "high",
      "sharpness": "high",
      "dynamic_range": "wide"
    }
  },
  "materials_and_textures": {
    "subject": "surface/material notes",
    "environment": "environment texture notes"
  },
  "color_palette": {
    "dominant": ["main colors"],
    "accents": ["accent colors"]
  },
  "text_rendering": {
    "enabled": false,
    "text": [],
    "placement": "",
    "style": ""
  },
  "technical_preferences": {
    "aspect_ratio": "16:9",
    "lens": "35mm",
    "depth_of_field": "moderate",
    "realism": "high"
  },
  "negative_prompt": ["blurry image", "flat lighting", "text or watermark"]
}
```
````

### Guidance for structured prompting

- Put the **most important constraints first**.
- Keep the hierarchy clean.
- Avoid contradictory instructions like `minimalist` plus `highly cluttered`.
- Keep negative prompts targeted and relevant.
- If the prompt becomes too long and starts failing, shorten it to the essential visual hierarchy.

## Reference-image prompting

Use `--in` for any reference images.

### Best practice: assign each input image a role

When more than one reference image is used, explicitly define what each image contributes.

Good pattern:

```text
Use reference image 1 for the composition and camera angle.
Use reference image 2 for the fabric texture and color palette.
Use reference image 3 for the product silhouette only.
Do not copy the background from references 2 or 3.
```

### Strong multimodal formula

```text
[Reference images] + [role of each reference] + [what must remain unchanged] + [new scenario] + [style and quality target]
```

Example:

```text
Using the first attached image for the room layout and camera position, and the second attached image for the velvet texture and olive-green color, create a high-end interior design render of a reading chair in a sunlit minimalist living room. Keep the composition and scale consistent with the layout reference, but redesign the chair into a premium sculptural form with realistic stitching, soft shadows, and polished oak legs.
```

### Rules for reference use

- Do not say only `use these references`; specify **what to borrow** from each.
- State **what not to copy** when necessary.
- For identity-sensitive edits, say what must remain unchanged: face, pose, camera angle, outfit color, logo placement, product geometry, etc.
- If references conflict, declare the priority order.

## Editing prompts

Editing prompts are different from fresh generation prompts.

### The golden rule for edits

**Be explicit about what changes and what stays exactly the same.**

Weak:

```text
Make this image better.
```

Better:

```text
Remove the man from the background while keeping the street, perspective, lighting, shadows, storefront signage, and camera position unchanged.
```

### Editing formula

```text
[Edit verb] + [specific target] + [exact change] + [what to preserve] + [quality/style target]
```

Examples:

```text
Replace the cloudy sky with a dramatic golden-hour sunset while keeping the building, camera angle, reflections, and street activity unchanged.
```

```text
Transform this product photo into a premium studio advertisement while preserving the exact bottle shape, label wording, brand colors, and front-facing composition.
```

```text
Remove the table lamp from the nightstand. Keep the bed, wall art, shadows, color palette, and image framing identical.
```

### Editing tips

- Name the object to change clearly.
- State preserve rules in plain language.
- For local edits, mention nearby context so the patch blends naturally.
- For realism, tell the model to preserve matching shadows, reflections, perspective, and grain.

## Text rendering and localization

Text in images is much better than it used to be, but it still benefits from very explicit prompting.

### Rules for good text rendering

- Put exact text in **quotes**.
- Keep text short whenever possible.
- State the **number of lines**.
- Specify the **placement**.
- Specify the **font feel** or a recognizable font style.
- Describe the **graphic design context** so the text feels integrated.

Example:

```text
Create a premium skincare advertisement. On the right side of the frame, render three lines of text with exact spelling: "GLOW" on the first line in an elegant flowing brush-script style, "10% OFF" on the second line in a bold block sans-serif style, and "Your First Order" on the third line in a thin minimalist geometric sans-serif. Keep the product jar large and centered-left, with warm studio lighting and clean luxury packaging aesthetics.
```

### Localization prompt pattern

```text
Render the poster text in Korean and Arabic with correct script rendering and natural layout. Keep the brand hierarchy identical, with the Korean text as the main headline and the Arabic text as the supporting line.
```

### Typography tips

- Quote the exact words.
- Keep copy shorter than you think.
- State the visual hierarchy: headline, subhead, caption, badge, CTA.
- For posters, specify whether the text is printed on a physical object, floating in layout space, or cut out of the background.
- If text keeps failing, shorten it and simplify the layout.

## Five prompt frameworks

### 1. Text-to-image without references

Use when starting from nothing.

Formula:

```text
[Subject] + [Action] + [Location/context] + [Composition] + [Lighting] + [Style]
```

### 2. Reference-guided generation

Use when you need consistency or blended inspiration.

Formula:

```text
[Attached references] + [role of each] + [new scenario] + [what to preserve] + [style target]
```

### 3. Conversational image editing

Use when you already have a base image and want to change part of it.

Formula:

```text
[Edit action] + [what changes] + [what stays the same]
```

### 4. Style transfer / composition transfer

Use when one image supplies content and another supplies the look.

Formula:

```text
[Base image content] + [style source] + [what must remain recognizable]
```

### 5. Text-first design prompts

Use for posters, ads, label mockups, and graphics.

Formula:

```text
[Design type] + [layout] + [exact text in quotes] + [font/style guidance] + [placement] + [background/subject]
```

## Advanced prompting tactics

### Put non-negotiables early

The first part of the prompt should contain the things that must be right even if the model ignores the rest.

### Separate must-haves from nice-to-haves

A useful structure is:

- **Must-have:** subject, composition, lighting, text, preserved identity
- **Nice-to-have:** extra atmosphere, tiny props, secondary story details

If quality drops, cut nice-to-haves first.

### Avoid contradiction density

The more conflicting adjectives you pile in, the more generic the result becomes.

Examples of bad pairings:

- minimalist + crowded with detail everywhere
- documentary realism + stylized anime cel shading
- soft diffused fog + razor-sharp hard sunlight everywhere

### Add a narrative moment

A picture gets more interesting when it captures a moment, not just an object.

Examples:

- `the instant before the temple mechanism awakens`
- `mid-step entering the rain`
- `just after the champagne cork pops`
- `the second before sunrise breaks through the clouds`

### Use materiality to escape the generic look

When an image looks synthetic or cheap, the fix is often not `make it realistic`. The fix is naming the materials, imperfections, surfaces, and light behavior.

### Use negative prompts sparingly

Good negative prompts remove common artifacts. Bad negative prompts become a giant bag of unrelated anxieties.

Good:

```text
negative_prompt: ["blurry image", "distorted hands", "flat lighting", "text or watermark"]
```

Less good:

```text
negative_prompt: [dozens of unrelated items that are unlikely to appear anyway]
```

## Symptom -> fix guide

### Problem: composition is wrong

Fix with:

- shot type
- camera angle
- focal subject
- subject placement
- lens choice
- depth layers

### Problem: image looks flat or cheap

Fix with:

- stronger primary light source
- secondary rim or bounce light
- material and surface detail
- realistic shadows/reflections
- color grading direction

### Problem: too busy / no focal point

Fix with:

- one primary subject
- simpler background
- explicit focus target
- fewer secondary objects

### Problem: anatomy or hands are bad

Fix with:

- simpler pose
- fewer visible fingers/hands if hands are not essential
- medium shot instead of extreme close-up of hands
- natural action with clear limb positions

### Problem: text is misspelled or ugly

Fix with:

- shorten copy
- put exact text in quotes
- define line breaks
- specify poster/ad layout
- choose a model with stronger text rendering

### Problem: references are ignored

Fix with:

- reduce the number of references
- assign one explicit role per reference
- state what must be preserved from the base image
- declare priority if references conflict

### Problem: image feels generic

Fix with:

- add a story moment
- add material specificity
- add camera/lens choices
- add atmosphere/weather/time of day
- replace vague style labels with concrete visual direction

## Example high-control prompt

This example shows the general style of prompt that often produces strong results for complex scenes.

````md
Create a cinematic fantasy-realist image with a clear focal point, believable lighting, and rich environmental detail.

```json
{
  "title": "Bioluminescent Jungle Temple at Dawn",
  "style": {
    "genre": "fantasy realism",
    "visual_aesthetic": ["cinematic", "ultra-detailed", "atmospheric", "mythic"]
  },
  "scene": {
    "location": "ancient jungle temple courtyard",
    "environment": "dense tropical rainforest",
    "time_of_day": "early dawn",
    "weather": "light mist after rainfall"
  },
  "composition": {
    "camera_angle": "low three-quarter angle",
    "framing": "wide shot",
    "focus": "central altar and lone explorer",
    "depth_layers": [
      "foreground wet roots and glowing fungi",
      "midground broken steps and altar",
      "background towering ruins and canopy"
    ]
  },
  "lighting": {
    "primary_light_source": "soft golden dawn light through the canopy",
    "secondary_light_sources": [
      "warm lantern glow",
      "subtle bioluminescent cyan glow"
    ],
    "mood": "mysterious, sacred, awe-inspiring"
  },
  "technical_preferences": {
    "aspect_ratio": "16:9",
    "lens": "24mm cinematic wide-angle",
    "realism": "high"
  },
  "negative_prompt": [
    "cartoon style",
    "low detail",
    "flat lighting",
    "text or watermark"
  ]
}
```
````

## Final quality checklist

Before you stop, make sure the image has the following:

- a clear focal point
- composition that matches the use case
- lighting that supports the intended mood
- believable materials and textures
- no obvious artifacting or accidental clutter
- text that is spelled correctly if text is present
- aspect ratio that suits the output channel
- prompt file saved for reproducibility if the task is important

## Minimal agent playbook

When the user asks for an image:

1. infer the deliverable type and aspect ratio
2. choose a suitable image model
3. write the prompt in a file if the request is non-trivial
4. use structured prompting for complex scenes or edits
5. generate once
6. if the model produces multiple output images, **review every single output** before deciding which one(s) to use — do not just pick the first image
7. inspect what is wrong
8. revise only the necessary sections
9. prefer prompt improvement over random model hopping

**IMPORTANT**: state of the art image generation models are expensive. **Check with the user** before revising images.

The fastest path to better image output is usually **clearer direction, cleaner hierarchy, and more deliberate visual language**.
