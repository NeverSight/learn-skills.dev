---
name: mage-generate
description: |
  Generate images, video, and audio with Mage's models through the Mage
  connector (MCP): pick the right model, quote the price in Gems, generate,
  and wait for the result. Defaults: Mango 3 for images, Cherry 2 Pro for
  video, Seed Audio for audio. Use when: "generate an image", "make a
  picture", "make a video", "animate this image", "image to video", "edit
  this image", "change the background", "make music", "sound effect",
  "voiceover", "make it with Mage", or any other request to create media with
  Mage. Chain with mage-characters to keep a person consistent. NOT for:
  product photoshoots (use mage-product-photoshoot), marketplace listing
  images (mage-marketplace-cards), ad variants, resizes, or translations
  (mage-ad-multiplier, mage-ad-resizer, mage-ad-localizer), UGC product videos
  (mage-ugc-video), narrated faceless videos (mage-faceless-video), YouTube
  thumbnails (mage-youtube-thumbnail), or swaps, inpainting, relighting, lip
  sync, and edits of an existing video (the mage-* skill named for each).
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Generate

Create images, video, and audio with Mage. Every generation runs through the Mage connector's tools and is paid in Gems from the connected account.

## Before you start

1. **Mage tools.** This skill calls the connector's tools: `list_models`, `get_model`, `estimate_cost`, `generate`, `get_request`, and `create_upload` for local files. If they are not available, ask the user to connect Mage, then wait:
   - Claude: Customize → Connectors → Add custom connector, URL `https://mcp.mage.space/mcp`, then sign in to Mage.
   - Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`, then `/mcp` to sign in.
   - ChatGPT, Grok, Cursor, and others: https://www.mage.space/mcp.
2. **Balance.** `get_account` shows the Gems balance. Check it only when a price is large or a generation fails with `insufficient_gems`.

## UX rules

1. Be concise. Deliver the media link with a one-line summary: model, size or length, Gems spent. No JSON, no request ids.
2. Don't narrate tool calls ("calling estimate_cost", "polling").
3. Reply in the user's language. Field names, model ids, and prompts sent to Mage stay in English unless the user wants text in another language inside the image.
4. Don't batch-ask. Pick sensible defaults and ask one question only when the answer changes the result.
5. Always state the price in Gems. Before a video, or more than one generation, quote the total and wait for a yes. A single image can start at once with its price in the same message.
6. Results expire after 30 days. Say so once and suggest downloading anything worth keeping.

## Choose a model

Use these defaults unless the user names a model or the request needs something below.

| Media | Default | Architecture | `model_id` |
|---|---|---|---|
| Image | Mango 3 | `mango` | `mango-v3` |
| Video | Cherry 2 Pro | `cherry` | `cherry-2-pro` |
| Audio | Seed Audio | `seed_audio` | `seed-audio-1.0` |

Switch when the request calls for it:

- **Text in the image** (posters, memes, comics, infographics, UI) → GPT Image 2.5 Flare (`gpt_image_2`, `gpt-image-2.5-flare`; set the `model_id`, the family default is opt-in). Cheap at its default quality. OpenAI's safety filter applies. Mango 3 handles short text itself.
- **Photoreal people and products** (portraits, fashion, skin and fabric texture) → Guava 2 Pro (`guava`, `guava-2-pro`; set the `model_id`, the family default is the oldest Guava). Up to 3 reference images. Name the lens and the light.
- **A faster, cheaper Mango** → Mango 3 Turbo (`mango-v3-turbo`). **3K stills** → Mango 3S (`mango-v3s`), only for 3K. **4K stills** → Mango 2 (`mango-v2`).
- **A first or last frame, or cheaper video with sound** → Lemon (`lemon`, 2–30 s). Frames and reference images cannot be combined.
- **4K video** → Cherry Pro (`cherry-pro`). **Cheap video drafts** → Cherry Mini (`cherry-mini`).
- **The most natural narration or voiceover** → Eleven Speech (`eleven_speech`, `eleven-v4`), in one of 16 preset voices. **A full song, with or without vocals** → Eleven Music (`eleven_music`, `eleven-music-v2.5`).
- **Any other model** only when the user names it. `list_models` with `include_opt_in: true` lists them.

A model the user named stays in use for follow-ups on the same work. After a result, offer at most one alternative when its trade-off fits: cheaper drafts, higher resolution, a longer clip. Ids, options, and prices change; `get_model` is the source of truth. See `references/model-guide.md`.

## Workflow

1. **Pick** the model and variant as above.
2. **Read the model** with `get_model` once per model in the conversation: fields (`input_schema`), options (`options_by_model`), rules, and `max_images`.
3. **Build `config`:** `prompt`, `model_id`, and only the fields the request needs (`aspect_ratio`, `resolution`, `duration`, media inputs). Leave the rest at their defaults. Write the prompt with the model's own file (below) and `references/prompt-guide.md`.
4. **Price it** with `estimate_cost` using the same architecture and config, and quote it (UX rule 5).
5. **Generate** with a new UUID as `idempotency_key`. Reuse a key only to retry a call whose response never arrived; that returns the original request without charging again.
6. **Wait** with `get_request` and `wait_seconds: 120` until the status is `completed`, `failed`, or `cancelled`. Images take seconds to a minute, video several minutes. Keep calling quietly.
7. **Deliver** `result.url`. If `result.moderation.nsfw` is true, say the result was flagged.

For several independent generations, start all of them first, then wait on each. An account runs up to 20 at once.

## Prompt guide per model

Before the first prompt on a model in the conversation, read its file. It covers the prompt's structure, how Mage numbers images and voices for that model, dialogue and text syntax, what to avoid, and worked examples. Read Mango 3's or Cherry 2 Pro's for anything past a plain prompt: references, characters, an edit, several shots, dialogue, text in the image, or a result that missed.

| `architecture` | File |
|---|---|
| `mango` | `references/models/mango.md` |
| `cherry` | `references/models/cherry.md` |
| `lemon` | `references/models/lemon.md` |
| `guava` | `references/models/guava.md` |
| `gpt_image_2` | `references/models/gpt-image.md` |
| `seed_audio` | `references/models/seed-audio.md` |
| `eleven_speech` | `references/models/eleven-speech.md` |
| `eleven_music` | `references/models/eleven-music.md` |
| `berry` | `references/models/berry.md` |
| `blueberry` | `references/models/blueberry.md` |
| `kiwi` | `references/models/kiwi.md` |
| `raspberry` | `references/models/raspberry.md` |
| `plum` | `references/models/plum.md` |
| `melon` | `references/models/melon.md` |
| `nano_banana_v2` | `references/models/nano-banana.md` |
| `grok_image` | `references/models/grok-image.md` |
| `grok_video` | `references/models/grok-video.md` |
| `flux2` | `references/models/flux-2.md` |
| `krea_2` | `references/models/krea-2.md` |
| `moss_image` | `references/models/moss-image.md` |
| `z_image` | `references/models/z-image.md` |
| `anima` | `references/models/anima.md` |
| `ltx_video` | `references/models/ltx-video.md` |
| `minimax_h3` | `references/models/minimax-h3.md` |
| `wan_22` | `references/models/wan-video-2-2.md` |
| `hidream`, `chroma`, `stable_diffusion_v35_large`, `stable_diffusion_xl`, `sdxl_plus`, `stable_diffusion_v15` | `references/models/open-image-models.md` |

A model missing from the table has no file yet: follow `references/prompt-guide.md` and `get_model`'s rules.

## Media inputs

- **Fields.** Reference images go in `image` (the first) and `additional_images` (the rest), up to the model's `max_images`. Lemon also takes `first_image` and `last_image`. A video to edit goes in `videos` (one source video, on Cherry 2 Pro or Lemon).
- **In the prompt,** `@image1`, `@image2`, … name the request's own images in order (`image` first), on models that take references: "Put the bottle from @image1 on the table from @image2".
- **Values** are https URLs of the file itself, or data URLs up to about 3 MB. A web page (YouTube, Instagram, a Drive preview) is not a file.
- **Files attached to the chat never reach Mage.** If you can run commands and the file is on disk, call `create_upload`, PUT the file with the returned headers, and pass the returned `url`. Otherwise ask for a direct link.
- **Earlier results** are https URLs: pass a `result.url` to edit, extend, or animate it.

Details and edit patterns: `references/media-inputs.md`.

## Characters and references

Saved characters and references go in the prompt as `@handle`: "@ana walking through a night market wearing @red-coat". `list_characters` and `list_references` show the handles. To save new ones, use `mage-characters`.

## Audio

Seed Audio makes voices, dialogue, music, and sound effects at exactly the requested `duration` (5, 10, 30, 60, or 120 seconds). Quote the words to be spoken and describe the voice: age, accent, pace, emotion. For music, give the genre, tempo, instruments, and mood. It takes one image reference (a picture of a person, for a voice that fits the face) or voice clips by `@handle`, not both.

Eleven Speech speaks the prompt as written in its preset `voice`, directed by bracketed audio tags (`[whispers]`, `[laughs]`); write numbers and symbols as words. Eleven Music writes a song to `duration`; never name an artist or quote existing lyrics, which it refuses.

## Errors

| Code | What to do |
|---|---|
| `insufficient_gems` | Tell the user the price and balance; Gems are added at https://www.mage.space/api?tab=billing. |
| `invalid_config` | The message names the field, value, or `@handle`. Fix it from `get_model` and retry with a new key. |
| `content_blocked` | Mage's content policy or the model's lab refused it. Rephrase only if the request is legitimate; never try to slip past a filter. |
| `too_many_requests` | 20 generations are already running. Wait for some to finish, then submit again. |
| `generation_failed` | Usually transient and refunded. Retry once with a new key. |

More in `references/troubleshooting.md`.

## References

- `references/model-guide.md`: every recommended model, what it is for, and its fields.
- `references/prompt-guide.md`: prompts that work for images, edits, video, and audio, keeping a person on model, and UGC realism.
- `references/models/<model>.md`: one prompting guide per model (table above).
- `references/media-inputs.md`: image, frame, video, and audio inputs, with edit patterns.
- `references/troubleshooting.md`: errors, stuck requests, and bad results.
