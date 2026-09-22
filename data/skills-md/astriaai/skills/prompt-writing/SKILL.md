---
name: prompt-writing
description: Use when writing, improving, or debugging image generation prompts or choosing prompt parameters.
allowed-tools: Bash(astria:*)
---

# Prompt Writing

Always write generation prompt text in English, even when the user communicates
in another language. The surrounding conversation may remain in the user's
language, but every prompt shown to the user or sent to Astria must be English.

Before writing a prompt, get to know the user with the `astria` CLI (see the
`astria-api` skill):

- `astria prompts list --limit 20` — their recent prompts, to learn their style and parameters.
- `astria packs list` — their packs. If the request is about a specific subject (e.g. a shirt), find a pack whose `main_class_name` matches and inspect its template prompts with `astria prompts list --pack-id <id>`.
- `astria tunes list` — their references/tunes. If any match what they want to generate, reference it in the prompt via `<model_type:id:1> name` syntax (see the `astria-api` skill).

Do not send the user off to browse packs or tunes themselves — query with the
CLI and bring concrete suggestions back to them. When offering choices, your
ask-user question tool (`AskUserQuestion` in Claude Code, `ask_user` in the
Astria chat agent) with image thumbnails helps them pick.

If no tune matches the request, follow intent:
- For headshots / models / avatars, do NOT ask for a reference first. Propose ready-to-generate prompt options and trait options (look, age range, styling, framing, lighting), then confirm generation settings.
- For product or person-specific identity requests where likeness matters, ask the user to provide a reference image (upload it as a tune with `astria tunes create`, or drag it into the prompt box in the web app).
- Do not suggest web search for this flow.

After writing a prompt, show the user the prompt text and let them review or
edit it before generating. Confirm how many images per prompt (via an
ask-user question) before calling `astria generate`.

# Types of request

1. **E-commerce / product shots** — reference tunes to create a new image.
2. **Image editing** — pass `astria generate --input-image <url|file>` to modify an existing image (change background, change style, add/remove objects).
3. **Upscaling** — `astria generate --model gemini --text "Recreate this image in 4K" --input-image <url>`. If the image has prominent text labels, mention them in the prompt so they survive the upscale.

# Prompt Writing Guide

By default generate with the **gemini** model (`astria generate --model gemini`).
No need to ask the user about model type unless they explicitly mention another
one or ask for a recommendation.

## Default intent mapping

If the user asks to create "models", "avatars", or "headshots", interpret this
as a request for realistic, unique face headshots on a clean white studio
background:
- Do not use any reference tune for this request type.
- Keep framing as a face headshot (not full body), white `#fff` studio backdrop, studio lighting.
- Proactively offer prompt/trait choices with an ask-user question instead of asking for references.
- Treat nationality words ("israeli", "french", "japanese") as styling/trait guidance for facial features and casting diversity, not as a request for references.
- Do NOT suggest fashion, lookbook, lifestyle, full-body, or outfit-led prompts for this request type unless the user explicitly asks for those.

See the `unique-headshot` skill for the detailed face-trait template.

## Interaction rule (strict)

Never ask a question and suggest prompt text in the same response.
- If you use the ask-user question tool, return only questions/options in that turn.
- After the user answers, return the prompt suggestion(s) in the next turn.

## References

For a reference tune always use `<model_type:tune.id:1> tune.name` to reference
the trained subject:
- `portrait of <faceid:123:1> woman in a garden wearing <faceid:124:1> dress` — CORRECT
- `portrait of John in a garden` — WRONG (the model doesn't know "John")

The trailing `:1` is a fixed part of the token syntax — it is NOT a weight or
strength. Always write `:1`; never vary it, and never tell a user to change it.

## Reviewing bad results

If the user says results are bad, figure out what went wrong:
1. Inspect each reference's `orig_images` (`astria tunes get <id>`) and check the `name` matches the image content. If `name=woman` but the image is a full-body shot including clothes or a hat, tell the user to re-crop the training images on that tune's page (`/tunes/<id>` → "training images" → crop tool).
2. The `name` must represent the main subject. "jewelry" is a poor name — it should be "ring" or "necklace" depending on the subject. If a tune named "jewelry" holds a ring, suggest renaming it (`astria tunes update <id> --name ring`) and retraining.
3. Distorted or competing faces (e.g. a LoRA and a FaceID of the same person in one prompt): turn on "Inpaint faces" in the composer settings, or remove the extra face reference (✕ on its chip). Do NOT suggest adjusting the numbers inside reference tokens — there is no reference-weight control.

## Key parameters

| Parameter | CLI flag | Common values |
|-----------|----------|---------------|
| Prompt text | `--text` | Required |
| Number of images | `--num-images` | 1–4 |
| Aspect ratio | `--aspect-ratio` | `1:1 16:9 9:16 21:9 9:21 3:2 2:3 5:4 4:5 4:3` |
| Resolution (gemini only) | `--resolution` | `1K`, `2K` (default), `4K` |

## Tips for better results

- Include background descriptions: "clean white studio", "blurred urban street", "autumn forest".
- For product shots, describe the surface and arrangement.

## Keeping the background identical across generations

Gemini / Nano Banana does not hold a backdrop exactly from one generation to
the next — the shade and brightness of a studio background drift even when a
background reference is attached. Wording cannot fix this; the reliable fix is
the post-processing flag, appended to the prompt text:

```
astria generate --text "<faceid:123:1> woman in a studio --background_color #f2f0ed"
```

`--background_color #RRGGBB` recolors the detected background to that exact hex
after generation, so a whole catalog lands on the same backdrop. It runs on
Gemini / Nano Banana, partner models and Kontext — not on Flux. In the web app
it is the "Background color" row in the composer's options cog.

Two related mistakes to check when a user reports a drifting background:

- Text like "match the provided background reference" with no background
  reference actually attached — the model then invents a backdrop every run.
  Attach it as a reference (`<faceid:ID:1> background`) or describe the exact
  colour instead.
- Five or six references stacked in one prompt (subject + outfit + shoes + hat
  + bag + background). They compete, and the background gives way first — keep
  the essentials and add accessories in a second pass.

# Fashion and garments

1. Always work with a consistent face reference. If the user has none, suggest a faceid tune from the public gallery (`astria tunes list --gallery --model-type faceid --limit 200`) or generate a face first (no reference) and convert one of those outputs into a tune with `astria tunes create`.
2. Figure out the intent — a lookbook (e.g. prompt `look book plain white background #fff`) or a campaign shot. Campaign example: `A direct flash paparazzi style shot of <faceid:3904080:1> woman moving through a crowded bar. She looks straight into the lens with an intense expression. She wears the <faceid:3907553:1> dress and the <faceid:3907242:1> bag on her shoulder. The background is dark and out of focus. High contrast, sharp flash.`
