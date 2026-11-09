---
name: create-short
description: Create a short-form vertical video (TikTok, Instagram Reels, YouTube Shorts). Optimized 9:16 pipeline with a live Studio preview, auto-captions, hook-first structure, and background music mood selection; renders to MP4 only when you ask.
---

# Create Short — Vertical Short-Form Video Pipeline

You are creating a short-form vertical video optimized for TikTok, Instagram Reels, or YouTube Shorts.

**Load the `remotion-production` skill** for the MCP steps and the `captions-workflow` rule, plus the official `remotion-best-practices` skill for all Remotion markup, preview and render (it routes to `remotion-create`, `remotion-markup`, `remotion-captions`, `remotion-render`). The official skills win on Remotion APIs.

## Key Differences from `/create-video`

- **Aspect ratio**: 9:16 (1080x1920) — ALWAYS vertical
- **Duration**: 15–60 seconds max (sweet spot: 30s)
- **Hook first**: First 2-3 seconds must grab attention
- **Captions required**: Always add TikTok-style word-by-word captions
- **Background music**: Always include — with mood tags
- **Pacing**: Fast cuts, 2-5 seconds per scene, no slow moments

## Pipeline

### Phase 0: Project and Preview

1. Use the existing Remotion project, or scaffold one exactly as official `remotion-create` says (`npx create-video@latest --yes --blank --no-tailwind`, after inspecting the folder).
2. As soon as it runs, start Studio and keep it open: `npx remotion studio` (or `npx remotion studio --no-open` with an in-app browser). Open the exact URL it prints, then `/<composition-id>` once the composition exists.

### Phase 1: Concept (Keep It Simple)

Ask the user what the short is about, then structure it:

```
📱 Short Video Plan

Platform: [TikTok / Reels / Shorts]
Duration: [15-60 seconds]
Format: 1080x1920 (9:16 vertical)
FPS: 30

Structure:
  🪝 Hook (0-3s): [attention grabber — question, bold claim, visual shock]
  📖 Body (3-Xs): [main content — 2-4 fast scenes]
  📣 CTA (last 3-5s): [call to action — follow, link, comment]

Voiceover: [yes/no] — [style: energetic, conversational, dramatic]
Music Mood: [upbeat, chill, dramatic, inspiring, dark, funny]
Caption Style: [TikTok bold / karaoke / minimal]
```

**Get the user's approval on this plan before generating assets.**

### Phase 2: Generate Audio (voiceover drives everything)

Audio comes from the **official ElevenLabs skills** (`text-to-speech`, `music`, `sound-effects`), all in one script, `scripts/generate-audio.ts` (`@elevenlabs/elevenlabs-js`, `ELEVENLABS_API_KEY`), run with `node scripts/generate-audio.ts`. See the `production-pipeline` rule (Step 4) for the file table.

#### 2a. Voiceover
Write a TIGHT script — every word must earn its place in a short. Generate one file per part with `eleven_v4`:
```
text-to-speech (official skill):
- text: [short, punchy hook line — no filler words]
- voice: [an energetic voice ID]
- model: eleven_v4
→ public/vo-hook.mp3
```
Repeat for `vo-body`, `vo-cta` (or `vo-body1`, `vo-body2` for several body scenes).

Nothing returns a duration: measure each file in `calculateMetadata` (see the `voiceover-sync` rule and official `remotion-multimedia`).

#### 2b. Background Music
```
music (official skill):
- prompt: "[mood] background music for social media short, energetic, [genre], instrumental"
- length: the short's length
- model: music_v2_5
→ public/music-bg.mp3
```

**Good short music prompts:**
- "upbeat trendy pop beat for TikTok, energetic, no vocals"
- "dark cinematic bass, dramatic tension, no vocals, short form"
- "chill lofi beat for educational content, relaxed, no vocals"

Eleven Music is cleared for commercial use on paid plans. For quick drafts you can use remotion-media's `generate_speech` / `generate_music` (KIE) with the same `output_name`s, but Suno and the other KIE-resold models aren't licensed by their owners through KIE. Use KIE audio for drafts and internal work, and generate final commercial audio with ElevenLabs.

