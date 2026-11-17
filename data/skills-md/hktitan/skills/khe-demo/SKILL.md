---
name: khe-demo
description: "Records a demo of the real running product: seeds its state, writes the flow as a script file, drives the actual web app or desktop app, and hands back a short clean take (mp4 or webm, plus a GIF for a README) in which one thing happens and every pointer move has a cause. Use when someone says \"record a demo of the app\", \"screen recording for the README\", \"walkthrough video\", \"GIF of the feature\", \"capture the real flow\", \"show it working\", or wants a product take to cut into a film. For a faux or illustrated UI that never runs the product use `stageshow`; for a cut, scored launch video use `khe-launch-film` (a take from here is often one shot inside it); for sound use `khe-sound`."
license: MIT
metadata:
  author: Harshit Khemani
  version: "1.0.0"
---

# Demo

You own the demo from the request to a recorded, gated file and its handover. A script the user still has to run, or a take nobody watched, is not a result.

A construction skill. It does ONE thing: record the real product doing one thing, from a seeded state, by a script that runs twice. It does not draw faux or illustrated UI (that's `stageshow`, where a click only draws a cursor), cut, title or score a launch video (that's `khe-launch-film`; a take from here is often one shot inside it), make or place sound (that's `khe-sound`), or fix the product's own motion (that's `khe-ui`).

## The one idea

**A demo is the real product doing one thing, from a state you seeded and can reset, driven by a script you can run twice, captured at the size it will be watched.**

Five ways it fails:

- **Dirty.** A real customer's name, a personal inbox, a token in the address bar, a notification sliding in, the bookmarks bar. Whatever is on screen is published.
- **Dead air.** The app loads for three real seconds and the take waits with it, or a hold sits where nothing is being read.
- **Teleport.** The pointer jumps between controls in one frame, or drifts to a place the next step never uses.
- **Tiny.** A full desktop window shown a third of its size: 13 px labels landing at 5 px in a README.
- **One-shot.** The flow worked once. Take two starts from what take one left, so nothing can be re-recorded, trimmed differently or trusted.

The fix: seed the state, write the script, rehearse it dry, record it twice at a fixed size, then cut the waits and gate the file.

You cannot fake state here. A row that should be on screen is in the seed; a result that should appear is produced by the app. Injecting DOM to stage a result makes it faux UI, and that is another skill.

## Initial response

When this skill is invoked with no request, reply only with:

> I'm ready to record a demo of your running app. Usage: `/khe-demo [plan | record | post | review] [url or app] [readme | site | social | film]`

Then wait. Give nothing else until the user asks.

## How hard to press

Work as someone who records product demos for a launch page and will be judged on one viewing. The scripts in `examples/` are the bar, not a reference: set yours beside the closest one, and if yours has more beats, a hold with no reason, a target found by position or no reset, that is the first fix. Then picture the one frame the most exacting viewer would pause on and send back: the notification in the corner, the pointer parked on a label, the spinner at second four, the email address that is somebody's. That frame is the next fix.

## Safety, before anything runs

1. **Record only the user's own app, or one they are authorised to demo.** `record.mjs` refuses a host that is not local until it is named with `--allow-host`. Never record a production page that shows real users' data.
2. **Never type a real credential on camera.** Start the take already signed in to a test account from the project's seed files. A password step is reported by the gate every time.
3. **Never record a real person's data.** Names, emails, avatars and messages come from the seed; emails sit on `example.com` or a `.test` name.
4. **Ask before recording more than the app's window.** A desktop take captures the window's rectangle. The whole display needs the user's yes, in chat.
5. **Recordings stay out of the repository.** Write them to a scratch or `out/` folder the project ignores, and commit only the script and `DEMO.md`.

## Workflow

Most of the quality is decided before the browser opens. The second word picks the job: `plan` stops after step 5, `post` enters at step 7 with a take in hand, `review` enters at step 9. Under `khe-auto` the same loop runs with this skill's gate.

1. **Surface and place.** Read [pov](references/pov.md) and [gotchas](references/gotchas.md). Name the surface (web or desktop), its driver and its capture layer from [surfaces](references/surfaces.md), and the destination (readme, site, social, film), which sets the viewport, scale, length and size ceiling in [capture](references/capture.md). Exit: one line is written, `web, playwright, readme, 1024 x 640 at 2, 30 fps`.
2. **The story.** Two to five beats and a payoff, one thing happening, each beat a sentence saying what the viewer sees ([script](references/script.md), The story). No pointer move you cannot explain. Exit: every beat has its sentence, the last one is the payoff, and a person who reads only the sentences knows what the product did.
3. **Seed and reset.** Write the state the take opens on and the steps that restore it: a test account, fixed data, a frozen clock, a clean window ([state](references/state.md)). Exit: the reset runs from a shell or the script's `reset` block, and running it twice gives the same first frame.
4. **Write the script as a file.** Copy the closest gold in `examples/` (the Examples table) and replace its product. Targets by test id or role and name, every action with the condition it waits for, holds with a reason ([script](references/script.md)). Exit: `node scripts/demo-check.mjs demo.json --gate` ends `demo-check passed`.
5. **Dry run.** `node scripts/record.mjs demo.json --dry-run`. Every step meets its condition at real pace; read each wait it prints. Exit: it ends `dry run finished`, and every wait over 1000 ms is either fixed in the app or marked `"ramp": true`.
6. **Record.** `node scripts/record.mjs demo.json --out take.mp4 --takes 2` at the declared viewport, scale and frame rate ([capture](references/capture.md)). A desktop app is walked with its driver while ffmpeg captures the window ([surfaces](references/surfaces.md)). Exit: it prints `repeatable: 2 takes ended on the same screen` and `recorded`, and the frames arrived at viewport times scale.
7. **Post.** Trim the handles, ramp the waits, push in on the action only when the text needs it, then export the delivery files with `scripts/post.mjs` ([post](references/post.md)). No captions, music or sound here. Exit: each delivery file exists, and a contact sheet of the final file is made.
8. **Gate.** `node scripts/demo-check.mjs demo.json take.take.json <the files you will hand over> --gate`. Fix the largest fault first: state, then story, then pace, then size. Exit: the last line is `demo-check passed`. `inconclusive` is not a pass. Passing is necessary, not sufficient.
9. **Walk [verify](references/verify.md) from evidence.** Watch the file at full speed, then read the contact sheet frame by frame. Answer each question from a frame, never from the script. Exit: every answer is yes, or is written down as a finding and fixed.
10. **Fresh eye.** Hand a reviewer the file, the sheet and the brief in [review](references/review.md), never your reasons. Exit: the reviewer returns "nothing", or a ranked list you answered row by row.
11. **Hand over.** Write `DEMO.md` beside the script from the template in [verify](references/verify.md). Exit: it holds the gate's last line pasted, each candidate line with its reason, the files with their sizes, and a `Not checked:` line.

## Faults that come back every round

Check these before handing over.

- **A reset that only works in a fresh browser profile** ([state](references/state.md), Reset).
- **A sleep where a condition belongs** ([script](references/script.md), Waits).
- **A pointer resting on the words it just clicked** ([script](references/script.md), The pointer).
- **A take captured at scale 1, then pushed in on** ([capture](references/capture.md), Scale).
- **Frames that arrived at CSS size and were upscaled** ([surfaces](references/surfaces.md), What the screencast gives).
- **A GIF at 15 or 30 fps** ([capture](references/capture.md), GIF).
- **A wait left at real time because "it is only two seconds"** ([post](references/post.md), Ramp).
- **A notification, an update badge or today's date in the take** ([state](references/state.md), The window).
- **A snapshot ref written into the script** ([surfaces](references/surfaces.md), Refs).
- **"Recorded" claimed from the runner's exit code** ([verify](references/verify.md), Gate).

## Hard rules

1. **Seed the state; never stage it.** Every row, name and number on screen comes from seed data the app loaded itself, because a faked result is a claim about the product that is not true.
2. **The script is a file, and it runs twice.** A demo driven by hand, or by a chat of one-off commands, cannot be re-recorded when the copy changes next week.
3. **Wait on conditions, never on time.** A sleep is too long on a fast machine and too short on a slow one. The only fixed pauses are holds for reading, capped at 1500 ms, and the payoff hold of 1500 to 3000 ms.
4. **One viewport, one scale, one frame rate, declared before recording.** The gate checks the file against them, and a number chosen after the take is a number nobody can check.
5. **Nothing on camera that is secret or somebody's.** The gate reads what the script types, loads and opens; the frames are checked by eye, one by one.
6. **Never upscale a take.** If the frames did not arrive at viewport times scale, record again; `record.mjs` stops when they do not.
7. **A passing gate is not a watched take.** Say what nobody looked at.

## Examples

| Need | Example | What to learn |
|---|---|---|
| A feature on a site, with seeded data | `examples/web-flow.demo.json` | One reset step, four beats, a 900 ms save waited for by condition and marked for a ramp |
| A loop or a GIF for a README | `examples/readme-loop.demo.json` | The payoff is the last beat; `loop.return` undoes it by causes the viewer sees, so the last frame is the first |
| A phone-sized vertical take | `examples/mobile.demo.json` | 360 x 640 at scale 3 is 1080 x 1920 with no resize; a touch dot, the app's own phone layout |
| A native desktop app | `examples/desktop.demo.json` | The driver acts, ffmpeg records the window, targets are role and name, no ref in the file |
| Something to run these against | `examples/app/` | A task list whose whole state is one localStorage key; `node examples/app/serve.mjs` serves it |

`teaching/` holds fourteen bad/good pairs ([teaching](references/teaching.md)) for diagnosing a script; the bad halves are never starting points.

## Find the reference

Open a reference only when the job needs it. Never load the whole folder.

| Job or symptom | Open |
|---|---|
| Web or desktop, which driver, which commands exist, what cannot record | [surfaces](references/surfaces.md) |
| Real data on screen, a take that works once, sign-in, the clock, notifications | [state](references/state.md) |
| The script format, targets, waits, pointer speed, typing speed, holds | [script](references/script.md) |
| Viewport per destination, scale, frame rate, codecs, GIF, size ceilings | [capture](references/capture.md) |
| Trimming, speeding up a wait, zooming on the action, exporting | [post](references/post.md) |
| A gate line, the last pass, the `DEMO.md` template | [verify](references/verify.md) |
| Briefing a reviewer who has not seen the script | [review](references/review.md) |
| The gate printed a line and the script still looks right to you | [teaching](references/teaching.md) |

## Never ship

Check the work against this table before finishing.

| Never | Instead |
|---|---|
| A take of production, or of a real account | A local or test host, a seeded test account, emails on `example.com` |
| A password typed on camera | A take that opens signed in; the reset loads the session |
| A result staged by editing the page | Seed data the app loads itself |
| `sleep 3000` while the app loads | A wait on the row, text or URL the viewer is waiting for, marked `"ramp": true` when it takes over 1000 ms |
| A hold over 1500 ms before the payoff | A hold sized to what is read; only the payoff holds 1500 to 3000 ms |
| A target by `nth-child`, a generated class, a coordinate or `@e12` | A test id, or a role and its name |
| A pointer that arrives in one frame | 300 to 900 ms of travel, set by distance and target size, on a shallow arc |
| Text typed at 50 characters a second | 12 a second, and no more than 60 characters in one step |
| A 1920 px window shown 830 px wide | The destination's viewport: 1024 x 640 for a README, at scale 2 |
| A take at scale 1 that is then zoomed | Scale 2, so a 2x push still shows one file pixel per screen pixel |
| A GIF at 15 or 30 fps, or over 10 MB | 20 fps at 800 px wide from a palette built for the clip; past 5 MB ship the mp4 |
| An `.mp4` in yuv444p | H.264 in yuv420p with the index at the front |
| A loop whose last frame is not its first | `loop.return`: the demo undone by a cause the viewer sees |
| A recording committed to the repository | The script and `DEMO.md` committed; the files in an ignored folder |
| "Recorded" written for a file nobody probed or watched | The gate's last line pasted, then a `Not checked:` line |

## Output

For a plan, in this order:

1. The surface line: surface, driver, destination, viewport and scale, frame rate.
2. The beats as a table, `beat | what the viewer sees | waits for`.
3. The state: account, seed, reset steps, clock, what is hidden.
4. The script as a file, and the gate's last line pasted.

For a recording: the delivery files with duration, size in pixels and megabytes; the gate's last line; the candidates that stand, each with its reason; then `DEMO.md`. For a review: findings as `Frame | What | Fix` rows, worst first, then one `Not checked:` line.

Leave out adjectives about the product, any number without its reason, and rows for checks that passed.

## Tone

Plain and short. Say "the take works once; here is the missing reset" before any polish. Say "nothing fails; here is what I did not watch" when that is the result. When a driver cannot do something on this machine, say so and name the fallback you used.

## Yours to edit

Read both before producing anything. They outrank the defaults in this skill.

- [gotchas](references/gotchas.md): lived failures, one line each. Append one when something goes wrong.
- [pov](references/pov.md): your taste calls.

## Pairs with

- `stageshow`: when the product cannot be run, seeded or shown, or the shot needs a simplified picture of it, the UI is authored there. Never mix the two in one take.
- `khe-launch-film`: a take from here is one shot. The film's register, cuts, type and length are decided there, and its numbers outrank this skill's holds inside a film.
- `khe-sound`: clicks, a bed or a voice are added there, after the take is locked, because the next trim moves every cue.
- `khe-ui`: when the take shows the product's own motion is wrong, it is fixed in the product there, never painted over in post.
- `khe-auto`: runs this skill's loop for a routed job, with `scripts/demo-check.mjs` as the gate.

Sources: the method (one idea, named failures, gold examples, teaching pairs, a gate, a fresh-eye review, a handover file) follows Benji Taylor's Stageshow ([benjitaylor/skills](https://github.com/benjitaylor/skills)). The drivers it can call are [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) and [vercel-labs/agent-desktop](https://github.com/vercel-labs/agent-desktop). They are tools this skill runs when they are installed; nothing of theirs is bundled. Names without the `khe-` prefix are other people's skills: install them from their own repos.

Harshit Khemani. MIT.
