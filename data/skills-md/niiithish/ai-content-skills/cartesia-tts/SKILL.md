---
name: cartesia-tts
description: >
  Text to speech with Cartesia (Sonic 3.6, the latest model) from the `cartesia` command: list and
  download voice samples, audition a script's first lines in a few voices, and read a whole script
  into one WAV with Cartesia's own word timestamps (OUT.words.json, the layout `transcribe` uses) and
  each line's start and end. Always asks the user first: the tool, the voice, the speed and the
  emotion are the user's choice. Use for any TTS, voiceover, scratch read, voice sample or "read this
  out", and before planning a video so its shots are timed from a real read.
---

# Cartesia TTS

Every voice the agent makes goes through `cartesia` (`~/.local/bin/cartesia`, which runs `scripts/cartesia.py`). It uses the model alias `sonic-3.6`, the latest stable model. Use `--model sonic-3.6-2026-08-27` to pin the snapshot so a re-read sounds the same.

**Key:** the key is read from `~/.config/cartesia/api_key` (folder 700, file 600), or from `$CARTESIA_API_KEY`. Never print it, never put it in a project file or a commit, and never paste it into a command line.

## Ask first, then make

Never make a voice before the user has picked it. Before any read, ask in one message:

1. **Tool.** "Cartesia (default), or another (ElevenLabs, the client's own recording)?" If it's another tool, stop here and follow the user.
2. **Voice.** Suggest 3–5 voices that fit the brief, picked from `cartesia voices`. Name the first one as your pick. Download their samples so the user can play them (see the commands below), and give the folder's full path. The user can also paste a voice id from play.cartesia.ai, including a cloned voice (`cartesia voices --mine`).
3. **Speed** (0.6–1.5, default 1.0). The user's ads usually end up at 1.1x in the edit, so ask whether to read at 1.0 and speed up later, or read faster now.
4. **Emotion**, optional. The six most reliable are neutral, calm, content, sad, angry and scared (`cartesia emotions`). Inline tags change it mid-script: `<emotion value="sad"/>`, `<speed ratio="0.9"/>`, `<volume ratio="1.2"/>`, `[laughter]`.

When the user wants to hear the choices on their own script, run `audition` on the first two lines in each candidate voice and wait for their pick. Only then read the whole script.

## Commands

```bash
cartesia voices warm narrator --gender feminine --limit 10 --previews voiceover/voices   # list + samples as mp3
cartesia audition --script voiceover/script.md --voices ID1,ID2,ID3 --out voiceover/audition
cartesia say --script voiceover/script.md --voice ID --speed 1.0 --out voiceover/recording.wav
cartesia say "One line to test." --voice ID --out /tmp/x.wav
cartesia emotions ; cartesia models
```

`say` writes:

- `recording.wav`: 44.1 kHz mono, one line after another with `--gap` seconds of silence between them (0.4 by default).
- `recording.words.json`: Cartesia's own word times, as `[{word, start, end}]`. This is exact for a TTS read, so there's no need to transcribe it.
- `recording.lines.json`: each script line's start and end.
- `recording.voice.json`: the voice, model, speed and emotion used. Name these in the plan.

Each line is cached in `recording.lines/`. When one line of the script changes, a rerun reads only that line and rebuilds the rest from the cache.

## For a video plan

The voice comes first. Write `voiceover/script.md` (one spoken line per row), ask as above, then read it to `voiceover/recording.wav`. After that, `plan.py voiceover <video>` (video-plan) times every line from `recording.words.json`, and the shot table and clip lengths come from those times. A read saved anywhere else isn't picked up by the plan.

## Notes

- Voice samples come from the API as raw 16-bit 44.1 kHz PCM; the script turns them into mp3. Not every voice has a sample. For one without, use `audition`.
- `files.cartesia.ai` refuses Python's default user agent with a 403, so the script sends its own user agent.
- Docs: https://docs.cartesia.ai (API version `2026-08-14`, `/tts/sse` with `add_timestamps`, `/voices`).
