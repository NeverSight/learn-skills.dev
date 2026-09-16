---
name: grouchygiraffe-ingest
description: Full grouchygiraffe ingestion workflow — given a grouchygiraffe media file path, a loose image such as a pasted or screenshotted thumbnail, or a recipe URL (YouTube, Instagram, or any recipe page), identify the recipe, upload the thumbnail to Imgur where applicable, and write a cleaned recipe note to the vault.
---

## Grouchygiraffe Ingest Workflow

The argument is either a local file path or a URL.

Detect the input mode from the argument:
- If it starts with `http://` or `https://`: **URL mode** — skip to the URL path below
- Otherwise: **file mode** — follow the file path below

File mode covers both a media file that already lives in the grouchygiraffe data directory and a loose image such as a pasted or screenshotted thumbnail. Do not assume a loose image is unrelated to grouchygiraffe — Step 0 below decides that, and it decides it cheaply.

Do not prompt the user between steps unless a step fails.

---

## URL mode

When the argument is a URL, skip Steps 1 and 2 of the file flow and go directly to recipe-cleanup, with one variation depending on the URL type:

**YouTube URLs** (`youtube.com/watch?v=...` or `youtu.be/...`):

Invoke the `recipe-cleanup` skill with the YouTube URL directly.

`recipe-cleanup` extracts the video thumbnail from YouTube and sets the `pic` field — no separate Imgur upload is needed.

**Instagram or other social media URLs**:

First invoke the `social-to-imgur` skill with the URL to get a permanent Imgur thumbnail URL.

Then invoke the `recipe-cleanup` skill with the URL.

After `recipe-cleanup` writes the file, update the `pic` frontmatter field to use the Imgur URL — social CDN URLs expire.

**Final report (URL mode)**:

After all steps complete, report:
- The recipe name
- The author's name
- The recipe file path written to the vault
- The source URL

---

## File mode

The data directory is `/Users/mtm/pdev/taylormonacelli/grouchygiraffe/data` — referred to below as DATA.

Every archived post is stored there as `<shortcode>.mp4` (or `.jpg`), `<shortcode>.yaml`, and `<shortcode>_thumb.jpg`.

Resolve the file to a shortcode first (Step 0), then run the three skills in order.

### Step 0: resolve the input file to a shortcode

If the file already lives in DATA (e.g. `/Users/mtm/pdev/taylormonacelli/grouchygiraffe/data/DX9oSBkjsZR.mp4`), the shortcode is the filename without its extension and without any trailing `_thumb`. Go straight to Step 1.

Otherwise the argument is a loose image — a pasted screenshot, a saved thumbnail, a file in a job or downloads directory. Recover the shortcode by content hash before doing anything else.

An image saved or pasted from an Instagram post is frequently byte-identical to the `_thumb.jpg` grouchygiraffe already archived for that post, so an exact digest match identifies the post outright and costs two commands.

Hash the input:

```
md5 -q <input_file>
```

Write the digests of every archived thumbnail to a scratch file, then search it for that digest:

```
md5 -r <DATA>/*_thumb.jpg > "$TMPDIR/gg_thumb_digests.txt"
```

```
rg "^<digest>" "$TMPDIR/gg_thumb_digests.txt"
```

A hit gives a path of the form `<DATA>/<shortcode>_thumb.jpg`. Strip the directory and the `_thumb.jpg` suffix to get the shortcode, then continue with Step 1 using it.

**If no digest matches**, the image was re-encoded, cropped, or resized somewhere along the way — or it genuinely is not from an archived post. Do not conclude the latter yet, and do not fall back to treating the image as an orphan until this search comes up empty too:

Read the image and identify the dish and any visible text overlay.

Search the archived captions for it, e.g. for a dish identified as hash browns:

```
rg -il "hash brown" --glob "*.yaml" <DATA>
```

Read the `_thumb.jpg` of each candidate shortcode and compare it visually to the input. A crop or re-encode of the same photograph is easy to confirm this way — match the framing, the props, and the plating.

Only if that also finds nothing should the image be treated as having no archived post. In that case identify the recipe from the image directly, note in the final report that no shortcode was found, and skip Step 2's use of the Instagram URL.

**Duplicate posts:** the same recipe is often posted more than once by the same account, sometimes with different crops of one photograph. Ingest the post that actually matched, and mention any sibling posts for the same recipe in the final report rather than writing separate notes for them.

### Step 1: grouchygiraffe-recipe-lookup

Invoke the `grouchygiraffe-recipe-lookup` skill on the media file for the shortcode resolved in Step 0 — `<DATA>/<shortcode>.mp4`, or the `.jpg` if the post is a still.

When Step 0 recovered the shortcode from a loose image, pass the archived path, not the path the user supplied — the lookup skill derives the sibling `.yaml` and `_thumb.jpg` from it.

Collect from the output:
- The original Instagram post URL (from the `url` field in the YAML)
- The direct recipe URL (on the author's site, TikTok, or Substack)
- The author's name and Instagram handle
- The recipe name

### Step 2: social-to-imgur

Invoke the `social-to-imgur` skill using the original Instagram post URL collected in Step 1.

Collect from the output:
- The permanent Imgur URL for the thumbnail image

### Step 3: recipe-cleanup

Invoke the `recipe-cleanup` skill using the recipe URL from Step 1.

`recipe-cleanup` writes the ingredient wikilinks and then delegates to the `resolve-recipe-ingredient-link` skill to resolve any link that does not point to an existing product note — so the ingredient links in the note this workflow produces are already resolved by the time Step 3 returns. Do not resolve them separately.

After the recipe file is written, update the `pic` frontmatter field to use the Imgur URL from Step 2 instead of whatever URL was set during cleanup — the Imgur URL is permanent and not subject to CDN expiry.

### Final report (file mode)

After all three steps complete, report:
- The recipe name
- The author's name and Instagram handle
- The recipe file path written to the vault
- The Imgur thumbnail URL
- The original Instagram post URL
- The shortcode, and — when the input was a loose image — how it was resolved (exact digest match, or visual confirmation against a candidate caption search)
- Any sibling posts carrying the same recipe

## Check for an Existing Note First

Before writing the target note, check whether it already exists, and read it if so.

Many older notes are stubs holding only a hero image and caption, but their `pic` already points at a permanent Imgur URL from an earlier run.

Overwriting the stub silently destroys that URL, and re-uploading the same image spends the shared Imgur quota that is already the bottleneck.

Before the write, check for `<name>.md` and run `git log -- <path>`. If a prior version exists, recover its `pic` value and reuse it rather than running the upload, and carry forward any caption or notes the stub held.

Concurrent writers make this urgent: another process can commit an overwritten file before the mistake is noticed.
