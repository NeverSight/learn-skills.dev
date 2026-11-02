---
name: mage-recreate
description: |
  Turn a reference image into a detailed generation prompt with Mage, then
  make new images in that look: composition, subject, style, light, camera,
  materials, color, and mood are described, and the prompt is handed to the
  image model. The Recreate app as a skill. Use when: "recreate this image",
  "what prompt would make this", "reverse-engineer this picture", "write a
  prompt from this image", "make something in this style", "I want this look",
  "variations on this reference", "copy this vibe with my own subject".
  NOT for: editing the image itself (mage-refine, mage-inpaint), putting a
  specific person or product into it (mage-character-swap,
  mage-product-photoshoot), ads (mage-ad-multiplier), or copying a real
  person's likeness or a brand's protected artwork.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Recreate

Start from a look instead of a description: read a reference image into a prompt, then generate from the prompt. This is the [Recreate app](https://www.mage.space/apps/recreate) as a skill. The app gives back a prompt to take to a model; this skill does the same, then offers to run it.

## Before you start

1. **Mage tools:** `search_creations`, `get_model`, `estimate_cost`, `generate`, and `get_request`. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **You must be able to see the reference.** The prompt comes from looking at the image: an attachment in the chat, a link you can open, or a file on disk. If you can't view images, say so and stop; don't guess from a filename or a caption.
3. **Rights.** Recreate a look, not a person or a protected work. Don't name real people, living artists, brands, or characters in the prompt.

## UX rules

1. Don't ask for what the request already gives. Ask for a missing reference in one question, then wait.
2. The prompt is the product of this skill: write it as the app's instruction says and show it in full.
3. Offer to generate with the model and the price in Gems in the same message. One image can start when the user asked for an image; a batch waits for a yes.
4. Deliver results as links with a one-line label (model, size, Gems spent). No ids or JSON. Reply in the user's language. Links last 30 days.

## Inputs

1. **The reference image.** The user's own, or one of their saved creations: `search_creations` finds them by meaning ("a red car at night"). The app also has a gallery to browse by category; the connector doesn't expose it, so the reference has to come from the user.
2. **Optional changes:** a different subject, setting, or ratio ("same look, but a lighthouse").

## Write the prompt

Look at the image and follow the app's instruction exactly:

```
Describe this image as a detailed image-generation prompt for recreating it. Focus on composition, subject, style, lighting, camera angle, framing, materials, textures, colors, mood, and any important visual details. Return only the prompt text. Do not include markdown, labels, bullet points, or commentary.
```

So the prompt is one block of plain prose, with no headings, bullets, or notes, covering each of those aspects in turn: usually 100 to 300 words. Describe only what is visible, and leave out text you can't read. If the user asked for a change, write the prompt for the reference first, then swap only the part they named and keep the rest of the look.

## Deliver the prompt

Give the prompt in a code block, with one line saying it is ready to generate from. This is where the app stops.

## Generate (optional)

Offer to run it, with the price from `estimate_cost`, and do so when the user asked for an image rather than a prompt:

- Model: Mango 3 (`mango`, `model_id: "mango-v3"`) at `2K`, Mage's default for stills, unless the user names another model. The same prompt gives different results on different models.
- `aspect_ratio`: the option closest to the reference's shape, unless the user asked for another.
- **Don't pass the reference image.** Recreate works from the prompt alone, so the result is a new image in the same look, not an edit.

```json
{
  "model_id": "mango-v3",
  "resolution": "2K",
  "aspect_ratio": "<closest to the reference>",
  "prompt": "<the prompt>"
}
```

1. `get_model` for the architecture, once per conversation, to confirm its fields and options.
2. `estimate_cost` with the exact config. Say the model and the price in Gems. One image can start in the same message; more than one waits for a yes.
3. `generate` with a new UUID as `idempotency_key`, then `get_request` with `wait_seconds: 120` until the status is `completed`, `failed`, or `cancelled`.

For variations, change one element of the prompt per generation, quote the total, and wait for a yes. To stay closer to the reference than a prompt can, use the reference as an input with `mage-generate` instead.

## Errors

| Code | What to do |
|---|---|
| `insufficient_gems` | Give the price and the balance; Gems are added at https://www.mage.space/api?tab=billing. |
| `invalid_config` | The message names the field, value, or `@handle`. Fix it from `get_model` and retry with a new key. |
| `content_blocked` | Mage's policy or the model's filter refused it. Never try to slip past a filter. |
| `too_many_requests` | 20 generations are already running. Wait, then submit again. |
| `generation_failed` | Usually transient and refunded. Retry once with a new key. |
