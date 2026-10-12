---
name: scenario-multi-reference
description: "Use when one image must be composed from several reference pictures through the Scenario MCP server, each lending one thing: the character from one, the place, pose, style, light, palette, material, outfit, or layout from others. Also when a reference leaks into the result (its object, colors, or face showing where it should not) or a reference's role is ignored. Keywords: multi-reference, reference roles, combine references, style reference, pose reference, give each picture a job."
license: MIT
---

# Scenario Multi-Reference Composition

## Overview

A reference image lends everything it shows unless the prompt says otherwise: hand a model a raccoon chef as a style reference and the raccoon walks into the scene. The fix is to give **each picture exactly one job**, then say, for every picture, what **not** to take from it. Four or five pictures, one idea each (a drawing, a photo, a mannequin, a film still, a color swatch), compose into one image that keeps each contribution and nothing else. Connection and the generation loop: see the `scenario` skill. Per-family reference caps and syntax: `scenario-image` lists the image model-family skills. One subject held across many images: `scenario-consistency`. Animating the result: `scenario-video`. Refusals: `scenario-moderation`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Job                | The picture lends            | Typical "not" line                                               |
| ------------------ | ---------------------------- | ---------------------------------------------------------------- |
| Main subject (WHO) | the character, product       | "Use only the idea of a gecko. Do not copy the photo's colors."  |
| Stage (WHERE)      | the place                    | "redrawn as woodblock architecture" when the medium differs      |
| Pose               | the body pose                | "Do not show the mannequin or any wood."                         |
| Angle              | the camera                   | "Do not include the lighthouse."                                 |
| Style              | medium, render, texture      | "Do not include the raccoon, the kitchen, the apron or the pot." |
| Light              | the light only               | "Do not include the flowers or vase."                            |
| Palette            | the only allowed colors      | "No green anywhere."                                             |
| Material           | a surface                    | "Do not show any fish, fins or water."                           |
| Expression         | the mood of a face           | "No human skin, no nose, no ears, no hair."                      |
| Wear               | clothing or armor            | "The cat's own face stays visible; no human face mask."          |
| Inspiration        | a design idea, not the thing | "a gown designed from this jellyfish. Do not show a jellyfish."  |
| Layout             | grid and composition         | "Do not copy the word MONDAY."                                   |

The prompt, one line per picture (the kept prompts wrote Main subject and Stage as WHO and WHERE):

```text
<One sentence naming the medium.> Each reference picture has exactly one job:
Image N (<what it shows>) = <JOB> only. <What it lends, concretely.> Do not <what to leave out>.
...
<Framing: shot size, placement, mood, text rules.>
```

## Rules that held

- **One job per picture.** Two jobs on one card (subject plus palette) blur both. A card kept in the call but unused gets "Image 4 = no job: ignore it completely."
- **One main subject.** Two identities in one run split attention; compose them per `scenario-consistency`.
- **The job most likely to be ignored goes first**, usually Style, with "This is the most important job". A clay scene came back as chrome CG until the Style line moved to the top.
- **Lend concretely.** "Copy its 3D render look, soft materials, warm bounce light" beats "use its style". A palette job names each element's color ("the gecko is Prussian blue with vermilion spots"); "palette only" barely recolors.
- **Settle conflicts between jobs.** Every picture carries more than its job, so a Style card brings its own colors and a subject photo its own fur. With a Palette card, the Style line adds "do not copy its colors", and the subject's colors are named from the swatch. When that recolors something the user cares about (their dog, their product), ask before running; unattended, follow the task instructions, else keep the subject's own colors and report the conflict.
- **Idea, not copy.** When a subject photo must not survive literally: "Use only the idea of a gecko ... Do not copy the photo's pose, lighting, colors or realism."
- **Text** is quoted exactly with "No extra words, no duplicate text"; copy that must be letter-perfect goes to `scenario-text-overlay`.
- **Clean cards.** Plain backgrounds, no readable signs or logos. The user's own pictures are best; generate a missing card with a text-to-image run, one idea per card.

## Worked example: a crayon drawing becomes a film still

Cards: a child's crayon monster (Main subject), a backyard photo (Stage), a wooden mannequin leaping (Pose), a 3D animated film still of a raccoon chef (Style).

