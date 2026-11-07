---
name: create-typecast-shorts
description: Create a captioned 9:16 short or reel from one rights-cleared local video or image using Typecast narration, timestamp output, and ffmpeg. Use when a user asks to make a short-form video, reel, vertical video, narrated social clip, or Typecast-powered short from media they own or are authorized to use.
---

# Create Typecast Shorts

Create one 1080×1920 MP4 from a local video or image, Typecast narration, and timestamp-aligned subtitles.

## Boundaries

- Accept only an attached file or local file the user owns or is authorized to use.
- If rights are unclear, ask the user to confirm them before processing.
- Do not search for, download, scrape, or reuse third-party video, news, or social media.
- Do not remove logos, watermarks, attribution, or embedded subtitles to conceal a source.
- Do not upload or publish the result. Return local artifacts for user review.
- Do not print, log, or place a Typecast API key in chat, commands, scripts, or output files.
- Support one background video or image per run. Ask the user to choose one when several are provided.

## Workflow

### 1. Confirm inputs

Collect:

- Local media path
- Topic or finished script
- Language
- Target duration; default to 45–60 seconds
- Typecast voice ID, or permission to open the interactive voice picker
- Output directory inside the current workspace

Use these defaults unless the user specifies otherwise:

- 1080×1920, 30 fps
- Center crop to fill the frame
- Discard source audio
- White bottom-centered subtitles with a black outline

Confirm media rights, the final script, and the voice before making the paid TTS request.

### 2. Check the environment

Run:

```bash
command -v cast
command -v ffmpeg
command -v ffprobe
cast --help
ffmpeg -filters 2>/dev/null | grep subtitles
```

If a command or the ffmpeg `subtitles` filter is missing, explain the missing dependency. Install it only with user approval.

After installing cast with Go, add it to the current shell without hardcoding the user's home directory:

```bash
export PATH="$(go env GOPATH)/bin:$PATH"
```

For cast installation, use the official options:

```bash
brew install neosapience/tap/cast
# or
go install github.com/neosapience/cast@latest
```

The tempo/silence example below requires Cast v1.0.10 or later. Check `cast --help` for `--remove-silence-ms`; if unavailable, update Cast before synthesis instead of omitting the option.

Authenticate with `cast login` so the key is entered in its own prompt. Never ask the user to paste the key into chat.

### 3. Create a clean work directory

Create a new, explicit directory inside the current workspace. Do not overwrite an existing output.

Keep these artifacts:

```text
script.txt
script-tts.txt
narration.wav
captions.srt
preview.mp4
final.mp4
```

Work from this directory while rendering so `captions.srt` does not require platform-specific path escaping.

### 4. Prepare the script

If the user supplied only a topic, draft a concise script with:

1. Hook
2. Main point
3. Supporting detail
4. Closing line

Save the approved text as `script.txt`.

Create `script-tts.txt` separately. Change only pronunciations that TTS may misread, such as numbers, abbreviations, URLs, symbols, or mixed-language terms. Preserve the meaning and never overwrite `script.txt`.

### 5. Select a voice and generate audio plus captions

If no voice ID was provided, run:

```bash
cast voices pick
```

After approval, generate narration and SRT together. This example uses a slightly faster short-form pace (`--tempo 1.1`) and keeps up to 300 ms of each detected silence (`--remove-silence-ms 300`); choose tempo to match the user’s request (the normal default is `1.0`).

```bash
cast "$(cat script-tts.txt)" \
  --voice-id VOICE_ID \
  --language LANGUAGE_CODE \
  --tempo 1.1 \
  --remove-silence-ms 300 \
  --format wav \
  --out narration.wav \
  --timestamp-out captions.srt \
  --timestamp-format srt
```

Use ISO 639-3 language codes such as `kor`, `eng`, or `jpn`. For Japanese or Chinese, cast automatically selects character-level alignment; use the latest cast release if that behavior is unavailable.

`--remove-silence-ms` is the silence duration to keep, not the amount to subtract: use an integer from `0` to `1000`; `0` removes detected silence and omission disables duration-based removal. Generate the audio and captions in the same request. Returned timestamps already match the tempo-adjusted, silence-processed audio; do not subtract silence durations from them or run ffmpeg silence removal/tempo changes on narration afterward, as that invalidates caption timing.

Do not fall back to Whisper merely to create timestamps. Typecast captions already returns aligned audio and subtitles without another model or dependency.

### 6. Inspect the source

Run:

```bash
ffprobe -v error -show_entries stream=codec_type,width,height,duration \
  -of default=noprint_wrappers=1 "SOURCE_PATH"
```

Use the video command for a video source and the image command for a still image. Quote every user-provided path.

### 7. Render a 15-second preview

For a video:

```bash
ffmpeg -y -stream_loop -1 -i "SOURCE_PATH" -i narration.wav \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,subtitles=captions.srt:force_style='FontSize=16,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=1.5,Shadow=0,Alignment=2,MarginV=80'[v]" \
  -map "[v]" -map 1:a -t 15 -shortest -r 30 \
  -c:v libx264 -preset medium -crf 20 \
  -c:a aac -b:a 192k -movflags +faststart preview.mp4
```

For an image:

```bash
ffmpeg -y -loop 1 -framerate 30 -i "SOURCE_PATH" -i narration.wav \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,subtitles=captions.srt:force_style='FontSize=16,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=1.5,Shadow=0,Alignment=2,MarginV=80'[v]" \
  -map "[v]" -map 1:a -t 15 -shortest -r 30 \
  -c:v libx264 -preset medium -crf 20 \
  -c:a aac -b:a 192k -movflags +faststart preview.mp4
```

Show the preview to the user. Check framing, subtitle readability, pronunciation, and timing before the full render.

If center crop cuts off important content, replace the scale and crop portion with:

```text
scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black
```

### 8. Render and verify the final video

After preview approval, rerun the matching command without `-t 15`, add `-shortest`, and write `final.mp4`.

Verify:

```bash
ffprobe -v error \
  -show_entries stream=codec_name,width,height -show_entries format=duration,size \
  -of default=noprint_wrappers=1 final.mp4
```

Require:

- 1080×1920 video
- H.264 video and AAC audio
- Non-zero duration and size
- Narration and subtitles ending with the video

Return the output directory and artifact list. Remind the user to review the complete video before publishing it themselves.

## Optional feedback after the task

Finish the requested short and report the actual result first; failed or stopped attempts also qualify. Then offer one short optional Typecast API/docs interview per session, unless the user has already declined or been invited. Explain that it is anonymous, with no reward or account connection, and that a reviewed summary is sent only after separate transmission approval. Stop and wait for participation consent. Follow https://typecast.ai/docs/agent-interview.md before asking questions or preparing a submission, using interview `source=shorts`. Do not search previous sessions or personal files automatically, submit raw scripts/media/logs/keys, or require feedback to receive the video. Keep any TTS integration attribution unchanged; it is separate from interview source.

## Failure handling

- For 401 or 403 from cast, re-run `cast login` and verify the Global API plan without exposing the key.
- For 402 or 429, report the billing or rate-limit response; do not retry repeatedly.
- If timestamp flags are unavailable, update cast instead of adding a parallel transcription stack.
- If ffmpeg cannot load subtitles, use an ffmpeg build with libass.
- If rendering fails, preserve all existing artifacts and rerun only the failed step.
