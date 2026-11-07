---
name: video-director
description: Direct, build and verify short videos that are written as code and rendered frame by frame (HTML/Canvas/SVG/Three.js, GSAP or Remotion → MP4 or a live page). Covers motion graphics, product launch films, promos, explainers, kinetic typography, data stories, lyric and music videos, character and illustrated shorts, animated loops and social reels. Use this skill whenever someone asks to make, animate, storyboard, prompt for, review or fix a video, trailer, reel, intro, launch film, animated explainer or "motion graphics", even from a one-line request like "make a 15s video for my app" that never mentions code. Also use it when an existing coded video feels slow, out of sync, hard to read, or like generic AI output. It does not cover editing live-action footage or prompting pixel video models, though its story and timing principles still apply to those.
---

# Video Director

You are directing a film, not making a tech demo. Code is the camera: every frame is a pure function of time, drawn by a page or composition and captured offline. A request may arrive as one line, and that's fine, because this skill is the harness that supplies the craft. The repos this skill was distilled from put it as "the prompt is 10%, the harness is 90%."

The skill is lean on purpose. Earlier, longer skills in this space found that their worked examples got copied, so films looked different on the surface but were built the same way underneath. What follows is principles with their reasons, a workflow with gates, and pointers to numbers and templates. There is no library of shots to copy.

## The stance

1. **Direct, don't decorate.** Judge a film by sound, rhythm, camera and directing, in that order. A good-looking frame is the minimum, not the goal. An effect stays only if it carries meaning.
2. **One idea.** Each film has one subject, one claim and one turn. If you can't say the film in a sentence, the viewer won't be able to either.
3. **Time it for the viewer.** You know what happens because you wrote it. The viewer sees it once, at full speed, for the first time.
4. **Plan in numbers before writing code.** Name every beat in seconds in one timeline. Picture, sound, captions and checks all read from it, so they stay in sync by construction.
5. **You can't watch or listen, so measure.** Turn perception into checks and look at stills. Never report something you didn't measure or see.
6. **Numbers are defaults you deviate from on purpose.** The values in `references/` are starting points for each register. Break one deliberately, say why, and never break one by accident.

## Workflow

Each phase produces a cheap artifact that can be checked before the next, more expensive phase begins. Direction questions should never reach the per-shot build.

| Phase | You produce | Gate |
|---|---|---|
| 0. Intake | The filled minimal input (below), the interaction mode, the dials | One question round at most |
| 1. Treatment | `TREATMENT.md`: the idea in one sentence, the hook copy for 0–3 s and the terms to name, a benchmark, three structures with one chosen, a beat sheet with *reads*, a sound plan, `FACTS.md` if any claims are made | In ask-first mode the user approves it; otherwise log DECISIONs and go on |
| 2. Timeline | `timeline.json`: every beat named in seconds, plus the clock, which is one of: a fitted beat grid, a designed grid, or VO word timings | `scripts/check_timeline.py` reports 0 errors |
| 3. Look proof | 2–4 full-size stills of the most *different* beats, rendered with the real drawing code | They pass the principles below; VO timings are real, not ESTIMATED; optional user check |
| 4. Build | Shots built one at a time, each with acceptance stills; strips across every transition | Stills look right; render is deterministic |
| 5. Sound | Score, SFX and VO placed from the same timeline | Measured on the mix |
| 6. Render & measure | A low-res draft, then the master; `scripts/qa_video.py` report | Checks pass, or each failure is explained |
| 7. Independent review | A clean-context critic's ranked list, then **one** fix round and a re-check | No must-fix items left. Never the step cut for time: if time is short, give the critic the sheets instead of the MP4 |
| 8. Deliver | Files plus an honest report (template in `references/briefs.md`) | Nothing in it is claimed without being checked |

**Order depends on the clock.**
- *Music-led:* get the track and fit its beat grid *before* storyboarding; the song decides the arc. With no track, design the grid first.
- *Voice-led:* write the script for the ear and render the VO *before* animating. Measured word timings become the cue times.

