---
name: novelai-mcp-tools
description: Invoke the 11 NovelAI MCP tools (generate, img2img, inpaint, upscale, director, annotate, tags, vibe, account) from an MCP host. Use when generating/transforming images via MCP rather than the CLI.
---

# novelai-mcp-tools

Instructions for the agent to follow when invoking NovelAI MCP tools from an MCP host.

## When to use

Use this skill when an MCP host (Claude Desktop, Cline, or a custom agent) needs to invoke a single NovelAI tool — picking a model, setting parameters, or generating/transforming an image interactively during an agent session. For shell scripting, batch jobs, or headless pipelines, use the `novelai-cli` skill instead; for multi-step recipes that orchestrate several tools, use the `novelai-workflows` skill.

## Instructions

1. **Pick the right model** — see `### Model selection` below for the decision tree.
2. **Set generation parameters** — see `### Parameter guide` for the full parameter tables.
3. **Check Anlas cost** — see `### Anlas cost awareness` before expensive generations.
4. **Call the tool** — see `### Practical tool-call patterns` for examples.

### Model selection

Model ids live in `Model` (`nai/constants.py`). Pick by quality need and
content domain:

```text
Want best overall quality / natural language / multi-character?
  → nai-diffusion-5-full             (V5, best quality, EN/JP natural language,
                                      true alpha; vibes not yet supported)
  → nai-diffusion-5-curated          (V5 curated, tighter aesthetics)

Solid all-rounder with vibes?
  → nai-diffusion-4-5-full            (V4.5, default, supports character_prompts + vibes)
  → nai-diffusion-4-5-curated         (V4.5 curated, tighter aesthetics, fewer Anlas)

Good quality, slightly faster, still V4 family?
  → nai-diffusion-4-full              (V4)
  → nai-diffusion-4-curated-preview   (V4 curated)

Pure anime, fastest, cheapest?
  → nai-diffusion-3                   (V3 anime)

Furry content?
  → nai-diffusion-furry-3             (Furry v3)

Inpainting (any family)?
  → append "-inpainting" to the model id, e.g.
     nai-diffusion-4-5-full-inpainting, nai-diffusion-3-inpainting,
     nai-diffusion-furry-3-inpainting
```

**Endpoint split (handled automatically by the client):**

- V3 / Furry → `POST /ai/generate-image` → ZIP archive (`application/zip`),
  HTTP 201.
- V4 / V4.5 / V5 → `POST /ai/generate-image-stream` → MessagePack stream
  (`stream: "msgpack"`), HTTP 200. Selected via `is_v4_model()` in
  `client.py`.
- `/ai/upscale` and `/ai/annotate-image` are **not** on `image.novelai.net` —
  they remain on the legacy Primary API `api.novelai.net`
  (`NOVELAI_LEGACY_IMAGE_BASE_URL`). Never point that base URL at
  `image.novelai.net` or these two tools 404.

**V4/V4.5-only features:** `references` (vibe transfer) — V5 does not
support vibes yet and rejects them. `character_prompts` (multi-character
with per-character center coords) works on V4 / V4.5 / V5; V3/Furry ignore
both. Vibes must be encoded with `encode_vibe` first (V4/V4.5 only).

### Parameter guide

All parameters below are optional unless noted; unset values fall back to
`NOVELAI_DEFAULT_*` settings (defaults: model `nai-diffusion-4-5-full`,
832×1216, 28 steps, scale 5.0, sampler `k_euler_ancestral`).

#### Common generation params (`generate_image` / `image_to_image` / `inpaint`)

