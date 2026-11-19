---
name: transcribe
description: Transcribe audio or video files to text with timestamps. Produces word-level Caption JSON through the official remotion-captions flow (whisper-webgpu, or ElevenLabs Scribe via @remotion/elevenlabs when there's no GPU), plus an SRT export generated from those captions and plain text, for use with Remotion's captions system.
---

# Transcribe: Audio/Video to Text

You are helping the user transcribe audio or video files into text with precise timestamps.

**Load the `remotion-production` skill** for the `captions-workflow` rule (both routes, including the Scribe script), and the official **`remotion-captions`** skill. For the Scribe route, also load the official ElevenLabs **`speech-to-text`** skill. The official skills win on any API detail.

## Workflow

### 1. Identify the Source File

Find audio/video files to transcribe:

```bash
ls public/ public/footage/ 2>/dev/null | grep -E '\.(mp3|wav|m4a|ogg|mp4|mov|webm)$'
```

Ask the user which file to transcribe if multiple exist. Transcribe each source file separately, and keep its timestamps relative to the start of that file.

### 2. Transcribe to Word-Level JSON

Every route below produces the same thing: a `Caption[]` with one entry per word, saved as `public/<source>.captions.json` (e.g. `vo-scene1.captions.json`). The SRT and plain-text outputs in step 4 are generated from it.

| Route | Use it when | Runs |
|---|---|---|
| **A. Official whisper-webgpu** (default) | A compatible GPU is available | Locally, free, no key |
| **B. ElevenLabs Scribe** (fallback) | whisper-webgpu can't run: no GPU, CI, Linux arm64, many VMs | In the cloud, paid, needs `ELEVENLABS_API_KEY` |

#### Route A: whisper-webgpu

Follow official `remotion-captions/transcribe-captions.md`. It writes a Node script using `@remotion/whisper-webgpu` (`canUseWhisperWebGpu`, `downloadWhisperModel`, `loadWhisperModel`, `transcribe`, then `toCaptions({ whisperWebGpuOutput })`) that decodes audio or video with Mediabunny and saves `Caption` JSON. `small.en` is the default model for English. For other languages, use a multilingual model and pass `language`: there's no auto-detect. If `canUseWhisperWebGpu()` reports no support, switch to Route B.

#### Route B: ElevenLabs Scribe

Transcribe with Scribe v2 (`timestamps_granularity: "word"`) and convert with `elevenLabsTranscriptToCaptions()` from `@remotion/elevenlabs` (`npx remotion add @remotion/elevenlabs`). The script is in the `captions-workflow` rule.
- If `ELEVENLABS_API_KEY` isn't set, run `npx -y @elevenlabs/cli@latest onboard init` from the project root. Never ask for the key in chat.
- It sends the audio to ElevenLabs and costs credits, so tell the user first.
- It takes video files directly, auto-detects the language (or pass `language_code`), and accepts `keyterms` for names it might mishear (official `speech-to-text` skill).

Don't use the ElevenLabs MCP `speech_to_text` tool: it returns plain text with no timestamps.

### 3. Present the Transcript

Show the transcription with timestamps, grouped into readable lines:

```
Transcription: [filename]

[00:00:00 → 00:00:03] Welcome to our product demo
[00:00:03 → 00:00:07] Today we're going to show you how easy it is
[00:00:07 → 00:00:11] to create professional videos with code
...

Total duration: [X]s
Word count: [X] words
```

### 4. Output Formats

Deliver what the user asked for:

**JSON Captions** (always): the `Caption` type from `@remotion/captions`. Every entry needs `timestampMs` and `confidence` (either may be `null`), and each word starts with a space:
```json
[
  { "text": " Welcome", "startMs": 0, "endMs": 800, "timestampMs": 400, "confidence": 0.95 },
  { "text": " to", "startMs": 800, "endMs": 1000, "timestampMs": 900, "confidence": 0.98 },
  { "text": " our", "startMs": 1000, "endMs": 1200, "timestampMs": 1100, "confidence": 0.97 }
]
```

**SRT export** (when the user wants an `.srt` file, e.g. to upload to YouTube): the official captions skill covers SRT import but not export, so generate it from the JSON with `serializeSrt()` from `@remotion/captions`. It takes `lines`, an array of lines where each line is an array of captions. Group the words into subtitle lines first:

```ts
// scripts/export-srt.ts: node scripts/export-srt.ts
import { serializeSrt, type Caption } from "@remotion/captions";
import { readFileSync, writeFileSync } from "node:fs";

const name = "vo-scene1";
const words: Caption[] = JSON.parse(readFileSync(`public/${name}.captions.json`, "utf8"));

// New line after 7 words, at a sentence end, or at a pause longer than 0.6 s
const lines: Caption[][] = [];
let line: Caption[] = [];
words.forEach((word, i) => {
  line.push(word);
  const next = words[i + 1];
  if (!next || line.length >= 7 || /[.!?]$/.test(word.text) || next.startMs - word.endMs > 600) {
    lines.push(line);
    line = [];
  }
});

writeFileSync(`public/${name}.srt`, serializeSrt({ lines }));
```

`serializeSrt()` joins a cue's words without adding spaces, which is right because each word's `text` already starts with one. Each cue runs from its first word's `startMs` to its last word's `endMs`. The result is standard SRT:
```srt
1
00:00:00,000 --> 00:00:03,200
Welcome to our product demo

2
00:00:03,200 --> 00:00:07,100
Today we're going to show you how easy it is
```

**Plain text**: join the words' `text` and trim, no timestamps:
```
Welcome to our product demo. Today we're going to show you how easy it is to create professional videos with code.
```

### 5. Common Use Cases

After transcription, suggest next steps:

- **Add captions** → Run `/add-captions`; the word-level JSON works with every style, including TikTok and karaoke
- **Sync animations** → Use the word timestamps to trigger visual elements at specific words
- **Create a script** → Edit the transcript as the basis for a new voiceover
- **Translate** → Use the transcript to create versions in other languages
- **Content repurpose** → Extract key quotes for social media clips

Route A runs entirely on-device with no API key. Route B is a cloud call to ElevenLabs.
