---
name: cut-video
description: Tighten a long recording aggressively — remove silences, fillers, hedges, false starts, and repetitions while preserving laughs and comedic pauses. Cuts are driven by Montreal Forced Aligner (MFA) word boundaries (auto-installs on first run), not raw Whisper timestamps. Use when the user pastes a video and says "cut this", "tighten this video", "remove silences", "strip ums", "clean this up", or any variant of "make this video shorter without losing the good parts".
---

# Cut Video

Tighten a long-form recording **aggressively**: remove silences, fillers, hedges, weak transitions, false starts, and repetitions. Preserves laughs and comedic pauses. Outputs a cleaned MP4 ready to drop into CapCut for layouts/zooms/memes.

> **This skill is more accurate than cutting from Whisper alone.** Cuts are driven by **Montreal Forced Aligner (MFA)** word boundaries (~10–20ms precision, with true inter-word silences as explicit intervals), not Whisper timestamps (±100–300ms, with pauses embedded inside word durations). Whisper is used only to produce the transcript *text* that MFA aligns to the audio. The result: tighter cuts, no clipped word onsets/tails, and reliable silence detection.

> **⚠️ But MFA times are a DRAFT, not ground truth (burned 2026-07-02, `AI is bad at jokes` DJI run).** MFA can only align the transcript whisper gave it. On retake-heavy footage whisper COLLAPSES repeated lines, so MFA smears one transcribed instance across several spoken takes — measured drift on that run was **1–6 seconds** in the back half ("the average of all working code": MFA said 217.2s, real onset 225.4s; the final "what this means" take: MFA said 114.7s, real 130.4s). Every keep boundary must be **ground-truthed with isolated-window re-transcription (Step 2.5)** before rendering. Skipping that step on that video would have produced garbage cuts for the entire second half.

**Style target** (calibrated from `AI mogging my dad.mp4`):
- ~1 cut every 1.3–1.5 seconds (median cut duration ~1.1s)
- ~40–60% total runtime reduction from raw
- Cuts happen mid-sentence, not just between sentences
- Word-by-word tightening — fillers, hedges, and weak openers get sliced

## Inputs

- Video file path (the user will provide; otherwise ask)
- Optional: tone preference (`aggressive` / `balanced` / `sentimental` / `documentary`) — default: `aggressive`

## Working directory

`/tmp/cut-video/<basename>/` — mkdir at start, leave artifacts for debugging.

---

## Step 0 — Make a proxy (the single biggest speed move)

If the source is HEVC, >500MB, or 4K+, transcode to a 1080p H.264 working copy FIRST. Every subsequent step runs against the proxy, not the source.

**Check orientation first** (`ffprobe … width,height`) — DJI/phone footage is often vertical 9:16, and a hard-coded `scale=1920:1080` would squash it. Use `scale=1920:1080` only for landscape; use `scale=1080:1920` for portrait (or the orientation-proof `scale=-2:1080` / `scale=1080:-2`).

```bash
ffmpeg -y -hwaccel videotoolbox -i "$SRC" \
  -vf scale=1920:1080 \        # portrait sources: scale=1080:1920
  -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  /tmp/cut-video/$NAME/proxy.mp4
```

**Critical flags:**
- `-hwaccel videotoolbox` on the INPUT — hardware-decodes HEVC, ~5–10× faster on Apple Silicon. Skip this and you'll wait minutes instead of seconds.
- `-preset fast` — the libx264 default is `medium`, which is ~3× slower for no useful quality gain on a working copy.

Hardware encode alternative (even faster on M-series, slightly larger file):
```bash
-c:v h264_videotoolbox -b:v 8M
```

## Step 1 — Get the transcript TEXT (whisper, as input for MFA)

MFA is a **forced aligner, not a transcriber** — it needs a transcript to align. Whisper's only job here is to produce that text; **whisper word timestamps are NOT used for cutting** (they're ±100–300ms off and turbo embeds pauses inside word durations). MFA (Step 1.5) supplies all timing.

