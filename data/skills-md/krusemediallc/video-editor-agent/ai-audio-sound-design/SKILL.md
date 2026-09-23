---
name: ai-audio-sound-design
description: Rebuild the audio of an AI-generated video (Arcads / AI actors / UGC-gen / any clip whose voices sound like sterile studio AI) so every scene sounds like it was really filmed in the location shown — location-matched ambience beds, room-matched convolution reverb, outdoor distance treatment, censor bleeps over swears, removal of the AI high-frequency watermark whine, and a social loudness master, all with the video stream untouched. Use whenever someone says clips "sound AI / fake / sterile / like a voiceover", asks to "add ambient sounds / background noise", "make it sound like the location they're in", "add reverb to match the room", "bleep the swears / curse words", or hands over AI-actor footage for an audio pass — even if they never say "sound design". Also for revision rounds on an existing pass ("make the lawnmower louder", "add a car driving by", "make it sound like it's outside"). NOT for captions (embedded-captions), cutting footage (reel-recut), or full branded motion-graphic edits (branded-ad-edit).
---

# AI Audio Sound Design

AI-generated clips have three tells that scream "fake" before a viewer can articulate why:
**dead silence between words** (real rooms are never silent), **dry studio voices in visibly
reverberant spaces** (a bathroom that doesn't sound like a bathroom), and a **tonal watermark
whine at 13–16 kHz** that every Arcads-style generator leaves in the track. This skill fixes
all three per scene, plus broadcast-style censor bleeps, without touching a single video frame.

Proven on a real 10-scene AI-actor ad (5 approved client revision rounds). The
engine is [scripts/build_mix.py](scripts/build_mix.py); per-location recipes and level targets
are in [references/acoustics.md](references/acoustics.md) — read it before filling in the
scene table.

## What ships

- `out/<name>-vN.mp4` — video stream **copied bit-exact** (`-c:v copy`), audio rebuilt (AAC 256k).
- Stems (`-dialog`, `-amb`, `-bleeps` wavs) — every level decision gets measured, not guessed.
- Review canvas per the `video-review-canvas` skill; new version = new filename, same slug.
- Deliver the finished file **next to the source** (same folder or cloud location it came from).

## Pipeline

### 1. Ingest and map the scenes

Download the source to local disk first if it lives in cloud storage. Then:

```bash
ffmpeg -y -i src.mp4 -vn -ac 2 -ar 48000 work/master-audio.wav
ffmpeg -i src.mp4 -vf "select='gt(scene,0.25)',metadata=print" -an -f null - 2>&1 | grep pts_time
```

Scene-cut `pts_time`s are your ambience cut points — **ambience hard-cuts with the picture**
(short 40–60 ms edge fades only). That's how real location audio behaves at an edit, and the
abrupt texture change is itself a cue that the location changed. Extract one midpoint frame per
segment (`-vf scale=360:-1`) and *look at them*: the visible location decides the ambience bed,
the reverb size, and the treatment. A ~0.25-score cut may be a punch-in, not a new location —
two adjacent segments showing the same room share one bed.

### 2. Transcribe and lock the censor list

Whisper (`whisper-1`, `verbose_json`, word timestamps) on the master audio. Pick the words to
bleep with the user's actual instruction in hand — e.g. one client's brief was swears **plus
"freaking"**, and explicitly *not* "I swear to God"; don't silently widen or narrow the list,
flag judgment calls on the canvas instead.

Then verify every span before trusting it: slice ±0.7 s around each word, re-transcribe the
slice, and require the two passes to agree within ~50 ms. Whisper word *starts* run 100–200 ms
late on this kind of footage, so pad each confirmed span **−0.10 s at the start, +0.06 s at the
end**. A zero-duration word in the full pass (e.g. `using 11.62–11.62`) means collapsed
timestamps — the isolated slice is the truth.

### 3. Generate the ambience kit

Use the ElevenLabs kit runner that already audits and retries:

```bash
# ELEVENLABS_API_KEY from the environment or a .env at the repo root
python3 .claude/skills/branded-ad-edit/scripts/generate-sfx.py kit.json work/ambience
```

Prompt patterns, per-location bed recipes, and the dud/mosquito-whine gotchas are in
[references/acoustics.md](references/acoustics.md). Rules that always apply:

- End every prompt with **"steady, no voices"** — beds must be loopable texture, not events.
- Bed duration = longest scene using it + ~1.5 s; the engine loops shorter beds.
- One-shot events (a car passing, a printer run) are separate generations from beds.
- Set the kit's `min_peak_db` to −35: room tones are *supposed* to be quiet, and the default
  dud threshold would regenerate them forever.

### 4. Build the mix

Copy [scripts/build_mix.py](scripts/build_mix.py) into the project's `work/` and edit only the
tables at the top: `SCENES` (one row per segment: bed, gain, RT60, damping, wet level, predelay,
highpass), `LAYERS` (extra beds on top — how you add an element without touching a bed the
client already approved), `EVENTS` (timed one-shots, no looping), `AMB_FX` (outdoor distance
treatment per source), `BLEEPS`, `AMB_MASTER_DB` (global ambience trim).

The chain order inside the engine is load-bearing — keep it:

1. **Mute censored words BEFORE the reverb convolution.** The swear then never enters the
   reverb, so nothing of it can leak out of the tail. The tail of the *previous* word ringing
   under the bleep tone is correct — real broadcast censoring sounds exactly like that.
2. Highpass (80–100 Hz) then **steep lowpass at 13 kHz + a final FFT brick-wall (cosine edge
   13.0→13.5 kHz) on the whole mix.** This kills the AI watermark whine. A butterworth alone
   does NOT: slopes are dB per *octave*, and 13→15.6 kHz is only a quarter octave (~13 dB off a
   40 dB tone). Verify the kill: max residual above 13.6 kHz should sit below −80 dB relative
   to peak. Chopping >13 kHz is free realism — phone mics roll off there anyway.
3. Synthetic-IR convolution reverb per room (recipes in the reference), **truncated at the
   picture cut** with a 30 ms fade — a new room means the old room's tail stops existing.
4. Bleep tone: **dry** 1 kHz sine, RMS-matched to the surrounding ±0.8 s of dialog +1 dB,
   8 ms cosine edges. Dry is the convention; matched level keeps it from feeling pasted on.
5. Outdoor scenes get `apply_outdoor()`, not room reverb — outside is *distance*, not reverb.
   See the reference's outdoor section. Its output is **RMS-matched to its input**, so a
   character change never moves a level the client already approved.

### 5. Master and mux

Measure the source first (`loudnorm=print_format=summary`). AI raws often arrive very quiet
(the proving-run source was −23.6 LUFS). For a clip that may publish directly, master to
**−14 LUFS / ≤−1.2 dBTP** (`volume=<gap>dB,alimiter=limit=0.87:attack=3:release=60:level=false`)
and keep the un-mastered mix on disk — offer it on the canvas in case the clip feeds a bigger
edit downstream. Then mux: `-map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart`.

### 6. Verify — measurements, not vibes

Every render, before it ships:

- **Censor check:** re-transcribe the final mix; every target word must be gone and no
  neighbor word lost. A "lost" clean word → isolated-slice re-probe arbitrates by word
  *presence*. If it's still ambiguous, band-scan the SOURCE at that spot — the proving run's
  recurring "ads→ad" flag turned out to be a final /s/ the AI actor never pronounced
  (−70 dB in the 4–10 kHz band). Measure before blaming the mix.
- **Level table:** print per-scene ambience-under-dialog from the stems (the engine writes
  them). Targets are in the reference; a bed peak-normalized to −3 dB can still be *inaudible*
  (sparse content → RMS −60). **Judge beds by RMS under dialog, never by peak.**
- **Spectrogram read:** `showspectrumpic` — beds must fill inter-word gaps (no black silence),
  bleep bars clean at 1 kHz, no horizontal whine lines above 13 kHz.
- **Harness:** the `video-qa` engine — `npm --prefix tools/video-qa run qa:video -- --video out.mp4
  --instructions intent.txt` — write the intent file so Gemini judges the sound design (bleeps are INTENTIONAL, ambience per scene,
  reverb per room) instead of flagging it.

### 7. Deliver and iterate

Publish on a review canvas (`video-review-canvas` skill — lead the reply with the URL), deliver
the file next to the source, log the session. Revision notes come back pinned to timestamps;
map each pin to its scene (pins can land a beat late — a pin at 15.4 next to a cut at 15.53
usually means the scene *before* the cut).

Revision protocol, learned over 5 rounds:

- **Keep what they praised, layer what they asked for.** "I like the birds but add a lawnmower"
  = a `LAYERS` entry on the same bed, never a regeneration of the bed they liked.
- Client level language: **"2x" = +6 dB** (double amplitude). "Increase the ambient volume"
  with no scene named = `AMB_MASTER_DB`, one global number, every approved ratio preserved.
- **Level-match new elements to whatever the client called "perfect"** — that scene's
  ambience-under-dialog ratio is now the house target for this project.
- Timed events must dodge the bleeps and dialog peaks: the proving run's car pass first landed its
  swell exactly on a bleep at 1.3 s; check the event's loudest 0.5 s window against the
  transcript before rendering.
- A character change (EQ, wash, reverb) should be RMS-matched so the approved loudness
  doesn't move with it. Ship every round as a NEW file, same canvas slug.

## Environment notes

- ffmpeg/ffprobe from PATH (`FFMPEG` env var overrides). If an agent sandbox kills ffmpeg or
  node, re-run with the sandbox disabled.
- `OPENAI_API_KEY` (Whisper) and `ELEVENLABS_API_KEY` (ambience kit) from the environment or a
  `.env` at the repo root — never hardcode either.
- python3 with numpy + scipy (`pip install numpy scipy`).
