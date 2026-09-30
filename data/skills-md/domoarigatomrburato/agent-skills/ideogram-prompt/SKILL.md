---
name: ideogram-prompt
description: >
  Write, validate and deliver prompts for Ideogram 4 (Ideogram 4.0 / V_4_0) in two modes:
  structured JSON caption (magic prompt off, exact control over text, palette and layout) or
  plain text (magic prompt on, exploratory). Picks the mode for the brief, or asks when unsure.
  Use this whenever the user mentions Ideogram, wants a poster, logo, flyer, social card,
  thumbnail, cover, packaging, label, menu, product shot, typography piece or any image made
  through the Ideogram MCP, REST API, web app or open weights; asks for a "JSON prompt",
  "v4 caption", "magic prompt", bounding boxes, hex color palette control or a
  transparent-background asset; pastes an Ideogram JSON caption to fix or validate; or wants a
  style recipe extracted from reference images (describe_image) and applied to new subjects.
  Trigger even for "make me an image with Ideogram" or "generate a logo" when the Ideogram MCP
  is connected.
---

# Ideogram 4 prompting

Ideogram 4 was trained **exclusively on structured JSON captions**. Every plain-text prompt it
receives is first rewritten into that JSON by a "magic prompt" LLM; JSON you send directly is
consumed as written. So this skill has one job: produce the best possible caption for the
brief, in the mode that fits, and get it to Ideogram without breaking the schema.

Everything below is reconstructed from Ideogram's official sources (listed at the end). The
advertised `https://ideogram.ai/skill/ideogram-prompt.md` download returns an HTML page, not a
skill, so do not fetch it as a reference.

Companion files in this folder (read when the pointer says so; paths are relative to this skill's
folder, the base directory shown when the skill loads):

