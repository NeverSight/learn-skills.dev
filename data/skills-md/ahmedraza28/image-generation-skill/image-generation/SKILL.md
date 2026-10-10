---
name: image-generation
description: Best practices for prompting any text-to-image model (e.g. Imagen, Gemini Image, GPT Image, DALL·E, Stable Diffusion, Flux, Ideogram, Leonardo, Midjourney) to produce predictable, production-quality images. Use this skill whenever the task involves calling an image generation API, generating images programmatically, writing or revising prompts for image models, producing illustrations / photos / logos / posters / mockups / infographics / UI shots with AI, or debugging poor image output. Apply this even when the user just says "generate an image of X" — well-structured prompts dramatically outperform terse ones across every current model, and the cost of a bad prompt is almost always paid in retries.
---

# Image Generation

A model-agnostic guide for prompting modern text-to-image models well. Optimized for text→image (generating from scratch); the same principles transfer to image editing.

> **The single most important rule:** Describe a scene in coherent prose. Do **not** list keywords. Modern image models are language models with vision — a paragraph that reads like a director's note will outperform a comma-separated string of tags every time.

A weak prompt: `cat, cyberpunk, neon, 4k, masterpiece, trending on artstation`

A strong prompt: `A photorealistic close-up of a black cat sitting on a rain-slick Tokyo side street at night. Neon signs in pink and cyan reflect off wet asphalt and the cat's fur. Shot on a 50mm lens at f/1.8, shallow depth of field, the background blurred into soft bokeh.`

Both describe roughly the same idea. Only one will reliably produce what you want.

---

## The skeleton

Most strong prompts compose six elements, in roughly this order. Not all are required for every image, but if output is wrong, the missing element is usually one of these.

1. **Subject** — what / who is the focus, in concrete terms (age, materials, expression, posture).
2. **Action / state** — what they are doing, or what relationship they hold to the scene.
3. **Setting / context** — where it takes place, including background detail and time of day.
4. **Composition** — framing (close-up, wide, top-down), camera angle (eye-level, low-angle, 45°), and what occupies the frame.
5. **Lighting & mood** — direction, quality, color temperature, atmosphere.
6. **Style / medium** — photo vs illustration vs 3D render vs vector, plus stylistic anchors (film stock, art movement, era).

**Reusable template:**

```
A [style/medium] [shot type] of [subject], [action/expression], in [setting].
[Composition detail]. Lit by [lighting], creating a [mood] atmosphere.
[Stylistic anchors — lens, film, art reference, color grading].
[Aspect ratio if relevant].
```

When prompts get long or complex, break them into short labeled segments or line breaks rather than one runaway paragraph. The model parses structured prose more reliably than walls of text.

---

## Vocabulary that earns its keep

Image models were trained on captioned images from photography, film, design, and art communities — so they speak that vocabulary fluently. Use it.

**Photography (for realism):** `35mm film`, `85mm portrait lens`, `macro lens`, `wide-angle`, `shallow depth of field`, `bokeh`, `golden hour`, `blue hour`, `overcast diffused light`, `three-point softbox`, `chiaroscuro`, `Rembrandt lighting`, `backlit`, `silhouette`, `eye-level`, `low-angle`, `bird's-eye view`, `Dutch tilt`, `Fujifilm color science`, `Kodak Portra 400`, `disposable camera flash`, `medium-format analog`, `cinematic color grading`, `muted teal tones`, `subtle film grain`.

**Illustration / design:** `flat design`, `line art`, `cel-shaded`, `cross-hatching`, `watercolor`, `gouache`, `ink wash`, `vector illustration`, `isometric`, `3D render`, `claymation`, `pixel art`, `risograph`, `screen print`, `kawaii`, `Studio Ghibli-inspired`, `Bauhaus`, `mid-century modern`, `Art Deco`, `Memphis style`.

**Materials & texture:** `matte ceramic`, `brushed aluminum`, `worn leather`, `wet asphalt`, `frosted glass`, `silk`, `tweed`, `velvet`, `polished concrete`, `weathered`, `iridescent`, `subsurface scattering`, `PBR materials`.

**Composition shorthand:** `rule of thirds`, `centered with negative space on the left`, `subject occupies foreground, blurred environment behind`, `extreme close-up`, `medium shot`, `full body`, `hero shot`, `over-the-shoulder`.

