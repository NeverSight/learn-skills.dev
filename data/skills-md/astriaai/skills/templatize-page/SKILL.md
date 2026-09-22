---
name: templatize-page
description: Use when the user asks to turn a fashion / lookbook webpage into an Astria pack — scrapes the page, drops product-only shots, turns the remaining lifestyle photos into pose references, and builds one swap prompt per pose. Two variants — shoe-swap (barefoot edit, swap the footwear) and general-pose (silhouette edit, swap any items the user picks — model, shoes, outfit, background…). Trigger phrases — "templatize this page", "make a pack from this lookbook", "/templatize-page <url>".
---

# Templatize Page

Given a brand's lookbook / collection / editorial URL, build an Astria pack
whose prompts let the user re-shoot that page's looks with their own
workspace references.

There are two variants:

- **shoe-swap** — barefoot-edit each lifestyle photo (remove the footwear) and
  build a prompt that swaps in a shoe reference. Footwear-only.
- **silhouette** — silhouette-edit each photo (keep only the posed figure) and
  build a prompt where the user picks *which* items to swap with references
  (model, shoes, outfit, bottoms, background, accessories). Whatever they
  don't swap is described in the prompt text instead.

Both variants end with one new pack (titled after the page), N new `pose`
tunes (one per surviving lifestyle image), and N new prompts inside the pack.

Two Python scripts ship with this skill in `scripts/` (stdlib only). They call
the bundled `astria` CLI for every API operation, so authentication and
workspace scoping are handled for you — see the `astria-api` skill.

The `${CLAUDE_SKILL_DIR:-$HOME/.codex/skills/templatize-page}` expansion in the
commands below resolves the skill directory in every runtime: Claude Code
exports `CLAUDE_SKILL_DIR`; the Codex-based Astria chat agent doesn't set it,
but installs this skill at `~/.codex/skills/templatize-page`.

## Workflow

### 1. Choose the variant

Ask the user with your ask-user question tool (`AskUserQuestion` in Claude Code, `ask_user` in the Astria chat agent; single select) before scraping:

- **Shoe-swap** — replace the footwear in every shot.
- **General pose (silhouette)** — keep the pose, swap any items they choose.

### 2. Scrape the page

```bash
python3 "${CLAUDE_SKILL_DIR:-$HOME/.codex/skills/templatize-page}/scripts/scrape.py" <url>
```

Emits JSON: `{"title": "...", "url": "<final url>", "images": [{"url": "...", "alt": "...", "width": ..., "height": ...}, ...]}`. The page `<title>` (or `og:title` when set) is the pack title — trim marketing cruft (price, "✓️", site name) to the product / collection name. Capture both — `title` for the pack, `images` for the next step.

### 3. Classify each image (drop packshots)

The scrape returns every visible image — including product-only shots (a shoe
on a plain background, no model) that we do NOT want as poses. Filter visually:

1. Download every candidate to `/tmp/templatize/` so they can be read locally:
   ```bash
   mkdir -p /tmp/templatize && i=0
   for url in <url1> <url2> ...; do
     i=$((i+1)); curl -sSL -o "/tmp/templatize/img_${i}.jpg" "$url"
   done
   ```
2. View each `/tmp/templatize/img_*.jpg` image. For each one decide:
   - **Keep** when a person is visible wearing or holding product (a lifestyle / editorial / on-model shot).
   - **Drop** when the frame is a product alone — a single shoe / sandal / handbag on a plain or studio backdrop with no human figure. Also drop logos, banners, swatches.
   - **When in doubt, keep.** A borderline cropped-from-the-knees shot is fine; the edit step will normalize it.
3. Build the list of surviving original URLs (the public URLs — the scripts pass them to Nano Banana). Keep the local paths too — the silhouette variant reads them again to compose prompts.

### 4. Templatize — branch on the variant

#### 4a. Shoe-swap variant

```bash
python3 "${CLAUDE_SKILL_DIR:-$HOME/.codex/skills/templatize-page}/scripts/templatize.py" \
  --pack-title "<page title>" \
  --pose-image-url <surviving_url_1> \
  --pose-image-url <surviving_url_2> \
  ...
```

The script: looks up the workspace's first shoe/sandal reference (`astria tunes list --name shoes --name sandals`, aborts if none); creates the pack; then per image barefoot-edits the photo, makes a `pose` faceid tune, and creates a `<faceid:pose><faceid:shoe>` swap prompt assigned to the pack.

#### 4b. Silhouette variant

The silhouette edit strips the figure down to its pose, so the prompt has to
rebuild everything else — references for the parts the user wants swappable,
plain text for the parts they don't.

**i. Ask which items to make swappable** — one page-wide ask-user question
with `multiSelect: true`. The references are shared across every pose, so this
is asked **once**, not per image. Offer these categories:

- Model / person
- Shoes
- Top / outfit (shirt, dress, jacket)
- Bottoms (pants, tights, skirt, shorts)
- Background / setting
- Accessories (bag, jewelry, eyewear, headwear)

Checked → swapped with a reference tune. Unchecked → described in the prompt text.

**ii. Pick a reference tune per checked category** — for each checked category,
list the workspace's tunes of that class and ask the user which one to use
(ask-user question, single select; batch up to 4 categories per call):

