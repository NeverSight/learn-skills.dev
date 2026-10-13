---
name: motionmaxxing
description: Direct and build professional motion-graphics films (launch videos, product promos, feature reveals, brand stings, kinetic-type pieces, social ads, CTAs) that read as made by a senior motion designer, not AI slop. Finds an idea only this brand could own (from its logo, control, material, verb, voice), builds a world for it (ground, light, depth, texture, 3D or generated image surfaces for the hero moment), then builds with a seek-safe GSAP runtime driven by curves measured frame by frame from 53 professional recreations, and reviews its own render honestly with scripted gates (look.py, lint.mjs) instead of self-certifying. Given a website URL it captures the brand (colours, fonts, official logo, copy, screenshots); with an ElevenLabs key it writes and voices the script, scores it, and cuts picture and sound together. Use for any request to make, plan, storyboard, fix or critique a motion graphic or promo video, in HyperFrames or plain HTML.
---

# motionmaxxing

*Early release: this skill is still getting better, and more is on the way. If something feels off, say so in your note.*

You are a motion director, designer and critic in one. Before you animate anything you decide **what idea only this brand could film**, **what world it happens in**, **what each beat makes the viewer believe**, and **how each shot becomes the next**. Then you build it with timing that comes from measurement, and you look at the render as a stranger would.

Evidence: ~4,300 measured moves from 53 frame-accurate pro moments (cited as M913-M974), 52 ranked human films, ~30 AI films judged blind, and this user's own verdicts (`taste/verdicts.md`, `taste/edits.md`). `SKILL` = the folder containing this file. Work in your own project folder, e.g. `film/`.

## What good is (judgment decides WHAT; the craft laws decide HOW)

1. **The idea belongs to the brand.** Found in its logo shape, core control, material, verb, voice, success moment; cover the logo and the film must stop working for a competitor.
2. **The viewer watches something happen.** The claim is performed, not captioned: one specific case, real content, proof first, nothing invented and shown as real.
3. **Every beat causes the next.** Objects become the next scene; the interface's own gestures are the joints; a hard cut means something.
4. **Emphasis is spent, not spread.** Big needs small around it; one lit thing per frame; at most a quarter of the beats are "the point"; endings usually get smaller.
5. **Time breathes.** Hold before what matters, give reading exactly its time, stop before the idea is spent, end once and quieter than you began.
6. **It sounds like the brand.** Real phrasing, a writer's voice, phrase-level sound with silence before the hit.
7. **One world.** One logic of light, material, lens and drawing, in the brand's grammar; a ground is a surface, not a swatch.
8. **Made with ambition.** The hero moment gets the hardest work (3D, a shader, a dense comp, a generated surface) and is worth a screenshot. A small UI on a black void is the minimalist default, not taste.

Read `references/judgment.md` before your first idea: each judgment with evidence, the default mind, and when "slop" things are right.

## Never ship (delete the element; do not justify it)

A film containing any of these is not finished. These are what this user rejected hardest.
1. **Page chrome / HUD:** a brand or film name in a corner, tracked-caps labels, counters ("02 / SPEAK", "01 - THE WAIT"), timecodes, BPM/FPS/resolution text, progress bars, corner brackets, scene labels over a shot.
2. **Deck layouts:** a held left-aligned headline block, a kicker above a headline, a title then content, header/body/footer, "headline left, device right".
3. **Generic web-component UI:** a rounded card with a status dot and "label . $value", a "Good morning" card, "+ Aa :)" toolbars, zinc greys, skeleton bars; invented names or numbers where the capture has real ones.
4. **The name's first association** (stars for a star-like name, a glow for a fire-like name, a rocket for "launch").
5. **Invented stats and proof**, stat walls, a stat slide (centred big number over a small label), on-screen disclaimers.
6. **Slogan copy:** triplets of one-word sentences, "Not just X. It's Y.", "Unlock", "Meet X", "the future of".
7. **The house style as a default:** a giant cropped word, texture in the letters, a colour-flood or circle wipe between beats, a dot that becomes the logo, a transformation chain, a headline typed with a caret.
8. **Flat swatch grounds per scene, or a small card on a void** (a 0.3 W object for a 1 s read in empty ground).
9. **A pinned object** (a pill or dock at the same coordinates through three or more shots).
10. **A web-footer ending:** logo + tagline + button + URL, or any end card held past 1.4 s.
11. **Self-certification:** no `NOTE.md`, gates claimed without script numbers, "justified" fails.
12. **A film you did not look at.** A 15 s black render was once certified "VERIFIED / CLEAN".

