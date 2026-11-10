---
name: vox-explainer
description: End-to-end pipeline for producing Vox-style explainer videos from a single topic prompt. One topic in, finished film out — script, keyframes (Seedream 5.0 Pro), animation (Gemini Omni Flash), voiceover (xAI TTS), music (MiniMax Music 2.6), all assembled locally with ffmpeg via the Atlas Cloud API. Use this skill whenever the user asks for an explainer video, a Vox-style video, a documentary short, an educational video essay, a "one prompt to video" pipeline, or wants to turn a topic/article/report into a narrated video with subtitles and music. Also trigger when the user mentions Atlas Cloud video pipelines, keyframe-to-animation workflows, or automated video essays — even if they don't say "Vox."
---

# Vox-Style Explainer Video Pipeline

Produce a complete, narrated, subtitled, scored explainer video from a single topic. The pipeline runs in six stages, each producing artifacts the next stage consumes. Voiceover is generated BEFORE animation because VO duration drives all timing decisions.

```
TOPIC → 1.Script → 2.Voiceover → 3.Keyframes → 4.Animation → 5.Music → 6.Assembly
         (Claude)   (xAI TTS)    (Seedream)    (Omni Flash)  (MiniMax)  (ffmpeg)
```

## Prerequisites

- `ATLASCLOUD_API_KEY` environment variable set (get one at atlascloud.ai — free credits on signup)
- `ffmpeg` and `ffprobe` installed (with libass for subtitle burning)
- Python 3.10+ with `requests`
- ~$3–8 in API credit per 60-second film (see cost table in `references/atlas-cloud-api.md`)

Before making any API calls, verify current endpoint paths and model IDs against https://www.atlascloud.ai/docs — media model APIs evolve quickly. The patterns in `references/atlas-cloud-api.md` were verified July 2026.

## Project structure

Create this layout for every film and keep it — every stage reads from and writes to it:

```
project/
├── brief.md            # topic, angle, target length, audience
├── script.json         # beats with narration, shot descriptions, captions
├── audio/
│   ├── vo/             # beat_01.mp3 ... beat_NN.mp3
│   ├── vo_durations.json
│   └── music.mp3
├── frames/             # keyframe_01.png ... style_anchor.png
├── clips/              # clip_01.mp4 ... (silent animated clips)
├── subs/               # captions.ass
└── final/              # film.mp4
```

## Stage 1 — Script

You write this yourself. No API call. This is the stage that most determines quality — a great script with average visuals beats the reverse.

Read `references/vox-style-guide.md` (Writing section) before drafting. Core rules:

1. **Structure as beats.** A beat = one narration paragraph (1–3 sentences, 8–14 seconds spoken) + one visual. A 60-second film is 6–8 beats; 3 minutes is 16–22 beats.
2. **Vox narrative arc:** cold-open hook (a surprising concrete fact or question) → context ("to understand X, you have to go back to...") → escalating explanation with one clear throughline → complication or twist → resolution that reframes the hook.
3. **Voice:** second person welcome ("you've probably seen..."), present tense for historical narrative, concrete numbers over abstractions, short declarative sentences. No throat-clearing, no "in this video we will."
4. **One idea per beat.** If a sentence introduces a second concept, split the beat.

Write `script.json`:

```json
{
  "title": "Tang Golden Age",
  "topic": "How Tang Dynasty China built the world's largest city",
  "style_seed": "mixed-media paper collage, ink-wash Chinese mountains, vermillion red and aged cream palette",
  "accent_color": "#C0392B",
  "beats": [
    {
      "id": 1,
      "narration": "In the seventh century, Tang China built Chang'an — the largest, richest city on Earth. The whole world came to its gates.",
      "visual": "Emperor Taizong enthroned at center as paper cutout, court figures flanking, pagodas and ink-wash mountains behind, red seal stamp upper right reading 盛唐",
      "caption_text": null,
      "motion": "slow push-in on emperor, clouds drift left, subtle parallax between cutout layers"
    }
  ]
}
```

`caption_text` is for on-screen kinetic typography moments (a key stat or term) — most beats leave it null; narration subtitles are handled at assembly. `motion` becomes the animation prompt in Stage 4.

## Stage 2 — Voiceover (xAI TTS v1)

Generate one audio file per beat, then measure durations. These durations are the master clock for the whole film.

Call the Atlas Cloud audio endpoint per beat (model: xAI TTS v1 — see `references/atlas-cloud-api.md` for the exact request shape and voice selection guidance). Pick ONE voice for the whole film. Vox register: measured, warm, slightly wry — avoid "movie trailer" voices.