```bash
ffmpeg -y -hwaccel videotoolbox -i /tmp/cut-video/$NAME/proxy.mp4 \
  -vn -ac 1 -ar 16000 /tmp/cut-video/$NAME/audio.wav
whisper /tmp/cut-video/$NAME/audio.wav \
  --model tiny.en --word_timestamps True --output_format json \
  --output_dir /tmp/cut-video/$NAME --language en
```

**Model choice (revised 2026-07-02 — "we only need the words" was WRONG):** the transcript text IS the alignment input, so transcript errors become timing errors. On the `AI is bad at jokes` run, `tiny.en` dropped exactly the words the old warning predicted ("bland", "slop"), misheard "Compare this to" as "comparative is", and collapsed full-line retakes — and MFA, aligning that wrong text, drifted 1–6s across the back half. Use **`tiny.en` only for a first fast pass to see the take structure**; if the transcript shows retakes/repetitions, or the footage is noisy/outdoor, the per-region ground-truth pass (Step 2.5) with `small.en` supplies the real cut times anyway. (A full-pass `small.en` transcript is a reasonable upgrade for the MFA input too — ~1–2 min on a 5-min video — but it ALSO collapses retakes, so it does not remove the need for Step 2.5.) For non-English use `--model base` and drop `--language`. We keep `--word_timestamps True` only so whisper times survive as a cross-check/fallback (Step 1.5 caveats, 2a-legacy) — never as the primary cut source.

## Step 1.5 — Align the transcript to the audio with MFA (Montreal Forced Aligner) — the timing engine

This is the spine of the skill. **MFA forced-aligns the whisper transcript text to the audio** and returns word boundaries at ~10–20ms precision, with true inter-word silences as explicit empty intervals. **All cut decisions (gaps, fillers, false starts, retakes) use MFA word times.**

