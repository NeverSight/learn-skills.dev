---
name: suggest-sfx
description: The SFX pass. Analyze a short's beats + narration and propose tasteful sound effects synced to them, drawing from (and growing) a shared, reusable SFX library, then render an SFX-mixed audition preview. Use when the user wants to "add SFX / sound effects", "suggest sfx", "score the transitions", "sound-design this beat", generate/source sound effects, build or extend the sfx library/catalog, author or audit a sfx-plan, or mix SFX over a rendered short in this repo. Covers reading beats + word times + brand §7, the library-first flow, generating misses with the ElevenLabs Sound Effects API, the per-video sfx-plan.json, the hard user-audit gate, and mixing with tools/mix_sfx.py (light voice ducking).
---

# suggest-sfx — the SFX pass

Take a rendered, voiced short and add **tasteful sound effects**, synced to the visual beats and
the narration, drawn from a **shared, growing SFX library**. Work **collaboratively and
beat-by-beat**; the user audits the plan and gives notes.

The shape: a **declarative plan** (`sfx-plan.json`) is the source of truth → a **tool** consumes it
(`tools/mix_sfx.py`) → a **library** grows (`media/library/sfx/`) → a **hard USER-AUDIT gate**
before anything is mixed.

Sound taste is a brand contract — read **`brand.md` §7** every time. The house style is calm/premium
(Linear / Anthropic / Vercel), felt-not-heard, always under the voice. NOT MrBeast-loud.

## Inputs (read these first, every session)

- **`brand.md` §7 (Sound design)** — the SFX taste contract: subtlety, density, palette, levels,
  sync, signature motifs, source policy. Non-negotiable.
- **`shorts/short-N-<niche>/beats.json`** — the beats and REAL per-word voice times (written back
  by `gen_voice.py`). Sync cues to these words (a pop on "boom", a chime on "free").
- **The shot source** `remotion/src/shots/short-N/*.tsx` — the INTERNAL animation frames are where
  the real visual beats are (piece lands, digit pops, badge stamps). Read the shot, convert its
  local frame to global time: `at_s = (local_frame + sequence_from) / fps`. Do not guess — the
  cue must land on the exact frame the thing happens.
- **`media/library/sfx/catalog.json`** + **`palette.json`** — the library you draw from and grow.

## The library (`media/library/sfx/`) — the durable asset

- `palette.json` — generation recipes: generic, reusable sound ids + prompts + duration + tags.
  The source of truth for what the library SHOULD contain.
- `catalog.json` — the manifest of what EXISTS: `{id, file, category, tags, duration_s, peak_dbfs,
  loudness_lufs, source, model, license, prompt, used_in}` per clip. Written by `gen_sfx.py`.
- `clips/*.mp3` — loudness-normalized clips (~−20 LUFS, −1.5 dBFS ceiling) so a plan's per-cue
  `gain_db` is perceptually meaningful.
- **Library-first, always.** Reuse an existing clip before generating. Name/tag clips GENERICALLY
  (`ui-toggle-on`, `whoosh-soft`, `pop-reveal`) so future videos reuse them — the library is the
  durable asset, each video is one draw from it. Only genuinely-missing sounds get added to
  `palette.json` and generated.

## Workflow

1. **Read** brand §7 + beats.json + the shot source + catalog. Pull exact cue times: for each
   candidate beat, find the visual moment's local frame in the shot and/or the narration word,
   and convert to global seconds.
2. **Decide taste with the user up front** if unsettled (present-ness, density, which kinds,
   source) — then apply brand §7. Don't re-ask settled decisions.
3. **Propose the cue list — function-first.** For each beat ask what it needs (brand §7): **motion**
   (whoosh) · **tension** (riser) · **emphasis** (impact/pop) · **snap** (click). Score key
   transitions, reveals, and tasteful click-sequences; a 3–4-shot click-sequence counts as ONE
   gesture. Mark genuinely deniable texture as `"optional": true`. **Layer the 2–3 biggest moments**
   (build-and-drop): riser→impact on a scripted reveal, whoosh→pop so a cut stands out — in the
   plan a layer is two events at the same/adjacent `at_s` that sum. Sync each cue to the VISUAL
   beat and often the exact word.
4. **Library-first sourcing.** For each distinct sound the plan needs, reuse a catalog clip if one
   fits. For misses, add a generic recipe to `palette.json` and generate: `python tools/gen_sfx.py`
   (ElevenLabs Sound Effects API → normalized clip → catalog). Fall back to curated royalty-free
   only where generation is weak; record `source` + `license` either way.
5. **Author `shorts/short-N-<niche>/sfx-plan.json`** — one event per cue, `at_s` in global seconds.
   (Schema below.)
6. **USER-AUDIT GATE (hard).** Present the resolved cue sheet
   (`python tools/mix_sfx.py <plan> --print`) and get the user's approval/notes BEFORE mixing.
