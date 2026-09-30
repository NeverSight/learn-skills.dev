---
name: z-image-prompt
description: Write, lint and deliver prompts for Z-Image Turbo (Z Image Turbo 1.0, "ZIT") from Tongyi-MAI (Alibaba), in English or Chinese, then hand over the right settings for Draw Things, Diffusers, ComfyUI or the official Hugging Face Space. Use this skill whenever the user mentions Z-Image, Z Image Turbo, ZIT, Tongyi-MAI or Tongyi's image model, or wants an image prompt for it, even if they never say the word "prompt". It covers the official prompt enhancer's rules, text rendering in quotes, bilingual prompts, the 512-token window, official resolutions, sampler settings and iteration.
---

# Z-Image Turbo prompting

Z-Image is Tongyi-MAI's 6-billion-parameter single-stream diffusion transformer (Apache-2.0).
**Z-Image Turbo** is its distilled checkpoint: 8 function evaluations, guidance off, strong at
photorealism and at rendering English and Chinese text. Its text encoder is Qwen3 4B (Draw Things
ships it as Qwen3-VL 4B Instruct). Everything here comes from Tongyi-MAI's own sources, listed at the
end. Companion files, with paths relative to this skill's folder:

- `scripts/lint_prompt.py` — lints a prompt (tokens against the 504-token budget, quoted text, meta tags, similes, negation, hedges, weighting syntax, instructions); English and Chinese.
- `references/official-guidance.md` — the prompt enhancer's rules in English, the encoder template, the official examples' shape, settings and resolution tiers, with sources.

## 0. Facts that decide how you prompt

1. **The prompt is a single user turn and nothing else.** The reference pipeline wraps it as `<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n`, with no system prompt; Draw Things does the same. The model reads a finished description, so write one.
2. **504 tokens.** The reference pipeline cuts template plus prompt at 512 tokens, leaving 504 for the prompt. Draw Things does not cut, but the model was trained on that window. The linter counts exactly once the tokenizer is fetched.
3. **Turbo is guidance-free.** `guidance_scale=0.0` in Diffusers, Text Guidance 1 in Draw Things. The negative prompt does nothing, and negation words turn into content: say what you want, never what you do not want.
4. **Nothing expands the prompt, except the official Space.** Its optional prompt enhancer is an LLM with a system prompt (`pe.py`); this skill applies the same rules, so always hand over the full description. In Draw Things, Diffusers and ComfyUI your text reaches the encoder as written.
5. **English and Chinese are both first-class.** Most official examples are Chinese, one is English, and text renders in both. Write in the user's language unless the text to render or a cultural subject suggests the other; never translate text that must appear in the image.

## 1. Read the brief

Pull out the subject, the count, the action or state, named things (people, places, brands, IP),
colors, the exact text to render and its language, the medium, and the format (aspect ratio, size).
Ask only when a missing item blocks you.

## 2. Write the prompt: the enhancer's rules

The official enhancer turns any input into "the final visual description" in four steps. Follow them
by hand (paraphrased from `pe.py`; the original is Chinese):

1. **Lock the core.** Subject, quantity, action, state, and any named IP, color or text in the brief are fixed. Keep them exactly.
2. **Reason when the brief is a question.** If it asks what something is, asks for a design, or asks how to solve something, first work out a complete, concrete answer that can be drawn, then describe that answer.
3. **Add professional aesthetic and realistic detail.** State the composition, the light and atmosphere, the materials and textures, the color scheme, and a layered space (foreground, middle ground, background).
4. **Handle text precisely.** Transcribe every word that must appear, exactly, inside English double quotes (`"..."`). For posters, menus and UI, describe all the text with its typeface and layout. For signs, road signs and screens, give the content, position, size and material. Text you add yourself (a chart, a label) follows the same rule. With no text in the picture, spend the words on visual detail.

Then the tone rule: the description is **objective and concrete**. No metaphors, no emotional
rhetoric, no meta tags such as "8K" or "masterpiece", no drawing instructions.