| Param | Range / type | Default | Notes |
|---|---|---|---|
| `prompt` | str (required) | — | Text prompt. Quality tags auto-appended when `quality=true`. |
| `negative_prompt` | str | `""` | Merged with the model's UC preset. |
| `model` | model id str | `nai-diffusion-4-5-full` | See §Model selection. |
| `width` / `height` | 64–49152, multiple of 64 | 832 / 1216 | Rounded up to next multiple of 64. Total ≤ 3,047,424 px. |
| `steps` | 1–50 | 28 | More = higher quality, more Anlas. |
| `scale` | float > 0 (≤20) | 5.0 | CFG scale. Higher = stricter prompt adherence; too high burns contrast. 4–7 is the sweet spot. |
| `sampler` | sampler id | `k_euler_ancestral` | `k_euler`, `k_euler_ancestral`, `ddim_v3`, `k_dpmpp_2s_ancestral`, `k_dpmpp_2m`, `k_dpmpp_2m_sde`, `k_dpmpp_sde`. |
| `seed` | 0 – 2³²−1 | 0 | `0` = random per call. Positive int = reproducible. |
| `n_samples` | 1–8 | 1 | Capped by resolution (see below). |
| `quality` | bool | `true` | Appends `QUALITY_TAGS[model]` to the prompt. |
| `uc_preset` | 0–3 | 0 | Picks the negative-preset row from `UC_PRESETS[model]`. |
| `noise_schedule` | str | `karras` | `native`, `karras`, `exponential`, `polyexponential`. |
| `cfg_rescale` | 0–1 | 0.0 | CFG rescale; tames over-saturated highs. |
| `smea` / `smea_dynamic` / `auto_smea` | bool | None / False | SMEA multipliers (1.2 / 1.4 / 1.2). Raise Anlas cost. |

**Resolution-based `n_samples` cap** (enforced server-side):
`≤512×704`→8, `≤640×640`→6, `≤1,310,720 px`→4, `≤1,572,864 px`→2,
`≤1,024×3,072`→1, larger→rejected. Requesting more raises `ValueError`.

#### img2img / inpaint extras

| Param | Range | Default | Notes |
|---|---|---|---|
| `image` | base64 PNG/JPEG (required) | — | The source image. |
| `mask` | base64 PNG/JPEG | — | **Required for `inpaint`.** Non-transparent pixels = region to redraw. |
| `strength` | 0.01–0.99 | 0.3 | How far the result diverges from the input. Higher = more change. |
| `noise` | 0–0.99 | 0.0 | Extra variation added on top. |
| `extra_noise_seed` | int | random | Seed for the noise layer (independent of `seed`). |

`inpaint` additionally **requires an inpainting model** (`*-inpainting`).
Passing a non-inpaint model raises `ValueError`.

#### `generate_image`-only: multi-character & vibes

| Param | Type | Notes |
|---|---|---|
| `character_prompts` | list[dict] | V4 / V4.5 / V5. Each dict: `{prompt, negative_prompt, x, y, enabled}`. `x`/`y` are center coords in 0.1–0.9. |
| `references` | list[str] | V4/V4.5 only. Base64 vibe tokens from `encode_vibe`; rejected on V5. |
| `straight_alpha` | bool | V5 only. True alpha channel; pair with `transparent background` / `has alpha`. |

#### Tool-specific params

- **`upscale_image`**: `image` (base64, required), `factor` (`2` or `4`,
  default `4`).
- **`director_tool`**: `tool` (required; `lineart`, `sketch`, `bg-removal`,
  `declutter`, `colorize`, `emotion`), `image` (base64, required), `prompt`
  (guides `colorize` + `emotion`), `defry` (0–10, line-art sharpening),
  `emotion` (required when `tool=emotion`; see `Emotion` enum for the 24
  names), `emotion_level` (0–5; 0 = normal, 5 = weakest).
- **`annotate_image`**: `image` (base64, required), `model` (required;
  `hed`, `midas`, `fake_scribble`, `mlsd`, `uniformer`).
- **`suggest_tags`**: `prompt` (required), `model` (default
  `nai-diffusion-4-5-full`), `language` (ISO 639-1, e.g. `en`, `ja`, `zh`).
  Returns `[{description, text, count}, ...]`.
- **`encode_vibe`**: `reference` (base64, required),
  `information_extracted` (0.01–1.0, default 1.0; lower = more stylistic,
  higher = more literal), `model` (must be V4/V4.5; V5 rejected). Returns a
  base64 vibe token string.

### Anlas cost awareness

**Always call `estimate_anlas_cost` before expensive generations** (large
`n_samples`, high resolution, many steps). It is pure/offline — no API call,
no Anlas charged — and mirrors NovelAI's public web-client formula.

```python
estimate_anlas_cost(
    width=832, height=1216, steps=28, n_samples=4,
    model="nai-diffusion-4-5-full", action="generate",
    opus=True
)
→ {"anlas": <int>, "opus_free_sample": <bool>}
```

Cost drivers, in order of impact:

