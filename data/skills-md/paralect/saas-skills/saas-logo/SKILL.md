---
name: saas-logo
description: "Generate a logo mark for a software product in the manner of Notion, Linear, Vercel, Slack, Miro, Airtable, Intercom, PostHog, Webflow, Mintlify and Claude — one flat geometric symbol, in one of the five families those marks fall into — through an image model, several concepts at once, then pick, and cut the pick into transparent PNGs ready to drop into a site: the mark alone and the app-icon tile. Use when asked for a logo, logomark, app icon, brand mark, favicon or icon for a product, \"like Linear's\" or \"like Slack's\", or a logo in the style of a named SaaS brand."
---

# SaaS logo

Every file this skill uses ships in its own folder, next to this SKILL.md, and paths here are relative to that folder. It needs nothing from other skills or other folders, so don't go looking for them. Unless the user names another place, save everything it makes in `out/saas-logo/` under the current project.

One symbol, flat. What comes back is the mark alone on a transparent
background, trimmed to its edges, plus the same mark on its app-icon tile:
files that drop straight into a site. The marks this skill draws from are studied in
`references/analysis.md`: what each of the eleven is as geometry, the eight
rules they all keep, and the five families they fall into. Read it once before
the first logo; it is what "looks like a real SaaS logo" means here.

The prompt sent to the image model lives in `prompt.md` and carries everything
the model needs: the shared rules (canvas, tile, flat fills, weight, colour)
and the five families the reference marks fall into, each with its own rules.
Your job is the thinking before the prompt (the family and the symbol) and the
judging after.

## Steps

### 1. Learn the product

Read the brief, README, landing copy, whatever exists. Write one line: *"Name —
what the user does with it, in one verb, on one object."* "Hands tasks to
coding agents" → *hand over, a task card*. "Publishes a folder as a site" →
*publish, a page*. The mark shows the verb or the object, never the category
(no gear, cloud, rocket, chart). Note the brand colour if the product has one
(its CSS tokens, its favicon) and its initial.

### 2. Pick a family

The five families in `prompt.md` section 3, with what each is best for:

- **Solid primitive** (Vercel, Miro): infrastructure, developer tools,
  anything that wants to feel inevitable, where one shape carries the idea.
- **Repeated primitive** (Slack, Claude, Linear, Intercom, PostHog):
  collaboration, communication, AI, anything about many parts moving together.
- **Letterform** (Webflow, Miro, Notion): a product whose name is its brand,
  when the initial has a strong shape (A, M, N, W, K, Z, S, V).