How the official examples are built, which is the shape to copy:

- **Picture type first**: "A vertical digital illustration depicting...", "a medium-shot phone selfie photo...", "a fictional movie poster...".
- **Subject and its attributes next**, then its surroundings, from near to far. Each person or object gets its own clothes, colors and props in its own clause.
- **Photographic or stylistic attributes last**, as a compact run: photo type, lighting, shadows, dominant palette, genre, depth of field, what is in focus. The README's Chinese example ends like that ("photograph, natural light, soft shadows, a neutral palette of navy and cream, casual fashion photography, medium depth of field...").
- **Length follows the brief.** The examples run from one sentence to about 300 words; a single subject usually needs 80 to 200 words, a poster with a lot of text more.
- **One paragraph**, plain text, no JSON, no bullets, no weighting syntax.

Commit to one value per attribute ("or", "maybe", "various" make the model draw both or neither), and
place things with grounded phrases ("in the lower left", "behind her", "along the top edge").

### Lint

```bash
python3 scripts/lint_prompt.py --fetch-tokenizer   # once: Z-Image-Turbo's tokenizer from Hugging Face, ~4.4 MB
python3 scripts/lint_prompt.py prompt.txt
```

It reports the exact token count against 504 (or an estimate without the tokenizer) and flags
instructions, meta phrases, negative-prompt markers, weighting syntax, negation, hedges, similes,
meta and quality tags, text cues without quotes, markdown and missing medium words. Findings (`-`)
are fixes; hints (`~`) are for judgement.

## 3. Settings

