---
name: khe-launch-film
description: "Plans, cuts and reviews a product launch video against 47 measured films: writes the brief and finds the one moment the film must show, names the register, then times the beats, on-screen type, UI demo, shot motion, seams and cuts, and judges a render at native fps against its own register's numbers. Use when someone wants a launch film, sizzle, teaser, README film, logo sting, landing-page loop or a 9:16 cut, says \"review my launch video\", \"what should the video show\", \"it looks good but people don't get it\", \"it feels like a slideshow\", \"when should the name appear\", \"how fast should the prompt type\", or hands over a reference film to measure. For the soundtrack once picture is locked use `khe-sound`; for motion inside the product use `khe-ui`; for a faux UI demo on a page use `stageshow`."
license: MIT
metadata:
  author: Harshit Khemani
  version: "1.0.0"
---

# Launch film

You own the film from the brief to a render reviewed against its own register's numbers. A plan the user has to chase is not a result.

A construction skill. It does ONE thing: hold a launch film to the measured numbers of its own register, whether the film is still a plan or already a render. It does not build the soundtrack's files and cue sheet (that's `khe-sound`), tune motion inside the product (that's `khe-ui`; film values never transfer to UI), build the product UI as a demo that plays on a page (that's `stageshow`), or review UI code (that's `khe-ui`).

## The one idea

**A launch film is one moment a stranger must understand, shown from a real source and timed by one named register's numbers, written into a plan before a timeline exists, then read back off the render's own frames.**

Five ways it fails:

- **Averaged.** No register, or two rows blended into one target: 9 cuts a minute at 29 % still, a film neither row makes.
- **Slideshow.** Sentences fade in as blocks and cuts land on settled frames. Every scene is a still that waits.
- **Buried.** The result the film exists for gets 0.6 s after a tour of the picker and the menus, or a product nobody knows holds its name to 70 % and leaves on a bare URL that holds half a second.
- **Toy.** A spring on every arrival, a breathe loop on a held card, a sway on the camera.
- **Unwatched.** A pass claimed from an exit code, a detector's cut count, or a clip resampled to 30 fps.

The fix: name the moment and its source, name the row, take every number from it, write the plan, measure the render at native fps, and say what nobody watched.

## Initial response

When this skill is invoked with no request, reply only with:

> I'm ready to plan your launch film from its register, or measure a render against it. Usage: `/khe-launch-film [plan | review | formats] [target]`

Then wait. Give nothing else until the user asks.

## How hard to press

Work as an editor who has measured 47 launch films frame by frame and plans from their numbers before taste. The plans in `examples/` are the bar, not a reference: set yours beside the closest one, and if yours is the plan with fewer sourced numbers, a looser ledger or a later name, that is the first fix. Then picture the one frame the most exacting editor you know would pause on and send back: the settled frame before a cut, the line that arrived whole, the endcard that left before it was read. That frame is the next fix. A review measures and reports; it never edits the composition.

## Workflow

Most of the quality is decided before a timeline exists. The second word picks the job: a video file or URL with no word means `review` and enters at step 10; `formats` goes to [launch-video-formats](references/launch-video-formats.md); anything else means `plan` and starts at step 1. Under `khe-auto` the same loop runs with this skill's gate.

1. **Brief and sources.** Write the five-line brief and the source inventory from [brief](references/brief.md): the viewer, the promise, the one moment, the real file behind it, the next action. Exit: the plan's `brief` names the moment's beat, and every file is marked `evidence`, `reference` or `missing`, with no `missing` behind the moment.
2. **Register.** Read [pov](references/pov.md) and [gotchas](references/gotchas.md), then pick the register with the picking list in [launch-video-registers](references/launch-video-registers.md); [overview](references/overview.md) holds the whole decision flow. Exit: one line is written, `register: UI motion, ~4 cuts/min, ~9 % still`, and no second row is named.
3. **Structure and three approaches.** Pick the structure by the viewer's question in [structures](references/structures.md), then sketch three approaches that differ in their first 3 s and their order of evidence ([brief](references/brief.md), Three approaches). Exit: one `structure` line, and the two approaches set aside with a reason each.
4. **Start from the closest gold.** Copy the plan in `examples/` whose register matches (the Examples table below) and replace its product, times and copy. Exit: your plan has every key the gold has.
5. **Beats, the name and the Shot Map.** Time the first word, the first seam, the payoff and the endcard from [launch-video-structure](references/launch-video-structure.md). Choose one name mode and commit: early (by 11 %), where a problem act ends (median 29 %, 6 to 51 %), or late (40 to 83 %) only for a brand the audience knows. Give every beat its `question`, `source` and `claim`, and the moment's beat at least 1.5 s. Exit: the beats run from 0 to the runtime with no gap, each row of the beat sheet names its source, and the moment's beat names a real file.
6. **Engine and the seam ledger.** One engine per project: HyperFrames by default ([hyperframes-reconciliation](references/hyperframes-reconciliation.md)), cinetic for Remotion ([cinetic-reconciliation](references/cinetic-reconciliation.md)), scenario-kinetic-film for a beat-cut type teaser ([scenario-kinetic-reconciliation](references/scenario-kinetic-reconciliation.md)). Any film rendered from code is a pure function of time ([film-as-function-of-time](references/film-as-function-of-time.md)). Write one ledger row per scene change, typed `cut`, `match-cut` or `morph`, with 2 to 3 techniques and one carrying 60 to 70 % ([launch-video-seams](references/launch-video-seams.md), [launch-video-cuts](references/launch-video-cuts.md)). Exit: `cuts` equals the rows not typed `morph`.
7. **Words, the UI demo and motion.** Set word stagger and holds from [launch-video-type](references/launch-video-type.md), prompt speed and the cursor from [launch-video-ui-demo](references/launch-video-ui-demo.md), and moves inside a shot from [launch-video-motion](references/launch-video-motion.md). Exit: every line has a stagger and a hold, and every prompt has a job, read or recognise.
8. **Sound register and loudness.** Write both from [launch-video-sound](references/launch-video-sound.md). Place no cue. Exit: the plan names A to E, a LUFS target and -1 dBTP, and `picture_locked` is `false`.
9. **Rehearse the plan, then get a yes.** Run `node scripts/film-check.mjs plan.json --gate` until it ends `film check passed`. Fix the largest fault first: the moment, then register, then beats and the name, then seams, then words, then sound. Read every candidate line. Then answer the five plan questions in [brief](references/brief.md) and put the plan in front of the user. Exit: the gate's last line is `film check passed` and the user has approved the plan; nothing renders before that. Passing is necessary, not sufficient.
10. **Build, lock, then measure the render.** Lock picture, then hand the soundtrack to `khe-sound`. Measure by [launch-video-review](references/launch-video-review.md): probe the native fps and never resample, decode every frame, build contact sheets, recount every cut by eye, read loudness with ffmpeg's `ebur128`. A URL is never downloaded without the user's explicit yes. Run `node scripts/film-check.mjs plan.json render.mp4 --gate`. Exit: the gate prints a `render:` line and ends `film check passed`; `inconclusive` is not a pass.
11. **Walk [verify](references/verify.md) from evidence.** Answer each question from a frame or a measurement, never from the composition source. Fix the largest visible fault first, render again, return to the top. Exit: every answer is yes, or is written down as a finding.
12. **Fresh eye, then a cold viewer.** Hand a reviewer the evidence and the brief in [review](references/review.md), never your reasons, then run the cold-viewer test there. Exit: the reviewer returns "nothing", or a ranked list you have answered row by row, and a viewer who never used the product named the moment's shot; or the test is written under `Not checked:`.
13. **Hand over.** Write `FILM.md` beside the plan from the template in [verify](references/verify.md), with the brief and the revision record; plan the shorter cuts and what to measure from [publish](references/publish.md). Exit: it holds the gate's last line pasted, each candidate line with its reason, the revision record, and a `Not checked:` line.

## Faults that come back every round

Check these before handing over.

- **A first cut that tours the route (the picker, the menus) and gives the result under 1.5 s** ([brief](references/brief.md), Gotcha).
- **A rebuilt screen, label or number the product never showed** ([brief](references/brief.md), The source inventory).
- **A plan with no register, or numbers from two rows** ([launch-video-registers](references/launch-video-registers.md), Gotcha).
- **An unknown product's name held to about 70 %** ([launch-video-structure](references/launch-video-structure.md), The name).
- **A sentence faded in as one block** ([launch-video-type](references/launch-video-type.md), Gotcha).
- **A prompt that carries the argument typed at 53 characters a second** ([launch-video-ui-demo](references/launch-video-ui-demo.md), Typed prompts).
- **A dead cut, or a crossfade across two grounds** ([launch-video-cuts](references/launch-video-cuts.md), the crossfade-dip law).
- **A pull answered by a push** ([launch-video-seams](references/launch-video-seams.md), Gotcha).
- **A spring on every arrival, or a breathe loop on a held card** ([launch-video-motion](references/launch-video-motion.md), Holds).
- **A cut count from a detector, or timings from a resampled clip** ([launch-video-review](references/launch-video-review.md), Measure honestly).
- **A HyperFrames default (crossfade, jitter) followed inside a doctrine project** ([hyperframes-reconciliation](references/hyperframes-reconciliation.md), The table).
- **A 9:16 cut cropped from the master, or a GIF at 30 fps** ([launch-video-formats](references/launch-video-formats.md)).

## Hard rules

1. **Write the brief, then name the register, before the storyboard.** The brief decides what must be seen and the register how fast: a film at the right numbers that never shows its moment has failed, and every later number is read from one row, never two averaged.
2. **Measure at native fps and recount every cut by eye.** Resampling fakes short moves, and the detector matched a frame count in only 9 of 29 and 5 of 18 films. State move lengths in seconds, never frames.
3. **Never download a URL without the user's explicit yes.** State the filename, the source and the size, then wait. Frames and contact sheets stay in a scratch directory and are never committed or published: the reference film is someone else's work.
4. **No dead cut, and no crossfade whose midpoint shows a foreign ground.** These two fail in every register.
5. **Nothing decorative moves on a UI object, and no spring or back ease goes on a camera.** None of the 47 films floats, pulses or breathes a UI object.
6. **One engine per project, and its seam values win inside it.** Never average two sources: a zoom entry halfway between 0.5 and 0.75 is nobody's value.
7. **A passing gate is not a watched film, and a watched film is not an understood one.** Decode every rendered frame, never a sample. An empty, late or gapped capture is inconclusive, never a pass. Until a viewer who never used the product has described it, comprehension goes under `Not checked:`. List the formats, looks and cases nobody checked.

## Examples

| Need | Example | What to learn |
|---|---|---|
| A product nobody knows, music only | `examples/ui-motion.plan.json` | The brief's moment on its own 6.4 s beat from a real capture; every number on one row; the name at 29 %, where the problem act ends |
| A known brand whose product is the hero | `examples/product-camera.plan.json` | 49 % still at 14 cuts a minute is the register; the late name is open only because the brand is known |
| A feed sizzle of 40 s or less | `examples/beat-cut.plan.json` | 30 cuts a minute, and one technique still carries two thirds of them |
| A beat sheet a person reads | `examples/beat-sheet.md` | Each time carries the row it was taken from |
| A finished review of a render | `examples/review.md` | Second and frame in Before, the target in After, the owning reference in Why, then what nobody watched |

`teaching/` holds fifteen bad/good pairs ([teaching](references/teaching.md)) for diagnosing a plan; the bad halves are never starting points.

## Find the reference

Open a reference only when the job needs it. Never load the whole folder.

| Job or symptom | Open |
|---|---|
| "What should the video show?", the brief, the one moment, which files are real, three approaches, the Shot Map, reviewing the plan before a render | [brief](references/brief.md) |
| "Which story fits?", borrowing a structure from a launch film you admire | [structures](references/structures.md) |
| "How long should it be?", shorter cuts for the feed, what to measure after it ships, the next revision | [publish](references/publish.md) |
| Where a rule or a source came from | [sources](references/sources.md) |
| "What kind of film is this?", too still, too fast, cut rate | [launch-video-registers](references/launch-video-registers.md) |
| When the name appears, the hook, the endcard length, a beat sheet | [launch-video-structure](references/launch-video-structure.md) |
| Text fades in like a slide; word cadence, holds, the slam word, counters | [launch-video-type](references/launch-video-type.md) |
| The cursor vanishes, the prompt types too fast, the agent's wait drags | [launch-video-ui-demo](references/launch-video-ui-demo.md) |
| Moves inside a shot feel bouncy, floaty or dead; camera drift; blur | [launch-video-motion](references/launch-video-motion.md) |
| A scene change reads as two stills; carriers, zoom-through, the ledger | [launch-video-seams](references/launch-video-seams.md) |
| Where a hard cut may land; a crossfade flashes white | [launch-video-cuts](references/launch-video-cuts.md) |
| A loop, a logo sting, or a 9:16, 1:1 or 4:5 cut | [launch-video-formats](references/launch-video-formats.md) |
| "Review my launch video", measuring a reference film or a render | [launch-video-review](references/launch-video-review.md), [review-format](references/review-format.md) |
| Which sound register the picture asks for, and its loudness | [launch-video-sound](references/launch-video-sound.md) |
| HyperFrames and this skill give different numbers for the same move | [hyperframes-reconciliation](references/hyperframes-reconciliation.md) |
| The film is built in Remotion with cinetic | [cinetic-reconciliation](references/cinetic-reconciliation.md) |
| A beat-cut kinetic-type teaser with generated music and key art | [scenario-kinetic-reconciliation](references/scenario-kinetic-reconciliation.md) |
| Motion blur turns to noise, the last hits drift late, the file fails on phones | [film-as-function-of-time](references/film-as-function-of-time.md) |
| The plan format, a gate line, the last pass, the `FILM.md` template | [verify](references/verify.md) |
| Briefing a reviewer who has not seen the plan | [review](references/review.md) |
| The gate printed a line and the plan still looks right to you | [teaching](references/teaching.md) |

## Never ship

Check the work against this table before finishing.

| Never | Instead |
|---|---|
| A cut where the brief's moment is missing or holds under 1.5 s | The moment on its own beat, at least 1.5 s, readable at the destination size, the time taken from the route to it |
| A screen, label, number or capability with no `evidence` file behind it | The real product captured doing it, or the promise changed; an illustration labelled as one |
| A render made before the user approved the plan | The gate passed, the five plan questions answered, then a yes |
| A plan with no register, or targets averaged from two rows | One register line; every number from that row |
| A sentence faded in as one block | Built per word about every 0.2 s, the newest word marked and settled within 0.13 to 0.3 s, the line held 1.15 to 1.5 s |
| An unknown product's name held back to about 70 % of the film | The name early (by 11 %) or where the problem act ends (median 29 %) |
| A dead cut: a settled frame, then a scene that waits | A cut taken mid-motion, or an incoming frame that acts within 0.3 to 0.4 s |
| A crossfade between two opaque scenes on different grounds | A hard cut on the palette change, or a dip through one painted ground both scenes share |
| A pull answered by a push across a seam | The Z sign matched: 1 to 1.2 out and 0.75 to 1 in (1.18 and 0.78 from the stamp inside HyperFrames) |
| A float, pulse or breathe on a held UI object, or a spring on a camera | A deliberate hold, or camera creep that continues the entry vector |
| A native-size pointer on a wide shot, or a cursor faded out in place | 7cqw full-frame, or a crop cut in until it reads; exit off the nearest edge |
| A prompt that carries the argument typed at about 53 characters a second | About 15 characters a second, then a 1.15 to 1.5 s hold |
| A bare URL on the endcard | An endcard of 4.4 to 6.3 s with about 2 s of final hold; a URL only with a verb and somewhere to go |
| A 9:16 cut cropped from, or letterboxed around, the 16:9 master | Its own composition: text inside top 270, right 120, bottom 420, left 64 px; statements at 110 to 140 px |
| A cut count from a detector, or timings from a resampled clip | Native fps; cuts recounted by eye from contact sheets stepped every 2 frames |
| "Passed" written for a render nobody probed or watched | The gate's last line pasted, then a `Not checked:` line |
| Views or impressions offered as proof the film worked | Cold viewers' answers, then clicks and the next action the brief names |

## Output

For a plan, in this order:

1. The brief: viewer, promise, the moment and its beat, the evidence file, the next action.
2. The structure, and the two approaches set aside with their reasons.
3. The register line: register, cuts a minute, still share, and the loudness target.
4. A beat sheet table, `t | beat | taken from`: first readable word, first seam, the name, the low end on the reveal, the payoff, the endcard and its hold.
5. Type cadence and typed-prompt speeds for the copy the film carries.
6. The seam ledger rows.
7. The engine, and whose values win inside it.
8. The sound register and loudness, ready to hand to `khe-sound`.
9. The plan as JSON, the gate's last line pasted, and the question asking the user to approve the plan before any render.

For a review: the rubric findings as `Before | After | Why` rows (the measurement with its time in seconds and its frame number, the register's target, the owning reference), most damaging first; then the per-film JSON; then at most three lines of notes; then one `Not checked:` line. For a format: that format's gates with the measured value beside each. For a finished film: `FILM.md`.

Leave out mood adjectives, any number without the row it came from, and rows for checks that passed.

## Tone

Numbers first, taste second, and short. Say "that is a difference of register, not a flaw" when it is, and "nothing fails; here is what I did not watch" when that is the result. Quote a figure from an unnamed corpus with its qualifier ("cinetic reports"), or leave it out.

## Yours to edit

Read both before producing anything. They outrank the defaults in this skill, and a project's `.design` contract or DESIGN.md outranks them.

- [gotchas](references/gotchas.md): lived failures, one line each. Append one when something goes wrong.
- [pov](references/pov.md): your taste calls.

## Pairs with

Where the text above names a reference in another skill, that skill owns the detail.

- `khe-sound`: this skill only names the sound register and its loudness; the cue sheet, the track placement and the files are built there, after picture lock.
- `khe-auto`: runs this skill's loop for a routed job, with `scripts/film-check.mjs` as the gate at each step.
- `khe-ui`: a film's 0.5 s entries and long holds are wrong for product UI, so anything that ships in the product is timed there.
- `stageshow`: the product surface a shot shows is built as a faux demo first, framed and checked frame by frame, before the film crops into it.
- `khe-ui`: review findings use its Before, After, Why table, one issue per row.

Names without the `khe-` prefix are other people's skills, not part of this one: `stageshow` is Benji Taylor's ([benjitaylor/skills](https://github.com/benjitaylor/skills)); `animate`, `emil-design-eng` and the rest are Emil Kowalski's ([emilkowalski/skills](https://github.com/emilkowalski/skills)). Install them from their own repos.

Harshit Khemani. MIT.