1. **Resolution** (`width × height`) — dominant term. 4× the pixels ≈ 4× the
   cost (before per-sample rounding).
2. **Steps** — linear multiplier on the resolution term.
3. **`n_samples`** — linear. But Opus tier gets one **free sample** when
   `steps ≤ 28` and resolution ≤ 1024×1024 (returned as
   `opus_free_sample: true`); the formula subtracts that sample.
4. **SMEA** (`smea` ×1.2, `smea_dynamic` ×1.4, `auto_smea` ×1.2 for V4+
   only).
5. **`strength`** (img2img only) — scales cost proportionally; `strength=0.3`
   costs ~30% of a full gen.

Check the balance with `get_subscription` (returns `tier`, `active`,
`trainingStepsLeft`, etc.) before starting a long batch. Opus
(`tier` = All-Access) has substantially more Anlas than lower tiers and
unlocks the free-sample perk.

### Practical tool-call patterns

These show the **tool name + key arguments** an MCP host would send. They
are not CLI commands — for shell scripting see the `novelai-cli` skill, and
for multi-step recipes see the `novelai-workflows` skill.

#### Basic text-to-image (defaults)

```python
generate_image(prompt="a girl reading under cherry blossoms, soft light")
```

#### Reproducible batch at a fixed seed

```python
generate_image(
    prompt="study, 1girl, reading, detailed background",
    seed=42, n_samples=4,
    width=832, height=1216, steps=28, scale=5.0
)
```

#### Stronger prompt adherence

```python
generate_image(prompt="...", scale=7.0, steps=35, uc_preset=0)
```

#### Multi-character composition (V4.5 only)

```python
generate_image(
    prompt="two characters talking in a cafe",
    model="nai-diffusion-4-5-full",
    character_prompts=[
        {"prompt": "1girl, red hair, school uniform", "x": 0.3, "y": 0.5},
        {"prompt": "1boy, blue hair, barista apron",  "x": 0.7, "y": 0.5}
    ]
)
```

#### Vibe transfer (V4+ only)

```python
# 1. Encode a reference (do this once, reuse the token)
vibe_token = encode_vibe(reference=<base64>, information_extracted=0.5,
                         model="nai-diffusion-4-5-full")

# 2. Apply it
generate_image(prompt="...", references=[vibe_token])
```

`information_extracted` < 1.0 = more stylistic / less literal. Multiple
vibes can be passed in the list.

#### img2img: light refinement vs. heavy rework

```python
# Light touch-up (keep most of the input)
image_to_image(prompt="...", image=<base64>, strength=0.2, noise=0.0)

# Heavy rework (diverge from the input)
image_to_image(prompt="...", image=<base64>, strength=0.75, noise=0.1)
```

#### Inpaint a region

```python
inpaint(
    prompt="a book in her hand",
    image=<base64>,
    mask=<base64 of mask where non-transparent = redraw>,
    model="nai-diffusion-4-5-full-inpainting",   # inpaint model required
    strength=0.5
)
```

#### Upscale → Director → Annotate chain

Each step reads the previous tool's saved PNG, re-encodes to base64, and
feeds it to the next tool's `image` parameter.

```python
upscale_image(image=<base64>, factor=4)
director_tool(tool="lineart", image=<upscaled base64>, defry=5)
annotate_image(image=<lineart base64>, model="midas")
```

#### Prompt engineering with tag suggestions

```python
suggest_tags(prompt="1girl, out", model="nai-diffusion-4-5-full", language="en")
```→ [{"description": "...", "text": "outfit", "count": 12345}, ...]
```

Fold high-`count` suggestions back into `generate_image`'s `prompt`.

#### Cost check before a big batch

```python
estimate_anlas_cost(width=1024, height=1024, steps=50, n_samples=8,
                    model="nai-diffusion-4-5-full", opus=True)
