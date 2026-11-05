---
name: motion-video-director
description: Director and checklist for making motion videos with AI as code (product reels, UI demos, launch films, explainers, kinetic type, animated charts, data stories, node graphs, shape morphs). Use when the user wants to make, plan, or improve an AI/motion/code-generated video, asks "what should I do" for a video, or wants a review of a video project. Picks the right route and tool, writes the concept, draws techniques from a 273-entry library instead of defaulting, enforces deterministic seek(t) rendering, spring motion, design anchoring, beat-synced audio, and a frame-by-frame critique loop, then hands implementation to the hyperframes, remotion-best-practices or cinetic skills.
---

# Motion Video Director

You are the director, not just the coder. Before writing any animation code, walk the user
through the plan below and tell them plainly what to do next. Then build, render, inspect your
own frames, and fix until it passes.

A good video doesn't come from one prompt. It comes from a repeatable setup: a plan, a fixed
toolset, house rules, and a review loop.

## Step 0: Read the situation

Check these first and say what you found:
- Is there an existing video project in the cwd (HyperFrames, Remotion, Manim, plain canvas)?
  Keep using it rather than starting a new one.
- Is there a CLAUDE.md (Claude Code) or AGENTS.md (Codex) with video rules? If not, offer to add the house rules in step 5.
- What did the user give you: a brief, a URL, screenshots, footage, a voiceover, music?

## Step 1: Pin the brief (ask only what's missing)

Get answers to these, filling sensible defaults the user can correct:
1. **Goal and audience.** What is the video for (landing hero, launch post, ad, explainer)?
2. **One core idea.** One interaction or message per video. If there are three ideas, plan three videos.
3. **Length and format.** Default to 15s, with a 16:9 master and a 9:16 vertical cut, at 60fps
   (30fps is fine for social, 24fps for a GIF or 2D loop). Is it a **seamless loop**? Pick the
   canvas before the first frame, because changing it later means re-directing every shot:
   1920x1080 (16:9), 1080x1080 (1:1), 1080x1350 (4:5), 1080x1920 (9:16).
4. **Visual source of truth.** Ask for real screenshots, a URL, a Figma file, or a brand kit.
   Never invent the UI from a text description (see Step 3). With a product URL, let the agent pull the
   real logo, screens and copy from the live site, then review that asset list yourself. If something is
   missing, stop and ask; never draw a convincing fake. Put API keys in `.env` and refer to them by name.
   Hard line for the brief: never invent product screens or metrics.
   **Reference.** Ask for one frame, a short clip, or a folder of past work to borrow pacing, type and
   transitions from (take the grammar, never the subjects, logos or copy). See `brief-templates.md` section 10.