**Auto-install MFA (the skill does this itself — don't make the user do it).** Run this idempotent bootstrap at the start of every run; it's a no-op once everything's present (a few seconds), and a one-time ~2–3 min install on a fresh machine. Tell the user "installing MFA (one-time)…" only when it actually installs something.

```bash
# 1. Ensure conda exists (MFA's only supported install path). Install miniforge via brew if missing.
if ! command -v conda >/dev/null 2>&1; then
  echo "conda not found — installing miniforge (one-time)…"
  brew install --cask miniforge || brew install miniforge
  # make conda available in this shell
  eval "$("$(brew --prefix)/bin/conda" shell.bash hook 2>/dev/null || conda shell.bash hook)"
fi
source "$(conda info --base)/etc/profile.d/conda.sh"

# 2. Ensure the mfa env exists with MFA installed
if ! conda env list | grep -q '^mfa\b'; then
  echo "creating mfa conda env (one-time)…"
  conda create -n mfa -c conda-forge montreal-forced-aligner -y
fi

# 3. Ensure the English acoustic model + dictionary are downloaded (idempotent; skips if present)
conda run -n mfa mfa model download acoustic english_mfa  2>/dev/null || true
conda run -n mfa mfa model download dictionary english_mfa 2>/dev/null || true
```

If `brew` itself is missing, MFA can't be auto-installed — fall back to the whisper+silencedetect path (see the fallback bullet below) and tell the user, with the one-line `brew install miniforge` they'd need to unlock MFA precision.

**Per run:**
```bash
# corpus = a dir with audio.wav + audio.txt (the whisper transcript as PLAIN TEXT, no timestamps)
mkdir -p /tmp/cut-video/$NAME/corpus
cp /tmp/cut-video/$NAME/audio.wav /tmp/cut-video/$NAME/corpus/
python3 -c "import json;d=json.load(open('/tmp/cut-video/$NAME/audio.json'));open('/tmp/cut-video/$NAME/corpus/audio.txt','w').write(d['text'])"
conda run -n mfa mfa align --clean /tmp/cut-video/$NAME/corpus english_mfa english_mfa /tmp/cut-video/$NAME/aligned
# → aligned/audio.TextGrid — "words" tier: (start, end, word); EMPTY-label intervals = true silences
```
Parse the TextGrid `words` tier (pip `praatio`, or a 20-line parser — interval tiers are plain text). What MFA buys:
- **True word boundaries** → cut pads shrink to ~0.02s, no clipped word onsets/tails.
- **True silences are explicit empty intervals** → the 2a gap table works directly off the TextGrid; the whisper embedded-pause problem disappears.
- **Caveat:** MFA aligns the transcript it's GIVEN. If whisper collapsed a spoken stutter ("growth… growth marketer" → "growth marketer"), alignment drifts locally around it — keep the `silencedetect` pass (2a) as a CROSS-CHECK, and treat disagreements > 0.3s as suspect regions to re-inspect. **On retake-heavy self-shot footage the drift is not local — it's cumulative and can reach seconds** (see the warning at the top and Step 2.5). And when the noise floor kills silencedetect too (low-dynamic-range guard), you have NO automatic cross-check — Step 2.5 is then mandatory, not optional.
- **Drift smoke alarm — stretched words:** any short word whose MFA or whisper duration is ≳1s ("like" 1.16s, "there's" 1.5s, "of" 2.4s, "the" 4.9s on the 2026-07-02 run) is hiding a pause, a flub, or an ENTIRE collapsed retake inside it. Collect every stretched word up front; each one marks a region whose true content is unknown until re-windowed (Step 2.5). One stretched "the" turned out to contain a complete clean take of the whole sentence — the take that got kept.
- **Fallback:** if MFA/conda is unavailable and the user doesn't want the install, fall back to whisper words + audio silencedetect (2a) — and say so in the plan summary. This is the ONLY path where whisper timestamps drive cuts.

## Step 2 — Build the cut list (AGGRESSIVE by default)

Compute a list of (start, end) intervals to KEEP from the **MFA word intervals** (whisper JSON only as fallback). Aggressive cutting removes content in four categories:

### 2a. Silence gaps — MFA empty intervals first, audio silencedetect as cross-check (updated 2026-06-10)
With MFA (Step 1.5), true silences are the TextGrid's empty-label intervals — apply the gap table below to those directly. Cross-check with audio silence detection — **but CALIBRATE the threshold to the recording's own noise floor; never hard-code `-30dB`** (added 2026-06-16, burned on a DJI-mic to-camera take whose floor sat at ~-24dB: a fixed `-30dB` saw the ENTIRE take as non-silent, so every "silent" gap measured "above threshold = content, keep" and ~8s dead-air pauses survived the cut):

```bash
# 1. Measure the noise floor F and speech level S from per-0.5s-window RMS
#    (slice the wav into 0.5s windows, run volumedetect on each, collect mean_volume;
#     F ≈ 10th-percentile window RMS  (room tone),  S ≈ 90th-percentile  (speech))
# 2. Set the silence threshold RELATIVE to the floor, not absolute:
THRESH=$(python3 -c "print(f'{F + 6:.0f}')")        # 6 dB above the measured floor
ffmpeg -i proxy.mp4 -af silencedetect=noise=${THRESH}dB:d=0.14 -f null - 2>&1 | grep silence_
```

**⚠️ Low-dynamic-range guard (the real lesson, 2026-06-16):** if `S − F < ~8dB` (noisy mic — outdoor/DJI/lav with AC hum, where the per-second RMS reads the SAME during speech and silence), NO energy threshold can separate speech from silence. Do **not** trust silencedetect/volumedetect at all in that case — drive every cut from MFA word boundaries, or in the no-MFA fallback from **`small.en` word ONSETS + stretched-word pause detection** (a whisper word whose duration ≫ a normal word IS a hidden pause: keep ~`0.10 + 0.105·len(word)`s of onset, then cut to the next word's start). Say which path you used in the plan summary.

Without MFA, the silencedetect pass is the trustworthy gap source ONLY when the dynamic-range guard passes: **`mlx_whisper`/whisper-turbo (and `tiny.en`) EMBED pauses inside word durations** — a 3s "word" is really "word [long pause]", inter-word *gaps* read ~0.00, and gap-based trimming does NOTHING. **Use `small.en` (not `tiny.en`) for the fallback path** — tiny stretches words across silence even worse and silently drops words ("bland", "slop") and whole retakes. Parse `silence_start`/`silence_end`, remove those intervals (keep ~0.04s pad; MFA-precision boundaries allow ~0.02s). For "almost no pauses" → `d=0.12`, pad 0.03. Combine with the dedup (2c/2d) by removing `silences ∪ dropped-word-ranges`. This is how you hit median ~1.1–1.3s.
- **Stutters whisper hides:** turbo collapses spoken repetitions ("growth… growth marketer" → "growth marketer") and varies run-to-run (drops/re-adds words). These are invisible to transcript-based cutting — MFA alignment drift + silencedetect disagreement marks the region; re-inspect it, or ask the user for the timecode and cut a precise window.

### 2a-legacy. Silence gaps between words (TIGHT thresholds)

| Gap | `aggressive` (default) | `balanced` | `sentimental` | `documentary` |
|---|---|---|---|---|
| `< 0.25s` | keep | keep | keep | keep |
| `0.25–1s` | trim to **0.1s** | trim to 0.3s | trim to 0.5s | keep |
| `1–3s` | trim to **0.2s** | trim to 0.8s | trim to 1.5s | trim to 2s |
| `> 3s` | trim to **0.2s** | trim to 0.5s | trim to 1s | trim to 3s |

The aggressive thresholds match the reference video's pacing (median cut 1.13s).

### 2b. Filler words — cut with 50ms padding

Always cut: `um`, `uh`, `umm`, `uhh`, `er`, `erm`, `ah`, `mhm`, `hmm` (standalone)

### 2c. Hedges & weak transitions — cut aggressively in default mode

Cut these when they're delivered as filler (not as substantive content). Mark for cut, then verify against context in the review step:

- **Hedges:** `like` (as filler, not as comparison), `you know`, `I mean`, `I guess`, `I think` (when hedging, not asserting), `kind of`, `sort of`, `basically`, `literally`, `actually` (as filler)
- **Weak transitions:** `so` (sentence-opener), `and so`, `and then`, `but um`, `but uh`, `okay so`, `right so`, `well`
- **Redundant qualifiers:** `kind of like`, `sort of like`, `or whatever`, `or something`
- **Re-orientation phrases:** `anyway`, `so anyway`, `the thing is`, `what I'm saying is`, `to be honest`, `honestly`

In `balanced` / `sentimental` / `documentary` modes, only cut hedges that precede a re-statement (false start, see 2d). Keep them in conversational moments.

### 2d. False starts and repetitions — cut aggressively

Detect by scanning for:
- **Self-corrections:** speaker re-states the same opening within ~3 seconds. Pattern: `"I want — I wanted to..."`, `"It's a — it's an interesting..."`. Drop the earlier attempt + the gap.
- **Restart preambles:** `"so basically what I'm saying is..."`, `"the point is..."`, `"let me start over..."`. Drop the preamble, keep the actual point.
- **Verbatim repetitions:** speaker says same 3+ words twice in a row. Keep the cleaner take.

Implementation hint: build a sliding-window fuzzy-match on consecutive word n-grams. When 3-gram similarity > 0.8 within a 3-second window, flag the earlier instance for removal.

### 2d-bis. FULL-LINE RETAKES (self-shot to-camera recordings, added 2026-06-10)
Self-shot intros/promos contain **whole-sentence retakes** separated by 5–60s ("The next person is Carmen who works. … The next person, the next guest I invited is Carmen who's social and content lead at Slate") — far outside 2d's 3-second window. Detect and resolve them:
- **Detection:** fuzzy n-gram match (4-grams, similarity > 0.7) across a **60-second window**; also match sentence OPENERS (first 3–5 words) since retakes usually restart the line.
- **Keep the LAST take by default** — speakers re-record until satisfied. Exception: if the last take is incomplete/flubbed and an earlier one is clean, keep the clean one and note the override in the plan summary.
- **A retake boundary is usually preceded by a long pause, a breath, a click, or a slate-phrase** ("okay", "again", "take two") — the pause+opener-match combo is the strongest signal.
- **Surface every retake group in the Step 3 plan** (`line → takes at [t1, t2, t3] → keeping t3`) so the user can override which take survives.

### 2e. NEVER cut these — protect explicitly

- **Laughs.** Whisper transcribes laughter as silence. Before applying ANY silence cut, check audio amplitude:
  ```bash
  ffmpeg -i audio.wav -af "volumedetect" -f null - 2>&1 | grep mean_volume
  ```
  Compare the window's RMS to the **measured noise floor F** (2a), NOT to a fixed dB: if window RMS > `F + ~10dB` it contains audible content (laugh, breath, reaction) — keep it. A hard-coded `-30dB`/`-25dB` cutoff fails on noisy mics whose floor already sits above it — it then "protects" pure room tone as if it were a laugh, which is exactly how dead air survives. Use `ffmpeg -i audio.wav -af "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level"` for per-window RMS. (And remember the low-dynamic-range guard in 2a: when `S − F < ~8dB`, RMS can't tell a laugh from room tone either — fall back to MFA/word-onset timing and surface anything ambiguous in the plan for the user to judge.)
- **Comedic beats.** A deliberate pause after a punchline. In `aggressive` mode, still trim to 0.4–0.6s (don't kill it, just tighten).
- **Reaction sounds.** Sighs, "ooh", "wow", gasps — all content.
- **Single-word punchlines.** If a sentence ends with a one-word zinger after a beat, keep the beat.

### 2f. STRICTNESS PASS — zero tolerance for repetitions (Louise, 2026-06-10: "get rid of ANY repetitions")
After building the keep list, run a machine scan — do NOT trust your eyes on the transcript:
1. **Scan the MFA words that fall INSIDE kept ranges** for (a) consecutive duplicate words, (b) duplicate bigrams ACROSS segment boundaries (a flubbed restart can straddle a cut — "…meet her. And we're [flub] / And we're going to…" survived a snap once), (c) duplicate sentence-openers in adjacent sentences ("So… So…" → cut the second).
2. **Cut hedge flubs** even mid-stat: "I believe", opener "Like", "I guess". Keep rhetorical repetition (parallel structure) — that's intentional.
3. **When excising a word, cut to the FULL MFA word end (+0.01s)** — a 15ms vowel residue still reads as the word.
4. **MFA OOV trap (burned 2026-06-10): acronyms/names missing from MFA's dictionary ("AI", brand names) silently VANISH from the alignment** — the word gets absorbed into its neighbor, and snapping a keep-end to "the last MFA word" then CLIPS the real spoken word. Guard: if whisper's chunk end exceeds the last MFA word end by >0.2s, trust the LATER of (whisper end, next silencedetect onset) for that boundary — and verify that junction with an isolated-segment transcription.
5. **Verification trap: whisper-of-the-output LIES twice.** It (a) COLLAPSES surviving stutters (a real "and we're… and we're" transcribes once — looks clean, isn't), and (b) HALLUCINATES context words at cut junctions (a "girls"+"Enjoy" junction transcribes as "So enjoy" — looks dirty, isn't). So verify with BOTH: the kept-range MFA dup-scan (catches real stutters), and per-segment isolated transcription of any suspect junction (clears hallucinations). Only ship when the dup-scan returns NONE.
6. **⭐ CROSS-ASR VERIFICATION — the strongest stutter detector (discovered 2026-06-10).** The MFA dup-scan only sees the words WHISPER transcribed — if whisper collapsed a phrase retake ("with the most recent video… with the most recent video" → once), MFA never knows it exists and the scan passes a dirty cut. The fix: **run the cut through a SECOND, independent ASR and diff.** Tella's transcript after upload is perfect for this (different model → different blind spots): it caught 5 repetitions in one pass that the whisper+MFA pipeline certified clean (a doubled phrase, a surviving "or, or", two mid-word fragments "pers-"/"per-", a doubled "into"). Workflow: upload the cut to Tella (or any second ASR) → scan ITS transcript for dup words/bigrams/phrases and mid-word fragments ("xyz-") → map hits back to source times → cut → re-verify. Disagreement between the two ASRs marks exactly the regions to fix or flag to the user.

## Step 2.5 — GROUND-TRUTH every keep boundary with isolated windows (added 2026-07-02 — this step saved the whole run)

MFA gives you the take STRUCTURE (what was said, roughly where). It does not reliably give you cut times on retake-heavy or noisy footage. Before rendering, re-transcribe **every region you plan to keep** in an isolated ±few-second window with `small.en` — within a short window whisper's word times are accurate, and it hears words the full pass dropped ("bland", "slop") and retakes the full pass collapsed ("It turns out— it turns out…").

```bash
# windows: name:start:duration — start ≥0.5s BEFORE the expected onset
for n in "r1:5.5:8.4" "r2:17.0:6.0" "r3:30.5:6.0"; do
  f=${n%%:*}; rest=${n#*:}; o=${rest%%:*}; t=${rest##*:}
  ffmpeg -y -hide_banner -loglevel error -ss $o -t $t -i audio.wav gt/$f.wav
  whisper gt/$f.wav --model small.en --word_timestamps True --output_format json --output_dir gt --language en >/dev/null 2>&1
  python3 -c "
import json
d=json.load(open('gt/$f.json'))
print('=== $f (+$o) ===')
for s in d['segments']:
    for w in s.get('words',[]):
        print(f\"{$o+w['start']:7.2f}-{$o+w['end']:7.2f} {w['word']}\")"
done
```
(That loop is zsh-safe — don't use `set -- $var`, zsh doesn't word-split unquoted variables.)

Rules for reading the windows:
- **Window-edge words are stretched and untrustworthy.** A first word spanning from exactly the window start, or a last word ending at the window end, was clipped — its true onset/offset is outside the window. Re-window with the boundary moved ~1s outward before using that time.
- **Stretched words INSIDE a window hide audio too** — `small.en` collapses within-window repeats just like the full pass ("to" spanning 93.1–97.9 contained an entire abandoned take). Re-window tighter around any word ≳1s. Sometimes what's inside is a **complete clean take** that neither full-pass ASR surfaced — check before assembling a splice from fragments.
- **Two windows can disagree about the same words** (one caught a flub the other clipped). Resolve with a third window positioned so the disputed moment sits mid-window, away from both edges.
- Final keep times: pad onset −0.03s, offset +0.04–0.08s (tight — stacked +0.10 pads across 20 keeps add 2s of mush).
- **Trim pauses INSIDE kept takes too (added 2026-07-02 — "even less silences").** Removing retakes and inter-take gaps is not enough: fluent takes still carry mid-sentence beats ("…for a living, [0.3s] I want to know…") and they add up. Scan the ground-truth words within each keep for inter-word gaps > 0.2s and trim each to ~0.1s (cut `[gap_start+0.05, gap_end−0.05]`). Leave deliberate rhetorical beats ("median… or average") no shorter than ~0.15s.
- **Stretched-word trap, keep-side (burned 2026-07-02):** a drawn-out spoken word looks identical to word+trailing-pause in the ASR ("slooop" transcribed as `slop 285.08–286.32`). Trimming what looks like the pause half CLIPS THE WORD mid-vowel. Before trimming into any stretched word at a keep boundary, re-window it tightly to find where the voice actually stops — and if the post-render verify transcript is missing a word that was there before, your trim ate it: push the boundary back out.

Cost on a 5-min video: ~10–15 windows × a few seconds of `small.en` each ≈ 2 minutes. It is the difference between a clean cut and re-doing the whole back half.

## Step 3 — Show the plan, render immediately

**Do NOT wait for approval — print the summary and start the render in the same turn** (changed 2026-07-09: the approval gate cost Louise a wasted wait when she didn't notice the question; the render is non-destructive and cheap to redo, so render-first is strictly better). Print this summary, then go straight to Step 4:

```
Original duration: 7m 25s
Cleaned duration: 3m 58s
Cut: 3m 27s (47%)
Total keep intervals: 312
Median cut duration: 1.2s (target: 1.1–1.5s)
Hard cuts (dead air > 3s removed): 23
Filler hits: 47
Hedge/transition cuts: 89
False-start drops: 12
Notable preserved long pauses: list timestamps + context (laughs, punchlines)
```

**Self-check vs benchmark:**
- If median cut > 2s → not aggressive enough. Tighten gap thresholds or expand hedge list, retry.
- If median cut < 0.7s → over-cut. Likely killing breath/cadence. Loosen 0.25–1s threshold to 0.3s.
- Target compression: 40–60% in aggressive mode.
- **Exception — retake-heavy footage (2026-07-02):** when most of the runtime is abandoned takes, the compression comes from dropping whole lines, not word-level slicing — median keep lands at 3–5s and compression at 65–75%, and that's CORRECT. Judge by compression % and final-script cleanliness instead; do NOT force extra mid-sentence cuts into fluent kept takes just to hit the 1.1–1.5s median (that target is for filler-dense monologue where nothing is re-recorded).

Run the self-check yourself and fix violations before rendering — that's the quality gate now, not the user. Then render immediately. The user reviews the *result*; if a cut killed a laugh or an intentional pause, adjust the keep list and re-render (fast — trim/concat, not re-transcription).

## Step 3.5 — Manual timeline editor (OPTIONAL — only when Louise asks for it)

(Demoted from always-on 2026-07-02: Louise found the editor fiddly in practice and prefers the pipeline to just cut tighter automatically — the intra-take pause trimming in Step 2.5 came out of that. Generate the editor only if she asks to review/adjust by hand.)

A timeline editor so she can trim silences and drop anything she doesn't want, before (or after) the render:

```bash
# keeps.json must be [start, end, "transcript text"] triplets in the working dir;
# needs proxy.mp4 (and ideally audio.wav) in the same dir. Generates wave.png once.
python3 ~/.claude/skills/cut-video/make_review.py /tmp/cut-video/$NAME
open /tmp/cut-video/$NAME/review.html
```

What the page gives her (self-contained HTML next to `proxy.mp4`, no server needed — waveform peaks and silence suggestions are embedded in the file, so it works on `file://`):
- **Canvas waveform timeline of the FULL source**, crisp at every zoom. **Pinch or ctrl/⌘+wheel zooms centered on the cursor** (continuous, fit → 400px/s); mouse wheel pans; +/−/Fit buttons too. Click to scrub; playhead synced to the video.
- **Drag ACROSS the waveform to delete that range** — the primary silence-removal gesture: see a flat stretch, swipe it, gone. Works across block boundaries (trims/splits/removes whatever it covers).
- **Amber hatched bands = auto-suggested silences inside keep blocks** (peak-based, adaptive threshold — computed by the generator and embedded). Click a band to cut it (leaves 0.1s of pause at each side), or **"✂ Cut all"** with a min-duration slider to sweep every suggestion at once. On noisy mics the suggestions degrade — they're visual candidates, she judges.
- **Drag a block's edges** to trim; the video seeks live while dragging so she hears the cut point. Selected edge nudges ±0.05s (buttons or ←/→, shift = 0.25s).
- **Split at playhead** (`S`), **drop/restore** a block (`D`/⌫ or click its card), **double-click a gap** to resurrect cut footage, **undo** (`Z`, 60 levels).
- Card list below with per-segment ▶ and transcript text; **"Preview final cut"** plays kept blocks back-to-back, skipping cuts — the render, live, without rendering.
- **"Copy decisions for Claude"** copies `{"keeps": [[a,b], ...]}` — the full edited keep list in source-proxy seconds.

Applying her decisions: the pasted `keeps` array REPLACES the old keep list — carry transcript text over by time-overlap with the previous `keeps.json` (blocks she created from gaps have no text; label them "(restored)"), rebuild `filter.txt`, re-render. The proxy is already there, so a revision costs seconds.

Boundary hygiene: her hand-dragged edges are intentional — do NOT re-snap them to MFA/ASR word boundaries. Only warn if an edge lands mid-word per the ground-truth words (say which word and offer the nearest clean boundary).

## Step 4 — Render with `trim` + `concat`, NOT `select`

**Critical:** Use the trim+concat filtergraph pattern, NOT `select`/`aselect`. The select filter compresses video frames but does NOT properly compress audio PTS, leaving audio and video misaligned.

Build a filtergraph with one trim+atrim pair per keep interval, then concat them:

```
[0:v]trim=A1:B1,setpts=PTS-STARTPTS[v0];
[0:a]atrim=A1:B1,asetpts=PTS-STARTPTS[a0];
[0:v]trim=A2:B2,setpts=PTS-STARTPTS[v1];
[0:a]atrim=A2:B2,asetpts=PTS-STARTPTS[a1];
...
[v0][a0][v1][a1]...concat=n=N:v=1:a=1[outv][outa]
```

Write the filtergraph to a file (it'll get long — aggressive cuts mean 200–400 intervals on a 7-min source) and use `-filter_complex_script`. Render call:

```bash
ffmpeg -y -hwaccel videotoolbox -i /tmp/cut-video/$NAME/proxy.mp4 \
  -filter_complex_script /tmp/cut-video/$NAME/filter.txt \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  /tmp/cut-video/$NAME/cleaned.mp4
```

**Faster alternative for many cuts:** if filtergraph exceeds ~500 trims, switch to per-segment extract + lossless concat:
1. Extract each keep interval as a separate stream-copied chunk
2. Build a concat demuxer file
3. `ffmpeg -f concat -safe 0 -i concat.txt -c copy cleaned.mp4`

This avoids re-encoding entirely on the trim pass.

## Step 5 — Deliver

- Save final to `<source_dir>/cut_out/<source_name>_cut.mp4` (mkdir if missing)
- Print one line: original duration → cleaned duration, percent cut, median cut, output path
- `open` the file so the user can review immediately
- Revisions are cheap: the proxy + ground-truthed times stay in the working dir, so "drop the second segment" / "tighten X" is a seconds-fast re-render. (If she asked for the Step 3.5 editor, remind her it's still live for pasting decisions back.)
- Offer to iterate: re-tune gap thresholds, switch tone preset, mark specific moments to preserve/cut

---

## Pitfalls — don't repeat these (learned from prior runs)

- **Don't skip `-hwaccel videotoolbox`** on the proxy step. HEVC software decode on a 7-min 4K source can take 5+ minutes. With the flag, ~30s.
- **Don't use the `select` filter for cuts.** It misaligns audio. Use trim+concat.
- **Don't use `-preset medium` (the libx264 default).** It's ~3× slower than `-preset fast` for no quality gain on a working copy.
- **Don't wait for approval before rendering** (changed 2026-07-09 — the gate wasted more time than it saved). Print the plan, render immediately. The old worry (a "silent" gap holding a laugh, a "filler" that's intentional emphasis) is handled by the amplitude check below + preserved-pauses list in the summary — and a bad cut just means a quick re-render.
- **Don't trim a long "silence" without checking amplitude** — that's usually laughter, a thinking pause, or a setup-payoff beat.
- **Don't `whisper` the entire raw source if a proxy exists.** Run whisper against `audio.wav` extracted from the proxy.
- **Don't re-encode audio twice.** If you only changed video, use `-c:a copy` to skip an unnecessary AAC pass.
- **Don't be timid.** Default to `aggressive`. The reference cut style is fast — if the output feels "safe", it's not matching Louise's CapCut pacing.
- **Don't render from MFA times alone on retake-heavy or noisy footage.** Measured 1–6s drift on the 2026-07-02 DJI run. Ground-truth every keep boundary with isolated windows (Step 2.5) first.
- **Don't scale a portrait source to 1920:1080.** Probe orientation first; DJI/phone footage is usually 9:16.
- **Don't trust window-edge word times** from an isolated transcription — a word touching the window boundary is clipped/stretched; re-window before using it as a cut point.
- **`h264_videotoolbox -b:v 8M` is fine for the final render too**, not just the proxy — the whole 4K-HEVC→proxy→18-segment render finished in ~1 min total on M-series.

## Benchmark reference

`AI mogging my dad.mp4` (2026-05-03, CapCut project `0501`):
- 335 cuts in 460s = 1 cut / 1.37s
- Median 1.13s, mean 1.37s
- 41% of cuts < 1s, 12% < 0.5s
- Only 3 cuts > 5s
- Raw source compressed ~60%

Use this as ground-truth for "aggressive" mode tuning.

## What this skill explicitly does NOT do

- Add zooms, layouts, or motion graphics (separate concern — handled in CapCut or via [[tella-edit]])
- Add memes or b-roll (user-curated, see [[clipify]] for short-form cuts)
- Burn captions (separate pass after cleanup)
- Upload anywhere

Keep this skill focused on one thing: produce a tighter MP4 from a long-form recording, fast and aggressive.