- **Faceted object** (Airtable, Notion's page): data, storage, documents,
  anything with a thing you fill or stack.
- **Soft stroke** (Mintlify, Intercom): friendly consumer-facing products,
  docs, support, anything warm rather than technical.

When the user names a reference brand, the family is given: "like Slack" or
"like Claude" → Repeated primitive; "like Vercel" → Solid primitive; "like
Webflow" or "like Notion" → Letterform; "like Airtable" → Faceted object;
"like Mintlify" or "like Intercom" → Soft stroke. When the user names a family,
use it. When nothing points anywhere, spread the concepts over two or three
families; the sheet decides.

### 3. Write 3–4 concepts

Each concept is 2–3 sentences the image model can draw without guessing:

- **Symbol as geometry**, not as a noun. Not "a task card" but "one rounded
  rectangle, wider than tall, with a second identical one behind it offset up
  and right by a quarter of its height". Not "a hash" but "four pills, each a
  bar with a round bump at one end, turned 90° around the centre".
- **The count and the rhythm** for a repeated primitive: "five vertical bars,
  heights stepping 3-5-4-2-3 left to right".
- **The family**, named, and for a letterform which letter and which two or
  three strokes.
- **The colour**: the brand colour by hex when there is one, or "black tile,
  white mark" or "marigold tile, black mark".
- **Exclusions** when the concept invites extras: "no dot", "no frame around
  the bars", "the counter stays empty".

Make the silhouettes differ across concepts (tall vs wide, one mass vs
scattered). Drop any concept that needs more primitives than its family allows,
or a colour the family forbids.

### 4. Compose and generate

For each concept, take `prompt.md` and replace `{{input}}` with:

```
<Product> — <what it is and does>. The verb is <verb>; the object is <object>.
Brand colour: <hex or "none">. Initial: <letter>.
Family: <one of the five>

Concept: <the concept from step 3>
```

Generate all concepts in parallel through OpenRouter (below), one image each,
square. Save as `<concept>.png` or `.jpg`, whichever came back (the snippet
below tells them apart).

Default model: `google/gemini-3.1-flash-lite-image` (Nano Banana 2 Lite),
the cheapest and quickest; it handles flat geometry well enough for the
whole run, and a concept that fails on it usually fails on the others too.
Step up only when asked, or when a keeper needs a cleaner render than two
rounds give: `google/gemini-3.1-flash-image` (Nano Banana 2), then
`google/gemini-3-pro-image` (Nano Banana Pro), which draws the cleanest
geometry: flat ends, even weight, true flat fills.

### 5. Look

Row the tiles up with `bash <this skill folder>/scripts/sheet.sh sheet.png a.png b.png …` and
open it. To see the references next to them, `bash <this skill folder>/scripts/fetch-references.sh
out/saas-logo/references` pulls the eleven marks through Brandfetch into a sheet of
their own (it needs a Brandfetch client ID; see the script's header). Judge
each tile the way the analysis judges the references:

- **Flat** — one fill per shape, no gradient, no shadow, no bevel. Anything
  else is a re-roll, not a keeper.
- **Committed corners** — all sharp or all round, as the family says.
- **Count** — the primitives the concept named and no more. An extra dot, a
  frame, a notch is a failure to name in the re-roll ("no frame around the
  bars").
- **Silhouette** — squint. One clear shape at 16px, no accidental second
  picture: three bars and a curve become a face, a chevron and a dot become a
  cursor, four pills become a windmill.
- **Meaning** — can you tell the verb or the object without the name? If it
  reads as a category icon, the concept is wrong, not the render.
- **Canvas** — tile centred on flat grey, nothing else on it, no text. Tile
  size and the exact colour vary a little between renders; that is normal.
  When a set has to match exactly, generate it all in one round with one
  model, or crop to the tile.

Re-roll only what failed, with the concept sharpened to name the failure. Two
rounds is normal; a concept that fails twice is usually the concept, not the
model. Replace it.

### 6. Cut

The render is a working file: a grey canvas with the tile on it. Cut every
keeper into the files that get used:

```bash
bash <this skill folder>/scripts/cut.sh <concept>.png out/saas-logo/<product> --name <product>
```

It writes `<product>-mark.png`, the mark alone on a transparent background,
trimmed to its edges with no padding, and `<product>-tile.png`, the rounded
app-icon tile with transparent corners. The canvas colour is read from the
render's corners and the tile colour from a band inside the tile's edge, and
edge pixels are unmixed from them, so the edges stay soft with no halo. When
several concepts are delivered, name them apart (`--name relay-bars`,
`--name relay-block`). The first run makes a small Python venv with Pillow
and NumPy in `scripts/.venv` inside this skill; after that it is instant.

Open the two files over a dark and a light background and check: no fringe of
tile colour along the mark's edge, no sliver of canvas at the tile's corners,
nothing of the mark clipped. A fringe means the render's tile wasn't flat
(a gradient or a vignette crept in); re-roll the render rather than patching
the cut. A faint colour tint right at the edge, seen only zoomed in, is JPEG
noise from the Lite and Flash models; when it matters, render the keeper once
more with `google/gemini-3-pro-image`, which answers in PNG.

### 7. Deliver

Put the mark and tile PNGs in `out/saas-logo/<product>/`. Copy them to where the
product keeps brand assets (`public/`, `brand/`, `assets/`) only when the user asks.
Keep the renders and `sheet.png` out of the way, in a `renders/` folder next to
them. In the summary name the recommended `-mark.png` and
`-tile.png` by path, say which concept you recommend in one line and why, and list the others as alternatives with their files.

## Generating through OpenRouter

The API key comes from `OPENROUTER_API_KEY`. If it isn't set, stop and ask the user
to set it rather than guessing at another provider.

```bash
KEY="$OPENROUTER_API_KEY"

# request.json: {"model": "google/gemini-3.1-flash-lite-image", "prompt": "<the composed prompt>", "aspect_ratio": "1:1"}
curl -sS https://openrouter.ai/api/v1/images \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d @request.json > response.json

python3 - <<'PY'
import base64, json, pathlib
data = json.loads(pathlib.Path("response.json").read_text())["data"][0]
image = base64.b64decode(data["b64_json"])
# Lite and Flash answer with JPEG bytes, Pro with PNG; name the file for what it is.
ext = "png" if image.startswith(b"\x89PNG") else "jpg"
pathlib.Path(f"concept.{ext}").write_bytes(image)
PY
```

`scripts/sheet.sh` and `scripts/cut.sh` take either format.

## Files

- `prompt.md` — the prompt template; `{{input}}` takes the product line, the
  family and the concept. Section 3 of it holds the five families.
- `references/analysis.md` — the study of the eleven marks: each one as
  geometry, the rules they share, the five families.
- `scripts/fetch-references.sh` — pulls the reference marks through
  Brandfetch's Logo API (client ID from `BRANDFETCH_CLIENT_ID`) into a folder and a sheet; any list of
  domains works, for a different set of references.
- `scripts/sheet.sh` — rows tiles up on the grey canvas (needs
  `rsvg-convert`; `brew install librsvg`).
- `scripts/cut.sh`, `scripts/cut.py` — cuts a render into the transparent
  mark and tile PNGs that get delivered.