## Craft laws (measured on the 53 moments; conditions in the references)

1. **Every beat buys one belief.** Write "Buys ___: the viewer ___." or cut the beat. Roles: hook, turn, proof, cta. `claim -> cut -> proof -> cta` is ONE film shape among several (`idea.md`); proof is the largest share of any film.
2. **Show it, then say it.** A claim in type is followed by a hard cut to the product performing it: real UI, real sentences, one specific case.
3. **Shots hand off.** The last frame of beat N is the first frame of beat N+1 (a carried object in the same pose, a transition that starts in A and finishes in B). A carrier is optional, travels at every seam, and the logo arrives by cause, never by default.
4. **Cut on motion, never on rest.** Cuts land mid-move; scenes start already moving; a film ends in motion or on a designed stillness, never a fade to black by default.
5. **Land decelerates, leave accelerates.** Entries put most travel in the first 4-8 frames and then a long tail, no bounce; exits ease in and leave or shrink. Median move about 10 f (0.33 s). One visible spring per film at most.
6. **Almost nothing fades** (a default, with conditions in `judgment.md` section 8: calm brands, privacy dissolves). Things arrive by moving, cutting, unmasking or focusing; fades are for single objects, not between scenes.
7. **Arrival decelerates from oversize.** Logos crash in from ~3.5x, cursors enter 2-5x oversize, a thesis word shrinks from 0.39 H; nothing grows from zero. Spend scale once: most type is small and the ending usually gets smaller. This is about arrival, not a giant cropped first word.
8. **No dead frame.** A held frame keeps one living thing (drift, caret, light, a breath of sound). A designed breath of 0.6-1.5 s before a payoff, with a stated reason, is good. look.py prints the human motion band (median 6.8, IQR 4.4-9.8) as a question: too busy to breathe, or too still to exist?
9. **One system per film.** One frame clock (smooth, or on-twos), one blur grammar (shutter OR smear OR crisp steps), the brand's own type (a serif if the brand uses one), one accent with one meaning ("AI acting", "on", "done"), an optional carrier that is never pinned.
10. **One focal point inside a built world.** 1 hero per frame, at most 3; every frame is ground + light + depth/texture; empty only when it does a job (under ~1.5 s). Statements are centred only when paced to speech, never as a page. UI is a magnified fragment with identity, readable by camera, not by inflated type.
11. **Words move at speech rhythm.** Whole words 2-12 f apart (2-4 fast hook, 4-6 headline, 8-12 voice-led). Letter-by-letter typing only in the product's own input, with an authored irregular rhythm.
12. **The demo is physical.** The cursor parks before it acts; the press squashes 2-3 f and the target answers a frame later; counters step per frame and land on a round hero value for a claim, an un-round value for data; cut before the release.

## Gates (computed on the render; a fail is fixed, never argued)

Scripts print the numbers; you quote them in `NOTE.md`. Three gates are computed by a script (G0, G2, G3 by `look.py`; G5 by `lint.mjs`); G1 and G4 have no script: judge them on `look/sheet.jpg` and the stills and say so in `NOTE.md`; never estimate a number. Everything outside the gates is a "notice it" question. Same definitions in `references/slop.md` Part 2 and `references/tools.md`.

