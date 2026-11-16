---
name: raea
description: Make video, motion graphics, games and 3D scenes with raea, the Render Anything Engine, by writing React/TypeScript compositions with raea and rendering them on the GPU with the raea CLI (or playing games live). Use when the user names raea, or wants 3D scenes (Bevy materials, lights, physics, Gaussian splats), 3D placed into footage (matchmove), a playable game, footage cut by its words, cuts timed to a song's beat map, or foley and instruments made locally on the Mac. Also for writing or fixing 3D TSX (Camera3d, Mesh3d, lights, materials, glTF models, post effects, an ECS world), a 3D render or play that looks wrong, extending raea's Bevy SDK, rendered video, captions and motion graphics from code, and frames rendered headlessly.
metadata:
  raea-tested-against: 0.1.0-rc1
  raea-verbs: render play run check init cut song guide skill skills app controller workspace project spec doctor next library setup gen context brand scene splat blender
---

# raea

raea renders compositions written in TypeScript and React with a GPU engine built on Bevy. A composition is a function
of the frame: give it frame N and it draws frame N. The same file renders to video, plays live as a game, or renders
single frames to check.

Each step below says where it runs. **HEADLESS**: the `raea` CLI alone, in any shell. **HOST**: needs the raea app
running on this machine (its host answers). **PAGE**: needs the person's feed open in the app. **PERSON**: only the
person can do it. Every PAGE step says what a headless agent does instead.

## 0. First, every time: which workspace, which project — HEADLESS
<!-- sources: apps/workspace/src engine/cli/src -->

Before you write, render or generate anything, settle where the work belongs, and keep it all there. Agents most often
go wrong by starting to make things first and finding a home for them later, or never.
1. **The workspace.** `raea workspace --json` says which one you're in. The workspaces are the folders under raea.root
   (`git config --global raea.root`). If you're in none, or not the one this work is for (the studio or client it's
   for), pick the right one, and ask the person when it isn't clear. `raea workspace init NAME` only when they want a
   new one.
2. **The project.** `raea workspace --json` lists the workspace's projects and their folders, and `raea project --json`
   says which one you're in. Pick the one the request belongs to. When
   none fits, say which project you'd make and make it (`raea project new NAME`) before any file of the work; ask
   when it's unclear which one is meant.
3. **Name it by id.** A project's id is its folder's name, as `raea workspace --json` lists it. Titles repeat and
   drift, and agents that go by them post to the wrong project; ids don't. So name a project by `WORKSPACE/ID`
   everywhere (`raea show --project WORKSPACE/ID`, your notes, what you tell the person). When the person pastes a line
   from the app's Copy reference (a line that reads raea feed item "Hero cut" (i-acp-1) in project "Launch"
   (launch), workspace "Acme": /path/..., naming no command), it names exactly the thing they mean: that item, in that
   project.
4. **Say it, then go there.** One line before you start: "Working in WORKSPACE / PROJECT (WORKSPACE/ID)." Then
   `cd` into the project's folder and read its context (section 3). Everything you make goes in it: compositions in
   `compositions/`, footage and media in `assets/`, renders in `out/`. Never in the home folder, the Desktop, a temp
   folder or wherever the shell happened to start.
5. **Plan before you make.** `plan.org` at the top of the project's folder is its to-do list, the one the person
   sees in the app. Read it, find the task this work is (or add it), and for work of more than one step write the
   steps as tasks first. Notes from the person (a round of comments, a list of fixes) are planned first too: the work
   they ask for as tasks in your own words, each linked to the notes it answers, never the notes pasted in. Keep it as
   you go: mark tasks as you start them, close them with what you made, add what's left. In the app, the plan tools;
   anywhere else, the file as Org text. [plan.md](plan.md) says how.

In the raea app, a chat opened from a project's feed is already in its workspace and project: work there. If the
person's request turns out to be for another project partway through, stop, say so, and move to it before going on.

## 1. Install (once) — HEADLESS
<!-- sources: tools/release.sh engine/cli/src/skill.rs -->

- macOS (Apple Silicon) or Linux (x86_64): `curl -fsSL https://raea.io/install | sh`. Windows 10 or 11, in
  PowerShell: `irm https://raea.io/install.ps1 | iex`. Either puts `raea` under `~/.raea`, puts it on your PATH, and
  adds this skill to `~/.claude/skills`. Run it again to update. `raea help` lists every verb. Linux needs ALSA and
  fontconfig (`apt install libasound2t64 libfontconfig1` on Ubuntu 24.04).
