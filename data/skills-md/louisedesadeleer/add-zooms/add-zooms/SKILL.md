---
name: add-zooms
description: Add emphasis motion to a flat talking-head video file — dramatic hard-cut punch-zooms on emphasised words + listicles, and subtle Ken Burns slow-pushes on insightful lines. Transcript-driven, ffmpeg-based (zoompan), non-destructive. Use when the user says "add zooms", "/add-zooms", "punch in on the emphasised words", "add motion/energy to this clip", or has an already-cut .mp4 (e.g. a LinkedIn hot-take) that needs zoom emphasis. The file-based sibling of /tella-edit and /tella-cut.
---

# Add Zooms

Add emphasis motion to a **flat talking-head video file** (usually a 9:16 vertical clip already cut for social): **dramatic punch-zooms** on emphasised words + listicles, and **Ken Burns slow-pushes** on insightful lines. Transcript-driven, ffmpeg-based, non-destructive (writes a new file).

This is the file-based sibling of `/tella-edit` and `/tella-cut` (which zoom *inside* Tella). Use `/add-zooms` when the video is already an `.mp4` on disk and you just want to add punch + push motion — e.g. a cut LinkedIn hot-take.

## Inputs
- A path to a video file (ask if not given). Works best on a fairly static talking-head.
- Optional: whether to render straight through, or return the zoom map for approval first (default: **render, then show the map for tweaks** — motion is taste-heavy).

## Tooling
- `whisper` (CLI) for word-level timestamps
- `ffmpeg` `zoompan` for the zoom, audio stream-copied
- `scripts/zoom_lib.py` — the engine (envelope model, punch/kenburns/ratchet events)

---

## The three moves

| Move | When | Feel | Peak zoom |
|---|---|---|---|
| **punch** | A single emphasised word ("outliers", "average", "bad") | **HARD CUT in (instant, 1 frame)**, hold, **hard cut out** | 1.18–1.30 |
| **ratchet** | A listicle — "jokes, scripts, content" / "good jokes, good tweets, good videos" | Each item **hard-cuts up** a level, hold, then hard cut back | build 1.12 → 1.28 |
| **kenburns** | An insightful / thesis line — the "here's the actual point" moment | Slow continuous push across the whole line (**the ONLY smooth move**) | 1.10–1.14 (subtle!) |

**Taste rules (learned defaults):**
- **HARD CUTS ONLY. Never a smooth/ramped zoom — except Ken Burns.** Punches and ratchets jump instantly to the zoom level (1-frame cut), hold, then jump back. No ease-in, no ease-out. Any smooth in/out on a punch reads as a creep and Louise hates it. Ken Burns is the single exception: it's a slow continuous push and is meant to glide.
- **Not every line.** Leave long stretches at 1.0× — the rest beats are what make the zooms land. Personal asides / filler = no zoom.
- **Punch peaks 1.18–1.30**, dramatic and quick. **Ken Burns stays subtle (≤1.14)** — it should be felt, not seen.
- **Focal point (0.5, 0.42)** — horizontally centered, biased up toward the face on a vertical clip. Override `--cy` if the face sits lower/higher.
- **Ratchets escalate** (each step higher than the last) so a list *builds*.
- Contrast payoffs ("the average of all jokes is just… an average joke") → punch the final word.
- CTA / sign-off ("give me a follow") → gentle Ken Burns push into it.
- Keep source resolution; peaks ≤1.30 keep a 1080p clip crisp.

---

## Workflow

### Step 0 — Probe
`ffprobe` the file for w/h/fps/duration. Confirm it's a talking-head (zooms on b-roll/drone footage need a different focal point — ask).

### Step 1 — Transcribe with word timestamps
```
ffmpeg -y -i INPUT -ac 1 -ar 16000 work/audio.wav
whisper work/audio.wav --model small.en --language en --word_timestamps True \
  --output_format json --output_dir work
```
Read `work/audio.json` → `segments[].words[]` = `{start,end,word}`.

### Step 2 — Author the zoom map (the taste step)
Read the transcript and mark:
- **Punch words** — the emphasised beat in a sentence (the word you'd lean on out loud).
- **Listicles** — 2–4 parallel items in a row → one `ratchet`.
- **Insight lines** — "it turns out…", "what this means is…", the thesis, the contrast → `kenburns`.

Write `work/map.json` — a list of events (times in **seconds**, from the word timestamps):
```json
[
  {"type":"ratchet","steps":[[4.55,1.16],[5.40,1.20],[5.95,1.24],[6.65,1.28]],"label":"hook list"},
  {"type":"punch","t":33.32,"peak":1.28,"hold":0.45,"label":"outliers"},
  {"type":"kenburns","t0":41.14,"t1":45.10,"peak":1.14,"label":"thesis line"}
]
```
Place `t` on (or ~0.05s before) the **word's `start`**. `hold` = how long to stay punched (short for a single word ~0.2–0.5s; longer to ride a whole phrase). Overlaps are fine — the engine takes the max envelope, so releases blend upward instead of snapping down.

### Step 3 — Render
```
python3 scripts/zoom_lib.py render INPUT OUTPUT work/map.json
# options: --cy 0.42 (focal height)  --cx 0.5  --crf 19
```
Prints the event list with peaks + timings, then renders (~5× realtime). Audio is stream-copied; output is `+faststart` for social.

### Step 4 — Verify
Pull frame pairs (source | zoomed) at a rest beat and a couple of peaks:
```
ffmpeg -ss T -i OUTPUT -frames:v 1 f.jpg   # eyeball: rest = untouched, peak = zoomed on face
```
Check: rest beats are full-frame, punches land on the emphasised word, focal point sits on the face (not chest/ceiling). Adjust `map.json` peaks/times or `--cy` and re-render.

---

## Notes
- **Non-destructive** — always writes a new file, never touches the source.
- **`zoompan` softness** — any zoom >1.0 upscales, so peaks ≤1.30 on a 1080p+ source stay sharp. Don't push past ~1.35 on a talking head.
- **b-roll / drone clips** — the (0.5, 0.42) face bias is wrong for landscape scenery; use `--cy 0.5` and gentler Ken Burns for those.
- To tune without re-transcribing, just edit `map.json` and re-run Step 3.