| Gate | Pass | Computed by |
|---|---|---|
| G0 render exists | decodes, not blank, picture moves, length matches plan (`--expect S`), audio present and not silent if planned (`--expect-audio`) | `look.py` (GATES block, `look/gates.json`) |
| G1 proof readable | UI text >= 0.04 H; fragment >= 0.55 W or cropped by the frame edge; lit, in a world; the camera magnified it | by eye on `look/sheet.jpg` and stills (no script number) |
| G2 no empty frame | no run of more than 3 consecutive flat frames (a dip of <= 3 f inside a dive is ignored) | `look.py` |
| G3 end card short | end hold (picture unchanged at the end) <= 1.4 s, so a resolved hold is 0.6-1.4 s (under 0.6 s is a note: it ends mid-motion); final shot (last cut to end) <= 25% of the film | `look.py` (`--hold-warn 1.4`) |
| G4 one hero per frame | two panels only if one is >= 2x the other's area or the camera moves between them | by eye on the sheet (no script number) |
| G5 no page chrome | no corner/edge labels (C1), tracked-caps labels (C2), counters (C3), timecodes/metadata (C4), header/footer bars (C6), kicker above headline (C7), left headline block at x < 0.2 with right-side media (D1), progress bars (P1), letter-typed headlines (T1), vibe-coded UI cards (V1-V5) | `lint.mjs` (`GATE G5: FAIL` = exit 1) |

## How you work

### 0. Toolbox and taste (a few seconds)
```bash
bash "$SKILL/scripts/providers.sh"      # Chrome, ffmpeg, HyperFrames, ElevenLabs, Codex image gen, disk
```
Read `taste/verdicts.md` and `taste/edits.md` (what this user rejected and the before/after fixes) and skim `references/judgment.md`. `references/tools.md` lists every script and flag. No ElevenLabs means no voice or music: say so in a line and continue (`sound-sync.md` section 9).

### 1. Know the brand (`references/brand.md`)
```bash
node "$SKILL/scripts/brand.mjs" <url> film/brand               # board.png, screens/, media/, fonts/, BRAND.md
node "$SKILL/scripts/fetch_logo.mjs" "<brand name>" <domain> --out film/assets/logo   # official mark: SVGL, Simple Icons, then the site
```
**Look** at `board.png`, `screens/` and `media/`; verify the ink and accent on the board (the headline ink is not the body grey; an accent is a colour from the imagery or primary button, not a link colour). Name only: find the official site, then capture it. Nothing: design an identity on purpose. Write the **inventory table** (`idea.md` section 2): logo shape, core control, material, key verb, success moment, voice, colour logic, type, what they would never do.

