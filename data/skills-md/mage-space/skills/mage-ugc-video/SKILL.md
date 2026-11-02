---
name: mage-ugc-video
description: |
  Creator-style (UGC) product videos with Mage: a presenter talking to the
  camera about the user's product in a review, unboxing, how-to, try-on,
  routine, or problem–solution format, with a scripted hook, spoken lines,
  and a call to action. Writes the script, previews the opening frame with
  Mango 3 for a few Gems, then renders a vertical video with sound on Cherry
  2 Pro (or Lemon for a cheaper cut), keeping the product exact. Use when:
  "UGC video", "UGC ad", "creator video for my product", "product review
  video", "unboxing video", "TikTok ad", "Reels ad", "talking head ad",
  "someone showing my product", "try-on video", "testimonial-style video".
  Chain with mage-characters to reuse the same creator and voice. NOT for:
  still product photos (use mage-product-photoshoot), narrated faceless
  videos (mage-faceless-video), editing an existing ad video
  (mage-ad-multiplier), or general video (mage-generate).
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage UGC Video

Make a vertical, phone-shot-looking creator video about the user's product: hook, demonstration, spoken lines, and a call to action. Approve a cheap still of the opening frame before paying for the video.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, `list_characters`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Product image:** an https link to the file, a data URL under about 3 MB, an upload from disk (`create_upload`), or a saved `object` reference by `@handle`. Files attached to the chat never reach Mage.

## UX rules

1. Ask at most two questions, as options: the format (below) and the creator (a saved `@character`, or a description: age, look, vibe). Default to a review by a friendly creator in their 20s–30s.
2. Show the script and the keyframe before the video. Video is the expensive step: quote it and wait for a yes.
3. Never claim results, awards, or reviews the product doesn't have. The creator speaks as a presenter, not as a named real customer. Remind the user once that platforms may require AI-generated ads to be labeled.
4. Deliver the video link with a one-line summary (format, length, Gems). Links expire after 30 days.

## Formats

| Format | Arc |
|---|---|
| `review` | Hook → what it is → one standout detail shown on camera → verdict → CTA |
| `unboxing` | Box in hand → opening reaction → product reveal → first impression → CTA |
| `how_to` | "Here's how I use it" → steps 1–2–3 on camera → result → CTA |
| `try_on` | Before → putting it on → turn to show fit → reaction → CTA |
| `routine` | "My morning routine" → product's moment in it → why it stays → CTA |
| `problem_solution` | Relatable problem → product as the fix → proof shown on camera → CTA |

Scripts, hooks, and timing: `references/ugc-scripts.md`.

## Workflow

1. **Script.** Write the lines for the chosen length: about 20–25 spoken words for 10 seconds, 35–40 for 15. Open with a hook in the first two seconds, keep the product on camera, end on a short CTA. Every statement about the product, including how it feels, smells, fits, or works, comes from the user's facts or their product page; ask for two or three talking points when you have none.
2. **Creator.** Use the user's `@character` (their voice comes along), or describe one. To reuse the same creator later, offer to save them with `mage-characters`.
3. **Keyframe** with Mango 3 (`mango`, `mango-v3`), `aspect_ratio: "9:16"`, product in `image`:

   ```
   Vertical phone video frame: <creator> in <setting>, holding the product from
   @image1 toward the camera at chest height, mid-sentence, natural smile.
   Keep the product's shape, colors, label, and logo exactly as in @image1.
   Shot on a smartphone front camera, natural window light, casual lived-in
   background, authentic UGC look, not a studio ad.
   ```

   Show the frame with the script and the video's price; wait for a yes. Adjust and regenerate the frame if asked (cheap).
4. **Video** with Cherry 2 Pro (`cherry`, `cherry-2-pro`), `aspect_ratio: "9:16"`, `duration: "10"` or `"15"`, `resolution: "720p"` (1080p on request; price climbs steeply). Pass the keyframe in `image` and the product photo in `additional_images`:

   ```
   Handheld vertical smartphone video, UGC style. <Creator, matching @image1>
   talks to the camera in <setting>, <actions per beat: holds up the product
   from @image2, taps the cap, turns the bottle to show the label>. They say:
   "<line 1>" "<line 2>" "<CTA>". Natural voice, casual delivery, room tone,
   no music. Keep the product identical to @image2: shape, colors, label.
   ```

   With a saved creator, write `@handle` instead of describing them; their saved voice speaks the lines.
   For a cheaper cut, use Lemon (`lemon`) with the keyframe as `first_image` (frames can't be combined with reference images there, so describe the product in words) and `audio: true`.
5. **Price and generate:** `get_model`, `estimate_cost`, quote, then `generate` (new UUID `idempotency_key`) and `get_request` with `wait_seconds: 120` until it's done. Video takes several minutes; keep waiting quietly.
6. **Check** if you can: the product matches, the lines are spoken, nothing garbled on the label. Offer one regeneration or a new take with a different hook.

## Deliver

```text
UGC review ready (15 s, 9:16, 720p, 5,198 Gems): https://…
Hook: "Okay, I didn't expect this serum to…"
```

Offer once: another hook for testing, a different creator, or a still set for the same product (`mage-product-photoshoot`).

## References

- `references/ugc-scripts.md`: hook formulas, format scripts with timing, and presenter direction.