After generation, probe every file and write `audio/vo_durations.json`:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 audio/vo/beat_01.mp3
```

```json
{"beats": [{"id": 1, "file": "audio/vo/beat_01.mp3", "duration": 9.83}], "total": 61.2}
```

Sanity-check total length against the brief. If a beat runs long, tighten the narration and regenerate that beat only.

## Stage 3 — Keyframes (Seedream 5.0 Pro)

One keyframe per beat, all in a consistent visual style. Consistency is the hard problem; solve it with the **style anchor pattern**:

1. **Generate the anchor.** Use `bytedance/seedream-v5.0-pro/text-to-image` for beat 1 (usually the title/hook frame). Build the prompt from the style block in `references/vox-style-guide.md` (Visual Grammar section) + the beat's `visual` + the film's `style_seed` and `accent_color`. Request 16:9, 2K.
2. **Review the anchor before proceeding.** Regenerate until the style is right — every other frame inherits it.
3. **Generate remaining frames with the edit model.** Use `bytedance/seedream-v5.0-pro/edit` with the anchor as a reference image (up to 10 refs supported; anchor + optionally the previous frame). Prompt: "Keep the exact art style, palette, paper-collage treatment, and border framing of the reference. New scene: {beat.visual}"

This locks palette, texture, and framing across the film the way a human art director would.

Every prompt should end with the style suffix (see style guide), which encodes the Vox look: paper cutouts with white borders, halftone dots, tape strips, bold flat geometric accents, generous margins, single accent color.

Frames with `caption_text` set: instruct Seedream to render the text in a bold condensed sans, since Seedream 5.0 Pro's typography rendering is strong. Keep it under 5 words per frame.

## Stage 4 — Animation (Gemini Omni Flash)

Animate each keyframe into a clip via image-to-video. Target clip duration = that beat's VO duration + 0.5s of breathing room (round up to the model's supported increments).

Motion prompts for the collage aesthetic should be SUBTLE — this is the most common failure mode. The Vox look is "motion graphics," not "footage." Good motion vocabulary:

- slow push-in / pull-out (2D camera, not 3D dolly)
- parallax drift between cutout layers
- clouds/smoke drifting laterally
- paper elements sliding in from frame edge and settling
- halftone dots or texture shimmering gently
- a single element animating (flag waving, water rippling) while everything else holds

Explicitly forbid in every prompt: "no camera shake, no 3D rotation, no morphing of faces or text, no style drift, elements remain flat paper cutouts."

Poll each generation task to completion and download to `clips/clip_NN.mp4`. Generations fail or drift sometimes — review each clip; regenerate any where text warps or the style breaks. Budget for ~15% regeneration.

## Stage 5 — Music (MiniMax Music 2.6)

One instrumental bed for the whole film. Request `is_instrumental: true` — vocals fight the narration.

Prompt formula: `{mood} {genre-adjacent texture}, {tempo}, {instrumentation}, {arc}`. Example for a history piece: "contemplative cinematic underscore, felt piano and soft strings with light percussion pulse, 90bpm, builds gradually from sparse to full, documentary style". Match instrumentation to subject (guzheng/dizi textures for the Tang piece; analog synth pulse for a tech topic).

Music 2.6 generates fixed-length songs; if the track is shorter than the film, loop it at assembly with a crossfade; if longer, trim with fade-out. Never let the music arc fight the film arc — a mid-track drop landing on a quiet beat is jarring, so audition the result against the film's shape.

## Stage 6 — Assembly (ffmpeg, local)

Read `references/ffmpeg-assembly.md` for full recipes. The sequence:

1. **Conform each clip** to its beat's VO duration (trim or hold last frame), normalize to 1920x1080 30fps.
2. **Concat** clips in order.
3. **Build the VO track** by concatenating beat audio with 0.5s gaps matching the video timing.
4. **Generate `subs/captions.ass`** from the script — Vox-style burned-in subtitles: bold sans, white with heavy black outline, bottom-centered, max 2 lines, split narration at clause boundaries and time each chunk within its beat's window.
5. **Mix audio:** VO at full level, music ducked -12 to -15dB under narration (sidechain compression or a simple volume automation — recipes in the reference).
6. **Burn subtitles + attribution** ("Made with ..." small lower-right if desired) and encode: H.264, CRF 18, AAC 192k, `-movflags +faststart`.

Final QC pass before delivering: watch for (a) subtitle/VO sync drift, (b) music overpowering narration, (c) a clip whose motion loops visibly, (d) style drift between frames. Fix at the stage where the problem originated, not with assembly hacks.

## Orchestration notes

- Run stages strictly in order the first time; after that, any stage can be re-run in isolation because all state lives in the project files.
- API generation is slow (video clips: 1–4 min each). Submit all animation tasks concurrently, then poll — don't serialize.
- Keep every prompt you send in a `prompts.log` file — reproducibility matters and users will want to tweak-and-regenerate single beats.
- Cost scales linearly with beats. Quote the user a rough cost before Stage 3 (the first paid-heavy stage): `beats × ($0.10 image + ~$1.20 per 10s clip) + ~$0.50 audio`.

## References

- `references/vox-style-guide.md` — read before Stage 1 and Stage 3. The visual grammar, writing voice, and prompt templates.
- `references/atlas-cloud-api.md` — read before Stage 2. Endpoints, model IDs, async task pattern, polling code, costs.
- `references/ffmpeg-assembly.md` — read before Stage 6. Conform, concat, subtitle, ducking, and encode recipes.
