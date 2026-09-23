---
name: edl-tighten
description: >-
  Surgically remove awkward pauses, dead air, and long silences from a FINISHED
  voiceover-driven cut while keeping video, VO audio, word-synced captions, SFX
  hits, and the composition timeline in sync. Use when asked to "tighten the
  cut", "remove the pause at 0:41", "cut the dead air", "the gap between
  sentences is too long", "shave the silences", "it drags here", or when a
  revision round adds new cuts to an already-tightened edit. Finds gaps two
  ways (silencedetect + RMS envelope), chooses frame-quantized cut windows that
  never clip speech onsets, masks splices at cuts or attention magnets,
  executes ONE trim/concat filtergraph per stream from the original source,
  remaps the transcript through the EDL with scripts/remap-transcript.py
  (never re-whisper), and verifies with a re-scan plus frame extraction.
  Needs ffmpeg/ffprobe + python3 only. Not for building the edit itself
  (branded-ad-edit / talking-head-recut) or QA of a render you didn't cut
  (video-qa).
---

# edl-tighten — surgical pause removal that keeps everything in sync

A finished VO-driven edit is a stack of synced layers: video, loudness-normalized
voiceover, word-synced captions, SFX hits, and a composition timeline whose card
positions were placed against the VO. Cutting 0.4s of dead air out of the audio
alone desyncs every other layer. This skill removes the pause from **all layers
at once** by treating the edit as one EDL (a list of removed source ranges) and
regenerating every stream from the original source through that EDL.

**The iron law: ONE cumulative EDL against the ORIGINAL source.** Never cut an
already-cut file. Every revision round appends ranges to the same EDL (in source
time), merges adjacent/overlapping ranges, and regenerates from source. Cuts-of-
cuts accumulate re-encode generations, drift the frame grid, and make timestamps
unmappable.

## Requirements

- `ffmpeg` / `ffprobe` on PATH
- `python3` (stdlib only — `scripts/remap-transcript.py` has no dependencies)
- The **original** source video, the **loudness-normalized** VO track that the
  composition actually uses, and the word-level `transcript.json` produced when
  the edit was built (whisper word timestamps). If the VO is baked into the
  video and no separate track exists, the same EDL still applies — cut the
  muxed file's audio with the identical `atrim` graph.
- Know the composition fps (usually 30). Everything quantizes to that grid.

## Pipeline

```
1 FIND      silencedetect + RMS envelope (BOTH — each misses gaps the other catches)
2 CHOOSE    frame-quantized cut windows, 0.10-0.15s pause kept, onsets protected
3 PLACE     put the splice where it's visually masked
4 EXECUTE   one trim/concat filtergraph per stream, from the original source
5 REMAP     transcript, timeline positions, SFX hits, caption ranges, duration
6 VERIFY    ffprobe + re-scan + frame-extract around each splice and LOOK
```

---

## 1. FIND the gaps — two detectors, both required

### 1a. silencedetect (hard silences)

```bash
ffmpeg -hide_banner -i vo_normalized.wav \
  -af silencedetect=noise=-38dB:d=0.22 -f null - 2>&1 | grep silence_
```

`noise=-38dB:d=0.22` is the tuned setting for normalized VO: it flags every
stretch ≥ 0.22s that sits below −38 dB. Run it on the full track first to get
the candidate list, then on the region the reviewer flagged.

### 1b. RMS envelope print (breathy lulls silencedetect misses)

**silencedetect alone is not enough.** Breath tails, mouth noise, and room tone
often sit at **−28 to −36 dB** — above the silence threshold, but perceptually
still dead air. A "pause that drags" flagged by a human reviewer is very often
one of these. Print a 50 ms RMS envelope of the suspect region and read it as a
bar chart:

```bash
# Envelope of source seconds 40-46 (adjust -ss / -t to the suspect region)
ffmpeg -v error -i vo_normalized.wav -ss 40 -t 6 -ac 1 -ar 16000 -f s16le - \
| python3 -c '
import sys, struct, math
data = sys.stdin.buffer.read()
n = len(data)//2
smp = struct.unpack(f"<{n}h", data[:n*2])
sr, t0 = 16000, 40.0            # t0 = the -ss value above
win = int(sr*0.050)             # 50 ms windows
for i in range(0, n - win, win):
    w = smp[i:i+win]
    rms = math.sqrt(sum(s*s for s in w)/win)/32768.0
    db = 20*math.log10(rms) if rms > 0 else -90.0
    bar = "#" * max(0, int((db+60)/1.5))
    print(f"{t0+i/sr:7.2f}s {db:6.1f} dB |{bar}")
'
```

Reading it:
- **< −38 dB sustained** → hard silence (silencedetect saw it too).
- **−28 to −36 dB sustained** → breathy lull. Audibly a gap. Cut candidate.
- **A sharp jump of 15+ dB in one window** → a speech **onset**. Mark its time;
  you must never cut into it (step 2).

