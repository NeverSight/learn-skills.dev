---
name: create-video
description: Full video production pipeline — from a text prompt to a live Studio preview with voiceover, music, sound effects, stock footage, and motion graphics, rendered to MP4 when you ask. The flagship command of Remotion Superpowers.
---

# Create Video — Full Production Pipeline

You are the Video Director. The user wants to create a complete video. Follow this pipeline step by step.

**IMPORTANT:** Load the `remotion-production` skill for the MCP steps, asset conventions and creative guidance. Load the official `remotion-best-practices` skill (it routes to `remotion-create`, `remotion-markup`, `remotion-studio`, `remotion-render`, `remotion-captions`) for all Remotion markup, preview and render. When they disagree on Remotion APIs, the official skills win.

## Pre-flight Check

Before starting, verify:
1. MCP servers are available — check with `/mcp` if unsure. If anything is missing, suggest running `/setup`.
2. `ELEVENLABS_API_KEY` is set for audio (if not, follow the official ElevenLabs `setup-api-key` skill), and the official ElevenLabs skills are installed (`npx skills add elevenlabs/skills`).
3. The agent was launched from the Remotion project root (remotion-media tools write to `public/` of the launch directory).

## Pipeline

### Phase 0: Project and Preview

1. **Project:** if a Remotion project exists (a `remotion` dependency in `package.json`), use it. Otherwise scaffold it exactly as official `remotion-create` says (inspect the folder first, then `npx create-video@latest --yes --blank --no-tailwind`).
2. **Studio, right away:** as soon as the project runs, start Studio and keep it open for the whole session:
   ```bash
   npx remotion studio            # opens the browser itself
   npx remotion studio --no-open  # with an in-app browser: open the URL it prints
   ```
   Open the exact URL Studio prints (it picks a free port), then `/<composition-id>` once the composition exists. Details: official `remotion-studio`.

The user now watches every scene and asset land live and can steer at any point.

### Phase 1: Concept Breakdown

Ask the user to describe their video (or use their existing description). Then break it down:

```
📋 Video Production Plan

Duration: [X seconds]
Aspect Ratio: [16:9 / 9:16 / 1:1]
Style: [describe visual style]

Scenes:
1. [0:00-0:05] Intro — [description]
2. [0:05-0:15] Main content — [description]  
3. [0:15-0:25] Supporting content — [description]
4. [0:25-0:30] Outro/CTA — [description]

Audio Plan:
- Voiceover: [yes/no] — [voice style]
- Music: [genre/mood description]
- Sound Effects: [list any needed SFX]

Visual Assets Needed:
- Stock footage: [list queries]
- Generated images: [list descriptions]
- Existing footage: [list files to analyze]
```

**Present this plan to the user and get approval before generating any assets.**

### Phase 2: Generate Audio Assets

Do this FIRST — audio determines timing.

Audio comes from the **official ElevenLabs skills** (`text-to-speech`, `music`, `sound-effects`); load them for the exact SDK calls. Write all of it in one script, `scripts/generate-audio.ts` (`@elevenlabs/elevenlabs-js`, `ELEVENLABS_API_KEY`), and run it with `node scripts/generate-audio.ts`. The full step, with the file table, is in the `production-pipeline` rule (Step 4).

#### 2a. Voiceover (if needed)
Write the narration script, split by scene. The script generates one file per scene with `eleven_v4`:
```
text-to-speech (official skill), once per scene:
- text: [narration for scene 1]
- voice: [chosen voice ID]
- model: eleven_v4
→ public/vo-scene1.mp3, public/vo-scene2.mp3, …
```

Nothing returns a duration. **Measure each file in `calculateMetadata`** (see the `voiceover-sync` rule and official `remotion-multimedia`); the per-scene durations set the scene lengths and the video length, in whole frames (`Math.ceil`).

#### 2b. Background Music
```
music (official skill):
- prompt: [music description, instrumental]
- length: the video's length
- model: music_v2_5
→ public/music-bg.mp3
```
Eleven Music is cleared for commercial use on paid plans.

#### 2c. Sound Effects (if needed)
For a generic whoosh or click, the hosted sounds in official `remotion-markup` sfx.md are fine and free. Generate only custom SFX:
```
sound-effects (official skill):
- text: [sound description]
- duration: [length in seconds]
→ public/sfx-whoosh.mp3, …
```

