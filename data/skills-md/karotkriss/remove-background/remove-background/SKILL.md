---
name: remove-background
description: Remove the background from an image (or a whole folder of images), producing a transparent-background PNG cutout. Runs the rembg segmentation model locally and offline via uvx - no API key, no rate limits, no anti-bot, full resolution. Use whenever the user wants to remove, erase, delete, strip, or knock out an image background; cut out a subject; make a photo/logo/product background transparent; create a PNG cutout or sticker; or asks for remove.bg-style background removal.
---

# Remove image background (local, offline)

Removes the background from images using **rembg** (a U^2-Net ONNX model) entirely on this machine.
No API key, no network calls after the one-time model download, no rate limits, and it keeps full
resolution. This is the robust local alternative to the remove.bg website/API.

The output is always a **PNG with a transparent alpha channel** (the subject kept, the background
knocked out). Confirm success by checking the output exists and is mode `RGBA` with both transparent
and opaque pixels.

## The command

Everything runs through this single, self-contained invocation - no install step, no wrapper file
needed. Substitute the input/output paths:

```bash
# Single image -> transparent PNG
uvx --python 3.11 --with "numba>=0.59.1" --from "rembg[cpu,cli]" rembg i INPUT OUTPUT.png

# Whole folder (batch) -> folder of transparent PNGs
uvx --python 3.11 --with "numba>=0.59.1" --from "rembg[cpu,cli]" rembg p INPUT_DIR OUTPUT_DIR
```

`rembg` subcommands: `i` = single file, `p` = folder, `b` = byte stream, `d` = download models,
`s` = http server.

**Example:**

Input: `~/Downloads/product.jpg` (a product on a white studio background)
Command:
```bash
uvx --python 3.11 --with "numba>=0.59.1" --from "rembg[cpu,cli]" rembg i ~/Downloads/product.jpg ~/Downloads/product-nobg.png
```
Output: `~/Downloads/product-nobg.png` - the product on transparency.

## Options: finer edges and model choice

Flags go **before** the input/output paths:

```bash
# Alpha matting: softer, more accurate edges for hair, fur, fuzzy outlines. Slower.
uvx --python 3.11 --with "numba>=0.59.1" --from "rembg[cpu,cli]" rembg i -a INPUT OUTPUT.png

# Choose a model with -m:
#   u2net             (default) general purpose, good all-rounder
#   isnet-general-use          heavier, often cleaner edges
#   u2net_human_seg            tuned for people / portraits
#   u2netp                     lightweight and faster, lower quality
uvx --python 3.11 --with "numba>=0.59.1" --from "rembg[cpu,cli]" rembg i -m isnet-general-use INPUT OUTPUT.png
```

Run `uvx --python 3.11 --with "numba>=0.59.1" --from "rembg[cpu,cli]" rembg i --help` for all flags.

## Dark subjects & solid-background logos (when rembg leaves a halo)

rembg does **salient-object detection**, not colour keying. On a **dark subject sitting on a dark or
solid-colour background** it often can't find a clean edge and leaves a **dark halo/fringe** around the
subject (and sometimes keeps interior dark holes it should have knocked out). This is worst on **JPEGs**,
where compression sprays near-black noise around the subject that rembg pulls into the cutout. rembg
handles most dark images fine - this is the specific edge case where it does not.

If the background is a **known, roughly solid colour**, don't ask a model to guess the subject - key out
the background colour directly. It's deterministic and halo-free whenever the subject colour differs from
the background.

### Fix A - solid-background subjects (dark OR light bg): colour-key the background

