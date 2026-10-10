---
name: image
version: 2.1.2
description: |
  Generate, edit, cut out, and inspect images with the best hosted image models (Nano Banana 2 / Pro, GPT Image 2, Seedream, Bria). Use for ANY image request — create from text, edit or retouch a photo, swap a logo/text, change background, upscale, product shots, portraits, try-on, 3D renders. This is THE image skill on Starchild — the former image-create / image-edit / image-3d / image-ecommerce / image-portrait / image-tryon / image-bg-remove skills are retired and folded in here.
metadata:
  starchild:
    emoji: "🎨"
    skillKey: image
user-invocable: true
disable-model-invocation: false
---

# image

One skill, four verbs. **You write the prompt; the skill validates, calls, downloads, and remembers.**

```bash
python3 - <<'EOF'
import sys; sys.path.insert(0, "skills/image")
from exports import generate, edit, remove_background, inspect, list_models
r = edit("Replace the first letter W of WALL ST with the logo in image 2, matching the sign's paint and perspective",
         ["uploads/sign.png", "uploads/logo.png"],
         keep="every other letter, the sign colour, background and lighting",
         model="nanopro", resolution="2K")
print(r["images"][0]["local_path"] if r["success"] else r["error"])
EOF
```

Always run in a bash `python3 - <<'EOF'` heredoc (not `python3 -c`). Result → `{"success", "images":[{"local_path","dims"}], "job_dir", "request_id", "cost_usd", "prompt", "params"}`; on failure `{"success": False, "error"}`. Every job gets its own directory — nothing is overwritten.

## The four verbs

| Verb | When | Key args |
|---|---|---|
| `generate(prompt, model=None, **params)` | Nothing to start from | `aspect_ratio`, `resolution` (nanopro), `image_size`+`quality` (gpt), `num_images`, `seed` |
| `edit(prompt, image_paths, keep=, mask_path=, model=, tx_id=, **params)` | Anything that starts from an existing image — retouch, background, logo/text, style, product/portrait/try-on/3D from a reference | `image_paths[0]` is the base, the rest are references; say what each one is in the prompt |
| `remove_background(image_path)` | Clean cut-out → transparent PNG | — |
| `inspect(images, question, mode=)` | You need to *see* before or after editing | `mode="inspect"` (what/where/OCR), `"compare"` (before vs after), `"qa"` (pass/fail against `goal`+`keep`) |

`list_models()` tells you each model's real capabilities. Read it when you're unsure; don't memorise.

## Picking a model — call `list_models()`, then:

- **Drafts / exploring** → `nano2` (fastest, cheapest).
- **Default, multi-reference, instruction-heavy edits** → `nanopro`. Output is 1K unless you pass `resolution="2K"|"4K"` — **always set it when the source is large**, or you'll shrink the user's image.
- **Region-locked edit** (change *only* this area, pixels elsewhere must not move) → `gpt` with `mask_path` (white = editable). It's the only model with a real mask. Slow (~2 min) — say so.
- **Many references / asset composition** → `seedream` (candidate: name it explicitly).
- **"Best quality" requests** → tell the user what you picked and why; run 2 candidates if the budget allows rather than guessing.

Unknown model, unsupported parameter, too many references, mask on a model without mask → the call **refuses before spending**. Read the error; it lists what *is* supported. Never work around it by dropping a parameter silently — that's how outputs come back the wrong size.

## Principles that prevent the known failures

1. **Restate the goal before you write the prompt.** Two sentences to yourself: *change* = … , *keep* = … . Put the *keep* into `keep=`. "Replace the first W, keep ALL ST" must never become "only the letter W" in the prompt.
2. **Name every reference's role.** "Image 1 is the base. Image 2 is the logo to place. Image 3 is the colour reference." Models can't infer roles from file order.
3. **Precise text, logos, exact type** → AI models are unreliable at this. Prefer: clear the region with `edit` (or mask), then composite the real vector/text deterministically (PIL), then optionally one `edit` pass "blend the pasted element's lighting and grain". Don't ask a diffusion model to draw a brand mark from memory.
4. **Look before you loop.** If you don't know where something is or what text says, `inspect(..., mode="inspect")` with a concrete question. Don't crop-and-ask five times; one good question with coordinates request suffices. Treat returned boxes as approximate.
5. **QA against the stage, not the final product.** An intermediate "W removed, logo still to be added" image must pass `mode="qa"` with *that* goal. Pass `goal=` and `keep=` explicitly.
6. **One automatic retry, then ask.** For multi-step edits open a transaction (`start_transaction(goal, base_path, keep=, logo=..., end_frame=...)`), pass `tx_id=` to each `edit`, mark `auto_fix=True` on your own retries. The budget is one; after that show candidates with a one-line diff each and let the user choose (`approve(tx_id, rev)`). Rejected outputs never become the next base.
7. **Deterministic ops stay deterministic.** Colour grading, blur, crop, resize, shadow, perspective — PIL/OpenCV, not a paid regeneration. Real upscaling = target pixel size with `resolution`/`image_size`, not the word "upscale" in a prompt.
8. **Video frames**: a start/end frame pair must be two *approved* revisions. If the video model takes one image, say so instead of hoping.

## Domain know-how

Product shots for Amazon/Xiaohongshu, ID photos, try-on wording, 3D render levers, the 20 old edit actions and where they went — `references/domain-guides.md` (read once when the request is in one of those domains).

## Recovery & cost

- Timeout or dropped connection → `recover(job_id)` re-fetches the paid result; don't resubmit.
- Costs land on the user's turn automatically; `cost_usd` in every result. Mention it when >$0.10 or when running multiple candidates.
- Local testing without the gateway: set `FAL_KEY`.

## Boundaries

Real people / faces: fine for the user's own photos; refuse impersonation or sexual content. Brands: use assets the user provides. When in doubt about a person's identity or consent, ask first.
