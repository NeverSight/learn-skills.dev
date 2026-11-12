---
name: add-music
description: Generate background music and add it to your Remotion project. Describe the mood/genre you want, and this will generate a commercially licensed track with Eleven Music (official ElevenLabs music skill) and wire it into your composition with proper fade in/out.
---

# Add Music — Generate & Integrate Background Music

You are helping the user add background music to their Remotion project.

**Load the `remotion-production` skill** for the `music-scoring` and `audio-integration` rules, and the official ElevenLabs **`music`** skill (`npx skills add elevenlabs/skills`) for the API details.

## Workflow

### 1. Understand the Mood

If not already described, ask the user:
- **Genre** — Electronic, jazz, classical, lo-fi, ambient, rock, orchestral, pop?
- **Mood** — Upbeat, calm, dramatic, inspiring, playful, cinematic?
- **Tempo** — Fast, medium, slow?
- **Vocals** — Instrumental only (recommended for background), or with vocals?

### 2. Generate Music

Generate with Eleven Music (`music_v2_5`). It's cleared for commercial use on paid ElevenLabs plans, and the Music API needs one.

1. If `ELEVENLABS_API_KEY` isn't set for the project, run `npx -y @elevenlabs/cli@latest onboard init` from the project root and follow what it prints. Never ask for the key in chat.
2. `npm i @elevenlabs/elevenlabs-js`, then add a `music` entry to `scripts/generate-audio.ts` (create it from the `audio-integration` rule if it doesn't exist):

```ts
const music = [
  { name: "music-bg", prompt: "[genre] background music, [mood], [tempo], [additional descriptors]", lengthMs: 30_000 },
];
```

3. Set `lengthMs` to the video length plus a few seconds (measure the voiceover first if there is one). The script forces instrumental output; for a track with vocals, set `forceInstrumental: false`.
4. Run `node scripts/generate-audio.ts` from the project root. The track lands at `public/music-bg.mp3`. To regenerate it, delete the file and run the script again.

**Good prompt examples:**
- "upbeat electronic background music, energetic, modern tech startup vibe"
- "calm acoustic guitar, warm and friendly, coffee shop atmosphere"
- "epic cinematic orchestral, building tension and release, trailer style"
- "chill lo-fi hip hop beats, relaxed and dreamy, study music vibe"

Don't name artists, bands or song lyrics in the prompt; Eleven Music rejects them and suggests a rewording.

**Alternatives:**
- The **ElevenLabs MCP** `compose_music` tool is deprecated (archived upstream) but still ships for quick interactive one-offs. It writes into `public/`; rename its output to `music-bg.mp3`.
- **KIE `generate_music`** (remotion-media, Suno) for cheap drafts: `prompt`, `output_name: music-bg`, `instrumental: true`. Suno and the other KIE-resold models aren't licensed by their owners through KIE. Use KIE audio for drafts and internal work, and generate final commercial audio with ElevenLabs.

### 3. Wire into Composition

Place it with `<Audio>` from `@remotion/media` (install with `npx remotion add @remotion/media`), following the official `remotion-markup` skill (audio.md), with fade in/out:

```tsx
import { Audio } from "@remotion/media";
import { interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { durationInFrames, fps } = useVideoConfig();

<Audio
  src={staticFile("music-bg.mp3")}
  volume={interpolate(
    frame,
    [0, fps, durationInFrames - 2 * fps, durationInFrames],
    [0, 0.25, 0.25, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  )}
/>
```

### 4. Adjust for Voiceover (if present)

If the project has a voiceover, implement volume ducking — lower music to 0.1 during narration, 0.3 during silent parts. See `audio-integration` rule for the pattern.

### 5. Preview in Studio

If Studio isn't running, start it with `npx remotion studio` (or `--no-open` with an in-app browser, then open the URL it prints). Ask the user to listen there. Don't render unless they ask for an MP4.

Offer adjustments:
- Volume too loud/quiet?
- Wrong mood? Change the prompt, delete `public/music-bg.mp3` and run the script again.
- Music too short? Regenerate with a longer `lengthMs`, or add `loop` to the `<Audio>`.
- Need different music for different sections? Add more `music` entries (`music-intro`, `music-main`, …) and give each `<Audio>` its own `from` and `durationInFrames`, or use a composition plan (official `music` skill) for one track with sections.
