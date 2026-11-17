---
name: make-motion
description: Use when someone wants a motion graphics video of their product (a launch video, feature demo, teaser or explainer), such as "make a launch video for this", "/make-motion" or "roast my video idea". It roasts the idea, scripts it in beats, builds it in Remotion in their design system with music made in code, checks it by measurement, and delivers an MP4. Not for editing footage.
metadata:
  summary: Makes a motion graphics video
---

# Make motion

The person brings an idea: a product, a feature, a launch. This skill turns it into a 15 to 25 second motion
graphics video, for X by default, that a stranger understands with the sound off, and that looks made by hand. It runs the whole loop by itself unless
the person asks to approve each stage (`step`).

| You say | It does |
|-|-|
| `/make-motion <idea>` | the whole loop, one shot |
| `/make-motion step <idea>` | stops for a yes after the script, the stills and the review cut |
| `/make-motion roast <idea>` | step 2 only: the roasted pitch and three hooks |
| `/make-motion theme <source>` | step 3 only: resolves and checks a theme |

## Before anything

Say this once, plainly: "This builds in Remotion. It is free for individuals and companies of up to 3 people; a
larger company needs a Remotion company licence (remotion.dev/license)." Then carry on. Never decide for them.

Needs Node 22.6 or later, about 400 MB for Remotion and its headless Chrome (downloaded on first render), and ffmpeg
for the contact sheet, the jump and energy checks and the X export. A one-shot run of a 20 s video takes about two
hours of agent time, most of it renders and review passes; say so up front.

Start from `template/`: copy it to the person's chosen folder (default `video/`), `npm install`, and render the
example once (`npm run stills example`) to prove the setup before writing anything. Then make the video in its own
folder under `src/` and delete the example. `references/pipeline.md` has every command.

## Steps

1. **Ask once.** In one message: what the product does in a sentence, who watches, what can be shown (screenshots,
   a URL, the repo, real numbers), a theme source if they have one, and anything that must be on screen. Take
   defaults for the rest and say which: 5:4 at 1350x1080, 60 fps, about 20 s, `punchy`. The look comes from the
   product's own brand (its site, its tokens); design.how's look is only for a person with no brand at all.
   Done when the idea, the material and the defaults are written down.

2. **Roast the pitch.** Run `references/story.md`, "The pitch roast", on the idea as given. Write the one-sentence
   story, three hooks, the pick and why, the signature move, and what was cut. The roast is the person's to see
   even in one-shot: show it in a few lines before building, then build on it.
   Done when the story is one sentence a stranger would get, and every scene is tied to it.

3. **Theme.** Resolve the theme from its source (`references/theme.md`; for a site,
   `npm run theme -- <url> --out src/<name>/theme.json` writes a draft). Decide every role, fill the
   derived ones, run the contrast check, load the fonts, and warn on any font whose licence is commercial or unknown.
   Done when every text role passes contrast on every ground it lands on.

4. **Script in beats.** Write `SCRIPT.md` (scenes, every word on screen, sound) and `timing.ts` (every moment as a
   beat number turned into frames). Use `references/story.md`, "Script", and `references/motion.md`, "Energy", for
   each scene: name its three things alive, its scale change and where the camera goes. Name the review stills in
   `STILLS`, the planned hard cuts in `CUTS` and any designed one-frame steps in `STEPS`.
   Done when SCRIPT.md and timing.ts agree and the length is within 2 s of the target.

5. **Stills.** Build each scene as a frame of the real composition and render the stills
   (`references/pipeline.md`). Look at every still yourself against the motion slop list in `references/motion.md`:
   real content, not placeholder bars; the subject filling the frame; UI text 22 px or more; nothing decorative.
   In `step`, stop here for a yes.
   Done when each still holds up on its own as a poster.

6. **Motion.** Animate with `src/kit/`. Every value a pure function of the frame. Render a silent review cut at scale
   1 (`npm run review <id>`), then `npm run jumps <id>` and `npm run energy <id>`. Fix every unplanned jump and every
   scene under the energy bar before anyone sees it.
   Done when both exit 0 and the contact sheet reads as the story, busy in every row.