### 1c. Do NOT trust whisper word times for gap boundaries

Whisper word-level timestamps **overshoot into silence** — a word's `end` is
routinely 0.1–0.4s later than the word actually ends, because whisper pads into
the pause. Word ends tell you roughly *where* a gap is, never *how wide* it is.
The envelope is the ground truth for both edges of the gap. (The same overshoot
is why `remap-transcript.py` clamps word ends at splices in step 5.)

## 2. CHOOSE the cut window

For each gap, pick the removed range `[cut_start, cut_end]` in **source time**:

1. **Leave 0.10–0.15s of natural pause.** Butt-splicing two phrases with zero
   gap sounds robotic and creates an audible bump. If the gap is 0.62s, remove
   ~0.48s and keep ~0.14s.
2. **Never clip a speech onset.** Set `cut_end` from the **envelope**, not from
   the next word's whisper `start` (also unreliable). Find the onset jump in
   the envelope and keep **at least one frame of margin** before it
   (`cut_end ≤ onset − 1/fps`). Clipping the first plosive of the next word is
   the most audible mistake this workflow can make.
3. **Frame-quantize both edges to the fps grid.** At 30 fps every boundary must
   be a multiple of 1/30 s (0.0333…). Round `cut_start` up and `cut_end` down
   (shrink the cut, never grow it) so quantization can't eat the safety margin.
   Un-quantized cuts make the video and audio graphs disagree by sub-frame
   amounts and produce one-frame freezes at splices.

Record each range in the EDL file (see Bookkeeping below) before executing.

## 3. PLACE the splice where it's masked

A splice in a continuous talking-head shot is a **jump cut** — the speaker's
head/hands teleport. Sometimes acceptable, but always check whether the cut can
land somewhere the eye won't see it:

- **At a framing or section cut** that already exists in the edit (a punch-in,
  a B-roll cut, a scene change). If a section boundary sits inside or near the
  gap, put the splice exactly on it — a cut on a cut is invisible.
- **Exactly where an attention magnet lands** — a card popping in, a big
  headline hit, a screenshot sliding on. The motion graphic steals the eye for
  ~10 frames; a jump on the speaker under it goes unnoticed. If the timeline
  has a card entering near the gap, bias the splice to land on the card's
  entrance frame.
- **If it must land mid-shot with nothing to mask it: expect a visible jump on
  the speaker** and say so when reporting the change. Options: accept it (fast
  social pacing tolerates jump cuts), add a 2–4% punch-in on one side of the
  splice, or drop a brief overlay on the splice frame.

## 4. EXECUTE — one filtergraph per stream, from the original source

Build the keep-segments from the merged EDL (keeps = the complement of the
cuts) and cut each stream in a single pass. Never run ffmpeg on a previous
round's output.

With cuts `41.400–41.833` and `62.100–62.500` in a 75.000s source:
keeps = `0–41.400`, `41.833–62.100`, `62.500–75.000`.

**Video** (from the original source video):

```bash
ffmpeg -y -i source.mp4 -filter_complex "
[0:v]split=3[v0][v1][v2];
[v0]trim=0:41.400,setpts=PTS-STARTPTS[va];
[v1]trim=41.833:62.100,setpts=PTS-STARTPTS[vb];
[v2]trim=62.500:75.000,setpts=PTS-STARTPTS[vc];
[va][vb][vc]concat=n=3:v=1:a=0[vout]" \
  -map "[vout]" -an \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -g 30 -keyint_min 30 \
  video_tight.mp4
```

- `split=N` → one `trim=A:B,setpts=PTS-STARTPTS` per keep → `concat`. One
  graph, one re-encode, N segments.
- **`-g 30 -keyint_min 30` is mandatory** (match the number to the fps): a
  keyframe every second keeps seeking frame-accurate when the tightened video
  is placed in a composition/player that scrubs. Default GOP sizes (250) make
  post-splice seeks land seconds off.
- Re-encoding is unavoidable and correct here — stream-copy concat can only cut
  on existing keyframes and will not hit your frame-quantized boundaries.

**Audio** — the **identical** boundaries as an `atrim` graph on the
loudness-normalized VO (not the raw VO; cutting the raw VO and re-normalizing
changes the level of the whole track):

```bash
ffmpeg -y -i vo_normalized.wav -filter_complex "
[0:a]asplit=3[a0][a1][a2];
[a0]atrim=0:41.400,asetpts=PTS-STARTPTS[aa];
[a1]atrim=41.833:62.100,asetpts=PTS-STARTPTS[ab];
[a2]atrim=62.500:75.000,asetpts=PTS-STARTPTS[ac];
[aa][ab][ac]concat=n=3:v=0:a=1[aout]" \
  -map "[aout]" vo_tight.wav
```

