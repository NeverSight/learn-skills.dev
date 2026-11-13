---
name: gpt-image
version: 3.0.0
description: |
  Generate or edit images via GPT Image 2.6 Flare or Sunburst through
  DroidProxy Codex OAuth (no OPENAI_API_KEY). Use when the user asks to
  generate, create, draw, or edit an image with GPT, OpenAI, Codex,
  gpt-image, or DALL-E, including transparent PNGs, and DroidProxy Codex
  OAuth is available. Prefer this over inventing image URLs or base64. If
  they name Grok or Imagine, use grok-imagine instead.
---

# GPT Image 2.6 (via DroidProxy Codex)

POST `http://localhost:8317/v1/images/generations` (or `/edits`) with
`Authorization: Bearer dummy-not-used`. Default to `gpt-image-2.6-flare`;
choose `gpt-image-2.6-sunburst` for detail and edit consistency. No dated
2.6 snapshots are documented. Never use an `OPENAI_API_KEY` with this skill.
These are Images API models, not chat models: do not register them in the
Factory chat-model picker or send them to `/v1/responses` or chat completions.

**Compatibility, checked November 4, 2026:** the installed CLIProxyAPI route
rejects both 2.6 IDs with HTTP 400 ("Model ... is not supported"). Upstream's
image allowlist also lacks them. This skill prepares the documented requests,
but does not upgrade that backend or claim working 2.6 OAuth access.
OpenAI's all-tier ChatGPT/Codex availability announcement does not establish
whether this OAuth backend accepts these IDs or new fields.
Keep the model and new features explicit/configurable. Never silently rename
2.6 to 2.5, drop markup, or return a raster image as an SVG/GIF.

Default to **Flare** for fast, high-quality everyday generation. Use
**Sunburst** when the user prioritizes demanding quality, editing precision,
or subject preservation over latency. If Sunburst meets the requirements,
prefer Flare only after it produces acceptable results on the same prompt,
references, dimensions, and quality setting.

Use this for generating or editing visual assets, not for understanding an
image the user already attached.

## Run the bundled helper (Bun, no dependencies)

Resolve `scripts/image.ts` relative to this installed skill, not the user's
working directory. Write request JSON to a file, then run:

```bash
SKILL="$HOME/.factory/skills/gpt-image"
bun "$SKILL/scripts/image.ts" generate /absolute/request.json /absolute/workspace/asset
```

The last argument is an output **prefix**, without an extension. The helper
decodes all `data[].b64_json` results, inspects their bytes, saves `.png`,
`.jpeg`, `.webp`, `.svg`, or `.gif` (numbered when `n>1`), and prints file
paths and response metadata. Embed the resulting absolute path in Markdown.
It never retries, substitutes a model, reads OAuth tokens, or logs image data.

| Configuration | Default | Purpose |
|---|---|---|
| `GPT_IMAGE_MODEL` | JSON `model`, else `gpt-image-2.6-flare` | Explicit override, including an older supported ID. |
| `GPT_IMAGE_FEATURES` | empty | Comma-separated opt-ins: `complexity,markup,svg,gif`. Only enable fields your backend accepts. |
| `GPT_IMAGE_MAX_FRAMES` | unset, API validates upper bound | Optional integer cap, e.g. `16` or `64`, while official docs disagree. |
| `GPT_IMAGE_PROXY_URL` | `http://localhost:8317` | Loopback HTTP origin only; no API-key or remote-provider mode. |

For a backend that rejects 2.6, explicitly select a known available older
model for a raster-only request, without new unsupported fields:

```bash
GPT_IMAGE_MODEL=gpt-image-2.5-flare \
  bun "$SKILL/scripts/image.ts" generate /absolute/request.json /absolute/workspace/asset
```

Preserve older API model IDs: `gpt-image-1-mini`, `gpt-image-1.5`,
`gpt-image-2`, `gpt-image-2-2026-04-21`, `gpt-image-2.5-flare`,
`gpt-image-2.5-flare-2026-09-08`, `gpt-image-2.5-sunburst`,
`gpt-image-2.5-sunburst-2026-09-08`, and `chatgpt-image-latest`.
The existing backend alias `gpt-image-2.5` is also passed through.
OpenAI API support is not a promise of OAuth backend support; older models
may have different parameter limits. `gpt-image-1` shut down October 23, 2026.

## Generate

Requests often take 15–70s. Use `--max-time 180`. Default `quality` to
`auto`; select a higher explicit setting only to meet a quality requirement.

