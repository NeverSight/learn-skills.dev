---
name: papercut-voice
description: Voice a papercut reel and time it to the picture. Three paths, local Qwen3-TTS, your own recording or another TTS, or a placeholder voice. Covers delivery rules, voice.json, captions and scene timing. Use for "set up the voice", "re-voice this", "time the script".
---

# Papercut voice

Every later stage needs two things in the narration folder: `voice/final_narrator/<id>.wav` (one WAV per script line) and `timing_narrator.js` (a start and end for every word). This skill produces them by one of three paths, then builds the captions and the scene plan. The full reference for the scripts is `library/voice/README.md`.

## Preflight

- Library: `$PAPERCUT_LIB`, else the `PAPERCUT_LIB=` line in `~/.config/papercut-explainer/config.env`, else ask once. Export it, and `. "$PAPERCUT_LIB/env.sh"` loads `ASR_PY`, `QWEN_TTS_PY` and the other config values into the shell.
- A scaffolded project (`papercut-build`, step 1) with `narration/script.json` and `papercut/episode.json` holding `scenes`. `new_episode.sh` copies `build_timing.py` into `narration/`.
- If the user already has a TTS installed, use it as it is and don't rebuild it (path B, or A if it is Qwen3-TTS). Ask once which one and where it runs. Otherwise ask which path, and say what it needs:

| Path | Needs | Install mode |
|---|---|---|
| A. Local Qwen3-TTS | the voice venv from `library/voice/setup_tts.sh` (model download 2.3-4.2 GB) | Full |
| B. Your own recording or another TTS | an ASR backend (mlx-whisper or faster-whisper) and librosa + numpy for the pitch pass, in the Python that `ASR_PY` and `QWEN_TTS_PY` name | Full, or those packages by hand |
| C. Placeholder | ffmpeg; macOS for `--say` | Standard |

If the path needs more than the install has, run `./install.sh --doctor` and hand over to `papercut-setup`. Without ASR, `build_timing.py` only estimates 2.75 words a second, so captions drift against real audio.

## Path A: local Qwen3-TTS

From the series folder:

```
cp $PAPERCUT_LIB/voice/voice.example.json voice/voice.json     # once per series; edit it
$PAPERCUT_LIB/voice/narrate.sh voice/voice.json episodes/NN-slug/narration
$PAPERCUT_LIB/voice/finalize.sh voice/voice.json episodes/NN-slug/narration episodes/NN-slug/narration/voice/takes/narrator [num.json]
```

- `voice.json`: `speaker` (CustomVoice: Aiden, Dylan, Eric, Ryan, Serena, Vivian, Sohee, Ono_anna, Uncle_fu) and `instruct`. Recommended: CustomVoice 1.7B, Ryan or Aiden, instruct *"friendly, natural, conversational, like telling a friend; clear pauses between sentences; stress the key word of each line"*. `takes_per_line` defaults to 3. `tempo` stays 1.0 (other values need `rubberband`). `qa_targets` set the pitch range and the ASR match (0.9).
- A script line can carry `tts` (respelled text for pronunciation; captions keep `text`) and its own `instruct`. `num.json` maps numerals to spoken words (`{"13,000": "thirteen thousand"}`) so ASR matching doesn't fail on digits.
- Run one TTS process at a time; the 1.7B model is memory-hungry.
- `finalize.sh` runs ASR and pitch on every take, picks one per line, trims, loudness-normalises to -16 LUFS, re-runs ASR on the finals and writes `timing_narrator.js`. After listening, put corrections in `voice/picks_override.json` (`{"l3_name": 2}`) and rerun with `SKIP_PICK=1`.
- Voice Design (describing a voice in words) is a Qwen3-TTS mode that `narrate.py` doesn't drive. Generate with it elsewhere and use path B.

## Path B: your own recording or another TTS

