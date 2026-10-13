---
name: video-translate
description: Translates a talking-head take (or a finished video) into another language with the creator's own cloned voice through ElevenLabs Dubbing, using their ElevenLabs API key - sets the key up, trims the take first so no stutter is paid for, estimates the minutes, sends it after a yes, waits, lays the dubbed voice back on the image, then hands the translated take to video-edit for captions in the new language. Use when the user says translate, dub, dubbing, English version, Spanish version, traduis, version anglaise, doublage, ElevenLabs, or wants a second account in another language.
argument-hint: "<take, slug or mp4> <target language> [from <source language>]"
allowed-tools: Bash(ffmpeg *) Bash(ffprobe *)
---

# Video Translate

One take in, the same take in another language out, in the creator's own voice (ElevenLabs clones it from the take itself). The image stays the original: no lip-sync. Then `/video-edit` edits the translated take like any other, with captions in the new language.

Talk to them in their language. `<slug>`: the take's slug; `<lang>`: the target language code (`en`, `es`, `fr`, `de`, `pt`, `it`, `ja`...), `<from>`: the source one.

## 1. The ElevenLabs key (once)

The key lives in `video-agent/.env`, never in a chat message, a script or a commit:

```bash
grep -c ELEVENLABS_API_KEY video-agent/.env 2>/dev/null
```

`0` or no file:

1. They create a key at [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys) (an ElevenLabs account; dubbing uses the credits of their plan, the free plan adds a watermark).
2. They paste it into `video-agent/.env` themselves, as one line: `ELEVENLABS_API_KEY=sk_...`. Offer to create the empty file and open it. Never ask them to paste the key in the chat; if they do anyway, write it to the file and tell them they can regenerate it.
3. `video-agent/.env` must be in the project's `.gitignore` (add the line `video-agent/.env` if it isn't).

Every command below loads it with `set -a; . video-agent/.env; set +a` and never prints it.

## 2. What to translate

Translate the **take**, not a finished video: a finished video has captions burned in the old language. Then video-edit cuts, captions and times everything on the new voice.

- **A take already edited** (`video-agent/edits/<slug>/edit.json` exists): send only the kept parts, so no silence, stutter or retake is paid for. Make the plain cut with video-edit's ranges (from `video-agent/studio/`):
  ```bash
  SEL=$(node -e 'const e=require("./public/<slug>.edit.json");console.log(e.ranges.map(r=>`between(t,${r.fromMs/1000},${r.toMs/1000})`).join("+"))')
  ffmpeg -y -i public/<slug>.mp4 -vf "select='$SEL',setpts=N/FRAME_RATE/TB" -af "aselect='$SEL',asetpts=N/SR/TB" -c:v libx264 -crf 18 -c:a aac -b:a 192k ../.tmp/<slug>-cut.mp4
  ```
  The source is `video-agent/.tmp/<slug>-cut.mp4`.
- **A raw take**: offer to run `/video-edit` up to its cut list first (steps 1 to 4) for the same reason. In a hurry: send the raw take as it is.

## 3. Estimate, then send

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 "<source>"
```

Show one line and wait for a yes: `Dub <slug> fr → en · 0:52 of video · billed on your ElevenLabs credits for about 1 minute (check your plan's dubbing price on elevenlabs.io/pricing) · no lip-sync`.

Then send it (about 10 s per minute of upload):

```bash
mkdir -p video-agent/.tmp
set -a; . video-agent/.env; set +a
curl -sS --fail-with-body -X POST https://api.elevenlabs.io/v1/dubbing \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F "file=@<source>" -F "target_lang=<lang>" -F "source_lang=<from or auto>" \
  -F "num_speakers=1" -F "watermark=false" -F "name=<slug>-<lang>" \
  > video-agent/.tmp/<slug>-<lang>.job.json
cat video-agent/.tmp/<slug>-<lang>.job.json
```

It returns `{"dubbing_id": "...", "expected_duration_sec": ...}`. Keep the id: if anything stops, polling again with it costs nothing. A 401 is a wrong key; a 402 or "quota" means no credits left on their plan; `watermark` refused: send it again without that field.

## 4. Wait, then download

Poll every 15 s until `status` is `dubbed` (`failed`: show the error and stop). Usually 1 to 5 minutes for a short; run it in the background:

```bash
set -a; . video-agent/.env; set +a
curl -sS --fail-with-body -H "xi-api-key: $ELEVENLABS_API_KEY" https://api.elevenlabs.io/v1/dubbing/<dubbing_id>
```

Then the dubbed file:

```bash
set -a; . video-agent/.env; set +a
curl -sS --fail-with-body -H "xi-api-key: $ELEVENLABS_API_KEY" -o video-agent/.tmp/<slug>-<lang>.dub https://api.elevenlabs.io/v1/dubbing/<dubbing_id>/audio/<lang>
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 video-agent/.tmp/<slug>-<lang>.dub
```

- It has a `video` stream: it is already the dubbed video, move it to `video-agent/takes/<slug>-<lang>.mp4`.
- Audio only: lay it back on the original image:
  ```bash
  ffmpeg -y -i "<source>" -i video-agent/.tmp/<slug>-<lang>.dub -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest video-agent/takes/<slug>-<lang>.mp4
  ```

Check it: same length as the source (within a second). Then ask them to listen to the first 10 seconds before editing (voice, accent, a wrong word).

## 5. Edit the translated take

`/video-edit <slug>-<lang>`, and tell it:

- **The language changed**: in `video-agent/studio/whisper-config.mjs`, set `WHISPER_LANG` to `<lang>` for this transcription (English: `WHISPER_MODEL = "medium.en"` works best; any other language: `"medium"`), and put it back after. The hook card, callouts and `post.md` are written in `<lang>`.
- **Same edit as the original** when there is one: same hook card and callouts (translated), placed on the matching words of the new transcript.
- The ask (CTA) in `<lang>`: ask them once for its translation, or translate the one in voice.md and show it.

Name everything `<slug>-<lang>` so both versions sit side by side. Then `/video-publish <slug>-<lang>` on the account for that language.

Delete `video-agent/.tmp/<slug>-*` at the end, except the job file if they may want to download the dub again.

## Honest limits

- No lip-sync: the lips move in the original language. Fine with a lot of motion, a small face or quick cuts; noticeable on a long close-up.
- The voice clone comes from the take: a noisy take or music under the voice gives a worse clone.
- Machine translation: names, jargon and jokes can come out wrong. Ask them (or a native speaker) to check the transcript of the dubbed take before posting.
- Dubbing costs ElevenLabs credits per minute, and the price depends on their plan. Trimming the take first is the cheapest saving.