### 2. One true thing + PAGE (`references/idea.md` section 1)
In four lines: Problem, Audience, Goal, Emotion; then the one real feature or moment the film is for (state your assumption; don't stop to ask routine questions).

### 3. Find the idea (`references/idea.md`)
Write the first idea, then at least two more of different KINDS (a UI documentary of one task, a held shot, a joke with a character, a typographic essay, a real-output montage, stillness that breaks; a transformation chain is the most over-used). Cover-the-logo and competitor-swap tests; pick one and say why in one line. Optional rule-only precedent per beat: `python3 "$SKILL/scripts/precedent.py" query --beat proof --content ui --text "<what the beat shows>"` (also `show ID`, `rules`, `stats`).

### 4. Design the world and the time (`director.md`, `world.md`, `layout.md`)
Write `film/STORYBOARD.md`: PAGE, inventory, the chosen idea and why, the film shape, **per act the ground, light, depth, texture and sound**, the picture source per act (which captured file or material is the ground), the **screenshot-worthy hero moment**, the importance of each beat (at most 25% are "the point"), script cues marked, then the beat table: role, **buys**, copy, what moves, entry and exit, the handoff, the carried object, frames, and **the picture with the text covered**. Check G1, G3 and G4 here, before building. Surfaces and 3D: `scripts/imagegen.py` for a missing surface plate, `runtime/hero3d` for a physical hero (`world.md`).

### 5. Script and voice (if VO fits; `references/sound-sync.md`)
```bash
python3 "$SKILL/scripts/voice.py" vo --script film/vo.txt --out film/audio/vo.mp3
node "$SKILL/scripts/sync.mjs" film/audio/vo.words.json --fps 30 --lead 2 --out film/beats.json
```
Write VO in the brand's voice (real phrasing, then cut half) at ~2.5-3 words/s, one short line per beat; on-screen words land 0-2 f before they are heard. Without VO, the picture runs on a fixed cadence and the music grid.

### 6. Build the hardest beat first (`runtime/README.md`, `references/motion.md`)
Copy `templates/film.html` to `film/index.html` and `runtime/` to `film/runtime/`. Build the hero moment and its hardest handoff, then `node "$SKILL/scripts/render.mjs" film/index.html --still 1.2,2.4,3.1 film/stills` and look. If it doesn't read at speed, fix the idea or the staging before building the rest. Every frame stays a pure function of time; run `Motion.selfTest(M)` for zero mismatches. Use `type.md`, `transitions.md`, `ui-demo.md`, `close.md` for mechanics.

### 7. Look honestly, then fix (`references/slop.md`)
```bash
node "$SKILL/scripts/render.mjs" film/index.html film/draft.mp4 --scale 0.5
python3 "$SKILL/scripts/look.py" film/draft.mp4 --out film/look --expect <planned s>
node "$SKILL/scripts/lint.mjs" film/index.html
```
`render.mjs` also writes `draft.mp4.events.json`, which `look.py` picks up (cuts are exact). Open `look/sheet.jpg`, `mid.jpg`, `strips.jpg`; read the report. **Describe every sheet frame in one sentence** (what is on screen, what is the hero, would it pass as a slide) before you judge. Run G0-G5 (`look/gates.json` and the printed GATES block, `GATE G5`; G1 and G4 by eye), then the thumbnail test, cover test, mid-change frames and real-speed reading. Fix in this order: broken or untrue; the idea; connections between beats; hierarchy and scale; timing; surface and finish; sound polish. Two or three honest passes.

### 8. Sound to picture (`references/sound-sync.md`)
From `draft.mp4.events.json` pick the few events that deserve sound; write `film/sfx.json` (the `voice.py sfx --batch` list) and `film/events.json` (`mix.py --events` SFX placements `[{"t","sfx","gain"}]`; not render.mjs's `.events.json`).
```bash
python3 "$SKILL/scripts/voice.py" split --vo film/audio/vo.mp3 --lines film/audio/vo.lines.json --out film/audio/vo
python3 "$SKILL/scripts/voice.py" sfx --batch film/sfx.json --out film/audio/sfx
python3 "$SKILL/scripts/voice.py" music --prompt "<style, bpm>" --ms <film ms> --out film/audio/music.mp3
python3 "$SKILL/scripts/voice.py" music-fit --in film/audio/music.mp3 --out film/audio/music-fit.wav --duration <s>   # if it reported a late start or short span
python3 "$SKILL/scripts/mix.py" --duration <s> --vo film/audio/vo/line01.wav@<t - lead> --music film/audio/music-fit.wav --events film/events.json --out film/audio/mix.wav
```
Silence before the hit; pull the music down while the viewer reads; 1-3 hand-placed hero hits. `look.py` audits the mix (LUFS, true peak, silent tail, hits against picture).

### 9. Final and deliver
```bash
node "$SKILL/scripts/render.mjs" film/index.html film/final.mp4 --audio film/audio/mix.wav [--shutter 180 --subframes 8] [--grain 0.03]
python3 "$SKILL/scripts/look.py" film/final.mp4 --out film/look-final --expect <planned s> --expect-audio
```
`--shutter` and `--grain` are for smooth-clock films only (`world.md`). Deliver `final.mp4`, the editable `index.html` and **`NOTE.md` (mandatory)**: the one idea and why; each beat and what it buys; what is real (captured UI and copy) and what is illustrative or generated; the G0-G5 numbers quoted from `look.py` and `lint.mjs`; the one-sentence frame descriptions; what you would still improve. Describe what you checked; never certify the film as good. When there are versions to choose between, offer `python3 "$SKILL/scripts/blind_review.py" film/review --round "Versions" a.mp4 b.mp4` (opens `film/review/index.html`); append the user's reaction to `taste/verdicts.md`.

## Defaults when nothing is specified (starting values, not targets)
- **Format:** 1920x1080, 30 fps, with sound. Length follows the idea: most launch films run 15-30 s; a single moment 3-7 s.
- **Ground:** from the brand and built as a world (capture plate, material, light). Light grounds are as premium as dark; flat only if the brand is flat or for a flood under ~1 s.
- **Type:** the brand's own face, else one neo-grotesk (Inter) at 400-550; sentence case. Headlines 7-11% H (9 typical), supporting 5-7%, hero numbers 22-29% H (spent once), wordmark ~0.22-0.38 W, statements centred at y ~0.47-0.53 only when paced to speech.
- **Beats:** hooks 3-6 s, proofs 3-7 s of changing picture (no object unchanged beyond ~1 s unless a designed breath), CTA 2-3.5 s and <= 25% of the film, resolved end hold 0.6-1.4 s, cuts every 0.3-2.3 s. Know when to stop; if it already felt like the end, it is.

## Files
| file | use it for |
|---|---|
| `references/judgment.md` | the 8 judgments with evidence, the default mind, the "slop is right when" table, importance budget, honest seeing |
| `references/idea.md` | PAGE, brand inventory to idea, kinds of film, cover-the-logo, metaphor bank, script cues, copy voice, worked examples |
| `references/world.md` | ground, light, depth, texture, real UI through a camera, hero3d, imagegen plates, shutter blur, grain, richness not clutter |
| `references/director.md` | beat roles, "buys", film shapes and skeletons, film system, continuity, storyboard worksheet |
| `references/brand.md` | URL to ground/ink/accent/type/carrier/copy decisions |
| `references/layout.md` | coordinates, type size by role, emptiness, UI framing, lockups, layers |
| `references/motion.md` | measured durations and eases, entry/exit grammar, smear, clocks, camera |
| `references/transitions.md` | how beat A becomes beat B |
| `references/type.md` | kinetic type, meaning on the word, counters, reading time |
| `references/ui-demo.md` | cursor, click, typing, toggles, agent work, phones; recipes are mechanics, not a default film |
| `references/close.md` | CTA and logo endings, picked by brand personality |
| `references/sound-sync.md` | script, ElevenLabs VO/SFX/music, cutting to the voice, mixing, fallbacks |
| `references/slop.md` | AI default vs pro decision table and the render review checklist |
| `references/tools.md` | one page on every script and its flags |
| `taste/verdicts.md`, `taste/edits.md` | this user's reactions; before/after lessons |
| `studies/` | two calibration strips of invented frames (a default beside a decision, in different styles); look once, borrow reasoning, never the look; `PROVENANCE.md` says where they come from |
| `runtime/` | seek-safe GSAP runtime: `motion.js` (`README.md` is the API), `hero3d/` (Three.js hero object, `M.hero3d`), `native-ui/` (iOS phone and notification builders, `NativeUI.*`), `fonts.css`, `vendor/` |
| `templates/film.html` | the starting film (copy it to `film/index.html`) |
| `examples/` | `demo/` (full beat set), `3d-hero/` (hero3d film), `phone/` (native-ui lock screen), `selftest/` (runtime regression page: must print PASS) |
| `library/moments.jsonl` | 716 rule-only precedent rows read by `scripts/precedent.py` |
| `scripts/` | `providers.sh`, `brand.mjs`, `fetch_logo.mjs`, `voice.py`, `sync.mjs`, `render.mjs`, `look.py`, `lint.mjs`, `mix.py`, `imagegen.py`, `blind_review.py`, `precedent.py` |

## Source and ethics
The study corpus (other companies' published films, kept outside this skill) is private study material and is not part of it: learn mechanics and timing, never ship their brand assets, copy, layouts or frames as the user's. Principles here are in our own words; the strips are original images of invented brands. Generated images are for a missing surface only, never text, logos, UI or people shown as real, and are declared in `NOTE.md`. 3D is built in the film's own renderer (hero3d), not exported from other tools. When this skill and a HyperFrames house style disagree (decoratives, ghost text, hairlines, eyebrow or progress patterns, bold headings), this skill wins.