# If anlas > remaining balance from get_subscription, reduce n_samples or steps.
```

### Tool inventory

| Tool | One-liner |
|---|---|
| `generate_image` | Text-to-image (V3 / V4 / V4.5, character prompts, vibe references) |
| `image_to_image` | Image-to-image with `strength` / `noise` |
| `inpaint` | Locally redraw a masked region (requires an inpaint model + mask) |
| `upscale_image` | 2× / 4× upscale via NovelAI's dedicated upscaler |
| `director_tool` | Line art / sketch / bg-removal / declutter / colorize / emotion |
| `annotate_image` | ControlNet preprocessor (hed, midas, fake_scribble, mlsd, uniformer) |
| `suggest_tags` | Complete/refine a prompt with NovelAI tag suggestions |
| `encode_vibe` | Encode a reference image into a vibe token for `generate_image` |
| `get_subscription` | Account subscription + Anlas balance |
| `get_user_data` | Authenticated account's email / chain / priority |
| `estimate_anlas_cost` | Offline Anlas cost estimate (no API call) |

All image-producing tools (`generate_image`, `image_to_image`, `inpaint`,
`upscale_image`, `director_tool`, `annotate_image`) return the same dual
payload (see §Image return format).

### Image return format

Every image-producing tool returns a **two-element list**:

1. An `ImageContent` block (base64 PNG) — the agent **sees** the image
   directly in the conversation. This is why the agent can self-critique
   composition, anatomy, and prompt adherence without the user pasting
   anything back.
2. A text string with the saved file path(s), e.g.
   `"Saved 4 image(s): ['C:\\...\\outputs\\generate-20260728-153012-001.png', ...]"`.

PNGs are written to `NOVELAI_OUTPUT_DIR` (default `outputs`, created if
missing). Filenames are timestamped with the operation name
(`generate-...`, `img2img-...`, `inpaint-...`, `upscale-...`,
`director-lineart-...`, `annotate-hed-...`).

> The dual return is intentional: the agent gets **visual feedback** for
> iteration *and* a **file path** to hand to downstream tools
> (`upscale_image`, `director_tool`, `annotate_image`) or the user. When
> chaining tools, pass the saved PNG's path forward by re-reading the file
> and base64-encoding it for the next tool's `image` parameter.

Internally the helper returns fastmcp's `Image` helper, which fastmcp
auto-converts to an `ImageContent` block — you do not need to construct
content blocks yourself when *calling* tools; this only matters if you
extend the server.

### Transport options

The server runs under one transport (set via `MCP_TRANSPORT` or `serve
--transport`):

- **stdio** (default) — for local agents (Claude Desktop, Cline). One
  process per agent; the MCP client spawns the server and communicates over
  stdin/stdout. Pooled `NovelAIClient` lives for the agent's session.
- **streamable-http** — for remote / multi-client / Docker. Listens on
  `http://<MCP_HOST>:<MCP_PORT>/mcp` (default `127.0.0.1:8000/mcp`).
  Authenticate by sending the NovelAI token in the `Authorization: Bearer
  pst-...` header; the server still needs `NOVELAI_TOKEN` configured to talk
  to NovelAI.

This skill does not cover client-side wiring (`mcpServers` JSON); see the
README's "Connect an agent" section for Claude Desktop / Cline / Docker
examples.

### Common pitfalls

- **Passing a non-inpaint model to `inpaint`** raises `ValueError`. Always
  use an `*-inpainting` model id.
- **`character_prompts` / `references` on V3/Furry** are silently ignored
  by the API. Switch to a V4/V4.5 model to use them.
- **`upscale_image` / `annotate_image` 404 on `image.novelai.net`** — they
  are routed to `api.novelai.net` automatically. Do not override
  `NOVELAI_LEGACY_IMAGE_BASE_URL` to point at `image.novelai.net`.
- **Unknown enum values** (`model`, `sampler`, `tool`, `emotion`,
  ControlNet `model`) raise `ValueError` with the accepted list in the
  message — read the error and retry with an exact value from the message.
- **`n_samples` above the resolution cap** raises `ValueError`. Drop
  `n_samples` or lower the resolution.

### Source reference

- Tool implementations:
  `apps/server/src/novelai_image_mcp/tools/{generate,enhance,tags,account}.py`
- Enums (models, samplers, director tools, emotions, controlnet):
  `apps/server/src/novelai_image_mcp/nai/constants.py`
- Parameter validation + Anlas formula:
  `apps/server/src/novelai_image_mcp/nai/models.py`
- Settings / env vars:
  `apps/server/src/novelai_image_mcp/settings.py`
- HTTP client + endpoint routing:
  `apps/server/src/novelai_image_mcp/nai/http.py`, `nai/client.py`
