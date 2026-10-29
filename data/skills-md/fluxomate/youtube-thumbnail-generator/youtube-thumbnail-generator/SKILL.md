---
name: youtube-thumbnail-generator
description: >-
  Generate YouTube thumbnails with fal.ai (nano-banana) that keep the creator's
  real face consistent and reflect their saved taste. Use this whenever the user
  wants to make, design, brainstorm, or iterate on a YouTube thumbnail — including
  when they paste a video transcript or video context and ask for thumbnail ideas,
  want concepts turned into images, ask to "generate more like that one", upscale a
  chosen thumbnail, or save reference photos of themselves / liked or disliked
  thumbnails / inspiration from other creators into memory. Trigger even if they
  don't say the word "skill" — phrases like "make a thumbnail for my new video",
  "here's my transcript, give me thumbnail concepts", or "save these as inspiration"
  all apply. This skill works best when generation COPIES a specific reference thumbnail — always
  anchor to a reference (one the user pastes, or one from the saved inspiration library). Requires
  a FAL_KEY environment variable.
---

# YouTube Thumbnail Generator

A local, memory-backed thumbnail studio. It remembers what the creator looks like,
what thumbnails they like and dislike, and inspiration from other creators, then
turns a video's transcript + context into approved concepts and real images via
fal.ai. Everything is stored locally; only image generation calls out to fal.

## The core method — copy a reference thumbnail (do this by default)
This skill produces **by far its best results when each generation is anchored to a specific
reference thumbnail that it copies**, instead of designing from scratch. Treat a reference as a
required input:
- **If the user pastes/links a thumbnail to emulate**, use that as the style reference.
- **Otherwise pick one from the saved library** (`memory/inspiration/reference-thumbnails/`, broken
  down in `references/reverse-engineered-examples.md`), or ask the user which style to copy. The
  validated style menu is in `memory/winning-style.md`: **dark premium · bright income-proof (A5) ·
  hand-drawn storyboard (A1) · shocked-over-laptop (A2)**.
- **How:** pass the creator's face refs PLUS the chosen reference via `--style-ref` (uploaded last;
  the script auto-flags it as style-only). The model recreates the reference's layout / lighting /
  text styling / graphics while keeping the creator's real face and the video's hook. **This is the
  single biggest quality lever — never skip it.**

## Setup (first run, or if anything looks missing)

1. **Check the key.** Image generation needs `FAL_KEY`. If a generation fails with a
   key error, tell the user:
   - This session only (PowerShell): `$env:FAL_KEY = "your-key"`
   - Permanent: `setx FAL_KEY "your-key"` then restart the terminal.
   - Keys: https://fal.ai/dashboard/keys
2. **Scaffold memory** (idempotent, never overwrites):
   `python scripts/init_memory.py`
3. Run scripts from the skill directory so relative `memory/...` paths resolve, or
   pass absolute paths.

## The memory model (read before generating)

Memory lives in `memory/` and is the difference between generic AI images and
*the creator's* thumbnails. Before writing concepts or prompts, **read**:
- `memory/profile/style-profile.md` — niche, persona, colors, fonts, do's & don'ts
- `memory/winning-style.md` — **the validated style menu + the STYLE-REFERENCE technique (the core
  method) + calibrated rules** (real elements, no white sticker outline, $10k polish). Read this first.
- `memory/example-concepts.md` — the creator's own example concepts; layout vocabulary and the
  graphic background modes (A light / B dark) — secondary to the cinematic style above
- `references/thumbnail-principles.md` — the craft field-guide (rule of thirds, palette,
  the ~10 thumbnail types, combining 2–3 formulas, cross-niche inspiration, testing)
- `references/reverse-engineered-examples.md` — proven reference thumbnails broken into reusable
  prompts + an **element library** (float glossy app/tool icons, money/result proof + income
  charts, shock-over-laptop pose, floating result cards, blurred content-wall backgrounds)
- `memory/preferences/likes/INDEX.md` and `dislikes/INDEX.md` — what works / what to avoid
- relevant entries in `memory/inspiration/INDEX.md`
- the face photos in `memory/profile/face/` (pass these as refs at generation time)

If `style-profile.md` is still a blank template, ask the creator a few quick
questions (niche, audience, on-camera persona, signature colors/fonts) and fill it
in — this pays off on every future thumbnail.

## Core workflow

### 1. Intake a video
The user pastes a **transcript** and/or **video context** (what the video is about,
the hook, the desired vibe, the title if known). Create a project:
- slugify the title/topic → `memory/projects/<slug>/`
- write `brief.md` with: title, topic, audience, the core hook/payoff, key moments
  from the transcript, and any must-include elements the user mentioned.

### 2. Generate concepts (text first — cheap, fast, no API cost)
Using the brief + memory, write **~5 genuinely distinct concepts** following the format in
`references/prompting.md` and the craft rules in `references/thumbnail-principles.md`.
Different angles, not five versions of one idea. For each concept:
- **Pick the reference thumbnail to copy** (the user's pasted one, or one from the style menu in
  `memory/winning-style.md`) and design the concept to fit that reference's layout. Copying a proven
  reference matters more than inventing a novel look.