- `scripts/validate_caption.py` — JSON schema validator/fixer/minifier (a port of Ideogram's `CaptionVerifier`); `--plain` lints a plain-text prompt.
- `references/caption-writing.md` — how to write each JSON field well (Ideogram's open-source magic-prompt rules).
- `references/plain-prompting.md` — how to write a plain-text prompt for magic-prompt mode.
- `references/delivery.md` — MCP, REST API, web app, open weights, resolutions, describe/style recipes.
- `references/examples.md` — official worked examples, verbatim.

## 0. Read the brief

Before choosing a mode, pull these out of the request (ask only if a missing item blocks you):

- **Subject and medium**: photo, illustration, 3D render, graphic design, painting.
- **Text that must render**: copy it verbatim, keep the user's language, capitalization and punctuation.
- **Colors**: hex codes, brand colors, named palettes.
- **Layout**: anything positional ("logo top-left", "title across the top", "same layout as last time").
- **Format**: aspect ratio, resolution, platform (Instagram 4:5, story 9:16, banner 3:1, print 2:3 …).
- **Quantity and consistency**: one image, a set, variants that must match.
- **Delivery target**: Ideogram MCP tools present in this session, REST API key, the web app, or the open-weights repo.
- **Explicit mode flags**: `--json`, `--plain`, `--ask` (or the words "JSON", "magic prompt on/off").

## 1. Choose the mode

Flags always win. Otherwise decide from the signals below. This is the decision Ideogram's own
guide calls the core of prompting Ideogram: *"Magic prompt on suits exploration: quick ideas,
loose briefs, cases where you want the model to interpret your intent. Magic prompt off is for
when you know exactly what you want: a precise palette, a specific composition, text that needs
to render legibly."*

**JSON mode** (magic prompt OFF, you are the expander) when **any** of these hold:

- Text must render: titles, names, dates, prices, labels, slogans, signage, logos, numbers.
- A palette, hex codes or brand colors are given.
- Placement or layout language appears, or the user wants a repeatable layout across a set.
- The artifact is a *designed* object: poster, logo, card, cover, banner, menu, packaging, UI, ad, sticker, icon, thumbnail.
- The user says JSON, caption, schema, bbox, "exact", "precise", "reproducible".
- The target is the open-weights model (plain text does not work there and trips the safety filter).
- The brief is already detailed (roughly 40+ words of concrete visual specifics). Rewriting detail into JSON keeps it; magic prompt may reinterpret it.

**Plain mode** (magic prompt ON, Ideogram expands) when the brief has **no text to render, no
palette and no placement constraints**, and **either** of these holds:

- It is short or loose, or uses exploration words: "surprise me", "some ideas", "a few directions", "moodboard", "whatever looks good".
- The user explicitly wants Ideogram's own interpretation / magic prompt.

**Unsure?** A mid-length brief with no strong signal either way:

- In an interactive session, ask **one** question with `AskUserQuestion`: "JSON (recommended): exact palette, layout and text, reproducible" vs "Plain (magic prompt): Ideogram interprets the brief, more surprise". Do not ask when the signals above already decide, and never ask twice in a session; remember the answer.
- When you cannot ask (subagent, batch, scheduled run) **and** the signals above did not already decide, choose **JSON**. It is the training format, it never loses information, and its output is repeatable. The only thing you give up is Ideogram's own creative expansion, which is exactly what an unattended run should not depend on. A brief that the Plain rule already matches stays Plain even unattended.

Edge cases: the user wants exploration *and* has text → JSON (legible text wins). The user wants
several loose directions → Plain for the first pass, then convert the winner to JSON for the
final; unattended, deliver the Plain set and stop, and convert only when someone picks a winner
or asks. "A few" ideas means three unless the user says otherwise. A pasted JSON caption → JSON
mode, validate and fix it (section 2A, "Validate, then present").

## 2A. JSON mode

### The schema (normative: `docs/prompting.md` and `CaptionVerifier` in ideogram-oss/ideogram4)

Three top-level keys, in this order, and **nothing else** (no `aspect_ratio`, `seed`, `negative_prompt`, `style_type`):

| Key | Required | Content |
|---|---|---|
| `high_level_description` | strongly recommended (the API requires it) | One or two sentences summarizing the whole image. |
| `style_description` | optional, but always include it | Aesthetics, lighting, medium, camera or art style, optional palette. |
| `compositional_deconstruction` | **required** | `background` (string) then `elements` (list), in that order. |

`style_description` must contain **exactly one** of `photo` or `art_style`; `aesthetics`, `lighting`
and `medium` are required when it is present; `color_palette` is optional and always last. **Key
order is strict** because the model was trained on one consistent order:

| Caption type | Key order |
|---|---|
| Photo (`medium: "photograph"`, uses `photo`) | `aesthetics`, `lighting`, `photo`, `medium`, `color_palette` |
| Non-photo (uses `art_style`) | `aesthetics`, `lighting`, `medium`, `art_style`, `color_palette` |

`medium` values used in the official docs: `"photograph"`, `"illustration"`, `"3d_render"`, `"painting"`, `"graphic_design"`.

Each element is one of these two shapes, with keys in exactly this order (`bbox` and
`color_palette` are optional; when present they sit in the positions shown):

```json
{"type":"obj","bbox":[y_min,x_min,y_max,x_max],"desc":"...","color_palette":["#RRGGBB"]}
{"type":"text","bbox":[y_min,x_min,y_max,x_max],"text":"LINE ONE\nLINE TWO","desc":"...","color_palette":["#RRGGBB"]}
```

- `bbox`: four **integers** in 0–1000, `[y_min, x_min, y_max, x_max]`, origin top-left, **y first**. Normalized to the frame whatever the resolution.
- `text`: the literal characters to render. `desc` describes size, position, typeface family, weight, color; it must not repeat the characters.
- `color_palette`: **uppercase** `#RRGGBB` only (`#1B1B2F`, never `#1b1b2f` or `#fff`). Up to 16 in `style_description`, up to 5 per element. The API applies it as a soft bias, not a per-pixel lock.
- Serialize minified UTF-8 with literal non-ASCII (`json.dumps(c, separators=(",", ":"), ensure_ascii=False)`); `\uXXXX` escapes are flagged.
- The open-weights pipeline rejects captions over 2048 text tokens; keep captions well inside that (a few hundred words is typical, the biggest official example is about 600 words).

### Writing the caption (guidance: Ideogram's open-source magic-prompt system prompt)

Read `references/caption-writing.md` before writing a caption, especially for a complex brief
(many elements, text-heavy layouts, transparent background). The rules that matter most:

1. **Pick the aspect ratio first.** Every bbox depends on it. Match the medium: portrait subjects and stories 9:16 or 4:5, posters 2:3 or 3:4, banners 3:1, ambiguous 1:1. If you cannot infer it and cannot ask, use 1:1.
2. **`high_level_description`**: one long sentence, at most two, 50 words at most. Starts with the subject ("A medium-shot photograph of …"), names the medium and composition, names real brands, people and characters in full. No feature lists; those go into elements.
3. **`style_description`**: name the style once with a recognizable label (`"35mm film photograph"`, `"flat vector illustration"`, `"Studio Ghibli animation"`). Put camera, film, depth of field and grain in `photo` or `art_style`, not in element descs. Include the background color in `color_palette` when you want a dark or tinted background, and include highlight plus shadow pairs for controlled lighting.
4. **`background` is the empty shell**: walls, floor, ground, sky, horizon, distant crowds, weather, ambient light. Anything you can place individually (furniture, people, props, signs, vehicles) is an element. The ground surface, puddles and reflections are **always** background; emitting a floor as an element makes the renderer clip the subject's legs into a flat band. Nothing may appear in both `background` and an element, except the shell-affixed objects in rule 5.
5. **One subject, one element.** A person, animal, car or building is a single `obj`; its parts are attributes in `desc`. Multiple distinct subjects get multiple elements. Elements are drawn in list order, back to front, so put backdrop-defining items (a chalkboard wall, a mounted TV, a stage) first, mention them once in `background` too, and open their desc with "the primary background element".
6. **Element `desc`, 30–60 words**: identity first, then major attributes (people: skin tone, hair, each garment with color, expression, pose, one distinguishing detail; objects: shape, material, color, markings). Anchor placement to named references ("resting on the lower-right corner of the table"). No shadows, no camera or render language, no impressions ("stunning", "vibrant"), no repeating scene-wide lighting per element.
7. **Commit to one value.** No hedges: "or", "such as", "various", "possibly", "implied". Typography: one family (serif / sans-serif / display / script / monospace), one weight, one style.
8. **Text**: every string the user quoted becomes its own `text` element, verbatim, once. Use `\n` for line breaks inside one block; stack long stylized titles at word breaks (`"ENTRE\nVERSOS E\nCONTOS"`). Numbers are text (dates, prices, jersey numbers). Real-world scenes carry text on shop signs, labels, menus, plates; populate them with specific content. Prose fields stay in English; only `text` follows the brief's language. Use single quotes when a desc refers to a string (`the 'OPEN' sign`). `desc` must never contradict `text`: if the design wants a string in capitals, put the capitals in `text` and tell the user you changed the casing. Dates, addresses, prices and names the user typed without quotes are still rendered exactly as typed; only add copy the user did not supply (a tagline, a sub-line) when the format clearly needs it, and say so.
9. **Named things stay named.** `Nike Dunk Low Panda`, `Spider-Man`, `Eiffel Tower`, not generic stand-ins, unless the user asked for a lookalike. Every visual unit the user named must appear as its own element; enumerable sets (12 place cards, 31 calendar dates) are listed in full, never "etc.".
10. **Bounding boxes**: include them where position matters (portrait subject, products on a surface, logos, each text block); omit them for dense unenumerable stuff (crowds, starry sky, wildflowers). Remember both axes are 0–1000 regardless of shape: a square-looking box on a 16:9 frame is a wide rectangle; for a round or square thing scale spans so `(x2-x1)/(y2-y1) ≈ H/W` (on a 16:9 frame the x-span is 9/16 of the y-span; Ideogram's system prompt prints this ratio the other way round, but its own advice, narrower x-spans on wide frames, is this one). Tight boxes per subject prevent duplicates.
11. **Photoreal defaults** (only when the user gave no style direction): phone-snapshot realism, neutral white balance, overcast or diffused daylight, off-center framing, no motion blur, mention saturation at most once. Avoid "warm" as a grade; describe the warm light *source* instead ("amber pool from the candle"). This steers away from the glossy AI look.
12. **Populate sparse briefs** with believable secondary subjects, micro-props and foreground/midground/background depth, and commit to a specific region or culture. Skip this when the brief says minimal, empty, lonely, single subject or negative space.
13. **Transparent background**: `background` must be exactly the string `transparent background`, and `high_level_description` must contain the phrase `on a transparent background`. Deliver through a transparent-background endpoint (see `references/delivery.md`).

### Validate, then present

Run the validator on the caption before showing it or sending it:

```bash
python3 scripts/validate_caption.py caption.json --fix --minify
```

It reports schema issues (unknown keys, wrong key order, both `photo` and `art_style`, lowercase
hex, bbox out of range, `\uXXXX` escapes) and advisory hints (hedge and negation words in every
prose field, a summary over 50 words or a desc over 60, a stray `aspect_ratio` key), `--fix` repairs the mechanical ones, and `--minify` prints the single-line
string to send. If the script is missing, walk the same list by hand: three known top-level keys,
`compositional_deconstruction` with `background` before `elements`, exactly one of `photo`/`art_style`,
strict key order, uppercase 6-digit hex, integer bboxes with y before x, no extra keys anywhere.

Present the caption pretty-printed in a `json` code block for reading, and send the minified
form to the API or MCP. State the aspect ratio or resolution alongside it, since it is not part
of the caption.

## 2B. Plain mode

You write a natural-language prompt; Ideogram's magic prompt turns it into JSON. Follow
Ideogram's plain-text guide (`references/plain-prompting.md`); the essentials:

- Structure it as: *[Image summary]. [Main subject details], [Pose or action], [Secondary elements], [Setting and background], [Lighting and atmosphere], [Framing and composition], [Technical enhancers].* Use full sentences, not tag soup. Skip parts you do not need.
- **Lead with what matters.** Earlier words carry more weight. Put the subject and any text near the start.
- **Text in double quotes**, described in context (`a poster that reads "Ride Free" in retro lettering along the bottom`). Keep it short; split multi-line copy into separate placement cues. Non-Latin scripts are best-effort in plain mode; use JSON when they must be exact.
- **Positive phrasing only.** "An empty beach at sunrise", not "a beach without people". Negation is read as a keyword.
- **Visually grounded words**: colors, materials, shapes, light. Replace "beautiful", "artistic", "modern" with a concrete style (`impressionist oil painting with thick brushstrokes`) or a specific detail.
- **Stay under roughly 150 words.** Longer plain prompts get truncated or ignored past that point.
- **Framing follows aspect ratio.** Say "full body, shoes on the pavement" for a full figure, "head and shoulders" for a close-up, and pick a ratio that suits it.
- **Aspect ratio**: same heuristic as JSON rule 1 (portraits 9:16 or 4:5, posters 2:3 or 3:4, banners 3:1, ambiguous 1:1). Ideas in a set with different framings get their own ratios; a set that must match gets one shared ratio.
- **Photoreal briefs** keep the neutral defaults of JSON rule 11 (no "warm" grade, no stacked saturation words, off-center framing, no motion blur) unless the user asked for a look. The blog's wolf prompt in `references/examples.md` section 5 is the official plain-mode example.
- Hex codes and weights do nothing in plain text; describe colors in words or switch to JSON.

Lint before presenting:

```bash
python3 scripts/validate_caption.py --plain prompt.txt
```

It checks the word ceiling, quoted text and its position, negation, hedges, vague adjectives, hex
codes and weight syntax. By hand: under roughly 150 words, every string to render in double
quotes near the start, no "no"/"without", no hex, one named style or medium.

Present the prompt in a plain code block, name the aspect ratio, and say that magic prompt will be
ON so the result may differ from the wording.

## 3. Aspect ratio and resolution

Aspect ratio lives **outside** the caption. The REST API takes a `resolution` enum, the magic-prompt
endpoint takes `aspect_ratio` buckets (`AUTO`, `1x4`, `1x3`, `1x2`, `9x16`, `10x16`, `2x3`, `3x4`, `4x5`,
`1x1`, `5x4`, `4x3`, `3x2`, `16x10`, `16x9`, `2x1`, `3x1`, `4x1`), the web app takes a ratio, and the open
weights take any `height`/`width` that are multiples of 16 between 256 and 2048 (up to 6:1).

Ideogram 4.0 API resolutions (1K first, 2K second), pick the closest to your ratio:

| Ratio | Resolutions |
|---|---|
| 1:1 | `1024x1024`, `2048x2048` |
| 4:5 / 5:4 | `896x1120` `1792x2240` / `1120x896` `2240x1792` |
| 3:4 / 4:3 | `864x1152` `1728x2304` / `1152x864` `2304x1728` |
| 2:3 / 3:2 | `832x1248` `1664x2496` / `1248x832` `2496x1664` |
| 10:16 / 16:10 | `800x1280` `1600x2560` / `1280x800` `2560x1600` |
| 9:16 / 16:9 | `720x1280` `1440x2560` / `1280x720` `2560x1440` |
| 1:2 / 2:1 | `720x1440` `1440x2880` / `1440x720` `2880x1440` |
| 1:3 / 3:1 | `512x1536` `1024x3072` / `1536x512` `3072x1024` |
| extra-tall / extra-wide 2K | `1296x3168` `1152x2944` `1248x3328` `1280x3072` and their transposes |

Use 2K for print and final deliverables, 1K for iteration. Paper sizes: ISO A-series (A4, A3) is 1:1.414, between 2:3 and 3:4, and US Letter is 1:1.294; pick the nearer ratio (2:3 for A-series), keep text inside safe margins so the trim crop costs nothing, and plan an upscale pass for 300 dpi print. `rendering_speed` accepts `TURBO`,
`DEFAULT`, `QUALITY` (`FLASH` returns 400 on V4 today).

## 4. Deliver

Match the target the user actually has; details and request shapes are in `references/delivery.md`.

- **Ideogram MCP in this session** (tools like `generate_image`, `generate_images_bulk`, `describe_image`, `remix_image`, `reframe_image`, `upscale_image`, collections): read the tool schema first. Pass the JSON caption as the minified string in the prompt field and turn magic prompt off if the tool exposes that switch; pass plain prompts with it on. Set resolution or aspect ratio from section 3. Generation spends the user's credits, so generate when they asked for an image, and only hand back the prompt when they asked for a prompt.
- **REST API**: `POST https://api.ideogram.ai/v1/ideogram-v4/generate` (multipart form) with `json_prompt` (JSON mode) **or** `text_prompt` (plain mode, magic prompt automatic), plus `resolution` and `rendering_speed`. `Api-Key` header. Never paste the key into the prompt or logs; read it from `IDEOGRAM_API_KEY`.
- **Web app** (ideogram.ai): select model 4.0, paste the pretty JSON into the prompt box; Magic Prompt switches off automatically for JSON. For plain mode, leave Magic Prompt on.
- **Open weights** (`ideogram-oss/ideogram4`): `python run_inference.py --no-magic-prompt --prompt '<minified json>' --height H --width W --sampler-preset V4_QUALITY_48`. Never send plain text there.
- **Draw Things** (Ideogram 4 on Draw Things+ cloud compute): save the caption as a `.json` file and render it with the `drawthings` skill, recipe `ideogram-4`; it minifies the caption and sends it as the prompt, magic prompt never runs there, and the recipe carries the app's own settings for "Ideogram 4 remote" (model file `ideogram_4_q8p.ckpt`, 32 steps, guidance 7, shift 2.99, DPM++ 2M Trailing, zero negative prompt on, 1920x1280). Long captions render fine at guidance 7 there, up to Ideogram's 2,048-token limit; JSON is token-expensive (braces, quotes and bboxes count), so watch the token count the renderer prints.

## 5. Look, then iterate

Treat generation as a loop: generate, look at the image, change one thing, regenerate.

- **Text wrong or missing**: shorten the string, split into more `text` elements, stack long titles with `\n`, give each block a tight bbox, simplify the scene around it.
- **Subject cropped or duplicated**: add or tighten the bbox; check the bbox shape against the aspect ratio; describe cues near the cropped edge (shoes on the pavement).
- **Figure sunk into the floor**: the ground was emitted as an element. Move it into `background`.
- **Object floating or in front of everything**: a shell-affixed object was not mentioned in `background`, or is not first in `elements`.
- **Palette ignored**: include the background color and a highlight/shadow pair in `color_palette`; the bias is soft, so also name colors in descs.
- **Looks "AI"**: remove "warm", stacked saturation words, motion blur and dramatic rim light from photoreal captions; use neutral daylight and off-center framing.
- **Layout drifts between runs** in plain mode: that is expected; move to JSON with bboxes.
- **Safety block** (gray image or HTTP 422): the caption tripped the filter. Rephrase; on open weights make sure you sent JSON, since plain text has a high false-positive rate there.

Keep the same seed while iterating on wording so you can attribute changes.

## 6. Style recipes from reference images

When the user has reference images and wants "this look" on new subjects:

1. Run `describe_image` (MCP) or `POST /v1/ideogram-v4/describe` on each reference. Ideogram 4.0 returns a full JSON caption of the image (`include_bbox` defaults to true).
2. Extract the shared visual logic: `style_description` (medium, aesthetics, lighting, `photo`/`art_style`, palette), plus recurring background and element patterns (texture, typography family, composition hierarchy). Drop subject-specific content.
3. Write the recipe as a reusable JSON block: a complete `style_description` plus a short prose note on composition and texture. Offer to save it for later sessions.
4. Apply it: new `high_level_description` and `compositional_deconstruction` for the new subject, recipe's `style_description` verbatim. Reuse the reference's bboxes only when the user wants the same layout.

Described-then-regenerated images reproduce layout best when the describe output keeps its bboxes; strip them when you want the sampler to compose freely.

## 7. Traps that break captions

- Any extra key anywhere (`aspect_ratio`, `size`, `font`, `position`, `weight`, `negative_prompt`).
- `photo` **and** `art_style` together, or neither, or `photo` with a non-photograph medium.
- Lowercase or 3-digit hex; more than 16 palette colors overall or 5 per element.
- Floats or `[x, y, …]` order in bbox; values outside 0–1000; `y_min > y_max`.
- Text characters repeated inside `desc`, or double quotes used to quote text inside prose.
- `\uXXXX` escapes instead of literal UTF-8 (`café`, `東京`).
- Negatives ("no people"), hedges ("or", "such as"), impressions ("breathtaking").
- A wall of `text` elements with no bboxes on a text-heavy layout: give each block a box.
- Sending plain text to the open-weights model.

## Two compact examples

Photo (JSON mode), 3:2, written from the brief "candid shot of a barista pouring latte art":

```json
{
  "high_level_description": "A candid medium-shot photograph of a barista pouring latte art into a white ceramic cup at the counter of a small specialty coffee shop.",
  "style_description": {
    "aesthetics": "documentary, natural, off-center rule-of-thirds framing",
    "lighting": "diffused daylight from a street-facing window, neutral white balance",
    "photo": "phone snapshot, medium depth of field, eye-level",
    "medium": "photograph",
    "color_palette": ["#F4EFE6", "#6B4A2B", "#2A2A2A", "#C9A66B", "#8C8C8C"]
  },
  "compositional_deconstruction": {
    "background": "A narrow coffee shop interior with a pale plaster wall, a wooden counter running left to right, and a bright out-of-focus window on the right. Soft daylight fills the room.",
    "elements": [
      {"type": "obj", "bbox": [80, 60, 1000, 560], "desc": "A barista in a black apron over a grey T-shirt, medium skin tone, short dark curly hair, leaning slightly forward as she pours steamed milk from a steel pitcher held in her right hand. Calm, focused expression looking down at the cup."},
      {"type": "obj", "bbox": [560, 520, 820, 760], "desc": "A white ceramic cup on a saucer on the counter, half-finished rosetta latte art forming on the surface of the coffee."},
      {"type": "text", "bbox": [120, 700, 200, 960], "text": "TODAY'S ROAST\nEthiopia Guji", "desc": "Hand-lettered white chalk text on a small black chalkboard propped on a shelf behind the counter, upper right."}
    ]
  }
}
```

Design (JSON mode), 2:3, from "a poster for the Beaches Jazz Festival, July 3, Toronto":

```json
{
  "high_level_description": "A bold retro event poster for the Beaches Jazz Festival on July 3 in Toronto, with a stylized saxophonist silhouette under large display type.",
  "style_description": {
    "aesthetics": "1960s jazz poster, high contrast, playful, textured print",
    "lighting": "flat graphic lighting, warm spotlight glow behind the figure",
    "medium": "graphic_design",
    "art_style": "flat vector illustration with coarse halftone grain and slightly misregistered spot color",
    "color_palette": ["#0B1C3F", "#F2B134", "#E4572E", "#F7F1E1", "#111111"]
  },
  "compositional_deconstruction": {
    "background": "A deep navy poster field with fine halftone grain and a large soft golden circle glowing behind the center of the composition.",
    "elements": [
      {"type": "text", "bbox": [50, 60, 260, 940], "text": "BEACHES\nJAZZ FESTIVAL", "desc": "Very large bold condensed sans-serif headline in cream, two stacked lines, spanning the full width near the top."},
      {"type": "obj", "bbox": [270, 200, 780, 800], "desc": "A saxophonist silhouette in solid black, standing in profile facing left, leaning back mid-solo with a tenor saxophone raised. Flat vector shapes with a few orange accent highlights along the instrument."},
      {"type": "text", "bbox": [800, 100, 880, 900], "text": "JULY 3 · TORONTO", "desc": "Medium bold sans-serif in golden yellow, centered below the figure."},
      {"type": "text", "bbox": [895, 250, 950, 750], "text": "Free concerts along Queen Street East", "desc": "Small regular-weight sans-serif in cream, centered near the bottom edge."}
    ]
  }
}
```

More official examples, including the color-palette and full multi-text captions, are in `references/examples.md`.

## Sources (official only, in priority order)

1. `ideogram-oss/ideogram4` on GitHub: `docs/prompting.md` (schema, key order, palettes, safety), `src/ideogram4/caption_verifier.py` (the checks this skill's validator ports), `src/ideogram4/magic_prompt.py` and `magic_prompt_system_prompts/v1.txt` (caption-writing guidance), `README.md` and `docs/inference.md` (resolutions, presets, CLI).
2. Ideogram blog, "The Ideogram 4.0 prompt guide" (`ideogram.ai/blog/claude-mcp/`): the two modes, when to use each, MCP tools, style extraction, the wolf example.
3. `docs.ideogram.ai` prompting guide (sections 2–9, "JSON Prompting (Ideogram 4.0)") and `developer.ideogram.ai` API reference (`generate-v4`, `magic-prompt-v4`, `describe-v4`, OpenAPI enums), `ideogram.ai/features/mcp/`.