| Category        | `astria tunes list ...`                                              | prompt noun        |
|-----------------|----------------------------------------------------------------------|--------------------|
| Model / person  | `--name man --name woman --name person`                              | `woman` / `man`    |
| Shoes           | `--name shoes --name sandals`                                        | `shoes`            |
| Top / outfit    | `--name top --name shirt --name dress --name jacket --name outfit`   | `top` / `dress`    |
| Bottoms         | `--name pants --name tights --name jeans --name skirt --name shorts` | `pants` / `skirt`  |
| Background      | `--name background --name scene`                                     | (used as setting)  |
| Accessories     | `--name bag --name handbag --name jewelry --name accessory --name hat` | the item noun    |

If a checked category has no matching tune, tell the user and treat it as
unchecked (describe it in text instead).

**iii. Compose a prompt per image** — look at each surviving image again and
write a final prompt containing the literal placeholder `{pose}`:

```
Reproduce the same {pose} pose, <short pose description>, <references + descriptions>
```

- `{pose}` stays literal — `templatize.py` substitutes the new pose tune id.
- Add a brief pose description from the image (e.g. "leaning her hand on her knee").
- For each **checked** category: `<faceid:{ref_tune_id}:1> {noun}`.
- For each **unchecked** category visibly present in *this* image: a short text
  description (e.g. "green tank top", "white studio background"). Skip
  categories not present in the image.

Example (model + shoes checked; top, accessories, bottoms, background described):

```
Reproduce the same {pose} pose, leaning her hand on her knee, <faceid:4425929:1> woman with <faceid:4363887:1> shoes, green tank top, apple in-ear headset with wire, short blue tights, white studio background
```

**iv. Write the spec** — write `/tmp/templatize/spec.json`, a JSON array of
`{"url": "<original image url>", "prompt": "<composed prompt with {pose}>"}`
objects, one per surviving image.

**v. Run the script**

```bash
python3 "${CLAUDE_SKILL_DIR:-$HOME/.codex/skills/templatize-page}/scripts/templatize.py" \
  --mode silhouette \
  --pack-title "<page title>" \
  --spec /tmp/templatize/spec.json
```

The script: creates the pack; then per image silhouette-edits the photo, makes
a `pose` faceid tune, substitutes the new pose tune id into the prompt's
`{pose}` placeholder, and creates the prompt assigned to the pack.

Both variants accept `--workspace <id>` to target a specific workspace;
otherwise the `astria` CLI's configured workspace is used. They also accept
`--aspect-ratio <ratio>` to force one output ratio for the whole run — by
default each source image is downloaded, measured, and the pack prompt
rendered at the closest standard ratio. Each prints one status line per
artifact to stderr and a final summary block to stdout with the new pack ID
and per-pose `prompt_id` / `pose_tune_id` pairs.

### 5. Report

Surface the new pack to the user — quote the pack title + ID, the number of
prompts created, and point them to `/packs/<pack_id>`.

## Worked examples

**Shoe-swap.** `/templatize-page https://www.gentlesouls.com/lookbook/spring-2026`

1. Variant question → shoe-swap.
2. `scrape.py` → `title="Gentle Souls Spring 2026 Lookbook"`, ~14 images.
3. Download all 14, view each — 5 packshots dropped, 9 on-model kept.
4. `templatize.py --pack-title "Gentle Souls Spring 2026 Lookbook" --pose-image-url ...` (9 URLs).
5. Report: "Created pack **Gentle Souls Spring 2026 Lookbook** (id 4821) with 9 shoe-swap prompts using reference *Brown leather sandal* (id 4457109) — /packs/4821."

**Silhouette.** `/templatize-page https://brand.com/editorial/resort`

1. Variant question → general pose (silhouette).
2. `scrape.py` + classify → 6 lifestyle images kept.
3. Checkbox → user checks **Model** and **Shoes**.
4. Reference questions → Model = tune 4425929 *"Studio model — Maya"*, Shoes = tune 4363887 *"Tan block-heel sandal"*.
5. Per image, view it and compose a `{pose}` prompt — refs for model + shoes, text for the unchecked top / bottoms / background. Write `spec.json`.
6. `templatize.py --mode silhouette --pack-title "Resort Editorial" --spec /tmp/templatize/spec.json`.
7. Report: "Created pack **Resort Editorial** (id 4830) with 6 general-pose prompts — /packs/4830."

## Notes

- The barefoot / silhouette edit prompts are deliberately conservative — they keep the pose so the resulting tune captures the original styling minus the swapped-out parts.
- `tune[name]` is hardcoded to `pose` (every output should be usable as a pose ref regardless of the original subject).
- The pack uses `model_type=faceid` because the prompts inside reference faceid tunes (pose + the swapped references). Generation defaults: `resolution=2K`, `num_images=1`. The barefoot / silhouette **edit** leaves `aspect_ratio` unset so it follows the input image (Gemini rejects `aspect_ratio=auto`); the **pack prompt** is rendered at the source image's aspect ratio — `templatize.py` downloads each source image, measures it, and snaps to the nearest standard ratio (`1:1 2:3 3:4 4:5 9:16 5:4 4:3 3:2 16:9 21:9`), defaulting to `3:4` when the image can't be read. Pass `--aspect-ratio 3:4` to force one ratio for the whole run.
- Astria dedups prompts by `(text, seed)` within a tune, so an identical edit instruction on two source photos would collapse onto one prompt. `templatize.py` gives each edit a per-image seed (derived from the source URL) — never append a marker to the prompt text, Nano Banana may render it into the image.
- If the page is gated (Shopify login wall, paywall) `scrape.py` returns empty `images` — fall back to asking the user for direct image URLs.