- Another agent: `raea skills install --agent claude|codex|kimi|gemini` puts this skill where that agent reads skills.
  `--pin quieter` (any move) adds a `/quieter` that loads one move. It also adds raea's hooks to that agent (after a
  composition is saved, `raea check --quick` runs and hands you what it finds; media opened in the Mac's viewer goes
  to `raea show` instead, once) and the Blender MCP server; `--no-hooks` and `--no-mcp` leave them out. In Claude Code
  the skill and hooks also come as a plugin: `/plugin install raea --marketplace shinyobjectz/raea-skills`.
- This file's front matter names the raea it shipped with (`version:`). If `raea --version` prints another, read
  `raea skill` instead: it is this skill as your raea ships it.
- From a checkout of the repository: `cargo build --release -p raea-cli`; the binary is `target/release/raea`.
- Optional settings live in `~/.raea/env` (`docs/settings.md`). Rendering needs none of them.

## Reference

Generated from the code by `tools/skills.sh gen`, so they're current. Read the one you need instead of guessing a flag:
- [reference/cli.md](reference/cli.md): every `raea` verb, its flags and where it runs (`raea help` prints the same).
- [reference/feed.md](reference/feed.md): the raea app's tools for an agent it launches, and which need its page.
- [reference/files.md](reference/files.md): a workspace's and a project's files, what lives in `~/.raea`, and each
  spec's fields (brief.ts, NAME.script.ts, taste.ts, plan.ts, controllers/ID.ts).
- [reference/sdk.md](reference/sdk.md): what each `raea` import gives a composition.
- [reference/app.md](reference/app.md): driving the raea app's window over MCP, as a person would (HOST).
- [reference/platforms.md](reference/platforms.md): each network the app publishes to: shapes, lengths, file and
  caption limits, and where its interface covers the frame.

## The guides, by what you're making

raea's craft guides travel with this skill: each file under `motion/`, `3d/` and `craft/` is a copy of the guide
`raea guide NAME` prints, so either works. Open the router for what you're making; it says which one or two files the
task needs.

| Making... | Open |
|---|---|
| a cut of real footage: takes cut by words, faces framed, captions, cuts to a song | [footage.md](footage.md) |
| motion graphics and type: cards, stats, logos, end cards | [graphics.md](graphics.md) |
| sound: voice, beds, foley, music for picture, the mix | [sound.md](sound.md) |
| a 3D scene: lights, materials, models, people, rooms, splats; three.js or React Three Fiber work | [3d.md](3d.md) |
| a game, 2D or 3D | [games.md](games.md) |
| an app's interface (web or native) | [apps.md](apps.md) |
| generated images, video, sound or meshes | [gen.md](gen.md) |
| the export, the share copy, platform specs, posting a deliverable | [delivery.md](delivery.md) |
| working with the person in the raea app: the feed, controllers, the editor, boards | [collaborate.md](collaborate.md) |
| planning the work and keeping its tasks: the project's plan.org, the person's to-do list | [plan.md](plan.md) |
| checking a cut against the person's taste, reading their notes on a sound, or teaching their fingerprint | [fingerprint.md](fingerprint.md) |

Across all of them, `craft/`: [craft/ROUTER.md](craft/ROUTER.md) is how to decide what to make (the order of work and
reading notes); [craft/floor.md](craft/floor.md) is read right before every edit; `craft/modes/` says what a pitch,
an explain, a story, a game or a tool has to do; `craft/verbs/` has one file per move a note asks for;
[craft/rubric.md](craft/rubric.md) is how a critique is judged and ranked.

## 2. The workspace and its projects — HEADLESS
<!-- sources: apps/workspace/src -->

Work lives in a workspace: a git repo under raea.root (`git config --global raea.root`; unset, `~/Studio` where
workspaces already are, else `~/Documents/raea`, or `~/raea` when iCloud keeps Documents), one per studio or client,
holding projects and controllers. In the raea app a project shows as a channel.
- `raea workspace init NAME` makes one; `raea workspace adopt DIR` makes an existing folder one. `raea workspace`
  shows it (`--json` for the projects and their paths).