This needs no global install (uvx pulls Pillow on demand, matching the skill's ethos). Tune `LO`/`HI` to
your background's luminance:

```bash
# near-black background -> transparent, feathered edge; tune LO/HI to your bg
uvx --python 3.11 --with pillow python - INPUT OUTPUT.png <<'PY'
import sys
from PIL import Image, ImageFilter
LO, HI, NEUTRAL = 45, 100, 28   # near-black bg luminance window; NEUTRAL guards a colourful subject
im = Image.open(sys.argv[1]).convert("RGBA"); px = im.load(); w, h = im.size
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]; lum = 0.299*r + 0.587*g + 0.114*b; chroma = max(r,g,b) - min(r,g,b)
        if chroma < NEUTRAL:
            if lum <= LO: px[x, y] = (r, g, b, 0)
            elif lum < HI: px[x, y] = (r, g, b, int(255*(lum-LO)/(HI-LO)))
r_, g_, b_, al = im.split(); al = al.filter(ImageFilter.GaussianBlur(1.0))
Image.merge("RGBA", (r_, g_, b_, al)).save(sys.argv[2])
PY
```

- **Light background instead?** Key the **bright** end: flip the test to `lum >= HI` -> transparent and
  ramp the alpha down as luminance rises (e.g. `LO, HI = 160, 215`), so a white/pale background drops out
  and the dark subject stays.
- **`chroma < NEUTRAL` is the guardrail.** It only keys near-grey pixels, so a colourful subject (a red
  mark, a bright logo detail) is never erased even if it falls in the luminance window. Raise `NEUTRAL`
  if some subject edge is still keyed; lower it if background tint survives.
- **Scope:** this only works when the **subject colour differs from the background colour**. It is not a
  universal replacement for rembg - on a near-black *detail* sitting on a near-black background the
  luminance test can't tell them apart and will erase the detail. For those, use Fix B.

### Fix B - dark photos / complex subjects: stay with rembg

Colour-key wants a solid background; a real photo doesn't have one. Keep using rembg but:

- Try **`-m isnet-general-use`** - it often segments dark subjects more cleanly than the default u2net.
- Add **`-a`** (alpha matting) for softer, more accurate edges.

```bash
uvx --python 3.11 --with "numba>=0.59.1" --from "rembg[cpu,cli]" rembg i -m isnet-general-use -a INPUT OUTPUT.png
```

If rembg can't even **find** a very dark subject, brighten a *copy*, run rembg on the **brightened copy**
to get the mask, then paste that mask's alpha back onto the **original** so the subject keeps its true
colours:

```bash
uvx --python 3.11 --with "numba>=0.59.1" --with pillow --from "rembg[cpu,cli]" python - INPUT OUTPUT.png <<'PY'
import sys
from PIL import Image, ImageEnhance
from rembg import remove
orig = Image.open(sys.argv[1]).convert("RGB")
bright = ImageEnhance.Brightness(orig).enhance(2.2)       # brighten a COPY so rembg can see the subject
mask = remove(bright).getchannel("A")                     # rembg finds the subject on the bright copy
out = orig.convert("RGBA"); out.putalpha(mask)            # apply that alpha to the ORIGINAL -> true colours
out.save(sys.argv[2])
PY
```

## Why the invocation looks the way it does

Do not simplify it to a bare `uvx rembg` - it will fail. The reasons:

- **`--python 3.11` + `--with "numba>=0.59.1"`** is a required workaround. `rembg` depends on
  `pymatting` -> `numba`, and on Python 3.12/3.13 uvx otherwise backtracks to an ancient
  `numba 0.53` / `llvmlite 0.36` that only builds on Python <3.10 and fails here. Pinning Python 3.11
  and forcing a modern numba pulls prebuilt wheels and resolves cleanly.
- **`rembg[cpu,cli]`** adds the `onnxruntime` CPU backend and the file/folder CLI commands; plain
  `rembg` reports "onnxruntime backend not found" / "CLI dependencies not installed".
- **First run** downloads the model (~176 MB) to `~/.u2net/` and caches it; every run after is fast
  and fully offline.

## Requirements

`uv` / `uvx` on PATH is the only prerequisite - it fetches rembg and its dependencies on demand into
uv's cache. No global pip install, no API key.

## Optional: a reusable wrapper

If you expect to do this often, it is convenient (not required) to save a small wrapper that fills in
default output names and folder handling. This repo ships one at `scripts/remove-bg.sh` for anyone who
clones it; a single-file skill install does not include it, so the inline command above is the
canonical path.

## When NOT to use this

If the user specifically needs remove.bg's own cloud model output (e.g. to match it exactly on a paid
plan), that is the remove.bg HTTP API (`api.remove.bg`, needs a key) - a different path. This skill is
the local, key-free route that covers the vast majority of "remove the background" requests.
