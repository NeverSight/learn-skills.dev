---
name: demo-director
description: Directs and builds product demo videos (walkthroughs of a real-looking app and motion-design pieces that are not a walkthrough) as frame-accurate, scripted films rendered from code with Playwright and ffmpeg. Use when someone asks to make a demo video, product walkthrough, launch or promo film, social clip, explainer, app-screen recreation, motion design, or "a video of the product", including when they want a storyboard first. Plans the film beat by beat for approval, then builds it. Covers app-screen fidelity, camera and cursor motion, easing and transitions, captions, honest claims, and a frame-by-frame review.
license: MIT
compatibility: Needs Node 18+, Playwright, and ffmpeg to render. The plan-stage storyboard needs Node only.
metadata:
  author: precious112
  version: "0.1.0"
  opencode/slash: "true"
---

# demo-director

A viewer decides in about two seconds whether a demo shows a real product or a
generated mood piece. This skill is how to make the first one, twice over:

- **A walkthrough.** The product's own screen, simulated faithfully, used the way
  a person uses it. Camera and cursor do the explaining. Use this when the value
  is visible in the product working.
- **A motion-design piece.** The product appears, but the film is composed: type,
  rhythm, transitions and shape carry it. Use this when there is little app to
  walk through (a skill, a library, a launch), or when the story needs a shape a
  walkthrough cannot give it.
- **A hybrid.** A designed frame around a real, faithful app screen. Most good
  launch films are this.

And it plans before it builds: a storyboard you can approve, skip, or change.

The rules that stop a film looking AI-made are the same in every mode, so read
them once, properly. Most of them are in this file; the detail is in
`references/`.

## The order of work

1. **Intake.** Establish what the film must move, for whom, in what format, how
   long, and what the real product actually does. Ask only what you cannot find.
2. **Choose a mode** (below) and say which you chose and why.
3. **Plan the beats as a storyboard** and, unless the owner says to skip it, wait
   for approval. This is plan mode.
4. **Build** the stage, the script and the captions.
5. **Review frames**, then motion, then copy. Fix and re-render.
6. **Deliver** the master, the cutdowns and the stills, and say where they are.

## Choose the mode, then say so

| The value is… | Mode | What carries it |
|---|---|---|
| A workflow the viewer can watch happen | **Walkthrough** | The real UI, in the real order, with the camera and cursor as the guide |
| An idea, a skill, a launch, or the product's taste | **Motion design** | Composition, typography, rhythm, transitions: the product shown, not toured |
| Both: a designed frame around a working screen | **Hybrid** | A composed ground with the product's real screen inside it |

Ask one question when it is genuinely ambiguous: *"Is the point that the product
works, or that the product is good?"* Working is a walkthrough. Good is motion
design. If the product has almost no interface to show, it is motion design by
default, however much the request says "demo".

**A motion-design film is not a walkthrough with fancier cards.** In a
walkthrough, every second must be a real action in the real UI. In a motion-design
film, you are allowed to compose, cut on beats, use type as the image, and hold a
frame for its own sake, but you are not allowed the slop in this file. The
fastest way to make a motion-design film look cheap is to decorate a walkthrough.
The fastest way to make a walkthrough boring is to compose it like an ad.

## Plan mode: the storyboard comes first

Unless the owner says otherwise, **write the plan and get approval before you
render a frame.** A rendered film is expensive to change; a plan is cheap.

1. Write `plan.json` following `references/storyboard.md`.
2. Build the review page: `node scripts/build-storyboard.mjs plan.json`.
3. Put the stills you will frame on into it as you go, so the owner sees the real
   app, not boxes.
4. Open it, and in your reply give: the one idea, the mode, the runtime, the
   formats, and the two or three decisions you want made. Do not repeat the whole
   plan in chat.
5. **Stop and wait** for the answer.

The gate is real, and so is the escape hatch:

- If the owner approves, or amends, build it.
- If the owner says to skip the review, or asks for speed, **offer to build a
  preview anyway**: render 8 to 12 stills at the key beats first (seconds, not
  minutes), show them, then render the film. Say plainly that you skipped the
  plan and that changes will cost a re-render.
- Never render a full master before the plan is settled unless you were told to.

A plan is not prose in chat. It is the storyboard file plus a short reply.

## The non-negotiables

These hold in both modes. The full list, with the reasoning, is split across the
references. Read the ones your film needs.

**Inside the app frame, fidelity is the only rule.** A recreated screen must be
the product's real screen: real components where you can mount them, real strings
copied from source, real density (12 to 14px text, 1px borders, 6 to 8px radii), real
states, real latency, the real platform window if a window is shown. Never scale
UI up for "readability". Make it readable with the camera. Never invent a
cleaner, emptier app. See `references/fidelity.md`.

**Outside the app frame, the product's identity and nothing generic.** Build
everything from the product's own tokens, type and shapes. In a walkthrough that
means a flat ground and captions that only fade. In motion design, type may be the
image and the ground may be designed, as long as the motion comes from the meaning
(a word that becomes the interface, a line revealed in reading order), not applied
to the sentence. Never glows, gradient blobs, floating feature cards, per-letter
cascades, emoji or sparkles. See `references/motion-design.md`.