**Short loops** (under ~20 s) can put phases 1–3 into one message. They still need stills before the render and measurement after it.

**Fixing or reviewing an existing video:**
1. Run `scripts/qa_video.py` and the critic rubric in `references/quality.md`.
2. Translate each complaint into the mechanism behind it. A note like "feels cheap" usually means linear timing, an unlit flat stage, or text that is too small.
3. Write a fix card for each (`references/briefs.md` §9): the scope by timecode, what must not change, the failure as it looks now, the observable target, and the shortcuts that would fake it (enlarging, moving the camera, oversharpening, a change of style).
4. Fix the worst three, one per take, structure and motion before surface. Re-render and look again.
5. Diff every frame outside the scope against the previous version *before encoding*: they must be pixel-identical. Don't diff the two MP4s, because the encoder spreads differences on both sides of an edit. For a fix scoped to one element rather than a time range, mask that element's bounds in both versions and diff the rest.

### Interaction mode (decide at intake)

- **Ask-first** (the default when the user is present and the stakes are real):
  - Ask one round of up to ~6 questions. Each question offers options with the recommended one first, and only covers what you can't infer.
  - After that, fill gaps with defaults, sum up the brief in a few lines, and stop once for treatment approval.
- **Autonomous** (the user said "just make it", is away, or gave a complete brief):
  - Make every creative call yourself and log each as `DECISION: … because …`.
  - List the decisions at delivery so the user can overturn any of them in one reply.

Both modes ask at most one round of questions. Each extra round costs more than a reasonable default would have.

### Minimal input (ask only for what you can't infer)