1. `upload_asset` each card, then `upload_asset_complete` (see `scenario`). Keep the asset ids in the order you will number them.
2. `recommend` with `capability="img2img"`, `features=["referenceImages"]` (keeps only members exposing that exact field; drop it to see members that name the slot differently), and the user's own words as `prompt`. Handle `next_step` as `scenario` directs.
3. `model_schema_get` on the pick. Read: the reference field's cap (four or five cards fit the leading members at authoring time, up to ten on some), `array: true`, how the description says the prompt addresses references (by order as "Image 1", or by tags such as `@Image1` on some families), the sizing family, and the quality tier. When the schema offers a dedicated slot for a job (a style-reference field, a pose control), put that card there instead of in the reference array (`scenario-consistency`), and read the field description for how the prompt refers to it, since prompt numbering follows the array.
4. `model_run` with `dry_run=true` (top-level, beside `model_id`, never inside `parameters`) and the schema's own names, for example `parameters={"prompt": "<below>", "referenceImages": ["asset_monster", "asset_yard", "asset_mannequin", "asset_raccoon"], "quality": "high"}` plus its sizing fields. Quote the user the total, any cards still to generate and the film included when one is wanted (a dry run rejects a payload missing its required image, so price against any uploaded picture, a small stand-in when no card exists yet), and run nothing paid until they agree (unattended, launch only inside a budget the task states; otherwise stop and report the quote). Then the same call with `wait=false`, `jobs_wait`, and `asset_display`.

```text
A still frame from a 3D animated family feature film. Each reference picture has exactly one job:
Image 1 (child's crayon drawing) = WHO. Turn this crayon monster into a soft, plush 3D animated character: round purple body, three uneven eyes, spiky green hair, tiny orange legs, big toothy smile. Keep its lopsided, hand-drawn charm.
Image 2 (backyard photo) = WHERE. Use this exact backyard: lawn, wooden fence, red hose, blue kiddie pool, swing set, lemon tree.
Image 3 (wooden mannequin) = POSE only. The monster leaps mid-air with both arms thrown up and one knee raised, exactly like the mannequin. Do not show the mannequin or any wood.
Image 4 (raccoon chef frame) = STYLE only. Copy its 3D render look, soft materials, warm bounce light and rich color. Do not include the raccoon, the kitchen, the apron or the pot.
Wide shot, the monster in the center above the lawn, afternoon sun, joyful.
```

5. **Check every picture for a leak** (below). Fix by tightening that picture's line and running again, never by retouching.
6. To animate it, hand the result to `scenario-video` as the first frame. The film prompt carries no jobs, only motion, camera, and sound: the frame already holds every job.

Seven more kept prompts across claymation, product ad, woodblock print, fashion editorial, pixel art, tilt-shift miniature, and risograph poster, each with its film prompt: [references/prompt-patterns.md](references/prompt-patterns.md).

## Leak check before keeping

For each picture, ask two questions: is its job visible, and is anything else from it visible?

- Pose and Angle: no mannequin, no wood, no prop from the sketch.
- Style: none of the style reference's own subject, set, or objects.
- Expression: the mood moved, the face did not (no human nose or skin on a toaster).
- Layout: the grid moved, the reference's own words did not.
- Palette: no color outside the swatch.

Before rewriting a line for an ignored job, `asset_get` the output: `metadata.referenceImages` lists what the run consumed, and a reference sent as a bare string where the schema says `array: true` was dropped silently, so no wording brings its job back.

## Common mistakes

- **The main subject copied the photo.** A green gecko photo came back as the same green gecko in a woodblock print. Put Style first, use "only the idea of", and make the palette strict.
- **A logo by accident.** Red, white and blue swooshes on generated billboards read as a soda brand: the image-to-video model refused the frame, and the image editor then refused it as input. Say what billboards and signs show (waves, clouds, cranes).
- **Brands in a reference.** A street photo with real shop signs was refused as a reference. Regenerate the card with "invented, blank signs, no logos".
- **A protected design named in the prompt.** A famous chair named outright was refused. Describe an original design instead.
- **A garment blocked by the safety filter.** A translucent gown was refused; "opaque, fully covered, high-necked" passed.
- **Drift in the film.** A guitar changed color mid-clip. Ask for "almost static", list what must not change, and move only what should.
- **Hardcoding a model id or price.** Discover with `recommend`, read caps off `model_schema_get`, price with `dry_run=true`.
