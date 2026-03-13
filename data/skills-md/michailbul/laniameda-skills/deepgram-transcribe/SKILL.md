---
name: deepgram-transcribe
description: >
  Transcribe audio files (ogg/mp3/wav/m4a/webm) using the Deepgram Nova-2 API.
  Use when the user sends a voice message or asks to transcribe audio.
metadata:
  requires:
    env:
      - DEEPGRAM_API_KEY
---

# deepgram-transcribe

Transcribe audio via Deepgram Nova-2.

## API Key
Set env var: `DEEPGRAM_API_KEY`

## Usage

### Transcribe a local file
```bash
FILE=/path/to/audio.ogg

# content-type guess
EXT="${FILE##*.}"
case "$EXT" in
  ogg) CT="audio/ogg" ;;
  mp3) CT="audio/mpeg" ;;
  wav) CT="audio/wav" ;;
  m4a) CT="audio/mp4" ;;
  webm) CT="audio/webm" ;;
  *) CT="audio/ogg" ;;
esac

curl -s -X POST \
  "https://api.deepgram.com/v1/listen?model=nova-2&punctuate=true&smart_format=true" \
  -H "Authorization: Token $DEEPGRAM_API_KEY" \
  -H "Content-Type: $CT" \
  --data-binary @"$FILE" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['results']['channels'][0]['alternatives'][0]['transcript'])"
```

### Notes
- For non-English audio, add `&language=xx` (e.g. `language=ru`).
- If transcript is empty, try removing `language` to auto-detect.
