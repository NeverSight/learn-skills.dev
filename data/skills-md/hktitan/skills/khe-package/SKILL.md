---
name: khe-package
description: "Packages something you built for people who have never heard of it: picks the format (an explainer rendered from HTML, a click-through of one live component, a hover reel, a recording page), sends three ideas as stills before any render, renders one frame at a time on a paused clock at 60 fps with the short side at 2000 px or more, crops to the work with 40 to 60 px of page around it, moves your system's real cursor on a slight curve and holds it still while the motion plays, then writes the post's first line for a stranger, not for you. Use when someone says \"package this\", \"make a video of this for X\", \"render it at 4k\", \"a clip for the launch post\", \"how should I show this off\", \"give me ideas for the announcement video\", or \"package my work\". To record a whole product flow use `khe-demo`; for a cut, scored film `khe-launch-film`; for faux UI `stageshow` (Benji Taylor); for the posts on each platform `khe-content-engine`. When unsure, `khe-auto`."
license: MIT
metadata:
  author: Harshit Khemani
  version: "1.0.0"
---

# Package

You own the package from "I built this" to a rendered video a stranger stops for and a first line that says what is in it for them. Building has become easy; how the work is shown is what sets it apart. This skill decides the format, gets a look agreed on stills, renders the video frame by frame, and hands the post to the writer.

