---
name: imagegen
description: Generate images via BlockRun's image API. Trigger when the user asks to generate, create, draw, or make an image.
metadata: { "openclaw": { "emoji": "🖼️", "requires": { "config": ["models.providers.blockrun"] } } }
---

# Image Generation

When the user asks to generate, create, draw, or make an image, generate it by calling ClawRouter's image API directly — no extra setup needed.

## How to Generate

POST to `http://localhost:8402/v1/images/generations`:

```json
{
  "model": "google/nano-banana",
  "prompt": "<user's prompt>",
  "size": "1024x1024",
  "n": 1
}
```

The response contains a public image URL:

```json
{
  "created": 1741460000,
  "data": [{ "url": "https://files.catbox.moe/abc123.png" }]
}
```

Display the image inline in your response:

```markdown
![generated image](https://files.catbox.moe/abc123.png)
```

## Model Selection

Pick the model based on what the user asks for (or default to `nano-banana`):

| Model shorthand | Full ID                     | Price | Best for                            |
| --------------- | --------------------------- | ----- | ----------------------------------- |
| `nano-banana`   | `google/nano-banana`        | $0.05 | Default — fast, cheap, good quality |
| `banana-pro`    | `google/nano-banana-pro`    | $0.10 | High-res up to 4096×4096            |
| `dall-e-3`      | `openai/dall-e-3`           | $0.04 | Photorealistic, complex scenes      |
| `gpt-image`     | `openai/gpt-image-1`        | $0.02 | Budget option                       |
| `flux`          | `black-forest/flux-1.1-pro` | $0.04 | Artistic styles, fewer restrictions |

If the user mentions "high res" or "large", use `banana-pro`. If they want "photorealistic" or "dall-e", use `dall-e-3`. Otherwise default to `nano-banana`.

## Size Options

Default is `1024x1024`. Adjust based on user request:

- Portrait: `1024x1792`
- Landscape: `1792x1024` (dall-e-3) or `1216x832` (nano-banana / flux)
- High-res: up to `4096x4096` with `banana-pro` only

## Example Interactions

**User:** Draw me a golden retriever surfing on a wave

→ Call `nano-banana` with prompt `"a golden retriever surfing on a wave"`, display the image.

**User:** Generate a high-res mountain landscape, landscape format

→ Call `banana-pro` with size `1024x1024` (max varies by model), prompt `"mountain landscape"`.

**User:** Make a cyberpunk city with dall-e

→ Call `dall-e-3` with prompt `"a futuristic cyberpunk city"`.

## Notes

- Payment is automatic via x402 — deducted from the user's BlockRun wallet
- If the call fails with a payment error, tell the user to fund their wallet at [blockrun.ai](https://blockrun.ai)
- DALL-E 3 applies OpenAI content policy; use `flux` or `nano-banana` for more flexibility
- Google models may return base64 — ClawRouter handles uploading automatically, you'll get a URL back
