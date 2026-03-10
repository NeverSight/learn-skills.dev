---
name: translate-video
description: "Translate video subtitles to any language with native-quality refinement. Full pipeline: transcribe → translate → refine → embed RTL-safe subtitles. Use for: translate video, תרגם סרטון, video translation, foreign subtitles, Hebrew subtitles, translated captions."
argument-hint: "[video-path] [target-language]"
---

# Translate Video

End-to-end video translation pipeline. Takes a video, transcribes it, translates to target language with native-speaker refinement, and burns subtitles onto the video.

## Usage

```
/translate-video /path/to/video.mp4 he
/translate-video /path/to/video.mp4 ar
/translate-video /path/to/video.mp4 es
```

**Arguments:**
- `$1` - Path to video file (required)
- `$2` - Target language code (default: `he`). Codes: he, ar, es, fr, de, ru, zh, ja, etc.

## Pipeline

### Step 1: Transcribe (via `/transcribe` skill)

Extract audio if video is too large (>25MB audio), then transcribe:

```bash
# Extract audio if needed (reduces upload size)
ffmpeg -i "$VIDEO" -vn -acodec libmp3lame -ab 128k "$AUDIO_PATH" -y

# Transcribe using the transcribe skill's script
cd ~/.claude/skills/transcribe/scripts && [ -d node_modules ] || npm install --silent
npx ts-node transcribe.ts -i "$INPUT" -o "$SRT_PATH"
```

This generates:
- `{basename}.srt` - Raw SRT file
- `{basename}.md` - Readable text

### Step 2: Translate

Read the `.md` file to understand full context, then translate the `.srt` file.

**Translation rules:**
- Translate ALL subtitle text entries, preserving SRT index numbers and timestamps exactly
- Do NOT translate proper nouns (product names, people's names, brand names)
- Keep technical terms that are commonly used untranslated in the target language (API, CLI, SaaS, etc.)
- Adapt idioms and expressions to natural equivalents in the target language
- Match the speaker's register (casual/formal) in the translation

### Step 3: Semantic Refinement

The raw transcription chunks by time, not meaning. Regroup for the target language:

1. **Read all translated text** as continuous prose
2. **Identify natural sentence/clause boundaries** in the target language
3. **Regroup words** into semantically coherent subtitle entries (max 2 lines per entry, ~40 chars per line)
4. **Adjust timestamps**: each entry starts at first word's original time, ends at last word's time
5. **Merge fragmented entries** - aim for 150-250 entries for a ~15min video (vs 500-600 raw)
6. **Native speaker test** - read each subtitle aloud. If it sounds awkward, rephrase

**Quality checklist:**
- [ ] No sentence split mid-clause
- [ ] No orphaned words (single word carrying over from previous thought)
- [ ] Punctuation at natural break points
- [ ] Reading pace is comfortable (not too much text per subtitle)
- [ ] Sounds like a native speaker wrote it, not a translation

### Step 4: Embed Subtitles (via `/embed-subtitles` skill)

**RTL is handled automatically** by the `embed-subtitles` skill - it detects RTL content and applies Unicode directional marks before embedding. No need to handle RTL here.

Burn the translated SRT onto the video:

```bash
cd ~/.claude/skills/embed-subtitles/scripts
npx ts-node embed-subtitles.ts \
  -i "$VIDEO" \
  -s "$TRANSLATED_SRT" \
  -o "$OUTPUT" \
  --font-size 24 --margin 30
```

Or directly with FFmpeg:

```bash
ffmpeg -i "$VIDEO" \
  -vf "subtitles='$TRANSLATED_SRT':force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=1,Alignment=2,MarginV=30'" \
  -c:v libx264 -preset fast -crf 23 -c:a copy \
  "$OUTPUT" -y
```

### Step 5: Open Result

```bash
open "$OUTPUT"  # macOS
```

## Output Files

All files saved next to the original video:

| File | Description |
|------|-------------|
| `{name}.srt` | Original language SRT |
| `{name}.md` | Original readable transcript |
| `{name}_{lang}.srt` | Translated + refined SRT (with RTL marks if applicable) |
| `{name}_{lang}_subtitled.mp4` | Final video with burned-in subtitles |

## Language Codes

| Code | Language | RTL? |
|------|----------|------|
| `he` | Hebrew | Yes |
| `ar` | Arabic | Yes |
| `fa` | Farsi | Yes |
| `en` | English | No |
| `es` | Spanish | No |
| `fr` | French | No |
| `de` | German | No |
| `ru` | Russian | No |
| `zh` | Chinese | No |
| `ja` | Japanese | No |
| `pt` | Portuguese | No |
| `it` | Italian | No |

## Examples

**Hebrew translation (most common use):**
```
/translate-video ~/Desktop/tutorial.mp4 he
```
Produces: `tutorial_he.srt` + `tutorial_he_subtitled.mp4`

**Spanish translation:**
```
/translate-video ~/Desktop/talk.mp4 es
```

**Default (Hebrew):**
```
/translate-video ~/Desktop/video.mp4
```