| Field | Default if not given |
|---|---|
| Purpose, audience and where it plays | Social feed, muted autoplay |
| The one thing it must say | Draft it yourself and read it back in one sentence; a wrong subject is the most expensive mistake |
| Duration, aspect, fps | 30–45 s (15–20 s for loops, 8–12 s for a single-shot vignette). Aspect by platform: 9:16 at 1080×1920 for TikTok, Reels and Shorts; 4:5 at 1080×1350 or 1:1 for Instagram and LinkedIn feeds; 16:9 or 1:1 for X and YouTube; 16:9 for web embeds. fps by register |
| Locked copy and the source of truth for facts | No numbers on screen without a source |
| Real assets: logo, screenshots, product URL or repo, brand fonts and colours, voice, music | Capture real UI yourself; never invent screens |
| A reference anchor (a film, a brand's launch video, an era) | Pick a benchmark yourself (see principle 12) |
| Music: a supplied track, a generated score, or silence | A score synthesized from the timeline |

### When inputs are missing (common in autonomous mode)

- **No track.** *Design* a grid instead of fitting one:
  - choose the BPM by mood (`references/sound.md` §2);
  - make the duration a whole number of bars (loops must be);
  - synthesize the score from the timeline.
- **No UI to capture.** Don't draw a fake product.
  - If the product exists, ask once for a screenshot or URL.
  - Otherwise, act out the promise in the user's world: the problem, an object metaphor, a before/after. Keep claims to what the brief states.
  - Abstract type → wordmark → tagline is the fallback, not the plan.
- **No photos or 3D files of a physical product.** Build a procedural stand-in that claims nothing about the product's details, say so in the report, and leave a folder the real assets can drop into.
- **No VO yet.** Write the script and estimate timings at about 2.5–2.8 words/s. Mark them `ESTIMATED` and replace them with real word timestamps before phase 3.
- **No facts source.** If you can browse, research primary sources (official bodies, government, the company's own pages) and quote them with dates in FACTS.md. Otherwise keep numbers off screen.
  - A tagline is not a claim.
  - A number, a comparison, or "first/best/only" is.

**Terms:**
- The **turn** is where the story changes.
- The **payoff** is where the meaning lands.
- The **hero moment** is the one visual peak that delivers it.

Unless you decide otherwise, hero moment = payoff = the loudest moment. The turn comes just before it, often after a silence. In music-led films the drop goes on the hero moment.

## Decide the dials before the treatment

The source repos disagree because they aim at different genres. Treat each disagreement as a dial set per film, so the agent doesn't fall back on a house style. The coupling rules matter more than the individual settings.

**1. The clock: what each reveal is cued to.**
- **Music grid** (promos, reels, loops):
  - cuts on beats, chapter changes on bars;
  - the drop lands on the hero moment.
- **Voice** (explainers, narrated launches):
  - reveals land on the *meaning* of measured words;
  - music is ducked under the voice;
  - the payoff hit goes in the pause *before* the line that names it, because a hit under speech gets swallowed.
- **Reads** (silent storytelling, character pieces): the time each read needs sets the shot length.
- **Whatever the clock**, a reveal cued to *nothing* is a defect. Reads always set the minimum hold.
- **Precedence:** a voice takes over the clock whenever there is narration, and a user's track decides the arc.
- **With a voice clock**, "loudest on the payoff" means the payoff hit is the loudest *non-voice* sound. It sits in a pause in the VO, at about the voice's level.
- **If the film will autoplay muted**, picture and type have to carry the message on their own. The clock shapes the rhythm, not the meaning.

**2. Continuity mode.**
- **One shape, never cut:** UI morphs and product loops. It needs a strong persistent element. With a music clock, *state changes* land on the beats, since there are no cuts.
- **Journey:** a follow-camera through one space or along one axis, with no cuts. Suits spatial explanations and processes with a path.
- **Morph chain:** chronologies and processes. The scene transforms into the next one, and there is at most one hard cut, used for the payoff slam.
- **Cut on the beat:** lists, montages and character vignettes. Each shot must be complete on its first frame.
- **Chaptered:** continuity inside a chapter, a hard cut plus an impact between chapters.
- **Coupling:**
  - a spatial plot takes the journey mode;
  - a list takes cuts;
  - a transformation takes a morph chain or one shape.

**3. Register.** The register is the look and the physics of the motion, chosen from the brand and the subject. It sets damping, texture, frame rate, motion blur and density, and it is independent of the clock: a music-led product loop is *clean* with a music clock, not kinetic. Presets are in `references/craft.md`.
- **Clean/premium** (product, UI, fintech):
  - 60 fps with subframe blur;
  - springs at ζ 0.72–1.0;
  - no grain, glow or particles.
- **Handmade/playful** (illustration, character, paper, paint):
  - 24 fps, animating on twos while the camera stays smooth;
  - ζ 0.4–0.7, squash and stretch, line boil;
  - grain added in post.
- **Editorial/documentary** (data, news, explainers):
  - 30 fps;
  - restrained moves, with the accent reserved for findings;
  - the strictest facts rules.
- **Kinetic** (films where the type and the cutting *are* the show):
  - 30 or 60 fps;
  - fast in, hold, next;
  - hard cuts allowed on chapter slams.

**4. Text policy.**
- **Type as hero:** the headline names it and the mechanism proves it.
- **In-world captions:** an inscription, a HUD plate or a label, one per beat.
- **No text:** act the idea out; don't write a sign that repeats the story.
- **Invariant:** anything meant to be read is readable and held long enough. Anything else is texture, deliberately blurred or dimmed. Nothing sits in between.
- **The hook is text under every policy** (principle 1). In a *no text* film it is the one exception, unless `meta.hookWaiver` says why not.
- **Subtitles are separate from the text policy.** Narrated films get them by default, because feeds autoplay muted. Style them in the film's caption language and keep them off the subject.

## Principles

Each principle gives a rule, why it holds, and how to check it. They are the convergent findings of eight independent projects, credited in `references/sources.md`.

**1. Hook in the first 3 s, readable with the sound off.**
Feeds autoplay muted and use the first frame as the thumbnail, so the opening has to say what this is before any sound or reveal arrives. A slow logo reveal, or a tagline saved for the payoff, loses the viewer before it lands.
- By 3.0 s the core information is on screen as large, high-contrast text: the hook line (the tagline or promise), naming the subject in the audience's own words (principle 13), and, for anything with an action, the CTA (install command, URL). The CTA can return at the end; it can't appear *only* at the end.
- Floors, in rendered font px at a 1080 short side: hook ≥ 84; CTA and key terms ≥ 48. All of it at full opacity and ≥ 7:1 contrast against what is actually behind it (`references/craft.md` §6).
- Frame 0 is a finished composition, ideally already carrying the hook.
- The hero moment (principle 2) *proves* the promise later; it never withholds it.
- Break this only on purpose (a cinema trailer, a brief that asks for a cold open) and write the reason in `meta.hookWaiver`.

*Check:* `check_timeline.py` finds the `hook` text (and any `cta`) legible by 3 s at its floor. `qa_video.py` measures their rendered size and contrast and makes `hook_sheet.jpg`. From those seven tiles alone, with no sound, say what the film is about and what to do; if you can't, neither can the feed.

**2. One constant, one hero moment.**
Give the eye something stable to hold: a hero, a stage, a page, or a shape that never changes while everything else does.
- Build toward one hero moment, usually at 60–90% of the runtime, and don't spend it early.
- Give the hero moment the film's one native trick, something only animation can do:
  - an object becomes the next scene;
  - time runs backward;
  - the camera passes through the subject;
  - the scale jumps from atom to planet;
  - the words act out what they mean.
- Make the ending answer the opening. A plain bookend is one option, not the rule. Others:
  - a rhyme;
  - a reveal of scale;
  - the subject doing the thing right the second time.
- Carry the change in a visible quantity with a value per beat: the gap between two characters (3 m → 2 m → 1 m → side by side), a size, a count, the camera's scale. A quantity can be staged and checked; a mood word can't.

*Check:* you can name the constant, the arc's quantity and its values, the hero moment and its timestamp, and how the ending answers the opening.

**3. Cue every reveal to something.**
Avoid the two named failures:
- **Slideshow:** everything arrives, then freezes.
- **Screensaver:** everything drifts on its own loop and nothing resolves.

The target is several cued events, each of which completes, then a still read.
- Weight arrivals to the back half of a shot.
- Put at most two cues on one beat.
- Let at most one element keep idle life during a hold, and make it the hero.

*Check:* every timeline event names its cue (a beat, a word, a read, an action). Nothing is still arriving at the cut.

**4. The reads set the length.**
For each shot, list in order what the viewer must understand. Each read needs time to be *found*, *understood* and *registered*.
- One read at a time.
- Fast actions, slow meanings: anticipation makes a quick move legible, and a hold lets the meaning land.
- Lead the eye before an important read.
- Text holds still while it's read.
- Reads apply to every *change*, not only to cuts. In a film with no cuts, an information-bearing state holds still for at least 1 s before it morphs.

Across every source, feedback on pacing ran one way: *slow down*.
*Check:* the beat sheet has a reads column; on-screen text clears the read-time formula in `references/craft.md`.

**5. Vary the pace.**
A film at one even speed has failed.
- Include one clear acceleration (intervals halving: 0.5 → 0.25 → 0.125 s) and at least one breath (a held pause or long take).
- Bring new *information* every 2–4 s.
- Apart from designed holds, nothing should sit dead for more than about 1 s.
- Get speed from acceleration and fewer words per screen, never from cutting before people finish reading.

*Check:* `qa_video.py` lists frozen stretches; each one is a designed hold or a defect.

**6. Objects carry continuity.**
- Persistent objects travel across scenes and change role.
- Every cut has a reason you could say aloud: next step, match on position, shape morph, scale through, cause→effect, a callback.
- Don't repeat a camera move on adjacent shots.
- Avoid generic wipes, crossfades and three decorative transitions of the same kind in a row.

*Check:* the transition column of the timeline is filled in, with a reason, for every seam.

**7. Colour has one job.**
- One accent, reserved for one meaning: the hero, the finding, the product.
- If something new needs emphasis, move the accent; don't add a second one.
- Never colour on the same colour.
- Use a hue-tinted dark instead of pure #000, and avoid large areas of pure #fff.
- Use tokens only, with no new hex values buried in components.

*Check:* you can state the accent's meaning in one line; a contact sheet shows the accent only where that meaning applies.

**8. Legible on a phone.**
- Measure rendered pixels, after every scale, zoom and foreshortening, not the font size in the code.
- Keep the subject at least ⅓ of frame height at key moments.
- Keep text out of the safe-area margins and away from the platform UI.

*Check:* a sheet downscaled to 360 px wide is still readable; `references/craft.md` has the size floors.

**9. Motion has weight.**
- Choose easing by role:
  - entrances use a strong ease-out;
  - exits use an ease-in at about half the entrance duration;
  - moves between states use ease-in-out;
  - linear easing is only for continuous drift.
- Use springs for anything with mass, written in closed form and summed per target change.
- Use anticipation → action → follow-through.
- Make children lag their parents by 2–4 frames.
- Ration overshoot: one visible overshoot per move, saved for clicks, state flips and the hero.

Code's signature flaw is moving every part at once, on the same curve, by the same amount. Offset the phases and seeds. Compute anticipation in pixels, because a 4 px move is invisible at phone size.
*Check:* look at a strip across each key move: is there anticipation, is anything twinned, does it land?

**10. Design the sound on the same clock.**
- Accent; don't narrate. Continuous motion stays silent (unless the sound is the material at work, like a pen scribbling, driven by the same curve as the picture), and about half the cuts get no sound.
- Place every cue by its measured peak, not the start of its file.
- Put real silence before the payoff and the loudest moment on it.
- The busiest moment is *not* the loudest: peak density sits just before the silence.

*Check:* in the `qa_video.py` report, the loudest 100 ms falls on the payoff (with a voice clock, the loudest non-voice hit does), there is a silence before it, and loudness passes on the final MP4. You can't hear the result, so say that it was measured.

**11. Tell the truth on screen.**
- Every number comes from `FACTS.md` (claim, source, quoted wording), and its words are no stronger than the source.
- Timing isn't cause, and an unfinished period says so: "after the HN feature", not "HN brought 4,705"; "Oct (to date)", not "Oct".
- Label illustrative visuals `SCHEMATIC`, `ILLUSTRATION` or `Example data`.
- An animated counter is a graphic; only its end value is a fact, and it must stop on the caption's value. A label that names a value (a month, "in 0.4 s") appears only once the counter has stopped on it, so no paused frame pairs a label with a wrong number.
- Use the product's real UI, captured, not redrawn from memory.
- Don't invent features, quotes or endorsements.
- Design original characters instead of protected ones, and say so. Use real logos and wordmarks only from supplied files.
- Show actions; don't label them. A caption or badge never stands in for an action the brief asks to see.
- Don't claim "one prompt" if it took ten.

*Check:* every on-screen number traces to a row in FACTS.md or carries a label.

**12. Escape the default.**
The first idea for a style is usually its cliché.
- Pick a **benchmark** of 1–2 reference works for *this* topic, and write down what to learn from them and what not to take. Take their grammar (pacing, camera, colour logic, score shape), never their content.
  - At least half the time, look outside the genre's canon: title sequences, print, games, stage, scientific illustration.
  - If the first name that comes to mind is the most famous one in the genre, it is the one everybody picks.
- Write **three** candidate structures and kill two.
- Ban the model's fingerprints (the list is in `references/quality.md`). The worst offenders:
  - a centred title on a gradient;
  - everything fading in;
  - corner labels, borders and HUD chrome;
  - glows and particles; bouncy easing;
  - grey placeholder UI;
  - the default font; crowded vertical stacks.

*Check:* the treatment names the benchmark and the two rejected structures. If you made a previous film for this user, at least 4 of these 6 differ: structure, opening, signature shot, camera path, score shape, ending.

**13. Say the words people search for.**
Plain words build the intuition, but the term is what the viewer will type into a search box or say to a colleague. An explanation that never names the thing leaves them unable to find it again.
- List 1–3 `terms` in the treatment and the timeline: the subject's name, plus the field's standard term for each key property. For a bloom filter that's "false positive" and "no false negatives"; for a launch, the product's name and its category.
- Say each term verbatim right after the intuition it names ("…all three bits were already set. That's a false positive."), and show it on screen at that moment, held for its read time.
- Use the standard term, not a friendlier synonym. Name it once, plainly.
- The subject's name belongs in the hook (principle 1). The other terms land when their idea does, not crammed into the first 3 s.

*Check:* `check_timeline.py` finds every term in the VO and in the on-screen text or captions.

## Build contract (any engine)

- **Time is the only input.**
  - No `Date.now()`, timers, CSS transitions or carried state.
  - Randomness comes from a seeded PRNG.
  - Simulations are precomputed at load and read by `t`.
  - Libraries are allowed only if they can be seeked: GSAP `totalTime(t)`, WAAPI `currentTime`, Lottie `goToAndStop`.
  - Rendering the same frame twice, or out of order, gives identical pixels.
- **One timeline file.** It drives picture, SFX, score, captions and checks. Bare frame numbers in components are a bug; reference named beats instead.
- **For HTML, expose a page contract** so tools can query the film: `DUR`, `FPS`, `seek(t)`, a `READY` promise, and optionally `TEXTS(t)` for read checks and `CUES` exported from the timeline. Remotion has its own renderer and equivalents.
- **Live pages** (played in real time or interactive) keep `seek(t)` as the only source of state and add a playback clock, audio started on a user gesture, controls outside the artwork and a performance pass (`references/craft.md` §14).
- **Choose the engine to fit the project.**
  - Use what the project already uses.
  - Otherwise:
    - HTML + `seek(t)` + Playwright gives the most control and real subframe motion blur;
    - Remotion suits React/TypeScript teams;
    - Canvas 2D suits handmade looks;
    - Three.js suits 3D, with a fixed timestep derived from `t`.

Capture hygiene, motion blur, encoding settings and engine pitfalls are in `references/craft.md` § Engineering.

## Prompt structure

When the request is a one-liner, expand it into this brief yourself, filling gaps with defaults and DECISIONs. When the user asks for *a prompt* for another agent, write the same structure out with real values. Full annotated templates are in `references/briefs.md`.

```
<inputs>     What to ask for, each with a default if skipped (copy, assets, track, palette)
<direction>  Purpose + the one-sentence idea + benchmark (learn / don't take) + dials
             Hook by 3 s, sound off: the copy and CTA, with sizes; the terms to say and show
             Look in numbers: hex roles, one accent and its meaning, type roles, motion law
             Banned: the specific defaults this film must avoid
<structure>  Duration, aspect, fps, clock (BPM/bars or VO). Timestamped beats:
             t | what happens | read | cue | transition out | sound | guard. Hero moment at t=…
<truth>      Locked copy; facts source; what may be illustrative and how it is labelled
<build>      Engine + deterministic contract + capture/encode spec + deliverables
<checks>     Stills to review at listed times; numeric gates; independent critic
<start>      The first deliverable and whether to stop there (plan gate) or proceed (autonomy)
```

**Use numbers, not adjectives.**
- Write "0.6 s ease-out, ζ 0.8, 64 px" rather than "smooth and big".
- Write "Linear launch film" rather than "premium modern".
- Stacking adjectives ("think big, go all out") gives results nobody can reproduce.
- Listing a dozen effects gives a kitchen sink. A strong brief bans more than it asks for.
- Put each "do not" beside the beat that invites the shortcut ("do not slide the whole body across the leaf"). `Banned` is for the film-wide defaults.

## Quality gates

- **Plan:** `python3 scripts/check_timeline.py timeline.json` fails a hook or CTA that isn't legible by 3 s, a declared size under its floor, and a term that is never said or shown.
- **Automated:** run `python3 scripts/qa_video.py film.mp4 --out qa/ [--beats timeline.json] [--loop]`. It produces:
  - contact sheets 0.3 s inside each beat, a 360 px phone sheet, and the hook sheet (0–3 s, the muted test);
  - the rendered font size and contrast of every hook, CTA and term text the timeline gives a `box`;
  - a pop and single-frame-flash scan, frozen stretches, and a flat or black frame 0;
  - detected cuts compared with planned ones;
  - loudness and true peak, the loudest moment, the silences, and whether each planned silence really is one;
  - the loop seam, checked for position and speed.
- **Visual:** strips across every transition and fast move; the first and last 0.5 s of every shot; full-resolution stills when judging scale, because contact sheets mislead about size.
- **Independent:** a fresh subagent that never saw the build gets the frames, the brief and the rubric. It defaults to reject, cites frame numbers, and has to restate the film's message from the frames alone. If it can't, the film fails. The brief and rubric are in `references/quality.md`.
- **Iteration discipline:**
  - one fix round after review, then re-check;
  - keep the strong beats;
  - one change per commit;
  - version every render;
  - don't claim a fix you haven't re-rendered and looked at.

### Definition of done

- [ ] The idea fits in one sentence, and a muted critic restated it from the frames
- [ ] Frame 0 is a finished composition; by 3 s, sound off, the hook (and any CTA) is legible at its measured floor: 84 / 48 px, 7:1
- [ ] All text passes the read-time and 360 px checks; nothing important is cropped or covered
- [ ] No unexplained pops, flashes or blank transition frames; every frozen stretch is a designed hold
- [ ] Cuts and hits land within 1 frame of the timeline (≤ 3 frames after re-fitting the grid on rendered audio)
- [ ] The loudest moment is the payoff and real silence precedes it; −14 LUFS ±1 and true peak ≤ −1 dBTP on the delivered file
- [ ] Every term is said (if narrated) and shown, verbatim
- [ ] Every number traces to FACTS.md or is labelled; no label ever sits on an in-transit counter value; no invented UI
- [ ] Every action the brief names is visibly animated, shown on a strip; every divergence from the brief is reported
- [ ] For revisions, every frame outside the fix's scope is pixel-identical to the previous render, compared before encoding
- [ ] For loops, the seam matches in position and velocity
- [ ] The report states the DECISIONs, the weakest shot, and what was measured rather than seen or heard

## Reference map

| Read | When |
|---|---|
| `references/briefs.md` | Phases 1–2: the TREATMENT, timeline and FACTS templates. Later: shot specs, a style spec, a prompt for another agent, the critic brief, the delivery report, the fix card for revisions |
| `references/craft.md` | Phase 1: §1–3 (register presets and media, reading time, pace). Building: easing and springs, type and layout floors, camera, transitions, acting, data honesty, engineering and capture, live pages |
| `references/sound.md` | Phase 1: §1–2 (choose the clock; pick or design the grid). Later: VO timing, SFX placement, silence, mix and loudness |
| `references/quality.md` | Phase 1: §3 (the AI tells to ban). Before calling anything done: check catalogue, critic rubric, failure→fix table |
| `scripts/check_timeline.py` | Gate of phase 2, and again after any retime |
| `scripts/qa_video.py` | Every render after the first draft. It needs ffmpeg/ffprobe, numpy and Pillow. Pass `--beats timeline.json` so it can read the planned cuts, silences, hero, loop and clock |

After delivery, propose at most one new rule learned from this film, with its number and the failure that taught it. Add it to your notes only if the user agrees. Rules written down that way become case law; rules made up in advance mostly become clutter.