| Setting | Value | Source |
|---|---|---|
| Steps | 8 (Diffusers: `num_inference_steps=9`, which is 8 transformer passes) | README, Space |
| Guidance | off: `guidance_scale=0.0`; Text Guidance 1 in Draw Things | README, `inference.py` config |
| Negative prompt | none (Draw Things' preset leaves a single space) | README; `configs/z-image-turbo-1.0` |
| Shift | 3.0, fixed | Space default; Draw Things preset |
| Sampler | Draw Things: UniPC Trailing (preset); trailing samplers in general | Draw Things preset and model note |
| Size | 512 to 2048 per side, official tiers below | Space `RES_CHOICES` |

Official resolution tiers (Space). Draw Things needs multiples of 64, so it takes the entries that
already are, or the nearest multiple of 64 at the same ratio:

| Ratio | 1024 tier | 1280 tier | 1536 tier |
|---|---|---|---|
| 1:1 | 1024x1024 | 1280x1280 | 1536x1536 |
| 3:2 / 2:3 | 1248x832 | 1536x1024 | 1872x1248 |
| 4:3 / 3:4 | 1152x864 | 1472x1104 | 1728x1296 |
| 16:9 / 9:16 | 1280x720 | 1536x864 | 2048x1152 |
| 21:9 / 9:21 | 1344x576 | 1680x720 | 2016x864 |

Swap width and height for the portrait ratio. Draw Things-ready picks: 1024x1024, 1536x1536,
1536x1024, 1024x1536, 2048x1152, 1152x2048.

The non-distilled Z-Image base model is different: 28 to 50 steps, guidance 3 to 5, and negative
prompts recommended. Do not carry those settings over to Turbo.

## 4. Deliver

- **Draw Things app**: paste the prompt, leave the negative prompt empty, Model "Z Image Turbo 1.0", Steps 8, Text Guidance 1, Shift 3 with resolution-dependent shift off, UniPC Trailing, a size from the table. Hand over settings in this shape:

  ```
  Model: Z Image Turbo 1.0   Size: 1536x1024   Steps: 8   Text Guidance: 1
  Shift: 3 (resolution-dependent off)   Sampler: UniPC Trailing   Negative: empty   Seed: any
  ```

- **Draw Things API server** (no pasting): save the prompt to a `.txt` file and render it with the `drawthings` skill, recipe `z-image-turbo`, which carries these settings.
- **Draw Things script** (images land in the open project): `pipeline.run({configuration, prompt})` with `model: "z_image_turbo_1.0_q8p.ckpt"`, `steps: 8`, `guidanceScale: 1`, `shift: 3`, `sampler: 17` (UniPC Trailing).
- **Diffusers**: `ZImagePipeline.from_pretrained("Tongyi-MAI/Z-Image-Turbo")`, then `pipe(prompt=..., height=H, width=W, num_inference_steps=9, guidance_scale=0.0)`.
- **Official Space**: turn the prompt enhancer off when you paste a full description, or it rewrites it a second time.

## 5. Look, then iterate

Change one thing per round and keep the schedule (steps, shift, sampler, size) fixed while you work on
the words.

- **Text wrong**: shorten the quoted string, split long copy into separate quoted strings, give each its position, typeface and size, and reduce competing detail around it.
- **Generic or flat picture**: add what the enhancer adds: a concrete light source and direction, the material of the main surfaces, a named palette, foreground and background layers.
- **Something appears that was never asked for**: look for a simile or a second mention and replace it with a plain description.
- **Style drifts**: put the picture type and medium in the first words and close with the style attributes.
- **Cut ending ignored**: you passed 504 tokens; cut the middle, not the closing attributes.

## 6. Traps

- A negative prompt on Turbo does nothing; guidance above 1 fights the distillation.
- `(word:1.3)`, `[word]` and `--no` are plain text to the encoder.
- "8K", "masterpiece", "best quality", "award winning" are the enhancer's forbidden meta tags.
- Text left out of double quotes may render as garbage or not at all.
- Settings of the base model (50 steps, CFG 4, negative prompts) on Turbo.

## 7. Two compact examples

**Photograph (3:2):**

```
A color documentary photograph, wide shot from across a wet street at dusk: a small flower stall on a corner in Lisbon, its green metal awning lit from inside by a single warm bulb. Buckets of red carnations, white lilies and yellow mimosa stand in two rows on the pavement in front of the stall. The florist, a woman in her sixties with short grey hair, a navy cardigan and a canvas apron, wraps a bouquet in brown paper at a wooden counter. Behind the stall, a yellow tram passes on the right, slightly motion-blurred, and pastel building facades rise into a deep blue sky. Warm tungsten light against blue dusk, reflections of the bulb on the wet cobblestones, 35mm lens, medium depth of field, the florist in sharp focus, natural colors, fine grain.
```

**Poster with text (2:3):**

```
A vertical flat vector poster for a bakery's opening day, printed on cream paper. A large golden croissant, drawn with thick brown outlines and two flat shades of amber, fills the middle of the poster at a slight diagonal. Across the top, the title "PANE & CO." is set in heavy black slab-serif capitals, centered, spanning the full width. Below the croissant, a line of medium red sans-serif capitals reads "GRAND OPENING", and under it smaller black text reads "SATURDAY 9 AM, VIA ROMA 12". Wide cream margins, a thin red border inset from the edges, three colors only: cream, amber and black with red accents, mid-century commercial print style.
```

## Sources

- Tongyi-MAI/Z-Image repository: `README.md` (model family, Turbo settings, base-model settings, examples), `src/zimage/pipeline.py` (chat template, 512-token window), `src/config/inference.py` (defaults).
- Tongyi-MAI/Z-Image-Turbo Hugging Face Space: `pe.py` (prompt enhancer system prompt), `app.py` (resolution tiers, shift, steps, example prompts); model card and tokenizer on Hugging Face.
- Draw Things: `configs/z-image-turbo-1.0/metadata.json` in `drawthingsai/community-models` (official preset), the Z Image Turbo entries in `Libraries/ModelZoo/Sources/ModelZoo.swift` and the `zImage` text template in `Libraries/LocalImageGenerator/Sources/LocalImageGenerator.swift` in `drawthingsai/draw-things-community`.
