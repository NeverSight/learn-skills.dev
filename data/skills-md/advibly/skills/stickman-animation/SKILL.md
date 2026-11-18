---
name: stickman-animation
description: >
  Direct a finished stick-figure animation ad or explainer on the Advibly MCP. Asks for the
  theme (white canvas with black figures, or black canvas with white figures) and the aspect
  ratio, writes a director's proposal (narration, ~10 second clips with three timed visual beats
  each, visual metaphors, camera moves, matched clip-to-clip transitions, SFX), stops for
  approval, then renders one flat line-art opening still per clip, animates each clip with Gemini
  Omni Flash 1.1 landing on the next clip's still, and composes per-clip voiceover, music, text
  overlays and an optional on-twos snap with advibly_render_composition. Trigger for "stickman
  ad", "stick figure ad", "stick-figure animation", "stickman explainer", "stick figure video",
  "kinetic line animation", "doodle animation ad", "minimalist line animation", "animate a stick
  figure", or a reference clip with the black-or-white stick-figure motion-graphics look. Use even
  without the word "skill" when that visual treatment is clearly requested.
---

# Advibly Stickman Animation

Turn a brand, a product angle, or a piece of copy into a **visually dense stick-figure video**:
faceless line-art figures, a flat monochrome canvas, up to three saturated accent colors, and a
visual change every two to three seconds. A stick figure is simple; the video must not be. A
static figure in an empty frame for ten seconds is the failure this skill exists to prevent.

The skill locks the STYLE and invents the STORY. The look (theme polarity, the figure, the
palette discipline, the no-text rule) is fixed. The concept, metaphors, settings, camera, and arc
are designed fresh for every brief.

Speak in the user's language. No em dashes anywhere in output; use periods or line breaks. The
narration is English unless the user asks otherwise; when the user writes in another language,
plan in their language and give a reference translation of the narration.

## The core idea (read this first)

1. **A clip is three beats, not one pose.** Every ~10 second clip is built as `[0-3s]` establish
   or inherit, `[3-7s]` transform or escalate, `[7-10s]` climax and hand off. Each clip uses at
   least four relevant visual devices (a metaphor made literal, an environment transformation, a
   camera move, particles or energy, a foreground wipe, a match cut, an oversized object). Density
   comes from meaning, never from unrelated spectacle.
2. **Clips connect through named interfaces.** Every clip ends on a visible state the next clip
   inherits: a shape that fills the frame, a moving object, a pose, a travel direction. The
   opening still of clip N+1 IS the landing frame of clip N, so `gemini-omni-flash-1.1` animates
   each clip from its own still and lands on the next one. The seams execute in-camera.
3. **The look is born in the still, the motion in the clip.** gpt-image-2 draws each clip's
   opening state as flat line art. The video model moves it. The two chronic failures are the
   video model adding shading or 3D volume, and redesigning the start frame; the prompts guard
   both every time.
4. **No words in any generation.** No captions, letters, numbers, or interface copy in any still
   or clip. Speech bubbles, cards, clocks, meters and notifications are icon-only. Any on-screen
   phrase is a `texts` overlay in the final composition, which renders crisp type the video model
   would garble. The one exception is a product prop's own logo, copied from its photo.
5. **Plain color names, never codes.** Prompts say "vivid red" or "electric blue", never hex, RGB,
   or Pantone. Models render prominent codes as visible text. Translate the brand's hex into an
   ordinary color name once in Phase 1 and use only that name afterwards.
6. **Narration is external.** Clips are SFX-only. One `advibly_generate_voiceover` segment per
   clip, same voice, placed at the clip's offset. A narrator baked into each clip changes voice
   every clip.

## Hard defaults (do not drift)

- **Theme and ratio are asked, never silently picked.** Ask both in the kickoff. If the user says
  "you choose", use light theme and 9:16 and say so. Urgency or cost pressure does not waive the
  ask.
- **Figure:** hollow circular head with no face, no hair, no clothing, no filled body, single-line
  torso and limbs, stable proportions, uniform medium line weight. Emotion lives in pose and
  timing. A simple dot-eyes face is allowed only when the user or the concept asks for comic
  expressions; lock that choice for the whole video.
- **Palette:** background and figures monochrome per theme. Up to **three** saturated accents
  across the whole video, each with one meaning (for example problem, insight, payoff). For a
  brand ad the brand's primary color is one of them and owns the product and the payoff.
- **Clip length and count:** ~10 seconds per clip, sized to the video. ~30s = 3 clips, ~60s = 6
  clips (the default for an explainer). Narration runs ~2.3 to 2.5 words per second: 20 to 25
  words per clip, 130 to 150 words for 60 seconds.
- **Stills:** `advibly_generate_image`, `model: "gpt-image-2"`, `quality: "high"`,
  `on_brand: false`, the generation aspect (below). `nano-banana-2` only for a single still that
  keeps picking up shading.