```bash
RESP=$(curl -sS --max-time 180 http://localhost:8317/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dummy-not-used" \
  -d "$(jq -n --arg p "A red balloon on a wooden table, soft natural light" \
    '{model:"gpt-image-2.6-flare", prompt:$p, size:"1024x1024",
      quality:"auto"}')")

if B64=$(printf '%s' "$RESP" | jq -er '.data[0].b64_json' 2>/dev/null); then
  printf '%s' "$B64" | base64 -d > out.png
else
  printf '%s\n' "$RESP" >&2
  exit 1
fi
```

Check the HTTP status and `.data[0].b64_json` before decoding. Codex errors
are JSON (`usage_limit_reached`, `auth_not_found`, `moderation_blocked`).
Report the error code/message, not request headers, credentials or image data.

## Edit

Same auth. Prefer JSON with a data URL, with no upload step. Public API
`file_id` inputs require access to that file and are not verified on OAuth. Do **not**
pass the data URL through `jq --arg`: a typical generated PNG is larger
than `ARG_MAX` (~1MB on macOS) and `jq` dies with `Argument list too long`.
Write the data URL to a file and use `--rawfile`, then POST with
`--data-binary`. Decode the same way as Generate.

```bash
SRC_FILE=$(mktemp)
REQ=$(mktemp)
printf 'data:image/png;base64,%s' "$(base64 -i ./photo.png)" > "$SRC_FILE"
jq -n --arg p "Make it blue-tinted studio lighting" --rawfile u "$SRC_FILE" \
  '{model:"gpt-image-2.6-sunburst", prompt:$p, images:[{image_url:$u}],
    quality:"auto"}' > "$REQ"

RESP=$(curl -sS --max-time 180 http://localhost:8317/v1/images/edits \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dummy-not-used" \
  --data-binary @"$REQ")
rm -f "$SRC_FILE" "$REQ"

if B64=$(printf '%s' "$RESP" | jq -er '.data[0].b64_json' 2>/dev/null); then
  printf '%s' "$B64" | base64 -d > out.png
else
  printf '%s\n' "$RESP" >&2
  exit 1
fi
```

Pick the data-URL mime from the source (`image/jpeg`, `image/png`,
`image/webp`). Optional `mask.image_url` (PNG with alpha) marks the region
to replace. Chain edits by feeding each output back as the next
`images[0].image_url`.

## Markup-guided edits (opt-in)

Keep the original as `images[0]`. Make a separate transparent PNG overlay
with circles, arrows, sketches or labels. After orientation, it must match
the first input's pixel dimensions and contain transparent pixels. Each may
have at most 16,777,216 pixels; the overlay must be at most 50 MB.
Do not flatten the overlay onto the source or combine `markup` with `mask`
or `prompt_rewriter`. Check these file properties locally before sending;
the helper checks JSON shape, not image dimensions or alpha.

JSON uses `images` and a `markup` object with **exactly one** of `image_url`
(HTTPS or base64 PNG data URL) or `file_id`. Additional images are references.
For local files, avoid `ARG_MAX` by writing data URLs to files:

```bash
base64 -i /absolute/photo.png | tr -d '\n' > /tmp/photo.b64
base64 -i /absolute/overlay.png | tr -d '\n' > /tmp/overlay.b64
jq -n --rawfile photo /tmp/photo.b64 --rawfile overlay /tmp/overlay.b64 \
  '{model:"gpt-image-2.6-sunburst",
    prompt:"Make only the circled vase cobalt blue. Preserve everything else. Remove the annotations.",
    images:[{image_url:("data:image/png;base64,"+$photo)}],
    markup:{image_url:("data:image/png;base64,"+$overlay)},quality:"medium"}' > /tmp/edit.json
GPT_IMAGE_FEATURES=markup bun "$SKILL/scripts/image.ts" edit /tmp/edit.json /absolute/workspace/vase
```

The public API also accepts multipart field `markup` (PNG file) alongside
`image` and `prompt` on `/v1/images/edits`. Prefer the JSON path through
DroidProxy: binary multipart forwarding and markup handling by CLIProxyAPI
are not verified. Markup has no extra fee.

## SVG export (generations only, opt-in)

Example request file:

```json
{"model":"gpt-image-2.6-flare","prompt":"A simple editable vector icon of a red balloon, clean paths and flat colors.","output_format":"svg","n":1,"quality":"medium","complexity":"low"}
```

```bash
GPT_IMAGE_FEATURES=svg,complexity \
  bun "$SKILL/scripts/image.ts" generate /absolute/svg-request.json /absolute/workspace/balloon
```

SVG requires `n=1`. Omit streaming, `partial_images`, `output_compression`,
and `prompt_rewriter`. Quality and complexity control the reference image
used to author the SVG. Base64-decode `data[0].b64_json` as UTF-8 XML and
save `.svg`, not PNG. Edits accept neither SVG input nor SVG output.
Inspect the XML before embedding it; do not treat untrusted SVG as executable
HTML. SVG incurs the reference image cost plus the unnamed authoring model's
token rate, so there is no documented fixed total SVG price.

