---
name: i-hate-editing
description: Turn raw talking-head takes into a finished, publishable video package — cut, captioned, scored, graded, with platform variants, post caption and thumbnail. For short-form vertical and YouTube talking-head footage. Opinionated by design; the studio makes the craft decisions and takes plain-language direction. Use when someone drops recorded footage in a folder and wants it edited.
---

# I Hate Editing

A studio, not a tool. Someone hands you raw takes; you hand back something they
can publish without touching an editor.

**The bar:** if a professional editor returned this, would the client accept it?
That question decides every call you make. "The pipeline ran" is not done.

## Principles

1. **Judgement is the product; configuration is a failure state.** Never ask
   which font, which transition, which decibel level. Decide, show the result,
   and take plain direction — *punchier*, *slower*, *less music*. The user
   describes the feeling; you own the numbers.
2. **The rules are not suggestions.** `rules/` holds craft decisions that were
   each paid for by a rejected render, and `HARD-RULES.md` holds things that
   fail silently if you deviate. Read both before editing. Artistic freedom
   without taste memory produces the median boring cut every time — that is
   the failure this skill exists to prevent.
3. **Audio is the authority on time.** Cut boundaries come from silence
   detection and word onsets, never from eyeballing video.
4. **Verify before you present.** If you did not look at the frame or measure
   the level, it is not done. See "Verify" below — it is a gate, not a habit.
5. **Deliver a package.** A cut file is not the deliverable. See "Output".
6. **Learn from every correction.** Feedback becomes a durable rule in
   `taste.md`, read before every future edit. The studio should be better on
   the tenth video than the first.
7. **Never fabricate proof.** When footage references a real repo, page, tweet
   or product, capture the real thing. Never mock up something that implies a
   screenshot of reality.

## Setup

First run performs a capability scan and asks what the user is making, then
installs only what is missing:

```bash
python3 scripts/scan.py
```

It writes `profile.yml` (brand, language, pacing, caption style, aspect
targets) and scaffolds the project. Everything downstream reads that file —
there are no hardcoded brand values anywhere in this skill.

Requirements, all free:

| Job | Tool | Notes |
|---|---|---|
| Transcription | `whisper.cpp` | Local. Model chosen by language + hardware. |
| Media processing | `ffmpeg` / `ffprobe` | |
| Captions, cards, compositing | HyperFrames | Renders HTML/CSS/GSAP compositions. |
| Designed scenes | Remotion | React motion graphics, one composition per scene. Installed per project by `scenes.py init`. |
| Composition runtime | `node` 22+ | Already required by Claude Code. |
| B-roll download | `yt-dlp` | Optional. |

Nothing requires an API key and nothing leaves the machine.

## Project layout

Footage lives wherever the user put it. All output goes in `<footage>/studio/`.

```
<footage>/
├── <source takes, untouched>
└── studio/
    ├── profile.yml          brand, language, pacing — the only config
    ├── taste.md             durable feedback; read before every edit
    ├── transcripts/         cached per source, never re-transcribed
    ├── takes.md             packed phrase-level transcript (reading view)
    ├── edl.json             cut decisions
    ├── composition/         HyperFrames project
    ├── scenes.json           designed scenes: which beat, what moves
    ├── scenes/               Remotion project for those scenes
    ├── assets/              fetched SFX, logos, screenshots
    ├── verify/              frames and measurements from the verify pass
    └── out/                 the delivered package
```

## The process

Run in order. Two stop gates; do not run past them.

**1 — Read state.** Load the taste memory and profile before anything else:

```bash
python3 scripts/taste.py --studio <footage>/studio brief
```

Those instructions override the defaults in `rules/` — they are what this
particular person has already corrected you on. Never regenerate an artifact
that is already on disk.

**2 — Inventory.** `ffprobe` every source. Note resolution, fps, duration,
audio channels. Flag anything that will bite later (variable frame rate,
mismatched fps between takes, silent audio track).

**3 — Transcribe.** `scripts/transcribe.py <sources>` — word-level, cached,
language pinned from `profile.yml`. Never auto-detect: auto-detect silently
*translates* some languages, which corrupts every downstream timestamp.

**4 — Pack.** `scripts/pack.py` produces `takes.md`, the phrase-level reading
view. This is what you actually read to make cut decisions — not raw JSON,
and not the video.

**5 — Plan the cut.** Identify beats, pick the best take of each, and place
boundaries. This is judgement work; `rules/cutting.md` has the craft.
Retakes cluster at file boundaries — expect one wherever a source ends.

**6 — Assemble.** Write `edl.json`, then `scripts/render.py` for a draft.

**7 — Verify the cut.** *Gate.* See below. Fix and re-verify before showing
anything.

**8 — Present the cut.**