You don't need to memorize all of these; you need to remember that *being specific in the right vocabulary* is what unlocks the model. "Dramatic light" is weak; "low-angle key light from camera-left, deep shadows on the right side of the face, faint rim light from a window behind the subject" is strong.

---

## Use positive framing

Describe what you want, not what you don't want. Many models handle negation poorly — saying "no cars" can make the model render cars.

| Weak (negation) | Strong (positive) |
| --- | --- |
| "a street with no cars" | "an empty pedestrian street" |
| "not cartoonish" | "photorealistic, with natural skin texture and pores" |
| "no extra people" | "a single figure alone in the frame" |
| "not blurry" | "sharp focus throughout, deep depth of field" |

The exception: hard exclusions like `no watermark`, `no logos`, `no extra text`, `no trademarks`. These tend to be respected. Stack them as constraints at the **end** of the prompt.

---

## Mode-specific patterns

Different output types reward different prompt shapes. Use these as starting templates.

### Photorealistic scenes

Lead with the word **photorealistic** (or `real photograph`, `taken on a real camera`, `35mm film`). This is the single strongest lever for triggering the model's photo mode. Then specify lens, lighting, and texture detail.

```
A photorealistic [shot type] of [subject], [expression/action], in [environment].
[Lighting: source, direction, quality, time of day].
Captured with a [camera/lens], [depth-of-field cue], [grain or color cue].
[Mood adjective] atmosphere.
```

For believability, ask explicitly for imperfections: skin pores, fabric wear, dust, grain, slight asymmetry. "Honest and unposed" and "everyday detail" are powerful phrases. Avoid words that imply over-retouching (`flawless`, `glossy`, `studio polish`) unless that's what you want.

### Stylized illustration / stickers / icons

Be explicit about line quality, shading, and palette. Most models cannot generate transparent backgrounds — instead, ask for `a plain white background` and remove it downstream.

```
A [style] illustration of [subject], featuring [key visual traits] in a [palette].
[Line style: bold clean outlines / hand-drawn / no outlines].
[Shading: cel-shading / flat colors / soft gradients].
The background is [solid color, usually white].
```

### Logos and brand marks

Constraints matter more than description. Ask for clean shapes, balanced negative space, and scalability. Generate multiple variants in one call (`n=4` if the API supports it) and pick.

```
Create an original, non-infringing logo for [brand], [one-line brand personality].
Clean vector-like shapes, strong silhouette, balanced negative space.
Favor simplicity over detail so it reads at small and large sizes.
[Color scheme]. [Flat / minimal strokes / no gradients].
Plain background, generous padding, single centered mark.
No watermarks, no trademarks.
```

### Text in images (the hardest subproblem)

Text rendering is where image models most often fail. Good prompts dramatically improve hit rate.

**Rules that consistently help:**

- Put the literal text in **straight double quotes**: `the words "Daily Grind"`. Many models will render quoted text far more accurately than unquoted.
- Spell unusual or brand names letter-by-letter on a second pass if the first attempt mangles them: `the brand name "Ployo" — spelled P-L-O-Y-O`.
- Specify font character explicitly: `bold sans-serif`, `clean geometric sans-serif like Futura`, `flowing brush script`, `slab serif`, `condensed display font`. Don't expect a specific named font to render exactly, but the family/style cue strongly biases the result.
- State placement, color, size, and contrast: `centered, white text on a black band at the bottom third, large display size`.
- Demand verbatim rendering with `(EXACT, verbatim, no extra characters)` after the quoted text. Add `Ensure text appears once and is perfectly legible` as a separate sentence.
- Keep the text **short**. Single words and 2–4 word phrases render most reliably. Paragraphs of body copy will degrade.
- For text-heavy outputs (posters, infographics, slides), use the highest available `quality` / `image_size` / `resolution` setting. Small text needs pixels.
- Some models support a "thinking" or "high reasoning" mode for image generation — turn it on for text-heavy outputs if available.

### Product mockups and commercial photography

```
A high-resolution, studio-lit product photograph of [product, materials],
on [background surface]. [Lighting setup, e.g., three-point softbox]
to [purpose, e.g., create soft diffused highlights and eliminate harsh shadows].
Camera angle: [angle] to showcase [feature].
Ultra-realistic, sharp focus on [key detail].
[Aspect ratio].
```

### Infographics, diagrams, and structured visuals

Treat the prompt as an **artifact spec**, not an illustration request. Name the deliverable, define the canvas, list the components and labels exactly, describe the visual language. Specify what should **not** be there (no decorative clutter, no stock-photo treatment).

