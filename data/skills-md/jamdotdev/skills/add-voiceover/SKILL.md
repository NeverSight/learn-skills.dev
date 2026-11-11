---
name: add-voiceover
description: "Add a spoken voiceover to a video: write the script for the ear, voice it line by line with ElevenLabs, Kokoro (a free local model) or your own text-to-speech command, and lay each line under the moment it describes, with a subtitle file. Use when the user asks to add narration, a voiceover, a voice or text-to-speech to a screen recording, demo video or walkthrough, to re-voice a video with another voice, or asks why a generated voiceover sounds robotic, echoes or drifts out of sync."
---

# Add a voiceover

A good voiceover sounds like a colleague showing you something: short spoken lines, each one landing on the moment it talks about. Most bad ones come from a script written for reading, one long take of text-to-speech laid over the whole video, or an expressive voice with unstable settings.

Needs `ffmpeg` and Node 22 or later. The script is `scripts/voiceover.mjs` in this skill's folder and needs no packages.

## 1. Pick the voice

The script takes the first voice that is set up:

1. `VOICEOVER_TTS`: the team's own command. `{out}` is the `.wav` file to write and `{text}` the line, also sent on stdin. Quote an argument that holds spaces (`--voice="Jane Doe"`); backslash escapes are not read.
2. `ELEVENLABS_API_KEY`: ElevenLabs. Defaults: model `eleven_v4`, voice `iP95p4xoKVk53GoZ742B`, stability 0.5, similarity 0.75, speaker boost on, and each line voiced with the two lines around it as context so the intonation carries across. `ELEVENLABS_VOICE_ID` and `ELEVENLABS_MODEL_ID` change them; for a female voice use River, `SAz9YHcvj6GT2YYXdXww`. v4 has no speed or style setting: pace it with punctuation and line length.
3. Kokoro, a free local model, once installed (`~/.cache/kokoro` holds its files) and Python 3 and `uv` are on PATH. Voice `am_michael`; `KOKORO_VOICE` picks another (`af_heart`, `bf_emma`, `bm_george`).
4. macOS `say`, for drafts only.

When none of the first three is set up, ask the user once which they want:

- **ElevenLabs**: they set `ELEVENLABS_API_KEY` in their own shell. Never ask them to paste the key into the chat or a file. It bills per character, so rehearse with `ELEVENLABS_MODEL_ID=eleven_flash_v2_5` or Kokoro and voice the final cut with the default model.
- **Kokoro**: free and local, a one-time download of about 340 MB. On a yes: `python3 <skill-dir>/scripts/kokoro.py --install`.
- **The OS voice**: nothing to set up, sounds robotic.

In CI or with no one to ask, use what is set up and never start the download.

## 2. Write the script for the ear

Write `lines.json`, one entry per spoken line:

```json
[
  {"say": "Hey, here's the new checkout flow, end to end.", "at": 0.5},
  {"say": "I'll add a jar,", "at": 3.2},
  {"say": "and place the order.", "at": 6.8},
  {"say": "And it fails. Payment provider timeout.", "at": 9.1}
]
```

- One idea per line, 4 to 14 words. Split a sentence across the actions it describes: "I'll add a jar," then "go to checkout," then "and place the order."
- Say what the viewer should notice, not what the mouse does. "Every item lands in the list" beats "I click the input and type".
- Talk, don't announce: contractions, "so", "here's", first person. No sales lines.
- Tell a story in three parts: what this is, what happens, what it means. The last line lands the result.
- Write numbers and symbols the way they are said: "five-oh-three", "two seconds", "dot env". The voice reads "503" as "five hundred three".
- No captions burned into the video unless the user asks. The script writes `voiceover.vtt` for players that show subtitles.

## 3. Time each line

`at` is the second the line starts. Start it about half a second before the action it names, so the word and the click land together.

- **From a recording you just made:** use the times the recorder wrote. `record-demo` writes them to `narration.json` in this format.
- **An existing video:** list the moments the picture changes and look at a frame from each:
  ```bash
  ffmpeg -i in.mp4 -vf "select='gt(scene,0.08)',showinfo" -f null - 2>&1 | grep -o 'pts_time:[0-9.]*'
  ffmpeg -v error -ss 9.1 -i in.mp4 -frames:v 1 at-9.1.png
  ```
- **No picture to match:** leave `at` out and the lines follow each other with a short breath.

To pace a recording by the voice instead, voice the lines first with no `--video`, and pass the `lines.json` it writes (each line with its `seconds`) to the recorder.

## 4. Voice and mix

```bash
node <skill-dir>/scripts/voiceover.mjs lines.json ./voiceover --video in.mp4
```

Output in `./voiceover`: `voiced.mp4` (the picture untouched, the narration raised by one fixed gain so it peaks at -1 dB; a video with its own sound keeps it, and both are lowered together if the mix would pass -1 dB), `narration.wav`, `lines.json` with each line's final `at` and `seconds`, one `.wav` per line, and `voiceover.vtt`. Each line is cached by its text and voice, so after editing one line a re-run voices only that line (with ElevenLabs, also the two on each side, which it hears as context), and switching the voice re-voices everything.

A line that would talk over the one before starts late, and the script prints which. Shorten one of the two lines, or move the later one, and run it again.

## 5. Check before you share

1. Read the warnings. Late lines and narration cut at the end of the video both mean the script is too long for the picture.
2. Loudness: `ffmpeg -i voiceover/voiced.mp4 -af volumedetect -f null - 2>&1 | grep -E 'mean|max'`. Expect a max of -1 dB and a mean between -18 and -24 dB. Never level the voice with `loudnorm`, a compressor or other dynamic filters: they raise each word's tail and the voice sounds like it echoes.
3. Sync: extract a frame one second after each line's `at` and check it shows what the line names.
4. Give the user one line's `.wav` to listen to before they watch the whole video.

An echo comes from a dynamic leveler in the mix: compare one line's `.wav` with the same moment in the video, and if only the video echoes, remove the filter. A laugh, a pitch jump between lines, or a voice that speeds up comes from low stability or an expressive character voice: keep the default settings and pick a narration voice. Never fix sync by stretching the audio; move the line or re-record.