```bash
python3 scripts/review.py --studio <footage>/studio
# phone preview on a trusted network only:
# python3 scripts/review.py --studio <footage>/studio --lan
```

Opens it in a browser with frame-stepping on **localhost**. Pass `--lan` only
on a trusted network if you need a phone URL — that mode has no auth, and a
machine's IP changes with the network anyway. **STOP.** Do not build captions,
motion or sound on an unapproved cut — every downstream timestamp depends on
it, and a base-cut change invalidates all of them.

**9 — Enhance the voice.** Every reel, right after the cut is approved and
before any sound effect is placed:

```bash
python3 scripts/enhance.py <studio>/cut.wav -o <studio>/voice_enhanced.wav
```

It runs Adobe Podcast Enhance Speech v2 through the signed-in ego-browser
session (upload, poll, download the stems) and mixes the website's default
"Speech 50%, Background 10%, Music 10%" locally. About 30s for a short reel.
Then:

1. Level it: `acompressor=threshold=0.045:ratio=3.2:attack=6:release=110:makeup=1`,
   then gain and `alimiter=limit=0.7` to land near -18.4 LUFS. Boosting it plain
   to -15 LUFS pushes speech into the limiter and every sting collapses.
2. Remux it as the cut's audio (`-c:v copy`), so no video re-render is needed and
   every timestamp holds. The script fails if the duration drifts over 50 ms.
3. Place stings and mix against this enhanced voice, not the raw take.

If it prints `NOT_SIGNED_IN`, ask the user to sign in to podcast.adobe.com in
ego-browser. Never type credentials. Use `--mix full` only when asked; 100%
enhanced speech sounds processed.

**10 — Enrich.** In order:

```bash
python3 scripts/grade.py    cut.mp4 --strength normal   # look at the comparison
python3 scripts/captions.py  --studio <studio>
python3 scripts/proofread.py fix --studio <studio> --name "Claude" --name "<tool>"
python3 scripts/capture.py  <url> --studio <studio> --find "<the phrase>"
python3 scripts/icons.py fetch claude github --studio <studio>
# Generated stills for beats with nothing real to show — see "Generated stills".
python3 scripts/gen_image.py "<full prompt>" --studio <studio> --name payoff --animate 3
# Optional: 2–3 AI B-roll clips (3s each) — writes studio/broll.json + assets/broll/
# Author studio/slots.json from takes.md beats first; see broll-gen skill.
~/.claude/skills/broll-gen/scripts/broll-gen generate --studio <studio> --slots <studio>/slots.json --duration 3
python3 scripts/sfx.py plan --studio <studio> --library <sfx>
# Designed scenes for beats with structure — see "Designed scenes".
python3 scripts/scenes.py init   --studio <studio>
python3 scripts/scenes.py check  --studio <studio>
python3 scripts/scenes.py render --studio <studio>
python3 scripts/compose.py  --studio <studio> --render
```

### Generated stills

`scripts/gen_image.py` talks to a local Gemini proxy
(`http://127.0.0.1:8081/v1`, key `sk-gemini`) — no account, no cost, no
watermark. Image generation there is a **route, not a model**: nothing in
`/v1/models` makes images, `n` must be 1, and `size`/`quality`/`style` are
rejected, so the aspect goes in the prompt text. The script injects the
vertical-9:16 clause for you and warns if what comes back is landscape. It
injects nothing else — when a beat needs text, logos, screens or UI kept out,
put that ban at the end of that beat's own prompt.

**Reach for it only after checking there is nothing real to show.** A repo, a
page, a dashboard always beats a generated still — see `rules/proof.md`. And a
generated image must never imply a screenshot of something real.

**Write the whole prompt.** A short prompt returns a stock-photo cliché. Every
prompt states, in this order: the subject, the setting, the camera (lens,
aperture, height), the lighting with its direction and colour temperature, the
composition including which parts of the frame stay empty, the mood, and the
ban list. `--animate N` renders a push-in clip from the still, because a
generated still that sits motionless is a dead frame; add the clip to
`broll.json` as an overlay.

Worked prompt, for the "gold mine" payoff beat of a reel about saving money:

> A deep underground cavern of glowing golden light, with streams of tiny
> luminous golden particles rising out of the darkness like sparks. Rich black
> background, warm gold highlights, high contrast, dramatic rim lighting,
> shot on a 35mm lens at f2, abstract and atmospheric, the lower third almost
> pure black so captions stay readable. Cinematic, fine film grain.

Full prompt library and failure log: `~/ai-me/reels/docs/agent-suggestions.md`
and `~/.claude/skills/virtual-bg/references/plate-prompts.md`.

**Do not generate a virtual background.** Reels ship with the real room — see
`taste.md` under framing, and the STOP notice in the `virtual-bg` skill.

