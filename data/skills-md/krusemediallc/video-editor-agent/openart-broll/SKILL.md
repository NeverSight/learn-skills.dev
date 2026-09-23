---
name: openart-broll
description: >
  GENERATE B-roll, talking-head clips, and screen-blend motion-graphic overlays for
  an edit through the OpenArt MCP (Seedance, Kling, Wan, Gemini Omni, Grok Imagine,
  Nano Banana and more) — identity-referenced talking heads from a reference video,
  product/scene beats, and flat-black overlay clips generated per spoken line. Use
  when an edit needs generated footage or overlays and the OpenArt MCP is connected
  ("openart", "seedance", "generate an overlay/b-roll clip", "AI clip of me saying
  X"). NOT for capturing real websites (broll-capture), Arcads-backed generation
  (arcads-broll), or hand-authored composition cards (branded-ad-edit).
---

# OpenArt B-roll & Motion Graphics (MCP)

Everything here was proven in a shipped edit: three overlay clips, a
reference-cloned talking head, and the billing/moderation scars to go with them.

## Connection — this skill's one requirement

OpenArt has **no API key**. It runs over the **OpenArt MCP connector** (tools named
`openart_*` appear in the session). Verify at the start:

- `openart_account_get` → email, plan, **credit balance**. If the tools are absent,
  have the user connect the OpenArt MCP in their client (claude.ai connectors /
  Claude Code MCP settings), then re-check.

## The call contract (every generation)

1. `openart_model_list` — pick the model whose description matches the job; modes
   matter: `text2video` (no reference), `image2video` (animate an exact first
   frame), `element2video` (subject/identity reference — pick this when unsure).
2. `openart_model_form_get(model, mode)` — exact fields (duration, aspectRatio,
   resolution, generateAudio, visualReferences…). Fill params to match.
3. `openart_model_cost({model, mode, params})` — quote the exact config. **Two
   billing quirks, both real:** `element2video` quotes EXCLUDE a video-reference
   surcharge (a 5s clip quoted 300 credits billed 670 with one 14.5s reference);
   `text2video` bills at quote. Failed/moderated runs bill 0. The credit pool is
   shared with the user's web-UI activity — re-check `openart_account_get` before
   quoting affordability.
4. **Show the user the verbatim prompt + config + credit estimate and get a yes
   BEFORE generating.** Retries and "same config" re-rolls included.
5. `openart_generate_video` → `historyId` (PENDING). Poll `openart_creation_get`
   (respect `pollAfterSeconds`; a 5s clip ≈ 5–12 min). If the host shows a
   self-polling result card, don't poll — end the turn.
6. Download the result URL, re-encode dense keyframes (`-g 30 -keyint_min 30`),
   frame-extract and LOOK before placing it.

## Recipe 1 — Motion-graphic overlays (per spoken line)

Generate short clips the editor layers over footage with a blend mode. The proven
config: `text2video`, 4–5s, resolution matching the master, `generateAudio: false`,
9:16. The prompt contract — every clause earned its place:

- **flat solid black background (#000000)** stated explicitly, plus "no background
  gradients, no vignette, no floor, no ambient glow filling the frame" — only
  BRIGHT elements (white/neon/brand color). Layered with **Screen or Add blend**,
  the black vanishes. Scope any glow "hugging the shapes only" (a blanket
  "no gradients" contradicts a requested glow and models drop one or the other).
- **One motion idea per clip**, ending settled or as a seamless pulse (loop/freeze
  room for the editor). Name the clip duration in the prompt so "holds for the
  rest of the clip" means something.
- Text ≤ 2–3 words, ALL CAPS, one string — renders cleanly even at 480p; more
  garbles. Zero-text icon clips are safest. Add "no letters, no numbers" to
  icon-only prompts or models invent labels.
- State a placement band (top 20% / bottom 25%) but EXPECT it to be ignored —
  clips come back centered. Fine: it's a keyed floater; reposition the layer.
- Append: "no watermark, no subtitles, no captions".
- Verify the rendered background is truly flat black (frame-extract) — gray wash
  reads as haze under Screen blend.

## Recipe 2 — Identity-referenced talking head / B-roll (`element2video`)

Give the model a reference video of the subject and direct new footage:

- **Getting references in:** local files upload via the `openart_upload_pick`
  widget (the user picks the file; it can take minutes to register — poll
  `openart_upload_list`). Reuse prior uploads from `openart_upload_list`;
  `openart_upload_metadata_get(url)` mints a ready `visualReferences` object —
  including from a previous GENERATION's result URL.
- **Reference caps are enforced:** video references must total **≤ 30s** — a
  30.04s clip is rejected at submit (`input_invalid`). Trim first.
- **Prompt pattern:** address references by slot — `The man in video 1 says:
  "<line>" ...` — with camera/energy directions and "No background music, no
  captions, no on-screen text." Voice and identity clone from the reference.
- **Phonetic spelling beats mispronunciation:** write acronyms as letters
  ("M C P"), dates as words ("July sixteenth"), and tricky names the way they
  sound. For non-English output, spell for THAT language's letter sounds.
- **Moderation trap (byte-plus models):** the output-audio copyright detector can
  trip on the SPOKEN LINE itself (`output_moderation_blocked` / "output audio may
  be related to copyright restrictions"). No-music guard clauses do NOT fix it —
  **reword the line**. Failed runs bill 0, so it's cheap to iterate.
- Whole-timeline b-roll beats follow the same grammar as `arcads-broll`: generate
  at the edit's aspect, slightly longer than the beat, match the grade, trim to
  the best 1.5–6s, QA hands/text/products, ~2 retries budget.

## Placement

Same as any generated media: `<video>` in a composition card (unique id,
`data-start`/`data-duration`), full-bleed takeover, or an overlay track with
Screen/Add blend in HyperFrames, CapCut, or any NLE.