7. **Roast the cut.** Run the review passes in `references/review.md`: fresh agents, one per area, with the saved
   briefs. Measured findings are fixed; taste findings are weighed against the one-sentence story. Two passes, the
   second on a new review cut of the fixed video. If pass two changes anything, render the review cut once more and
   rerun jumps and energy: the master is never the first render of a fix. In `step`, put the findings to the person.
   Done when the second pass finds nothing above "minor" and the last review cut passes jumps and energy.

8. **Music last.** Write `audio/cues.mjs` from `timing.ts` (the key, tempo and preset live there, nowhere else), then
   `npm run audio src/<name>` and `npm run audio:check src/<name>` (`references/sound.md`). Nobody can listen, so
   say that the sound is checked by measurement only, and give the numbers.
   Done when `audio:check` exits 0, and again with `-- --mp4 out/<id>/master.mp4` on the master.

9. **Final and hand-off.** Render the master at scale 2, mux the audio, make the 1350x1080 X cut and a thumbnail
   (`references/pipeline.md`). Tell the person: the file paths, the length, the one-sentence story, what the roasts
   changed, the measured audio numbers, and anything not verified.

## Rules

- Open on the product, busy from frame 0. Never a title card first.
- Every screen reads at a glance to a stranger: familiar UI doing one obvious thing, the outcome and not the
  machinery. No process diagrams, no internal steps, no tool vocabulary on screen.
- More going on, not less: three things alive in every scene, moves that overlap, a camera that works, one change of
  scale per scene, the subject filling the frame (`references/motion.md`, "Energy"). The energy check measures it.
- Every scene is new. Shared code is the kit (curves, blur, whips, captions, theme), never a previous video's scenes.
- Captions are one line per beat in plain words, no punctuation, no exclamation marks.
- One accent, used for what matters (a measurement, a highlight, the product's name). Everything else is ink on paper
  or paper on ink.
- Real numbers where they exist. Invented data never looks like a real company, person or secret.
- Anything decided per frame (which face, which digit, which letter typed) is picked on the whole frame, floored
  (`whole()` in the kit), so blur samples agree.
- Measure layout once, flat, after `document.fonts.ready`, before any camera transform.
- Sound effects are in the music's key. The mix is mastered to -14 LUFS.

## Never

- Call a check passed that did not run in this session. Not run is "not run".
- Claim the music sounds good. Report what was measured.
- Put a brand, company or font name on screen that isn't the person's own.
- Use AI-slop looks: purple-to-indigo gradients, gradient text, glassmorphism over gradients, sparkle emoji, icon
  tiles, a soft shadow on every card, centred hero copy, "seamlessly". Nor the motion slop in `references/motion.md`:
  placeholder bars, decorative frame lines, UI shrunk into half the frame, a static end card.
- Draw or imitate a company's logo, even for a spec video. Its name in plain text in an open font is the limit.
- Ship a font in the video whose licence the person hasn't confirmed.

## Files

- `references/story.md`: the pitch roast, hooks, the script and caption language. Load in steps 2 and 4.
- `references/theme.md`: the VideoTheme contract, sources, derivation, contrast and fonts. Load in step 3.
- `references/motion.md`: curves, camera, blur, whips, captions, micro-interactions, and the bugs that make jumps.
  Load in steps 4 and 6; take values from it, don't approximate.
- `references/sound.md`: the beat grid, the synth, effects, mastering targets and checks. Load in step 8.
- `references/review.md`: the roast briefs and the measured checks. Load in step 7.
- `references/pipeline.md`: project layout, render commands, stills, the X export. Load in steps 5, 6 and 9.
- `template/`: the starter project. `src/kit/` holds the theme (`theme.ts`: type, design.how's default, presets,
  contrast check, `mix`, font aliases), the motion parts (`motion.tsx`: ramp, scramble, Sampled, whipAt, Caption,
  Panel), scenes with whips and blur (`shot.tsx`), the pointer (`pointer.tsx`), font loading (`fonts.tsx`) and the
  soundtrack (`soundtrack.tsx`). `audio/` is the synth, renderer and checks (its README has the cues contract and the
  effect palette). `template/scripts/render.mjs` renders stills, the review cut, the master and the X cut and runs the jump
  and energy checks; `template/scripts/frame-jumps.mjs` and `template/scripts/energy.mjs` are those checks;
  `template/scripts/theme-from-site.mjs` drafts a theme from a site. `src/example/` is a smoke test, not a video to copy.