You author four files by hand, the same way you author the EDL. They are the
edit; the scripts only render them.

**`cards.json`** — the motion vocabulary. Without it the piece is a face with
captions, and `beats.py` will fail step 11.

```json
{"cards": [
  {"start": 0.35, "duration": 5.1, "style": "band", "big": "SIX WORDS OR FEWER"},

  {"start": 13.1, "duration": 4.2, "kicker": "small label above",
   "big": "HEADLINE WITH *ACCENT* WORD", "sub": "one supporting line",
   "items": [{"title": "row one", "note": "right-aligned"},
             {"title": "row two", "note": "staggered in"}]},

  {"start": 21.6, "duration": 1.9, "full": true, "big": "OWNS THE *FRAME*"}
]}
```

Add `"icon": "claude.svg"` to put a brand mark on a card, and
`"brand_colour": "#D97757"` to theme the whole card in that brand's colour —
`icons.py` reports the official hex when it fetches. A named tool with its own
mark on its own colour reads as designed; the same dark card every time reads
as a template.

`style: "band"` is the hook headline over a full frame. Default is a
half-screen split: card on top, face below. `full: true` takes the whole frame
and hides the face — captions are suppressed under it. `*asterisks*` mark the
accent word. `items` makes it a numbered list. Choose the form from what the
sentence is doing, and the arrival is chosen for you — see `rules/motion.md`.

Captions come out of `captions.py` as a raw pass and are marked
`proofread: false`. `proofread.py` restores product names and strips
punctuation artefacts, but it cannot fix meaning — so it only marks them
proofread when a model pass ran (`--llm "<any command>"`) or when you rewrote
the copy yourself and passed `--accept`. Verification fails while the flag is
false, because captions are the most-read thing on screen.

**`proof.json`** — real pages: which capture, which target, which move.

```json
{"beats": [
  {"asset": "repo", "start": 6.9, "duration": 3.1,
   "action": "scroll", "from_y": 60, "to_y": 560},
  {"asset": "repo", "start": 10.1, "duration": 2.9, "action": "zoom",
   "target": "the exact text", "highlight": true, "highlight_at": 0.75}
]}
```

`asset` is the `--name` you gave `capture.py`. `target` must be text that
capture found. `rules/proof.md` has the craft.

**`scenes.json`** — designed scenes, built in Remotion. A card is text on a
ground; a scene is a built visual with structure — a counter running, a
comparison assembling, a stylised UI typing. Beats with structure go here
rather than into a headline and a sub-line.

```json
{"scenes": [
  {"id": "token-waste", "start": 12.4, "duration": 3.2, "full": true,
   "line": "every retry re-sends the whole conversation",
   "visual": "context bar fills, three retry chips stack on it, bar turns red on the third",
   "assets": ["claude.svg"]}
]}
```

`scenes.py sync` writes the Remotion project's `Root.tsx` and
`src/data/scene-spec.json` from this file and the cut — one composition per
scene, at the cut's own size and frame rate. You write only the components, in
`<studio>/scenes/src/scenes/<Component>.tsx`. `scenes.py studio` opens Remotion
Studio to preview them, `render` writes one MP4 per scene and registers them as
overlays so `compose.py` composites them under the captions.

Show `scenes.json` before writing any component — a component written against
an unapproved beat is the expensive artefact to throw away. Craft and the
self-review checklist: `rules/scenes.md`. Scene stings go in `sfx.json`, never
inside the component: overlays composite muted (`HARD-RULES.md`).

**`profile.yml`** — written by `scan.py`, or by hand when it cannot run
interactively:

```yaml
language: ur
translate_captions: true
aspects: ["9:16"]
pacing: punchy            # punchy | balanced | restrained
brand: {accent: "#76B900", font: "Archivo Black"}
transcription: {model: large-v3-turbo}
face_half_y: 30           # vertical crop of the face in a split
```

This is where a trimmed recording becomes an edited video.

**11 — Verify the render.** *Gate.* Frames and levels, again, plus the beat
map:

```bash
python3 scripts/beats.py --studio <studio>      # stretches with nothing new
python3 scripts/sound.py check out/master.mp4   # stings audible, not just present
```

A shot that sits still is the most-reported defect in short-form and the
easiest to miss, because nothing errors when a face holds for ten seconds.

**12 — Deliver the package.**

```bash
python3 scripts/music.py   out/master.mp4 <bed>.mp3 -o out/final.mp4
python3 scripts/deliver.py --studio <studio>
python3 scripts/review.py  --studio <studio>
```

Then write `out/post.md` yourself from the spoken lines it surfaces, and look
at the thumbnail candidates and pick one. Neither is generated: a generated
title reads like a generated title, and "face clear, eyes open" is not a
metric.

