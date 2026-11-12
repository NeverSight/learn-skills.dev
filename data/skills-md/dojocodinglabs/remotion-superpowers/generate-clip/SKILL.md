---
name: generate-clip
description: Generate AI video clips for your Remotion project. Create unique footage from text descriptions or animate still images into video — no stock footage needed.
---

# Generate Clip — AI Video Generation

You are helping the user generate custom AI video clips for their Remotion project. This creates unique footage that doesn't exist anywhere — going beyond stock footage.

## Workflow

### 1. Understand the Need

Ask the user:
- **What should the clip show?** — A scene, product, animation, nature, abstract?
- **Duration** — How long? (typically 3-10 seconds for AI clips)
- **Style** — Cinematic, drone shot, close-up, slow motion, time-lapse?
- **Source** — Text-to-video (from description) or image-to-video (animate a still)?

### 2. Craft the Video Prompt

Write a scene description, following Replicate's official `prompt-videos` skill for technique (it's model-agnostic, so it applies to Veo too). Cover the camera movement, the subject and its action, the setting, lighting and mood, and the speed.

**Good prompt examples:**
- "Slow overhead crane shot of a modern city at golden hour, cars moving on the streets below, warm cinematic lighting."
- "Close-up of coffee being poured into a white mug, steam rising, soft morning light, shallow depth of field."
- "Abstract fluid art, flowing metallic gold and deep blue paint, mesmerizing slow motion."
- "Drone flying through a forest canopy, sunlight filtering through the leaves, cinematic nature footage."

For a video, also:
- **One continuous shot per clip**; Remotion does the cutting.
- **No burned-in text or subtitles**, and negative space where titles go.
- **Keep scenes consistent:** paste the same style block into every clip's prompt and keep one model for the whole video. See `skills/remotion-production/rules/video-generation.md`.

### 3. Generate via remotion-media (default)

```
Use remotion-media generate_video_from_text:
- prompt: [crafted prompt]
- output_name: clip-city-aerial
- model: veo3_fast      # default; veo3 for finals
- aspect_ratio: 16:9    # or 9:16 for shorts
```

To animate a still instead (image-to-video):
```
Use remotion-media generate_video_from_image:
- prompt: [how the image should move]
- image_urls: [1 image URL to animate, or 2 to transition from first to last frame]
- output_name: clip-animated-still
```

- The clip is saved to `public/<output_name>.mp4` in the directory your agent was launched from, so start your agent (Claude Code, Codex, Gemini CLI…) from the Remotion project root.
- **`image_urls` must be public URLs** KIE can fetch, not files in `public/`. Reuse the KIE-hosted URL that `generate_image` returns (deleted after 14 days) or a Replicate output URL (valid 1 hour).
- KIE's Veo clips run ~8 s at 720p, 16:9 or 9:16. Plan to trim.
- **If a KIE video call fails, fall back to Replicate (step 4).** KIE's Veo depends on a preview Google is shutting down, so errors or empty results may be permanent; don't retry in a loop.

### 4. Generate via Replicate (specific models, or when KIE fails)

It needs the local `replicate-mcp` server with `REPLICATE_API_TOKEN`. Follow Replicate's official `find-models` and `run-models` skills:

1. **Search, then read the schema.** `search_models` with `body: "image to video"` (or `"text to video"`), then `get_models` (`model_owner`, `model_name`) and `list_models_examples`. Durations, resolutions and image inputs differ per model, so use only inputs that exist in the schema.
2. **Create the prediction.** Official models: `create_models_predictions`. Community models: `create_predictions` with `version: "owner/name:<version_id>"`. Don't use `Prefer: "wait"` for video.

```
# Image-to-video with Kling v3 (check the schema first)
create_models_predictions:
  model_owner: "kwaivgi"
  model_name: "kling-v3-video"
  input:
    start_image: "[public image URL]"
    prompt: "[motion description]"
    # duration, aspect ratio, mode: names and allowed values from the schema
```

3. **Poll** `get_predictions` with `prediction_id` every 10–20 s until `status` is `succeeded`, `failed` or `canceled`. Video takes minutes.
4. **Download** the URL in `output` right away (it expires after 1 hour):

```bash
mkdir -p public/footage
curl -L -o public/footage/clip-[descriptive-name].mp4 "<output URL>"
```

**Starting points, as of Oct 2026** (search and read the schema before calling):
- **Quick default**: Veo 3.1 via remotion-media
- **Image-to-video, cinematic**: Kling v3 (`kwaivgi/kling-v3-video`): `start_image`, optional `end_image`
- **References (images, video)**: Seedance 2 (`bytedance/seedance-2.0`)
- **Open-weights, cheaper**: Wan 2.7 (`wan-video/wan-2.7-t2v`, `wan-video/wan-2.7-i2v`)

Ask for a duration that covers the scene plus about 1 s of handle, then trim in Remotion. See `skills/remotion-production/rules/replicate-models.md` and `rules/video-generation.md` for the full flow, durations and provider choice.

### 5. Show Usage in Remotion

Place the clip with `<Video>` from `@remotion/media` (`npx remotion add @remotion/media`). Trimming, looping, volume and cutting several clips together follow the official `remotion-markup` skill (embedding-videos.md, video-editing.md). The path is what changes per provider: remotion-media clips are at `public/<output_name>.mp4`, Replicate downloads at `public/footage/`.

```tsx
import { Video } from "@remotion/media";
import { staticFile, useVideoConfig } from "remotion";

const { fps } = useVideoConfig();

// remotion-media clip, trimmed to 3 s and starting 5 s into the scene
<Video
  src={staticFile("clip-city-aerial.mp4")}
  from={5 * fps}
  trimBefore={1 * fps}
  durationInFrames={3 * fps}
  muted
  objectFit="cover"
  style={{ width: "100%", height: "100%" }}
/>
```

### 6. Combine with Other Assets

AI-generated clips work great when layered:
- Use as backgrounds behind text overlays
- Intercut with stock footage from Pexels
- Add voiceover and music on top
- Apply subtle zoom/pan with `interpolate()` for extra dynamism

### Tips

- **Start short** — 3-5 second clips are the sweet spot for AI video
- **Be specific about camera motion** — "slow dolly zoom", "overhead crane shot"
- **Combine clips** — Generate several short clips and sequence them in Remotion
- **Image-to-video** — Generate a still with `/generate-image` first, then animate it for more control
- **Iterate** — If the first generation isn't perfect, refine the prompt
