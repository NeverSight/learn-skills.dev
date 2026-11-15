---
name: motion-graphics-video
description: "Create motion graphics videos (MP4) end to end with a free, local, deterministic pipeline: story brief, reference-derived style guide with a banned-defaults list, audio-first production (ACE-Step 1.5 local music generation, code-synthesized sound effects, optional Kokoro voiceover), shot list on a beat grid, Hyperframes HTML+GSAP compositions rendered by headless Chrome and FFmpeg, contact-sheet self-critique loops until every shot grades 8+, and multi-format export. Use when asked to make a motion graphics video, kinetic typography piece, lyric video, product teaser, launch film, or showreel-style MP4."
license: MIT
---

# Motion graphics video

Produce a finished motion graphics MP4 the way the viral Opus 5.5 creators do it:
the prompt is 10% of the video, the harness is the other 90%. This skill is the
harness.

The core insight from studying the viral motion graphics wave (2026): models
default to "mid" output (centered text on a gradient, everything fading in)
unless the setup forces otherwise. The setup has five load-bearing parts, and
skipping any one of them is what makes output look generated:

1. **Story, not a task.** A crew persona and a story beat sheet, not "make a
   video about X".
2. **A reference-derived style guide plus a banned-defaults list.**
3. **Audio first.** Real music (local, free), a measured beat grid, code-made
   sound effects. Motion without sound is a slideshow.
4. **A shot list cut to the beat grid** before any animation code.
5. **A self-critique loop.** The model renders, looks at its own frames, grades
   them, and fixes the worst problems before the final render.

## Usage

Load this skill for any request like:

- "Make a 15-second motion graphics video about our product launch"
- "Create a kinetic typography / lyric video for this track"
- "Turn this announcement into a showreel-style MP4 for X/Twitter"
- "Make me a teaser video, 9:16, with music and sound effects"

If the request is only about *scripting* the narration or voiceover text, use
`video-script-writing` instead. If the user explicitly wants a Remotion/React
codebase, use `remotion-video`. Otherwise this skill is the default for
finished motion graphics output.

## Requirements

Check all of these before starting; tell the user what is missing.

| Requirement | Check | Install |
| --- | --- | --- |
| Node.js 22+ | `node --version` | nodejs.org or `nvm` |
| FFmpeg | `ffmpeg -version` | `brew install ffmpeg` |
| Hyperframes CLI | `npx hyperframes --version` | `npx hyperframes init` |
| ACE-Step 1.5 music | steps in audio reference | `references/audio.md` |
| Kokoro TTS (voiceover, optional) | `pip show kokoro` | `references/audio.md` |

Everything runs locally and costs $0. No API keys. If the user declines local
music install, fall back to a user-supplied track or the free hosted fallback
in [references/audio.md](references/audio.md). Never silently ship a silent
video; motion graphics without audio is the number one tell of a bad result.

## What It Does

Eight phases. Phases 1-4 are planning and produce documents the user can veto
cheaply. Phases 5-7 are build and self-critique. Phase 8 ships.

| Phase | Output | Gate |
| --- | --- | --- |
| 0. Environment | render toolchain works | all checks pass |
| 1. Brief | `docs/brief.md`, story beats | user approves story |
| 2. Style | `docs/style_guide.md`, banned list | user approves look |
| 3. Audio | `track.wav`, `beats.json`, SFX set | music beat-mapped |
| 4. Shot list | `docs/shotlist.md` on beat grid | user approves shots |
| 5. Build | Hyperframes HTML + GSAP comp | lint clean, preview plays |
| 6. Critique loop | contact sheet, graded shots | all shots 8+, 3 rounds |
| 7. Final render | `out/final.mp4` verified | duration, audio, LUFS ok |
| 8. Deliver | video, contact, poster, notes | - |

## How It Works

### Phase 0 - Environment

Run the requirement checks above. Note free disk space before any music model
install (ACE-Step 1.5 needs about 10GB). Confirm target format(s) with the
user: 9:16 (1080x1920) for shorts, 1:1 or 16:9 (1920x1080) otherwise.

### Phase 1 - Brief

Adopt the crew persona in all work on this video: you are the director,
writer, animator, composer, sound designer, and render engineer. Then write
`docs/brief.md`:

- **Story** in one paragraph. If the user gave a topic, propose a story with an
  emotion (2:00 AM energy, launch-day swagger, quiet confidence). A task
  produces a demo; a story produces a video.
- **Beat sheet**: 5-8 beats, one sentence each, each 2-4 seconds on screen.
  Standard arc: hook (the tension in under 10 words of huge type) - build
  (the idea assembles) - proof (one number or moment) - turn - payoff/logo.
- **Audience, platform, duration, format(s), and references** the user named.

Get explicit approval of the story before styling. This is the one decision
that is genuinely the user's.

### Phase 2 - Style

If the user provided a reference (frame, video, or image folder): extract
frames with FFmpeg, study them, and write `docs/style_guide.md` from evidence.
Take the grammar of the reference, never its content, logos, or characters. If
there is no reference, name a real style/studio/look and write the guide from
that. Descriptions lose to names; "Swiss grid with brutalist type" beats
"clean and modern".