- **Motion:** `advibly_generate_video`, `model: "gemini-omni-flash-1.1"`, `duration: 10`,
  `resolution: "720p"`, `start_image_url` = this clip's still, `end_image_url` = next clip's still
  (omit on the last clip or on a planned hard cut). No `reference_image_urls` alongside a start
  frame. If the user names another model, use it for every clip. `seedance-2.0` (`mode: "pro"`)
  only for a single move that must run past 10 seconds, with approval.
- **Generation aspect:** Omni 1.1 renders 9:16 or 16:9 only. For `1:1`, generate 9:16 stills and
  clips with every important event inside the centered square, then compose at `1:1` (the renderer
  scales to fill and crops top and bottom).
- **Every call carries `brand_id` and `project_id`.** Create the project as soon as the brand is
  resolved.
- **Prompts cap at 2000 characters** on image and video tools. Trim adjectives, never the locks.
- **Final cadence:** `frame_cadence: "on_twos"` gives the snappy limited-animation feel and suits
  pose-driven comic pieces. Clips carrying long camera travel read smoother with `"smooth"`.
  Propose one in the director's proposal; the user decides.
- **Tools are deferred.** Load exact schemas with tool search before the first call ("advibly
  generate image", "advibly generate video", "advibly generate voiceover", "advibly generate
  music", "advibly render composition", "advibly create project", "advibly update project",
  "advibly get products", "advibly get brand") and trust what loads over this file.

## PHASE 1: KICKOFF (one batched message)

Resolve silently first: `advibly_list_brands` (one brand: use it; several: ask; none: send the
user to advibly.com/onboarding), then `advibly_get_brand` for tone, audience, brief, and primary
color. Then ask only what is still missing, in one message:

1. **Source**: the product or angle, or the copy, notes, or topic to turn into a video.
2. **Theme**: light (flat white canvas, black figures) or dark (flat black canvas, white figures).
3. **Aspect ratio**: `9:16` (Shorts, Reels, TikTok), `16:9` (YouTube, explainers), or `1:1`
   (feeds).
4. **Length** if not obvious: ~30s (3 clips) or ~60s (6 clips).

Do not re-ask anything already given. Optional preferences (narrator voice, tone, accent colors,
product to feature) get sensible defaults you state in the proposal.

For a product ad on a store brand, `advibly_get_products` and pick the product with the user. The
product appears as a **flat line-art prop** in the brand color, redrawn from its photo, never the
photo itself.

