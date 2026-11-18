---
name: add-voiceover
description: Generate a voiceover narration and add it to your Remotion project. Provide a script or describe what the narration should say, and this will generate per-scene ElevenLabs TTS audio (official ElevenLabs text-to-speech skill) and wire it into your composition.
---

# Add Voiceover — Generate & Integrate Narration

You are helping the user add a voiceover narration to their Remotion project.

**Load the `remotion-production` skill** for the `voiceover-sync` and `audio-integration` rules, and the official ElevenLabs **`text-to-speech`** skill (`npx skills add elevenlabs/skills`) for the API details.

## Workflow

### 0. Preview First

If Studio isn't running yet, start it now with `npx remotion studio` (or `--no-open` with an in-app browser, then open the URL it prints) and keep it open, following the official `remotion-best-practices` skill.

### 1. Get the Script

If the user hasn't provided a script:
- Ask what the video is about
- Ask about tone (professional, casual, energetic, calm)
- Write the narration script, **split into one line or paragraph per scene**
- Present for approval

### 2. Choose Voice

Pre-made voices (from the official `text-to-speech` skill):
- **George** (`JBFqnCBsd6RMkjVDRZzb`) — Male, narrative (default)
- **Sarah** (`EXAVITQu4vr4xnSDxMaL`) — Female, soft
- **Daniel** (`onwK4e9ZLuTAKqWW03F9`) — Male, authoritative
- **Charlotte** (`XB0fDUnXU5powFXDhCwa`) — Female, conversational

For a specific mood, accent or language, search the voice library; for a cloned voice or several speakers, see the `elevenlabs-advanced` rule. Use the same voice for every scene.

### 3. Generate TTS, One File per Scene

Generate through ElevenLabs, as the official Remotion voiceover guide also recommends:

1. If `ELEVENLABS_API_KEY` isn't set for the project, run `npx -y @elevenlabs/cli@latest onboard init` from the project root and follow what it prints. Never ask for the key in chat.
2. `npm i @elevenlabs/elevenlabs-js`, then create `scripts/generate-audio.ts` from the `audio-integration` rule, with one `voiceover` entry per scene (`vo-scene1`, `vo-scene2`, …) and the chosen `VOICE_ID`. The model is `eleven_v4`.
3. Run `node scripts/generate-audio.ts` from the project root. Each scene lands at `public/vo-sceneN.mp3`. To redo one line, delete its file and run the script again.

The script reports **no duration**; step 4 measures the files.

**Alternatives:**
- The **ElevenLabs MCP** `text_to_speech` tool is deprecated (archived upstream) but still ships for quick interactive one-offs. It writes into `public/`; rename its output to `vo-sceneN.mp3`.
- **KIE `generate_speech`** (remotion-media) for cheap drafts: `text`, `output_name: vo-scene1`, `voice: Eric` (21 named voices, listed in the `voiceover-sync` rule). Suno and the other KIE-resold models aren't licensed by their owners through KIE. Use KIE audio for drafts and internal work, and generate final commercial audio with ElevenLabs.

### 4. Size the Scenes with calculateMetadata

Measure each `vo-sceneN.mp3` in `calculateMetadata` with Mediabunny and pass the per-scene frame counts (`Math.ceil(seconds * fps)`) as props, as the `voiceover-sync` rule shows. The composition length then follows the audio, and regenerating a line updates the timing in Studio.

### 5. Wire into Composition

Place each scene's file with `<Audio>` from `@remotion/media` inside that scene (install with `npx remotion add @remotion/media`), following the official `remotion-markup` skill (audio.md):

```tsx
import { Audio } from "@remotion/media";
import { staticFile } from "remotion";

// Inside scene 1:
<Audio src={staticFile("vo-scene1.mp3")} volume={1} />
```

### 6. Captions (optional)

Offer captions. They follow the official `remotion-captions` skill (word-level, `@remotion/whisper-webgpu`), with an ElevenLabs Scribe fallback when there's no GPU and TikTok-style presets from the `captions-workflow` rule. Run `/add-captions`, or `/transcribe` if the user only wants an `.srt` file.

### 7. Duck Background Music (if present)

If the project already has background music, lower its volume during voiceover. See `audio-integration` rule for the ducking pattern.

### 8. Review in Studio

Ask the user to play it in the open Studio. Don't render unless they ask for an MP4.
