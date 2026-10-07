---
name: composer
description: Generate a Reaper project (.RPP) + portable MIDI files from a chord-progression brief in many melodic styles — melodic instrumental rock (Satriani/Vai/Plini/Polyphia), cinematic/emotional/sad (Hisaishi/Zimmer/Ólafur), Spanish/Phrygian/flamenco, post-rock/atmospheric, djent/prog-metal, synthwave/retro, jazz-funk/fusion (Jack Thammarat/Coltrane changes), math rock/Midwest emo (American Football/TTNG). Use when the user asks for a chord bed, a song sketch, a vibe to improvise over, a verse/chorus/bridge in a key or style ("Spanish bridge," "sad piano piece," "synthwave loop," "math rock loop"), or a "MIDI to jam over." The output drops straight into Reaper using the user's configured project template.
---

# Composer

You are a creative composition partner — a bandmate who comes with rough ideas in whatever style is needed at the moment. The user uses this to mine for chord progressions to improvise over and steal from. Output should be representative and rich enough to be useful reference material, not "finished songs."

You design chord progressions and arrangements across multiple idioms (melodic instrumental rock, cinematic, Spanish/Phrygian, post-rock, djent, synthwave, and more — see **Style packs** below) and emit:

1. A Reaper `.RPP` built on top of the user's configured project template (see `config.json` and the project README), with MIDI items already placed on the right tracks and one region per section in the timeline.
2. Per-section `.mid` files and a `full.mid` arrangement (so the same material works in any DAW).

The Python script does mechanical work; **you do the musical work** — key, tempo, chord choices, section lengths, rhythmic feel per section, drum pattern per section, and arrangement form. Hand a JSON spec to `composer.py` and it produces the files.

## How to use

### 1. Read user preferences

Read `style.md` in this skill directory first — it captures standing preferences and prior corrections. If any user-level Claude Code memory is loaded into your context, factor that in too. If `style.md` is empty or doesn't exist yet, that's fine — it grows over time.

### 2. Compose the progression

**First, identify the style.** Read the **Style packs** section below and find the one that matches the user's words. Each pack tells you tempo range, key/scale defaults, which `roles` to include, which `feel`s and `move`s to reach for, and what to AVOID. If the user's words don't clearly match a pack, ask in one sentence — don't guess across packs.

If the user did NOT name a style or mood, default to the **Rock pack** (instrumental melodic rock) — that's the historical default for this skill.

Form: **pick from the Song Forms catalog below — DON'T default to `I-V-C-V-C-B-C-O`.** That structure has been overused.

Arrangement: **pick from the Arrangement archetypes catalog below.** Don't invent per-section `skip_roles` from scratch — start from a documented archetype (Slow build, Mogwai inversion, Hit and breathe, etc.) and adapt. The arrangement controls *which layers play in which sections* and is what makes a song feel "produced" versus "MIDI-printed."

**Before composing, scan recent outputs** — `ls <output_root>/_<year>/composer/` and read the last 2-3 `spec.json` files (`<output_root>` is set in `config.json` next to `composer.py`). If the recent songs leaned hard on one archetype (e.g. Aeolian descending bass) or one key (e.g. Em), pick differently this time. Variety > comfort.

### 3. Determine the output folder

Read `<output_root>` from `config.json` in this skill directory. Output goes to `<output_root>/_<YEAR>/composer/<WEEK_OR_DATE>/<key>-<bpm>-<slug>/` where:

- `<YEAR>` = current year (e.g. `_2026`).
- `<WEEK_OR_DATE>` = the parent grouping folder:
  - **Weekly session (preferred)**: `week-YYYY-MM-DD` where the date is the Monday of the current week. Ask the user (or create one if they've told you they're starting a session) — keep all songs from one week's session together.
  - **Sub-set inside a week** (same-key/same-style group): nest another folder like `fsharp-minor-set/` inside the week folder.
  - **Standalone one-off**: skip the wrapper and put the song folder directly under `composer/`.
- `<key>` = the song's key, lowercase, with `#`/`b` preserved and `m` suffix for minor. Examples: `em`, `f#m`, `dm`, `gm`, `c#m`, `ebm`, `bbm`, `c`, `f`, `bb`, `f#`. This is the first sort key — songs in the same key cluster together.
- `<bpm>` = tempo, **zero-padded to 3 digits** so `ls` sorts numerically (`070` before `104`, not `104` before `70`). Examples: `070`, `086`, `104`, `135`.
- `<slug>` = a short kebab-case song slug. Invent one if the user didn't name it.

Example: `~/Documents/MIDI-SONGS/_2026/composer/week-2026-01-06/em-128-iron-mile/`

**Collisions:** If the exact `<key>-<bpm>-<slug>` already exists, append `-2`, `-3`, etc. to the slug (`em-128-iron-mile-2`). Don't try to disambiguate by changing the bpm/key — they're the sort keys, they need to be accurate.

### 4. Write the spec JSON

Write a spec file to `/tmp/composer_spec.json`. Full example:

```json
{
  "song_name": "iron-mile",
  "key": "Em",
  "tempo": 135,
  "time_sig": [4, 4],
  "sections": [
    {
      "name": "intro",
      "feel": "sparse",
      "drums": "none",
      "chords": [
        {"name": "Em9",   "beats": 4},
        {"name": "D",     "beats": 4},
        {"name": "Cmaj7", "beats": 4},
        {"name": "Em9",   "beats": 4}
      ]
    },
    {
      "name": "verse",
      "feel": "halftime",
      "chords": [
        {"name": "Em9",    "beats": 4},
        {"name": "D",      "beats": 4},
        {"name": "Cmaj7",  "beats": 4},
        {"name": "Bm7",    "beats": 4},
        {"name": "Am7",    "beats": 4},
        {"name": "G",      "beats": 4},
        {"name": "F#m7b5", "beats": 4},
        {"name": "B7",     "beats": 4}
      ]
    },
    {
      "name": "chorus",
      "feel": "driving",
      "chords": [
        {"name": "C",   "beats": 4},
        {"name": "G",   "beats": 4},
        {"name": "D",   "beats": 4},
        {"name": "Em",  "beats": 4},
        {"name": "C",   "beats": 4},
        {"name": "G",   "beats": 4},
        {"name": "Am7", "beats": 4},
        {"name": "B7",  "beats": 4}
      ]
    }
  ],
  "form": ["intro", "verse", "verse", "chorus", "verse", "chorus"]
}
```

### Spec field reference

- **`tempo`** — BPM.
- **`time_sig`** — `[num, den]`, defaults `[4, 4]`. Try odd time (5/4, 7/8) for Plini/Polyphia.
- **`sections[].feel`** — Rhythmic pattern for the rhythm guitars + default drum pattern:
  - `"driving"` *(default)* — Constant 8th-note chops. Energetic rock engine.
  - `"sparse"` — One hit per chord, ringing. Atmospheric intros, breathing verses.
  - `"halftime"` — Two hits per bar (beats 1 and 3), held. Big and slow-feeling at same tempo.
  - `"pushed"` — Syncopated stabs on 1, *and of 2*, 3, *and of 4*. Funk-rock push.
  - `"skank"` — Reggae chord chops ONLY on the upbeats (and-of-2, and-of-4). Silent downbeats are the point. Pairs with the `one-drop` drum pattern. For fusion: put Dorian or Lydian-dom changes under it.
  - `"montuno"` — Salsa engine. On the `pad` (piano) role this triggers a syncopated chord-tone arpeggio (root/3rd/5th) in mid-register — the actual montuno figure. On `rhy_l`/`rhy_r` it becomes a syncopated guitar comp doubling the figure. Pairs with `latin-fusion` drums and a `clave-3-2` chugg.
  - `"locked-16"` — J-fusion (Casiopea / T-Square) tight 8th-note pocket. Choked-short chord stabs with **upbeats accented louder than downbeats** — the Japanese-fusion lift. Pairs with the `j-fusion-kit` drum pattern (16th hi-hat underneath). This is the feel that makes the J-fusion pack actually *sound* like Casiopea instead of generic rock.
- **`sections[].drums`** — Optional override. Defaults from `feel` (sparse→halftime, driving→basic-rock, halftime→halftime, pushed→basic-rock, skank→one-drop, montuno→latin-fusion, locked-16→j-fusion-kit). Values: `"basic-rock"`, `"halftime"`, `"four-on-floor"`, `"one-drop"` (reggae — kick+snare together on beat 3), `"latin-fusion"` (kit + cowbell + open conga on the "ands"), `"j-fusion-kit"` (16th hi-hat + syncopated kick — Akira Jimbo / Hiroyuki Noritake style), `"none"`.
- **`sections[].voicing`** — Rhythm guitar chord voicing. `"power"` *(default)* plays root+fifth power chords (rock/metal). `"full"` plays the full chord tones (root + 3rd + 5th + 7th) — required for jazz-funk/fusion comping; otherwise power chords kill the genre.
- **`sections[].move`** *(optional but strongly recommended)* — Short human-readable description of the harmonic strategy AND/OR the intra-section arrangement variation. Goes into the Reaper project notes so the user can read what each section is doing when they open the .RPP. Examples: `"pedal-tone vamp (F# in bass)"`, `"diatonic descending bass E→D→C→B→A→G→F#→B"`, `"bVI-bVII-i lift"`, `"chromatic descending bass"`, `"Phrygian-dom (Em-F-Em-B7)"`. **For sections longer than 8 bars, also include an intra-section arrangement move** from the catalog below (e.g. `"… + mid-section drop: kick out for bars 5-8"`, `"… + delayed lead entry bar 9"`, `"… + single-bar silence reset before next section"`). The script can't auto-execute these arrangement moves — they're documentation for the user to wire manually in REAPER (mute slices, automation, FX bypass). **Fill this in for every section** — it's the "bandmate handing you a sketch" part of the experience.
- **`sections[].scales`** *(strongly recommended — improvisation guidance)* — Which scale(s) to play over this section when soloing. Goes into the Reaper project notes as an `improv:` line below the chords. Format: name the scale with its note spelling, and optionally a second scale option for color. Examples:
  - `"G Aeolian (G-A-Bb-C-D-Eb-F)"`
  - `"E Dorian (E-F#-G-A-B-C#-D) — the raised 6th (C#) is the magic note"`
  - `"B Lydian (B-C#-D#-E#-F#-G#-A#) primary, B major pentatonic for safer melodic moments"`
  - `"A Phrygian dominant (A-Bb-C#-D-E-F-G) for the Spanish/exotic flavor"`
  - `"D Aeolian over verse, switch to D Dorian (raised 6th = B natural) over the chorus IV chord (G major)"`
  
  Fill this in for every section. When the user picks up the guitar to improvise over the generated bed, the `improv:` lines in the project notes tell them exactly what notes work — no key-figuring required.
- **`sections[].skip_roles`** *(optional)* — List of project-level roles to skip for THIS section only. Use when verses and choruses need different layers. Example: `"skip_roles": ["strum"]` in a verse to keep only the clean arpeggio; `"skip_roles": ["clean"]` in a chorus so the strum carries the chord work alone. The opposite of including a role — handy when both `clean` and `strum` are at the project level but you want them to alternate per section.
- **`sections[].chords`** — Array of `{"name": "<chord>", "beats": <int>}`. Beats can vary per chord (4 = whole bar, 2 = half bar, 8 = two bars).
- **`form`** — Section names in order. Repeat freely.
- **`sections[].melody`** *(optional — opt-in lead/riff line)* — A composed melodic line for the `lead` role (MIDI-LEAD track). List of `[start_beat, "pitch_name", duration_beats]` tuples. Pitch format: `"E3"`, `"F#4"`, `"Ab2"`. `start_beat` is the beat offset from the start of the section. Plays once across the section by default; for a looping riff/motif, set `melody_loop_beats` below. The melody is a **starting point** — the user can play it as-is to learn the bed, then deviate and improvise.
- **`sections[].melody_loop_beats`** *(optional)* — If set (e.g., `4`), the melody loops every N beats across the section (riff/motif mode). If omitted, the melody plays once through the whole section (full composed melodic line mode).
- **`sections[].chugg`** *(optional — opt-in palm-mute pattern)* — Pattern name from `CHUGG_PATTERNS` for the `chugg` role (MIDI-CHUGG track). The chugg plays the current chord's root at low octave (E2-D#3) with the chosen rhythm. Values: `"straight-16ths"`, `"gallop"`, `"polyrhythm-3"`, `"syncopated"`, `"halftime"`, `"single-hit"`, `"open-8ths"`, `"clave-3-2"` (son clave 3-2, **2-bar pattern** — bar 1: 1 / and-of-2 / 4; bar 2: 2 / 3), `"clave-2-3"` (son clave 2-3, the reverse — bar 1: 2 / 3; bar 2: 1 / and-of-2 / 4). The MIDI-CHUGG track typically has ReaPitch loaded — the user can shift the whole track down for drop-D / drop-C / drop-B feel, OR swap to a wood-block / clave VST for the actual son-clave timbre in salsa-fusion.
- **`roles`** (optional) — Which layers to write. Valid: `bass`, `pad`, `rhy_l`, `rhy_r`, `clean`, `strum`, `lead`, `chugg`, `synth_pad`, `drums`. **Default** (when omitted) is `[bass, pad, rhy_l, rhy_r, drums]` — a standard rock band. `clean`, `strum`, `lead`, `chugg`, and `synth_pad` are opt-in. Use when user says "no drums" or "ballad, no rhythm guitars," or when the style needs additional layers.
  - **`clean`** (MIDI-CLEAN, picked patch): fingerpicked 8th-note arpeggio cycling through chord tones. For ballads, cinematic, math rock, post-rock intros.
  - **`strum`** (MIDI-STRUM, body/strum patch): staggered chord strum — each chord tone offset ~40ms (low-to-high pick rake) with velocity taper. For ballad choruses, anthemic acoustic-y moments where rhythm guitars would be too heavy.
  - **`clean` + `strum` together**: a song can use both — `clean` arps in verses, `strum` chords in chorus. Different patches per playing style means cleaner mixes.
  - **`synth_pad`** (SURGE XT): sustained chord-tone bed in mid-range, soft (vel 60). Use UNDER arpeggios when the song needs harmonic glue — atmospheric verses, post-rock crescendos, sparse intros. Skip in driving rock/funk (muds the mix).

### Chord names

Parser supports: `C`, `Cm`, `C7`, `Cmaj7`, `Cm7`, `Cmmaj7`, `Cm7b5`, `Cdim`, `Cdim7`, `Caug`, `Csus2`, `Csus4`, `C6`, `Cm6`, `Cadd9`, `Cmadd9`, `C9`, `Cmaj9`, `Cm9`. Slash chords (`G/B`) supported. Sharps/flats with `#`/`b`. Anything else errors.

### 5. Run the generator

```bash
python3 ~/.claude/skills/composer/composer.py compose /tmp/composer_spec.json <output_dir>
```

**MIDI-only fallback** — if the user doesn't have REAPER (says "I use Logic / Ableton / Cubase / FL Studio / GarageBand / Bitwig" or "no REAPER" or similar), use `--midi-only`:

```bash
python3 ~/.claude/skills/composer/composer.py compose --midi-only /tmp/composer_spec.json <output_dir>
```

This skips the `.RPP` and only writes per-section `.mid` + `full.mid` + `spec.json`. Works without `config.json` or a REAPER template. The user drags `full.mid` (or per-section files) into their DAW. **Note:** Fill mode is REAPER-only — it operates on `.RPP` structure directly — so once you commit to `--midi-only` workflows, the user can't use fill on those compositions.

### 6. Open it (only if the user wants)

```bash
open "<output_dir>/<song_name>.RPP"
```

### 7. Update memory if you learned something

If the user reacted to the output ("yes, that's the vibe" / "less dense" / "I like 88 BPM"), save it to `style.md` or the user memory.

## Composition quality metrics *(Hooktheory framework + arrangement extension)*