Create the project: `advibly_create_project` with `brand_id` and a deliverable name ("Acme
stickman explainer"). Continuing an earlier run: find it with `advibly_list_projects`.

## PHASE 2: DIRECTOR'S PROPOSAL (the approval gate)

Read `references/director-proposal.md` and produce the proposal. It contains:

- Title, core message, and the opening hook (the first 3 seconds).
- Theme, aspect ratio, and the composition strategy for that ratio.
- Narrator voice and delivery, word count, estimated duration.
- Up to three accents in plain color names, each with its meaning.
- Music direction with the emotional turn and its timestamp; proposed final cadence.
- The clip table: one row per ~10 second clip with narrative purpose, the three timed beats, the
  visual devices and camera, the narration line (plus reference translation when the user writes
  in another language), SFX, and the **named transition interface** to the next clip.
- Optional post-production text overlays (2 to 5 words, clip, position), kept outside every
  generation prompt.
- The credit estimate (see the reference).

End with three choices: approve and render, revise a named clip or line, or change a global
setting (theme, ratio, palette, voice, tone, length). **Stop.** Do not generate anything until the
user approves the current proposal.

- Approval of the topic, of an earlier draft, or "just go" before seeing a proposal is not
  approval of the current proposal.
- A change to theme, ratio, length, narration, clip structure, or palette **invalidates approval**.
  Recompose (a new ratio means new staging, camera paths, and overlay space, not a relabel) and ask
  again. A local edit to one clip only needs that clip re-shown.

## PHASE 3: OPENING STILLS (one per clip)

Read `references/storyboard-prompts.md`. Each still is the **first frame of its clip**, which is
also the landing frame of the clip before it. Draw exactly the state the transition interface
names (the violet tangle filling the frame, the raised foot, the gold beam across the width).

```
advibly_generate_image
  prompt: <STYLE LOCK + FRAME + PALETTE + NEGATIVE, plain color names only>
  brand_id, project_id
  model: "gpt-image-2"
  quality: "high"
  on_brand: false
  aspect_ratio: "9:16" or "16:9"
  reference_image_urls: [<style plate URL>, <product photo URL on product clips only>]
```

1. Render clip 1's still first. It is the **style plate**: it fixes line weight, head size, and
   proportions. Show it and get a quick yes before the rest.
2. Render the remaining stills in parallel, each with the style plate attached (plus the product
   photo only where the product is in frame).
3. QA each still against the checklist in the reference. Re-roll misses; stills are cheap next to
   clips.
4. Show all stills in order with their narration lines. This is the second gate. Do not animate
   until the user approves.

## PHASE 4: CLIPS (parallel, anchored on the stills)

Read `references/animate-prompts.md`. Every clip prompt follows the clip contract: frame hold,
locks, three timed beats, landing state, SFX, negatives. Every prompt is standalone and repeats the
locks; the model has no memory of the other clips.

```
advibly_generate_video
  prompt: <clip contract, under 2000 chars>
  brand_id, project_id
  model: "gemini-omni-flash-1.1"
  aspect_ratio: "9:16" or "16:9"
  duration: 10
  resolution: "720p"
  start_image_url: <clip N still>
  end_image_url: <clip N+1 still>          # omit on the last clip or a planned hard cut
```

- Both anchors are stills, never a previous clip's output, so **every clip renders in parallel**.
- QA every clip (checklist in the reference): flat linework end to end, no shading or 3D, the start
  frame held, all three beats happened, no visible text, lands on the next still.
- Re-roll a failed clip with the specific constraint tightened, up to two retries. A clip whose
  middle idles needs a busier beat 2, not a shorter duration.

## PHASE 5: VOICEOVER, MUSIC, FINAL COMPOSITION

Read `references/audio-and-gotchas.md`.

1. **Voiceover**: one `advibly_generate_voiceover` per clip line, same `voice` every time. Check
   each fits its 10 second window; rewrite and regenerate any line that overflows.
2. **Music**: `advibly_generate_music`, `instrumental: true`, in the proposal's mood. One bed, or
   two with a hard switch at the emotional turn when the arc demands it.
3. **Compose once** with `advibly_render_composition`: clips as ordered `scenes` (each
   `volume: 0.25`), one `voiceovers` entry per clip at `start_seconds` = the sum of the previous
   clips' durations, `music`, `keep_scene_audio: true`, the proposal's `frame_cadence`, the
   approved overlays as `texts`, `aspect_ratio` (the final ratio, `1:1` included), `project_id`.
4. `advibly_update_project` with `cover_generation_id` = the composition's generation id.
5. Deliver the video and the `edit_url` (the user can adjust overlays, cadence, and timing in the
   Advibly editor).

Optional after delivery: captions via `advibly_add_subtitles` on the finished render, and
publishing via `advibly_social_list_accounts` then `advibly_social_create_post`, offered only once
the user has seen the finished video.

## Notes and rules

- **Source fidelity.** Strengthen the hook, the progression, and the close; never invent
  statistics, quotes, studies, or product claims. Pull claims from the brand brief, dossier, or the
  user's copy.
- **Recompose, do not rename.** `16:9` stages action left, center, right with lateral tracking and
  negative space. `9:16` uses depth, vertical reveals, stacked motion, and interface-safe margins.
  `1:1` keeps action compact and central with short travel.
- **Theme change** inverts the canvas and base line art, keeps the accent meanings, and rechecks
  contrast. It needs new stills.
- **Say "rapid scene changes and kinetic transformations while preserving an identical stick
  figure design"**, never "rapid style changes", which invites the model to change the drawing.
- **On failure:** `content_rejected` means rework wording (no real people, no third-party marks).
  `insufficient_credits`: `advibly_buy_credits` and share the link. Shading creeping into a still:
  re-roll, then try `nano-banana-2` for that still only.

## Honest limits

- The video model can still add soft shading, gray tint on a light canvas, or boil the lines.
  Guarded hard, but watch every clip; on_twos also hides minor wobble.
- End-frame landings are strong but not exact; a clip may reach the landing state a few frames
  early or late. Trim in the editor if a seam stutters.
- Product logo text on a small flat prop can garble in motion. Keep the prop large on the clips
  that feature it.
- Voices are the five xAI voices, not bespoke casting.

## Reference files

- `references/director-proposal.md`: story patterns, the visual-density recipe, the device menu,
  composition by ratio, palette and text rules, transition interfaces, the proposal format,
  cost shape, and the proposal checks. Read before Phase 2.
- `references/storyboard-prompts.md`: the theme-aware STYLE LOCK, the opening-still scaffold, the
  product prop rule, and the still QA checklist. Read before Phase 3.
- `references/animate-prompts.md`: the Omni 1.1 clip contract, the compact lock and negative
  blocks, the character budget, and the clip QA checklist. Read before Phase 4.
- `references/audio-and-gotchas.md`: voice map and timing, music, the composition call, overlays,
  cadence, and failure modes. Read before Phase 5.
- `references/example.md`: one complete worked example (proposal excerpt, two stills, two clip
  prompts, the composition call). Load only when a concrete example would resolve ambiguity; reuse
  its method and level of detail, never its topic, metaphors, or palette.