- `raea project new NAME` adds a project: its folder with `brief.ts`, `AGENTS.md`, `compositions/`, `components/`,
  `controllers/`, `assets/`, `artifacts/` and `out/`. The workspace's `shared/` has the same five folders, which any
  project imports from as `@shared/components/NAME`. A project can live inline or as its own repo
  (`raea project split NAME`, `raea project join NAME`); both keep its history.
- Work in the project's folder. Footage and other media go in `assets/` (`media/` in a project made before the
  layout), renders in `out/`.

## 3. Read before you make — HEADLESS
<!-- sources: engine/cli/src/guide.rs apps/workspace/src core/brief/src -->

- `raea context .` in the project prints everything to read first, in order: the person's taste
  (`~/.raea/taste/taste.ts`; a line there beats any guide's default), the workspace's taste, the brief, the look, the
  workspace's controllers, the craft floor and each of the brief's modes' guides. Read all of it.
- Run it once a session. If it refuses, say so in one line ("raea context failed: its message; reading the brief and
  controllers directly") and read `brief.ts`, any `*.script.ts`, `~/.raea/taste/taste.ts` and `raea controller ls`
  yourself. A `CONTEXT_STALE` line means `raea doctor` finds files from another version: run `raea doctor --fix`.
- With no request in hand, `raea next` lists the two or three useful next steps from the brief, the compositions,
  the renders and their checks. Offer them; never run one unasked.
- The controllers (`raea controller ls`, `raea controller get PATH`) are the workspace's settings and workflows:
  delivery specs, who reviews what, the tools every agent gets. Work to them. Change one only when the person asks:
  `raea controller set PATH VALUE` (each change is a commit).
- A controller is not a feed item. A feed item is one piece of work (a render, a still, a question): the person
  reviews it once and a note on it is answered by its next version. A controller is a standing decision every agent
  reads before it starts, so changing it changes all the work after. If the person would say it again on the next
  piece ("always 9:16", "Grade checks every cut"), it belongs in a controller; if it's about this piece only, it's a
  note. When the work needs such a decision from the person, put the controller in front of them with the feed's
  `controller_post` (its id, the fields as group.field, a line on what you need decided) rather than asking in prose;
  a controller you make with `controller_write` reaches their feed on its own. Fields are typed (toggle, choice,
  number, text, list, agents, channels, workflow, servers, skills, rule; reference/files.md), so put what they'll
  adjust in fields, one controller per concern.
- A `rule` field is a line every piece is held to and the check that holds it: one of raea's by name with its values,
  or a `.ts` check written with `raea/check` (craft/ROUTER.md, step 7). `raea check PROJECT` runs every rule that
  applies, with raea's floor and the person's taste, and says what waits for a render.
- If the brief isn't shaped (no `believe`, no `mode`), shape it before making anything: ask who it's for and the one
  thing they should believe, or write your best guess and add its field to the brief's `assumed` list.
- For a pitch, an explain or a story, plan first: write the deliverable's storyboard as `NAME.script.ts` beside the
  brief (`export default script({...})` from "raea/brief": scenes of beats, what's on screen and what each scene must
  land; its fields are in reference/files.md), name it on the deliverable, and add a task "storyboard approved" tagged `gate`. `raea spec NAME.script.ts`
  checks it. Render nothing until the person approves it (PERSON).
- Show a plan as what it will be, in this order: previz (a rough, fast raea render of the blocking, timing and
  camera: grey shapes, placeholder type, no polish; it is the plan, not the piece, so the gate allows it), else a
  storyboard (key frames as one `feed_post` look with `files` in order), else the script itself (`feed_post` read
  with its `NAME.script.ts`: the feed shows it as a screenplay and as an A/V table, timed from each beat's `seconds`).
  People judge a picture faster than a description. A whiteboard maps how ideas, options and references connect; it
  isn't the plan.
- The person's footage and files: `raea library search "WORDS"` finds them by meaning across the libraries they've
  indexed (HEADLESS once indexed; adding a folder waits for the person's yes, PERSON).
- Right before any edit to a composition, even a one-line change, read the floor: `raea guide craft`. Read
  `raea guide router` once for the order of work.

## 4. Make an item — HEADLESS
<!-- sources: sdk/raea/src/index.tsx sdk/raea/src/3d.tsx apps/direction/src/findings.rs apps/fingerprint/src systems/fingerprint-things/src -->

One `.tsx` file whose root registers compositions (`raea init` in a footage project writes the files to start from):

```tsx
import { AbsoluteFill, Composition, Sequence, interpolate, registerRoot, useCurrentFrame } from "raea";

function Card({ text }: { text: string }) {
  const f = useCurrentFrame();
  const opacity = interpolate(f, [0, 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ background: "#000", color: "#fff", justifyContent: "center", alignItems: "center", fontSize: 96 }}><span style={{ opacity }}>{text}</span></AbsoluteFill>;
}

registerRoot(() => (
  <Composition id="piece" width={1080} height={1920} fps={30} durationInFrames={90} component={() => (
    <><Sequence from={0} durationInFrames={45}><Card text="One" /></Sequence><Sequence from={45} durationInFrames={45}><Card text="Two" /></Sequence></>
  )} />
));
```

Rules that keep renders right (`raea guide motion` has all ten, under "The core rules"; every file needs these):
- **Frame-pure.** Everything that moves reads `useCurrentFrame()`; `useState`, `useEffect` and timers don't animate a
  render. `Math.random()` is seeded per frame, so seed what should hold still from an index.
- **Clamp every interpolate.** Do it unless you mean the line to run on past its ends.
- **Cue on words, not on guessed frames.** `word("phrase")` is the frame where it's said, so cues follow the cut.
- Footage: `<Video>` and `<Audio>`. Games: `useGameState(initial, step)` with a pure `step`, keys from `useInput()`.
- Brand: the kit's `--brand-*` variables in `brand/brand.css` (`raea brand DOMAIN` reads them from a site), then
  `import { css } from "./styles.gen"` and Tailwind classes like `bg-brand-bg`.
- 3D: read [3d.md](3d.md) first; it routes to one file per topic in `3d/`. An asset to fix first (scale, pivot, FBX
  to .glb) goes through Blender (`raea setup blender`, then [3d/blender.md](3d/blender.md)); a step can be TypeScript
  (`raea/blender`). A Godot project is scripted from TypeScript too (`raea setup godot`, then [3d/godot.md](3d/godot.md)).
- Sound: `raea guide sound` and `raea guide music`; to cut to a song, run `raea song FILE --plot FILE.song.png` and
  time cuts from its map, never a constant BPM. npm packages and React apps: `raea guide apps`.
- Generated media: `raea guide gen` before the first `raea gen`.

`raea check --quick piece.tsx` checks three stills' text (clipped, cramped, safe areas) in about a second: run it
after each save when no hook does. Then render, and look before you call it done:

```sh
raea render piece.tsx --at 0,45,89 -o frames/                 # stills to look at: text fits, nothing overlaps
raea render piece.tsx --alpha -o frames/                     # transparent PNGs, for an overlay in another editor
raea render piece.tsx -o out/piece.mp4 --manifest out/render.json
raea check out/piece.mp4 --manifest out/render.json --taste ~/.raea/taste/taste.ts -o out/piece.check.json   # P0-P3; exits 1 on a P0 or P1
raea findings --open                                          # what still stands, from every render and check so far
```

In a project, every render and check is kept in its record (`.raea/record/`), so `raea findings` tells you where the
piece stands without rereading old check files: for each thing rendered or checked, what its last run fixed, what is
new and what it carries (and since which render). `--open` keeps only what stands, `--about NAME` one part,
`--check ID` one check, `--since RENDER` sets it against an earlier run, and `--json` is for a script. Read it before
you fix and after each render; say what it lists rather than "looks good". A render with an error exits 1; when the
person accepts one, `raea render ... --despite CHECK "why"` lets it through, and findings lists what was let through.

Before you post a cut, score it with the person's fingerprint, what raea has learned of their eye on this machine
from their notes, marks and approvals: `raea fingerprint score out/piece.mp4` lists the moments it expects a note on,
each named in the person's own words, beside raea check's findings. On a picture axis that has learned where, a moment
also says where in the frame and, on a render with a layer pass, the layers there ("top right on Floor"): start the fix
with that layer. Fix each gating moment, or say why you didn't, and
score the fix against the cut before: `raea fingerprint score out/v2.mp4 --was out/v1.mp4` says whether each flag is
fixed, still there, or looks disguised (nearer the axis's disguised defects than clean work, so the fix hid the defect
rather than removing its cause); only a fixed flag is fixed. `raea fingerprint which out/piece.mp4` names the fingerprint that judges this piece (the
project's, the workspace's, then the person's own) and why. Tell the person the axis and the moment, never a score. [fingerprint.md](fingerprint.md) has the rest: reading a
note's box on the sound, teaching the fingerprint, and keeping one with a project.
`raea fingerprint report` says what each axis has learned and what it can't judge yet. A fingerprint's axes are
~/.raea/fingerprints/NAME/fingerprint.ts, typed by `raea/fingerprint`: add, remove or reword an axis there, never its
evidence. A script or brief scores on text axes only, and raea's own axes read pictures and sound, so a script scores
only once the person has added an axis that reads text.

For a 3D shot, check how its things sit and move. Render it with `--layers`, and render `--aov -o out/shot.aov` beside
it. Then run `raea fingerprint things out/shot.mp4 --json > things.json` and
`raea check out/shot.mp4 --things things.json`. It finds a thing floating or passing through another, the camera
lurching mid-move, and an empty frame. When the person says a project is finished,
`raea fingerprint postmortem PROJECT` asks them at most ten yes/no questions in the app about what the fingerprint is
least sure of. Once they've answered, `--tally` makes the answers evidence.

`raea guide rendering` covers stills, the check, bitrate and quality; `raea guide rubric` covers judging the rest.

## 5. Show it and read the notes — PAGE, PERSON
<!-- sources: skills/skills/raea/reference/feed.md -->

- In the raea app, post the render to the project's feed with `feed_post` (a watch, look, listen or play item); the
  person watches, plays and leaves notes on it there (PERSON). `feed_items` reads the items and their notes.
- Outside the app (a session in a terminal: Claude Code, Codex, Gemini CLI, Kimi Code, any harness), `raea show` does
  what `feed_post` does: `raea show FILE...` puts stills (several make a storyboard), a video, a sound, a
  `NAME.script.ts` or `.md`, or a `.tsx` artifact in the project's feed as an item the person can use. Name the project
  as `--project WORKSPACE/ID` (an id from `raea workspace --json`, or the person's Copy reference line pasted whole),
  never its title: raea refuses a title when your folder is in another project or two projects share it. Check that
  the place it prints (`item ID, project ID in WORKSPACE`) is the one you meant. It lands
  quietly, with a notice, and the window stays where the person is (they may be working); `--open` brings the window
  up on it only when they're waiting on it. Ask everything you need at once, as one item: every question in it, and
  each choice with what it is to play or read while answering (`--preview FILE` after a `--choice` is that choice's;
  after the `--question`, before its choices, the question's own, such as the script it asks about):
  `raea show --title "Orientation: three picks" --question "Which narrator?" --choice Henry --preview henry.mp3
  --choice Measured --preview measured.mp3 --question "Graybox the script?" --preview film.script.ts --choice Yes
  --choice "Not yet"`. Put the choice you suggest first. Never post each option, sample or question as its own item.
  While the raea app is installed, never open a render, a still, a contact sheet or a question in Preview or a
  browser: show it. raea's hook (`raea skills install --agent A` adds it
  to any of them) stops such an open once and names the `raea show` command; run the same command again only when the
  person asked for the viewer. What the person sends on it (notes, edits, picks, answers, an artifact's `app.result`)
  comes back as JSON lines in the inbox file `raea show` prints. raea's hook hands each new line to you after your
  next tool call and keeps your turn from ending until you have it (where there is no hook, follow the file with
  `tail -n0 -F FILE` or your harness's monitor). Answer each: it may change what you're doing. Without the app,
  `raea show` opens the file in the Mac's own viewer and says so; take the person's notes as text then.
- When you need the person to choose or fill something in (pick an opening, rank cuts, set a price), post an artifact:
  a React `.tsx` of your own, `feed_post` with `type: "artifact"`, the file, and an `ask` line. The app builds it and
  runs it sandboxed in the feed. Its default export is the component. It imports `react`, `@raea/app` and its own
  files, nothing else (no fetch, no other packages). Tailwind classes use the feed's tokens (`bg-ground`, `text-ink`,
  `text-ink-3`, `border-line`, `bg-accent`). Saving the file updates the open artifact in place, and a file that
  doesn't compile shows its file and line there.

  ```tsx
  import { useState } from "react"
  import { app, useItem } from "@raea/app"

  const CUTS = ["15 s, hook first", "30 s, product last", "6 s bumper"]

  export default function PickCut() {
    const item = useItem() // { title, ask, status, answered, preview, media }
    const [sent, setSent] = useState(false)
    if (!item) return null
    return (
      <main className="p-8 text-ink">
        <h1 className="text-lg font-semibold">{item.ask}</h1>
        <div className="mt-4 grid gap-2">
          {CUTS.map((c) => (
            <button key={c} disabled={sent || item.answered} className="rounded-lg border border-line p-3 text-left hover:bg-accent/10"
              onClick={() => app.result(`Picked: ${c}`).then(() => setSent(true))}>{c}</button>
          ))}
        </div>
      </main>
    )
  }
  ```

  `app.result(text)` comes back to you as the person's next message; `app.comment(text, { x, y })` leaves a note on
  the item, pinned to a point (0 to 1 across and down). Any other call is refused, naming it. On a card the artifact
  is a preview that reads only; it acts once the person opens it.
- Every note, from the feed or as text, gets a move before any edit: pick the one it asks for (quieter, bolder,
  distill, clarify, retime, recut, regrade, remix, harden, layout, typeset, animate, delight, adapt, optimize, extract,
  generate, polish, critique) on the part or moment it names, and read it (`craft/verbs/MOVE.md`, or `raea guide MOVE`)
  before you touch the composition. Answer in their words, and never name the move to them.

## 6. The next version — HEADLESS, then PAGE
<!-- sources: skills/skills/raea/reference/feed.md -->

- Change the composition under the person's hand edits (the `edit` segments and `<Nudge>` props the app writes; see
  `raea guide rendering`), render again and check again.
- Render each version to a new file beside the old (`piece-v2.mp4`), never over it: the earlier version stays
  watchable. In the app, post it with `feed_post` naming the item it `replaces` (outside it, `raea show --replaces
  ITEM FILE`), so the feed keeps both as versions.
- The person's edits are tasks they watch, each with an id (in your turn's prompt in the app; in the inbox line's
  `comments` outside it). Mark each working as you start it and done when it's settled: in the app, `comment_task`,
  or `feed_post` with `answers` naming the comments the version settles; outside it, `raea show --on ITEM --working
  ID` and `--done ID [--note LINE]`, or `raea show FILE --replaces ITEM --done ID...`. When subagents split them, name
  the one on each (`sub`, `--sub NAME`). Done stays in view until the person resolves it; Not done sends it back as a
  new edit.

## 7. Deliver — HEADLESS
<!-- sources: runtime/export/src -->

- The delivered file: `--quality master` for motion graphics and type, `--quality high` for a film. A version made
  for notes takes no `--quality` flag (a fifth of the bytes for the same picture: `raea guide rendering`). Name files
  with lowercase letters, digits and hyphens only (`spring-launch-9x16.mp4`).
- A render is a standard MP4 but large: H.264 High and AAC on a Mac (VideoToolbox), H.264 Constrained Baseline and
  Opus on Windows and Linux (openh264), yuv420p on all. Hand over a share copy too, which any player takes:
  `ffmpeg -i film.mp4 -c:v libx264 -preset slow -crf 23 -maxrate 2600k -bufsize 5200k -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart film-share.mp4`.
- Deliver to the controllers' specs (sizes, platforms, loudness) when the workspace sets them; each network's shapes,
  lengths and UI zones are in [reference/platforms.md](reference/platforms.md), and [delivery.md](delivery.md) routes
  the rest (one composition per shape, cutdowns, tags, handing over).

## Apps: web or native — HEADLESS
<!-- sources: apps/targets/src sdk/ui/src/app.ts sdk/rune/src -->

An app is a React file with a default export: DOM elements, inline `style` or Tailwind `className`, on @raea/ui. One
setting picks the host that draws it. Both are desktop windows that draw every pixel themselves (neither uses the
OS's widgets or a browser), with the same kind of text and layout engines. **web** (the default) is Blitz on Bevy: a
browser engine, so all of CSS (grid included), web npm UI packages and the 3D world. **native** is Rune, an app UI
framework: springs on every change, GPU effects and kit components, a screen-reader tree (AccessKit), a ~27 MB host
against web's ~175 MB, a subset of CSS (no grid) and no 3D yet. The SDK is the same; only the setting differs. Pick
native for a small, motion-heavy app with no 3D that passes its check; anything else stays on web. A composition or a
game stays a composition; an app is an application's interface.

- Say the target in the app's own file, as a literal (anything else is refused at its line):
  `export const app = { target: "native", title: "Notes", size: [480, 640], minSize: [360, 480] };`. With no
  `app` export, or no `target` in it, the target is `"web"`. `--target web|native` on the command line overrides it.
- The verbs, the same on both targets: `raea app run app.tsx` opens it in a window; `raea app check app.tsx` runs it
  headless; `raea app bundle app.tsx -o Notes.app` makes a Mac app. `raea app bundle` signs ad hoc unless you give
  `--identity "Developer ID Application: ..."` (or RAEA_SIGN_IDENTITY) and `--notarize PROFILE` (a notarytool
  keychain profile): it always signs with your own identity, never raea's.
- Check before you show it. Give the app its input as `export const steps = [{ press: "add" }, { type: "Ada", into: "name" }, { key: "Tab" }, { wheel: "list", dy: 120 }, { frames: 30 }];`
  (elements by `data-testid`), or as `--script steps.json`. `raea app check app.tsx --png out/` writes a PNG after
  the mount and after each step (00-mount.png, 01-press-add.png, ...) and tree.json (each element's role, label,
  text and box). Read the PNGs. Check on both targets when the app should run on both: `--target web` and
  `--target native`.
- What the check holds each target to. **native** fails on any prop Rune doesn't map or call its host doesn't
  answer, naming each with its element's path (unmapped.json, unanswered.json). Change the prop, or keep the app on
  web. **web** passes when it draws, and says what native wouldn't draw and which Rune props it ignores.
- Native draws flex layout (no grid), sizes, padding, margin, gap, absolute insets, scroll, colours and gradients,
  borders, radius, shadows and rings, outlines, opacity, transforms and transitions, text, images and video, fonts
  from the app's folder, and Tailwind's classes with hover:, focus:, focus-visible:, active:, disabled:, dark: and
  sm: to 2xl:. Anything else is reported, never dropped. An empty unmapped.json means the page maps whole.
- What only Rune does is typed props from `@raea/rune`:
  `<div {...rune({ motion: "pop", transition: { effect: { push: "top" }, enter: "pop" } })}>`, plus `lead`,
  `instant`, `blur`, `backdropBlur` and `glass`, and its `Badge`, `Spinner`, `Progress`, `RollingText` and
  `Switch`. On web, a preset motion becomes a CSS transition and an entrance a keyframe, blur and glass become filters,
  and the rest is ignored and listed by the check. Without these props an element lands at once, as in a browser.
- Part of a web page can be Rune's: `<RuneLayer className="w-80 h-48">...</RuneLayer>` from `@raea/rune` draws its
  children with Rune, on the GPU, in its box, and the rest of the page stays Blitz's. Give it a size: the layer is
  its content box. Clicks and wheel reach its elements, and their handlers run as anywhere else. A
  `getBoundingClientRect` inside one is zero, and keys don't reach a field in one yet. In a browser it's a plain
  div. `RAEA_RUNE_LAYERS=0` draws it with Blitz.
- Host calls (`call` and `callSync` from `@raea/ui/wire`), answered on both targets: `net.fetch`, `net.ws.*`,
  `net.storage.*`, `net.clipboard.*`, `os.open` (http, https, mailto), `fs.pick`, `fs.save`, `fs.read`, `fs.write`
  and `dialog.message`. Headless, a step answers a dialog: `{ pick: ["a.txt"] }`, `{ save: "out.txt" }`,
  `{ dialog: 0 }`. `world.*` (BRP on the 3D world) is web's only: native refuses it with "no world on the native
  target".
- Examples ship with raea and pass the check on both targets: `sdk/rune/examples/signin.tsx` (Tailwind only) and
  `sdk/rune/examples/motion.tsx` (Rune's props). On a native app, `raea app check --video out/app.mp4 [--audio
  music.wav]` films it on the virtual clock at 60 fps, with a cursor gliding to each element it presses. The same app
  and steps give the same frames.

## Go further

- The guides: the routers above, or `raea guide` (it lists them; `raea guide NAME` prints one, the same text as the copy here).
- The SDK's behaviour: `sdk/raea/spec/motion.feature`; what 3D reaches: `raea guide coverage`.