**The camera is one steady operator.** One move at a time, 1.0 to 1.6s on a soft
ease-in-out, with a slight pull-back on long trips. Linger before each move, but
time spent acting in the shot counts. When the camera goes somewhere so the viewer
can see something, the cursor goes to that exact thing. Open on the product, not a
black title card. No bounce, no shake, no drift during an action, no 3D tilt inside
a screenshot. See `references/camera.md`.

**Say what happens on screen.** Plain, specific, short captions in the viewer's
terms. No banned words (supercharge, unleash, seamless, effortless, empower…),
no unmeasured numbers, no invented testimonials. The product is the only brand
the film names. See `references/copy.md`.

**Everything shown is real.** A scripted simulation may remove errors and waiting,
never add capability. Compressing time is honest when it is visible. If a beat
needs the product to do something it cannot, cut the beat. See `references/direction.md`.

## Build with the render kit

Films are rendered frame by frame from a stage page, so every frame is exact and
repeatable. The engine is `scripts/engine.mjs`; the stage shell is `assets/stage/`;
a complete walkthrough example is `assets/examples/walkthrough/`.

```bash
# a walkthrough stage: the shell around your product's world
node assets/examples/walkthrough/film.mjs phone preview      # stills only, fast
node assets/examples/walkthrough/film.mjs phone final        # 2x master + mp4
node assets/examples/walkthrough/film.mjs wide final         # a second format, one script
```

Two modes, one engine:

- `mode: "film"`: the stage exposes `window.__stage.set({camera, cursor, caption,
  card})` and your script drives camera moves, cursor travel, clicks and typing.
  Use this for walkthroughs. See `references/camera.md`.
- `mode: "timeline"`: the stage exposes `window.seek(t)` and `window.DURATION`
  and the engine samples every frame. Use this for self-contained motion design.
  See `references/rendering.md`.

Scaffold a project with `node scripts/new-project.mjs ./films/my-film "My film"`:
it copies the stage shell and the tools in, and writes a starter `film.mjs` and
`package.json`.

**A film must never bloat the product's repository.** The scaffolder adds the
film's top-level folder (`films/`) to the repo's `.gitignore` and gives each film
its own `.gitignore` for `renders/`, `node_modules/` and video. Tell the owner
where the film lives and that git ignores it. Use `--track` only if the owner asks
to keep the plan and script in git; renders stay ignored either way. If you set a
film up without the scaffolder, do the same by hand before you render anything,
and never `git add` a film folder or a video. Then write `world.html`, `world.css`, `world.js`. Do not edit the
shell per film. Render at 2x device scale so a zoom stays crisp; encode H.264,
`yuv420p`, CRF 12 to 14, `+faststart`.

## Review before you call it done

Render stills at a fixed interval and look at every one at full size; then watch
the film at 1x and at 0.25x around every move. The checklist and the exact
questions are in `references/review.md`. At minimum:

1. Could each frame be a real screenshot of the product?
2. Is there one thing to look at, and is it framed?
3. Does any text overlap something it should not, in any frame of a move?
4. Is anything glowing, floating, tilted or gradient-filled?
5. Does any caption use a banned word, an unmeasured number, or an emoji?
6. Would the audience reproduce what they saw and find the product does it?

Anything that makes you wince is a finding, even if no rule names it. Fix it, then
add the rule here.

## Files

- `references/modes.md`: choosing and mixing the three modes; what each may and may not do.
- `references/direction.md`: the one idea, structure, hook, runtime and formats, honesty.
- `references/storyboard.md`: `plan.json`, the builder, the approval gate and the escape hatch.
- `references/fidelity.md`: inside the app frame: real UI, real content, real states.
- `references/camera.md`: camera, cursor, typing, the stage contract for `mode: "film"`.
- `references/motion-design.md`: type, rhythm, transitions, choreography, backgrounds.
- `references/copy.md`: captions and on-screen words, with the banned list.
- `references/rendering.md`: the engine, the stage contract, formats, encoding, contact sheets.
- `references/review.md`: the frame, motion and copy checklists, and accessibility.
- `references/research.md`: the sources the rules come from.
- `scripts/engine.mjs`: the renderer.
- `scripts/new-project.mjs`: scaffold a film project with the shell and tools.
- `scripts/build-storyboard.mjs`: plan → review page.
- `scripts/check-copy.mjs`: the caption checker.
- `scripts/contact-sheet.mjs`, `scripts/to-gif.mjs`: review and delivery helpers.
- `assets/stage/`: the stage shell you copy into a project.
- `assets/examples/walkthrough/`: a full walkthrough: plan, storyboard, world, film.
- `assets/examples/code-slowmo/`: a full motion-design film: stage, script, storyboard.
- `assets/examples/caret/`: a real launch campaign, as a case study.