7. **Mix the audition preview** once approved: `python tools/mix_sfx.py shorts/short-N-<niche>/sfx-plan.json`
   → the plan's `render.out`. Light sidechain duck under the voice + a safety limiter. Iterate on
   the user's notes (gains, timing, add/cut cues) — re-print, re-mix.
   - **Verify audibility with numbers, not hope.** After mixing, RMS-diff the mixed audio vs the
     voice-only preview at each cue window: a story-critical cue should add **≥ +4 dB**, texture
     +1–3 dB. Inaudible cues hide in cue sheets — don't ship a cue you haven't confirmed lands.
   - **Transient-clip gain gotcha.** Short percussive clips (knock/stamp/keys/snap) hit the
     −1.5 dBFS peak ceiling BEFORE reaching the −20 LUFS loudness target, so they catalog ~3–5 dB
     quieter than sustained clips. Their plan `gain_db` must be **~3–5 dB higher** than the brand
     table implies. The audibility check above is what surfaces this.
   - **SHORTS calibration.** Under a short's near-continuous narration (~2.7 w/s, few gaps) a
     conservative gain table is **4–8 dB too quiet across the board** — the duck + voice masking
     eat everything. Proven landing zone: transitions/whooshes **−3**, story pops/impacts **0..+3**,
     stamps/snaps **0..+7**, layered-hero risers **0..+2**. Start a short's plan there.
   - **Cues that sit fully UNDER continuous speech never measure — accept felt-not-heard or cut
     them.** The sidechain duck suppresses quiet clips the whole time the voice is active (a
     click-sequence can measure +0 dB at ANY gain). Set such cues at a sane +6-ish and let them
     live in the word gaps, or delete them; do NOT chase them with gain (a pause would make them
     spike).
   - **Measure transients with tight windows.** RMS over 0.6s dilutes a 50 ms click to nothing and
     an adjacent loud cue can leak in and fake a pass. Use ~0.3s windows for snap/pop/zap/stamp,
     and measure a riser at its final third (its energy is at the END).
   - **A noisy TEXTURE cannot be fixed by gain.** Static/glitchy/hummy clips read as NOISE over
     speech even at −4 dB; lowering them just makes quiet noise. If the user says "noisy", swap the
     sound's CHARACTER (clean mechanical snap) or use silence — see brand §7 "no static/glitch
     textures under narration".
8. **Save back.** New clips stay in the library + catalog (they carry to the next video). Update
   `used_in`.

## sfx-plan.json (the source of truth)

```jsonc
{
  "master": "remotion/out/ShortNName-voiced.mp4", "master_fps": 30,
  "catalog": "media/library/sfx/catalog.json",
  "render": {
    "preview": "remotion/out/ShortNName-voiced.mp4",   // the voiced render to mix over
    "out": "shorts/short-N-<niche>/output/short-N-sfx.mp4",
    "end_s": 42, "duck": true
  },
  "events": [
    { "at_s": 4.9, "sfx_id": "chess-piece-thock", "gain_db": -8, "shot": "MainScene",
      "cue": "e4 pawn lands (local f51)", "note": "diegetic board foley" },
    { "at_s": 13.03, "sfx_id": "ui-click-soft", "gain_db": -18, "optional": true, "cue": "card locks" }
  ]
}
```

- `at_s` — global-timeline seconds (same clock as beats.json).
- `gain_db` — dB relative to the clip's normalized level (lower = quieter). See the SHORTS
  calibration above for starting values.
- `optional: true` — deniable texture; `mix_sfx.py --no-optional` drops it. Use it liberally so
  the audit is about the core set.
- `cue` / `note` — human-readable anchor (the exact frame/word) so the audit is legible.

## Tooling quick reference

- Grow the library: `python tools/gen_sfx.py [--dry-run] [--only id1,id2] [--force] [--renorm]`.
  `--renorm` re-balances existing clips to the loudness target (no API/billing). Needs
  `ELEVENLABS_API_KEY` in `.env`.
- Print the cue sheet (the audit artifact): `python tools/mix_sfx.py <plan> --print [--no-optional]`.
- Mix: `python tools/mix_sfx.py <plan> [--no-optional] [--no-duck] [--end S] [--out path]`.

## Principles (the house style — apply them)

- **Under the voice, always.** SFX are seasoning; the voice is the show. Duck them, keep them
  quiet, never let one peak above the narration. Silence is part of the mix.
- **Key transitions & reveals only** — plus the diegetic action sounds that ARE a synthetic short's
  content (piece thocks, digit pops). Everything past that is `optional`.
- **Sync to the visual beat AND the word.** A click exactly on the toggle flip; a pop exactly on
  the reveal. Off-by-100ms reads as sloppy — use real frame/word times.
- **Reusable-first.** Generic names + tags so the library compounds across videos. Reuse before
  you generate. The library is the deliverable that outlives this video.
- **Function over vibe.** Pick the sound by its job — motion/tension/emphasis/snap (brand §7) —
  not by browsing the catalog for something that "feels right." The same few foundational sounds
  do the heavy lifting; more is not better. Keep signature motifs consistent.
- **Layer the big moments, keep the rest single.** Build-and-drop (riser→impact, whoosh→pop) is
  where SFX earn their keep — but only on the 2–3 hero beats.
- **Take structure, not drama.** Calm/premium: no cymbal-urgency risers, no trailer slams, no
  whoosh on every move.
- **Audit before mixing.** The user reads and approves `sfx-plan.json` first. Non-negotiable.

Done = the library has the needed clips (catalogued with source+license), `sfx-plan.json` is
authored and **audited by the user**, the SFX-mixed preview is rendered and spot-checked by ear,
and any new clips + `used_in` are saved back to the library.