### Phase 3: Source Visuals

Search for VERTICAL footage:
```
Use Pexels pexels_search_videos:
- query: [keywords]
- orientation: portrait  ← IMPORTANT: portrait for 9:16
- size: medium           (Full HD is enough for 1080x1920)
- per_page: 5
```
Get the renditions with `pexels_get_video` (`id`) and download the closest one into `public/footage/` (`mkdir -p public/footage`, then `curl -L -o`). Download only the clips you'll use. Pexels doesn't require attribution, but it's appreciated.

Or generate images/clips with `aspect_ratio: "9:16"`:
```
Use remotion-media generate_image / generate_video_from_text (or generate_video_from_image to animate an image; image_urls must be public URLs)
- output_name: img-hook / clip-body1 / ...
- aspect_ratio: 9:16
```
If a KIE call fails, fall back to Replicate (the `replicate-models` rule: `search_models`, read the schema with `get_models`, `create_models_predictions`, download into `public/images/` or `public/footage/`).

### Phase 4: Build the Composition Live

Build each part while Studio is open, so the user sees the hook as soon as it exists. Follow official `remotion-markup` for all markup (`multi-scene-video.md`, `audio.md`, `embedding-videos.md`) and `remotion-create/video-layout.md` for layout:

- Register the composition at **1080x1920, 30 fps**, with `calculateMetadata` summing the measured voiceover durations (`Math.ceil`)
- **Hook → Body → CTA** as three adjacent scenes (`<TransitionSeries.Sequence>` items), each holding its own `vo-*` audio
- Music (`music-bg.mp3`) runs under everything with `loop`, ducked under the voice (see the `audio-integration` rule)
- `<Audio>`/`<Video>` from `@remotion/media`

**Typography for vertical** (above official video-layout.md minimums):
- Title text: 84-96px bold (fills width)
- Body text: 48-64px
- Captions: 64-80px bold with outline
- Keep key text in the center ~60% of the screen; platform UI covers the bottom ~15% and the right ~15%

### Phase 5: Add Captions

Captions are MANDATORY for shorts. Use the same workflow as `/add-captions`:

1. Transcribe each voiceover file with the official word-level flow (`remotion-captions/transcribe-captions.md`, `@remotion/whisper-webgpu`). Without a usable GPU, use ElevenLabs Scribe instead (official `speech-to-text` skill, `scribe_v2` with word timestamps) and convert it to `Caption[]` with `elevenLabsTranscriptToCaptions()` from `@remotion/elevenlabs` (https://www.remotion.dev/docs/elevenlabs). Both give word-level timing, so the TikTok styles still work.
2. Copy the official caption element for the chosen style (Popping Word Captions for TikTok bold) and put one inside each scene, next to that scene's voiceover, with the captions inlined (official `display-captions.md`)
3. Apply the TikTok preset from the `captions-workflow` rule: bold, high contrast, highlight color
4. Place it 15-25% up from the bottom, clear of the platform UI

### Phase 6: Review in Studio, Render on Request

Ask the user to check the short in Studio at 1080x1920 (and on a phone-sized window). Iterate on their feedback, and **preserve any edits they made in the code or in Studio**.

Render only when the user asks for the MP4, following official `remotion-render` (or use Studio's render button):
```bash
npx remotion render MyShort out/short.mp4 --codec h264 --crf 18
```

## Short-Form Best Practices

- **Hook or die** — If the first 2 seconds aren't compelling, viewers scroll away
- **One idea per short** — Don't try to fit everything, pick ONE topic
- **Text on screen** — Reinforce key points with bold text overlays
- **Fast pacing** — Cut every 2-4 seconds, no scene longer than 5s
- **Captions always** — 85% of social media videos are watched without sound
- **End with CTA** — "Follow for more", "Link in bio", "Comment below"
- **Safe zones** — Keep text away from edges (platform UI overlaps)
- **Loop-friendly** — Consider making the end transition into the beginning
