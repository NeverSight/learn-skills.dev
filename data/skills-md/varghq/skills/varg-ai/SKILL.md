---
name: varg-ai
description: >-
  Generate AI videos, images, speech, and music using varg.
  Use when creating videos, animations, talking characters, slideshows,
  product showcases, social content, or single-asset generation.
  Supports zero-install cloud rendering (just API key + curl) and
  full local rendering (bun + ffmpeg).
  Triggers: "create a video", "generate video", "make a slideshow",
  "talking head", "product video", "generate image", "text to speech",
  "varg", "vargai", "render video", "lip sync", "captions".
license: MIT
metadata:
  author: vargHQ
  version: "2.0.0"
compatibility: >-
  Requires VARG_API_KEY (get at https://varg.ai).
  Cloud mode: curl only (zero dependencies).
  Local mode: bun runtime + ffmpeg.
---

## Environment Detection

Before generating anything, determine the rendering mode.

Run `bash scripts/setup.sh` from the skill directory to auto-detect, or check manually:

| bun | ffmpeg | Mode |
|-----|--------|------|
| No  | No     | **Cloud Render** -- read [cloud-render.md](references/cloud-render.md) |
| Yes | No     | **Cloud Render** -- read [cloud-render.md](references/cloud-render.md) |
| Yes | Yes    | **Local Render** (recommended) -- read [local-render.md](references/local-render.md) |

`VARG_API_KEY` is required for all modes. Get one at https://varg.ai

## Critical Rules

Everything you know about varg is likely outdated. Always verify against this skill and its references before writing code.

1. **Never guess model IDs** -- consult [models.md](references/models.md) for current models, pricing, and constraints.
2. **Function calls for media, JSX for composition** -- `Image({...})` creates media, `<Clip>` composes timeline. Never write `<Image prompt="..." />`.
3. **Cache is sacred** -- identical prompt + params = instant $0 cache hit. When iterating, keep unchanged prompts EXACTLY the same. Never clear cache.
4. **One image per Video** -- `Video({ prompt: { images: [img] } })` takes exactly one image. Multiple images cause errors.
5. **Duration constraints differ by model** -- kling-v3: 3-15s (integer only). kling-v2.5: ONLY 5 or 10. Check [models.md](references/models.md).
6. **Gateway namespace** -- use `providerOptions: { varg: {...} }`, never `fal`, when going through the gateway (both modes).
7. **Renders cost money** -- 1 credit = 1 cent. A typical 3-clip video costs $2-5. Use preview mode (local) or cheap models to iterate.

## Quick Start

### Cloud Render (no bun/ffmpeg needed)

```bash
# Submit TSX code to the render service
curl -s -X POST https://render.varg.ai/api/render \
  -H "Authorization: Bearer $VARG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "const img = Image({ model: fal.imageModel(\"nano-banana-pro\"), prompt: \"a cabin in mountains at sunset\", aspectRatio: \"16:9\" });\nexport default (<Render width={1920} height={1080}><Clip duration={3}>{img}</Clip></Render>);"}'

# Poll for result (repeat until "completed" or "failed")
curl -s https://render.varg.ai/api/render/jobs/JOB_ID \
  -H "Authorization: Bearer $VARG_API_KEY"
```

Full details: [cloud-render.md](references/cloud-render.md)

### Local Render (bun + ffmpeg)

```tsx
/** @jsxImportSource vargai */
import { Render, Clip, Image } from "vargai/react"
import { createVarg } from "@vargai/gateway"

const varg = createVarg({ apiKey: process.env.VARG_API_KEY! })

const img = Image({
  model: varg.imageModel("nano-banana-pro"),
  prompt: "a cabin in mountains at sunset",
  aspectRatio: "16:9"
})

export default (
  <Render width={1920} height={1080}>
    <Clip duration={3}>{img}</Clip>
  </Render>
)
```

```bash
bunx vargai render video.tsx --preview   # free preview
bunx vargai render video.tsx --verbose   # full render (costs credits)
```

Full details: [local-render.md](references/local-render.md)

### Single Asset (no video composition)

For one-off images, videos, speech, or music without building a multi-clip template:

```bash
curl -X POST https://api.varg.ai/v1/image \
  -H "Authorization: Bearer $VARG_API_KEY" \
  -d '{"model": "nano-banana-pro", "prompt": "a sunset over mountains"}'
```

Full API reference: [gateway-api.md](references/gateway-api.md)

## How to Write Video Code

Video code has two layers: **media generation** (function calls) and **composition** (JSX).

```tsx
// 1. GENERATE media via function calls
const img = Image({ model: ..., prompt: "..." })
const vid = Video({ model: ..., prompt: { text: "...", images: [img] }, duration: 5 })
const voice = Speech({ model: ..., voice: "rachel", children: "Hello!" })

// 2. COMPOSE via JSX tree
export default (
  <Render width={1080} height={1920}>
    <Music model={...} prompt="upbeat electronic" duration={10} volume={0.3} />
    <Clip duration={5}>
      {vid}
      <Title position="bottom">Welcome</Title>
    </Clip>
    <Captions src={voice} style="tiktok" />
  </Render>
)
```

### Component Summary

| Component | Type | Purpose |
|-----------|------|---------|
| `Image()` | Function call | Generate still image |
| `Video()` | Function call | Generate video (text-to-video or image-to-video) |
| `Speech()` | Function call | Text-to-speech audio |
| `<Render>` | JSX | Root container -- sets width, height, fps |
| `<Clip>` | JSX | Timeline segment -- duration, transitions |
| `<Music>` | JSX | Background audio (always set `duration`!) |
| `<Captions>` | JSX | Subtitle track from Speech |
| `<Title>` | JSX | Text overlay |
| `<Overlay>` | JSX | Positioned layer |
| `<Split>` / `<Grid>` | JSX | Layout helpers |

Full props: [components.md](references/components.md)

### Provider Differences (Cloud vs Local)

| Cloud Render | Local Render |
|---|---|
| No imports needed | `import { ... } from "vargai/react"` |
| `fal.imageModel("nano-banana-pro")` | `varg.imageModel("nano-banana-pro")` |
| `fal.videoModel("kling-v3")` | `varg.videoModel("kling-v3")` |
| `elevenlabs.speechModel("eleven_v3")` | `varg.speechModel("eleven_v3")` |
| Globals are auto-injected | Must call `createVarg()` |

## Cost & Iteration

- **1 credit = 1 cent.** nano-banana-pro = 5 credits, kling-v3 = 150 credits, speech = 20-25 credits.
- **Cache saves money.** Keep unchanged prompts character-for-character identical across iterations.
- **Preview first** (local mode only): `--preview` generates free placeholders to validate structure.
- Full pricing: [models.md](references/models.md)

## References

Load these on demand based on what you need:

| Need | Reference | When to load |
|------|-----------|-------------|
| Render via API | [cloud-render.md](references/cloud-render.md) | No bun/ffmpeg, or user wants cloud rendering |
| Render locally | [local-render.md](references/local-render.md) | bun + ffmpeg available |
| Patterns & workflows | [recipes.md](references/recipes.md) | Talking head, character consistency, slideshow, lipsync |
| Model selection | [models.md](references/models.md) | Choosing models, checking prices, duration constraints |
| Component props | [components.md](references/components.md) | Need detailed props for any component |
| Better prompts | [prompting.md](references/prompting.md) | User wants cinematic / high-quality results |
| REST API | [gateway-api.md](references/gateway-api.md) | Single-asset generation or Render API details |
| Debugging | [common-errors.md](references/common-errors.md) | Something failed or produced unexpected results |
| Full examples | [templates.md](references/templates.md) | Need complete copy-paste-ready templates |