For dense layouts, use the highest quality setting available, and prefer landscape canvases (16:9, 3:2) for slide-style outputs. List required labels verbatim in quotes — the model will treat them as text-in-image and try to render them faithfully.

### Minimalist / negative-space layouts

Useful when something else (a headline, a product) will be composited or overlaid downstream.

```
A minimalist composition featuring [subject] positioned in the [corner/edge]
of the frame. The vast majority of the composition is [empty color/texture],
creating significant negative space. [Lighting]. [Aspect ratio].
```

### UI mockups

Describe the product as if it already exists. Avoid concept-art language. Focus on layout, hierarchy, spacing, real interface elements. Place the result inside a device frame if you need realistic context: `Place the UI inside an iPhone frame`.

---

## Multi-image / reference inputs

Modern models accept reference images alongside the text prompt — for character consistency, style transfer, product placement, or composition. Different models cap the count differently (commonly 3–14). Index every input and describe its role explicitly.

**Pattern:**

```
[Reference image 1: description of what it provides — e.g., "the product"]
[Reference image 2: description — e.g., "the style reference"]
[Reference image 3: description — e.g., "the target environment"]

[Relationship instruction]: Apply the style of Image 2 to the product
in Image 1, placed in the environment from Image 3.
[New scenario or constraint].
[Preserve list — see "Iterate vs regenerate" below].
```

