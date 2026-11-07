---
name: image-generation
description: Generate original imagery with the generate_image host tool, such as illustrations, scenes, textures, hero objects, look plates for storyboards and transparent cut-outs. Not for layouts, logos, exact copy, charts or product UI.
---

# Image generation

The image model makes artwork the HTML path cannot: an engraving, a painterly sky, a hero object, a
scene, a texture, a character. Anything with the logo or exact copy is built in HTML on brand, not
left to the image model: generate the picture here without words or marks, then lay the real type
and the real logo over it in `stills` (or `thumbnails`, or a HyperFrames scene).

| The ask | Route |
| --- | --- |
| Type-forward layout, an ad with copy, a slide | `stills` (HTML, exact, free) |
| A chart, a diagram, product UI | `data-viz`, a real screenshot, or HTML |
| Illustration, scene, texture, hero object, campaign concept, "explore directions" | here |
| A finished ad around a generated illustration | here, then `stills` for copy, logo and every size |

Say so when it is the wrong tool. When a film's or an ad's proof is that the surfaces are real (real
UI, real numbers, real people), generated pixels undermine it, whoever offered the idea.

## Generate

```text
generate_image(prompt="…", sandbox_path="projects/<slug>/art/hero.png",
               size="1536x1024", quality="low", n=3)
```

The tool runs on the host, so no key ever enters the sandbox; never call a provider API from a
script. It writes the files (`_0`, `_1` suffixes when `n` > 1) and returns their paths. `model`,
`size`, `quality`, `n`, `background`, `output_format` and any extra `params` pass straight through to
the provider, which validates them and explains a refusal in its own words: read the message and
adjust rather than guessing from memory what is allowed. When the deployment makes images with
Google, `size` becomes the nearest aspect ratio, `quality="high"` asks for 2K, and there is no
transparent background: generate on a plain ground and cut the subject out. Every call spends money: explore at low
quality, finish once at high.

The prompt is the leverage: concrete subject, action, medium, light, composition, and "no text, no
words, no letters, no logos". Prompting craft, schemas for complex scenes and the failure modes:
[references/craft.md](references/craft.md).

## Transparent cut-outs

For a subject that sits on something else (a layered design, a sticker, an object reused across
grounds), generate a real cut-out rather than masking a square later:

```text
generate_image(prompt="… Isolated object on fully transparent alpha; no backdrop, no floor, no cast
shadow, no text, no watermark.", sandbox_path="projects/<slug>/art/cutout.png",
               background="transparent", output_format="png")
```

The prompt outranks the flag: describe a backdrop and the model paints it, and you get an opaque
rectangle. The tool reports whether each file really has alpha. Report that to the person as it is;
never call a cut-out transparent unless the receipt says so. On a missing-alpha receipt, strip the
backdrop language and re-prompt; the same words give the same plate. For an existing photo, remove the
background with `hyperframes remove-background` instead (see `media-use`).

## Ground it in the brand

Read `/workspace/brand/graphic-language.md` and `voice.md` before writing a prompt. Describe the
palette in words and hex from `/workspace/brand/tokens.json` ("a calm paper-coloured ground, one small
area of the signal colour #…, no other saturated colour"), the mood the voice describes, and a visual
idea tied to the subject. A campaign illustration can depart from the brand's graphic system; it
still follows its voice. Never generate the logo, a wordmark or any real mark: models render fake
letterforms. Composite the real SVG afterwards.

**Generate the surface, composite the truth.** When a deliverable needs photoreal pixels and real
type or artwork (merchandise, a device screen, a poster in a scene), generate the blank surface
("large flat empty area, no print, no text, no logo"), then composite the verified artwork onto it with
`image-ops --composite` or an HTML layer.

## Look before delivery (two rounds at most)

Generation is a slot machine: look at every result, and do not loop forever.

1. **Explore cheap.** Two or three prompt directions at low quality, `n=2` or `3`; tile them into one
   sheet (`node /workspace/tools/review-thumb.mjs --sheet ...`) and `look` against
   [references/brand-image-rubric.md](references/brand-image-rubric.md). Name per variant what works,
   what fails and the fix; if every variant fails the same way, change the prompt, not the seed.
2. **Regenerate only for a real defect** (garbled text or marks, an uncut plate or halo, broken
   anatomy, off-brand mood). Polish is not a reason to loop.
3. **One high-quality final** of the chosen direction. If two correction rounds still leave a
   blocking defect, stop and say what is blocking rather than ship it.
4. **Compose and gate.** Hand the final to `stills` (or the film) for type, logo and sizes, lint the
   composition, look at the composed result, then deliver.

A revision to an approved image is one regeneration at the approved quality, or a deterministic edit
(`image-ops`, `stills`).

## Exploring a campaign

State two to four directions in one line each (the visual idea, the medium, the mood), probe each
cheaply, look at them side by side, then recommend one with the reason and show the runners-up before
spending on a final. Say what the exploration cost (variants times quality).

## Icons and marks

Generation can explore icon directions; it never produces the final small icon. Ask for flat,
one-colour, high-contrast silhouettes without text, pick a direction, then rebuild it as a vector on
the brand's grid and test it at 24, 48 and 300 px beside the existing set. When an approved generated
mark must become an SVG, trace it and verify the trace against the raster (render it back, stack,
diff); do not redraw it by eye.