It does not record a whole product flow from a seeded state (that's `khe-demo`), cut a film with titles and a score (`khe-launch-film`), draw faux product UI (`stageshow`, Benji Taylor), write the post for every platform (`khe-content-engine`), or post anything: a person posts.

The approach is Emil Kowalski's way of packaging work, rewritten here in this collection's format; the credit is in [sources](references/sources.md).

## The one idea

**The video is watched muted, small, on a phone, and scrolled past: the work has to read in the first second, sharp, with nothing else in the frame.**

Five ways it fails:

- **Speck.** The component is a small thing on a whole page at 800 by 450. On a phone it is a few hundred pixels of blur.
- **Jitter.** Captured in real time: dropped frames, a soft webm, a transition that stutters on the one frame that mattered.
- **Ghost hand.** No cursor, a drawn cursor, or a cursor that teleports, drifts during the animation or covers the label it clicked.
- **Slow open.** A blank tab, a load, a long hold before the first action; the thumb has moved on.
- **About me.** The post opens with "I made" or "Excited to share". Nobody cares who made it until they know what it does for them.

## Initial response

When this skill is invoked with no request, reply only with:

> I'm ready to package what you built. Point me at it (a route, a component, a page) and say where it goes. I'll send three ideas as stills first, then render. Usage: `/khe-package [what] [for X | newsletter | launch post] [ideas | stills | render]`

Then wait.

## Operating posture

You are the person who has posted their work for years and knows which first second stops a thumb. Two failure modes, the worse first:

1. **Rendering before agreeing.** A full render costs minutes; three rounds of it cost the afternoon. Stills first, always.
2. **Showing the page instead of the work.** The wrapper, the site header, the replay button, the blank margin: everything in the frame that is not the work is noise at phone size.

## How hard to press

The gold plans in `examples/plans/` and the two sources in `examples/explainer/` and `examples/live/` are the bar. Beside the closest one, if your frame is softer, your first action later, or your first line about you, that is the first fix. Then watch your render as a stranger scrolling at speed: if the first second does not say what the thing does, nothing after it will be seen.

## Hard rules

1. **Three ideas, as stills, before any render.** Each idea is a different way to show the work, with one still. The user picks; then two to four stills of the chosen look; then the render. When they change something, re-send only the frames it touches.
2. **Never deliver real-time capture.** Every rendered format steps time one frame at a time on a paused clock. Real-time capture drops frames and Playwright's video is soft. The only real-time footage is a recording the user made themselves.
3. **Sharp and playable.** The short side is at least 2000 device pixels and the long side at most 4096; 60 fps, H.264, crf 14, yuv420p, faststart, no audio. Under 2000 is soft on a phone; over 4096 plays badly.
4. **Crop to the work.** 40 px of page around a reel item, 60 px around a click-through (40 can feel cramped on a wide one), the component at its real width. Raise the device scale for sharpness; never CSS-scale a live component.
5. **The cursor is the system's, and it holds still.** The real arrow and hand from the machine that renders, never a drawn one. It glides on a slight curve, starts and ends off-frame, and stops dead while the animation plays.
6. **The first second is the hook, and the first line is for a stranger.** The first action lands 0.3 to 0.4 s in; cuts are hard. The post's first line says what the viewer gets: how it was made, what they can take from it, or what it solves.
7. **Copy the real thing.** The component, its copy, durations, curves and colors come from the current source, re-read before every render. Never edit real names, posts, reviews or dates; crop them out.

## Workflow

1. **Plan.** Read [gotchas](references/gotchas.md) and [pov](references/pov.md). Name the work, where it goes and who watches. Pick the format by [formats](references/formats.md). Exit: `Work:`, `For:`, `Format:` and `Why this format:` in `PACKAGE.md`.
2. **Ideas.** Three different ways to show it, each one sentence and one still. Render stills only: `node scripts/render.mjs <mode> <source> stills <t1,t2>`. Exit: three ideas under `Ideas:`, each with a still path, sent to the user. Wait for a pick.
3. **Build the source.** An explainer page with `window.render(t)` ([render](references/render.md), Explainers), or a temporary stage route and a shot list for a live component ([render](references/render.md), Live). Start from the closest gold in `examples/`. Exit: the source renders a still that matches the chosen idea.
4. **Agree the look.** Two to four stills of the chosen idea, at the moments that matter: the first action, mid-animation, the rest state. By [framing](references/framing.md) and [cursor](references/cursor.md). Exit: `Stills:` and `Approved:` filled from the user's answer.
5. **Time it.** Holds and glides by [timing](references/timing.md); a shorter hold beats a longer one. Exit: `Length:` inside the format's range, `Hook:` naming what the first second shows.
6. **Render.** `node scripts/render.mjs <mode> <source> video out/<name>-<length>s.mp4`. Keep the previous render until the new one is approved. Exit: the file exists.
7. **Check the file.** `node scripts/package-check.mjs PACKAGE.md --video out/<name>.mp4 --gate`, then the frames in [verify](references/verify.md): an idle frame, a mid-animation frame, the last frame, and a contact sheet. Exit: `package-check passed`, and you can say which frames you looked at.
8. **The post.** Write the first line by [post](references/post.md) and run its stranger test; hand the full draft to `khe-content-engine` when there is one, or write one plain post. Exit: `First line:` in the plan, passing the gate's `about-me` line.
9. **Hand over** in the Output format. Delete temporary routes.

## Faults that come back every round

- **A render started before a still was agreed.** `no-stills`; Hard rule 1.
- **Playwright's `recordVideo` reached for because it is one line.** `real-time`; [render](references/render.md).
- **A live component scaled with CSS to fill the frame.** It re-rasterizes and blurs. Raise the device scale instead; [framing](references/framing.md).
- **The cursor gliding on through the animation.** [cursor](references/cursor.md), Holding still.
- **Holds that felt right in the draft.** They always end up shorter; [timing](references/timing.md).
- **Copy from memory instead of the current source.** Hard rule 7.
- **A first line that starts with "I" or "We".** `about-me`; [post](references/post.md).

## Examples

| Need | Example | What to learn |
|---|---|---|
| One live component, two states | `examples/plans/metrics-click-through.md` with `examples/live/` | Three ideas, a stage at 60 px, a shot list, the system cursor resting low-right of the label |
| A comparison of motion | `examples/plans/easing-explainer.md` with `examples/explainer/index.html` | `window.render(t)` sets every style from `t`; the same open on the same frame; twice at 1x, once at 4x |
| Many items, one interaction | `examples/plans/cards-hover-reel.md` | One item per cut at 40 px, the entry side varied, the plan at the reel's own length |

`teaching/` holds bad/good pairs ([teaching](references/teaching.md)) for diagnosing a fault; the bad halves are never starting points.

## Find the reference

| The job or the symptom | Open |
|---|---|
| Which format: explainer, click-through, hover reel, recording page, phone recording | [formats](references/formats.md) |
| Frame size, device scale, margins, what stays on screen, fonts, alignment | [framing](references/framing.md) |
| Holds, glides, scene lengths, the hook, loops, "make it shorter" | [timing](references/timing.md) |
| The cursor: where it comes from, its path, where it rests, holding still | [cursor](references/cursor.md) |
| Running `render.mjs`: explainers, live stages, shot lists, the paused clock | [render](references/render.md) |
| The plan file the gate reads | [plan](references/plan.md) |
| The first line, value over announcement, proof of work | [post](references/post.md) |
| Probing the file, frames to look at, the contact sheet, the report | [verify](references/verify.md) |
| A second reviewer's brief | [review](references/review.md) |
| Which teaching pair matches a fault | [teaching](references/teaching.md) |
| Where the approach came from | [sources](references/sources.md) |
| Faults this skill has made before | [gotchas](references/gotchas.md) |
| Your own calls | [pov](references/pov.md) |

Scripts: `scripts/render.mjs` renders stills and video from an explainer page or a live stage; `scripts/package-check.mjs` checks the plan and, with `--video`, the file (`--self-test` proves it on the examples and pairs).

## Never ship

| Never | Instead |
|---|---|
| A render nobody agreed a still for | Three ideas as stills, a pick, then the look on two to four stills |
| Playwright `recordVideo` or a screen capture | `render.mjs` on a paused clock, one frame at a time |
| The whole page at 800 by 450 | The component plus 60 px, short side 2000 px or more |
| A 4860 px long side | Device scale lowered until the long side is 4096 or less |
| A drawn arrow | The system's own cursor image, at its largest size |
| A cursor drifting while the bars grow | The cursor stopped dead until the motion settles |
| A blank first second | The first action 0.3 to 0.4 s in |
| A fade between two demos | A hard cut |
| "Excited to share what I built" | What the viewer gets: the trick, the steal, the problem solved |
| A real person's post or name edited to fit | Cropped out |
| "Ready to post" | `Not verified:` and what nobody checked |

## Output

Files first: the video in `out/`, named with its length; the stills; `PACKAGE.md` beside the source.

The reply, in this order:

1. The video, shown inline where the client can, with its absolute path.
2. Resolution, frame rate, length and size, and which frames you checked.
3. `Gate:` the last line of `package-check.mjs --gate`, pasted.
4. The first line for the post.
5. One concrete next cut and what it saves ("dropping the second normal-speed run saves 3.5 s"), not a menu.
6. `Not verified:` the last line.

## Tone

Short and visual. Show stills rather than describe them. Say the number you chose and why. Never praise the work; let the frame do it.

## Yours to edit

- [gotchas](references/gotchas.md): faults in how the skill works, one line each.
- [pov](references/pov.md): your calls, such as a default theme or where video projects live. Neither overrides Hard rules 1 to 3.

## Pairs with

- `khe-demo`: a whole product flow from seeded state, recorded as a take; this skill packages one component or one idea.
- `khe-launch-film`: when the package is a film with titles, cuts and sound, it takes this skill's renders as shots.
- `khe-content-engine`: writes the post for each platform from the plan; this skill writes only the first line.
- `khe-ui`: the motion worth showing; fix the animation there before packaging it.
- `khe-poteto-pyramid`: when the same packaging mistake comes back, place it there so the next agent cannot repeat it.
- `stageshow` (Benji Taylor): when the work should be shown as faux product UI rather than the real thing.

Harshit Khemani. MIT.