For **character consistency** across multiple generations (children's books, comic panels, ad series): create a single "anchor" image first, lock the character description (clothing, proportions, palette, personality) in your own notes, and on every subsequent generation pass the anchor as a reference and restate the locked traits in text. Drift is the default; explicit re-specification is what prevents it.

---

## Iterate vs regenerate — the preserve-list pattern

When an image is *almost* right, edit; when it's fundamentally wrong, regenerate.

**Editing discipline.** State exactly what changes and exactly what must not. Repeat the preserve list on every iteration — models drift if you don't.

```
Change: [single specific change, e.g., "the jacket color from blue to olive green"].
Keep unchanged: face, body, pose, expression, hair, lighting direction,
shadows, background, camera angle, framing, and all other elements.
Do not alter saturation, contrast, or composition.
```

For surgical edits (object swap, text swap, weather change), explicitly forbid changes to: identity, geometry, layout, arrows/labels, camera angle, surrounding objects. Models love to "improve" things you didn't ask about.

**Regenerate from scratch when:** the composition is wrong, the subject is wrong, the style is wrong, or you've iterated 3+ times without convergence. Editing a broken base image rarely fixes it.

---

## API-level parameters worth setting

The text prompt is most of the battle, but a handful of API parameters meaningfully affect output. Names vary by vendor; look up the exact field for the model in use.

| Lever | What it controls | When to tune |
| --- | --- | --- |
| **Aspect ratio** | Frame shape (1:1, 16:9, 9:16, 3:2, 2:3, 4:5, etc.) | Always — the right ratio for the output's eventual use is non-negotiable. Square for profile pics; 16:9 for slides/landscape; 9:16 for stories/reels; 3:2 or 2:3 for editorial photography. |
| **Resolution / size** | Pixel count of output (e.g., 1K / 2K / 4K, or explicit `1024x1536`) | Use the highest the model supports for: text-heavy images, infographics, dense detail, anything destined for print. Use the smallest for: rapid iteration, drafts, low-stakes batches. |
| **Quality / fidelity tier** | Compute spent per image (e.g., `low` / `medium` / `high`, or `standard` / `hd`) | Default: `medium` or equivalent. Step up to `high` for finals, text rendering, dense layouts. Step down to `low` for ideation and high-volume drafting where unit cost matters. |
| **Number of variants (`n`)** | How many candidates per call | Set `n=4` for logo/concept/style exploration. Set `n=1` for refinement passes once you have a direction. |
| **Reference / input fidelity** | How tightly the output adheres to a reference image | Crank to `high` when identity, geometry, or label preservation matters (try-on, product mockups, character consistency). Lower it when you want creative interpretation of a reference. |
| **Seed** | Reproducibility | Pin a seed when you need to compare prompt variants holding everything else constant. Don't pin in production unless you have a reason to. |
| **Background** | Opaque vs (where supported) transparent | Most models output opaque only. For transparent assets, ask for a plain white background and remove it downstream with a separate background-removal step. |

---

## Debugging checklist

When output is wrong, run through this in order. The fix is usually higher up the list than you'd expect.

1. **Is the prompt prose, or a keyword list?** Rewrite as prose if it's a list.
2. **Is the subject specific?** "A man" produces an average man. "A 60-year-old fisherman with weathered skin and a grey beard, wearing a worn yellow raincoat" produces a specific person.
3. **Is there a style anchor?** Without one, the model picks an average style. Add a medium (`photorealistic`, `watercolor`, `3D render`) and a stylistic reference (era, lens, art movement, film stock).
4. **Is composition stated?** If output framing is wrong, say it explicitly: `medium shot`, `centered`, `subject in lower-left third`, etc.
5. **Is lighting stated?** Lighting is usually what makes a competent image great — if the result feels flat, the lighting clause is missing or weak.
6. **Are there contradictions?** "Minimalist scene with intricate detail in every corner" pulls the model two ways. Pick one.
7. **Is the prompt using negation?** Convert to positive framing.
8. **Is text rendering wrong?** Quote the text, specify font character, raise quality, shorten the copy.
9. **Are there too many subjects?** More than 2–3 distinct subjects in one frame degrades fast. Generate them separately and composite, or simplify.
10. **Is the aspect ratio wrong for the framing being asked for?** A "vertical portrait" prompt at 16:9 will fight itself.
11. **Is the model the right one for the job?** Some models are stronger at text, some at photorealism, some at illustration, some at diagrams. If a prompt fails repeatedly on one model, try another before assuming the prompt is wrong.

---

## Anti-patterns

- **Keyword soup.** `4k, masterpiece, ultra detailed, trending on artstation` was Stable Diffusion 1.x folklore. Modern models do not benefit from these tags and may actively distort output.
- **Stuffing every modifier into one sentence.** A 200-word run-on with seven adjectives stacked per noun is harder for the model to parse than three short labeled clauses.
- **Fighting the model with negation.** See above — describe what you want.
- **Asking for one image to do too many jobs.** "A logo, a hero shot, and a product photo, with the tagline and three feature callouts." Generate the parts separately.
- **Editing a broken base.** If the first generation has the wrong composition, regenerate; don't try to edit a misframed shot into a correct one.
- **Skipping the preserve list on edits.** Drift is silent and cumulative. Restate invariants every iteration.
- **Chasing a specific named font.** Font *family* and *character* cues work; exact named fonts usually do not. Don't waste prompt budget on `"in Helvetica Neue 47 Condensed Light"` — say `clean geometric sans-serif, condensed, light weight`.
- **Generating identifiable real people, copyrighted characters, or trademarked logos.** Most providers refuse, and the ones that don't expose the user to legal risk. For people, describe archetypes; for brands, describe original equivalents.

---

## Quick-reference template

When in doubt, start here and fill in:

```
A [photorealistic / illustrated / 3D rendered / vector / watercolor] [shot type]
of [specific subject with concrete details], [action or expression],
in [setting with detail and time of day].

[Composition: framing, what occupies the frame, where the subject sits].
Lit by [lighting source, direction, quality], creating a [mood] atmosphere.
[Stylistic anchors: lens / film stock / art reference / color grading].

[Any text to render, in quotes, with font character described].
[Hard exclusions: no watermark, no logos, no extra text].
[Aspect ratio].
```

Generate. Look at it. If it's wrong, walk the debugging checklist. If it's almost right, edit with a preserve list. If it's fundamentally wrong, regenerate from a revised prompt — don't iterate on a broken base.

---

## Notes for agents calling this skill

- **Pre-validate the prompt before calling the API.** A 3-second prompt review saves a 30-second generation. Walk the debugging checklist on the prompt itself before the first call.
- **Default to `medium` quality and `n=1` for first attempts**, then escalate based on result. Don't burn `high` quality on a prompt you haven't validated yet.
- **Save intermediate outputs.** Store generated images alongside the exact prompt and parameters used. When iterating, having the prompt diff between v1 and v2 is what teaches you which lever moved which dimension.
- **Read the target model's docs once for vendor-specific quirks** — supported sizes, content policies, parameter names, max reference images. The principles here are universal; the parameter names and limits are not.
- **Surface the prompt to the user when output is wrong.** Most "the model is bad" complaints are prompt issues. Showing the user the prompt that was actually sent often reveals the gap immediately.