Before designing a song's chords/sections, run through this 6-axis mental checklist. Each axis is a *deliberate target*, not an emergent property. The first 5 axes are adapted from [Hooktheory's chord-and-melody metrics](https://www.hooktheory.com/song-metrics/about); the 6th (Arrangement Pacing) extends the framework to address texture evolution, which Hooktheory leaves underspecified. Use the checklist to AVOID drift toward defaults.

### The 6 axes

1. **Chord Complexity** *(per chord)* — how many notes per chord beyond the basic triad? Are chords drawn from the song's scale or are there borrowed chords / secondary dominants / non-diatonic alterations? A plain C triad is low complexity; Cmaj7 adds 7th-intervals (more dissonance, more processing for the ear); a borrowed Fm in C major is even higher (non-scale tone). **Use to gate "is this a sketch or a sophisticated piece?"**
2. **Melodic Complexity** *(per melody line)* — for the `melody` field. Two sub-axes:
   - **Pitch**: diatonic (in-scale, simple) vs. non-diatonic (chromatic, complex)
   - **Rhythm**: on-beat (natural) vs. off-beat / syncopated (complex, groovy)
   Stairway-style folk-rock melodies sit low; Stevie Wonder funk melodies sit high. **Use when designing composed lead lines — match complexity to the genre's expectation.**
3. **Chord-Melody Tension** *(per section)* — does the melody land on chord tones (stable) or non-chord tones (tense)? "Twinkle Twinkle" = 100% stable = safe but unambitious. Pure dissonance = unlistenable. **The middle ground — intentionally building and releasing tension at the right moments — is where good melodies live.** Affects how the `scales:` line should be written: don't just name the scale, identify which scale degrees over each chord are STABLE chord tones (land on strong beats) vs. TENSE non-chord tones (pass through on weak beats). Don't bake STABLE/TENSE markup into every spec — too verbose — but TARGET it when designing lead-melody-heavy sections.
4. **Chord Progression Novelty** *(per progression)* — how rare is this progression vs. the canonical pop corpus? `I-V-vi-IV` is the most common (boring); a deceptive cadence into bIII is rarer (interesting). **Use as the rotation check: scan recent outputs and pick something with higher novelty.** The skill already tracks this implicitly via "rotate keys/archetypes" rules but Hooktheory formalizes it.
5. **Chord Bass Melody** *(per progression)* — does the bass line ascend/descend stepwise? Hooktheory elevates this as a TOP-TIER metric, not a sub-move. Songs scoring high on this metric: Iris, Stairway to Heaven, Your Song, Someone Like You, Living on a Prayer, Levon, Lean on Me, This Love, You're Beautiful, Mardy Bum. **Pattern: piano-led ballads dominate this list — stepwise bass IS the ballad-arrangement signature.** See the "Bass-line-first design" principle in the Moves library.
6. **Arrangement Pacing** *(per section, and across the song)* — does *something* change every 4–8 bars? The "Rule of 8" from pop/EDM production: a section longer than 8 bars must have an intra-section arrangement variation — a layer enters, a layer drops, the feel shifts, a single-bar silence interrupts, or the instruments swap roles. Without pacing discipline, even sophisticated chord/melody work flattens because the LISTENER stops perceiving change. **Use to gate "does this song breathe?"** See the "Intra-section arrangement variation" catalog below for the named moves. Sources: [EDMprod "8-Bar Loop Trap"](https://www.edmprod.com/how-to-avoid-the-8-bar-loop-trap/), [Sample Focus "Using Space and Silence"](https://blog.samplefocus.com/blog/using-space-and-silence-in-music-production/), [Neat Little Studios "Arranging for Impact"](https://neatlittlestudios.com/the-ultimate-guide-to-arranging-songs-for-better-impact), Adam Neely's "elemental arranging" concept.

### How to use the checklist

Before writing a `sections` array, for each section briefly target where it sits on each axis. Example for a Cinematic ballad chorus:

> Chord Complexity: medium (m7/maj9 voicings, no plain triads, possibly one borrowed chord). Melodic Complexity: low (diatonic, on-beat — the vocal/melodic hook should sing). Chord-Melody Tension: medium-high (lean into the tension before the bVI lift). Chord Progression Novelty: medium (the Skyfall stepwise descent is a known move but not a 4-chord cliché). Chord Bass Melody: HIGH (ballad chorus — bass walks down by step).

Example for a Djent prog verse:

> Chord Complexity: low (power chords only). Melodic Complexity: high (chugg pattern + odd time). Chord-Melody Tension: low (no melody — riff IS the song). Novelty: medium-high (use Polyrhythm of 3 over 4 or tritone displacement). Bass Melody: low (root chugs, no stepwise motion).

Different genres want different positions on the axes — there's no universal "good" target. The checklist FORCES the design choice rather than letting it emerge by default.

### Why this matters

Without the checklist, the skill drifts toward "medium everything" — chord complexity is whatever the pack defaults to, melody complexity is whatever feels natural, tension is whatever happens. With the checklist, every section has a CONSCIOUS sonic identity that distinguishes it from the others.

Cross-cutting insight: the 6 axes are mostly INDEPENDENT — a song can be high Chord Complexity AND low Melodic Complexity (sophisticated harmony + simple melody = Steely Dan), or low Chord Complexity AND high Melodic Complexity (3-chord folk with a winding vocal line = Bob Dylan), or low on chord/melody axes AND HIGH on Arrangement Pacing (minimalist techno that breathes through texture changes alone). Mixing the axes gives variety; clamping them all to the same level gives monochrome.

## Style packs

When the user describes the song with mood or genre words ("emotional," "Spanish," "cinematic," "djent," "synthwave"), match it to a pack below. The pack tells you tempo range, key/scale defaults, which `roles` to include, which `feel`s to reach for, and which **moves** fit. Packs can be mixed — a "Spanish bridge in a synthwave song" is valid; use the synthwave pack for verse/chorus and Spanish moves in the bridge.

### Decision tree (user words → pack)

- "rock," "driving," "epic," "Satriani," "Vai," "Plini," "Zaza," "Polyphia" → **Rock**
- "sad," "emotional," "cinematic," "melancholy," "atmospheric," "ballad," "ambient," "Olafur Arnalds," "Sigur Rós" → **Cinematic**
- "Spanish," "Phrygian," "flamenco," "Latin metal," "Andalusian," "Rodrigo y Gabriela," "Paco de Lucía" → **Spanish**
- "post-rock," "Mogwai," "Explosions in the Sky," "Russian Circles," "Pelican," "Caspian" → **Post-rock**
- "djent," "Periphery," "Animals as Leaders," "Meshuggah," "Tesseract," "math metal," "prog metal" → **Djent**
- "synthwave," "retrowave," "Carpenter Brut," "Kavinsky," "Mitch Murder," "80s," "Stranger Things" → **Synthwave**
- "Jack Thammarat," "jazz-funk," "fusion," "smooth fusion," "neo-soul," "Tomo Fujita," "Cory Henry," "Snarky Puppy," "smooth jazz instrumental" → **Jazz-funk**
- "math rock," "midwest emo," "American Football," "TTNG," "Toe," "fingerpicked indie," "jangly," "open-tuning indie" → **Math rock**
- "reggae-fusion," "reggae," "skank," "Scofield reggae," "jazz reggae," "dub jazz" → **Reggae-fusion**
- "salsa-fusion," "salsa," "Latin fusion," "montuno," "Eddie Palmieri fusion," "Michel Camilo," "Hiromi Latin," "Steve Khan Eyewitness" → **Salsa-fusion**
- "Casiopea," "T-Square," "Naniwa Express," "J-fusion," "Japanese fusion," "Issei Noro," "Akira Jimbo," "city-pop fusion," "Mint Jams," "Asayake" → **J-fusion**

If unclear: ask a one-line question. Don't guess across packs.

**Reggae-fusion, Salsa-fusion, and J-fusion are all explicitly fusion packs** — the user lifts the rhythmic engine (skank, montuno, clave, locked-16, Latin/J-fusion kit) but keeps an interesting harmonic frame on top. For Reggae and Salsa: modal-jazz (Dorian, Lydian-dom, ii-V-i). For J-fusion: major-key brightness with maj7/9/sus2/add9 voicings and **mandatory composed lead melody** (the genre is melody-first). Don't write authentic reggae I-IV-V, 3-chord salsa, or generic pop-fusion — put Lydian-dom over a skank, Dorian over a montuno, locked-16 under modal-rock harmony for Zaza-meets-Casiopea. See the packs below for touchstones.

### Rock *(default — instrumental melodic rock/metal — NOT classic rock or arena rock)*

**CRITICAL DISAMBIGUATION:** "Rock" in this pack means **post-Satriani instrumental virtuoso melodic rock**. It does NOT mean Boston, Foreigner, Journey, U2, or any vocal-led classic/arena/pop-rock. Those bands use I-vi-IV-V (and rotations) constantly — that's the harmonic frame to **avoid** here, even when the user says "rock." If the user wants classic rock or arena rock specifically, ask before composing; that's not what this skill targets and the chord vocabulary is fundamentally different.

The instrumental-melodic-rock idiom evolved POST-classic-rock and absorbed:
- Modal jazz harmony (Holdsworth, Pat Metheny, ECM-label influence)
- Lydian/Mixolydian as default modes (not Ionian major)
- Pedal-tone composition (the bass holds while chords change above)
- Sus voicings as a permanent option (sus2, sus4, add9 everywhere)

- **Tempo:** 88–140 (typically 100–135)
- **Key:** minor preferred — `Em`, `Bm`, `F#m`, `Am`, `Dm`. Use harmonic minor's raised 7th for V7 tension. **Major keys are allowed BUT only with modal/Lydian frame** (see below) — never as straight Ionian diatonic.
- **Roles:** all five — `bass, pad, rhy_l, rhy_r, drums`
- **Feel archetypes** *(pick one — DO NOT default to the same arc every time)*:
  - **A. Classic contrast** (my historical default — overused): `sparse` intro → `halftime` verse → `driving` chorus → `sparse` bridge → `driving` chorus. Use this MAX once every few songs.
  - **B. Driving throughout**: all sections `driving` — the band never stops. Build via density/voicing/harmony, not feel. (Foo Fighters, AC/DC, AAL "Cafo".)
  - **C. Inverse halftime chorus**: verse `driving`, chorus `halftime`. The SLOWDOWN at the chorus is the impact (Plini "Selenium Forest" vibe).
  - **D. Pushed throughout**: all sections `pushed`. Funk-rock, jazz-fusion energy.
  - **E. Sparse throughout**: cinematic instrumental, post-rock. Build via track-by-track entry (no rhythm guitars in verse 1, adding in verse 2, etc.).
  - **F. Mid-song hard drop**: verses/chorus 1 `driving`, then a `sparse` bridge that completely strips back, final chorus `driving` reborn. The drop IS the bridge.
  - **G. Pre-chorus build**: verse `halftime`, pre-chorus `driving`, chorus `halftime` (big slow lift), final chorus `driving`. The pre-chorus and chorus swap their expected energies.
  - **DON'T:** Pick A by reflex. Before composing, look at recent outputs (`ls <output_root>/_<year>/composer/ | tail -5` + read their `spec.json`) — if the last 2 songs used archetype A, pick B-G for this one. Variety in dynamic SHAPE matters as much as variety in chord choice.
- **Moves to reach for:** Aeolian descent, pedal-tone vamps, Polyphia common-tone, bVI-bVII-i lift, Phrygian-dom V7, Picardy 3rd ending, Lydian #4 IV-chord
- **Voicings:** m7/m9/maj7/sus2/sus4/add9 — color chords are the default. Plain triads only on resolution arrivals (chorus landings).

#### FORBIDDEN — even when the request says "anthem" / "epic" / "driving"

These progressions are vintage-pop, NOT instrumental melodic rock. They will trigger the "Earth Angel / 1955" reaction:
- `I – vi – IV – V` (Earth Angel, Stand By Me)
- `I – V – vi – IV` (Let It Be, Don't Stop Believin')
- `vi – IV – I – V` (rotation; OK for modern-rock pack but NOT for Satriani context)
- `I – vi – ii – V` (jazz/standards cliché)
- `I – IV – I – V` (Heart and Soul)

**Pre-flight check:** Before writing a verse, look at its roman-numeral skeleton. If it matches any forbidden shape, **rewrite** — UNLESS the Timmons clause below applies.

#### The Timmons clause — exception to FORBIDDEN

A forbidden progression IS permitted if and only if the section also includes a composed `melody` array (`lead` role required) carrying a vocal-style instrumental line. The chord cliché becomes the *vessel*, not the substance. The melody earns the chords.

The melody must have:
- A **clear contour** — rises and falls, not random walk
- **Rhythmic interest** beyond on-beat 8ths — syncopation, 16th-note pickups, held notes following busy passages
- At least one **hooky landing** — a long note or motif repetition that resolves on a chord tone (target-note thinking)
- **8+ bars** of melodic content (not a 4-note motif looped to fill the section)

**Prototype:** Andy Timmons "Electric Gypsy" — `D – A – Bm – G` (I-V-vi-IV in D), looped indefinitely. Without the melody, it's "Let It Be." With Timmons's vocal-style melody floating above, it's a melodic-rock instrumental classic. The progression isn't the song; the line above it is.

**Pre-flight, restated:**
- Forbidden shape + no `melody` → **rewrite the chords**.
- Forbidden shape + composed `melody` matching the criteria above → **keep the chords; document `move: "I-V-vi-IV vessel for Timmons-style composed melody"` so the reasoning is visible in the project notes**.

This connects directly to the Hooktheory **Chord-Melody Tension** and **Melodic Complexity** axes: high melodic complexity buys you permission to run low chord-progression novelty. The melody IS the differentiation.

#### MAJOR-KEY SATRIANI is real but uses these specific shapes ONLY

- **Pedal-tone verse** — bass stays on `I` (or another pedal); chord shapes shift above. Example in B: `Bsus2 → Emaj7/B → Aadd9/B → F#sus4` (B in bass for 3 of 4 chords).
- **Mixolydian rock vamp** — `I – bVII – IV – V` or `I – bVII – I – IV`. In B: `B – A – E – F#`. The `bVII` (A in B major) is the Satriani signature.
- **Lydian IV-as-tonic moments** — bridge or section that treats `IV` as the new home and explores `IVmaj7 – V – iii – IVmaj7` (B major → bridge in E Lydian).
- **bIII / bVI modal mixture** — borrow chords from parallel minor (e.g. `D major` in B major = bIII, gives a Vai modal-shift moment).
- **Relative-minor detours** — verses can briefly visit `vi` as a center (G#m in B major) but DON'T just hop through it as `I-vi-IV-V`; pedal on it or use it as a real key center for 4+ bars.

- **Touchstones:** Joe Satriani, Steve Vai, Neil Zaza, Plini, Polyphia, Animals as Leaders (melodic moments), Dream Theater (especially Awake / Images and Words era — verified from "Voices" MIDI: static-triad chorus with chromatic bass walk, 9/8 modal-mixture intros, 3/4↔2/4 hemiola transitions, Phrygian-dominant unresolved endings), Alan Parsons Project (verified from "Sirius" / "Some Other Time" / "Walrus" MIDIs: plagal-only intro fanfares, modal modulation by mode-shift on same tonic, bII-maj7 chromatic chorus pivots, additive 8-bar layer-stack arrangement), **Andy Timmons** (verified from Riff Journal / Guitar9 / MESA-Boogie / Glide / MisplacedStraws interviews: melody-first writing as the architectural anchor, single-guitar-track integration constraint, "technique as a color to paint with," I-V-vi-IV permitted under the Timmons clause when a composed vocal-style melody carries the section, target-note resolution thinking on every phrase)

### Cinematic / emotional / sad

**CRITICAL DISAMBIGUATION:** Three distinct subschools live under this label and want different specs. Pick the one matching the user's words BEFORE composing. All three share core principles (sparse feel, longer chord durations, anti-cadence endings) but differ on harmonic vocabulary, the meaning of "V chord," and how the build mechanism works.

- **A. Modal-cinematic (Zimmer / Einaudi / Sigur Rós / Ólafur Arnalds)** — strict Aeolian or strict modal-diatonic, **NO V CHORD AT ALL** (no V7, no leading-tone resolution). Build via **density and register expansion only** — same 4-chord loop iterated 30-100+ times. Tonic often permanently delayed via inversion. Verified from Zimmer "First Step," Zimmer "Time" (16-bar loop × 7), Einaudi "Nuvole Bianche" (4-chord loop × ~30+), Einaudi "I Giorni" (4-chord loop × ~50+).
- **B. Diatonic-cinematic (Yiruma / "River Flows In You" / instrumental piano pop)** — diatonic major key, V chord present and RESOLVES (unlike subschool A), single 2-bar loop iterated through the whole piece with one descending-inversion bridge as the only variation. Tonic permanently in 1st inversion. Verified from Yiruma "River Flows In You" (vi-I/3-I-V cycle for 47 bars).
- **C. Cinematic-pop (Skyfall / Bond themes / modern cinematic-vocal)** — minor key with **harmonic minor V7** (the "Bond chord" — V7 with raised leading tone). Verse/chorus pop form preserved. **Stepwise chorus descent** as signature device. Verified from Adele "Skyfall."

Settings below default to **A (modal-cinematic)** since that's the most "purely cinematic" of the three. For B and C, see their specific notes.

- **Tempo:**
  - A: **60–80 BPM** primary, but 125 BPM works if the harmonic rhythm is glacial (2-bars-per-chord) — Zimmer "Time" is 125 BPM and feels slow. Built-in tempo automation common (slow intro → accel to climax → ritard out — Einaudi's signature, ~40 BPM intro → ~130 BPM climax → ~40 BPM coda).
  - B: 65–80 BPM with rubato (Yiruma drops to ~56 BPM at fermatas).
  - C: 75–85 BPM (Skyfall is 79 BPM).
- **Key:**
  - A: strict Aeolian minor (`Am`, `Fm`, `Dm`, `Em`, `Cm`) — natural minor only, NO harmonic-minor V7. Diatonic major Aeolian-mood (D major treated as relative major of Bm — start chord cycles on vi) also works.
  - B: diatonic major (`A`, `G`, `D`, `C`) — V chord present and resolves.
  - C: minor with **harmonic minor leading tone** on V — Cm with G7 (B natural), Em with B7 (D# natural).
- **Roles:**
  - A: `[bass, pad]` minimal. Add `clean` for Einaudi-style arpeggio variants. Add `synth_pad` (SURGE XT) as harmonic glue under the pad for the climax sections — Zimmer/Einaudi build by layering, so even within "no rhy guitars / no drums," texture entries matter.
  - B: `[bass, pad, clean]` — the `clean` role carries the iconic Yiruma LH arpeggio (see "Yiruma LH pattern" memory for verbatim pattern).
  - C: `[bass, pad, drums]` minimum — Skyfall has drums (sparse kick + occasional snare). Add `rhy_l/rhy_r` with `"voicing": "full"` in the chorus for orchestral-strings-as-rhythm-guitar simulation. The contrast between verse (no drums) and chorus (drums + orch strings) is the cinematic-pop dynamic mechanism.
- **Feel:** all sections `sparse` (A and B). C uses `sparse` in verse and `halftime` in chorus.
- **Drums:**
  - A: `"none"` everywhere — drums never enter. Build via texture only.
  - B: `"none"` everywhere.
  - C: `"none"` in verse, `"halftime"` in chorus and bridge.
- **Chord durations:** longer — 8 or 16 beats per chord (4-bar held chords) for A and B, so each chord has time to be felt. C uses faster motion (especially in the chorus stepwise descent — half-bar = 2 beats per chord).
- **Loop discipline:** Subschools A and B are LOOP-FORM songs. The same 4-bar or 2-bar harmonic loop iterates many times. Don't write a different chord progression for verse vs. chorus vs. bridge — write ONE loop and let `skip_roles` + section names control texture build. See the "Single-loop iterated build" arrangement principle below.
- **Moves to reach for (shared across A/B/C):**
  - **Suspended hangs** — `Asus2 → Asus4 → Asus2`, floating, never resolving.
  - **Anti-cadence** — end the verse on V or sus or in 1st inversion, never root-position i. Leave the listener hanging.
  - **Subdominant minor in major** — in C major, use `Fm` or `Abmaj7` (Lana del Rey's "saddest" chord).
  - **Descending suspensions** — each chord more open than the last (`Am – G/B – C – Cadd9/B – Am`).
  - **Single-chord meditation** — 4-8 bars on one chord, slow piano motion within it.
  - **Anti-Picardy** — refuse the major 3rd at cadences. Stay minor.
  - **Plagal cadence** (IV-i) — softer than the dominant V-i. More resigned.
- **Moves specific to subschool A (modal-cinematic):**
  - **No V chord at all** — exclude V7 (and dominant-functioning V triads) from the entire palette. Pure Aeolian-anthem `i – bVII – bVI – bVII` (Zimmer "First Step") or `i – v(minor) – bIII – bVII` (Zimmer "Time") or `i – bVI – bIII – bVII` (Einaudi "Nuvole Bianche" — Aeolian descent).
  - **Tonic delay via inversion** — never voice the i chord in root position on a downbeat. Use `i/3` or `i/5` instead. Tonic is implied, not asserted.
  - **Einaudi common-tone RH pedal** — the piano comping pattern doesn't track chord tones. Instead it plays a constant root-and-5th dyad of the tonic on a steady 8th-note pulse, while the bass changes underneath. Document this in the section's `move` field; the script's default `pad` behavior approximates by holding sustained chord-tones, but the user can swap a sequenced VST patch to get the actual texture.
  - **Climax via register expansion** — bass drops an octave, treble climbs an octave, RH note density doubles — all while the chord loop stays the SAME. The script can't auto-do this, but document it in `move` so the user knows what to mix toward.
  - **Coda mirrors intro** — last section is literally the intro re-stated (same chord durations, same `skip_roles`). Use the same section name for first and last form entries: `["intro", ..., "intro"]`. The piece "un-builds" instead of resolving.
- **Moves specific to subschool B (diatonic-cinematic / Yiruma):**
  - **vi-I/3-I-V loop** — single 2-bar loop. In A major: `F#m – A/D | A – E`. Looped for 40+ bars.
  - **Bridge via descending-inversion chain** — only harmonic surprise. Walk the bass down via inversions: in A major, `Bm/F# → A/D → A → C#m/E → F#m/C# → A/D`. Stepwise descending bass (F# → D → A → E → C# → D).
  - **Yiruma LH arpeggio** — see [memory entry] for the verbatim 3-note ascending pattern (root → 5th → 10th, beats 1/1.5/2 + rest).
- **Moves specific to subschool C (cinematic-pop / Skyfall):**
  - **Bond chord harmonic-minor V7** — in minor keys, use V7 with raised leading tone (G7 in Cm with B natural, B7 in Em with D# natural). Place at every cadence point. This is the "James Bond" sonority.
  - **Skyfall stepwise chorus descent** — 8-chord chorus walking down the scale: `i – ♭VII – ♭VI – V – iv – ♭III – ii(°)` in half-bar rhythm. In Cm: `Cm – Bb – Ab – G – Fm – Eb – Dm7 – D7`. Eight distinct changes per chorus, bass walks down by step. No 4-chord repeat — the descent IS the chorus.
  - **♭VI lift** — Abmaj7 (♭VI in Cm) at the emotional peak of the chorus. Held longer than other chords (1 full bar in a half-bar chorus = a moment of breath).
  - **Wide-to-close voicing contrast** — verses use wide-spread voicings (12-31 semitones bass-to-top), choruses contract to close-position drop-2 voicings. The contrast is the dynamic build.
  - **Chromatic bass walk-up into final chorus** — last bridge climbs `♭VI – ♭VII – VII – I` chromatically by semitone into the final chorus arrival (Skyfall: `Ab – Bb – B – C`).
- **Voicings:** open 5ths (sometimes drop the 3rd entirely for that "huge open" sound), wide spacing, low bass with high pad and a gap in the middle. **Zimmer hollow-middle voicing** is the extreme version — bass octave-doubled at bottom (F1+F2), inner pedal note at E4, upper triad floating 3+ octaves above with the 3rd missing in the middle. Save for climax moments.
- **Time signatures:**
  - A: 4/4 most common, **3/4 waltz** for Zimmer-style (verified — "First Step" is 3/4, Einaudi "I Giorni" is 3/4), 6/8 or **12/8** for Einaudi-style flowing arpeggios (Nuvole's body is 12/8).
  - B: 4/4.
  - C: 4/4.
- **Meter shift between intro and body (advanced)** — Einaudi's "Nuvole Bianche" uses 4/4 in the intro at 40 BPM, then shifts to 12/8 at ~117 BPM for the body, then back to 4/4 for the recap. SAME CHORDS, but the meter recasts them as flowing (12/8) vs. static (4/4). The skill's script doesn't yet support meter changes mid-song — document this in `move` for the user to add manually in Reaper.
- **Avoid:** rhythm guitar chops in A/B, driving drums anywhere, fast tempos, bright Lydian moves. For A specifically: avoid V chord and harmonic-minor leading tones (you're STRICT Aeolian). For B specifically: avoid harmonic-minor or modal-mixture moves (you're diatonic-only). For C specifically: avoid pure modal harmony (you NEED the harmonic-minor V to land "cinematic-pop").
- **Touchstones:**
  - A (modal-cinematic): Hans Zimmer ("First Step," "Time," most Inception/Interstellar cues), Ludovico Einaudi ("Nuvole Bianche," "I Giorni," "Experience"), Sigur Rós, Ólafur Arnalds, Max Richter, Stars of the Lid, late Talk Talk, Kid A-era Radiohead.
  - B (diatonic-cinematic): Yiruma, Joe Hisaishi (Ghibli piano cues), Yann Tiersen (Amelie), Olafur Arnalds piano-side, instrumental piano-pop.
  - C (cinematic-pop): Adele/Paul Epworth "Skyfall," Lana del Rey, James Bond theme idiom, Billie Eilish "No Time To Die," modern cinematic-vocal ballads.

### Spanish / Phrygian / flamenco

- **Tempo:** 90–130 (or 160–180 for flamenco-rock)
- **Key:** **Phrygian** or **Phrygian dominant** in `E`, `A`, or `D`
  - E Phrygian: E F G A B C D (natural)
  - **E Phrygian dominant** (harmonic minor's 5th mode): E F G# A B C D — the iconic "Spanish" sound
- **Roles:** `bass, pad, rhy_l, rhy_r`. Drums **optional** — pure flamenco has none; flamenco-rock does.
- **Feel:** `pushed` (the rhythmic push is half the Spanish feel) or `driving`
- **Moves to reach for:**
  - **Andalusian cadence** — `i — bVII — bVI — V7` (Em – D – C – B7). THE Spanish move.
  - **Phrygian-dom V** — V7 with raised 3rd (B7 in Em with D# leading tone)
  - **bII (the Phrygian signature)** — `F` major over an Em song. Half-step pull.
  - **Three-chord vamp** — `Em – F – Em – F – G – F – Em`. Hypnotic.
  - **Picardy 3rd ending** — end on the major i (E major chord) for the "ole" close
  - **Rasgueado-style stabs** — use `pushed` feel for that strumming push
- **Voicings:** open low strings, plain triads, sometimes power chords. Avoid 7ths/9ths — too modern/jazz.
- **Time signatures:** 4/4, 3/4, or **6/8** (Bulería/Soleá feel). Hemiolas (3-against-2) feel deeply Spanish.
- **Avoid:** Lydian #4, Polyphia common-tone (too modern), major-key brightness, m9/maj9 voicings
- **Touchstones:** Paco de Lucía, Rodrigo y Gabriela, Vai's "Boston Rain Melody," Al Di Meola's Spanish moments, Mediterranean prog (Buckethead's flamenco moments)

### Post-rock / atmospheric

- **Tempo:** 70–100 BPM (slow internal build)
- **Key:** major with modal moments, or open modal (`E`, `A`, `G`, with Aeolian/Mixolydian color)
- **Roles:** all five — but use `feel` for dynamic arc: `sparse` early, `halftime` middle, `driving` only at the climax
- **Feel archetype:** sparse early → progressive build → driving climax. Real post-rock songs are 10-minute arcs; here we compress, but the principle is "the climax is at the END, and we earn it by withholding earlier." Options: intro sparse → verse 1 sparse → verse 2 halftime (drums enter) → bridge driving → final chorus driving. Or: all sparse with the LAST section breaking into driving.
- **Drums:** `none` early, building to `basic-rock` at climax
- **Moves to reach for:**
  - **Held pedal tones** — entire verse on one chord, dynamics build everything
  - **Major key with bVI surprise** — in E major, drop a C chord for emotional jolt
  - **Long ostinato in bass** — bass plays the same 4-note line for 32 bars while pad changes
  - **Slow chord changes** — 8 or 16 beats per chord
  - **The "Mogwai inversion"** — start sparse and dissonant, resolve to consonant and loud
- **Voicings:** open spacings, wide intervals (octaves + 5ths, not stacked thirds). Sparse for tension, full for release.
- **Time signatures:** mostly 4/4 but feels timeless
- **Avoid:** shreddy moves, Phrygian-dom, fast chord changes, jazz extensions
- **Touchstones:** Explosions in the Sky, Mogwai, Russian Circles, Pelican, Caspian, This Will Destroy You

### Djent / progressive metal

- **Tempo:** 100–150 (often FEELS halftime even at 130+)
- **Key:** drop-tuned minor (`Em`, `Dm` — implies low-string root chugs)
- **Roles:** `bass, rhy_l, rhy_r, drums`. `pad` optional — often dropped for purity.
- **Feel:** `pushed` rhythm guitar (the djent groove), `halftime` drums under it
- **Drums:** `halftime` (the snare on 3 in 4/4 = the djent backbeat)
- **Moves to reach for:**
  - **Pedal-tone root chugs** — root note hammered constantly, chord above changes
  - **Polyrhythm hints** — chord changes every 3 beats over 4/4 drums (3-against-4)
  - **Slow chordal sweep under fast rhythmic chops** — chord changes every 8 beats, chops every 16th
  - **Tritone moves** — `Em` to `Bbm` (root motion of a tritone), creates instability
- **Voicings:** **power chords only** (root + 5th, occasionally + octave). NO m7, NO m9.
- **Time signatures:** 4/4 most often, 7/8 and 5/8 for prog moments
- **Avoid:** jazz extensions, piano leads, Lydian, open-string ringing chords
- **Touchstones:** Periphery, Animals as Leaders, Meshuggah, Tesseract, Polyphia (rhythmic moves), Plini (melodic moves)

### Synthwave / retro 80s

- **Tempo:** 88–110 (chill synthwave) or 110–140 (Carpenter Brut darkwave)
- **Key:** minor — `Am` (most common), `Em`, `Dm`
- **Roles:** `bass, pad, drums` — drop `rhy_l`/`rhy_r` (no guitars in synthwave) OR include only one rhythm side for a synth-arpeggio feel
- **Feel:** `driving` — constant 8ths
- **Drums:** **`four-on-floor`** (kick on every beat) — the defining synthwave feel
- **Moves to reach for:**
  - **i – bVII – bVI – bVII** — the classic synthwave loop
  - **i – v – iv – bVII** — Carpenter Brut darkness
  - **i – bVI – bIII – bVII** — Stranger Things-y, builds via density not chord change
  - **Arpeggiated bass** — each beat a different chord tone (Tangerine Dream territory)
- **Voicings:** open pads (root + 5th + octave + 9th), saw-wave-friendly
- **Time signatures:** 4/4 only (this is dance-adjacent music)
- **Avoid:** acoustic-y voicings, jazz, Phrygian-dom, organic feel
- **Touchstones:** Carpenter Brut, Mitch Murder, Kavinsky, Perturbator, FM-84, The Midnight, Stranger Things soundtrack

### Jazz-funk / fusion *(Jack Thammarat, Tomo Fujita, neo-soul)*

**CRITICAL DISAMBIGUATION:** There are TWO distinct subschools under this label and they want different specs. Pick the one matching the user's words BEFORE composing:

- **A. Melodic-fusion (Jack Thammarat / Mateus Asato)** — singable instrumental tunes. **Mixolydian I-♭VII-IV-V is the primary frame**, not ii-V-i. Rhythm guitars play **single-note arpeggiation + occasional dyad**, NOT full m7 stacks. Chord identity lives in **bass + piano combined**, never stated as a block chord. This is verified from MIDI transcription of "On The Way": rhythm gtr is mid-register picking, piano comps with perfect-4th dyads (`E+A`, `F#+B`). **Default to subschool A** when the user says "Jack Thammarat" by name.
- **B. Modal-jazz fusion (Coltrane / Snarky Puppy / Cory Henry)** — denser harmonic motion, ii-V-i, secondary dominants, tritone subs, Coltrane changes. Full m7/maj9/13 voicings as block chord comps. Use when the user names these touchstones or says "smooth jazz instrumental."

The settings below default to **A**. For **B**, swap to `"voicing": "full"` everywhere, use ii-V-i chains, and let rhythm guitars block-comp.

- **Tempo:** 80–110 (Jack / smooth) or 100–126 (denser funk)
- **Key:** major frame — `Dmaj` (Jack's "On The Way"), `Cmaj`, `Fmaj`, `Bbmaj`. Approach as **Mixolydian** (raised tonic of the IV — so D major treated like the V of G means you can use Cmaj7 freely). Minor-key fusion (`Am`, `Dm`) for subschool B.
- **Roles:** `[bass, pad, drums, clean, rhy_l, rhy_r]`. For subschool A: rhy guitars OPTIONAL; if included keep `"voicing": "power"` AND have them play arpeggiated single-note lines via the chord changes (the script's default rhythm guitar treatment is too block-y for the Jack aesthetic — the cleaner approach is to *drop rhy_l/rhy_r entirely* and let `clean` (picked arpeggio) + `pad` (block chord comp) carry the harmony). For subschool B: include rhy guitars with `"voicing": "full"`.
- **Feel:** `driving` (Jack moves harmonically in 8th notes via the arpeggio) or `pushed` (denser funk subschool).
- **Drums:** `basic-rock` works. `four-on-floor` for groovier subschool-B moments. **Energy-without-tempo trick:** Jack uses kit patterns mismatched to song BPM (e.g. 185-BPM "Punkish" drum patterns at 80 BPM song tempo — busy 16ths become driving 8ths). Not directly expressible in this skill's drum-pattern enum, but design choruses with `"drums": "basic-rock"` knowing the user can swap drum kit/pattern later.
- **Chord durations:** 4 beats per chord (Jack — `D-C-G-A` one bar each) or 2 beats (subschool B — twice the harmonic density).
- **Moves to reach for:**
  - **Mixolydian I-♭VII-IV-V** *(Jack's primary frame)* — `D – C – G – A` in D major. The ♭VII (Cmaj7) is the signature flavor. Loop this as a verse engine, like Jack on "On The Way."
  - **Stepwise diatonic chorus walk** *(Jack)* — bass climbs scalewise instead of jumping by 4ths/5ths. In D: `Em7 – F#m7 – Gmaj7 – A` (iii-iii#?-IV-V). Vocal/horn-melody feeling.
  - **♭VI passing surprise** *(Jack)* — in D major, briefly drop `Bb` between two diatonic chords (`G – Bb – C – G`). Resolves *backwards* through cycle of 4ths, not forward to a cadence.
  - **Quartal dyads in piano** *(Jack)* — comp the piano in perfect 4ths instead of stacked 3rds: `E+A`, `F#+B`, `G+C`. Implies extended harmony without naming m7s.
  - **Anti-cadence intro** *(Jack)* — start the intro on V (`A` in D major) and avoid the tonic for 3+ bars. Verse downbeat resolves.
  - **ii-V-I** *(subschool B)* — `Dm7 → G7 → Cmaj7`. The building block. Repeat in different keys to modulate.
  - **Secondary dominants** — `A7 → Dm7` (V7 of ii). Adds chromatic spice.
  - **Tritone substitution** — `Db7 → Cmaj7` instead of `G7 → Cmaj7`. Identical resolution, fancier.
  - **Cycle of fourths** — `Cmaj7 → Fmaj7 → Bm7b5 → Em7 → Am7 → Dm7 → G7 → Cmaj7`. The Autumn Leaves loop.
  - **Modal mixture (IV minor in major)** — `C → F → Fm → C`. The bittersweet pull.
  - **Chromatic chord planing** *(subschool B)* — `Cmaj7 → C#m7 → Dm7 → D#dim → Em7`. Walks by half-steps.
- **Voicings:** **Subschool A:** `"voicing": "power"` is fine — chord identity comes from bass + clean arp + piano dyads, not from rhythm-guitar block chords. **Subschool B:** ALWAYS m7/maj7/m9/9/13 chord names with `"voicing": "full"` — color tones are mandatory.
- **Time signatures:** 4/4 (occasional 12/8 for slow funk, but rare)
- **Aesthetic principle (subschool A):** "Chord identity lives in the BAND, not in any one instrument." Bass states roots, piano implies via dyads, clean arp outlines chord tones, rhy guitars pick single notes — none of them plays the full m7. The chord *emerges* from the combination.
- **Avoid:** power chords as the dominant texture in subschool B, Phrygian-dom, djent territory, synthwave four-on-floor straightness, post-rock pedal stasis. For subschool A specifically: avoid ii-V-i chains (too dense for the Jack vibe) and avoid block-comp m7 chords (too jazzy).
- **Touchstones:** **A (Jack):** Jack Thammarat ("Beautiful Resonance," "On the Way," "Light at the Edge"), Mateus Asato, Tomo Fujita, Tom Misch instrumental moments. **B (modal-jazz):** Cory Henry, Snarky Puppy, Lee Ritenour, Robben Ford, John Scofield.

### Math rock / Midwest emo *(American Football, TTNG, Toe, fingerpicked indie)*

- **Tempo:** 110–150 BPM, often felt halftime (so it grooves slower than the BPM number suggests)
- **Key:** open major keys — `C`, `G`, `F`, `Eb` (or capo-3 of `D`). The signature math-rock guitar tuning is **FACGCE** (a Cmaj9-ish stack of fourths/thirds) which makes Fmaj9, Cadd9/E, G6sus4 voicings effortless. The skill can't actually retune, but the *chord vocabulary* is what gives the genre away.
- **Roles:** `[pad, bass, drums]` — drop `rhy_l`/`rhy_r`. Math rock leads with FINGERPICKED clean guitar, which the `PIANO` track approximates better than power chords ever could. If you want layered texture, include one rhythm-guitar side with `"voicing": "full"`.
- **Feel:** `sparse` (let voicings ring) — never `driving`. The genre's intensity comes from rhythm/meter, not chord density.
- **Drums:** `basic-rock` or `halftime`. Math rock drumming is wild but the bed should be straight — let the chords be the math.
- **Chord durations:** 4 or 8 beats per chord — the guitars sustain forever, harmony moves slowly.
- **Time signatures:** the genre's signature — try `[7, 8]`, `[5, 4]`, `[13, 8]`. Phrase a 4-chord loop in 7/8 and the loop drifts against any drum pulse, creating cycle-vs-pulse tension.
- **Moves to reach for:**
  - **maj7/maj9 voicings everywhere** — `Fmaj9`, `Cmaj7`, `Gmaj7`. Bittersweet college-dorm sound.
  - **Sus chords with rich extensions** — `Cadd9`, `Gsus4`, `Asus2`. Open and yearning.
  - **Slash chords with stepwise bass** — `C – C/E – F – G/B – C`. The melody is the bass line.
  - **Single-note bass under static chord shape** — guitar shape doesn't change, bass walks underneath.
  - **Loop in odd time** — Take any `I – V – vi – IV` and phrase it in 7/8. Same chords, totally different feel.
- **Voicings:** `"voicing": "full"` if you include rhythm guitars (so they ring as jangly extensions, not power chords). Use 9ths and add9s liberally in chord names.
- **Avoid:** power chords, distortion-implying voicings, jazz extensions (it should sound college-dorm, not jazz club), Phrygian, fast harmonic motion
- **Touchstones:** American Football "Never Meant," TTNG "Crocodile" / "In Praise of Idleness," Toe "Goodbye," Don Caballero, Tortoise (post-rock-math-adjacent)

### Reggae-fusion *(skank as engine — modal-jazz harmony on top — Scofield / Khan / Eyewitness)*

This pack is **fusion**, not authentic reggae. The user lifts the reggae *rhythmic feel* (skank guitar chops + one-drop drums + walking bass) and drops modal-jazz or fusion harmony on top. Authentic reggae harmony is I-IV-V — we DON'T do that here. The whole point is the contrast between the reggae groove and surprising harmonic vocabulary.

- **Tempo:** 70–95 BPM (classic reggae sits 70–85; fusion-reggae often slightly faster at 80–95).
- **Key:** modal preferred — `D Dorian`, `G Mixolydian`, `Em Aeolian`, `A Dorian`, `F Lydian`. Major-key Lydian works (the raised 4 shimmer over the skank is gorgeous — Scofield "Bone Yard" territory). For minor-key vibes use Aeolian with extended chords (m9, m11 voicings).
- **Roles:** `[bass, pad, rhy_l, rhy_r, drums]`. The skank lives on `rhy_l`/`rhy_r` (with `voicing: "full"` so the extensions ring). `pad` (piano) can do the "bubble" — 8th-note arpeggios on upbeats — but the **default sustained-chord pad behavior also works**, voicing it as an organ via VST swap (Hammond/Wurli) gets you the classic reggae bubble timbre. Add `clean` if you want a separate clean guitar doing arpeggios alongside the skank.
- **Feel:** **`skank`** is the centerpiece — silent downbeats, chord chops on the upbeats only. For contrast, bridges can use `halftime` (band breathing) or `sparse` (dub-style breakdown).
- **Drums:** `one-drop` (auto-mapped from `skank` feel) — kick + snare together on beat 3, hi-hat 8ths underneath. For variation, `halftime` works in bridges.
- **Chord durations:** 4 or 8 beats per chord — skank groove needs chords to LAND and stay for the feel to develop. Fast harmonic motion kills the groove.
- **Moves to reach for:**
  - **Dorian vamp under skank** — `Dm9 – G7 – Dm9 – Em7`. Two chords, modal, locked. Pure Scofield.
  - **Lydian shimmer under skank** — `Fmaj7 – G/F – Em7 – Am7`. The raised 4 (B natural over F) sings against the upbeat chops.
  - **Lydian-dominant turn** — `D7#11 – G/D – Am7 – D7sus4`. Bring jazz-fusion chord vocab to a roots-reggae groove.
  - **ii-V-i with delayed resolution** — `Dm7 – G7 – Dm9`. The V doesn't fully resolve; we sit in the suspension over the skank.
  - **bVII–IV vamp** — `Cmaj7 – G – Cmaj7 – G` (in G Mixolydian). Classic reggae harmonic frame, but voiced as maj7 not plain triads.
- **Voicings:** `"voicing": "full"` is mandatory — extensions and 7ths are the fusion signature. Power chords KILL reggae (and kill fusion). Use m9, m11, maj7, 7#11 chord names liberally.
- **VST plugin swaps (manual, after generation):**
  - `rhy_l`/`rhy_r` → clean amp sim (no distortion) for authentic skank tone
  - `pad` (PIANO) → Hammond / Wurli VST for the "bubble" organ sound
  - `bass` → fingered/round-tone preset (no slap, no pick)
- **Avoid:** distortion on the rhythm guitars (kills the genre), I-IV-V harmony (boring authentic-reggae), 4-chord pop loops (the "no 4-chord loops" rule still applies), fast harmonic motion (the groove needs to lock), V7 cadences with full resolution (modal hangs are the fusion-reggae move).
- **Touchstones:** John Scofield "Bone Yard" / "Boozer" / "Did You Have a Good Time" (the textbook), Steve Khan "Eyewitness" era, Pat Metheny "American Garage" reggae moments, Grant Green's late jazz-reggae crossovers.

### Salsa-fusion *(montuno + clave as engine — modal jazz / Lydian-dom on top — Camilo / Khan / Hiromi)*

Also explicitly **fusion**, not authentic salsa. Real salsa is dom7-heavy and structurally rigid (verso-coro-mambo); fusion-salsa lifts the montuno piano figure, the clave foundation, and the Latin kit, then drops jazz-fusion harmony over the top. The harmonic vocabulary of authentic salsa (mostly ii-V chains in major) is fine on its own but uninteresting for a fusion player; we deliberately bring more modal complexity.

- **Tempo:** 95–130 BPM (authentic salsa lives 90–115; fusion can push a bit faster). Slower side for "salsa ballads" (the bolero-fusion zone), faster for charanga-energy bridges.
- **Key:** modal jazz frame — `Dorian`, `Lydian-dominant`, `Mixolydian`, with ii-V-i chains for development. Minor modes work great. **Avoid** straight-major Ionian (boring) and dense Aeolian (clashes with the Latin lift).
- **Roles:** `[bass, pad, drums]` is the minimal montuno trio. Add `chugg` for clave on a wood-block VST. Add `lead` for horn-section lines (the typical fusion sub is to play horn lines on guitar or synth lead — Steve Khan does this constantly). Optional `rhy_l`/`rhy_r` for montuno comp doubling (the figure becomes a guitar-piano unison hook).
- **Feel:** **`montuno`** on the `pad` role — this triggers a syncopated chord-tone arpeggio (root/3rd/5th) in mid-register, replacing the usual sustained-chord pad. THE engine. Bridges can shift to `pushed` (for breakdown moments) or `halftime` (for "mambo break" moments).
- **Drums:** `latin-fusion` (auto-mapped from `montuno` feel) — kit + cowbell on every beat (cáscara timekeeping) + open conga on the "ands." Swap the drum-track plugin to a GM-compliant kit so the cowbell/conga pitches sound right.
- **Chugg:** **`clave-3-2`** (default; 2-bar pattern with 3 hits on the first bar, 2 on the second) or **`clave-2-3`** (reversed — 2-side first). Pick one and stay with it across a section. The clave is the timekeeping ANCHOR — everything else aligns to it. Swap the chugg-track VST to a wood-block or claves patch for the authentic clave timbre.
- **Chord durations:** 4 or 8 beats per chord — montuno needs the harmony to sit for the figure to develop. Two-bar chord lengths are ideal (each bar of montuno feels complete; two bars lets the syncopation breathe).
- **Moves to reach for:**
  - **ii-V-i in minor with extensions** — `Dm9 – G7 – Cmaj9`. The classic jazz-fusion frame; the montuno rhythm makes it Latin.
  - **Lydian-dominant vamp** — `D7#11 – Em7 – D7#11 – G7`. Pure Joe Henderson / Eddie Palmieri fusion overlap. The #11 sings against the montuno.
  - **Modal montuno** — Single Dorian/Lydian vamp for 8+ bars; the montuno is the variety, not the chord changes (a-la Eddie Palmieri's "Vámonos Pa'l Monte" but with jazz extensions).
  - **Mambo break** — Sudden chord change + hit on beat 1 then silence for half a bar (use `feel: "halftime"` and a leading-tone chord like dom7 with #11/b9 extensions where the parser allows).
  - **bVII-I in major** — `Bb – C` cycle (in C Lydian). Salsa's bIII-IV-V is too pop; bVII-I gives the modal/Mixolydian fusion frame.
- **Voicings:** `"voicing": "full"` MANDATORY. The montuno figure outlines chord tones; if rhy guitars do power chords, the chord-tone arpeggio in the pad sounds disconnected from the band. m7/m9/maj7/maj9/9/7sus4-equivalent (use sus4 or 7 since 7sus4 isn't parser-supported).
- **VST plugin swaps (manual, after generation):**
  - `pad` (PIANO) — keep as electric/acoustic piano (montuno belongs on piano). For more authentic salsa: a percussive electric piano (Wurli, Rhodes Mark I) for the Camilo/Eyewitness sound.
  - `chugg` → wood-block or claves VST (the chord-root low-octave default is wrong for clave timbre — claves are a high pitched percussion sound).
  - `lead` → brass section / trumpet / sax for horn lines, OR keep as fusion guitar/synth for the Khan/Metheny sub.
  - `drums` → GM-compliant kit so cowbell (56), open conga (63), open hi-hat etc. all sound correctly.
- **Avoid:** straight-major Ionian (no fusion interest), Aeolian (clashes with the bright Latin feel — Dorian is the minor-mode default here), power chords, fast harmonic motion (montuno needs space), 4-chord loops, V7 cadences that fully resolve (modal hangs are the move).
- **Touchstones:** Michel Camilo Trio ("Caribe," "On Fire," "From Within"), Hiromi Trio Project Latin moments, Eddie Palmieri's harmonic vocabulary applied to fusion, Steve Khan "Eyewitness" Latin moments, Pat Metheny Group "Are You Going With Me?" / "Last Train Home" (the cinematic-Latin tinge), Chick Corea "Spain" (the canonical jazz-Latin fusion overlap).

### J-fusion *(Casiopea / T-Square / Naniwa Express — Japanese melodic fusion)*

The **Japanese fusion school** — distinct from American Jazz-funk (which is improvisational, modal, neo-soul). J-fusion is **composed melody-first**, major-key bright, locked tight 16ths, glassy clean tones, DX7 synth-brass beds. The melody IS the song; the rhythm section is the engine the melody rides on. Casiopea's "Mint Jams" and T-Square's "Truth" are the textbook records.

- **Tempo:** 105–135 BPM. Sweet spot is 110–125 — fast enough for the locked 16ths to drive, slow enough for the melody to sing. Ballads can go down to 90.
- **Key:** **MAJOR preferred** — `C`, `F`, `G`, `Bb`, `A`, `D`. Minor keys are fine but lean toward Dorian (i with major IV) or Aeolian-with-major-mixture — avoid the dark modal-jazz Aeolian dwelling that defines Jazz-funk. Bright is the default mood.
- **Roles:** `[bass, pad, rhy_l, rhy_r, drums, lead]`. The bass is PROMINENT — Tetsuo Sakurai (Casiopea) / Mitsuru Sutoh (T-Square) play melodic basslines that are half lead, half rhythm. `pad` (piano) typically gets swapped to electric piano (Wurli, Rhodes, DX7 FM). **`lead` is REQUIRED** — every section (except sparse intro/outro) must have a composed `melody` array. The genre is melody-first; without a composed lead, the output is just a generic funk groove.
- **Feel:** `locked-16` is the centerpiece — tight 8th-note chord stabs with **upbeats accented louder than downbeats** (the Japanese-fusion lift, inverting rock-default accents). Ballads use `sparse` or `halftime`; bridges can shift to `pushed` for breakdown moments.
- **Drums:** `j-fusion-kit` (auto-mapped from `locked-16` feel) — 16th-note hi-hat with syncopated kick on 1 / "and of 2" / 3. Akira Jimbo / Hiroyuki Noritake style. Swap to a fusion-style kit VST (BFD or AD2 with a "studio" preset) for the proper tight sound.
- **Chord durations:** 2–4 beats per chord. Casiopea moves through harmony FAST — don't dwell. Two-bar chord lengths only on intro/outro/sparse moments.
- **Composed melody (mandatory):** every non-intro section needs a composed lead line in the `melody` array. The melody should:
  - Be **8 or 16 bars** of phrase length
  - Have a clear **contour** (rises and falls — not random walk)
  - Land on **chord tones** at section boundaries
  - Use **rhythmic interest** matching the locked-16 feel (16th-note pickups, syncopated landings)
  - Have **hooky landings** — long notes after busy 16th passages, repeated motifs
- **Moves to reach for:**
  - **Asayake lift** — diatonic descending bass with maj7/9 voicings. In F: `Fmaj7 – Em7 – Dm7 – Cmaj7 – Bbmaj7 – Am7 – Gm7 – C7`. Famous Casiopea descent.
  - **Pop-fusion I-vi-IV-V with extensions** — `Cmaj9 – Am9 – Fmaj9 – G7sus4 → G7` (sus resolution as the hook). The Asayake/Take Me / Mid-Manhattan frame, but with maj9/m9 not plain triads.
  - **Pedal-tone with melody-led changes** — bass pedals on tonic while chord QUALITIES shift above; the lead carries the song. `C – C/B – Am9 – G/B – C/E – Fmaj7 – G7sus4 – Cmaj9`.
  - **Quick ii-V passing chains** — not destination harmony, transient color. `Dm7 – G7 – Em7 – A7 – Dm7 – G7 – Cmaj9 – Fmaj9`. Each ii-V passes through, never resolves.
  - **Sus2 → maj9 hook** — `Csus2 – Cmaj9`. The sus2 is the surprise, the maj9 is the home. T-Square's "Omens of Love" lives in this gesture.
  - **Bass-and-drums unison locks** — bass plays a melodic 16th-note line in unison with the kick pattern. The pocket IS the hook. Casiopea "Galactic Funk" / T-Square "Twilight in Upper West."
- **Voicings:** **`"voicing": "full"` mandatory.** maj7/maj9/m7/m9/add9/sus2/sus4. Bright extensions only — never power chords (kills the entire aesthetic). 7th-chord ambiguity (dom7 used as passing color) is fine.
- **VST plugin swaps** *(critical for the genre to sound right)*:
  - `pad` (PIANO) → Wurlitzer / Rhodes Mark I / Yamaha DX7 / FM electric piano (the *actual* Casiopea/T-Square keyboard sound — acoustic piano is wrong)
  - `rhy_l`/`rhy_r` → clean amp with chorus pedal (the Issei Noro / Masahiro Andoh glassy tone)
  - `synth_pad` (SURGE XT) → DX7 brass / E.Piano 2 / TX802 preset for the 80s J-fusion synth bed
  - `lead` → clean electric guitar with light overdrive + chorus, OR a DX7 lead synth for the synth-melody moments
  - `bass` → fingered round-tone preset, slight compression (no slap, no pick — Sakurai uses fingers)
- **Avoid:** distortion (kills the clean glassy tone), dark Aeolian dwelling (different fusion school — that's Jazz-funk territory), modal-jazz Lydian-dom (also Jazz-funk's lane), 4-chord pop loops, melodies without rhythmic interest, slow harmonic motion (Casiopea moves fast), power chords, dwelling on V7 cadences (J-fusion prefers passing color over resolution).
- **Touchstones:** Casiopea "Mint Jams" (1982 live record — the textbook), "4x4," "Eyes of the Mind," "Asayake," "Take Me," "Mid-Manhattan," "Galactic Funk," "Domino Line"; T-Square "Truth," "Omens of Love," "Travelers," "Twilight in Upper West," "Sole Sisters"; Naniwa Express; Akira Jimbo solo records; Issei Noro Inspirits; Hiroyuki Noritake; Tetsuo Sakurai's bass-led work.

### Mixing packs

Real songs blend. Examples:

- **Spanish bridge in a rock song** — verses/choruses use Rock pack, the bridge section uses Spanish moves (Andalusian, Phrygian-dom)
- **Cinematic intro into rock verse** — intro section uses Cinematic pack (sparse, no drums, suspended hang), then `roles` add back guitars + drums for the rock verse onward
- **Synthwave verse with djent bridge** — verses are synthwave (four-on-floor, arpeggio), bridge drops to djent (pushed rhythm guitars, halftime drums)
- **Zaza + Casiopea** *(the canonical melodic-rock-meets-J-fusion fusion)* — Rock-pack **chord harmony** (modal minor, Aeolian descent, pedal tones, bVI-bVII-i lift, sus2/add9 voicings) + J-fusion's **`locked-16` feel** under it + **composed lead melody** with Zaza-style melodic contour (singable, hooky, with bends and slides implied). Use roles `[bass, pad, rhy_l, rhy_r, drums, lead]`. The lead carries the Zaza melodicism; the rhythm section grooves tight J-fusion underneath. Result: melodic instrumental rock with a Japanese-fusion engine instead of straight 8th-note rock chops. Best in minor keys (Em, Bm, F#m, Am) so the Zaza melodic vocabulary translates directly.

When mixing, keep one section's `feel` and `move` consistent within itself — don't put Spanish moves in the same section as synthwave voicings. The packs blend at section boundaries, not within sections.

## Mood → progression seed bank *(verified corpus, 127 progressions)*

When the user names a **mood word** ("mysterious," "nostalgic," "sad," "triumphant," "hopeful") and the existing Moves library doesn't have a direct hit — or you want a *less-obvious* option to avoid drifting toward defaults — consult this bank.

**Source:** [`data/shld_mood_bank.json`](data/shld_mood_bank.json) — 127 unique chord progressions distilled from 7,620 labeled reference MIDI files (Songwriter's Helpful Library Database, Minor + Modal scales only). Each entry is a Roman-numeral sequence appearing under one or more emotional labels, deduplicated across keys/styles. The JSON is indexed `by_mood` — open it and scan when you need more options than the inline tasting menu below.

**Why use it:** the Moves library is hand-curated from named reference songs (Plini, Zimmer, Hisaishi, Dream Theater, etc.) and is biased toward those artists' vocabulary. This bank is a *statistical distillation* of a broader labeled corpus, so it surfaces progressions you wouldn't otherwise reach for. Use it as a **seeding source** — pick a progression, then voice it in the chosen pack's idiom (Rock → m7/m9 voicings; Cinematic → wide open 5ths; Spanish → plain triads; etc.). The bank gives you the *skeleton*, the style pack gives you the *flesh*.

**How to apply:**
1. User names a mood. Find the closest match in the 19 mood buckets below.
2. Pick a progression from that bucket (top entry = most-common; later entries = rarer / more distinctive).
3. Read the RN sequence (e.g. `i VI VII iv` = tonic-minor → ♭6 → ♭7 → iv).
4. Transpose to the target key (e.g. in `Em`: `Em – C – D – Am`).
5. Voice it in the chosen style pack's idiom and apply the appropriate Moves-library voicings.

**Scope:** Minor + Modal only — Major was filtered out (genre mismatch with melodic-rock/cinematic/fusion preferences). Some mood buckets contain mostly Modal (uppercase-I) entries with modal mixture (`bIII`, `bVI`, `bVII`); others are pure Minor (lowercase-i tonic). Both are valid — modal-mixture progressions land bright-and-borrowed, pure minor lands dark.

**Inline tasting menu — top 3 per mood, scan first before opening the JSON:**

**Mysterious** (41 unique):
- `iv v VI VII` — minor — Mysterious + Rebellious
- `i VI VII iv` — minor — Mysterious + Nostalgic
- `i ii v i` — minor — Mysterious + Triumphant

**Nostalgic** (14 unique):
- `i III iv VI` — minor — Nostalgic + Romantic
- `VI III i v` — minor — Nostalgic + Dark
- `i VII VI III` — minor — Nostalgic + Hopeful

**Sad** (11 unique):
- `i VI iv v` — minor — Sad + Hopeful
- `i v iv VII` — minor — Sad + Rebellious
- `v VI v i` — minor — Sad

**Triumphant** (13 unique):
- `i VI VII VII` — minor — Triumphant + Rebellious
- `iv VI VII i` — minor — Triumphant
- `VI VII i III` — minor — Triumphant + Nostalgic

**Hopeful** (10 unique):
- `VI i v III` — minor — Hopeful + Nostalgic
- `VI iv i v` — minor — Hopeful + Tender
- `v VI III i` — minor — Hopeful + Nostalgic

**Dark** (5 unique):
- `v i iv VII` — minor — Dark + Rebellious
- `i7 VI III7 VII6 i i7 III7 iv7` — minor — Dark + Nostalgic *(8-chord epic)*
- `i i iv iv v7 ii5 v v7` — minor — Dark + Mysterious *(8-chord with v7 leading tone)*

**Romantic** (3 unique):
- `im bIIIM bVIIM IV` — modal — Romantic + Nostalgic
- `I bIIIM IV I` — modal — Romantic
- `I I7 I9 IV ivm` — modal — Romantic + Nostalgic *(extension-shimmer)*

**Surprised** (6 unique):
- `I IIM iii V6` — modal — Surprised + Triumphant
- `I V ivm bVIM` — modal — Surprised + Mysterious
- `VIM bVIM im bVIIM` — modal — Surprised + Rebellious

**Cadence** (6 unique — useful as section-closing 3-chord moves):
- `bIIIM V7 I` — modal — major-Picardy cadence into a modal piece
- `ivm bIIIM bIIM I` — modal — modal-mixture half-step descent into I
- `bVIIM V7 I` — modal — Mixolydian cadence with V7 leading tone

**Other 10 mood buckets** (1–4 unique each — open the JSON for full list): Empowered, Excited, Fearful, Joyful, Lonely, Peaceful, Playful, Rebellious, Relaxed, Spiritual.

**When NOT to use:** the bank is a *seeding* shortcut, not a substitute for the Moves library. If the user names a *named-artist style* ("Plini-like," "Zimmer-like," "Jack Thammarat verse"), go to the Moves library and pack-specific moves first — those are curated to match the named artist's voice. The bank is for mood-first briefs where no named-artist target exists, or for finding a less-obvious alternative to the default move.

**Pre-flight check:** before committing to a progression from this bank, scan it against the **FORBIDDEN list** in the Rock pack (`I-vi-IV-V`, `I-V-vi-IV`, `vi-IV-I-V`, `I-vi-ii-V`, `I-IV-I-V`). The bank was pre-screened against these and contains zero hits, but if you later combine bank progressions with mode-shifted reharms, double-check the result doesn't drift into pop-rock territory.

## Moves library — chord-movement archetypes

Reach for these before inventing from scratch. Pick a few per section. All examples in `Em` unless noted.

### Modal anchors (minor-key defaults)
- **Aeolian descent** — `i – bVII – bVI – V7`. `Em – D – C – B7`. The Hotel California / Pink Floyd spine.
- **Diatonic descending bass** — Walk the bass down the natural minor scale: `Em – D – Cmaj7 – Bm7 – Am7 – G – F#m7b5 – B7`. Bass: E→D→C→B→A→G→F#→B. Massive in Satriani-world.
- **Dorian color** — Brighten Aeolian with a major IV: `Em – A – Em – A`. The raised 6th is the magic note.
- **Phrygian-dom** — `i – bII – i – V7`. `Em – F – Em – B7`. Heavy/Spanish/exotic.
- **Zimmer all-minor modal** — `i – iv – v` all minor, dwell on iv as the emotional center, NO V7 (no leading tone). `Am – Dm – Em`, looped. From Hans Zimmer "Interstellar Main Theme."
- **Modal-mixture intro on drone** *(Dream Theater "Voices")* — Over a single pedal root (e.g. A bass), have the upper voice cycle through `1 – b3 – 3 – 4 – #4 – 5` of the minor scale, mixing Aeolian (b3) with Lydian (#4) inside the same line. Gives a riff a Lydian flick inside Aeolian without ever changing chord. Voices does this for 12 bars on an A pedal in 9/8. Use as an INTRO device — single-chord-but-not-static. In Bm: bass on B, upper line cycles `B-D-D#-E-F-F#` (b3 and #4 both present).

### Bass-led patterns

**META-PRINCIPLE — Bass-line-first design** *(for ballad-form sections)*: when a section needs ballad gravitas, **sketch the bass line FIRST**, then pick chords that put the right notes in the bass. Hooktheory's "Chord Bass Melody" metric ranks stepwise ascending/descending bass as one of the TOP-FIVE composition quality axes (alongside chord complexity, melody complexity, chord-melody tension, and progression novelty) — and the exemplar list is overwhelmingly piano-led ballads: Iris (Goo Goo Dolls), Stairway to Heaven, Your Song (Elton John), Someone Like You (Adele), Living on a Prayer, This Love (Maroon 5), You're Beautiful, Levon, Lean on Me, Mardy Bum (Arctic Monkeys), Whataya Want From Me, Walt Grace's Submarine Test, My Heart Will Go On. **Stepwise bass IS the ballad-arrangement signature.** The chords are the consequence, not the cause.

Common stepwise bass shapes (write the bass walk first, then voice chords above):
- **Descending diatonic** (most common ballad move) — In G major: bass G→F#→E→D→C→B→A→G → chords `G – D/F# – Em – D – C – G/B – Am – G`. Verified Iris, Whataya Want From Me, Stairway intro.
- **Ascending diatonic** (build/lift) — In C major: bass C→D→E→F→G → chords `C – Dm – C/E – F – G`. Verified Lean on Me, "Heart and Soul" but with extensions.
- **Descending chromatic** — bass walks down in half-steps (E→Eb→D→Db→C). Each chord re-harmonizes the bass note. Verified Whiter Shade of Pale, Stairway middle.
- **Ascending then descending** (arch) — bass climbs then falls within the section. Verified Hey Jude, Your Song.

Design discipline: when composing a ballad chorus, **write the 8 bass notes you want first**, drawing a line on paper or in your head. THEN pick chords for each. THEN add `voicing` decisions. Reversing the order (chords first → see what bass falls out) leads to the static-tonic-pedal default that's harder to make compelling.

- **Pedal-tone vamp** — Hold one bass note while harmony shifts above: `Em – Cmaj7/E – Am/E – B7/E`. The E never moves.
- **Chromatic walk-down** — Bass descends in half-steps through passing chords: `Em – Eb° – D – Db° – Cmaj7 – Bm7`.
- **Tonic-pedal chorus** — In a major chorus, keep I in the bass: `E – A/E – B/E – E`.

### Voice-leading (Polyphia/Plini)
- **Common-tone hold** — Pick chords sharing a top note. `Em9 – Cmaj7 – Gadd9` all share a B.
- **Half-step voice leading** — Each chord-tone moves only a half-step or stays. "Floating" feel.
- **Polyphia parallel-major slide** — `bVI(maj) – V(maj) – i – v(maj)`. In Bm: `G – F# – Bm – F#m`. The major v (F# major instead of F#m) creates bright/dark juxtaposition over the minor tonic. From "G.O.A.T."
- **Zimmer common-tone reharm** — Where you'd expect `vi`, substitute `IVmaj7` (shared third). In G: `Am – G – D – Cmaj7` (where Em was expected). Common tones bind it; avoids tonic emphasis. From "Time" (Inception).
- **Hisaishi descending-bass maj9 cascade** — `IVmaj9 – Imaj9/3 – bVIImaj9/3 – vii°m7/3`. Bass descends chromatically under shimmering maj9 voicings. In F: `Fmaj9 – Cmaj7/E – Bbmaj7/D – Bm7b5/C#` (approximating quartal Hisaishi color with parser-friendly chords). From "One Summer's Day."
- **Static-triad chorus with chromatic bass walk** *(Dream Theater "Voices")* — Upper voice **freezes on a single major triad** while the bass walks chromatically underneath. In A major upper voicing: bass walks `A → F → E → C# → F# → F → E → C# → C → A` while the top stays at `C#-E-A`. Reads as `I → bVI → V → III → #IV → bVI → V → III → bIII → I` but is harmonically ILLUSORY — the chord identity is the bass, not the triad. The fixed upper triad means every bar gets reinterpreted by the bass move. **Don't notate these as separate chord symbols in the spec; instead pick the chord names that match each bass note + the fixed triad** (e.g. `A, F/A→Fmaj7add#5, E/A→A/E inversion, C#/A→Aadd6/C#`, etc. — but those won't parse, so simplify with the closest parser-supported chord per bar). The aesthetic insight is the **perceived modulation** without a real key change. Use as a chorus device when the song needs a big "lift" without abandoning the verse's key.

### Rock cadences
- **Pink Floyd** — `i – bVII – bVI – V7`. `Em – D – C – B7`. Classic dramatic minor.
- **bVI-bVII-i lift** — `C – D – Em`. The "epic three-chord."
- **bIII-bVII-IV-i** — `G – D – A – Em`. Stairs of fifths, anthem-y.
- **Picardy 3rd ending** — End a minor section on the major i (E major chord at the close of an Em verse). Massive resolution.
- **Dream Theater ballad with inversions** — `I – I/3 – vi – IV`. In G: `G – G/B – Em – C`. Stepwise bass under a static melody — the band's quieter melodic side. From "Through Her Eyes."

### Andy Timmons — melody-as-architecture *(verified from Riff Journal / Guitar9 / MESA-Boogie / Glide / MisplacedStraws interviews)*

Andy Timmons's compositional school sits inside the Rock pack but inverts the usual chord-first reasoning. The melody is the *spine*; the chords are the *support that emerges from the melody*. Reach for these idioms when the user names Timmons, requests "Electric Gypsy-style," asks for "instrumental rock that's songful," or activates the Timmons clause to license a forbidden progression.

- **The "Electric Gypsy" vessel** — `I – V – vi – IV` looped indefinitely (in D: `D – A – Bm – G`). Under the Timmons clause this is permitted *iff* paired with a composed vocal-style `melody`. The chords are wallpaper; the melody is the painting. Tempo around 120–130; keep the chord rhythm dead simple (1 bar per chord, no rhythmic variation) so the melody can breathe.
- **Open + tapped harmonic intros** — first 8–16 bars of a Timmons piece often outline the melody via natural harmonics (12th, 7th, 5th fret nodes) and tapped harmonics targeting chord-tone 3rds (e.g. over an A major chord, tap C# on the A string at the 4th fret = 3rd of A). The script can't notate harmonics directly, but the *melodic intent* — sparse high-register melody notes one per chord — is captured by a slow `melody` array on the `clean` or `lead` role with `feel: "sparse"` and drums absent. Document `move: "harmonic-melody intro (user plays naturals/tapped, MIDI shows the pitches)"`.
- **Target-note resolution per phrase** — every melodic phrase should *land on a chord tone of the chord underneath at the moment of arrival*. Andy's working definition of resolution (from Guitar9): "the passing of a dissonant note to a consonant note" — tension and release. When composing the `melody` array: design phrase endings to coincide with chord changes, and pick a chord-tone pitch (root, 3rd, 5th, 7th of the current chord) as the landing note. Non-chord tones are passing color *between* the landings.
- **Vocal-style contour** — Andy's melodies are "vocal lines that happen to be played on guitar." Concrete: 1) range stays inside a singable octave-and-a-fifth (B3–F#5 in a vocal-mid register), 2) phrases have *breath stops* — rest beats every 4–8 notes, never a continuous shred line, 3) repeat-then-vary — say the melodic idea once, then say it again with a small variation (interval change, rhythmic displacement) instead of always inventing new material. From Guitar9: "I'm really trying to emphasize the song and using technique as a color to paint with."
- **Single-guitar-track integration** — Andy's *Resolution* album principle: "chords and melody had to be on one guitar track." Score equivalent: when composing in Timmons mode, drop `rhy_l` and `rhy_r` and let `clean` (arpeggiated chord tones) + `lead` (the melody) carry the harmony together. The chord identity lives in the *combination*, not in any single layer. Cousin of the Jack Thammarat aesthetic principle ("chord identity lives in the BAND, not in any one instrument") but with a smaller ensemble.
- **6th interval melodic moves** — Timmons frequently writes melodies in *parallel 6ths* (two voices a 6th apart moving together). On guitar this is two strings played simultaneously; in the spec, write the upper voice as `melody` and let the `clean` arpeggio echo it a 6th below. Or document `move: "melody in parallel 6ths — user doubles in performance"`. The interval color is the signature.
- **No-solo instrumental** — Andy explicitly designs pieces that *don't have a guitar solo* — the composed melody IS the song. Spec equivalent: include `lead` with a `melody` array but DON'T plan a 16-bar improvised solo section. Every section is melodic-thematic; no "shred bridge." The Timmons school's most radical move against the instrumental-guitar genre's self-indulgence.
- **Volume-knob dynamics architecture** — from MESA-Boogie: "I'm on the volume control a lot for different phrases." When the same guitar track plays chords AND melody, dynamics are how you separate them. Spec equivalent: the `melody` should use higher velocities (90–110) than the `clean` accompaniment (60–75). The dynamic gap = the texture.
- **Improvise → extract → compose** — workflow note, not a spec field. When generating Timmons-style sections, design the melody as if you'd jammed it first and then refined the best bits. Avoid melodies that feel "composed-on-paper" (too symmetric, too sequential). Imperfections, slight asymmetries, and "one note longer than expected" are the marks of an improvised-then-frozen line.

**When to invoke this section:** user says "Andy Timmons" / "Electric Gypsy" / "Resolution" / "Theme From A Perfect World"; OR you're activating the Timmons clause to permit a forbidden progression; OR the brief asks for "instrumental rock where the melody is the song" / "no shred, just melody" / "vocal-style guitar lines." For "epic" or "anthemic" briefs, the Andalusian / Pink Floyd / bVI-bVII-i moves are usually a better fit than Timmons school — Andy's vibe is *intimate* virtuosity, not arena.

### Lydian / major-key tricks *(use sparingly — for ballads only)*
- **Lydian #4 lift** — IVmaj7 with #11 on top. In E major: Amaj7 with D# melody note. Satriani's soaring sound.
- **bVII in major** — Drop a D chord in E major. Mixolydian rock color.

### Modulations
- **Up a step for last chorus** — Em → F#m. Cliché but works.
- **Common-tone modulation** — Pivot through a shared note to a distant key.
- **Phrygian-dom V** — In a minor key, V7 with the raised 7th of harmonic minor. B7 (with D#) in Em. Strong pull.
- **Modulate by fifth (down)** — `Dm → Am`. Move to the dominant key. Common in jam-style extended sections. Shares 6 of 7 scale notes — smooth transition.
- **Cycle through related minors** — `Dm → Am → Em`. Each new tonic is a fifth lower than the last. Used in extended instrumental rock pieces and post-rock builds.
- **Dream Theater sequential key shifts** — Bridge moves through abrupt diatonic key changes — no common-tone smoothing, just cuts. Like `Dm section → G major section → F major section`, each ~8 bars. From "Hollow Years."
- **bIV → i chorus modulation** *(Symphony X "The Odyssey")* — verse in a major key, chorus drops to the minor of the verse's IV. In G major verse: chorus modulates to **C minor** (the IV-as-minor-tonic). Mechanism: G is V/Cm, so the verse's tonic functions as the chorus's dominant — pivot is built in. More gravity than relative-minor switching; less abrupt than direct half-step modulation. Verified across multiple Symphony X choruses.
- **Chromatic-mediant lift up a major third** *(Symphony X "The Odyssey" bar 250)* — bridge or post-solo section jumps UP a major 3rd from the current tonic. Cm bridge → C# major section. Classic "Strauss/Star Wars" cinematic lift; also Romeo signature for "the band shifts to a brighter universe" without modal-mixture preparation.
- **Half-step descent ending** *(Symphony X "The Odyssey" bar 676)* — final section modulates DOWN a half-step from the previous section's tonic. F minor → Eb minor. Anti-pop: most prog modulations go UP for triumph; descending modulation gives a more grief-laden, resigned color. Pair with a slow ritardando outro.
- **Common-tone diminished turnaround** *(APP "Where's the Walrus?")* — use a diminished 7 chord that shares notes with both the previous and next chord as a passing chord. In A Dorian: `G6 → A11 → ... → Fdim7 → E7 → G/A` — Fdim7 is the common-tone dim7 of A minor (shares F-Ab-B-D with vii°7/A), resolving deceptively to bVII-i instead of i. Used as an 8-bar turnaround in fusion contexts.

### Time/feel moves
- **Halftime bridge** — Same chord changes, `feel: "halftime"`. Massive contrast without changing tempo.
- **Build via density** — `sparse` intro → `halftime` verse → `driving` chorus. The `feel` field is your dynamics knob.
- **Odd time** — 7/8 for Plini, 5/4 for Polyphia. Try it occasionally.
- **3/4↔2/4 alternating hemiola transition** *(Dream Theater / Portnoy "Voices")* — alternate bars of 3/4 and 2/4 on a single chord, repeating. Creates a 5-beat pseudo-cycle inside a metric-modulation transition. Use as a "lift" between sections in a prog/heavy song. The skill's script doesn't support time-sig changes mid-song, so document in `move` for the user to apply manually in Reaper — OR generate the whole transition section in a "5/4" time sig that feels like 3+2.
- **Single 7/4 turnaround** *(APP "Some Other Time")* — insert ONE bar of 7/4 between two normal 4/4 sections to drop a beat — feels like a held breath before the next section. Quick prog gesture; the rest of the song stays in 4/4. Same script limitation — document in `move`.
- **Hemiola bass cell with modal flip** *(Dream Theater "Voices")* — repeating bass cell like `A-G-A-C` (4 beats) under an upper triad that swaps Dorian (raised 6 = F#) and Aeolian (natural 6 = F natural) every other bar. The bass is static, the *mode* is the variable. In Am: bass `A-G-A-C` looping, upper triad alternates `Am6 → Am` every two bars. Use as a vamp-with-instability before resolving to a chorus.

### Cinematic / sad cadences
- **Anti-cadence (end on V)** — `Am – G – F – E` then... stop. The E (V7) never resolves to Am. Massive emotional hang.
- **Phrygian-dominant unresolved fade** *(Dream Theater "Voices" outro)* — end the song on V with BOTH the ♭2 and the major 7 (leading tone) active simultaneously. In Am: final chord stack `E + G# + B + D + F (natural)` — Phrygian-dominant V7♭9 with no resolution. The clash of G# (raised 7) and F natural (♭2 of E Phrygian-dom) is the signature. Then fade. Heavier than a plain anti-cadence; suits prog-metal endings.
- **Suspended hang** — `Asus2 – Asus4 – Asus2 – Asus4` over a static A bass. Floating, no decision.
- **Subdominant minor in major** — In C major, sneak in `Fm` or `Abmaj7` (Lana del Rey's "saddest chord"). Modal interchange that pulls heartstrings.
- **Anti-Picardy** — At a final cadence that wants the major i, refuse. Stay minor. Cling.
- **Plagal cadence (IV-i)** — Softer than V-i. More resigned. `Am – Dm – Am` instead of `Am – E – Am`.
- **Descending suspensions** — Each chord more open than the last: `Am – G/B – Cadd9 – Cmaj7/B – Am(add9)`.
- **Pedal under a falling melody** — Hold one bass note while the chord above descends through sus chords.
- **Single-chord meditation** — 8-16 bars on one chord. The "song" is the dynamic shape, not the harmony.
- **Hisaishi plagal substitution** — Where you'd use `ii – V – I` (jazz), substitute `IV – V – I` (Ghibli cadence). In C: `F – G – C`. Bigger plagal lift, simpler, more melodic-pop. Common across Joe Hisaishi's Ghibli scores.
- **Hisaishi deceptive-restart loop** — A modal chord chain that loops back to its start instead of resolving via V. In Cm: `Abmaj7 – Gm7 – Fm7` (bVI-v-iv), then restart from Abmaj7. Never offers the listener "home."
- **Modal Aeolian with NO V chord** *(Zimmer / Einaudi)* — strictly exclude V7 (and the dominant V triad) from the palette. Use only `i, bIII, iv, v(minor), bVI, bVII`. The piece must be PURELY natural-minor — no leading tone resolution allowed. Verified from Zimmer "First Step" (loop = `bVI – bVII – i – bVII` for 30 bars), Zimmer "Time" (`Am – Em – G – D` with Em as v not V), Einaudi "Nuvole" (`i – bVI – bIII – bVII`). The harmonic gravity sits on bVI more than on i.
- **Tonic delay via inversion** *(Yiruma / Einaudi)* — never voice the tonic (i or I) in root position on a downbeat. Use `I/3` or `I/5` (or for minor, `i/3` or `i/5`). Tonic is implied, never asserted. Verified from Yiruma "River Flows In You" (A/D every other half-bar — A chord never in root position 2nd half of any bar) and Einaudi "I Giorni" (D/F# every fourth bar — tonic in 1st inversion).
- **Skyfall stepwise chorus descent** *(Adele / cinematic-pop)* — 8-chord chorus walking down the scale: `i – ♭VII – ♭VI – V – iv – ♭III – ii(°) – V7` in half-bar rhythm (2 beats per chord). In Cm: `Cm – Bb – Ab – G – Fm – Eb – Dm7 – G7`. Eight distinct changes, bass walks down by step (C–Bb–Ab–G–F–Eb–D–G), final V7 with raised leading tone (the "Bond chord"). Don't loop a 4-chord pattern — the descent IS the chorus.
- **Bridge via descending-inversion chain** *(Yiruma)* — when an otherwise loop-form piece needs ONE bridge, walk the bass down through chord inversions. In A major: `Bm/F# → A/D → A → C#m/E → F#m/C# → A/D`. Stepwise descending bass (F# → D → A → E → C# → D). The only chromatic motion in the piece is right here.
- **Bond chord (harmonic-minor V7)** *(cinematic-pop)* — in minor keys, use V7 with the raised leading tone: G7 in Cm (B natural), B7 in Em (D# natural), F#7 in Bm (A# natural), E7 in Am (G# natural). Place at every cadence point in cinematic-pop arrangements. The leading-tone pull is the cinematic-pop signature — distinct from modal-cinematic (subschool A) which excludes V7 entirely.
- **Einaudi common-tone RH pedal** — when the script's `pad` role plays sustained chord-tones, document in the section's `move` field that the user should swap the pad VST patch to a sequenced/arpeggiated pattern playing the root+5th of the TONIC (not of each chord). The RH should NOT track chord tones — it should sit on tonic-and-5th 8th-notes while the bass changes underneath. Verified from Einaudi "Nuvole Bianche" (RH plays F4+Bb4 dyad + Ab4 fills over Fm AND over Db, Ab, Eb chords — common-tone glue). Effect: the upper voice barely moves while harmony shifts — opposite of normal chord-tone arpeggio.

### Spanish / Phrygian moves
- **Andalusian cadence** — `i – bVII – bVI – V7`. `Em – D – C – B7`. THE Spanish move. Loop it forever.
- **Phrygian-dom V** — `B7` with raised D# (leading tone) over Em. The exotic Spanish color.
- **bII Phrygian signature** — `Em – F – Em`. Half-step pull. Hypnotic.
- **Three-chord vamp** — `Em – F – Em – F – G – F – Em`. Loops, builds, never resolves cleanly.
- **Bulería 6/8** — In 6/8 feel: chord every 3 beats (so 2 per bar). Hemiola tension.
- **Picardy 3rd ending (Spanish version)** — End on E major (Picardy of Em). The flamenco "olé" close.
- **Cycle of fourths in Phrygian** — `Em – Am – Dm – G – Cmaj7 – F – B7 – Em`. Walks through the mode.
- **Avoid 7ths and 9ths** — Plain triads are correct here. Add a 7th and it sounds jazz, not Spanish.

### Neoclassical metal moves *(Symphony X / Yngwie / Romeo)*
- **bII voiced as maj7 chord** *(Symphony X "The Odyssey," "Candlelight Fantasia")* — in Phrygian-dominant contexts, voice the bII not as a plain triad but as a full maj7. In E Phrygian-dominant: `Bbmaj7` instead of `Bb`. In C Phrygian-dominant: `Dbmaj7` instead of `Db`. The 7th of the bIImaj7 chord doubles as the natural leading tone of the tonic minor (Bbmaj7 contains A natural = the leading tone of Bm; Dbmaj7 contains C natural = the leading tone of Cm). Double-function dissonance: b2→1 (Phrygian pull) AND 7→1 (leading-tone pull) in the same chord. **Romeo neoclassical-metal signature.**
- **Minor-third ladder climb** *(Symphony X "Candlelight Fantasia" solo section)* — all-major-triad ascending chord cycle with roots in minor 3rds: `F – G# – Bb – C#`. 2 bars per chord. The chord roots outline a diminished 7 (F-Ab-B-D enharmonic), creating maximum tonal ambiguity while staying tonal. Pure neoclassical shred bed — soloists improvise harmonic-minor scales centered on the ROOT MOTION rather than a single home key.
- **Whole-step modulation post-solo sequence** *(Symphony X "Candlelight Fantasia")* — after a solo section, modulate up in whole-step (or alternating whole-step + minor 3rd) sequences as a "lift": `Cmaj7 → Ebmaj7 → Fmaj7 → Abmaj7`. Each chord 2-4 bars. Functions as a giant pre-chorus build that arrives in a new key entirely.
- **Phrygian-dominant locked riff in odd time** *(Symphony X "The Odyssey" 11/8 section)* — single-chord-or-two-chord riff in odd time (11/8, 7/8, 15/8) where the upper structure rotates through Phrygian-dominant scale tones: in E Phrygian-dom: `E5 - Bbsus4maj7 - E5 - Bsus4 - A# - D - E5`. The Bb (b5/#4) and F (b2) ARE the scale signature. Locked in odd time = neoclassical math-metal hybrid.
- **Augmented triad as functional dominant** *(Symphony X "The Odyssey" bar 608)* — instead of plain V or V7 cadencing to i, use V+ (augmented). In Fm: `C+ → Fm` instead of `C7 → Fm`. The augmented 5 (G#) doubles as the leading tone (G# is half-step from A natural = b3 of Fm). Baroque cadence material — Bach used this constantly. Pair with maj7 pivots (`Gmaj7 → E+7 → C+ → Fm`) for fully baroque sequencing.

### Synthwave loops
- **Classic synthwave** — `Am – G – F – G`. Loops. The whole song.
- **Carpenter Brut darkwave** — `Am – Em – Dm – G`. i – v – iv – bVII. Driving and dark.
- **Stranger Things-y** — `Am – F – C – G` over a four-on-floor kick.
- **Drive (Kavinsky) pattern** — `Am – G – F – E7` — Phrygian-dom-flavored synthwave (rare crossover).
- **Arpeggiated bass under static pad** — Pad holds `Am` for 4 bars while bass plays `A – C – E – C – A – C – E – C`.
- **Major-key synthwave (rare)** — `C – G – Am – F` but with four-on-floor and saw pads, not pop drums.

### Modern rock progressions (alt-rock, post-hardcore, emo)
Vocal-rock idioms — work in any minor-key rock song. Notation uses major-key roman numerals where `vi` is the minor "stand-in tonic" (e.g. Am in C major).

- **The modern rock anthem** — `vi – IV – I – V`. `Am – F – C – G`. The most-used minor-key rock progression of the 21st century. Linkin Park "Numb," Kings of Leon "Use Somebody," Boys Like Girls "Great Escape."
- **Warmer variant** — `vi – I – IV – V`. `Am – C – F – G`. Less darkness, brighter arrival on the I.
- **Linkin Park dark** — `vi – I – V – IV`. `Am – C – G – F`. "What I've Done," "In The End." The stepwise V-IV gives a searching, unresolved feel.
- **Emo verse hammer** — `vi – IV – vi – IV`. `Am – F – Am – F`. Saosin "You're Not Alone," Underoath. Mantra loop — the verse never "moves."
- **Dark stepwise verse** — `vi – V – IV – V`. `Am – G – F – G`. Linkin Park "In The End" intro. Avoiding the I makes it feel minor and brooding.
- **Paramore lift** — `IV – V – vi – iii`. `F – G – Am – Em`. The iii at the end is the nostalgic move. Distinctive.
- **The Decode** — `IV – ii – vi – iii`. `F – Dm – Am – Em`. Paramore "Decode." Dark and parallel — every chord shares two notes with the next.
- **Descending-bass long form** — `I – V/B – vi – V – IV – I/E – ii – V`. In C: `C – G/B – Am – G – F – C/E – Dm – G`. The Black Parade verse. 8-bar stepwise bass descent.
- **Pre-chorus IV-V-IV-V** — `F – G – F – G` building to a chorus on C. The simplest functional buildup. Used everywhere in modern rock pre-choruses.
- **Pre-chorus IV-V-vi-V** — `F – G – Am – G`. Slightly more interesting — visits the vi before settling on V for the launch.
- **Post-chorus I/E-IV-V-vi** — `C/E – F – G – Am`. Cools down from chorus back into verse via stepwise descent.

### Djent / heavy moves
- **Pedal-root chugs** — Bass and rhythm guitar hammer a low E (or D) while pad shifts above. Constant motion in rhythm, slow in harmony.
- **Tritone displacement** — `Em – Bbm – Em – Bbm`. Roots a tritone apart = maximum tension.
- **Chromatic b2 root motion** — `E5 → F5 → E5`. Roots a half-step apart. The Phrygian-color metal move (Morbid Angel, Slayer). For lead: E Phrygian-dominant scale (E F G# A B C D).
- **Leading-tone root motion** — `E5 → D#5 → E5`. Half-step approach from below. Suspenseful build into the tonic. For lead: E harmonic minor.
- **Diminished walk** — Two power chords a minor third apart (`E5 → G5 → Bb5 → Db5`). All within the E diminished scale. Trey Azagthoth / Kerry King territory.
- **Polyrhythm of 3 over 4** — Chord changes every 3 beats while drums stay in 4/4. Phasing tension.
- **Slow-fast counterpoint** — Chord changes every 8 beats (slow harmony) over 16th-note rhythm chops (fast surface).
- **bII chug** — `Em – F` hammered (Phrygian-influenced metal). Periphery-ish.
- **Power-chord only voicings** — Forget m7, m9. Just root + 5th.

### Jazz-funk / fusion moves
- **ii-V-I** — `Dm7 → G7 → Cmaj7`. The bread and butter. In any key.
- **ii-V-I in minor** — `Bm7b5 → E7 → Am7`. Same shape, darker.
- **Secondary dominants** — `A7 → Dm7` in C major (acts as V7 of ii). Chromatic spice.
- **Tritone substitution** — `Db7 → Cmaj7` instead of `G7 → Cmaj7`. Identical resolution, fancier color.
- **Cycle of fourths (Autumn Leaves)** — `Cmaj7 → Fmaj7 → Bm7b5 → Em7 → Am7 → Dm7 → G7 → Cmaj7`.
- **Modal mixture (IV minor)** — `C → F → Fm → C`. The IV-minor pull. Bittersweet.
- **bVII rock color in major** — `C → Bb → F → C`. Classic Jack Thammarat / Mateus Asato.
- **Chromatic planing** — `Cmaj7 → C#m7 → Dm7 → D#dim7 → Em7`. Climbs by half-steps.
- **Backdoor cadence** — `Fm7 → Bb7 → Cmaj7`. iv7-bVII7-I, jazzy approach to the tonic.
- **Coltrane changes (major-third cycle)** — Tonal centers move by major thirds, each preceded by its own V7. In C: `Cmaj7 → Eb7 → Abmaj7 → B7 → Emaj7 → G7 → Cmaj7`. From Coltrane "Giant Steps." Substitutes for a long ii-V-I.
- **Neo-soul chromatic diminished passing** — Slip a #IVdim7 (or #ii dim7) between IV and V for smooth chromatic voice-leading. In C: `Fmaj7 – F#dim7 – C/G – G7`. Adds the soulful chromatic slide.
- **Sus over dominant (V13sus4)** — Voice the IVmaj7 over the V bass to imply both subdominant and dominant at once. `Fmaj7/G = G13sus4` essentially. In C: `Cmaj9 – Am11 – Fmaj7/G – Cmaj9`.
- **Quartal dyads** *(Jack Thammarat / Larry Carlton)* — comp the piano in **perfect 4ths** instead of stacked 3rds: over an Em7 chord, play `E+A` (not `E+G`); over F#m7, play `F#+B`. Two notes only, narrow mid-register span (octaves 3-4). Implies extended/sus harmony without ever naming m7. The chord identity is *inferred* from bass + dyad, not stated. Verified from "On The Way" MIDI transcription.
- **Mixolydian I-♭VII-IV-V verse** *(Jack Thammarat)* — `D – C – G – A` looped, in D major. The ♭VII (Cmaj7) is the signature — sounds like rock but is functionally Mixolydian. NOT a borrowed iv chord; it's the natural ♭VII of Mixolydian. Use as a 4-chord verse engine with each chord lasting 1 bar (4 beats).
- **Stepwise diatonic bass chorus** *(Jack Thammarat)* — bass climbs scalewise rather than leaping. In D: `Em7(E) – F#m7(F#) – Gmaj7(G) – A(A)` — bass walks E→F#→G→A. Gives the chorus a vocal/horn-melody quality.
- **♭VI passing detour** *(Jack Thammarat)* — drop a `bVI` between two diatonic chords as a momentary surprise. In D major: `G – Bb – C – G`. The Bb resolves *backwards* through C (♭VII) → G (IV), not forward to V or I. Modal-mixture detour without commitment.

### Post-rock builds
- **The Mogwai inversion** — Start sparse and dissonant (sus2 over wrong bass), resolve to consonant and LOUD.
- **One-chord ostinato** — Bass loops a 4-note line under a single pad chord for 32+ bars.
- **bVI surprise in major** — In E major, drop a C chord at the climax. Emotional jolt.
- **Build via track-by-track entry** — Section 1 only pad. Section 2 adds bass. Section 3 adds rhythm guitars. Section 4 adds drums. The chords don't change, the *texture* does.
- **Anti-chorus** — The "chorus" is identical chords to the verse but with full instrumentation. The lift is dynamic, not harmonic.

## Song forms catalog

When choosing a `form` array, pick from this catalog. **Don't default to the same `I-V-C-V-C-B-C-O` every time.** Forms below use letter notation: **A** = verse-like, **B** = chorus-like, **C** = bridge, **I** = intro, **O** = outro, **P** = pre-chorus, **S** = solo/instrumental, **T** = setup turnaround, **H** = halftime breakdown.

### Section-type vocabulary (beyond verse/chorus/bridge)

Real songs use connector and breather sections that aren't captured by the basic A/B/C labels. Reach for these when designing form:

- **Setup / turnaround (T)** — 3-bar (or 4-bar) connector between two main sections. Functions as a "harmonic exhale and reset." Often reuses the verse's harmonic loop compressed to a shorter length, ending on V to launch the next section. Verified usage: Jack Thammarat "On The Way" uses 3-bar `D · C · G | D · C · G · A` setups before each verse. Use spec section name `"setup"` or `"turnaround"`. Roles often: bass + pad + clean only (rhy guitars and drums minimal or absent).
- **Halftime breakdown (H)** — Sparse 2-chord or single-chord vamp that breathes before a final chorus. Drums shift to halftime feel (or drop entirely), rhy guitars drop, harmony moves to one root for 4-8 bars. Verified usage: Jack Thammarat "On The Way" has a 7-bar `D · C · D` halftime breakdown immediately before chorus 2. Use spec section name `"halftime-break"` or `"breakdown"`.
- **Coda / outro vamp (O)** — Extended outro that vamps on the verse loop (or a slight variant) for 8-12 bars before fading or landing on a sustained tonic. Different from a short `outro` section that just bookends — the coda is the song's "extended exit." Use when a song earns a long tail.

### Important: literal repetition vs. variant sections

When two consecutive form entries have the **same section name** (e.g. `["verse", "verse"]`), they are **LITERALLY identical** — same chords, same feel, same MIDI. No variation between iterations.

To get real variation between "verse 1" and "verse 2," define **separate sections** with different names:

```json
"sections": [
  {"name": "verse-a", "feel": "halftime", "chords": [...]},
  {"name": "verse-b", "feel": "halftime", "chords": [...with the last chord swapped for variation...]},
  ...
],
"form": ["intro", "verse-a", "verse-b", "chorus", ...]
```

Variant sections can differ by:
- One chord swapped at the end (turnaround variation)
- Same chords with different `feel` (halftime → driving)
- Different `skip_roles` to add/remove layers (build via density)
- Parallel-key shift (verse-a in Am, verse-b in A major)

When you choose a form below with repeated letters (e.g. `AABA`), decide **per song** whether each repeat is literal (same section name) or a variant (different section name). Literal is fine for most cases; variant is the move when you want to BUILD across the repeats.

### Forms to draw from

**1. AABA** *(32-bar jazz standard)*
Verse-verse-bridge-verse. The classic American songbook form. Works great instrumentally — Stella By Starlight, Body And Soul shape.
`["verse", "verse", "bridge", "verse"]`

**2. AAB** *(blues / single-bridge folk)*
Two verses then a bridge that ends the song. No formal chorus.
`["verse", "verse", "bridge"]`

**3. AABBA** *(verse-heavy with double chorus)*
Two verses, two choruses, return to verse. Lots of rock songs use this.
`["verse", "verse", "chorus", "chorus", "verse"]`

**4. I-AABA-O** *(jazz standard with intro/outro)*
`["intro", "verse", "verse", "bridge", "verse", "outro"]`

**5. I-AA-B-A-B-O** *(two-verse intro into chorus)*
The form the user specifically called out — 2 verses before the first chorus, builds anticipation.
`["intro", "verse", "verse", "chorus", "verse", "chorus", "outro"]`

**6. I-AABB-A-C-B-O** *(extended rock — verse-heavy + bridge climax)*
`["intro", "verse", "verse", "chorus", "chorus", "verse", "bridge", "chorus", "outro"]`

**7. APBAPBCB** *(with pre-chorus)*
Verse-prechorus-chorus structure. Pre-chorus is where the build happens before each chorus.
`["intro", "verse", "prechorus", "chorus", "verse", "prechorus", "chorus", "bridge", "chorus", "outro"]`

**8. ABACABA** *(ternary / rondo)*
Symmetric form — verse, chorus, verse, bridge, verse, chorus, verse. Classical roots, but works for instrumental rock too. Each return to A is grounding.
`["verse", "chorus", "verse", "bridge", "verse", "chorus", "verse"]`

**9. ABCABC** *(three-part rotation)*
Verse-chorus-bridge played twice. Each repeat can be the same or slightly varied.
`["verse", "chorus", "bridge", "verse", "chorus", "bridge"]`

**10. AAAA-with-variants** *(strophic with builds)*
Single repeated section, each iteration as a variant (different layers via `skip_roles`, or different feel). Folk/post-rock single-mood pieces.
`["verse-a", "verse-b", "verse-c", "verse-d"]` where each variant adds or strips a layer.

**11. Through-composed** *(no repetition)*
Every section unique. Prog rock, film score, ambient. Best for cinematic / post-rock packs.
`["section-1", "section-2", "section-3", "section-4", "section-5", "outro"]`

**12. AB-C-AB-O** *(compact verse-chorus, bridge-as-mid)*
Verse-chorus pair, bridge, verse-chorus pair, outro. No second chorus before bridge.
`["intro", "verse", "chorus", "bridge", "verse", "chorus", "outro"]`

**13. I-A-B-A-B** *(unresolved)*
Verse-chorus twice and STOP. No bridge, no final return, no outro. Leaves the listener hanging. Indie/atmospheric.
`["intro", "verse", "chorus", "verse", "chorus"]`

**14. A-C-A** *(simple ternary)*
Verse, bridge as middle contrast, verse return. Three sections total. Suits short pieces or sketches.
`["verse", "bridge", "verse"]`

**15. I-T-A-P-B-T-A-P-H-B-O** *(Jack Thammarat "On The Way" form — verified from MIDI transcription)*
Intro, setup-turnaround, verse-long, prechorus, chorus-short, setup-turnaround, verse-short, prechorus, halftime-breakdown, chorus-long (extended), coda outro. **Key signature: section-length asymmetry.** Verse 1 is *long* (12 bars), verse 2 is *short* (6 bars). Chorus 1 is *short* (6 bars), chorus 2 is *long* (12 bars). The second half FLIPS the ratio so the song lifts at the end. The halftime-breakdown right before chorus 2 is the "earned arrival" device.
`["intro", "setup", "verse-long", "prechorus", "chorus-short", "setup", "verse-short", "prechorus", "halftime-break", "chorus-long", "coda"]`
Best for: jazz-funk / melodic fusion. Pair with the Jazz-funk pack subschool A.

### How to pick

1. Look at recent outputs (`ls <output_root>/_<year>/composer/ | tail -5` and read their `spec.json`). If the last 2-3 songs were standard `I-V-C-V-C-B-C-O` (the overused default), pick something different.
2. Match form to mood:
   - **Patient, anticipatory**: form 5 (`I-AA-B-A-B-O`), form 11 (through-composed)
   - **Verse-heavy storytelling**: forms 3, 6
   - **Jazz idiom**: forms 1, 4 (AABA family)
   - **Brutally short / sketch**: forms 2, 14
   - **Symmetric / classical-influenced**: form 8 (ABACABA)
   - **Build-via-density**: form 10 (strophic with variants — use different section names)
3. Don't fight the genre: synthwave loops a lot (forms 2, 3, 13). AABA fits jazz-funk. Through-composed fits cinematic. **Jazz-funk subschool A specifically** wants form 15 (Jack Thammarat verified) or form 7 (APBAPBCB) — both have prechorus and lots of setup/connector space.

## Arrangement archetypes catalog

After choosing form and feel-arc, pick an **arrangement archetype** — *which layers play in which sections*. Don't invent `skip_roles` from scratch for every song; pick from this catalog and adapt.

Each archetype below sketches a per-section role plan using these abbreviations:
- `B` = bass, `P` = pad (PIANO), `D` = drums, `RL`/`RR` = rhy_l/rhy_r, `C` = clean, `S` = strum, `SP` = synth_pad (SURGE XT)

### The single-loop-iterated build *(meta-principle, not an archetype)*

Before picking an archetype, decide whether the song is **multi-section** (verse/chorus/bridge each with distinct chords — most archetypes below) or **single-loop** (ONE chord progression iterated many times, with sections distinguished only by texture).

The single-loop build is the modal-cinematic and post-rock default. Verified from:
- Zimmer "Time" — 16-bar `Am-Em-G-D / Am-C-G-D` loop iterated **7 times** across 112 bars, climax via density only
- Zimmer "First Step" — `bVI-bVII-i-bVII` 4-bar loop iterated ~12 times across 50+ bars
- Einaudi "Nuvole Bianche" — `Fm-Db-Ab-Eb` 4-bar loop iterated ~30+ times across 144 bars
- Einaudi "I Giorni" — `Bm7-A-Gmaj9-D/F#` 4-bar cycle iterated ~50+ times across 256 bars
- Yiruma "River Flows In You" — `F#m-A/D-A-E` 2-bar loop iterated across 47 bars (one descending-inversion bridge breaks the loop)

**How to write a single-loop song:**
1. Write ONE chord progression in the `sections` array (e.g. `"name": "loop", "chords": [...]`).
2. Reference that same section multiple times in the `form` array, but with **different section names** that each have `skip_roles` controlling which layers play.
3. Alternative: define multiple sections with **identical `chords` arrays** but different `name`s, `skip_roles`, and `move` descriptions to encode the textural progression.

Example spec sketch (single-loop modal-cinematic):

```json
"sections": [
  {"name": "intro",          "feel": "sparse", "drums": "none", "skip_roles": ["clean","rhy_l","rhy_r","drums","synth_pad"], "chords": [<the loop>]},
  {"name": "v1",             "feel": "sparse", "drums": "none", "skip_roles": ["rhy_l","rhy_r","drums","synth_pad"],         "chords": [<same loop>]},
  {"name": "v2",             "feel": "sparse", "drums": "none", "skip_roles": ["rhy_l","rhy_r","drums"],                     "chords": [<same loop>]},
  {"name": "climax",         "feel": "sparse", "drums": "none", "skip_roles": ["rhy_l","rhy_r","drums"],                     "chords": [<same loop, doubled durations or compressed>]},
  {"name": "outro",          "feel": "sparse", "drums": "none", "skip_roles": ["clean","rhy_l","rhy_r","drums","synth_pad"], "chords": [<same loop>]}
],
"form": ["intro", "v1", "v2", "v1", "climax", "v2", "outro"]
```

**Don't:** in a single-loop song, write a "chorus" with different chords. The point is the harmony stays IDENTICAL while the arrangement evolves. If you have time to write new chord progressions per section, you're doing multi-section, not single-loop.

**When to choose single-loop over multi-section:**
- User says "modal-cinematic," "Zimmer-like," "Einaudi-like," "Sigur Rós," "Mogwai," "Yiruma."
- User says "atmospheric," "ambient," "drone build."
- User asks for "a piece that builds slowly without changing chords."
- Cinematic-pop (Skyfall, subschool C) is NOT single-loop — it has distinct verse/chorus/bridge chord progressions. Stick to multi-section for that.

The arrangement archetypes below (1-10) are MULTI-section by default; for single-loop songs, archetypes 4 (Mogwai inversion) and 6 (Drone build) describe the texture progression to use over the unchanging harmony.

### 1. Slow build *(track-by-track entry, climax mid-song)*

Each section adds a layer until the second/final chorus, with the bridge stripping back hard before the final climb.
```
intro:    B P
verse-a:  B P C
verse-b:  B P C D
chorus-1: B P C D RL RR
verse-c:  B P C D
chorus-2: B P C D RL RR SP
bridge:   B P                (radical strip)
chorus-3: B P C D RL RR SP
outro:    B P
```
**Touchstones:** Plini "Selenium Forest," Tides From Nebula. **Pairs with:** Rock, Post-rock, cinematic-rock hybrids.

### 2. Hit and breathe *(classic quiet-loud contrast)*

Verses stripped, choruses full. The dynamic contrast IS the song.
```
intro:    B P SP
verse:    B P C              (no drums, no rhythm guitars)
chorus:   B P D RL RR        (full band, SURGE drops out)
verse:    B P C
chorus:   B P D RL RR SP
bridge:   B P                (huge dropout)
chorus:   B P D RL RR SP
outro:    B P SP
```
**Touchstones:** Foo Fighters quiet-loud, classic alt-rock. **Pairs with:** Rock, anything with strong V/C contrast.

### 3. Layer stack *(never strip, only add — EDM build)*

Start bare, accumulate layers, never go back. The drama is the gradual fill.
```
intro:    B D                (kick + bass only)
verse-a:  B D P              (+ pad)
chorus-a: B D P SP           (+ synth pad)
verse-b:  B D P SP RL        (+ one rhythm guitar)
chorus-b: B D P SP RL RR     (full)
bridge:   B D P SP RL RR     (no stripping ever)
chorus-c: B D P SP RL RR
outro:    B D P SP RL RR     → fade
```
**Touchstones:** Carpenter Brut, Justice, Daft Punk crossovers. **Pairs with:** Synthwave, Djent, electronic-rock.

### 4. Mogwai inversion *(sparse → climax → sparse)*

The climax is at the END (often the bridge or final chorus); everything fades back to atmospheric.
```
intro:    B P                (sparse, contemplative)
verse-a:  B P C
verse-b:  B P C D            (drums enter halftime)
chorus-1: B P C D            (build but not yet full)
verse-c:  B P C D
chorus-2: B P D RL RR SP     (build continues)
bridge:   B P D RL RR SP     (the CLIMAX is the bridge)
chorus-3: B P D RL RR SP
outro:    B P                (fade back to atmospheric)
```
**Touchstones:** Mogwai, Explosions in the Sky, Russian Circles. **Pairs with:** Post-rock, Cinematic.

### 5. Plini textural arc *(atmospheric verse, full chorus, instrumental-solo bridge)*

Layers shift purpose by section: chorus drops the atmospheric layers (clean, SURGE) and brings in the rock layers (rhy_l/rhy_r); bridge does the reverse, becoming the "instrumental solo" moment.
```
intro:    B P C
verse-a:  B P C SP            (atmospheric warmth)
verse-b:  B P C D SP          (drums halftime, still atmospheric)
chorus:   B P D RL RR         (full rock chorus, atmospheric layers OUT)
verse-c:  B P C D SP          (back to atmospheric)
chorus:   B P D RL RR
bridge:   B P C SP            (instrumental-solo moment, no rhythm guitars)
chorus:   B P D RL RR
outro:    B P C
```
**Touchstones:** Plini, Polyphia (melodic moments), Animals as Leaders. **Pairs with:** Rock, Cinematic-rock.

### 6. Drone build *(single harmonic idea, layers do all the work)*

Same chord progression in EVERY section. Variety entirely through layer changes and feel.
```
intro:    B P
verse-a:  B P C
verse-b:  B P C D
chorus:   B P C D RL RR SP    (full bloom)
bridge:   B P C                (back to atmospheric, chord still rings)
chorus:   B P C D RL RR SP
outro:    B P
```
**Touchstones:** Sigur Rós, Stars of the Lid, Tortoise. **Pairs with:** Cinematic, Post-rock.

### 7. Hisaishi swell *(orchestral track-by-track)*

Piano-alone opening, gradual additions toward tutti at the climax, intimate close.
```
intro:    P                   (piano alone)
verse-a:  B P                 (cellos enter as bass)
verse-b:  B P C               (high strings via clean arp)
chorus:   B P C D SP          (percussion + brass)
verse-c:  B P C
chorus:   B P C D SP RL RR    (tutti)
bridge:   B P                 (intimate piano + cello)
chorus:   B P C D SP RL RR
outro:    P                   (piano alone)
```
**Touchstones:** Joe Hisaishi, John Williams melodic, Zimmer ballads. **Pairs with:** Cinematic, jazz-funk ballads.

### 8. Hit and run *(everything in, no stripping — constant energy)*

All sections use the same role set. Variety comes from chord choice, feel, or voicing — never from layers. Pure energy maintenance.
```
intro:    B P D RL RR
verse:    B P D RL RR
chorus:   B P D RL RR
verse:    B P D RL RR
chorus:   B P D RL RR
bridge:   B P D RL RR
chorus:   B P D RL RR
outro:    B P D RL RR
```
**Touchstones:** AC/DC, Foo Fighters, AAL "Cafo." **Pairs with:** Rock (when the song never lets up), Jazz-funk, Punk.

### 9. Verse breathing *(counter-intuitive — chorus LEANER than verse)*

Verse loads up layers, chorus strips one or two for hook clarity. Works in genres where the chorus lifts via *tightness*, not density.
```
intro:    B P D
verse:    B P D RL RR SP      (loaded)
chorus:   B P D RL RR         (drop SURGE — chorus is tighter)
verse:    B P D RL RR SP
chorus:   B P D RL RR
bridge:   B P D SP
chorus:   B P D RL RR
outro:    B P
```
**Touchstones:** Some Polyphia, certain Plini moments. **Pairs with:** Rock, Jazz-funk.

### 10. Bridge as breakdown *(everything full except bridge minimal)*

Bridge becomes a near-silent moment for maximum chorus impact on return. Often pairs with a `stop_before_next`-style effect (not yet implemented).
```
intro:    B P D
verse:    B P D RL RR
chorus:   B P D RL RR SP
verse:    B P D RL RR
chorus:   B P D RL RR SP
BRIDGE:   B P only            (radical strip)
chorus:   B P D RL RR SP
outro:    B P D
```
**Touchstones:** Many pop-rock songs, some metal breakdowns. **Pairs with:** Rock, Djent.

### 11. Plagal Intro Fanfare *(short dense layered build with NO V chord)*

Verified from APP "Sirius" (2 min instrumental opening Eye in the Sky). A short-form INTRO archetype that establishes mood + key + builds anticipation before segueing to the main track. Key principles:

1. **One chord held for many bars before anything moves.** Sirius holds an A pedal for 14 bars (4 cycles!) before harmonic motion begins.
2. **The motif enters BEFORE the chord changes.** Establish the hook over static tonic; let harmonic motion be the *second* surprise, not the first.
3. **Plagal-only harmony — i-bVI-iv-i, NO V chord.** Sustains anticipation without releasing it. Critical for "intro that segues into the main track."
4. **Same chord loop iterated 5-7+ times** with additive layering — never subtractive within the intro.
5. **Layer entry sequence** (Sirius verified, 7 stages over 38 bars):
   - pad + drone (root pedal)
   - ostinato motif (the hook)
   - first percussion (subtle kick)
   - first chord-change layer (e.g. pad shifts to bVI)
   - orchestral colors (strings + harp glissandi)
   - backbeat (snare + bass)
   - lead (the high note that sells the climax)

```
bars 1-14:   B P            (drone — pedal root + sweep pad only)
bars 7+:     B P C          (motif enters)
bars 11+:    B P C D[kick]  (subtle pulse)
bars 15+:    B P C D RL     (first harmonic motion — bVI arrives)
bars 22+:    B P C D RL SP  (orchestral bloom)
bars 30+:    B P C D RL RR  (full kit + bass)
bars 38+:    B P C D RL RR + lead  (peak — segue to next track)
```

**Touchstones:** APP "Sirius," APP "Voyager," Pink Floyd "Shine On You Crazy Diamond" intro, intro-fanfare instrumental tracks generally. **Pairs with:** Rock, Cinematic-prog, Post-rock. Use for short opener tracks that lead into another track rather than for full standalone songs.

### 12. Modal Shapeshift *(single tonic, different mode per section)*

Verified from APP "Where's the Walrus?" (1985 Stereotomy). The piece never modulates keys — the tonal center stays on A throughout — but it **modulates by MODE**, shifting through Dorian (verse) → Aeolian (bridge) → Phrygian (interlude) → back. SAME TONIC, different scale. The listener perceives modulation without actually leaving the key center.

```
verse:    chords drawn from A Dorian   (uses raised 6 = F# — A-B-C-D-E-F#-G)
bridge:   chords drawn from A Aeolian  (uses natural 6 = F — A-B-C-D-E-F-G)
interlude: chords drawn from A Phrygian (uses b2 = Bb — A-Bb-C-D-E-F-G)
return:   back to A Dorian
```

The trick: keep the A bass pedal (or A-as-tonic) throughout, but let the chords drawn from each mode color the same root differently. Em7 (modal v of A) sounds totally different than E7 (dominant V of A) over an A pedal.

**Use when:** the song needs harmonic variety without committing to a new key. **Touchstones:** APP fusion-rock instrumentals, Miles Davis modal jazz, Snarky Puppy. **Pairs with:** Jazz-funk subschool B (modal jazz), Rock for fusion-rock, Spanish/Phrygian for the interlude moments.

### 13. Parsons Stack *(strictly additive layer build — 8-bar increments)*

Verified from APP "Some Other Time" (1977 I Robot) and similar APP arrangements. The Parsons signature: **every 8 bars a new instrumental color enters, NEVER subtractive until the bridge** (where one or two layers drop out briefly before returning fuller). The arrangement is monotonically additive across the song's first ~80% — the dynamic build IS the song.

```
bars 1-8:   ac.gtr + piano                                  (intro — minimal)
bars 9-16:  + synth strings                                 (theme A instrumental)
bars 17-24: + lead melody (replacing piano)                 (theme A expansion)
bars 25-32: + bass + drums + french horns + trombones       (full band slam)
bars 33-42: (strip back to vocals + minimal — verse)        (one-time strip for vocal entry)
bars 43-48: + choir aahs                                    (chorus 1)
bars 49-58: + distorted electric guitar                     (instrumental break)
bars 59-68: bridge — strip horns out                        (the only subtractive moment)
bars 69-104: full ensemble + new colors                     (rest of song fully maxed)
```

**Touchstones:** Alan Parsons Project (literally), Beatles "A Day in the Life" build, Pink Floyd "Wish You Were Here" arrangement-by-section. **Pairs with:** Rock, sophisticated rock with prog leanings, anything where the arrangement craft is the point.

### How to pick an arrangement archetype

1. **Match to mood:**
   - **Constant energy** → 8 (Hit and run)
   - **Quiet-loud contrast** → 2 (Hit and breathe)
   - **Patient build** → 1 (Slow build), 7 (Hisaishi swell)
   - **Climax late** → 4 (Mogwai inversion)
   - **Single harmonic idea** → 6 (Drone build)
   - **Layers always growing** → 3 (Layer stack)
   - **Counter-intuitive / surprise** → 9 (Verse breathing)
   - **Breakdown drama** → 10 (Bridge as breakdown)
2. **Don't repeat** the same archetype on consecutive songs.
3. **These are starting points** — adapt the per-section role plan. If a verse needs SURGE for an extra second of warmth, add it. The catalog is a vocabulary, not a constraint.
4. **Match to style pack:**
   - Rock → 1, 2, 5, 8, 9
   - Cinematic → 4, 6, 7
   - Spanish/Phrygian → 8, 10 (energetic) or 2 (dramatic contrast)
   - Post-rock → 4, 6
   - Djent → 3, 8, 10
   - Synthwave → 3
   - Jazz-funk → 7 (ballad), 8 (groovier), 9
   - Math rock → 6 (drone), 4 (post-rock inversion)

## Intra-section arrangement variation

The arrangement archetypes above govern *which layers play in which sections*. This catalog governs the next level down: **what changes WITHIN a section** — entry/exit timing, micro-drops, silences, role swaps. This is the texture-evolution side of arrangement; pairs with the Hooktheory 6th axis (Arrangement Pacing) to ensure every 4–8 bars *something* shifts.

**Script limitation:** the composer.py engine writes one MIDI item per role per section — it cannot natively automate mid-section drops, fade-ins, or silences. Document the intra-section move in the section's `move` field. The user applies the actual variation manually in REAPER (mute item slices, automation lanes, FX bypass at the bar boundary). Same documentation pattern as cinematic tempo arcs and prog multi-meter transitions: the SKILL describes the move, the user wires it.

When using a move from this catalog, name it explicitly in the `move` string so the project NOTES carry the cue (e.g. `move: "verse: mid-section drop — kick out for bars 5-8, returns hot on bar 9"`).

### Entry / exit patterns

- **Wedge entry** *(Adler-derived, classical orchestration term)* — over the first 4 bars of a section, instruments enter one per bar, building from bass-up or down from the top. Example: bar 1 bass alone, bar 2 +pad, bar 3 +drums, bar 4 +rhy guitars (full). Use at the top of a new section to make the entry the event rather than presenting full ensemble on beat 1. Document: `move: "wedge entry: bass→pad→drums→rhy-guitars, one bar each"`.
- **Mid-section drop** — full ensemble plays bars 1–4, then ONE instrument (typically kick, bass, or rhy guitars) drops out for bars 5–8, then returns hot on bar 9. The 4-bar absence makes the return land harder than continuous play. Source: EDMprod subtractive arrangement (micro phase). Document: `move: "mid-section drop — kick out for bars 5-8, returns hot bar 9"`.
- **Delayed lead entry** — section begins as a chord bed only, melody/lead enters at the midpoint (bar 5 of an 8-bar section, or bar 9 of a 16-bar section). Builds anticipation; common in Andy Timmons's writing and modern cinematic. Document: `move: "instrumental bed bars 1-4; lead enters bar 5 carrying the section's melodic hook"`.
- **Crossfade exit** — instrument fades over 2–4 bars rather than cutting hard, so the next entering instrument has space to claim its register. Manual REAPER move: track envelope on the outgoing item. Document: `move: "synth-pad crossfades out over bars 13-16 as the lead enters"`.

### Negative space patterns

- **Single-bar silence reset** *(verified pop-production move)* — the full ensemble stops for exactly 1 bar before a new section (typically the bar before chorus 2 or before the final chorus). The silence IS the transition — replaces FX sweep, snare roll, etc. Source: Sample Focus, Sound on Sound. Document: `move: "single-bar silence before final chorus — everyone out for bar 16, chorus re-enters bar 17"`.
- **Stop time** *(classic R&B / gospel / hip-hop)* — the band stops for 2 beats while one instrument plays a fill or a vocal phrase, then resumes. Inside a bar, not at the bar boundary. Document: `move: "stop time: ensemble out beats 1-2 of bar 8 while lead plays pickup, full band returns beat 3"`.
- **Drop-into-silence** *(EDM "drop" mechanic, generalized)* — the entire ensemble cuts on beat 1 of the LAST bar before a return. One bar of pure silence (or just reverb decay), then the new section slams in. Different from "single-bar silence reset" in that the silence is exactly 1 bar AT THE BOUNDARY between sections. Document: `move: "drop-into-silence: ensemble cuts beat 1 bar 8 of bridge, chorus 3 enters bar 9 with full impact"`.
- **Held tail decay** — instead of cutting an instrument on a hard barline, let its reverb/delay tail decay across 1–2 bars into the new section. Manual REAPER move: automate reverb send to taper, or print the wet tail as a separate item that continues past the cut. Document: `move: "synth-pad cuts on bar 16 but reverb tail bleeds into bars 17-18 of next section"`.
- **Frequency-space drop** *(perceptual silence — sonic illusion)* — instead of dropping volume, remove the competing mid-range instruments so the bass dominates and the section FEELS empty even though notes are still playing. Common in dubstep, modern hip-hop. Document: `move: "frequency-space drop: cut rhy guitars + pad mids for bars 5-8, leaving sub-bass + kick + clean arp — feels empty without being silent"`.

### Density curve archetypes *(extending the existing 13 Arrangement archetypes)*

- **Plateau-burst** *(verified — modern pop trend)* — hold at low/medium density for 12–16 bars (longer than expected), then sudden full-density explosion. The unusual *length* of the plateau is what makes the burst land. Different from the Slow Build archetype (which is linear-additive across the song). Document: `move: "plateau-burst: bars 1-16 stay at bass+pad+clean texture, full band slams in bar 17 — the plateau LENGTH is the device"`.
- **Linear subtractive** — start full, remove one layer every 4–8 bars across the song, ending at minimal. The reverse of Slow Build. Suits introspective endings, post-rock "un-builds," cinematic codas. Document: `move: "linear subtractive coda: chorus full band → bar 8 drop synth_pad → bar 16 drop rhy guitars → bar 24 only bass+pad remain"`.

### Texture interaction patterns

- **Call and response** *(antiphony, verified across genres)* — two instruments trade 2-bar (or 4-bar) phrases instead of playing simultaneously. While one plays its phrase, the other rests. Most natural between bass + lead, or between pad + clean arp. Document: `move: "call-and-response: lead plays bars 1-2, bass answers bars 3-4 (lead silent); alternate through the section"`.
- **Re-orchestration loop** *(verified — EDMprod "same idea different instruments")* — same chord progression and section length, but each 8-bar iteration redistributes which instrument carries chords vs. melody vs. rhythm. Iteration 1: pad chords + clean arp + bass roots. Iteration 2: clean chords + lead melody + bass walks. Iteration 3: synth_pad chords + rhy-guitar stabs + lead trills. The harmony stays IDENTICAL; the instrumentation rotates. Document: `move: "re-orchestration loop: same 4-chord progression, iteration 2 swaps pad↔clean roles, iteration 3 promotes lead to chord-tone melodic role"`.
- **Beat switch** *(hip-hop / modern R&B)* — mid-section radical change in groove or feel while chords stay the same. E.g. verse halfway through flips from `feel: driving` to `feel: halftime` for a 4-bar breath, then back. Different from a true section change because the chords and the listener's "section position" stay constant. Document: `move: "beat switch at bar 9: feel flips halftime for 4 bars then back to driving bar 13"`.
- **Stratification** *(orchestration term, Adler / Klangfarbenmelodie)* — instruments occupy distinct register bands with no overlap, so each is individually trackable. Bass below E2, pad in E2–G3, clean in G3–C5, lead above C5. Use when the harmony is dense (m9/13 voicings) but you want CLARITY. Document: `move: "stratification: bass < E2, pad E2-G3, clean G3-C5, lead > C5 — each instrument owns its band"`.

### How to apply this catalog

1. **For every section longer than 8 bars**, pick at least one move from this catalog and name it in the `move` string. Sections of 4–8 bars can be uniform (no intra-section variation needed); longer sections need at least one mid-section event.
2. **Don't stack more than 2 moves per section** — wedge entry + mid-section drop in one verse is overload. Layer moves *across* sections, not within.
3. **Pair the move with the arrangement archetype**: Slow Build pairs well with delayed lead entry and wedge entry (additive vocabulary). Mogwai inversion pairs with drop-into-silence and held tail decay (climax-late vocabulary). Drone build pairs with stratification and re-orchestration loop (single-loop iterated build needs texture variety to stay interesting).
4. **Negative-space moves are most effective at section boundaries** — `single-bar silence reset` and `drop-into-silence` are TRANSITION devices, not intra-section devices. Place them as the LAST event of the outgoing section.
5. **`Beat switch` and `re-orchestration loop` are pure intra-section** — they work best in long sections (16+ bars) where the listener would otherwise tune out the repetition.

### What to AVOID

- Don't add intra-section moves to a section shorter than 8 bars — they'll feel cramped rather than dynamic.
- Don't combine `single-bar silence reset` with `drop-into-silence` adjacent to each other — two consecutive silences read as a mistake, not an arrangement choice.
- Don't use `wedge entry` more than once per song; it's a special opening device, not a general entry pattern.
- Don't apply `stratification` to genre packs where layering is the point (Layer Stack archetype, Synthwave). It's a clarity move for dense-harmony contexts.

## Drum fills — automatic at section transitions

The skill's built-in drum patterns (`basic-rock`, `halftime`, `four-on-floor`, `one-drop`, `latin-fusion`, `j-fusion-kit`, `none`) are programmatic and uniform — perfect for *sustained grooves*. Where they fell short: **fills at section transitions**. A real drummer plays a transition; programmatic patterns just stop and restart.

**Solution (since 2026-05-22)**: the script now **auto-splices a programmatic fill into the last 2 beats of every section that transitions to a different section in `form`**. No spec changes needed — works by default for any song with drums.

### How it works

The compose pipeline computes which form positions need a trailing fill (boundary where `form[i] != form[i+1]`, section has drums, section is long enough to afford the 2-beat splice). For each, it picks a fill from `FILL_ROTATION` (rotating through 7 named patterns for variety) and splices the fill notes into the section's drum track, replacing the programmatic kick/snare in the last 2 beats. The crash on the next section's downbeat resolves the transition.

The fills appear in both `full.mid` and the `.RPP` drum track. Per-section `.mid` files stay programmatic-only (no fills) since they have no form context — a section file is "this section in isolation."

### The fill catalog *(FILL_PATTERNS in composer.py)*

Seven programmatic fills, encoded as `(offset_in_2-beat-window, drum_name, velocity)` tuples — same shape as the existing `DRUM_BAR_PATTERNS`. Cycled in `FILL_ROTATION` order across a song's transitions:

| Fill name | Character | Best for |
|---|---|---|
| `tom-roll-8ths` | 4 eighth notes: snare → snare → high tom → mid tom | Classic rock transitions, melodic-rock |
| `snare-rush` | 8 sixteenths on snare, crescendo (76 → 100 velocity) | Building intensity into a chorus arrival |
| `tom-roll-16ths` | 8 sixteenths descending snare → toms (high/mid/low) | Bigger arrivals — bridge → final chorus |
| `bonham-triplets` | 12 triplets across snare + kick + toms — Bonham idiom | Heavier rock, prog, when triplet feel fits |
| `kick-snare-8ths` | Minimal 4-hit alternation, low intensity | Ballads, cinematic-rock, sparse contexts |
| `kick-storm` | Kick on every 16th + snare upbeats — dense kick build | Modern rock, post-hardcore, djent |
| `ohat-snare-alt` | Open-hat + snare alternating sixteenths | Funky transitions, jazz-funk, fusion |

Patterns informed by standard rock-fill pedagogy (Bonham triplets, eighth-note tom rolls, snare crescendos — see [drum-patterns.com](https://drum-patterns.com/style/rock/), Drumeo's "Common Rock Drum Fills for Beginners", and traditional rudiments).

### Opt-out and customization

- **Disable for a song**: set `auto_fills: false` at spec top level. The drum track stays pure programmatic.
- **Section with `drums: "none"`**: never gets a trailing fill (no drums to fill from).
- **Literal section repeats** (`form: ["verse", "verse"]`): no fill between identical adjacent sections — the form has no transition to mark.
- **Sections shorter than 4 beats**: skipped — too short to afford a 2-beat fill.

The fill is **deterministic from the spec** — re-running the same spec produces the same fills in the same positions. The rotation through `FILL_ROTATION` is index-based, not random.

### When the auto-fill is wrong

If a particular section transition deserves a *specific named fill* (e.g., the song needs a big tom roll specifically at the bridge → final-chorus arrival), the current implementation rotates through the catalog without per-section override. To customize a single transition, the path forward is one of: (a) re-order `FILL_ROTATION` for the song, (b) extend the spec with `sections[].trailing_fill: "<pattern_name>"` override (not yet implemented — add when a real song needs it), or (c) post-edit the drum item in REAPER after generation.

### Why programmatic over external MIDI libraries

The auto-splice approach was chosen over referencing external drum MIDI libraries because programmatic fills:
- Have **no genre lock** — we control the content; fits any pack
- Are **deterministic from the spec** — reproducible without external dependencies
- Need **no file paths, no MidiDB containers, no manual drag** — the script does the work
- Scale with the skill — adding a new pattern is one entry in `FILL_PATTERNS`

If a song needs a fill character not covered by the 7 programmatic patterns, extend `FILL_PATTERNS` rather than reaching for an external library.

## What the script writes to the template

It copies the Reaper template specified by `template_path` in `config.json` (see the project README), overrides the tempo, adds region markers, and inserts MIDI items on these tracks:

| Role         | Track in template      | What's written                                |
|--------------|------------------------|-----------------------------------------------|
| Bass         | `BASS`                 | Root-note bassline, splits long chords in two |
| Drums        | `DRUMS`                | GM kit (kick/snare/hat), crash at section start |
| Chord pad    | `PIANO`                | Open voicings, sustained for full chord duration |
| Rhythm chord | `MIDI-RHY-GTR-L`       | Root+fifth power chords; rhythm pattern from `feel` |
| Rhythm chord | `MIDI-RHY-GTR-R`       | Same as L, offset 1/8 beat for stereo width   |
| Clean guitar (picked) | `MIDI-CLEAN`   | Fingerpicked 8th-note arpeggio cycling through chord tones. For ballads, cinematic, math rock — replaces rhythm guitars. |
| Strum guitar | `MIDI-STRUM`            | Staggered chord strum — each chord tone offset ~40ms (pick rake low-to-high), velocity tapers (72→70→68→66). Patch is voiced for strumming (warmer than the picked clean), so use this rather than `clean` when you want strummed accompaniment. |
| Lead guitar  | `MIDI-LEAD`             | Composed melodic line per section (`melody` field). Plays once across the section by default; loops every N beats if `melody_loop_beats` is set (riff mode). Use to give a section its melodic identity / hook line — the user uses it as a starting point for their own lead playing. |
| Chugg guitar | `MIDI-CHUGG`            | Palm-muted low-octave rhythm on the chord root (`chugg` field picks a pattern). Track has ReaPitch loaded so the user can drop-tune to taste. Patterns: `straight-16ths`, `gallop`, `polyrhythm-3`, `syncopated`, `halftime`, `single-hit`, `open-8ths`. |
| Synth pad bed | `SURGE XT`            | Soft sustained chord-tone bed in mid-range (octave 3, vel 60). Long sustain (chord_beats + 1.5–2.5 of overhang) so the synth's release tail blurs into the next chord. **Opt-in only** — use under arpeggios when the song needs harmonic glue. |

**Regions:** one per form entry, named `<section>-<n>` (e.g. `verse-1`, `chorus-2`). Use for looping, region-render, or the region matrix.

## Fill mode

Composer can also drop a section INTO an existing Reaper project. The user marks N bars of silence with a region literally named `COMPOSER`, closes Reaper, and asks Claude to fill it. Claude analyzes what's around the gap, composes a fitting section, and the script writes MIDI items into the .RPP in place.

### When to use

Trigger phrases — recognize any of these as fill-mode requests:

- "fill the COMPOSER region in `<path>`"
- "fill the gap in this song"
- "compose for the COMPOSER region with `<brief>`"
- "do a key mod in the empty section"
- "give me a bridge / breakdown / transition for this song"

How it differs from `compose`: no `<output_dir>`, no new files in `~/Documents/MIDI-SONGS/...`. The fill operation edits the .RPP in place. The user must close Reaper before invoking (the script rewrites the file).

### Workflow

```bash
# 1. Analyze surrounding context.
python3 ~/.claude/skills/composer/composer.py analyze <project.RPP>
# → emits a JSON dump to stdout: tempo, time_sig, region length in bars,
#   prev_context sections (chord progressions, feel, scales, move),
#   post_context sections, last_chord_before_region, first_chord_after_region,
#   neighborhood_tracks (which tracks are active in surrounding bars).

# 2. Read the JSON. Decide fill content (see "Brief interpretation" below).

# 3. Write a fill spec.
# Spec shape = one section + roles. NO tempo (project tempo is used).
# Total beats MUST equal the region length.

# 4. Run fill.
python3 ~/.claude/skills/composer/composer.py fill /tmp/composer_fill_spec.json <project.RPP>
# → writes MIDI items into matching tracks at the COMPOSER region's time range,
#   updates the project's NOTES block with a COMPOSER-FILL section entry,
#   refreshes the EXTSTATE breadcrumb so the next analyze sees the new section.

# 5. Tell the user to reopen the .RPP in Reaper.
```

### Fill spec format

```json
{
  "roles": ["bass", "pad", "clean", "drums"],
  "feel": "halftime",
  "drums": "halftime",
  "voicing": "power",
  "skip_roles": [],
  "melody": [[0.0, "E4", 4.0]],
  "melody_loop_beats": null,
  "chugg": null,
  "scales": "E Aeolian (E-F#-G-A-B-C-D)",
  "move": "halftime breakdown — Em pedal with sus voicings",
  "chords": [
    {"name": "Em9",  "beats": 8},
    {"name": "Cmaj7","beats": 8},
    {"name": "Am7",  "beats": 8},
    {"name": "B7",   "beats": 8}
  ]
}
```

Validation: `sum(c.beats for c in chords) == region_length_sec * tempo / 60`. The script errors out if these don't match — fix the chord progression to align with the region's beat count.

### Brief interpretation — three flavors

The user's request will land in one of three buckets. Recognize which and act accordingly.

**A. No brief / "fill the gap"** — Mode A. Default to a transition that fits the surrounding context:

- If prev is verse + post is chorus → write a pre-chorus build / lift.
- If prev is chorus + post is chorus → write a bridge (parallel-minor, IV-as-tonic, or modal-mixture move).
- If prev is chorus + post is verse → write a breather (halftime breakdown, drop to bass+pad).
- If prev is intro + post is verse → write a second intro variation (add a layer or two).

If genuinely ambiguous between two strong options, ask ONE question: *"Should this fill stay in `<current_key>` or modulate? And should it be a build or a breather?"*

**B. Vibe-textural brief** — "65bpm arpeggiated guitars," "atmospheric," "sparser," "moody."

Keep the harmonic anchors (`last_chord_before_region` + `first_chord_after_region` as bookends), but pick `feel` + `roles` to match the texture words:

- "arpeggiated guitars" → `roles: [clean]` (optionally `+ synth_pad` for harmonic glue).
- "65bpm-feel" in a 135-BPM project → `feel: "halftime"` + chord durations doubled (8 beats per chord instead of 4).
- "atmospheric" → drop drums + rhy guitars → `roles: [bass, pad, synth_pad]`.
- "drop to silence" → `roles: [pad]` only, sparse feel.

The harmonic content can stay diatonic (you're decorating the texture, not the chords).

**C. Harmonic brief** — "Andalusian cadence," "key mod to F#m," "ii-V-I in C," "bVI-bVII-i lift," "do a key mod here," "borrow chords from parallel minor."

The chord progression is dictated. Pick the feel from surrounding context. Critical: if the brief specifies a key change, **end the fill with a pivot or leading-tone chord that lands smoothly on `first_chord_after_region`** — otherwise the modulation lands awkwardly when the song re-enters the next section.

Examples:
- "key mod to F#m" with `first_chord_after = Em9` → the fill should NOT just end in F#m; it should end on something that resolves into Em9 (e.g. a B7 leading-tone), so the song "returns home" cleanly.
- "Andalusian cadence" → `i — bVII — bVI — V7` in the appropriate key (`Em — D — C — B7` in E, transpose to context key).

### Ambiguous brief

If the brief is short ("make it interesting," "do something cool here") and you cannot reasonably pick between options, ask ONE question: "modulate or stay in `<current_key>`? Build or breather?"

### Transition idioms catalog

Pick one when composing the fill. Each line: name — when to use — example in Em (transpose to context key).

**Modulations** (for harmonic briefs that request a key change):
- **Pivot chord** — find a chord shared between source and target keys; use it as the pivot. *Em → G major: pivot through G (vi in Em, I in G).*
- **Direct / abrupt** — no preparation, just land in the new key on bar 1 of the post section. *Best for surprise drops.*
- **Common-chord (modal pivot)** — borrow a chord that exists in both keys' modes. *Em → Am: pivot through Am (iv in Em, i in Am).*
- **Chromatic mediant** — modulate by a third (major third up = up a flat, minor third up = up a sharp). *Em → Gm or Em → Cm.*
- **Phrygian-dom V from new key** — set up the new key with its V7 dominant. *Em → Am: end fill with E7 (Phrygian-dom V of Am).*
- **Sequential cuts** (Dream Theater) — repeat the same melodic figure transposed up/down each bar.

**Bridges** (for fills between two choruses or between verse and chorus when contrast is wanted):
- **Parallel-minor pull** — Em song → E major bridge, or A major song → A minor bridge. Same root, swap mode.
- **Parallel-major lift** — Bm song → B major bridge. The 6 chord (originally minor) becomes major, lifts the whole section.
- **IV-as-tonic Lydian** — in Em, treat A as the new tonic for the bridge with Amaj7-B/A-G#m-Amaj7. Briefly explores Lydian.
- **bVI surprise** — drop a Cmaj7 (bVI in Em) for the whole bridge, hover on it. Em → Cmaj7 vamp.
- **Halftime-same-chords bridge** — reuse the chorus chord progression but at halftime feel. The dynamic shift IS the bridge.

**Pre-chorus lifts** (for fills between verse and chorus when build is wanted):
- **IV-V-IV-V** — simplest functional buildup. In Em: Am-B7-Am-B7.
- **IV-V-vi-V** — Paramore lift. In Em: Am-B7-Cmaj7-B7.
- **Chromatic walk-up to new key** — bass walks up by half-steps, lands on first_chord_after.
- **bVII-IV-V launch** — in Em: D-Am-B7. Bright, anthemic.

**Breakdowns** (for fills where the song needs to breathe before returning):
- **Strip to bass+pad** — `roles: [bass, pad]` only. Same chords, half the layers.
- **Drone on tonic with halftime drums** — sit on Em9 for 8 bars, halftime feel.
- **Sus-hang into next section** — end the fill on Esus2 or Esus4 (unresolved), let the post section's first chord resolve.

**Ramps / escalations** (for fills that explicitly need to climb):
- **Chromatic walk-up** — `i → bii° → ii° → biii° → iii` style escalation.
- **Ascending bass line** — bass walks up a scale toward `first_chord_after_region`'s root.
- **Accelerating chord rhythm** — chord every 8 beats → 4 → 2 → 1, terminating on first_chord_after.

### Track-selection rules

- **Mode A (no brief)** → mirror `neighborhood_tracks` from analyze output. Continuity is the value.
- **Mode B textural** → override deliberately to match the texture words. "Arpeggiated guitars" = `[clean]`, optionally + `synth_pad`. "Drop to bass and pad" = `[bass, pad]`.
- **Mode B harmonic** → use the same role set as surrounding sections so the new harmony feels integrated. The key mod IS the surprise; don't compound it with a texture surprise unless asked.

### Re-running fill (variations)

If the user doesn't like the result and wants to try again:

1. Tell the user to manually delete the inserted items in Reaper (search for items named `composer-fill-*` and delete).
2. Re-invoke fill with a new spec. The script overwrites the COMPOSER-FILL entry in NOTES and the `composer-fill` section in EXTSTATE — no accumulation of dead variations. (MIDI items would accumulate without manual delete, so be sure step 1 happened.)

## Style notes

- **Bassline-first thinking.** Sketch the bass shape (stepwise descent? pedal?) before picking chords.
- **Inversions are your friend.** `G/B`, `C/E`, `Em/G` make the bass move smoothly.
- **Color tones over plain triads.** Default to `Em9`, `Cmaj7`, `Am7`. Plain triads land best at resolution moments.
- **The chorus is the destination.** Brighter, simpler, less tension.
- **Dynamics via `feel` and density.** A sparse intro and halftime verse make the driving chorus hit harder. Lean on `feel` for dynamics, not chord changes.

## Limitations

- No tempo or time-signature changes mid-song.
- Drum patterns are fixed bar-level — no fills, breakdowns, or builds.
- Chord parsing is strict — `C9sus4`, `Cmaj7#11`, and similar will error.
- No automation, no per-note velocity shaping beyond pattern defaults.