- Put one WAV per line in `voice/final_narrator/<id>.wav`, or raw takes as `voice/takes/narrator/<id>_<k>.wav` and run `finalize.sh` as above.
- For finished lines, transcribe them, write `voice/chosen_narrator.json` as `{id: "voice/final_narrator/<id>.wav"}`, then from `narration/`:

```
$ASR_PY $PAPERCUT_LIB/voice/asr.py voice/final_narrator/*.wav > voice/asr_narrator_final.json
CHOSEN=voice/chosen_narrator.json TIMING_OUT=timing_narrator.js python3 build_timing.py voice/asr_narrator_final.json
```

## Path C: placeholder

From the `narration/` folder:

```
python3 $PAPERCUT_LIB/tools/placeholder_vo.py [--wps 3.0] [--say [VOICE]]
```

It writes silent WAVs (or the macOS `say` voice with `--say`) and `timing_narrator.js` from `script.json` alone, spreading word times by word length. `--wps 3.5` to `4` approximates the target pace (default 3.0). The reel can be built and timed first and re-voiced later: swap the WAVs, rerun `finalize.sh`, rerun `build_vo.py`, and the word cues follow.

## Delivery rules

Delivery is human, unhurried and emphasised. The viewer must follow every line on the first listen.
- **Breathing room.** A real pause at every sentence end and between list beats ("Fine. Fine. Fine."). Start with 0.3-0.4 s between lines (`gap` in `episode.json`, default 0.22; `gaps` adds an extra beat after one named line) and judge by ear. Pauses go at sentence or clause boundaries only: a 0.2 s gap inside a phrase, such as "copied it, | by taking...", reads as lag. Use the 30 s ceiling for air instead of cutting pauses, and never slow the tempo to get it.
- **Emphasis.** The one or two words each line leans on (the number, the twist word, the verdict) come from the script's staging table. Pass them as a per-line `instruct`.
- **Tone.** Conversational and a little amused, not announcer energy. Questions sound like real questions, the catch line sounds curious, the CTA is warm. The narrator still doesn't joke; the picture does.
- **Clone model (no instructions).** With a clone voice (`ref_audio` + `ref_text`, Base model) the levers are the text and the take. Write the pauses into the punctuation (full stops between list beats, a short question as its own sentence). Generate several seeds of one continuous take (`SEED_BASE`, `takes_per_line`), pick the one with the most pitch movement on the target words and ASR 0.9 or better, and re-take a flat line alone (`ONLY=l4_peak`) and splice it at a sentence boundary. Only clone a voice you have the right to use.
- **Whole script at once** gives consistent prosody: generate one take, `split_take.py` cuts it per line, then set `"gap": 0` in `episode.json`. Per scene is fine if the user prefers.
- **Play the first three lines to the user before the full run**: `ONLY=l1_hook,l2_...,l3_... narrate.sh ...`.

## Captions and timing

From `papercut/`, once `episode.json` has `scenes`:

```
python3 $PAPERCUT_LIB/tools/build_vo.py     # public/vo/voiceover.wav, public/vo/captions.json, src/plan.json
python3 $PAPERCUT_LIB/tools/timing_md.py    # Timing section of STORYBOARD.md
```

`captions.json` is a Remotion `Caption[]`; scene boundaries come from the word timestamps; the composition length is `plan.json`'s `durationInFrames`. `build_vo.py` flags any scene under 1.2 s. With no library, transcribe the WAV with the Remotion captions skill (whisper.cpp) or any speech-to-text tool that returns word timestamps.

Captions are one torn tag per word, pages of 1-3 words, at 3.5-4 words a second (`../papercut-explainer/references/style-guide.md`, sections 11 and 13).

## Hand-off

Next is `papercut-build` (stubs, scenes, sound, render). It reads `src/plan.json` and the Timing section of `papercut/STORYBOARD.md`. Any later voice change reruns `build_vo.py` and `timing_md.py`; the scene cache then re-renders everything.