The style guide must pin: palette (hex, one accent), type (one display face,
one UI face, weights, tracking), shot lengths, transition types, camera moves,
texture/grain, and how text enters and exits. Full template and the default
banned-defaults list: [references/brief-and-style.md](references/brief-and-style.md).

### Phase 3 - Audio

Audio before animation. Produce, in order:

1. **Music** - generate or select the track. Preferred: ACE-Step 1.5 locally;
   generate 6+ candidates with genre/BPM/structure prompts and pick the one
   whose build and drop land on the video's story beats. Use the chosen track
   unchanged. Full options and install steps:
   [references/audio.md](references/audio.md).
2. **Beat grid** - run `scripts/beat_grid.py audio/track.wav -o docs/beats.json`
   to measure onsets and BPM. Every scene cut lands on a beat or a half-beat.
3. **Sound effects** - synthesize with `scripts/sfx_synth.py` (whoosh, impact,
   riser, sparkle, tick). One SFX per meaningful motion, never more; remove
   anything loud or unnecessary.
4. **Voiceover** (optional) - Kokoro TTS per section; word-level timing if
   lyrics or narration must sync on screen.
5. Note the mix target now: final master normalized to -14 LUFS.

### Phase 4 - Shot list

Write `docs/shotlist.md` on the beat grid. Every shot records: start/end
seconds, duration in seconds and frames, camera move, on-screen text (exact
copy), SFX cue, and which story beat it serves. Cut scene boundaries to beats.
Show the shot list to the user and wait for approval (or proceed if they
pre-authorized it). Re-cutting a list is free; re-rendering is not.

### Phase 5 - Build

Scaffold with `npx hyperframes init <project>`, then author `index.html`:
plain HTML + CSS + a GSAP timeline, scenes marked with `data-start` /
`data-duration` attributes. Follow the house rules (below) and the Hyperframes
gotchas in [references/render-and-critique.md](references/render-and-critique.md).
Validate with `npx hyperframes lint`, then `npx hyperframes preview` and watch
it end to end before rendering.

**House rules (non-negotiable, applies to all code in the project):**

- Every frame is a pure function of time. The renderer seeks the timeline; no
  `Date.now()`, no `setTimeout`, no `requestAnimationFrame`, no CSS
  transitions/animations in the render path, no state carried between frames.
- Seeded randomness only (e.g. mulberry32 with a fixed seed). Never
  `Math.random()`.
- Entrances ease and overlap; nothing moves linearly; nothing just fades in.
- Every 2-4 seconds something new happens on screen. A still element on a
  still background is a JPEG with a progress bar.
- Banned by default (unless the brief overrides): centered title on a gradient,
  everything fading in, corner labels and frame borders, glow on UI chrome,
  generic particle bursts, default system fonts.
- One display face, one UI face, one accent color.
- Shader/WebGL transitions at 2-3 key moments maximum; hard cuts elsewhere.
- Use `autoAlpha`, not bare `visibility`, for scene toggles. Grain via CSS
  gradients, never SVG filters (they break headless capture).

### Phase 6 - Critique loop

Render a draft (`npx hyperframes render --quality draft`). Then:

1. `scripts/contact_sheet.sh out/draft.mp4 <duration> 12` produces
   `contact.png`, one frame per beat.
2. Look at the contact sheet. Grade every shot 1-10 on story clarity,
   composition, motion quality, typography, and sync with the music.
3. Write down the three worst problems. Fix those only. Re-render draft.
4. Repeat. Minimum 3 rounds. No shot below 8 in the final render.

Then an animatic check at 960x540 with placeholder audio to verify pacing
before the expensive pass. Full rubric:
[references/render-and-critique.md](references/render-and-critique.md).

### Phase 7 - Final render and verification

```bash
npx hyperframes render --quality high --fps 30 -o out/final.mp4
scripts/verify_render.sh out/final.mp4 <expected-duration>
```

Mix to -14 LUFS. Verify duration matches the composition, the audio stream
exists, and a mid-video frame extract looks right. Then export every requested
format from the same composition by reflowing the layout per format
(type sizes, positions), never by cropping a 16:9 render to 9:16.

### Phase 8 - Deliver

Hand the user: `out/final.mp4` (plus other formats), `contact.png`, a poster
frame, and three concrete notes on what you would improve with another round.
Iteration is the method; say where the next hour would go.

## Common pitfalls

- **Silent video.** If music generation is unavailable, stop and ask. Never
  ship motion graphics without an audio track.
- **Skipping the shot list.** Animation before a beat-grid shot list is how
  "mid" videos get made.
- **Letting the banned list lapse on revision passes.** Every re-render
  re-checks the banned defaults; fixes regress toward defaults under pressure.
- **One giant render at the end.** Draft renders are cheap; use them.
- **Wall-clock motion.** It previews fine and renders garbage. Determinism
  rules exist because the renderer seeks, it does not play.