**Drafts only:** remotion-media's `generate_speech`, `generate_music` and `generate_sound_effect` (KIE) are a cheap way to sketch, with the same `output_name`s. Suno and the other KIE-resold models aren't licensed by their owners through KIE. Use KIE audio for drafts and internal work, and generate final commercial audio with ElevenLabs.

### Phase 3: Source Visual Assets

#### 3a. Stock Footage (Pexels)
For each scene needing stock footage:
```
Use Pexels pexels_search_videos:
- query: [descriptive keywords]
- orientation: landscape
- size: medium   (Full HD; large = 4K)
- per_page: 5
```
Get the renditions with `pexels_get_video` (`id`), take the file link closest to the composition size and download it: `mkdir -p public/footage && curl -L -o public/footage/<name>.mp4 <link>`. Download only the clips you'll use. Pexels doesn't require attribution, but it's appreciated.

#### 3b. Analyze Existing Footage (TwelveLabs)
If user has footage files:
```
- create-asset (file: absolute path) → asset ID
- async-analyse-video (assetId, modelName: "pegasus1.5", analysisMode: "time_based_metadata", segmentDefinitions) for a scene map,
  or sync-analyse-video (assetId, modelName: "pegasus1.5", prompt, jsonSchema) to pick clips directly
- delete-asset when the timestamps are saved
```
Details: the `video-analysis` rule (it also covers `search` for finding moments across an indexed library).

#### 3c. Generate Images and Clips (if needed)
```
Use remotion-media generate_image:
- prompt: [image description]
- output_name: img-scene1
- aspect_ratio: [16:9 / 9:16 / 1:1, matching the video]
```
For AI clips, `generate_video_from_text` or `generate_video_from_image` (`output_name: clip-<name>`; `image_urls` must be public URLs). If a KIE call fails, fall back to Replicate as the `replicate-models` rule shows (`search_models`, read the schema with `get_models`, then `create_models_predictions`, download into `public/images/` or `public/footage/`).

### Phase 4: Build the Composition Live

Build scene by scene while Studio is open, so each one appears in the preview as soon as its assets exist. Don't wait until every asset is done.

For all markup, follow official `remotion-markup` (and its `multi-scene-video.md`, `audio.md`, `embedding-videos.md`, `transitions.md`), plus `remotion-create/video-layout.md` for layout and text sizes:

1. **One component per scene** in `src/scenes/`, each in its own `<TransitionSeries.Sequence>` or `Track` item, as official multi-scene-video.md describes
2. **Audio:** voiceover inside its scene, music with `loop` and fades/ducking (see the `audio-integration` and `music-scoring` rules), SFX at the right frames. `<Audio>` and `<Video>` come from `@remotion/media` (`npx remotion add @remotion/media`); reference files with `staticFile("vo-scene1.mp3")`, `staticFile("footage/city.mp4")` and so on
3. **Register the composition** in `src/Root.tsx` with `calculateMetadata` measuring the voiceover
4. **Captions** (if wanted): run `/add-captions`, which follows official `remotion-captions` (whisper-webgpu with a GPU; ElevenLabs Scribe through `@remotion/elevenlabs` as the fallback)

After each scene, tell the user to look at it in Studio.

### Phase 5: Iterate

Ask for feedback and make adjustments:
- Timing changes
- Visual tweaks
- Audio volume adjustments
- Text/copy changes

**Preserve user changes:** if the user edited the code or tweaked things in Studio between turns, keep their edits and build on them.

### Phase 6: Offer to Render

Don't render automatically. When the user is happy, offer the options:
- Render from Studio's render button (the most intuitive option)
- Or render on request from the command line, following official `remotion-render`:
  ```bash
  npx remotion render [CompositionId] out/video.mp4 --codec h264 --crf 18
  ```
- Or run `/review-video` for an AI director's review (that skill renders as part of its job)

## Guidelines

- **Keep visuals simple** — clean text, smooth transitions, not too many moving elements
- **Iterate incrementally** — get basics working, then add polish
- **Test audio sync** — check in Studio after adding each audio layer
- **Use consistent styling** — pick a color palette and font family, stick with them
- **Organize files** — generated files at the `public/` root with typed names (`vo-`, `music-`, `sfx-`, `img-`, `clip-`), downloads in `public/footage/` and `public/images/`, the audio script in `scripts/generate-audio.ts`, scenes in `src/scenes/`
