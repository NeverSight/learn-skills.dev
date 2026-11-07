---
name: animation-studio
description: This skill should be used when the user asks to "make an animated video about X with music", "make a cartoon / animated short", "animate this story", "make a video like the Opus animations", "make an explainer animation (with a voiceover)", "make a promo video for my app / brand / website", "make an animated Reel / TikTok / Short", "make a lyric video / animate to my song", "make an animated map or infographic", or "make a jingle / birthday video" — a new hand-drawn 2D film where every frame is drawn in code and the soundtrack is synthesized in code (or is the user's own song, beat-analysed), synced from one score, delivered as a 1080p MP4 in 16:9, 9:16, 1:1 or 4:5. Not for CSS/web/UI animation, Lottie/SVG/GIF assets, editing existing video footage, or Remotion/Manim projects.
version: 1.0.1
---

# Animation Studio

Make short films (typically 15–60s at 30fps, in 16:9, 9:16, 1:1 or 4:5) where **every frame is drawn on a canvas and every sound is synthesized in JavaScript**. There are no samples, no stock footage and no npm dependencies. The signature trick is one `score.js` timeline that both the music and the animation read, so they cannot drift apart. Each ball touch plays a note, each letter stamps on an 8th note, and each firework bursts on the clap.

Requirements: Node 22+ (built-in WebSocket), ffmpeg, and Google Chrome/Chromium (headless). No `npm install`. Supported on macOS and Linux. Voiceovers use the computer's own text-to-speech (macOS `say`, piper, kokoro or espeak-ng); without one they are silent placeholders.

## How a film is built

```
my-film/
├── score.js    the timeline: tempo, chords, melody, voice lines and EVERY event (single source of truth)
├── song.js     synthesizes the soundtrack from score.js    -> out/music.wav (+ out/voice.json)
├── film.js     draws frame t from score.js                  (pure function of t)
├── index.html  loads engine + score + film in headless Chrome
└── engine/     vendored toolkit (synth, voice, drawing, renderer): copied in, never edited per film
```

The renderer serves the project on an OS-assigned port and drives parallel headless Chrome workers over the DevTools protocol. It calls `window.renderAt(t)` for every frame and pipes the PNGs to ffmpeg.

## Workflow

### 0. Pin down the brief
From the request, or with at most one round of questions, settle:
- the subject and the emotional arc,
- the length (default 20–40s),
- who appears, including exact name spellings,
- whether the Claude mascot belongs (yes for Opus-style or Claude films),
- the language(s) of the words,
- whether there is a voice (a voiceover, singing, or the user's own song),
- where it will be posted: 16:9 for YouTube/X, **9:16 for Reels, TikTok and Shorts**, 1:1 or 4:5 for feeds. Ask if a brand or social brief doesn't say.

Characters are never fixed. Use a preset (`Ch.STYLES.afaq`), customize `Ch.person` (hair, beard, glasses, outfits from jersey to sari, thobe, suit, sherwani or lehenga, headwear, build, colours), add `Ch.dog` / `Ch.cat` / `Ch.bird`, or build new characters from `G.*` primitives. When the user shares a photo of someone, translate it into `style` options and never store the photo. Their own images can appear as taped prints (`G.photo`) or a Ken Burns pan (`G.kenBurns`). See `references/custom-characters.md`.

### 1. Choose a story shape, then storyboard it as music

| shape | fits | pacing and music |
|---|---|---|
| **Big payoff** | sports, surprises, launches: any real "will it happen?" | quiet intro → tension → build → a beat of silence → loud drop → soft outro |
| **Comic escalation** | birthdays, pets, mishaps | the same gag three times, each bigger; bouncy 130–150 BPM, staccato plucks, cartoon SFX; a record-scratch stop before the punchline |
| **Tender memory** | anniversaries, thank-yous, farewells | 70–90 BPM, music box, pads, soft keys, no drums; no drop; slow push-ins, warm light; ends on a held chord |
| **Montage** | trips, a year in review, celebrations | a steady groove, one shot per bar, energy rising every 4 bars; no silence |
| **Musical explainer** | products, ideas, how-tos | 100–110 BPM, one idea per bar, each with its own sound (or a voiceover with the music ducked under it) |
| **Performance** | a band, a qawwali, a dance | the music leads: call and response, a tempo that speeds up, the players' hands on the notes |

The silence-and-drop is a tool, not a signature: use it only when the story has a real moment of suspense. Think in bars, not seconds (at 120 BPM, 1 beat = 0.5s and 1 bar = 2s), and put cuts on bar lines. Pick 3–5 **sync gimmicks** where the picture visibly makes the music, such as a ball that plays the melody, stars that are notes, or claps the chorus makes. See `references/storytelling.md`.

Keep facts honest. If real events are involved and their details are unknown (a result, a date), keep them fictional or generic. For a brand, run `node engine/render.js brand-from https://their-site` after scaffolding. It writes `brand.json` (colours, fonts, logo, CTA), which every film picks up. Add the claims it must never make.

### 2. Scaffold the project

```bash
node <skill-dir>/scripts/new-project.js <target-dir> [--from <starter>] [--format 9:16]
```

`<skill-dir>` is the "Base directory for this skill" shown when this skill loaded. Create `<target-dir>` as a new, descriptive kebab-case folder in the user's current working directory unless they name a location; the folder name becomes the output name (`out/<folder-name>.mp4`). Never scaffold inside `<skill-dir>`. **Run every later command from inside `<target-dir>`**, prefixing each with `cd <target-dir> &&`. If a preflight line shows ✗, stop, tell the user what is missing and how to get it, and ask before installing anything.

Pick the starter that fits (details in `references/starters.md`):
- **template**, the default: any format.
- **app-promo**, 9:16: an app with phone screens.
- **product-launch**, 16:9: a voiceover, captions, counters, and style and genre montages.
- **qawwali-night**, 16:9: a performance, with singing and a tempo that speeds up.
- **gully-cricket**, 9:16: a comic escalation with dialogue.
- **birthday-card**, 1:1: a sung name.
- **wedding-invite**, 9:16 (lays itself out for every format): a shaadi card with a shehnai, the dhol, a baraat on a horse, and the Mehndi, Baraat and Walima details.
- **lyric-video**, 9:16: the user's own song.

Keep the starter's structure and replace the story. `world-cup-2026` uses an older API: read it for staging patterns only.

### 3. Write `score.js`
- Use `MUSIC.makeClock({ bpm, offset })` for `T(bar, beat)`. Add `tempo: [[bar, bpm], …]` for accelerando, `beatsPerBar: 3` for waltz time, and `beats` from `analyze` for a real song.
- Use `placeBar` for 8th-note melody bars and `makeChords` for harmony.
- Export `FPS`, `FORMAT`, `DURATION`, `S` (named sections), every event list, the voice lines (`vo`) and the `subtitles`. Add `STYLE` too if it isn't paper.
- Generate any randomness here with a seeded `U.mulberry32`, so the audio and the video see identical events.
- Keep the UMD wrapper and its last line: `song.js` and `render.js` `require()` score.js, while `index.html` loads it as a script.

Name the key moments in `markers` (`drop: { t: ev.drop, sync: 'av' }`). Every command then accepts `@drop`, `@drop-2` or `8:2` instead of seconds. Give `sync: 'av'` to the hits (landings, cuts, stamps, drops, flashes) so `verify` measures them; `'a'` is sound only, `'v'` picture only.

### 4. Write `song.js` and measure it
Render parts into buses, add reverb or delay sends, and sidechain the pads and bass to the kick in energetic sections. Then run `MIX.mixdown → highpass → gate (a silence, after the reverbs) → fadeOut → master → writeWav`. What the engine offers (recipes in `references/music-cookbook.md`):
- **Instruments:** kit, bass, pads, brass, music box, marimba, guitar, e-piano, strings, pizzicato, timpani, 808, supersaw, chip waves, dholak, tabla, harmonium, shehnai, dhol, ghungroo, and SFX (glass, scratch, whoosh, pop…).
- **Genre packs:** `Genre.play('lofi'|'chiptune'|'orchestral'|'edm'|'afrobeats'|'qawwali'|'desi'|'boombap', …)`, a full backing in one call. You write the hook.
- **Voiceover:** `Voice.speak([{ at, text, voice, who, display, alt }])` does offline TTS with estimated word times and a mouth track (`out/voice.json`). Duck the music under it with `MIX.duck`.
- **Singing:** `Sing.line('si-tey dot pee-kay', notes)` or `Sing.phrase(notes)`, and `Sing.happyBirthday(name)`, from a formant singer. It is best on short hooks, doubled by an instrument, with the words on screen.
- **The user's song:** run `node engine/render.js analyze song.mp3 [--lrc lyrics.lrc]` to get `beats.js`, then `MIX.loadAudio` for the soundtrack. Only use music the user has the rights to.

**The model cannot hear the result, so measure it.**
- `STEMS=1 node song.js && node engine/tools/levels.js out/music.wav out/stem-*.wav` gives the RMS and peak per stem per section. Fix balance with the `GAIN` table: voices on top, the hits clear, silences truly `-inf`.
- `LUFS=-14 node song.js` sets the loudness: -14 for YouTube and Spotify-normalised platforms, -12 to -11 for X and feeds. The master limits the true peak to -1.5 dBTP.
- Read spectrograms (`showspectrumpic`) to confirm the structure.

### 5. Write `film.js`
Call `Studio.film({ draw(ctx, t) {...}, post, init })`. Every visual is a **pure function of t**. Other rules:
- **Layout:** lay out from `G.W` / `G.H` and keep text, faces and logos inside `G.SAFE`. On 9:16, the platforms cover the top ~11%, the bottom ~22% and the right edge.
- **Drawing:** draw with `G.*`, so lines boil and fills get hatching.
- **Motion:** drive it from the clock: hops on beats, cuts on bar lines. For many shots, use `Shots.film([...])` with transitions and camera moves.
- **More files:** add each extra film file as a `<script>` after `engine/video/boot.js`.

The toolbox (every call is in `references/engine-api.md`):
- **Looks:** `STYLE` `'paper'|'flat'|'pixel'|'chalk'|'neon'|'watercolor'` (or `--style` on any command), with `G.bg` for the background (visual-style.md).
- **Acting:** poses `stand`, `sit`, `floor` (cross-legged) and `walk` (`Ch.walk`), 18 `gesture`s (wave, point, phone, cheer, clap, dua, mic, bat, bhangra, dhol…), IK hand targets, and lip-sync with `mouth: Subs.mouth(VO, t, who)`.
- **Words:** `Subs.draw` captions (`pop`, `karaoke`, `box`, `clean`) from `Subs.fromVoice(VO)` or `SCORE.subtitles`. Urdu, Arabic and Hindi come out right in every text call.
- **Products:** the UI kit (`UI.phone`, cards, chat, stats…) after `UI.setTheme`. `render.js snap https://site --full` + `UI.imageScreen` shows a real site scrolling in the phone. Use only facts the client confirms.
- **Data:** `Data.counter` (`lakh: true` for Rs amounts), `Data.bars` / `line` / `donut`, and maps (`Data.map`, `drawMap`, `pin`, `route`) with Pakistan in detail.

### 6. Review like a director (loop until it's good)

```bash
cd <target-dir> && node engine/render.js stills @drop 8:2 12.5    # key moments -> out/stills/
cd <target-dir> && node engine/render.js sheet 0 <DURATION> 30 6  # 30 frames across the film -> out/sheet.png
cd <target-dir> && node engine/render.js clip @drop-2 @drop+3     # that section WITH sound
```

Read the PNGs and critique every shot:
- legibility and overlapping text,
- faces hidden by props,
- muddy colours,
- poses that read wrong, and seated people who should sit on the floor,
- elbows bending inward,
- clutter,
- the frames just before and after each cut.

Fix, then re-render the same times. Useful checks:
- `cast` shows every character in `globalThis.CAST` in 6 expressions.
- `plan` writes a one-page treatment and a claims checklist.
- `qa` checks the text drawn in sampled frames (one per second, plus each marker; add times to check more) for the safe area, size, overlap and contrast.
- `pacing` checks the first-3-seconds hook and the cuts.
- Add `--draft` to renders for half-resolution speed. Render commands warn about `Math.random`/`Date.now` in film files.

**Let the user watch and listen before the full render.**
1. Run `node engine/render.js preview` with `run_in_background: true` and give the user the printed link (the port is OS-assigned, never a fixed one like 3000). It plays the music with a live timeline and reloads when files change. You can't watch it yourself.
2. Show them `render.js board` (every marker as one storyboard) and the music measurements, and let them approve or redirect.
3. When they're done, stop that preview task, and only that one.

### 7. Render, mux, verify

```bash
cd <target-dir> && node song.js
cd <target-dir> && node engine/render.js video      # parallel workers -> out/video.mp4 (minutes: run_in_background)
cd <target-dir> && node engine/render.js mux        # -> out/<folder-name>.mp4 (H.264 + AAC)
cd <target-dir> && node engine/render.js check      # contact sheet + loudness
cd <target-dir> && node engine/render.js verify     # sound ±20 ms and picture ±1 frame at every sync marker
```

`video` takes longer than the Bash tool's 2-minute timeout: launch it with `run_in_background: true` and wait for `out/video.mp4 done`.
- A ✗ from `verify` means one side is late: fix it in `score.js`, never by nudging one side by hand.
- A `?` (unclear) also fails. Either nothing distinct happens there, or two onsets are almost equally steep and far apart, like a sung pickup just before a sung downbeat, or a drum roll into the hit. Fix it with a real transient in the sound, a flash or cut in the picture, or an 8th of held breath before it; otherwise drop its `sync`. `--allow-unclear` turns these into warnings. Verify the files you actually publish: a re-encode can tip a near-tie.

For publishing, use:
- `srt` for subtitle files,
- `poster` for three thumbnails and a vertical cover,
- `formats 16:9,9:16` for every format from one score (add `--res 2160` for a 4K master or `--res 1440` for 2K),
- `mux --subs` for a soft subtitle track,
- `clip … --gif` for a shareable GIF.

See `references/reach-and-workflow.md`.

### 8. Deliver
Report the output path, duration, resolution and size. Explain the sync gimmicks in a sentence or two. State plainly that the audio was verified by measurement rather than listening, and invite feedback on the sound. Offer variations: names, colours, a different length or tempo, another look (`--style`), or another format (a 9:16 cut means re-staging the shots, not cropping).

## Rules that prevent the usual failures
- **Single source of truth.** Never time a sound or an animation by hand in two places. Put the event in `score.js` and read it from both sides.
- **Determinism.** Use `U.hash(...)` or a seeded `mulberry32`, never `Math.random()`. Parallel workers must draw identical frames.
- **Hits are hits.** A sync moment needs a sharp change on both sides, like a transient and a cut or flash. Pickups, rolls and swells *into* a moment blur it, so end them a beat early or leave an 8th of silence.
- **Words on screen.** Keep captions inside `G.SAFE` and at least ~16 px on a 1080 frame. Give a voiceover about 2.5 words a second, and never put a big hit on top of a spoken word.
- **Impact frames and draw order.** Draw sunbursts *behind* characters, and draw captions before full-screen wipes.
- **Culture with care.** Dress and stage people as the audience would expect (a qawwali seated on the floor, a bride in a red sari). Write lyrics and dialogue in the user's language with its script, and avoid caricature.
- **Safety on the user's machine.** Ports are OS-assigned, and the renderer only serves the project folder. It only kills the Chrome processes it launched itself, so never kill anything else: other Claude sessions may be rendering. Never touch the user's dev servers or ports, and ask before git commits, pushes, publishing or installing anything.

## Additional Resources

### Reference files
- **`references/starters.md`**: every starter in detail and which one fits which brief
- **`references/storytelling.md`**: story arcs mapped to bars, the sync-gimmick catalogue, caption voice, endings
- **`references/music-cookbook.md`**: instruments, genre packs, singing, voiceover, cutting to a song, tempo maps, arrangement, mix and loudness targets
- **`references/visual-style.md`**: style packs, palette, line, lighting, camera, acting, formats, UI kit, data and maps, text
- **`references/custom-characters.md`**: presets, every `Ch.person` option, walking, gestures, lip-sync, outfits, animals, new characters, real images
- **`references/reach-and-workflow.md`**: captions, voiceover, pacing, thumbnails, formats, drafts, brand kit, plan, QA, preview, shots, snap, multilingual text
- **`references/engine-api.md`**: every function in the engine, with its parameters
- **`references/review-and-gotchas.md`**: review commands, sync verification, known pitfalls and fixes

### Scripts
- **`scripts/new-project.js`**: scaffold a project (`--from <starter>`, `--format 9:16|1:1|4:5`) with a preflight check
- **`scripts/test-audio.js`**: a fast audio regression test covering every instrument, genre, the singer and the loudness meter. Run it after touching `engine/audio`.
- **`scripts/smoke-test.js`**: an end-to-end engine check covering render, mux, verify, the tools, voice, analyze, styles and every starter. Run it after changing the engine.
- **`engine/render.js`** modes: `stills`, `sheet`, `board`, `clip [--gif]`, `preview`, `cast`, `video`, `mux [--subs]`, `check`, `verify`, `pacing`, `qa`, `plan`, `poster`, `srt`, `formats`, `brand`, `brand-from <url>`, `analyze <song>`, `snap <url>`.
  - Flags: `--draft`, `--res 1440` (2K) or `--res 2160` (4K), `--format 9:16`, `--style neon`.
  - Times: seconds, `bar:beat` or `@marker±sec`.
- **`engine/tools/levels.js`**: a per-section RMS and peak meter for the mix and stems