Same numbers, same order. If video and audio boundaries differ by even one
frame, lipsync drifts after the splice for the rest of the piece.

Music beds and ambient tracks usually should **not** be EDL-cut (a music splice
is audible); keep them continuous and just shorten the tail to the new
duration, unless a music hit was synced to a VO moment — then re-place it in
step 5 like an SFX hit.

## 5. REMAP everything downstream

The EDL changes every timestamp after the first cut. Remap **in code**, never
by re-deriving:

**Transcript / captions** — run the bundled script:

```bash
python3 .claude/skills/edl-tighten/scripts/remap-transcript.py \
  transcript.json --cuts edl.json --fps 30 -o transcript.tight.json
```

It shifts every word's start/end through the EDL, clamps word ends that
overshoot into a removed range to the splice point, drops entries that were
entirely inside a cut (warns — verify those were silence), and preserves the
JSON structure (OpenAI whisper `segments[].words[]`, flat word lists, and
whisper.cpp ms `offsets` all supported).

**NEVER re-whisper the tightened audio.** Whisper on concatenated cuts drifts
late — errors compound across splices and by the end of the piece karaoke
captions highlight the wrong word. The remap is exact; a fresh transcription is
not. This is the single most tempting shortcut in this workflow and it always
loses.

**Everything else with a timestamp** — map each one with the same tool:

```bash
python3 .claude/skills/edl-tighten/scripts/remap-transcript.py \
  --cuts edl.json --query 44.10,62.30,71.05
```

Apply the mapped values to:
- **Composition timeline positions** — every card/overlay/B-roll clip start and
  duration that lands after the first cut (a clip *spanning* a cut also
  shortens: map its start and end separately).
- **SFX hit times** — whooshes/pops synced to card entrances move with their
  cards.
- **Caption config ranges** — any per-range styling or section boundaries
  expressed in seconds.
- **Stage/composition duration** — new duration = old duration − total removed
  (the script prints both). Update it explicitly; a stale duration leaves
  frozen frames or trailing black at the end of the render.

## 6. VERIFY

1. **Durations**: `ffprobe -v error -show_entries format=duration -of csv=p=0
   video_tight.mp4` (and the wav). Both must equal source − total_removed
   within one frame, and match each other.
2. **Re-scan the target region**: re-run silencedetect **and** the envelope
   print on `vo_tight.wav` around each splice. Expect **zero gaps ≥ 0.15s** in
   the tightened region, and no clipped onset (the first window of the next
   phrase should jump straight to speech level, not ramp from a chopped
   plosive).
3. **Frame-extract around each splice and LOOK** — this step is not optional;
   a graph cannot see a jump cut:

   ```bash
   # splice at output time T, at 30 fps — 3 frames either side
   ffmpeg -y -ss $(echo "$T - 3/30" | bc -l) -i video_tight.mp4 \
     -frames:v 7 -vf fps=30 splice_%02d.png
   ```

   Read the frames. Check: no freeze/duplicate frame, no black frame, and
   whether the speaker jump (if mid-shot) is acceptable. If a card was used as
   the mask, confirm it actually enters on the splice frame.
4. If the tightened video feeds a composition, re-render and spot-check the
   captions around each splice — the karaoke highlight must stay on the spoken
   word after every cut.

---

## Bookkeeping — one EDL, every revision round

Keep a single `edl.json` next to the project, always in **source time**:

```json
{
  "source": "source.mp4",
  "fps": 30,
  "cuts": [
    [41.400, 41.833],
    [62.100, 62.500]
  ]
}
```

Rules that make round 3 as clean as round 1:

- **Append, merge, regenerate.** A new reviewer note ("also tighten the pause
  at 55s") = find the gap in the **source** (source time ≈ output time + total
  removed before it; confirm with the envelope on the source VO), append the
  range, then merge and regenerate everything from the original source:

  ```bash
  python3 .claude/skills/edl-tighten/scripts/remap-transcript.py \
    --cuts edl.json --write-merged edl.json --query 0
  ```

  (`merge` combines overlapping/adjacent ranges automatically — two revision
  rounds nibbling at the same pause become one clean cut.)
- **Never express a new cut in tightened-file time and cut the tightened
  file.** Convert to source time, add to the EDL, re-run step 4. The extra
  re-encode you "save" costs you the ability to remap anything ever again.
- The original `transcript.json` (against the source) is likewise immutable —
  every round re-remaps it through the full merged EDL in one shot.
- Timeline/SFX/caption positions are best kept in source time in your working
  notes too, mapped through the EDL at build time; if the composition stores
  output-time values, recompute all of them from the source-time originals
  each round rather than incrementally shifting them.
