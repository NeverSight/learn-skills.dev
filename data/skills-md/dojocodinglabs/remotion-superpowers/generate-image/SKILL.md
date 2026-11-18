---
name: generate-image
description: Generate AI images for your Remotion project. Describe what you need — backgrounds, thumbnails, characters, abstract art — and get production-ready images via AI generation or Replicate models.
---

# Generate Image — AI Image Creation

You are helping the user generate custom images for their Remotion video project.

## Workflow

### 1. Understand the Need

Ask the user (if not already clear):
- **What is the image for?** — Scene background, thumbnail, character, product shot, abstract art, diagram?
- **Style** — Photorealistic, illustration, 3D render, flat design, watercolor, pixel art?
- **Dimensions** — Landscape (1920x1080), portrait (1080x1920), square (1080x1080)?
- **Mood/Colors** — Bright, dark, warm, cool, neon, pastel?

### 2. Craft the Prompt

Write the prompt in full sentences, following Replicate's official `prompt-images` skill for technique (it's model-agnostic, so it applies to KIE too). Cover, in order: subject, style, lighting, camera angle, color palette, background details.

**Good prompt examples:**
- "A modern tech startup office seen from above, clean minimalist design with white desks and blue accents, bright natural light from large windows, photorealistic."
- "An abstract geometric pattern of glowing neon purple and blue lines on a dark background, futuristic 3D render."
- "A friendly robot mascot waving, cartoon illustration with pastel colors on a clean white background, suitable for a logo."
- "A downtown skyline silhouetted against a warm orange and pink golden-hour sky, drone aerial shot, cinematic."

For a video, also:
- **Leave negative space** where Remotion will place titles or captions, and ask for "no text, no watermark"; Remotion renders the text.
- **Keep scenes consistent:** reuse one style block verbatim across every image in the video, and pass the first good image as a reference. See `skills/remotion-production/rules/image-generation.md`.

### 3. Generate via remotion-media (default)

```
Use remotion-media generate_image:
- prompt: [crafted prompt]
- output_name: img-hero
- aspect_ratio: 16:9  # always pass it (default is 1:1); 9:16 for shorts
- resolution: 2K      # default 1K; use 2K+ for 1080p compositions
- image_urls: [optional reference images, up to 8, public URLs only]
```

The image is saved to `public/img-hero.png` in the directory your agent was launched from, so start your agent (Claude Code, Codex, Gemini CLI…) from the Remotion project root. Reference images in `image_urls` must be public URLs KIE can fetch, not files in `public/`.

### 4. Generate via Replicate (specific models)

Use Replicate when the user wants a specific model (typography, several references, a particular look) or KIE fails. It needs the local `replicate-mcp` server with `REPLICATE_API_TOKEN`. Follow Replicate's official `find-models` and `run-models` skills:

1. **Search, then read the schema.** `search_models` with `body: "<task>"`, then `get_models` (`model_owner`, `model_name`) and `list_models_examples`. Use only inputs that exist in the schema; the aspect-ratio input name varies per model.
2. **Create the prediction.** Official models: `create_models_predictions` with `model_owner`, `model_name` and `input`. Community models: `create_predictions` with `version: "owner/name:<version_id>"`. Fast image models can take `Prefer: "wait"` (blocks up to 60 s).
3. **Poll** `get_predictions` with `prediction_id` until `status` is `succeeded`, `failed` or `canceled`.
4. **Download** the URL in `output` right away (it expires after 1 hour):

```bash
mkdir -p public/images
curl -L -o public/images/img-[descriptive-name].png "<output URL>"
```

Starting points, as of Oct 2026 (search and read the schema before calling):
- **FLUX.2 Pro / Max** (`black-forest-labs/flux-2-pro`, `-max`): photoreal, several reference images via `input_images`
- **Nano Banana Pro** (`google/nano-banana-pro`): image with text, editing
- **GPT Image 2** (`openai/gpt-image-2`)
- **Ideogram v3 Quality / Turbo** (owner `ideogram-ai`, one ID per tier; search `ideogram`): typography, logos
- **FLUX Kontext Pro** (`black-forest-labs/flux-kontext-pro`): edit from a single reference (`input_image`)

See `skills/remotion-production/rules/replicate-models.md` for the full flow and `rules/image-generation.md` for provider choice and consistency guidance.

### 5. Show Usage in Remotion

Add the image with `<CanvasImage>` from `remotion`, as the official `remotion-markup` skill does (`<Img>` still works; both accept `effects`). Sizing and animation follow its images.md and timing.md. The path depends on the provider: `generate_image` saves to `public/<output_name>.png`, Replicate downloads to `public/images/`.

```tsx
import { CanvasImage, Easing, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

// As a background (remotion-media output)
<CanvasImage
  src={staticFile("img-hero.png")}
  style={{ width: "100%", height: "100%", objectFit: "cover" }}
/>

// As an element that pops in (Replicate download)
<CanvasImage
  src={staticFile("images/img-product.png")}
  style={{
    scale: interpolate(frame, [0, 0.6 * fps], [0, 1], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp",
      easing: Easing.spring({ damping: 200 }),
      output: "perceptual-scale",
    }),
  }}
/>
```

For a slow Ken Burns move on a still, see `skills/remotion-production/rules/image-generation.md`.

### 6. Iterate

If the image isn't right:
- Adjust the prompt — be more specific about what's wrong (see `prompt-images` for editing and common pitfalls)
- Generate multiple variations and let the user pick
- Use exclusions only if the model supports them ("no text, no watermark"); some models get worse with negative prompts
- Change one thing at a time so the image still matches the other scenes