## Animated GIF (generations only, experimental opt-in)

```json
{"model":"gpt-image-2.6-flare","prompt":"A red balloon gently bobbing up and down in a seamless loop, locked camera.","output_format":"gif","frame_count":9,"frame_duration_ms":200,"size":"auto"}
```

```bash
GPT_IMAGE_FEATURES=gif GPT_IMAGE_MAX_FRAMES=16 \
  bun "$SKILL/scripts/image.ts" generate /absolute/gif-request.json /absolute/workspace/balloon
```

GIF may need preview access. The guide says `frame_count` 2–64, but the API
reference says 2–16. Do not hard-code either as universal: set an optional
local cap and let the API validate. Defaults are 9 frames and 200 ms.
`frame_duration_ms` is 20–2000, rounded by the API to 10 ms. Frame fields
are GIF-only. Omit streaming, partial images, compression and
`prompt_rewriter`. Save decoded binary as `.gif`; never rename a PNG to GIF.
If a pixel-budget error occurs, reduce frames, frame size, or `n`.

## Prompting

If the user gives a detailed prompt or asks you to use theirs, use it
verbatim. Otherwise define the intended result, then describe the subject,
action/pose, setting, style, composition, lighting/mood, visible details, and
constraints. For complex work, use labeled sections. Keep requirements easy
to read rather than relying on special prompt syntax.

Quote required text exactly, specify its placement and typography, ask for no
extra text, and verify spelling and legibility. For edits, say “change only X”
and explicitly list what must stay the same. Identify each reference image by
number and role (subject, style, clothing, or background). Make one change per
edit and restate critical preservation constraints on every turn.

Ground named people, brands, places, and “current/latest” facts with a web
search first. For a named real person, edit from a real reference photo —
do not generate the likeness from text alone.

## Parameters

| Field | Values | Notes |
|---|---|---|
| `model` | `gpt-image-2.6-flare`, `gpt-image-2.6-sunburst` | Flare by default; Sunburst for demanding quality or precise edits. Older IDs remain configurable. |
| `prompt` | string | Required on generate and edit. |
| `size` | `auto`, `1024x1024`, `1536x1024`, `1024x1536`, custom `WIDTHxHEIGHT` | 2.6 custom limits are not explicitly documented; pass through for API validation. The 2.5 limits (edges ≤3840, multiples of 16, ratio 1:3–3:1, 655,360–8,294,400 px) are not a 2.6 contract. |
| `quality` | `auto`, `low`, `medium`, `high`, `xhigh`, `max` | Default `auto`. Compare one setting at a time; use `xhigh`/`max` only for an unmet quality requirement. Never send `hd` or `standard`. |
| `complexity` | `low`, `medium`, `high` | Default `high` if omitted; independent of quality. Lower for focused edits, higher for dense text/layouts. No separate fee; can affect latency and unwanted changes. SVG: reference-image complexity. |
| `n` | 1–10 | Default 1. Same-prompt variations use `n`, not parallel calls. |
| `background` | `auto`, `opaque`, `transparent` | `transparent` needs `output_format` `png` or `webp`. |
| `output_format` | `png`, `jpeg`, `webp`; `svg`, `gif` on generations only | Send `png` for transparency. SVG/GIF are opt-in. |
| `output_compression` | 0–100 | JPEG/WebP only. Omit unless asked. |
| `images` | `[{image_url}]` or `[{file_id}]` | Edits only. Raster data URL or HTTPS URL; file IDs not verified on OAuth. |
| `mask` | `{image_url}` | Edits only. PNG with alpha. |
| `markup` | `{image_url}` or `{file_id}` | Edits only; exactly one source. Transparent PNG annotation overlay; incompatible with mask and prompt_rewriter. |
| `frame_count` | ≥2; conflicting published upper limits 16/64 | GIF only; default 9. Configurable local cap; API validates. |
| `frame_duration_ms` | 20–2000 | GIF only; default 200, rounded to 10 ms. |

## Response

```json
{"created": 0, "background": "opaque", "data": [{"b64_json": "..."}],
 "output_format": "png", "quality": "low", "size": "1536x1024", "usage": {}}
```

GPT Image returns base64, so do not send `response_format`.
`.data[0]` is only `b64_json` — no `url`, no `mime_type`. Pick the file
extension from top-level `output_format` when present, otherwise from the
decoded magic bytes (`PNG` / `JFIF` / `RIFF…WEBP`).

Previously observed with 2.5: Codex OAuth often ignores `size` and sometimes `quality`. A `1024x1024` /
`low` request may come back `1536x1024` / `low`, or an off-enum size like
`1312x1199` with `quality: medium`. Trust the response `size` / `quality` /
`background` and the decoded IHDR. Do **not** retry just because they
differ from the request.