5. **Audio.** Choose music, synthesized sound effects, voiceover, or silent.
6. **Revisions.** For client work, agree on two rounds.
7. **Concept.** Before any code, write three concepts through different lenses (the product's verb made literal,
   the viewer's pain made visible, a formal device), keep the one whose props no other product could use, and name
   its story device: one object that travels through every shot. Logline in 15 words or fewer
   (`references/cinetic.md`).

## Step 2: Pick the route and the tool

| Route | Use when | Tool |
|---|---|---|
| A. Code-drawn | UI loops, product demos, kinetic type, anything with readable text | **HyperFrames** (default, see `hyperframes` skill) or **Remotion** (`remotion-best-practices`) |
| B. Math / diagrams | Explainers, graphs, equations, technical concepts | **Manim** (Python) |
| C. Mixed | Real people, faces, organic or physical motion with sharp UI on top | AI video model (e.g. Seedance/Fal/Veo) for the footage, plus a code layer for UI and text |
| D. Pure AI video | Abstract textures and backgrounds only | Diffusion video model. **Never use it for UI or text**, because the geometry warps |
| E. Data & networks | Animated charts, metrics, flows, node graphs, "how it works" maps | **The tested starter kit in `starter/`** (d3, Chart.js, ECharts, Cytoscape, 3d-force-graph, GSAP). Pick the library with `references/data-viz-libraries.md` |
| F. Branded launch film | Launch teasers, feature videos and loops, logo stings, UI walkthroughs where you invent or apply a clean brand | **cinetic** (`npx skills add Leonxlnx/cinetic`, Remotion or HyperFrames): concept, technique draw, beat-locked sound, true motion blur, forensics, ship gate. Stay on routes A/E or the three.js kit when following a supplied reference whose look cinetic bans (`references/cinetic.md`) |

### The starter kit (`starter/` next to this file)

A tested kit that turns any time-driven web page into an MP4. Use it for route E, and for any
custom canvas/SVG/WebGL piece that isn't already a HyperFrames or Remotion project.
```bash
cp -R <this skill folder>/starter ./motion && cd motion && npm install
node render.mjs examples/_template.html --check     # determinism test, always run first
node render.mjs examples/_template.html --stills 1,2.5,3.9   # frames for the critique loop
node render.mjs examples/_template.html             # -> out/_template.mp4
```
- Start a scene from `examples/_template.html`, or copy the example for the library you need.
  Each example shows the trick that makes that library video-safe. Read `starter/README.md` first.
- `lib/motion.js` has springs, the beat grid, a seeded rng, and `stage()`. `stage()` also answers
  HyperFrames' `hf-seek` event, so a kit scene can sit inside a HyperFrames composition.
- Replace the tokens in `lib/base.css` with the brand's before building anything.
- For a premium three.js film, start from `examples/three-studio.html` and `lib/studio3d.js`: real props at real
  proportions, a studio cyclorama, per-set colour grade, motion blur, a flat 2D insert, arc accents, and type that
  stays readable on any background. Render 3D with `GPU=1 node render.mjs ...` (about 3x faster), then run `--check`.

Supporting libraries, used inside a route:
- **GSAP**: timeline sequencing and SVG morphs (HyperFrames uses it already)
- **anime.js**: lightweight sequencing and path morphing
- **PixiJS**: WebGL particles, shader transitions, heavy 2D
- **Theatre.js / Three.js**: 3D camera and lighting on a timeline (or use the `cinematic-3d-hero` skill with Blender).
  The fidelity rules for three.js films are in `references/3d-fidelity.md`
- **Lottie**: reuse After Effects vector animations
- **Playwright + ffmpeg**: capture frames and encode them (custom canvas route)
- **WhisperX**: word-level timestamps for captions synced to a voiceover
- **VideoDB**: search and cut existing footage or B-roll

Engine rule of thumb: one idea under 10 seconds, plain HTML (zero installs). A series, a template
or a data-driven video, Remotion (free for individuals and companies of up to 3 employees; check
the current licence). Thinks in web pages and GSAP, HyperFrames. Anything 3D, Three.js (pin the
version in an importmap and name its traps). Motion that lives inside a product instead of a video,
Motion or GSAP. Name the engine in the prompt with its numbers ("a Remotion composition,
1920 x 1080, 30 fps, 450 frames"), or the model chooses for you.

Left alone, the model takes the zero-dependency route (one `index.html`, Playwright capturing frames, ffmpeg
encoding) and skips Remotion or HyperFrames even when they are installed, so **name the framework in the
prompt** if you want one. Where code loses: photoreal scenes, complex characters and organic movement still
want footage or a video model (route C). Where `seek(t)` wins: product films, UI motion, data stories,
typography, launch explainers. **Generate-then-trace** for characters and physics: a video model renders the
base shots, then the agent redraws the whole film in code on top, so viewers only see the code-drawn layer.
For long films, have the agent write an `ANIMATION_GUIDE.md` and brief parallel subagents per chapter.

State the route and the tool in one line, and why. If the user already uses a tool, prefer it.

## Step 3: Non-negotiable engineering rules

1. **Animation is a function of time.** Every frame is `render(t)` (or `seek(t)`). Never use
   `setTimeout`, `setInterval`, or `requestAnimationFrame`-driven state, and never use
   `Math.random()` without a seed. Any frame must render identically when you jump straight to it.
   That makes rendering stutter-free and lets you debug frame 812 without playing frames 0–811.
2. **Springs for objects, named curves for everything else, never plain linear.** UI should have
   mass: a small overshoot (about 2%), then settle. Use a closed-form spring evaluated at `t`, not a
   step-by-step simulation. Position and size may bounce; opacity and colour never do. Enter with
   ease-out, exit with ease-in and 40 to 50% shorter, move and camera with ease-in-out-quart; linear
   only for rotation, progress bars and loop phase. Give the model damping ratios and cubic-beziers,
   not "smooth". See `references/motion-math.md` and `references/motion-numbers.md`.
3. **Anchor to the real design.** Extract exact hex colours, radii, spacing and type scale from
   the screenshots or brand kit into tokens, and use only those tokens. Text-only briefs produce
   generic, lookalike videos.
4. **Avoid these amateur tells:** a giant centred headline with a muddy drop shadow, dated
   gradients, the same fade on every element, a logo fading to black at the end, low-contrast
   text over light panels.
5. **Structure the story in beats, and write what the viewer knows at each second.** "Zoom in, morph, add
   particles" is a list of activity, not a story. For 15 to 16s use HOOK (0-2s, one image that earns
   attention), PROBLEM (2-5s, the friction shown on screen), REVEAL (5-9s, the product enters through a real
   interaction), PROOF (9-13s, one screen or number backs the claim), CLOSE (13-16s, clean final state and a
   readable CTA). Every beat needs an entry state, an exit state and a reason to exist; if you cannot explain
   why shot four is there, cut it. Something new should reach the screen every 2 to 4 seconds. Write the
   storyboard as a timestamped list of elements and properties, not prose (`references/brief-templates.md`).
6. **Library animations must obey the clock.** Chart, graph and diagram libraries ship their own
   time-based animations and physics. Turn those off and drive their state from `t` yourself.
   Precompute force layouts with a fixed seed and tick count, then interpolate. Never let a library
   animate on wall-clock time inside a render. Some renderers can't be made frame-accurate at all
   (Cytoscape's canvas failed testing): keep the library for its maths and draw with SVG yourself.
   Prove it with `render.mjs --check`, then look at the stills. Passing the check doesn't mean
   the frames look right.
7. **Shape-morph pieces:** one element morphing through 8–12 UI states (button → loader → player
   → card…) is a strong format on its own. Define every state as data (size, radius, colour,
   content), and spring between neighbouring states on the beat grid.
8. **Numbers, not adjectives.** "Premium" becomes materials (roughness, clearcoat, hex), "cool"
   becomes lights (colour, intensity, position), "modern" becomes a camera (field of view, orbit,
   push-in curve), "animation" becomes beats and springs (BPM, anticipation frames, damping).
   Fill the directed prompt template in `references/brief-templates.md` section 5 before any code.
9. **One hero per shot.** Everything else waits, dims to 40%, or holds still. Secondary moves
   travel 50 to 70% as far as the hero and start 100 to 200 ms after it; ambient motion stays
   under 5% of the hero's travel. Exaggerate key poses 10 to 30%: the feed shrinks everything.
10. **Ban the defaults by name, then extend the list.** A general "no generic AI look" swaps one
    default for another. Put the exact patterns in BANNED (see the starter list in
    `brief-templates.md`), and after every first render add whatever the model used anyway.
11. **Render contract.** Expose `window.renderAt(t)`, support `?t=` to freeze a single frame (no
    requestAnimationFrame then), set `window.__ready` after fonts and bakes, pin library versions,
    and render loop frames 0 to N-1 only. Paste the full contract from `brief-templates.md`
    section 6 under every motion prompt; the starter's `stage()` already does this.
12. **Show, do not just name.** When the video lists capabilities, each one gets its own animation that
    demonstrates what it means (a spring overshooting and settling, a slider changing a curve, one shape morphing
    through states, tools connected to one clock), plus a short caption. Use real match cuts, not only wipes.
    A narrated story needs pauses in the voice so each visual lands (`references/narrated-ad.md`).
13. **One spring per retarget.** When a value changes target several times (a cursor, a container's width),
    stack springs instead of restarting one: `track(t) = v0 + sum (v_i - v_(i-1)) * spring(t - t_i)`
    (`Motion.springTrack`). It stays a pure function of `t`. Give each class of object its own rule: small UI
    snaps with minimal overshoot, panels settle, the camera glides almost invisibly, headlines land hard and
    hold long enough to read, mascots bounce on purpose. If everything overshoots, nothing feels precise.
14. **Formats come from one timeline, never a crop.** Vertical gets bigger type and fewer elements, square gets
    tighter holds, wide gets more spatial context.
15. **One motion personality per film.** Pick one archetype (Playful, Premium, Corporate, Energetic) and fix three
    constants in `style_guide.md`: a signature easing for about 80% of moves, a duration palette of three, one
    entrance pattern. Never opacity-only for an important state change; never let any move travel a third of the
    screen without a keyframe change; at most a third of the elements moving at once. Numbers and the full set of
    tables in `references/ui-motion.md`.
16. **Legibility floor.** Text at 4.5:1 contrast on every frame, never more than 3 flashes per
    second, and every text state held 0.3 s per word plus 0.5 s before it moves. Don't guess the theme per
    shot: measure the luminance under each text block every frame, flip ink/white, and add a soft scrim only on
    busy or mid-tone backgrounds (`legible()` in `starter/examples/three-studio.html`).
17. **Fidelity is proportions, objects, then colour.** One scale per set (desk 1 unit = 10 cm, room 20 cm) with
    props at real sizes; never a rounded box, capsule or sphere cluster standing in for a prop (build it from
    lathes, extrusions and tubes, or take it from `lib/studio3d.js`); no haze (no fog, bloom threshold 1.6, small
    aperture); bright sets at exposure about 0.8 and environment intensity about 0.5.
18. **Variety across the film.** Rotate backgrounds (lilac, white, cool grey, sky blue, cream, navy, charcoal) and
    grade each set to its own tint; keep the accent colour for type and hero props. Make about one shot in four
    flat 2D (giant kinetic type, a halftone scribble, a website-style layout, an end card) and add 2D arcs over 3D
    landings. No full-width lens streaks or ghosts: they read as a white line across the video.
19. **Explain a process by acting on one object,** not with a ring of labelled tiles and a moving dot. Each step
    does something visible to the same hero object, with the word placed under it.
20. **Draw the techniques, don't choose them.** Left alone, every film gets the same fade-up, push-in and end card.
    Run `python3 tools/cinetic/pick.py --format <launch|feature|loop|sting|walkthrough|vertical> --energy <calm|medium|high> --seconds <n>`
    and build the 273-entry library's picks the concept can carry; reroll a pick at most twice, write the seed in the
    shot list. Copy arrives as 1 to 4 word fragments with picture between them, never a sentence at once
    (`references/cinetic.md`).

## Step 4: Audio on the same clock

- Pick a tempo and put the motion on its grid. At 120 BPM there is one beat every 0.5s
  (30 frames at 60fps, 15 at 30fps). Key motion hits land on beats.
- Keep motion cues and sound cues in **one shared timing file** (JSON), so moving a transition
  moves its sound with it.
- Each sound hit **peaks 1 frame after** its picture event (light beats sound). The model cannot
  listen: score from frame numbers, then measure the decoded audio (first peak sample vs frame,
  hit level 3 to 6 dB over the bed, energy above 150 Hz so phone speakers play it). Compute each
  beat as `n * 60 / BPM` and round per beat, never by adding a rounded frame count.
- Mix to about -14 LUFS, peak under -1 dBTP after the AAC encode (limit the WAV to -2.2 dBTP). The
  AAC encode adds about 16 ms of padding that breaks a seamless loop; see
  `references/export-and-audio.md`.
- With a supplied track, measure it before animating: `node starter/tools/beats.mjs song.wav > beats.json`
  gives bpm, beats, downbeats and hits. State changes go on beats, big moments on downbeats, clicks and
  whooshes on hits. Blindfold test: if the audio has no shape without the picture, the sound design is
  unfinished.
- **You cannot hear.** Meter the finished film: `node starter/tools/audio-check.mjs film.mp4` (loudness, true peak,
  first sound, ending, dead air against the measured range of 7 pro launch films). For ears, use earshot
  (`references/sound.md`): `earshot critique`, `timeline`, `sheet` and `realness`. Never say how audio sounds, or that
  a sound "fits", without a reading behind it.
- Pro launch films: music leads, about -14 LUFS, first sound within 0.5 s, end at body level with a short fade or a
  designed sting, a few big accents instead of a hit on every cut, whoosh peaking on the cut, riser then stop-down
  then impact for the one big reveal, voice-over ducks the music 3 to 6 dB. Details in `references/sound.md`.
- Synthesized beeps and oscillator whooshes read cheap next to those films. Short UI sound effects (clicks,
  swooshes, bass drops) can be synthesized in code for a prototype (`motion-math.md`); for a premium result use
  real licensed recordings with a licence check (CC0, public domain, CC BY only) and let earshot's `real-sound`
  workflow pick, trim and verify them. See
  `references/motion-math.md`. For music or voiceover, use the `hyperframes-audio` skill.
- Captions for a voiceover: use word timestamps (WhisperX or `hyperframes transcribe`).

## Step 5: Set up the harness once, then reuse it

If the project lacks these, propose adding them:
- **House rules in CLAUDE.md / AGENTS.md:** fps, resolution, tempo, colour and type tokens, "no timers, pure
  render(t)", the spring presets, and the beat structure.
- **Folders:** `sources/` (client assets, read-only), `drafts/` (experiments), `published/` (approved renders).
- **Gates, in order.** The agent can work for hours between gates; a missing asset is a blocker, an unclear
  reference gets a question or one test frame before 900 polished wrong ones. Don't write polish code before
  gate 2.
  1. references and product assets approved
  2. style guide and shot list approved (user approves)
  3. stills for every shot, critiqued
  4. animatic at 960x540 with placeholder audio
  5. full pass, polish, sound
  6. formats, loop check, poster frame, README
- **Studio folder** so the next video starts from files, not a chat: `brief.md` (goal and product facts),
  `style_guide.md` (palette, type, motion, banned defaults), `shotlist.md` (beats, states, timestamps, purpose),
  `assets/` (approved logos, screens, sound), `src/` (seekable composition), `reviews/` (contact sheets and
  defect notes), `out/` (one export per format). One session per brand: the renderer, audio synth and export
  pipeline carry over to the next film. Wrap it in a skill or command ("a 20s vertical reel for [URL]").
- **Circuit breaker:** if the same render or compile error happens twice, stop, rethink (raise
  effort), and don't loop.
- **Load context on demand:** load only the style guide or component you're working on, not the
  whole codebase.
- **Definition of done:** the MP4 exists on disk, its duration is checked with ffprobe, the
  checkpoint frames pass review, and both aspect ratios are exported. For loops, the first and
  last frames also match.
- **Split the work by model strength.** Use the strongest model (Opus / top Codex model) for the
  storyboard, timing, art direction and frame critique. Hand bulk component code, chart setup
  and repetitive scenes to a faster model or subagent (Sonnet / a smaller Codex model) with a
  tight spec, then have the strong model review the result.
- **Keep the receipts.** Save every prompt and every follow-up in the project (`prompts/`), count
  the creative follow-ups (any note that changes how the piece looks or moves), and log technical
  fixes separately. Honest numbers (a 400-word first prompt, then 4 to 15 follow-ups) are the
  norm; real pieces took 2 to 4 review rounds. Effort: medium for small fixes and patches, xhigh for a new
  film, max when the first 3 seconds have to carry a launch (reports from viral pieces say the one-shots
  ran on xhigh or max). A chat app alone gives mid results: only an agent with a shell can render, listen to
  and look at its own frames.
- **"One prompt" is a myth.** Viral "one-shot" videos came from long, detailed briefs with
  examples, skills and hours of iteration. Save the finished brief as a file in the project so
  the next video reuses it.

## Step 6: The critique loop (most important)

Don't ship from the first render.
1. Render, then grab still frames at 4–6 checkpoints (one per beat, plus the final frame).
   Use `hyperframes snapshot` or `ffmpeg -ss <t> -frames:v 1`.
2. Look at each frame yourself (Read the PNGs) and score it against:
   - Text contrast and legibility. Is anything clipped or colliding?
   - Have the elements settled before the next headline or beat starts?
   - Does it match the design tokens and brand?
   - Is there any of the Step 3 tells?
   - Score polish from 1 to 10.
3. If the score is below 8, name the two worst defects, patch the code minimally, and re-render.
   Expect at least two passes. Send one or two notes per round: ten at once turns a fix into a rewrite.
4. Give every note a frame number and a number, not a feeling. "Frame 84 peaks late, move it 2
   frames earlier", not "make it pop". Translate feelings with the table in
   `references/motion-numbers.md`.
4b. Grade each defect by severity (CRITICAL, HIGH, MEDIUM; the tiers and a motion smell-to-fix table are in
   `references/ui-motion.md` section 11) and fix critical ones first. A flat-looking piece usually lacks secondary
   and ambient layers, follow-through or settle time.
5. Sharper views when stills are not enough: a **contact sheet** (`render.mjs --contact`, a
   storyboard of 12 frames), an **onion skin** (frames at 25% opacity: spacing should tighten near
   keys), a **speed graph** (position and scale per frame: straight lines are linear motion, sharp
   corners are dead starts), a **frame pair** (`--frames 83,85`) when a fix does not hold, and a
   **numeric audit** that reads the live scene on every frame and compares it with the numbers in
   the prompt (the voxel-mascot lab ran 71 checks, 6 failed on the first run).
6. Build the evidence with ffmpeg and judge only the rendered frames, ignoring what you meant to make:
   contact sheet at 2 frames per second (`--sheet`), a strip of 12 consecutive frames around the fastest move
   (`--strip <frame>`), phone-size frames at 360 px wide (`--phone`), the clip played twice (`--loopcheck`),
   and a determinism check (the same frame twice must hash the same). Score 1-10 on: hook in 2s, phone
   readability, motion, variety, sound sync, brand accuracy. List the 3 worst defects with timestamp,
   evidence and a local fix; patch those seconds, re-render them, repeat until every score is 8+. Hunt for:
   overlapping text, elements sliding where they should ease, corner labels, blurry scaled type, a dead
   beat with nothing happening, a stutter at the loop point. Skipping this loop because the first render
   feels like progress is the usual failure. Review the sound the same way: `audio-check.mjs`, and earshot's
   `critique` / `sheet` when installed (`references/sound.md`).
7. Check every transition frame by frame, and isolate each light or glint (render with it on and
   off and count changed pixels) rather than judging the whole frame.
7a. Measure speed, not feel: text being read moves at most 3 px per frame (at 60 fps), labelled chips under 20,
   ordinary moves under 25; anything over 12 gets real motion blur and nothing passes 60 to 80 except a
   frame-filling wipe. Check for pops (one or two unexplained frames), stalls, ghost frames, banding in dark
   gradients and a hook that moves less than half the film's median. For a ship decision use cinetic's
   11-dimension gate (every dimension 3+, finish and sync 5, mean 4.2+), in `references/cinetic.md`.
7b. With a visual reference, put your stills beside its contact sheet and judge like a designer: proportions,
   anything that reads as a box or blob, a palette that never changes, text lost on bright backgrounds, white
   streaks or haze. Tile stills with `xstack=...:grid=CxR`. Details in `references/3d-fidelity.md`.
8. Add each fix that worked to the render contract / house rules, and each default the model used
   anyway to BANNED.
9. Tell the user the scores and what you fixed, and show them the frames or the video.

## Export and loops

Loops render frames 0 to N-1 and run on `phase = frame / N` with whole-number cycles; frame 0 is a
finished composition. Export an MP4 (H.264 High, yuv420p, CRF 18, faststart), plus a one-palette
GIF if asked (24 fps, 1200 px wide, at most 350 frames, 5 frames at 40 ms then 1 at 50 ms to hold
exact 24 fps timing). Verify a loop by playing it three times back to back. Commands, X limits and
the sound-measurement loop are in `references/export-and-audio.md`.

## Step 7: Tell the user what to do

End every planning turn with a short, numbered **"Do this next"** list: what you need from them
(assets, approvals, decisions) and what you'll do. Keep it concrete, with no hype.

## Cost sense

Long agent runs are mostly cached context, so prompt caching matters more than the per-token
model price. A stronger model that needs fewer fix loops is often cheaper overall. Don't promise
the user specific dollar figures from social posts.

## If the video is for selling

If the user is making these for clients: pitch the outcome ("15-second demo of your core
workflow, 16:9 + 9:16"), not "AI video". Build one unprompted concept demo of a real product as a
portfolio piece. Fix the scope at one interaction, a fixed length, two formats, and two revisions.

## Reference files

- `references/brief-templates.md`: brief, storyboard, shape-morph, critique prompt, the directed
  prompt template, the render contract, follow-ups that work, and the failure-to-fix table.
- `references/motion-numbers.md`: easing, springs, durations, stagger, holds, hierarchy, camera,
  animation principles as frames, feeling-to-number translations.
- `references/motion-math.md`: deterministic loop, closed-form spring, beat grid, synthesized SFX.
- `references/export-and-audio.md`: loops, sound sync and loudness, AAC padding, MP4/GIF/X export.
- `references/data-viz-libraries.md`: chart and graph libraries for route E.
- Second source for the production-brief, reference, state-list and critic additions: "Opus 5.5 Motion
  Design: What the Viral One-Prompt Videos Are Hiding" by seeco (x.com/seeconvm/status/2106096193235259564).
- `references/ui-motion.md`: design-sense layer for UI and product motion (personality, four-act timing, material
  easing, choreography budgets, severity tiers, smells, reduced motion). From github.com/LottieFiles/motion-design-skill.
- `references/sound.md`: what pro launch films do with sound (measured ranges), foley and accent rules, how an
  agent hears (audio-check meter, earshot), real-recordings workflow and licences. From github.com/Leonxlnx/earshot.
- `references/3d-fidelity.md`: premium three.js look: matching a reference, real proportions, modelled props
  (`starter/lib/studio3d.js`), light and exposure, per-set grade and colour variety, mixing 2D shots, effects that
  hurt, auto-legible type, explaining a process, long-film workflow.
- `references/cinetic.md`: from github.com/Leonxlnx/cinetic (MIT): when to hand a film to cinetic, the vendored
  technique draw (`tools/cinetic/pick.py`, 273 techniques), concept lenses and story device, fragment copy grammar,
  calm and crisp pace profiles, named curves and springs, speed limits in px/f, sound placement, BT.709 and
  banding finish, the 11-dimension ship gate.
- `references/narrated-ad.md`: voice-first narrated ads and explainers: show every capability as animation,
  real match cuts, Google AI Studio TTS with pause tags, cues from the take, sidechain mix, image decode gotcha.
- Latest additions come from "Opus 5.5 Motion Lab" by @flxrnc (x.com/flxrnc/status/2105311836190978392).
