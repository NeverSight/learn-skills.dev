---
name: add-captions
description: Add TikTok-style, karaoke, YouTube or minimal captions to your Remotion video. Gets word-level captions through the official remotion-captions flow (whisper-webgpu, or ElevenLabs Scribe via @remotion/elevenlabs when there's no GPU), or imports the user's SRT with parseSrt, places one official caption element per clip, and applies a style preset with platform-safe placement.
---

# Add Captions: Animated Subtitles

You are helping the user add captions to their Remotion video.

**Load the `remotion-production` skill** for the `captions-workflow` rule (routes, presets and safe zones), and the official **`remotion-captions`** skill for transcription and display. For the Scribe fallback, also load the official ElevenLabs **`speech-to-text`** skill. The official skills win on any API detail.

## Workflow

### 1. Identify the Audio Source

Find the voiceover or primary audio file(s):

```bash
ls public/ public/footage/ 2>/dev/null | grep -E '\.(mp3|wav|m4a|ogg|mp4|mov|webm|srt)$'
```

If the user already has an `.srt` file, use it (step 3). If no audio exists, suggest running `/add-voiceover` first. If the video has one voiceover per scene (`vo-scene1.mp3`, `vo-scene2.mp3`, …), caption **each file separately**.

Make sure Studio is already running (`npx remotion studio`, or `--no-open` with an in-app browser; open the URL it prints), so the user sees captions appear.

### 2. Choose Caption Style

Ask the user what style they want:

- **TikTok style** (default): bold, a few words at a time, the active word pops in a highlight color. *Needs word-level.*
- **Karaoke style**: full phrase on screen, words highlight as they're spoken. *Needs word-level.*
- **YouTube style**: bottom of screen, a sentence at a time. *Also works with the user's SRT.*
- **Minimal**: small, subtle, bottom-left. *Also works with the user's SRT.*

### 3. Transcribe

Both routes give word-level `Caption` JSON, so every style works. Save each file's result as `public/<source>.captions.json` (e.g. `vo-scene1.captions.json`).

**Default: official whisper-webgpu.** Follow official `remotion-captions/transcribe-captions.md`. It writes a Node script with `@remotion/whisper-webgpu` that outputs one `Caption` per word. Local and free. It needs a compatible GPU and doesn't run on Linux arm64. Use `small.en` for English; for other languages use a multilingual model and pass `language`.

**Fallback: ElevenLabs Scribe.** When the script's `canUseWhisperWebGpu()` check fails, transcribe with Scribe v2 and convert with `elevenLabsTranscriptToCaptions()` from `@remotion/elevenlabs` (`npx remotion add @remotion/elevenlabs`). The script is in the `captions-workflow` rule. It needs `ELEVENLABS_API_KEY` (if it isn't set, run `npx -y @elevenlabs/cli@latest onboard init`), costs credits and sends the audio to ElevenLabs, so tell the user before running it. It accepts video files directly.

**User's own SRT.** Put it in `public/` and read it with `parseSrt()` from `@remotion/captions`, as official `import-srt-captions.md` shows. SRT is line-level: each caption is a whole subtitle line, so a word highlight can't work from it. If the user picked TikTok or karaoke, offer to transcribe the audio instead, or use the YouTube style with their SRT.

Keep each transcript's timestamps relative to its own source file.

### 4. Place the Official Caption Element

Follow official `remotion-captions/display-captions.md`:

- Install `@remotion/captions` with `npx remotion add @remotion/captions` if needed.
- Copy the element for the chosen style into the project from `https://www.remotion.dev/elements/captions/<element>.md`: Popping Word Captions for TikTok, Word Highlight Captions for karaoke, Basic Captions for YouTube and minimal.
- Put **one element per captioned clip, inside that clip's own `<Sequence>`** next to its `<Audio>`/`<Video>`. Don't add one global caption layer over the whole composition.
- **Inline the caption array** in the `captions` prop so the Studio Caption editor can write back.

### 5. Customize Appearance

Apply the preset from the `captions-workflow` rule, then offer these options. Change them through the element's `width`, `style` and `combineTokensWithinMilliseconds` props, or the style constants at the top of the copied file:

- **Position**: top (10%), center (50%), bottom (15-25% on vertical, to stay clear of platform UI). See the safe-zone table in the rule.
- **Font size**: Small (40px), Medium (56px), Large (72px) at 1080 wide
- **Highlight color**: Yellow (#FFD700), Cyan (#00FFFF), Green (#00FF88), custom
- **Background**: None, semi-transparent box
- **Font**: Inter, Poppins, or whatever the project uses (load it as official `remotion-markup` google-fonts.md shows)
- **Words per page**: `combineTokensWithinMilliseconds` (lower = fewer words per page)

Any extra animation uses inline `interpolate()` in `style` with the `scale`/`translate` properties. Never use CSS `transition` or `animation`; they don't render.

### 6. Check in the Preview

Tell the user to scrub the captions in the open Studio. Common adjustments:
- Text too small/large on mobile? → Adjust font size
- Words changing too fast? → Increase `combineTokensWithinMilliseconds`
- Wrong timing? → Check that the captions sit in the same sequence as their audio, and that timestamps weren't offset
- Overlapping with visuals or platform UI? → Change position (top vs bottom)
- Wording mistakes? → Fix them in the Studio Caption editor, or edit the inlined array

Don't render unless the user asks for an MP4.
