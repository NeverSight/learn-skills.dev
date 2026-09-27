---
name: scenario-fan-cam
description: "Use when putting a person from a photo into live-broadcast crowd footage with Scenario: a stadium or arena fan-cam reaction, a jumbotron or kiss-cam moment, a spectator cutaway at a match or concert, a courtside or front-row sighting, or a personalized sports-TV still that then animates into video. Keywords: fan cam, crowd reaction, jumbotron, stadium screen, kiss cam, broadcast cutaway, spectator, crowd shot, sports TV, courtside, arena."
license: MIT
---

# Scenario Fan Cam

## Overview

A fan cam is a two-stage build: an identity-preserving image edit places the person into a 16:9 broadcast still, and image-to-video animates the approved still into a reaction. The uploaded photo is an identity reference, never a start frame: feeding it straight to a video model animates a portrait, not a broadcast. Stage one is cheap and stage two is not, so the still carries every decision worth approving.

Use only photos of the user or of people who gave them permission; refuse celebrity or stranger insertions. Real faces also trip provider filters more than most subjects: on a block, see `scenario-moderation`. Connection and the core loop: see the `scenario` skill in this repo. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Discover members with `recommend`, passing the stage's capability and the user's own words: it ranks by measured cost and latency and names the purpose-built pick, where a capability-worded `search` returns hundreds of keyword hits with nothing to choose between them. Read `next_step` before taking a pick, per the `scenario` skill. Keep `search` for a member you can already name. Never assert a generative model's id as a constant. Scenario's own single-purpose tool models are named outright below: there is exactly one of each, so discovering them would only re-derive a constant.

| Stage             | What happens                                                                     | Detail                                             |
| ----------------- | -------------------------------------------------------------------------------- | -------------------------------------------------- |
| 1. Identity still | Image-edit member (`img2img`) composites the person into a 16:9 crowd frame      | `scenario-image`, `scenario-consistency`           |
| 2. Still gate     | Likeness checked against the photo before any video money is spent               | `scenario-asset-analysis`                          |
| 3. Animate        | Image-to-video from the approved still, reaction beats, one camera move          | `scenario-kling`, `scenario-video`                 |
| 4. Identity gate  | Frames extracted from the clip, compared to the approved still                   | `scenario-asset-analysis`                          |
| 5. Overlays       | Score strip, channel bug, lower third composited as post layers, never generated | `scenario-text-overlay`, `scenario-video-assembly` |
| 6. Derivatives    | 9:16 and 1:1 social cuts off the 16:9 master                                     | `scenario-formats`                                 |

Broadcast grammar is what sells the shot, so prompt it explicitly at both stages: long-lens compression with the crowd defocused in front and behind, harsh stadium floodlight or arena strobe, slight motion blur, the camera hunting and reframing as it finds the subject. Keep the person mid-ground among other fans, off-center, at broadcast camera height. A centered, well-lit, eye-level subject reads as a photoshoot in a stadium, not a cutaway.

Give the reaction an arc rather than a state: oblivious, then noticing the camera or the screen, then the reaction the user asked for (cheering, laughing, disbelief, heartbreak). Multi-beat prompting per the video family's contract keeps the turn inside one clip.

## Worked example: caught on the stadium screen, 8 seconds

1. Collect the photo, the sport or event, venue mood, wardrobe, and the wanted reaction. `upload_asset` the photo once and reuse the returned asset id.
2. Create this run's collection before the first generation (`collection_create`, catalog write lane, `name` only), then `collection_add_assets` each keeper as it lands; its returned `itemCount` is the receipt.
3. `recommend` with `capability="img2img"` and the placement described in words; prefer a ranked entry that takes several reference images, and read `model_schema_get` for those inputs (`scenario-image` for the lane, `scenario-consistency` for reference discipline).
4. Edit prompt: "the person from the reference image seated mid-crowd at a floodlit football stadium, 16:9 television cutaway, long-lens crowd compression, no text, logos, or graphics in frame". Keep the plate text-free: overlays come later.
5. Gate the still: `asset_display` it for approval, and inventory the likeness features that must hold (face geometry, hairline, skin tone, wardrobe) with the analysis lane from `scenario-asset-analysis`; a change in any inventoried feature fails. Unattended, that inventory stands in for the user's sign-off.
6. `recommend` with `capability="img2video"` and the reaction described in words, then check the pick against `scenario-kling` or `scenario-video`. The brief's length filters members: `duration` is usually a fixed enum a member either reaches or does not, and the tiers that reach it sit far apart on price, so `model_schema_get` each candidate and compare with `model_run` `dry_run=true`.
7. Run with the approved still as the start image and two beats: "she chats, unaware" then "she spots herself on the stadium screen, stands, and cheers", one slow reframing move, `wait=false`, then `jobs_wait` re-called with `pending_job_ids` on timeout, never a second `model_run`.
8. Check the clip against the approved still on frames the platform produced: the free `firstFrame` and `lastFrame` off `asset_get` first, then `model_scenario-video-to-image-seq` for a mid-clip frame (a tool-model lane per `scenario-video-editing`). A local extraction is not a substitute at any budget, because it yields no asset to file or audit and the gate stops being traceable. A change in any inventoried feature fails the clip, and so does legible generated type: ribbon boards and jumbotron glyphs creep in even against a no-text prompt, worst late in the clip. The retry starts from the same still, never from the drifted output.
9. Assemble on-platform with `model_scenario-compose-video` (a tool-model lane per `scenario-video-assembly`), layering the score strip and channel bug from `scenario-text-overlay` in the safe corners; a local editor is the wrong lane. Give every overlay layer an explicit `width` and `height`, since leaving them empty is documented as native size and does not hold, and pin `durationMode: "custom"` to the clip's length, since an image layer otherwise stretches the composition past it. A succeeded compose job is not proof the layers drew: pull a frame from the composite (the free `firstFrame`) and confirm every layer is present and placed before delivering. Then cut 9:16 per `scenario-formats`, a resize rather than a reframe, whose video members outpaint a wider frame instead of cutting one. Its `cover` mode crops from the center, so when the subject sits off-center put the master on a 9:16 compositor canvas positioned to hold them instead. `asset_display` both.

## Common mistakes

- Animating the uploaded photo directly: the mandatory stage is the broadcast still; skip it only when the user hands over an already approved 16:9 frame.
- Letting the image or video model render the scoreboard, channel bug, or jersey sponsor text: generated type drifts frame to frame; composite graphics in post on a text-free plate.
- Portrait staging: centered subject, flattering light, and empty seats around them break the documentary read; bury them in a reacting crowd.
- Judging likeness from one glance at the moving clip: drift hides between glances; run the frame-extract gate.
- Retrying from a drifted clip instead of the approved still: errors compound.
- Composing the master at 9:16: broadcast is 16:9; verticals are derivatives.
- A flat emotional state for the whole clip: without the notice-then-react turn, the result is a looping portrait, not a fan cam.
- Compound camera moves: one reframing drift; the crowd and the reaction supply the motion.
