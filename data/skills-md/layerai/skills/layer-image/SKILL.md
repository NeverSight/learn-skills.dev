---
name: layer-image
description: "Use when generating a still image with Layer: concept art, key art, illustrations, marketing images, icons, or any text-to-image run. Also when a prompt is not landing, when the aspect ratio or resolution is wrong, when a style or pose reference should steer the result, when readable text must appear in the image, or when several images must share one look. Keywords: txt2img, text to image, prompt, aspect ratio, negative prompt, style reference, seed."
license: MIT
---

# Layer Image Generation

## Overview

The loop is the one the `layer` skill teaches: `list_base_models` with
`filter.use_case: "text_to_image"`, `get_base_model`, estimate, execute, poll. What separates a
usable image from a near miss is the prompt and the per-model contract, not the model choice, which
the curated ranking already handles.

Editing an image that already exists is a different use case with different rules: see
`layer-image-editing`. Sprites, icons, and game UI have their own constraints: see
`layer-game-assets`. Holding one look across a set: see `layer-reference-sets`.

If a sibling skill named here is missing from your available skills, ask the user to install it
(`npx skills add layerai/skills --skill <name>`); unattended, proceed from tool schemas and flag the
gap.

## What a prompt must name

A model fills every gap you leave, and it fills it with the most average answer in its training data.
Each of these is a gap worth closing, in roughly this order of impact:

1. **Subject**, concretely. "A dwarf blacksmith" beats "a fantasy character".
2. **Style register**, as a production term rather than an artist's name: hand-painted, cel-shaded,
   flat vector, painterly semi-realism, stylised PBR render, gouache, 90s airbrush.
3. **Shot and framing**: full body, three-quarter portrait, top-down, isometric, extreme close-up.
   This is the single most common omission and the most common cause of a reroll.
4. **Lighting**: key direction, hardness, time of day, practical sources. "Rim-lit from behind,
   warm forge glow below" is a decision; "good lighting" is not.
5. **Palette**, named or constrained: "muted teal and rust, two accent hues only".
6. **Background treatment**: flat colour, isolated on transparent, environment implied, full scene.
   Assets that will be composited need this stated, not assumed.

Leave out what does not matter. A prompt that specifies everything specifies nothing, because the
model weights the whole string and dilutes the parts you cared about.

## Sizing, and the fields that differ

Aspect ratio and resolution are per-model contracts. Two models that both do text-to-image disagree
about whether they take an aspect ratio string, explicit width and height, or a fixed set of named
sizes, so read `get_base_model` rather than reusing the shape that worked last time.

When the deliverable has a fixed ratio, filter for it. `filter.capabilities` is an object of
booleans, not a list of names, so it is `{portrait_9_16: true}`: `square`, `portrait_9_16`,
`landscape_16_9`, or `multiple_aspect_ratios` when the user will want several crops from one setup.
Set only what the task needs, since `false` filters rather than defaults.

## Negatives, references, and seeds

`negative_prompt` is a capability, not a universal parameter. Filter for it when the run needs one,
and do not send it blindly: on a model without it, it is either ignored or an error, and on a model
with it, a long negative list costs more than it saves. Reach for it to suppress one specific,
recurring defect.

Three reference types steer a text-to-image run, all passed through `guidance_files` after an upload:

- `reference_image` with the `image_editing` capability, for "reproduce this subject" and for new
  art that has to match a reference. `style_reference` is the older style-only transfer: it moves a
  look across, it does not carry a subject, so reaching for it to hold a character is the usual
  reason a cast drifts.
- `pose` with `character_pose`, for "put the character in this position".
- `depth`, `canny`, `lineart`, or `scribble` with `structure` or `outline`, for "keep this layout".

A reference is worth more than three adjectives. When a user has an image and is describing it in
words, upload the image.

Seeds make a run repeatable, which matters when iterating: hold the seed and change one clause to see
what that clause actually does. They do not make two different prompts consistent with each other.
For a look held across a set, train it: see `layer-reference-sets`.

## Text in the image

Most image models garble text. When the deliverable needs readable words, filter for a model whose
description claims typography, keep the string short, and put it in quotes in the prompt. If it still
fails after two attempts, stop rerolling: generate the art clean and composite the text, which is
also what makes it editable and localisable later.

## Worked example

"Key art for our roguelike, 16:9, for the Steam page."

1. `list_base_models` with `filter.use_case: "text_to_image"` and
   `filter.capabilities: {landscape_16_9: true}`. Take the first result.
2. `get_base_model`, which reports the sizing fields it accepts and whether it needs a trigger word.
3. Compose against the six points above: "Hooded rogue mid-leap over a collapsing stone bridge, seen
   three-quarter from below, hand-painted semi-realism, hard moonlight from the upper left with cold
   blue rim light, warm torchlight pooling below, muted slate and amber, storm-lit ruins receding
   into fog behind."
4. `estimate_forge_price` with `batch_size: 4`, to see four compositions of one idea.
5. Under 20 CUs, so execute, then poll at `poll_interval_seconds`.
6. Present all four. Pick one, hold its seed, and iterate one clause at a time.

## Common mistakes

- Omitting shot and framing, then rerolling the same prompt hoping for a different crop.
- Describing a reference image in words instead of uploading it.
- Sending `negative_prompt` to a model that does not declare the capability.
- Reusing the sizing fields from a different model rather than reading `get_base_model`.
- Using `batch_size` for N different assets. It makes variations of one prompt.
- Chasing readable text through a sixth reroll instead of compositing it.
- Stacking five style adjectives, which averages them into none of them.
