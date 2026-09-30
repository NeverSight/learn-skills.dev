---
name: nano-banana
description: Google Gemini image generation (Nano Banana) via the Gemini API. Use when user mentions "Nano Banana", "Gemini image generation", "gemini-3-pro-image", "gemini-3.1-flash-image", or wants to generate/edit images with Google's native image model.
---

# Nano Banana (Gemini Image Generation)

Generate and edit images using Google's Gemini native image models. Supports text-to-image, image editing, and multi-image composition via the standard `generateContent` endpoint.

> Official docs: `https://ai.google.dev/gemini-api/docs/generate-content/image-generation`

---

## When to Use

Use this skill when you need to:

- Generate images from text prompts
- Edit an existing image with a text instruction (inpaint / restyle / add-remove)
- Compose multiple input images into one output (e.g. put a product into a scene)
- Iterate on an image conversationally with fine-grained control

---

## Prerequisites

Connect the **Nano Banana** connector at [app.okou.ai/connectors](https://app.okou.ai/connectors). Enabling the connector provisions `NANO_BANANA_TOKEN` — no Google Cloud account or user-supplied key is required.

> **Troubleshooting:** If requests fail, run `okou doctor check-connector --env-name NANO_BANANA_TOKEN` or `okou doctor check-connector --url https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent --method POST`

---

## How to Use

All calls hit `POST https://generativelanguage.googleapis.com/v1beta/models/<model>:generateContent` with header `x-goog-api-key: $NANO_BANANA_TOKEN`. The output image comes back Base64-encoded in `candidates[0].content.parts[*].inline_data.data` — see section 3 for picking the right part.

### 1. Text-to-Image (Flash — fast, versatile default)

Write to `/tmp/nano_banana_request.json`:

```json
{
  "contents": [
    {
      "parts": [
        { "text": "A golden retriever puppy wearing a tiny chef hat, studio lighting, photorealistic" }
      ]
    }
  ]
}
```

```bash
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent" --header "x-goog-api-key: $NANO_BANANA_TOKEN" --header "Content-Type: application/json" -d @/tmp/nano_banana_request.json > /tmp/nano_banana_response.json
```

### 2. Text-to-Image (Pro — highest quality)

```bash
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent" --header "x-goog-api-key: $NANO_BANANA_TOKEN" --header "Content-Type: application/json" -d @/tmp/nano_banana_request.json > /tmp/nano_banana_response.json
```

### 3. Extract and Save the Image

Gemini 3 image models think before they answer, and the thinking is returned inline: up to two interim images come back as parts marked `"thought": true`, followed by the final render. **Take the last image part that is not a thought** — selecting every image part concatenates the interim frames into a corrupt file.

```bash
jq -r '[ .candidates[0].content.parts[]
         | select((.thought // false) | not)
         | (.inlineData // .inline_data)
         | select(. != null) ]
       | last | .data // empty' /tmp/nano_banana_response.json | base64 -d > /tmp/nano_banana_output.png
```

If generation was refused or safety-blocked there is no image part at all, and the command above writes an empty file. Check the size before using the output, and read `candidates[0].finishReason` and the text parts to find out why.

### 4. Edit an Existing Image (Image-to-Image)

Pass the input image as a second part. Use a local file or URL → Base64:

```bash
base64 -w0 /path/to/input.jpg > /tmp/nano_banana_input_b64.txt
```

Write to `/tmp/nano_banana_request.json`:

```json
{
  "contents": [
    {
      "parts": [
        { "text": "Replace the background with a snowy mountain range at sunset. Keep the subject unchanged." },
        {
          "inline_data": {
            "mime_type": "image/jpeg",
            "data": "<PASTE_CONTENTS_OF_/tmp/nano_banana_input_b64.txt>"
          }
        }
      ]
    }
  ]
}
```

Or build the JSON with `jq` to avoid pasting:

```bash
jq -n --rawfile img /tmp/nano_banana_input_b64.txt '{
  contents: [{
    parts: [
      { text: "Replace the background with a snowy mountain range at sunset. Keep the subject unchanged." },
      { inline_data: { mime_type: "image/jpeg", data: $img } }
    ]
  }]
}' > /tmp/nano_banana_request.json
```

```bash
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent" --header "x-goog-api-key: $NANO_BANANA_TOKEN" --header "Content-Type: application/json" -d @/tmp/nano_banana_request.json > /tmp/nano_banana_response.json
```

### 5. Multi-Image Composition

Combine multiple input images into one output — e.g. put a product (image A) into a scene (image B):

```bash
jq -n \
  --rawfile a /tmp/product_b64.txt \
  --rawfile b /tmp/scene_b64.txt \
  '{
    contents: [{
      parts: [
        { text: "Place the product from the first image onto the wooden table in the second image. Match the lighting and shadows." },
        { inline_data: { mime_type: "image/png", data: $a } },
        { inline_data: { mime_type: "image/jpeg", data: $b } }
      ]
    }]
  }' > /tmp/nano_banana_request.json

curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent" --header "x-goog-api-key: $NANO_BANANA_TOKEN" --header "Content-Type: application/json" -d @/tmp/nano_banana_request.json > /tmp/nano_banana_response.json
```

Gemini 3 models mix up to 14 reference images, but the per-model budget differs by role:

| Reference role | `gemini-3.1-flash-lite-image` | `gemini-3.1-flash-image` | `gemini-3-pro-image` |
|---|---|---|---|
| Objects (high fidelity) | 14 | 10 | 6 |
| Characters (consistency) | — | 4 | 5 |
| Style references | — | — | 3 |

### 6. Control Output Modalities and Aspect Ratio

Gemini can return text alongside images. To request image-only output and a specific aspect ratio, add `generationConfig`:

```json
{
  "contents": [
    { "parts": [{ "text": "A minimalist poster for a jazz festival" }] }
  ],
  "generationConfig": {
    "responseModalities": ["IMAGE"],
    "imageConfig": {
      "aspectRatio": "16:9",
      "imageSize": "2K"
    }
  }
}
```

```bash
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent" --header "x-goog-api-key: $NANO_BANANA_TOKEN" --header "Content-Type: application/json" -d @/tmp/nano_banana_request.json > /tmp/nano_banana_response.json
```

### 7. Conversational Editing (Multi-Turn Refinement)

Continue refining by appending the previous model turn and a new user message. Reuse the Base64 image the model returned so you don't re-upload — feed back the **final** image, not an interim thought frame:

```bash
PREV_IMG=$(jq -r '[ .candidates[0].content.parts[]
                    | select((.thought // false) | not)
                    | (.inlineData // .inline_data)
                    | select(. != null) ]
                  | last | .data // empty' /tmp/nano_banana_response.json)

jq -n --arg img "$PREV_IMG" '{
  contents: [
    { role: "user",  parts: [{ text: "A minimalist poster for a jazz festival" }] },
    { role: "model", parts: [{ inline_data: { mime_type: "image/png", data: $img } }] },
    { role: "user",  parts: [{ text: "Make the typography bolder and shift the palette to deep blue and gold." }] }
  ]
}' > /tmp/nano_banana_request.json

curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent" --header "x-goog-api-key: $NANO_BANANA_TOKEN" --header "Content-Type: application/json" -d @/tmp/nano_banana_request.json > /tmp/nano_banana_response.json
```

`gemini-3.1-flash-lite-image` is not optimized for multi-turn sequential editing or multiple reference inputs — use Flash or Pro for sections 5 and 7.

### 8. Inspect Any Text the Model Returns

The model may include a short text caption/explanation alongside the image. Skip `thought` parts to get the caption rather than the model's reasoning:

```bash
jq -r '.candidates[0].content.parts[] | select((.thought // false) | not) | select(.text != null) | .text' /tmp/nano_banana_response.json
```

To read the reasoning that led to the image, select the thought parts instead:

```bash
jq -r '.candidates[0].content.parts[] | select(.thought == true) | select(.text != null) | .text' /tmp/nano_banana_response.json
```

---

## Model Reference

| Model | Name | Tier | Image sizes | Output price per image |
|---|---|---|---|---|
| `gemini-3.1-flash-image` | Nano Banana 2 | Default — versatile workhorse, strong text rendering | `512` / `1K` / `2K` / `4K` | $0.045 / $0.067 / $0.101 / $0.151 |
| `gemini-3-pro-image` | Nano Banana Pro | Highest quality, best world knowledge and brand consistency | `1K` / `2K` / `4K` | $0.134 / $0.134 / $0.24 |
| `gemini-3.1-flash-lite-image` | Nano Banana 2 Lite | Cheapest, lowest latency, high volume | `512` / `1K` | $0.0336 at `1K` |

Prices are the standard paid tier at the time of writing; check `https://ai.google.dev/gemini-api/docs/pricing` before relying on them for budgeting.

## Aspect Ratios

`gemini-3.1-flash-image` and `gemini-3.1-flash-lite-image` support all 14 ratios:

`1:1`, `1:4`, `1:8`, `2:3`, `3:2`, `3:4`, `4:1`, `4:3`, `4:5`, `5:4`, `8:1`, `9:16`, `16:9`, `21:9`.

`gemini-3-pro-image` supports 10 — the four extreme panoramic ratios `1:4`, `4:1`, `1:8` and `8:1` are **not** available:

`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`.

If no ratio is specified the model picks one based on any reference images provided, falling back to `1:1`.

## Image Size

`generationConfig.imageConfig.imageSize` — `"512"`, `"1K"` (default), `"2K"`, `"4K"`. Larger sizes cost more and are only relevant to final renders; keep iteration at `1K`. `gemini-3-pro-image` does not offer `512`, and `gemini-3.1-flash-lite-image` stops at `1K`.

## Response Shape

```json
{
  "candidates": [{
    "content": {
      "parts": [
        { "thought": true, "text": "Considering the composition..." },
        { "thought": true, "inline_data": { "mime_type": "image/png", "data": "<interim base64>" } },
        { "text": "Optional caption..." },
        { "inline_data": { "mime_type": "image/png", "data": "<final base64>" } }
      ]
    },
    "finishReason": "STOP"
  }]
}
```

## Guidelines

1. **Endpoint is per-model** — the URL ends with `<model>:generateContent`. Don't try `/v1beta/models:generateContent` with a `model` field in the body; the firewall only allows the per-model endpoints.
2. **Use JSON files for request bodies** — write to `/tmp/nano_banana_*.json` to avoid shell quoting issues with long prompts and Base64 payloads.
3. **Always `base64 -w0`** when preparing Linux image input — `base64` without `-w0` inserts newlines that break JSON escaping.
4. **Output is Base64, never a URL** — decode the image part's `data` and write bytes directly to disk. The `mime_type` tells you the extension (`png` / `jpeg` / `webp`).
5. **Take the last non-thought image** — Gemini 3 image models always think and return up to two interim images first. Thinking cannot be disabled. Grabbing the first image part gives you a draft; grabbing all of them gives you a corrupt file.
6. **Prefer Flash** for iteration, switch to Pro for finals — Flash turns around in a few seconds; Pro is noticeably slower and roughly 2x the cost, but sharper on text, hands, and fine detail.
7. **Keep prompts concrete** — describe subject, style, lighting, composition, and mood. For edits, say what to change and what to keep.
8. **Input image size** — downscale very large inputs before Base64-encoding; the full round-trip cost scales with payload size.