## Transparency

When the user **explicitly** wants a transparent PNG or alpha background
(sticker, cutout, icon), send both:

```json
{"background":"transparent","output_format":"png"}
```

If they asked for a campaign, slide, or print asset without mentioning
transparency, keep opaque or ask. Don't assume.

The prompt beats `background`. If it describes a backdrop, scene, color,
plinth, or shadow, the model paints that instead of alpha. Keep the prompt
on an isolated subject and say so explicitly:

- Isolated object, fully visible, generously padded
- Actual fully transparent alpha
- No backdrop, rectangle, plinth, cast shadow, watermark, or readable label text
- Preserve natural transparency, refraction, and fine material edges (glass, ribbon, fibers)

Size by use: icons/stickers `1024x1024`, product shots `1024x1536`, charts
`1536x1024`. Compare `medium` or `high` when the asset has small text.
Expect the returned pixel size to differ; that's not a failure.

**Products / campaign cutouts.** One object. No scene. Ask for fully
transparent alpha around the silhouette. Good for reuse across storefronts
and seasonal backgrounds.

**Charts for dark slides.** Ask for a genuinely transparent background
*and* a transparent plot area — not just a transparent silhouette. No
card, frame, filled panel, title, or grid fill. Specify pale/white labels
and bright series colors so they read on navy or gradient themes. Keep
exact data values in the prompt, then verify labels and proportions
against the source before using the chart.

**Icons, stickers, decorations.** Keep everything outside the tile, die-cut
border, or sprig transparent — including gaps between branches and leaves.
No text, watermark, or drop shadow.

**Print-on-demand.** Generate the artwork and any blank garments as
separate transparent PNGs. Keep open space *inside* the design transparent
too (no white rectangle or badge). Composite locally; do not bake the
print onto the garment in one generation if they need to reuse it.

After decoding, confirm a real alpha channel (RGBA / PNG `tRNS`) and that
some pixels are fully transparent. Also check top-level
`"background":"transparent"`. If the file is opaque, strip backdrop
language from the prompt and retry once.

If `background:transparent` 400s, generate on a flat uniform background
that contrasts with the subject and key it out locally (PIL, ImageMagick).
Recolor the subject for the background they named before you finish — a
near-black mark on a dark header is invisible. Say what you did.

## API pricing and quota

Both 2.6 variants have the same published rates, per 1M tokens:

| Token type | Input | Cached input | Output |
|---|---:|---:|---:|
| Text | $5 | $1.25 | — |
| Image | $8 | $2 | $30 |

These are public API rates, not a subscription charge or guaranteed cache
discount on this OAuth route. No fixed per-image price, published rate-limit
table, or image-specific subscription quota is available. Limits vary by
tier. Do not infer remaining image quota from the Codex text-token gauge.
Use returned usage/errors and reset information; do not probe in a loop.

## Failures

| Symptom | Fix |
|---|---|
| Connection refused | DroidProxy isn't running — tell the user to launch it |
| `auth_not_found` / no auth for `codex` | Check Settings → Connect Codex. Older backends reject Free accounts; 2.6 is announced for all ChatGPT/Codex tiers, but this route's tier support is unverified. |
| `usage_limit_reached` (`plan_type`, `resets_in_seconds`) | Quota exhausted. Tell the user when it resets. Do not retry in a loop. |
| 401 after a long idle | OAuth session dead — Settings → Connect Codex |
| 400 unsupported model | The backend may not allow 2.6 yet. Report the rejection. Explicitly select a known older ID for raster-only work, or wait for a backend update; never silently downgrade. |
| Unsupported complexity/markup/SVG/GIF | Disable that opt-in only if the user accepts losing the feature. Do not discard annotation guidance or claim a different format succeeded. |
| Format mismatch | Helper refuses to save raster bytes under `.svg`/`.gif`. Report the backend's actual format. |
| `jq: Argument list too long` | You put a data URL in `jq --arg`. Use `--rawfile` as in Edit. |
| Response `size`/`quality` ≠ request | Not a failure. Save the image. Do not retry. |

On `moderation_blocked`, stop. Don't retry and don't paraphrase the prompt
to evade the filter. Report the API's own message. Never invent image
content or a URL for a request that failed.

## Sources

- [GPT Image 2.6 Flare](https://developers.openai.com/api/docs/models/gpt-image-2.6-flare)
- [GPT Image 2.6 Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.6-sunburst)
- [Image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting)
- [Image generation guide](https://developers.openai.com/api/docs/guides/image-generation)
- [Images generate reference](https://developers.openai.com/api/reference/cli/resources/images/methods/generate/index.md)