**13 — Learn.** Record every correction the user made, phrased as an
instruction for next time and filed under the area it affects:

```bash
python3 scripts/taste.py --studio <footage>/studio add captions \
  "Start each caption 0.08s after the word is spoken, never before" \
  --said "we show early for a sec then I start speaking"
```

Always pass `--said` with their actual words. The instruction is your reading
of the feedback and can be wrong; keeping the original means a bad reading can
be corrected later instead of quietly hardening into a rule.

When a rule stops applying, retire it rather than deleting it —
`taste.py retire <area> <n>` — so the reversal stays visible.

## Verify

Two failures survive every automated check and both get flagged by users, so
hunt them explicitly.

**Repeated phrases at seams.** A join can leave a word said twice. Transcribe
the rendered cut in short windows aligned to each seam — never one whole-file
pass, which condenses and hides the defect.

**Clipped clauses.** Every kept block must start and end on a complete
thought. A cut that lops a negation inverts the meaning of the sentence. If
the clause only completes in a later take, stitch the two rather than shipping
the fragment.

Then: `ffprobe` the duration against what the EDL predicts, extract frames at
every boundary and look at them, and measure audio levels at each sound effect
against a voice-only baseline. "Not clipping" is not the same as "audible" —
see `rules/sound.md`.

## Output

Every finished run delivers a package, because that is what an editor hands
back:

- **Master** — graded, mixed, captioned
- **Platform variants** — vertical, square, landscape as `profile.yml` requests
- **Post caption** — hook line, substance, hashtags
- **Thumbnail frame** — pulled from the cut, face visible, no mid-blink
- **Title options** — a small set to choose from

## House style

Locked on the NVIDIA and Promptive reels (2026-10-02). Apply it by default; the
details and the reasons are in the rules files named.

- **Hook, 0 to about 3.4s** (`rules/hooks.md`, "The split-proof hook"):
  - Split from frame 0, with an HD visual on top and the face below.
  - Text: 2-3 familiar words plus one emoji ("CLAUDE / LIMIT ISSUE 😕").
  - The top panel changes once at 1.0-1.3s.
  - Named tools' marks pop in on their spoken names.
  - A loss word turns the whole frame red for about 0.5s.
  - Plan it with `hook_plan.py --proof <capture>`.
- **Everything HD:**
  - The hook's top panel is a motion graphic built at frame resolution, never
    an upscaled screenshot.
  - Rebuild product screenshots as native Flick/Remotion scenes at 1080x960,
    using the real UI's text (`rules/proof.md`).
- **Palette:** green `#76B900` for emphasis words in captions, accents, chips
  and borders. The ground is near-black green with a slow-drifting grid. It is
  the profile default; a brand colour in `profile.yml` still wins.
- **Sound:**
  - Pop sting: `assets/sfx/pop_dragon.mp3` (peak 0.197s; start = hit - 0.197).
  - Impact on frame 1, swoosh on a panel swap, click on a highlight.
  - Every sting +2 to +4 dB above the enhanced voice (centre +3.1). Master at
    -15 LUFS.
- **Voice:** Adobe Enhance (step 9) on every reel.
- **Cut:** transcribe the first 0.3s of every block on its own. A clipped false
  start ("com" before "link chahiye") hides at block heads.

## Craft rules

Read the relevant file before touching that part of the edit. Each rule states
the failure it prevents.

| File | Covers |
|---|---|
| `HARD-RULES.md` | Correctness. Silent failures. Non-negotiable. |
| `rules/cutting.md` | Take selection, boundaries, silence, pacing |
| `rules/hooks.md` | Openings, headline, retention |
| `rules/captions.md` | Timing, chunking, style |
| `rules/sound.md` | Sound effect placement, levels, music |
| `rules/proof.md` | Screenshots, B-roll, zoom and highlight |
| `rules/motion.md` | Zooms, transitions, cards, layout |
| `rules/scenes.md` | Designed Remotion scenes: when, how, what to check |
| `rules/framing.md` | Crops, splits, composition |
| `rules/assets.md` | Where pictures come from: proof, reference clips, flick, generated stills, Flow |

## Anti-patterns

- Asking the user to configure something you should have decided.
- Building captions or motion before the cut is approved.
- Trusting a whole-file transcript to verify a cut.
- Concluding a sound effect works because it did not clip.
- Re-transcribing a source that has not changed.
- Auto-detecting the spoken language.
- Presenting output you did not look at.
- Rendering a sentence with structure as a headline and a sub-line.
- Writing a scene component before `scenes.json` was agreed.
- Baking a sound effect into a scene, where the mix never hears it.
- Adding a feature nobody asked for.
- Finishing an edit without recording what the user corrected.