- Compose on the **rule of thirds** (face on one third, hook text on another).
- **Combine 2–3 of the thumbnail types** and name them (e.g. "big number + comparison + blur").
- Respect the brand **palette** (orange main; vary only the highlight) and a consistent font.
- Lean on **cross-niche** inspiration over niche clichés; keep text **≤4 words** (blank is OK).
- Note any **finishing** to do after generation (darken behind text, blur bg, warp, composite).

Save them to `memory/projects/<slug>/concepts.md`, each with an ID and a `[ ] pending`
status. Present them to the user and **wait for approval** — do not generate images yet.

### 3. Generate images for approved concepts
**Always anchor to a style reference** (see "The core method" above). For each approved concept,
write the prompt to a file and run:

```
python scripts/generate.py \
  --prompt-file "memory/projects/<slug>/concepts/<id>.txt" \
  --refs "memory/profile/face/face3.png,memory/profile/face/face1.webp" \
  --style-ref "memory/inspiration/reference-thumbnails/<chosen>.png" \
  --model nano-banana-2 --resolution 4K --num 2 \
  --out "memory/projects/<slug>/generated/<id>"
```

- `--style-ref` is the key input — the thumbnail to copy (the user's pasted one, or a library one).
  The script appends the "style-only, keep the face" instruction automatically.
- Keep face refs (`face3.png` + `face1.webp`) so the subject stays *them*.
- The prompt describes the **scene + hook + which style you're copying**; the model fuses it with
  the style ref. Use `--prompt-file` for long prompts (avoids shell-escaping quotes/`#`).
- Default **nano-banana-2 @ 4K, 2 variations**. **Each 4K image costs money** — confirm large
  batches (e.g. 5 concepts × 2 = 10). Mark the concept `[x] generated` in `concepts.md`.
- **Validate first:** generate one concept, look at it, then batch the rest.

Then show the user the saved images, **always with clickable file links** (see the
present-outputs-as-links preference).

### 4. Iterate
- **"Make it like THIS thumbnail"** → use that image as `--style-ref` (the core move). To try a
  different look, just swap the `--style-ref` to another reference and regenerate.
- **"More like v2"** → keep the same `--style-ref`, vary one axis (expression / text / color) per
  batch so variations stay distinct.
- **"More concepts"** → return to step 2 with a fresh angle, then step 3.
- **Refine** → adjust the prompt (punchier text, simpler scene, different emotion) and
  regenerate that concept's folder.
- See `references/prompting.md` for the iteration vocabulary.

### 5. Upscale the winner
When the user picks a final:
```
python scripts/upscale.py \
  --image "memory/projects/<slug>/generated/<id>/v2.jpg" \
  --factor 2 \
  --out "memory/projects/<slug>/final"
```
Low `creativity` + high `resemblance` (the defaults) keep the face and text from drifting.

## Memory management tasks

These can happen any time, independent of a video:

- **Add face photos** → user provides images; copy/save them into
  `memory/profile/face/` and add a row to its `INDEX.md` (angle, expression). More
  varied, high-res refs = better likeness.
- **Save a liked thumbnail** → save the image under `memory/preferences/likes/`, add an
  INDEX row capturing *why it works* (the reason is what makes it reusable).
- **Save a disliked thumbnail** → same under `dislikes/`, note *why to avoid*.
- **Add inspiration / a thumbnail to copy** → save the image into
  `memory/inspiration/reference-thumbnails/` (so it can be used directly as `--style-ref`), and log
  in `inspiration/INDEX.md` *what* to reuse (layout, lighting, text placement, graphics). When the
  user pastes a thumbnail "make it like this", save it here too. Optionally reverse-engineer it into
  `references/reverse-engineered-examples.md`.
- **Update style profile** → whenever a pattern emerges from likes/dislikes, fold it
  into `profile/style-profile.md` so future concepts start sharper.

When the user reacts to generated images ("love this", "hate the text"), capture that
signal: update `style-profile.md` or the likes/dislikes notes so the skill learns.

## Guardrails
- Don't generate images before concepts are approved — it wastes API budget.
- Don't invent the creator's likeness from text; use the face refs.
- Confirm before large/expensive batches.
- Keep generated text short (3–5 words) and quoted in the prompt; image models
  garble long text. If it garbles, suggest fewer words or adding text in an editor.

## Files
- `scripts/generate.py` — generate variations (nano-banana / nano-banana edit)
- `scripts/upscale.py` — upscale a chosen thumbnail (clarity-upscaler)
- `scripts/init_memory.py` — scaffold/repair the memory tree
- `scripts/lib.py` — shared fal helpers (key, upload, run, download)
- `references/prompting.md` — concept format + image prompt craft (read for steps 2–4)
- `references/thumbnail-principles.md` — design field-guide (thirds, palette, types, combining,
  cross-niche inspiration, finishing, testing)
- `references/reverse-engineered-examples.md` — proven thumbnails → prompts + element library
- `references/fal-api.md` — exact fal model params + how to add models
